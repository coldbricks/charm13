# Support-constrained extremal curve $G_2(K,r)$

**Status:** OPEN (partial envelope only)

## Definition

$$
G_2(K,r)
=\sup\bigl\{
  D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}
  :\ \text{active arity}\le K,\ |S_\mu|\le r
\bigr\}.
$$

## Known envelope (Proposition 6.1)

A gain-bearing root branch must contain both signs, so at most

$$
m\le\min\Bigl\{K,\Bigl\lfloor\frac r2\Bigr\rfloor\Bigr\}
$$

branches can gain. Combined with the root-arity argument this constrains how much of the adaptive value can sit above the static optimum, but a complete matching construction for every $(K,r)$ is **not** claimed.

## Known points

| $(K,r)$ | Value | Source |
|-----------|-------|--------|
| any $K$, $r\le 3$ | $G_2=0$ at $B=2$ | Flattening $r\le B+1=3$ |
| $K=2$, $r=4$ | $G_2=1/2$ | M4 butterfly / Theorem 5.3 at $K=2$ |
| arity $\le K$, unrestricted $r$ | $G_2(K)=1-1/K$ | Theorem 5.3 |

## Next attacks

1. Prove or kill $G_2(K,r)=(1-1/m_*)$ with $m_*=\min(K,\lfloor r/2\rfloor)$ under suitable mass balance.  
2. Enumerate small $(K,r)$ with independent DP solvers.  
3. Store minimal counterexamples in `COUNTEREXAMPLES/` if the envelope fails.
