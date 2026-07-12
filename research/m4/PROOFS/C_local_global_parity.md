# Result M4-C — Local match does not control D_1

**Status:** MINIMAL COUNTEREXAMPLE ESTABLISHED (classical content)  
**Novelty:** `KNOWN RESULT` in graphical models / parity; specialization to `D_B` notation  
**Artifact:** `COUNTEREXAMPLES/wit-C-parity-local-global.json`

---

## Theorem C (parity separation)

Let worlds be bit pairs `(b1,b2) ∈ {0,1}²` ordered `00,01,10,11`.

$$
P=\tfrac12\delta_{00}+\tfrac12\delta_{11},
\qquad
Q=\tfrac12\delta_{01}+\tfrac12\delta_{10}.
$$

Local predicates / queries: `φ1=b1`, `φ2=b2` (unit cost).  
Global query: `ρ = b1 XOR b2` (unit cost).

Then:

1. `Law_P(φj) = Law_Q(φj) = Bern(1/2)` for j=1,2 (locals matched).  
2. `D_1` using only `{φ1,φ2}` equals **0**.  
3. `D_1` using `{ρ}` equals **1**.  

### Proof

(1) Under P: `b1=0` on 00 (mass ½), `b1=1` on 11 (mass ½). Under Q: `b1=0` on 01, `b1=1` on 10. Same for `b2`.

(2) Any single local leaves TV=0 (same Bernoulli laws). Empty budget TV=0.

(3) `ρ` is 0 under all P-mass and 1 under all Q-mass ⇒ TV=1. ∎

### Note

With **both** locals and budget 2, `D_2=1` (full pair recovery). So local family is informative when budget covers the whole support of the local cover — the failure mode is **budget-1 local-only** vs **budget-1 global**.

---

## CHARM reading (not a new theorem)

Smell codes that each inspect a small support (magic of one file, one checksum line) can all pass in law while a **set-level** relation (manifest completeness, co-occurrence ban, parity of linkage) distinguishes P from Q at cost 1.

Product implication (P6, optional): prefer explicit global relation smells over stacking redundant local warns.
