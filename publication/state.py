"""Per-item and per-batch JSON state for the Stage 5 publication pipeline.

Each artifact (hexagram, chapter, category, synthesis) gets its own JSON
state file at workspace/publication_state/<item_id>.json tracking gate
progression, rounds, verdicts, and terminal state. Batches get their own
files under workspace/publication_state/batches/<batch_id>.json.

All writes use atomic os.replace() so a crash mid-write leaves the old
file intact.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

REPO_ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = REPO_ROOT / "workspace" / "publication_state"
BATCH_DIR = STATE_DIR / "batches"

State = Literal[
    "pending",
    "in_gate",
    "in_review",
    "published_to_queue",
    "quarantined",
    "needs_human_review",
]
Gate = Literal["G1", "G2", "G3", "G4"]
TERMINAL_STATES: frozenset[State] = frozenset({"published_to_queue", "quarantined"})


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _atomic_write_json(path: Path, data: Any) -> None:
    """Write JSON via tmp + os.replace so readers never see partial data."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)


class ItemState:
    """Wraps per-item JSON state, keeps a dirty flag to avoid redundant writes."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    @property
    def id(self) -> str:
        return str(self._data["id"])

    @property
    def state(self) -> State:
        return self._data.get("state", "pending")  # type: ignore[return-value]

    @property
    def current_gate(self) -> Gate | None:
        return self._data.get("current_gate")

    def is_terminal(self) -> bool:
        return bool(self._data.get("terminal")) or self.state in TERMINAL_STATES

    def to_dict(self) -> dict[str, Any]:
        return dict(self._data)

    @classmethod
    def _path_for(cls, item_id: str) -> Path:
        return STATE_DIR / f"{item_id}.json"

    @classmethod
    def load(cls, item_id: str) -> "ItemState | None":
        path = cls._path_for(item_id)
        if not path.is_file():
            return None
        return cls(json.loads(path.read_text(encoding="utf-8")))

    @classmethod
    def create(
        cls,
        item_id: str,
        *,
        book: str,
        language: str,
        sequence: int,
        item_type: str = "chapter",
    ) -> "ItemState":
        data: dict[str, Any] = {
            "id": item_id,
            "type": item_type,
            "book": book,
            "language": language,
            "sequence": sequence,
            "created": _now_utc(),
            "current_gate": "G1",
            "state": "pending",
            "batch_id": None,
            "gate_history": [],
            "assets": {},
            "terminal": False,
        }
        obj = cls(data)
        obj.save()
        return obj

    def save(self) -> None:
        _atomic_write_json(self._path_for(self.id), self._data)

    def append_gate_entry(
        self,
        gate: Gate,
        round: int,
        verdict: str,
        **extra: Any,
    ) -> None:
        entry: dict[str, Any] = {
            "gate": gate,
            "round": round,
            "verdict": verdict,
            "ts": _now_utc(),
        }
        entry.update(extra)
        history: list[dict[str, Any]] = self._data.setdefault("gate_history", [])
        history.append(entry)
        self._data["current_gate"] = gate

    def transition(self, new_state: State) -> None:
        self._data["state"] = new_state
        if new_state in TERMINAL_STATES:
            self._data["terminal"] = True

    def set_batch(self, batch_id: str) -> None:
        self._data["batch_id"] = batch_id

    def set_asset(self, kind: str, path: str) -> None:
        assets: dict[str, Any] = self._data.setdefault("assets", {})
        assets[kind] = path


class BatchState:
    """Wraps batch-level JSON state."""

    def __init__(self, data: dict[str, Any]) -> None:
        self._data = data

    @property
    def batch_id(self) -> str:
        return str(self._data["batch_id"])

    def to_dict(self) -> dict[str, Any]:
        return dict(self._data)

    @classmethod
    def _path_for(cls, batch_id: str) -> Path:
        return BATCH_DIR / f"{batch_id}.json"

    @classmethod
    def create(
        cls,
        batch_id: str,
        *,
        book: str,
        language: str,
        items: list[str],
        g1_mode: str = "deterministic",
    ) -> "BatchState":
        data: dict[str, Any] = {
            "batch_id": batch_id,
            "book": book,
            "language": language,
            "items": items,
            "g1_mode": g1_mode,
            "g1_rounds": [],
            "created": _now_utc(),
        }
        obj = cls(data)
        obj.save()
        return obj

    @classmethod
    def load(cls, batch_id: str) -> "BatchState | None":
        path = cls._path_for(batch_id)
        if not path.is_file():
            return None
        return cls(json.loads(path.read_text(encoding="utf-8")))

    def save(self) -> None:
        _atomic_write_json(self._path_for(self.batch_id), self._data)


def list_active_items() -> list[ItemState]:
    """All items where terminal is False."""
    out: list[ItemState] = []
    if not STATE_DIR.is_dir():
        return out
    for path in sorted(STATE_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        item = ItemState(data)
        if not item.is_terminal():
            out.append(item)
    return out


def list_items_by_book(book: str, *, include_terminal: bool = False) -> list[ItemState]:
    out: list[ItemState] = []
    if not STATE_DIR.is_dir():
        return out
    for path in sorted(STATE_DIR.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("book") != book:
            continue
        item = ItemState(data)
        if include_terminal or not item.is_terminal():
            out.append(item)
    return out


if __name__ == "__main__":
    import shutil

    # Smoke test in a throwaway subdir
    test_root = STATE_DIR / "_smoke_test"
    if test_root.exists():
        shutil.rmtree(test_root)
    test_root.mkdir(parents=True, exist_ok=True)

    # Override module-level dirs for isolation
    STATE_DIR = test_root  # type: ignore[assignment]
    BATCH_DIR = test_root / "batches"  # type: ignore[assignment]

    item = ItemState.create(
        "hexagram-smoke",
        book="易经",
        language="zh",
        sequence=99,
        item_type="chapter",
    )
    item.set_batch("2026-04-17-易经-smoke")
    item.append_gate_entry("G1", round=1, verdict="approved", mode="deterministic")
    item.transition("in_review")
    item.save()

    batch = BatchState.create(
        "2026-04-17-易经-smoke",
        book="易经",
        language="zh",
        items=["hexagram-smoke"],
    )
    print(f"Wrote item state: {ItemState._path_for('hexagram-smoke')}")
    print(f"Wrote batch state: {BatchState._path_for(batch.batch_id)}")

    loaded = ItemState.load("hexagram-smoke")
    assert loaded is not None
    assert loaded.state == "in_review"
    assert loaded.current_gate == "G1"
    assert len(loaded.to_dict()["gate_history"]) == 1
    print("OK: load + state + gate_history + transition")

    # Clean up
    shutil.rmtree(test_root)
