"""
main.py - Quest Engine entry point
Loads a skill pack by name and runs the game.

Usage:
    python -m engine bash
    python -m engine postgres
"""

import sys
import traceback

try:
    from rich.console import Console
except ImportError:
    print("ERROR: 'rich' library not found.")
    print("Install it with: pip install rich")
    sys.exit(1)

from .challenges import ChallengeRunner
from .engine import GameEngine
from .skill_pack import SkillPack, load_skill_pack
from .ui import (
    console,
    render_banner,
    render_boss_intro,
    render_main_menu,
    render_zone_intro,
    render_zone_complete,
    render_challenge_panel,
    render_challenge_menu,
    render_result,
    render_hint,
    render_achievement,
    celebrate_level_up,
    render_achievements_screen,
    render_zone_select,
    render_stats_screen,
    render_session_summary,
    render_name_prompt,
    confirm_new_game,
    prompt_command,
    render_output,
    render_stats_panel,
    render_separator,
    print_narrative,
    print_info,
    print_warning,
    _press_enter,
    animate_zone_progress,
    render_daily_challenge_banner,
    render_completion_certificate,
    render_bookmarks_screen,
    render_difficulty_select,
    render_help_screen,
    render_zone_preview,
    render_new_record_flash,
    render_personal_bests,
)


class GameSession:
    def __init__(self, skill_pack: SkillPack):
        self.skill_pack = skill_pack
        runner_class = skill_pack.runner_class or ChallengeRunner
        self.engine = GameEngine(skill_pack)
        self.runner = runner_class(kids_mode=skill_pack.kids_mode)

    # ── Main Loop ─────────────────────────────────────────────────────────────

    def run(self):
        while True:
            choice = render_main_menu(self.engine)

            if choice == "1":
                self._new_game()
            elif choice == "2":
                self._continue_game()
            elif choice == "3":
                self._zone_select()
            elif choice == "4":
                render_achievements_screen(self.engine)
            elif choice == "5":
                render_stats_screen(self.engine)
            elif choice == "6":
                self._review_weak_spots()
            elif choice == "7":
                self._export_notes()
            elif choice == "8":
                self._daily_challenge()
            elif choice == "9":
                self._view_bookmarks()
            elif choice == "p":
                self._personal_bests()
            elif choice == "t":
                self._timed_drill()
            elif choice == "d":
                self._set_difficulty()
            elif choice == "0":
                self._quit()
                break

    def _quit(self):
        self.engine.save()
        console.clear()
        render_banner(self.skill_pack)
        render_session_summary(self.engine)
        console.print(f"\n[bold cyan]{self.skill_pack.quit_message}[/bold cyan]\n")
        console.print("[dim]Your progress has been saved.[/dim]")
        console.print()

    def _review_weak_spots(self):
        """Play through challenges the player has previously answered wrong."""
        weak_zones = self.engine.get_weak_zones()
        if not weak_zones:
            console.clear()
            render_banner(self.skill_pack)
            console.print(Panel(
                "[bold green]No weak spots found![/bold green]\n\n"
                "[dim]You've answered every practiced challenge correctly.\n"
                "Keep playing to build your review list.[/dim]",
                title="[bold green]★  CLEAN RECORD[/bold green]",
                border_style="green",
                padding=(1, 4),
            ))
            _press_enter()
            return

        from rich import box as rbox
        console.clear()
        render_banner(self.skill_pack)
        zone_names = []
        for zone_id in weak_zones:
            zone = self.skill_pack.get_zone(zone_id)
            if zone:
                count = len(self.engine.wrong_answer_journal.get(zone_id, []))
                zone_names.append(f"  • {zone['name']} — [yellow]{count} challenge(s)[/yellow]")

        console.print(Panel(
            "\n".join(zone_names),
            title="[bold yellow]📋  REVIEW — WEAK SPOTS[/bold yellow]",
            subtitle="[dim]Challenges you've previously missed[/dim]",
            border_style="yellow",
            padding=(1, 4),
        ))
        console.print()

        # Let player pick a zone to review
        for i, zone_id in enumerate(weak_zones):
            zone = self.skill_pack.get_zone(zone_id)
            console.print(f"  [bold cyan][{i+1}][/bold cyan]  {zone['name'] if zone else zone_id}")
        console.print("  [dim][0]  Back[/dim]\n")

        raw = console.input("[cyan]Choose a zone to review: [/cyan]").strip()
        if not raw.isdigit() or int(raw) == 0:
            return
        idx = int(raw) - 1
        if 0 <= idx < len(weak_zones):
            self._review_zone(weak_zones[idx])

    def _review_zone(self, zone_id: str):
        """Play only the struggled challenges from a zone."""
        challenges = self.engine.get_review_challenges(zone_id)
        if not challenges:
            return

        zone = self.skill_pack.get_zone(zone_id)
        total = len(challenges)
        console.clear()
        render_banner(self.skill_pack)
        print_info(f"Reviewing {total} challenge(s) from {zone['name'] if zone else zone_id}...")
        _press_enter()

        for i, challenge in enumerate(challenges):
            result = self._run_challenge_loop(zone, challenge, i + 1, total, zone_id, 0)
            if result is None:
                return  # Player quit

    def _export_notes(self):
        """Export lesson notes from completed zones."""
        path = self.engine.export_notes()
        console.clear()
        render_banner(self.skill_pack)
        if path:
            console.print(Panel(
                f"[bold green]Notes exported![/bold green]\n\n"
                f"[white]All lessons from completed zones saved to:[/white]\n"
                f"[bold cyan]{path}[/bold cyan]\n\n"
                f"[dim]Open this file in any text editor to review your notes.[/dim]",
                title="[bold cyan]📄  NOTES EXPORTED[/bold cyan]",
                border_style="cyan",
                padding=(1, 4),
            ))
        else:
            console.print("[dim]No completed zones to export yet. Keep playing![/dim]")
        _press_enter()

    # ── Bookmarks ─────────────────────────────────────────────────────────────

    def _view_bookmarks(self):
        """Show bookmarked challenges and allow the player to jump to one."""
        bookmarks = render_bookmarks_screen(self.engine)
        if not bookmarks:
            return

        raw = console.input("[cyan]Enter number to practice (0 to back): [/cyan]").strip()
        if not raw.isdigit() or int(raw) == 0:
            return
        idx = int(raw) - 1
        if not (0 <= idx < len(bookmarks)):
            return

        ch = bookmarks[idx]
        zone = ch.get("_zone")
        if zone is None:
            return

        zone_id = zone["id"]
        total = len(self.skill_pack.get_zone_challenges(zone_id))
        challenge_num = next(
            (i + 1 for i, c in enumerate(self.skill_pack.get_zone_challenges(zone_id)) if c["id"] == ch["id"]),
            1,
        )
        self._run_challenge_loop(zone, ch, challenge_num, total, zone_id, 0)

    # ── Difficulty ────────────────────────────────────────────────────────────

    def _set_difficulty(self):
        """Let the player change difficulty mode from the main menu."""
        new_mode = render_difficulty_select()
        self.engine.difficulty_mode = new_mode
        self.engine.save()
        diff_colors = {"easy": "green", "normal": "white", "hard": "red"}
        color = diff_colors.get(new_mode, "white")
        console.print(f"\n[{color}]Difficulty set to {new_mode.title()}![/{color}]\n")
        _press_enter()

    # ── Personal Bests ────────────────────────────────────────────────────────

    def _personal_bests(self):
        """Show the personal bests screen and return."""
        render_personal_bests(self.engine)

    # ── Timed Drill ───────────────────────────────────────────────────────────

    def _timed_drill(self):
        """Run a timed blitz of mixed challenges. Player chooses duration."""
        import time as _time
        from rich import box as rbox

        # ── Duration picker ────────────────────────────────────────────────
        console.clear()
        render_banner(self.skill_pack)
        console.print(Panel(
            "[bold white]TIMED DRILL[/bold white]\n\n"
            "Race the clock through a mixed set of challenges.\n"
            "Wrong-answer challenges appear first, then completed zones,\n"
            "then new material.\n\n"
            "[bold yellow]Choose your duration:[/bold yellow]\n"
            "  [bold cyan][1][/bold cyan]  5 minutes   — Quick warm-up\n"
            "  [bold cyan][2][/bold cyan]  10 minutes  — Standard session\n"
            "  [bold cyan][3][/bold cyan]  15 minutes  — Deep practice\n"
            "  [bold cyan][0][/bold cyan]  Back",
            title="[bold cyan]⏱  TIMED DRILL[/bold cyan]",
            border_style="cyan",
            padding=(1, 4),
        ))
        console.print()

        duration_map = {"1": 5 * 60, "2": 10 * 60, "3": 15 * 60}
        while True:
            pick = console.input("[cyan]Duration: [/cyan]").strip()
            if pick == "0":
                return
            if pick in duration_map:
                drill_seconds = duration_map[pick]
                break
            console.print("[red]Choose 1, 2, 3, or 0.[/red]")

        # ── Load challenges ────────────────────────────────────────────────
        # Load more than we need; we'll cycle through them
        challenges = self.engine.get_drill_challenges(count=50)
        if not challenges:
            console.print(Panel(
                "[dim]No challenges available yet. Complete at least one zone first![/dim]",
                border_style="yellow",
            ))
            _press_enter()
            return

        # ── Run drill ─────────────────────────────────────────────────────
        drill_start = _time.time()
        drill_correct = 0
        drill_wrong = 0
        drill_xp = 0
        idx = 0
        total_available = len(challenges)

        while True:
            elapsed = _time.time() - drill_start
            remaining = drill_seconds - elapsed
            if remaining <= 0:
                break

            challenge = challenges[idx % total_available]
            idx += 1

            zone = challenge.get("_zone", {})
            zone_id = zone.get("id", "")
            num = idx
            mins_left = int(remaining // 60)
            secs_left = int(remaining % 60)

            # Show time remaining above challenge
            console.print(
                f"\n[dim]  ⏱  {mins_left}:{secs_left:02d} remaining  |  "
                f"✓ {drill_correct}  ✗ {drill_wrong}[/dim]"
            )

            result = self._run_challenge_loop(zone, challenge, num, total_available, zone_id, 0)

            if result is None:
                # Player quit the drill early
                break

            _xp, _lvl, hints_used = result
            drill_xp += _xp
            # Determine correct/wrong by XP: if XP > 0 and hints were 0, correct
            if _xp > 0:
                drill_correct += 1
            else:
                drill_wrong += 1

            # Re-check time after each challenge
            if _time.time() - drill_start >= drill_seconds:
                break

        # ── Drill summary ──────────────────────────────────────────────────
        total_answered = drill_correct + drill_wrong
        accuracy = int(drill_correct / total_answered * 100) if total_answered > 0 else 0
        elapsed_total = _time.time() - drill_start
        mins = int(elapsed_total // 60)
        secs = int(elapsed_total % 60)

        acc_color = "green" if accuracy >= 80 else "yellow" if accuracy >= 50 else "red"

        console.clear()
        render_banner(self.skill_pack)
        console.print(Panel(
            f"[bold white]Drill Complete![/bold white]\n\n"
            f"[dim]Time:[/dim]       [white]{mins}:{secs:02d}[/white]\n"
            f"[dim]Answered:[/dim]   [white]{total_answered}[/white] challenges\n"
            f"[dim]Correct:[/dim]    [bold green]{drill_correct}[/bold green]  "
            f"[dim]Wrong:[/dim] [bold red]{drill_wrong}[/bold red]\n"
            f"[dim]Accuracy:[/dim]   [{acc_color}]{accuracy}%[/{acc_color}]\n"
            f"[dim]XP earned:[/dim]  [bold yellow]+{drill_xp} XP[/bold yellow]",
            title="[bold cyan]⏱  DRILL RESULTS[/bold cyan]",
            border_style="cyan",
            box=rbox.ROUNDED,
            padding=(1, 4),
        ))
        self._show_new_achievements()
        _press_enter()

    # ── Daily Challenge ───────────────────────────────────────────────────────

    def _daily_challenge(self):
        """Fetch and run today's daily challenge."""
        from rich import box as rbox
        challenge = self.engine.get_daily_challenge(self.skill_pack)
        if challenge is None:
            console.clear()
            render_banner(self.skill_pack)
            console.print(Panel(
                "[dim]No challenges available in this pack.[/dim]",
                title="[bold yellow]★  DAILY CHALLENGE[/bold yellow]",
                border_style="yellow",
                padding=(1, 4),
            ))
            _press_enter()
            return

        if self.engine.daily_challenge_completed:
            console.clear()
            render_banner(self.skill_pack)
            console.print(Panel(
                "[bold green]You've already completed today's daily challenge![/bold green]\n\n"
                "[dim]Come back tomorrow for a new one.[/dim]",
                title="[bold yellow]★  DAILY CHALLENGE  ★[/bold yellow]",
                border_style="yellow",
                padding=(1, 4),
            ))
            _press_enter()
            return

        zone = challenge.get("_zone", {})
        zone_name = zone.get("name", "Unknown Zone")
        challenge_title = challenge.get("title", "Daily Challenge")
        base_xp = challenge.get("xp", 50)
        bonus_xp = max(100, base_xp * 2)

        console.clear()
        render_banner(self.skill_pack)
        console.print(Panel(
            f"[bold white]{challenge_title}[/bold white]\n"
            f"[dim]Zone: {zone_name}[/dim]\n\n"
            f"[yellow]Complete this challenge to earn [bold]+{bonus_xp} XP[/bold] (2× bonus)![/yellow]\n"
            f"[dim]Daily challenge streak: {self.engine.daily_challenge_streak} day(s)[/dim]",
            title="[bold yellow]★  TODAY'S DAILY CHALLENGE  ★[/bold yellow]",
            border_style="bold yellow",
            box=rbox.DOUBLE,
            padding=(1, 4),
        ))
        console.print()
        _press_enter()

        # Run the challenge — use zone_id from zone dict or empty string fallback
        zone_id = zone.get("id", "")
        result = self._run_challenge_loop(zone, challenge, 1, 1, zone_id, 0)

        if result is not None:
            # Challenge was attempted and not quit — award bonus XP and mark done
            _xp, _lvl, _hints = result
            actual_bonus, leveled_up = self.engine.award_xp(bonus_xp)
            self.engine.complete_daily_challenge()

            console.print()
            console.print(Panel(
                f"[bold green]Daily Challenge Complete![/bold green]\n\n"
                f"[bold yellow]+{actual_bonus} XP[/bold yellow] [dim](2× daily bonus)[/dim]\n"
                f"[dim]Challenge streak: {self.engine.daily_challenge_streak} day(s)[/dim]",
                title="[bold yellow]★  DAILY BONUS  ★[/bold yellow]",
                border_style="bold yellow",
                box=rbox.ROUNDED,
                padding=(1, 4),
            ))

            if leveled_up:
                celebrate_level_up(self.engine.level, self.engine.level_title)

            self._show_new_achievements()
            _press_enter()

    # ── New Game ──────────────────────────────────────────────────────────────

    def _new_game(self):
        if self.engine.total_challenges_completed() > 0:
            if not confirm_new_game():
                return

        console.clear()
        render_banner(self.skill_pack)
        print_narrative(self.skill_pack.intro_story)

        name = render_name_prompt(self.skill_pack)
        self.engine.reset()
        self.engine.player_name = name
        self.engine.current_zone = self.skill_pack.zone_order[0]
        self.engine.save()

        console.print(f"\n[bold cyan]Welcome, {name}. Your quest begins...[/bold cyan]\n")
        _press_enter()

        self._play_zone(self.skill_pack.zone_order[0])

    # ── Continue ──────────────────────────────────────────────────────────────

    def _continue_game(self):
        if self.engine.total_challenges_completed() == 0:
            console.print("\n[yellow]No saved progress found. Starting a new game![/yellow]")
            _press_enter()
            self._new_game()
            return

        self._play_zone(self.engine.current_zone)

    # ── Zone Select ───────────────────────────────────────────────────────────

    def _zone_select(self):
        all_zones = self.skill_pack.get_all_zones()
        zone_id = render_zone_select(self.engine, all_zones)
        if zone_id is None:
            return
        # Show a zone preview before committing
        zone = self.skill_pack.get_zone(zone_id)
        if zone:
            render_zone_preview(zone, self.engine)
        self.engine.current_zone = zone_id
        self.engine.save()
        self._play_zone(zone_id)

    # ── Zone Flow ─────────────────────────────────────────────────────────────

    def _play_zone(self, zone_id: str):
        zone = self.skill_pack.get_zone(zone_id)
        if not zone:
            print_warning(f"Zone '{zone_id}' not found!")
            return

        completed_here = self.engine.challenges_completed_in_zone(zone_id)
        already_done = zone_id in self.engine.completed_zones
        if not completed_here and not already_done:
            intro_text = self.skill_pack.zone_intros.get(zone_id, "")
            render_zone_intro(intro_text, zone, self.skill_pack)
        elif already_done and not completed_here:
            # Replay mode — brief reminder
            stars = self.engine.get_zone_stars(zone_id)
            console.clear()
            from .ui import _zone_star_str
            console.print(f"\n[bold cyan]Replaying: {zone['name']}[/bold cyan]  {_zone_star_str(stars)}")
            console.print(f"[dim]Answer every question correctly with no hints to earn ★★★[/dim]\n")
            _press_enter()

        challenges = self.skill_pack.get_zone_challenges(zone_id)
        total = len(challenges)
        zone_xp_earned = 0
        hints_used_this_zone = 0

        for i, challenge in enumerate(challenges):
            challenge_id = challenge["id"]

            if self.engine.is_challenge_complete(zone_id, challenge_id):
                continue

            if challenge.get("is_boss"):
                boss_intro = self.skill_pack.boss_intros.get(zone_id, "A great trial awaits...")
                render_boss_intro(boss_intro, challenge["title"])

            result = self._run_challenge_loop(
                zone, challenge, i + 1, total, zone_id, hints_used_this_zone
            )

            if result is None:
                return

            xp_gained, leveled_up, hints_this = result
            zone_xp_earned += xp_gained
            hints_used_this_zone += hints_this

        completed = self.engine.challenges_completed_in_zone(zone_id)
        all_ids = {ch["id"] for ch in challenges}
        just_completed = all_ids.issubset(completed) and zone_id not in self.engine.completed_zones

        if just_completed:
            self.engine.mark_zone_complete(zone_id)

            if hints_used_this_zone == 0:
                self.engine.unlock_achievement("no_hints")

            animate_zone_progress(self.engine, zone_id)

            stars = self.engine.get_zone_stars(zone_id)
            completion_text = self.skill_pack.zone_completions.get(zone_id, "Zone Complete!")
            render_zone_complete(completion_text, zone, zone_xp_earned, stars=stars)

            self._show_new_achievements()

            # Show completion certificate if the whole pack is now done
            if self.engine.is_pack_complete(self.skill_pack):
                render_completion_certificate(self.engine, self.skill_pack)

            current_idx = self.skill_pack.zone_order.index(zone_id)
            if current_idx < len(self.skill_pack.zone_order) - 1:
                next_zone_id = self.skill_pack.zone_order[current_idx + 1]
                self.engine.current_zone = next_zone_id
                self.engine.save()

                next_zone = self.skill_pack.get_zone(next_zone_id)
                console.print(f"\n[bold cyan]Proceeding to {next_zone['name']}...[/bold cyan]")
                _press_enter()
                self._play_zone(next_zone_id)

        elif zone_id in self.engine.completed_zones:
            # Already completed — offer replay for better score
            stars = self.engine.get_zone_stars(zone_id)
            if stars < 3:
                console.print(f"\n[dim]Zone already complete. Replay to improve your star rating?[/dim]")
                raw = console.input("[cyan]Replay for better score? (y/n): [/cyan]").strip().lower()
                if raw in ("y", "yes"):
                    # Reset zone scores but not completion, then replay
                    self.engine.zone_scores.pop(zone_id, None)
                    self.engine.save()
                    self._play_zone(zone_id)
        else:
            remaining = all_ids - completed
            if remaining:
                console.print(f"\n[yellow]{len(remaining)} challenge(s) remaining in this zone.[/yellow]")

    def _run_challenge_loop(self, zone, challenge, num, total, zone_id, hints_so_far):
        hint_index = 0
        hints_used = 0
        attempts = 0
        xp_gained = 0
        leveled_up = False
        show_lesson = False

        while True:
            console.clear()
            console.print()
            stats_panel = render_stats_panel(self.engine)
            console.print(stats_panel)
            render_separator()
            console.print(render_challenge_panel(challenge, zone, num, total, show_lesson=show_lesson))
            render_challenge_menu(has_url=bool(challenge.get("url")))

            ctype = challenge.get("type", "quiz")
            user_input = prompt_command(ctype).strip()

            if not user_input:
                continue

            lower = user_input.lower()
            # Quiz option letters (a/b/c/d) must never be intercepted by shortcuts
            is_quiz_answer = ctype == "quiz" and lower in ("a", "b", "c", "d")

            if lower in ("q", "quit", "menu", ":q"):
                return None
            elif not is_quiz_answer and lower in ("h", "hint"):
                diff = getattr(self.engine, "difficulty_mode", "normal")
                hint_display_cost = 0 if diff == "easy" else (15 if diff == "hard" else 10)
                cost_ok = self.engine.pay_hint_cost()
                hint_text = self.runner.get_hint(challenge, hint_index)
                render_hint(hint_text, hint_display_cost)
                if cost_ok:
                    hint_index += 1
                    hints_used += 1
                else:
                    print_warning("Not enough XP for a hint!")
                _press_enter()
                continue
            elif not is_quiz_answer and lower in ("l", "lesson"):
                show_lesson = not show_lesson
                continue
            elif not is_quiz_answer and lower in ("b", "bookmark"):
                is_bookmarked = self.engine.toggle_bookmark(zone_id, challenge["id"])
                if is_bookmarked:
                    console.print("\n[bold yellow]★ Bookmarked![/bold yellow]")
                else:
                    console.print("\n[dim yellow]★ Bookmark removed[/dim yellow]")
                _press_enter()
                continue
            elif not is_quiz_answer and lower in ("d", "difficulty"):
                new_mode = render_difficulty_select()
                self.engine.difficulty_mode = new_mode
                self.engine.save()
                diff_colors = {"easy": "green", "normal": "white", "hard": "red"}
                color = diff_colors.get(new_mode, "white")
                console.print(f"\n[{color}]Difficulty set to {new_mode.title()}![/{color}]")
                _press_enter()
                continue
            elif lower in ("?", "help"):
                render_help_screen()
                continue
            elif lower in ("v", "view"):
                url = challenge.get("url")
                if url:
                    import webbrowser
                    webbrowser.open(url)
                    console.print(f"\n[bold cyan]Opening in browser...[/bold cyan]")
                    console.print(f"[dim]{url}[/dim]")
                else:
                    console.print("\n[dim]No resource linked for this challenge.[/dim]")
                _press_enter()
                continue
            elif lower in ("s", "skip"):
                print_info("Challenge skipped. You can come back to it later.")
                self.engine.record_incorrect()
                _press_enter()
                return (0, False, hints_used)

            self.engine.start_challenge_timer()
            result, output = self.runner.run_challenge(challenge, user_input)
            elapsed = self.engine.get_elapsed()

            if output.strip() and ctype == "live":
                render_output(output)

            if result.success:
                self.engine.record_correct()
                self.engine.check_speed_achievement()
                self.engine.record_zone_attempt(zone_id, challenge["id"], correct=True, used_hint=hints_used > 0)

                is_new_record = self.engine.try_set_speed_record(zone_id, challenge["id"], elapsed)

                base_xp = challenge.get("xp", 50)
                actual_xp, did_level_up = self.engine.award_xp(base_xp)
                xp_gained += actual_xp
                leveled_up = leveled_up or did_level_up

                self.engine.mark_challenge_complete(zone_id, challenge["id"])

                if is_new_record:
                    render_new_record_flash(elapsed)

                render_result(
                    True,
                    result.message,
                    xp_gained=base_xp,
                    leveled_up=did_level_up,
                    streak=self.engine.streak,
                    actual_xp=actual_xp,
                )

                if did_level_up:
                    celebrate_level_up(self.engine.level, self.engine.level_title)

                self._show_new_achievements()
                _press_enter()
                return (xp_gained, leveled_up, hints_used)
            else:
                self.engine.record_incorrect()
                self.engine.record_zone_attempt(zone_id, challenge["id"], correct=False, used_hint=False)
                attempts += 1

                render_result(False, result.message)

                if attempts == 1:
                    show_lesson = True
                    console.print(f"\n[dim]Study the lesson above, then try again.[/dim]")
                else:
                    hint_text = self.runner.get_hint(challenge, hint_index)
                    render_hint(hint_text, 0)
                    hint_index = min(hint_index + 1, len(challenge.get("hints", [])) - 1)
                _press_enter()

    def run_linear(self) -> bool:
        """
        Play all zones in sequence without showing the main menu.
        Used by CampaignSession to drive a pack as a chapter.
        Returns True if all zones completed, False if player quit mid-pack.
        """
        first_incomplete = next(
            (z for z in self.skill_pack.zone_order if z not in self.engine.completed_zones),
            None,
        )
        if first_incomplete is None:
            return True  # pack already fully complete

        self._play_zone(first_incomplete)
        # _play_zone chains through remaining zones automatically via recursion

        return all(z in self.engine.completed_zones for z in self.skill_pack.zone_order)

    def _show_new_achievements(self):
        new_ach = self.engine.pop_new_achievements()
        for ach_id in new_ach:
            render_achievement(ach_id, self.skill_pack.achievements)


# ── Entry Points ───────────────────────────────────────────────────────────────

def run(pack_name: str = "bash"):
    try:
        skill_pack = load_skill_pack(pack_name)
        session = GameSession(skill_pack)
        session.run()
    except KeyboardInterrupt:
        console.print("\n\n[bold cyan]Disconnecting...[/bold cyan]\n")
        sys.exit(0)
    except ValueError as e:
        console.print(f"\n[bold red]{e}[/bold red]\n")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error: {e}[/bold red]")
        console.print_exception()
        sys.exit(1)


def main():
    pack_name = sys.argv[1] if len(sys.argv) > 1 else "bash"
    run(pack_name)


def main_postgres():
    run("postgres")


def main_git():
    run("git")


def main_docker():
    run("docker")


def run_campaign(campaign_name: str = "nexus"):
    try:
        from .campaign import load_campaign, CampaignSession
        campaign = load_campaign(campaign_name)
        session = CampaignSession(campaign)
        session.run()
    except KeyboardInterrupt:
        console.print("\n\n[bold cyan]Campaign paused...[/bold cyan]\n")
        sys.exit(0)
    except ValueError as e:
        console.print(f"\n[bold red]{e}[/bold red]\n")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error: {e}[/bold red]")
        console.print_exception()
        sys.exit(1)


def main_nexus():
    run_campaign("nexus")


def main_vim():
    run("vim")


def main_ssh():
    run("ssh")
