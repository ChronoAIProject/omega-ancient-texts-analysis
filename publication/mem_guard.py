"""macOS memory-pressure guard for the Stage 5 publication pipeline.

Ported from automath PR #37 (codex_formalize.py). Gates worker dispatch
on memory-pressure indicators so the pipeline backs off before the system
panics — parallel NotebookLM calls + ffmpeg encoding + cover rendering
can saturate unified memory on M-series Macs.

Usage:
    from publication.mem_guard import memory_pressure_wait, configure

    configure(level_threshold=2, swap_ceiling_gb=16.0)

    # Before dispatching expensive work:
    memory_pressure_wait("G2 notebooklm batch")
"""

from __future__ import annotations

import logging
import re
import subprocess
import sys
import threading
import time

logger = logging.getLogger(__name__)

# kern.memorystatus_vm_pressure_level mapping (XNU):
#   1 = NORMAL, 2 = WARN, 4 = URGENT, 8 = CRITICAL
_MEM_LEVEL_NAMES = {1: "NORMAL", 2: "WARN", 4: "URGENT", 8: "CRITICAL"}

_cfg = {
    "enabled": sys.platform == "darwin",
    "level_threshold": 2,       # block when level >= WARN
    "swap_ceiling_gb": 16.0,    # block when swap exceeds 16GB
    "poll_seconds": 30,
    "max_wait_seconds": 1800,   # 30 min max wait, then proceed anyway
}
_lock = threading.Lock()

_SWAP_RE = re.compile(r"used\s*=\s*([\d.]+)([MG])", re.IGNORECASE)


def configure(**kwargs: float | int | bool) -> None:
    """Override guard settings. Call before pipeline starts."""
    for k, v in kwargs.items():
        if k in _cfg:
            _cfg[k] = v


def _macos_pressure_level() -> int:
    if sys.platform != "darwin":
        return 0
    try:
        r = subprocess.run(
            ["sysctl", "-n", "kern.memorystatus_vm_pressure_level"],
            capture_output=True, text=True, timeout=5,
            stdin=subprocess.DEVNULL,
        )
        return int((r.stdout or "0").strip() or "0")
    except Exception:
        return 0


def _macos_swap_used_gb() -> float:
    if sys.platform != "darwin":
        return 0.0
    try:
        r = subprocess.run(
            ["sysctl", "-n", "vm.swapusage"],
            capture_output=True, text=True, timeout=5,
            stdin=subprocess.DEVNULL,
        )
        m = _SWAP_RE.search(r.stdout or "")
        if not m:
            return 0.0
        val = float(m.group(1))
        return val / 1024.0 if m.group(2).upper() == "M" else val
    except Exception:
        return 0.0


def memory_pressure_snapshot() -> tuple[int, float]:
    """Return (pressure_level, swap_used_gb). level=0 if unsupported."""
    return _macos_pressure_level(), _macos_swap_used_gb()


def memory_pressure_wait(context: str = "") -> bool:
    """Block until macOS memory pressure is below threshold.

    Returns True if pressure is OK (or guard disabled/unsupported).
    Returns False if max_wait timed out — caller should proceed with
    a warning rather than deadlock the pipeline.
    """
    if not _cfg["enabled"]:
        return True

    lvl_thresh = int(_cfg["level_threshold"])
    swap_cap = float(_cfg["swap_ceiling_gb"])
    poll = int(_cfg["poll_seconds"])
    max_wait = int(_cfg["max_wait_seconds"])

    # Fast path: no pressure
    lvl, swap = memory_pressure_snapshot()
    if (lvl == 0 or lvl < lvl_thresh) and swap < swap_cap:
        return True

    # Serialize waits so parallel callers don't spam logs
    with _lock:
        start = time.time()
        warned = False
        while True:
            lvl, swap = memory_pressure_snapshot()
            under_level = lvl == 0 or lvl < lvl_thresh
            under_swap = swap < swap_cap
            if under_level and under_swap:
                if warned:
                    lvl_name = _MEM_LEVEL_NAMES.get(lvl, str(lvl))
                    logger.info(
                        f"[mem-guard] pressure cleared (level={lvl_name}, "
                        f"swap={swap:.1f}GB)"
                        + (f" — resuming {context}" if context else "")
                    )
                return True

            elapsed = int(time.time() - start)
            if elapsed >= max_wait:
                lvl_name = _MEM_LEVEL_NAMES.get(lvl, str(lvl))
                logger.warning(
                    f"[mem-guard] timeout after {elapsed}s "
                    f"(level={lvl_name}, swap={swap:.1f}GB) — proceeding anyway"
                    + (f" with {context}" if context else "")
                )
                return False

            lvl_name = _MEM_LEVEL_NAMES.get(lvl, str(lvl))
            logger.warning(
                f"[mem-guard] pressure elevated (level={lvl_name}, "
                f"swap={swap:.1f}GB) — pausing "
                f"{context or 'dispatch'}, retry in {poll}s "
                f"(waited {elapsed}s)"
            )
            warned = True
            time.sleep(poll)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    lvl, swap = memory_pressure_snapshot()
    lvl_name = _MEM_LEVEL_NAMES.get(lvl, str(lvl))
    print(f"Memory pressure: level={lvl_name} ({lvl}), swap={swap:.1f}GB")
    print(f"Threshold: level>={_cfg['level_threshold']}, swap>={_cfg['swap_ceiling_gb']}GB")
    ok = memory_pressure_wait("smoke test")
    print(f"Result: {'OK — clear to proceed' if ok else 'TIMEOUT — proceeding anyway'}")
