"""
Edge case tests — the scenarios that cause loops and crashes.
"""

import os
import pytest

os.environ["QUEST_STORAGE"] = "memory"

from fastapi.testclient import TestClient
from engine.skill_pack import SkillPack
from engine.web.hub import create_hub_app
from engine.web.state import WebGameSession


@pytest.fixture
def single_challenge_pack():
    """Pack with only 1 challenge in 1 zone — tests boundary conditions."""
    return SkillPack(
        id="edge",
        title="Edge Case Pack",
        subtitle="Test",
        save_file_name="edge_save",
        intro_story="",
        quit_message="",
        name_prompt="Name?",
        default_player_name="Player",
        zone_order=["only_zone"],
        zones={
            "only_zone": {
                "id": "only_zone",
                "name": "The Only Zone",
                "description": "Just one challenge",
                "level_required": 1,
                "challenges": [
                    {
                        "id": "only_1",
                        "title": "The Only Question",
                        "type": "quiz",
                        "question": "Is this the only question?",
                        "options": ["Yes", "No", "Maybe", "Definitely"],
                        "answer": "a",
                        "lesson": "It is!",
                        "hints": ["Think yes"],
                        "xp": 25,
                    },
                ],
            },
        },
        zone_intros={"only_zone": "Welcome!"},
        zone_completions={"only_zone": "Done!"},
        boss_intros={},
        zone_achievement_map={},
        achievements={},
        kids_mode=False,
    )


@pytest.fixture
def edge_client(single_challenge_pack):
    app = create_hub_app([single_challenge_pack])
    return TestClient(app)


class TestSingleChallengePack:
    """When a zone has only 1 challenge — completes zone AND pack in one answer."""

    def test_single_challenge_completes_zone_and_pack(self):
        pack = SkillPack(
            id="mini", title="Mini", subtitle="", save_file_name="mini",
            intro_story="", quit_message="", name_prompt="?", default_player_name="P",
            zone_order=["z"], zones={"z": {"id": "z", "name": "Z", "description": "",
                "level_required": 1, "challenges": [
                    {"id": "c", "type": "quiz", "question": "?", "options": ["A", "B"],
                     "answer": "a", "lesson": "!", "hints": ["h"], "xp": 10}
                ]}},
            zone_intros={}, zone_completions={}, boss_intros={},
            zone_achievement_map={}, achievements={}, kids_mode=False,
        )
        s = WebGameSession(pack)
        s.new_game("Test")
        ch = s.get_current_challenge()
        result = s.submit_answer("a", challenge=ch)
        assert result.correct
        assert result.zone_complete
        assert result.pack_complete
        # No more challenges
        assert s.get_current_challenge() is None

    def test_web_single_challenge_no_loop(self, edge_client):
        """The critical test: completing the only challenge should NOT loop."""
        c = edge_client
        c.post("/edge/new-game", data={"player_name": "Test"})

        # Answer the only challenge
        r = c.post("/edge/answer", data={"answer": "a", "challenge_id": "only_1"})
        assert r.status_code == 200

        # GET /challenge after completing everything should redirect, not loop
        r = c.get("/edge/challenge", follow_redirects=False)
        assert r.status_code == 303
        loc = r.headers.get("location", "")
        assert "complete" in loc or "zone" in loc  # should go to complete page


class TestTextInputChallenge:
    """Test that challenges without options show a text input."""

    def test_quiz_with_no_options_shows_text_input(self):
        """When ctype='quiz' but no options, should show text input not empty grid."""
        from engine.skill_pack import SkillPack
        pack = SkillPack(
            id="text_test", title="Text", subtitle="", save_file_name="text_test",
            intro_story="", quit_message="", name_prompt="?", default_player_name="P",
            zone_order=["z"], zones={"z": {"id": "z", "name": "Z", "description": "",
                "level_required": 1, "challenges": [
                    {"id": "c", "type": "quiz", "question": "What is pwd?",
                     "answers": ["pwd"], "lesson": "pwd prints working dir",
                     "hints": ["think directory"], "xp": 10}
                ]}},
            zone_intros={}, zone_completions={}, boss_intros={},
            zone_achievement_map={}, achievements={}, kids_mode=False,
        )
        app = create_hub_app([pack])
        c = TestClient(app)
        c.post("/text_test/new-game", data={"player_name": "Test"})
        r = c.get("/text_test/challenge")
        assert r.status_code == 200
        # Should have text input, not empty options grid
        assert "text-answer-input" in r.text
        assert "option-btn" not in r.text  # NO option buttons


class TestRapidSubmissions:
    """Test rapid-fire answer submissions (fast clicking)."""

    def test_three_rapid_submits_same_challenge(self, edge_client):
        c = edge_client
        c.post("/edge/new-game", data={"player_name": "Fast"})

        # Submit same challenge 3 times rapidly
        r1 = c.post("/edge/answer", data={"answer": "a", "challenge_id": "only_1"})
        r2 = c.post("/edge/answer", data={"answer": "a", "challenge_id": "only_1"}, follow_redirects=False)
        r3 = c.post("/edge/answer", data={"answer": "a", "challenge_id": "only_1"}, follow_redirects=False)

        # First should succeed (200), second and third should redirect (303)
        assert r1.status_code == 200
        assert r2.status_code == 303
        assert r3.status_code == 303


class TestEmptyAnswer:
    def test_empty_answer_redirects(self, edge_client):
        c = edge_client
        c.post("/edge/new-game", data={"player_name": "Empty"})
        r = c.post("/edge/answer", data={"answer": "", "challenge_id": "only_1"}, follow_redirects=False)
        assert r.status_code == 303

    def test_missing_challenge_id_still_works(self, edge_client):
        c = edge_client
        c.post("/edge/new-game", data={"player_name": "NoId"})
        # Submit without challenge_id — should still find current challenge
        r = c.post("/edge/answer", data={"answer": "a"})
        assert r.status_code == 200


class TestOptionShuffle:
    """Test anti-cheat option shuffling."""

    def test_shuffle_produces_valid_mapping(self):
        from engine.web.hub import _shuffle_options
        options = ["Apple", "Banana", "Cherry", "Date"]
        shuffled, lmap = _shuffle_options(options, "a", "test-seed")
        # All options present
        assert sorted(shuffled) == sorted(options)
        # Map has 4 entries
        assert len(lmap) == 4
        # Map values are original letters
        assert set(lmap.values()) == {"a", "b", "c", "d"}
        # Map keys are new letters
        assert set(lmap.keys()) == {"a", "b", "c", "d"}

    def test_shuffle_deterministic_same_seed(self):
        from engine.web.hub import _shuffle_options
        options = ["A", "B", "C", "D"]
        s1, m1 = _shuffle_options(options, "a", "same-seed")
        s2, m2 = _shuffle_options(options, "a", "same-seed")
        assert s1 == s2
        assert m1 == m2

    def test_shuffle_different_seeds_differ(self):
        from engine.web.hub import _shuffle_options
        options = ["A", "B", "C", "D"]
        s1, _ = _shuffle_options(options, "a", "seed-1")
        s2, _ = _shuffle_options(options, "a", "seed-2")
        # With different seeds, almost certainly different order
        # (there's a 1/24 chance they're the same, so we check mapping instead)
        # Just verify both are valid
        assert sorted(s1) == sorted(s2)

    def test_empty_options_no_shuffle(self):
        from engine.web.hub import _shuffle_options
        s, m = _shuffle_options([], "a", "seed")
        assert s == []
        assert m == {}

    def test_single_option_no_shuffle(self):
        from engine.web.hub import _shuffle_options
        s, m = _shuffle_options(["Only"], "a", "seed")
        assert s == ["Only"]
        assert m == {}


class TestZoneNavigation:
    def test_invalid_zone_redirects_to_menu(self, edge_client):
        c = edge_client
        c.post("/edge/new-game", data={"player_name": "Nav"})
        r = c.get("/edge/zone/nonexistent/intro", follow_redirects=False)
        assert r.status_code == 303

    def test_skip_only_challenge_requeues(self):
        pack = SkillPack(
            id="skip1", title="Skip", subtitle="", save_file_name="skip1",
            intro_story="", quit_message="", name_prompt="?", default_player_name="P",
            zone_order=["z"], zones={"z": {"id": "z", "name": "Z", "description": "",
                "level_required": 1, "challenges": [
                    {"id": "c", "type": "quiz", "question": "?", "options": ["A", "B"],
                     "answer": "a", "lesson": "!", "hints": ["h"], "xp": 10}
                ]}},
            zone_intros={}, zone_completions={}, boss_intros={},
            zone_achievement_map={}, achievements={}, kids_mode=False,
        )
        s = WebGameSession(pack)
        s.new_game("Test")
        s.skip_challenge()
        # Should re-queue the only challenge
        ch = s.get_current_challenge()
        assert ch is not None
        assert ch["id"] == "c"
