"""
engine.py - Generic game engine for Quest Engine
Manages state, XP, levels, progress, achievements.
All skill-specific data comes from the SkillPack.
"""

import json
import time
from pathlib import Path

from .skill_pack import SkillPack

SAVE_BASE = Path.home() / ".quest_engine"

LEVEL_TITLES = {
    range(1, 6): "Apprentice",
    range(6, 11): "Journeyman",
    range(11, 16): "Adept",
    range(16, 21): "Expert",
    range(21, 26): "Master",
    range(26, 31): "Grandmaster",
}

XP_PER_LEVEL = 300


def get_level_title(level: int) -> str:
    for level_range, title in LEVEL_TITLES.items():
        if level in level_range:
            return title
    return "Grandmaster"


def xp_for_level(level: int) -> int:
    return (level - 1) * XP_PER_LEVEL


def level_from_xp(total_xp: int) -> int:
    level = 1 + total_xp // XP_PER_LEVEL
    return min(level, 30)


def xp_in_current_level(total_xp: int) -> int:
    level = level_from_xp(total_xp)
    return total_xp - xp_for_level(level)


class GameEngine:
    def __init__(self, skill_pack: SkillPack):
        self.skill_pack = skill_pack
        self.player_name = "Ghost"
        self.total_xp = 0
        self.streak = 0
        self.max_streak = 0
        self.current_zone = skill_pack.zone_order[0]
        self.completed_challenges = {}  # zone_id -> set of challenge ids
        self.completed_zones = set()
        self.achievements = set()
        self.hint_costs_paid = 0
        self.challenge_start_time = None
        self.new_achievements = []
        self._prev_level = 1

        self._save_dir = SAVE_BASE / skill_pack.save_file_name
        self._save_file = self._save_dir / "progress.json"
        self.load()

    # ── Persistence ──────────────────────────────────────────────────────────

    def load(self):
        if self._save_file.exists():
            try:
                with open(self._save_file, "r") as f:
                    data = json.load(f)
                self.player_name = data.get("player_name", "Ghost")
                self.total_xp = data.get("total_xp", 0)
                self.streak = data.get("streak", 0)
                self.max_streak = data.get("max_streak", 0)
                self.current_zone = data.get("current_zone", self.skill_pack.zone_order[0])
                raw_cc = data.get("completed_challenges", {})
                self.completed_challenges = {k: set(v) for k, v in raw_cc.items()}
                self.completed_zones = set(data.get("completed_zones", []))
                self.achievements = set(data.get("achievements", []))
                self.hint_costs_paid = data.get("hint_costs_paid", 0)
                self._prev_level = self.level
            except (json.JSONDecodeError, KeyError):
                pass

    def save(self):
        self._save_dir.mkdir(parents=True, exist_ok=True)
        data = {
            "player_name": self.player_name,
            "total_xp": self.total_xp,
            "streak": self.streak,
            "max_streak": self.max_streak,
            "current_zone": self.current_zone,
            "completed_challenges": {k: list(v) for k, v in self.completed_challenges.items()},
            "completed_zones": list(self.completed_zones),
            "achievements": list(self.achievements),
            "hint_costs_paid": self.hint_costs_paid,
        }
        with open(self._save_file, "w") as f:
            json.dump(data, f, indent=2)

    def reset(self):
        self.player_name = "Ghost"
        self.total_xp = 0
        self.streak = 0
        self.max_streak = 0
        self.current_zone = self.skill_pack.zone_order[0]
        self.completed_challenges = {}
        self.completed_zones = set()
        self.achievements = set()
        self.hint_costs_paid = 0
        self.new_achievements = []
        self._prev_level = 1
        self.save()

    # ── Properties ───────────────────────────────────────────────────────────

    @property
    def level(self) -> int:
        return level_from_xp(self.total_xp)

    @property
    def level_title(self) -> str:
        return get_level_title(self.level)

    @property
    def xp_this_level(self) -> int:
        return xp_in_current_level(self.total_xp)

    @property
    def xp_for_next_level(self) -> int:
        return XP_PER_LEVEL

    @property
    def level_progress_pct(self) -> float:
        return min(self.xp_this_level / XP_PER_LEVEL, 1.0)

    # ── XP & Leveling ────────────────────────────────────────────────────────

    def calculate_xp_gain(self, base_xp: int) -> int:
        multiplier = 1.0
        if self.streak >= 10:
            multiplier = 2.0
        elif self.streak >= 5:
            multiplier = 1.5
        elif self.streak >= 3:
            multiplier = 1.25
        return int(base_xp * multiplier)

    def award_xp(self, base_xp: int) -> tuple:
        prev_level = self.level
        actual_xp = self.calculate_xp_gain(base_xp)
        self.total_xp += actual_xp
        leveled_up = self.level > prev_level
        if leveled_up:
            self._check_level_achievements()
        self.save()
        return actual_xp, leveled_up

    def deduct_xp(self, amount: int):
        self.total_xp = max(0, self.total_xp - amount)
        self.save()

    # ── Streak ───────────────────────────────────────────────────────────────

    def record_correct(self):
        self.streak += 1
        self.max_streak = max(self.max_streak, self.streak)
        self._check_streak_achievements()
        self.save()

    def record_incorrect(self):
        self.streak = 0
        self.save()

    # ── Challenges & Zones ───────────────────────────────────────────────────

    def mark_challenge_complete(self, zone_id: str, challenge_id: str):
        if zone_id not in self.completed_challenges:
            self.completed_challenges[zone_id] = set()
        self.completed_challenges[zone_id].add(challenge_id)
        total_done = sum(len(v) for v in self.completed_challenges.values())
        if total_done == 1:
            self.unlock_achievement("first_blood")
        self.save()

    def is_challenge_complete(self, zone_id: str, challenge_id: str) -> bool:
        return challenge_id in self.completed_challenges.get(zone_id, set())

    def mark_zone_complete(self, zone_id: str):
        self.completed_zones.add(zone_id)
        ach = self.skill_pack.zone_achievement_map.get(zone_id)
        if ach:
            self.unlock_achievement(ach)
        if len(self.completed_zones) == len(self.skill_pack.zone_order):
            self.unlock_achievement("completionist")
        self.save()

    def is_zone_complete(self, zone_id: str) -> bool:
        return zone_id in self.completed_zones

    def is_zone_unlocked(self, zone_id: str) -> bool:
        if zone_id == self.skill_pack.zone_order[0]:
            return True
        idx = self.skill_pack.zone_order.index(zone_id)
        prev_zone = self.skill_pack.zone_order[idx - 1]
        return prev_zone in self.completed_zones

    def get_unlocked_zones(self) -> list:
        return [z for z in self.skill_pack.zone_order if self.is_zone_unlocked(z)]

    def challenges_completed_in_zone(self, zone_id: str) -> set:
        return self.completed_challenges.get(zone_id, set())

    # ── Achievements ─────────────────────────────────────────────────────────

    def unlock_achievement(self, achievement_id: str):
        if achievement_id not in self.achievements:
            self.achievements.add(achievement_id)
            self.new_achievements.append(achievement_id)
            self.save()

    def _check_streak_achievements(self):
        if self.streak >= 10:
            self.unlock_achievement("streak_10")
        elif self.streak >= 5:
            self.unlock_achievement("streak_5")
        elif self.streak >= 3:
            self.unlock_achievement("streak_3")

    def _check_level_achievements(self):
        lvl = self.level
        if lvl >= 30:
            self.unlock_achievement("level_30")
        elif lvl >= 20:
            self.unlock_achievement("level_20")
        elif lvl >= 10:
            self.unlock_achievement("level_10")

    def pop_new_achievements(self) -> list:
        ach = list(self.new_achievements)
        self.new_achievements = []
        return ach

    # ── Timer ─────────────────────────────────────────────────────────────────

    def start_challenge_timer(self):
        self.challenge_start_time = time.time()

    def get_elapsed(self) -> float:
        if self.challenge_start_time is None:
            return 0.0
        return time.time() - self.challenge_start_time

    def check_speed_achievement(self):
        elapsed = self.get_elapsed()
        if elapsed > 0 and elapsed < 5:
            self.unlock_achievement("speed_demon")

    # ── Hints ─────────────────────────────────────────────────────────────────

    def pay_hint_cost(self) -> bool:
        cost = 10
        if self.total_xp >= cost:
            self.deduct_xp(cost)
            self.hint_costs_paid += 1
            self.save()
            return True
        return False

    # ── Statistics ───────────────────────────────────────────────────────────

    def total_challenges_completed(self) -> int:
        return sum(len(v) for v in self.completed_challenges.values())

    def get_stats_dict(self) -> dict:
        return {
            "name": self.player_name,
            "level": self.level,
            "title": self.level_title,
            "total_xp": self.total_xp,
            "xp_this_level": self.xp_this_level,
            "xp_for_next_level": self.xp_for_next_level,
            "streak": self.streak,
            "max_streak": self.max_streak,
            "current_zone": self.current_zone,
            "zones_completed": len(self.completed_zones),
            "challenges_completed": self.total_challenges_completed(),
            "achievements_count": len(self.achievements),
        }
