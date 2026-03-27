# Quest Engine

```
  ██████╗ ██╗   ██╗███████╗███████╗████████╗
 ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
 ██║   ██║██║   ██║█████╗  ███████╗   ██║
 ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║
 ╚██████╔╝╚██████╔╝███████╗███████║   ██║
  ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝
```

A pluggable terminal RPG framework for building skill-based learning games.

**Powers:**
- [NEXUS Quest](https://github.com/thorski1/nexus-quest) — cyberpunk hacker RPG (Bash · SSH · Vim · Git · Docker · Postgres · Python · Regex · Linux · Kubernetes · AWS)
- [The Young Lady's Illustrated Primer](https://github.com/thorski1/primer) — children's educational adventure (Letters · Numbers · Science · Kindness · Geography · Math · History · Art · Coding)

---

## What Is This?

Quest Engine is the pure game loop — XP, levels, saves, difficulty, daily challenges, star ratings, achievements, bookmarks, zone previews, completion certificates. It has zero game content of its own.

You bring the content (zones and challenges). The engine handles everything else.

**Two play modes, zero config:**
- **Terminal (TUI)** — Rich-powered full-color terminal interface
- **Web** — FastAPI + HTMX browser interface with dual theming (cyberpunk / playful)

---

## Install

```bash
git clone https://github.com/thorski1/quest-engine
pip install -e ./quest-engine
```

For web mode:

```bash
pip install -e './quest-engine[web]'
```

**Requirements:** Python 3.10+, `rich >= 13.0.0`

---

## Web Mode

Quest Engine includes a built-in web interface. Any game built on it gets a browser UI for free by passing `--web` to its entry point:

```bash
nexus-quest --web      # opens http://localhost:8080
primer --web
```

The web server is a FastAPI app (`engine/web/server.py`) serving Jinja2 templates with HTMX for partial page updates — no JS build step, no webpack, no Node.

### Theming

The interface auto-selects a theme based on `SkillPack.kids_mode`:

| Theme | `kids_mode` | Colors | Font |
|-------|-------------|--------|------|
| `cyberpunk` | `False` | Dark navy · Neon green · Cyan | JetBrains Mono |
| `playful` | `True` | Warm cream · Purple · Rounded | Nunito |

### Adding Web Mode to Your Game

Add `--web` handling to your entry point:

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

### Vercel Deployment

Games can be deployed as serverless web apps on Vercel. See the `api/index.py` pattern in [nexus-quest](https://github.com/thorski1/nexus-quest) or [primer](https://github.com/thorski1/primer) for a reference implementation.

---

## Project Structure

Your game lives in its own repo alongside the engine:

```
quest-engine/               ← this package (engine only, no game content)
  engine/
    engine.py               ← XP, levels, saves, achievements, speed records
    ui.py                   ← all Rich TUI components
    challenges.py           ← quiz / fill-blank / live / ordered / arrange runner
    skill_pack.py           ← SkillPack dataclass + load_skill_pack()
    campaign.py             ← Campaign dataclass + CampaignSession
    zone.py                 ← Zone dict helper
    challenge.py            ← Challenge dict helper
    main.py                 ← run() and run_campaign() entry points

your-game/                  ← your repo (content only)
  skill-packs/
    bash/
      __init__.py           ← exports SKILL_PACK = SkillPack(...)
      zones.py              ← all zone and challenge data
      story.py              ← narrative text (intros, outros, story)
  campaigns/
    my_campaign/
      __init__.py           ← exports CAMPAIGN = Campaign(...)
      story.py              ← chapter bridges, entry summaries
  your_game/
    main.py                 ← sets env vars, calls run() or run_campaign()
  setup.cfg / pyproject.toml
```

---

## Quick Start: Your First Pack

### 1. Install the engine

```bash
pip install -e ./quest-engine
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
    "advanced_zone": Zone(
        id="advanced_zone",
        title="Advanced Topics",
        description="Going deeper.",
        challenges=[
            Challenge(
                id="q3",
                type="flag_quiz",
                prompt="Which flag shows hidden files with ls?",
                answers=["-a", "--all", "ls -a"],
                explanation="`ls -a` includes dotfiles (hidden files beginning with `.`).",
                hints=["The flag is a single letter.", "Think 'all'."],
                xp=15,
            ),
        ],
    ),
}
```

### 5. Write your narrative

**`skill-packs/my_pack/story.py`**

```python
INTRO_STORY = """
Your game's opening narrative. Shown once at the very beginning.
Can be multiple paragraphs. Supports Rich markup like [bold]bold[/bold].
"""

ZONE_INTROS = {
    "intro_zone": "Text shown when the player first enters this zone.",
    "advanced_zone": "Text shown when the player first enters the advanced zone.",
}

ZONE_COMPLETIONS = {
    "intro_zone": "Text shown when the player finishes all challenges in this zone.",
    "advanced_zone": "Well done — you've mastered the advanced zone.",
}

BOSS_INTROS = {
    "intro_zone": "Text shown before the final challenge in the zone.",
    "advanced_zone": "This is the hardest challenge yet.",
}
```

### 6. Define your SkillPack

**`skill-packs/my_pack/__init__.py`**

```python
from engine.skill_pack import SkillPack
from .story import INTRO_STORY, ZONE_INTROS, ZONE_COMPLETIONS, BOSS_INTROS
from .zones import ZONES, ZONE_ORDER

SKILL_PACK = SkillPack(
    id="my_pack",
    title="My Pack",
    subtitle="◈  My Subtitle  ◈",
    save_file_name="my_pack",
    intro_story=INTRO_STORY,
    quit_message="Come back soon.",
    zone_order=ZONE_ORDER,
    zones=ZONES,
    zone_intros=ZONE_INTROS,
    zone_completions=ZONE_COMPLETIONS,
    boss_intros=BOSS_INTROS,
    zone_achievement_map={
        "intro_zone": "intro_done",
        "advanced_zone": "advanced_done",
    },
    achievements={
        "intro_done":    ("First Steps",      "Completed the intro zone"),
        "advanced_done": ("Going Deep",       "Mastered the advanced zone"),
    },
    level_titles=[
        (1,  "Novice"),
        (5,  "Learner"),
        (10, "Scholar"),
        (15, "Expert"),
        (20, "Master"),
    ],
    banner_ascii=r"""
 __  ____   __  ____  _   _  ___  _  _
 \ \/ /\ \ / / |  _ \| | | |/ _ \| \| |
  >  <  \ V /  | |_) | |_| | (_) | .` |
 /_/\_\  \_/   |____/ \___/ \___/|_|\_|
""",
)
```

### 7. Wire up setup.cfg

**`setup.cfg`**

```ini
[metadata]
name = my-game
version = 0.1.0

[options]
install_requires =
    quest-engine

[options.entry_points]
console_scripts =
    my-game = your_game.main:main
```

### 8. Run it

```bash
pip install -e ./my-game
my-game
```

---

## Challenge Types — Full Reference

### `quiz` — Multiple Choice

The player types A / B / C / D (or the option text, or 1/2/3/4).

```python
Challenge(
    id="q1",
    type="quiz",
    prompt="Which command lists directory contents?",
    options=["ls", "cd", "pwd", "cat"],
    answer="a",                           # correct option letter (a/b/c/d)
    explanation="ls lists files and directories in the current directory.",
    hints=["Think 'list'.", "Two letters."],
    xp=10,
    difficulty="easy",                    # easy / medium / hard / boss
)
```

### `fill_blank` — Free Text Answer

The player types the exact answer (case-insensitive).

```python
Challenge(
    id="q2",
    type="fill_blank",
    prompt="The command ___ prints the current working directory.",
    answer="pwd",
    explanation="pwd stands for Print Working Directory.",
    hints=["Three letters.", "P-W-D."],
    xp=10,
)
```

### `flag_quiz` — Multiple Valid Answers

Accepts any entry from the `answers` list. Great for command flags where `ls -a` and `-a` are both valid.

```python
Challenge(
    id="q3",
    type="flag_quiz",
    prompt="What flag shows hidden files with ls?",
    answers=["-a", "--all", "ls -a", "ls --all"],
    explanation="`-a` includes dotfiles. `ls -a` also accepted.",
    hints=["Single letter flag.", "Think 'all'."],
    xp=15,
)
```

### `live` — Real Command in Sandbox

The player runs an actual shell command. The engine creates a temp directory, runs the command in it, and validates the result.

```python
Challenge(
    id="q4",
    type="live",
    prompt="Create a directory named 'output' inside the sandbox.",
    explanation="mkdir creates a new directory: `mkdir output`",
    hints=["Use mkdir.", "mkdir output"],
    xp=20,
    setup={
        "dirs": ["src"],                              # pre-created directories
        "files": {
            "src/hello.txt": "hello world\n",        # pre-created files
        },
    },
    validation={"type": "dir_exists", "target": "output"},
)
```

**Available validators:**

| type | fields | passes when |
|------|--------|-------------|
| `dir_exists` | `target` | directory exists in sandbox |
| `file_exists` | `target` | file exists in sandbox |
| `file_missing` | `target` | file does NOT exist |
| `output_contains` | `expected` | stdout or stderr contains expected string |
| `file_contains` | `target`, `expected` | file content contains expected string |
| `file_executable` | `target` | file has execute bit set |
| `file_perms` | `target`, `expected_mode` | file permissions match (e.g. `"755"`) |
| `multi` | `checks: [...]` | all nested validators pass |

### `ordered` — Sequence Ordering

The player types the correct order of steps as a space-separated number sequence.

```python
Challenge(
    id="q5",
    type="ordered",
    prompt="Put these git steps in order: commit, add, push, init",
    items=["git commit -m 'msg'", "git add .", "git push", "git init"],
    # correct order is: init(3), add(1), commit(0), push(2) — 0-based indices
    answer=[3, 1, 0, 2],
    explanation="init → add → commit → push is the correct git workflow.",
    xp=20,
)
```

### `arrange` — Matching Pairs

The player matches left items to right items using letters.

```python
Challenge(
    id="q6",
    type="arrange",
    prompt="Match each command to its purpose.",
    pairs=[
        {"left": "ls",    "right": "List files"},
        {"left": "cd",    "right": "Change directory"},
        {"left": "pwd",   "right": "Print working directory"},
    ],
    # right items may be shuffled for display; answer reflects the correct mapping
    answer="A B C",
    explanation="ls=List, cd=Change, pwd=Print.",
    xp=20,
)
```

---

## SkillPack — Full Field Reference

```python
SkillPack(
    # Required
    id="my_pack",                   # unique string identifier
    title="My Pack",                # display title
    zone_order=["zone_1", ...],     # ordered list of zone IDs
    zones={                         # dict of zone_id → zone dict
        "zone_1": {
            "id": "zone_1",
            "name": "Zone Display Name",    # shown in UI
            "description": "...",           # shown in zone preview
            "challenges": [...],            # list of challenge dicts
        },
    },

    # Narrative text
    intro_story="...",              # shown once at start
    zone_intros={"zone_1": "..."},  # shown on first entry to each zone
    zone_completions={"zone_1": "..."},  # shown on zone complete
    boss_intros={"zone_1": "..."},       # shown before last challenge

    # Save / display
    save_file_name="my_pack",       # filename (no spaces) for JSON save
    subtitle="◈  Tagline  ◈",       # shown under banner
    quit_message="See you later.",  # shown on quit
    default_player_name="Agent",    # default name if player skips input

    # Achievements
    zone_achievement_map={"zone_1": "achievement_id"},
    achievements={
        "achievement_id": ("Short Title", "Longer description"),
    },

    # Progression
    level_titles=[
        (1,  "Novice"),             # (min_level, title)
        (5,  "Learner"),
        (10, "Expert"),
    ],

    # Display
    banner_ascii=r"...",            # raw string ASCII art for banner
    kids_mode=False,                # True → kid-friendly praise phrases

    # Optional advanced
    recommended_age="8+",           # informational only
)
```

---

## Campaign — Chaining Packs Into a Story

A Campaign sequences SkillPacks into chapters with connecting narrative.

**`campaigns/my_campaign/__init__.py`**

```python
from engine.campaign import Campaign, ChapterDef

CAMPAIGN = Campaign(
    id="my_campaign",
    title="The Full Journey",
    save_file_name="my_campaign",
    intro_story="The opening of your campaign...",
    final_story="The ending, shown after the last chapter.",
    quit_message="Your journey continues...",
    entry_summary_prefix="Last time, you...",
    campaign_achievements={
        "campaign_complete": ("Journey's End", "Finished all chapters"),
    },
    chapters=[
        ChapterDef(
            pack_name="intro_pack",         # must match SkillPack.id
            title="Chapter 1: Beginnings",
            entry_summary="You are just starting out.",
            intro_bridge="Transition text shown before this chapter starts.",
            outro_bridge="Text shown after this chapter ends, before the next begins.",
            recommended_age="8+",           # optional
        ),
        ChapterDef(
            pack_name="advanced_pack",
            title="Chapter 2: The Deep End",
            entry_summary="Having mastered the basics, you push further.",
            intro_bridge="You descend into the advanced section...",
            outro_bridge="You have completed the journey.",
        ),
    ],
)
```

**Entry point:**

```python
from engine.main import run_campaign

def main():
    run_campaign("my_campaign")   # loads CAMPAIGN from campaigns/my_campaign/__init__.py
```

---

## Zone Helper — `engine.zone.Zone`

`Zone` is a `dict` subclass. Use it instead of plain dicts for cleaner zone definitions.

```python
from engine.zone import Zone

Zone(
    id="zone_1",
    title="Zone One",           # maps to dict key "name" (what the engine reads)
    description="...",
    challenges=[...],
    # Optional display fields:
    color="cyan",
    icon="⚡",
    subtitle="Subheader",
)
```

---

## Challenge Helper — `engine.challenge.Challenge`

`Challenge` is a `dict` subclass. Use it for cleaner challenge definitions.

```python
from engine.challenge import Challenge

Challenge(
    id="ch_1",
    type="quiz",                 # quiz / fill_blank / flag_quiz / live / ordered / arrange
    prompt="...",                # maps to dict key "question" (what the engine reads)
    explanation="...",           # maps to dict key "lesson"
    answer="b",                  # for quiz/fill_blank
    answers=["-a", "--all"],     # for flag_quiz (multiple valid answers)
    options=["A", "B", "C", "D"],
    hints=["Hint 1", "Hint 2"],
    xp=10,
    difficulty="medium",         # easy / medium / hard / boss
    # For live challenges:
    setup={"dirs": [...], "files": {...}},
    validation={"type": "output_contains", "expected": "hello"},
    # For ordered challenges:
    items=["step A", "step B", "step C"],
    # For arrange challenges:
    pairs=[{"left": "cmd", "right": "description"}],
)
```

---

## Engine Features

| Feature | Description |
|---------|-------------|
| **XP & Levels** | Configurable `level_titles` per pack; XP scales with difficulty |
| **Star Ratings** | 1–3 stars per zone based on hints used and challenges skipped |
| **Achievements** | Auto-unlocked when zone is completed; displayed in stats |
| **Daily Challenge** | Deterministic pick per pack per day; 2× XP; streak tracking |
| **Difficulty Modes** | Easy (0.75× XP, free hints) / Normal / Hard (1.5× XP) |
| **Speed Records** | Per-challenge personal bests; new-record flash on screen |
| **Bookmarks** | Toggle with `[b]`; review from main menu |
| **Zone Preview** | Challenge list shown before entering zone |
| **Help Screen** | Full keybinding reference via `[?]` |
| **Completion Certificate** | ASCII grade art (S/A/B/C/D) on pack complete |
| **Campaign Stats** | Per-chapter star ratings, XP totals, overall grade |
| **Kids Mode** | `kids_mode=True` → kid-friendly praise pool and gentler UX |
| **Save/Resume** | JSON saves in `~/.quest_engine/<save_file_name>/` |
| **Placement Quiz** | Campaign can start with optional assessment to pick chapter |

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

## Games Built on Quest Engine

| Game | Audience | Chapters | What You Learn |
|------|----------|----------|----------------|
| [NEXUS Quest](https://github.com/thorski1/nexus-quest) | Adults / Developers | 11 | Bash · SSH · Vim · Git · Docker · Postgres · Python · Regex · Linux · Kubernetes · AWS |
| [The Primer](https://github.com/thorski1/primer) | Children (5–12) | 9 | Letters · Numbers · Science · Kindness · Geography · Math · History · Art · Coding |

---

## Requirements

- Python 3.10+
- `rich >= 13.0.0`

---

## License

MIT
