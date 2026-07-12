"""Exact-rational certificates for CHARM13 M5.

The code is deliberately small and independent of the M4 enumerator. It verifies
finite instances; analytic proofs remain in SEED_THEOREMS.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from typing import Hashable, Iterable, Sequence

F = Fraction
ZERO = F(0)
ONE = F(1)


@dataclass(frozen=True)
class Query:
    name: str
    obs: tuple[Hashable, ...]


@dataclass(frozen=True)
class Instance:
    p: tuple[Fraction, ...]
    q: tuple[Fraction, ...]
    queries: tuple[Query, ...]

    def validate(self) -> None:
        if len(self.p) != len(self.q):
            raise ValueError("P and Q lengths differ")
        if sum(self.p, ZERO) != ONE or sum(self.q, ZERO) != ONE:
            raise ValueError("P and Q must each sum to one")
        if any(x < 0 for x in self.p + self.q):
            raise ValueError("negative probability")
        for query in self.queries:
            if len(query.obs) != len(self.p):
                raise ValueError(f"bad observation length for {query.name}")



def partition_value(inst: Instance, query_indices: Sequence[int]) -> Fraction:
    """TV of the joint output of a fixed query set."""
    inst.validate()
    cells: dict[tuple[Hashable, ...], list[int]] = {}
    for w in range(len(inst.p)):
        key = tuple(inst.queries[j].obs[w] for j in query_indices)
        cells.setdefault(key, []).append(w)
    l1 = ZERO
    for worlds in cells.values():
        pm = sum((inst.p[w] for w in worlds), ZERO)
        qm = sum((inst.q[w] for w in worlds), ZERO)
        l1 += abs(pm - qm)
    return l1 / 2



def nonadaptive_value(inst: Instance, budget: int = 2) -> Fraction:
    """Best globally addressable static set of at most budget unit-cost queries."""
    best = partition_value(inst, ())
    m = len(inst.queries)
    for size in range(1, min(budget, m) + 1):
        for idxs in combinations(range(m), size):
            best = max(best, partition_value(inst, idxs))
    return best



def depth2_policy_value(
    inst: Instance,
    root: int,
    continuation_by_output: dict[Hashable, int | None],
) -> Fraction:
    """Value of root followed by one output-dependent continuation."""
    inst.validate()
    root_query = inst.queries[root]
    cells: dict[tuple[Hashable, Hashable | None], list[int]] = {}
    for w, root_output in enumerate(root_query.obs):
        nxt = continuation_by_output.get(root_output)
        second_output = None if nxt is None else inst.queries[nxt].obs[w]
        cells.setdefault((root_output, second_output), []).append(w)
    l1 = ZERO
    for worlds in cells.values():
        pm = sum((inst.p[w] for w in worlds), ZERO)
        qm = sum((inst.q[w] for w in worlds), ZERO)
        l1 += abs(pm - qm)
    return l1 / 2



def adaptive_depth2_value(inst: Instance) -> Fraction:
    """Exhaustive best deterministic depth-two policy."""
    inst.validate()
    best = partition_value(inst, ())
    m = len(inst.queries)
    for root_idx, root in enumerate(inst.queries):
        outputs = tuple(dict.fromkeys(root.obs))
        options = tuple([None, *range(m)])
        for choices in product(options, repeat=len(outputs)):
            mapping = dict(zip(outputs, choices, strict=True))
            value = depth2_policy_value(inst, root_idx, mapping)
            if value > best:
                best = value
    return best



def m4_butterfly() -> Instance:
    p = (F(1, 2), ZERO, F(1, 2), ZERO)
    q = (ZERO, F(1, 2), ZERO, F(1, 2))
    queries = (
        Query("gate", (0, 0, 1, 1)),
        Query("left", (0, 1, 0, 0)),
        Query("right", (0, 0, 1, 0)),
    )
    return Instance(p, q, queries)



def sharp_arity_instance(k: int) -> Instance:
    """Construction proving G_2(k) = 1 - 1/k.

    Worlds are (i, x) with i in [k] and x in {0,1}^k.
    P is uniform on x_i=0; Q is uniform on x_i=1.
    """
    if k < 2:
        raise ValueError("k must be at least two")

    worlds: list[tuple[int, tuple[int, ...]]] = []
    for i in range(k):
        for x in product((0, 1), repeat=k):
            worlds.append((i, tuple(x)))

    mass = F(1, k * (2 ** (k - 1)))
    p = tuple(mass if x[i] == 0 else ZERO for i, x in worlds)
    q = tuple(mass if x[i] == 1 else ZERO for i, x in worlds)

    queries = [Query("gate", tuple(i for i, _ in worlds))]
    for j in range(k):
        queries.append(Query(f"bit_{j}", tuple(x[j] for _, x in worlds)))

    return Instance(p, q, tuple(queries))



def sharp_adaptive_policy_value(k: int) -> Fraction:
    inst = sharp_arity_instance(k)
    mapping = {i: i + 1 for i in range(k)}
    return depth2_policy_value(inst, 0, mapping)



def canonical_binary_queries(n: int) -> tuple[tuple[int, ...], ...]:
    """Nonconstant binary cuts modulo output complement."""
    result = []
    for bits in product((0, 1), repeat=n):
        if bits[0] != 0:
            continue
        if all(bit == bits[0] for bit in bits):
            continue
        result.append(tuple(bits))
    return tuple(result)



def four_world_extremal_cores() -> list[tuple[tuple[int, ...], ...]]:
    """Enumerate raw (g,l,r) triples for the uniform +/- four-atom model.

    The analytic classification is in Theorem 7.1. This function is only an
    independent finite certificate.
    """
    p = (F(1, 2), ZERO, F(1, 2), ZERO)
    q = (ZERO, F(1, 2), ZERO, F(1, 2))
    cuts = canonical_binary_queries(4)
    found: list[tuple[tuple[int, ...], ...]] = []

    for g, left, right in product(cuts, repeat=3):
        inst = Instance(
            p,
            q,
            (Query("g", g), Query("l", left), Query("r", right)),
        )
        outputs = tuple(dict.fromkeys(g))
        if set(outputs) != {0, 1}:
            continue
        adaptive = depth2_policy_value(inst, 0, {0: 1, 1: 2})
        static = nonadaptive_value(inst, 2)
        if adaptive == ONE and static == F(1, 2):
            found.append((g, left, right))
    return found



def _all_grid_distributions(n: int, denominator: int) -> Iterable[tuple[Fraction, ...]]:
    """All probability vectors with coordinates in multiples of 1/denominator."""
    def rec(prefix: list[int], remaining: int, slots: int):
        if slots == 1:
            yield tuple(F(x, denominator) for x in [*prefix, remaining])
            return
        for x in range(remaining + 1):
            yield from rec([*prefix, x], remaining - x, slots - 1)

    yield from rec([], denominator, n)



def sanity_small_support_no_gap(max_n: int = 3, denominator: int = 3) -> int:
    """Finite sanity sweep for Theorem 4.1 at B=2.

    Enumerates every binary query family consisting of all canonical cuts and
    every P,Q grid pair. The theorem itself is analytic and not dependent on
    this bounded grid.
    """
    checked = 0
    for n in range(1, max_n + 1):
        cuts = canonical_binary_queries(n)
        queries = tuple(Query(f"q{i}", cut) for i, cut in enumerate(cuts))
        for p in _all_grid_distributions(n, denominator):
            for q in _all_grid_distributions(n, denominator):
                inst = Instance(p, q, queries)
                if adaptive_depth2_value(inst) != nonadaptive_value(inst, 2):
                    raise AssertionError((n, p, q))
                checked += 1
    return checked



def main() -> None:
    m4 = m4_butterfly()
    print("M4 adaptive:", adaptive_depth2_value(m4))
    print("M4 nonadaptive:", nonadaptive_value(m4, 2))

    for k in range(2, 8):
        inst = sharp_arity_instance(k)
        ad = sharp_adaptive_policy_value(k)
        na = nonadaptive_value(inst, 2)
        print(f"K={k}: adaptive={ad}, nonadaptive={na}, gap={ad-na}")

    cores = four_world_extremal_cores()
    print("Raw four-world extremal triples modulo cut complement:", len(cores))
    for core in cores:
        print(core)


if __name__ == "__main__":
    main()
