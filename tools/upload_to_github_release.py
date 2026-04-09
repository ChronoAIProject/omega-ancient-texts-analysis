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
TAG = "cultural-media-v1"


def gh(*args) -> subprocess.CompletedProcess:
    return subprocess.run(["gh"] + list(args), capture_output=True, text=True, timeout=300)


def ensure_release():
    """Create release if it doesn't exist."""
    r = gh("release", "view", TAG, "-R", REPO)
    if r.returncode != 0:
        print(f"Creating release {TAG}...")
        gh("release", "create", TAG, "-R", REPO,
           "--title", "Cultural Track Media Assets",
           "--notes", "NotebookLM-generated videos, slides, and infographics for 道德经, 易经, 黄帝内经 Omega analyses.")
        print(f"  ✓ Release {TAG} created")
    else:
        print(f"  Release {TAG} exists")


def list_existing_assets() -> set:
    """Get names of already-uploaded assets."""
    r = gh("release", "view", TAG, "-R", REPO, "--json", "assets", "--jq", ".[].name")
    if r.returncode == 0:
        return set(r.stdout.strip().split("\n")) if r.stdout.strip() else set()
    return set()


def upload_artifacts(track_filter: str = None, dry_run: bool = False):
    """Upload all artifacts to the release."""
    existing = list_existing_assets()
    print(f"  Existing assets: {len(existing)}")

    uploaded = 0
    for artifact_dir in sorted(ARTIFACTS_DIR.iterdir()):
        if not artifact_dir.is_dir():
            continue

        for f in sorted(artifact_dir.iterdir()):
            if f.suffix not in (".mp4", ".pdf", ".png", ".wav"):
                continue
            if f.name in existing:
                continue
            if track_filter and track_filter not in f.name:
                continue

            if dry_run:
                print(f"  [DRY RUN] would upload: {f.name} ({f.stat().st_size // 1024}KB)")
            else:
                print(f"  Uploading: {f.name} ({f.stat().st_size // 1024}KB)...")
                r = gh("release", "upload", TAG, str(f), "-R", REPO, "--clobber")
                if r.returncode == 0:
                    print(f"    ✓ uploaded")
                    uploaded += 1
                else:
                    print(f"    ✗ failed: {r.stderr[:200]}")

    print(f"\n{'[DRY RUN] ' if dry_run else ''}Uploaded: {uploaded} new assets")


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
