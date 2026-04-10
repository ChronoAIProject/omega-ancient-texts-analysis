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
import subprocess
import sys
from pathlib import Path

REPO = "the-omega-institute/Omega-paper-series"
ARTIFACTS_DIR = Path(__file__).parent.parent / "workspace" / "artifacts"

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

TAG = "cultural-media-v1"  # default for --track filtering; actual routing via release_for_file


def gh(*args) -> subprocess.CompletedProcess:
    return subprocess.run(["gh"] + list(args), capture_output=True, text=True, timeout=300)


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
            gh("release", "create", t, "-R", REPO, "--title", titles.get(t, t), "--notes", f"Assets for {t}")


def list_existing_assets_all() -> dict[str, set]:
    """Get names of already-uploaded assets for each release."""
    result = {}
    for tag in ["cultural-media-v1", "papers-media-v1", "master-videos-v1"]:
        r = gh("release", "view", tag, "-R", REPO, "--json", "assets", "--jq", ".assets[].name")
        if r.returncode == 0 and r.stdout.strip():
            result[tag] = set(r.stdout.strip().split("\n"))
        else:
            result[tag] = set()
    return result


def list_existing_assets() -> set:
    """Legacy — returns cultural release assets only."""
    return list_existing_assets_all().get("cultural-media-v1", set())


def upload_artifacts(track_filter: str = None, dry_run: bool = False):
    """Upload all artifacts to the appropriate release (routed by filename)."""
    existing_by_release = list_existing_assets_all()
    print(f"  Existing: cultural={len(existing_by_release['cultural-media-v1'])}, "
          f"papers={len(existing_by_release['papers-media-v1'])}, "
          f"master={len(existing_by_release['master-videos-v1'])}")

    uploaded_by_release = {"cultural-media-v1": 0, "papers-media-v1": 0, "master-videos-v1": 0}
    for artifact_dir in sorted(ARTIFACTS_DIR.iterdir()):
        if not artifact_dir.is_dir():
            continue

        for f in sorted(artifact_dir.iterdir()):
            if f.suffix not in (".mp4", ".pdf", ".png", ".wav"):
                continue
            target_release = release_for_file(f.name)
            if f.name in existing_by_release[target_release]:
                continue
            if track_filter and track_filter not in f.name:
                continue

            if dry_run:
                print(f"  [DRY RUN] {target_release} ← {f.name} ({f.stat().st_size // 1024}KB)")
            else:
                print(f"  → {target_release}: {f.name} ({f.stat().st_size // 1024}KB)")
                r = gh("release", "upload", target_release, str(f), "-R", REPO, "--clobber")
                if r.returncode == 0:
                    print(f"    ✓ uploaded")
                    uploaded_by_release[target_release] += 1
                else:
                    print(f"    ✗ failed: {r.stderr[:200]}")

    total = sum(uploaded_by_release.values())
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Uploaded: {total} new assets")
    for t, n in uploaded_by_release.items():
        if n:
            print(f"  {t}: {n}")


def main():
    parser = argparse.ArgumentParser(description="Upload artifacts to GitHub release")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--track", help="Filter by track name")
    args = parser.parse_args()

    ensure_release()
    upload_artifacts(track_filter=args.track, dry_run=args.dry_run)

    # Print download URLs
    if not args.dry_run:
        print(f"\nRelease URL: https://github.com/{REPO}/releases/tag/{TAG}")
        print(f"Download base: https://github.com/{REPO}/releases/download/{TAG}/")


if __name__ == "__main__":
    main()
