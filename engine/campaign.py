"""
campaign.py - Campaign system for Quest Engine

A Campaign ties multiple SkillPacks into a single continuous narrative.
Each chapter = one skill pack, played in linear mode (no main menu).
Campaign save state is stored separately from individual pack saves.
"""

import importlib
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from rich import box as rbox
from rich.align import Align
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .ui import console, print_narrative, _press_enter, render_separator

SAVE_BASE = Path.home() / ".quest_engine"


# ── Campaign Dataclass ────────────────────────────────────────────────────────

@dataclass
class ChapterDef:
    """One chapter in a campaign. Maps to a single skill pack."""
    pack_name: str         # matches directory under skill-packs/
    title: str             # "Chapter 1: The Shell Awakens"
    intro_bridge: str      # narrative shown BEFORE chapter starts
    outro_bridge: str      # narrative shown AFTER chapter ends
    entry_summary: str = ""   # shown when player jumps here after skipping prior chapters
    recommended_age: str = ""  # hint used by placement quiz, e.g. "5-7"


@dataclass
class Campaign:
    """Top-level campaign definition. Exported as CAMPAIGN from campaigns/<name>/__init__.py."""
    id: str
    title: str
    subtitle: str
    save_file_name: str    # ~/.quest_engine/<save_file_name>/campaign.json
    intro_story: str       # shown once at campaign start
    final_story: str       # shown when all chapters complete
    quit_message: str
    chapters: list         # list[ChapterDef] in play order
    banner_ascii: Optional[str] = None
    achievements: dict = field(default_factory=dict)
    player_name_prompt: str = "What do they call you, Agent?"
    default_player_name: str = "Ghost"
    placement_questions: list = field(default_factory=list)  # assessment quiz at campaign start


# ── Campaign Loader ───────────────────────────────────────────────────────────

def load_campaign(name: str, *, campaigns_dir=None) -> Campaign:
    """Dynamically import a campaign by name from the campaigns/ directory.

    Resolution order for the campaigns directory:
      1. explicit campaigns_dir argument
      2. QUEST_CAMPAIGNS_DIR environment variable
      3. <repo-root>/campaigns/ (default for the monorepo layout)
    """
    import os
    if campaigns_dir is None:
        env_dir = os.environ.get("QUEST_CAMPAIGNS_DIR")
        campaigns_dir = Path(env_dir) if env_dir else Path(__file__).parent.parent / "campaigns"
    else:
        campaigns_dir = Path(campaigns_dir)

    if str(campaigns_dir) not in sys.path:
        sys.path.insert(0, str(campaigns_dir))

    try:
        module = importlib.import_module(name)
        if not hasattr(module, "CAMPAIGN"):
            raise ImportError(f"Campaign '{name}' must export a CAMPAIGN instance.")
        campaign = module.CAMPAIGN
        if not isinstance(campaign, Campaign):
            raise TypeError(f"CAMPAIGN in '{name}' must be a Campaign instance.")
        return campaign
    except ModuleNotFoundError:
        available = [
            p.name for p in Path(campaigns_dir).iterdir()
            if p.is_dir() and (p / "__init__.py").exists()
        ]
        raise ValueError(
            f"Campaign '{name}' not found.\n"
            f"Available campaigns: {', '.join(sorted(available))}"
        )


# ── Campaign Save ─────────────────────────────────────────────────────────────

class CampaignSave:
    """
    Handles campaign-level progress. Stored separately from individual pack saves.
    Schema: { campaign_id, player_name, current_chapter_index, completed_chapters, started_at }
    """

    def __init__(self, campaign: Campaign):
        self._campaign = campaign
        self._save_dir = SAVE_BASE / campaign.save_file_name
        self._save_file = self._save_dir / "campaign.json"

        self.player_name = "Ghost"
        self.current_chapter_index = 0
        self.completed_chapters: list = []
        self.started_at: Optional[str] = None
        self.placement_done: bool = False
        self.skipped_chapters: list = []
        self.starting_chapter_index: int = 0

        self._load()

    def _load(self):
        if not self._save_file.exists():
            return
        try:
            with open(self._save_file) as f:
                data = json.load(f)
            if data.get("campaign_id") != self._campaign.id:
                return
            self.player_name = data.get("player_name", "Ghost")
            self.current_chapter_index = data.get("current_chapter_index", 0)
            self.completed_chapters = data.get("completed_chapters", [])
            self.started_at = data.get("started_at")
            self.placement_done = data.get("placement_done", False)
            self.skipped_chapters = data.get("skipped_chapters", [])
            self.starting_chapter_index = data.get("starting_chapter_index", 0)
        except (json.JSONDecodeError, KeyError):
            pass

    def save(self):
        self._save_dir.mkdir(parents=True, exist_ok=True)
        with open(self._save_file, "w") as f:
            json.dump({
                "campaign_id": self._campaign.id,
                "player_name": self.player_name,
                "current_chapter_index": self.current_chapter_index,
                "completed_chapters": self.completed_chapters,
                "started_at": self.started_at,
                "placement_done": self.placement_done,
                "skipped_chapters": self.skipped_chapters,
                "starting_chapter_index": self.starting_chapter_index,
            }, f, indent=2)

    def mark_chapter_complete(self, pack_name: str):
        if pack_name not in self.completed_chapters:
            self.completed_chapters.append(pack_name)
        chapters = self._campaign.chapters
        for i, ch in enumerate(chapters):
            if ch.pack_name not in self.completed_chapters:
                self.current_chapter_index = i
                break
        else:
            self.current_chapter_index = len(chapters)
        self.save()

    def is_chapter_complete(self, pack_name: str) -> bool:
        return pack_name in self.completed_chapters

    def is_campaign_complete(self) -> bool:
        return all(ch.pack_name in self.completed_chapters for ch in self._campaign.chapters)

    def has_progress(self) -> bool:
        return bool(self.completed_chapters)

    def mark_chapter_skipped(self, pack_name: str):
        if pack_name not in self.skipped_chapters:
            self.skipped_chapters.append(pack_name)
        self.save()

    def reset(self, player_name: str, starting_chapter_index: int = 0):
        import datetime
        self.player_name = player_name
        self.current_chapter_index = starting_chapter_index
        self.starting_chapter_index = starting_chapter_index
        self.completed_chapters = []
        self.skipped_chapters = []
        self.started_at = str(datetime.date.today())
        self.save()


# ── Campaign Session ──────────────────────────────────────────────────────────

class CampaignSession:
    def __init__(self, campaign: Campaign):
        self.campaign = campaign
        self.csave = CampaignSave(campaign)

    # ── Main Loop ─────────────────────────────────────────────────────────────

    def run(self):
        while True:
            choice = self._render_menu()
            if choice == "1":
                self._new_campaign()
            elif choice == "2" and self.csave.has_progress():
                self._continue_campaign()
            elif choice == "3":
                self._show_chapter_map()
            elif choice == "j" and self.csave.has_progress():
                self._jump_to_chapter()
            elif choice == "0":
                self._quit()
                break

    # ── Menu ──────────────────────────────────────────────────────────────────

    def _render_menu(self) -> str:
        console.clear()
        _render_campaign_banner(self.campaign)

        completed = self.csave.completed_chapters
        total = len(self.campaign.chapters)
        current_idx = self.csave.current_chapter_index

        # Chapter status list
        table = Table.grid(padding=(0, 2))
        table.add_column()
        table.add_column()
        for i, ch in enumerate(self.campaign.chapters):
            if ch.pack_name in completed:
                status = "[bold green]✓[/bold green]"
                label = f"[dim]Chapter {i + 1}: {ch.title}[/dim]"
                if ch.recommended_age:
                    label += f" [dim](ages {ch.recommended_age})[/dim]"
            elif i == current_idx and self.csave.has_progress():
                status = "[bold yellow]▶[/bold yellow]"
                label = f"[bold]Chapter {i + 1}: {ch.title}[/bold] [dim](in progress)[/dim]"
            else:
                status = "[dim]·[/dim]"
                label = f"[dim]Chapter {i + 1}: {ch.title}[/dim]"
                if ch.recommended_age:
                    label += f" [dim](ages {ch.recommended_age})[/dim]"
            table.add_row(status, label)

        console.print(Panel(
            table,
            title="[bold cyan]CHAPTERS[/bold cyan]",
            border_style="dim cyan",
            box=rbox.SIMPLE,
            padding=(0, 2),
        ))

        progress_text = f"{len(completed)}/{total} chapters complete"
        if self.csave.has_progress() and self.csave.player_name != self.campaign.default_player_name:
            progress_text = f"{self.csave.player_name}  ·  {progress_text}"
        console.print(f"  [dim]{progress_text}[/dim]\n")

        console.print("  [bold cyan][1][/bold cyan] New Campaign")
        if self.csave.has_progress() and not self.csave.is_campaign_complete():
            console.print("  [bold cyan][2][/bold cyan] Continue")
        elif self.csave.is_campaign_complete():
            console.print("  [bold green][2][/bold green] Replay / Review")
        console.print("  [bold cyan][3][/bold cyan] Chapter Map")
        if self.csave.has_progress():
            console.print("  [bold cyan][j][/bold cyan] Jump to Chapter")
        console.print("  [bold cyan][0][/bold cyan] Exit\n")

        return console.input("[bold cyan]>[/bold cyan] ").strip().lower()

    # ── New Campaign ──────────────────────────────────────────────────────────

    def _new_campaign(self):
        if self.csave.has_progress():
            console.print("\n[bold red]This will reset your campaign progress (pack progress is preserved).[/bold red]")
            answer = console.input("[cyan]Continue? (yes/no): [/cyan]").strip().lower()
            if answer not in ("yes", "y"):
                return

        console.clear()
        _render_campaign_banner(self.campaign)
        print_narrative(self.campaign.intro_story)

        console.print(f"\n[bold cyan]{self.campaign.player_name_prompt}[/bold cyan]")
        name = console.input("[cyan]> [/cyan]").strip()
        if not name:
            name = self.campaign.default_player_name

        # Run placement quiz if campaign has one
        start_index = 0
        if self.campaign.placement_questions:
            start_index = self._run_placement(name)

        self.csave.reset(name, starting_chapter_index=start_index)
        _press_enter()
        self._play_from(start_index)

    # ── Placement Quiz ────────────────────────────────────────────────────────

    def _run_placement(self, player_name: str) -> int:
        """
        Run the placement assessment. Returns the recommended starting chapter index.
        Questions are structured as:
          { "question": str, "options": [str, ...], "answer": "a"|"b"|..., "chapter": int }
        where "chapter" is the index the question tests competency for.
        """
        questions = self.campaign.placement_questions
        if not questions:
            return 0

        console.clear()
        _render_campaign_banner(self.campaign)

        console.print(Panel(
            f"[bold yellow]Hi {player_name}! Let's figure out the best place for you to start.[/bold yellow]\n\n"
            "[cyan]Puck will ask a few quick questions. There are no wrong answers —\n"
            "they just help the Primer know where to begin your adventure.[/cyan]\n\n"
            "[dim]If you need a helper to read the questions aloud, ask them now![/dim]",
            title="[bold cyan]FINDING YOUR STARTING PLACE[/bold cyan]",
            border_style="cyan",
            box=rbox.DOUBLE,
            padding=(1, 4),
        ))
        _press_enter()

        scores_by_chapter = {}  # chapter_index -> (correct, total)

        for q_idx, q in enumerate(questions):
            console.clear()
            _render_campaign_banner(self.campaign)

            chapter_idx = q.get("chapter", 0)
            options = q.get("options", [])
            correct_letter = q.get("answer", "a").lower()

            # Build display
            lines = [f"[bold white]Question {q_idx + 1} of {len(questions)}[/bold white]\n"]
            lines.append(f"[bold]{q['question']}[/bold]\n")
            for j, opt in enumerate(options):
                letter = chr(ord("a") + j)
                lines.append(f"  [bold cyan]{letter.upper()}.[/bold cyan]  {opt}")

            console.print(Panel(
                "\n".join(lines),
                border_style="cyan",
                box=rbox.SIMPLE,
                padding=(1, 4),
            ))

            raw = console.input("\n[cyan]Your answer (A/B/C/D): [/cyan]").strip().lower()
            if raw and raw[0] in "abcd":
                answer_letter = raw[0]
            else:
                answer_letter = ""

            correct = (answer_letter == correct_letter)

            if chapter_idx not in scores_by_chapter:
                scores_by_chapter[chapter_idx] = [0, 0]
            scores_by_chapter[chapter_idx][1] += 1
            if correct:
                scores_by_chapter[chapter_idx][0] += 1
                console.print("[bold green]  ✓ Great![/bold green]")
            else:
                console.print(f"[dim]  The answer was {correct_letter.upper()}. That's okay![/dim]")

            import time
            time.sleep(0.8)

        # Determine starting chapter: find the first chapter index where score < 100%
        chapters = self.campaign.chapters
        recommended = 0
        for i in range(len(chapters)):
            if i in scores_by_chapter:
                correct, total = scores_by_chapter[i]
                if total > 0 and correct == total:
                    # Full marks on this chapter's questions → can skip it
                    recommended = i + 1
                else:
                    break
            # No questions for this chapter → always start here if not skipped by prior

        recommended = min(recommended, len(chapters) - 1)

        # Show result
        console.clear()
        _render_campaign_banner(self.campaign)

        if recommended == 0:
            result_msg = (
                f"[bold cyan]Puck smiles.[/bold cyan]\n\n"
                f"[white]Let's start at the very beginning — [bold]{chapters[0].title}[/bold].\n"
                f"That's where every great adventure starts.[/white]"
            )
        else:
            ch = chapters[recommended]
            result_msg = (
                f"[bold cyan]Puck is impressed![/bold cyan]\n\n"
                f"[white]You already know quite a bit! Let's start you at\n"
                f"[bold]{ch.title}[/bold] — Chapter {recommended + 1}.[/white]\n\n"
                f"[dim]You can always go back to earlier chapters from the Chapter Map.[/dim]"
            )

        console.print(Panel(
            result_msg,
            title="[bold yellow]YOUR STARTING CHAPTER[/bold yellow]",
            border_style="yellow",
            box=rbox.DOUBLE,
            padding=(1, 4),
        ))
        _press_enter()

        return recommended

    # ── Continue ──────────────────────────────────────────────────────────────

    def _continue_campaign(self):
        self._play_from(self.csave.current_chapter_index)

    # ── Chapter Map ───────────────────────────────────────────────────────────

    def _show_chapter_map(self):
        console.clear()
        _render_campaign_banner(self.campaign)
        completed = self.csave.completed_chapters
        skipped = self.csave.skipped_chapters

        table = Table(
            show_header=True,
            header_style="bold cyan",
            box=rbox.SIMPLE,
            padding=(0, 2),
        )
        table.add_column("#", style="dim", width=4)
        table.add_column("Chapter")
        if any(ch.recommended_age for ch in self.campaign.chapters):
            table.add_column("Ages", style="dim")
        table.add_column("Status", justify="center")

        show_ages = any(ch.recommended_age for ch in self.campaign.chapters)
        for i, ch in enumerate(self.campaign.chapters):
            if ch.pack_name in completed:
                status = "[bold green]COMPLETE[/bold green]"
            elif ch.pack_name in skipped:
                status = "[bold yellow]SKIPPED[/bold yellow]"
            else:
                status = "[dim]pending[/dim]"
            row = [str(i + 1), ch.title]
            if show_ages:
                row.append(ch.recommended_age or "—")
            row.append(status)
            table.add_row(*row)

        console.print(table)
        console.print()
        _press_enter()

    # ── Jump to Chapter ───────────────────────────────────────────────────────

    def _jump_to_chapter(self):
        console.clear()
        _render_campaign_banner(self.campaign)
        completed = self.csave.completed_chapters

        console.print("[bold cyan]Jump to Chapter[/bold cyan]\n")
        for i, ch in enumerate(self.campaign.chapters):
            marker = "[bold green]✓[/bold green]" if ch.pack_name in completed else f"[dim]{i + 1}[/dim]"
            age_hint = f" [dim](ages {ch.recommended_age})[/dim]" if ch.recommended_age else ""
            console.print(f"  {marker}  {i + 1}. {ch.title}{age_hint}")

        console.print()
        raw = console.input("[cyan]Enter chapter number (or Enter to cancel): [/cyan]").strip()
        if not raw or not raw.isdigit():
            return

        idx = int(raw) - 1
        if idx < 0 or idx >= len(self.campaign.chapters):
            console.print("[red]Invalid chapter number.[/red]")
            _press_enter()
            return

        ch = self.campaign.chapters[idx]
        if ch.pack_name in completed:
            console.print(f"\n[dim]You already completed {ch.title}. Replaying...[/dim]")
            _press_enter()

        # Mark any prior incomplete chapters as skipped
        for j in range(idx):
            prior = self.campaign.chapters[j]
            if prior.pack_name not in completed:
                self.csave.mark_chapter_skipped(prior.pack_name)

        self.csave.current_chapter_index = idx
        self.csave.save()
        self._play_from(idx)

    # ── Chapter Playthrough ───────────────────────────────────────────────────

    def _play_from(self, start_index: int):
        for i in range(start_index, len(self.campaign.chapters)):
            ch = self.campaign.chapters[i]

            if self.csave.is_chapter_complete(ch.pack_name):
                continue

            # Entry summary: shown when prior chapters were not completed normally
            has_prior_skipped = any(
                self.campaign.chapters[j].pack_name not in self.csave.completed_chapters
                for j in range(i)
            )
            if has_prior_skipped and ch.entry_summary and i > 0:
                console.clear()
                _render_campaign_banner(self.campaign)
                console.print(Panel(
                    f"[italic]{ch.entry_summary}[/italic]",
                    title="[bold dim]Previously in The Primer...[/bold dim]",
                    border_style="dim yellow",
                    box=rbox.SIMPLE,
                    padding=(1, 4),
                ))
                _press_enter()

            # Intro bridge
            console.clear()
            _render_campaign_banner(self.campaign)
            console.print(Panel(
                f"[italic]{ch.intro_bridge}[/italic]",
                title=f"[bold yellow]Chapter {i + 1} of {len(self.campaign.chapters)}: {ch.title.upper()}[/bold yellow]",
                border_style="bold yellow",
                box=rbox.DOUBLE,
                padding=(1, 4),
            ))
            _press_enter()

            # Load pack and run in linear mode
            from .skill_pack import load_skill_pack
            from .main import GameSession
            pack = load_skill_pack(ch.pack_name)
            session = GameSession(pack)
            session.engine.player_name = self.csave.player_name

            completed_ok = session.run_linear()

            if not completed_ok:
                # Player quit mid-chapter
                self.csave.current_chapter_index = i
                self.csave.save()
                return

            # Mark complete, show outro
            self.csave.mark_chapter_complete(ch.pack_name)

            console.clear()
            _render_campaign_banner(self.campaign)
            console.print(Panel(
                f"[italic]{ch.outro_bridge}[/italic]",
                title=f"[bold green]Chapter {i + 1} Complete: {ch.title}[/bold green]",
                border_style="bold green",
                box=rbox.DOUBLE,
                padding=(1, 4),
            ))
            _press_enter()

        if self.csave.is_campaign_complete():
            self._campaign_complete()

    # ── Campaign Complete ─────────────────────────────────────────────────────

    def _campaign_complete(self):
        console.clear()
        _render_campaign_banner(self.campaign)
        print_narrative(self.campaign.final_story)
        _press_enter()

    # ── Quit ──────────────────────────────────────────────────────────────────

    def _quit(self):
        console.clear()
        _render_campaign_banner(self.campaign)
        console.print(f"\n[bold cyan]{self.campaign.quit_message}[/bold cyan]\n")
        console.print("[dim]Campaign progress saved.[/dim]\n")


# ── UI Helpers ────────────────────────────────────────────────────────────────

def _render_campaign_banner(campaign: Campaign):
    """Render the campaign's ASCII banner and subtitle."""
    ascii_art = campaign.banner_ascii or ""
    if ascii_art:
        console.print(Align.center(Text(ascii_art, style="bold cyan")))
    console.print(Align.center(Text(campaign.subtitle, style="bold yellow")))
    console.print()
