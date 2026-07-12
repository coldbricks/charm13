# M4 CONJECTURES — Exact statements for kill / proof

**Status:** open candidates  
**Primary track:** Claim A  
**Side lemma:** Claim B  
**Secondary:** Claim C  
**Do not treat titles as proved.**

Formal symbols: `DEFINITIONS.md`. Ledger ids: `CLAIM_LEDGER.json`.

---

## Meta rules for this file

1. Every conjecture is false until proved or replaced by a counterexample.  
2. Before proof search, HUNTER runs the enumeration ranges in §H of each claim.  
3. Weakening a claim requires a new id (e.g. A → A1) and a ledger note.  
4. Elementary baselines (monotonicity of `D_B`, `D_0=0`, …) are lemmas, not main results.

---

# Claim A — Adaptive gap for path-prefix queries

**Ledger id:** `M4-A`  
**Form:** separation / minimal counterexample  
**Status:** `CANDIDATE NOVEL COUNTEREXAMPLE` (pending hunt)

## A.0 Setup

- Query family: `𝒬₀ = {list(v), stat(u), head(u)}` with unit costs.  
- Root known. Non-root nodes only after ancestor `list` chain.  
- P, Q explicit rational distributions on path-labeled trees.  
- Budget worst-case. Policies deterministic first; randomized if needed for optimality.

## A.1 Conjecture (strict adaptive gap at B=2)

**There exist** finite P, Q and attribute alphabets with:

- max `|V| ≤ 6`,  
- `|A| ≤ 4` (effective free attributes),  
- probability masses in `k/12` for integer k,  

such that

$$
D_2^{\mathrm{na}}(P,Q) \le \tfrac14
\quad\text{and}\quad
D_2(P,Q) = \tfrac12.
$$

## A.2 Conjecture (minimality of node count)

No instance with max `|V| ≤ 3` under the same query model, unit costs, and masses in `k/12` achieves

$$
D_2(P,Q) > D_2^{\mathrm{na}}(P,Q).
$$

## A.3 Conjecture (optional strengthening — gap form)

On the instance witnessing A.1, the optimal adaptive policy has the shape:

1. `list(root)` (or `list` of a fixed internal node),  
2. `head` or `stat` on a child chosen as a function of the list outcome,

and every nonadaptive pair of queries has TV ≤ 1/4.

## A.4 Fallback conjectures (if A.1 false)

| Id | Statement |
|----|-----------|
| A.1′ | Strict gap exists but only with B=3 or `|V|≤8` or larger denominators |
| A.1″ | Under `𝒬₀`, `D_B = D_B^{na}` for all B on all trees of depth ≤ 2 — **universality of nonadaptivity** (negative for A.1) |
| A.4 | Computing exact `D_B` for explicit finite (P,Q) and grounded `𝒬₀` is possible in time `f(B)·poly(m,n,r)` via belief-state DP |

A.4 is algorithmic; may become primary if separation collapses to prior art.

## A.H HUNTER range (mandatory first)

| Instance class | n | B | Notes |
|----------------|---|---|-------|
| H-A1 star | root+2 | 0..3 | one hot child under Q |
| H-A2 path | 4 nodes | 0..3 | intermediate list |
| H-A3 two branches | ≤6 | 0..3 | first list chooses side |
| H-A4 point masses | ≤6 | 0..3 | support mismatch |
| H-A5 P=Q | ≤6 | 0..3 | must give D=0 |
| H-A6 depth-1 only | ≤5 | 0..3 | stress A.2 |

Emit machine-readable JSON under `COUNTEREXAMPLES/` on any kill or witness.

---

# Claim B — Score non-monotonicity under defect coupling

**Ledger id:** `M4-B`  
**Form:** impossibility / counterexample to Bayes-monotone reading of `S`  
**Status:** `CANDIDATE NOVEL COUNTEREXAMPLE` (novelty bar high)

## B.0 Setup

- Severity map and `S`, `R` as in DEFINITIONS §6 (v0.3.3 numbers).  
- Latent defect cover model `(𝔇, Φ)`.  
- Pick comparison oracle **O** (must be fixed per subclaim):  
  - **O_full:** LR on fully observed tree;  
  - **O_smell:** LR on smell transcript `σ(X)` only.

**Default for B.1–B.2:** `O_full` with equal prior Bayes ordering.  
**Companion:** restate under `O_smell` as B.1s / B.2s.

## B.1 Conjecture (order reversal)

There exist finite P, Q and trees X₀, X₁ with positive mass under at least one of P,Q such that

$$
S(\sigma(X_0)) < S(\sigma(X_1))
\quad\text{but}\quad
\Lambda(X_0) > \Lambda(X_1)
$$

under a defect cover with `|𝔇|≤2`, `|Φ(d)|≤3`, using CHARM weights.

## B.2 Conjecture (equal score, unequal evidence)

There exist X₀, X₁ with `S(σ(X₀))=S(σ(X₁))` but optimal Bayes decisions under full observation differ for some equal-prior (P,Q).

## B.3 Lemma target (dual gate — elementary, not main invention)

For `F = {one bad finding}`, `S(F)=0.55 < 0.6` but `R(F)=1`.  
Hence `R` is not the thresholding of `S` alone.

**Status:** true by direct computation; record as lemma, not M4 main result.

## B.4 Conjecture (stronger characterization — optional)

The map from finding multiset → `S` is a **strict garbling** of the defect set in the Blackwell sense for some nontrivial cover Φ, hence cannot be sufficient for Bayes decisions among all (P,Q) consistent with that cover.

## B.H HUNTER range

| Id | Scenario |
|----|----------|
| H-B1 | one defect → two warns vs two defects → one warn each |
| H-B2 | one bad vs three warns (refuse vs score order) |
| H-B3 | format_magic + habitat_clash common cause |
| H-B4 | dedupe same (code,path_key) vs distinct path_keys |
| H-B5 | equal S, different Λ |
| H-B6 | production `σ` on synthetic trees (not only abstract Φ) |

---

# Claim C — Local predicates do not control D_B

**Ledger id:** `M4-C`  
**Form:** local-to-global separation  
**Status:** `CANDIDATE NOVEL COUNTEREXAMPLE` (classical collision risk)

## C.0 Setup

- Family `{φ_j}_{j=1}^J` of Boolean predicates, each locality ≤ ℓ.  
- Query system includes `𝒬₀` and one cost-1 `global_rel(ρ)`.  
- Matched locals: Law_P(φⱼ)=Law_Q(φⱼ) for all j.

## C.1 Conjecture (separation)

For every ℓ ≥ 1 and every finite family of ≤ℓ-local predicates, **there exist** P, Q on trees with `n = O(ℓ)` nodes such that locals match and

$$
D_1(P,Q) \ge \tfrac12
$$

when the allowed queries for this D_1 are `{global_rel(ρ)}` for some ρ not in the linear span / Boolean algebra generated by the φⱼ in the sense fixed by the experiment (explicit: ρ not equal to any φⱼ and not a function of any single φⱼ).

*Note:* The quantifier order is: ∀ smell-like families ∃ hard (P,Q,ρ). HUNTER may kill a *fixed* family without killing the ∀∃ claim.

## C.2 Conjecture (CHARM-shaped family)

There exist P, Q such that every predicate corresponding to current CHARM smell codes (magic match, habitat family membership, GIAB token absence, per-file checksum line OK, size-band flag, toy-sibling flag, monolith flag) has identical law under P and Q, yet `D_1 ≥ 1/2` via a single global co-occurrence or manifest-set relation.

## C.3 Conjecture (positive companion — tree-Markov)

If P and Q are tree-Markov on a known junction tree of treewidth ≤ k and all maximal-clique marginals agree, then for unit-cost node queries and budget B,

$$
D_B(P,Q) \le f(k,B)
$$

for an explicit f with f(k,B)→0 as … *(f to be found or disproved)*.

If false, replace by the weakest true bound or mark DISPROVED.

## C.H HUNTER range

| Id | Scenario |
|----|----------|
| H-C1 | companion size-ratio global, local magic OK |
| H-C2 | checksum lines OK, file-set parity differs |
| H-C3 | each specialist legal alone; joint co-occurrence banned under P |
| H-C4 | all φⱼ matched; only global_rel distinguishes |
| H-C5 | tree-Markov matched cliques — probe C.3 |

---

# Capacity track (not a primary claim yet)

**Ledger id:** `M4-CAP`  
**Status:** background definition only

## CAP.1 Research question

Under which special cases does `C_H(B,ε,K)` reduce to a known distribution-matching or steganographic capacity?

## CAP.2 Conjecture (zero capacity under strong observer)

If `𝒬` includes full tree readout at finite cost C_full and `B ≥ C_full`, then for any H with `TV(P_H, Q_{H,θ,s}) > ε` for all θ,s in the allowed generator class, `C_H(B,ε,K)=0` or empty.

Elementary once unrestricted observation is cheap; record as sanity check.

---

# Repair track (tertiary)

**Ledger id:** `M4-R`  
**Status:** deferred until A/B/C resolve

## R.1 Conjecture target

Under laminar witness sets on rooted paths, min-cost repair to achieve `D_B ≤ ε` admits an FPT algorithm in (B, depth).

Do not open P4 on R until primary track finishes.

---

# Dependency graph of claims

```text
B.3 (dual gate lemma) ── independent, elementary
B.1 / B.2 ── honesty of score ── side lemma for RESULT.md
A.1 / A.2 ── PRIMARY
A.4 ── fallback primary (algorithm)
C.1 / C.2 ── secondary
C.3 ── optional positive companion
CAP.*, R.* ── later
```

---

# What would falsify the provisional primary (A)

1. Exhaustive enumeration over H-A1..H-A6 with denominators ≤ 12 and n≤6 shows `D_B = D_B^{na}` always.  
2. A published theorem already classifies adaptive gaps for this exact query geometry with matching constants.  
3. Proof that unit-cost list/stat/head on trees never benefits from adaptivity when observations are non-destructive and root is known — then A.1″ wins.

---

# Promotion rules

| Event | Action |
|-------|--------|
| HUNTER finds witness for A.1 | Status → search for minimality A.2; draft PROOFS/A_gap.md |
| HUNTER kills A.1 | Activate A.1′ or A.4; update ledger |
| MIRROR collision on A | PRIOR-ART COLLISION; switch primary to A.4 or C.2 |
| B.1 established | Include as side result in RESULT.md regardless of A |
| C.2 established | Candidate secondary RESULT section or follow-on mission |
