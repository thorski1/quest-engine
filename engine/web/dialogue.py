"""
dialogue.py — AI-generated contextual dialogue scripts for zone intros.

Instead of splitting a narrative into paragraphs and interleaving random
canned player responses, we ask Gemini to turn the zone's intro text into
a real back-and-forth teaching dialogue between a specific narrator
character and the player's character.

Gemini is used (not Claude) because the Gemini API key is free and lives
in the same env var the rest of the app uses for image generation.

Results are cached on disk so repeat visits cost zero API calls.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import urllib.request
from pathlib import Path
from typing import Optional

# Cache directory — /tmp is the only reliably writable spot on Vercel.
_CACHE_DIR = Path(os.environ.get("QUEST_DIALOGUE_CACHE", tempfile.gettempdir())) / "quest_dialogue_cache"
try:
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    pass

_MAX_INTRO_CHARS = 2500  # trim very long intros before sending to the API
_GEMINI_MODEL = "gemini-2.5-flash"
_GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{_GEMINI_MODEL}:generateContent"
)


def _strip_rich(text: str) -> str:
    """Remove Rich markup like [bold]...[/bold] from text."""
    return re.sub(r"\[/?[^\]]+\]", "", text or "").strip()


def _cache_key(zone_id: str, character_id: str, player_class: str,
               alignment: str, tone: str, intro_text: str) -> str:
    """Hash of the inputs so content changes bust the cache automatically."""
    payload = "|".join([
        zone_id, character_id, player_class, alignment, tone,
        hashlib.sha256(intro_text.encode()).hexdigest()[:16],
    ])
    return hashlib.sha256(payload.encode()).hexdigest()[:24]


def _cache_path(key: str) -> Path:
    return _CACHE_DIR / f"{key}.json"


def _load_cached(key: str) -> Optional[list[dict]]:
    path = _cache_path(key)
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def _save_cached(key: str, dialogue: list[dict]) -> None:
    try:
        _cache_path(key).write_text(json.dumps(dialogue, ensure_ascii=False))
    except Exception:
        pass


def is_available() -> bool:
    return bool(os.environ.get("GEMINI_API_KEY"))


_CLASS_DESCRIPTIONS = {
    "scholar": "a quiet, bookish student who takes notes, asks precise questions, and loves footnotes",
    "speedrunner": "an impatient, quick-thinking player who wants the short version and is always ready to act",
    "explorer": "a curious wanderer who wants to see every corner, asks about side paths and hidden details",
    "champion": "a confident, bold fighter who is ready to prove themselves and responds with bravado",
}
_ALIGNMENT_DESCRIPTIONS = {
    "hero": "they speak with idealism and warmth, believing learning makes the world better",
    "shadow": "they speak with dark intensity, seeking power through knowledge, suspicious of easy answers",
    "trickster": "they speak with playful mischief, quick jokes, and unexpected angles",
}
_TONE_DESCRIPTIONS = {
    "epic": "the tone is grand, mythic, dramatic — every exchange feels weighty",
    "dark": "the tone is gritty and foreboding, shadowy vocabulary, stakes feel real",
    "funny": "the tone is light and comedic, jokes and wordplay are welcome, keep it playful",
    "chill": "the tone is casual and relaxed, like friends talking over coffee",
}


def _build_prompt(*, character_name: str, character_role: str,
                  player_name: str, player_class: str, alignment: str, tone: str,
                  zone_name: str, intro_text: str) -> str:
    cls_desc = _CLASS_DESCRIPTIONS.get(player_class, "a learner")
    align_desc = _ALIGNMENT_DESCRIPTIONS.get(alignment, "")
    tone_desc = _TONE_DESCRIPTIONS.get(tone, "")

    return (
        f"You are writing a teaching dialogue script for an educational RPG.\n\n"
        f"The zone is called: {zone_name!r}\n"
        f"The narrator is **{character_name}**, {character_role}.\n"
        f"The learner is **{player_name}**, {cls_desc}. {align_desc}\n"
        f"{tone_desc}\n\n"
        f"The learning content for this zone is below. Rewrite it as a natural "
        f"back-and-forth conversation between {character_name} and {player_name}. "
        f"The narrator teaches; the learner asks smart questions, reacts, "
        f"sometimes pushes back, and demonstrates understanding. Every fact in "
        f"the source material must appear somewhere in the dialogue — nothing "
        f"important is dropped. Keep each bubble under 240 characters. Aim for "
        f"8-14 turns total. The learner speaks in character (class + tone).\n\n"
        f"--- SOURCE MATERIAL ---\n"
        f"{intro_text}\n"
        f"--- END SOURCE ---\n\n"
        f"Output ONLY a JSON array (no markdown, no prose around it) where each "
        f'item is {{"speaker": "narrator"|"player", "text": "..."}}. Start with '
        f'the narrator. Do not wrap the array in an object. Example:\n'
        f'[{{"speaker":"narrator","text":"Welcome."}},{{"speaker":"player","text":"Tell me more."}}]\n'
    )


def _call_gemini(prompt: str, timeout: int = 30) -> Optional[list[dict]]:
    api_key = os.environ.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    try:
        payload = json.dumps({
            "contents": [{
                "role": "user",
                "parts": [{"text": prompt}],
            }],
            "generationConfig": {
                "temperature": 0.9,
                "maxOutputTokens": 2048,
                "responseMimeType": "application/json",
            },
        }).encode()
        req = urllib.request.Request(
            f"{_GEMINI_ENDPOINT}?key={api_key}", data=payload, method="POST"
        )
        req.add_header("content-type", "application/json")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
        candidates = data.get("candidates") or []
        if not candidates:
            return None
        parts = candidates[0].get("content", {}).get("parts") or []
        text = "".join(p.get("text", "") for p in parts).strip()
        if not text:
            return None
        # Strip code fences if the model wraps the JSON despite the prompt
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*", "", text)
            text = re.sub(r"\s*```$", "", text)
        parsed = json.loads(text)
        if not isinstance(parsed, list):
            return None
        out = []
        for item in parsed:
            if not isinstance(item, dict):
                continue
            speaker = item.get("speaker")
            body = item.get("text")
            if speaker in ("narrator", "player") and isinstance(body, str) and body.strip():
                out.append({"speaker": speaker, "text": body.strip()})
        return out if len(out) >= 4 else None
    except Exception:
        return None


def generate_dialogue(
    *,
    zone_id: str,
    zone_name: str,
    intro_text: str,
    character_id: str,
    character_name: str,
    character_role: str,
    player_name: str,
    player_class: str,
    alignment: str,
    tone: str,
) -> Optional[list[dict]]:
    """Return a list of dialogue turns or None if generation fails.

    Each turn is {"speaker": "narrator"|"player", "text": str}. Caller is
    responsible for adding expression / speaker_id / speaker_name fields.
    """
    raw = _strip_rich(intro_text)[:_MAX_INTRO_CHARS]
    if not raw:
        return None

    key = _cache_key(zone_id, character_id,
                     player_class or "scholar",
                     alignment or "hero",
                     tone or "epic", raw)
    cached = _load_cached(key)
    if cached:
        return cached

    if not is_available():
        return None

    prompt = _build_prompt(
        character_name=character_name,
        character_role=character_role,
        player_name=player_name or "You",
        player_class=player_class or "scholar",
        alignment=alignment or "hero",
        tone=tone or "epic",
        zone_name=zone_name or zone_id,
        intro_text=raw,
    )
    result = _call_gemini(prompt)
    if result:
        _save_cached(key, result)
    return result
