# M5 Frozen Model — Budgeted Inspection

**Status:** frozen for seed theorems and extremal claims  
**Date:** 2026-07-12

## Object

Let $W$ be finite. Let $P,Q$ be probability distributions on $W$, and

$$
\mu = P - Q.
$$

A deterministic query is a total finite-valued map $q: W \to Y_q$.

**Central model (OPEN):** every query is globally addressable, non-destructive, and unit-cost.

## Policies

- **Adaptive budget $B$:** a query decision tree of worst-case depth at most $B$.
- **Nonadaptive budget $B$:** a fixed set of at most $B$ queries chosen before observations.

The terminal hypothesis decision is post-processing and is **excluded** from the observation transcript.

## Value

For a partition $\Pi$ of $W$,

$$
V_\mu(\Pi) = \frac12\sum_{C\in\Pi}|\mu(C)|.
$$

$D_B^{\mathrm{ad}}$ and $D_B^{\mathrm{na}}$ optimize transcript total variation over the two policy classes.

Active signed support:

$$
S_\mu = \{w : \mu(w)\ne 0\}, \qquad r = |S_\mu|.
$$

## Models kept separate

| Label | Meaning |
|-------|---------|
| OPEN | Globally addressable unit-cost queries (main theorems) |
| GUARDED | Query requires prior discoveries |
| OPEN CLOSURE | Remove guards; keep maps and costs |
| STATIC PRECEDENCE-CLOSED | Fixed set must contain predecessors |
| EXPECTED BUDGET | Separate object; forbidden in main theorems unless restated |

Do **not** call a guarded-access gap an informational adaptivity gap.

## Objective hygiene

The declared objective is **transcript total variation**. Substitutions of KL, mutual information, likelihood, classifier accuracy, or CHARM's engineering `blown_score` for this objective are vetoed unless restated as a different claim.

## Two families in this docket

1. **Sharp arity construction** (extremal geometry): worlds $(i,x)$ with $x\in\{0,1\}^K$; gate $g(i,x)=i$; bits $b_j(i,x)=x_j$. Yields $D_2^{\mathrm{ad}}=1$, $D_2^{\mathrm{na}}=1/K$.
2. **k-pair / which-then-bit habitat** (CHARM-shaped application): worlds $w_{i,b}$; `which` returns $i$; `bit_j` returns $b$ if $i=j$ else `na`. Yields $D_2^{\mathrm{ad}}=1$, $D_2^{\mathrm{na}}=2/k$, plus myopic greedy failure.

Both are correct. Only (1) saturates the universal root-arity bound $G_2(K)=1-1/K$.
