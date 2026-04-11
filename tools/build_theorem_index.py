#!/usr/bin/env python3
"""Build a theorem → cultural interpretations reverse index using MemPalace.

For each of the top Omega theorems, search MemPalace for cultural files that
cite it, and emit a reverse index markdown.

Output: Omega-paper-series/cultural/theorem-index/<theorem_name>.md

Usage:
    python tools/build_theorem_index.py --list                # Show top theorems
    python tools/build_theorem_index.py --theorem fibonacci_cardinality
    python tools/build_theorem_index.py --all                 # Build full index
"""

import argparse
import re
import subprocess
from pathlib import Path

PALACE = "/Users/lexa/Desktop/lexa/omega/omega-palace"
MEMPALACE = "/Users/lexa/Desktop/lexa/omega/omega-ancient-texts-analysis/.venv/bin/mempalace"
OUTPUT_DIR = Path("/Users/lexa/Desktop/lexa/omega/Omega-paper-series/cultural/theorem-index")

# Top theorems to index (ordered by expected frequency)
TOP_THEOREMS = [
    "fibonacci_cardinality",
    "fibonacci_cardinality_recurrence",
    "goldenMean_characteristic_recurrence",
    "goldenMeanAdjacency_cayley_hamilton",
    "inverse_limit_extensionality",
    "inverse_limit_bijective",
    "inverse_limit_left",
    "topological_entropy_eq_log_phi",
    "goldenMeanAdjacency_has_goldenRatio_eigenvector",
    "zeckendorf_unique",
    "zeckendorf_representation",
    "fold_idempotent",
    "restrict_compose",
    "prefixWord",
    "stableZero_unique",
    "CompatibleFamily",
]


def mempalace_search(query: str) -> str:
    """Run mempalace search and return raw output."""
    r = subprocess.run(
        [MEMPALACE, "--palace", PALACE, "search", query],
        capture_output=True, text=True, timeout=60,
    )
    return r.stdout


def parse_results(output: str, theorem: str) -> list[dict]:
    """Extract (source, match_score, snippet) from mempalace output."""
    results = []
    # Parse [N] source matches
    entries = re.split(r'\n\s*\[\d+\]', output)
    for entry in entries[1:]:  # skip header
        source_match = re.search(r'Source:\s*(\S+)', entry)
        match_score = re.search(r'Match:\s*([-.\d]+)', entry)
        if not source_match:
            continue
        # Only include entries that actually mention the theorem name
        if theorem not in entry:
            continue
        results.append({
            "source": source_match.group(1),
            "score": float(match_score.group(1)) if match_score else 0.0,
            "snippet": entry[:500].strip(),
        })
    return results[:15]  # top 15 citations


def build_index_entry(theorem: str) -> str:
    """Build markdown for one theorem."""
    output = mempalace_search(theorem)
    results = parse_results(output, theorem)

    # Deduplicate by source (keep highest score)
    by_source = {}
    for r in results:
        src = r["source"]
        if src not in by_source or r["score"] > by_source[src]["score"]:
            by_source[src] = r

    lines = [
        f"---",
        f"title: \"`{theorem}`\"",
        f"subtitle: \"Theorem-level reverse index\"",
        f"categories: [theorem-index, omega]",
        f"---",
        f"",
        f"## 引用位置 / Citations",
        f"",
        f"MemPalace 检索到 {len(by_source)} 处对 `{theorem}` 的引用：",
        f"",
    ]

    # Group by type
    cultural = []
    automath = []
    other = []
    for src, r in sorted(by_source.items(), key=lambda x: -x[1]["score"]):
        if "hexagram" in src or "chapter" in src or "category" in src or "essay" in src:
            cultural.append(r)
        elif src.endswith(".py") or "Omega" in src:
            automath.append(r)
        else:
            other.append(r)

    if cultural:
        lines.append("### 文化映射 / Cultural Mappings")
        lines.append("")
        for r in cultural:
            lines.append(f"- **{r['source']}** (match {r['score']:.2f})")
        lines.append("")

    if automath:
        lines.append("### Automath / Lean 4 Source")
        lines.append("")
        for r in automath:
            lines.append(f"- **{r['source']}** (match {r['score']:.2f})")
        lines.append("")

    if other:
        lines.append("### Other Context")
        lines.append("")
        for r in other:
            lines.append(f"- **{r['source']}** (match {r['score']:.2f})")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--theorem", help="Single theorem name to index")
    parser.add_argument("--all", action="store_true", help="Build index for all top theorems")
    parser.add_argument("--list", action="store_true", help="List top theorems")
    args = parser.parse_args()

    if args.list:
        for t in TOP_THEOREMS:
            print(f"  {t}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    theorems = [args.theorem] if args.theorem else (TOP_THEOREMS if args.all else [])
    if not theorems:
        parser.print_help()
        return

    for theorem in theorems:
        print(f"Building: {theorem}")
        content = build_index_entry(theorem)
        out_file = OUTPUT_DIR / f"{theorem}.md"
        out_file.write_text(content)
        print(f"  → {out_file.name}")


if __name__ == "__main__":
    main()
