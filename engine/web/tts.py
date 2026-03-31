"""
tts.py — Text-to-Speech integration for quest-engine.

Supports Google Cloud Text-to-Speech for:
- Narrated zone intros (story text read aloud)
- Challenge question audio
- Pronunciation audio for language packs (Chinese, Japanese, Spanish)

Audio is generated once and cached. Subsequent requests serve the cached file.

Env vars:
  GOOGLE_APPLICATION_CREDENTIALS — path to service account key JSON
  GOOGLE_TTS_CREDENTIALS — base64-encoded key JSON (for Vercel/serverless)
  QUEST_TTS_CACHE_DIR — where to cache audio files (default: /tmp/quest_tts_cache)
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Optional

# Cache directory
CACHE_DIR = Path(os.environ.get("QUEST_TTS_CACHE_DIR", "/tmp/quest_tts_cache"))

# Voice configs — Studio voices (highest quality) with character differentiation
# Each character gets a distinct voice personality
VOICE_CONFIGS = {
    # ── NARRATORS (read questions, lessons) ──────────────────────────
    # Puck — warm, bright, young-sounding (kids game narrator)
    "puck":        {"language_code": "en-US", "name": "en-US-Studio-O", "pitch": 3.0, "rate": 0.95},
    # CIPHER — deep, authoritative, tech (NEXUS Quest narrator)
    "cipher":      {"language_code": "en-US", "name": "en-US-Studio-M", "pitch": -3.0, "rate": 0.98},
    # ARIA — clear, calm, intelligent (AI Academy narrator)
    "aria":        {"language_code": "en-US", "name": "en-US-Studio-Q", "pitch": 0.0, "rate": 1.0},
    # Long Long — warm, wise (Chinese dragon guide)
    "longlong":    {"language_code": "en-US", "name": "en-US-Studio-M", "pitch": -1.0, "rate": 0.92},
    # Sofia — warm, encouraging (Spanish teacher)
    "sofia":       {"language_code": "es-US", "name": "es-US-Studio-B", "pitch": 1.0, "rate": 0.95},
    # Sensei — patient, measured (Japanese teacher)
    "sensei":      {"language_code": "en-US", "name": "en-US-Studio-M", "pitch": -2.0, "rate": 0.88},

    # ── QUESTION/LESSON READERS (neutral, clear) ─────────────────────
    "en-playful":  {"language_code": "en-US", "name": "en-US-Studio-O", "pitch": 1.0, "rate": 0.95},
    "en-cyberpunk": {"language_code": "en-US", "name": "en-US-Studio-M", "pitch": -2.0, "rate": 1.0},
    "en-neural":   {"language_code": "en-US", "name": "en-US-Studio-Q", "pitch": 0.0, "rate": 1.0},

    # ── LANGUAGE-SPECIFIC (native speakers) ──────────────────────────
    "zh":          {"language_code": "cmn-CN", "name": "cmn-CN-Wavenet-A", "pitch": 0.0, "rate": 0.85},
    "zh-slow":     {"language_code": "cmn-CN", "name": "cmn-CN-Wavenet-A", "pitch": 0.0, "rate": 0.7},
    "ja":          {"language_code": "ja-JP", "name": "ja-JP-Wavenet-B", "pitch": 0.0, "rate": 0.85},
    "ja-slow":     {"language_code": "ja-JP", "name": "ja-JP-Wavenet-B", "pitch": 0.0, "rate": 0.7},
    "es":          {"language_code": "es-US", "name": "es-US-Studio-B", "pitch": 0.0, "rate": 0.9},
    "es-slow":     {"language_code": "es-US", "name": "es-US-Studio-B", "pitch": 0.0, "rate": 0.75},

    # ── FALLBACK ─────────────────────────────────────────────────────
    "default":     {"language_code": "en-US", "name": "en-US-Studio-O", "pitch": 0.0, "rate": 1.0},
}


_tts_client = None

def _get_client():
    """Get or create the Google TTS client."""
    global _tts_client
    if _tts_client is not None:
        return _tts_client
    try:
        # Check for base64-encoded credentials (Vercel)
        b64_creds = os.environ.get("GOOGLE_TTS_CREDENTIALS", "")
        if b64_creds:
            creds_json = base64.b64decode(b64_creds).decode()
            creds_path = Path(tempfile.gettempdir()) / "quest_tts_key.json"
            creds_path.write_text(creds_json)
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(creds_path)

        from google.cloud import texttospeech
        _tts_client = texttospeech.TextToSpeechClient()
        return _tts_client
    except ImportError:
        return None
    except Exception as e:
        import logging
        logging.getLogger("quest-engine.tts").warning(f"TTS client init failed: {e}")
        return None


def _cache_key(text: str, voice_id: str) -> str:
    """Generate a deterministic cache key for text + voice combo."""
    h = hashlib.sha256(f"{voice_id}:{text}".encode()).hexdigest()[:16]
    return f"{voice_id}_{h}"


def synthesize(text: str, voice_id: str = "default") -> Optional[bytes]:
    """
    Synthesize text to MP3 audio bytes.
    Returns cached version if available, otherwise generates and caches.
    Returns None if TTS is not configured.
    """
    if not text or not text.strip():
        return None

    # Strip Rich markup
    import re
    clean_text = re.sub(r'\[/?[^\]]+\]', '', text).strip()
    if not clean_text:
        return None

    # Check cache
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    key = _cache_key(clean_text, voice_id)
    cache_path = CACHE_DIR / f"{key}.mp3"

    if cache_path.exists():
        return cache_path.read_bytes()

    # Generate
    client = _get_client()
    if not client:
        return None

    try:
        from google.cloud import texttospeech

        config = VOICE_CONFIGS.get(voice_id, VOICE_CONFIGS["default"])

        synthesis_input = texttospeech.SynthesisInput(text=clean_text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=config["language_code"],
            name=config.get("name", ""),
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=config.get("rate", 1.0),
            pitch=config.get("pitch", 0.0),
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Cache
        cache_path.write_bytes(response.audio_content)
        return response.audio_content

    except Exception:
        return None


def get_voice_for_pack(theme: str, language_hint: str = "") -> str:
    """Determine the best voice ID for a skill pack's question/lesson reader."""
    if language_hint == "zh" or "chinese" in theme.lower():
        return "zh"
    if language_hint == "ja" or "japanese" in theme.lower():
        return "ja"
    if language_hint == "es" or "spanish" in theme.lower():
        return "es"
    if theme == "playful":
        return "en-playful"
    if theme == "cyberpunk":
        return "en-cyberpunk"
    if theme == "neural":
        return "en-neural"
    return "default"


def get_character_voice(text: str, theme: str = "") -> str:
    """Detect character dialogue in text and return the appropriate voice.

    Characters are identified by their speech patterns:
    - Puck: appears in playful theme intros
    - CIPHER: appears in cyberpunk theme intros
    - ARIA: appears in neural theme intros
    - 龙龙/Long Long: appears in medieval theme
    - Sofia: appears in sunset theme
    - Sensei/先生: appears in ocean theme
    """
    text_lower = text.lower()

    if "puck" in text_lower or theme == "playful":
        return "puck"
    if "cipher" in text_lower or theme == "cyberpunk":
        return "cipher"
    if "aria" in text_lower or theme == "neural":
        return "aria"
    if "龙龙" in text or "long long" in text_lower or "lóng" in text_lower or theme == "medieval":
        return "longlong"
    if "sofia" in text_lower or theme == "sunset":
        return "sofia"
    if "sensei" in text_lower or "先生" in text or theme == "ocean":
        return "sensei"

    return "default"


def is_tts_available() -> bool:
    """Check if TTS is configured and available."""
    return bool(
        os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        or os.environ.get("GOOGLE_TTS_CREDENTIALS")
    )
