#!/usr/bin/env python3
"""Omega Ancient Texts Analysis Pipeline.

三阶段工作流:
  Stage 1 (Claude): 获取原文 → 分类 → 确定 Omega 映射方向
  Stage 2 (Codex):  每个方向迭代生成映射论文/故事
  Stage 3 (Claude): Review Codex 产出 → NotebookLM 视频

Usage:
    python pipeline.py 道德经                     # 全流程
    python pipeline.py 道德经 --stage classify     # 只跑 Stage 1 分类
    python pipeline.py 道德经 --stage generate     # 只跑 Stage 2 生成
    python pipeline.py 道德经 --stage review       # 只跑 Stage 3 审查
    python pipeline.py --list                      # 列出支持的作品
"""

import argparse
import json
import os
import subprocess
import sys
import textwrap
import time
from pathlib import Path

import yaml

from analysis.omega_bridge import OmegaBridge
from analysis.theorem_mapper import format_category_citations, select_candidates_for_category

AUTOMATH_ROOT = Path(__file__).parent.parent / "automath"
NOTEBOOKLM_DISPATCH = AUTOMATH_ROOT / "tools" / "notebooklm-oracle" / "notebooklm_dispatch.py"
WORK_DIR = Path(__file__).parent / "workspace"

KNOWN_WORKS = {
    "道德经": {"en": "Tao Te Ching", "author": "老子", "chapters": 81, "lang": "zh"},
    "易经": {"en": "I Ching", "author": "伏羲/文王/孔子", "chapters": 64, "lang": "zh"},
    "黄帝内经": {"en": "Huangdi Neijing", "author": "黄帝/岐伯", "chapters": 162, "lang": "zh"},
    "红楼梦": {"en": "Dream of the Red Chamber", "author": "曹雪芹", "chapters": 120, "lang": "zh"},
    "论语": {"en": "Analects", "author": "孔子", "chapters": 20, "lang": "zh"},
    "几何原本": {"en": "Euclid's Elements", "author": "Euclid", "chapters": 13, "lang": "en"},
    "孙子兵法": {"en": "The Art of War", "author": "孙武", "chapters": 13, "lang": "zh"},
}


def load_config(path: str = "config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def get_omega_context() -> str:
    """Load Omega theorem summary for LLM prompts."""
    candidate_paths = [
        AUTOMATH_ROOT / "discovery" / "discovery_report.json",
        AUTOMATH_ROOT / "tools" / "discovery-export" / "discovery" / "discovery_report.json",
    ]
    for discovery_path in candidate_paths:
        if discovery_path.exists():
            with open(discovery_path) as f:
                data = json.load(f)
            entries = data.get("entries", data.get("discoveries", []))
            return (
                f"Omega 定理库: {len(entries)} 条机器验证定理, "
                f"覆盖 Core/Folding/Zeta/SPG/GU/EA/Frontier 等模块"
            )
    return "Omega: 10,588+ 机器验证定理, 从 x²=x+1 推导, Lean 4 形式化"


# ============================================================
# Stage 1: Claude 分类 — 获取文本, 分析结构, 确定映射方向
# ============================================================

CLASSIFY_PROMPT = """\
你是 Omega 项目的研究助手。Omega 从一个方程 x²=x+1 出发，通过形式化验证推导出覆盖多个数学分支的定理体系。

{omega_context}

核心数学结构（可用于映射的方向）:
1. 黄金平均移位 (golden-mean shift) — 二进制约束, 不允许连续1
2. Fibonacci 增长 — 计数与递推
3. Zeckendorf 表示 — 唯一分解, 不连续 Fibonacci 求和
4. 折叠算子 (Fold operator) — 信息丢失, 分辨率层次
5. 环算术 (Ring arithmetic) — 模 Fibonacci 数的代数结构
6. 谱理论 (Spectral theory) — 碰撞核, Cayley-Hamilton
7. 模塔与逆极限 (Modular tower) — 层次化, 无限逼近
8. 动力系统 (Dynamical systems) — 熵, 不动点, 周期轨道
9. 率失真与信息论 (Rate-distortion) — 最优编码, 信息界

现在请分析《{work_name}》({work_en}, {author})。

任务:
1. 获取/回忆该作品的完整结构（{chapters} 章/卦/篇）
2. 将所有章节按主题分成 8-12 个类别（每类有清晰的主题标签）
3. 对每个类别, 判断它与上述 9 个 Omega 数学方向中的哪些有结构性对应
4. 输出 JSON 格式:

```json
{{
  "work": "{work_name}",
  "total_chapters": {chapters},
  "categories": [
    {{
      "id": 1,
      "name_zh": "类别中文名",
      "name_en": "Category English Name",
      "chapters": [1, 2, 3],
      "theme": "主题描述",
      "omega_directions": ["golden-mean-shift", "fold-operator"],
      "mapping_rationale": "为什么这个类别与这些数学方向对应"
    }}
  ]
}}
```

只输出 JSON, 不要其他内容。
"""


def stage1_classify(work_name: str, config: dict) -> dict:
    """Stage 1: Claude classifies the text and determines Omega mapping directions."""
    work = KNOWN_WORKS[work_name]
    work_dir = WORK_DIR / work_name
    work_dir.mkdir(parents=True, exist_ok=True)

    classify_file = work_dir / "classification.json"
    if classify_file.exists():
        print(f"[Stage 1] 已有分类结果: {classify_file}")
        with open(classify_file) as f:
            return json.load(f)

    omega_ctx = get_omega_context()
    prompt = CLASSIFY_PROMPT.format(
        omega_context=omega_ctx,
        work_name=work_name,
        work_en=work["en"],
        author=work["author"],
        chapters=work["chapters"],
    )

    prompt_file = work_dir / "classify_prompt.txt"
    prompt_file.write_text(prompt, encoding="utf-8")

    print(f"[Stage 1] 分类《{work_name}》— Claude 分析中...")
    print(f"  分类提示词已写入: {prompt_file}")
    print(f"  请在 Claude Code 中运行以下命令完成分类:")
    print(f"  读取 {prompt_file} 的内容, 按要求输出 JSON, 保存到 {classify_file}")
    print()
    print(f"  或者手动: claude -p \"$(cat {prompt_file})\" > {classify_file}")

    return {"status": "prompt_generated", "prompt_file": str(prompt_file), "output_file": str(classify_file)}


# ============================================================
# Stage 2: Codex 生成 — 每个方向迭代生成映射论文
# ============================================================

GENERATE_PROMPT_TEMPLATE = """\
IMPORTANT: Do NOT read or execute any files under ~/.claude/, ~/.agents/, .claude/skills/, or agents/. Stay focused on the task.

你是一位数学-文学跨学科研究者。请为以下主题撰写一篇完整的映射分析文章。

## 源文本
作品: 《{work_name}》({work_en})
类别: {category_name} (章节: {chapters})
主题: {theme}

## Omega 数学方向
映射方向: {omega_directions}
映射依据: {mapping_rationale}

## Omega 数学背景
{omega_context}

## 候选 Omega 定理
{omega_theorem_candidates}

## 输出要求
撰写一篇 2000-4000 字的**映射分析文章**。重点不是给读者做古籍导读，而是用古籍确认 Omega 数学结构的美与强度。

结构如下:

1. **结构入口** — 只用最少背景说明该类别的核心文本结构
2. **原文锚点** — 选取 3-5 段最能承载结构映射的原文, 附简洁翻译
3. **Omega 映射分析** — 这是全文核心:
   - 明确指出对应的 Omega 对象与具体定理
   - 优先给出 theorem-level mapping, 不要停留在方向级标签
   - 区分"形式对应"(可证明的结构同构/同型) 和"启发性类比"(有趣但非严格)
   - 说明为什么这个映射能体现 Omega 数学结构的美
4. **结构综合** — 总结该类别最终确认了 Omega 的哪些核心结构
5. **参考** — 原文出处 + Lean 定理名/模块名

额外约束:
- 文本解释要有, 但只能服务于映射, 不能喧宾夺主
- 不要写“对主论文的直接回流”“给我们写作的建议”之类面向内部的口吻
- 不要把文章写成古籍导论、文学赏析或论文写作 memo
- 尽量引用具体 Lean 定理名, 例如 `fibonacci_cardinality`, `fold_is_idempotent`, `inverse_limit_equiv`
- 若提供了候选定理, 优先使用其中最贴切的 2-6 条, 不要虚构 Lean 名称
- 若缺少精确定理, 才退回到模块/对象级映射

语言: 中英双语 (中文为主, 关键术语附英文)
风格: 严谨、凝练、映射优先, 面向有教育背景的非专业读者
"""


def stage2_generate(work_name: str, classification: dict, config: dict) -> list[dict]:
    """Stage 2: Codex generates mapping articles for each category."""
    work = KNOWN_WORKS[work_name]
    work_dir = WORK_DIR / work_name
    gen_dir = work_dir / "generated"
    gen_dir.mkdir(parents=True, exist_ok=True)

    omega_ctx = get_omega_context()
    categories = classification.get("categories", [])
    results = []
    theorem_bridge = None
    theorem_bridge_error = None

    try:
        theorem_bridge = OmegaBridge()
    except Exception as exc:
        theorem_bridge_error = str(exc)
        print(f"  [Stage 2] 定理库加载失败, 回退到方向级映射: {exc}")

    for cat in categories:
        cat_id = cat["id"]
        output_file = gen_dir / f"category_{cat_id:02d}_{cat['name_en'].replace(' ', '_').lower()}.md"

        if output_file.exists():
            print(f"  [Stage 2] 跳过 category {cat_id} — 已生成: {output_file.name}")
            results.append({"category": cat_id, "file": str(output_file), "status": "exists"})
            continue

        theorem_candidates = "暂未提供自动筛出的候选定理，请至少落到明确的 Omega 对象或模块。"
        theorem_mapping = None
        if theorem_bridge:
            theorem_mapping = select_candidates_for_category(theorem_bridge, cat)
            if theorem_mapping.get("theorem_candidates"):
                theorem_candidates = format_category_citations(theorem_mapping)
            theorem_file = gen_dir / f"theorem_candidates_{cat_id:02d}.json"
            theorem_file.write_text(
                json.dumps(theorem_mapping, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        prompt = GENERATE_PROMPT_TEMPLATE.format(
            work_name=work_name,
            work_en=work["en"],
            category_name=f"{cat['name_zh']} / {cat['name_en']}",
            chapters=", ".join(str(c) for c in cat["chapters"]),
            theme=cat["theme"],
            omega_directions=", ".join(cat["omega_directions"]),
            mapping_rationale=cat["mapping_rationale"],
            omega_context=omega_ctx,
            omega_theorem_candidates=theorem_candidates,
        )

        prompt_file = gen_dir / f"prompt_{cat_id:02d}.txt"
        prompt_file.write_text(prompt, encoding="utf-8")

        print(f"  [Stage 2] Category {cat_id}: {cat['name_zh']} — 调用 Codex...")

        # Call Codex to generate
        try:
            result = subprocess.run(
                ["codex", "exec", f"Read {prompt_file} and write the article to {output_file}. Follow the instructions exactly.",
                 "-C", str(Path(__file__).parent),
                 "-s", "read-write",
                 "-c", 'model_reasoning_effort="xhigh"'],
                capture_output=True, text=True, timeout=600,
            )
            if output_file.exists():
                print(f"    ✓ 生成完成: {output_file.name}")
                result_entry = {"category": cat_id, "file": str(output_file), "status": "generated"}
                if theorem_mapping:
                    result_entry["theorem_candidates"] = [
                        item["lean_theorem"] for item in theorem_mapping.get("theorem_candidates", [])
                    ]
                results.append(result_entry)
            else:
                print(f"    ✗ 生成失败, Codex stderr: {result.stderr[:200]}")
                results.append({"category": cat_id, "status": "failed", "error": result.stderr[:500]})
        except subprocess.TimeoutExpired:
            print(f"    ✗ Codex 超时 (10 min)")
            results.append({"category": cat_id, "status": "timeout"})
        except FileNotFoundError:
            print(f"    ✗ codex CLI 未安装")
            print(f"    提示词已保存: {prompt_file}")
            results.append({"category": cat_id, "prompt": str(prompt_file), "status": "codex_missing"})
            break

    # Save generation manifest
    manifest = {
        "work": work_name,
        "results": results,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    if theorem_bridge and theorem_bridge.discovery_path:
        manifest["discovery_path"] = str(theorem_bridge.discovery_path)
    if theorem_bridge_error:
        manifest["theorem_bridge_error"] = theorem_bridge_error
    (gen_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    return results


# ============================================================
# Stage 3: Claude Review — 审查 Codex 产出, 输出最终版本
# ============================================================

REVIEW_PROMPT_TEMPLATE = """\
你是 Omega 项目的质量审查员。请审查以下由 AI 生成的映射分析文章。

## 审查标准
1. **数学准确性** — 引用的 Omega 定理是否存在? 映射是否合理?
2. **区分形式/启发** — 是否清楚区分了"形式对应"和"启发性类比"?
3. **原文准确性** — 引用的古文是否准确? 翻译是否恰当?
4. **可读性** — 非专业读者能否理解?
5. **完整性** — 是否覆盖了该类别的核心内容?

## 待审查文章
{article_content}

## 输出
如果文章质量可接受 (≥7/10):
  输出 "ACCEPT" + 简短评语 + 修改建议

如果需要大幅修改 (< 7/10):
  输出 "REVISE" + 具体问题列表 + 修改要求

格式:
```
VERDICT: ACCEPT/REVISE
SCORE: X/10
COMMENTS: ...
SUGGESTIONS: ...
```
"""


def stage3_review(work_name: str, config: dict) -> list[dict]:
    """Stage 3: Claude reviews Codex-generated articles."""
    work_dir = WORK_DIR / work_name
    gen_dir = work_dir / "generated"
    review_dir = work_dir / "reviewed"
    review_dir.mkdir(parents=True, exist_ok=True)

    if not gen_dir.exists():
        print(f"[Stage 3] 没有生成内容: {gen_dir}")
        return []

    articles = sorted(gen_dir.glob("category_*.md"))
    results = []

    for article_path in articles:
        review_file = review_dir / f"review_{article_path.stem}.txt"

        if review_file.exists():
            print(f"  [Stage 3] 跳过 — 已审查: {review_file.name}")
            results.append({"file": str(article_path), "review": str(review_file), "status": "exists"})
            continue

        content = article_path.read_text(encoding="utf-8")
        prompt = REVIEW_PROMPT_TEMPLATE.format(article_content=content[:8000])

        prompt_file = review_dir / f"review_prompt_{article_path.stem}.txt"
        prompt_file.write_text(prompt, encoding="utf-8")

        print(f"  [Stage 3] 审查: {article_path.name}")
        print(f"    审查提示词: {prompt_file}")
        print(f"    请在 Claude Code 中审查, 输出保存到: {review_file}")

        results.append({"file": str(article_path), "prompt": str(prompt_file), "output": str(review_file), "status": "pending"})

    return results


# ============================================================
# Stage 4: NotebookLM — 生成多媒体
# ============================================================

def stage4_notebooklm(work_name: str, config: dict) -> list[dict]:
    """Stage 4: Feed reviewed articles to NotebookLM for video generation."""
    work_dir = WORK_DIR / work_name
    reviewed_dir = work_dir / "reviewed"
    gen_dir = work_dir / "generated"

    if not NOTEBOOKLM_DISPATCH.exists():
        print(f"[Stage 4] NotebookLM dispatch 不存在: {NOTEBOOKLM_DISPATCH}")
        return []

    # Find accepted articles
    articles = sorted(gen_dir.glob("category_*.md"))
    results = []

    for article in articles:
        review_file = reviewed_dir / f"review_{article.stem}.txt"
        if review_file.exists():
            review_content = review_file.read_text()
            if "ACCEPT" not in review_content:
                print(f"  [Stage 4] 跳过 (未通过审查): {article.name}")
                continue

        print(f"  [Stage 4] NotebookLM: {article.name}")
        try:
            result = subprocess.run(
                ["python3", str(NOTEBOOKLM_DISPATCH), "--paper", str(article.parent)],
                capture_output=True, text=True, timeout=300,
            )
            results.append({"file": str(article), "status": "dispatched"})
        except Exception as e:
            results.append({"file": str(article), "status": "error", "error": str(e)})

    return results


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Omega 古典著作分析管线: 三阶段工作流",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
        三阶段工作流:
          Stage 1 (classify):  Claude 分类文本, 确定 Omega 映射方向
          Stage 2 (generate):  Codex 迭代生成映射论文
          Stage 3 (review):    Claude 审查 Codex 产出
          Stage 4 (media):     NotebookLM 生成视频

        Examples:
          python pipeline.py 道德经                  # 全流程
          python pipeline.py 道德经 --stage classify  # 只分类
          python pipeline.py 易经 --stage generate    # 只生成
        """),
    )
    parser.add_argument("work", nargs="?", help="作品名（如：道德经、易经）")
    parser.add_argument("--stage", choices=["classify", "generate", "review", "media", "all"], default="all")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)

    if args.list:
        print("支持的经典著作:\n")
        for name, info in KNOWN_WORKS.items():
            print(f"  {name:8s}  {info['en']:35s}  {info['chapters']:>3d} 章  {info['author']}")
        return

    if not args.work:
        parser.print_help()
        return

    if args.work not in KNOWN_WORKS:
        print(f"未知作品: {args.work}")
        print(f"支持: {', '.join(KNOWN_WORKS.keys())}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"Omega 古典著作分析管线")
    print(f"作品: {args.work} ({KNOWN_WORKS[args.work]['en']})")
    print(f"阶段: {args.stage}")
    print(f"{'='*60}\n")

    # Stage 1
    if args.stage in ("classify", "all"):
        print("[Stage 1] 文本分类与 Omega 映射方向确定")
        classification = stage1_classify(args.work, config)

        if classification.get("status") == "prompt_generated":
            print("\n  → 分类提示词已生成, 请手动运行 Claude 完成分类")
            if args.stage == "all":
                print("  → 分类完成后重新运行 pipeline.py 继续")
                return
        else:
            print(f"  → 分类完成: {len(classification.get('categories', []))} 个类别")

    # Stage 2
    if args.stage in ("generate", "all"):
        print("\n[Stage 2] Codex 迭代生成映射论文")
        classify_file = WORK_DIR / args.work / "classification.json"
        if not classify_file.exists():
            print(f"  → 请先运行 Stage 1: python pipeline.py {args.work} --stage classify")
            return
        with open(classify_file) as f:
            classification = json.load(f)
        results = stage2_generate(args.work, classification, config)
        generated = sum(1 for r in results if r["status"] in ("generated", "exists"))
        print(f"\n  → 生成完成: {generated}/{len(results)}")

    # Stage 3
    if args.stage in ("review", "all"):
        print("\n[Stage 3] Claude 审查 Codex 产出")
        results = stage3_review(args.work, config)
        print(f"  → {len(results)} 篇待审查")

    # Stage 4
    if args.stage in ("media", "all"):
        print("\n[Stage 4] NotebookLM 多媒体生成")
        results = stage4_notebooklm(args.work, config)
        print(f"  → {len(results)} 篇已提交")

    print(f"\n{'='*60}")
    print(f"完成。工作目录: {WORK_DIR / args.work}")


if __name__ == "__main__":
    main()
