#!/usr/bin/env python3
"""Fetch and normalize local Yijing source texts from Wikisource."""

from __future__ import annotations

import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.build_yijing_hexagram_registry import LOOKUP_ROWS, TRIGRAMS, UPPER_ORDER

OUTPUT_DIR = REPO_ROOT / "texts" / "yijing"
USER_AGENT = "Mozilla/5.0 (compatible; OmegaYijingBot/1.0)"


def iter_hexagrams():
    """Yield structured hexagram metadata from the King Wen table."""
    for lower_name, row in LOOKUP_ROWS.items():
        lower = TRIGRAMS[lower_name]
        for upper_name, entry in zip(UPPER_ORDER, row):
            number, chinese, pinyin, english, _symbol = entry
            upper = TRIGRAMS[upper_name]
            yield {
                "number": number,
                "name_zh": chinese,
                "pinyin": pinyin,
                "name_en": english,
                "lower_name": lower_name,
                "upper_name": upper_name,
                "binary": lower["bits"] + upper["bits"],
            }


def fetch_raw_wikisource(name_zh: str) -> str:
    """Fetch raw wikitext for one hexagram page."""
    title = quote(f"周易/{name_zh}")
    url = f"https://zh.wikisource.org/wiki/{title}?action=raw"
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8")


def normalize_wikitext(raw: str, name_zh: str) -> list[str]:
    """Convert noisy wikitext into plain-text source lines."""
    text = raw.replace("\r\n", "\n")
    text = re.sub(r"<span[^>]*>", "", text, flags=re.S)
    text = re.sub(r"</span>", "", text)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text, flags=re.S)
    text = re.sub(r"\{\{\*\|([^{}]+)\}\}", r"（\1）", text)
    text = re.sub(r"-\{([^{}]+)\}-", r"\1", text)
    text = re.sub(r"\[\[File:[^\]]+\]\]", "", text)
    text = re.sub(r"\[\[([^|\]]+)\|([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", lambda m: m.group(1).split("/")[-1], text)
    text = text.replace("'''", "").replace("''", "")
    text = unescape(text)

    started = False
    lines: list[str] = []
    for raw_line in text.splitlines():
        if not started:
            if "[[周易]]" in raw_line or "周易" in raw_line:
                started = True
            else:
                continue

        line = raw_line.replace("\u3000", " ").strip()
        line = re.sub(r"^[*#:;]+", "", line).strip()
        line = re.sub(r"\s+", " ", line).strip()

        if not line:
            continue
        if line.startswith(("{{", "}}", "|", "header2", "previous", "next", "section=", "T|周易/")):
            continue
        if line in {"-", ":"}:
            continue
        if line.startswith("周易 "):
            continue
        if line == name_zh:
            continue

        lines.append(line)

    cleaned: list[str] = []
    previous_blank = False
    for line in lines:
        if line:
            cleaned.append(line)
            previous_blank = False
        elif not previous_blank:
            cleaned.append("")
            previous_blank = True
    return cleaned


def render_text_file(item: dict, lines: list[str]) -> str:
    """Render a local plain-text file."""
    title = f"{item['name_zh']} — 第{item['number']}卦"
    notes = [
        "--- Notes ---",
        "Source: 維基文庫《周易》分卦頁面（public domain transcription）",
        f"Hexagram: {item['number']} ({item['name_zh']} {item['pinyin'].title()} / {item['name_en']})",
        f"Structure: {item['lower_name']}下{item['upper_name']}上 ({item['binary']} in binary)",
        "Acquisition: fetched from Wikisource raw pages and normalized into local plain text.",
    ]
    return "\n".join([title, "", *lines, "", *notes]) + "\n"


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for item in iter_hexagrams():
        raw = fetch_raw_wikisource(item["name_zh"])
        lines = normalize_wikitext(raw, item["name_zh"])
        filename = OUTPUT_DIR / f"hexagram_{item['number']:02d}_{item['pinyin']}.txt"
        filename.write_text(render_text_file(item, lines), encoding="utf-8")
        print(f"Wrote {filename}")


if __name__ == "__main__":
    main()
