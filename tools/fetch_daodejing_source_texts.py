#!/usr/bin/env python3
"""Fetch and split Tao Te Ching source text into per-chapter files."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = REPO_ROOT / "texts" / "daodejing"
SOURCE_URL = "https://zh.wikisource.org/wiki/%E9%81%93%E5%BE%B7%E7%B6%93_%28%E7%8E%8B%E5%BC%BC%E6%9C%AC%29?action=raw"
USER_AGENT = "Mozilla/5.0 (compatible; OmegaDaodejingBot/1.0)"

DIGITS = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def chinese_to_int(token: str) -> int:
    """Convert chapter numerals like 四十二 or 十一 into ints."""
    token = token.strip()
    if token == "十":
        return 10
    if "十" in token:
        left, right = token.split("十", 1)
        tens = 1 if not left else DIGITS[left]
        ones = 0 if not right else DIGITS[right]
        return tens * 10 + ones
    return DIGITS[token]


def normalize_line(line: str) -> str:
    """Normalize one raw chapter line into plain text."""
    line = line.replace("\u3000", " ").strip()
    line = re.sub(r"-\{([^{}]+)\}-", r"\1", line)
    line = re.sub(r"\{\{\*\|([^{}]+)\}\}", r"（\1）", line)
    line = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", line)
    line = re.sub(r"\[\[([^\]]+)\]\]", lambda m: m.group(1).split("/")[-1], line)
    line = line.replace("'''", "").replace("''", "")
    return line.strip()


def fetch_raw_text() -> str:
    """Fetch Wang Bi version raw text from Wikisource."""
    request = Request(SOURCE_URL, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def parse_chapters(raw_text: str) -> dict[int, list[str]]:
    """Split the raw page into 81 chapter bodies."""
    chapters: dict[int, list[str]] = {}
    current_number: int | None = None
    current_lines: list[str] = []

    def flush_current():
        nonlocal current_number, current_lines
        if current_number is None:
            return
        cleaned = [line for line in current_lines if line]
        chapters[current_number] = cleaned
        current_number = None
        current_lines = []

    for raw_line in raw_text.splitlines():
        line = raw_line.strip()
        heading = re.match(r"^==([一二三四五六七八九十]+)章==$", line)
        if heading:
            flush_current()
            current_number = chinese_to_int(heading.group(1))
            current_lines = []
            continue

        if current_number is None:
            continue
        if line.startswith("="):
            flush_current()
            continue
        if not line or line.startswith(":"):
            continue

        normalized = normalize_line(line)
        if normalized:
            current_lines.append(normalized)

    flush_current()
    return chapters


def render_chapter_file(number: int, body_lines: list[str]) -> str:
    """Render one local chapter source file."""
    title = f"道德经 — 第{number}章"
    incipit = body_lines[0] if body_lines else ""
    notes = [
        "--- Notes ---",
        "Source: 維基文庫《道德經（王弼本）》",
        f"Chapter: {number}",
        f"Incipit: {incipit}",
        "Acquisition: fetched from Wikisource raw page and split into local chapter files.",
    ]
    return "\n".join([title, "", *body_lines, "", *notes]) + "\n"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    chapters = parse_chapters(fetch_raw_text())
    if len(chapters) != 81:
        raise SystemExit(f"Expected 81 chapters, got {len(chapters)}")

    for number in range(1, 82):
        body_lines = chapters[number]
        output_file = OUTPUT_DIR / f"chapter_{number:02d}.txt"
        output_file.write_text(render_chapter_file(number, body_lines), encoding="utf-8")
        print(f"Wrote {output_file}")


if __name__ == "__main__":
    main()
