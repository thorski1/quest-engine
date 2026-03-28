# Changelog

## 2.0.0 (2026-03-28)

Major release — quest-engine is now a full-featured educational game platform.

### Web Experience (12 page types)
- **Hub** — multi-pack chapter selector with animated cards
- **Onboarding** — 4-step welcome flow for new players
- **Menu** — zone selector with quick stats + daily challenge banner
- **Zone Intro** — narrative with challenge count, XP, progress status
- **Challenge** — quiz/text with confetti, sounds, adaptive difficulty
- **Daily Challenge** — one per day, 2× XP bonus, streak tracking
- **Stats** — accuracy, streaks, zone breakdown, improvement areas
- **Review** — wrong answer journal with lessons for spaced repetition
- **Leaderboard** — XP + streaks + Hall of Fame, multi-player ready
- **Achievements** — progress bar, categorized (unlocked/locked)
- **Bookmarks** — saved challenges for later review
- **Settings** — theme override, font size, sound, reduced motion
- **Complete** — celebration with confetti + share to X
- **Parent Dashboard** — strengths, struggles, tips (kids_mode only)

### Three Themes
- **Cyberpunk** — neon green on dark blue (NEXUS Quest)
- **Playful** — purple on cream (The Primer)
- **Neural** — electric purple + cyan (AI Academy)

### Engine Features
- **Pluggable storage**: SQLite, JSON file, or in-memory backends
- **Adaptive difficulty**: suggests changes based on session accuracy
- **Daily challenges**: deterministic per-day, 2× XP, streak tracking
- **Sound effects**: synthesized via Web Audio API (no audio files)
- **PWA**: service worker, offline caching, installable
- **Accessibility**: ARIA labels, skip-link, reduced motion, keyboard shortcuts
- **OG meta tags**: rich link previews when sharing
- **SkillPack.theme**: custom theme field per pack

### Keyboard Shortcuts
- A-D / 1-4: answer quiz options
- Enter/Space: advance to next challenge
- H: hint, S: skip

## 1.5.2 (2026-03-27)
- Multi-pack hub with auto-theme detection
- Serverless support (read-only filesystem)
- Web mode with FastAPI + Jinja2

## 1.0.0 (2026-03-25)
- Initial release: terminal RPG framework
- Skill pack system, XP, levels, achievements
- Rich TUI with themes
