# Equality cases

## $K=2$ (binary) — resolved

Theorem 7.1: under four active worlds, perfect adaptive depth-two policy, and static pairs $\le 1/2$, the core is uniquely the M4 butterfly up to natural symmetries (world relabel, $P/Q$ swap, branch swap, output complements, query rename).

Independent finite check: `four_world_extremal_cores()` finds four raw triples related by those symmetries.

## $K>2$ — open

Classify all signed experiments attaining

$$
D_2^{\mathrm{ad}}=1,\qquad D_2^{\mathrm{na}}=1/K.
$$

The address-function construction in Theorem 5.3 is one extremizer. Whether all extremizers are address-function atoms (up to equivalence), orthogonal arrays, signed transportation cycles, or another polytope is unresolved.

## k-pair family

The k-pair habitat saturates adaptive perfect separation at budget 2 but only achieves nonadaptive $2/k$, not $1/k$. It is **not** an equality case of the sharp arity law for the same $K=k$.
