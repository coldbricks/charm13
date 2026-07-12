# research/m5 — Unbounded adaptivity gap

**Status:** Primary theorems **PROVED** (analytic + certificates)  
**Novelty packaging:** known phenomenon, exact infinite family, CHARM scar  
**Product:** see `PRODUCT_DELTA.md`

## Central result

At inspection budget **2**:

- Adaptive: `D = 1` for every k in the k-pair family  
- Nonadaptive: `D = 2/k`  
- Gap → 1, ratio → ∞ as branching k grows  
- Myopic greedy ratio k/2 → ∞  

## Start here

1. `RESULT.md`  
2. `PROOFS/UNBOUNDED_ADAPTIVITY_GAP.md`  
3. `EXPERIMENTS/test_m5.py`  
4. `PRODUCT_DELTA.md`  

## Reproduce

```powershell
cd C:\Users\coldb\charm13\research\m5\EXPERIMENTS
python test_m5.py
```

## Relation to M4

M4: one gap of 1/2, minimality n=4.  
M5: **unbounded** gap envelope + greedy failure + checklist incompleteness.
