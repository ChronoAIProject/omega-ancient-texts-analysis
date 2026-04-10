#!/usr/bin/env python3
"""Rename paper artifacts to match canonical prefixes expected by .qmd pages.

NotebookLM generates files like:
    Zero_Jitter_Information_Clocks_Parry_Gibbs_Rigidity_Jtp_video.mp4

But .qmd pages expect:
    zero_jitter_information_clocks_video.mp4

This script downloads from papers-media-v1, renames, uploads back with
canonical names, then deletes the old names.
"""

import subprocess
import tempfile
from pathlib import Path

REPO = "the-omega-institute/Omega-paper-series"
RELEASE = "papers-media-v1"

# Map: NotebookLM auto-name prefix → canonical prefix
RENAME_MAP = {
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


def gh(*args) -> subprocess.CompletedProcess:
    return subprocess.run(["gh"] + list(args), capture_output=True, text=True, timeout=300)


def main():
    r = gh("release", "view", RELEASE, "-R", REPO, "--json", "assets", "--jq", ".assets[].name")
    if r.returncode != 0:
        print(f"Failed to list assets: {r.stderr}")
        return
    existing = set(r.stdout.strip().split("\n")) if r.stdout.strip() else set()
    print(f"Existing assets: {len(existing)}")

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        renamed = 0

        for asset in sorted(existing):
            matched_prefix = None
            for long_prefix, canonical in RENAME_MAP.items():
                if asset.startswith(long_prefix):
                    matched_prefix = long_prefix
                    canonical_name = asset.replace(long_prefix, canonical)
                    break
            if not matched_prefix:
                continue
            if canonical_name == asset:
                continue
            if canonical_name in existing:
                print(f"  [skip] {canonical_name} already exists")
                continue

            print(f"  Rename: {asset}")
            print(f"      →: {canonical_name}")

            # Download
            dl_r = gh("release", "download", RELEASE, "-R", REPO, "-p", asset, "--dir", str(tmp), "--clobber")
            if dl_r.returncode != 0:
                print(f"    ✗ download failed: {dl_r.stderr[:100]}")
                continue

            downloaded = tmp / asset
            if not downloaded.exists():
                print(f"    ✗ file not found after download")
                continue

            # Move with new name
            new_path = tmp / canonical_name
            downloaded.rename(new_path)

            # Upload with new name
            up_r = gh("release", "upload", RELEASE, str(new_path), "-R", REPO, "--clobber")
            if up_r.returncode != 0:
                print(f"    ✗ upload failed: {up_r.stderr[:100]}")
                continue

            print(f"    ✓ uploaded canonical")
            renamed += 1

            # Delete old asset
            del_r = gh("release", "delete-asset", RELEASE, asset, "-R", REPO, "--yes")
            if del_r.returncode == 0:
                print(f"    ✓ deleted old")

        print(f"\nRenamed: {renamed}")


if __name__ == "__main__":
    main()
