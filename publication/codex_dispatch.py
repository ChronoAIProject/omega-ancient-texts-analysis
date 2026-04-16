"""Codex CLI dispatcher for the Stage 5 pipeline.

Delivers prompts via stdin (avoids ARG_MAX and shell metachar issues with
Chinese content), enforces a <json>...</json> response envelope, and logs
every call to workspace/dispatch_log.jsonl under an exclusive file lock.

Mock mode: set MOCK_CODEX=1 or pass mock=True to avoid calling the CLI
(useful for tests and for running the pipeline skeleton offline).
"""

from __future__ import annotations

import fcntl
import json
import os
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE = REPO_ROOT / "workspace"
DISPATCH_LOG = WORKSPACE / "dispatch_log.jsonl"
DISPATCH_LOCK = WORKSPACE / ".dispatch_log.lock"

DEFAULT_TIMEOUT_S = 300
JSON_ENVELOPE = re.compile(r"<json>(.*?)</json>", re.DOTALL)


class CodexDispatchError(Exception):
    """Raised when the Codex CLI invocation fails (non-zero exit, timeout)."""


class CodexSchemaError(Exception):
    """Raised when the Codex response lacks the expected <json> envelope."""


def _now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _locked_append_log(entry: dict[str, Any]) -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    if not DISPATCH_LOCK.exists():
        DISPATCH_LOCK.touch()
    line = json.dumps(entry, ensure_ascii=False) + "\n"
    with open(DISPATCH_LOCK, "a") as lock:
        fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
        try:
            with open(DISPATCH_LOG, "a", encoding="utf-8") as f:
                f.write(line)
                f.flush()
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def _run_codex(
    prompt: str,
    *,
    reasoning: str,
    timeout_s: int,
) -> subprocess.CompletedProcess[str]:
    if shutil.which("codex") is None:
        raise CodexDispatchError(
            "codex binary not found on PATH. Install the Codex CLI or "
            "set MOCK_CODEX=1 to run the pipeline in mock mode."
        )
    return subprocess.run(
        [
            "codex", "exec",
            "--sandbox", "read-only",
            "-C", str(REPO_ROOT),
            "-c", f'model_reasoning_effort="{reasoning}"',
        ],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=timeout_s,
        check=False,
    )


def _extract_json(stdout: str) -> dict[str, Any]:
    match = JSON_ENVELOPE.search(stdout)
    if not match:
        raise CodexSchemaError(
            f"no <json>...</json> envelope found. First 500 chars of output:\n{stdout[:500]}"
        )
    return json.loads(match.group(1))


def dispatch(
    prompt: str,
    *,
    reasoning: str = "medium",
    timeout_s: int = DEFAULT_TIMEOUT_S,
    gate: str = "unknown",
    item_id: str = "unknown",
    mock: bool | None = None,
) -> dict[str, Any]:
    """Send a prompt to Codex, parse a JSON response out of the <json> envelope.

    Auto-retries once on schema parse failure with an appended instruction
    reminding the model to produce the envelope.
    """
    use_mock = mock if mock is not None else os.environ.get("MOCK_CODEX") == "1"
    started = time.monotonic()

    if use_mock:
        latency_ms = int((time.monotonic() - started) * 1000)
        result = {"mock": True, "gate": gate, "item_id": item_id}
        _locked_append_log({
            "ts": _now_utc(),
            "dispatcher": "codex",
            "gate": gate,
            "item_id": item_id,
            "reasoning": reasoning,
            "tokens_in": None,
            "tokens_out": None,
            "latency_ms": latency_ms,
            "cost_usd": None,
            "mock": True,
            "success": True,
        })
        return result

    try:
        proc = _run_codex(prompt, reasoning=reasoning, timeout_s=timeout_s)
    except subprocess.TimeoutExpired as exc:
        _locked_append_log({
            "ts": _now_utc(),
            "dispatcher": "codex",
            "gate": gate,
            "item_id": item_id,
            "reasoning": reasoning,
            "latency_ms": timeout_s * 1000,
            "mock": False,
            "success": False,
            "error": "timeout",
        })
        raise CodexDispatchError(f"codex timed out after {timeout_s}s") from exc

    if proc.returncode != 0:
        _locked_append_log({
            "ts": _now_utc(),
            "dispatcher": "codex",
            "gate": gate,
            "item_id": item_id,
            "reasoning": reasoning,
            "latency_ms": int((time.monotonic() - started) * 1000),
            "mock": False,
            "success": False,
            "error": f"exit_{proc.returncode}",
            "stderr_tail": proc.stderr[-500:] if proc.stderr else "",
        })
        raise CodexDispatchError(
            f"codex exited {proc.returncode}: {proc.stderr[-500:]}"
        )

    # Parse, with a single retry on schema failure
    try:
        parsed = _extract_json(proc.stdout)
    except CodexSchemaError:
        retry_prompt = (
            prompt
            + "\n\nYour previous response did not contain a <json>...</json> "
            + "envelope. Please retry, wrapping the JSON result in <json> and </json> tags."
        )
        proc = _run_codex(retry_prompt, reasoning=reasoning, timeout_s=timeout_s)
        if proc.returncode != 0:
            raise CodexDispatchError(
                f"codex exited {proc.returncode} on retry: {proc.stderr[-500:]}"
            )
        parsed = _extract_json(proc.stdout)

    latency_ms = int((time.monotonic() - started) * 1000)
    _locked_append_log({
        "ts": _now_utc(),
        "dispatcher": "codex",
        "gate": gate,
        "item_id": item_id,
        "reasoning": reasoning,
        "tokens_in": None,   # codex CLI does not report these
        "tokens_out": None,
        "latency_ms": latency_ms,
        "cost_usd": None,
        "mock": False,
        "success": True,
    })
    return parsed


if __name__ == "__main__":
    # Mock-mode smoke test
    os.environ["MOCK_CODEX"] = "1"
    result = dispatch(
        "Say hi inside <json>{\"hi\": true}</json>",
        gate="G3",
        item_id="smoke-test",
    )
    print(f"mock result: {result}")
    assert result == {"mock": True, "gate": "G3", "item_id": "smoke-test"}
    print("OK: mock dispatch returned expected payload")
