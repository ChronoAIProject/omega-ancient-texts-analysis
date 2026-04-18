#!/usr/bin/env python3
"""Validate generated video artifacts before publishing."""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_ARTIFACTS_DIR = ROOT / "workspace" / "artifacts"
REPORT_PATH = ROOT / "workspace" / "validation_report.json"
VIDEO_PATTERN = "*_video.mp4"
MIN_DURATION_SECONDS = 10.0
MIN_MEAN_VOLUME_DB = -60.0
ALLOWED_VIDEO_CODECS = {"h264", "h265", "hevc"}
ALLOWED_AUDIO_CODECS = {"aac", "mp3", "opus"}

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"


def supports_color() -> bool:
    return (
        sys.stdout.isatty()
        and os.environ.get("NO_COLOR") is None
        and os.environ.get("TERM") not in (None, "", "dumb")
    )


def colorize_status(status: str, enabled: bool) -> str:
    if not enabled:
        return status
    color = GREEN if status.strip() == "PASS" else RED
    return f"{color}{status}{RESET}"


def float_or_none(value: Any) -> float | None:
    try:
        if value in (None, "", "N/A"):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def round_or_none(value: float | None) -> float | None:
    if value is None or not math.isfinite(value):
        return None
    return round(value, 1)


def format_number(value: float | None) -> str:
    if value is None:
        return "-"
    return f"{value:.1f}"


def format_mean_volume(value: float | None) -> str:
    if value is None:
        return "-"
    if math.isinf(value) and value < 0:
        return "-inf"
    return f"{value:.1f}"


def relative_file_label(path: Path, artifacts_root: Path) -> str:
    try:
        return path.relative_to(artifacts_root).as_posix()
    except ValueError:
        return path.name


def discover_video_files(artifacts_root: Path) -> list[Path]:
    """Recursively find all *_video.mp4 files under artifacts_root."""
    return sorted(artifacts_root.rglob(VIDEO_PATTERN))


def discover_in_dir(target_dir: Path) -> list[Path]:
    return sorted(target_dir.glob(VIDEO_PATTERN))


def run_subprocess(command: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def probe_media(file_path: Path, ffprobe_bin: str) -> tuple[dict[str, Any] | None, str | None]:
    command = [
        ffprobe_bin,
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_streams",
        "-show_format",
        str(file_path),
    ]
    try:
        result = run_subprocess(command, timeout=120)
    except (OSError, subprocess.TimeoutExpired):
        return None, "ffprobe_failed"

    if result.returncode != 0:
        return None, "ffprobe_failed"

    try:
        return json.loads(result.stdout), None
    except json.JSONDecodeError:
        return None, "ffprobe_parse_failed"


def detect_mean_volume(file_path: Path, ffmpeg_bin: str) -> tuple[float | None, str | None]:
    command = [
        ffmpeg_bin,
        "-hide_banner",
        "-nostats",
        "-i",
        str(file_path),
        "-map",
        "0:a:0",
        "-vn",
        "-af",
        "volumedetect",
        "-f",
        "null",
        "-",
    ]
    try:
        result = run_subprocess(command, timeout=600)
    except (OSError, subprocess.TimeoutExpired):
        return None, "ffmpeg_volumedetect_failed"

    output = f"{result.stdout}\n{result.stderr}"
    match = re.search(r"mean_volume:\s*(-?(?:\d+(?:\.\d+)?|inf))\s*dB", output)
    if not match:
        if result.returncode != 0:
            return None, "ffmpeg_volumedetect_failed"
        return None, "mean_volume_unavailable"

    token = match.group(1).lower()
    if token == "-inf":
        return float("-inf"), None

    try:
        return float(token), None
    except ValueError:
        return None, "mean_volume_unavailable"


def normalize_duration(probe_data: dict[str, Any], video_stream: dict[str, Any] | None, audio_stream: dict[str, Any] | None) -> float | None:
    format_duration = float_or_none(probe_data.get("format", {}).get("duration"))
    if format_duration is not None:
        return format_duration
    if video_stream is not None:
        stream_duration = float_or_none(video_stream.get("duration"))
        if stream_duration is not None:
            return stream_duration
    if audio_stream is not None:
        stream_duration = float_or_none(audio_stream.get("duration"))
        if stream_duration is not None:
            return stream_duration
    return None


def build_result_template(file_label: str) -> dict[str, Any]:
    return {
        "file": file_label,
        "status": "fail",
        "duration_s": None,
        "has_video": False,
        "has_audio": False,
        "mean_volume_db": None,
        "video_codec": None,
        "audio_codec": None,
        "resolution": None,
        "file_size_mb": 0.0,
    }


def validate_video(file_path: Path, artifacts_root: Path, ffprobe_bin: str, ffmpeg_bin: str) -> dict[str, Any]:
    file_label = relative_file_label(file_path, artifacts_root)
    result = build_result_template(file_label)
    errors: list[str] = []

    if not file_path.exists():
        errors.append("missing_file")
        result["errors"] = errors
        return result

    file_size_bytes = file_path.stat().st_size
    result["file_size_mb"] = round(file_size_bytes / (1024 * 1024), 1)
    if file_size_bytes <= 0:
        errors.append("empty_file")
        result["errors"] = errors
        return result

    probe_data, probe_error = probe_media(file_path, ffprobe_bin)
    if probe_error is not None or probe_data is None:
        errors.append(probe_error or "ffprobe_failed")
        result["errors"] = errors
        return result

    streams = probe_data.get("streams", [])
    video_stream = next((stream for stream in streams if stream.get("codec_type") == "video"), None)
    audio_stream = next((stream for stream in streams if stream.get("codec_type") == "audio"), None)

    result["has_video"] = video_stream is not None
    result["has_audio"] = audio_stream is not None
    result["video_codec"] = video_stream.get("codec_name") if video_stream is not None else None
    result["audio_codec"] = audio_stream.get("codec_name") if audio_stream is not None else None

    if video_stream is not None:
        width = video_stream.get("width")
        height = video_stream.get("height")
        if width and height:
            result["resolution"] = f"{width}x{height}"

    duration = normalize_duration(probe_data, video_stream, audio_stream)
    result["duration_s"] = round_or_none(duration)

    if video_stream is None:
        errors.append("no_video_stream")
    elif result["video_codec"] not in ALLOWED_VIDEO_CODECS:
        errors.append(f"unsupported_video_codec:{result['video_codec']}")

    if audio_stream is None:
        errors.append("no_audio_stream")
    else:
        if result["audio_codec"] not in ALLOWED_AUDIO_CODECS:
            errors.append(f"unsupported_audio_codec:{result['audio_codec']}")

        mean_volume, volume_error = detect_mean_volume(file_path, ffmpeg_bin)
        result["mean_volume_db"] = round_or_none(mean_volume)
        if volume_error is not None:
            errors.append(volume_error)
        elif mean_volume is not None and mean_volume <= MIN_MEAN_VOLUME_DB:
            errors.append("audio_too_silent")

    if duration is None:
        errors.append("duration_unavailable")
    elif duration <= MIN_DURATION_SECONDS:
        errors.append("duration_too_short")

    if not errors:
        result["status"] = "pass"
    else:
        result["errors"] = errors

    return result


def missing_video_result(target_dir: Path, artifacts_root: Path) -> dict[str, Any]:
    expected = target_dir / f"{target_dir.name}_video.mp4"
    result = build_result_template(relative_file_label(expected, artifacts_root))
    result["errors"] = ["missing_video_file"]
    return result


def result_row(result: dict[str, Any]) -> dict[str, str]:
    reason = "-" if result["status"] == "pass" else ", ".join(result.get("errors", []))
    codecs = f"{result.get('video_codec') or '-'} / {result.get('audio_codec') or '-'}"
    return {
        "Status": result["status"].upper(),
        "File": result["file"],
        "Duration": format_number(result.get("duration_s")),
        "Video": "yes" if result.get("has_video") else "no",
        "Audio": "yes" if result.get("has_audio") else "no",
        "Mean dB": format_mean_volume(result.get("mean_volume_db")),
        "Codecs": codecs,
        "Resolution": result.get("resolution") or "-",
        "Size MB": format_number(result.get("file_size_mb")),
        "Reason": reason,
    }


def print_results_table(results: list[dict[str, Any]]) -> None:
    rows = [result_row(result) for result in results]
    headers = ["Status", "File", "Duration", "Video", "Audio", "Mean dB", "Codecs", "Resolution", "Size MB", "Reason"]
    widths = {
        header: max(len(header), *(len(row[header]) for row in rows))
        for header in headers
    }
    color_enabled = supports_color()

    header_line = " | ".join(f"{header:<{widths[header]}}" for header in headers)
    separator_line = "-+-".join("-" * widths[header] for header in headers)
    print(header_line)
    print(separator_line)

    for row in rows:
        cells = []
        for header in headers:
            raw_value = row[header]
            padded = f"{raw_value:<{widths[header]}}"
            if header == "Status":
                padded = colorize_status(padded, color_enabled)
            cells.append(padded)
        print(" | ".join(cells))


def write_report(results: list[dict[str, Any]]) -> None:
    passed = sum(1 for result in results if result["status"] == "pass")
    failed = len(results) - passed
    report = {
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
        "total": len(results),
        "passed": passed,
        "failed": failed,
        "results": results,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate generated video artifacts with ffprobe and ffmpeg.")
    parser.add_argument(
        "--dir",
        type=Path,
        help="Validate one artifact directory instead of scanning workspace/artifacts.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    ffprobe_bin = shutil.which("ffprobe")
    ffmpeg_bin = shutil.which("ffmpeg")
    missing_tools = [name for name, binary in (("ffprobe", ffprobe_bin), ("ffmpeg", ffmpeg_bin)) if binary is None]
    if missing_tools:
        missing_list = ", ".join(missing_tools)
        print(
            f"Error: missing required media tool(s) on PATH: {missing_list}. Install FFmpeg so both ffprobe and ffmpeg are available.",
            file=sys.stderr,
        )
        return 1

    if args.dir is not None:
        target_dir = args.dir.expanduser().resolve()
        if not target_dir.is_dir():
            print(f"Error: artifact directory not found: {target_dir}", file=sys.stderr)
            return 1
        artifacts_root = target_dir.parent if target_dir.parent.exists() else DEFAULT_ARTIFACTS_DIR
        video_files = discover_in_dir(target_dir)
        if not video_files:
            results = [missing_video_result(target_dir, artifacts_root)]
        else:
            results = [validate_video(path, artifacts_root, ffprobe_bin, ffmpeg_bin) for path in video_files]
    else:
        artifacts_root = DEFAULT_ARTIFACTS_DIR
        if not artifacts_root.is_dir():
            print(f"Error: artifacts directory not found: {artifacts_root}", file=sys.stderr)
            return 1
        video_files = discover_video_files(artifacts_root)
        if not video_files:
            print(f"Error: no files matching {VIDEO_PATTERN!r} found under {artifacts_root}", file=sys.stderr)
            return 1
        results = [validate_video(path, artifacts_root, ffprobe_bin, ffmpeg_bin) for path in video_files]

    print_results_table(results)
    write_report(results)

    passed = sum(1 for result in results if result["status"] == "pass")
    failed_files = [result["file"] for result in results if result["status"] == "fail"]
    print()
    print(f"{passed}/{len(results)} passed, {len(failed_files)} failed: {json.dumps(failed_files, ensure_ascii=False)}")
    print(f"Report written to {REPORT_PATH}")
    return 0 if not failed_files else 1


if __name__ == "__main__":
    raise SystemExit(main())
