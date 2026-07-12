# M4 HUNTER REPORT — Distinguishing adversary

**Role:** HUNTER  
**Phase:** P1 complete (enumeration + certificates)  
**Date:** 2026-07-12  

---

## Executive verdicts

| Claim | Verdict | Artifact |
|-------|---------|----------|
| M4-A (qualitative adaptive gap) | **WITNESS + PROVED** D₂=1, D₂^{na}=½, gap=½ | `wit-A-asym-branch-B2.json` |
| M4-A.1 literal constants (½ vs ≤¼) | **NOT WITNESSED** | stronger adaptive, weaker na bound |
| M4-A path-prefix FS | **WITNESS** under requires; **KILL gap** under path-free na | `wit-A-list-then-head-B2.json` |
| M4-A.2 n≤3 no gap | **PROVED** (Lemma 3, unguarded depth-2) — search demoted | `PROOFS/A_adaptive_gap.md` |
| External scientist cert suite | **8/8 independent pass** | `SCIENTIST_REVIEW.md` |
| M4-B order reversal | **WITNESS** | `wit-B-score-lr-reversal.json` |
| M4-B equal score ≠ equal LR | **WITNESS** | `wit-B-equal-score-unequal-lr.json` |
| M4-B3 dual gate | **CONFIRM** elementary | `PROOFS/B3_dual_gate.md` |
| M4-C parity | **WITNESS** (classical) | `wit-C-parity-local-global.json` |

---

## A — Adaptive gap details

### Primary witness (asym_branch)

```
B=2: D_ad=1  D_na=1/2  gap=1/2
```

Policy: gate then left/right.  
Nonadaptive every 2-subset ≤ ½ (hand proof in `PROOFS/A_adaptive_gap.md`).

### FS witness (list_then_head)

```
B=2: D_ad=1  D_na=1/2  gap=1/2
D_na path_free=1  (gap dies)
```

**Hidden assumption attack:** succeeded against naive FS novelty — legality model is load-bearing.

### three_pair_bit

```
B=2: D_ad=1  D_na=2/3  gap=1/3
```

### Random search

800 trials n=4 m=4 B=2: **17** gaps; best random gap **2/5**.

### Minimality

n=3, m=3 binary queries, ≤2-support count probs: **gap=0** over 156672 instances.

---

## B — Score attacks

| Test | Result |
|------|--------|
| S(two warn)=7/16 < S(bad)=11/20 but Λ 4 > 1/4 | PASS kill monotone reading |
| R(bad)=1, R(two warn)=0 opposite Λ order | PASS |
| Equal S, unequal Λ | PASS |
| Dual gate | PASS |

---

## C — Local global

| Test | Result |
|------|--------|
| Locals Bern matched | PASS |
| D₁ locals only = 0 | PASS |
| D₁ parity = 1 | PASS |
| D₂ locals = 1 | PASS (locals not useless with enough budget) |

---

## Tooling

- `EXPERIMENTS/enum_core.py` — exact Fraction DP for adaptive W; subset enum for nonadaptive  
- `EXPERIMENTS/hunt.py` — driver  

### Sanity

- P=Q ⇒ D=0 on demos  
- Monotone D in B on demos  
- Certificate assert `gap(asym,2)==1/2` green  

---

## Remaining kill attempts (optional P1b)

1. Independent reimplementation of W DP in another language.  
2. Broader n=3 search (ternary obs, unequal costs).  
3. Randomized policies — does mixed na close the ½ gap? (unlikely for pure TV of deterministic kernels; check).  

---

## Sign-off

HUNTER: **claims A/B/C finite witnesses established.**  
Literal A.1 constants from CHARTER: **weaken to qualitative + exact proven constants.**  
No product code modified.
