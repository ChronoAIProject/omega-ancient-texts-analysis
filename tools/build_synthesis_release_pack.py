#!/usr/bin/env python3
"""Build structured release packs for cross-text synthesis essays.

Outputs:
  - workspace/synthesis/media_registry.json
  - workspace/synthesis/notebooklm_sources/*.md
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SYNTHESIS_DIR = ROOT / "workspace" / "synthesis"
REGISTRY_PATH = SYNTHESIS_DIR / "registry.json"
MEDIA_REGISTRY_PATH = SYNTHESIS_DIR / "media_registry.json"
NOTEBOOKLM_DIR = SYNTHESIS_DIR / "notebooklm_sources"
MEDIA_LANGUAGE_PROFILE = "zh_primary_bilingual"


WORK_LINKS = {
    "道德经": "cultural/tao-te-ching/index.qmd",
    "易经": "cultural/i-ching/index.qmd",
    "黄帝内经": "cultural/huangdi-neijing/index.qmd",
    "孙子兵法": "cultural/sunzi/index.qmd",
    "几何原本": "cultural/elements/index.qmd",
}


def build_source_markdown(entry: dict, essay_body: str) -> str:
    support = ", ".join(f"`{name}`" for name in entry.get("support_theorems", [])) or "无"
    works = "\n".join(f"- {name}" for name in entry.get("works", []))
    papers = "\n".join(f"- {slug}" for slug in entry.get("paper_refs", []))
    return f"""# 综合 {entry['id']:02d}：{entry['title_zh']}

## 核心元数据

- 主标题: {entry['title_zh']}
- 英文标题: {entry['title_en']}
- 主定理核: `{entry['primary_theorem']}`
- 支撑定理: {support}

## 覆盖经典

{works}

## 关联论文

{papers}

## NotebookLM 使用说明

请保持 **中文主叙事 + 英文辅助 rigor** 的双语方式，突出这篇综合文如何从一个 Omega 定理核出发，贯穿五部经典与 Gen 2 论文。

### 语言与受众

- 主要受众: 中文社交媒体与中文教育传播场景
- 主语言: 中文
- 辅助语言: 英文
- 英文的职责: theorem names、关键术语、每个大段结尾的 1-2 句 rigor summary
- 禁止把整支视频或整套 slides 变成英文主讲

### 输出风格

- 先用中文讲结构美感与跨文本映射
- 保留原始中文引文，不要把古籍改写成纯英文 paraphrase
- 每个大段可附一个很短的英文小结，方便国际受众和技术读者
- Lean 定理名、论文标题、数学对象名保留英文或中英并列

### 输出重点

输出重点依次为：

1. 主定理核与支持定理
2. 五部经典的结构映射
3. 与 Gen 2 论文的严格数学回收
4. 明确区分 formal correspondence 与 metaphorical analogy

---

{essay_body.strip()}
"""


def main() -> None:
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    NOTEBOOKLM_DIR.mkdir(parents=True, exist_ok=True)

    media_entries = []
    for entry in registry["essays"]:
        essay_path = ROOT / entry["file"]
        essay_body = essay_path.read_text(encoding="utf-8")
        artifact_slug = f"synthesis_{entry['id']:02d}_{entry['slug']}"
        notebooklm_path = NOTEBOOKLM_DIR / f"{artifact_slug}_source.md"
        notebooklm_path.write_text(
            build_source_markdown(entry, essay_body),
            encoding="utf-8",
        )

        media_entries.append(
            {
                "id": entry["id"],
                "slug": entry["slug"],
                "title_zh": entry["title_zh"],
                "title_en": entry["title_en"],
                "media_language_profile": MEDIA_LANGUAGE_PROFILE,
                "primary_theorem": entry["primary_theorem"],
                "support_theorems": entry.get("support_theorems", []),
                "works": entry.get("works", []),
                "work_links": {name: WORK_LINKS[name] for name in entry.get("works", []) if name in WORK_LINKS},
                "paper_refs": entry.get("paper_refs", []),
                "status": entry.get("status", "published"),
                "source_markdown": entry["file"],
                "notebooklm_source": str(notebooklm_path.relative_to(ROOT)),
                "artifact_slug": artifact_slug,
                "expected_artifacts": {
                    "slides": f"workspace/artifacts/{artifact_slug}/{artifact_slug}_slides.pdf",
                    "infographic": f"workspace/artifacts/{artifact_slug}/{artifact_slug}_infographic.png",
                    "audio": f"workspace/artifacts/{artifact_slug}/{artifact_slug}_audio.wav",
                    "video": f"workspace/artifacts/{artifact_slug}/{artifact_slug}_video.mp4",
                },
            }
        )

    media_registry = {
        "series": registry["series"],
        "generated_at": registry["generated_at"],
        "language_policy": registry["language_policy"],
        "media_language_policy": MEDIA_LANGUAGE_PROFILE,
        "release_pack": "cross-text synthesis media pack",
        "entries": media_entries,
    }
    MEDIA_REGISTRY_PATH.write_text(
        json.dumps(media_registry, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {MEDIA_REGISTRY_PATH}")
    print(f"Wrote {len(media_entries)} NotebookLM source packs to {NOTEBOOKLM_DIR}")


if __name__ == "__main__":
    main()
