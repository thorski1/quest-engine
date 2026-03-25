"""
engine.py - Generic game engine for Quest Engine
Manages state, XP, levels, progress, achievements.
All skill-specific data comes from the SkillPack.
"""

import datetime
import json
import time
from pathlib import Path

from .skill_pack import SkillPack

SAVE_BASE = Path.home() / ".quest_engine"

# Engine-level achievements available in every game
BASE_ACHIEVEMENTS = {
    "first_blood": ("First Steps", "Answered your very first challenge"),
    "streak_3": ("On a Roll", "3 correct answers in a row"),
    "streak_5": ("Hot Streak", "5 correct answers in a row"),
    "streak_10": ("Unstoppable", "10 correct answers in a row"),
    "speed_demon": ("Speed Demon", "Answered a challenge in under 5 seconds"),
    "no_hints": ("Standing Alone", "Completed a zone without using any hints"),
    "completionist": ("Completionist", "Completed every zone"),
    "level_10": ("Veteran", "Reached level 10"),
    "level_20": ("Expert", "Reached level 20"),
    "level_30": ("Grandmaster", "Reached the highest level"),
    "week_streak": ("Seven Days Strong", "Played for 7 consecutive days"),
    "month_streak": ("Committed", "Played for 30 consecutive days"),
    "daily_hero": ("Daily Hero", "Complete 7 consecutive daily challenges"),
}

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

        # Zone mastery: tracks accuracy and hints per zone
        self.zone_scores: dict = {}  # zone_id -> {"wrong": int, "hints": int}
        # Wrong answer journal: challenges the player has struggled with
        self.wrong_answer_journal: dict = {}  # zone_id -> [challenge_id, ...]
        # Daily streak: consecutive days played
        self.daily_streak: int = 0
        self.last_played_date: str = ""
        # Daily challenge tracking
        self.daily_challenge_completed: bool = False
        self.daily_challenge_date: str = ""
        self.daily_challenge_streak: int = 0
        self.last_daily_challenge_date: str = ""
        # Bookmarks: list of {"zone_id": str, "challenge_id": str}
        self.bookmarks: list = []
        # Difficulty mode: "normal" | "hard" | "easy"
        self.difficulty_mode: str = "normal"

        # Session stats (reset each run, not persisted)
        self.session_start: float = time.time()
        self.session_xp: int = 0
        self.session_correct: int = 0
        self.session_wrong: int = 0

        self._save_dir = SAVE_BASE / skill_pack.save_file_name
        self._save_file = self._save_dir / "progress.json"
        self.load()
        self._update_daily_streak()

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
                self.zone_scores = data.get("zone_scores", {})
                self.wrong_answer_journal = data.get("wrong_answer_journal", {})
                self.daily_streak = data.get("daily_streak", 0)
                self.last_played_date = data.get("last_played_date", "")
                self.daily_challenge_completed = data.get("daily_challenge_completed", False)
                self.daily_challenge_date = data.get("daily_challenge_date", "")
                self.daily_challenge_streak = data.get("daily_challenge_streak", 0)
                self.last_daily_challenge_date = data.get("last_daily_challenge_date", "")
                self.bookmarks = data.get("bookmarks", [])
                self.difficulty_mode = data.get("difficulty_mode", "normal")
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
            "zone_scores": self.zone_scores,
            "wrong_answer_journal": self.wrong_answer_journal,
            "daily_streak": self.daily_streak,
            "last_played_date": self.last_played_date,
            "daily_challenge_completed": self.daily_challenge_completed,
            "daily_challenge_date": self.daily_challenge_date,
            "daily_challenge_streak": self.daily_challenge_streak,
            "last_daily_challenge_date": self.last_daily_challenge_date,
            "bookmarks": self.bookmarks,
            "difficulty_mode": self.difficulty_mode,
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
        self.zone_scores = {}
        self.wrong_answer_journal = {}
        # Preserve daily streak, daily challenge streak and dates across resets
        self.daily_challenge_completed = False
        self.daily_challenge_date = ""
        self.session_xp = 0
        self.session_correct = 0
        self.session_wrong = 0
        self.session_start = time.time()
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
        if self.difficulty_mode == "hard":
            actual_xp = int(actual_xp * 1.5)
        elif self.difficulty_mode == "easy":
            actual_xp = int(actual_xp * 0.75)
        self.total_xp += actual_xp
        self.session_xp += actual_xp
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
        self.session_correct += 1
        self._check_streak_achievements()
        self.save()

    def record_incorrect(self):
        self.streak = 0
        self.session_wrong += 1
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

    # ── Zone Mastery ──────────────────────────────────────────────────────────

    def record_zone_attempt(self, zone_id: str, challenge_id: str, correct: bool, used_hint: bool = False):
        """Track per-challenge accuracy for zone mastery stars."""
        score = self.zone_scores.setdefault(zone_id, {"wrong": 0, "hints": 0, "wrong_ids": []})
        journal = self.wrong_answer_journal.setdefault(zone_id, [])

        if not correct:
            if challenge_id not in score.get("wrong_ids", []):
                score.setdefault("wrong_ids", []).append(challenge_id)
                score["wrong"] += 1
            if challenge_id not in journal:
                journal.append(challenge_id)
        else:
            # On correct answer, remove from struggle journal
            if challenge_id in journal:
                journal.remove(challenge_id)

        if used_hint:
            score["hints"] += 1

        self.save()

    def get_zone_stars(self, zone_id: str) -> int:
        """Return 0-3 stars for a zone. 0 = not completed."""
        if zone_id not in self.completed_zones:
            return 0
        score = self.zone_scores.get(zone_id, {"wrong": 0, "hints": 0})
        wrong = score.get("wrong", 0)
        hints = score.get("hints", 0)
        if wrong == 0 and hints == 0:
            return 3
        if wrong <= 1 and hints <= 2:
            return 2
        return 1

    def get_weak_zones(self) -> list:
        """Return zone_ids where the player has unanswered wrong questions."""
        return [
            zone_id for zone_id, entries in self.wrong_answer_journal.items()
            if entries
        ]

    def get_review_challenges(self, zone_id: str) -> list:
        """Return challenge dicts for all wrong-answer journal entries in a zone."""
        challenge_ids = self.wrong_answer_journal.get(zone_id, [])
        all_challenges = self.skill_pack.get_zone_challenges(zone_id)
        return [c for c in all_challenges if c["id"] in challenge_ids]

    # ── Daily Streak ──────────────────────────────────────────────────────────

    def _update_daily_streak(self):
        today = str(datetime.date.today())
        if self.last_played_date == today:
            return  # Already counted today
        yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
        if self.last_played_date == yesterday:
            self.daily_streak += 1
        elif self.last_played_date == "":
            self.daily_streak = 1
        else:
            self.daily_streak = 1  # Streak broken
        self.last_played_date = today
        if self.daily_streak >= 7:
            self.unlock_achievement("week_streak")
        if self.daily_streak >= 30:
            self.unlock_achievement("month_streak")
        self.save()

    # ── Daily Challenge ───────────────────────────────────────────────────────

    def get_daily_challenge(self, skill_pack=None) -> dict | None:
        """Pick a deterministic challenge for today based on date + pack name hash."""
        pack = skill_pack or self.skill_pack
        today = str(datetime.date.today())
        # Reset daily_challenge_completed if it's a new day
        if self.daily_challenge_date != today:
            self.daily_challenge_completed = False
            self.daily_challenge_date = today
            self.save()

        # Collect all challenges across all zones
        all_challenges = []
        for zone_id in pack.zone_order:
            zone = pack.get_zone(zone_id)
            if not zone:
                continue
            for ch in pack.get_zone_challenges(zone_id):
                ch_copy = dict(ch)
                ch_copy["_zone"] = zone
                all_challenges.append(ch_copy)

        if not all_challenges:
            return None

        key = today + pack.id
        idx = hash(key) % len(all_challenges)
        return all_challenges[idx]

    def complete_daily_challenge(self):
        """Mark daily challenge done, award 2x XP (min 100), update streak."""
        today = str(datetime.date.today())
        self.daily_challenge_completed = True
        self.daily_challenge_date = today
        self._update_daily_challenge_streak()
        if "daily_hero" not in self.achievements and self.daily_challenge_streak >= 7:
            self.unlock_achievement("daily_hero")
        self.save()

    def _update_daily_challenge_streak(self):
        today = str(datetime.date.today())
        yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
        if self.last_daily_challenge_date == today:
            return  # Already counted today
        if self.last_daily_challenge_date == yesterday:
            self.daily_challenge_streak += 1
        else:
            self.daily_challenge_streak = 1  # New streak or broken
        self.last_daily_challenge_date = today
        if self.daily_challenge_streak >= 7:
            self.unlock_achievement("daily_hero")
        self.save()

    # ── Pack Completion ───────────────────────────────────────────────────────

    def is_pack_complete(self, skill_pack=None) -> bool:
        """Return True if all zones in zone_order are in completed_zones."""
        pack = skill_pack or self.skill_pack
        return all(z in self.completed_zones for z in pack.zone_order)

    def get_completion_grade(self) -> str:
        """Return S/A/B/C/D based on average zone stars across completed zones."""
        completed = [z for z in self.skill_pack.zone_order if z in self.completed_zones]
        if not completed:
            return "D"
        avg = sum(self.get_zone_stars(z) for z in completed) / len(completed)
        if avg >= 3.0:
            return "S"
        if avg >= 2.5:
            return "A"
        if avg >= 2.0:
            return "B"
        if avg >= 1.5:
            return "C"
        return "D"

    # ── Session Stats ─────────────────────────────────────────────────────────

    def get_session_stats(self) -> dict:
        elapsed = time.time() - self.session_start
        total = self.session_correct + self.session_wrong
        accuracy = (self.session_correct / total * 100) if total > 0 else 0
        minutes = int(elapsed // 60)
        seconds = int(elapsed % 60)
        return {
            "xp_earned": self.session_xp,
            "correct": self.session_correct,
            "wrong": self.session_wrong,
            "total": total,
            "accuracy": accuracy,
            "time_str": f"{minutes}m {seconds}s" if minutes else f"{seconds}s",
            "daily_streak": self.daily_streak,
        }

    # ── Notes Export ──────────────────────────────────────────────────────────

    def export_notes(self) -> str:
        """Export all lessons from completed zones to a text file. Returns the path."""
        notes_path = self._save_dir / "notes.txt"
        lines = [
            f"═══════════════════════════════════════",
            f"  {self.skill_pack.title} — Study Notes",
            f"  Player: {self.player_name}",
            f"═══════════════════════════════════════",
            "",
        ]

        for zone_id in self.skill_pack.zone_order:
            if zone_id not in self.completed_zones:
                continue
            zone = self.skill_pack.get_zone(zone_id)
            if not zone:
                continue
            lines.append(f"── {zone['name'].upper()} ──")
            lines.append(zone.get("subtitle", ""))
            lines.append("")
            for challenge in self.skill_pack.get_zone_challenges(zone_id):
                lesson = challenge.get("lesson") or challenge.get("prompt", "")
                if lesson.strip():
                    lines.append(f"  [{challenge.get('title', challenge['id'])}]")
                    for ln in lesson.strip().splitlines():
                        lines.append(f"    {ln.strip()}")
                    lines.append("")
            lines.append("")

        self._save_dir.mkdir(parents=True, exist_ok=True)
        notes_path.write_text("\n".join(lines))
        return str(notes_path)

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
        if self.difficulty_mode == "easy":
            # Free hints in easy mode
            self.hint_costs_paid += 1
            self.save()
            return True
        cost = 10
        if self.difficulty_mode == "hard":
            cost = int(cost * 1.5)
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
            "daily_streak": self.daily_streak,
            "weak_zones": len(self.get_weak_zones()),
        }
