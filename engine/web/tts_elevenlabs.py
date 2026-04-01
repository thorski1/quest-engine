"""
tts_elevenlabs.py — ElevenLabs TTS integration for quest-engine.

Premium character voices with much better quality than Google TTS.
Each character gets a unique ElevenLabs voice ID for maximum differentiation.

Env: ELEVENLABS_API_KEY
"""

import hashlib
import os
import re
from pathlib import Path
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import URLError
import json

CACHE_DIR = Path(os.environ.get("QUEST_TTS_CACHE_DIR", "/tmp/quest_tts_cache"))

# ElevenLabs voice IDs — using Sarah (female) and Daniel (male)
# Differentiated by stability/similarity/style settings
VOICE_MAP = {
    # Characters — Sarah for female/bright, Daniel for male/deep
    "puck":     {"voice_id": "EXAVITQu4vr4xnSDxMaL", "stability": 0.3, "similarity": 0.9, "style": 0.8},  # Sarah — expressive, whimsical
    "cipher":   {"voice_id": "onwK4e9ZLuTAKqWW03F9", "stability": 0.7, "similarity": 0.8, "style": 0.3},  # Daniel — steady, intense
    "aria":     {"voice_id": "EXAVITQu4vr4xnSDxMaL", "stability": 0.6, "similarity": 0.7, "style": 0.5},  # Sarah — calm, knowing
    "longlong": {"voice_id": "onwK4e9ZLuTAKqWW03F9", "stability": 0.8, "similarity": 0.6, "style": 0.2},  # Daniel — slow, wise
    "sofia":    {"voice_id": "EXAVITQu4vr4xnSDxMaL", "stability": 0.4, "similarity": 0.85, "style": 0.7},  # Sarah — warm, encouraging
    "sensei":   {"voice_id": "onwK4e9ZLuTAKqWW03F9", "stability": 0.9, "similarity": 0.7, "style": 0.1},  # Daniel — very measured

    # Narrators
    "en-playful":  {"voice_id": "EXAVITQu4vr4xnSDxMaL", "stability": 0.5, "similarity": 0.75, "style": 0.5},
    "en-cyberpunk": {"voice_id": "onwK4e9ZLuTAKqWW03F9", "stability": 0.6, "similarity": 0.75, "style": 0.4},
    "en-neural":   {"voice_id": "EXAVITQu4vr4xnSDxMaL", "stability": 0.55, "similarity": 0.7, "style": 0.4},

    # Default
    "default":  {"voice_id": "EXAVITQu4vr4xnSDxMaL", "stability": 0.5, "similarity": 0.75, "style": 0.5},
}


def is_available() -> bool:
    return bool(os.environ.get("ELEVENLABS_API_KEY"))


def synthesize(text: str, voice_id: str = "default") -> Optional[bytes]:
    """Synthesize text using ElevenLabs API. Returns MP3 bytes or None."""
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    if not api_key or not text or not text.strip():
        return None

    # Strip Rich markup
    clean = re.sub(r'\[/?[^\]]+\]', '', text).strip()
    if not clean:
        return None

    # Check cache
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_key = f"el_{voice_id}_{hashlib.sha256(clean.encode()).hexdigest()[:16]}"
    cache_path = CACHE_DIR / f"{cache_key}.mp3"
    if cache_path.exists():
        return cache_path.read_bytes()

    # Get voice config
    config = VOICE_MAP.get(voice_id, VOICE_MAP["default"])
    el_voice_id = config["voice_id"]

    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{el_voice_id}"
        payload = json.dumps({
            "text": clean[:500],
            "model_id": "eleven_turbo_v2_5",
            "voice_settings": {
                "stability": config.get("stability", 0.5),
                "similarity_boost": config.get("similarity", 0.75),
                "style": config.get("style", 0.5),
                "use_speaker_boost": True,
            }
        }).encode()

        req = Request(url, data=payload, method="POST")
        req.add_header("xi-api-key", api_key)
        req.add_header("Content-Type", "application/json")
        req.add_header("Accept", "audio/mpeg")

        with urlopen(req, timeout=15) as resp:
            audio = resp.read()
            if audio and len(audio) > 100:
                cache_path.write_bytes(audio)
                return audio
    except Exception as e:
        import logging
        logging.getLogger("quest-engine.elevenlabs").warning(f"ElevenLabs synthesis failed: {e}")

    return None
