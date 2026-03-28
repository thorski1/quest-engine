"""
hub.py — Multi-pack hub server for quest-engine.

Creates a single FastAPI app serving multiple skill packs, each at /{pack_id}/.
The root / shows a pack chooser. Individual pack routes are at /{pack_id}/challenge, etc.

Usage:
    from engine.web.hub import serve_hub
    serve_hub(["bash", "git", "vim"], packs_dir="/path/to/skill-packs")
"""

from __future__ import annotations
import datetime
import os
from pathlib import Path
from typing import Optional

try:
    from fastapi import FastAPI, Request, Form
    from fastapi.responses import HTMLResponse, RedirectResponse
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
except ImportError:
    raise ImportError("Web mode requires FastAPI. Install it with: pip install 'quest-engine[web]'")

from ..skill_pack import SkillPack, load_skill_pack
from .state import WebGameSession
from .markup import rich_to_html, strip_rich

_HERE = Path(__file__).parent
_TEMPLATES_DIR = _HERE / "templates"
_STATIC_DIR = _HERE / "static"

# Session registry: pack_id -> WebGameSession
_sessions: dict[str, WebGameSession] = {}


def create_hub_app(skill_packs: list[SkillPack]) -> FastAPI:
    """Build a FastAPI app serving multiple skill packs at /{pack_id}/ paths."""

    hub = FastAPI(title="Quest Engine Hub", docs_url=None, redoc_url=None)
    templates = Jinja2Templates(directory=str(_TEMPLATES_DIR))
    hub.mount("/static", StaticFiles(directory=str(_STATIC_DIR)), name="static")

    templates.env.globals["rich_to_html"] = rich_to_html
    templates.env.globals["strip_rich"] = strip_rich

    # Initialize sessions
    for pack in skill_packs:
        if pack.id not in _sessions:
            _sessions[pack.id] = WebGameSession(pack)

    # ── Hub landing page ───────────────────────────────────────────────────────

    @hub.get("/", response_class=HTMLResponse)
    async def hub_index(request: Request):
        pack_cards = []
        for pack in skill_packs:
            session = _sessions[pack.id]
            pack_cards.append({
                "id": pack.id,
                "title": pack.title,
                "subtitle": pack.subtitle,
                "theme": pack.theme or ("playful" if pack.kids_mode else "cyberpunk"),
                "has_progress": session.has_progress(),
                "completed_zones": len(session.engine.completed_zones),
                "total_zones": len(pack.zone_order),
                "total_xp": session.engine.total_xp,
            })
        # Hub theme: use the most common theme among packs
        themes = [p.theme or ("playful" if p.kids_mode else "cyberpunk") for p in skill_packs]
        hub_theme = max(set(themes), key=themes.count)
        total_challenges = sum(
            sum(len(z.get("challenges", [])) for z in p.zones.values())
            for p in skill_packs
        )
        return templates.TemplateResponse(request, "hub.html", {
            "request": request,
            "packs": pack_cards,
            "theme": hub_theme,
            "total_challenges": total_challenges,
        })

    # ── Per-pack routes ────────────────────────────────────────────────────────
    # All routes are duplicated from server.py but with /{pack_id} prefix.
    # We import and call create_app to create per-pack sub-apps, then add the hub routes inline.

    for pack in skill_packs:
        _register_pack_routes(hub, pack, templates)

    return hub


def _register_pack_routes(hub: FastAPI, skill_pack: SkillPack, templates: "Jinja2Templates"):
    """Register all routes for one pack under /{pack_id}/."""
    pack_id = skill_pack.id
    prefix = f"/{pack_id}"
    theme = skill_pack.theme or ("playful" if skill_pack.kids_mode else "cyberpunk")

    def _session() -> WebGameSession:
        return _sessions[pack_id]

    def _ctx(request: Request, **extra) -> dict:
        sess = _session()
        return {
            "request": request,
            "theme": theme,
            "pack": skill_pack,
            "pack_url_prefix": prefix,
            **sess.stats_context(),
            **extra,
        }

    @hub.get(f"{prefix}/", response_class=HTMLResponse)
    async def menu(request: Request, _pid: str = pack_id):
        s = _session()
        # Redirect new players to onboarding
        if not s.has_progress():
            return templates.TemplateResponse(request, "onboarding.html", _ctx(request))
        zones = s.all_zones_context()
        return templates.TemplateResponse(request, "menu.html", _ctx(
            request, zones=zones,
            has_progress=True,
            intro_story=rich_to_html(skill_pack.intro_story),
        ))

    @hub.post(f"{prefix}/new-game", response_class=HTMLResponse)
    async def new_game(request: Request, player_name: str = Form(default=""), _pid: str = pack_id):
        name = player_name.strip() or skill_pack.default_player_name
        _session().new_game(name)
        first_zone = skill_pack.zone_order[0]
        return RedirectResponse(f"{prefix}/zone/{first_zone}/intro", status_code=303)

    @hub.post(f"{prefix}/continue", response_class=HTMLResponse)
    async def continue_game(request: Request, _pid: str = pack_id):
        if not _session().has_progress():
            return RedirectResponse(f"{prefix}/", status_code=303)
        return RedirectResponse(f"{prefix}/challenge", status_code=303)

    @hub.get(f"{prefix}/zone/{{zone_id}}/intro", response_class=HTMLResponse)
    async def zone_intro(request: Request, zone_id: str, _pid: str = pack_id):
        zone = skill_pack.get_zone(zone_id)
        if not zone:
            return RedirectResponse(f"{prefix}/", status_code=303)
        s = _session()
        s.start_zone(zone_id)
        intro_text = skill_pack.zone_intros.get(zone_id, "")
        challenges = zone.get("challenges", [])
        completed = s.engine.completed_challenges.get(zone_id, set())
        zone_xp = sum(c.get("xp", 25) for c in challenges)
        zone_progress = len(completed) if isinstance(completed, set) else len(set(completed))
        zone_status = "complete" if zone_id in s.engine.completed_zones else (
            "in_progress" if zone_progress > 0 else "not_started"
        )
        return templates.TemplateResponse(request, "zone_intro.html", _ctx(
            request, zone=zone, zone_id=zone_id,
            intro_html=rich_to_html(intro_text) if intro_text else "",
            challenge_count=len(challenges),
            zone_xp=zone_xp,
            zone_progress=zone_progress,
            zone_status=zone_status,
        ))

    @hub.get(f"{prefix}/challenge", response_class=HTMLResponse)
    async def challenge_page(request: Request, _pid: str = pack_id):
        s = _session()
        challenge = s.get_current_challenge()
        if not challenge:
            zone_id = s.engine.current_zone
            next_id = s._next_zone_id(zone_id)
            if next_id:
                return RedirectResponse(f"{prefix}/zone/{next_id}/intro", status_code=303)
            return RedirectResponse(f"{prefix}/complete", status_code=303)

        zone = s.get_current_zone()
        num, total = s.challenge_position()
        is_boss = challenge.get("is_boss", False)
        boss_intro = ""
        if is_boss:
            boss_intro = rich_to_html(skill_pack.boss_intros.get(s.engine.current_zone, ""))

        ctype = challenge.get("type", "quiz")
        options = challenge.get("options", [])
        if ctype == "live":
            ctype = "text"

        return templates.TemplateResponse(request, "challenge.html", _ctx(
            request,
            challenge=challenge, challenge_num=num, challenge_total=total,
            zone=zone, zone_id=s.engine.current_zone,
            ctype=ctype, options=options,
            is_boss=is_boss, boss_intro=boss_intro,
            prompt_html=rich_to_html(challenge.get("prompt", challenge.get("question", ""))),
            lesson_html=rich_to_html(challenge.get("lesson", "")),
            url=challenge.get("url", ""),
            result=None, hint_text=None, show_lesson=False,
            difficulty_suggestion=s.engine.get_difficulty_suggestion(),
        ))

    @hub.post(f"{prefix}/answer", response_class=HTMLResponse)
    async def submit_answer(request: Request, answer: str = Form(default=""), _pid: str = pack_id):
        if not answer.strip():
            return RedirectResponse(f"{prefix}/challenge", status_code=303)
        s = _session()
        challenge = s.get_current_challenge()
        if not challenge:
            return RedirectResponse(f"{prefix}/challenge", status_code=303)
        result = s.submit_answer(answer.strip())
        zone = s.get_current_zone()
        num, total = s.challenge_position()
        ctype = challenge.get("type", "quiz")
        if ctype == "live":
            ctype = "text"
        next_num, _ = s.challenge_position()
        return templates.TemplateResponse(request, "challenge.html", _ctx(
            request,
            challenge=challenge,
            challenge_num=num if not result.correct else next_num,
            challenge_total=total,
            zone=zone, zone_id=s.engine.current_zone,
            ctype=ctype, options=challenge.get("options", []),
            is_boss=challenge.get("is_boss", False), boss_intro="",
            prompt_html=rich_to_html(challenge.get("prompt", challenge.get("question", ""))),
            lesson_html=rich_to_html(challenge.get("lesson", "")),
            url=challenge.get("url", ""),
            result=result, hint_text=None,
            show_lesson=not result.correct,
            submitted_answer=answer.strip(),
            difficulty_suggestion=s.engine.get_difficulty_suggestion(),
        ))

    @hub.post(f"{prefix}/hint", response_class=HTMLResponse)
    async def get_hint(request: Request, _pid: str = pack_id):
        s = _session()
        hint_text = s.get_hint()
        challenge = s.get_current_challenge()
        zone = s.get_current_zone()
        num, total = s.challenge_position()
        ctype = challenge.get("type", "quiz") if challenge else "quiz"
        if ctype == "live":
            ctype = "text"
        return templates.TemplateResponse(request, "challenge.html", _ctx(
            request,
            challenge=challenge, challenge_num=num, challenge_total=total,
            zone=zone, zone_id=s.engine.current_zone,
            ctype=ctype,
            options=challenge.get("options", []) if challenge else [],
            is_boss=challenge.get("is_boss", False) if challenge else False, boss_intro="",
            prompt_html=rich_to_html(challenge.get("prompt", challenge.get("question", ""))) if challenge else "",
            lesson_html=rich_to_html(challenge.get("lesson", "")) if challenge else "",
            url=challenge.get("url", "") if challenge else "",
            result=None, hint_text=hint_text, show_lesson=False,
        ))

    @hub.post(f"{prefix}/skip", response_class=HTMLResponse)
    async def skip_challenge(request: Request, _pid: str = pack_id):
        _session().skip_challenge()
        return RedirectResponse(f"{prefix}/challenge", status_code=303)

    @hub.post(f"{prefix}/bookmark", response_class=HTMLResponse)
    async def toggle_bookmark(request: Request, _pid: str = pack_id):
        _session().toggle_bookmark()
        return RedirectResponse(f"{prefix}/challenge", status_code=303)

    @hub.post(f"{prefix}/difficulty", response_class=HTMLResponse)
    async def set_difficulty(request: Request, mode: str = Form(default="normal"), _pid: str = pack_id):
        _session().set_difficulty(mode)
        return RedirectResponse(f"{prefix}/challenge", status_code=303)

    @hub.get(f"{prefix}/stats", response_class=HTMLResponse)
    async def stats_page(request: Request, _pid: str = pack_id):
        s = _session()
        return templates.TemplateResponse(request, "stats.html", _ctx(
            request,
            zones=s.all_zones_context(),
            **s.detailed_stats_context(),
        ))

    @hub.get(f"{prefix}/daily", response_class=HTMLResponse)
    async def daily_page(request: Request, _pid: str = pack_id):
        s = _session()
        engine = s.engine
        ch = engine.get_daily_challenge(skill_pack)
        today = datetime.date.today().strftime("%A, %B %d, %Y")
        if engine.daily_challenge_completed and engine.daily_challenge_date == str(datetime.date.today()):
            return templates.TemplateResponse(request, "daily.html", _ctx(
                request, daily_completed=True, today_display=today,
                daily_streak=engine.daily_streak,
                daily_challenge_streak=engine.daily_challenge_streak,
                prompt_html="", lesson_html="", ctype="quiz", options=[], result=None,
            ))
        if not ch:
            return RedirectResponse(f"{prefix}/", status_code=303)
        ctype = ch.get("type", "quiz")
        if ctype == "live": ctype = "text"
        return templates.TemplateResponse(request, "daily.html", _ctx(
            request, daily_completed=False, today_display=today,
            daily_streak=engine.daily_streak,
            daily_challenge_streak=engine.daily_challenge_streak,
            prompt_html=rich_to_html(ch.get("prompt", ch.get("question", ""))),
            lesson_html=rich_to_html(ch.get("lesson", "")),
            ctype=ctype, options=ch.get("options", []),
            result=None, hint_text=None,
        ))

    @hub.post(f"{prefix}/daily/answer", response_class=HTMLResponse)
    async def daily_answer(request: Request, answer: str = Form(default=""), _pid: str = pack_id):
        s = _session()
        engine = s.engine
        ch = engine.get_daily_challenge(skill_pack)
        if not ch or not answer.strip():
            return RedirectResponse(f"{prefix}/daily", status_code=303)
        result = s.check_daily_answer(ch, answer.strip())
        today = datetime.date.today().strftime("%A, %B %d, %Y")
        ctype = ch.get("type", "quiz")
        if ctype == "live": ctype = "text"
        return templates.TemplateResponse(request, "daily.html", _ctx(
            request, daily_completed=False, today_display=today,
            daily_streak=engine.daily_streak,
            daily_challenge_streak=engine.daily_challenge_streak,
            prompt_html=rich_to_html(ch.get("prompt", ch.get("question", ""))),
            lesson_html=rich_to_html(ch.get("lesson", "")),
            ctype=ctype, options=ch.get("options", []),
            result=result, submitted_answer=answer.strip(),
        ))

    @hub.get(f"{prefix}/achievements", response_class=HTMLResponse)
    async def achievements_page(request: Request, _pid: str = pack_id):
        all_ach = _session().achievements_context()
        unlocked = [a for a in all_ach if a.get("unlocked")]
        locked = [a for a in all_ach if not a.get("unlocked")]
        return templates.TemplateResponse(request, "achievements.html", _ctx(
            request, achievements=all_ach,
            unlocked=unlocked, locked=locked,
            unlocked_count=len(unlocked), total_count=len(all_ach),
        ))

    @hub.get(f"{prefix}/bookmarks", response_class=HTMLResponse)
    async def bookmarks_page(request: Request, _pid: str = pack_id):
        s = _session()
        return templates.TemplateResponse(request, "bookmarks.html", _ctx(
            request, bookmarked_challenges=s.bookmarks_context(),
        ))

    @hub.get(f"{prefix}/leaderboard", response_class=HTMLResponse)
    async def leaderboard_page(request: Request, _pid: str = pack_id):
        s = _session()
        return templates.TemplateResponse(request, "leaderboard.html", _ctx(
            request, **s.leaderboard_context(),
        ))

    @hub.get(f"{prefix}/parent", response_class=HTMLResponse)
    async def parent_page(request: Request, _pid: str = pack_id):
        s = _session()
        return templates.TemplateResponse(request, "parent.html", _ctx(
            request, **s.parent_dashboard_context(),
        ))

    @hub.get(f"{prefix}/settings", response_class=HTMLResponse)
    async def settings_page(request: Request, _pid: str = pack_id):
        return templates.TemplateResponse(request, "settings.html", _ctx(request))

    @hub.get(f"{prefix}/zones", response_class=HTMLResponse)
    async def zones_page(request: Request, _pid: str = pack_id):
        s = _session()
        return templates.TemplateResponse(request, "menu.html", _ctx(
            request, zones=s.all_zones_context(),
            has_progress=s.has_progress(), intro_story="",
        ))

    @hub.get(f"{prefix}/complete", response_class=HTMLResponse)
    async def pack_complete(request: Request, _pid: str = pack_id):
        s = _session()
        return templates.TemplateResponse(request, "complete.html", _ctx(
            request,
            completed_zones=len(s.engine.completed_zones),
            total_zones=len(skill_pack.zone_order),
        ))


def serve_hub(
    pack_names: list[str],
    *,
    port: int = 8080,
    open_browser: bool = True,
    packs_dir=None,
):
    """Load multiple packs and start the hub web server."""
    try:
        import uvicorn
    except ImportError:
        raise ImportError("uvicorn is required. Install it with: pip install 'quest-engine[web]'")

    packs = [load_skill_pack(name, packs_dir=packs_dir) for name in pack_names]
    app = create_hub_app(packs)

    if open_browser:
        import threading
        import webbrowser
        import time as _time

        def _open():
            _time.sleep(1.2)
            webbrowser.open(f"http://localhost:{port}")

        threading.Thread(target=_open, daemon=True).start()

    print(f"\n  Quest Engine Hub — {len(packs)} packs")
    for p in packs:
        print(f"  → http://localhost:{port}/{p.id}/")
    print()

    uvicorn.run(app, host="localhost", port=port, log_level="warning")
