"""
Tests for the web routes — auth flow, challenge pages, redirects.
Uses FastAPI TestClient.
"""

import os
import pytest

os.environ["QUEST_STORAGE"] = "memory"

from fastapi.testclient import TestClient
from engine.skill_pack import SkillPack
from engine.web.hub import create_hub_app


@pytest.fixture
def mini_pack():
    """Minimal pack for web route testing."""
    return SkillPack(
        id="test",
        title="Test",
        subtitle="Test Pack",
        save_file_name="test_save",
        intro_story="Welcome!",
        quit_message="Bye!",
        name_prompt="Name?",
        default_player_name="Player",
        zone_order=["z1"],
        zones={
            "z1": {
                "id": "z1",
                "name": "Zone 1",
                "description": "Test zone",
                "level_required": 1,
                "challenges": [
                    {
                        "id": "c1",
                        "title": "Q1",
                        "type": "quiz",
                        "question": "1+1?",
                        "options": ["1", "2", "3", "4"],
                        "answer": "b",
                        "lesson": "1+1=2",
                        "hints": ["Not 1"],
                        "xp": 25,
                    },
                    {
                        "id": "c2",
                        "title": "Q2",
                        "type": "quiz",
                        "question": "2+2?",
                        "options": ["3", "4", "5", "6"],
                        "answer": "b",
                        "lesson": "2+2=4",
                        "hints": ["Not 3"],
                        "xp": 25,
                    },
                ],
            },
        },
        zone_intros={"z1": "Intro!"},
        zone_completions={"z1": "Done!"},
        boss_intros={"z1": "Boss!"},
        zone_achievement_map={"z1": "z1_done"},
        achievements={"z1_done": ("Z1 Master", "Done!")},
        kids_mode=False,
    )


@pytest.fixture
def client(mini_pack):
    """TestClient with a single-pack hub (no auth gating in memory mode)."""
    app = create_hub_app([mini_pack])
    return TestClient(app)


class TestHubRoutes:
    def test_hub_index(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert "Test" in r.text

    def test_pack_menu_shows_onboarding_for_new_player(self, client):
        r = client.get("/test/")
        assert r.status_code == 200
        assert "onboard" in r.text.lower() or "welcome" in r.text.lower()

    def test_new_game_redirects_to_zone_intro(self, client):
        r = client.post("/test/new-game", data={"player_name": "Tester"}, follow_redirects=False)
        assert r.status_code == 303
        assert "/test/zone/z1/intro" in r.headers["location"]

    def test_zone_intro_page(self, client):
        client.post("/test/new-game", data={"player_name": "Tester"})
        r = client.get("/test/zone/z1/intro")
        assert r.status_code == 200
        assert "Zone 1" in r.text

    def test_challenge_page_shows_question(self, client):
        client.post("/test/new-game", data={"player_name": "Tester"})
        r = client.get("/test/challenge")
        assert r.status_code == 200
        assert "1+1" in r.text

    def test_correct_answer_shows_result(self, client):
        client.post("/test/new-game", data={"player_name": "Tester"})
        r = client.post("/test/answer", data={"answer": "b", "challenge_id": "c1"})
        assert r.status_code == 200
        assert "correct" in r.text.lower() or "✓" in r.text

    def test_wrong_answer_shows_error(self, client):
        client.post("/test/new-game", data={"player_name": "Tester"})
        r = client.post("/test/answer", data={"answer": "a", "challenge_id": "c1"})
        assert r.status_code == 200
        assert "✗" in r.text or "wrong" in r.text.lower() or "incorrect" in r.text.lower()

    def test_challenge_flow_no_loops(self, client):
        """Critical test: complete all challenges without getting stuck."""
        client.post("/test/new-game", data={"player_name": "Tester"})

        # Answer c1 correctly
        r = client.post("/test/answer", data={"answer": "b", "challenge_id": "c1"})
        assert r.status_code == 200

        # Next challenge page should show c2
        r = client.get("/test/challenge")
        assert r.status_code == 200
        assert "2+2" in r.text

        # Answer c2 correctly
        r = client.post("/test/answer", data={"answer": "b", "challenge_id": "c2"})
        assert r.status_code == 200

        # After all challenges done, /challenge should redirect
        r = client.get("/test/challenge", follow_redirects=False)
        assert r.status_code == 303

    def test_double_submit_redirects(self, client):
        """Submitting the same challenge twice should redirect, not crash."""
        client.post("/test/new-game", data={"player_name": "Tester"})

        # First submit
        r1 = client.post("/test/answer", data={"answer": "b", "challenge_id": "c1"})
        assert r1.status_code == 200

        # Second submit of same challenge — should redirect
        r2 = client.post("/test/answer", data={"answer": "b", "challenge_id": "c1"}, follow_redirects=False)
        assert r2.status_code == 303

    def test_skip_works(self, client):
        client.post("/test/new-game", data={"player_name": "Tester"})
        r = client.post("/test/skip", follow_redirects=False)
        assert r.status_code == 303

    def test_hint_works(self, client):
        client.post("/test/new-game", data={"player_name": "Tester"})
        r = client.post("/test/hint")
        assert r.status_code == 200

    def test_stats_page(self, client):
        client.post("/test/new-game", data={"player_name": "Tester"})
        r = client.get("/test/stats")
        assert r.status_code == 200

    def test_achievements_page(self, client):
        client.post("/test/new-game", data={"player_name": "Tester"})
        r = client.get("/test/achievements")
        assert r.status_code == 200

    def test_settings_page(self, client):
        client.post("/test/new-game", data={"player_name": "Tester"})
        r = client.get("/test/settings")
        assert r.status_code == 200

    def test_leaderboard_page(self, client):
        client.post("/test/new-game", data={"player_name": "Tester"})
        r = client.get("/test/leaderboard")
        assert r.status_code == 200

    def test_daily_page(self, client):
        client.post("/test/new-game", data={"player_name": "Tester"})
        r = client.get("/test/daily")
        assert r.status_code == 200

    def test_review_page(self, client):
        client.post("/test/new-game", data={"player_name": "Tester"})
        r = client.get("/test/review")
        assert r.status_code == 200

    def test_bookmarks_page(self, client):
        client.post("/test/new-game", data={"player_name": "Tester"})
        r = client.get("/test/bookmarks")
        assert r.status_code == 200


    def test_profile_page(self, client):
        client.post("/test/new-game", data={"player_name": "Profiler"})
        r = client.get("/test/profile")
        assert r.status_code == 200
        assert "Profiler" in r.text

    def test_zone_complete_page(self, client):
        client.post("/test/new-game", data={"player_name": "Completer"})
        # Complete both challenges
        client.post("/test/answer", data={"answer": "b", "challenge_id": "c1"})
        client.post("/test/answer", data={"answer": "b", "challenge_id": "c2"})
        r = client.get("/test/zone/z1/complete")
        assert r.status_code == 200


class TestAuthPages:
    """Test auth pages render (actual auth requires Postgres)."""

    def test_login_page_renders(self, client):
        r = client.get("/test/auth/login")
        assert r.status_code == 200
        assert "Sign In" in r.text or "Welcome" in r.text

    def test_register_page_renders(self, client):
        r = client.get("/test/auth/register")
        assert r.status_code == 200
        assert "Create Account" in r.text
