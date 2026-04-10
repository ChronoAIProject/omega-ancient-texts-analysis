# Codex Next Priorities

Current state (2026-04-10):
- 5 classical texts (道德经 12 + 易经 12 + 黄帝内经 12 + 孙子兵法 10 + 几何原本 8) = **54 category essays**, all complete, all clean (no backflow content)
- **道德经 81 chapter dossiers** in `Omega-paper-series/cultural/tao-te-ching/chapters/`
- **易经 64 hexagram dossiers** in `Omega-paper-series/cultural/i-ching/hexagrams/`
- **21 GMS-valid hexagrams** singled out in `Omega-paper-series/cultural/i-ching/gms-valid/`
- **190 files with theorem-level Lean 4 anchors**
- MemPalace indexed with 10,000 drawers (automath + all content)
- 6 master NotebookLM videos generated and published

## Highest-ROI Next Work

### P0: Cross-Text Synthesis Essays (10 articles)

Write 10 long-form essays, each tracing ONE Omega theorem across all 5 texts + Gen 2 papers.
These become the flagship thought-leadership content — nothing else like this exists.

Each essay should:
- Be 3500-5000 words, bilingual (zh primary for cultural angle, en for rigor)
- Cite exact Lean 4 theorem names (use MemPalace search: `mempalace search "theorem name"`)
- Include passages from at least 3 of the 5 classical texts
- Reference at least 1 Gen 2 paper
- Distinguish formal correspondence from metaphorical analogy
- Save to `workspace/synthesis/` as `synthesis_NN_topic.md`

**The 10 topics:**

| # | Topic | Texts to cover | Key Lean anchors |
|---|-------|---------------|------------------|
| 1 | Golden-mean shift (No11) | 道德经"知足" + 易经 21 GMS-valid + 孙子"守则不胜" + 黄帝"中庸" + 几何原本约束构造 | `X_m`, `No11`, `fibonacci_cardinality` |
| 2 | Fibonacci growth F_{m+2} | 道德经"道生一一生二" + 易经卦系递推 + 几何原本比例论 | `fibonacci_cardinality_recurrence`, `goldenMean_characteristic_recurrence` |
| 3 | Fold operator | 道德经"将欲弱之必固强之" + 易经乾→既济 + 孙子"奇正相生" + 黄帝邪气传变 | `Fold`, `fold_idempotent`, `Fold : Word m → X_m` |
| 4 | Zeckendorf unique decomposition | 道德经"朴" + 孙子"全胜" + 几何原本素因子分解 + 易经本位分解 | `zeckendorf_unique`, `zeckendorf_representation` |
| 5 | Modular tower / inverse limit | 道德经"道不可道" + 易经层级 + 几何原本穷竭法 + 黄帝多尺度 | `inverse_limit_extensionality`, `inverse_limit_bijective`, `XInfinity` |
| 6 | Spectral theory | 易经变易动力学 + 孙子兵势 + 黄帝脉象 + Gen 2 spectral papers | `goldenMeanAdjacency_has_goldenRatio_eigenvector`, `topological_entropy_eq_log_phi` |
| 7 | Rate-distortion | 道德经"少则得" + 孙子"不战而屈" + 黄帝"未病之治" + 几何原本公设最小性 | `rate_distortion`, `optimal_code` (search MemPalace) |
| 8 | Ring arithmetic | 易经卦变代数 + 黄帝藏象相生相克 + 几何原本面积演算 | `X_m ≅ Z/F_{m+2}Z`, ring structure theorems |
| 9 | Dynamical systems | 易经循环 + 黄帝四时 + 孙子势动 + 道德经反向 | `restrict`, `shift`, `periodic_orbit` |
| 10 | Fiber / scan (information & observation) | 道德经"视之不见" + 易经象数观测 + 黄帝脉诊 + 孙子"知彼" | `fiber`, `d(x)`, scan projection theorems |

**Workflow for each essay:**
1. Search MemPalace for all relevant theorems: `mempalace search "<topic>" --wing omega`
2. Search classical text sources: grep or mempalace search in each work
3. Write the essay with direct quotes from texts and exact Lean 4 theorem names
4. Save to `workspace/synthesis/synthesis_NN_<slug>.md`
5. No "backflow" / "advice to papers" sections — stay on the mapping

### P1: Per-章 dossiers for remaining texts

Currently only 道德经 (81) and 易经 (64) have per-unit dossiers. Add:
- **孙子兵法 13 篇** → `Omega-paper-series/cultural/sunzi/chapters/chapter-NN.md`
- **几何原本 13 books** → `Omega-paper-series/cultural/euclid/books/book-NN.md`
- **黄帝内经** — too many chapters (162), pick 30 most-cited instead, save to `cultural/huangdi-neijing/selections/`

Each dossier follows the same 6-section structure as existing hexagram dossiers:
结构签名 / 映射定位 / Omega 对象 / Omega 定理锚点 / 语料状态 / 小结

### P2: Theorem → interpretations reverse index

For each of the top 50 most-cited Omega theorems, build a reverse index:
`workspace/theorem_index/<theorem_name>.md` listing every cultural dossier that cites it.

This makes the knowledge base navigable from the math side: "show me every cultural interpretation that uses `fibonacci_cardinality`."

Can be auto-generated from existing dossier front matter by a script, but having Codex write the narrative commentary ("why this theorem shows up across these specific texts") is where the value is.

### P3: Paper deep-read companions

For each of 9 Gen 2 papers, write a 2000-word "reader's companion":
- Plain-language introduction to the problem
- Key theorem statements (from paper)
- One classical text analogy (for motivation only, not rigor)
- "Why this matters"

Save to `Omega-paper-series/science/gen2/companion/<paper-slug>.md`.

---

**Most important:** Start with P0 synthesis essays. That's the unique work only this research program can produce.
