"""
server.py — FastAPI web server for quest-engine.

Creates a FastAPI app for a given skill pack. Entry point: serve().

    from engine.web.server import serve
    serve("bash")            # http://localhost:8080, opens browser
    serve("bash", port=9000, open_browser=False)
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

try:
    from fastapi import FastAPI, Request, Form, Response
    from fastapi.responses import HTMLResponse, RedirectResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
except ImportError:
    raise ImportError(
        "Web mode requires FastAPI. Install it with:\n"
        "  pip install 'quest-engine[web]'"
    )

from ..skill_pack import SkillPack, load_skill_pack
from .state import WebGameSession
from .markup import rich_to_html, strip_rich

# ── Template + Static paths ───────────────────────────────────────────────────

_HERE = Path(__file__).parent
_TEMPLATES_DIR = _HERE / "templates"
_STATIC_DIR = _HERE / "static"

# ── Session registry ──────────────────────────────────────────────────────────
# Single-player local: one session per skill pack ID.
_sessions: dict[str, WebGameSession] = {}


def _session(pack_id: str) -> WebGameSession:
    return _sessions[pack_id]


# ── App factory ───────────────────────────────────────────────────────────────

def create_app(skill_pack: SkillPack) -> FastAPI:
    """Build and return a FastAPI app wired to *skill_pack*."""

    pack_id = skill_pack.id

    # Initialise (or reuse) session
    if pack_id not in _sessions:
        _sessions[pack_id] = WebGameSession(skill_pack)
    session = _sessions[pack_id]

    theme = "playful" if skill_pack.kids_mode else "cyberpunk"

    app = FastAPI(title=skill_pack.title, docs_url=None, redoc_url=None)

    templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))
    app.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")

    # ── Jinja2 globals ────────────────────────────────────────────────────────

    templates.env.globals["rich_to_html"] = rich_to_html
    templates.env.globals["strip_rich"] = strip_rich
    templates.env.globals["theme"] = theme
    templates.env.globals["pack"] = skill_pack

    def _ctx(request: Request, **extra) -> dict:
        """Build base template context merged with *extra*."""
        ctx = {
            "request": request,
            "theme": theme,
            "pack": skill_pack,
            **session.stats_context(),
            **extra,
        }
        return ctx

    # ── Routes ────────────────────────────────────────────────────────────────

    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        zones = session.all_zones_context()
        return templates.TemplateResponse(request, "menu.html", _ctx(
            request,
            zones=zones,
            has_progress=session.has_progress(),
            intro_story=rich_to_html(skill_pack.intro_story),
        ))

    @app.post("/new-game", response_class=HTMLResponse)
    async def new_game(
        request: Request,
        player_name: str = Form(default=""),
    ):
        name = player_name.strip() or skill_pack.default_player_name
        session.new_game(name)
        first_zone = skill_pack.zone_order[0]
        return RedirectResponse(f"/zone/{first_zone}/intro", status_code=303)

    @app.post("/continue", response_class=HTMLResponse)
    async def continue_game(request: Request):
        if not session.has_progress():
            return RedirectResponse("/", status_code=303)
        return RedirectResponse("/challenge", status_code=303)

    @app.get("/zone/{zone_id}/intro", response_class=HTMLResponse)
    async def zone_intro(request: Request, zone_id: str):
        zone = skill_pack.get_zone(zone_id)
        if not zone:
            return RedirectResponse("/", status_code=303)
        session.start_zone(zone_id)
        intro_text = skill_pack.zone_intros.get(zone_id, "")
        return templates.TemplateResponse(request, "zone_intro.html", _ctx(
            request,
            zone=zone,
            zone_id=zone_id,
            intro_html=rich_to_html(intro_text) if intro_text else "",
        ))

    @app.get("/challenge", response_class=HTMLResponse)
    async def challenge_page(request: Request):
        challenge = session.get_current_challenge()
        if not challenge:
            # Zone complete — find next zone
            zone_id = session.engine.current_zone
            next_id = session._next_zone_id(zone_id)
            if next_id:
                return RedirectResponse(f"/zone/{next_id}/intro", status_code=303)
            return RedirectResponse("/complete", status_code=303)

        zone = session.get_current_zone()
        num, total = session.challenge_position()
        is_boss = challenge.get("is_boss", False)
        boss_intro = ""
        if is_boss:
            boss_intro = rich_to_html(skill_pack.boss_intros.get(
                session.engine.current_zone, ""
            ))

        ctype = challenge.get("type", "quiz")
        options = challenge.get("options", [])
        # For live challenges in web mode, treat like text-answer quiz
        if ctype == "live":
            ctype = "text"

        return templates.TemplateResponse(request, "challenge.html", _ctx(
            request,
            challenge=challenge,
            challenge_num=num,
            challenge_total=total,
            zone=zone,
            zone_id=session.engine.current_zone,
            ctype=ctype,
            options=options,
            is_boss=is_boss,
            boss_intro=boss_intro,
            prompt_html=rich_to_html(challenge.get("prompt", challenge.get("question", ""))),
            lesson_html=rich_to_html(challenge.get("lesson", "")),
            url=challenge.get("url", ""),
            result=None,
            hint_text=None,
            show_lesson=False,
        ))

    @app.post("/answer", response_class=HTMLResponse)
    async def submit_answer(
        request: Request,
        answer: str = Form(default=""),
    ):
        if not answer.strip():
            return RedirectResponse("/challenge", status_code=303)

        challenge = session.get_current_challenge()
        if not challenge:
            return RedirectResponse("/challenge", status_code=303)

        result = session.submit_answer(answer.strip())
        zone = session.get_current_zone()
        num, total = session.challenge_position()
        ctype = challenge.get("type", "quiz")
        if ctype == "live":
            ctype = "text"

        # Determine next action context
        next_challenge = session.get_current_challenge() if result.correct else challenge
        next_num, _ = session.challenge_position()

        return templates.TemplateResponse(request, "challenge.html", _ctx(
            request,
            challenge=challenge,
            challenge_num=num if not result.correct else next_num,
            challenge_total=total,
            zone=zone,
            zone_id=session.engine.current_zone,
            ctype=ctype,
            options=challenge.get("options", []),
            is_boss=challenge.get("is_boss", False),
            boss_intro="",
            prompt_html=rich_to_html(challenge.get("prompt", challenge.get("question", ""))),
            lesson_html=rich_to_html(challenge.get("lesson", "")),
            url=challenge.get("url", ""),
            result=result,
            hint_text=None,
            show_lesson=not result.correct,  # auto-show lesson on wrong
            submitted_answer=answer.strip(),
        ))

    @app.post("/hint", response_class=HTMLResponse)
    async def get_hint(request: Request):
        hint_text = session.get_hint()
        challenge = session.get_current_challenge()
        zone = session.get_current_zone()
        num, total = session.challenge_position()
        ctype = challenge.get("type", "quiz") if challenge else "quiz"
        if ctype == "live":
            ctype = "text"

        return templates.TemplateResponse(request, "challenge.html", _ctx(
            request,
            challenge=challenge,
            challenge_num=num,
            challenge_total=total,
            zone=zone,
            zone_id=session.engine.current_zone,
            ctype=ctype,
            options=challenge.get("options", []) if challenge else [],
            is_boss=challenge.get("is_boss", False) if challenge else False,
            boss_intro="",
            prompt_html=rich_to_html(challenge.get("prompt", challenge.get("question", ""))) if challenge else "",
            lesson_html=rich_to_html(challenge.get("lesson", "")) if challenge else "",
            url=challenge.get("url", "") if challenge else "",
            result=None,
            hint_text=hint_text,
            show_lesson=False,
        ))

    @app.post("/skip", response_class=HTMLResponse)
    async def skip_challenge(request: Request):
        session.skip_challenge()
        return RedirectResponse("/challenge", status_code=303)

    @app.post("/bookmark", response_class=HTMLResponse)
    async def toggle_bookmark(request: Request):
        bookmarked = session.toggle_bookmark()
        # Return to challenge page
        return RedirectResponse("/challenge", status_code=303)

    @app.post("/difficulty", response_class=HTMLResponse)
    async def set_difficulty(request: Request, mode: str = Form(default="normal")):
        session.set_difficulty(mode)
        return RedirectResponse("/challenge", status_code=303)

    @app.get("/achievements", response_class=HTMLResponse)
    async def achievements_page(request: Request):
        achievements = session.achievements_context()
        return templates.TemplateResponse(request, "achievements.html", _ctx(
            request,
            achievements=achievements,
        ))

    @app.get("/zones", response_class=HTMLResponse)
    async def zones_page(request: Request):
        zones = session.all_zones_context()
        return templates.TemplateResponse(request, "menu.html", _ctx(
            request,
            zones=zones,
            has_progress=session.has_progress(),
            intro_story="",
        ))

    @app.get("/complete", response_class=HTMLResponse)
    async def pack_complete(request: Request):
        return templates.TemplateResponse(request, "complete.html", _ctx(
            request,
            completed_zones=len(session.engine.completed_zones),
            total_zones=len(skill_pack.zone_order),
        ))

    return app


# ── Entry point ───────────────────────────────────────────────────────────────

def serve(
    pack_name: str,
    *,
    port: int = 8080,
    open_browser: bool = True,
    packs_dir=None,
):
    """Load *pack_name* and start the web server."""
    try:
        import uvicorn
    except ImportError:
        raise ImportError(
            "uvicorn is required for web mode. Install it with:\n"
            "  pip install 'quest-engine[web]'"
        )

    skill_pack = load_skill_pack(pack_name, packs_dir=packs_dir)
    app = create_app(skill_pack)

    if open_browser:
        import threading
        import webbrowser
        import time as _time

        def _open():
            _time.sleep(1.2)
            webbrowser.open(f"http://localhost:{port}")

        threading.Thread(target=_open, daemon=True).start()

    print(f"\n  Quest Engine Web — {skill_pack.title}")
    print(f"  → http://localhost:{port}\n")

    uvicorn.run(app, host="localhost", port=port, log_level="warning")
