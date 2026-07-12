"""Exact rational budgeted distinguishability D_B / D_B^na.

Finite worlds, deterministic queries, adaptive policies via DP on masks.
Fractions only. Research-only (M4).
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from typing import Callable, Hashable, Iterable


Zero = Fraction(0)
One = Fraction(1)


def _half(x: Fraction) -> Fraction:
    return x / 2


@dataclass(frozen=True)
class Query:
    name: str
    cost: int
    # observation for each world index
    obs: tuple[Hashable, ...]
    # indices of queries that must have been issued (by index) — simple legality
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


def l1_mass(p: tuple[Fraction, ...], q: tuple[Fraction, ...], mask: int) -> Fraction:
    """|P(S)-Q(S)| for S = bits set in mask."""
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
    """sum_cells |P-Q| for worlds in mask partitioned by key_fn(world_index)."""
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
    """Max sum_leaves |P-Q| over adaptive policies cost <= budget on full support."""
    inst.validate()
    n = inst.n
    p = inst.p
    q = inst.q
    queries = inst.queries
    full = (1 << n) - 1

    # requires: map query index -> required prior query indices
    # legality tracked via bitset of used queries (issued along the path)
    m = len(queries)

    @lru_cache(maxsize=None)
    def W(mask: int, b: int, used: int) -> Fraction:
        # best L1 leaf sum on worlds in mask, remaining budget b, queries used bits
        best = l1_mass(p, q, mask)  # stop now
        if b <= 0 or mask == 0:
            return best
        # try each legal unused query (allow re-query? skip used for determinism)
        for j, qu in enumerate(queries):
            if (used >> j) & 1:
                continue
            if qu.cost > b:
                continue
            ok = True
            for r in qu.requires:
                if not ((used >> r) & 1):
                    ok = False
                    break
            if not ok:
                continue
            # split mask by observation
            buckets: dict[Hashable, int] = {}
            i = 0
            mm = mask
            while mm:
                if mm & 1:
                    o = qu.obs[i]
                    buckets[o] = buckets.get(o, 0) | (1 << i)
                mm >>= 1
                i += 1
            # if query gives no split info on this mask, still pay cost
            sub = Zero
            new_used = used | (1 << j)
            for submask in buckets.values():
                sub += W(submask, b - qu.cost, new_used)
            if sub > best:
                best = sub
        return best

    return W(full, budget, 0)


def nonadaptive_W(inst: Instance, budget: int, *, path_free: bool = False) -> Fraction:
    """Max sum_cells |P-Q| over fixed query sets with total cost <= budget.

    path_free=False: respect requires (query only if all requirements also in the set).
    path_free=True: ignore requires (absolute-path nonadaptive model for stress test).
    """
    inst.validate()
    n = inst.n
    p = inst.p
    q = inst.q
    queries = inst.queries
    m = len(queries)
    full = (1 << n) - 1
    best = l1_mass(p, q, full)  # empty query set

    for r in range(0, m + 1):
        for idxs in combinations(range(m), r):
            cost = sum(queries[j].cost for j in idxs)
            if cost > budget or cost == 0:
                if cost == 0 and r == 0:
                    pass
                if cost > budget:
                    continue
            if not path_free:
                chosen = set(idxs)
                legal = True
                for j in idxs:
                    for req in queries[j].requires:
                        if req not in chosen:
                            legal = False
                            break
                    if not legal:
                        break
                if not legal:
                    continue

            def key_fn(i: int, idxs=idxs) -> Hashable:
                return tuple(queries[j].obs[i] for j in idxs)

            val = partition_l1(p, q, full, key_fn)
            if val > best:
                best = val
    return best


def D_adaptive(inst: Instance, budget: int) -> Fraction:
    return _half(adaptive_W(inst, budget))


def D_nonadaptive(inst: Instance, budget: int, *, path_free: bool = False) -> Fraction:
    return _half(nonadaptive_W(inst, budget, path_free=path_free))


def gap(inst: Instance, budget: int, *, path_free_na: bool = False) -> tuple[Fraction, Fraction, Fraction]:
    da = D_adaptive(inst, budget)
    dn = D_nonadaptive(inst, budget, path_free=path_free_na)
    return da, dn, da - dn


# ---------------------------------------------------------------------------
# Constructors for Claim A hunts
# ---------------------------------------------------------------------------


def f(*nums: int) -> tuple[Fraction, ...]:
    """Normalize non-negative ints to a probability tuple."""
    s = sum(nums)
    assert s > 0
    return tuple(Fraction(x, s) for x in nums)


def inst_star_hot_child() -> Instance:
    """Root + 2 children. Exactly one hot under Q; both cold or structured under P.

    Worlds: (L,R) magic bits
      0: 00, 1: 10, 2: 01, 3: 11
    """
    # obs for head_L, head_R, list (always 'LR')
    # worlds 0..3
    head_L = Query("head_L", 1, (0, 1, 0, 1))
    head_R = Query("head_R", 1, (0, 0, 1, 1))
    list_r = Query("list_r", 1, ("LR", "LR", "LR", "LR"))
    # P: equal bits; Q: single hot
    p = f(1, 0, 0, 1)  # 00 and 11
    q = f(0, 1, 1, 0)  # 10 and 01
    return Instance("star_parity", 4, p, q, (list_r, head_L, head_R))


def inst_three_files_one_hot() -> Instance:
    """3 files, P all cold; Q exactly one hot. Queries = head each."""
    # worlds: 0=000, 1=100, 2=010, 3=001
    p = f(1, 0, 0, 0)
    q = f(0, 1, 1, 1)
    ha = Query("hA", 1, (0, 1, 0, 0))
    hb = Query("hB", 1, (0, 0, 1, 0))
    hc = Query("hC", 1, (0, 0, 0, 1))
    return Instance("three_one_hot", 4, p, q, (ha, hb, hc))


def inst_asymmetric_branch() -> Instance:
    """Classic adaptive gap candidate:

    First query indicates which expensive query to run.
    Worlds 0,1,2,3.
    q_gate: obs 0 for worlds {0,1}, obs 1 for {2,3}
    q_left: distinguishes 0 vs 1
    q_right: distinguishes 2 vs 3
    P concentrates on even pattern; Q on odd — craft TV gap at B=2.
    """
    # worlds: 0,1,2,3
    # P: 0 and 2 equal; Q: 1 and 3 equal — need distinguish within pairs
    p = f(1, 0, 1, 0)  # worlds 0,2
    q = f(0, 1, 0, 1)  # worlds 1,3
    q_gate = Query("gate", 1, (0, 0, 1, 1))
    q_left = Query("left", 1, (0, 1, 0, 1))  # distinguishes 0|1 and also 2|3 same labels
    q_right = Query("right", 1, (0, 0, 1, 1))  # same as gate — bad

    # Better left/right:
    # left: obs = world bit for {0,1}, constant on {2,3}
    q_left = Query("left", 1, (0, 1, 0, 0))  # splits 0 vs 1; 2,3 both 0
    q_right = Query("right", 1, (0, 0, 0, 1))  # splits 2 vs 3? 2->0,3->1; 0,1 ->0
    q_right = Query("right", 1, (0, 0, 0, 1))
    # Fix: world2 should differ from world3 on right
    q_right = Query("right", 1, (0, 0, 1, 0))  # 2->1, 3->0

    return Instance("asym_branch", 4, p, q, (q_gate, q_left, q_right))


def inst_gate_and_payload() -> Instance:
    """Strong adaptive candidate.

    Worlds: G0P0, G0P1, G1P0, G1P1  (indices 0..3)
    P: uniform on G0P0, G1P1  (payload matches gate)
    Q: uniform on G0P1, G1P0  (payload mismatches)

    Queries:
      gate: returns G bit  (obs 0,0,1,1)
      pay0: returns P if G=0 else 0  — only informative in left branch
      pay1: returns P if G=1 else 0

    Actually P bit: worlds 0:(0,0), 1:(0,1), 2:(1,0), 3:(1,1)
    """
    p = f(1, 0, 0, 1)
    q = f(0, 1, 1, 0)
    gate = Query("gate", 1, (0, 0, 1, 1))
    # payload bit as direct queries (nonadaptive can read both)
    pay = Query("pay", 1, (0, 1, 0, 1))
    # path-style: pay_L only meaningful after gate=0; encode requires
    pay_L = Query("pay_L", 1, (0, 1, 0, 1), requires=())  # same as pay without requires first
    return Instance("gate_pay", 4, p, q, (gate, pay))


def inst_list_then_head_topology() -> Instance:
    """Filesystem-shaped: two possible child names; only one present.

    Worlds:
      0: child A hot
      1: child B hot
      2: child A cold (decoy genuine?)
    Better:

    Topology differs:
      W0: only child 'a' with bit 0
      W1: only child 'a' with bit 1
      W2: only child 'b' with bit 0
      W3: only child 'b' with bit 1

    list(root) -> 'a' or 'b'
    head_a requires list? We model head_a legal only after list (requires list index 0)
    head_a obs: for worlds with a: the bit; for worlds without a: N/A
    """
    # worlds 0: a0, 1: a1, 2: b0, 3: b1
    list_r = Query("list", 1, ("a", "a", "b", "b"))
    head_a = Query("head_a", 1, (0, 1, "na", "na"), requires=(0,))
    head_b = Query("head_b", 1, ("na", "na", 0, 1), requires=(0,))
    # P: a0 or b0 (cold) equal; Q: a1 or b1 (hot) equal — list alone no TV?
    # list under P: a with 1/2, b with 1/2; same under Q. TV=0 from list.
    # head after list: see bit.
    p = f(1, 0, 1, 0)
    q = f(0, 1, 0, 1)
    return Instance("list_then_head", 4, p, q, (list_r, head_a, head_b))


def inst_adaptive_classic_chernoff_style() -> Instance:
    """3 pairs: gate chooses which pair; need second query to finish.

    Worlds 0..5: pair i in {0,1,2}, bit in {0,1} -> world = 2*i+bit
    P: pair uniform, bit=0 always
    Q: pair uniform, bit=1 always

    Queries:
      which_pair: returns pair id (cost 1) — same under P and Q always if pair same dist
      bit_i: returns bit for pair i, 'na' otherwise
    """
    # Actually if P always bit0 Q always bit1, which_pair has same law; bit_i distinguishes
    # if we know pair. Nonadaptive: without knowing pair, querying bit_0 only works 1/3.

    n = 6
    # world i: pair i//2, bit i%2
    p_list = []
    q_list = []
    for pair in range(3):
        for bit in range(2):
            # P: only bit=0; Q: only bit=1; pair uniform
            if bit == 0:
                p_list.append(1)
                q_list.append(0)
            else:
                p_list.append(0)
                q_list.append(1)
    # each pair has mass 1/3 under P on bit0 worlds: worlds 0,2,4
    p = f(*p_list)  # 1,0,1,0,1,0 -> normalize 3 ones -> 1/3 each
    q = f(*q_list)  # 0,1,0,1,0,1

    which = Query("which", 1, tuple(i // 2 for i in range(6)))
    bits = []
    for pair in range(3):
        obs = []
        for i in range(6):
            if i // 2 == pair:
                obs.append(i % 2)
            else:
                obs.append("na")
        bits.append(Query(f"bit{pair}", 1, tuple(obs)))
    return Instance("three_pair_bit", 6, p, q, (which, *bits))


def random_search_gaps(
    n_worlds: int = 4,
    n_queries: int = 4,
    n_obs: int = 2,
    budget: int = 2,
    trials: int = 2000,
    seed: int = 0,
) -> list[tuple[Fraction, Instance]]:
    """Monte Carlo over random observation tables and random rational P,Q."""
    import random

    rng = random.Random(seed)
    hits: list[tuple[Fraction, Instance]] = []

    for t in range(trials):
        queries = []
        for j in range(n_queries):
            obs = tuple(rng.randrange(n_obs) for _ in range(n_worlds))
            queries.append(Query(f"q{j}", 1, obs))
        # random sparse probs
        raw_p = [rng.randint(0, 3) for _ in range(n_worlds)]
        raw_q = [rng.randint(0, 3) for _ in range(n_worlds)]
        if sum(raw_p) == 0 or sum(raw_q) == 0:
            continue
        inst = Instance(
            f"rand_{t}",
            n_worlds,
            f(*raw_p),
            f(*raw_q),
            tuple(queries),
        )
        da, dn, g = gap(inst, budget)
        if g > 0:
            hits.append((g, inst))
    hits.sort(key=lambda x: x[0], reverse=True)
    return hits


def exhaustive_binary_queries_gap(
    n_worlds: int = 3,
    n_queries: int = 3,
    budget: int = 2,
) -> tuple[Fraction, Instance | None]:
    """Exhaust all binary-observation query tables (expensive small)."""
    best_g = Zero
    best_inst: Instance | None = None
    # all functions world->bit for each query: 2^{n_worlds} possibilities per query
    n_fun = 1 << n_worlds
    # probability extremes: all dirac and uniform-ish
    from itertools import product as iproduct

    prob_candidates = []
    # all pairs of distributions with denominator n_worlds (counts summing to n_worlds)
    for counts_p in iproduct(range(n_worlds + 1), repeat=n_worlds):
        if sum(counts_p) != n_worlds:
            continue
        for counts_q in iproduct(range(n_worlds + 1), repeat=n_worlds):
            if sum(counts_q) != n_worlds:
                continue
            if counts_p == counts_q:
                continue
            prob_candidates.append((counts_p, counts_q))

    # subsample probs if huge
    if len(prob_candidates) > 80:
        # keep those with small support
        prob_candidates = [pq for pq in prob_candidates if sum(x > 0 for x in pq[0]) <= 2 and sum(x > 0 for x in pq[1]) <= 2]
        if len(prob_candidates) > 100:
            prob_candidates = prob_candidates[:100]

    for qs in iproduct(range(n_fun), repeat=n_queries):
        queries = []
        for j, code in enumerate(qs):
            obs = tuple((code >> i) & 1 for i in range(n_worlds))
            queries.append(Query(f"q{j}", 1, obs))
        for cp, cq in prob_candidates:
            inst = Instance("exh", n_worlds, f(*cp), f(*cq), tuple(queries))
            da, dn, g = gap(inst, budget)
            if g > best_g:
                best_g = g
                best_inst = inst
                if best_g >= Fraction(1, 2):
                    return best_g, best_inst
    return best_g, best_inst


def report_instance(inst: Instance, budgets: Iterable[int] = (0, 1, 2, 3)) -> str:
    lines = [f"== {inst.name} n={inst.n} queries={len(inst.queries)} =="]
    lines.append(f"P={inst.p}")
    lines.append(f"Q={inst.q}")
    for b in budgets:
        da, dn, g = gap(inst, b)
        dn_free = D_nonadaptive(inst, b, path_free=True)
        lines.append(
            f"B={b}: D_ad={da}  D_na={dn}  gap={g}  D_na_pathfree={dn_free}  gap_pf={da-dn_free}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    demos = [
        inst_star_hot_child(),
        inst_three_files_one_hot(),
        inst_asymmetric_branch(),
        inst_gate_and_payload(),
        inst_list_then_head_topology(),
        inst_adaptive_classic_chernoff_style(),
    ]
    for inst in demos:
        print(report_instance(inst))
        print()
