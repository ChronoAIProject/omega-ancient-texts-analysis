#!/usr/bin/env python3
"""Generate manifest.json files for the 64 hexagram artifact directories."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS_DIR = ROOT / "workspace" / "artifacts"
ARTICLES_DIR = ROOT / "workspace" / "易经" / "hexagrams" / "all"
REGISTRY_PATH = ROOT / "workspace" / "易经" / "hexagrams" / "registry.json"
HEXAGRAM_DIR_RE = re.compile(r"^hexagram-(\d{2})-([a-z0-9-]+)$")

TRIGRAM_LABELS_ZH = {
    "qian": "天",
    "kun": "地",
    "zhen": "雷",
    "xun": "风",
    "kan": "水",
    "li": "火",
    "gen": "山",
    "dui": "泽",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build manifest.json for hexagram artifact directories."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing manifest.json files.",
    )
    return parser.parse_args()


def load_registry(path: Path) -> tuple[dict[int, dict[str, Any]], str | None]:
    if not path.exists():
        return {}, f"Registry not found: {path}"

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {}, f"Failed to read registry {path}: {exc}"

    if isinstance(data, dict):
        records = data.get("records")
    elif isinstance(data, list):
        records = data
    else:
        return {}, f"Unsupported registry structure in {path}"

    if not isinstance(records, list):
        return {}, f"Registry records are missing or not a list in {path}"

    registry_by_number: dict[int, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict):
            continue
        try:
            number = int(record["number"])
        except (KeyError, TypeError, ValueError):
            continue
        registry_by_number[number] = record

    if not registry_by_number:
        return {}, f"No usable registry records found in {path}"

    return registry_by_number, None


def chinese_number(value: int) -> str:
    if not 1 <= value <= 99:
        raise ValueError(f"Chinese numeral conversion only supports 1-99, got {value}")

    digits = {
        0: "零",
        1: "一",
        2: "二",
        3: "三",
        4: "四",
        5: "五",
        6: "六",
        7: "七",
        8: "八",
        9: "九",
    }

    if value < 10:
        return digits[value]
    if value == 10:
        return "十"
    if value < 20:
        return f"十{digits[value % 10]}"

    tens, ones = divmod(value, 10)
    if ones == 0:
        return f"{digits[tens]}十"
    return f"{digits[tens]}十{digits[ones]}"


def ordinal_zh(value: int) -> str:
    return f"第{chinese_number(value)}卦"


def title_case_pinyin(value: str) -> str:
    parts = [part for part in value.split("-") if part]
    return "".join(part[:1].upper() + part[1:] for part in parts)


def trigram_display_zh(trigram: dict[str, Any] | None) -> str:
    if not isinstance(trigram, dict):
        return ""
    pinyin = str(trigram.get("pinyin", "")).strip().lower()
    if pinyin in TRIGRAM_LABELS_ZH:
        return TRIGRAM_LABELS_ZH[pinyin]
    return str(trigram.get("name_zh", "")).strip()


def trigram_display_en(trigram: dict[str, Any] | None) -> str:
    if not isinstance(trigram, dict):
        return ""
    name_en = str(trigram.get("name_en", "")).strip()
    if name_en:
        return name_en
    pinyin = str(trigram.get("pinyin", "")).strip()
    return title_case_pinyin(pinyin)


def trigram_summary_zh(record: dict[str, Any] | None) -> str:
    if not isinstance(record, dict):
        return ""
    upper = trigram_display_zh(record.get("upper_trigram"))
    lower = trigram_display_zh(record.get("lower_trigram"))
    if upper and lower and upper == lower:
        return upper
    if upper and lower:
        return f"{upper}{lower}"
    return upper or lower


def trigram_summary_en(record: dict[str, Any] | None) -> str:
    if not isinstance(record, dict):
        return ""
    upper = trigram_display_en(record.get("upper_trigram"))
    lower = trigram_display_en(record.get("lower_trigram"))
    if upper and lower and upper == lower:
        return upper
    if upper and lower:
        return f"{upper} over {lower}"
    return upper or lower


def relative_posix(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def resolve_source_article(number: int, pinyin_candidates: list[str]) -> str:
    seen: list[str] = []
    for candidate in pinyin_candidates:
        candidate = candidate.strip()
        if candidate and candidate not in seen:
            seen.append(candidate)

    if not seen:
        seen.append(f"{number:02d}")

    article_paths: list[Path] = []
    for pinyin in seen:
        article_paths.append(ARTICLES_DIR / f"hexagram-{number:02d}-{pinyin}.md")
        article_paths.append(ARTICLES_DIR / f"hexagram_{number:02d}_{pinyin}.md")

    for article_path in article_paths:
        if article_path.exists():
            return relative_posix(article_path)

    return relative_posix(article_paths[0])


def parse_hexagram_dir_name(path: Path) -> tuple[int, str] | None:
    match = HEXAGRAM_DIR_RE.fullmatch(path.name)
    if not match:
        return None
    return int(match.group(1)), match.group(2)


def build_manifest(artifact_dir: Path, registry_record: dict[str, Any] | None) -> dict[str, Any]:
    parsed = parse_hexagram_dir_name(artifact_dir)
    if parsed is None:
        raise ValueError(f"Unsupported hexagram artifact directory name: {artifact_dir.name}")

    number, dir_pinyin = parsed
    record = registry_record or {}
    slug = artifact_dir.name
    name_zh = str(record.get("name_zh", "")).strip()
    name_en = str(record.get("name_en", "")).strip()
    name_pinyin = str(record.get("pinyin", "")).strip() or dir_pinyin

    assets = {
        "video": f"{slug}_video.mp4",
        "slides": f"{slug}_slides.pdf",
        "cover_4x3": f"{slug}_cover_4x3.png",
        "cover_3x4": f"{slug}_cover_3x4.png",
    }
    assets_status = {
        key: "present" if (artifact_dir / filename).exists() else "missing"
        for key, filename in assets.items()
    }

    zh_suffix = trigram_summary_zh(record)
    en_suffix = trigram_summary_en(record)
    title_zh = f"{ordinal_zh(number)} {name_zh or dir_pinyin}"
    if zh_suffix:
        title_zh = f"{title_zh} — {zh_suffix}"

    title_en = f"Hexagram {number:02d}: {title_case_pinyin(name_pinyin)}"
    en_parts = [part for part in [name_en, en_suffix] if part]
    if en_parts:
        title_en = f"{title_en} — {' / '.join(en_parts)}"

    source_article = resolve_source_article(number, [dir_pinyin, name_pinyin])
    ready_to_publish = assets_status["video"] == "present" and (
        assets_status["cover_4x3"] == "present" or assets_status["cover_3x4"] == "present"
    )

    return {
        "id": slug,
        "type": "hexagram",
        "book": "易经",
        "sequence": number,
        "title_zh": title_zh,
        "title_en": title_en,
        "name_zh": name_zh,
        "name_pinyin": name_pinyin,
        "language": "zh",
        "source_article": source_article,
        "assets": assets,
        "assets_status": assets_status,
        "ready_to_publish": ready_to_publish,
        "timestamp": datetime.now().astimezone().isoformat(timespec="seconds"),
    }


def find_hexagram_dirs() -> list[Path]:
    if not ARTIFACTS_DIR.exists():
        return []
    return sorted(
        path
        for path in ARTIFACTS_DIR.iterdir()
        if path.is_dir() and HEXAGRAM_DIR_RE.fullmatch(path.name)
    )


def main() -> int:
    args = parse_args()

    registry_by_number, registry_error = load_registry(REGISTRY_PATH)
    if registry_error:
        print(f"Warning: {registry_error}")
        print("Falling back to directory names where registry metadata is unavailable.")
    else:
        print(f"Loaded registry metadata for {len(registry_by_number)} hexagrams.")

    hexagram_dirs = find_hexagram_dirs()
    total = len(hexagram_dirs)
    if total == 0:
        print(f"No hexagram artifact directories found under {ARTIFACTS_DIR}")
        return 1

    print(f"Discovered {total} hexagram artifact directories under {relative_posix(ARTIFACTS_DIR)}")
    if total != 64:
        print(f"Warning: expected 64 hexagram directories, found {total}.")

    written = 0
    skipped = 0
    fallback_used = 0

    for index, artifact_dir in enumerate(hexagram_dirs, start=1):
        parsed = parse_hexagram_dir_name(artifact_dir)
        if parsed is None:
            print(f"[{index:02d}/{total:02d}] Skipped {artifact_dir.name}: unsupported directory name.")
            skipped += 1
            continue

        number, _ = parsed
        manifest_path = artifact_dir / "manifest.json"
        if manifest_path.exists() and not args.force:
            print(f"[{index:02d}/{total:02d}] Skipped {artifact_dir.name}: manifest.json exists.")
            skipped += 1
            continue

        record = registry_by_number.get(number)
        used_fallback = record is None
        if used_fallback:
            fallback_used += 1

        manifest = build_manifest(artifact_dir, record)
        action = "Overwrote" if manifest_path.exists() else "Wrote"
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        suffix = " (directory fallback)" if used_fallback else ""
        print(
            f"[{index:02d}/{total:02d}] {action} "
            f"{relative_posix(manifest_path)}{suffix}"
        )
        written += 1

    print("\nSummary")
    print(f"  Total directories: {total}")
    print(f"  Manifests written: {written}")
    print(f"  Manifests skipped: {skipped}")
    print(f"  Directory fallback used: {fallback_used}")
    print(f"  Force overwrite: {'yes' if args.force else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
