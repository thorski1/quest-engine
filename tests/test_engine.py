"""
Tests for GameEngine — save/load, XP, levels, zone tracking, daily challenges.
"""

import pytest


class TestGameEngine:
    def test_new_game_resets_state(self, engine):
        engine.total_xp = 999
        engine.reset(); engine.player_name = "Fresh"
        assert engine.player_name == "Fresh"
        assert engine.total_xp == 0
        assert engine.streak == 0
        assert engine.completed_zones == set()

    def test_award_xp(self, engine):
        actual, leveled = engine.award_xp(100)
        assert actual == 100
        assert engine.total_xp == 100

    def test_record_correct_increments_streak(self, engine):
        engine.record_correct()
        assert engine.streak == 1
        engine.record_correct()
        assert engine.streak == 2
        assert engine.max_streak == 2

    def test_record_incorrect_resets_streak(self, engine):
        engine.record_correct()
        engine.record_correct()
        engine.record_incorrect()
        assert engine.streak == 0
        assert engine.max_streak == 2

    def test_mark_challenge_complete(self, engine):
        engine.mark_challenge_complete("zone_a", "za_01")
        assert "za_01" in engine.completed_challenges["zone_a"]

    def test_is_challenge_complete(self, engine):
        assert not engine.is_challenge_complete("zone_a", "za_01")
        engine.mark_challenge_complete("zone_a", "za_01")
        assert engine.is_challenge_complete("zone_a", "za_01")

    def test_zone_completion(self, engine):
        assert "zone_a" not in engine.completed_zones
        engine.mark_challenge_complete("zone_a", "za_01")
        engine.mark_challenge_complete("zone_a", "za_02")
        engine.mark_challenge_complete("zone_a", "za_03")
        engine.mark_zone_complete("zone_a")
        assert "zone_a" in engine.completed_zones

    def test_save_and_load(self, sample_pack):
        from engine.engine import GameEngine
        e1 = GameEngine(sample_pack)
        e1.reset(); e1.player_name = "SaveTest"
        e1.total_xp = 500
        e1.streak = 5
        e1.mark_challenge_complete("zone_a", "za_01")
        e1.save()

        e2 = GameEngine(sample_pack)
        e2.load()
        assert e2.player_name == "SaveTest"
        assert e2.total_xp == 500
        assert "za_01" in e2.completed_challenges.get("zone_a", set())

    def test_difficulty_suggestion_not_enough_data(self, engine):
        # Fewer than 10 attempts — no suggestion
        for _ in range(5):
            engine.record_correct()
        assert engine.get_difficulty_suggestion() is None

    def test_difficulty_suggestion_increase(self, engine):
        for _ in range(15):
            engine.record_correct()
        suggestion = engine.get_difficulty_suggestion()
        assert suggestion == "increase"

    def test_difficulty_suggestion_decrease(self, engine):
        for _ in range(3):
            engine.record_correct()
        for _ in range(8):
            engine.record_incorrect()
        suggestion = engine.get_difficulty_suggestion()
        assert suggestion == "decrease"


class TestDailyLoginBonus:
    def test_first_login_gives_bonus(self, engine):
        engine.last_played_date = ""
        engine.total_xp = 0
        engine._update_daily_streak()
        # First day: 10 base + 5 * 1 streak = 15 XP
        assert engine._daily_login_bonus == 15
        assert engine.total_xp == 15
        assert engine.daily_streak == 1

    def test_consecutive_login_increases_bonus(self, engine):
        import datetime
        yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
        engine.last_played_date = yesterday
        engine.daily_streak = 5
        engine.total_xp = 0
        engine._update_daily_streak()
        # Day 6: 10 base + 5 * 6 = 40 XP
        assert engine._daily_login_bonus == 40
        assert engine.daily_streak == 6

    def test_same_day_no_double_bonus(self, engine):
        engine.last_played_date = str(__import__('datetime').date.today())
        engine.total_xp = 100
        engine._update_daily_streak()
        assert engine.total_xp == 100  # No change


class TestSpeedBonus:
    def test_speed_bonus_under_5s(self, engine):
        actual, _ = engine.award_xp(100, elapsed_s=3.0)
        # 100 base + 25% speed bonus = 125
        assert actual == 125

    def test_speed_bonus_under_10s(self, engine):
        actual, _ = engine.award_xp(100, elapsed_s=8.0)
        # 100 base + 10% speed bonus = 110
        assert actual == 110

    def test_no_speed_bonus_over_10s(self, engine):
        actual, _ = engine.award_xp(100, elapsed_s=15.0)
        assert actual == 100

    def test_no_speed_bonus_zero_elapsed(self, engine):
        actual, _ = engine.award_xp(100, elapsed_s=0.0)
        assert actual == 100


class TestStreakFreeze:
    def test_buy_streak_freeze(self, engine):
        engine.total_xp = 100
        assert engine.buy_streak_freeze()
        assert engine.streak_freeze_active
        assert engine.total_xp == 50

    def test_freeze_protects_streak(self, engine):
        engine.total_xp = 100
        engine.record_correct()
        engine.record_correct()
        engine.record_correct()
        assert engine.streak == 3
        engine.buy_streak_freeze()
        engine.record_incorrect()
        # Streak preserved, freeze consumed
        assert engine.streak == 3
        assert not engine.streak_freeze_active

    def test_freeze_only_protects_once(self, engine):
        engine.total_xp = 100
        engine.record_correct()
        engine.record_correct()
        engine.buy_streak_freeze()
        engine.record_incorrect()  # protected
        assert engine.streak == 2
        engine.record_incorrect()  # not protected
        assert engine.streak == 0

    def test_cant_buy_freeze_without_xp(self, engine):
        engine.total_xp = 30
        assert not engine.buy_streak_freeze()
        assert not engine.streak_freeze_active

    def test_cant_buy_freeze_twice(self, engine):
        engine.total_xp = 200
        assert engine.buy_streak_freeze()
        assert not engine.buy_streak_freeze()  # already active
        assert engine.total_xp == 150  # only charged once


class TestStorage:
    def test_memory_store_save_load(self):
        from engine.storage import MemoryStore
        store = MemoryStore()
        store.save("pack1", "player1", {"xp": 100})
        data = store.load("pack1", "player1")
        assert data["xp"] == 100

    def test_memory_store_delete(self):
        from engine.storage import MemoryStore
        store = MemoryStore()
        store.save("pack1", "player1", {"xp": 100})
        store.delete("pack1", "player1")
        assert store.load("pack1", "player1") is None

    def test_memory_store_list_players(self):
        from engine.storage import MemoryStore
        store = MemoryStore()
        store.save("pack1", "p1", {"xp": 100})
        store.save("pack1", "p2", {"xp": 200})
        players = store.list_players("pack1")
        assert set(players) == {"p1", "p2"}

    def test_sqlite_store_save_load(self, tmp_path):
        from engine.storage import SqliteStore
        store = SqliteStore(tmp_path / "test.db")
        store.save("pack1", "player1", {"xp": 500})
        data = store.load("pack1", "player1")
        assert data["xp"] == 500

    def test_sqlite_store_list_players(self, tmp_path):
        from engine.storage import SqliteStore
        store = SqliteStore(tmp_path / "test.db")
        store.save("pack1", "p1", {"xp": 100})
        store.save("pack1", "p2", {"xp": 200})
        assert set(store.list_players("pack1")) == {"p1", "p2"}
