"""
Shared test fixtures for quest-engine tests.
"""

import os
import pytest
from pathlib import Path

# Force memory storage for tests (no file or DB side effects)
os.environ["QUEST_STORAGE"] = "memory"

from engine.skill_pack import SkillPack
from engine.engine import GameEngine
from engine.web.state import WebGameSession


@pytest.fixture
def sample_pack():
    """A minimal SkillPack for testing."""
    return SkillPack(
        id="test_pack",
        title="Test Pack",
        subtitle="Test",
        save_file_name="test_save",
        intro_story="Welcome to the test!",
        quit_message="Goodbye!",
        name_prompt="Name?",
        default_player_name="Tester",
        zone_order=["zone_a", "zone_b"],
        zones={
            "zone_a": {
                "id": "zone_a",
                "name": "Zone A",
                "description": "First zone",
                "level_required": 1,
                "challenges": [
                    {
                        "id": "za_01",
                        "title": "Q1",
                        "type": "quiz",
                        "question": "What is 1+1?",
                        "options": ["1", "2", "3", "4"],
                        "answer": "b",
                        "lesson": "1+1=2",
                        "hints": ["It's not 1", "Think simple"],
                        "xp": 25,
                    },
                    {
                        "id": "za_02",
                        "title": "Q2",
                        "type": "quiz",
                        "question": "What is 2+2?",
                        "options": ["3", "4", "5", "6"],
                        "answer": "b",
                        "lesson": "2+2=4",
                        "hints": ["Not 3", "Double 2"],
                        "xp": 25,
                    },
                    {
                        "id": "za_03",
                        "title": "Q3 Boss",
                        "type": "quiz",
                        "question": "What is 3+3?",
                        "options": ["5", "6", "7", "8"],
                        "answer": "b",
                        "lesson": "3+3=6",
                        "hints": ["Not 5", "Double 3"],
                        "xp": 30,
                        "is_boss": True,
                    },
                ],
            },
            "zone_b": {
                "id": "zone_b",
                "name": "Zone B",
                "description": "Second zone",
                "level_required": 1,
                "challenges": [
                    {
                        "id": "zb_01",
                        "title": "Q4",
                        "type": "quiz",
                        "question": "What is 4+4?",
                        "options": ["7", "8", "9", "10"],
                        "answer": "b",
                        "lesson": "4+4=8",
                        "hints": ["Not 7", "Double 4"],
                        "xp": 25,
                    },
                    {
                        "id": "zb_02",
                        "title": "Q5",
                        "type": "quiz",
                        "question": "What is 5+5?",
                        "options": ["9", "10", "11", "12"],
                        "answer": "b",
                        "lesson": "5+5=10",
                        "hints": ["Not 9", "Double 5"],
                        "xp": 30,
                        "is_boss": True,
                    },
                ],
            },
        },
        zone_intros={"zone_a": "Welcome to Zone A!", "zone_b": "Welcome to Zone B!"},
        zone_completions={"zone_a": "Zone A done!", "zone_b": "Zone B done!"},
        boss_intros={"zone_a": "Boss time!", "zone_b": "Final boss!"},
        zone_achievement_map={"zone_a": "zone_a_done", "zone_b": "zone_b_done"},
        achievements={
            "zone_a_done": ("Zone A Master", "Completed Zone A"),
            "zone_b_done": ("Zone B Master", "Completed Zone B"),
        },
        kids_mode=False,
    )


@pytest.fixture
def session(sample_pack):
    """A fresh WebGameSession."""
    s = WebGameSession(sample_pack)
    s.new_game("TestPlayer")
    return s


@pytest.fixture
def engine(sample_pack):
    """A fresh GameEngine."""
    e = GameEngine(sample_pack)
    e.reset()
    e.player_name = "TestPlayer"
    return e
