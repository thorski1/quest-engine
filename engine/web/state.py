"""
state.py — Web session state for quest-engine web mode.

WebGameSession wraps GameEngine + ChallengeRunner for request-driven
(non-blocking) play. One session per skill pack per server instance.
"""

from __future__ import annotations

import random
from typing import Optional

from ..challenges import ChallengeRunner
from ..engine import GameEngine
from ..skill_pack import SkillPack


class AnswerResult:
    def __init__(
        self,
        correct: bool,
        message: str,
        xp: int = 0,
        actual_xp: int = 0,
        level_up: bool = False,
        level: int = 1,
        level_title: str = "",
        streak: int = 0,
        new_achievements: list | None = None,
        zone_complete: bool = False,
        pack_complete: bool = False,
        next_zone_id: str | None = None,
    ):
        self.correct = correct
        self.message = message
        self.xp = xp
        self.actual_xp = actual_xp
        self.level_up = level_up
        self.level = level
        self.level_title = level_title
        self.streak = streak
        self.new_achievements = new_achievements or []
        self.zone_complete = zone_complete
        self.pack_complete = pack_complete
        self.next_zone_id = next_zone_id


class WebGameSession:
    """Manages game state for one web player on one skill pack."""

    def __init__(self, skill_pack: SkillPack):
        self.skill_pack = skill_pack
        self.engine = GameEngine(skill_pack)
        self.runner = ChallengeRunner(kids_mode=skill_pack.kids_mode)

        # Per-challenge tracking (reset when challenge changes)
        self._hint_index: int = 0
        self.hints_used_this_zone: int = 0

        # Track message to show after zone completion
        self._pending_zone_complete: Optional[str] = None

        # Challenges skipped this zone (temporarily bypassed, revisited at end)
        self._skipped_ids: set[str] = set()

    # ── Navigation ────────────────────────────────────────────────────────────

    def start_zone(self, zone_id: str):
        """Set the active zone, reset per-zone hint tracking."""
        self.engine.current_zone = zone_id
        self.hints_used_this_zone = 0
        self._hint_index = 0
        self._skipped_ids.clear()
        self.engine.save()

    def get_current_zone(self) -> Optional[dict]:
        zone_id = self.engine.current_zone
        if not zone_id:
            return None
        return self.skill_pack.get_zone(zone_id)

    def get_current_challenge(self) -> Optional[dict]:
        """Return the next unanswered challenge in the current zone, or None.

        Skipped challenges are bypassed on the first pass; once all non-skipped
        challenges are answered the skipped ones are re-queued.
        """
        zone_id = self.engine.current_zone
        if not zone_id:
            return None
        challenges = self.skill_pack.get_zone_challenges(zone_id)
        completed = self.engine.challenges_completed_in_zone(zone_id)

        # First pass: find an incomplete, non-skipped challenge
        for ch in challenges:
            if ch["id"] not in completed and ch["id"] not in self._skipped_ids:
                return ch

        # All non-skipped done — clear skip set and retry skipped ones
        if self._skipped_ids:
            self._skipped_ids.clear()
            self._hint_index = 0
            for ch in challenges:
                if ch["id"] not in completed:
                    return ch

        return None

    def challenge_position(self) -> tuple[int, int]:
        """Return (current_number, total) for the active challenge."""
        zone_id = self.engine.current_zone
        if not zone_id:
            return (0, 0)
        challenges = self.skill_pack.get_zone_challenges(zone_id)
        completed = self.engine.challenges_completed_in_zone(zone_id)
        total = len(challenges)
        done = sum(1 for ch in challenges if ch["id"] in completed)
        return (done + 1, total)

    def new_game(self, player_name: str):
        """Reset engine and start from the beginning."""
        self.engine.reset()
        self.engine.player_name = player_name or self.skill_pack.default_player_name
        first_zone = self.skill_pack.zone_order[0]
        self.engine.current_zone = first_zone
        self.hints_used_this_zone = 0
        self._hint_index = 0
        self.engine.save()

    def has_progress(self) -> bool:
        return self.engine.total_challenges_completed() > 0

    # ── Challenge interaction ─────────────────────────────────────────────────

    def submit_answer(self, user_input: str) -> AnswerResult:
        challenge = self.get_current_challenge()
        if not challenge:
            return AnswerResult(False, "No active challenge.")

        zone_id = self.engine.current_zone

        self.engine.start_challenge_timer()
        result, output = self.runner.run_challenge(challenge, user_input)
        elapsed = self.engine.get_elapsed()

        if result.success:
            self.engine.record_correct()
            self.engine.check_speed_achievement()
            base_xp = challenge.get("xp", 50)
            actual_xp, did_level_up = self.engine.award_xp(base_xp)
            self.engine.mark_challenge_complete(zone_id, challenge["id"])
            self.engine.record_zone_attempt(zone_id, challenge["id"], correct=True, used_hint=self._hint_index > 0)

            new_achievements = self.engine.pop_new_achievements()

            # Check zone completion
            zone_complete = self._is_zone_now_complete(zone_id)
            pack_complete = False
            next_zone_id = None

            if zone_complete:
                self.engine.mark_zone_complete(zone_id)
                if self.hints_used_this_zone == 0:
                    self.engine.unlock_achievement("no_hints")
                pack_complete = self.engine.is_pack_complete(self.skill_pack)
                if not pack_complete:
                    next_zone_id = self._next_zone_id(zone_id)
                self.hints_used_this_zone = 0
                self._hint_index = 0
                self.engine.save()

            return AnswerResult(
                correct=True,
                message=result.message,
                xp=base_xp,
                actual_xp=actual_xp,
                level_up=did_level_up,
                level=self.engine.level,
                level_title=self.engine.level_title,
                streak=self.engine.streak,
                new_achievements=new_achievements,
                zone_complete=zone_complete,
                pack_complete=pack_complete,
                next_zone_id=next_zone_id,
            )
        else:
            self.engine.record_incorrect()
            self.engine.record_zone_attempt(zone_id, challenge["id"], correct=False, used_hint=False)
            return AnswerResult(
                correct=False,
                message=result.message,
                level=self.engine.level,
                level_title=self.engine.level_title,
                streak=self.engine.streak,
            )

    def get_hint(self) -> str:
        challenge = self.get_current_challenge()
        if not challenge:
            return "No active challenge."

        # Try hints list first, then fall back to explanation
        hints = challenge.get("hints", [])
        if hints:
            idx = min(self._hint_index, len(hints) - 1)
            text = hints[idx]
            self._hint_index = min(idx + 1, len(hints) - 1)
        else:
            text = challenge.get("explanation", "No hint available for this challenge.")

        self.hints_used_this_zone += 1
        self.engine.pay_hint_cost()
        return text

    def skip_challenge(self):
        challenge = self.get_current_challenge()
        if not challenge:
            return
        # Add to the skip set so get_current_challenge() bypasses it this pass.
        # The challenge stays incomplete and will be re-queued after the rest.
        self._skipped_ids.add(challenge["id"])
        self._hint_index = 0
        self.engine.record_incorrect()
        self.engine.save()

    def toggle_bookmark(self) -> bool:
        challenge = self.get_current_challenge()
        if not challenge:
            return False
        zone_id = self.engine.current_zone
        return self.engine.toggle_bookmark(zone_id, challenge["id"])

    def set_difficulty(self, mode: str):
        if mode in ("easy", "normal", "hard"):
            self.engine.difficulty_mode = mode
            self.engine.save()

    # ── Zone helpers ──────────────────────────────────────────────────────────

    def _is_zone_now_complete(self, zone_id: str) -> bool:
        if zone_id in self.engine.completed_zones:
            return False  # already completed in a previous session
        challenges = self.skill_pack.get_zone_challenges(zone_id)
        completed = self.engine.challenges_completed_in_zone(zone_id)
        all_ids = {ch["id"] for ch in challenges}
        return all_ids.issubset(completed)

    def _next_zone_id(self, zone_id: str) -> Optional[str]:
        order = self.skill_pack.zone_order
        try:
            idx = order.index(zone_id)
            if idx + 1 < len(order):
                return order[idx + 1]
        except ValueError:
            pass
        return None

    def advance_to_next_zone(self, next_zone_id: str):
        """Call after zone completion to move to the next zone."""
        self.engine.current_zone = next_zone_id
        self.hints_used_this_zone = 0
        self._hint_index = 0
        self.engine.save()

    # ── Stats helpers ─────────────────────────────────────────────────────────

    def stats_context(self) -> dict:
        """Return template context dict with all stats needed for the header."""
        engine = self.engine
        return {
            "player_name": engine.player_name,
            "total_xp": engine.total_xp,
            "level": engine.level,
            "level_title": engine.level_title,
            "level_progress_pct": int(engine.level_progress_pct * 100),
            "xp_this_level": engine.xp_this_level,
            "xp_for_next_level": engine.xp_for_next_level,
            "streak": engine.streak,
            "difficulty": engine.difficulty_mode,
            "completed_zones": len(engine.completed_zones),
            "total_zones": len(self.skill_pack.zone_order),
        }

    def all_zones_context(self) -> list[dict]:
        """Return zone list enriched with completion status for the menu."""
        zones = []
        for zone_id in self.skill_pack.zone_order:
            zone = self.skill_pack.get_zone(zone_id)
            if not zone:
                continue
            completed = zone_id in self.engine.completed_zones
            in_progress = (
                not completed
                and self.engine.challenges_completed_in_zone(zone_id)
            )
            is_current = zone_id == self.engine.current_zone
            total_ch = len(self.skill_pack.get_zone_challenges(zone_id))
            done_ch = len(self.engine.challenges_completed_in_zone(zone_id))
            stars = self.engine.get_zone_stars(zone_id) if completed else 0
            zones.append({
                "id": zone_id,
                "name": zone.get("name", zone_id),
                "completed": completed,
                "in_progress": in_progress,
                "is_current": is_current,
                "done": done_ch,
                "total": total_ch,
                "stars": stars,
            })
        return zones

    def parent_dashboard_context(self) -> dict:
        """Return context for the parent dashboard page."""
        engine = self.engine
        from ..engine import BASE_ACHIEVEMENTS

        # Accuracy
        total_correct = sum(len(c) for c in engine.completed_challenges.values())
        total_wrong = sum(zs.get("wrong", 0) for zs in engine.zone_scores.values())
        total = total_correct + total_wrong
        accuracy = int((total_correct / total * 100) if total > 0 else 0)

        # Strength zones: completed with 3 stars (no wrong answers, no hints)
        strengths = []
        for zone_id in self.skill_pack.zone_order:
            if zone_id in engine.completed_zones:
                stars = engine.get_zone_stars(zone_id)
                zs = engine.zone_scores.get(zone_id, {})
                if stars >= 3 and zs.get("wrong", 0) == 0:
                    zone = self.skill_pack.get_zone(zone_id)
                    if zone:
                        strengths.append({"name": zone.get("name", zone_id), "stars": stars})

        # Struggle zones: most wrong answers + hints
        struggles = []
        for zone_id, zs in engine.zone_scores.items():
            wrong = zs.get("wrong", 0)
            hints = zs.get("hints", 0)
            if wrong > 0 or hints > 2:
                zone = self.skill_pack.get_zone(zone_id)
                if zone:
                    struggles.append({
                        "id": zone_id,
                        "name": zone.get("name", zone_id),
                        "wrong_count": wrong,
                        "hint_count": hints,
                    })
        struggles.sort(key=lambda x: x["wrong_count"], reverse=True)

        return {
            "accuracy_pct": accuracy,
            "max_streak": engine.max_streak,
            "daily_streak": engine.daily_streak,
            "strength_zones": strengths[:5],
            "struggle_zones": struggles[:5],
        }

    def check_daily_answer(self, challenge: dict, user_input: str) -> "AnswerResult":
        """Check answer for the daily challenge. Awards 2x XP on correct."""
        result, _ = self.runner.run_challenge(challenge, user_input)
        if result.success:
            base_xp = challenge.get("xp", 30)
            bonus_xp = base_xp * 2
            actual_xp, did_level_up = self.engine.award_xp(bonus_xp)
            self.engine.complete_daily_challenge()
            new_achievements = self.engine.pop_new_achievements()
            return AnswerResult(
                correct=True, message=result.message,
                xp=base_xp, actual_xp=actual_xp,
                level_up=did_level_up, level=self.engine.level,
                level_title=self.engine.level_title, streak=self.engine.streak,
                new_achievements=new_achievements,
            )
        return AnswerResult(correct=False, message=result.message)

    def detailed_stats_context(self) -> dict:
        """Return rich stats context for the stats page."""
        engine = self.engine
        from ..engine import BASE_ACHIEVEMENTS

        # Count total correct across all zones
        total_correct = sum(
            len(completed) for completed in engine.completed_challenges.values()
        )
        # Count total wrong from zone_scores
        total_wrong = sum(
            zs.get("wrong", 0) for zs in engine.zone_scores.values()
        )
        total_attempts = total_correct + total_wrong
        accuracy = int((total_correct / total_attempts * 100) if total_attempts > 0 else 0)

        # Achievements count
        all_ach = {**BASE_ACHIEVEMENTS, **self.skill_pack.achievements}
        ach_unlocked = len([a for a in all_ach if a in engine.achievements])

        # Wrong-answer zones (for "areas to improve")
        wrong_zones = []
        for zone_id, journal in engine.wrong_answer_journal.items():
            if journal:
                zone = self.skill_pack.get_zone(zone_id)
                if zone:
                    wrong_zones.append({
                        "id": zone_id,
                        "name": zone.get("name", zone_id),
                        "wrong_count": len(journal),
                    })
        wrong_zones.sort(key=lambda x: x["wrong_count"], reverse=True)

        return {
            "total_correct": total_correct,
            "total_wrong": total_wrong,
            "accuracy_pct": accuracy,
            "max_streak": engine.max_streak,
            "achievements_unlocked": ach_unlocked,
            "achievements_total": len(all_ach),
            "wrong_zones": wrong_zones[:5],  # top 5
        }

    def achievements_context(self) -> list[dict]:
        """Return achievement list with unlock status."""
        all_ach = {**self.engine.skill_pack.achievements}
        # merge engine base achievements
        from ..engine import BASE_ACHIEVEMENTS
        all_ach_full = {**BASE_ACHIEVEMENTS, **all_ach}
        result = []
        for ach_id, (name, desc) in all_ach_full.items():
            result.append({
                "id": ach_id,
                "name": name,
                "description": desc,
                "unlocked": ach_id in self.engine.achievements,
            })
        return result
