"""M5 exact rational D_B engine (fork of m4 enum_core with k-pair family)."""

from __future__ import annotations

import sys
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from pathlib import Path
from typing import Callable, Hashable, Iterable

# allow importing sibling patterns
Zero = Fraction(0)
One = Fraction(1)


def _half(x: Fraction) -> Fraction:
    return x / 2


from dataclasses import dataclass


@dataclass(frozen=True)
class Query:
    name: str
    cost: int
    obs: tuple[Hashable, ...]
    requires: tuple[int, ...] = ()


@dataclass
class Instance:
    name: str
    n: int
    p: tuple[Fraction, ...]
    q: tuple[Fraction, ...]
    queries: tuple[Query, ...]

    def validate(self) -> None:
        assert self.n == len(self.p) == len(self.q)
        assert sum(self.p, Zero) == One
        assert sum(self.q, Zero) == One
        for qu in self.queries:
            assert len(qu.obs) == self.n
            assert qu.cost > 0


def f(*nums: int) -> tuple[Fraction, ...]:
    s = sum(nums)
    assert s > 0
    return tuple(Fraction(x, s) for x in nums)


def l1_mass(p: tuple[Fraction, ...], q: tuple[Fraction, ...], mask: int) -> Fraction:
    sp = Zero
    sq = Zero
    i = 0
    m = mask
    while m:
        if m & 1:
            sp += p[i]
            sq += q[i]
        m >>= 1
        i += 1
    return abs(sp - sq)


def partition_l1(
    p: tuple[Fraction, ...],
    q: tuple[Fraction, ...],
    mask: int,
    key_fn: Callable[[int], Hashable],
) -> Fraction:
    cells: dict[Hashable, list[int]] = {}
    i = 0
    m = mask
    while m:
        if m & 1:
            cells.setdefault(key_fn(i), []).append(i)
        m >>= 1
        i += 1
    total = Zero
    for idxs in cells.values():
        sp = sum((p[j] for j in idxs), Zero)
        sq = sum((q[j] for j in idxs), Zero)
        total += abs(sp - sq)
    return total


def adaptive_W(inst: Instance, budget: int) -> Fraction:
    inst.validate()
    n = inst.n
    p = inst.p
    q = inst.q
    queries = inst.queries
    full = (1 << n) - 1

    @lru_cache(maxsize=None)
    def W(mask: int, b: int, used: int) -> Fraction:
        best = l1_mass(p, q, mask)
        if b <= 0 or mask == 0:
            return best
        for j, qu in enumerate(queries):
            if (used >> j) & 1:
                continue
            if qu.cost > b:
                continue
            if any(not ((used >> r) & 1) for r in qu.requires):
                continue
            buckets: dict[Hashable, int] = {}
            i = 0
            mm = mask
            while mm:
                if mm & 1:
                    o = qu.obs[i]
                    buckets[o] = buckets.get(o, 0) | (1 << i)
                mm >>= 1
                i += 1
            sub = Zero
            new_used = used | (1 << j)
            for submask in buckets.values():
                sub += W(submask, b - qu.cost, new_used)
            if sub > best:
                best = sub
        return best

    return W(full, budget, 0)


def nonadaptive_W(inst: Instance, budget: int, *, path_free: bool = False) -> Fraction:
    inst.validate()
    n = inst.n
    p = inst.p
    q = inst.q
    queries = inst.queries
    m = len(queries)
    full = (1 << n) - 1
    best = l1_mass(p, q, full)

    for r in range(0, m + 1):
        for idxs in combinations(range(m), r):
            cost = sum(queries[j].cost for j in idxs)
            if cost == 0:
                continue
            if cost > budget:
                continue
            if not path_free:
                chosen = set(idxs)
                if any(req not in chosen for j in idxs for req in queries[j].requires):
                    continue

            def key_fn(i: int, idxs=idxs) -> Hashable:
                return tuple(queries[j].obs[i] for j in idxs)

            val = partition_l1(p, q, full, key_fn)
            if val > best:
                best = val
    return best


def D_adaptive(inst: Instance, budget: int) -> Fraction:
    return _half(adaptive_W(inst, budget))


def D_nonadaptive(inst: Instance, budget: int, **kw) -> Fraction:
    return _half(nonadaptive_W(inst, budget, **kw))


def gap(inst: Instance, budget: int) -> tuple[Fraction, Fraction, Fraction]:
    da = D_adaptive(inst, budget)
    dn = D_nonadaptive(inst, budget)
    return da, dn, da - dn


# ---------------------------------------------------------------------------
# Flagship family: k labeled pairs (branch, bit)
# ---------------------------------------------------------------------------


def inst_k_pairs(k: int) -> Instance:
    """P: uniform over (pair=i, bit=0); Q: uniform over (pair=i, bit=1).

    Queries: which (pair id), bit_i for each i.
    Adaptive B=2: perfect. Nonadaptive B=2: at most 2/k.
    """
    assert k >= 1
    n = 2 * k
    raw_p = []
    raw_q = []
    for i in range(k):
        raw_p.extend([1, 0])  # bit0, bit1
        raw_q.extend([0, 1])
    p = f(*raw_p)
    q = f(*raw_q)
    which = Query("which", 1, tuple(i // 2 for i in range(n)))
    bits = []
    for pair in range(k):
        obs = tuple((i % 2) if (i // 2 == pair) else "na" for i in range(n))
        bits.append(Query(f"bit{pair}", 1, obs))
    return Instance(f"k_pairs_{k}", n, p, q, (which, *bits))


def myopic_single_tv(inst: Instance, qindex: int) -> Fraction:
    """TV from issuing only queries[qindex]."""
    qu = inst.queries[qindex]

    def key_fn(i: int) -> Hashable:
        return qu.obs[i]

    return _half(partition_l1(inst.p, inst.q, (1 << inst.n) - 1, key_fn))


def greedy_depth2_tv(inst: Instance) -> Fraction:
    """Myopic greedy: pick max single-query TV, then best second given first (approx via
    evaluating all second queries after fixing first as the myopic choice).

    More precisely: choose q1 = argmax single TV; then among remaining, choose q2
    maximizing nonadaptive {q1,q2} TV (still nonadaptive pair — true adaptive
    second step after q1 would condition; for bit-first this is fine).
    """
    m = len(inst.queries)
    best_j = 0
    best_tv = Fraction(-1)
    for j in range(m):
        tv = myopic_single_tv(inst, j)
        if tv > best_tv:
            best_tv = tv
            best_j = j
    # second: best partner in nonadaptive pair (upper bounds weak greedy)
    # True adaptive after q1: compute properly
    return adaptive_after_first(inst, best_j)


def adaptive_after_first(inst: Instance, j_first: int) -> Fraction:
    """TV of optimal depth-2 policy that is forced to start with query j_first."""
    # Use restricted query order via temporary cost: only allow j_first first by
    # computing leaf L1 after first split then best second in each cell.
    p, q = inst.p, inst.q
    qu = inst.queries[j_first]
    n = inst.n
    full = (1 << n) - 1
    buckets: dict[Hashable, int] = {}
    i = 0
    mm = full
    while mm:
        if mm & 1:
            o = qu.obs[i]
            buckets[o] = buckets.get(o, 0) | (1 << i)
        mm >>= 1
        i += 1
    total = Zero
    for submask in buckets.values():
        # best: stop or one more query
        cell_best = l1_mass(p, q, submask)
        for j2, qu2 in enumerate(inst.queries):
            if j2 == j_first:
                continue
            if qu2.cost > 1:
                continue
            # split submask
            parts: dict[Hashable, int] = {}
            i = 0
            mm = submask
            while mm:
                if mm & 1:
                    o = qu2.obs[i]
                    parts[o] = parts.get(o, 0) | (1 << i)
                mm >>= 1
                i += 1
            sub = sum((l1_mass(p, q, sm) for sm in parts.values()), Zero)
            if sub > cell_best:
                cell_best = sub
        total += cell_best
    return _half(total)


def greedy_vs_optimal(inst: Instance) -> dict:
    m = len(inst.queries)
    myopic = [myopic_single_tv(inst, j) for j in range(m)]
    j_star = max(range(m), key=lambda j: myopic[j])
    greedy_tv = adaptive_after_first(inst, j_star)
    opt = D_adaptive(inst, 2)
    return {
        "myopic_tvs": myopic,
        "greedy_first": inst.queries[j_star].name,
        "greedy_tv": greedy_tv,
        "optimal_tv": opt,
        "ratio_opt_over_greedy": (opt / greedy_tv) if greedy_tv > 0 else None,
    }


if __name__ == "__main__":
    for k in [2, 3, 4, 5, 8, 12]:
        inst = inst_k_pairs(k)
        da, dn, g = gap(inst, 2)
        gv = greedy_vs_optimal(inst)
        print(
            f"k={k:2d}  D_ad={da}  D_na={dn}  gap={g}  "
            f"theory_na={Fraction(min(2, k), k)}  "
            f"greedy={gv['greedy_tv']} first={gv['greedy_first']} "
            f"ratio={gv['ratio_opt_over_greedy']}"
        )
