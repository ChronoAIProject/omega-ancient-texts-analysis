# 易经 Omega Theorem Pilot

This file is generated from `discovery_report.json` and the work classification metadata.

## 01. 创生与纯态 / Primal Creation and Pure States

Omega directions: golden-mean-shift, fibonacci-growth, modular-tower-inverse-limit

### golden-mean-shift

- `fibonacci_cardinality` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality (m : Nat) :
    Fintype.card (X m) = Nat.fib (m + 2)
- `fibonacci_cardinality_recurrence` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)
- `goldenMean_characteristic_recurrence` [Omega.Graph.Sofic] — theorem goldenMean_characteristic_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

### fibonacci-growth

- `fibonacci_cardinality` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality (m : Nat) :
    Fintype.card (X m) = Nat.fib (m + 2)
- `fibonacci_cardinality_recurrence` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)
- `goldenMean_characteristic_recurrence` [Omega.Graph.Sofic] — theorem goldenMean_characteristic_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

### modular-tower-inverse-limit

- `inverse_limit_extensionality` [Omega.Frontier.ConditionalArithmetic] — theorem inverse_limit_extensionality (a b : X.XInfinity) :
    a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m
- `inverse_limit_bijective` [Omega.Frontier.ConditionalSummary] — theorem inverse_limit_bijective :
    Function.Bijective (X.ofFamily : X.CompatibleFamily → X.XInfinity)
- `inverse_limit_left` [Omega.Frontier.ConditionalArithmetic] — theorem inverse_limit_left (F : X.CompatibleFamily) :
    X.toFamily (X.ofFamily F) = F

## 02. 动态变易与循环 / Dynamic Change and Cyclic Completion

Omega directions: dynamical-systems, golden-mean-shift, fold-operator

### dynamical-systems

- `topological_entropy_eq_log_phi` [Omega.Folding.Entropy] — theorem topological_entropy_eq_log_phi :
    Tendsto (fun n => Real.log (Nat.fib (n + 2) : ℝ) / (n : ℝ)) atTop (𝓝 (Real.log φ))
- `goldenMeanAdjacency_has_goldenRatio_eigenvector` [Omega.Graph.TransferMatrix] — theorem goldenMeanAdjacency_has_goldenRatio_eigenvector :
    ∃ v : Fin 2 → ℝ, v ≠ 0 ∧
      Matrix.mulVec goldenMeanAdjacencyℝ v = fun i => Real.goldenRatio * v i
- `goldenMean_characteristic_recurrence` [Omega.Graph.Sofic] — theorem goldenMean_characteristic_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

### golden-mean-shift

- `fibonacci_cardinality` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality (m : Nat) :
    Fintype.card (X m) = Nat.fib (m + 2)
- `fibonacci_cardinality_recurrence` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)
- `goldenMean_characteristic_recurrence` [Omega.Graph.Sofic] — theorem goldenMean_characteristic_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

### fold-operator

- `fold_is_idempotent` [Omega.Frontier.ConditionalArithmetic] — theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w
- `fold_fixes_stable` [Omega.Frontier.ConditionalArithmetic] — theorem fold_fixes_stable (x : X m) : Fold x.1 = x
- `fold_is_surjective` [Omega.Frontier.ConditionalArithmetic] — theorem fold_is_surjective : Function.Surjective (Fold (m

## 03. 困阻与险难 / Obstruction, Danger, and the Abysmal

Omega directions: golden-mean-shift, fold-operator, fiber-structure

### golden-mean-shift

- `fibonacci_cardinality` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality (m : Nat) :
    Fintype.card (X m) = Nat.fib (m + 2)
- `fibonacci_cardinality_recurrence` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)
- `goldenMean_characteristic_recurrence` [Omega.Graph.Sofic] — theorem goldenMean_characteristic_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

### fold-operator

- `fold_is_idempotent` [Omega.Frontier.ConditionalArithmetic] — theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w
- `fold_fixes_stable` [Omega.Frontier.ConditionalArithmetic] — theorem fold_fixes_stable (x : X m) : Fold x.1 = x
- `fold_is_surjective` [Omega.Frontier.ConditionalArithmetic] — theorem fold_is_surjective : Function.Surjective (Fold (m

### fiber-structure

- `maxFiberMultiplicity_bounds` [Omega.Combinatorics.FibonacciCube] — theorem maxFiberMultiplicity_bounds (m : Nat) :
    m / 2 + 1 ≤ X.maxFiberMultiplicity m ∧
    X.maxFiberMultiplicity m ≤ Nat.fib (m + 2)
- `maxFiberMultiplicity_eight` [Omega.Folding.MaxFiberHigh] — theorem maxFiberMultiplicity_eight : maxFiberMultiplicity 8 = 8
- `maxFiberMultiplicity_nine` [Omega.Folding.MaxFiberHigh] — theorem maxFiberMultiplicity_nine : maxFiberMultiplicity 9 = 10

## 04. 止静与内省 / Stillness, Restraint, and Inner Contemplation

Omega directions: golden-mean-shift, zeckendorf-representation, rate-distortion-information-theory

### golden-mean-shift

- `fibonacci_cardinality` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality (m : Nat) :
    Fintype.card (X m) = Nat.fib (m + 2)
- `fibonacci_cardinality_recurrence` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)
- `goldenMean_characteristic_recurrence` [Omega.Graph.Sofic] — theorem goldenMean_characteristic_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

### zeckendorf-representation

- `zeckendorf_uniqueness` [Omega.Frontier.ConditionalArithmetic] — theorem zeckendorf_uniqueness {x y : X m} (h : X.zeckIndices x = X.zeckIndices y) : x = y
- `zeckendorf_injective` [Omega.Frontier.ConditionalArithmetic] — theorem zeckendorf_injective (m : Nat) : Function.Injective (X.zeckIndices (m
- `paper_zeckendorf_primes_no_short_forbidden` [Omega.Folding.CollisionZetaOperator] — theorem paper_zeckendorf_primes_no_short_forbidden :
    Nat.Prime 2 ∧ Nat.Prime 3 ∧ Nat.Prime 7 ∧ True

### rate-distortion-information-theory

- `observation_refinement_reduces_error` [Omega.Frontier.ConditionalArithmetic] — theorem observation_refinement_reduces_error
    {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (μ : PMF α) (obs₁ : α → β) (obs₂ : α → γ) (f : γ → β)
    (hRef : ∀ x, obs₁ x = f (obs₂ x)) (P : Set α) :
    SPG.s
- `prefix_resolution_decreases_error` [Omega.Frontier.ConditionalArithmetic] — theorem prefix_resolution_decreases_error {m₁ m₂ n : Nat}
    (μ : PMF (Word n)) (h₁ : m₁ ≤ n) (h₂ : m₂ ≤ n) (hm : m₁ ≤ m₂)
    (P : Set (Word n)) :
    SPG.prefixScanError μ h₂ P ≤ SPG.prefixScanError μ h₁ P
- `scanError_hasCertificate` [Omega.Frontier.Conditional] — theorem scanError_hasCertificate {α β : Type*} [Fintype α] [Fintype β]
    (μ : PMF α) (obs : α → β) (P : Set α) :
    ScanErrorCertificate.Valid
      ({ μ

## 05. 刚健与突破 / Strength, Power, and Forceful Advance

Omega directions: fold-operator, fiber-structure, golden-mean-shift

### fold-operator

- `fold_is_idempotent` [Omega.Frontier.ConditionalArithmetic] — theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w
- `fold_fixes_stable` [Omega.Frontier.ConditionalArithmetic] — theorem fold_fixes_stable (x : X m) : Fold x.1 = x
- `fold_is_surjective` [Omega.Frontier.ConditionalArithmetic] — theorem fold_is_surjective : Function.Surjective (Fold (m

### fiber-structure

- `maxFiberMultiplicity_bounds` [Omega.Combinatorics.FibonacciCube] — theorem maxFiberMultiplicity_bounds (m : Nat) :
    m / 2 + 1 ≤ X.maxFiberMultiplicity m ∧
    X.maxFiberMultiplicity m ≤ Nat.fib (m + 2)
- `maxFiberMultiplicity_eight` [Omega.Folding.MaxFiberHigh] — theorem maxFiberMultiplicity_eight : maxFiberMultiplicity 8 = 8
- `maxFiberMultiplicity_nine` [Omega.Folding.MaxFiberHigh] — theorem maxFiberMultiplicity_nine : maxFiberMultiplicity 9 = 10

### golden-mean-shift

- `fibonacci_cardinality` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality (m : Nat) :
    Fintype.card (X m) = Nat.fib (m + 2)
- `fibonacci_cardinality_recurrence` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)
- `goldenMean_characteristic_recurrence` [Omega.Graph.Sofic] — theorem goldenMean_characteristic_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

## 06. 柔顺与养育 / Receptivity, Nourishment, and Gentle Cultivation

Omega directions: golden-mean-shift, fibonacci-growth, zeckendorf-representation

### golden-mean-shift

- `fibonacci_cardinality` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality (m : Nat) :
    Fintype.card (X m) = Nat.fib (m + 2)
- `fibonacci_cardinality_recurrence` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)
- `goldenMean_characteristic_recurrence` [Omega.Graph.Sofic] — theorem goldenMean_characteristic_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

### fibonacci-growth

- `fibonacci_cardinality` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality (m : Nat) :
    Fintype.card (X m) = Nat.fib (m + 2)
- `fibonacci_cardinality_recurrence` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)
- `goldenMean_characteristic_recurrence` [Omega.Graph.Sofic] — theorem goldenMean_characteristic_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

### zeckendorf-representation

- `zeckendorf_uniqueness` [Omega.Frontier.ConditionalArithmetic] — theorem zeckendorf_uniqueness {x y : X m} (h : X.zeckIndices x = X.zeckIndices y) : x = y
- `zeckendorf_injective` [Omega.Frontier.ConditionalArithmetic] — theorem zeckendorf_injective (m : Nat) : Function.Injective (X.zeckIndices (m
- `stable_language_exponentially_sparse` [Omega.Folding.CollisionZetaOperator] — theorem stable_language_exponentially_sparse (m : Nat) (hm : 2 ≤ m) :
    Nat.fib (m + 2) < 2 ^ m

## 07. 交感与关系 / Mutual Influence, Union, and Relationship

Omega directions: ring-arithmetic, spectral-theory, fold-operator

### ring-arithmetic

- `stableValue_ring_isomorphism` [Omega.Frontier.ConditionalArithmetic] — theorem stableValue_ring_isomorphism (m : Nat) :
    (∀ x y : X m, stableValue (X.stableAdd x y) =
      (stableValue x + stableValue y) % Nat.fib (m + 2)) ∧
    (∀ x y : X m, stableValue (X.stableMul x y) =
      (stabl
- `modular_projection_add_no_carry` [Omega.Frontier.ConditionalArithmetic] — theorem modular_projection_add_no_carry (x y : X (m + 1))
    (h : stableValue x + stableValue y < Nat.fib (m + 3)) :
    X.modularProject (X.stableAdd x y) =
      X.stableAdd (X.modularProject x) (X.modularProject y)
- `stableAdd_comm` [Omega.Folding.FiberArithmetic] — theorem stableAdd_comm (x y : X m) :
    stableAdd x y = stableAdd y x

### spectral-theory

- `goldenMeanAdjacency_has_goldenRatio_eigenvector` [Omega.Graph.TransferMatrix] — theorem goldenMeanAdjacency_has_goldenRatio_eigenvector :
    ∃ v : Fin 2 → ℝ, v ≠ 0 ∧
      Matrix.mulVec goldenMeanAdjacencyℝ v = fun i => Real.goldenRatio * v i
- `eigenvalue_eq_goldenRatio_or_goldenConj` [Omega.Graph.TransferMatrix] — theorem eigenvalue_eq_goldenRatio_or_goldenConj
    {μ : ℝ} (hμ : μ ^ 2 = μ + 1) :
    μ = Real.goldenRatio ∨ μ = Real.goldenConj
- `characteristic_polynomial_witness` [Omega.Frontier.ConditionalArithmetic] — theorem characteristic_polynomial_witness (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

### fold-operator

- `fold_is_idempotent` [Omega.Frontier.ConditionalArithmetic] — theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w
- `fold_fixes_stable` [Omega.Frontier.ConditionalArithmetic] — theorem fold_fixes_stable (x : X m) : Fold x.1 = x
- `fold_is_surjective` [Omega.Frontier.ConditionalArithmetic] — theorem fold_is_surjective : Function.Surjective (Fold (m

## 08. 变革与重构 / Revolution, Transformation, and Structural Renewal

Omega directions: fold-operator, fiber-structure, dynamical-systems

### fold-operator

- `fold_is_idempotent` [Omega.Frontier.ConditionalArithmetic] — theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w
- `fold_fixes_stable` [Omega.Frontier.ConditionalArithmetic] — theorem fold_fixes_stable (x : X m) : Fold x.1 = x
- `fold_is_surjective` [Omega.Frontier.ConditionalArithmetic] — theorem fold_is_surjective : Function.Surjective (Fold (m

### fiber-structure

- `maxFiberMultiplicity_bounds` [Omega.Combinatorics.FibonacciCube] — theorem maxFiberMultiplicity_bounds (m : Nat) :
    m / 2 + 1 ≤ X.maxFiberMultiplicity m ∧
    X.maxFiberMultiplicity m ≤ Nat.fib (m + 2)
- `maxFiberMultiplicity_eight` [Omega.Folding.MaxFiberHigh] — theorem maxFiberMultiplicity_eight : maxFiberMultiplicity 8 = 8
- `maxFiberMultiplicity_nine` [Omega.Folding.MaxFiberHigh] — theorem maxFiberMultiplicity_nine : maxFiberMultiplicity 9 = 10

### dynamical-systems

- `topological_entropy_eq_log_phi` [Omega.Folding.Entropy] — theorem topological_entropy_eq_log_phi :
    Tendsto (fun n => Real.log (Nat.fib (n + 2) : ℝ) / (n : ℝ)) atTop (𝓝 (Real.log φ))
- `goldenMeanAdjacency_has_goldenRatio_eigenvector` [Omega.Graph.TransferMatrix] — theorem goldenMeanAdjacency_has_goldenRatio_eigenvector :
    ∃ v : Fin 2 → ℝ, v ≠ 0 ∧
      Matrix.mulVec goldenMeanAdjacencyℝ v = fun i => Real.goldenRatio * v i
- `goldenMean_characteristic_recurrence` [Omega.Graph.Sofic] — theorem goldenMean_characteristic_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

## 09. 渐进与发展 / Gradual Progress, Development, and Measured Advance

Omega directions: modular-tower-inverse-limit, fibonacci-growth, golden-mean-shift

### modular-tower-inverse-limit

- `inverse_limit_extensionality` [Omega.Frontier.ConditionalArithmetic] — theorem inverse_limit_extensionality (a b : X.XInfinity) :
    a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m
- `inverse_limit_bijective` [Omega.Frontier.ConditionalSummary] — theorem inverse_limit_bijective :
    Function.Bijective (X.ofFamily : X.CompatibleFamily → X.XInfinity)
- `inverse_limit_left` [Omega.Frontier.ConditionalArithmetic] — theorem inverse_limit_left (F : X.CompatibleFamily) :
    X.toFamily (X.ofFamily F) = F

### fibonacci-growth

- `fibonacci_cardinality` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality (m : Nat) :
    Fintype.card (X m) = Nat.fib (m + 2)
- `fibonacci_cardinality_recurrence` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)
- `goldenMean_characteristic_recurrence` [Omega.Graph.Sofic] — theorem goldenMean_characteristic_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

### golden-mean-shift

- `fibonacci_cardinality` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality (m : Nat) :
    Fintype.card (X m) = Nat.fib (m + 2)
- `fibonacci_cardinality_recurrence` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)
- `goldenMean_characteristic_recurrence` [Omega.Graph.Sofic] — theorem goldenMean_characteristic_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

## 10. 明照与分辨 / Illumination, Discernment, and Clarity

Omega directions: spectral-theory, modular-tower-inverse-limit, rate-distortion-information-theory

### spectral-theory

- `goldenMeanAdjacency_has_goldenRatio_eigenvector` [Omega.Graph.TransferMatrix] — theorem goldenMeanAdjacency_has_goldenRatio_eigenvector :
    ∃ v : Fin 2 → ℝ, v ≠ 0 ∧
      Matrix.mulVec goldenMeanAdjacencyℝ v = fun i => Real.goldenRatio * v i
- `eigenvalue_eq_goldenRatio_or_goldenConj` [Omega.Graph.TransferMatrix] — theorem eigenvalue_eq_goldenRatio_or_goldenConj
    {μ : ℝ} (hμ : μ ^ 2 = μ + 1) :
    μ = Real.goldenRatio ∨ μ = Real.goldenConj
- `characteristic_polynomial_witness` [Omega.Frontier.ConditionalArithmetic] — theorem characteristic_polynomial_witness (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

### modular-tower-inverse-limit

- `inverse_limit_extensionality` [Omega.Frontier.ConditionalArithmetic] — theorem inverse_limit_extensionality (a b : X.XInfinity) :
    a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m
- `inverse_limit_bijective` [Omega.Frontier.ConditionalSummary] — theorem inverse_limit_bijective :
    Function.Bijective (X.ofFamily : X.CompatibleFamily → X.XInfinity)
- `inverse_limit_left` [Omega.Frontier.ConditionalArithmetic] — theorem inverse_limit_left (F : X.CompatibleFamily) :
    X.toFamily (X.ofFamily F) = F

### rate-distortion-information-theory

- `observation_refinement_reduces_error` [Omega.Frontier.ConditionalArithmetic] — theorem observation_refinement_reduces_error
    {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (μ : PMF α) (obs₁ : α → β) (obs₂ : α → γ) (f : γ → β)
    (hRef : ∀ x, obs₁ x = f (obs₂ x)) (P : Set α) :
    SPG.s
- `prefix_resolution_decreases_error` [Omega.Frontier.ConditionalArithmetic] — theorem prefix_resolution_decreases_error {m₁ m₂ n : Nat}
    (μ : PMF (Word n)) (h₁ : m₁ ≤ n) (h₂ : m₂ ≤ n) (hm : m₁ ≤ m₂)
    (P : Set (Word n)) :
    SPG.prefixScanError μ h₂ P ≤ SPG.prefixScanError μ h₁ P
- `scanError_hasCertificate` [Omega.Frontier.Conditional] — theorem scanError_hasCertificate {α β : Type*} [Fintype α] [Fintype β]
    (μ : PMF α) (obs : α → β) (P : Set α) :
    ScanErrorCertificate.Valid
      ({ μ

## 11. 节制与平衡 / Limitation, Moderation, and Balanced Measure

Omega directions: zeckendorf-representation, ring-arithmetic, golden-mean-shift

### zeckendorf-representation

- `zeckendorf_uniqueness` [Omega.Frontier.ConditionalArithmetic] — theorem zeckendorf_uniqueness {x y : X m} (h : X.zeckIndices x = X.zeckIndices y) : x = y
- `zeckendorf_injective` [Omega.Frontier.ConditionalArithmetic] — theorem zeckendorf_injective (m : Nat) : Function.Injective (X.zeckIndices (m
- `scanError_measure_le_complement` [Omega.Frontier.ConditionalArithmetic] — theorem scanError_measure_le_complement [MeasurableSpace α] [Fintype β]
    [MeasurableSpace β] [MeasurableSingletonClass β]
    (μ : MeasureTheory.Measure α) (obs : α → β) (hObs : Measurable obs)
    (P : Set α) (hP : M

### ring-arithmetic

- `stableValue_ring_isomorphism` [Omega.Frontier.ConditionalArithmetic] — theorem stableValue_ring_isomorphism (m : Nat) :
    (∀ x y : X m, stableValue (X.stableAdd x y) =
      (stableValue x + stableValue y) % Nat.fib (m + 2)) ∧
    (∀ x y : X m, stableValue (X.stableMul x y) =
      (stabl
- `modular_projection_add_no_carry` [Omega.Frontier.ConditionalArithmetic] — theorem modular_projection_add_no_carry (x y : X (m + 1))
    (h : stableValue x + stableValue y < Nat.fib (m + 3)) :
    X.modularProject (X.stableAdd x y) =
      X.stableAdd (X.modularProject x) (X.modularProject y)
- `stableAdd_comm` [Omega.Folding.FiberArithmetic] — theorem stableAdd_comm (x y : X m) :
    stableAdd x y = stableAdd y x

### golden-mean-shift

- `fibonacci_cardinality` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality (m : Nat) :
    Fintype.card (X m) = Nat.fib (m + 2)
- `fibonacci_cardinality_recurrence` [Omega.Frontier.ConditionalArithmetic] — theorem fibonacci_cardinality_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)
- `goldenMean_characteristic_recurrence` [Omega.Graph.Sofic] — theorem goldenMean_characteristic_recurrence (m : Nat) :
    Fintype.card (X (m + 2)) = Fintype.card (X (m + 1)) + Fintype.card (X m)

## 12. 聚散与流通 / Gathering, Dispersal, and Information Flow

Omega directions: rate-distortion-information-theory, fold-operator, modular-tower-inverse-limit

### rate-distortion-information-theory

- `observation_refinement_reduces_error` [Omega.Frontier.ConditionalArithmetic] — theorem observation_refinement_reduces_error
    {α β γ : Type*} [Fintype α] [Fintype β] [Fintype γ]
    (μ : PMF α) (obs₁ : α → β) (obs₂ : α → γ) (f : γ → β)
    (hRef : ∀ x, obs₁ x = f (obs₂ x)) (P : Set α) :
    SPG.s
- `prefix_resolution_decreases_error` [Omega.Frontier.ConditionalArithmetic] — theorem prefix_resolution_decreases_error {m₁ m₂ n : Nat}
    (μ : PMF (Word n)) (h₁ : m₁ ≤ n) (h₂ : m₂ ≤ n) (hm : m₁ ≤ m₂)
    (P : Set (Word n)) :
    SPG.prefixScanError μ h₂ P ≤ SPG.prefixScanError μ h₁ P
- `scanError_hasCertificate` [Omega.Frontier.Conditional] — theorem scanError_hasCertificate {α β : Type*} [Fintype α] [Fintype β]
    (μ : PMF α) (obs : α → β) (P : Set α) :
    ScanErrorCertificate.Valid
      ({ μ

### fold-operator

- `fold_is_idempotent` [Omega.Frontier.ConditionalArithmetic] — theorem fold_is_idempotent (w : Word m) : Fold (Fold w).1 = Fold w
- `fold_fixes_stable` [Omega.Frontier.ConditionalArithmetic] — theorem fold_fixes_stable (x : X m) : Fold x.1 = x
- `fold_is_surjective` [Omega.Frontier.ConditionalArithmetic] — theorem fold_is_surjective : Function.Surjective (Fold (m

### modular-tower-inverse-limit

- `inverse_limit_extensionality` [Omega.Frontier.ConditionalArithmetic] — theorem inverse_limit_extensionality (a b : X.XInfinity) :
    a = b ↔ ∀ m, X.prefixWord a m = X.prefixWord b m
- `inverse_limit_bijective` [Omega.Frontier.ConditionalSummary] — theorem inverse_limit_bijective :
    Function.Bijective (X.ofFamily : X.CompatibleFamily → X.XInfinity)
- `inverse_limit_left` [Omega.Frontier.ConditionalArithmetic] — theorem inverse_limit_left (F : X.CompatibleFamily) :
    X.toFamily (X.ofFamily F) = F
