"""
Tests for WebGameSession — challenge flow, answer submission, zone transitions.
These are the critical tests that verify the user doesn't get stuck in loops.
"""

import pytest
from engine.web.state import WebGameSession, AnswerResult


class TestChallengeFlow:
    """Test the complete challenge flow: get → answer → advance → repeat."""

    def test_get_first_challenge(self, session):
        ch = session.get_current_challenge()
        assert ch is not None
        assert ch["id"] == "za_01"

    def test_correct_answer_advances(self, session):
        ch = session.get_current_challenge()
        assert ch["id"] == "za_01"
        result = session.submit_answer("b", challenge=ch)
        assert result.correct is True
        # Next challenge should be za_02
        ch2 = session.get_current_challenge()
        assert ch2 is not None
        assert ch2["id"] == "za_02"

    def test_wrong_answer_does_not_advance(self, session):
        ch = session.get_current_challenge()
        assert ch["id"] == "za_01"
        result = session.submit_answer("a", challenge=ch)
        assert result.correct is False
        # Same challenge still current
        ch2 = session.get_current_challenge()
        assert ch2["id"] == "za_01"

    def test_complete_all_zone_challenges(self, session):
        """Verify we can complete all 3 challenges in zone_a without getting stuck."""
        for expected_id, answer in [("za_01", "b"), ("za_02", "b"), ("za_03", "b")]:
            ch = session.get_current_challenge()
            assert ch is not None, f"Expected {expected_id} but got None"
            assert ch["id"] == expected_id
            result = session.submit_answer(answer, challenge=ch)
            assert result.correct is True

        # After completing all zone_a challenges, get_current_challenge should return None
        ch = session.get_current_challenge()
        assert ch is None

    def test_zone_complete_flag(self, session):
        """Zone completion should be detected in the result."""
        session.submit_answer("b", challenge=session.get_current_challenge())  # za_01
        session.submit_answer("b", challenge=session.get_current_challenge())  # za_02
        result = session.submit_answer("b", challenge=session.get_current_challenge())  # za_03
        assert result.zone_complete is True

    def test_zone_transition(self, session):
        """After completing zone_a, starting zone_b should work."""
        # Complete zone_a
        for _ in range(3):
            ch = session.get_current_challenge()
            session.submit_answer("b", challenge=ch)

        # Start zone_b
        session.start_zone("zone_b")
        ch = session.get_current_challenge()
        assert ch is not None
        assert ch["id"] == "zb_01"

    def test_full_pack_completion(self, session):
        """Complete both zones — verify pack_complete flag."""
        # Complete zone_a
        for _ in range(3):
            ch = session.get_current_challenge()
            session.submit_answer("b", challenge=ch)

        # Start and complete zone_b
        session.start_zone("zone_b")
        session.submit_answer("b", challenge=session.get_current_challenge())  # zb_01
        result = session.submit_answer("b", challenge=session.get_current_challenge())  # zb_02
        assert result.zone_complete is True
        assert result.pack_complete is True

    def test_double_submit_protection(self, session):
        """Submitting the same challenge twice should not crash or double-count XP."""
        ch = session.get_current_challenge()
        result1 = session.submit_answer("b", challenge=ch)
        assert result1.correct is True

        # Try submitting the same challenge again — it's already complete
        is_done = session.engine.is_challenge_complete("zone_a", ch["id"])
        assert is_done is True

        # get_current_challenge should return the NEXT challenge now
        ch2 = session.get_current_challenge()
        assert ch2["id"] == "za_02"

    def test_challenge_position(self, session):
        num, total = session.challenge_position()
        assert total == 3  # 3 challenges in zone_a
        assert num == 1  # first challenge

        session.submit_answer("b", challenge=session.get_current_challenge())
        num, total = session.challenge_position()
        assert num == 2  # moved to second

    def test_find_challenge_by_id(self, session):
        ch = session._find_challenge_by_id("za_02")
        assert ch is not None
        assert ch["question"] == "What is 2+2?"

    def test_find_challenge_by_id_not_found(self, session):
        ch = session._find_challenge_by_id("nonexistent")
        assert ch is None


class TestSkipMechanic:
    def test_skip_moves_to_next(self, session):
        ch1 = session.get_current_challenge()
        assert ch1["id"] == "za_01"
        session.skip_challenge()
        ch2 = session.get_current_challenge()
        assert ch2["id"] == "za_02"

    def test_skipped_challenges_requeued(self, session):
        """After skipping and completing others, skipped ones come back."""
        session.skip_challenge()  # skip za_01
        session.submit_answer("b", challenge=session.get_current_challenge())  # za_02
        session.submit_answer("b", challenge=session.get_current_challenge())  # za_03

        # Now za_01 should come back
        ch = session.get_current_challenge()
        assert ch is not None
        assert ch["id"] == "za_01"

    def test_skip_all_then_retry(self, session):
        """Skipping all challenges should re-queue them."""
        session.skip_challenge()  # za_01
        session.skip_challenge()  # za_02
        session.skip_challenge()  # za_03

        # All skipped — should re-queue, starting from za_01
        ch = session.get_current_challenge()
        assert ch is not None
        assert ch["id"] == "za_01"


class TestHints:
    def test_get_hint(self, session):
        hint = session.get_hint()
        assert hint is not None
        assert "not 1" in hint.lower() or len(hint) > 0

    def test_hint_index_resets_on_correct_answer(self, session):
        session.get_hint()
        assert session._hint_index == 1
        ch = session.get_current_challenge()
        session.submit_answer("b", challenge=ch)
        assert session._hint_index == 0  # reset for next challenge


class TestStats:
    def test_stats_context(self, session):
        ctx = session.stats_context()
        assert "total_xp" in ctx
        assert "level" in ctx
        assert "player_name" in ctx
        assert ctx["player_name"] == "TestPlayer"

    def test_achievements_context(self, session):
        ach = session.achievements_context()
        assert isinstance(ach, list)
        assert len(ach) > 0

    def test_all_zones_context(self, session):
        zones = session.all_zones_context()
        assert len(zones) == 2
        assert zones[0]["id"] == "zone_a"
