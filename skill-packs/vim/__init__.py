"""
Vim Quest skill pack.
Theme: Ghost is twelve hops deep in the NEXUS network with only vim available.
       No GUI. No nano. Learn the editor or lose the mission.
"""

from engine.skill_pack import SkillPack
from .story import INTRO_STORY, ZONE_INTROS, ZONE_COMPLETIONS, BOSS_INTROS, ACHIEVEMENT_DESCRIPTIONS
from .zones import ZONES, ZONE_ORDER

BANNER_ASCII = r"""
 ██╗   ██╗██╗███╗   ███╗     ██████╗ ██╗   ██╗███████╗███████╗████████╗
 ██║   ██║██║████╗ ████║    ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
 ██║   ██║██║██╔████╔██║    ██║   ██║██║   ██║█████╗  ███████╗   ██║
 ╚██╗ ██╔╝██║██║╚██╔╝██║    ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║
  ╚████╔╝ ██║██║ ╚═╝ ██║    ╚██████╔╝╚██████╔╝███████╗███████║   ██║
   ╚═══╝  ╚═╝╚═╝     ╚═╝     ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝
"""

SKILL_PACK = SkillPack(
    id="vim",
    title="Vim Quest",
    subtitle="◈  Deep in the Network — No GUI, No Escape  ◈",
    save_file_name="vim_quest",
    intro_story=INTRO_STORY,
    quit_message="The editor is still open. The files are still there.",
    zone_order=ZONE_ORDER,
    zones=ZONES,
    zone_intros=ZONE_INTROS,
    zone_completions=ZONE_COMPLETIONS,
    boss_intros=BOSS_INTROS,
    zone_achievement_map={
        "normal_vault":    "navigator",
        "insert_protocol": "archivist",
        "command_line":    "seeker",
        "visual_mode":     "pipe_dream",
        "search_engine":   "necromancer",
        "motion_objects":  "warden",
        "split_network":   "scriptor",
        "macro_forge":     "grandmaster",
    },
    achievements=ACHIEVEMENT_DESCRIPTIONS,
    banner_ascii=BANNER_ASCII,
)
