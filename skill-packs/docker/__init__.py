"""
Docker Quest skill pack.
Theme: Container breach forensics — Containment Specialist auditing a
       compromised corporate microservices environment.
"""

from engine.skill_pack import SkillPack
from .story import (
    INTRO_STORY,
    ZONE_INTROS,
    ZONE_COMPLETIONS,
    BOSS_INTROS,
    ACHIEVEMENT_DESCRIPTIONS,
)
from .zones import ZONES, ZONE_ORDER

BANNER_ASCII = r"""
  ██████   ██████   ██████ ██   ██ ███████ ██████      ██████  ██    ██ ███████ ███████ ████████
  ██   ██ ██    ██ ██      ██  ██  ██      ██   ██    ██    ██ ██    ██ ██      ██         ██
  ██   ██ ██    ██ ██      █████   █████   ██████     ██    ██ ██    ██ █████   ███████    ██
  ██   ██ ██    ██ ██      ██  ██  ██      ██   ██    ██ ▄▄ ██ ██    ██ ██           ██    ██
  ██████   ██████   ██████ ██   ██ ███████ ██   ██     ██████   ██████  ███████ ███████    ██
                                                               ▀▀
"""

SKILL_PACK = SkillPack(
    id="docker",
    title="Docker Quest",
    subtitle="◈  Containment Specialist — Map Every Misconfiguration  ◈",
    save_file_name="docker_quest",
    intro_story=INTRO_STORY,
    quit_message="The containers are still running. The misconfigurations will wait.",
    zone_order=ZONE_ORDER,
    zones=ZONES,
    zone_intros=ZONE_INTROS,
    zone_completions=ZONE_COMPLETIONS,
    boss_intros=BOSS_INTROS,
    zone_achievement_map={
        "surface_layer":  "navigator",
        "image_vault":    "archivist",
        "container_grid": "seeker",
        "port_matrix":    "pipe_dream",
        "volume_sanctum": "necromancer",
        "network_forge":  "warden",
        "build_engine":   "scriptor",
        "compose_matrix": "networked",
        "registry_core":  "grandmaster",
    },
    achievements=ACHIEVEMENT_DESCRIPTIONS,
    banner_ascii=BANNER_ASCII,
)
