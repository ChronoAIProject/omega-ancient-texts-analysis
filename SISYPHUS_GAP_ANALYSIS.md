# Sisyphus Gap Analysis — Math Vertical (2026-04-14)

> Based on code review of aevatarAI/aevatar feature/sisyphus-v2 + ADR-008 interface contract + Automath project requirements.

## Current State (what Sisyphus v2 has)

From Codex code review of `feature/sisyphus-v2`:

| Capability | Evidence | Maturity |
|---|---|---|
| Generic workflow engine | WorkflowGAgent + YAML-based declarative workflows on Aevatar | Working |
| MAKER vote consensus | RoleGAgent-based multi-agent verification loop | Working |
| Knowledge graph read/write | Via NyxID MCP integration | Partial (v1 had this, v2 migration incomplete) |
| Research loop | research → verification → KG write → deeper research | Architecture exists, domain-specific logic TBD |
| Paper export PDF | v1 had this capability | Needs migration to v2 |
| Frontend graph visualization | v1 had this | Needs migration to v2 |
| CI/CD + 12 unit tests | v1 | Needs migration |

**Key observation:** Sisyphus v2 is a **generic automated reasoning platform**. It has the workflow engine and consensus mechanism but **zero math-domain-specific logic**. It doesn't know what a theorem is, what Lean 4 is, or what a discovery report looks like.

## Ideal State (what a math researcher needs)

Based on Lexa's role as Automath lead (10,588 Lean 4 theorems, discovery-first model per ADR-008):

### Discovery Ingestion
- Accept ADR-008 `discovery_report.json` as input
- Auto-parse `lean_module` field to classify by Omega module (Core, Folding, Frontier, Graph, SPG, etc.)
- Auto-detect theorem dependencies from `exploration_context`
- Reject duplicates (`is_novel` check against existing KG entries)

### Knowledge Graph Queries
- "Show all theorems in the Folding module discovered this week"
- "Which theorems depend on `fibonacci_cardinality`?" (reverse dependency)
- "What's the discovery rate by module over the last 30 days?"
- "Find theorems that touch both spectral-theory and ring-arithmetic"

### Direction Suggestions (advisory, per ADR-008 Flow 2)
- "Module X has 50 theorems, Module Y has 3 — consider exploring Y"
- "Theorem A and B are structurally similar — there may be a generalization"
- "No new discoveries in direction Z for 14 days — stale area?"

### Visualization
- Theorem dependency graph (directed, colored by module)
- Discovery timeline (when was each theorem found, grouped by module)
- Module heat map (density of discoveries by direction)
- "Frontier view" (theorems at the boundary of explored space)

### Export
- Discovery report JSON per ADR-008 (Automath → Sisyphus)
- Direction hint JSON per ADR-008 (Sisyphus → Automath)
- Paper-ready theorem list (filtered by topic, formatted for LaTeX inclusion)

## Gap Table

| Feature | Sisyphus Has | Math Vertical Needs | Priority | Notes |
|---|:---:|:---:|:---:|---|
| ADR-008 discovery report ingestion | ❌ | ✅ | **P0** | Without this, Sisyphus can't consume Automath output |
| Lean 4 theorem parsing | ❌ | ✅ | **P0** | Need to understand theorem declarations, module structure, dependencies |
| Theorem deduplication | ❌ | ✅ | **P0** | 10,588 existing theorems must not be re-entered as "new" |
| KG schema for math objects | ❌ | ✅ | **P0** | Nodes = theorems, edges = dependencies + module membership |
| Module-based classification | ❌ | ✅ | **P1** | Auto-tag theorems by Omega module (11 modules) |
| Reverse dependency query | ❌ | ✅ | **P1** | "What theorems use fibonacci_cardinality?" |
| Direction hint generation | ❌ | ✅ | **P1** | Per ADR-008 Flow 2 |
| Discovery timeline view | ❌ | ✅ | **P1** | When was each theorem discovered? |
| Theorem dependency graph viz | ❌ (v1 had generic graph viz) | ✅ | **P2** | Needs math-aware layout |
| Module heat map | ❌ | ✅ | **P2** | Density by direction |
| Paper-ready export | ❌ (v1 had PDF export) | ✅ | **P2** | Filtered theorem lists for LaTeX |
| Direction suggestion AI | ❌ | ✅ | **P2** | "Explore this area" advisory |
| Generic workflow engine | ✅ | ✅ | — | Already working |
| MAKER consensus | ✅ | ✅ | — | Already working |
| NyxID MCP integration | ✅ (partial) | ✅ | — | v1→v2 migration needed |

## Recommended Next Steps for Shining

**Sprint 1 (unblock math vertical):**
1. Implement ADR-008 discovery report ingestion endpoint
2. Define KG schema: theorem nodes (id, module, declaration, dependencies, timestamp) + edges (depends_on, same_module, generalization_of)
3. Bulk import existing 10,588 theorems from Automath's `export_discovery_report.py` output

**Sprint 2 (make it useful):**
4. Module-based filtering and reverse dependency queries
5. Discovery timeline view
6. Direction hint generation (rule-based first, AI later)

**Sprint 3 (make it impressive):**
7. Theorem dependency graph visualization
8. Module heat map
9. Paper-ready export

## What Lexa Will Provide

- `export_discovery_report.py` (ADR-008 compliant JSON from Automath) — being built now
- Test dataset: 10,588 theorem entries for bulk import testing
- Validation: Lexa will be the first real user of the math vertical
- Feedback loop: weekly gap review as features ship

## Activation Trigger (per sisyphus.md)

This gap analysis, once reviewed and accepted by Shining + CEO, satisfies condition 1 of the INCUBATING → ACTIVE upgrade: "Discovery Registry MVP 跑通 (闭环 POC)". The POC is: Automath produces a discovery report → Sisyphus ingests it → Sisyphus stores in KG → Sisyphus can answer "what theorems use X?" → Done.
