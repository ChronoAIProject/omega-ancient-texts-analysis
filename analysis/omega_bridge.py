#!/usr/bin/env python3
"""Bridge to automath Lean 4 discovery export.

Loads theorem inventory from automath's discovery_report.json
and provides query interface for the analysis pipeline.
"""

import json
from pathlib import Path


class OmegaBridge:
    """Interface to Omega's formal mathematical results."""

    def __init__(self, discovery_path: str = None):
        self.discoveries = {}
        self.theorems = []
        if discovery_path:
            self.load(discovery_path)

    def load(self, path: str):
        """Load discovery report JSON."""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(
                f"Discovery report not found: {path}\n"
                "Run: cd ../automath && python tools/discovery-export/lean4_discovery_export.py"
            )
        with open(p) as f:
            self.discoveries = json.load(f)
        self.theorems = self.discoveries.get("entries", [])
        print(f"[OmegaBridge] Loaded {len(self.theorems)} theorems from {path}")

    def search(self, keywords: list[str], module: str = None) -> list[dict]:
        """Search theorems by keywords and optional module filter."""
        results = []
        for thm in self.theorems:
            if module and module not in thm.get("lean_module", ""):
                continue
            text = f"{thm.get('lean_theorem', '')} {thm.get('lean_statement', '')}".lower()
            if any(kw.lower() in text for kw in keywords):
                results.append(thm)
        return results

    def get_by_module(self, module: str) -> list[dict]:
        """Get all theorems from a specific module."""
        return [t for t in self.theorems if module in t.get("lean_module", "")]

    def get_summary(self) -> dict:
        """Get summary statistics."""
        modules = set()
        types = {}
        for thm in self.theorems:
            modules.add(thm.get("lean_module", "unknown").split(".")[1] if "." in thm.get("lean_module", "") else "unknown")
            t = thm.get("lean_type", "unknown")
            types[t] = types.get(t, 0) + 1
        return {
            "total_theorems": len(self.theorems),
            "modules": sorted(modules),
            "type_counts": types,
        }

    def format_for_prompt(self, theorems: list[dict], max_items: int = 20) -> str:
        """Format theorems for LLM prompt injection."""
        lines = []
        for thm in theorems[:max_items]:
            name = thm.get("lean_theorem", "?")
            module = thm.get("lean_module", "?")
            stmt = thm.get("lean_statement", "")[:200]
            lines.append(f"- [{module}] {name}: {stmt}")
        return "\n".join(lines)
