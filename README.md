# Quest Engine

A generic terminal RPG framework for building skill-based learning games. Powers [NEXUS Quest](https://github.com/thorski1/nexus-quest) and [The Young Lady's Illustrated Primer](https://github.com/thorski1/primer).

---

## Architecture

```
quest-engine/          ← this package (engine only)
  engine/
    engine.py          ← XP, levels, saves, achievements
    ui.py              ← all Rich TUI components
    challenges.py      ← quiz/fill-blank/live challenge runner
    skill_pack.py      ← SkillPack dataclass + load_skill_pack()
    campaign.py        ← Campaign dataclass + CampaignSession
    main.py            ← GameSession, entry points

your-game/             ← your package (content only)
  skill-packs/
    <name>/__init__.py ← exports SKILL_PACK = SkillPack(...)
  campaigns/
    <name>/__init__.py ← exports CAMPAIGN = Campaign(...)
  your_game/main.py    ← sets env vars, delegates to engine
```

Content directories resolve in this order:
1. Explicit argument `load_skill_pack(name, packs_dir=...)`
2. `QUEST_SKILL_PACKS_DIR` environment variable
3. `<repo-root>/skill-packs/` (monorepo fallback)

---

## Building a Game

### Define a skill pack

```python
# skill-packs/my_pack/__init__.py
from engine.skill_pack import SkillPack

SKILL_PACK = SkillPack(
    id="my_pack",
    title="My Pack",
    subtitle="A subtitle",
    save_file_name="my_pack",
    intro_story="Your story here...",
    quit_message="See you next time.",
    default_player_name="Player",
    zone_order=["zone_1"],
    zones={
        "zone_1": {
            "id": "zone_1",
            "name": "Zone One",
            "subtitle": "A description",
            "challenges": [
                {
                    "id": "q1",
                    "title": "Question 1",
                    "type": "quiz",
                    "question": "What is 2 + 2?",
                    "answer": "b",
                    "options": ["3", "4", "5", "6"],
                    "hints": ["Count on your fingers"],
                    "xp": 50,
                }
            ],
        }
    },
    zone_intros={"zone_1": "Welcome..."},
    zone_completions={"zone_1": "Complete!"},
    boss_intros={"zone_1": "Final challenge..."},
    zone_achievement_map={"zone_1": "zone_1_done"},
    achievements={"zone_1_done": ("Zone 1!", "Finished zone 1")},
)
```

### Challenge types

| type | answer format | description |
|------|---------------|-------------|
| `quiz` | `"answer": "b"` + `"options": [...]` | Multiple choice A/B/C/D |
| `fill_blank` | `"answer": "text"` | Type the answer |
| `quiz`/`flag_quiz` | `"answers": ["cmd", "-flag"]` | Free-text multi-answer |
| `live` | `"validation": {...}` | Run a real command in sandbox |

### Live challenge validators

```python
{"type": "dir_exists",     "target": "path/dir"}
{"type": "file_exists",    "target": "path/file"}
{"type": "file_missing",   "target": "path/file"}
{"type": "output_contains","expected": "text"}
{"type": "file_contains",  "target": "file", "expected": "text"}
{"type": "file_perms",     "target": "file", "expected_mode": "755"}
{"type": "multi",          "checks": [...]}
```

### Entry point pattern

```python
# my_game/main.py
import os
from pathlib import Path

_HERE = Path(__file__).parent.parent
os.environ.setdefault("QUEST_SKILL_PACKS_DIR", str(_HERE / "skill-packs"))
os.environ.setdefault("QUEST_CAMPAIGNS_DIR", str(_HERE / "campaigns"))

from engine.main import run, run_campaign

def main():
    run("my_pack")
```

---

## Install

```bash
git clone https://github.com/thorski1/quest-engine
pip install -e ./quest-engine
```

Or as a dependency in `pyproject.toml`:
```toml
dependencies = ["rich>=13.0.0", "quest-engine @ git+https://github.com/thorski1/quest-engine.git"]
```

---

## Requirements

- Python 3.10+
- `rich >= 13.0.0`

---

## Games Built on Quest Engine

| Game | Audience | Description |
|------|----------|-------------|
| [NEXUS Quest](https://github.com/thorski1/nexus-quest) | Adults | Cyberpunk hacker RPG — Bash, SSH, Vim, Git, Docker, Postgres |
| [The Primer](https://github.com/thorski1/primer) | Children | Letters, Numbers, Science, Kindness |
