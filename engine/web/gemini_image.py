"""
gemini_image.py — Free 2D avatar generation via Gemini 2.5 Flash Image (Nano Banana).

Free tier: 500 images/day, ~10/min, 1024x1024.
No credit card required.

Get your API key: https://aistudio.google.com/apikey
Docs: https://ai.google.dev/gemini-api/docs/image-generation

Env vars:
    GEMINI_API_KEY — from Google AI Studio
"""

import base64
import json
import os
from urllib.request import Request, urlopen
from urllib.error import HTTPError


MODEL = "gemini-2.5-flash-image"
API_BASE = "https://generativelanguage.googleapis.com/v1beta/models"


def is_available() -> bool:
    return bool(os.environ.get("GEMINI_API_KEY"))


# Style prompts tailored for RPG/game avatars
STYLE_PROMPTS = {
    "fantasy": "epic fantasy RPG character, full-body portrait, detailed armor, magical aura, game concept art, centered on plain gradient background, studio lighting",
    "cyberpunk": "cyberpunk character, full-body, neon accents, futuristic gear, glowing implants, concept art, centered on dark gradient background",
    "cute": "chibi kawaii character, full body, adorable big eyes, pastel colors, stylized, centered on soft background",
    "realistic": "photorealistic character portrait, full body, detailed face and clothing, professional studio lighting, centered composition",
    "anime": "anime character, full body, vibrant colors, sharp lineart, dynamic pose, centered on clean background",
    "pixel": "pixel art character sprite, retro 16-bit style, full body, vibrant palette, centered on plain background",
    "steampunk": "steampunk character, full body, brass gears, Victorian clothing, mechanical accessories, sepia tones",
    "dark": "dark gothic character, full body, dramatic shadows, brooding expression, ornate details, cinematic lighting",
    "watercolor": "watercolor painting of character, full body, soft brushstrokes, artistic, centered composition",
    "comic": "comic book style character, full body, bold inks, halftone shading, dynamic pose",
}


def generate_image_from_prompt(prompt: str, style: str = "fantasy") -> dict:
    """Generate a 2D character image using Gemini 2.5 Flash Image (free).

    Returns: {"ok": bool, "image_data_url": str (base64), "error": str}
    """
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return {"ok": False, "error": "GEMINI_API_KEY not set"}

    style_suffix = STYLE_PROMPTS.get(style, STYLE_PROMPTS["fantasy"])
    full_prompt = f"{prompt}, {style_suffix}"

    url = f"{API_BASE}/{MODEL}:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{
            "parts": [{"text": full_prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
        }
    }).encode()

    req = Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())

        # Parse response to find inline image data
        candidates = data.get("candidates", [])
        if not candidates:
            return {"ok": False, "error": "No candidates in response"}

        parts = candidates[0].get("content", {}).get("parts", [])
        for part in parts:
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                mime = inline.get("mimeType", "image/png")
                b64 = inline["data"]
                return {
                    "ok": True,
                    "image_data_url": f"data:{mime};base64,{b64}",
                    "prompt": full_prompt,
                }

        return {"ok": False, "error": "No image in response"}

    except HTTPError as e:
        try:
            err = json.loads(e.read())
            msg = err.get("error", {}).get("message", str(e))
        except Exception:
            msg = f"HTTP {e.code}: {e.reason}"
        return {"ok": False, "error": msg}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def edit_image(image_data_url: str, edit_prompt: str) -> dict:
    """Edit an existing image using Gemini (e.g. 'make the armor blue').

    Nano Banana excels at image editing — this lets players iterate on avatars.
    """
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return {"ok": False, "error": "GEMINI_API_KEY not set"}

    # Extract base64 data from data URL
    if image_data_url.startswith("data:"):
        header, b64_data = image_data_url.split(",", 1)
        mime = header.split(";")[0].replace("data:", "") or "image/png"
    else:
        return {"ok": False, "error": "Invalid image data URL"}

    url = f"{API_BASE}/{MODEL}:generateContent?key={api_key}"
    payload = json.dumps({
        "contents": [{
            "parts": [
                {"text": edit_prompt},
                {"inlineData": {"mimeType": mime, "data": b64_data}},
            ]
        }],
        "generationConfig": {"responseModalities": ["IMAGE"]},
    }).encode()

    req = Request(url, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read())

        candidates = data.get("candidates", [])
        if not candidates:
            return {"ok": False, "error": "No candidates"}

        parts = candidates[0].get("content", {}).get("parts", [])
        for part in parts:
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and inline.get("data"):
                out_mime = inline.get("mimeType", "image/png")
                return {
                    "ok": True,
                    "image_data_url": f"data:{out_mime};base64,{inline['data']}",
                }

        return {"ok": False, "error": "No edited image in response"}

    except HTTPError as e:
        try:
            err = json.loads(e.read())
            msg = err.get("error", {}).get("message", str(e))
        except Exception:
            msg = f"HTTP {e.code}"
        return {"ok": False, "error": msg}
    except Exception as e:
        return {"ok": False, "error": str(e)}
