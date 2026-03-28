"""
storage.py — Pluggable storage backends for quest-engine.

Supports:
  - JsonFileStore (default): saves progress as JSON files (~/.quest_engine/)
  - SqliteStore: SQLite database for local multi-user support
  - MemoryStore: in-memory only (serverless, testing)

Usage:
    from engine.storage import get_store
    store = get_store()  # auto-detects best backend
    store.save("bash_quest", "player1", data_dict)
    data = store.load("bash_quest", "player1")
"""

import json
import os
import sqlite3
import threading
from abc import ABC, abstractmethod
from pathlib import Path


class BaseStore(ABC):
    """Abstract storage backend."""

    @abstractmethod
    def load(self, pack_name: str, player_id: str = "default") -> dict | None:
        """Load player progress. Returns dict or None if not found."""

    @abstractmethod
    def save(self, pack_name: str, player_id: str, data: dict) -> None:
        """Save player progress."""

    @abstractmethod
    def delete(self, pack_name: str, player_id: str = "default") -> None:
        """Delete player progress."""

    @abstractmethod
    def list_players(self, pack_name: str) -> list[str]:
        """List all player IDs for a pack."""


class JsonFileStore(BaseStore):
    """Original JSON file storage. One file per pack per player."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def _path(self, pack_name: str, player_id: str) -> Path:
        if player_id == "default":
            return self.base_dir / pack_name / "progress.json"
        return self.base_dir / pack_name / f"{player_id}.json"

    def load(self, pack_name: str, player_id: str = "default") -> dict | None:
        p = self._path(pack_name, player_id)
        if not p.exists():
            return None
        try:
            with open(p) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

    def save(self, pack_name: str, player_id: str, data: dict) -> None:
        p = self._path(pack_name, player_id)
        try:
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "w") as f:
                json.dump(data, f, indent=2)
        except OSError:
            pass  # read-only filesystem

    def delete(self, pack_name: str, player_id: str = "default") -> None:
        p = self._path(pack_name, player_id)
        try:
            p.unlink(missing_ok=True)
        except OSError:
            pass

    def list_players(self, pack_name: str) -> list[str]:
        d = self.base_dir / pack_name
        if not d.exists():
            return []
        players = []
        for f in d.glob("*.json"):
            name = f.stem
            players.append("default" if name == "progress" else name)
        return players


class SqliteStore(BaseStore):
    """SQLite storage. Single DB file, supports multiple players per pack."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._local = threading.local()
        self._init_db()

    def _conn(self) -> sqlite3.Connection:
        if not hasattr(self._local, "conn") or self._local.conn is None:
            self._local.conn = sqlite3.connect(str(self.db_path))
            self._local.conn.execute("PRAGMA journal_mode=WAL")
        return self._local.conn

    def _init_db(self):
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            conn = self._conn()
            conn.execute("""
                CREATE TABLE IF NOT EXISTS progress (
                    pack_name TEXT NOT NULL,
                    player_id TEXT NOT NULL DEFAULT 'default',
                    data TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (pack_name, player_id)
                )
            """)
            conn.commit()
        except (OSError, sqlite3.OperationalError):
            pass  # read-only filesystem

    def load(self, pack_name: str, player_id: str = "default") -> dict | None:
        try:
            row = self._conn().execute(
                "SELECT data FROM progress WHERE pack_name = ? AND player_id = ?",
                (pack_name, player_id),
            ).fetchone()
            return json.loads(row[0]) if row else None
        except (sqlite3.OperationalError, json.JSONDecodeError):
            return None

    def save(self, pack_name: str, player_id: str, data: dict) -> None:
        try:
            self._conn().execute(
                """INSERT INTO progress (pack_name, player_id, data, updated_at)
                   VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                   ON CONFLICT(pack_name, player_id)
                   DO UPDATE SET data = excluded.data, updated_at = CURRENT_TIMESTAMP""",
                (pack_name, player_id, json.dumps(data)),
            )
            self._conn().commit()
        except (OSError, sqlite3.OperationalError):
            pass

    def delete(self, pack_name: str, player_id: str = "default") -> None:
        try:
            self._conn().execute(
                "DELETE FROM progress WHERE pack_name = ? AND player_id = ?",
                (pack_name, player_id),
            )
            self._conn().commit()
        except (OSError, sqlite3.OperationalError):
            pass

    def list_players(self, pack_name: str) -> list[str]:
        try:
            rows = self._conn().execute(
                "SELECT player_id FROM progress WHERE pack_name = ?",
                (pack_name,),
            ).fetchall()
            return [r[0] for r in rows]
        except sqlite3.OperationalError:
            return []


class MemoryStore(BaseStore):
    """In-memory store for serverless/testing. Data lost on restart."""

    def __init__(self):
        self._data: dict[str, dict[str, dict]] = {}

    def load(self, pack_name: str, player_id: str = "default") -> dict | None:
        return self._data.get(pack_name, {}).get(player_id)

    def save(self, pack_name: str, player_id: str, data: dict) -> None:
        self._data.setdefault(pack_name, {})[player_id] = data

    def delete(self, pack_name: str, player_id: str = "default") -> None:
        if pack_name in self._data:
            self._data[pack_name].pop(player_id, None)

    def list_players(self, pack_name: str) -> list[str]:
        return list(self._data.get(pack_name, {}).keys())


# ── Store factory ────────────────────────────────────────────────────────────

_store_instance: BaseStore | None = None


def get_store() -> BaseStore:
    """Get or create the global store instance. Auto-detects best backend."""
    global _store_instance
    if _store_instance is not None:
        return _store_instance

    # Check env override
    backend = os.environ.get("QUEST_STORAGE", "").lower()
    save_dir = os.environ.get("QUEST_SAVE_DIR", "")

    if backend == "memory":
        _store_instance = MemoryStore()
    elif backend == "sqlite":
        db_path = Path(save_dir) / "quest_engine.db" if save_dir else _default_base() / "quest_engine.db"
        _store_instance = SqliteStore(db_path)
    elif backend == "json":
        base = Path(save_dir) if save_dir else _default_base()
        _store_instance = JsonFileStore(base)
    else:
        # Auto-detect: try SQLite first (better for multi-user), fall back to JSON
        base = Path(save_dir) if save_dir else _default_base()
        try:
            db_path = base / "quest_engine.db"
            _store_instance = SqliteStore(db_path)
        except Exception:
            _store_instance = JsonFileStore(base)

    return _store_instance


def _default_base() -> Path:
    """Default save directory — writable home dir or /tmp."""
    home = Path.home()
    if os.access(str(home), os.W_OK):
        return home / ".quest_engine"
    return Path("/tmp/.quest_engine")
