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

    def reset(self, player_name: str):
        import datetime
        self.player_name = player_name
        self.current_chapter_index = 0
        self.completed_chapters = []
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
            elif i == current_idx and self.csave.has_progress():
                status = "[bold yellow]▶[/bold yellow]"
                label = f"[bold]Chapter {i + 1}: {ch.title}[/bold] [dim](in progress)[/dim]"
            else:
                status = "[dim]·[/dim]"
                label = f"[dim]Chapter {i + 1}: {ch.title}[/dim]"
            table.add_row(status, label)

        console.print(Panel(
            table,
            title="[bold cyan]CHAPTERS[/bold cyan]",
            border_style="dim cyan",
            box=rbox.SIMPLE,
            padding=(0, 2),
        ))

        progress_text = f"{len(completed)}/{total} chapters complete"
        console.print(f"  [dim]{progress_text}[/dim]\n")

        console.print("  [bold cyan][1][/bold cyan] New Campaign")
        if self.csave.has_progress() and not self.csave.is_campaign_complete():
            console.print("  [bold cyan][2][/bold cyan] Continue")
        elif self.csave.is_campaign_complete():
            console.print("  [bold green][2][/bold green] Replay / Review")
        console.print("  [bold cyan][3][/bold cyan] Chapter Map")
        console.print("  [bold cyan][0][/bold cyan] Exit\n")

        return console.input("[bold cyan]>[/bold cyan] ").strip()

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

        self.csave.reset(name)
        _press_enter()
        self._play_from(0)

    # ── Continue ──────────────────────────────────────────────────────────────

    def _continue_campaign(self):
        self._play_from(self.csave.current_chapter_index)

    # ── Chapter Map ───────────────────────────────────────────────────────────

    def _show_chapter_map(self):
        console.clear()
        _render_campaign_banner(self.campaign)
        completed = self.csave.completed_chapters

        table = Table(
            show_header=True,
            header_style="bold cyan",
            box=rbox.SIMPLE,
            padding=(0, 2),
        )
        table.add_column("#", style="dim", width=4)
        table.add_column("Chapter")
        table.add_column("Pack", style="dim")
        table.add_column("Status", justify="center")

        for i, ch in enumerate(self.campaign.chapters):
            status = "[bold green]COMPLETE[/bold green]" if ch.pack_name in completed else "[dim]pending[/dim]"
            table.add_row(str(i + 1), ch.title, ch.pack_name, status)

        console.print(table)
        console.print()
        _press_enter()

    # ── Chapter Playthrough ───────────────────────────────────────────────────

    def _play_from(self, start_index: int):
        for i in range(start_index, len(self.campaign.chapters)):
            ch = self.campaign.chapters[i]

            if self.csave.is_chapter_complete(ch.pack_name):
                continue

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
