# Theorem M5-T2/T3 — Sharp root-arity law

**Status:** PROVED (analytic) + machine-checked for $K\in\{2,\ldots,7\}$  
**Novelty posture:** `PROVED — NOVELTY UNRESOLVED`  
**Canonical writeup:** `../SEED_THEOREMS.md` §§5  

## Statements

**Root-arity bound.** For any deterministic adaptive budget-two policy whose first query has $k$ nonempty active outcomes,

$$
V(\pi)\le k\,D_2^{\mathrm{na}}(P,Q).
$$

If every available query has active arity $\le K$, then $D_2^{\mathrm{ad}}\le K\,D_2^{\mathrm{na}}$.

**Sharpness.** For every integer $K\ge 2$ there exists a finite OPEN query system with

$$
D_2^{\mathrm{ad}}=1,\qquad D_2^{\mathrm{na}}=\frac1K,
$$

hence

$$
G_2(K)=1-\frac1K.
$$

## Construction (sketch)

Worlds $(i,x)$ with $i\in[K]$, $x\in\{0,1\}^K$. $P$ uniform on $x_i=0$; $Q$ uniform on $x_i=1$. Gate $g(i,x)=i$; bits $b_j(i,x)=x_j$. Adaptive: ask gate then $b_i$. Nonadaptive: every pair evaluates to TV $1/K$.

## Relation to k-pair family

The habitat family with off-branch `na` achieves only $D_2^{\mathrm{na}}=2/k$. See `UNBOUNDED_ADAPTIVITY_GAP.md`. It does **not** contradict sharpness: different observation maps.

## Certificates

```text
research/m5/EXPERIMENTS/m5_exact.py
research/m5/EXPERIMENTS/test_m5_exact.py
```
