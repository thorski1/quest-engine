"""
trellis_3d.py — 3D avatar generation via Microsoft TRELLIS.

Uses Hugging Face Inference API to generate 3D avatars from text prompts
or reference images. Returns URLs to GLB mesh files that can be rendered
in the browser with <model-viewer> or three.js.

TRELLIS: https://github.com/microsoft/TRELLIS
HF Space: https://huggingface.co/spaces/Microsoft/TRELLIS

Env vars:
    HUGGINGFACE_TOKEN — HF API token (from https://huggingface.co/settings/tokens)
    REPLICATE_API_TOKEN — Alternative: use Replicate's hosted TRELLIS
"""

import json
import os
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError


def is_available() -> bool:
    """Check if 3D generation is configured."""
    return bool(
        os.environ.get("HUGGINGFACE_TOKEN")
        or os.environ.get("REPLICATE_API_TOKEN")
    )


def generate_avatar_from_prompt(prompt: str, style: str = "fantasy") -> dict:
    """Generate a 3D avatar from a text description.

    Returns: {"ok": bool, "glb_url": str, "preview_url": str, "error": str}
    """
    # Enhance prompt with style
    style_prompts = {
        "fantasy": "epic fantasy RPG character, detailed armor, magical aura, game asset, 3D model",
        "cyberpunk": "cyberpunk hacker with neon accents, futuristic gear, glowing visor, game asset",
        "cute": "cute chibi cartoon character, big eyes, vibrant colors, stylized 3D model",
        "realistic": "photorealistic human character, detailed face, professional attire",
        "anime": "anime style character, bright colors, large eyes, dynamic pose, 3D model",
        "pixel": "pixel art character, retro 8-bit style, voxel 3D model",
    }
    full_prompt = f"{prompt}, {style_prompts.get(style, style_prompts['fantasy'])}"

    # Try Replicate first (easier API)
    if os.environ.get("REPLICATE_API_TOKEN"):
        return _generate_via_replicate(full_prompt)

    # Fallback to Hugging Face Inference API
    if os.environ.get("HUGGINGFACE_TOKEN"):
        return _generate_via_hf(full_prompt)

    return {"ok": False, "error": "No 3D generation API configured"}


def _generate_via_replicate(prompt: str) -> dict:
    """Use Replicate's hosted TRELLIS endpoint."""
    api_token = os.environ.get("REPLICATE_API_TOKEN", "")
    if not api_token:
        return {"ok": False, "error": "REPLICATE_API_TOKEN not set"}

    # Replicate TRELLIS model
    model_version = "firtoz/trellis:e8f6c45206993f297372f5436b90350817bd9b4a0d52d2a76df50c1c8afa2b3c"

    try:
        payload = json.dumps({
            "version": model_version,
            "input": {
                "prompt": prompt,
                "images": [],  # text-to-3D mode
                "slat_sampling_steps": 12,
                "mesh_simplify": 0.9,
                "texture_size": 1024,
            }
        }).encode()

        req = Request("https://api.replicate.com/v1/predictions", data=payload, method="POST")
        req.add_header("Authorization", f"Token {api_token}")
        req.add_header("Content-Type", "application/json")

        with urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())

        prediction_id = data.get("id")
        if not prediction_id:
            return {"ok": False, "error": "No prediction ID returned"}

        # Poll for completion (max 60s)
        status_url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
        for _ in range(60):
            time.sleep(2)
            req = Request(status_url)
            req.add_header("Authorization", f"Token {api_token}")
            with urlopen(req, timeout=10) as resp:
                status_data = json.loads(resp.read())

            status = status_data.get("status")
            if status == "succeeded":
                output = status_data.get("output", {})
                return {
                    "ok": True,
                    "glb_url": output.get("model_file", ""),
                    "preview_url": output.get("preview_video", ""),
                    "prediction_id": prediction_id,
                }
            elif status in ("failed", "canceled"):
                return {"ok": False, "error": status_data.get("error", "Generation failed")}

        return {"ok": False, "error": "Timeout waiting for generation"}

    except HTTPError as e:
        return {"ok": False, "error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _generate_via_hf(prompt: str) -> dict:
    """Use Hugging Face Inference API for TRELLIS."""
    token = os.environ.get("HUGGINGFACE_TOKEN", "")
    if not token:
        return {"ok": False, "error": "HUGGINGFACE_TOKEN not set"}

    # HF Spaces API via Gradio
    # Note: HF Spaces can be slow/unavailable; production should use dedicated inference
    try:
        payload = json.dumps({"inputs": prompt, "parameters": {"style": "3d"}}).encode()
        req = Request(
            "https://api-inference.huggingface.co/models/Microsoft/TRELLIS-text-xlarge",
            data=payload, method="POST",
        )
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Content-Type", "application/json")

        with urlopen(req, timeout=120) as resp:
            data = resp.read()
            # HF returns the GLB bytes directly or a URL
            if resp.headers.get("Content-Type", "").startswith("application/json"):
                result = json.loads(data)
                return {"ok": True, "glb_url": result.get("url", ""), "preview_url": ""}
            else:
                # Raw bytes — would need to save and serve
                return {"ok": False, "error": "HF returned raw bytes (needs file handler)"}

    except HTTPError as e:
        return {"ok": False, "error": f"HF Error {e.code}: {e.reason}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# Preset avatar library (fallback when no API is available)
PRESET_AVATARS = [
    {"id": "wizard", "name": "Wizard", "glb_url": "/static/avatars/wizard.glb", "preview": "🧙", "desc": "Master of arcane knowledge"},
    {"id": "knight", "name": "Knight", "glb_url": "/static/avatars/knight.glb", "preview": "🛡️", "desc": "Honorable warrior"},
    {"id": "rogue", "name": "Rogue", "glb_url": "/static/avatars/rogue.glb", "preview": "🥷", "desc": "Shadow operative"},
    {"id": "bard", "name": "Bard", "glb_url": "/static/avatars/bard.glb", "preview": "🎭", "desc": "Charismatic storyteller"},
    {"id": "druid", "name": "Druid", "glb_url": "/static/avatars/druid.glb", "preview": "🌿", "desc": "Nature guardian"},
    {"id": "cyborg", "name": "Cyborg", "glb_url": "/static/avatars/cyborg.glb", "preview": "🤖", "desc": "Tech-enhanced warrior"},
    {"id": "hacker", "name": "Hacker", "glb_url": "/static/avatars/hacker.glb", "preview": "💻", "desc": "Digital infiltrator"},
    {"id": "scholar", "name": "Scholar", "glb_url": "/static/avatars/scholar.glb", "preview": "📚", "desc": "Pursuer of wisdom"},
]


def get_preset_avatars() -> list[dict]:
    """Get the preset avatar library (always available)."""
    return PRESET_AVATARS
