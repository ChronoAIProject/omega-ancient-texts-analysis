#!/usr/bin/env python3
"""Structural pattern analysis for classical texts.

Identifies patterns in text structure that may correspond
to Omega mathematical structures.
"""

import re
from dataclasses import dataclass


@dataclass
class TextPattern:
    """A structural pattern found in a text."""
    name: str
    pattern_type: str  # symmetry, recursion, duality, hierarchy, numeric
    description: str
    location: str  # chapter/verse/line reference
    confidence: float  # 0.0 - 1.0


def analyze_structure(text: str, metadata: dict = None) -> list[TextPattern]:
    """Analyze text for structural patterns relevant to Omega."""
    patterns = []

    # Detect binary/duality structures (e.g., yin-yang)
    duality_markers = ["阴", "阳", "刚", "柔", "动", "静", "有", "无", "虚", "实"]
    duality_count = sum(text.count(m) for m in duality_markers)
    if duality_count > 5:
        patterns.append(TextPattern(
            name="binary_duality",
            pattern_type="duality",
            description=f"Binary opposition structure ({duality_count} markers)",
            location="throughout",
            confidence=min(duality_count / 20, 1.0),
        ))

    # Detect numeric sequences
    numbers = [int(n) for n in re.findall(r'\d+', text)]
    fib = {1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89}
    fib_hits = [n for n in numbers if n in fib]
    if len(fib_hits) > 2:
        patterns.append(TextPattern(
            name="fibonacci_numbers",
            pattern_type="numeric",
            description=f"Fibonacci numbers present: {fib_hits}",
            location="numeric references",
            confidence=min(len(fib_hits) / 5, 1.0),
        ))

    # Detect hierarchical structure (nested sections)
    section_depths = []
    for line in text.split("\n"):
        depth = len(line) - len(line.lstrip())
        if line.strip():
            section_depths.append(depth)
    unique_depths = len(set(section_depths))
    if unique_depths > 3:
        patterns.append(TextPattern(
            name="hierarchical_structure",
            pattern_type="hierarchy",
            description=f"Hierarchical nesting ({unique_depths} levels)",
            location="document structure",
            confidence=min(unique_depths / 6, 1.0),
        ))

    # Detect repetitive/recursive patterns
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    if len(lines) > 10:
        line_starts = {}
        for line in lines:
            start = line[:4] if len(line) >= 4 else line
            line_starts[start] = line_starts.get(start, 0) + 1
        repeated = {k: v for k, v in line_starts.items() if v > 3}
        if repeated:
            patterns.append(TextPattern(
                name="recursive_pattern",
                pattern_type="recursion",
                description=f"Repeated structural motifs: {list(repeated.keys())[:5]}",
                location="paragraph openings",
                confidence=min(max(repeated.values()) / 10, 1.0),
            ))

    return patterns
