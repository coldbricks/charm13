# Result M4-B — Severity product is not Bayes-monotone

**Status:** MINIMAL COUNTEREXAMPLE ESTABLISHED  
**Novelty:** qualitative claim is classical; CHARM constants + refuse dual-gate are project-specific  
**Artifact:** `COUNTEREXAMPLES/wit-B-score-lr-reversal.json`

---

## Score and refuse (v0.3.3)

$$
w(\mathrm{bad})=\frac{11}{20},\\;
w(\mathrm{warn})=\frac{1}{4},\\;
w(\mathrm{info})=\frac{1}{20},
$$

$$
S(F)=1-\prod_{f\in F}\bigl(1-w(\mathrm{sev}(f))\bigr),
\qquad
R(F)=\mathbf{1}[\exists\\,\mathrm{bad}]\lor\mathbf{1}[S(F)\ge 3/5].
$$

---

## Theorem B1 (order reversal)

There exist trees X₀, X₁ and rational laws P, Q on {X₀,X₁,X₂} such that

$$
S(\sigma(X_0)) < S(\sigma(X_1))
\quad\text{but}\quad
\Lambda(X_0) > \Lambda(X_1),
$$

where `Λ = Q/P` and `σ` is the finding map (here idealized by severity multisets).

### Witness

| Tree | Findings | S | R |
|------|----------|---|---|
| X₀ | {warn, warn} | 1−(¾)² = **7/16** | 0 |
| X₁ | {bad} | **11/20** | 1 |
| X₂ | ∅ | 0 | 0 |

Check: `7/16 = 0.4375 < 0.55 = 11/20`.

Masses:

$$
P=(1/6,\\;2/3,\\;1/6),\qquad Q=(2/3,\\;1/6,\\;1/6).
$$

$$
\Lambda(X_0)=4,\qquad \Lambda(X_1)=1/4,\qquad \Lambda(X_2)=1.
$$

Thus `S(X₀)<S(X₁)` but `Λ(X₀)>Λ(X₁)`. ∎

### Corollary (refuse vs evidence)

`R(X₁)=1 > R(X₀)=0` while X₀ is strictly more Q-like under Λ.  
So the operator refuse rule is **not** a monotone transform of the full-tree likelihood ratio for all (P,Q).

---

## Theorem B2 (equal score, unequal LR)

If two trees share the same severity multiset, then `S` agrees, but `Λ` need not.

Witness: both trees one `warn` (`S=1/4`),  
`P=(1/2,1/2)`, `Q=(3/4,1/4)` ⇒ `Λ ∈ {3/2, 1/2}`. ∎

**Interpretation:** `S` is not a sufficient statistic for Bayes decisions under full observation.

---

## Lemma B3 (dual gate) — already proved

`PROOFS/B3_dual_gate.md`: one `bad` has `S=11/20 < 3/5` but `R=1`.

---

## What this does **not** say

- Not: “noisy-OR is never useful as an engineering monoid.”  
- Not: a new probability inequality.  
- Yes: the v0.3.3 score **cannot** be marketed as calibrated P(generated) or as LR-monotone evidence under CHARM-like multi-finding defects.
