#!/usr/bin/env python3
"""Build reusable theorem-level Omega mapping indices."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from analysis.omega_bridge import OmegaBridge
from analysis.theorem_mapper import build_direction_index, select_candidates_for_category


def render_markdown(work_name: str, category_mappings: list[dict]) -> str:
    """Create a compact human-readable theorem mapping summary."""
    lines = [
        f"# {work_name} Omega Theorem Pilot",
        "",
        "This file is generated from `discovery_report.json` and the work classification metadata.",
        "",
    ]
    for category in category_mappings:
        lines.append(f"## {category['id']:02d}. {category['name_zh']} / {category['name_en']}")
        lines.append("")
        lines.append(f"Omega directions: {', '.join(category.get('omega_directions', []))}")
        lines.append("")
        for group in category.get("direction_groups", []):
            lines.append(f"### {group['direction']}")
            lines.append("")
            if not group.get("candidates"):
                lines.append("- No theorem candidates selected.")
                lines.append("")
                continue
            for theorem in group["candidates"]:
                lines.append(
                    f"- `{theorem['lean_theorem']}` [{theorem['lean_module']}]"
                    f" — {theorem['lean_statement'][:220]}"
                )
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description="Build theorem-level Omega mapping index")
    parser.add_argument("--work", default="易经", help="Work name under workspace/")
    parser.add_argument(
        "--classification",
        help="Optional explicit path to classification.json",
    )
    parser.add_argument(
        "--output-json",
        help="Optional explicit output JSON path",
    )
    parser.add_argument(
        "--output-md",
        help="Optional explicit output Markdown path",
    )
    parser.add_argument(
        "--direction-limit",
        type=int,
        default=8,
        help="Candidates per global Omega direction",
    )
    parser.add_argument(
        "--per-direction",
        type=int,
        default=3,
        help="Candidates per direction inside each work category",
    )
    parser.add_argument(
        "--overall-limit",
        type=int,
        default=10,
        help="Overall candidate cap per category",
    )
    args = parser.parse_args()

    work_dir = REPO_ROOT / "workspace" / args.work
    classification_path = Path(args.classification) if args.classification else work_dir / "classification.json"
    output_json = Path(args.output_json) if args.output_json else work_dir / "omega_theorem_map.json"
    output_md = Path(args.output_md) if args.output_md else work_dir / "omega_theorem_map.md"

    classification = json.loads(classification_path.read_text(encoding="utf-8"))
    bridge = OmegaBridge()

    direction_index = build_direction_index(bridge, limit=args.direction_limit)
    category_mappings = [
        select_candidates_for_category(
            bridge=bridge,
            category=category,
            per_direction=args.per_direction,
            overall_limit=args.overall_limit,
        )
        for category in classification.get("categories", [])
    ]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "work": args.work,
        "discovery_path": str(bridge.discovery_path) if bridge.discovery_path else "",
        "classification_path": str(classification_path),
        "direction_index": direction_index,
        "category_mappings": category_mappings,
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(render_markdown(args.work, category_mappings), encoding="utf-8")

    print(f"Wrote {output_json}")
    print(f"Wrote {output_md}")


if __name__ == "__main__":
    main()
