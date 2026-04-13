# Email Draft — Terence Tao

**Status:** DRAFT — Lexa to review and personalize before sending

**To:** tao@math.ucla.edu
**Subject:** Lean 4 formalization of golden-mean shift dynamics (10,588 theorems from x²=x+1)

---

Dear Professor Tao,

I lead the Automath project at Chrono AI, where we are building a formally verified mathematical discovery engine. Starting from a single constraint — x²=x+1 and the golden-mean shift it induces — we have produced 10,588 machine-verified theorems in Lean 4, covering symbolic dynamics, Fibonacci arithmetic, spectral theory, ergodic measures, and modular tower structures. Nine papers have been submitted to journals including ETDS, JTP, RAIRO-ITA, and SIAM JADS.

One result I think may interest you: we formalized a complete proof that the topological entropy of the golden-mean shift equals log φ (`topological_entropy_eq_log_phi` in our library). The proof chain goes through Fibonacci cardinality → ratio convergence → Cesàro average → entropy, entirely within Lean 4. The companion result `goldenMeanAdjacency_has_goldenRatio_eigenvector` establishes the Perron-Frobenius spectral underpinning. Both are verified end-to-end with no axioms beyond Mathlib's core.

We read your recent post on mathematical methods in the age of AI, and the SAIR Foundation's vision of formal verification as a "lie detector" for AI-assisted mathematics resonates strongly with our approach. Our library is a working example of exactly this paradigm — AI-driven discovery constrained by Lean 4 proof. We would welcome any perspective you might have on this work, and we would be glad to explore whether any of our formalized results or tooling could be useful to SAIR's mission.

Lean 4 repository: https://github.com/the-omega-institute/automath
Showcase site: https://the-omega-institute.github.io/Omega-paper-series/

Best regards,
Lexa
Chrono AI — Automath Project Lead

---

## Notes for Lexa

- **Personalize paragraph 1**: Add your actual title/name as you'd like it to appear.
- **Hook theorem**: `topological_entropy_eq_log_phi` chosen because (a) self-contained and recognizable to any dynamicist, (b) formally verified real analysis is exactly what SAIR champions, (c) pairs with spectral result for a "two-theorem pitch".
- **SAIR connection**: Tao co-founded SAIR Foundation (Feb 2026, UCLA). Their thesis = formal verification as "lie detector" for AI math. This is literally what you do. Frame it as alignment, not asking for help.
- **What NOT to include**: No videos, no cultural interpretations, no company pitch. Pure math + Lean 4. That's his language.
- **Length**: 3 paragraphs, ~200 words. Busy people read short emails.
- **Follow-up**: If no response in 2 weeks, one follow-up with a different specific theorem result.
