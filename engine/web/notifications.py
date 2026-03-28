"""
notifications.py — Signup event tracking and webhook notifications.

Logs every new registration to the signup_events Postgres table.
Optionally sends notifications to Slack and/or Discord via webhooks.

Env vars:
  SLACK_WEBHOOK_URL   — Incoming webhook URL for Slack notifications
  DISCORD_WEBHOOK_URL — Incoming webhook URL for Discord notifications
"""

from __future__ import annotations

import json
import logging
import os
import threading
from datetime import datetime, timezone
from typing import Optional
from urllib.request import Request, urlopen
from urllib.error import URLError

logger = logging.getLogger("quest-engine.notifications")

# ── Schema ────────────────────────────────────────────────────────────────────

SIGNUP_EVENTS_SQL = """
CREATE TABLE IF NOT EXISTS signup_events (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER NOT NULL,
    username        VARCHAR(64) NOT NULL,
    display_name    VARCHAR(128),
    game_name       VARCHAR(64),
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_signup_events_time ON signup_events(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_signup_events_game ON signup_events(game_name);
"""


def _ensure_table(conn):
    """Create signup_events table if it doesn't exist."""
    try:
        with conn.cursor() as cur:
            cur.execute(SIGNUP_EVENTS_SQL)
        conn.commit()
    except Exception:
        if conn and not conn.closed:
            conn.rollback()
        # Try statement-by-statement as fallback
        try:
            for stmt in SIGNUP_EVENTS_SQL.split(";"):
                stmt = stmt.strip()
                if stmt and not stmt.startswith("--"):
                    try:
                        with conn.cursor() as cur:
                            cur.execute(stmt)
                        conn.commit()
                    except Exception:
                        conn.rollback()
        except Exception as e:
            logger.warning("Could not create signup_events table: %s", e)


# ── Webhook helpers (fire-and-forget in background thread) ────────────────────

def _post_json(url: str, payload: dict) -> None:
    """POST JSON to a URL. Runs in background — errors are logged, never raised."""
    try:
        data = json.dumps(payload).encode("utf-8")
        req = Request(url, data=data, headers={"Content-Type": "application/json"})
        urlopen(req, timeout=10)
        logger.info("Webhook notification sent to %s", url[:40])
    except (URLError, OSError) as e:
        logger.warning("Webhook failed (%s): %s", url[:40], e)


def _send_slack(username: str, display_name: str, game_name: str, timestamp: str) -> None:
    """Send a signup notification to Slack."""
    url = os.environ.get("SLACK_WEBHOOK_URL", "").strip()
    if not url:
        return
    text = (
        f":tada: *New Signup!*\n"
        f">:bust_in_silhouette: *{display_name}* (`{username}`)\n"
        f">:video_game: Game: *{game_name or 'Unknown'}*\n"
        f">:clock3: {timestamp}"
    )
    threading.Thread(
        target=_post_json,
        args=(url, {"text": text}),
        daemon=True,
    ).start()


def _send_discord(username: str, display_name: str, game_name: str, timestamp: str) -> None:
    """Send a signup notification to Discord."""
    url = os.environ.get("DISCORD_WEBHOOK_URL", "").strip()
    if not url:
        return
    embed = {
        "title": "\U0001f389 New Signup!",
        "color": 0x00E5A0,  # quest-engine green
        "fields": [
            {"name": "\U0001f464 Player", "value": f"**{display_name}** (`{username}`)", "inline": True},
            {"name": "\U0001f3ae Game", "value": game_name or "Unknown", "inline": True},
            {"name": "\U0001f552 Time", "value": timestamp, "inline": False},
        ],
    }
    threading.Thread(
        target=_post_json,
        args=(url, {"embeds": [embed]}),
        daemon=True,
    ).start()


# ── Public API ────────────────────────────────────────────────────────────────

def notify_signup(user_id: int, username: str, display_name: str, game_name: str,
                  store=None) -> bool:
    """
    Record a signup event and fire webhook notifications.

    Args:
        user_id:      Numeric user ID from the users table.
        username:     Login username.
        display_name: Display name chosen at registration.
        game_name:    Which game they signed up for ('nexus-quest', 'primer', etc).
        store:        A PostgresStore instance (uses store._get_conn()).

    Returns True if the DB insert succeeded, False otherwise.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    # 1. Always log to Postgres
    db_ok = False
    if store is not None:
        try:
            conn = store._get_conn()
            _ensure_table(conn)
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO signup_events (user_id, username, display_name, game_name)
                       VALUES (%s, %s, %s, %s)""",
                    (user_id, username, display_name, game_name),
                )
            conn.commit()
            db_ok = True
            logger.info("Signup event recorded: %s (%s) for %s", username, display_name, game_name)
        except Exception as e:
            logger.error("Failed to record signup event: %s", e)
            if store._conn and not store._conn.closed:
                store._conn.rollback()
    else:
        logger.warning("notify_signup called without store — DB insert skipped")

    # 2. Fire webhooks (non-blocking)
    _send_slack(username, display_name, game_name, timestamp)
    _send_discord(username, display_name, game_name, timestamp)

    return db_ok


def get_recent_signups(store, limit: int = 50) -> list[dict]:
    """
    Query the most recent signup events.

    Args:
        store: A PostgresStore instance.
        limit: Max rows to return (default 50).

    Returns a list of dicts with keys: id, user_id, username, display_name, game_name, created_at.
    """
    try:
        conn = store._get_conn()
        _ensure_table(conn)
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, user_id, username, display_name, game_name, created_at
                   FROM signup_events
                   ORDER BY created_at DESC
                   LIMIT %s""",
                (limit,),
            )
            rows = cur.fetchall()
            conn.commit()
            return [
                {
                    "id": r[0],
                    "user_id": r[1],
                    "username": r[2],
                    "display_name": r[3],
                    "game_name": r[4],
                    "created_at": r[5],
                }
                for r in rows
            ]
    except Exception as e:
        logger.error("Failed to query signup events: %s", e)
        if store._conn and not store._conn.closed:
            store._conn.rollback()
        return []


def get_signup_count(store) -> int:
    """Return total number of registered users from the users table."""
    try:
        conn = store._get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM users WHERE is_active = TRUE")
            row = cur.fetchone()
            conn.commit()
            return row[0] if row else 0
    except Exception:
        if store._conn and not store._conn.closed:
            store._conn.rollback()
        return 0
