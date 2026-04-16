"""Append-only event log with cursor for the Stage 5 pipeline.

Events are appended by both sync_artifacts.sh (bash) and publication_pipeline
(Python) so writes must go through fcntl.flock to avoid interleaving on
files larger than PIPE_BUF (512 bytes).

Consumer protocol (at-least-once):
  1. Read cursor offset from events.cursor.
  2. Read events from that offset to end of file.
  3. Process events.
  4. Only after successful processing, advance cursor to current EOF.

Bash equivalent for sync_artifacts.sh (install flock via `brew install flock`
on macOS, or fall back to a sentinel-file approach):

    flock workspace/.events.lock -c \
        "echo '{\"ts\":\"...\",\"type\":\"artifact_ready\",\"item_id\":\"hexagram-09\"}' \
         >> workspace/events.jsonl"
"""

from __future__ import annotations

import fcntl
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = REPO_ROOT / "workspace"
EVENTS_PATH = WORKSPACE / "events.jsonl"
CURSOR_PATH = WORKSPACE / "events.cursor"
LOCK_PATH = WORKSPACE / ".events.lock"

VALID_EVENT_TYPES = frozenset({
    "artifact_ready",
    "media_fail",
    "notebooklm_outage",
    "quarantined",
    "gate_passed",
    "batch_created",
})


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _ensure_workspace() -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    if not LOCK_PATH.exists():
        LOCK_PATH.touch()


def append_event(event_type: str, item_id: str, **extra: Any) -> dict[str, Any]:
    """Atomically append a single event under exclusive file lock.

    Returns the full event dict that was written.
    """
    if event_type not in VALID_EVENT_TYPES:
        raise ValueError(
            f"unknown event_type {event_type!r}; must be one of {sorted(VALID_EVENT_TYPES)}"
        )
    _ensure_workspace()
    event: dict[str, Any] = {
        "ts": _now_utc(),
        "type": event_type,
        "item_id": item_id,
    }
    event.update(extra)
    line = json.dumps(event, ensure_ascii=False) + "\n"

    with open(LOCK_PATH, "a") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            # Open in append mode so writes are atomic at the kernel level
            # for lines < PIPE_BUF; flock handles the larger-line case.
            with open(EVENTS_PATH, "a", encoding="utf-8") as f:
                f.write(line)
                f.flush()
                os.fsync(f.fileno())
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)
    return event


def get_cursor() -> int:
    """Current cursor byte offset into events.jsonl. 0 if missing."""
    if not CURSOR_PATH.is_file():
        return 0
    try:
        text = CURSOR_PATH.read_text(encoding="utf-8").strip()
        return int(text) if text else 0
    except (OSError, ValueError):
        return 0


def get_file_size() -> int:
    """Size of events.jsonl in bytes, 0 if missing."""
    if not EVENTS_PATH.is_file():
        return 0
    return EVENTS_PATH.stat().st_size


def advance_cursor(new_offset: int) -> None:
    """Atomically update cursor file via tmp + os.replace."""
    _ensure_workspace()
    tmp = CURSOR_PATH.with_suffix(".cursor.tmp")
    tmp.write_text(str(int(new_offset)), encoding="utf-8")
    os.replace(tmp, CURSOR_PATH)


def read_new_events() -> Iterator[dict[str, Any]]:
    """Yield events after cursor offset. Does not advance the cursor.

    Caller is responsible for calling advance_cursor(get_file_size()) after
    processing succeeds (at-least-once semantics).
    """
    if not EVENTS_PATH.is_file():
        return
    offset = get_cursor()
    with open(EVENTS_PATH, "r", encoding="utf-8") as f:
        f.seek(offset)
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                # Skip a malformed line rather than crash the pipeline.
                # Log visibly so the issue is caught in review.
                print(f"WARN: malformed event line skipped: {exc}: {line[:200]}")
                continue


if __name__ == "__main__":
    # Self-test: append 3 events, consume them, advance cursor
    _ensure_workspace()
    # Reset for demo
    if EVENTS_PATH.exists():
        EVENTS_PATH.unlink()
    if CURSOR_PATH.exists():
        CURSOR_PATH.unlink()

    append_event("artifact_ready", "hexagram-09-xiaoxu", artifact_kind="video")
    append_event("artifact_ready", "hexagram-10-lu", artifact_kind="video")
    append_event("media_fail", "hexagram-11-tai", reason="notebooklm_timeout")

    print(f"Events file size: {get_file_size()} bytes")
    print(f"Cursor starts at: {get_cursor()}")
    print("Consuming events:")
    for ev in read_new_events():
        print(f"  {ev['type']} -> {ev['item_id']}")

    advance_cursor(get_file_size())
    print(f"Cursor advanced to: {get_cursor()}")

    # Second read should yield nothing
    remaining = list(read_new_events())
    assert remaining == [], "cursor should have advanced past all events"
    print("OK: cursor idempotency confirmed")
