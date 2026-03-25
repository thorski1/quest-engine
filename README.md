# Quest Engine

A pluggable terminal RPG framework for building skill-based learning games.

Powers [NEXUS Quest](https://github.com/thorski1/nexus-quest) (cyberpunk hacker RPG) and [The Young Lady's Illustrated Primer](https://github.com/thorski1/primer) (children's educational adventure).

---

## Architecture

```
quest-engine/               <- this package (engine only, no game content)
  engine/
    engine.py               <- XP, levels, saves, achievements, speed records
    ui.py                   <- all Rich TUI components
    challenges.py           <- quiz / fill-blank / live / ordered / arrange runner
    skill_pack.py           <- SkillPack dataclass + load_skill_pack()
    campaign.py             <- Campaign dataclass + CampaignSession
    main.py                 <- GameSession entry points

your-game/                  <- your package (content only)
  skill-packs/
    <name>/__init__.py      <- exports SKILL_PACK = SkillPack(...)
  campaigns/
    <name>/__init__.py      <- exports CAMPAIGN = Campaign(...)
```

---

## Building a Skill Pack

```python
from engine.skill_pack import SkillPack

SKILL_PACK = SkillPack(
    id="my_pack",
    title="My Pack",
    subtitle="A tagline",
    save_file_name="my_pack",
    intro_story="Your story here...",
    quit_message="See you next time.",
    default_player_name="Player",
    zone_order=["zone_1"],
    zones={"zone_1": {"id": "zone_1", "name": "Zone One", "challenges": [...]}},
    zone_intros={"zone_1": "Welcome..."},
    zone_completions={"zone_1": "Complete!"},
    boss_intros={"zone_1": "Final challenge..."},
    zone_achievement_map={"zone_1": "zone_1_done"},
    achievements={"zone_1_done": ("Zone 1!", "Finished zone 1")},
    # Optional:
    kids_mode=False,            # True -> kid-friendly praise phrases
    level_titles=[(1,"Rookie"),(6,"Operative"),(11,"Shadow")],
    banner_ascii=r"...",
)
```

---

## Challenge Types

| type | format | description |
|------|--------|-------------|
| `quiz` | `"answer": "b"` + `"options": [...]` | Multiple choice A/B/C/D |
| `fill_blank` | `"answer": "text"` | Type the exact answer |
| `flag_quiz` | `"answers": ["-flag", "--option"]` | Accept multiple valid forms |
| `live` | `"setup": {...}, "validation": {...}` | Run real command in sandbox |
| `ordered` | `"items": [...], "answer": [2,0,3,1]` | Arrange steps in sequence |
| `arrange` | `"pairs": [...], "answer": "B A C"` | Match left items to right by letter |

### Live Challenge Validators

```python
{"type": "dir_exists",      "target": "path/dir"}
{"type": "file_exists",     "target": "path/file"}
{"type": "file_missing",    "target": "path/file"}
{"type": "output_contains", "expected": "text"}
{"type": "file_contains",   "target": "file", "expected": "text"}
{"type": "file_executable", "target": "file"}
{"type": "file_perms",      "target": "file", "expected_mode": "755"}
{"type": "multi",           "checks": [...]}
```

---

## Engine Features

| Feature | Description |
|---------|-------------|
| **XP & Levels** | Configurable per-pack level titles; generic fallback |
| **Star Ratings** | 1-3 stars per zone based on hints used and skips |
| **Achievements** | Unlocked automatically; shown in stats panel |
| **Daily Challenge** | Deterministic daily pick per pack; 2x XP; streak tracking |
| **Difficulty Modes** | Easy (0.75x XP, free hints) / Normal / Hard (1.5x XP) |
| **Speed Records** | Per-challenge personal bests; new-record flash |
| **Bookmarks** | Toggle with `[b]`; review from main menu |
| **Zone Preview** | Challenge list shown before entering zone |
| **Help Screen** | Full keybinding reference via `[?]` |
| **Completion Certificate** | ASCII grade art (S/A/B/C/D) on pack complete |
| **Campaign Stats** | Per-chapter star ratings, XP, overall grade |
| **Kids Mode** | `kids_mode=True` -> kid-friendly praise pool and UX |
| **Save/Resume** | JSON saves in `~/.quest_engine/<save_file_name>/` |

---

## Building a Campaign

```python
from engine.campaign import Campaign, ChapterDef

CAMPAIGN = Campaign(
    id="my_campaign",
    title="My Campaign",
    save_file_name="my_campaign",
    intro_story="...",
    final_story="...",
    quit_message="...",
    entry_summary_prefix="Previously...",
    campaign_achievements={"campaign_complete": ("Title", "Description")},
    chapters=[
        ChapterDef(
            pack_name="my_pack",
            title="Chapter One",
            intro_bridge="...",
            outro_bridge="...",
            entry_summary="...",
        ),
    ],
)
```

---

## Install

```bash
git clone https://github.com/thorski1/quest-engine
pip install -e ./quest-engine
```

---

## Requirements

- Python 3.10+
- `rich >= 13.0.0`

---

## Games Built on Quest Engine

| Game | Audience | Chapters | Content |
|------|----------|----------|---------|
| [NEXUS Quest](https://github.com/thorski1/nexus-quest) | Adults | 8 | Bash · SSH · Vim · Git · Docker · Postgres · Python · Regex |
| [The Primer](https://github.com/thorski1/primer) | Children | 7 | Letters · Numbers · Science · Kindness · Geography · Math · Coding |
