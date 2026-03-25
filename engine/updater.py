"""
engine/updater.py — Auto-update checker for Quest Engine games.

Checks PyPI for a newer version of the game package. If one is found,
shows a styled prompt and offers to install it. On accept, installs the
update via pip and re-execs the process so the new version starts immediately.

Results are cached for 24 hours so the network is only hit once per day.

Usage (in your game's main.py, before calling run() / run_campaign()):

    from engine.updater import check_and_prompt

    def main_nexus():
        check_and_prompt("nexus-quest")
        run_campaign("nexus")
"""

import json
import os
import subprocess
import sys
import time
import urllib.request
from importlib.metadata import version as pkg_version, PackageNotFoundError
from pathlib import Path

_CACHE_DIR = Path.home() / ".quest_engine"
_CACHE_FILE = _CACHE_DIR / "update_cache.json"
_CHECK_INTERVAL = 86_400  # 24 hours


# ── Version helpers ────────────────────────────────────────────────────────────

def _installed_version(package: str) -> str | None:
    try:
        return pkg_version(package)
    except PackageNotFoundError:
        return None


def _parse_version(v: str) -> tuple[int, ...]:
    try:
        return tuple(int(x) for x in v.split(".")[:3])
    except (ValueError, AttributeError):
        return (0,)


def _pypi_latest(package: str) -> str | None:
    try:
        url = f"https://pypi.org/pypi/{package}/json"
        req = urllib.request.Request(url, headers={"User-Agent": "quest-engine-updater"})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read())
            return data["info"]["version"]
    except Exception:
        return None


# ── Cache ──────────────────────────────────────────────────────────────────────

def _load_cache() -> dict:
    try:
        if _CACHE_FILE.exists():
            return json.loads(_CACHE_FILE.read_text())
    except Exception:
        pass
    return {}


def _save_cache(cache: dict) -> None:
    try:
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _CACHE_FILE.write_text(json.dumps(cache, indent=2))
    except Exception:
        pass


# ── Public API ─────────────────────────────────────────────────────────────────

def latest_version(package: str) -> str | None:
    """
    Return the latest PyPI version of `package`, or None.
    Result is cached for 24 hours. Network errors are silently ignored.
    """
    now = time.time()
    cache = _load_cache()
    entry = cache.get(package, {})

    if now - entry.get("checked_at", 0) < _CHECK_INTERVAL:
        return entry.get("latest_version")

    fetched = _pypi_latest(package)
    cache[package] = {"checked_at": now, "latest_version": fetched}
    _save_cache(cache)
    return fetched


def update_available(package: str) -> tuple[bool, str, str]:
    """
    Returns (is_available, current_version, latest_version).
    `is_available` is True when a newer version exists on PyPI.
    """
    current = _installed_version(package)
    if not current:
        return False, "unknown", "unknown"

    latest = latest_version(package)
    if not latest:
        return False, current, current

    if _parse_version(latest) > _parse_version(current):
        return True, current, latest

    return False, current, latest


def check_and_prompt(package: str) -> None:
    """
    Check for an update and, if one is available, show a styled prompt.
    If the user accepts, installs the update and re-execs the current process.
    Call this at the top of your game's entry-point functions.

    Fails silently on any error — the game always starts regardless.
    """
    try:
        _check_and_prompt_inner(package)
    except Exception:
        pass  # never block startup


def _check_and_prompt_inner(package: str) -> None:
    available, current, latest = update_available(package)
    if not available:
        return

    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text

    console = Console()
    console.print()

    text = Text()
    text.append("  Update available!\n\n", style="bold yellow")
    text.append("  Installed : ", style="dim white")
    text.append(f"v{current}\n", style="white")
    text.append("  Latest    : ", style="dim white")
    text.append(f"v{latest}", style="bold green")

    console.print(
        Panel(text, title="[bold cyan]SOFTWARE UPDATE[/bold cyan]", border_style="cyan"),
        justify="left",
    )

    try:
        answer = input("  Install update now? [y/N] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        console.print()
        return

    if answer != "y":
        console.print()
        return

    console.print(f"\n[cyan]Downloading {package} v{latest}...[/cyan]")

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "--quiet", package],
            check=True,
        )
    except subprocess.CalledProcessError:
        console.print(
            f"\n[bold red]Update failed.[/bold red] "
            f"Try manually: [cyan]pip install --upgrade {package}[/cyan]\n"
        )
        return

    console.print(f"\n[bold green]Updated to v{latest}! Restarting...[/bold green]\n")

    # Re-exec so the new version's code is loaded
    os.execv(sys.executable, [sys.executable] + sys.argv)
