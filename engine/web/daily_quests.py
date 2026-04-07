"""
daily_quests.py — Rotating daily objectives for bonus XP.

Each day, 3 quests are generated based on the current date.
Completing them earns significant bonus XP.
Inspired by: Fortnite daily quests, WoW daily quests, Duolingo daily goals.
"""

import datetime
import hashlib


QUEST_TEMPLATES = [
    {"id": "streak_3", "title": "Streak Starter", "desc": "Get a 3-answer streak", "icon": "🔥", "xp": 50, "check": lambda s: s.get("streak", 0) >= 3},
    {"id": "streak_5", "title": "Hot Streak", "desc": "Get a 5-answer streak", "icon": "🔥", "xp": 100, "check": lambda s: s.get("streak", 0) >= 5},
    {"id": "correct_5", "title": "Knowledge Seeker", "desc": "Answer 5 questions correctly today", "icon": "✅", "xp": 75, "check": lambda s: s.get("session_correct", 0) >= 5},
    {"id": "correct_10", "title": "Scholar's Path", "desc": "Answer 10 questions correctly today", "icon": "📚", "xp": 150, "check": lambda s: s.get("session_correct", 0) >= 10},
    {"id": "correct_20", "title": "Master's Journey", "desc": "Answer 20 questions correctly today", "icon": "🎓", "xp": 300, "check": lambda s: s.get("session_correct", 0) >= 20},
    {"id": "speed_3", "title": "Quick Thinker", "desc": "Answer 3 questions in under 5 seconds each", "icon": "⚡", "xp": 80, "check": lambda s: s.get("speed_answers", 0) >= 3},
    {"id": "no_wrong", "title": "Perfectionist", "desc": "Answer 5 questions without getting any wrong", "icon": "💎", "xp": 120, "check": lambda s: s.get("session_correct", 0) >= 5 and s.get("session_wrong", 0) == 0},
    {"id": "use_hint", "title": "Wise Choice", "desc": "Use a hint and still get the answer right", "icon": "💡", "xp": 40, "check": lambda s: s.get("hint_correct", 0) >= 1},
    {"id": "zone_complete", "title": "Zone Conqueror", "desc": "Complete an entire zone today", "icon": "🏁", "xp": 200, "check": lambda s: s.get("zones_completed_today", 0) >= 1},
    {"id": "daily_challenge", "title": "Daily Champion", "desc": "Complete the daily challenge", "icon": "⭐", "xp": 100, "check": lambda s: s.get("daily_done", False)},
    {"id": "lesson_reader", "title": "Bookworm", "desc": "Read 3 lessons after answering", "icon": "📖", "xp": 60, "check": lambda s: s.get("lessons_read", 0) >= 3},
    {"id": "comeback", "title": "Comeback Kid", "desc": "Get a question wrong, then get the next 3 right", "icon": "💪", "xp": 90, "check": lambda s: s.get("comeback_streak", 0) >= 3},
]


def get_daily_quests(date: datetime.date = None, count: int = 3) -> list[dict]:
    """Get today's rotating daily quests. Deterministic per date."""
    if date is None:
        date = datetime.date.today()

    seed = hashlib.md5(str(date).encode()).hexdigest()
    indices = []
    for i in range(len(QUEST_TEMPLATES)):
        h = hashlib.md5(f"{seed}-{i}".encode()).hexdigest()
        indices.append((int(h[:8], 16), i))
    indices.sort()

    quests = []
    for _, idx in indices[:count]:
        q = QUEST_TEMPLATES[idx].copy()
        del q["check"]  # Don't send the lambda to template
        q["completed"] = False
        quests.append(q)

    return quests


def check_quest_completion(quest_id: str, session_stats: dict) -> bool:
    """Check if a specific quest is completed based on session stats."""
    for qt in QUEST_TEMPLATES:
        if qt["id"] == quest_id:
            return qt["check"](session_stats)
    return False
