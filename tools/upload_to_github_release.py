#!/usr/bin/env python3
"""Upload NotebookLM artifacts (video, slides, infographic) to GitHub releases.

Creates a 'media-v1' release on Omega-paper-series and uploads all artifacts.
Marketing team can then grab video URLs directly from GitHub.

Usage:
    python tools/upload_to_github_release.py                    # Upload all artifacts
    python tools/upload_to_github_release.py --dry-run          # Preview only
    python tools/upload_to_github_release.py --track tao-te-ching  # Single track
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = "the-omega-institute/Omega-paper-series"
ARTIFACTS_DIR = Path(__file__).parent.parent / "workspace" / "artifacts"
MEDIA_SUFFIXES = {".mp4", ".pdf", ".png", ".wav"}

# Route artifacts to releases by filename pattern
def release_for_file(filename: str) -> str:
    """Determine which release a file should go to."""
    if filename.startswith("master_"):
        return "master-videos-v1"
    # Paper notebook outputs (English title-cased filenames)
    paper_prefixes = (
        "Zero_Jitter", "Zeckendorf_Streaming", "Resolution_Folding",
        "Grg_Shell", "Folded_Rotation", "Fibonacci_Stabilization",
        "Fibonacci_Moduli_Cross", "Branch_Cubic_Regular",
        "Dynamical_Zeta",
    )
    if any(filename.startswith(p) for p in paper_prefixes):
        return "papers-media-v1"
    # Default: cultural
    return "cultural-media-v1"


# Map from NotebookLM auto-names to canonical names (for skip logic)
PAPER_NAME_MAP = {
    "Zero_Jitter_Information_Clocks_Parry_Gibbs_Rigidity_Jtp": "zero_jitter_information_clocks",
    "Zeckendorf_Streaming_Normalization_Automata_Rairo_Ita": "zeckendorf_streaming_normalization_automata",
    "Resolution_Folding_Core_Symbolic_Dynamics_Jnt": "resolution_folding_core_symbolic",
    "Grg_Shell_Geometry_From_Stationary_Detector_Thermality_Grg": "grg_shell_geometry_from",
    "Folded_Rotation_Histogram_Certificates_Siads": "folded_rotation_histogram_certificates",
    "Folded_Rotation_Histogram_Etds": "folded_rotation_histogram",
    "Fibonacci_Stabilization_Sharp_Threshold_Conjugacy_Nonlineari": "fibonacci_stabilization_sharp_threshold",
    "Fibonacci_Moduli_Cross_Resolution_Arithmetic_Rint": "fibonacci_moduli_cross_resolution",
    "Branch_Cubic_Regular_S4_Closure_Prym_Ray_Class_Jnt": "branch_cubic_regular_s4",
}


def canonical_version_exists(filename: str, existing_names: set) -> bool:
    """Check if a canonical version of this file already exists in release."""
    for long_prefix, canonical in PAPER_NAME_MAP.items():
        if filename.startswith(long_prefix):
            canonical_name = filename.replace(long_prefix, canonical)
            if canonical_name in existing_names:
                return True
    return False


def normalize_asset_name(filename: str) -> str:
    """Normalize a local filename to the form used by GitHub CLI release assets."""
    # gh release upload normalizes characters like spaces/colon into dots.
    normalized = re.sub(r"[^A-Za-z0-9._-]", ".", filename)
    normalized = re.sub(r"\.+", ".", normalized)
    normalized = normalized.strip(".")
    return normalized

TAG = "cultural-media-v1"  # default for --track filtering; actual routing via release_for_file


def gh(*args) -> subprocess.CompletedProcess:
    return subprocess.run(["gh"] + list(args), capture_output=True, text=True, timeout=300)


def require_gh_success(result: subprocess.CompletedProcess, action: str) -> None:
    if result.returncode == 0:
        return
    detail = (result.stderr or result.stdout).strip()
    print(f"Error: gh failed while trying to {action}.", file=sys.stderr)
    if detail:
        print(detail[:1000], file=sys.stderr)
    print("Run: gh auth login -h github.com", file=sys.stderr)
    raise SystemExit(1)


def ensure_release(tag: str = None):
    """Create release(s) if they don't exist."""
    tags = [tag] if tag else ["cultural-media-v1", "papers-media-v1", "master-videos-v1"]
    titles = {
        "cultural-media-v1": "Cultural Track Media Assets",
        "papers-media-v1": "Paper Media Assets (Infographics + Extras)",
        "master-videos-v1": "Master Flagship Videos",
    }
    for t in tags:
        r = gh("release", "view", t, "-R", REPO)
        if r.returncode != 0:
            print(f"Creating release {t}...")
            created = gh(
                "release",
                "create",
                t,
                "-R",
                REPO,
                "--title",
                titles.get(t, t),
                "--notes",
                f"Assets for {t}",
            )
            require_gh_success(created, f"create release {t}")


def list_existing_assets_all(required: bool = True) -> dict[str, set]:
    """Get names of already-uploaded assets for each release."""
    result = {}
    for tag in ["cultural-media-v1", "papers-media-v1", "master-videos-v1"]:
        r = gh("release", "view", tag, "-R", REPO, "--json", "assets", "--jq", ".assets[].name")
        if r.returncode == 0 and r.stdout.strip():
            result[tag] = set(r.stdout.strip().split("\n"))
        elif r.returncode == 0:
            result[tag] = set()
        elif required:
            require_gh_success(r, f"list assets for release {tag}")
        else:
            print(f"  [WARN] Could not list {tag}; dry run will assume no existing assets")
            result[tag] = set()
    return result


def list_existing_assets() -> set:
    """Legacy — returns cultural release assets only."""
    return list_existing_assets_all().get("cultural-media-v1", set())


def iter_media_files() -> list[Path]:
    """Recursively list media artifacts from the current hierarchical layout."""
    return sorted(
        path
        for path in ARTIFACTS_DIR.rglob("*")
        if path.is_file() and path.suffix in MEDIA_SUFFIXES
    )


def upload_artifacts(track_filter: str = None, dry_run: bool = False):
    """Upload all artifacts to the appropriate release (routed by filename)."""
    existing_by_release = list_existing_assets_all(required=not dry_run)
    print(f"  Existing: cultural={len(existing_by_release['cultural-media-v1'])}, "
          f"papers={len(existing_by_release['papers-media-v1'])}, "
          f"master={len(existing_by_release['master-videos-v1'])}")

    uploaded_by_release = {"cultural-media-v1": 0, "papers-media-v1": 0, "master-videos-v1": 0}
    seen_by_release = {tag: set(names) for tag, names in existing_by_release.items()}
    seen_by_release_norm = {
        tag: {normalize_asset_name(name) for name in names}
        for tag, names in existing_by_release.items()
    }
    for f in iter_media_files():
        target_release = release_for_file(f.name)
        normalized_name = normalize_asset_name(f.name)
        if f.name in seen_by_release[target_release] or normalized_name in seen_by_release_norm[target_release]:
            continue
        # Skip auto-named NotebookLM files if canonical version already exists.
        if canonical_version_exists(f.name, seen_by_release[target_release]):
            continue
        if track_filter and track_filter not in f.name:
            continue

        if dry_run:
            rel = f.relative_to(ARTIFACTS_DIR).as_posix()
            print(f"  [DRY RUN] {target_release} ← {rel} ({f.stat().st_size // 1024}KB)")
            uploaded_by_release[target_release] += 1
            seen_by_release[target_release].add(f.name)
            seen_by_release_norm[target_release].add(normalized_name)
        else:
            rel = f.relative_to(ARTIFACTS_DIR).as_posix()
            print(f"  → {target_release}: {rel} ({f.stat().st_size // 1024}KB)")
            r = gh("release", "upload", target_release, str(f), "-R", REPO, "--clobber")
            if r.returncode == 0:
                print(f"    ✓ uploaded")
                uploaded_by_release[target_release] += 1
                seen_by_release[target_release].add(f.name)
                seen_by_release_norm[target_release].add(normalized_name)
            else:
                print(f"    ✗ failed: {r.stderr[:200]}")

    total = sum(uploaded_by_release.values())
    label = "Would upload" if dry_run else "Uploaded"
    print(f"\n{'[DRY RUN] ' if dry_run else ''}{label}: {total} new assets")
    for t, n in uploaded_by_release.items():
        if n:
            print(f"  {t}: {n}")


def main():
    parser = argparse.ArgumentParser(description="Upload artifacts to GitHub release")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--track", help="Filter by track name")
    args = parser.parse_args()

    if not args.dry_run:
        ensure_release()
    upload_artifacts(track_filter=args.track, dry_run=args.dry_run)

    # Print download URLs
    if not args.dry_run:
        print(f"\nRelease URL: https://github.com/{REPO}/releases/tag/{TAG}")
        print(f"Download base: https://github.com/{REPO}/releases/download/{TAG}/")


if __name__ == "__main__":
    main()
