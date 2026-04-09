#!/usr/bin/env python3
"""Curated theorem profiles for direction-level Omega mappings."""

DIRECTION_PROFILES = {
    "golden-mean-shift": {
        "label": "Golden-Mean Shift",
        "keywords": [
            "No11",
            "goldenMean",
            "golden mean",
            "characteristic recurrence",
            "adjacency",
            "fibonacci",
        ],
        "module_hints": [
            "Omega.Core.No11",
            "Omega.Graph.Sofic",
            "Omega.Graph.TransferMatrix",
            "Omega.Frontier.ConditionalArithmetic",
            "Omega.Combinatorics.FibonacciCube",
        ],
        "preferred_theorems": [
            "fibonacci_cardinality",
            "fibonacci_cardinality_recurrence",
            "goldenMean_characteristic_recurrence",
            "goldenMeanAdjacency_has_goldenRatio_eigenvector",
        ],
    },
    "fibonacci-growth": {
        "label": "Fibonacci Growth",
        "keywords": [
            "fibonacci",
            "recurrence",
            "cardinality",
            "fib",
        ],
        "module_hints": [
            "Omega.Frontier.ConditionalArithmetic",
            "Omega.Core.Fib",
            "Omega.Graph.Sofic",
            "Omega.Graph.TransferMatrix",
        ],
        "preferred_theorems": [
            "fibonacci_cardinality",
            "fibonacci_cardinality_recurrence",
            "goldenMean_characteristic_recurrence",
        ],
    },
    "zeckendorf-representation": {
        "label": "Zeckendorf Representation",
        "keywords": [
            "zeckendorf",
            "non-consecutive",
            "injective",
            "unique",
        ],
        "module_hints": [
            "Omega.Frontier.ConditionalArithmetic",
            "Omega.Folding.FiberArithmetic",
            "Omega.Folding.CollisionZetaOperator",
        ],
        "preferred_theorems": [
            "zeckendorf_uniqueness",
            "zeckendorf_injective",
        ],
    },
    "fold-operator": {
        "label": "Fold Operator",
        "keywords": [
            "fold",
            "stable",
            "surjective",
            "idempotent",
            "fiber",
        ],
        "module_hints": [
            "Omega.Frontier.ConditionalArithmetic",
            "Omega.Folding",
        ],
        "preferred_theorems": [
            "fold_is_idempotent",
            "fold_fixes_stable",
            "fold_is_surjective",
        ],
    },
    "ring-arithmetic": {
        "label": "Ring Arithmetic",
        "keywords": [
            "ring",
            "stableAdd",
            "stableMul",
            "modular",
            "isomorphism",
        ],
        "module_hints": [
            "Omega.Frontier.ConditionalArithmetic",
            "Omega.Folding.FiberArithmetic",
            "Omega.Folding.FiberArithmeticProperties",
        ],
        "preferred_theorems": [
            "stableValue_ring_isomorphism",
            "modular_projection_add_no_carry",
            "stableAdd_comm",
            "stableMul_comm",
        ],
    },
    "spectral-theory": {
        "label": "Spectral Theory",
        "keywords": [
            "spectral",
            "eigen",
            "characteristic polynomial",
            "collision",
            "kernel",
        ],
        "module_hints": [
            "Omega.Folding.CollisionZeta",
            "Omega.Folding.CollisionZetaOperator",
            "Omega.Graph.TransferMatrix",
            "Omega.Frontier.ConditionalArithmetic",
        ],
        "preferred_theorems": [
            "collision_kernels_all_real_eigenvalues",
            "characteristic_polynomial_witness",
            "eigenvalue_eq_goldenRatio_or_goldenConj",
        ],
    },
    "modular-tower-inverse-limit": {
        "label": "Modular Tower and Inverse Limit",
        "keywords": [
            "inverse_limit",
            "inverse limit",
            "round",
            "restrict",
            "extensionality",
        ],
        "module_hints": [
            "Omega.Frontier.ConditionalArithmetic",
            "Omega.Frontier.ConditionalSummary",
        ],
        "preferred_theorems": [
            "inverse_limit_left",
            "inverse_limit_right",
            "inverse_limit_extensionality",
            "inverse_limit_round_left",
            "inverse_limit_round_right",
            "inverse_limit_bijective",
        ],
    },
    "dynamical-systems": {
        "label": "Dynamical Systems",
        "keywords": [
            "entropy",
            "shift",
            "orbit",
            "golden ratio eigenvector",
            "recurrence",
        ],
        "module_hints": [
            "Omega.Folding.Entropy",
            "Omega.Graph.Sofic",
            "Omega.Graph.TransferMatrix",
        ],
        "preferred_theorems": [
            "topological_entropy_eq_log_phi",
            "goldenMean_characteristic_recurrence",
            "goldenMeanAdjacency_has_goldenRatio_eigenvector",
        ],
    },
    "rate-distortion-information-theory": {
        "label": "Rate-Distortion and Information Theory",
        "keywords": [
            "error",
            "certificate",
            "refinement",
            "resolution",
            "kappa",
            "scan",
        ],
        "module_hints": [
            "Omega.Frontier.ConditionalArithmetic",
            "Omega.Frontier.Conditional",
            "Omega.Frontier.Certificates",
            "Omega.SPG.ErrorThreshold",
        ],
        "preferred_theorems": [
            "observation_refinement_reduces_error",
            "prefix_resolution_decreases_error",
            "scanError_hasCertificate",
            "prefixScanError_hasCertificate",
            "kappa_ge_of_eps_ge",
            "eps_lt_of_kappa_lt",
        ],
    },
    "fiber-structure": {
        "label": "Fiber Structure",
        "keywords": [
            "fiber",
            "maxFiberMultiplicity",
            "split",
            "moment",
            "bound",
        ],
        "module_hints": [
            "Omega.Combinatorics.FibonacciCube",
            "Omega.Folding.FiberSplit",
            "Omega.Folding.MaxFiber",
            "Omega.Folding.MaxFiberHigh",
            "Omega.Folding.MomentBounds",
            "Omega.Folding.MomentRecurrence",
        ],
        "preferred_theorems": [
            "maxFiberMultiplicity_bounds",
            "maxFiberMultiplicity_fibonacci_bound",
            "maxFiberMultiplicity_eight",
            "maxFiberMultiplicity_nine",
            "maxFiberMultiplicity_ten",
        ],
    },
}


def iter_profile_keywords(direction: str, extra_keywords: list[str] | None = None) -> list[str]:
    """Return profile keywords extended by caller-provided terms."""
    profile = DIRECTION_PROFILES.get(direction, {})
    keywords = list(profile.get("keywords", []))
    if extra_keywords:
        for keyword in extra_keywords:
            if keyword and keyword not in keywords:
                keywords.append(keyword)
    return keywords
