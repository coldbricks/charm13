# M5 RESULT — Unbounded adaptivity gap

**Mission:** M5-Ω track (crowned claim: characterization of Gap at fixed B)  
**Date:** 2026-07-12  
**Baseline:** CHARM13 v0.3.3; M4 closed  

---

## Terminal status

### Primary

**`PROVED, FORMALIZATION PARTIAL WITH AN EXPLICIT GAP`**

(Analytic closed form + machine certificates for finite k; no Lean yet.)

### Central statement

> There exists an explicit infinite family of finite instances `(P_k, Q_k)` (the **k-pair / which-then-bit** habitat) such that for every `k ≥ 2`:
>
> $$D_2(P_k,Q_k)=1, \qquad D_2^{\mathrm{na}}(P_k,Q_k)=\frac2k,$$
>
> hence
>
> $$\mathrm{Gap}_2(k)=1-\frac2k \to 1, \qquad \frac{D_2}{D_2^{\mathrm{na}}}=\frac k2 \to \infty.$$
>
> Moreover adaptive budget to perfect separation is **2**, nonadaptive is **k** (unbounded separation), and **myopic greedy** first-query selection has approximation ratio `k/2` (unbounded failure).

Proof: `PROOFS/UNBOUNDED_ADAPTIVITY_GAP.md`  
Code: `EXPERIMENTS/enum_core.py`, `EXPERIMENTS/test_m5.py`

---

## Why this is bolder than M4

| M4 | M5 |
|----|----|
| One gap of ½ on 4 worlds | **Gap → 1** at fixed budget 2 |
| Minimality n=4 unguarded | **Unbounded ratio** adaptive/nonadaptive |
| Existence | **Closed-form infinite family** |
| — | **Greedy unboundedly bad** |
| — | **No fixed checklist size dominates adaptive T1** (Cor U6) |

---

## Honest hierarchy (scientist protocol)

1. **The inequalities are real** — not prose.  
2. **The abstract idea that adaptivity helps is known** — fixed-horizon active HT, feature acquisition.  
3. **Residual value:** exact family, unbounded gap/ratio, budget separation, greedy failure, CHARM product scar.  
4. **Not claimed:** new distance; T4; that real disk habitats equal this family.  
5. **Formalization:** Lean still open.  
6. **Literature:** entry points only until MIRROR completes OPENED citations.

Novelty label for packaging: **`KNOWN RESULT, NEW APPLICATION`** (strong application + exact envelope).

---

## Companion theorems in the same proof file

| Id | Statement |
|----|-----------|
| U1 | D₂ = 1 for all k |
| U2 | D₂^{na} = 2/k for k≥2 |
| U3 | Gap→1, ratio→∞ |
| U4 | B_ad^*=2, B_na^*=k (k≥2) |
| U5 | Myopic greedy ratio k/2 |
| U6 | No fixed-B nonadaptive suite uniformly controls adaptive risk |

---

## Machine verification

```powershell
cd C:\Users\coldb\charm13\research\m5\EXPERIMENTS
python test_m5.py
python enum_core.py
```

Expected: all tests OK; table k=2..12 matches theory.

---

## Product scar

`PRODUCT_DELTA.md` — docs: static smell ≠ adaptive T1; myopic local-first can be arbitrarily weak; bench/smell sketches for gate-before-local.

---

## What was believed before M5

- M4 gap of ½ might be “the” illustrative constant.  
- Fixed smell suites might be thought to scale as “more rules ⇒ closer to T1.”  
- Greedy strongest-finding-first might seem reasonable.

## What is now proved

- Gap can be **worse than any constant < 1** at **B=2**.  
- Nonadaptive budget must **grow with habitat branching** to match adaptive budget 2.  
- Myopic local-first is **arbitrarily suboptimal**.

## Falsifier

- Error in case analysis of nonadaptive pairs.  
- Different nonadaptive model (e.g. free adaptive addressing) — must be stated.  
- Prior paper with identical closed forms on this exact family — then pure KNOWN RESULT (still useful packaging).

---

## How CHARM13 should change

See PRODUCT_DELTA. Minimum: **docs honesty this week**.  
Do not retune weights as M5 output.

---

## Sign-off

| Role | Verdict |
|------|---------|
| CHARM13 | Crown U-family as M5 primary |
| HUNTER | Certificates green for k≤12; analytic holds for all k |
| MIRROR | Package as known-phenomenon + exact envelope; block “new theory of TV” |
| Press | Do **not** say “proves when folders are fake”; say “proves adaptive gap can be arbitrarily large at budget 2 in an explicit family” |

**Mission M5 mathematical core: SUCCESS under proved unbounded gap.**  
**Annals-grade pure novelty: NOT CLAIMED.**
