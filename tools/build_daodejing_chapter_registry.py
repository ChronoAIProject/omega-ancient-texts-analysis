#!/usr/bin/env python3
"""Build a structured Tao Te Ching chapter registry."""

from __future__ import annotations

import json
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WORK_DIR = REPO_ROOT / "workspace" / "道德经"
TEXTS_DIR = REPO_ROOT / "texts" / "daodejing"


def load_source_lines(path: Path) -> list[str]:
    """Load chapter body lines without notes."""
    lines = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line == "--- Notes ---":
            break
        if line.startswith("道德经 — 第"):
            continue
        lines.append(line)
    return lines


def shorten(text: str, limit: int = 18) -> str:
    """Shorten one line for titles and tables."""
    compact = text.replace("；", "，").replace("。", "").replace("、", "，")
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1] + "…"


def build_registry() -> dict:
    """Build chapter records using classification and theorem mappings."""
    classification = json.loads((WORK_DIR / "classification.json").read_text(encoding="utf-8"))
    theorem_map = json.loads((WORK_DIR / "omega_theorem_map.json").read_text(encoding="utf-8"))
    category_map = {item["id"]: item for item in classification["categories"]}
    theorem_by_category = {item["id"]: item for item in theorem_map["category_mappings"]}

    chapter_to_categories: dict[int, list[int]] = OrderedDict((number, []) for number in range(1, 82))
    for category in classification["categories"]:
        for chapter in category["chapters"]:
            chapter_to_categories.setdefault(chapter, []).append(category["id"])

    records = []
    for number in range(1, 82):
        text_path = TEXTS_DIR / f"chapter_{number:02d}.txt"
        source_lines = load_source_lines(text_path) if text_path.exists() else []
        category_ids = chapter_to_categories.get(number, [])
        category_refs = []
        direction_order = []
        theorem_hits = []
        theorem_seen = set()

        for category_id in category_ids:
            category = category_map[category_id]
            category_refs.append(
                {
                    "id": category_id,
                    "name_zh": category["name_zh"],
                    "name_en": category["name_en"],
                    "omega_directions": category["omega_directions"],
                    "formal_strength": category.get("formal_strength", ""),
                }
            )
            for direction in category["omega_directions"]:
                if direction not in direction_order:
                    direction_order.append(direction)
            theorem_mapping = theorem_by_category.get(category_id, {})
            for theorem in theorem_mapping.get("theorem_candidates", []):
                theorem_name = theorem["lean_theorem"]
                if theorem_name not in theorem_seen:
                    theorem_seen.add(theorem_name)
                    theorem_hits.append(theorem)

        incipit = source_lines[0] if source_lines else f"第{number}章"
        records.append(
            {
                "number": number,
                "incipit": incipit,
                "short_title": shorten(incipit),
                "source_text_path": str(text_path.relative_to(REPO_ROOT)) if text_path.exists() else "",
                "line_count": len(source_lines),
                "category_ids": category_ids,
                "category_refs": category_refs,
                "omega_directions": direction_order,
                "theorem_candidates": theorem_hits[:8],
            }
        )

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "work": "道德经",
        "total_chapters": len(records),
        "records": records,
    }


def render_markdown(registry: dict) -> str:
    """Render a compact chapter registry summary."""
    lines = [
        "# 道德经 81 章 Registry",
        "",
        "This registry combines per-chapter source files, the 12-category classification, and theorem-level Omega mapping candidates.",
        "",
        f"- Total chapters: {registry['total_chapters']}",
        "",
        "| # | 章首 | Categories | Omega Directions |",
        "|---|---|---|---|",
    ]
    for item in registry["records"]:
        categories = " / ".join(ref["name_zh"] for ref in item["category_refs"]) or "—"
        directions = ", ".join(item["omega_directions"]) or "—"
        lines.append(
            f"| {item['number']} | {item['short_title']} | {categories} | {directions} |"
        )
    lines.append("")
    return "\n".join(lines)


def main():
    output_dir = WORK_DIR / "chapters"
    output_dir.mkdir(parents=True, exist_ok=True)
    registry = build_registry()
    (output_dir / "registry.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "registry.md").write_text(render_markdown(registry), encoding="utf-8")
    print(f"Wrote {output_dir / 'registry.json'}")
    print(f"Wrote {output_dir / 'registry.md'}")


if __name__ == "__main__":
    main()
