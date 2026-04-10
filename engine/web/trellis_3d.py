"""
trellis_3d.py — 3D avatar generation via Replicate (TRELLIS + FLUX).

Pipeline:
    text prompt → FLUX Schnell (image) → TRELLIS (3D GLB mesh)

TRELLIS is image-conditioned (not text-conditioned), so we first generate
a reference image with FLUX, then feed it to TRELLIS for 3D reconstruction.

Env vars:
    REPLICATE_API_TOKEN — from https://replicate.com/account/api-tokens
"""

import json
import os
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError


# Model versions (pinned for reproducibility)
FLUX_VERSION = "c846a69991daf4c0e5d016514849d14ee5b2e6846ce6b9d6f21369e564cfe51e"
TRELLIS_VERSION = "e8f6c45206993f297372f5436b90350817bd9b4a0d52d2a76df50c1c8afa2b3c"


def is_available() -> bool:
    return bool(os.environ.get("REPLICATE_API_TOKEN"))


# Style prompts enhance the base description
STYLE_PROMPTS = {
    "fantasy": "epic fantasy RPG character, full body portrait, detailed armor and weapons, magical aura, centered on plain gray background, studio lighting, game asset reference sheet",
    "cyberpunk": "cyberpunk character, full body, neon accents, futuristic gear, glowing implants, centered on plain gray background, studio lighting, game asset reference",
    "cute": "chibi cute stylized character, full body, big eyes, vibrant pastel colors, centered on plain gray background, studio lighting, 3D model reference",
    "realistic": "photorealistic character, full body portrait, detailed face and clothing, centered on plain gray background, professional studio lighting, concept art",
    "anime": "anime style character, full body, bright colors, clean lines, dynamic pose, centered on plain gray background, studio lighting",
    "pixel": "low-poly voxel character, full body, retro pixel art aesthetic, blocky features, centered on plain gray background, isometric view",
    "steampunk": "steampunk character, full body, brass gears and copper mechanical parts, Victorian era clothing, centered on plain gray background, studio lighting",
    "dark": "dark gothic character, full body, dramatic shadows, ornate details, brooding expression, centered on plain gray background, cinematic lighting",
}


def _replicate_request(method: str, path: str, payload: dict = None) -> dict:
    """Make an authenticated request to the Replicate API."""
    token = os.environ.get("REPLICATE_API_TOKEN", "")
    url = f"https://api.replicate.com/v1{path}"
    data = json.dumps(payload).encode() if payload else None

    req = Request(url, data=data, method=method)
    req.add_header("Authorization", f"Token {token}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Prefer", "wait=60")  # Replicate will wait up to 60s for completion

    try:
        with urlopen(req, timeout=90) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        try:
            err_body = json.loads(e.read())
            return {"error": err_body.get("detail", str(e))}
        except Exception:
            return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def _poll_prediction(prediction_id: str, max_wait: int = 180) -> dict:
    """Poll a prediction until it completes."""
    start = time.time()
    while time.time() - start < max_wait:
        result = _replicate_request("GET", f"/predictions/{prediction_id}")
        status = result.get("status")
        if status == "succeeded":
            return result
        if status in ("failed", "canceled"):
            return {"error": result.get("error", f"Prediction {status}")}
        time.sleep(2)
    return {"error": "Timeout"}


def generate_image_from_prompt(prompt: str, style: str = "fantasy") -> dict:
    """Step 1: Generate a reference image with FLUX Schnell."""
    enhanced = f"{prompt}, {STYLE_PROMPTS.get(style, STYLE_PROMPTS['fantasy'])}"

    result = _replicate_request("POST", "/predictions", {
        "version": FLUX_VERSION,
        "input": {
            "prompt": enhanced,
            "aspect_ratio": "1:1",
            "num_outputs": 1,
            "output_format": "webp",
            "output_quality": 90,
            "num_inference_steps": 4,
        },
    })

    if "error" in result:
        return {"ok": False, "error": f"FLUX: {result['error']}"}

    # If not completed yet, poll
    if result.get("status") != "succeeded":
        result = _poll_prediction(result.get("id", ""), max_wait=60)
        if "error" in result:
            return {"ok": False, "error": f"FLUX: {result['error']}"}

    output = result.get("output")
    if isinstance(output, list) and output:
        return {"ok": True, "image_url": output[0]}
    if isinstance(output, str):
        return {"ok": True, "image_url": output}
    return {"ok": False, "error": "FLUX returned no output"}


def generate_3d_from_image(image_url: str) -> dict:
    """Step 2: Generate 3D GLB mesh from a reference image with TRELLIS."""
    result = _replicate_request("POST", "/predictions", {
        "version": TRELLIS_VERSION,
        "input": {
            "images": [image_url],
            "texture_size": 1024,
            "mesh_simplify": 0.9,
            "generate_color": True,
            "generate_model": True,
            "generate_normal": False,
            "save_gaussian_ply": False,
            "ss_sampling_steps": 12,
            "slat_sampling_steps": 12,
            "return_no_background": True,
            "ss_guidance_strength": 7.5,
            "slat_guidance_strength": 3.0,
            "randomize_seed": True,
        },
    })

    if "error" in result:
        return {"ok": False, "error": f"TRELLIS: {result['error']}"}

    # TRELLIS takes longer — poll up to 3 minutes
    if result.get("status") != "succeeded":
        result = _poll_prediction(result.get("id", ""), max_wait=180)
        if "error" in result:
            return {"ok": False, "error": f"TRELLIS: {result['error']}"}

    output = result.get("output") or {}
    if isinstance(output, dict):
        return {
            "ok": True,
            "glb_url": output.get("model_file", ""),
            "preview_url": output.get("color_video", output.get("preview_video", "")),
        }
    return {"ok": False, "error": "TRELLIS returned unexpected output"}


def generate_avatar_from_prompt(prompt: str, style: str = "fantasy") -> dict:
    """Full pipeline: text prompt → 3D GLB avatar.

    Returns: {"ok": bool, "glb_url": str, "preview_url": str, "image_url": str, "error": str}
    """
    if not is_available():
        return {"ok": False, "error": "REPLICATE_API_TOKEN not set"}

    # Step 1: Generate reference image
    img = generate_image_from_prompt(prompt, style)
    if not img.get("ok"):
        return img

    # Step 2: Generate 3D from image
    mesh = generate_3d_from_image(img["image_url"])
    if not mesh.get("ok"):
        return {**mesh, "image_url": img["image_url"]}

    return {
        "ok": True,
        "glb_url": mesh["glb_url"],
        "preview_url": mesh.get("preview_url", ""),
        "image_url": img["image_url"],
    }


def generate_avatar_from_image(image_url: str) -> dict:
    """Skip text-to-image; go directly from user-provided image to 3D."""
    if not is_available():
        return {"ok": False, "error": "REPLICATE_API_TOKEN not set"}
    return generate_3d_from_image(image_url)


# ── Preset avatar library (fallback) ─────────────────────────────────────

PRESET_AVATARS = [
    {"id": "wizard", "name": "Wizard", "preview": "🧙", "desc": "Master of arcane knowledge",
     "prompt": "wise old wizard with long white beard, blue robes, magical staff, stars on hat"},
    {"id": "knight", "name": "Knight", "preview": "🛡️", "desc": "Honorable warrior",
     "prompt": "noble knight in shining silver plate armor, red cape, holding sword and shield"},
    {"id": "rogue", "name": "Rogue", "preview": "🥷", "desc": "Shadow operative",
     "prompt": "stealthy rogue assassin in dark leather armor, hood covering face, twin daggers"},
    {"id": "bard", "name": "Bard", "preview": "🎭", "desc": "Charismatic storyteller",
     "prompt": "charismatic bard in colorful medieval clothing, holding a lute, flamboyant pose"},
    {"id": "druid", "name": "Druid", "preview": "🌿", "desc": "Nature guardian",
     "prompt": "forest druid in leaf-covered robes, wooden staff with crystal, vines wrapping around"},
    {"id": "cyborg", "name": "Cyborg", "preview": "🤖", "desc": "Tech-enhanced warrior",
     "prompt": "cyberpunk cyborg warrior with glowing blue neon implants, mechanical arm, tactical gear"},
    {"id": "hacker", "name": "Hacker", "preview": "💻", "desc": "Digital infiltrator",
     "prompt": "cyberpunk hacker with hood, holographic glasses, glowing laptop, neon city background"},
    {"id": "scholar", "name": "Scholar", "preview": "📚", "desc": "Pursuer of wisdom",
     "prompt": "scholar in academic robes, carrying books, round glasses, thoughtful expression"},
    {"id": "ninja", "name": "Ninja", "preview": "🥷", "desc": "Silent assassin",
     "prompt": "Japanese ninja in black shinobi outfit, katana on back, mask covering face"},
    {"id": "mage", "name": "Battle Mage", "preview": "🔮", "desc": "Combat sorcerer",
     "prompt": "powerful battle mage in purple robes with gold trim, floating crystal orb, glowing hands"},
    {"id": "paladin", "name": "Paladin", "preview": "⚔️", "desc": "Holy warrior",
     "prompt": "holy paladin in gold plate armor, white cape, glowing holy warhammer, radiant aura"},
    {"id": "ranger", "name": "Ranger", "preview": "🏹", "desc": "Wilderness tracker",
     "prompt": "forest ranger in green cloak and leather armor, bow and quiver, wolf companion"},
]


def get_preset_avatars() -> list[dict]:
    return PRESET_AVATARS
