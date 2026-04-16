#!/usr/bin/env python3
"""Build a unified publish registry for workspace artifacts."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
WORKSPACE_DIR = REPO_ROOT / "workspace"
ARTIFACTS_DIR = WORKSPACE_DIR / "artifacts"
OUTPUT_PATH = WORKSPACE_DIR / "publish_registry.json"

BOOKS = {
    "易经": {"en": "I Ching", "lang": "zh", "prefix": "hexagram", "total": 64},
    "道德经": {"en": "Tao Te Ching", "lang": "zh", "prefix": "daodejing_chapter", "total": 81},
    "黄帝内经": {"en": "Huangdi Neijing", "lang": "zh"},
    "孙子兵法": {"en": "Art of War", "lang": "zh"},
    "几何原本": {"en": "Euclid's Elements", "lang": "en"},
    "庄子": {"en": "Zhuangzi", "lang": "zh"},
    "论语": {"en": "Analects", "lang": "zh"},
}

EXTRA_BOOKS = {
    "综合": {"en": "Synthesis", "lang": "zh"},
    "Omega": {"en": "Omega", "lang": "en"},
    "未知": {"en": "Unknown", "lang": "zh"},
}

BOOK_ORDER = {
    name: index
    for index, name in enumerate([*BOOKS.keys(), "综合", "Omega", "未知"], start=1)
}

TYPE_ORDER = {
    "master": 0,
    "chapter": 1,
    "category": 2,
    "synthesis": 3,
}

HEXAGRAM_RE = re.compile(r"^hexagram-(\d{2})-([a-z0-9-]+)$")
DAODEJING_RE = re.compile(r"^daodejing_chapter-(\d{2})$")
CATEGORY_RE = re.compile(r"^category_(\d{2})_(.+)$")
SYNTHESIS_RE = re.compile(r"^synthesis_(\d{2})_(.+)$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", re.DOTALL)
BILINGUAL_RE = re.compile(r"(?P<zh>[\u4e00-\u9fff][^/\n\"”]{1,80})\s*/\s*(?P<en>[A-Za-z][^\n\"”]{2,160})")

MASTER_BOOK_HINTS = (
    ("I_Ching", "易经"),
    ("Tao_Te_Ching", "道德经"),
    ("Huangdi_Neijing", "黄帝内经"),
    ("Art_of_War", "孙子兵法"),
    ("Euclid's_Elements", "几何原本"),
    ("Euclids_Elements", "几何原本"),
    ("Zhuangzi", "庄子"),
    ("Analects", "论语"),
)


def chinese_number(value: int) -> str:
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

    if value < 0:
        raise ValueError(f"Chinese numeral conversion does not support negative values: {value}")
    if value < 10:
        return digits[value]
    if value == 10:
        return "十"
    if value < 20:
        return f"十{digits[value % 10]}"
    if value < 100:
        tens, ones = divmod(value, 10)
        if ones == 0:
            return f"{digits[tens]}十"
        return f"{digits[tens]}十{digits[ones]}"
    if value < 1000:
        hundreds, remainder = divmod(value, 100)
        if remainder == 0:
            return f"{digits[hundreds]}百"
        if remainder < 10:
            return f"{digits[hundreds]}百零{digits[remainder]}"
        return f"{digits[hundreds]}百{chinese_number(remainder)}"
    raise ValueError(f"Chinese numeral conversion only supports values below 1000: {value}")


def book_meta(book: str) -> dict[str, Any]:
    return BOOKS.get(book, EXTRA_BOOKS.get(book, EXTRA_BOOKS["未知"]))


def relative_to_workspace(path: Path) -> str | None:
    try:
        return path.relative_to(WORKSPACE_DIR).as_posix()
    except ValueError:
        return None


def normalize_workspace_path(raw: Any, require_exists: bool = False) -> str | None:
    if not isinstance(raw, str):
        return None

    value = raw.strip()
    if not value or value.startswith("error:"):
        return None

    raw_path = Path(value)
    candidates: list[Path] = []
    if raw_path.is_absolute():
        candidates.append(raw_path)
    else:
        if value.startswith("workspace/"):
            candidates.append(REPO_ROOT / value)
        candidates.append(WORKSPACE_DIR / value)
        candidates.append(REPO_ROOT / value)

    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        relative = relative_to_workspace(candidate)
        if relative is None:
            continue
        if require_exists and not candidate.exists():
            continue
        return relative
    return None


def existing_relative_file(path: Path) -> str | None:
    if path.is_file():
        return relative_to_workspace(path)
    return None


def first_existing_relative(paths: list[Path]) -> str | None:
    for path in paths:
        relative = existing_relative_file(path)
        if relative:
            return relative
    return None


def first_candidate_relative(paths: list[Path]) -> str | None:
    existing = first_existing_relative(paths)
    if existing:
        return existing
    for path in paths:
        relative = relative_to_workspace(path)
        if relative:
            return relative
    return None


def load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def load_text(path: Path | None) -> str:
    if path is None or not path.is_file():
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


def frontmatter_value(text: str, key: str) -> str | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None

    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        candidate_key, candidate_value = line.split(":", 1)
        if candidate_key.strip() != key:
            continue
        value = candidate_value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        return value.strip()
    return None


def first_markdown_heading(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return None


def heading_prefix(heading: str | None) -> str | None:
    if not heading:
        return None
    for separator in ("：", ":"):
        if separator in heading:
            return heading.split(separator, 1)[0].strip()
    return heading.strip() or None


def metadata_bullet_value(text: str, label: str) -> str | None:
    pattern = re.compile(rf"^- {re.escape(label)}:\s*(.+)$", re.MULTILINE)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return None


def extract_category_english_title(text: str, zh_title: str | None) -> str | None:
    sample = "\n".join(text.splitlines()[:80])
    fallback: str | None = None
    for match in BILINGUAL_RE.finditer(sample):
        zh_value = match.group("zh").strip(" “\"'`，,。：:;；")
        en_value = match.group("en").strip(" ”\"'`，,。：:;；")
        if zh_value in {"摘要", "引言", "原文精选"} or en_value in {"Abstract", "Introduction", "Selected Passages"}:
            continue
        if zh_title and (zh_title in zh_value or zh_value in zh_title):
            return en_value
        if fallback is None:
            fallback = en_value
    return fallback


def title_case_slug(value: str) -> str:
    words = [word for word in re.split(r"[_-]+", value) if word]
    titled = []
    for word in words:
        if any(char.isdigit() for char in word):
            titled.append(word[:1].upper() + word[1:])
        else:
            titled.append(word.capitalize())
    return " ".join(titled)


def artifact_media_paths(artifact_dir: Path) -> dict[str, str | None]:
    base = artifact_dir.name
    return {
        "video": existing_relative_file(artifact_dir / f"{base}_video.mp4"),
        "slides": existing_relative_file(artifact_dir / f"{base}_slides.pdf"),
        "cover_4x3": existing_relative_file(artifact_dir / f"{base}_cover_4x3.png"),
        "cover_3x4": existing_relative_file(artifact_dir / f"{base}_cover_3x4.png"),
    }


def video_ready(artifact_dir: Path) -> bool:
    video_path = artifact_dir / f"{artifact_dir.name}_video.mp4"
    try:
        return video_path.is_file() and video_path.stat().st_size > 0
    except OSError:
        return False


def build_generated_index() -> dict[str, Path]:
    index: dict[str, Path] = {}
    for book in BOOKS:
        generated_dir = WORKSPACE_DIR / book / "generated"
        if not generated_dir.is_dir():
            continue
        for path in generated_dir.glob("*.md"):
            index[path.stem] = path
    return index


def infer_category_article(artifact_dir: Path, manifest: dict[str, Any], generated_index: dict[str, Path]) -> str | None:
    source = normalize_workspace_path(manifest.get("source"), require_exists=False)
    if source:
        return source
    source_path = generated_index.get(artifact_dir.name)
    if source_path is not None:
        return relative_to_workspace(source_path)
    return None


def infer_book_from_article(article: str | None) -> str:
    if not article:
        return "未知"
    book = Path(article).parts[0]
    if book in BOOKS:
        return book
    if book == "synthesis":
        return "综合"
    return "未知"


def infer_master_book(directory_name: str) -> str:
    if directory_name == "master_Omega_Research_Papers_Overview":
        return "Omega"
    for fragment, book in MASTER_BOOK_HINTS:
        if fragment in directory_name:
            return book
    return "未知"


def hexagram_article_candidates(sequence: int, slug: str) -> list[Path]:
    return [
        WORKSPACE_DIR / "易经" / "hexagrams" / "all" / f"hexagram-{sequence:02d}-{slug}.md",
        WORKSPACE_DIR / "易经" / "hexagrams" / "all" / f"hexagram_{sequence:02d}_{slug}.md",
    ]


def daodejing_article_candidates(sequence: int) -> list[Path]:
    return [
        WORKSPACE_DIR / "道德经" / "chapters" / "all" / f"chapter-{sequence:02d}.md",
        WORKSPACE_DIR / "道德经" / "chapters" / "all" / f"daodejing_chapter-{sequence:02d}.md",
    ]


def article_absolute_path(article: str | None) -> Path | None:
    if not article:
        return None
    return WORKSPACE_DIR / Path(article)


def build_hexagram_entry(artifact_dir: Path) -> dict[str, Any] | None:
    match = HEXAGRAM_RE.fullmatch(artifact_dir.name)
    if not match:
        return None

    sequence = int(match.group(1))
    slug = match.group(2)
    article = first_candidate_relative(hexagram_article_candidates(sequence, slug))
    article_text = load_text(article_absolute_path(article))
    frontmatter_title = frontmatter_value(article_text, "title")

    name_zh = ""
    if frontmatter_title and "." in frontmatter_title:
        name_zh = frontmatter_title.split(".", 1)[1].strip()
    if not name_zh:
        name_zh = title_case_slug(slug)

    media = artifact_media_paths(artifact_dir)
    book = "易经"
    meta = book_meta(book)

    return {
        "id": artifact_dir.name,
        "book": book,
        "book_en": meta["en"],
        "sequence": sequence,
        "title_zh": f"第{chinese_number(sequence)}卦 {name_zh}",
        "title_en": f"Hexagram {sequence:02d}: {title_case_slug(slug)}",
        "language": meta["lang"],
        "type": "chapter",
        "video": media["video"],
        "article": article,
        "slides": media["slides"],
        "cover_4x3": media["cover_4x3"],
        "cover_3x4": media["cover_3x4"],
        "ready": video_ready(artifact_dir),
    }


def build_daodejing_entry(artifact_dir: Path) -> dict[str, Any] | None:
    match = DAODEJING_RE.fullmatch(artifact_dir.name)
    if not match:
        return None

    sequence = int(match.group(1))
    article = first_candidate_relative(daodejing_article_candidates(sequence))
    article_text = load_text(article_absolute_path(article))
    frontmatter_title = frontmatter_value(article_text, "title")

    title_zh = f"第{chinese_number(sequence)}章"
    if frontmatter_title and "." in frontmatter_title:
        suffix = frontmatter_title.split(".", 1)[1].strip()
        if suffix:
            title_zh = f"{title_zh} {suffix}"

    media = artifact_media_paths(artifact_dir)
    book = "道德经"
    meta = book_meta(book)

    return {
        "id": artifact_dir.name,
        "book": book,
        "book_en": meta["en"],
        "sequence": sequence,
        "title_zh": title_zh,
        "title_en": f"Chapter {sequence:02d}",
        "language": meta["lang"],
        "type": "chapter",
        "video": media["video"],
        "article": article,
        "slides": media["slides"],
        "cover_4x3": media["cover_4x3"],
        "cover_3x4": media["cover_3x4"],
        "ready": video_ready(artifact_dir),
    }


def build_category_entry(artifact_dir: Path, generated_index: dict[str, Path]) -> dict[str, Any] | None:
    match = CATEGORY_RE.fullmatch(artifact_dir.name)
    if not match:
        return None

    sequence = int(match.group(1))
    slug = match.group(2)
    manifest = load_json(artifact_dir / "manifest.json")
    article = infer_category_article(artifact_dir, manifest, generated_index)
    book = infer_book_from_article(article)
    meta = book_meta(book)

    article_text = load_text(article_absolute_path(article))
    heading = first_markdown_heading(article_text)
    title_zh = heading_prefix(heading) or f"类别 {sequence:02d}"
    title_en = extract_category_english_title(article_text, title_zh) or title_case_slug(slug)
    media = artifact_media_paths(artifact_dir)

    return {
        "id": artifact_dir.name,
        "book": book,
        "book_en": meta["en"],
        "sequence": sequence,
        "title_zh": title_zh,
        "title_en": title_en,
        "language": meta["lang"],
        "type": "category",
        "video": media["video"],
        "article": article,
        "slides": media["slides"],
        "cover_4x3": media["cover_4x3"],
        "cover_3x4": media["cover_3x4"],
        "ready": video_ready(artifact_dir),
    }


def build_synthesis_entry(artifact_dir: Path) -> dict[str, Any] | None:
    if artifact_dir.name.endswith("_source"):
        return None

    match = SYNTHESIS_RE.fullmatch(artifact_dir.name)
    if not match:
        return None

    sequence = int(match.group(1))
    slug = match.group(2)
    manifest = load_json(artifact_dir / "manifest.json")
    article = normalize_workspace_path(manifest.get("source"), require_exists=False)
    article_text = load_text(article_absolute_path(article))

    main_title = metadata_bullet_value(article_text, "主标题")
    english_title = metadata_bullet_value(article_text, "英文标题")
    heading = first_markdown_heading(article_text)
    title_zh = heading or (f"综合 {sequence:02d}：{main_title}" if main_title else f"综合 {sequence:02d}")
    title_en = (
        f"Synthesis {sequence:02d}: {english_title}"
        if english_title
        else f"Synthesis {sequence:02d}: {title_case_slug(slug)}"
    )

    media = artifact_media_paths(artifact_dir)
    book = "综合"
    meta = book_meta(book)

    return {
        "id": artifact_dir.name,
        "book": book,
        "book_en": meta["en"],
        "sequence": sequence,
        "title_zh": title_zh,
        "title_en": title_en,
        "language": meta["lang"],
        "type": "synthesis",
        "video": media["video"],
        "article": article,
        "slides": media["slides"],
        "cover_4x3": media["cover_4x3"],
        "cover_3x4": media["cover_3x4"],
        "ready": video_ready(artifact_dir),
    }


def build_master_entry(artifact_dir: Path) -> dict[str, Any] | None:
    if not artifact_dir.name.startswith("master_"):
        return None

    book = infer_master_book(artifact_dir.name)
    meta = book_meta(book)

    if book in BOOKS:
        title_zh = f"《{book}》的数学"
        title_en = f"The Mathematics of {meta['en']}"
    elif artifact_dir.name == "master_Omega_Research_Papers_Overview":
        title_zh = "Omega 研究论文总览"
        title_en = "Omega Research Papers Overview"
    else:
        title_zh = title_case_slug(artifact_dir.name.removeprefix("master_"))
        title_en = title_case_slug(artifact_dir.name.removeprefix("master_"))

    media = artifact_media_paths(artifact_dir)

    return {
        "id": artifact_dir.name,
        "book": book,
        "book_en": meta["en"],
        "sequence": 0,
        "title_zh": title_zh,
        "title_en": title_en,
        "language": meta["lang"],
        "type": "master",
        "video": media["video"],
        "article": None,
        "slides": media["slides"],
        "cover_4x3": media["cover_4x3"],
        "cover_3x4": media["cover_3x4"],
        "ready": video_ready(artifact_dir),
    }


def build_entry(artifact_dir: Path, generated_index: dict[str, Path]) -> dict[str, Any] | None:
    name = artifact_dir.name
    if name.startswith("hexagram-"):
        return build_hexagram_entry(artifact_dir)
    if name.startswith("daodejing_chapter-"):
        return build_daodejing_entry(artifact_dir)
    if name.startswith("category_"):
        return build_category_entry(artifact_dir, generated_index)
    if name.startswith("synthesis_"):
        return build_synthesis_entry(artifact_dir)
    if name.startswith("master_"):
        return build_master_entry(artifact_dir)
    return None


def sort_key(entry: dict[str, Any]) -> tuple[int, int, int, str]:
    return (
        BOOK_ORDER.get(str(entry["book"]), 999),
        int(entry["sequence"]),
        TYPE_ORDER.get(str(entry["type"]), 999),
        str(entry["id"]),
    )


def build_registry() -> list[dict[str, Any]]:
    generated_index = build_generated_index()
    entries: list[dict[str, Any]] = []

    if not ARTIFACTS_DIR.is_dir():
        return entries

    for artifact_dir in sorted(path for path in ARTIFACTS_DIR.iterdir() if path.is_dir()):
        entry = build_entry(artifact_dir, generated_index)
        if entry is not None:
            entries.append(entry)

    entries.sort(key=sort_key)
    return entries


def write_registry(entries: list[dict[str, Any]]) -> None:
    OUTPUT_PATH.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def print_summary(entries: list[dict[str, Any]]) -> None:
    ready_count = sum(1 for entry in entries if entry["ready"])
    breakdown: dict[str, dict[str, int]] = defaultdict(lambda: {"entries": 0, "ready": 0})

    for entry in entries:
        book = str(entry["book"])
        breakdown[book]["entries"] += 1
        if entry["ready"]:
            breakdown[book]["ready"] += 1

    print(f"Wrote {OUTPUT_PATH}")
    print(f"{len(entries)} entries, {ready_count} ready")
    print("By book:")
    for book in sorted(breakdown, key=lambda name: BOOK_ORDER.get(name, 999)):
        counts = breakdown[book]
        print(f"- {book}: {counts['entries']} entries, {counts['ready']} ready")


def main() -> None:
    entries = build_registry()
    write_registry(entries)
    print_summary(entries)


if __name__ == "__main__":
    main()
