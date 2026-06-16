# Broadcast Exports — Ancient Texts

Auto-populated by broadcast-local exports. Inputs are videos, captions, covers, audio, post-mortems, and A/B-test conclusions for ancient-text content (易经, 道德经, 黄帝内经, 孙子兵法, 几何原本, 庄子, hexagram and chapter series).

Upstream producer: `../../../omega-broadcast-local/` (local-only; may not exist on every machine).

## Program Board

Current human-facing broadcast board:

[`PROGRAM_BOARD.md`](PROGRAM_BOARD.md)

Use it for data trends, style shifts, scope, relative performance, and whether new measures were actually implemented.

## Buckets

```text
videos/             — final published videos (.mp4)
audio/              — NotebookLM podcasts + narration tracks (.wav, .mp3)
captions/           — shipped captions + caption variants (.md, .json)
covers/             — short-video covers, 4:3 横版 + 3:4 竖版 (.png)
post-mortems/       — per-卦象 / 章节 / 篇章 distribution retrospectives (.md)
ab-tests/           — A/B-test conclusions: hook framing, cover, caption length (.md, .json)
hexagram-series/    — series-specific cohort tracking for 64-卦 / 81-章 rollups
accounts-summary/   — per-account campaign rollups when a cycle closes
```

## Expected file-naming pattern

```text
{book}_{unit}_{slug}_{kind}.{ext}

book:   yijing | daodejing | huangdineijing | sunzi | euclid | zhuangzi
unit:   hexagram-NN | chapter-NN | category-NN | master | synthesis-NN
slug:   short snake_case identifier (e.g. qian, meng, dao-can-be-spoken)
kind:   video | audio | cover4x3 | cover3x4 | caption | postmortem | abtest
```

Examples:

```text
yijing_hexagram-04_meng_video.mp4
daodejing_chapter-01_dao-can-be-spoken_audio.wav
yijing_hexagram-04_meng_cover3x4.png
yijing_hexagram-04_meng_postmortem.md
yijing_hexagram-cohort_ab-hook-framing.md
```

See [`../../docs/distribution/README.md`](../../docs/distribution/README.md) for the broader 4-piece architecture and routing rules.
