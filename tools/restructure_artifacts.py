#!/usr/bin/env python3
"""Reorganize flat artifact directories into a book-based hierarchy."""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

ARTIFACTS_ROOT = Path(__file__).resolve().parent.parent / "workspace" / "artifacts"

ROOT_DESTINATIONS = (
    "易经",
    "道德经",
    "黄帝内经",
    "孙子兵法",
    "几何原本",
    "庄子",
    "categories",
    "synthesis",
    "masters",
    "papers",
)
RESERVED_ROOT_DIRS = set(ROOT_DESTINATIONS)

RESET = "\033[0m"
BOLD = "\033[1m"
YELLOW = "\033[33m"
GRAY = "\033[90m"
RED = "\033[31m"
GREEN = "\033[32m"

BUCKET_LABELS = {
    "hexagrams": "hexagrams",
    "chapters": "chapters",
    "synthesis": "synthesis",
    "masters": "masters",
    "categories": "categories",
    "papers": "papers",
}
BUCKET_ORDER = (
    "hexagrams",
    "chapters",
    "synthesis",
    "masters",
    "categories",
    "papers",
)


@dataclass(slots=True)
class ArtifactPlan:
    source: Path
    target: Path
    bucket: str
    source_relative: str
    target_relative: str
    category_book: str | None = None
    notes: list[str] = field(default_factory=list)


def colorize(text: str, color: str) -> str:
    return f"{color}{text}{RESET}"


def print_move(message: str) -> None:
    print(colorize(message, YELLOW))


def print_skip(message: str) -> None:
    print(colorize(message, GRAY))


def print_error(message: str) -> None:
    print(colorize(message, RED))


def print_success(message: str) -> None:
    print(colorize(message, GREEN))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Reorganize workspace/artifacts into a hierarchical structure grouped by "
            "book. Dry run by default."
        )
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Perform the move operations and write migration metadata.",
    )
    return parser


def iter_flat_artifact_dirs(root: Path) -> tuple[list[Path], list[Path]]:
    candidates: list[Path] = []
    ignored: list[Path] = []

    for child in sorted(root.iterdir(), key=lambda path: path.name):
        if not child.is_dir():
            continue
        if child.name in RESERVED_ROOT_DIRS:
            ignored.append(child)
            continue
        candidates.append(child)

    return candidates, ignored


def extract_book_from_source(source: str) -> str | None:
    parts = [part for part in source.replace("\\", "/").split("/") if part]
    if not parts:
        return None

    if len(parts) >= 2 and parts[0] == "workspace":
        book = parts[1]
        if book not in {".", "..", "generated"}:
            return book

    for known_book in ROOT_DESTINATIONS[:6]:
        if known_book in parts or known_book in source:
            return known_book

    return None


def detect_category_book(artifact_dir: Path) -> tuple[str, list[str]]:
    manifest_path = artifact_dir / "manifest.json"
    if not manifest_path.exists():
        return "unknown", [
            f"WARNING {artifact_dir.name}: manifest.json missing, using categories/unknown"
        ]

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return "unknown", [
            f"WARNING {artifact_dir.name}: could not read manifest.json ({exc}), using categories/unknown"
        ]

    source = manifest.get("source")
    if not isinstance(source, str) or not source.strip():
        return "unknown", [
            f"WARNING {artifact_dir.name}: manifest.json has no usable 'source', using categories/unknown"
        ]

    book = extract_book_from_source(source)
    if book is None:
        return "unknown", [
            f"WARNING {artifact_dir.name}: could not determine book from source '{source}', using categories/unknown"
        ]

    return book, []


def classify_artifact(root: Path, artifact_dir: Path) -> ArtifactPlan:
    name = artifact_dir.name
    notes: list[str] = []

    if name.startswith("hexagram-"):
        relative_target = Path("易经") / name
        bucket = "hexagrams"
        category_book = None
    elif name.startswith("daodejing_chapter"):
        relative_target = Path("道德经") / name
        bucket = "chapters"
        category_book = None
    elif name.startswith("synthesis_"):
        relative_target = Path("synthesis") / name
        bucket = "synthesis"
        category_book = None
    elif name.startswith("master_"):
        relative_target = Path("masters") / name
        bucket = "masters"
        category_book = None
    elif name.startswith("category_"):
        category_book, notes = detect_category_book(artifact_dir)
        relative_target = Path("categories") / category_book / name
        bucket = "categories"
    else:
        relative_target = Path("papers") / name
        bucket = "papers"
        category_book = None

    return ArtifactPlan(
        source=artifact_dir,
        target=root / relative_target,
        bucket=bucket,
        source_relative=artifact_dir.relative_to(root).as_posix(),
        target_relative=relative_target.as_posix(),
        category_book=category_book,
        notes=notes,
    )


def target_conflict_reason(target: Path) -> str | None:
    if not target.exists():
        return None

    if not target.is_dir():
        return "target path already exists and is not a directory"

    try:
        has_content = any(target.iterdir())
    except OSError as exc:
        return f"could not inspect existing target ({exc})"

    if has_content:
        return "target directory already exists with content"

    return None


def prepare_layout(root: Path) -> None:
    for directory in ROOT_DESTINATIONS:
        (root / directory).mkdir(parents=True, exist_ok=True)


def ensure_target_parent(target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_summary_parts(counts: dict[str, int]) -> str:
    return ", ".join(
        f"{counts[bucket]} {BUCKET_LABELS[bucket]}" for bucket in BUCKET_ORDER
    )


def build_category_summary(category_books: dict[str, int]) -> str:
    if not category_books:
        return ""
    ordered_books = sorted(category_books.items(), key=lambda item: item[0])
    return ", ".join(f"{book}: {count}" for book, count in ordered_books)


def remove_empty_placeholder(target: Path) -> None:
    if target.exists() and target.is_dir():
        try:
            next(target.iterdir())
        except StopIteration:
            target.rmdir()


def empty_counts() -> dict[str, int]:
    return {bucket: 0 for bucket in BUCKET_ORDER}


def execute_moves(
    plans: Iterable[ArtifactPlan], root: Path
) -> tuple[list[dict[str, str]], dict[str, str], dict[str, int], int, int]:
    migration_log: list[dict[str, str]] = []
    publish_registry: dict[str, str] = {}
    moved_counts = empty_counts()
    skipped = 0
    errors = 0

    prepare_layout(root)

    for plan in plans:
        for note in plan.notes:
            print_skip(note)

        conflict = target_conflict_reason(plan.target)
        if conflict is not None:
            print_skip(f"SKIP {plan.source_relative} -> {plan.target_relative} ({conflict})")
            publish_registry[plan.source.name] = plan.source_relative
            skipped += 1
            continue

        try:
            ensure_target_parent(plan.target)
            remove_empty_placeholder(plan.target)
            shutil.move(str(plan.source), str(plan.target))
        except Exception as exc:  # noqa: BLE001
            print_error(f"ERROR moving {plan.source_relative} -> {plan.target_relative}: {exc}")
            publish_registry[plan.source.name] = plan.source_relative
            errors += 1
            continue

        print_move(f"MOVE {plan.source_relative} -> {plan.target_relative}")
        migration_log.append({"from": plan.source_relative, "to": plan.target_relative})
        publish_registry[plan.source.name] = plan.target_relative
        moved_counts[plan.bucket] += 1

    return migration_log, publish_registry, moved_counts, skipped, errors


def preview_moves(plans: Iterable[ArtifactPlan]) -> tuple[dict[str, str], dict[str, int], int]:
    publish_registry: dict[str, str] = {}
    would_move_counts = empty_counts()
    skipped = 0

    for plan in plans:
        for note in plan.notes:
            print_skip(note)

        conflict = target_conflict_reason(plan.target)
        if conflict is not None:
            print_skip(f"SKIP {plan.source_relative} -> {plan.target_relative} ({conflict})")
            publish_registry[plan.source.name] = plan.source_relative
            skipped += 1
            continue

        print_move(f"WOULD MOVE {plan.source_relative} -> {plan.target_relative}")
        publish_registry[plan.source.name] = plan.target_relative
        would_move_counts[plan.bucket] += 1

    return publish_registry, would_move_counts, skipped


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not ARTIFACTS_ROOT.exists():
        print_error(f"Artifacts root does not exist: {ARTIFACTS_ROOT}")
        return 1
    if not ARTIFACTS_ROOT.is_dir():
        print_error(f"Artifacts root is not a directory: {ARTIFACTS_ROOT}")
        return 1

    artifact_dirs, ignored_dirs = iter_flat_artifact_dirs(ARTIFACTS_ROOT)
    plans = [classify_artifact(ARTIFACTS_ROOT, artifact_dir) for artifact_dir in artifact_dirs]

    category_books: dict[str, int] = {}
    for plan in plans:
        if plan.category_book:
            category_books[plan.category_book] = category_books.get(plan.category_book, 0) + 1

    heading = "EXECUTE" if args.execute else "DRY RUN"
    print(colorize(f"{heading} {ARTIFACTS_ROOT}", BOLD))

    if ignored_dirs:
        ignored_names = ", ".join(path.name for path in ignored_dirs)
        print_skip(f"Ignoring already-structured directories at root: {ignored_names}")

    if not plans:
        print_skip("No flat artifact directories found to process.")
        return 0

    if args.execute:
        migration_log, publish_registry, moved_counts, skipped_count, errors = execute_moves(
            plans, ARTIFACTS_ROOT
        )
        try:
            write_json(ARTIFACTS_ROOT / "migration_log.json", migration_log)
            write_json(ARTIFACTS_ROOT / "publish_registry.json", publish_registry)
        except OSError as exc:
            print_error(f"ERROR writing metadata files: {exc}")
            return 1

        moved_count = len(migration_log)
        print_success(f"Moved {moved_count} directories ({build_summary_parts(moved_counts)})")
        if skipped_count:
            print_skip(f"Skipped {skipped_count} directories because targets were not safe to overwrite.")
        if errors:
            print_error(f"Encountered {errors} move errors.")
        category_summary = build_category_summary(category_books)
        if category_summary:
            print(f"Category books: {category_summary}")
        print_success(
            f"Wrote migration_log.json ({len(migration_log)} entries) and publish_registry.json ({len(publish_registry)} entries)."
        )
        return 1 if errors else 0

    publish_registry, would_move_counts, skipped = preview_moves(plans)
    would_move_total = sum(would_move_counts.values())
    print_success(f"Would move {would_move_total} directories ({build_summary_parts(would_move_counts)})")
    if skipped:
        print_skip(f"Would skip {skipped} directories because targets already exist with content.")
    category_summary = build_category_summary(category_books)
    if category_summary:
        print(f"Category books: {category_summary}")
    print_success(
        f"Would write migration_log.json ({would_move_total} entries) and publish_registry.json ({len(publish_registry)} entries) on --execute."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
