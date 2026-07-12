# research/m5 — Extremal geometry of budgeted inspection

**Status:** Seed package **PROVED in-model** (analytic + certificates); novelty unresolved  
**Terminal label:** `PROVED — NOVELTY UNRESOLVED`  
**Product:** see `PRODUCT_DELTA.md`

## Crown result

At inspection budget **2**, with query active-arity at most $K$:

$$
G_2(K) = \sup\bigl(D_2^{\mathrm{ad}} - D_2^{\mathrm{na}}\bigr) = 1 - \frac1K.
$$

Matching construction: $D_2^{\mathrm{ad}}=1$, $D_2^{\mathrm{na}}=1/K$.

Companion theorems: flattening ($r\le B+1$ kills the gap), four-world butterfly uniqueness, first stability statement.

## Habitat application (k-pair)

CHARM-shaped **which-then-bit** family (off-branch `na`):

- Adaptive: $D=1$ for every $k$
- Nonadaptive: $D=2/k$
- Gap $1-2/k\to 1$; greedy ratio $k/2\to\infty$

Valid and product-critical; **not** the sharp universal envelope (see `RESULT.md` correction table).

## Start here

1. `RESULT.md` — terminal status and correction note  
2. `MODEL.md` — frozen definitions  
3. `SEED_THEOREMS.md` — full seed proofs  
4. `PROOFS/UNBOUNDED_ADAPTIVITY_GAP.md` — k-pair + greedy  
5. `EXPERIMENTS/test_m5_exact.py` + `test_m5.py`  
6. `PRODUCT_DELTA.md`  

## Reproduce

```powershell
cd research\m5\EXPERIMENTS
python test_m5_exact.py
python test_m5.py
```

## Relation to M4

M4: one gap of $1/2$, support $n=4$.  
M5: proves that binary budget-two gap $1/2$ is **globally maximal**, support-minimal, and uniquely the butterfly; then lifts to sharp arity-$K$ law $1-1/K$.
