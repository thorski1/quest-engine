"""
engine/analytics.py — In-game analytics for Quest Engine games.

Uses PostHog to track gameplay events. The same PostHog project key used on
your landing page works here too — giving you cross-channel funnels:
  website visit → install → first game start → zone complete → pack complete

Events tracked:
  game_started           — player opens the game
  zone_started           — player enters a zone
  challenge_completed    — player answers correctly
  challenge_failed       — player answers incorrectly
  hint_used              — player asked for a hint
  challenge_skipped      — player skipped a challenge
  zone_completed         — player finishes all challenges in a zone
  pack_completed         — player completes a full skill pack
  level_up               — player reaches a new level
  difficulty_changed     — player switches difficulty
  daily_challenge_done   — player completes the daily challenge
  bookmark_toggled       — player bookmarks a challenge

Setup:
  1. pip install posthog  (or add to your game's dependencies)
  2. Set POSTHOG_KEY env var (same key as your website)
  3. Optionally set POSTHOG_HOST (defaults to https://us.i.posthog.com)

The analytics module is completely optional — if posthog is not installed or
POSTHOG_KEY is not set, all calls are silent no-ops.

Opt-out: players can set QUEST_NO_ANALYTICS=1 to disable all tracking.
"""

import os
import uuid
from pathlib import Path

# ── State ──────────────────────────────────────────────────────────────────────

_client = None
_distinct_id: str | None = None
_enabled: bool | None = None


def _get_client():
    global _client, _enabled

    if _enabled is None:
        # Respect opt-out env var
        if os.environ.get("QUEST_NO_ANALYTICS"):
            _enabled = False
            return None

        key = os.environ.get("POSTHOG_KEY") or os.environ.get("PUBLIC_POSTHOG_KEY")
        if not key:
            _enabled = False
            return None

        try:
            import posthog as ph
            host = os.environ.get("POSTHOG_HOST", "https://us.i.posthog.com")
            ph.project_api_key = key
            ph.host = host
            # Disable PostHog's own exception capture — don't want game crashes
            # reported as PostHog errors; the game handles its own errors.
            ph.on_error = lambda e, _: None
            _client = ph
            _enabled = True
        except ImportError:
            _enabled = False

    return _client if _enabled else None


def _get_distinct_id() -> str:
    """
    Stable anonymous player ID stored in ~/.quest_engine/player_id.
    Not linked to any personal information.
    """
    global _distinct_id
    if _distinct_id:
        return _distinct_id

    id_file = Path.home() / ".quest_engine" / "player_id"
    try:
        if id_file.exists():
            _distinct_id = id_file.read_text().strip()
        else:
            _distinct_id = str(uuid.uuid4())
            id_file.parent.mkdir(parents=True, exist_ok=True)
            id_file.write_text(_distinct_id)
    except Exception:
        _distinct_id = str(uuid.uuid4())

    return _distinct_id


def capture(event: str, properties: dict | None = None) -> None:
    """
    Send an analytics event. Silently no-ops if analytics is not configured.

    Args:
        event:      Event name (e.g. "zone_completed")
        properties: Optional dict of additional properties
    """
    client = _get_client()
    if not client:
        return
    try:
        client.capture(
            distinct_id=_get_distinct_id(),
            event=event,
            properties=properties or {},
        )
    except Exception:
        pass  # never let analytics break the game


# ── Convenience helpers ────────────────────────────────────────────────────────

def game_started(pack_id: str, is_campaign: bool = False) -> None:
    capture("game_started", {
        "pack_id":     pack_id,
        "is_campaign": is_campaign,
    })


def zone_started(pack_id: str, zone_id: str, zone_name: str) -> None:
    capture("zone_started", {
        "pack_id":   pack_id,
        "zone_id":   zone_id,
        "zone_name": zone_name,
    })


def challenge_completed(pack_id: str, zone_id: str, challenge_id: str,
                        challenge_type: str, xp: int, hints_used: int,
                        seconds: float | None = None) -> None:
    capture("challenge_completed", {
        "pack_id":        pack_id,
        "zone_id":        zone_id,
        "challenge_id":   challenge_id,
        "challenge_type": challenge_type,
        "xp":             xp,
        "hints_used":     hints_used,
        "seconds":        round(seconds, 1) if seconds else None,
    })


def challenge_failed(pack_id: str, zone_id: str, challenge_id: str,
                     challenge_type: str, attempt: int) -> None:
    capture("challenge_failed", {
        "pack_id":        pack_id,
        "zone_id":        zone_id,
        "challenge_id":   challenge_id,
        "challenge_type": challenge_type,
        "attempt":        attempt,
    })


def hint_used(pack_id: str, zone_id: str, challenge_id: str, hint_index: int) -> None:
    capture("hint_used", {
        "pack_id":      pack_id,
        "zone_id":      zone_id,
        "challenge_id": challenge_id,
        "hint_index":   hint_index,
    })


def challenge_skipped(pack_id: str, zone_id: str, challenge_id: str) -> None:
    capture("challenge_skipped", {
        "pack_id":      pack_id,
        "zone_id":      zone_id,
        "challenge_id": challenge_id,
    })


def zone_completed(pack_id: str, zone_id: str, stars: int,
                   challenges_total: int, challenges_skipped: int,
                   hints_total: int) -> None:
    capture("zone_completed", {
        "pack_id":             pack_id,
        "zone_id":             zone_id,
        "stars":               stars,
        "challenges_total":    challenges_total,
        "challenges_skipped":  challenges_skipped,
        "hints_total":         hints_total,
    })


def pack_completed(pack_id: str, total_xp: int, grade: str,
                   zones_completed: int) -> None:
    capture("pack_completed", {
        "pack_id":         pack_id,
        "total_xp":        total_xp,
        "grade":           grade,
        "zones_completed": zones_completed,
    })


def level_up(pack_id: str, new_level: int, new_title: str) -> None:
    capture("level_up", {
        "pack_id":    pack_id,
        "new_level":  new_level,
        "new_title":  new_title,
    })


def difficulty_changed(pack_id: str, from_difficulty: str,
                       to_difficulty: str) -> None:
    capture("difficulty_changed", {
        "pack_id":         pack_id,
        "from_difficulty": from_difficulty,
        "to_difficulty":   to_difficulty,
    })


def daily_challenge_done(pack_id: str, challenge_id: str,
                         streak: int) -> None:
    capture("daily_challenge_done", {
        "pack_id":      pack_id,
        "challenge_id": challenge_id,
        "streak":       streak,
    })


def bookmark_toggled(pack_id: str, challenge_id: str, added: bool) -> None:
    capture("bookmark_toggled", {
        "pack_id":      pack_id,
        "challenge_id": challenge_id,
        "added":        added,
    })
