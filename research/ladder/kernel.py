"""Shared exact-rational ladder kernel (k-pair family + D_B)."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from typing import Callable, Hashable

Zero = Fraction(0)
One = Fraction(1)


def half(x: Fraction) -> Fraction:
    return x / 2


@dataclass(frozen=True)
class Query:
    name: str
    cost: int
    obs: tuple[Hashable, ...]


@dataclass
class Instance:
    name: str
    n: int
    p: tuple[Fraction, ...]
    q: tuple[Fraction, ...]
    queries: tuple[Query, ...]


def f(*nums: int) -> tuple[Fraction, ...]:
    s = sum(nums)
    return tuple(Fraction(x, s) for x in nums)


def l1_mass(p, q, mask: int) -> Fraction:
    sp = sq = Zero
    i, m = 0, mask
    while m:
        if m & 1:
            sp += p[i]
            sq += q[i]
        m >>= 1
        i += 1
    return abs(sp - sq)


def partition_l1(p, q, mask: int, key_fn: Callable[[int], Hashable]) -> Fraction:
    cells: dict[Hashable, list[int]] = {}
    i, m = 0, mask
    while m:
        if m & 1:
            cells.setdefault(key_fn(i), []).append(i)
        m >>= 1
        i += 1
    tot = Zero
    for idxs in cells.values():
        tot += abs(sum((p[j] for j in idxs), Zero) - sum((q[j] for j in idxs), Zero))
    return tot


def adaptive_W(inst: Instance, budget: int) -> Fraction:
    p, q, queries = inst.p, inst.q, inst.queries
    full = (1 << inst.n) - 1

    @lru_cache(maxsize=None)
    def W(mask: int, b: int, used: int) -> Fraction:
        best = l1_mass(p, q, mask)
        if b <= 0 or mask == 0:
            return best
        for j, qu in enumerate(queries):
            if (used >> j) & 1 or qu.cost > b:
                continue
            buckets: dict[Hashable, int] = {}
            i, mm = 0, mask
            while mm:
                if mm & 1:
                    o = qu.obs[i]
                    buckets[o] = buckets.get(o, 0) | (1 << i)
                mm >>= 1
                i += 1
            sub = sum((W(sm, b - qu.cost, used | (1 << j)) for sm in buckets.values()), Zero)
            if sub > best:
                best = sub
        return best

    return W(full, budget, 0)


def nonadaptive_W(inst: Instance, budget: int) -> Fraction:
    p, q, queries = inst.p, inst.q, inst.queries
    full = (1 << inst.n) - 1
    best = l1_mass(p, q, full)
    m = len(queries)
    for r in range(1, m + 1):
        for idxs in combinations(range(m), r):
            if sum(queries[j].cost for j in idxs) > budget:
                continue

            def key_fn(i: int, idxs=idxs) -> Hashable:
                return tuple(queries[j].obs[i] for j in idxs)

            val = partition_l1(p, q, full, key_fn)
            if val > best:
                best = val
    return best


def D_ad(inst: Instance, B: int) -> Fraction:
    return half(adaptive_W(inst, B))


def D_na(inst: Instance, B: int) -> Fraction:
    return half(nonadaptive_W(inst, B))


def inst_k_pairs(k: int) -> Instance:
    n = 2 * k
    raw_p, raw_q = [], []
    for _ in range(k):
        raw_p.extend([1, 0])
        raw_q.extend([0, 1])
    p, q = f(*raw_p), f(*raw_q)
    which = Query("which", 1, tuple(i // 2 for i in range(n)))
    bits = [
        Query(f"bit{pair}", 1, tuple((i % 2) if i // 2 == pair else "na" for i in range(n)))
        for pair in range(k)
    ]
    return Instance(f"k_pairs_{k}", n, p, q, (which, *bits))


# ----- Closed forms (theorems) -----


def theory_D_ad(k: int, B: int) -> Fraction:
    if B <= 0:
        return Zero
    if B == 1:
        return Fraction(1, k)  # best single bit
    return One  # B >= 2: which then bit


def theory_D_na(k: int, B: int) -> Fraction:
    if B <= 0:
        return Zero
    # best: min(B, k) distinct bit queries → TV = min(B,k)/k
    return Fraction(min(B, k), k)


def theory_gap(k: int, B: int) -> Fraction:
    return theory_D_ad(k, B) - theory_D_na(k, B)


def myopic_greedy_tv(k: int, B: int) -> Fraction:
    """Myopic never picks which (TV 0); each step gains one new bit → B/k capped at 1."""
    return Fraction(min(B, k), k)


def camouflage_capacity_adaptive(B: int, eps: Fraction) -> int | None:
    """Max k such that D_B^ad(P_k,Q_k) <= eps.

    For B >= 2, D=1 for all k, so capacity is 0 if eps < 1, else infinite symbolically.
    Return 0 if eps < 1 and B >= 2; return None meaning +∞ if eps >= 1.
    """
    if eps >= 1:
        return None  # +∞
    if B >= 2:
        return 0  # cannot achieve D<=eps<1 for any k
    # B == 1: D = 1/k <= eps ⇒ k >= 1/eps
    # capacity as max k with D<=eps: 1/k <= eps ⇒ k >= 1/eps, all large k work
    # sup k = +∞
    return None


def camouflage_capacity_nonadaptive(B: int, eps: Fraction) -> int | None:
    """Max k with D_B^na <= eps: B/k <= eps ⇒ k >= B/eps if B<=k...

    D_na = min(B,k)/k. For k >= B, D = B/k <= eps ⇒ k >= B/eps.
    For all k >= ceil(B/eps), satisfied. Again sup = +∞.
    Min k such that still D > eps is the interesting dual.

    Define capacity as max "safe branching" under nonadaptive for which D_na <= eps:
    actually any k >= ceil(B/eps) is safe. Capacity infinite.

    Dual risk: max D_na for given k is B/k. Product: under nonadaptive, large k is safer.

    Define C^risk_na(k,B) = B/k. Document both.
    """
    if eps >= 1:
        return None
    if B == 0:
        return None
    # smallest k with D_na <= eps when using best nonadaptive: need min(B,k)/k <= eps
    # if k <= B: D=1, need eps>=1
    # if k > B: B/k <= eps ⇒ k >= B/eps
    # all k >= ceil(B/eps) work; max k unbounded
    return None


def min_k_nonadaptive_below_eps(B: int, eps: Fraction) -> int:
    """Minimal k such that D_B^na(P_k,Q_k) <= eps (for eps < 1, B>=1)."""
    if eps <= 0:
        raise ValueError("eps must be > 0")
    if eps >= 1:
        return 1
    # need B/k <= eps and k >= B (else D=1 if k<=B... if k < B, min(B,k)/k = 1)
    # so need k > B and k >= B/eps. Actually k >= B gives D = B/k only when k>=B;
    # for k < B, D_na = 1.
    # So k >= max(B, ceil(B/eps)) but if k=B, D=1. So k >= floor(B/eps)+1 carefully.
    # B/k <= eps ⇒ k >= B/eps. Also need k > B if we need D < 1... 
    # If B/eps > B i.e. eps < 1, then k >= ceil(B/eps) > B when B/eps > B i.e. always for eps<1? 
    # B/eps > B iff 1/eps > 1 iff eps < 1. Yes ceil(B/eps) >= B+ something.
    # For B=2, eps=1/2: k >= 4, D=2/4=1/2 <= 1/2 ok.
    from math import ceil

    return max(B + 1, int(ceil(float(B / eps) - 1e-15)))


# ----- m-bit payload per branch (M12+) -----


def theory_D_ad_mbit(k: int, m: int, B: int) -> Fraction:
    """k branches; active branch has m bits. P: all-zero payload; Q: all-one payload.

    Queries: which + bit_{i,j} for branch i bit j.
    Adaptive: which then all m bits of that branch → need B >= 1+m for D=1.
    With B <= m: can read at most B bits of one branch after which? 
      - B=0: 0
      - without enough for full separation: if only which: TV 0
      - adaptive optimal:
        * if B >= 1+m: D=1
        * if B == 0: 0
        * if 1 <= B <= m: best is pick a branch somehow... 
          Without which, reading bit j of branch i: if P/Q differ on that bit fully on that branch mass 1/k.
          Actually each bit of each branch: under P bit always 0 on active, under Q always 1.
          So bit_{i,j} alone: same as single bit in 1-bit case, TV=1/k.
          After reading t < m bits of same branch (with or without which), still not fully separated if we need all m? 
          Wait - if ANY bit differs between P and Q fully, ONE bit of the correct branch separates completely!
          
    Careful redesign: if all bits are 0 under P and 1 under Q on the active branch, then a SINGLE bit of the active branch already gives perfect separation on that mass. Then which+one bit = B=2 still perfect, m is irrelevant.

    Correct m-bit hard version: separation requires the FULL m-bit string.
    Model: payload is a codeword.
    P: active branch has codeword 0^m
    Q: active branch has codeword drawn from a set that matches any proper subset of coordinates' marginals...
    
    Simpler hard m-bit model used in literature:
    P and Q differ only in the AND of all m bits / or parity of m bits on active branch.
    
    Use PARITY model:
    Active branch i uniform.
    P: m free bits uniform with even parity on active branch (or fixed: bits uniform subject to xor=0)
    Actually keep discrete finite support small:
    
    Worlds: (i, x) i in [k], x in {0,1}^m
    Too big for DP when m large.

    Closed form only without full DP:

    Model M12 (threshold):
    - which reveals i
    - test_i costs 1, reveals whether payload on i is "P-type" or "Q-type" (one composite test)
    That's back to 1-bit.

    Model M12 (m sequential bits, need all):
    On active branch, P has bits (0,0,...,0), Q has bits (1,1,...,1). 
    Any single bit of the active branch FULLY separates P from Q on that branch's mass!
    So D_ad with which+any bit_i,* = 1 at B=2 still.

    To make m matter, use:
    **Matched marginals on each bit, global parity differs** (like M4-C) per branch:
    On active branch, P: uniform even parity strings; Q: uniform odd parity.
    Each single bit is Bern(1/2) under both.
    Need which + all m bits to see parity? Actually need which + enough to compute parity: m bits of that branch.
    Adaptive B = 1+m: which then m bits → know parity → D=1.
    Nonadaptive: hard.

    Support size k*2^m - only closed form theory, verify small m,k with DP when 2k*2^m small.

    For closed form adaptive:
    - B >= 1+m: D=1 (which + m bits of that branch)
    - B <= m: without full m bits on one branch after selecting it...
    
    I'll implement inst and theory carefully for small cases and analytic lower/upper bounds.
    """
    raise NotImplementedError("use theory_D_ad_parity / inst_k_parity")


def theory_D_ad_parity(k: int, m: int, B: int) -> Fraction:
    """k branches, m-bit even/odd parity payloads (see inst_k_parity).

    Adaptive:
      B=0 → 0
      If B < 1+m: cannot always finish which+m bits.
        Lower bound strategies:
        - spend B on bit queries of one fixed branch (no which): each bit is Bern1/2 under both → TV 0 for any nonadaptive bits on fixed branch without knowing if active!
        Actually if we don't know active branch, reading bit j of branch i:
          Under P: with prob 1/k branch i active and bit is Bern on even-parity conditioned...
        This gets messy. Restrict analytic theorems to:
        D_ad = 1 if B >= 1+m else use DP only for small params.
    """
    if B <= 0:
        return Zero
    if B >= 1 + m:
        return One
    # partial budget: at best separate mass if we guess branch and read m bits with B=m (no which) 
    # only works if we pick correct branch without which - probability 1/k of picking right branch's m bits when B>=m
    if B >= m:
        # non-adaptive style fixed branch full read: TV = 1/k
        # adaptive cannot do better than 1 without which for identifying branch... 
        # With B = m: read m bits of branch 0. If that branch inactive, all bits might still look like noise.
        # For inactive branch under our model: we need to define attributes on inactive branches.
        return Fraction(1, k)  # conservative closed form used as theory target for B=m < 1+m
    return Zero  # B < m: not enough bits for parity on any branch


def theory_D_na_parity(k: int, m: int, B: int) -> Fraction:
    """Rough upper/exact for simple policy class: each 'full branch read' costs m.

    Number of full branch parity tests affordable: t = B // m.
    Each fully read branch contributes TV 1/k if we get full m bits.
    which costs 1 and doesn't separate alone.
    Best: t = B//m full branches → TV = min(1, t/k).
    If B >= 1+m, can do which+one branch in nonadaptive set cost 1+m → TV=1.
    """
    if B <= 0:
        return Zero
    if B >= 1 + m:
        # nonadaptive set {which, bit_0_0, ..., bit_0_{m-1}} cost 1+m, perfect
        return One
    t = B // m
    return Fraction(min(t, k), k)


def inst_k_parity(k: int, m: int) -> Instance:
    """k branches; on each branch all 2^m patterns as separate worlds? Too many.

    Slim model: only two worlds per branch — Even and Odd prototypes.
    World (i, 0): branch i, even-type (P-support)
    World (i, 1): branch i, odd-type (Q-support)
    P: uniform on (i,0); Q: uniform on (i,1).

    Queries:
      which: i
      fulltest_i: returns type 0/1 on branch i (costs m) — composite
    OR bit queries that only together reveal type:

    For bit queries with matched single-bit marginals while type differs:
    Represent type by m bits where even-type = 0^m and odd-type = e_1 = (1,0,...,0) 
    then bit0 separates! Bad.

    Use: even-type world responds to bit_j with obs 0 for all j (degenerate),
    odd-type responds 1 for all j — again one bit separates.

    True parity coupling needs multiple x per branch. Support k*2^m.

    For m=2, k=2: n=8 worlds — OK for DP.
    World index: i * 2^m + x_int, x_int in 0..2^m-1
    P: for each i, mass 1/k * 1/2^{m-1} on even parity x
    Q: similarly on odd parity x
    """
    n = k * (1 << m)
    # masses
    raw_p = [0] * n
    raw_q = [0] * n
    half_m = 1 << (m - 1)  # number of even/odd strings
    for i in range(k):
        for x in range(1 << m):
            parity = bin(x).count("1") % 2
            idx = i * (1 << m) + x
            if parity == 0:
                raw_p[idx] = 1  # uniform later among evens: use weight 1 each
            else:
                raw_q[idx] = 1
    p = f(*raw_p)
    q = f(*raw_q)
    which = Query("which", 1, tuple(i for i in range(k) for _ in range(1 << m)))
    bits = []
    for i in range(k):
        for j in range(m):
            obs = []
            for ii in range(k):
                for x in range(1 << m):
                    if ii != i:
                        obs.append("na")
                    else:
                        obs.append((x >> j) & 1)
            bits.append(Query(f"b{i}_{j}", 1, tuple(obs)))
    return Instance(f"k{k}_m{m}_parity", n, p, q, (which, *bits))


def theory_D_ad_parity_tight(k: int, m: int, B: int) -> Fraction:
    """Tight adaptive for parity family (analytic).

    Adaptive which-then-m-bits costs 1+m and yields TV=1.
    With budget m (no room for which+full): read m bits of a fixed branch → TV=1/k.
    With budget < m: cannot complete parity on any branch → TV=0.
    """
    if B <= 0:
        return Zero
    if B >= 1 + m:
        return One
    if B >= m:
        return Fraction(1, k)
    return Zero


def theory_D_na_parity_tight(k: int, m: int, B: int) -> Fraction:
    """Nonadaptive: must precommit which branches to fully instrument (m bits each).

    which alone does not separate; which + m bits on one fixed branch only separates
    when that branch is active → TV=1/k, cost 1+m.
    Best: t=floor(B/m) fully instrumented branches → TV=min(1,t/k).
    Perfect nonadaptive requires t=k ⇒ B >= k*m.
    """
    if B <= 0:
        return Zero
    t = B // m
    return Fraction(min(t, k), k)

