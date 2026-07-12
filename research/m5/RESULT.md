# M5 RESULT — Extremal geometry of budgeted inspection

**Mission:** M5 theorem package (seed audit + sharp envelope + habitat application)  
**Date:** 2026-07-12  
**Baseline:** CHARM13 ≥ v0.3.3; M4 closed  

---

## Terminal status

### Primary

**`PROVED — NOVELTY UNRESOLVED`**

Analytic seed package independently re-derived and machine-certified on finite instances. Literature novelty audit incomplete (no public “new math” language). Lean formalization not started.

### Crown statements (proved in the frozen OPEN model)

| Id | Statement | Status |
|----|-----------|--------|
| M5-L0 | Deterministic policies suffice for finite TV | PROVED — known baseline |
| M5-L1 | Exact weighted classification-tree reduction $D=1-2R$ | PROVED — prior-art bridge |
| M5-T1 | $r\le B+1$ ⇒ $D_B^{\mathrm{ad}}=D_B^{\mathrm{na}}$ (flattening) | PROVED — novelty unresolved |
| M5-T2 | Root-arity: $D_2^{\mathrm{ad}}\le K\\,D_2^{\mathrm{na}}$ | PROVED — novelty unresolved |
| M5-T3 | Sharp law $G_2(K)=1-1/K$ with matching construction | PROVED — novelty unresolved |
| M5-T4 | Four-active-world binary extremizer = M4 butterfly (unique up to symmetry) | PROVED — novelty unresolved |
| M5-T5 | Near factor-two equality forces branch balance and locality | PROVED — baseline stability |
| M5-U | k-pair habitat: $D_2=1$, $D_2^{\mathrm{na}}=2/k$, greedy ratio $k/2$ | PROVED — application family |

### Central sharp statement

> Under globally addressable unit-cost queries of active arity at most $K$, at budget two:
>
> $$
> D_2^{\mathrm{ad}}\le K\\,D_2^{\mathrm{na}},
> \qquad
> D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}\le 1-\frac1K,
> 
$$
>
> and both are **exactly sharp**: there exists a finite family with
>
> $$
> D_2^{\mathrm{ad}}=1,\qquad D_2^{\mathrm{na}}=\frac1K.
> 
$$
>
> Hence
>
> $$
> G_2(K) := \sup\bigl(D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}\bigr) = 1-\frac1K.
> 
$$

For binary queries ($K=2$): $D_2^{\mathrm{ad}}\le 2D_2^{\mathrm{na}}$ and the largest additive gap is exactly $1/2$. The M4 four-world witness is therefore **support-minimal** (by flattening, $r\ge 4$) and **gap-maximal** among binary OPEN queries at budget two.

Proofs: `SEED_THEOREMS.md`  
Sharp certificates: `EXPERIMENTS/m5_exact.py`, `EXPERIMENTS/test_m5_exact.py`  
k-pair application: `PROOFS/UNBOUNDED_ADAPTIVITY_GAP.md`, `EXPERIMENTS/test_m5.py`

---

## Correction relative to earlier M5 packaging

Earlier M5 crowned the **k-pair / which-then-bit** family as the primary envelope with

$$
D_2^{\mathrm{na}}=\frac2k,\qquad \mathrm{Gap}=1-\frac2k\to 1.
$$

That family remains **correct** and remains the right CHARM-shaped model for myopic greedy failure and “gate before local.” It is **not** the sharp universal construction under arity-$k$ queries.

| Family | Gate arity | $D_2^{\mathrm{ad}}$ | $D_2^{\mathrm{na}}$ | Gap | Role |
|--------|------------|------------------------|------------------------|-----|------|
| Sharp address construction | $K$ | $1$ | $1/K$ | $1-1/K$ | **Extremal law** |
| k-pair (`bit_j` → `na` off-branch) | $k$ | $1$ | $2/k$ | $1-2/k$ | Habitat + greedy scar |

Both gaps tend to $1$ as arity/branching $\to\infty$. The sharp package is the tighter finite law.

---

## Honest hierarchy

1. **Inequalities are real** — analytic + rational certificates.  
2. **Adaptivity helps** is classical (active HT, feature acquisition, classification trees).  
3. **Residual value:** support flattening, sharp finite root-arity law, equality classification of the binary butterfly, first stability statement, CHARM product scars.  
4. **Not claimed:** literature novelty; new statistical distance; T4; that real disks equal either family.  
5. **Open:** support-constrained curve $G_2(K,r)$; full metric stability; $B\ge 3$ sharp law; Lean; completed prior-art collision.

Novelty packaging for residual packaging language: **`PROVED — NOVELTY UNRESOLVED`** (sharp package); k-pair product scars remain **`KNOWN RESULT, NEW APPLICATION`**.

---

## Machine verification

```powershell
cd research\m5\EXPERIMENTS
python test_m5_exact.py   # sharp package + butterfly + support sanity
python test_m5.py         # k-pair closed forms + greedy
python m5_exact.py        # table K=2..7
python enum_core.py       # k-pair table
```

Expected: all PASS; sharp $K=2..7$ gives $\mathrm{ad}=1$, $\mathrm{na}=1/K$; k-pair $k=2..12$ gives $\mathrm{na}=2/k$.

---

## Product scar

`PRODUCT_DELTA.md` — static smell ≠ adaptive T1; gate-before-local; do not present $2/k$ as the universal extremal constant; cite $G_2(K)=1-1/K$ for the sharp envelope and k-pair for habitat/greedy stories.

---

## Open frontier (post-seed)

1. Exact support-constrained curve $G_2(K,r)$.  
2. Equality classification for $K>2$.  
3. Quantitative distance-to-extremizer stability beyond Theorem 8.1.  
4. Sharp $G_B(K)$ for $B\ge 3$.  
5. Guarded-vs-informational compilation theorems (abstract only).  
6. Lean formalization of T1–T4.  
7. Completed primary-source collision matrix.

---

## Sign-off

| Role | Verdict |
|------|---------|
| DIRECTOR | Freeze OPEN model; crown sharp $G_2(K)$; retain k-pair as application |
| BLACKWELL | TV objective held; score monoid not substituted |
| HYDRA | Finite certificates green; no counterexample to seed package in scope |
| ARCHIVIST | Collision map started; novelty unresolved |
| REFEREE | Accept as proved-in-model; block novelty press |
| BRIDGE | Docs honesty + catalog pointers only |

**Mission M5 mathematical core: SUCCESS under sharp seed package.**  
**Annals-grade pure novelty: NOT CLAIMED.**
