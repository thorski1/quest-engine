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
import hashlib
import json
import os
import random
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


def _shuffle_options(options: list, answer: str, seed: str) -> tuple[list, dict]:
    """Shuffle quiz options deterministically.

    Returns (shuffled_options, letter_map) where letter_map maps
    shuffled letters back to original letters for answer checking.
    e.g. if original answer was 'b' and it moved to position 'd',
    letter_map['d'] = 'b'.
    """
    if not options or len(options) < 2:
        return options, {}
    letters = ["a", "b", "c", "d"][:len(options)]
    indexed = list(enumerate(options))  # [(0, "opt A"), (1, "opt B"), ...]
    rng = random.Random(seed)
    rng.shuffle(indexed)
    shuffled = [opt for _, opt in indexed]
    # Map: new_letter -> original_letter
    letter_map = {}
    for new_idx, (orig_idx, _) in enumerate(indexed):
        letter_map[letters[new_idx]] = letters[orig_idx]
    return shuffled, letter_map


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

    # ── Auth middleware: gate all game routes when Postgres is active ─────────
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.responses import RedirectResponse as StarletteRedirect

    class AuthGateMiddleware(BaseHTTPMiddleware):
        async def dispatch(self, request, call_next):
            path = request.url.path
            # Always allow: static files, auth routes, hub root, admin, API
            if (path.startswith("/static") or "/auth/" in path or path == "/" or path.startswith("/admin") or path.startswith("/api/")):
                return await call_next(request)
            # Check if Postgres is in use
            from ..storage import get_store
            store = get_store()
            if not hasattr(store, 'create_user'):
                return await call_next(request)  # no auth in local mode
            # Check session cookie
            from .auth import AuthManager, SESSION_COOKIE
            session_id = request.cookies.get(SESSION_COOKIE, "")
            if session_id:
                user = AuthManager(store).get_user_from_session(session_id)
                if user:
                    request.state.user = user
                    return await call_next(request)
            # No valid session — find the pack prefix for redirect
            parts = path.strip("/").split("/")
            pack_prefix = f"/{parts[0]}" if parts else ""
            return StarletteRedirect(f"{pack_prefix}/auth/login", status_code=303)

    hub.add_middleware(AuthGateMiddleware)

    # ── Hub landing page ───────────────────────────────────────────────────────

    @hub.get("/", response_class=HTMLResponse)
    async def hub_index(request: Request):
        pack_cards = []
        for pack in skill_packs:
            session = _sessions[pack.id]
            # Get pack image
            pack_image = ""
            try:
                from .images import get_zone_image
                pack_image = get_zone_image(pack.id)
            except Exception:
                pass
            pack_cards.append({
                "id": pack.id,
                "title": pack.title,
                "subtitle": pack.subtitle,
                "theme": pack.theme or ("playful" if pack.kids_mode else "cyberpunk"),
                "category": pack.category or "",
                "image_url": pack_image,
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
        # Get user count if Postgres is available
        total_users = 0
        try:
            from ..storage import get_store
            store = get_store()
            if hasattr(store, '_get_conn'):
                conn = store._get_conn()
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) FROM users WHERE is_active = TRUE")
                    total_users = cur.fetchone()[0]
        except Exception:
            pass

        # Daily teaser — pick a random challenge to show on the hub
        import datetime as _dt, re as _re
        daily_teaser = None
        try:
            day_hash = hash(str(_dt.date.today())) % len(skill_packs)
            teaser_pack = skill_packs[day_hash]
            all_chs = []
            for z in teaser_pack.zones.values():
                for ch in z.get("challenges", []):
                    if ch.get("options"):  # only quiz with options
                        all_chs.append(ch)
            if all_chs:
                ch_idx = hash(str(_dt.date.today()) + "ch") % len(all_chs)
                ch = all_chs[ch_idx]
                q = _re.sub(r'\[/?[^\]]+\]', '', ch.get("question", ch.get("prompt", "")))
                daily_teaser = {"question": q[:150], "pack_id": teaser_pack.id, "pack_title": teaser_pack.title}
        except Exception:
            pass

        # Get current user for welcome banner
        current_user = None
        user_total_xp = 0
        user_chapters_started = 0
        try:
            from .auth import AuthManager, SESSION_COOKIE
            from ..storage import get_store
            store = get_store()
            if hasattr(store, 'create_user'):
                session_id = request.cookies.get(SESSION_COOKIE, "")
                if session_id:
                    current_user = AuthManager(store).get_user_from_session(session_id)
        except Exception:
            pass
        if current_user:
            user_total_xp = sum(p.get("total_xp", 0) for p in pack_cards)
            user_chapters_started = sum(1 for p in pack_cards if p.get("has_progress"))

        is_platform = len(skill_packs) > 20

        # Platform mode: show landing page with realm cards
        if is_platform:
            # Count packs per category
            cat_counts = {}
            cat_challenges = {}
            cat_first = {}
            for p in skill_packs:
                cat = p.category or "Other"
                cat_counts[cat] = cat_counts.get(cat, 0) + 1
                cat_challenges[cat] = cat_challenges.get(cat, 0) + sum(
                    len(z.get("challenges", [])) for z in p.zones.values()
                )
                if cat not in cat_first:
                    cat_first[cat] = p.id

            # Build dynamic realm list
            realm_meta = {
                "Kids (Ages 5-12)": {"icon": "✨", "css": "r-kids", "name": "The Primer", "desc": "A magical adventure for kids ages 5-12", "guide": "Puck"},
                "DevOps & Engineering": {"icon": "⚡", "css": "r-devops", "name": "NEXUS Quest", "desc": "Master DevOps through a cyberpunk RPG", "guide": "CIPHER"},
                "AI & Machine Learning": {"icon": "🧠", "css": "r-ai", "name": "AI Academy", "desc": "Learn AI from basics to building agents", "guide": "ARIA"},
                "Learn Chinese": {"icon": "🐉", "css": "r-chinese", "name": "Learn Chinese", "desc": "Mandarin from pinyin to conversation", "guide": "龙龙"},
                "Learn Spanish": {"icon": "🌅", "css": "r-spanish", "name": "Learn Spanish", "desc": "Spanish from basics to fluency", "guide": "Sofia"},
                "Learn Japanese": {"icon": "🌊", "css": "r-japanese", "name": "Learn Japanese", "desc": "Japanese from hiragana to conversation", "guide": "Umi"},
                "Learn Korean": {"icon": "🇰🇷", "css": "r-korean", "name": "Learn Korean", "desc": "Korean from Hangul to conversation", "guide": "하나"},
                "Learn French": {"icon": "🇫🇷", "css": "r-french", "name": "Learn French", "desc": "French from basics to fluency", "guide": "Marie"},
                "Learn German": {"icon": "🇩🇪", "css": "r-german", "name": "Learn German", "desc": "German from basics to conversation", "guide": "Hans"},
                "Learn Italian": {"icon": "🇮🇹", "css": "r-italian", "name": "Learn Italian", "desc": "Italian from basics to fluency", "guide": "Marco"},
                "Cybersecurity": {"icon": "🔐", "css": "r-cyber", "name": "Cybersecurity Academy", "desc": "Defend networks, hack ethically", "guide": "CIPHER"},
                "Data Science": {"icon": "📊", "css": "r-data", "name": "Data Science Quest", "desc": "Statistics, pandas, visualization", "guide": "ARIA"},
                "Web Development": {"icon": "🌐", "css": "r-webdev", "name": "Web Dev Quest", "desc": "HTML, CSS, JavaScript, React", "guide": "PIXEL"},
                "Finance": {"icon": "💰", "css": "r-finance", "name": "Finance Quest", "desc": "Personal finance, investing, crypto", "guide": "SAGE"},
                "Psychology": {"icon": "🧠", "css": "r-psych", "name": "Psychology 101", "desc": "Understand the human mind", "guide": "ARIA"},
                "Cooking": {"icon": "👨‍🍳", "css": "r-cooking", "name": "Cooking Academy", "desc": "Kitchen skills, world cuisines, baking", "guide": "Chef"},
            }
            realms = []
            for cat_name in cat_counts:
                meta = realm_meta.get(cat_name, {"icon": "📚", "css": "r-kids", "name": cat_name, "desc": "", "guide": "Guide"})
                realms.append({
                    "name": meta["name"],
                    "icon": meta["icon"],
                    "css": meta["css"],
                    "desc": meta["desc"],
                    "guide": meta["guide"],
                    "count": cat_counts[cat_name],
                    "challenges": cat_challenges.get(cat_name, 0),
                    "first_pack": cat_first[cat_name],
                })

            return templates.TemplateResponse(request, "landing.html", {
                "request": request,
                "total_packs": len(skill_packs),
                "total_challenges": total_challenges,
                "realm_count": len(realms),
                "realms": realms,
                "current_user": current_user,
                "first_pack_id": skill_packs[0].id,
                "user_chapters_started": user_chapters_started,
                "user_total_xp": user_total_xp,
                "packs": pack_cards,
                "active_avatar_url": _get_active_avatar_url(current_user),
                "character": _get_platform_character(request),
            })

        # Single-game mode: show hub grid
        return templates.TemplateResponse(request, "hub.html", {
            "request": request,
            "packs": pack_cards,
            "theme": hub_theme,
            "total_challenges": total_challenges,
            "total_users": total_users,
            "daily_teaser": daily_teaser,
            "current_user": current_user,
            "user_total_xp": user_total_xp,
            "user_chapters_started": user_chapters_started,
            "active_avatar_url": _get_active_avatar_url(current_user),
            "character": _get_platform_character(request),
        })

    # ── Browse all courses (with search/filter/pagination) ────────────────
    @hub.get("/browse", response_class=HTMLResponse)
    async def browse_courses(request: Request):
        """Full course catalog with search, filters, and pagination."""
        pack_cards = []
        category_counts = {}
        for pack in skill_packs:
            session = _sessions[pack.id]
            cat = pack.category or "Other"
            category_counts[cat] = category_counts.get(cat, 0) + 1
            pack_cards.append({
                "id": pack.id, "title": pack.title, "subtitle": pack.subtitle,
                "category": cat,
                "has_progress": session.has_progress(),
                "completed_zones": len(session.engine.completed_zones),
                "total_zones": len(pack.zone_order),
            })

        # Get current user for header
        current_user = None
        try:
            from .auth import AuthManager, SESSION_COOKIE
            from ..storage import get_store
            store = get_store()
            if hasattr(store, 'create_user'):
                sid = request.cookies.get(SESSION_COOKIE, "")
                if sid:
                    current_user = AuthManager(store).get_user_from_session(sid)
        except Exception:
            pass

        return templates.TemplateResponse(request, "browse.html", {
            "request": request,
            "packs": pack_cards,
            "category_counts": dict(sorted(category_counts.items())),
            "current_user": current_user,
            "first_pack_id": skill_packs[0].id if skill_packs else "letters",
            "active_avatar_url": _get_active_avatar_url(current_user),
            "character": _get_platform_character(request),
        })

    # ═══ PLATFORM-LEVEL ONBOARDING FLOW ═══════════════════════════════════
    # Global routes that aren't tied to a specific course.

    def _get_current_user_hub(request: Request) -> dict | None:
        """Helper to get current user at hub level."""
        try:
            from .auth import AuthManager, SESSION_COOKIE
            from ..storage import get_store
            store = get_store()
            if hasattr(store, 'create_user'):
                sid = request.cookies.get(SESSION_COOKIE, "")
                if sid:
                    return AuthManager(store).get_user_from_session(sid)
        except Exception:
            pass
        return None

    # Platform-level character + preferences are stored in a cookie so
    # they persist across individual courses without needing a DB migration.
    CHARACTER_COOKIE = "quest_character"
    PREFERENCES_COOKIE = "quest_preferences"

    def _get_platform_character(request: Request) -> dict:
        """Read platform-level character (class/alignment/tone/avatar) from cookie."""
        try:
            raw = request.cookies.get(CHARACTER_COOKIE, "")
            if raw:
                return json.loads(raw)
        except Exception:
            pass
        return {}

    def _get_platform_preferences(request: Request) -> dict:
        """Read onboarding preferences (age/game-type/style) from cookie."""
        try:
            raw = request.cookies.get(PREFERENCES_COOKIE, "")
            if raw:
                return json.loads(raw)
        except Exception:
            pass
        return {}

    def _get_active_avatar_url(user: dict | None) -> str:
        """Return the currently active avatar image URL for a user, or empty."""
        if not user:
            return ""
        try:
            from ..storage import get_store
            store = get_store()
            if hasattr(store, 'get_user_avatars'):
                avatars = store.get_user_avatars(user["id"])
                for a in avatars:
                    if a.get("is_active"):
                        return a.get("image_data_url", "")
                if avatars:
                    return avatars[0].get("image_data_url", "")
        except Exception:
            pass
        return ""

    @hub.get("/welcome", response_class=HTMLResponse)
    async def welcome_page(request: Request):
        """First stop after sign-up. Explains the flow."""
        user = _get_current_user_hub(request)
        character = _get_platform_character(request)
        prefs = _get_platform_preferences(request)
        avatar_url = _get_active_avatar_url(user)
        # Determine which step the user has reached
        done_prefs = bool(prefs.get("age_level"))
        done_char = bool(character.get("class"))
        done_avatar = bool(avatar_url) or character.get("avatar_emoji") not in (None, "", "🧙")
        return templates.TemplateResponse(request, "welcome.html", {
            "request": request, "current_user": user,
            "total_packs": len(skill_packs),
            "total_challenges": sum(sum(len(z.get("challenges", [])) for z in p.zones.values()) for p in skill_packs),
            "active_avatar_url": avatar_url,
            "character": character,
            "platform_character": character,
            "preferences": prefs,
            "done_prefs": done_prefs,
            "done_char": done_char,
            "done_avatar": done_avatar,
            "is_returning": done_prefs or done_char or done_avatar,
            "first_pack_id": skill_packs[0].id if skill_packs else "letters",
        })

    def _platform_base_ctx(request: Request, user: dict | None) -> dict:
        """Default context for platform-level pages that extend base.html."""
        # Use first pack as a visual placeholder for header rendering.
        placeholder = skill_packs[0] if skill_packs else None
        return {
            "request": request,
            "current_user": user,
            "theme": "cyberpunk",
            "pack_url_prefix": "",
            "pack": placeholder,
            "streak": 0,
            "level": 1,
            "level_progress_pct": 0,
            "total_xp": 0,
            "pack_image": "",
            "active_avatar_url": _get_active_avatar_url(user),
            "platform_character": _get_platform_character(request),
        }

    @hub.get("/character", response_class=HTMLResponse)
    async def platform_character(request: Request):
        """Platform-level character creation (global, not per-course)."""
        user = _get_current_user_hub(request)
        existing = _get_platform_character(request)
        ctx = _platform_base_ctx(request, user)
        ctx["existing_character"] = existing
        return templates.TemplateResponse(request, "character_create.html", ctx)

    @hub.post("/character/save")
    async def platform_character_save(request: Request,
                                      player_name: str = Form(default=""),
                                      player_class: str = Form(default="scholar"),
                                      player_alignment: str = Form(default="hero"),
                                      player_tone: str = Form(default="epic")):
        """Save platform-level character and move to avatar step."""
        # Preserve any existing avatar_emoji from prior character data so we
        # don't drop it when the user re-edits their character.
        prior = _get_platform_character(request)
        char = {
            "name": player_name or "Adventurer",
            "class": player_class,
            "alignment": player_alignment,
            "tone": player_tone,
            "avatar_emoji": prior.get("avatar_emoji", ""),
        }
        resp = RedirectResponse("/avatar", status_code=303)
        resp.set_cookie(
            CHARACTER_COOKIE,
            json.dumps(char),
            max_age=60 * 60 * 24 * 365,  # 1 year
            httponly=False,
            samesite="lax",
            path="/",
        )
        return resp

    @hub.get("/preferences", response_class=HTMLResponse)
    async def platform_preferences(request: Request):
        """Collect onboarding preferences: age level, game type, play style."""
        user = _get_current_user_hub(request)
        existing = _get_platform_preferences(request)
        # Collect available categories for interest selection
        cats = sorted({p.category for p in skill_packs if p.category})
        return templates.TemplateResponse(request, "preferences.html", {
            "request": request, "current_user": user,
            "existing": existing, "categories": cats,
            "active_avatar_url": _get_active_avatar_url(user),
            "platform_character": _get_platform_character(request),
            "first_pack_id": skill_packs[0].id if skill_packs else "letters",
        })

    @hub.post("/preferences/save")
    async def platform_preferences_save(request: Request,
                                        age_level: str = Form(default="adult"),
                                        game_type: str = Form(default="rpg"),
                                        play_style: str = Form(default="balanced"),
                                        interests: str = Form(default="")):
        """Persist preferences and continue to character creation."""
        prefs = {
            "age_level": age_level,
            "game_type": game_type,
            "play_style": play_style,
            "interests": [i.strip() for i in interests.split(",") if i.strip()],
        }
        resp = RedirectResponse("/character", status_code=303)
        resp.set_cookie(
            PREFERENCES_COOKIE,
            json.dumps(prefs),
            max_age=60 * 60 * 24 * 365,
            httponly=False,
            samesite="lax",
            path="/",
        )
        return resp

    @hub.get("/avatar", response_class=HTMLResponse)
    async def platform_avatar(request: Request):
        """Platform-level avatar creation."""
        from .trellis_3d import get_preset_avatars, is_available as trellis_ok
        from .gemini_image import is_available as gemini_ok
        user = _get_current_user_hub(request)
        ctx = _platform_base_ctx(request, user)
        ctx.update({
            "presets": get_preset_avatars(),
            "trellis_available": trellis_ok(),
            "gemini_available": gemini_ok(),
        })
        return templates.TemplateResponse(request, "avatar_3d.html", ctx)

    @hub.post("/avatar/save", response_class=HTMLResponse)
    async def platform_save_avatar(request: Request,
                                   avatar_id: str = Form(default=""),
                                   avatar_url: str = Form(default=""),
                                   avatar_image: str = Form(default=""),
                                   prompt: str = Form(default=""),
                                   style: str = Form(default="")):
        """Save an avatar at the platform level."""
        from ..storage import get_store
        store = get_store()
        user = _get_current_user_hub(request)
        if user and hasattr(store, 'save_avatar') and avatar_image:
            source = "gemini" if avatar_image.startswith("data:") else "preset"
            new_id = store.save_avatar(
                user_id=user["id"], image_data_url=avatar_image,
                glb_url=avatar_url if avatar_url.endswith(".glb") else "",
                prompt=prompt, style=style, source=source,
            )
            if new_id:
                store.set_active_avatar(user["id"], new_id)
        # Next step: course picker
        return RedirectResponse("/pick-course", status_code=303)

    @hub.get("/avatar/gallery", response_class=HTMLResponse)
    async def platform_avatar_gallery(request: Request):
        from ..storage import get_store
        store = get_store()
        user = _get_current_user_hub(request)
        avatars = []
        if user and hasattr(store, 'get_user_avatars'):
            avatars = store.get_user_avatars(user["id"])
        ctx = _platform_base_ctx(request, user)
        ctx["avatars"] = avatars
        return templates.TemplateResponse(request, "avatar_gallery.html", ctx)

    @hub.post("/avatar/activate/{avatar_id}", response_class=HTMLResponse)
    async def platform_activate_avatar(request: Request, avatar_id: int):
        from ..storage import get_store
        store = get_store()
        user = _get_current_user_hub(request)
        if user and hasattr(store, 'set_active_avatar'):
            store.set_active_avatar(user["id"], avatar_id)
        return RedirectResponse("/avatar/gallery", status_code=303)

    @hub.post("/avatar/delete/{avatar_id}", response_class=HTMLResponse)
    async def platform_delete_avatar(request: Request, avatar_id: int):
        from ..storage import get_store
        store = get_store()
        user = _get_current_user_hub(request)
        if user and hasattr(store, 'delete_avatar'):
            store.delete_avatar(user["id"], avatar_id)
        return RedirectResponse("/avatar/gallery", status_code=303)

    # Higher-level learning "paths" — groups of related categories.
    # Order matters: first match wins. Category substrings are matched
    # case-insensitively against pack.category.
    LEARNING_PATHS = [
        {
            "id": "languages",
            "name": "Languages",
            "icon": "🗣️",
            "color": "#00b4d8",
            "desc": "Speak a new tongue — Mandarin, Spanish, Japanese, and more",
            "keywords": ["chinese", "spanish", "japanese", "korean", "french", "german", "italian", "language"],
        },
        {
            "id": "tech",
            "name": "Tech & Code",
            "icon": "💻",
            "color": "#00e5a0",
            "desc": "Programming, DevOps, cybersecurity, web development",
            "keywords": ["devops", "code", "programming", "web", "cyber", "data", "ai", "machine"],
        },
        {
            "id": "kids",
            "name": "Kids Zone",
            "icon": "🧒",
            "color": "#ffd93d",
            "desc": "Playful learning for young adventurers (ages 5-12)",
            "keywords": ["kids", "learn", "age"],
        },
        {
            "id": "creative",
            "name": "Creative & Life",
            "icon": "🎨",
            "color": "#a855f7",
            "desc": "Art, cooking, finance, psychology — skills for living well",
            "keywords": ["cooking", "finance", "psych", "art", "music", "creative", "life"],
        },
    ]

    def _assign_path(category: str) -> str:
        cat_lower = (category or "").lower()
        for path in LEARNING_PATHS:
            for kw in path["keywords"]:
                if kw in cat_lower:
                    return path["id"]
        return "other"

    @hub.get("/pick-course", response_class=HTMLResponse)
    async def pick_course(request: Request):
        """Let user pick their first course. Grouped into high-level paths."""
        user = _get_current_user_hub(request)
        prefs = _get_platform_preferences(request)
        interests = set(prefs.get("interests", []))
        age_level = prefs.get("age_level", "adult")

        # Build list of all courses with metadata
        all_courses = []
        for p in skill_packs:
            cat = p.category or "Other"
            path_id = _assign_path(cat)
            session = _sessions[p.id]
            is_kids = bool(p.kids_mode) or "kids" in cat.lower() or path_id == "kids"
            all_courses.append({
                "id": p.id,
                "title": p.title,
                "subtitle": (p.subtitle or "").replace("◈", "").strip(),
                "category": cat,
                "path_id": path_id,
                "total_zones": len(p.zone_order),
                "has_progress": session.has_progress(),
                "is_recommended": cat in interests,
                "is_kids": is_kids,
                "theme": p.theme or ("playful" if p.kids_mode else "cyberpunk"),
            })

        # Age-level ordering: kids users see Kids Zone first, adults see it last.
        # "teen" and "adult" both de-prioritize kids content without hiding it.
        def _path_order(path_id: str) -> int:
            kids_rank = {"kids": 0, "teen": 3, "adult": 3}.get(age_level, 3)
            if path_id == "kids":
                return kids_rank
            # Push path matching user interests higher
            order_map = {"languages": 1, "tech": 1, "creative": 2}
            return order_map.get(path_id, 2)

        ordered_paths = sorted(LEARNING_PATHS, key=lambda p: _path_order(p["id"]))

        # Group by path
        paths_with_courses = []
        for path in ordered_paths:
            courses = [c for c in all_courses if c["path_id"] == path["id"]]
            if courses:
                # Recommended first, then alphabetical
                courses.sort(key=lambda c: (not c["is_recommended"], c["title"]))
                paths_with_courses.append({
                    **path,
                    "courses": courses,
                    "count": len(courses),
                })

        # "Other" catch-all
        other_courses = [c for c in all_courses if c["path_id"] == "other"]
        if other_courses:
            paths_with_courses.append({
                "id": "other",
                "name": "More Courses",
                "icon": "✨",
                "color": "#ff6b6b",
                "desc": "Everything else",
                "courses": sorted(other_courses, key=lambda c: c["title"]),
                "count": len(other_courses),
            })

        # Featured: top 3 recommended or first 3
        recommended = [c for c in all_courses if c["is_recommended"]][:6]
        if not recommended:
            recommended = all_courses[:6]

        char = _get_platform_character(request)
        return templates.TemplateResponse(request, "pick_course.html", {
            "request": request, "current_user": user,
            "paths": paths_with_courses,
            "recommended": recommended,
            "preferences": prefs,
            "character": char,
            "platform_character": char,
            "active_avatar_url": _get_active_avatar_url(user),
            "total_courses": len(all_courses),
            "first_pack_id": skill_packs[0].id if skill_packs else "letters",
        })

    # ── Admin analytics (hub-level, cross-game) ────────────────────────────────

    @hub.get("/admin/analytics", response_class=HTMLResponse)
    async def admin_analytics(request: Request):
        from ..storage import get_store
        store = get_store()
        ctx = {
            "request": request,
            "total_users": 0, "total_attempts": 0, "global_pass_rate": 0,
            "signups_today": 0, "active_today": 0,
            "recent_signups": [], "hardest_challenges": [], "easiest_challenges": [],
        }
        if not hasattr(store, '_get_conn'):
            return templates.TemplateResponse(request, "admin_analytics.html", ctx)
        try:
            import psycopg2.extras
            conn = store._get_conn()
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
                cur.execute("SELECT COUNT(*) FROM users WHERE is_active = TRUE")
                ctx["total_users"] = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*), SUM(CASE WHEN correct THEN 1 ELSE 0 END) FROM challenge_attempts")
                row = cur.fetchone()
                ctx["total_attempts"] = row[0] or 0
                correct = row[1] or 0
                ctx["global_pass_rate"] = round(correct / max(row[0] or 1, 1) * 100)

                cur.execute("SELECT COUNT(*) FROM users WHERE created_at::date = CURRENT_DATE")
                ctx["signups_today"] = cur.fetchone()[0]

                cur.execute("SELECT COUNT(DISTINCT user_id) FROM challenge_attempts WHERE attempted_at::date = CURRENT_DATE")
                ctx["active_today"] = cur.fetchone()[0]

                cur.execute("""
                    SELECT username, display_name, created_at FROM users
                    WHERE is_active = TRUE ORDER BY created_at DESC LIMIT 20
                """)
                ctx["recent_signups"] = [dict(r) for r in cur.fetchall()]

                cur.execute("""
                    SELECT challenge_id, pack_name, COUNT(*) as total,
                           ROUND(SUM(CASE WHEN correct THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100) as rate
                    FROM challenge_attempts GROUP BY challenge_id, pack_name
                    HAVING COUNT(*) >= 3 ORDER BY rate ASC LIMIT 15
                """)
                ctx["hardest_challenges"] = [dict(r) for r in cur.fetchall()]

                cur.execute("""
                    SELECT challenge_id, pack_name, COUNT(*) as total,
                           ROUND(SUM(CASE WHEN correct THEN 1 ELSE 0 END)::numeric / COUNT(*) * 100) as rate
                    FROM challenge_attempts GROUP BY challenge_id, pack_name
                    HAVING COUNT(*) >= 5 ORDER BY rate DESC LIMIT 10
                """)
                ctx["easiest_challenges"] = [dict(r) for r in cur.fetchall()]

            conn.commit()
        except Exception:
            pass

        return templates.TemplateResponse(request, "admin_analytics.html", ctx)

    # ── Google OAuth routes (hub-level) ─────────────────────────────────────
    @hub.get("/auth/google/login")
    async def google_login(request: Request, redirect: str = "/"):
        from .google_auth import is_available, get_login_url
        if not is_available():
            return RedirectResponse("/", status_code=303)
        url, state = get_login_url()
        response = RedirectResponse(url, status_code=303)
        response.set_cookie("oauth_state", state, max_age=600, httponly=True, samesite="lax", path="/")
        response.set_cookie("oauth_redirect", redirect, max_age=600, httponly=True, samesite="lax", path="/")
        return response

    @hub.get("/auth/google/callback")
    async def google_callback(request: Request, code: str = "", state: str = ""):
        from .google_auth import exchange_code, find_or_create_user
        from .auth import AuthManager
        from ..storage import get_store

        store = get_store()
        redirect_to = request.cookies.get("oauth_redirect", "/")

        try:
            user_info = exchange_code(code)
            if not user_info.get("ok"):
                return RedirectResponse(f"/{skill_packs[0].id}/auth/login", status_code=303)

            user = find_or_create_user(store, user_info)
            if not user.get("id"):
                return RedirectResponse(f"/{skill_packs[0].id}/auth/login", status_code=303)

            # Create session
            auth = AuthManager(store)
            session_id = auth.create_session(user["id"])

            response = RedirectResponse(redirect_to, status_code=303)
            response.set_cookie("quest_session", session_id, max_age=60*60*24*90, httponly=True, samesite="lax", path="/")
            response.delete_cookie("oauth_state")
            response.delete_cookie("oauth_redirect")
            return response
        except Exception:
            return RedirectResponse(f"/{skill_packs[0].id}/auth/login", status_code=303)

    # ── Per-pack routes ────────────────────────────────────────────────────────
    for pack in skill_packs:
        _register_pack_routes(hub, pack, templates)

    # ── TTS audio endpoint ─────────────────────────────────────────────────
    from starlette.responses import Response

    @hub.get("/api/tts")
    async def tts_audio(request: Request, text: str = "", voice: str = "", theme: str = ""):
        """Generate and serve TTS audio. Prefers ElevenLabs, falls back to Google."""
        if not text:
            return Response(status_code=204)
        try:
            # Auto-detect voice from text + theme
            if not voice:
                from .tts import get_character_voice
                voice = get_character_voice(text, theme)

            # Try ElevenLabs first (much better quality)
            from .tts_elevenlabs import synthesize as el_synth, is_available as el_available
            if el_available():
                audio = el_synth(text[:500], voice)
                if audio:
                    return Response(content=audio, media_type="audio/mpeg",
                                   headers={"Cache-Control": "public, max-age=86400"})

            # Fall back to Google TTS
            from .tts import synthesize as g_synth, is_tts_available
            if is_tts_available():
                audio = g_synth(text[:500], voice)
                if audio:
                    return Response(content=audio, media_type="audio/mpeg",
                                   headers={"Cache-Control": "public, max-age=86400"})

            return Response(status_code=204)
        except Exception:
            return Response(status_code=204)

    # ── 3D Avatar generation endpoints ─────────────────────────────────────
    @hub.get("/api/generate-avatar")
    async def generate_3d_avatar(request: Request, prompt: str = "", style: str = "fantasy"):
        """Generate a 3D avatar from a text prompt (FLUX → TRELLIS pipeline)."""
        from .trellis_3d import generate_avatar_from_prompt, is_available
        if not is_available():
            return Response(
                content=json.dumps({"ok": False, "error": "Set REPLICATE_API_TOKEN in Vercel to enable 3D generation"}),
                media_type="application/json"
            )
        result = generate_avatar_from_prompt(prompt, style)
        return Response(content=json.dumps(result), media_type="application/json")

    @hub.post("/api/generate-2d")
    async def generate_2d_image(request: Request):
        """Generate a 2D character image using Gemini 2.5 Flash Image (free)."""
        from .gemini_image import generate_image_from_prompt as gen_gemini, is_available as gemini_ok
        body = await request.json()
        prompt = body.get("prompt", "")
        style = body.get("style", "fantasy")
        if gemini_ok():
            result = gen_gemini(prompt, style)
            return Response(content=json.dumps(result), media_type="application/json")
        # Fallback to Replicate FLUX
        from .trellis_3d import generate_image_from_prompt as gen_flux, is_available as rep_ok
        if rep_ok():
            result = gen_flux(prompt, style)
            # FLUX returns a URL not base64
            if result.get("ok"):
                return Response(content=json.dumps({"ok": True, "image_data_url": result["image_url"]}), media_type="application/json")
            return Response(content=json.dumps(result), media_type="application/json")
        return Response(
            content=json.dumps({"ok": False, "error": "Set GEMINI_API_KEY (free) or REPLICATE_API_TOKEN"}),
            media_type="application/json"
        )

    @hub.post("/api/edit-2d")
    async def edit_2d_image(request: Request):
        """Edit an existing image with a text prompt (Nano Banana specialty)."""
        from .gemini_image import edit_image, is_available as gemini_ok
        body = await request.json()
        if not gemini_ok():
            return Response(
                content=json.dumps({"ok": False, "error": "Set GEMINI_API_KEY to enable image editing"}),
                media_type="application/json"
            )
        result = edit_image(body.get("image_data_url", ""), body.get("prompt", ""))
        return Response(content=json.dumps(result), media_type="application/json")

    @hub.get("/api/image-to-3d")
    async def image_to_3d_avatar(request: Request, url: str = ""):
        """Convert a reference image directly to 3D GLB mesh."""
        from .trellis_3d import generate_avatar_from_image, is_available
        if not is_available():
            return Response(
                content=json.dumps({"ok": False, "error": "Set REPLICATE_API_TOKEN in Vercel to enable 3D generation"}),
                media_type="application/json"
            )
        if not url:
            return Response(
                content=json.dumps({"ok": False, "error": "No image URL provided"}),
                media_type="application/json"
            )
        result = generate_avatar_from_image(url)
        return Response(content=json.dumps(result), media_type="application/json")

    # ── AI Tutor endpoint ──────────────────────────────────────────────────
    @hub.get("/api/explain")
    async def ai_explain(request: Request, question: str = "", answer: str = ""):
        """Use Claude to explain why the correct answer is right."""
        import os
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not api_key or not question:
            return Response(content=json.dumps({"explanation": "AI tutor not configured."}),
                          media_type="application/json")
        try:
            import json as _json
            from urllib.request import Request as Req, urlopen
            payload = _json.dumps({
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 200,
                "messages": [{
                    "role": "user",
                    "content": f"Explain simply in 2-3 sentences why the answer to this question is '{answer}': {question}"
                }]
            }).encode()
            req = Req("https://api.anthropic.com/v1/messages", data=payload, method="POST")
            req.add_header("x-api-key", api_key)
            req.add_header("anthropic-version", "2023-06-01")
            req.add_header("content-type", "application/json")
            with urlopen(req, timeout=10) as resp:
                data = _json.loads(resp.read())
                text = data.get("content", [{}])[0].get("text", "")
                return Response(content=_json.dumps({"explanation": text}),
                              media_type="application/json")
        except Exception:
            return Response(content=json.dumps({"explanation": "Couldn't generate explanation right now."}),
                          media_type="application/json")

    # ── 404 handler ──────────────────────────────────────────────────────────
    from starlette.exceptions import HTTPException as StarletteHTTPException
    from starlette.responses import HTMLResponse as StarletteHTML

    @hub.exception_handler(404)
    async def not_found(request, exc):
        content = templates.get_template("404.html").render()
        return StarletteHTML(content=content, status_code=404)

    return hub


def _register_pack_routes(hub: FastAPI, skill_pack: SkillPack, templates: "Jinja2Templates"):
    """Register all routes for one pack under /{pack_id}/."""
    pack_id = skill_pack.id
    prefix = f"/{pack_id}"
    theme = skill_pack.theme or ("playful" if skill_pack.kids_mode else "cyberpunk")

    def _is_postgres() -> bool:
        """Check if we're using Postgres (auth-gated mode)."""
        from ..storage import get_store
        return hasattr(get_store(), 'create_user')

    def _get_user(request: Request) -> dict | None:
        """Get authenticated user from session cookie, or None."""
        if not _is_postgres():
            return None  # no auth in local mode
        from .auth import AuthManager, SESSION_COOKIE
        from ..storage import get_store
        session_id = request.cookies.get(SESSION_COOKIE, "")
        if not session_id:
            return None
        return AuthManager(get_store()).get_user_from_session(session_id)

    def _require_auth(request: Request) -> dict | RedirectResponse:
        """Check auth. Returns user dict or a redirect response."""
        if not _is_postgres():
            return {"id": 0, "username": "local", "display_name": "Player"}
        user = _get_user(request)
        if not user:
            return RedirectResponse(f"{prefix}/auth/login", status_code=303)
        return user

    def _session_for_user(user: dict) -> WebGameSession:
        """Get or create a session for a specific user.
        Always reloads from store to prevent stale data in serverless warm instances."""
        user_id = user.get("id", 0)
        session_key = f"{pack_id}:{user_id}"
        if session_key not in _sessions:
            sess = WebGameSession(skill_pack)
            sess.engine._player_id = str(user_id) if user_id else "default"
            sess.engine.player_name = user.get("display_name", "Player")
            _sessions[session_key] = sess
        # ALWAYS reload from store — prevents stale state between serverless requests
        _sessions[session_key].engine.load()
        return _sessions[session_key]

    def _session(request: Request = None) -> WebGameSession:
        """Get session — user-specific if authed, default otherwise."""
        if request and _is_postgres():
            user = _get_user(request)
            if user:
                return _session_for_user(user)
        # Fallback to default session
        if pack_id not in _sessions:
            _sessions[pack_id] = WebGameSession(skill_pack)
        return _sessions[pack_id]

    def _ctx(request: Request, **extra) -> dict:
        sess = _session(request)
        user = _get_user(request) if _is_postgres() else None

        # Pull platform-level avatar + character so pack pages display them too.
        active_avatar_url = ""
        platform_character = {}
        if user:
            try:
                from ..storage import get_store
                store = get_store()
                if hasattr(store, 'get_user_avatars'):
                    avatars = store.get_user_avatars(user["id"])
                    for a in avatars:
                        if a.get("is_active"):
                            active_avatar_url = a.get("image_data_url", "")
                            break
                    if not active_avatar_url and avatars:
                        active_avatar_url = avatars[0].get("image_data_url", "")
            except Exception:
                pass
        try:
            raw = request.cookies.get("quest_character", "")
            if raw:
                platform_character = json.loads(raw)
        except Exception:
            pass

        return {
            "request": request,
            "theme": theme,
            "pack": skill_pack,
            "pack_url_prefix": prefix,
            "current_user": user,
            "active_avatar_url": active_avatar_url,
            "platform_character": platform_character,
            **sess.stats_context(),
            **extra,
        }

    # ── Auth routes ─────────────────────────────────────────────────────────

    @hub.get(f"{prefix}/auth/login", response_class=HTMLResponse)
    async def login_page(request: Request, _pid: str = pack_id):
        from .google_auth import is_available as google_available
        return templates.TemplateResponse(request, "auth.html", {
            "request": request, "theme": theme, "mode": "login",
            "prefix": prefix, "error": None, "form_username": "",
            "google_auth": google_available(),
        })

    @hub.get(f"{prefix}/auth/register", response_class=HTMLResponse)
    async def register_page(request: Request, _pid: str = pack_id):
        return templates.TemplateResponse(request, "auth.html", {
            "request": request, "theme": theme, "mode": "register",
            "prefix": prefix, "error": None, "form_username": "", "form_display_name": "",
        })

    @hub.post(f"{prefix}/auth/register", response_class=HTMLResponse)
    async def register_submit(request: Request, username: str = Form(default=""), password: str = Form(default=""), display_name: str = Form(default=""), _pid: str = pack_id):
        from .auth import AuthManager
        from ..storage import get_store
        store = get_store()
        if not hasattr(store, 'create_user'):
            # Not using Postgres — fall back to normal flow
            return RedirectResponse(f"{prefix}/", status_code=303)
        auth = AuthManager(store)
        result = auth.register(username, password, display_name)
        if not result["ok"]:
            return templates.TemplateResponse(request, "auth.html", {
                "request": request, "theme": theme, "mode": "register",
                "prefix": prefix, "error": result["error"],
                "form_username": username, "form_display_name": display_name,
            })
        # Auto-login after registration
        try:
            login_result = auth.login(username, password)
        except Exception:
            login_result = {"ok": False}

        # Notify signup (non-blocking)
        try:
            from .notifications import notify_signup
            game_name = "primer" if skill_pack.kids_mode else ("ai-academy" if (skill_pack.theme == "neural") else "nexus-quest")
            notify_signup(result["user_id"], username, display_name or username, game_name, store)
        except Exception:
            pass

        if login_result.get("ok"):
            # New user: send to /welcome for full onboarding
            response = RedirectResponse("/welcome", status_code=303)
            response.set_cookie("quest_session", login_result["session_id"], max_age=60*60*24*90, httponly=True, samesite="lax", path="/")
            return response
        return RedirectResponse(f"{prefix}/auth/login", status_code=303)

    @hub.post(f"{prefix}/auth/login", response_class=HTMLResponse)
    async def login_submit(request: Request, username: str = Form(default=""), password: str = Form(default=""), _pid: str = pack_id):
        from .auth import AuthManager
        from ..storage import get_store
        store = get_store()
        if not hasattr(store, 'create_user'):
            return RedirectResponse(f"{prefix}/", status_code=303)
        auth = AuthManager(store)
        result = auth.login(username, password)
        if not result["ok"]:
            return templates.TemplateResponse(request, "auth.html", {
                "request": request, "theme": theme, "mode": "login",
                "prefix": prefix, "error": result["error"], "form_username": username,
            })
        # Returning users go back to the landing page (shows "Continue Playing")
        response = RedirectResponse("/", status_code=303)
        response.set_cookie("quest_session", result["session_id"], max_age=60*60*24*90, httponly=True, samesite="lax", path="/")
        return response

    @hub.get(f"{prefix}/auth/logout")
    async def logout(request: Request, _pid: str = pack_id):
        from .auth import AuthManager, SESSION_COOKIE
        from ..storage import get_store
        store = get_store()
        session_id = request.cookies.get(SESSION_COOKIE, "")
        if hasattr(store, 'create_user') and session_id:
            auth = AuthManager(store)
            auth.logout(session_id)
        response = RedirectResponse(f"{prefix}/", status_code=303)
        response.delete_cookie(SESSION_COOKIE)
        return response

    # ── Main routes ──────────────────────────────────────────────────────────

    @hub.get(f"{prefix}/", response_class=HTMLResponse)
    async def menu(request: Request, _pid: str = pack_id):
        s = _session(request)
        # If new player and they already have a platform-level character,
        # auto-start the game using that character — skip per-course creation.
        if not s.has_progress():
            try:
                raw = request.cookies.get("quest_character", "")
                platform_char = json.loads(raw) if raw else {}
            except Exception:
                platform_char = {}
            if platform_char.get("class"):
                name = platform_char.get("name") or skill_pack.default_player_name
                s.new_game(name)
                first_zone = skill_pack.zone_order[0]
                return RedirectResponse(f"{prefix}/zone/{first_zone}/intro", status_code=303)
            # No platform character yet — send to platform-level flow
            return RedirectResponse("/welcome", status_code=303)
        zones = s.all_zones_context()
        return templates.TemplateResponse(request, "menu.html", _ctx(
            request, zones=zones,
            has_progress=True,
            intro_story=rich_to_html(skill_pack.intro_story),
        ))

    @hub.post(f"{prefix}/new-game", response_class=HTMLResponse)
    async def new_game(request: Request, player_name: str = Form(default=""), _pid: str = pack_id):
        name = player_name.strip() or skill_pack.default_player_name
        _session(request).new_game(name)
        first_zone = skill_pack.zone_order[0]
        return RedirectResponse(f"{prefix}/zone/{first_zone}/intro", status_code=303)

    @hub.post(f"{prefix}/continue", response_class=HTMLResponse)
    async def continue_game(request: Request, _pid: str = pack_id):
        if not _session(request).has_progress():
            return RedirectResponse(f"{prefix}/", status_code=303)
        return RedirectResponse(f"{prefix}/challenge", status_code=303)

    @hub.get(f"{prefix}/zone/{{zone_id}}/intro", response_class=HTMLResponse)
    async def zone_intro(request: Request, zone_id: str, _pid: str = pack_id):
        zone = skill_pack.get_zone(zone_id)
        if not zone:
            return RedirectResponse(f"{prefix}/", status_code=303)
        s = _session(request)
        s.start_zone(zone_id)
        intro_text = skill_pack.zone_intros.get(zone_id, "")
        challenges = zone.get("challenges", [])
        completed = s.engine.completed_challenges.get(zone_id, set())
        zone_xp = sum(c.get("xp", 25) for c in challenges)
        zone_progress = len(completed) if isinstance(completed, set) else len(set(completed))
        zone_status = "complete" if zone_id in s.engine.completed_zones else (
            "in_progress" if zone_progress > 0 else "not_started"
        )
        # Get zone image from curated library
        zone_image = ""
        try:
            from .images import get_zone_image
            zone_image = get_zone_image(zone_id)
        except Exception:
            pass
        zone_with_image = dict(zone)
        if zone_image:
            zone_with_image["image_url"] = zone_image

        return templates.TemplateResponse(request, "zone_intro.html", _ctx(
            request, zone=zone_with_image, zone_id=zone_id,
            intro_html=rich_to_html(intro_text) if intro_text else "",
            zone_intros_raw=intro_text,
            challenge_count=len(challenges),
            zone_xp=zone_xp,
            zone_progress=zone_progress,
            zone_status=zone_status,
        ))

    @hub.get(f"{prefix}/challenge", response_class=HTMLResponse)
    async def challenge_page(request: Request, _pid: str = pack_id):
        s = _session(request)
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

        # Motivational message — uses narrative system if available
        from .narrative import get_motivation
        # TODO: load alignment+tone from user profile (defaults for now)
        _align = "hero"
        _tone = "epic" if not skill_pack.kids_mode else "funny"
        motivation = get_motivation(
            alignment=_align, tone=_tone,
            streak=s.engine.streak,
            is_first=(num == 1),
            is_last=(num == total),
        )
        if not motivation:
            # Fallback
            if s.engine.streak >= 10:
                motivation = "🔥 UNSTOPPABLE! 10+ streak — double XP!"
            elif s.engine.streak >= 5:
                motivation = "⚡ On fire! 5+ streak — 1.5x XP bonus!"
            elif s.engine.streak >= 3:
                motivation = "💪 Nice streak! Keep it going for bonus XP!"

        # Shuffle options for anti-cheat (deterministic per user+challenge+date)
        shuffle_map_json = ""
        if options and ctype == "quiz":
            user = _get_user(request) if _is_postgres() else None
            uid = str(user["id"]) if user else "local"
            seed = hashlib.md5(f"{challenge.get('id','')}-{uid}-{datetime.date.today()}".encode()).hexdigest()
            options, letter_map = _shuffle_options(options, challenge.get("answer", "a"), seed)
            shuffle_map_json = json.dumps(letter_map)

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
            shuffle_map=shuffle_map_json,
            motivation=motivation,
        ))

    @hub.post(f"{prefix}/answer", response_class=HTMLResponse)
    async def submit_answer(request: Request, answer: str = Form(default=""), challenge_id: str = Form(default=""), shuffle_map: str = Form(default=""), elapsed: str = Form(default="0"), _pid: str = pack_id):
        if not answer.strip():
            return RedirectResponse(f"{prefix}/challenge", status_code=303)
        s = _session(request)

        # Reverse-map shuffled answer back to original letter
        actual_answer = answer.strip()
        if shuffle_map:
            try:
                lmap = json.loads(shuffle_map)
                actual_answer = lmap.get(actual_answer, actual_answer)
            except (json.JSONDecodeError, TypeError):
                pass

        # Get the specific challenge that was displayed, not the "current" one
        challenge = s.get_current_challenge()
        if challenge_id and challenge and challenge.get("id") != challenge_id:
            # The displayed challenge doesn't match current — find the right one
            challenge = s._find_challenge_by_id(challenge_id)
        if not challenge:
            return RedirectResponse(f"{prefix}/challenge", status_code=303)

        # Check if already completed (double-submit protection)
        zone_id = s.engine.current_zone
        if s.engine.is_challenge_complete(zone_id, challenge.get("id", "")):
            return RedirectResponse(f"{prefix}/challenge", status_code=303)

        try:
            elapsed_s = float(elapsed)
        except (ValueError, TypeError):
            elapsed_s = 0.0
        result = s.submit_answer(actual_answer, challenge=challenge, elapsed_s=elapsed_s)

        # Override result message with narrative-aware text
        from .narrative import get_correct_message, get_wrong_message
        _align = "hero"
        _tone = "epic" if not skill_pack.kids_mode else "funny"
        if result.correct:
            result.message = get_correct_message(_align, _tone)
        else:
            result.message = get_wrong_message(_align, _tone)

        # Record attempt to Postgres for analytics
        try:
            from ..storage import get_store
            store = get_store()
            if hasattr(store, 'record_attempt'):
                user = getattr(request.state, 'user', None)
                if user:
                    store.record_attempt(
                        user_id=user["id"], pack_name=skill_pack.save_file_name,
                        zone_id=zone_id, challenge_id=challenge.get("id", ""),
                        correct=result.correct, answer=answer.strip(),
                        hints=s._hint_index, difficulty=s.engine.difficulty_mode,
                    )
        except Exception:
            pass  # analytics should never block gameplay

        zone = s.get_current_zone()
        num, total = s.challenge_position()
        ctype = challenge.get("type", "quiz")
        if ctype == "live":
            ctype = "text"

        # Re-shuffle options for result display (same seed = same order)
        result_options = challenge.get("options", [])
        result_shuffle_map = ""
        if result_options and ctype == "quiz":
            user = _get_user(request) if _is_postgres() else None
            uid = str(user["id"]) if user else "local"
            seed = hashlib.md5(f"{challenge.get('id','')}-{uid}-{datetime.date.today()}".encode()).hexdigest()
            result_options, rlmap = _shuffle_options(result_options, challenge.get("answer", "a"), seed)
            result_shuffle_map = json.dumps(rlmap)

        return templates.TemplateResponse(request, "challenge.html", _ctx(
            request,
            challenge=challenge,
            challenge_num=num,
            challenge_total=total,
            zone=zone, zone_id=s.engine.current_zone,
            ctype=ctype, options=result_options,
            is_boss=challenge.get("is_boss", False), boss_intro="",
            prompt_html=rich_to_html(challenge.get("prompt", challenge.get("question", ""))),
            lesson_html=rich_to_html(challenge.get("lesson", "")),
            url=challenge.get("url", ""),
            result=result, hint_text=None,
            show_lesson=not result.correct,
            submitted_answer=answer.strip(),
            difficulty_suggestion=s.engine.get_difficulty_suggestion(),
            shuffle_map=result_shuffle_map,
        ))

    @hub.post(f"{prefix}/hint", response_class=HTMLResponse)
    async def get_hint(request: Request, _pid: str = pack_id):
        s = _session(request)
        hint_text = s.get_hint()
        challenge = s.get_current_challenge()
        zone = s.get_current_zone()
        num, total = s.challenge_position()
        ctype = challenge.get("type", "quiz") if challenge else "quiz"
        if ctype == "live":
            ctype = "text"
        # Shuffle options consistently for hint display
        hint_options = challenge.get("options", []) if challenge else []
        hint_shuffle_map = ""
        if hint_options and ctype == "quiz" and challenge:
            user = _get_user(request) if _is_postgres() else None
            uid = str(user["id"]) if user else "local"
            seed = hashlib.md5(f"{challenge.get('id','')}-{uid}-{datetime.date.today()}".encode()).hexdigest()
            hint_options, hlmap = _shuffle_options(hint_options, challenge.get("answer", "a"), seed)
            hint_shuffle_map = json.dumps(hlmap)

        return templates.TemplateResponse(request, "challenge.html", _ctx(
            request,
            challenge=challenge, challenge_num=num, challenge_total=total,
            zone=zone, zone_id=s.engine.current_zone,
            ctype=ctype,
            options=hint_options,
            is_boss=challenge.get("is_boss", False) if challenge else False, boss_intro="",
            prompt_html=rich_to_html(challenge.get("prompt", challenge.get("question", ""))) if challenge else "",
            lesson_html=rich_to_html(challenge.get("lesson", "")) if challenge else "",
            url=challenge.get("url", "") if challenge else "",
            result=None, hint_text=hint_text, show_lesson=False,
            shuffle_map=hint_shuffle_map,
        ))

    @hub.post(f"{prefix}/skip", response_class=HTMLResponse)
    async def skip_challenge(request: Request, _pid: str = pack_id):
        _session(request).skip_challenge()
        return RedirectResponse(f"{prefix}/challenge", status_code=303)

    @hub.post(f"{prefix}/bookmark", response_class=HTMLResponse)
    async def toggle_bookmark(request: Request, _pid: str = pack_id):
        _session(request).toggle_bookmark()
        return RedirectResponse(f"{prefix}/challenge", status_code=303)

    @hub.post(f"{prefix}/difficulty", response_class=HTMLResponse)
    async def set_difficulty(request: Request, mode: str = Form(default="normal"), _pid: str = pack_id):
        _session(request).set_difficulty(mode)
        return RedirectResponse(f"{prefix}/challenge", status_code=303)

    @hub.post(f"{prefix}/streak-freeze", response_class=HTMLResponse)
    async def buy_streak_freeze(request: Request, _pid: str = pack_id):
        s = _session(request)
        s.engine.buy_streak_freeze()
        return RedirectResponse(f"{prefix}/challenge", status_code=303)

    @hub.get(f"{prefix}/stats", response_class=HTMLResponse)
    async def stats_page(request: Request, _pid: str = pack_id):
        s = _session(request)
        return templates.TemplateResponse(request, "stats.html", _ctx(
            request,
            zones=s.all_zones_context(),
            **s.detailed_stats_context(),
        ))

    @hub.get(f"{prefix}/daily", response_class=HTMLResponse)
    async def daily_page(request: Request, _pid: str = pack_id):
        s = _session(request)
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
        s = _session(request)
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
        all_ach = _session(request).achievements_context()
        unlocked = [a for a in all_ach if a.get("unlocked")]
        locked = [a for a in all_ach if not a.get("unlocked")]
        return templates.TemplateResponse(request, "achievements.html", _ctx(
            request, achievements=all_ach,
            unlocked=unlocked, locked=locked,
            unlocked_count=len(unlocked), total_count=len(all_ach),
        ))

    @hub.get(f"{prefix}/zone/{{zone_id}}/complete", response_class=HTMLResponse)
    async def zone_complete_page(request: Request, zone_id: str, _pid: str = pack_id):
        s = _session(request)
        zone = skill_pack.get_zone(zone_id)
        if not zone:
            return RedirectResponse(f"{prefix}/", status_code=303)
        challenges = zone.get("challenges", [])
        stars = s.engine.get_zone_stars(zone_id)
        zs = s.engine.zone_scores.get(zone_id, {})
        zone_xp = sum(c.get("xp", 25) for c in challenges)
        completion_text = skill_pack.zone_completions.get(zone_id, "")
        # Find achievement for this zone
        ach_id = skill_pack.zone_achievement_map.get(zone_id)
        ach_name = ""
        if ach_id and ach_id in s.engine.achievements:
            ach_data = skill_pack.achievements.get(ach_id)
            if ach_data:
                ach_name = ach_data[0]
        next_zone = s._next_zone_id(zone_id)
        return templates.TemplateResponse(request, "zone_complete.html", _ctx(
            request,
            zone_name=zone.get("name", zone_id),
            stars=stars,
            zone_xp=zone_xp,
            challenges_done=len(challenges),
            challenges_total=len(challenges),
            hints_used=zs.get("hints", 0),
            completion_html=rich_to_html(completion_text) if completion_text else "",
            new_achievement=ach_name,
            next_zone_id=next_zone,
        ))

    @hub.get(f"{prefix}/smart-review", response_class=HTMLResponse)
    async def smart_review_page(request: Request, _pid: str = pack_id):
        s = _session(request)
        return templates.TemplateResponse(request, "spaced_review.html", _ctx(
            request, **s.spaced_review_context(),
        ))

    @hub.post(f"{prefix}/review/rate", response_class=HTMLResponse)
    async def rate_review(request: Request, challenge_id: str = Form(default=""), zone_id: str = Form(default=""), rating: str = Form(default="good"), _pid: str = pack_id):
        # For now, redirect back — in future, update interval in DB
        return RedirectResponse(f"{prefix}/smart-review", status_code=303)

    @hub.get(f"{prefix}/review", response_class=HTMLResponse)
    async def review_page(request: Request, _pid: str = pack_id):
        s = _session(request)
        return templates.TemplateResponse(request, "review.html", _ctx(
            request, review_items=s.review_context(),
        ))

    @hub.get(f"{prefix}/bookmarks", response_class=HTMLResponse)
    async def bookmarks_page(request: Request, _pid: str = pack_id):
        s = _session(request)
        return templates.TemplateResponse(request, "bookmarks.html", _ctx(
            request, bookmarked_challenges=s.bookmarks_context(),
        ))

    @hub.get(f"{prefix}/leaderboard", response_class=HTMLResponse)
    async def leaderboard_page(request: Request, _pid: str = pack_id):
        s = _session(request)
        return templates.TemplateResponse(request, "leaderboard.html", _ctx(
            request, **s.leaderboard_context(),
        ))

    @hub.get(f"{prefix}/parent", response_class=HTMLResponse)
    async def parent_page(request: Request, _pid: str = pack_id):
        s = _session(request)
        return templates.TemplateResponse(request, "parent.html", _ctx(
            request, **s.parent_dashboard_context(),
        ))

    @hub.get(f"{prefix}/profile", response_class=HTMLResponse)
    async def profile_page(request: Request, _pid: str = pack_id):
        s = _session(request)
        from .gear import GEAR_CATALOG, RARITY_COLORS, get_new_gear_drops

        # Character data (defaults for now — will be stored per-user later)
        char_stats = {"int": 6, "wis": 5, "spd": 5, "end": 5, "cha": 5, "lck": 5}
        player_avatar = "🧙"
        player_class = "Scholar"

        # Determine gear from zone completion count
        zone_count = len(s.engine.completed_zones)
        owned_gear = []
        equipped = {}
        drops = get_new_gear_drops(zone_count, [])
        for d in drops:
            owned_gear.append(d["id"])
            slot = d.get("slot", "")
            if slot and slot not in equipped:
                equipped[slot] = d["id"]

        # Merge all achievements (engine + pack)
        from ..engine import BASE_ACHIEVEMENTS
        all_achs = {**BASE_ACHIEVEMENTS, **skill_pack.achievements}

        return templates.TemplateResponse(request, "character_sheet.html", _ctx(
            request,
            char_stats=char_stats,
            player_avatar=player_avatar,
            player_class=player_class,
            equipped=equipped,
            inventory=owned_gear,
            gear_catalog=GEAR_CATALOG,
            rarity_colors=RARITY_COLORS,
            all_achievements=all_achs,
            earned_achievements=s.engine.achievements,
            **s.detailed_stats_context(),
        ))

    # Avatar management lives at platform level only (/avatar, /avatar/save,
    # /avatar/gallery, /avatar/activate/{id}, /avatar/delete/{id}). Per-course
    # avatar routes were intentionally removed — every player has a single
    # avatar that follows them across all courses.

    @hub.get(f"{prefix}/quest-log", response_class=HTMLResponse)
    async def quest_log_page(request: Request, _pid: str = pack_id):
        s = _session(request)
        engine = s.engine

        # Build log entries from game state
        log_entries = []

        # Zone completions
        for zone_id in engine.completed_zones:
            zone = skill_pack.get_zone(zone_id)
            name = zone.get("name", zone_id) if zone else zone_id
            log_entries.append({
                "type": "zone_complete", "icon": "🏁",
                "title": f"Zone Complete: {name}",
                "desc": f"Conquered all challenges in {name}",
                "xp": sum(c.get("xp", 25) for c in zone.get("challenges", [])) if zone else 0,
                "time": "completed", "sort": 2,
            })

        # Achievements
        from ..engine import BASE_ACHIEVEMENTS
        all_achs = {**BASE_ACHIEVEMENTS, **skill_pack.achievements}
        for ach_id in engine.achievements:
            ach = all_achs.get(ach_id, ("Unknown", ""))
            log_entries.append({
                "type": "achievement", "icon": "🏆",
                "title": f"Achievement: {ach[0]}",
                "desc": ach[1] if len(ach) > 1 else "",
                "xp": None, "time": "earned", "sort": 3,
            })

        # Level milestones
        level = engine.level
        if level >= 5:
            for milestone in [5, 10, 15, 20, 25, 30]:
                if level >= milestone:
                    log_entries.append({
                        "type": "level_up", "icon": "⬆️",
                        "title": f"Reached Level {milestone}",
                        "desc": f"Earned enough XP to reach level {milestone}",
                        "xp": None, "time": f"level {milestone}", "sort": 1,
                    })

        # Current streak
        if engine.streak >= 3:
            log_entries.append({
                "type": "streak", "icon": "🔥",
                "title": f"{engine.streak}-Answer Streak!",
                "desc": "Consecutive correct answers",
                "xp": None, "time": "active", "sort": 4,
            })

        # Daily streak
        if engine.daily_streak >= 3:
            log_entries.append({
                "type": "daily", "icon": "📅",
                "title": f"{engine.daily_streak}-Day Login Streak",
                "desc": "Consecutive days of playing",
                "xp": None, "time": "active", "sort": 4,
            })

        # Sort: most recent/important first
        log_entries.sort(key=lambda x: x.get("sort", 0), reverse=True)

        return templates.TemplateResponse(request, "quest_log.html", _ctx(
            request, log_entries=log_entries,
            achievements=engine.achievements,
        ))

    @hub.get(f"{prefix}/settings", response_class=HTMLResponse)
    async def settings_page(request: Request, _pid: str = pack_id):
        return templates.TemplateResponse(request, "settings.html", _ctx(request))

    @hub.get(f"{prefix}/zones", response_class=HTMLResponse)
    async def zones_page(request: Request, _pid: str = pack_id):
        s = _session(request)
        return templates.TemplateResponse(request, "menu.html", _ctx(
            request, zones=s.all_zones_context(),
            has_progress=s.has_progress(), intro_story="",
        ))

    @hub.get(f"{prefix}/complete", response_class=HTMLResponse)
    async def pack_complete(request: Request, _pid: str = pack_id):
        s = _session(request)
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
    category: str = "",
):
    """Load multiple packs and start the hub web server."""
    try:
        import uvicorn
    except ImportError:
        raise ImportError("uvicorn is required. Install it with: pip install 'quest-engine[web]'")

    packs = [load_skill_pack(name, packs_dir=packs_dir) for name in pack_names]
    if category:
        for p in packs:
            if not p.category:
                p.category = category
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
