"""Stage 5 auto-publishing pipeline for the ancient texts content series.

Orchestrates content from the produced-artifact state to Lydia's
publish_queue.json via four gates:
  G1 — deterministic batch split (LLM only on ambiguous data)
  G2 — media production wrapping notebooklm_batch + build_covers
  G3 — dual-AI content review (Codex + Claude, with reconcile)
  G4 — idempotent queue writer

Design doc: ~/.gstack/projects/omega/lexa-main-design-20260416-154806.md
"""
