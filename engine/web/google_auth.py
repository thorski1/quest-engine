"""
google_auth.py — Google OAuth 2.0 for Quest Engine.

One-click Google sign-in. Creates user accounts automatically
on first login. No password needed.

Env vars:
    GOOGLE_CLIENT_ID — from Google Cloud Console
    GOOGLE_CLIENT_SECRET — from Google Cloud Console
    GOOGLE_REDIRECT_URI — callback URL (e.g. https://quest-platform-eight.vercel.app/auth/google/callback)
"""

import json
import os
import secrets
from urllib.parse import urlencode
from urllib.request import Request, urlopen


def is_available() -> bool:
    return bool(os.environ.get("GOOGLE_CLIENT_ID"))


def get_login_url(state: str = "") -> str:
    """Generate Google OAuth login URL."""
    client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "")
    if not state:
        state = secrets.token_urlsafe(32)

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "offline",
        "prompt": "select_account",
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}", state


def exchange_code(code: str) -> dict:
    """Exchange authorization code for tokens and user info."""
    client_id = os.environ.get("GOOGLE_CLIENT_ID", "")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET", "")
    redirect_uri = os.environ.get("GOOGLE_REDIRECT_URI", "")

    # Exchange code for tokens
    token_data = json.dumps({
        "code": code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
    }).encode()

    req = Request("https://oauth2.googleapis.com/token", data=token_data, method="POST")
    req.add_header("Content-Type", "application/json")

    with urlopen(req, timeout=10) as resp:
        tokens = json.loads(resp.read())

    access_token = tokens.get("access_token", "")
    if not access_token:
        return {"ok": False, "error": "No access token received"}

    # Get user info
    req = Request("https://www.googleapis.com/oauth2/v2/userinfo")
    req.add_header("Authorization", f"Bearer {access_token}")

    with urlopen(req, timeout=10) as resp:
        user_info = json.loads(resp.read())

    return {
        "ok": True,
        "email": user_info.get("email", ""),
        "name": user_info.get("name", ""),
        "picture": user_info.get("picture", ""),
        "google_id": user_info.get("id", ""),
    }


def find_or_create_user(store, user_info: dict) -> dict:
    """Find existing user by email or create a new one."""
    email = user_info["email"]
    name = user_info.get("name", email.split("@")[0])

    # Try to find by email
    if hasattr(store, '_get_conn'):
        try:
            conn = store._get_conn()
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, username, display_name, email, avatar_url FROM users WHERE email = %s AND is_active = TRUE",
                    (email,)
                )
                row = cur.fetchone()
                if row:
                    # Update avatar if we have a new one
                    if user_info.get("picture"):
                        cur.execute("UPDATE users SET avatar_url = %s WHERE id = %s", (user_info["picture"], row[0]))
                    return {
                        "id": row[0], "username": row[1],
                        "display_name": row[2], "email": row[3],
                        "avatar_url": user_info.get("picture", row[4] or ""),
                    }

                # Create new user
                username = email.split("@")[0].lower().replace(".", "_")[:20]
                # Ensure unique username
                cur.execute("SELECT COUNT(*) FROM users WHERE username = %s", (username,))
                if cur.fetchone()[0] > 0:
                    username = f"{username}_{secrets.token_hex(3)}"

                import hashlib
                # Use a random password hash (user logs in via Google, not password)
                pw_hash = hashlib.sha256(secrets.token_bytes(32)).hexdigest()

                cur.execute(
                    """INSERT INTO users (username, password_hash, display_name, email, avatar_url, is_active)
                       VALUES (%s, %s, %s, %s, %s, TRUE) RETURNING id""",
                    (username, pw_hash, name, email, user_info.get("picture", ""))
                )
                user_id = cur.fetchone()[0]
                return {
                    "id": user_id, "username": username,
                    "display_name": name, "email": email,
                    "avatar_url": user_info.get("picture", ""),
                }
        except Exception:
            pass

    return {"id": 0, "username": "guest", "display_name": name, "email": email, "avatar_url": ""}
