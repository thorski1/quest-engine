"""
email.py — Email notifications for quest-engine.

Sends welcome emails on registration and progress reports.
Uses Resend API (free tier: 100/day, 3000/month).

Env: RESEND_API_KEY
"""

import json
import os
from typing import Optional
from urllib.request import Request, urlopen


def is_available() -> bool:
    return bool(os.environ.get("RESEND_API_KEY"))


def send_welcome_email(to_email: str, display_name: str, game_name: str) -> bool:
    """Send a welcome email after registration."""
    api_key = os.environ.get("RESEND_API_KEY", "")
    if not api_key or not to_email:
        return False

    html = f"""
    <div style="font-family:-apple-system,system-ui,sans-serif;max-width:500px;margin:0 auto;padding:2rem;">
      <h1 style="color:#00e5a0;font-size:1.5rem;">Welcome to {game_name}! 🎉</h1>
      <p style="color:#333;line-height:1.6;">
        Hey {display_name},<br><br>
        Your account is ready. Here's what awaits you:
      </p>
      <ul style="color:#333;line-height:1.8;">
        <li>📚 Dozens of chapters to explore</li>
        <li>⚡ Daily challenges with 2x XP bonus</li>
        <li>🏆 Achievements and leaderboards</li>
        <li>🔊 Listen to questions with AI voices</li>
        <li>🤖 AI tutor explains wrong answers</li>
      </ul>
      <p style="color:#333;">
        <a href="https://primer-ecru.vercel.app" style="color:#00e5a0;font-weight:bold;">Start playing now →</a>
      </p>
      <p style="color:#999;font-size:0.8rem;margin-top:2rem;">
        Powered by Quest Engine · <a href="https://quest-roadmap.vercel.app" style="color:#999;">Roadmap</a>
      </p>
    </div>
    """

    try:
        payload = json.dumps({
            "from": "Quest Engine <onboarding@resend.dev>",
            "to": [to_email],
            "subject": f"Welcome to {game_name}! 🎉",
            "html": html,
        }).encode()

        req = Request("https://api.resend.com/emails", data=payload, method="POST")
        req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("Content-Type", "application/json")

        with urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False


def send_progress_report(to_email: str, display_name: str, game_name: str,
                         total_xp: int, level: int, zones_done: int, zones_total: int) -> bool:
    """Send a weekly progress report."""
    api_key = os.environ.get("RESEND_API_KEY", "")
    if not api_key or not to_email:
        return False

    pct = int(zones_done / max(zones_total, 1) * 100)

    html = f"""
    <div style="font-family:-apple-system,system-ui,sans-serif;max-width:500px;margin:0 auto;padding:2rem;">
      <h1 style="color:#00e5a0;font-size:1.5rem;">{display_name}'s Progress Report 📊</h1>
      <p style="color:#333;line-height:1.6;">Here's how things are going in {game_name}:</p>
      <div style="display:flex;gap:1.5rem;margin:1.5rem 0;">
        <div style="text-align:center;">
          <div style="font-size:2rem;font-weight:800;color:#00e5a0;">{total_xp}</div>
          <div style="font-size:0.75rem;color:#999;">Total XP</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:2rem;font-weight:800;color:#00b4d8;">Lv {level}</div>
          <div style="font-size:0.75rem;color:#999;">Level</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:2rem;font-weight:800;color:#ffa500;">{pct}%</div>
          <div style="font-size:0.75rem;color:#999;">Complete</div>
        </div>
      </div>
      <div style="height:8px;background:#eee;border-radius:4px;overflow:hidden;margin:1rem 0;">
        <div style="height:100%;width:{pct}%;background:linear-gradient(90deg,#00e5a0,#00b4d8);border-radius:4px;"></div>
      </div>
      <p style="color:#333;">{zones_done} of {zones_total} zones completed. Keep going! 💪</p>
      <p style="color:#999;font-size:0.8rem;margin-top:2rem;">
        Powered by Quest Engine
      </p>
    </div>
    """

    try:
        payload = json.dumps({
            "from": "Quest Engine <progress@resend.dev>",
            "to": [to_email],
            "subject": f"📊 {display_name}'s Weekly Progress — {game_name}",
            "html": html,
        }).encode()

        req = Request("https://api.resend.com/emails", data=payload, method="POST")
        req.add_header("Authorization", f"Bearer {api_key}")
        req.add_header("Content-Type", "application/json")

        with urlopen(req, timeout=5) as resp:
            return resp.status == 200
    except Exception:
        return False
