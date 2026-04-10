#!/usr/bin/env python3
"""Build a structured 64-hexagram registry for the I Ching."""

from __future__ import annotations

import json
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

TRIGRAMS = OrderedDict(
    [
        ("乾", {"pinyin": "qian", "english": "Heaven", "bits": "111", "symbol": "☰"}),
        ("兌", {"pinyin": "dui", "english": "Lake", "bits": "110", "symbol": "☱"}),
        ("離", {"pinyin": "li", "english": "Flame", "bits": "101", "symbol": "☲"}),
        ("震", {"pinyin": "zhen", "english": "Thunder", "bits": "100", "symbol": "☳"}),
        ("巽", {"pinyin": "xun", "english": "Wind", "bits": "011", "symbol": "☴"}),
        ("坎", {"pinyin": "kan", "english": "Water", "bits": "010", "symbol": "☵"}),
        ("艮", {"pinyin": "gen", "english": "Mountain", "bits": "001", "symbol": "☶"}),
        ("坤", {"pinyin": "kun", "english": "Earth", "bits": "000", "symbol": "☷"}),
    ]
)

UPPER_ORDER = list(TRIGRAMS.keys())

# Data transcribed from the King Wen lookup table on Wikipedia's "Hexagram (I Ching)" page.
LOOKUP_ROWS = OrderedDict(
    [
        (
            "乾",
            [
                (1, "乾", "qian", "Force", "䷀"),
                (43, "夬", "guai", "Displacement", "䷪"),
                (14, "大有", "dayou", "Great Possessing", "䷍"),
                (34, "大壯", "dazhuang", "Great Invigorating", "䷡"),
                (9, "小畜", "xiaoxu", "Small Harvest", "䷈"),
                (5, "需", "xu", "Attending", "䷄"),
                (26, "大畜", "dachu", "Great Accumulating", "䷙"),
                (11, "泰", "tai", "Pervading", "䷊"),
            ],
        ),
        (
            "兌",
            [
                (10, "履", "lu", "Treading", "䷉"),
                (58, "兌", "dui", "Open", "䷹"),
                (38, "睽", "kui", "Polarising", "䷥"),
                (54, "歸妹", "guimei", "Converting the Maiden", "䷵"),
                (61, "中孚", "zhongfu", "Inner Truth", "䷼"),
                (60, "節", "jie", "Articulating", "䷻"),
                (41, "損", "sun", "Diminishing", "䷨"),
                (19, "臨", "lin", "Nearing", "䷒"),
            ],
        ),
        (
            "離",
            [
                (13, "同人", "tongren", "Concording People", "䷌"),
                (49, "革", "ge", "Skinning", "䷰"),
                (30, "離", "li", "Radiance", "䷝"),
                (55, "豐", "feng", "Abounding", "䷶"),
                (37, "家人", "jiaren", "Dwelling People", "䷤"),
                (63, "既濟", "jiji", "Already Fording", "䷾"),
                (22, "賁", "bi", "Adorning", "䷕"),
                (36, "明夷", "mingyi", "Intelligence Hidden", "䷣"),
            ],
        ),
        (
            "震",
            [
                (25, "无妄", "wuwang", "Innocence", "䷘"),
                (17, "隨", "sui", "Following", "䷐"),
                (21, "噬嗑", "shihe", "Gnawing Bite", "䷔"),
                (51, "震", "zhen", "Shake", "䷲"),
                (42, "益", "yi", "Augmenting", "䷩"),
                (3, "屯", "zhun", "Sprouting", "䷂"),
                (27, "頤", "yi", "Swallowing", "䷚"),
                (24, "復", "fu", "Returning", "䷗"),
            ],
        ),
        (
            "巽",
            [
                (44, "姤", "gou", "Coupling", "䷫"),
                (28, "大過", "daguo", "Great Exceeding", "䷛"),
                (50, "鼎", "ding", "Holding", "䷱"),
                (32, "恆", "heng", "Persevering", "䷟"),
                (57, "巽", "xun", "Ground", "䷸"),
                (48, "井", "jing", "Welling", "䷯"),
                (18, "蠱", "gu", "Correcting", "䷑"),
                (46, "升", "sheng", "Ascending", "䷭"),
            ],
        ),
        (
            "坎",
            [
                (6, "訟", "song", "Arguing", "䷅"),
                (47, "困", "kun", "Confining", "䷮"),
                (64, "未濟", "weiji", "Before Completion", "䷿"),
                (40, "解", "jie", "Deliverance", "䷧"),
                (59, "渙", "huan", "Dispersing", "䷺"),
                (29, "坎", "kan", "Gorge", "䷜"),
                (4, "蒙", "meng", "Enveloping", "䷃"),
                (7, "師", "shi", "Leading", "䷆"),
            ],
        ),
        (
            "艮",
            [
                (33, "遯", "dun", "Retiring", "䷠"),
                (31, "咸", "xian", "Conjoining", "䷞"),
                (56, "旅", "lu", "Sojourning", "䷷"),
                (62, "小過", "xiaoguo", "Small Exceeding", "䷽"),
                (53, "漸", "jian", "Infiltrating", "䷴"),
                (39, "蹇", "jian", "Limping", "䷦"),
                (52, "艮", "gen", "Bound", "䷳"),
                (15, "謙", "qian", "Humbling", "䷎"),
            ],
        ),
        (
            "坤",
            [
                (12, "否", "pi", "Obstruction", "䷋"),
                (45, "萃", "cui", "Clustering", "䷬"),
                (35, "晉", "jin", "Prospering", "䷢"),
                (16, "豫", "yu", "Providing-For", "䷏"),
                (20, "觀", "guan", "Viewing", "䷓"),
                (8, "比", "bi", "Grouping", "䷇"),
                (23, "剝", "bo", "Stripping", "䷖"),
                (2, "坤", "kun", "Field", "䷁"),
            ],
        ),
    ]
)


def load_inputs():
    """Load classification and theorem-map inputs."""
    work_dir = REPO_ROOT / "workspace" / "易经"
    classification = json.loads((work_dir / "classification.json").read_text(encoding="utf-8"))
    theorem_map = json.loads((work_dir / "omega_theorem_map.json").read_text(encoding="utf-8"))
    category_map = {item["id"]: item for item in classification["categories"]}
    theorem_by_category = {item["id"]: item for item in theorem_map["category_mappings"]}
    return work_dir, classification, category_map, theorem_by_category


def build_registry() -> dict:
    """Construct the full 64-hexagram registry."""
    work_dir, classification, category_map, theorem_by_category = load_inputs()
    texts_dir = REPO_ROOT / "texts" / "yijing"
    records = []

    number_to_categories = {}
    for category in classification["categories"]:
        for number in category["hexagrams"]:
            number_to_categories.setdefault(number, []).append(category["id"])

    for lower_name, row in LOOKUP_ROWS.items():
        lower = TRIGRAMS[lower_name]
        for upper_name, entry in zip(UPPER_ORDER, row):
            number, chinese, pinyin, english, symbol = entry
            upper = TRIGRAMS[upper_name]
            binary = lower["bits"] + upper["bits"]
            category_ids = number_to_categories.get(number, [])
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

            text_matches = sorted(texts_dir.glob(f"hexagram_{number:02d}_*.txt"))
            record = {
                "number": number,
                "symbol": symbol,
                "name_zh": chinese,
                "name_en": english,
                "pinyin": pinyin,
                "binary": binary,
                "lower_trigram": {
                    "name_zh": lower_name,
                    "name_en": lower["english"],
                    "pinyin": lower["pinyin"],
                    "bits": lower["bits"],
                    "symbol": lower["symbol"],
                },
                "upper_trigram": {
                    "name_zh": upper_name,
                    "name_en": upper["english"],
                    "pinyin": upper["pinyin"],
                    "bits": upper["bits"],
                    "symbol": upper["symbol"],
                },
                "yang_count": binary.count("1"),
                "adjacent_one_pairs": binary.count("11"),
                "max_one_run": max((len(run) for run in binary.split("0")), default=0),
                "gms_valid": "11" not in binary,
                "category_ids": category_ids,
                "category_refs": category_refs,
                "omega_directions": direction_order,
                "theorem_candidates": theorem_hits[:8],
                "source_text_path": str(text_matches[0].relative_to(REPO_ROOT)) if text_matches else "",
            }
            records.append(record)

    records.sort(key=lambda item: item["number"])
    pattern_to_number = {item["binary"]: item["number"] for item in records}

    for item in records:
        complement = "".join("1" if bit == "0" else "0" for bit in item["binary"])
        reverse = item["binary"][::-1]
        item["complement_binary"] = complement
        item["complement_hexagram"] = pattern_to_number[complement]
        item["reverse_binary"] = reverse
        item["reverse_hexagram"] = pattern_to_number[reverse]

    gms_valid_numbers = [item["number"] for item in records if item["gms_valid"]]
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_note": "Hexagram number/name/trigram lookup derived from the King Wen lookup table.",
        "total_hexagrams": len(records),
        "gms_valid_hexagrams": gms_valid_numbers,
        "records": records,
    }


def render_markdown(registry: dict) -> str:
    """Render a compact registry summary in Markdown."""
    lines = [
        "# 易经 64 卦 Registry",
        "",
        "This registry combines the King Wen lookup table, the current 12-category classification, and theorem-level Omega mapping candidates.",
        "",
        f"- Total hexagrams: {registry['total_hexagrams']}",
        f"- GMS-valid hexagrams: {len(registry['gms_valid_hexagrams'])}",
        f"- GMS-valid list: {', '.join(str(n) for n in registry['gms_valid_hexagrams'])}",
        "",
        "| # | 卦 | Binary | GMS | Categories | Omega Directions |",
        "|---|---|---|---|---|---|",
    ]
    for item in registry["records"]:
        categories = " / ".join(ref["name_zh"] for ref in item["category_refs"]) or "—"
        directions = ", ".join(item["omega_directions"]) or "—"
        gms = "yes" if item["gms_valid"] else "no"
        lines.append(
            f"| {item['number']} | {item['name_zh']} | `{item['binary']}` | {gms} | {categories} | {directions} |"
        )
    lines.append("")
    return "\n".join(lines)


def main():
    work_dir = REPO_ROOT / "workspace" / "易经"
    output_dir = work_dir / "hexagrams"
    output_dir.mkdir(parents=True, exist_ok=True)
    registry = build_registry()
    (output_dir / "registry.json").write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    (output_dir / "registry.md").write_text(render_markdown(registry), encoding="utf-8")
    print(f"Wrote {output_dir / 'registry.json'}")
    print(f"Wrote {output_dir / 'registry.md'}")


if __name__ == "__main__":
    main()
