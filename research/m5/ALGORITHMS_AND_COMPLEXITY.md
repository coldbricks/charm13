# Algorithms and complexity

## Exact reduction

By Theorem 3.1, computing \(D_B^{\mathrm{ad}}\) is equivalent to minimizing weighted Bayes classification error over query decision trees of depth \(\le B\). Computing \(D_B^{\mathrm{na}}\) is fixed-feature acquisition of size \(\le B\) followed by optimal joint-output majority classification.

## Implementations in this docket

| Solver | Path | Notes |
|--------|------|-------|
| Exhaustive depth-2 adaptive + static pairs | `EXPERIMENTS/m5_exact.py` | Rational; independent of M4 enum |
| Mask DP adaptive / nonadaptive | `EXPERIMENTS/enum_core.py` | k-pair + general instances |
| Ladder kernel | `research/ladder/kernel.py` | Shared closed forms + regression |

## Complexity boundary (honest)

- Optimal decision trees are classically hard in identification / expected-test objectives (Hyafil–Rivest).  
- Depth-limited optimal classification trees admit specialized solvers (e.g. MurTree depth-two).  
- M5 does **not** claim a new hardness proof. A useful future result is a sharp FPT boundary under bounded \(B\), arity, active support, or prefix guards.

## Required dual implementations for future extremal search

1. Recursive decision-tree DP.  
2. Partition / polyhedral optimization with no shared recurrence.  

Agreement of independent solvers is required before crowning computational extremals.
