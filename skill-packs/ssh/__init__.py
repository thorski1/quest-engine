"""
SSH Quest skill pack.
Theme: Ghost navigates NEXUS's server infrastructure using SSH — tunnels,
       key chains, jump hosts, and agent forwarding to reach the deep network.
"""

from engine.skill_pack import SkillPack
from .story import INTRO_STORY, ZONE_INTROS, ZONE_COMPLETIONS, BOSS_INTROS, ACHIEVEMENT_DESCRIPTIONS
from .zones import ZONES, ZONE_ORDER

BANNER_ASCII = r"""
  ██████╗ ██████╗ ██╗  ██╗     ██████╗ ██╗   ██╗███████╗███████╗████████╗
 ██╔════╝██╔════╝ ██║  ██║    ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
 ╚█████╗ ╚█████╗ ███████║    ██║   ██║██║   ██║█████╗  ███████╗   ██║
  ╚═══██╗ ╚═══██╗██╔══██║    ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║
 ██████╔╝██████╔╝██║  ██║    ╚██████╔╝╚██████╔╝███████╗███████║   ██║
 ╚═════╝ ╚═════╝ ╚═╝  ╚═╝     ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝
"""

SKILL_PACK = SkillPack(
    id="ssh",
    title="SSH Quest",
    subtitle="◈  Remote Intrusion Specialist — Move Through the Network  ◈",
    save_file_name="ssh_quest",
    intro_story=INTRO_STORY,
    quit_message="The tunnels are still active. The jump chain is still open.",
    zone_order=ZONE_ORDER,
    zones=ZONES,
    zone_intros=ZONE_INTROS,
    zone_completions=ZONE_COMPLETIONS,
    boss_intros=BOSS_INTROS,
    zone_achievement_map={
        "connection_basics": "navigator",
        "key_vault":         "archivist",
        "config_matrix":     "seeker",
        "transfer_ops":      "pipe_dream",
        "tunnel_network":    "necromancer",
        "jump_chain":        "warden",
        "agent_protocol":    "scriptor",
        "hardening_core":    "grandmaster",
    },
    achievements=ACHIEVEMENT_DESCRIPTIONS,
    banner_ascii=BANNER_ASCII,
)
