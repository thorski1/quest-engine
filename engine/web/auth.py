"""
auth.py — User authentication and session management for quest-engine web mode.

Cookie-based sessions backed by Postgres. Supports:
- Registration (username + password)
- Login / logout
- Session cookies (httponly, secure)
- Anonymous play (upgradeable to account)
"""

from __future__ import annotations

import hashlib
import os
import secrets
import time
from typing import Optional

try:
    import bcrypt
    HAS_BCRYPT = True
except ImportError:
    HAS_BCRYPT = False

SESSION_COOKIE = "quest_session"
SESSION_MAX_AGE = 60 * 60 * 24 * 90  # 90 days


def hash_password(password: str) -> str:
    """Hash a password using bcrypt (or SHA-256 fallback)."""
    if HAS_BCRYPT:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    # Fallback: SHA-256 with salt (less secure but works without bcrypt)
    salt = secrets.token_hex(16)
    h = hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()
    return f"sha256:{salt}:{h}"


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hash."""
    if HAS_BCRYPT and hashed.startswith("$2"):
        return bcrypt.checkpw(password.encode(), hashed.encode())
    if hashed.startswith("sha256:"):
        _, salt, expected = hashed.split(":", 2)
        h = hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()
        return h == expected
    return False


def create_session_id() -> str:
    """Generate a cryptographically secure session ID."""
    return secrets.token_urlsafe(48)


class AuthManager:
    """Manages user auth against the Postgres store."""

    def __init__(self, store):
        """Store should be a PostgresStore instance."""
        self.store = store

    def register(self, username: str, password: str, display_name: str = "", email: str = "") -> dict:
        """Register a new user. Returns {"ok": True, "user_id": int} or {"ok": False, "error": str}."""
        username = username.strip().lower()
        if len(username) < 3:
            return {"ok": False, "error": "Username must be at least 3 characters"}
        if len(username) > 32:
            return {"ok": False, "error": "Username must be 32 characters or less"}
        if not username.isalnum() and "_" not in username:
            return {"ok": False, "error": "Username can only contain letters, numbers, and underscores"}
        if len(password) < 6:
            return {"ok": False, "error": "Password must be at least 6 characters"}

        existing = self.store.get_user_by_username(username)
        if existing:
            return {"ok": False, "error": "Username already taken"}

        pw_hash = hash_password(password)
        try:
            user_id = self.store.create_user(
                username=username,
                display_name=display_name.strip() or username,
                email=email.strip() or "",
                password_hash=pw_hash,
            )
            return {"ok": True, "user_id": user_id}
        except Exception as e:
            return {"ok": False, "error": "Registration failed. Try a different username."}

    def login(self, username: str, password: str) -> dict:
        """Authenticate user. Returns {"ok": True, "user_id": int, "session_id": str} or error."""
        username = username.strip().lower()
        user = self.store.get_user_by_username(username)
        if not user:
            return {"ok": False, "error": "Invalid username or password"}

        pw_hash = user.get("password_hash", "")
        if not pw_hash or not verify_password(password, pw_hash):
            return {"ok": False, "error": "Invalid username or password"}

        session_id = create_session_id()
        try:
            conn = self.store._get_conn()
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO sessions (id, user_id, expires_at)
                       VALUES (%s, %s, NOW() + make_interval(secs => %s))""",
                    (session_id, user["id"], SESSION_MAX_AGE),
                )
                cur.execute(
                    "UPDATE users SET last_login_at = NOW() WHERE id = %s",
                    (user["id"],),
                )
            conn.commit()
        except Exception:
            if self.store._conn and not self.store._conn.closed:
                self.store._conn.rollback()

        return {"ok": True, "user_id": user["id"], "session_id": session_id, "display_name": user.get("display_name", username)}

    def get_user_from_session(self, session_id: str) -> dict | None:
        """Look up user from session cookie. Returns user dict or None."""
        if not session_id:
            return None
        try:
            conn = self.store._get_conn()
            with conn.cursor() as cur:
                cur.execute(
                    """SELECT u.id, u.username, u.display_name, u.email, u.avatar_url
                       FROM sessions s JOIN users u ON u.id = s.user_id
                       WHERE s.id = %s AND (s.expires_at IS NULL OR s.expires_at > NOW())
                       AND u.is_active = TRUE""",
                    (session_id,),
                )
                row = cur.fetchone()
                conn.commit()
                if row:
                    return {
                        "id": row[0], "username": row[1], "display_name": row[2],
                        "email": row[3], "avatar_url": row[4],
                    }
        except Exception:
            if self.store._conn and not self.store._conn.closed:
                self.store._conn.rollback()
        return None

    def logout(self, session_id: str) -> None:
        """Delete a session."""
        try:
            conn = self.store._get_conn()
            with conn.cursor() as cur:
                cur.execute("DELETE FROM sessions WHERE id = %s", (session_id,))
            conn.commit()
        except Exception:
            if self.store._conn and not self.store._conn.closed:
                self.store._conn.rollback()
