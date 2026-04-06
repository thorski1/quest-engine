# Quest Engine — Claude Code Context

## What This Is
Quest Engine is a pluggable educational game engine. It powers 6 games with 132 chapters and 6,091+ challenges.

## Architecture
- **Engine**: `/Users/samuelthoyre/quest-engine/` — Python framework, FastAPI web mode
- **Games**: primer, nexus-quest, ai-academy, learn-chinese, learn-spanish, learn-japanese
- **Database**: Neon Postgres (shared across all games)
- **Deploy**: All games on Vercel, quest-engine installed from GitHub
- **Tests**: 82 tests in `tests/`, run with `python3 -m pytest tests/ -v`
- **CI**: GitHub Actions on Python 3.10/3.11/3.12

## Key Files
- `engine/web/hub.py` — all web routes (700+ lines)
- `engine/web/state.py` — game session management
- `engine/engine.py` — core XP/levels/achievements
- `engine/web/tts.py` — Google Cloud TTS integration
- `engine/web/auth.py` — user authentication
- `engine/storage.py` — pluggable storage (SQLite/JSON/Memory/Postgres)
- `engine/storage_postgres.py` — Postgres backend with user accounts

## MCP Servers Available
- `postgres` — query Neon DB directly
- `github` — manage repos/issues/PRs
- `filesystem` — broad file access
- `memory` — persistent knowledge store
- `elevenlabs` — premium TTS (needs API key)
- `fetch` — HTTP requests

## Deploy Commands
```bash
# Deploy all 6 games
for dir in primer nexus-quest ai-academy learn-chinese learn-spanish learn-japanese; do
  cd /Users/samuelthoyre/$dir && vercel --prod --yes &
done; wait
```

## Test Commands
```bash
cd /Users/samuelthoyre/quest-engine && python3 -m pytest tests/ -v
```

## Common Issues
- `time` skill pack name collides with Python stdlib → renamed to `telling_time`
- Postgres connections in serverless: always create fresh connection per request
- Studio TTS voices don't support SSML pitch → use AudioConfig pitch instead
- Auth middleware must whitelist `/static/`, `/auth/`, `/api/`, `/admin`
