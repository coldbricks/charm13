# EXPERIMENTS — Exact finite-model theorem search

**Status:** scaffold only (P0) — no enumerator implemented yet  
**Rule:** exact rationals; no neural nets; no private data  
**Rule:** research-only; do not import into `src/charm` until P3

---

## Planned modules

| Module | Purpose |
|--------|---------|
| `enum_policies.py` | Brute-force / DP `D_B` and `D_B^{na}` for small instances |
| `defect_score.py` | Claim B score vs Λ checks |
| `local_global.py` | Claim C matched-local / global gap toys |
| `fixtures/` | JSON (P,Q,queries) aligned with COUNTEREXAMPLES schema |

---

## Property tests (required when code exists)

- policy-value monotonicity in B  
- brute force agrees with DP (if both exist)  
- symmetry: `D_B(P,Q)=D_B(Q,P)`  
- known zero-distance: P=Q ⇒ D_B=0  
- known disjoint-support cheap witness cases  
- reproducibility of saved counterexample JSON  

---

## Run policy

```powershell
cd C:\Users\coldb\charm13\research\m4\EXPERIMENTS
# after implementation:
# python enum_policies.py --fixture fixtures/H-A1.json --budget 2
```

Exit codes: 0 ok; 2 claim-kill found; 3 internal inconsistency.

---

## P1 first fixture targets

1. `fixtures/H-A5_equal.json` — P=Q sanity  
2. `fixtures/H-A4_disjoint.json` — support split  
3. `fixtures/H-A1_star.json` — adaptive gap candidate  
4. `fixtures/H-B2_bad_vs_warns.json` — refuse vs score  

---

## Dependency policy

Python stdlib only unless ledger notes an approved exception (`mpmath` not needed if using `fractions`).
