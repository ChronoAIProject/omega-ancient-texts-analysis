"""Content quality anti-pattern detector for G3 review gate.

Ported concept from automath PR #37 detect_shell_pattern() — which
catches Codex producing fake Lean proofs wrapped in abstract structures.

Our equivalent: detect when G3 Codex review output is "fake pass" —
template text, suspiciously short, or repeats the prompt structure
instead of actually reviewing the content.

Usage:
    from publication.slop_detector import detect_slop

    issues = detect_slop(codex_response, item_id="hexagram-09")
    if issues:
        # Reject this G3 round, re-prompt or escalate
"""

from __future__ import annotations

import re
from typing import Any

# Patterns that indicate the review is template/placeholder, not genuine
TEMPLATE_PHRASES = [
    "no issues found",
    "everything looks good",
    "all checks passed",
    "content is satisfactory",
    "meets all requirements",
    "no problems detected",
    # Chinese equivalents
    "没有问题",
    "一切正常",
    "全部通过",
    "内容合格",
]

# If the entire review is shorter than this, it's suspiciously shallow
MIN_REVIEW_CHARS = 80

# If the review contains more prompt-echo than analysis
PROMPT_ECHO_MARKERS = [
    "you are reviewing",
    "your task is to",
    "please check the following",
    "检查以下内容",
    "你的任务是",
    "请审查",
]


def detect_slop(
    response: dict[str, Any],
    *,
    item_id: str = "",
) -> list[str]:
    """Scan a G3 Codex/Claude review response for quality anti-patterns.

    Returns a list of violation descriptions (empty = clean).
    """
    issues: list[str] = []

    # Flatten response to text for scanning
    text = _flatten_to_text(response)
    text_lower = text.lower().strip()

    # 1. Suspiciously short review
    if len(text_lower) < MIN_REVIEW_CHARS:
        issues.append(
            f"review too short ({len(text_lower)} chars < {MIN_REVIEW_CHARS} min) "
            f"— likely template or skipped analysis"
        )

    # 2. Template phrase detection
    for phrase in TEMPLATE_PHRASES:
        if phrase.lower() in text_lower:
            # Only flag if the review is ALSO short — a long detailed review
            # that happens to say "no issues found" at the end is fine
            if len(text_lower) < 300:
                issues.append(
                    f"template phrase detected: '{phrase}' in a {len(text_lower)}-char "
                    f"review — likely rubber-stamp"
                )
                break

    # 3. Prompt echo — model repeating the instructions instead of reviewing
    echo_count = sum(1 for m in PROMPT_ECHO_MARKERS if m.lower() in text_lower)
    if echo_count >= 2:
        issues.append(
            f"{echo_count} prompt-echo markers found — model may be "
            f"repeating instructions instead of analyzing content"
        )

    # 4. Perfect scores with no specifics
    if "score" in response:
        score = response.get("score")
        if isinstance(score, (int, float)) and score >= 9:
            # Check if there are specific findings
            findings = response.get("issues", response.get("findings", []))
            if not findings or (isinstance(findings, list) and len(findings) == 0):
                issues.append(
                    f"perfect score ({score}/10) with zero findings — "
                    f"suspiciously uncritical review"
                )

    # 5. All-same-value pattern (every check marked identical)
    checks = response.get("checks", {})
    if isinstance(checks, dict) and len(checks) >= 3:
        values = list(checks.values())
        if len(set(str(v) for v in values)) == 1:
            issues.append(
                f"all {len(checks)} checks have identical value '{values[0]}' — "
                f"likely batch-stamped without individual inspection"
            )

    return issues


def _flatten_to_text(obj: Any) -> str:
    """Recursively extract all string values from a dict/list structure."""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        return " ".join(_flatten_to_text(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return " ".join(_flatten_to_text(v) for v in obj)
    return str(obj)


if __name__ == "__main__":
    # Test cases
    print("=== Test 1: Template response (should detect) ===")
    issues = detect_slop(
        {"review": "No issues found. Everything looks good.", "score": 10, "issues": []},
        item_id="test-1",
    )
    for i in issues:
        print(f"  DETECTED: {i}")

    print("\n=== Test 2: Genuine review (should pass) ===")
    issues = detect_slop(
        {
            "review": (
                "Audio track present at -16.2dB mean volume. Language detected as Chinese "
                "via Whisper transcript. Title '第十卦 履' matches article heading. "
                "Cover 4:3 has title text fully visible. Cover 3:4 crops the bottom "
                "subtitle slightly — minor issue, acceptable for Douyin. "
                "One concern: the transcript mentions 'Fibonacci sequence' in English "
                "at 3:42 which breaks the zh-only language policy for this channel."
            ),
            "score": 7,
            "issues": ["english_term_in_zh_video"],
            "checks": {
                "audio_present": True,
                "language_match": True,
                "title_match": True,
                "cover_readable": "partial",
            },
        },
        item_id="test-2",
    )
    if not issues:
        print("  PASS (clean review)")
    else:
        for i in issues:
            print(f"  UNEXPECTED: {i}")

    print("\n=== Test 3: Perfect score + no findings (should detect) ===")
    issues = detect_slop(
        {"score": 10, "issues": [], "review": "Great content, very well done overall."},
        item_id="test-3",
    )
    for i in issues:
        print(f"  DETECTED: {i}")

    print("\n=== Test 4: All-same checks (should detect) ===")
    issues = detect_slop(
        {
            "review": "Checked everything, all good across the board.",
            "checks": {"audio": "pass", "video": "pass", "cover": "pass", "language": "pass"},
        },
        item_id="test-4",
    )
    for i in issues:
        print(f"  DETECTED: {i}")
