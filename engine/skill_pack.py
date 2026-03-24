"""
skill_pack.py - SkillPack contract for Quest Engine
Each skill pack (bash, postgres, etc.) creates a SkillPack instance
that the engine loads at startup.
"""

from dataclasses import dataclass, field
from typing import Optional, Type


@dataclass
class SkillPack:
    # Identity
    id: str                          # "bash" | "postgres"
    title: str                       # "Terminal Quest"
    subtitle: str                    # Tagline shown in banner
    save_file_name: str              # used for ~/.quest_engine/<save_file_name>/progress.json

    # Narrative
    intro_story: str                 # Shown on new game
    quit_message: str                # Shown on exit

    # Zone structure
    zone_order: list                 # Ordered list of zone IDs
    zones: dict                      # zone_id -> zone data dict (matches ZoneData shape)
    zone_intros: dict                # zone_id -> intro text (Rich markup)
    zone_completions: dict           # zone_id -> completion text (Rich markup)
    boss_intros: dict                # zone_id -> boss intro text
    zone_achievement_map: dict       # zone_id -> achievement_id

    # Achievements: id -> (display_name, description)
    achievements: dict

    # Optional: custom challenge runner class (default: ChallengeRunner from challenges.py)
    # Must be a class with the same interface as ChallengeRunner.
    runner_class: Optional[Type] = None

    # Optional: ASCII art banner (falls back to engine default)
    banner_ascii: Optional[str] = None

    # Optional: name prompt shown on new game (Rich markup string)
    name_prompt: Optional[str] = None

    # Default player name when player enters nothing at the name prompt
    default_player_name: str = "Ghost"

    def get_zone(self, zone_id: str) -> dict:
        return self.zones.get(zone_id, {})

    def get_all_zones(self) -> list:
        return [self.zones[z] for z in self.zone_order if z in self.zones]

    def get_zone_challenges(self, zone_id: str) -> list:
        return self.zones.get(zone_id, {}).get("challenges", [])


def load_skill_pack(name: str, *, packs_dir=None) -> SkillPack:
    """Dynamically import a skill pack by name from the skill-packs directory.

    Resolution order for the packs directory:
      1. explicit packs_dir argument
      2. QUEST_SKILL_PACKS_DIR environment variable
      3. <repo-root>/skill-packs/ (default for the monorepo layout)
    """
    import importlib
    import os
    import sys
    from pathlib import Path

    if packs_dir is None:
        env_dir = os.environ.get("QUEST_SKILL_PACKS_DIR")
        packs_dir = Path(env_dir) if env_dir else Path(__file__).parent.parent / "skill-packs"
    else:
        packs_dir = Path(packs_dir)

    skill_packs_dir = packs_dir
    pack_path = skill_packs_dir / name / "__init__.py"

    if not pack_path.exists():
        available = [p.name for p in skill_packs_dir.iterdir() if p.is_dir() and (p / "__init__.py").exists()]
        raise ValueError(
            f"Skill pack '{name}' not found.\n"
            f"Available skill packs: {', '.join(sorted(available))}"
        )

    # Use spec_from_file_location to load by absolute path, avoiding name
    # conflicts with Python built-in modules (e.g. a pack named "numbers").
    import importlib.util
    module_name = f"_quest_pack_{name}"
    spec = importlib.util.spec_from_file_location(
        module_name,
        pack_path,
        submodule_search_locations=[str(skill_packs_dir / name)],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    # Also register as the bare name so relative imports inside the pack work
    sys.modules[name] = module
    if str(skill_packs_dir) not in sys.path:
        sys.path.insert(0, str(skill_packs_dir))
    spec.loader.exec_module(module)

    if not hasattr(module, "SKILL_PACK"):
        raise ImportError(f"Skill pack '{name}' must export a SKILL_PACK instance.")
    pack = module.SKILL_PACK
    if not isinstance(pack, SkillPack):
        raise TypeError(f"SKILL_PACK in '{name}' must be a SkillPack instance.")
    return pack
