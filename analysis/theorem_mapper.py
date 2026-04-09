#!/usr/bin/env python3
"""Helpers for selecting theorem-level Omega citations for text mappings."""

from __future__ import annotations

import re
from typing import Iterable

from analysis.omega_bridge import OmegaBridge
from analysis.theorem_profiles import DIRECTION_PROFILES, iter_profile_keywords

STOPWORDS = {
    "and", "the", "with", "from", "into", "through", "over", "under", "between",
    "this", "that", "these", "those", "their", "theme", "category", "hexagrams",
    "chapters", "lines", "states", "dynamic", "structural", "change", "pure",
    "development", "system", "patterns", "pattern", "relation", "relations",
}


def _tokenize_english(text: str) -> list[str]:
    """Extract useful English search terms from category metadata."""
    tokens = []
    for token in re.findall(r"[A-Za-z][A-Za-z\\-]{2,}", text or ""):
        lowered = token.lower()
        if lowered not in STOPWORDS:
            tokens.append(lowered)
    return tokens


def _compact_theorem(entry: dict) -> dict:
    """Keep only fields useful for citation and indexing."""
    return {
        "lean_theorem": entry.get("lean_theorem", ""),
        "lean_module": entry.get("lean_module", ""),
        "lean_type": entry.get("lean_type", ""),
        "lean_statement": entry.get("lean_statement", ""),
        "paper_labels": entry.get("paper_labels", []),
        "matched_keywords": entry.get("_matched_keywords", []),
        "score": entry.get("_score", 0),
    }


def _merge_candidates(exact_hits: Iterable[dict], ranked_hits: Iterable[dict], limit: int) -> list[dict]:
    """Deduplicate candidates while preserving exact-hit priority."""
    merged = []
    seen = set()
    for entry in list(exact_hits) + list(ranked_hits):
        name = entry.get("lean_theorem", "")
        if not name or name in seen:
            continue
        seen.add(name)
        merged.append(_compact_theorem(entry))
        if len(merged) >= limit:
            break
    return merged


def select_candidates_for_direction(
    bridge: OmegaBridge,
    direction: str,
    extra_keywords: list[str] | None = None,
    limit: int = 6,
) -> dict:
    """Select theorem candidates for one Omega direction profile."""
    profile = DIRECTION_PROFILES.get(direction, {})
    exact_hits = bridge.get_by_names(profile.get("preferred_theorems", []))
    ranked_hits = bridge.search_ranked(
        keywords=iter_profile_keywords(direction, extra_keywords),
        module=profile.get("module_hints"),
        max_results=max(limit * 3, 12),
    )
    return {
        "direction": direction,
        "label": profile.get("label", direction),
        "module_hints": profile.get("module_hints", []),
        "candidates": _merge_candidates(exact_hits, ranked_hits, limit),
    }


def select_candidates_for_category(
    bridge: OmegaBridge,
    category: dict,
    per_direction: int = 3,
    overall_limit: int = 10,
) -> dict:
    """Build grouped and flattened theorem candidates for one category."""
    extra_keywords = _tokenize_english(category.get("name_en", ""))
    extra_keywords.extend(_tokenize_english(category.get("theme", "")))
    grouped = []
    flat = []
    seen = set()

    for direction in category.get("omega_directions", []):
        group = select_candidates_for_direction(
            bridge=bridge,
            direction=direction,
            extra_keywords=extra_keywords,
            limit=per_direction,
        )
        grouped.append(group)
        for entry in group["candidates"]:
            theorem_name = entry.get("lean_theorem", "")
            if theorem_name and theorem_name not in seen and len(flat) < overall_limit:
                seen.add(theorem_name)
                flat.append(entry)

    return {
        "id": category.get("id"),
        "name_zh": category.get("name_zh"),
        "name_en": category.get("name_en"),
        "omega_directions": category.get("omega_directions", []),
        "direction_groups": grouped,
        "theorem_candidates": flat,
    }


def build_direction_index(bridge: OmegaBridge, limit: int = 8) -> dict:
    """Build a reusable theorem index for all configured directions."""
    index = {}
    for direction in DIRECTION_PROFILES:
        result = select_candidates_for_direction(bridge, direction, limit=limit)
        index[direction] = result
    return index


def format_category_citations(category_mapping: dict, max_items: int = 8) -> str:
    """Render a prompt-friendly citation block for one category."""
    lines = []
    for entry in category_mapping.get("theorem_candidates", [])[:max_items]:
        line = (
            f"- `{entry['lean_theorem']}` [{entry['lean_module']}]"
            f" — {entry['lean_statement'][:220]}"
        )
        lines.append(line)
    return "\n".join(lines)
