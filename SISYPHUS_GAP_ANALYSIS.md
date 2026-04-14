# Sisyphus Math Vertical — Agent Workflow Design (2026-04-14)

> From the perspective of Lexa (Automath lead, first real user of the math vertical).
> Framed as AI agent collaboration, not traditional software features.

## System Context

```
Automath Oracle                         Sisyphus Agent Workflow
  │                                       │
  │ lake build pass → theorem verified     │
  │ ↓                                      │
  │ export_discovery_report.py             │
  │ ↓                                      │
  │ discovery_report.json (ADR-008) ─────→ WorkflowGAgent triggers
  │                                        ↓
  │                                      RoleGAgent: Ingester
  │                                        ↓
  │                                      RoleGAgent: Classifier
  │                                        ↓
  │                                      MAKER consensus vote
  │                                        ↓
  │                                      KG write (validated discovery)
  │                                        ↓
  │                                      RoleGAgent: Structure Analyzer
  │                                        ↓
  │                                      RoleGAgent: Direction Advisor
  │                                        ↓
  │ ←──────────────────────────────────── direction_hint.json (advisory)
  │
  │ (Oracle may follow or ignore hint)
```

## Agent Definitions

### Agent 1: Discovery Ingester (RoleGAgent)

**Trigger:** New `discovery_report.json` arrives (event from Automath or manual upload).

**Input:** ADR-008 JSON entry:
```json
{
  "discovery_id": "AUT-2026-0042",
  "lean_module": "Folding",
  "lean_theorem": "theorem fold_is_idempotent (m : Nat) (w : X m) : Fold (Fold w) = Fold w",
  "lean_proof": "by simp [Fold, ...(proof body)...]",
  "exploration_context": "from fibonacci_cardinality via Fold definition",
  "is_novel": true,
  "git_commit": "42ea45e8"
}
```

**Responsibilities:**
1. Validate JSON against ADR-008 schema (reject malformed)
2. Check `is_novel` — if false, log and skip
3. Check dedup against existing KG nodes by `lean_theorem` declaration hash
4. Extract metadata from `lean_theorem`: theorem name, parameter types, return type
5. Parse `lean_module` → map to one of 11 known Omega modules
6. Parse `exploration_context` → resolve references to existing KG theorem nodes

**Output:** `validated_discovery` event → forwarded to Classifier

**Error cases:**
- Unknown `lean_module` → flag for manual review, don't auto-classify
- `exploration_context` references a discovery not yet in KG → ingest anyway, mark edge as "pending resolution"
- Duplicate detection → log, don't re-ingest, emit "duplicate_detected" event

### Agent 2: Classifier (RoleGAgent)

**Trigger:** `validated_discovery` event from Ingester.

**Input:** Parsed theorem metadata + `lean_module` + `exploration_context` edges.

**Responsibilities:**
1. Propose primary classification: which Omega direction does this theorem belong to? (golden-mean-shift, fibonacci-growth, fold-operator, zeckendorf, modular-tower, spectral-theory, rate-distortion, ring-arithmetic, dynamical-systems, fiber-scan)
2. Propose secondary classifications (a theorem can touch multiple directions)
3. Propose dependency edges to existing KG nodes

**Output:** `classification_proposal` → forwarded to MAKER consensus

**Classification heuristics (Lexa defines, agents execute):**
- Module `Folding` → primary direction `fold-operator`
- Module `Frontier.ConditionalArithmetic` → primary `fibonacci-growth` or `modular-tower`
- Module `Graph.TransferMatrix` → primary `spectral-theory`
- Module `SPG.ScanError` → primary `rate-distortion`
- Theorem name contains `zeckendorf` → add `zeckendorf` direction
- Theorem name contains `entropy` → add `dynamical-systems`

### Agent 3: MAKER Consensus (built-in Sisyphus mechanism)

**Trigger:** `classification_proposal` from Classifier.

**What gets voted on:**
1. "Is the primary direction correct?" (vote: agree / disagree / suggest alternative)
2. "Are the dependency edges correct?" (vote: agree / disagree / add missing edge)
3. "Is this theorem genuinely novel?" (vote: yes / this is a trivial corollary of theorem X)

**Consensus threshold:** Majority vote (configurable). If no consensus, flag for Lexa's manual review.

**Output:** `verified_classification` → KG write

### Agent 4: Structure Analyzer (RoleGAgent)

**Trigger:** Periodically (every N new KG entries) or on-demand.

**Input:** Full KG state.

**Responsibilities:**
1. Detect theorem clusters (groups of theorems with dense internal dependencies)
2. Identify structural similarity (two theorems with isomorphic dependency patterns)
3. Detect "frontier" theorems (theorems at the boundary of explored space — few outgoing edges)
4. Compute module statistics (discovery rate, density, staleness)

**Output:** `structural_insight` events → KG annotations + input to Direction Advisor

### Agent 5: Direction Advisor (RoleGAgent)

**Trigger:** New `structural_insight` or periodic (weekly).

**Input:** KG statistics + structural insights + recent discovery velocity.

**Responsibilities:**
1. Generate ADR-008 Flow 2 direction hints
2. Prioritize based on: under-explored modules, stale areas (no discoveries in 14+ days), identified generalizations

**Direction hint rules (Lexa defines):**
- Module with < 5 theorems and high structural connectivity to other modules → `explore_near` priority 8
- Module with > 50 theorems and declining discovery rate → `broaden` priority 5
- Two structurally similar theorems in different modules → `check_conjecture` (there may be a generalization) priority 9
- No new discoveries in any direction for 14 days → `deepen` the most recent active direction, priority 7

**Output:** `direction_hint.json` per ADR-008:
```json
{
  "hint_id": "SIS-2026-0007",
  "hint_type": "check_conjecture",
  "target_description": "fold_is_idempotent and stableZero_unique share identical dependency patterns — possible common generalization",
  "related_discoveries": ["AUT-2026-0042", "AUT-2026-0015"],
  "priority": 9
}
```

**Semantics:** Best-effort advisory. Automath Oracle can ignore.

## Workflow YAML (sketch)

```yaml
name: math_discovery_workflow
version: 1.0
trigger:
  event: discovery_report_received
  source: automath_oracle

steps:
  - name: ingest
    agent: DiscoveryIngesterRole
    input: $trigger.payload
    on_error: flag_for_manual_review

  - name: classify
    agent: ClassifierRole
    input: $ingest.validated_discovery
    depends_on: ingest

  - name: verify
    agent: MAKERConsensus
    input: $classify.classification_proposal
    depends_on: classify
    config:
      vote_threshold: majority
      timeout: 60s
      on_no_consensus: flag_for_manual_review

  - name: write_kg
    agent: KGWriter
    input: $verify.verified_classification
    depends_on: verify

  - name: analyze
    agent: StructureAnalyzerRole
    input: $write_kg.node_id
    depends_on: write_kg
    config:
      run_condition: every_10_ingestions

  - name: advise
    agent: DirectionAdvisorRole
    input: $analyze.structural_insights
    depends_on: analyze
    config:
      run_condition: weekly_or_on_insight
```

## KG Schema (per ADR-008 + extensions)

### Theorem Node

| Field | Source | Required |
|---|---|:---:|
| `discovery_id` | ADR-008 `AUT-YYYY-NNNN` | ✓ |
| `theorem_name` | Extracted from `lean_theorem` | ✓ |
| `lean_theorem` | Full declaration without proof body | ✓ |
| `lean_proof` | Full proof term | ✓ |
| `lean_module` | One of 11 Omega modules | ✓ |
| `primary_direction` | Classifier output, MAKER verified | ✓ |
| `secondary_directions` | Classifier output | optional |
| `exploration_context` | Free text from ADR-008 | ✓ |
| `discovery_timestamp` | From report or git commit date | ✓ |
| `discovery_order` | Global sequence number | ✓ |
| `git_commit` | Source commit hash | ✓ |

### Edge Types

| Edge | Meaning | Source |
|---|---|---|
| `depends_on` | Theorem A uses theorem B in its proof | `exploration_context` + Classifier |
| `same_module` | Both in the same Lean module | `lean_module` field |
| `same_direction` | Both classified to same Omega direction | Classifier + MAKER |
| `structurally_similar` | Isomorphic dependency patterns | Structure Analyzer |
| `generalizes` | Theorem A is a special case of B | Structure Analyzer |

## What Exists vs What's Needed

| Component | Sisyphus v2 Has | Math Vertical Needs | Gap |
|---|:---:|:---:|---|
| WorkflowGAgent engine | ✅ | ✅ | Wire up math workflow YAML |
| RoleGAgent framework | ✅ | ✅ | Define 4 math-specific roles |
| MAKER vote consensus | ✅ | ✅ | Define math voting criteria |
| KG read/write (via NyxID) | ⚠️ partial (v1→v2 migration) | ✅ | Complete migration + add schema |
| ADR-008 JSON ingestion | ❌ | ✅ | **Build Ingester agent** |
| Lean theorem metadata extraction | ❌ | ✅ | **Part of Ingester agent** (JSON parsing, not Lean parsing — Automath's exporter already produces structured JSON) |
| Direction hint generation | ❌ | ✅ | **Build Advisor agent** |
| Theorem deduplication | ❌ | ✅ | **Part of Ingester agent** (hash-based) |
| Structure analysis | ❌ | ✅ | **Build Analyzer agent** |

**Key clarification:** Sisyphus does NOT need a Lean 4 parser. Automath's `export_discovery_report.py` already produces structured JSON with all fields extracted. Sisyphus agents consume JSON, not `.lean` files.

## Sprint Plan (agent-oriented)

### Sprint 1: First Agent Closes the Loop (2 weeks)

**Goal:** Automath produces a report → Sisyphus ingests it → it's in the KG → queryable.

| Item | Description | Acceptance Criteria |
|---|---|---|
| Define KG schema | Theorem node + 5 edge types per above | Schema documented, KG accepts writes |
| Build Ingester RoleGAgent | ADR-008 JSON in → validate → dedup → write to KG | Feed 3,592 theorem JSON → all appear as nodes |
| Wire math workflow YAML | Trigger on discovery_report event → Ingester → KG write | End-to-end event flow works |
| Bulk import test | Import `discovery_report.json` (3,592 entries from Automath) | All 3,592 in KG, no duplicates, queryable by module |

### Sprint 2: Consensus + Classification (2 weeks)

**Goal:** MAKER votes on classifications, Structure Analyzer runs.

| Item | Description | Acceptance Criteria |
|---|---|---|
| Build Classifier RoleGAgent | Propose primary/secondary directions per heuristics | Classification matches Lexa's manual spot-check on 50 theorems |
| Wire MAKER consensus | Classifier proposal → multi-agent vote → verified classification | Vote results visible, no-consensus cases flagged |
| Build Structure Analyzer | Cluster detection + frontier identification | Can answer "which theorems are at the frontier of Folding module?" |

### Sprint 3: Close the Feedback Loop (2 weeks)

**Goal:** Sisyphus sends direction hints back to Automath.

| Item | Description | Acceptance Criteria |
|---|---|---|
| Build Direction Advisor | Generate ADR-008 Flow 2 hints from KG state | Produces valid `direction_hint.json` |
| Advisory output channel | Direction hints emitted as events, consumable by Automath | Oracle can poll or subscribe for hints |
| Lexa review dashboard | View recent discoveries, classifications, direction hints | Lexa can review and override agent decisions |

## What Lexa Provides

| Deliverable | Status | Timeline |
|---|---|---|
| `export_discovery_report.py` | ✅ Done (3,592 theorems) | Now |
| `discovery_report.json` test dataset | ✅ Ready to generate | On demand |
| Classification heuristics (module → direction mapping) | Defined above | Now |
| Direction hint rules | Defined above | Now |
| MAKER voting criteria | Defined above | Now |
| Weekly review of agent decisions | Ongoing | Sprint 2+ |

## ADR-008 Validation Criteria Cross-Check

| ADR-008 Validation Step | Covered by Sprint | Status |
|---|---|---|
| 1. Schema spike (CEO fills discovery report manually) | Pre-Sprint 1 | ✅ `export_discovery_report.py` does this automatically |
| 2. Shining confirms ingestion works | Sprint 1 | Build Ingester agent |
| 3. Direction hint generation confirmed | Sprint 3 | Build Advisor agent |

## Activation Trigger

Per `sisyphus.md`, INCUBATING → ACTIVE requires:
1. Discovery Registry MVP 跑通 (闭环 POC) → **Sprint 1 completion**
2. CEO 决定分配专职开发资源 → **Pending CEO decision after Sprint 1 demo**
