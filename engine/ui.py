"""
ui.py - Rich TUI components for Quest Engine
Fully generic — all skill-specific text comes from engine.skill_pack.
"""

import datetime
import time
from typing import Optional

from rich import box
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.rule import Rule
from rich.style import Style
from rich.table import Table
from rich.text import Text

console = Console()

DIFFICULTY_COLORS = {
    "easy": "green",
    "medium": "yellow",
    "hard": "red",
    "boss": "bold red",
}

DIFFICULTY_STARS = {
    "easy": "★☆☆☆",
    "medium": "★★☆☆",
    "hard": "★★★☆",
    "boss": "★★★★",
}

DEFAULT_BANNER = r"""
  ██████╗ ██╗   ██╗███████╗███████╗████████╗
 ██╔═══██╗██║   ██║██╔════╝██╔════╝╚══██╔══╝
 ██║   ██║██║   ██║█████╗  ███████╗   ██║
 ██║▄▄ ██║██║   ██║██╔══╝  ╚════██║   ██║
 ╚██████╔╝╚██████╔╝███████╗███████║   ██║
  ╚══▀▀═╝  ╚═════╝ ╚══════╝╚══════╝   ╚═╝
"""


def render_banner(skill_pack=None):
    """Full-width ASCII art banner."""
    ascii_art = (skill_pack.banner_ascii if skill_pack and skill_pack.banner_ascii else DEFAULT_BANNER)
    subtitle = skill_pack.subtitle if skill_pack else "◈  Quest Engine  ◈"

    banner_text = Text(ascii_art, style="bold cyan")
    console.print(Align.center(banner_text))
    console.print(Align.center(Text(subtitle, style="bold yellow")))
    console.print()


def render_stats_panel(engine) -> Panel:
    """Compact stats panel shown during gameplay."""
    stats = engine.get_stats_dict()
    total_zones = len(engine.skill_pack.zone_order)

    pct = min(stats["xp_this_level"] / stats["xp_for_next_level"], 1.0)
    bar_width = 16
    filled = int(bar_width * pct)
    bar = "█" * filled + "░" * (bar_width - filled)
    xp_bar = f"[cyan]{bar[:filled]}[/cyan][dim]{bar[filled:]}[/dim]"

    streak_color = "white"
    if stats["streak"] >= 10:
        streak_color = "bold red"
    elif stats["streak"] >= 5:
        streak_color = "bold yellow"
    elif stats["streak"] >= 3:
        streak_color = "yellow"

    streak_flames = ""
    if stats["streak"] >= 3:
        streak_flames = " 🔥" * min(stats["streak"] // 3, 3)

    table = Table.grid(padding=(0, 2))
    table.add_column(style="dim", justify="right")
    table.add_column()
    table.add_column(style="dim", justify="right")
    table.add_column()

    table.add_row(
        "Player:", f"[bold white]{stats['name']}[/bold white]",
        "Zone:", f"[cyan]{stats['current_zone'].replace('_', ' ').title()}[/cyan]",
    )
    table.add_row(
        "Level:", f"[bold yellow]{stats['level']}[/bold yellow] [dim]{stats['title']}[/dim]",
        "Zones:", f"[green]{stats['zones_completed']}/{total_zones}[/green]",
    )
    table.add_row(
        "XP:", f"{xp_bar} [dim]{stats['xp_this_level']}/{stats['xp_for_next_level']}[/dim]",
        "Challenges:", f"[white]{stats['challenges_completed']}[/white]",
    )
    table.add_row(
        "Streak:", f"[{streak_color}]{stats['streak']}x[/{streak_color}]{streak_flames} [dim](best: {stats['max_streak']})[/dim]",
        "Achievements:", f"[magenta]{stats['achievements_count']}[/magenta]",
    )

    return Panel(table, title="[bold cyan]⚔  PLAYER STATS[/bold cyan]", border_style="cyan", box=box.ROUNDED)


def render_zone_map(engine, zones: list) -> Panel:
    """Visual zone progression map."""
    zone_order = engine.skill_pack.zone_order
    lines = []
    for i, zone_id in enumerate(zone_order):
        zone = next((z for z in zones if z["id"] == zone_id), None)
        if zone is None:
            continue

        icon = zone.get("icon", "?")
        name = zone["name"]
        is_complete = engine.is_zone_complete(zone_id)
        is_unlocked = engine.is_zone_unlocked(zone_id)
        is_current = zone_id == engine.current_zone

        if is_complete:
            status = "[bold green]✓[/bold green]"
            style = "dim green"
        elif is_current:
            status = "[bold yellow]▶[/bold yellow]"
            style = "bold white"
        elif is_unlocked:
            status = "[cyan]○[/cyan]"
            style = "cyan"
        else:
            status = "[dim]🔒[/dim]"
            style = "dim"

        lines.append(f"{status} [{style}]{icon} {name}[/{style}]")
        if i < len(zone_order) - 1:
            lines.append("[dim]  │[/dim]")

    content = "\n".join(lines)
    return Panel(content, title="[bold cyan]🗺  ZONE MAP[/bold cyan]", border_style="dim cyan")


def render_challenge_panel(challenge: dict, zone: dict, challenge_num: int, total: int, show_lesson: bool = False) -> Panel:
    """Display a challenge."""
    ctype = challenge.get("type", "quiz")
    difficulty = challenge.get("difficulty", "easy")
    xp = challenge.get("xp", 50)
    is_boss = challenge.get("is_boss", False)

    type_labels = {
        "quiz": "KNOWLEDGE CHECK",
        "flag_quiz": "FLAG QUIZ",
        "fill_blank": "FILL IN THE BLANK",
        "live": "LIVE CHALLENGE",
        "ordered": "SEQUENCE CHALLENGE",
    }
    type_label = "⚔  BOSS CHALLENGE" if is_boss else type_labels.get(ctype, ctype.upper())

    diff_color = DIFFICULTY_COLORS.get(difficulty, "white")
    diff_stars = DIFFICULTY_STARS.get(difficulty, "?")

    content = []
    content.append(f"[dim]Zone: {zone['name']}  |  Challenge {challenge_num}/{total}[/dim]")
    content.append("")

    flavor = challenge.get("flavor", "")
    if flavor:
        flavor_style = "bold italic red" if is_boss else "italic cyan"
        content.append(f"[{flavor_style}]{flavor}[/{flavor_style}]")
        content.append("")

    lesson = challenge.get("lesson", "")
    if lesson and show_lesson:
        content.append("─" * 48)
        content.append("[bold green]📖 LESSON[/bold green]")
        content.append("")
        for line in lesson.strip().splitlines():
            stripped = line.strip()
            if stripped.startswith("Syntax:") or stripped.startswith("Common flags:") or stripped.startswith("Example"):
                content.append(f"[bold yellow]{stripped}[/bold yellow]")
            elif stripped.startswith("-") or stripped.startswith("$"):
                content.append(f"[dim cyan]  {stripped}[/dim cyan]")
            elif stripped == "":
                content.append("")
            else:
                content.append(f"[white]{stripped}[/white]")
        content.append("─" * 48)
        content.append("")

    if is_boss:
        content.append(
            f"[bold red]{type_label}[/bold red]  "
            f"[{diff_color}]{diff_stars}[/{diff_color}]  "
            f"[bold yellow]⬟ {xp} XP[/bold yellow]"
        )
        content.append("")
        content.append("[dim red]╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍[/dim red]")
    else:
        content.append(
            f"[bold white]{type_label}[/bold white]  "
            f"[{diff_color}]{diff_stars}[/{diff_color}]  "
            f"[yellow]⬟ {xp} XP[/yellow]"
        )
    content.append("")

    question = challenge.get("question", "")
    question_style = "bold white" if not is_boss else "bold yellow"
    content.append(f"[{question_style}]{question}[/{question_style}]")

    options = challenge.get("options", [])
    if options:
        content.append("")
        for j, opt in enumerate(options):
            letter = chr(ord("A") + j)
            content.append(f"  [bold cyan]{letter}.[/bold cyan]  {opt}")

    # Ordered challenge: display shuffled items with numbers
    items = challenge.get("items", [])
    if items and ctype == "ordered":
        content.append("")
        content.append("[dim]Put these in the correct order:[/dim]")
        content.append("")
        for j, item in enumerate(items):
            content.append(f"  [bold cyan]{j+1}.[/bold cyan]  {item}")

    if is_boss:
        title = f"[bold red]💀 {challenge['title']}[/bold red]"
        border_style = "bold red"
        panel_box = box.DOUBLE
        padding = (1, 3)
    else:
        title = f"[bold cyan]📋 {challenge['title']}[/bold cyan]"
        border_style = "cyan"
        panel_box = box.ROUNDED
        padding = (1, 2)

    return Panel(
        "\n".join(content),
        title=title,
        border_style=border_style,
        box=panel_box,
        padding=padding,
    )


def render_result(success: bool, message: str, xp_gained: int = 0, leveled_up: bool = False, streak: int = 0, actual_xp: int = 0):
    if success:
        console.print()
        xp_text = f"[bold yellow]+{actual_xp} XP[/bold yellow]"
        if streak >= 3:
            multiplier = 1.25
            if streak >= 10:
                multiplier = 2.0
            elif streak >= 5:
                multiplier = 1.5
            xp_text += f"  [dim](×{multiplier} streak bonus)[/dim]"

        lines = [f"[bold green]{message}[/bold green]", "", xp_text]
        if streak >= 3:
            flame = "🔥" * min(streak // 3, 5)
            lines.append(f"[bold yellow]{flame} Streak: {streak}x[/bold yellow]")

        console.print(
            Panel(
                "\n".join(lines),
                title="[bold green]✓  CORRECT[/bold green]",
                border_style="bold green",
                box=box.ROUNDED,
                padding=(1, 2),
            )
        )
    else:
        console.print()
        console.print(
            Panel(
                f"[bold red]{message}[/bold red]",
                title="[bold red]✗  INCORRECT[/bold red]",
                border_style="red",
                box=box.ROUNDED,
                padding=(1, 2),
            )
        )


def render_hint(hint_text: str, cost: int = 10):
    console.print()
    cost_note = f"  [dim](-{cost} XP)[/dim]" if cost > 0 else ""
    console.print(
        Panel(
            f"[yellow]{hint_text}[/yellow]",
            title=f"[bold yellow]💡 HINT[/bold yellow]{cost_note}",
            border_style="yellow",
            box=box.ROUNDED,
            padding=(1, 2),
        )
    )


def render_boss_intro(intro_text: str, challenge_title: str):
    console.clear()
    console.print()
    console.print(Align.center(Text("⚔  ☠  ⚔", style="bold red")))
    console.print()
    intro_renderable = Text.from_markup(intro_text, justify="center")
    console.print(
        Panel(
            Align.center(intro_renderable),
            title=f"[bold red]💀  {challenge_title.upper()}  💀[/bold red]",
            border_style="bold red",
            box=box.DOUBLE,
            padding=(2, 6),
        )
    )
    console.print()
    console.print(Align.center(Text("⚔  ☠  ⚔", style="bold red")))
    console.print()
    _press_enter()


def render_zone_intro(intro_text: str, zone: dict, skill_pack=None):
    """Show zone introduction."""
    console.clear()
    icon = zone.get("icon", "")
    # Final zone is the last in zone_order
    is_final = skill_pack and zone["id"] == skill_pack.zone_order[-1]
    border = "bold yellow" if is_final else "bold cyan"
    title_color = "yellow" if is_final else "cyan"
    console.print()
    console.print(
        Panel(
            f"[italic]{intro_text}[/italic]",
            title=f"[bold {title_color}]{icon}  {zone['name'].upper()}[/bold {title_color}]",
            subtitle=f"[dim]{zone.get('subtitle', '')}[/dim]",
            border_style=border,
            box=box.DOUBLE,
            padding=(1, 4),
        )
    )
    console.print()
    _press_enter()


def render_zone_complete(completion_text: str, zone: dict, xp_earned: int, stars: int = 1):
    console.print()
    icon = zone.get("icon", "")
    star_display = _zone_star_str(stars)
    star_line = f"\n{star_display}  " if stars else ""

    if stars == 3:
        title_str = f"[bold green]{icon}  PERFECT ZONE!  ★★★[/bold green]"
        border = "bold green"
    elif stars == 2:
        title_str = f"[bold green]{icon}  ZONE COMPLETE!  ★★[/bold green]"
        border = "bold green"
    else:
        title_str = f"[bold green]{icon}  ZONE COMPLETE![/bold green]"
        border = "green"

    body = f"[italic]{completion_text}[/italic]\n\n[bold yellow]⬟  Zone XP Earned: +{xp_earned}[/bold yellow]{star_line}"
    if stars < 3:
        body += "\n[dim]Play again from Zone Select to improve your star rating.[/dim]"

    console.print(
        Panel(
            body,
            title=title_str,
            border_style=border,
            box=box.DOUBLE,
            padding=(1, 4),
        )
    )
    console.print()
    _press_enter()


def render_achievement(achievement_id: str, achievements: dict):
    """Show achievement popup. achievements = skill_pack.achievements dict."""
    if achievement_id not in achievements:
        return
    name, desc = achievements[achievement_id]

    content = Text()
    content.append(f"🏆  {name}\n", style="bold yellow")
    content.append(desc, style="white")

    console.print()
    console.print(
        Panel(
            content,
            title="[bold yellow]★  ACHIEVEMENT UNLOCKED  ★[/bold yellow]",
            border_style="bold yellow",
            box=box.DOUBLE,
            padding=(1, 3),
        )
    )
    time.sleep(1.5)


def celebrate_level_up(level: int, title: str):
    console.print()
    frames = ["⚡", "★", "⚡", "★", "✦", "★", "⚡"]
    msg = f"  LEVEL UP!  Level {level} — {title}!  "

    with Live(console=console, refresh_per_second=10) as live:
        for frame in frames:
            live.update(
                Align.center(
                    Panel(
                        Text(f"{frame}  {msg}  {frame}", style="bold yellow", justify="center"),
                        border_style="bold yellow",
                        padding=(0, 4),
                    )
                )
            )
            time.sleep(0.15)
        live.update(
            Align.center(
                Panel(
                    Text(f"⚡  LEVEL {level}!  {title.upper()}  ⚡", style="bold yellow", justify="center"),
                    border_style="bold yellow",
                    padding=(1, 4),
                )
            )
        )
        time.sleep(1)

    console.print()


def animate_zone_progress(engine, zone_id: str):
    """Briefly animate the XP bar filling up — shown after zone completion."""
    total_xp = engine.total_xp
    xp_in_lvl = engine.xp_this_level
    xp_needed = engine.xp_for_next_level
    pct = min(xp_in_lvl / xp_needed, 1.0)
    bar_width = 30

    with Live(console=console, refresh_per_second=20) as live:
        for step in range(11):
            frac = step / 10
            current_pct = pct * frac
            filled = int(bar_width * current_pct)
            bar = "[cyan]" + "█" * filled + "[/cyan][dim]" + "░" * (bar_width - filled) + "[/dim]"
            live.update(
                Align.center(Text.from_markup(
                    f"  XP  {bar}  {int(current_pct * xp_needed)}/{xp_needed}  ",
                    justify="center"
                ))
            )
            time.sleep(0.04)
    console.print()


def render_achievements_screen(engine):
    from .engine import BASE_ACHIEVEMENTS
    # Merge base achievements with pack-specific ones (pack takes priority)
    all_achievements = {**BASE_ACHIEVEMENTS, **engine.skill_pack.achievements}

    console.clear()
    console.print(
        Panel(
            "[bold yellow]Your Hall of Fame[/bold yellow]",
            title="[bold yellow]★ ACHIEVEMENTS ★[/bold yellow]",
            border_style="yellow",
        )
    )
    console.print()

    unlocked_count = sum(1 for aid in all_achievements if aid in engine.achievements)

    # Split into unlocked and locked sections
    table = Table(show_header=True, header_style="bold yellow", box=box.SIMPLE_HEAVY)
    table.add_column("", width=3, justify="center")
    table.add_column("Achievement", style="bold")
    table.add_column("Description", style="dim")

    for ach_id, (name, desc) in all_achievements.items():
        if ach_id in engine.achievements:
            table.add_row("[yellow]★[/yellow]", f"[yellow]{name}[/yellow]", desc)

    if unlocked_count < len(all_achievements):
        table.add_section()
        for ach_id, (name, desc) in all_achievements.items():
            if ach_id not in engine.achievements:
                table.add_row("[dim]☆[/dim]", f"[dim]{name}[/dim]", f"[dim]{desc}[/dim]")

    console.print(table)
    console.print(f"\n[dim]Unlocked: {unlocked_count}/{len(all_achievements)}[/dim]")
    console.print()
    _press_enter()


def _zone_star_str(stars: int) -> str:
    if stars == 3:
        return "[bold yellow]★★★[/bold yellow]"
    if stars == 2:
        return "[yellow]★★[/yellow][dim]☆[/dim]"
    if stars == 1:
        return "[dim yellow]★[/dim yellow][dim]☆☆[/dim]"
    return ""


def render_zone_select(engine, zones: list) -> Optional[str]:
    """Show zone selection menu. Returns zone_id or None."""
    zone_order = engine.skill_pack.zone_order
    console.clear()
    console.print(
        Panel("[bold cyan]Choose your destination[/bold cyan]", title="[bold cyan]🗺  ZONE SELECT[/bold cyan]", border_style="cyan")
    )
    console.print()

    unlocked = engine.get_unlocked_zones()
    menu_zones = []

    for i, zone_id in enumerate(zone_order):
        zone = next((z for z in zones if z["id"] == zone_id), None)
        if zone is None:
            continue

        is_complete = engine.is_zone_complete(zone_id)
        is_unlocked = zone_id in unlocked
        icon = zone.get("icon", "?")
        stars = engine.get_zone_stars(zone_id)

        if is_complete:
            star_str = _zone_star_str(stars)
            status = f"[green]✓[/green] {star_str}"
        elif zone_id == engine.current_zone:
            status = "[yellow]▶ CURRENT[/yellow]"
        elif is_unlocked:
            status = "[cyan]UNLOCKED[/cyan]"
        else:
            status = "[dim]🔒[/dim]"

        label = f"[dim]{i+1}.[/dim] {icon} {zone['name']} [dim]- {zone.get('subtitle', '')}[/dim]  {status}"
        console.print(f"  {label}")
        if is_unlocked:
            menu_zones.append((str(i + 1), zone_id))

    console.print()
    console.print("  [dim]0. Back to main menu[/dim]")
    console.print()

    valid_choices = {num: zid for num, zid in menu_zones}
    valid_choices["0"] = None

    while True:
        choice = console.input("[cyan]Enter zone number: [/cyan]").strip()
        if choice in valid_choices:
            return valid_choices[choice]
        console.print("[red]Invalid choice. Please try again.[/red]")


def render_daily_challenge_banner(engine, skill_pack=None):
    """Show a highlighted banner for today's daily challenge if not yet done."""
    pack = skill_pack or engine.skill_pack
    challenge = engine.get_daily_challenge(pack)
    if challenge is None:
        return

    zone = challenge.get("_zone", {})
    zone_name = zone.get("name", "Unknown Zone")
    challenge_title = challenge.get("title", "Daily Challenge")

    # Countdown to midnight
    now = datetime.datetime.now()
    midnight = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time.min)
    hours_left = int((midnight - now).total_seconds() // 3600)

    streak_line = ""
    if engine.daily_challenge_streak > 0:
        streak_line = f"\n[dim yellow]Challenge streak: {engine.daily_challenge_streak} day(s)[/dim yellow]"

    content = (
        f"[bold white]{challenge_title}[/bold white]\n"
        f"[dim]Zone: {zone_name}[/dim]\n"
        f"[dim yellow]Resets in {hours_left}h  ·  2× XP Bonus[/dim yellow]"
        f"{streak_line}"
    )
    console.print(
        Panel(
            content,
            title="[bold yellow]★  TODAY'S DAILY CHALLENGE  ★[/bold yellow]",
            border_style="bold yellow",
            box=box.DOUBLE,
            padding=(1, 4),
        )
    )
    console.print()


ASCII_GRADES = {
    "S": [
        " ███████╗",
        " ██╔════╝",
        " ███████╗",
        " ╚════██║",
        " ███████║",
        " ╚══════╝",
    ],
    "A": [
        "  █████╗ ",
        " ██╔══██╗",
        " ███████║",
        " ██╔══██║",
        " ██║  ██║",
        " ╚═╝  ╚═╝",
    ],
    "B": [
        " ██████╗ ",
        " ██╔══██╗",
        " ██████╔╝",
        " ██╔══██╗",
        " ██████╔╝",
        " ╚═════╝ ",
    ],
    "C": [
        "  ██████╗",
        " ██╔════╝",
        " ██║     ",
        " ██║     ",
        " ╚██████╗",
        "  ╚═════╝",
    ],
    "D": [
        " ██████╗ ",
        " ██╔══██╗",
        " ██║  ██║",
        " ██║  ██║",
        " ██████╔╝",
        " ╚═════╝ ",
    ],
}

GRADE_COLORS = {
    "S": "bold yellow",
    "A": "bold cyan",
    "B": "bold green",
    "C": "bold white",
    "D": "bold red",
}


def render_completion_certificate(engine, skill_pack=None):
    """Render a beautiful ASCII certificate for pack completion."""
    pack = skill_pack or engine.skill_pack
    grade = engine.get_completion_grade()
    grade_lines = ASCII_GRADES.get(grade, ASCII_GRADES["D"])
    grade_color = GRADE_COLORS.get(grade, "bold white")

    today_str = datetime.date.today().isoformat()
    ach_count = len(engine.achievements)
    total_ach = len({**engine.skill_pack.achievements})

    lines = []
    lines.append("[bold yellow]══════════════════════════════════════════════[/bold yellow]")
    lines.append("")
    lines.append(f"[bold white]  This certifies that[/bold white]")
    lines.append("")
    lines.append(f"[bold cyan]    {engine.player_name}[/bold cyan]")
    lines.append("")
    lines.append(f"[white]  has completed[/white]")
    lines.append("")
    lines.append(f"[bold yellow]    {pack.title}[/bold yellow]")
    lines.append("")
    lines.append(f"[dim]  Completed: {today_str}[/dim]")
    lines.append(f"[dim]  Total XP: {engine.total_xp:,}  ·  Level: {engine.level} {engine.level_title}[/dim]")
    lines.append(f"[dim]  Achievements: {ach_count}/{total_ach}[/dim]")
    lines.append("")
    lines.append("[bold yellow]══════════════════════════════════════════════[/bold yellow]")
    lines.append("")
    lines.append(f"[bold]  GRADE[/bold]")
    for gl in grade_lines:
        lines.append(f"[{grade_color}]{gl}[/{grade_color}]")
    lines.append("")
    lines.append("[bold yellow]══════════════════════════════════════════════[/bold yellow]")
    lines.append("")
    lines.append(f"[italic cyan]  {pack.quit_message}[/italic cyan]")

    console.print()
    console.print(
        Panel(
            "\n".join(lines),
            title="[bold yellow]🏆  CERTIFICATE OF COMPLETION  🏆[/bold yellow]",
            border_style="bold yellow",
            box=box.DOUBLE,
            padding=(1, 4),
        )
    )
    console.print()
    _press_enter()


def render_main_menu(engine) -> str:
    console.clear()
    render_banner(engine.skill_pack)

    # Show daily challenge banner if not yet completed today
    if not engine.daily_challenge_completed:
        render_daily_challenge_banner(engine)

    stats = engine.get_stats_dict()
    if stats["challenges_completed"] > 0:
        daily_str = ""
        if stats.get("daily_streak", 0) > 1:
            daily_str = f"  🔥 {stats['daily_streak']}-day streak"
        console.print(
            Align.center(
                Text(
                    f"Welcome back, {stats['name']}!  Level {stats['level']} {stats['title']}  |  {stats['total_xp']:,} XP{daily_str}",
                    style="dim cyan",
                )
            )
        )
        # Today's Focus: suggest review if weak spots exist
        if stats.get("weak_zones", 0) > 0:
            console.print(
                Align.center(
                    Text(
                        f"⚑  {stats['weak_zones']} zone(s) have challenges worth reviewing  [6] Review Weak Spots",
                        style="dim yellow",
                    )
                )
            )
        console.print()

    pack_title = engine.skill_pack.title if engine.skill_pack else "Quest Engine"
    has_progress = stats["challenges_completed"] > 0
    has_weak = stats.get("weak_zones", 0) > 0
    has_completed = stats["zones_completed"] > 0

    options = [
        ("1", "New Game", "Start from the beginning"),
        ("2", "Continue", "Resume your quest"),
        ("3", "Zone Select", "Jump to an unlocked zone"),
        ("4", "Achievements", "View your accomplishments"),
        ("5", "Stats", "Detailed statistics & mastery"),
    ]
    if has_weak:
        options.append(("6", "Review Weak Spots", "Replay challenges you've struggled with"))
    if has_completed:
        options.append(("7", "Export Notes", "Save lessons to a text file"))
    daily_label = "Daily Challenge" if not engine.daily_challenge_completed else "Daily Challenge ✓"
    daily_desc = "Today's special challenge — 2× XP" if not engine.daily_challenge_completed else "Already completed today"
    options.append(("8", daily_label, daily_desc))
    options.append(("0", "Quit", f"Exit {pack_title}"))

    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
    table.add_column(style="bold yellow", width=4)
    table.add_column(style="bold white", width=20)
    table.add_column(style="dim")

    for key, label, desc in options:
        table.add_row(f"[{key}]", label, desc)

    console.print(Align.center(table))
    console.print()

    valid = {"1", "2", "3", "4", "5", "6", "7", "8", "0"}
    while True:
        choice = console.input("[cyan]Your choice: [/cyan]").strip()
        if choice in valid:
            return choice
        console.print("[red]Invalid choice.[/red]")


def render_session_summary(engine):
    """Show what happened this session — shown on quit."""
    sess = engine.get_session_stats()
    if sess["total"] == 0:
        return  # Nothing happened this session

    acc_color = "green" if sess["accuracy"] >= 80 else "yellow" if sess["accuracy"] >= 50 else "red"
    lines = [
        f"[dim]Time played:[/dim]  [white]{sess['time_str']}[/white]",
        f"[dim]XP earned:[/dim]    [bold yellow]+{sess['xp_earned']} XP[/bold yellow]",
        f"[dim]Answered:[/dim]     [white]{sess['correct']} correct[/white]  [dim]/[/dim]  [white]{sess['total']} total[/white]",
        f"[dim]Accuracy:[/dim]     [{acc_color}]{sess['accuracy']:.0f}%[/{acc_color}]",
    ]
    if sess["daily_streak"] > 1:
        lines.append(f"[dim]Daily streak:[/dim]  [bold yellow]🔥 {sess['daily_streak']} days[/bold yellow]")

    console.print(Panel(
        "\n".join(lines),
        title="[bold cyan]SESSION COMPLETE[/bold cyan]",
        border_style="dim cyan",
        box=box.ROUNDED,
        padding=(1, 4),
    ))


def render_stats_screen(engine):
    console.clear()
    stats = engine.get_stats_dict()
    achievements = engine.skill_pack.achievements
    total_zones = len(engine.skill_pack.zone_order)

    console.print(
        Panel("[bold white]Your Journey So Far[/bold white]", title="[bold cyan]📊 STATISTICS[/bold cyan]", border_style="cyan")
    )
    console.print()

    table = Table(show_header=False, box=box.SIMPLE, padding=(0, 2))
    table.add_column(style="dim", justify="right", width=22)
    table.add_column(style="bold white")

    table.add_row("Player Name:", f"[bold white]{stats['name']}[/bold white]")
    table.add_row("Level:", f"[bold yellow]{stats['level']} — {stats['title']}[/bold yellow]")
    table.add_row("Total XP:", f"[cyan]{stats['total_xp']:,}[/cyan]")
    table.add_row("XP This Level:", f"[cyan]{stats['xp_this_level']}/{stats['xp_for_next_level']}[/cyan]")
    table.add_row("Current Streak:", f"[yellow]{stats['streak']}x[/yellow]")
    table.add_row("Best Streak:", f"[yellow]{stats['max_streak']}x[/yellow]")
    table.add_row("Daily Streak:", f"[bold yellow]🔥 {stats.get('daily_streak', 0)} days[/bold yellow]")
    table.add_row("Zones Completed:", f"[green]{stats['zones_completed']}/{total_zones}[/green]")
    table.add_row("Challenges Done:", f"[white]{stats['challenges_completed']}[/white]")
    table.add_row("Achievements:", f"[magenta]{stats['achievements_count']}/{len(achievements)}[/magenta]")
    if stats.get("weak_zones", 0):
        table.add_row("Weak Zones:", f"[yellow]{stats['weak_zones']} zone(s) to review[/yellow]")

    console.print(Align.center(table))
    console.print()

    # Zone mastery table
    if stats["zones_completed"] > 0:
        console.print("[bold cyan]  Zone Mastery[/bold cyan]")
        console.print()
        mast_table = Table(show_header=True, header_style="dim", box=box.SIMPLE, padding=(0, 2))
        mast_table.add_column("Zone", style="white")
        mast_table.add_column("Stars", justify="center")
        for zone_id in engine.skill_pack.zone_order:
            if not engine.is_zone_complete(zone_id):
                continue
            zone = engine.skill_pack.get_zone(zone_id)
            stars = engine.get_zone_stars(zone_id)
            mast_table.add_row(zone["name"] if zone else zone_id, _zone_star_str(stars))
        console.print(Align.center(mast_table))
        console.print()

    _press_enter()


def render_name_prompt(skill_pack=None) -> str:
    console.print()
    default_name = "Ghost"
    prompt_text = "[bold cyan]What do they call you, Ghost?[/bold cyan]"
    if skill_pack:
        default_name = getattr(skill_pack, "default_player_name", "Ghost")
        custom_prompt = getattr(skill_pack, "name_prompt", None)
        if custom_prompt:
            prompt_text = custom_prompt
    console.print(prompt_text)
    name = console.input("[cyan]> [/cyan]").strip()
    return name if name else default_name


def confirm_new_game() -> bool:
    console.print()
    console.print("[bold red]WARNING: Starting a new game will erase all progress![/bold red]")
    answer = console.input("[cyan]Are you sure? (yes/no): [/cyan]").strip().lower()
    return answer in ("yes", "y")


def _press_enter():
    console.input("[dim]Press Enter to continue...[/dim]")


def prompt_command(challenge_type: str = "live") -> str:
    prompts = {
        "quiz": "[cyan]Your answer: [/cyan]",
        "flag_quiz": "[cyan]Your flag/answer: [/cyan]",
        "fill_blank": "[cyan]Fill in the blank: [/cyan]",
        "live": "[cyan]$ [/cyan]",
        "ordered": "[cyan]Enter the order (e.g. 2 4 1 3): [/cyan]",
    }
    prompt = prompts.get(challenge_type, "[cyan]Your answer: [/cyan]")
    return console.input(prompt)


def render_challenge_menu():
    console.print()
    console.print(
        "  [dim cyan][h][/dim cyan][dim] Hint [/dim][yellow](10 XP)[/yellow]"
        "  [dim cyan][l][/dim cyan][dim] Lesson"
        "  [dim cyan][s][/dim cyan][dim] Skip"
        "  [dim cyan][q][/dim cyan][dim] Menu[/dim]"
    )
    console.print()


def render_output(output: str):
    if output.strip():
        console.print(
            Panel(
                f"[dim]{output.strip()}[/dim]",
                title="[dim]Output[/dim]",
                border_style="dim",
                padding=(0, 1),
            )
        )


def render_separator():
    console.print(Rule(style="dim"))


def print_narrative(text: str):
    console.print(f"\n[italic cyan]{text}[/italic cyan]\n")


def print_info(text: str):
    console.print(f"[dim]{text}[/dim]")


def print_error(text: str):
    console.print(f"[bold red]{text}[/bold red]")


def print_success(text: str):
    console.print(f"[bold green]{text}[/bold green]")


def print_warning(text: str):
    console.print(f"[bold yellow]{text}[/bold yellow]")
