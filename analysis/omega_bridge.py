#!/usr/bin/env python3
"""Bridge to automath Lean 4 discovery export.

Loads theorem inventory from automath's discovery report, generates it on demand
when possible, and provides query/citation helpers for the analysis pipeline.
"""

import json
import subprocess
from pathlib import Path


class OmegaBridge:
    """Interface to Omega's formal mathematical results."""

    def __init__(self, discovery_path: str = None):
        self.discoveries = {}
        self.theorems = []
        self.discovery_path = None
        if discovery_path:
            self.load(discovery_path)
        else:
            default = self.default_discovery_path()
            if default:
                self.load(str(default))

    @staticmethod
    def default_discovery_path() -> Path | None:
        """Return the best available discovery report path."""
        repo_root = Path(__file__).resolve().parent.parent.parent
        candidates = [
            repo_root / "automath" / "discovery" / "discovery_report.json",
            repo_root / "automath" / "tools" / "discovery-export" / "discovery" / "discovery_report.json",
        ]
        for path in candidates:
            if path.exists():
                return path
        return candidates[0]

    @staticmethod
    def ensure_discovery_report(path: str | Path):
        """Generate discovery report when missing and exporter is available."""
        p = Path(path)
        if p.exists():
            return

        repo_root = Path(__file__).resolve().parent.parent.parent
        exporter = repo_root / "automath" / "tools" / "discovery-export" / "lean4_discovery_export.py"
        if not exporter.exists():
            raise FileNotFoundError(
                f"Discovery report not found: {p}\n"
                f"Exporter missing: {exporter}"
            )

        p.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(
            ["python3", str(exporter), "--out", str(p)],
            cwd=exporter.parent,
            check=True,
            capture_output=True,
            text=True,
        )

    def load(self, path: str):
        """Load discovery report JSON."""
        p = Path(path)
        self.ensure_discovery_report(p)
        with open(p) as f:
            self.discoveries = json.load(f)
        self.theorems = self.discoveries.get("entries", self.discoveries.get("discoveries", []))
        self.discovery_path = p
        print(f"[OmegaBridge] Loaded {len(self.theorems)} theorems from {path}")

    @staticmethod
    def _module_match(lean_module: str, module: str | list[str] | None) -> bool:
        """Return True when a theorem matches the requested module hint(s)."""
        if not module:
            return True
        hints = [module] if isinstance(module, str) else module
        return any(hint in lean_module for hint in hints)

    def search(self, keywords: list[str], module: str | list[str] = None) -> list[dict]:
        """Search theorems by keywords and optional module filter."""
        results = []
        for thm in self.theorems:
            if not self._module_match(thm.get("lean_module", ""), module):
                continue
            text = f"{thm.get('lean_theorem', '')} {thm.get('lean_statement', '')}".lower()
            if any(kw.lower() in text for kw in keywords):
                results.append(thm)
        return results

    def search_ranked(
        self,
        keywords: list[str],
        module: str | list[str] = None,
        max_results: int = 20,
    ) -> list[dict]:
        """Keyword search with simple scoring for citation selection."""
        scored = []
        for thm in self.theorems:
            if not self._module_match(thm.get("lean_module", ""), module):
                continue
            name = thm.get("lean_theorem", "")
            stmt = thm.get("lean_statement", "")
            doc = thm.get("docstring", "")
            haystack = f"{name} {stmt} {doc}".lower()
            score = 0
            matched = []
            for kw in keywords:
                key = kw.lower()
                if key in name.lower():
                    score += 5
                    matched.append(kw)
                elif key in stmt.lower():
                    score += 3
                    matched.append(kw)
                elif key in doc.lower():
                    score += 1
                    matched.append(kw)
            if score > 0:
                entry = dict(thm)
                entry["_score"] = score
                entry["_matched_keywords"] = matched
                scored.append(entry)
        scored.sort(key=lambda x: (-x["_score"], x.get("lean_module", ""), x.get("lean_theorem", "")))
        return scored[:max_results]

    def get_by_names(self, theorem_names: list[str]) -> list[dict]:
        """Return theorems whose declaration names match exactly."""
        wanted = set(theorem_names)
        hits = [thm for thm in self.theorems if thm.get("lean_theorem", "") in wanted]
        hits.sort(key=lambda x: theorem_names.index(x.get("lean_theorem", "")))
        return hits

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

    def format_citations(self, theorems: list[dict], max_items: int = 8) -> str:
        """Format precise theorem citations for article insertion."""
        lines = []
        for thm in theorems[:max_items]:
            lines.append(
                f"- `{thm.get('lean_theorem', '?')}`"
                f" [{thm.get('lean_module', '?')}]"
                f" — {thm.get('lean_statement', '')[:220]}"
            )
        return "\n".join(lines)
