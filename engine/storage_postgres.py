"""
storage_postgres.py — PostgreSQL storage backend for quest-engine.

Requires: psycopg2 or asyncpg
Set QUEST_DATABASE_URL to enable.

Schema supports:
  - User accounts with authentication
  - Per-pack player progress
  - Challenge attempt history (for analytics)
  - Leaderboards via materialized views
  - Session management
"""

import json
import os
from datetime import datetime, timezone
from typing import Optional

from .storage import BaseStore

# Use psycopg2 (sync, widely available) — can swap for asyncpg later
try:
    import psycopg2
    import psycopg2.extras
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False


SCHEMA_SQL = """
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id              SERIAL PRIMARY KEY,
    username        VARCHAR(64) UNIQUE NOT NULL,
    display_name    VARCHAR(128),
    email           VARCHAR(256) UNIQUE,
    password_hash   VARCHAR(256),  -- bcrypt hash, NULL for anonymous
    avatar_url      TEXT,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    last_login_at   TIMESTAMPTZ DEFAULT NOW(),
    is_active       BOOLEAN DEFAULT TRUE
);

-- Sessions (cookie-based auth)
CREATE TABLE IF NOT EXISTS sessions (
    id              VARCHAR(64) PRIMARY KEY,
    user_id         INTEGER REFERENCES users(id) ON DELETE CASCADE,
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    expires_at      TIMESTAMPTZ,
    ip_address      VARCHAR(45),
    user_agent      TEXT
);
CREATE INDEX IF NOT EXISTS idx_sessions_user ON sessions(user_id);

-- Player progress per pack (replaces JSON file)
CREATE TABLE IF NOT EXISTS player_progress (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(id) ON DELETE CASCADE,
    pack_name       VARCHAR(128) NOT NULL,
    game_name       VARCHAR(64),  -- 'primer', 'nexus-quest', 'ai-academy'
    data            JSONB NOT NULL DEFAULT '{}',
    total_xp        INTEGER DEFAULT 0,
    level           INTEGER DEFAULT 1,
    completed_zones INTEGER DEFAULT 0,
    max_streak      INTEGER DEFAULT 0,
    daily_streak    INTEGER DEFAULT 0,
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, pack_name)
);
CREATE INDEX IF NOT EXISTS idx_progress_user ON player_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_progress_pack ON player_progress(pack_name);
CREATE INDEX IF NOT EXISTS idx_progress_xp ON player_progress(total_xp DESC);

-- Challenge attempts (analytics + spaced repetition)
CREATE TABLE IF NOT EXISTS challenge_attempts (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(id) ON DELETE CASCADE,
    pack_name       VARCHAR(128) NOT NULL,
    zone_id         VARCHAR(128) NOT NULL,
    challenge_id    VARCHAR(128) NOT NULL,
    correct         BOOLEAN NOT NULL,
    answer_given    TEXT,
    time_taken_ms   INTEGER,
    hints_used      INTEGER DEFAULT 0,
    difficulty      VARCHAR(16) DEFAULT 'normal',
    attempted_at    TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_attempts_user ON challenge_attempts(user_id, pack_name);
CREATE INDEX IF NOT EXISTS idx_attempts_challenge ON challenge_attempts(challenge_id);
CREATE INDEX IF NOT EXISTS idx_attempts_time ON challenge_attempts(attempted_at DESC);

-- Achievements earned
CREATE TABLE IF NOT EXISTS achievements (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(id) ON DELETE CASCADE,
    pack_name       VARCHAR(128) NOT NULL,
    achievement_id  VARCHAR(128) NOT NULL,
    earned_at       TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, pack_name, achievement_id)
);

-- Daily challenge completions
CREATE TABLE IF NOT EXISTS daily_completions (
    id              SERIAL PRIMARY KEY,
    user_id         INTEGER REFERENCES users(id) ON DELETE CASCADE,
    pack_name       VARCHAR(128) NOT NULL,
    challenge_date  DATE NOT NULL,
    xp_earned       INTEGER DEFAULT 0,
    completed_at    TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, pack_name, challenge_date)
);

-- Leaderboard materialized view (refresh periodically)
CREATE MATERIALIZED VIEW IF NOT EXISTS leaderboard AS
    SELECT
        u.id as user_id,
        u.display_name,
        u.username,
        pp.pack_name,
        pp.game_name,
        pp.total_xp,
        pp.level,
        pp.completed_zones,
        pp.max_streak,
        pp.daily_streak,
        pp.updated_at,
        RANK() OVER (PARTITION BY pp.pack_name ORDER BY pp.total_xp DESC) as xp_rank,
        RANK() OVER (PARTITION BY pp.pack_name ORDER BY pp.max_streak DESC) as streak_rank
    FROM player_progress pp
    JOIN users u ON u.id = pp.user_id
    WHERE u.is_active = TRUE
WITH NO DATA;

CREATE UNIQUE INDEX IF NOT EXISTS idx_leaderboard_pk ON leaderboard(user_id, pack_name);
"""


class PostgresStore(BaseStore):
    """PostgreSQL storage backend with full user account support."""

    def __init__(self, database_url: str):
        if not HAS_POSTGRES:
            raise ImportError("psycopg2 required for PostgreSQL storage. pip install psycopg2-binary")
        self.database_url = database_url
        self._conn = None
        self._init_schema()

    def _get_conn(self):
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(self.database_url)
            self._conn.autocommit = True  # Prevent transaction state leaking between serverless requests
        else:
            # Check connection health
            try:
                with self._conn.cursor() as cur:
                    cur.execute("SELECT 1")
            except Exception:
                try:
                    self._conn.close()
                except Exception:
                    pass
                self._conn = psycopg2.connect(self.database_url)
                self._conn.autocommit = True
        return self._conn

    def _init_schema(self):
        """Create tables if they don't exist."""
        try:
            conn = self._get_conn()
            with conn.cursor() as cur:
                # Execute entire schema as one block — CREATE IF NOT EXISTS is idempotent
                cur.execute(SCHEMA_SQL)
            conn.commit()
        except Exception as e:
            if self._conn and not self._conn.closed:
                self._conn.rollback()
            # Try statement by statement as fallback
            try:
                conn = self._get_conn()
                for stmt in SCHEMA_SQL.split(";"):
                    stmt = stmt.strip()
                    if stmt and not stmt.startswith("--"):
                        try:
                            with conn.cursor() as cur:
                                cur.execute(stmt)
                            conn.commit()
                        except Exception:
                            conn.rollback()
            except Exception as e2:
                print(f"[quest-engine] PostgreSQL schema warning: {e2}")

    # ── BaseStore interface ──────────────────────────────────────────────────

    def load(self, pack_name: str, player_id: str = "default") -> dict | None:
        try:
            conn = self._get_conn()
            user_id = self._resolve_user_id(player_id)
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT data FROM player_progress WHERE pack_name = %s AND user_id = %s",
                    (pack_name, user_id),
                )
                row = cur.fetchone()
                conn.commit()  # close transaction
                if row:
                    return json.loads(row[0]) if isinstance(row[0], str) else row[0]
                return None
        except Exception as e:
            if self._conn and not self._conn.closed:
                self._conn.rollback()
            return None

    def save(self, pack_name: str, player_id: str, data: dict) -> None:
        try:
            conn = self._get_conn()
            user_id = self._resolve_user_id(player_id)
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO player_progress (user_id, pack_name, data, total_xp, level, completed_zones, max_streak, daily_streak, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (user_id, pack_name)
                    DO UPDATE SET data = EXCLUDED.data, total_xp = EXCLUDED.total_xp,
                                  level = EXCLUDED.level, completed_zones = EXCLUDED.completed_zones,
                                  max_streak = EXCLUDED.max_streak, daily_streak = EXCLUDED.daily_streak,
                                  updated_at = NOW()
                """, (
                    user_id, pack_name, json.dumps(data),
                    data.get("total_xp", 0),
                    self._level_from_xp(data.get("total_xp", 0)),
                    len(data.get("completed_zones", [])),
                    data.get("max_streak", 0),
                    data.get("daily_streak", 0),
                ))
            conn.commit()
        except Exception as e:
            if self._conn and not self._conn.closed:
                self._conn.rollback()

    def delete(self, pack_name: str, player_id: str = "default") -> None:
        try:
            conn = self._get_conn()
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM player_progress WHERE pack_name = %s AND user_id = %s",
                    (pack_name, self._resolve_user_id(player_id)),
                )
            conn.commit()
        except Exception:
            if self._conn and not self._conn.closed:
                self._conn.rollback()

    def list_players(self, pack_name: str) -> list[str]:
        try:
            conn = self._get_conn()
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT user_id FROM player_progress WHERE pack_name = %s ORDER BY total_xp DESC",
                    (pack_name,),
                )
                return [str(r[0]) for r in cur.fetchall()]
        except Exception:
            return []

    # ── Extended methods for user accounts ───────────────────────────────────

    def create_user(self, username: str, display_name: str = "", email: str = "", password_hash: str = "") -> int:
        """Create a new user. Returns user ID."""
        try:
            conn = self._get_conn()
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO users (username, display_name, email, password_hash) VALUES (%s, %s, %s, %s) RETURNING id",
                    (username, display_name or username, email or None, password_hash or None),
                )
                user_id = cur.fetchone()[0]
            conn.commit()
            return user_id
        except Exception as e:
            if self._conn and not self._conn.closed:
                self._conn.rollback()
            raise

    def get_user_by_username(self, username: str) -> dict | None:
        try:
            conn = self._get_conn()
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("SELECT * FROM users WHERE username = %s AND is_active = TRUE", (username,))
                row = cur.fetchone()
            conn.commit()  # close transaction
            return dict(row) if row else None
        except Exception:
            if self._conn and not self._conn.closed:
                self._conn.rollback()
            return None

    def record_attempt(self, user_id: int, pack_name: str, zone_id: str,
                       challenge_id: str, correct: bool, answer: str = "",
                       time_ms: int = 0, hints: int = 0, difficulty: str = "normal"):
        """Record a challenge attempt for analytics."""
        try:
            conn = self._get_conn()
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO challenge_attempts
                    (user_id, pack_name, zone_id, challenge_id, correct, answer_given, time_taken_ms, hints_used, difficulty)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, pack_name, zone_id, challenge_id, correct, answer, time_ms, hints, difficulty))
            conn.commit()
        except Exception:
            if self._conn and not self._conn.closed:
                self._conn.rollback()

    def get_leaderboard(self, pack_name: str, limit: int = 20) -> list[dict]:
        """Get leaderboard for a pack."""
        try:
            conn = self._get_conn()
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("""
                    SELECT u.display_name, u.username, pp.total_xp, pp.level,
                           pp.completed_zones, pp.max_streak, pp.daily_streak
                    FROM player_progress pp
                    JOIN users u ON u.id = pp.user_id
                    WHERE pp.pack_name = %s AND u.is_active = TRUE
                    ORDER BY pp.total_xp DESC
                    LIMIT %s
                """, (pack_name, limit))
                return [dict(r) for r in cur.fetchall()]
        except Exception:
            return []

    def get_challenge_analytics(self, pack_name: str, challenge_id: str) -> dict:
        """Get analytics for a specific challenge."""
        try:
            conn = self._get_conn()
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT
                        COUNT(*) as total_attempts,
                        SUM(CASE WHEN correct THEN 1 ELSE 0 END) as correct_count,
                        AVG(time_taken_ms) as avg_time_ms
                    FROM challenge_attempts
                    WHERE pack_name = %s AND challenge_id = %s
                """, (pack_name, challenge_id))
                row = cur.fetchone()
                return {
                    "total_attempts": row[0] or 0,
                    "correct_count": row[1] or 0,
                    "avg_time_ms": int(row[2] or 0),
                    "pass_rate": round((row[1] or 0) / max(row[0] or 1, 1) * 100),
                }
        except Exception:
            return {"total_attempts": 0, "correct_count": 0, "avg_time_ms": 0, "pass_rate": 0}

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _resolve_user_id(self, player_id: str) -> int:
        """Resolve player_id to a numeric user ID. Create anonymous user if needed."""
        try:
            return int(player_id)
        except (ValueError, TypeError):
            # Create or find anonymous user
            user = self.get_user_by_username(player_id)
            if user:
                return user["id"]
            return self.create_user(player_id)

    @staticmethod
    def _level_from_xp(xp: int) -> int:
        level = 1
        while xp >= level * 100:
            xp -= level * 100
            level += 1
        return level
