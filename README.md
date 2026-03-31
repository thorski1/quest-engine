# Quest Engine

```
  ██████╗ ██╗   ██╗███████╗███████╗████████╗
 ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
 ██║   ██║██║   ██║█████╗  ███████╗   ██║
 ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║
 ╚██████╔╝╚██████╔╝███████╗███████║   ██║
  ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝
    E  N  G  I  N  E
```

**The gold standard educational game engine.** Build skill-based learning games that play in the terminal or browser — with XP, levels, daily challenges, achievements, leaderboards, user accounts, and adaptive difficulty. Zero game content included. You bring the curriculum; the engine handles everything else.

`v2.0.0` · Python 3.10+ · MIT License

---

## Games Built on Quest Engine

| Game | Audience | Chapters | Challenges | What You Learn |
|------|----------|----------|------------|----------------|
| [The Primer](https://github.com/thorski1/primer) | Children (5-12) | 28 | 1,381 | Letters, Numbers, Science, Kindness, Geography, Math, History, Art, Coding, Space, Music, Animals, Words, Cooking, Body, Money, Environment, Thinking, Time, Inventions, Oceans, Civics, Emotions, Measurement, Safety, Dinosaurs, Weather, Maps |
| [NEXUS Quest](https://github.com/thorski1/nexus-quest) | Developers | 27 | 1,551 | Bash, SSH, Vim, Git, Docker, Postgres, Python, Regex, Linux, K8s, AWS, Terraform, Networking, Security, CI/CD, Observability, Databases, Go, API Design, Rust, TypeScript, System Design, Data Engineering, Shell Scripting, Cloud Native, Web Dev, Python Advanced |
| [AI Academy](https://github.com/thorski1/ai-academy) | Everyone | 8 | 328 | AI Fundamentals, Prompt Engineering, Chatbots, AI Tools, Ethics, AI at Work, AI Coding, Agents |
| [Learn Chinese](https://github.com/thorski1/learn-chinese) | Language learners | 8 | 340 | Pinyin, Greetings, Numbers, Food & Drink, Family, Daily Life, Travel, Culture |
| [Learn Spanish](https://github.com/thorski1/learn-spanish) | Language learners | 8 | 293 | Basics, Greetings, Numbers, Food, Family, Travel, Daily Life, Culture |
| [Learn Japanese](https://github.com/thorski1/learn-japanese) | Language learners | 8 | 304 | Hiragana, Katakana, Greetings, Numbers, Food, Daily Life, Travel, Culture |

**6 games. 87 chapters. 4,237 challenges. One engine.**

---

## Roadmap

```
 ✅ SHIPPED                    🔨 IN PROGRESS               📋 PLANNED
 ─────────                    ──────────────               ─────────
 ✅ Terminal TUI               🔨 Mario-style 2D world      📋 Multiplayer PvP challenges
 ✅ Web mode (FastAPI)          🔨 More game content         📋 AI-generated challenges (LLM)
 ✅ 8 visual themes             🔨 Social media automation   📋 Voice input for answers
 ✅ Phaser.js RPG overworld                                  📋 Spaced repetition engine
 ✅ PWA + offline                                            📋 Parent email reports
 ✅ Sound effects                                            📋 Classroom/teacher mode
 ✅ User accounts + auth                                     📋 Mobile app (React Native)
 ✅ Postgres persistence                                     📋 AI tutor (Claude explains)
 ✅ Daily challenges                                         📋 Challenge editor (web UI)
 ✅ Adaptive difficulty                                      📋 Multi-language i18n
 ✅ Leaderboards                                             📋 Video lesson integration
 ✅ Parent dashboard                                         📋 Certification/badges (PDF)
 ✅ Admin analytics                                          📋 LTI integration (LMS)
 ✅ Signup notifications                                     📋 Plugin marketplace
 ✅ SVG illustrations                                        📋 Real-time multiplayer
 ✅ 66 tests + CI pipeline                                   📋 3D world (Three.js)
 ✅ Streak tracking + combos
 ✅ OG meta / SEO
 ✅ Review/bookmarks pages
 ✅ Profile page
 ✅ 6 games, 87 chapters, 4,237 ch.
 ✅ Google TTS (character voices)
 ✅ Images on zone intros
 ✅ Rich media (code/img/video)
```

### 2D Game World Roadmap (Phaser.js)

The overworld at `/{pack}/explore` is the foundation. Here's where it's going:

```
 Phase 1 ✅ DONE          Phase 2 🔨 NEXT          Phase 3 📋 FUTURE
 ─────────────           ──────────────           ────────────────
 ✅ Top-down overworld    🔨 Side-scrolling        📋 Procedural worlds
 ✅ WASD movement            Mario-style levels    📋 Boss battle mini-games
 ✅ Zone buildings        🔨 Platforms + jumping   📋 NPC dialogue system
 ✅ Proximity detection   🔨 Collectible coins     📋 Inventory system
 ✅ Enter zone on key        (XP pickups)          📋 Weather effects
 ✅ Theme palettes (8)    🔨 Enemies (wrong        📋 Day/night cycle
 ✅ Ambient particles        answers = damage)     📋 Multiplayer rooms
 ✅ Completion markers    🔨 Power-ups (hints,     📋 Custom character skins
 ✅ Locked zone gates        streak shield)        📋 Level editor
                          🔨 Animated sprites      📋 Leaderboard races
                          🔨 Sound effects per     📋 Seasonal events
                             action                📋 Achievement trophies
                          🔨 Death + respawn           in trophy room
                          🔨 Level progression
                             (zone = level)
```

**The vision:** Each zone becomes a Mario-style level. Platforms contain quiz
questions — answer correctly to progress, wrong answers cost a life. Coins
(XP) scattered through the level. Boss at the end of each zone. The overworld
map connects all levels. Your character levels up visually as you progress.

### Architecture Vision

```
                    ┌──────────────────┐
                    │   Quest Engine   │
                    │   (framework)    │
                    └────────┬─────────┘
           ┌─────────┬──────┴──────┬─────────┐
           │         │             │          │
      ┌────┴───┐ ┌───┴────┐ ┌─────┴──┐ ┌────┴─────┐
      │ Primer │ │ NEXUS  │ │   AI   │ │  Learn   │
      │ (kids) │ │ Quest  │ │Academy │ │ Chinese  │
      └────┬───┘ └───┬────┘ └────┬───┘ └────┬─────┘
           │         │           │           │
           └─────────┴─────┬─────┴───────────┘
                           │
                    ┌──────┴──────┐
                    │ Neon Postgres│
                    │  (shared)    │
                    └─────────────┘
```

---

## Why Quest Engine?

- **Two play modes, zero config** — Rich-powered terminal TUI and a FastAPI + HTMX browser interface
- **3 themes** — Cyberpunk (dark/neon), Playful (warm/rounded, kid-friendly), and Neural (AI-focused)
- **17 web page types** — Hub, menu, challenge, zone intro, zone complete, daily challenge, stats, achievements, bookmarks, leaderboard, auth, onboarding, settings, parent dashboard, review, completion certificate, and more
- **Postgres persistence** — Optional PostgreSQL backend for user accounts, leaderboards, and cross-device progress
- **PWA support** — Installable on mobile, works offline
- **Sound effects** — Synthesized audio feedback, no external files needed
- **6 challenge types** — Quiz, fill-in-the-blank, flag quiz, live sandbox, sequence ordering, matching pairs
- **Campaigns** — Chain skill packs into multi-chapter stories with placement quizzes and narrative bridges
- **Vercel-deployable** — Serverless deployment out of the box

---

## Install

### Recommended

```bash
pip install quest-engine
```

Or with [uv](https://docs.astral.sh/uv/):

```bash
uv pip install quest-engine
```

### With web mode

```bash
pip install 'quest-engine[web]'
```

### With Postgres support

```bash
pip install 'quest-engine[web,postgres]'
```

### From source

```bash
git clone https://github.com/thorski1/quest-engine
pip install -e './quest-engine[web]'
```

**Requirements:** Python 3.10+, `rich >= 13.0.0`

---

## Engine Features

| Feature | Description |
|---------|-------------|
| **XP & Levels** | Configurable `level_titles` per pack; XP scales with difficulty |
| **Star Ratings** | 1-3 stars per zone based on hints used and challenges skipped |
| **Achievements** | Auto-unlocked on zone completion; displayed in stats |
| **Daily Challenge** | Deterministic pick per pack per day; 2x XP; streak tracking |
| **Difficulty Modes** | Easy (0.75x XP, free hints) / Normal / Hard (1.5x XP) |
| **Speed Records** | Per-challenge personal bests; new-record flash on screen |
| **Bookmarks** | Toggle with `[b]`; review from main menu |
| **Zone Preview** | Challenge list shown before entering a zone |
| **Completion Certificate** | ASCII grade art (S/A/B/C/D) on pack or campaign complete |
| **Campaign Stats** | Per-chapter star ratings, XP totals, overall grade |
| **Placement Quiz** | Optional assessment to pick the right starting chapter |
| **Kids Mode** | `kids_mode=True` for kid-friendly praise and gentler UX |
| **User Accounts** | Optional signup/login with Postgres backend |
| **Leaderboards** | Global and per-pack rankings when Postgres is enabled |
| **PWA** | Installable progressive web app for mobile |
| **Sound Effects** | Synthesized audio for correct/wrong/level-up events |
| **Auto-Updates** | Version check at startup with upgrade prompt |
| **Save/Resume** | JSON saves in `~/.quest_engine/` (local) or Postgres (hosted) |

---

## Web Mode

Quest Engine includes a built-in web interface. Any game built on it gets a browser UI for free:

```bash
nexus-quest --web      # opens http://localhost:8080
primer --web
ai-academy --web
```

The web server is a FastAPI app serving Jinja2 templates with HTMX for partial page updates — no JS build step, no webpack, no Node.

### Themes

The interface auto-selects a theme based on the skill pack, or you can set it explicitly:

| Theme | Used By | Colors | Font |
|-------|---------|--------|------|
| `cyberpunk` | NEXUS Quest | Dark navy, neon green, cyan | JetBrains Mono |
| `playful` | The Primer | Warm cream, purple, rounded corners | Nunito |
| `neural` | AI Academy | Deep purple, electric highlights | System |

### Web Page Types (17)

Hub, menu, challenge, zone intro, zone complete, daily challenge, stats, achievements, bookmarks, leaderboard, auth (login/signup), onboarding, settings, parent dashboard, review mode, completion certificate, help.

### Vercel Deployment

Games can be deployed as serverless web apps on Vercel. See the `api/index.py` pattern in any of the three games for a reference implementation.

---

## Project Structure

Your game lives in its own repo alongside the engine:

```
quest-engine/               <-- this package (engine only, no game content)
  engine/
    engine.py               <-- XP, levels, saves, achievements, speed records
    ui.py                   <-- all Rich TUI components
    challenges.py           <-- quiz / fill-blank / live / ordered / arrange runner
    skill_pack.py           <-- SkillPack dataclass + load_skill_pack()
    campaign.py             <-- Campaign dataclass + CampaignSession
    zone.py                 <-- Zone dict helper
    challenge.py            <-- Challenge dict helper
    main.py                 <-- run() and run_campaign() entry points
    web/
      server.py             <-- FastAPI web server
      hub.py                <-- Multi-pack hub page
      auth.py               <-- User accounts + Postgres auth
      state.py              <-- Session and persistence layer

your-game/                  <-- your repo (content only)
  skill-packs/
    bash/
      __init__.py           <-- exports SKILL_PACK = SkillPack(...)
      zones.py              <-- all zone and challenge data
      story.py              <-- narrative text (intros, outros, story)
  campaigns/
    my_campaign/
      __init__.py           <-- exports CAMPAIGN = Campaign(...)
      story.py              <-- chapter bridges, entry summaries
  your_game/
    main.py                 <-- sets env vars, calls run() or run_campaign()
  pyproject.toml
```

---

## Quick Start: Your First Pack

### 1. Install the engine

```bash
pip install quest-engine
```

### 2. Set the skill-packs directory

```python
# your_game/main.py
import os
from pathlib import Path
from engine.main import run

_HERE = Path(__file__).parent.parent
os.environ.setdefault("QUEST_SKILL_PACKS_DIR", str(_HERE / "skill-packs"))

def main():
    run("my_pack")
```

### 3. Create your skill pack

```
your-game/
  skill-packs/
    my_pack/
      __init__.py
      zones.py
      story.py
```

### 4. Write your zones

**`skill-packs/my_pack/zones.py`**

```python
from engine.zone import Zone
from engine.challenge import Challenge

ZONE_ORDER = ["intro_zone", "advanced_zone"]

ZONES = {
    "intro_zone": Zone(
        id="intro_zone",
        title="Introduction",
        description="The basics.",
        challenges=[
            Challenge(
                id="q1",
                type="quiz",
                prompt="What is 2 + 2?",
                options=["3", "4", "5", "6"],
                answer="b",
                explanation="2 + 2 = 4. The answer is B.",
                hints=["Think about fingers on two hands.", "It's less than 5."],
                xp=10,
            ),
            Challenge(
                id="q2",
                type="fill_blank",
                prompt="The capital of France is ___.",
                answer="Paris",
                explanation="Paris has been the capital of France since the 10th century.",
                xp=10,
            ),
        ],
    ),
}
```

### 5. Define your SkillPack

**`skill-packs/my_pack/__init__.py`**

```python
from engine.skill_pack import SkillPack
from .story import INTRO_STORY, ZONE_INTROS, ZONE_COMPLETIONS, BOSS_INTROS
from .zones import ZONES, ZONE_ORDER

SKILL_PACK = SkillPack(
    id="my_pack",
    title="My Pack",
    subtitle="Learn something new.",
    save_file_name="my_pack",
    intro_story=INTRO_STORY,
    quit_message="Come back soon.",
    zone_order=ZONE_ORDER,
    zones=ZONES,
    zone_intros=ZONE_INTROS,
    zone_completions=ZONE_COMPLETIONS,
    boss_intros=BOSS_INTROS,
    level_titles=[(1, "Novice"), (5, "Learner"), (10, "Expert"), (20, "Master")],
)
```

### 6. Add web mode

```python
# your_game/main.py
import sys
from pathlib import Path

_HERE = Path(__file__).parent
_PACKS_DIR = str(_HERE / "skill-packs")
_WEB = "--web" in sys.argv

def main():
    if _WEB:
        from engine.web.server import serve
        serve("my_pack", port=8080, packs_dir=_PACKS_DIR)
        return
    from engine.main import run
    run("my_pack")
```

### 7. Run it

```bash
pip install -e ./my-game
my-game           # terminal
my-game --web     # browser
```

---

## Challenge Types

### `quiz` — Multiple Choice

```python
Challenge(type="quiz", prompt="Which command lists files?",
          options=["ls", "cd", "pwd", "cat"], answer="a", xp=10)
```

### `fill_blank` — Free Text

```python
Challenge(type="fill_blank", prompt="The command ___ prints the working directory.",
          answer="pwd", xp=10)
```

### `flag_quiz` — Multiple Valid Answers

```python
Challenge(type="flag_quiz", prompt="What flag shows hidden files?",
          answers=["-a", "--all", "ls -a"], xp=15)
```

### `live` — Real Command in Sandbox

```python
Challenge(type="live", prompt="Create a directory named 'output'.",
          setup={"dirs": ["src"], "files": {"src/hello.txt": "hello\n"}},
          validation={"type": "dir_exists", "target": "output"}, xp=20)
```

**Validators:** `dir_exists`, `file_exists`, `file_missing`, `output_contains`, `file_contains`, `file_executable`, `file_perms`, `multi`

### `ordered` — Sequence Ordering

```python
Challenge(type="ordered", prompt="Put these git steps in order.",
          items=["commit", "add", "push", "init"], answer=[3, 1, 0, 2], xp=20)
```

### `arrange` — Matching Pairs

```python
Challenge(type="arrange", prompt="Match commands to descriptions.",
          pairs=[{"left": "ls", "right": "List files"}, ...], answer="A B C", xp=20)
```

---

## Campaign — Chaining Packs Into a Story

```python
from engine.campaign import Campaign, ChapterDef

CAMPAIGN = Campaign(
    id="my_campaign",
    title="The Full Journey",
    save_file_name="my_campaign",
    intro_story="Opening narrative...",
    final_story="Ending narrative...",
    chapters=[
        ChapterDef(pack_name="intro_pack", title="Chapter 1: Beginnings",
                   intro_bridge="Transition text...", outro_bridge="Outro text..."),
        ChapterDef(pack_name="advanced_pack", title="Chapter 2: The Deep End",
                   intro_bridge="Deeper...", outro_bridge="Complete."),
    ],
)
```

---

## In-Game Controls

```
[h] Hint          Show next hint for current challenge
[b] Bookmark      Toggle bookmark on current challenge
[d] Difficulty    Switch difficulty (Easy / Normal / Hard)
[?] Help          Full control reference
[s] Skip          Skip current challenge (costs a star)
[q] Menu          Return to main menu
```

---

## Requirements

- Python 3.10+
- `rich >= 13.0.0`
- Web mode: `fastapi`, `uvicorn`, `jinja2` (installed via `pip install 'quest-engine[web]'`)
- Postgres: `psycopg2-binary`, `bcrypt` (installed via `pip install 'quest-engine[postgres]'`)

---

## License

MIT
