"""M4 P1 hunt driver: A gaps, B score order, C local-global."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

from enum_core import (
    D_adaptive,
    D_nonadaptive,
    Instance,
    Query,
    f,
    gap,
    inst_adaptive_classic_chernoff_style,
    inst_asymmetric_branch,
    inst_list_then_head_topology,
    random_search_gaps,
    report_instance,
)

ROOT = Path(__file__).resolve().parents[1]
CE = ROOT / "COUNTEREXAMPLES"


def frac_str(x: Fraction) -> str:
    return f"{x.numerator}/{x.denominator}"


def save_witness(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"WROTE {path}")


# ----- Claim A -----


def hunt_A() -> None:
    print("\n######## CLAIM A ########\n")
    for inst in [
        inst_asymmetric_branch(),
        inst_list_then_head_topology(),
        inst_adaptive_classic_chernoff_style(),
    ]:
        print(report_instance(inst))
        print()

    # minimality: n=3 worlds, m=3 binary queries, dirac/2-support probs, B=2
    print("--- minimality n=3 restricted exhaustive ---")
    best = Fraction(0)
    best_desc = None
    n = 3
    n_fun = 1 << n
    count_checked = 0
    # probability: all pairs of 0-1 supports with mass pattern (2,1,0) perms + diracs
    prob_pairs = []
    for cp in product(range(3), repeat=n):
        if sum(cp) == 0:
            continue
        if sum(1 for x in cp if x) > 2:
            continue
        for cq in product(range(3), repeat=n):
            if sum(cq) == 0 or cp == cq:
                continue
            if sum(1 for x in cq if x) > 2:
                continue
            prob_pairs.append((cp, cq))
    # queries: sample structured + all if small
    query_codes = list(product(range(n_fun), repeat=3))
    for qs in query_codes:
        queries = tuple(
            Query(f"q{j}", 1, tuple((code >> i) & 1 for i in range(n)))
            for j, code in enumerate(qs)
        )
        for cp, cq in prob_pairs:
            inst = Instance("min3", n, f(*cp), f(*cq), queries)
            da, dn, g = gap(inst, 2)
            count_checked += 1
            if g > best:
                best = g
                best_desc = (inst, da, dn, g)
    print(f"checked {count_checked} instances, best gap n=3 = {best}")
    if best_desc and best > 0:
        inst, da, dn, g = best_desc
        print(report_instance(inst))
        print("QUERIES", [(qu.name, qu.obs) for qu in inst.queries])
    else:
        print("No adaptive gap found for n=3 under restricted exhaustive (supports gap of A.2).")

    # n=4 known witness
    inst = inst_asymmetric_branch()
    da, dn, g = gap(inst, 2)
    assert g == Fraction(1, 2)
    assert da == 1
    assert dn == Fraction(1, 2)

    save_witness(
        CE / "wit-A-asym-branch-B2.json",
        {
            "id": "wit-A-asym-branch-B2",
            "kills_or_witnesses": "M4-A",
            "role": "witness",
            "statement": (
                "At B=2, D_adaptive=1 and D_nonadaptive=1/2 "
                "(gap=1/2) for gate/left/right query geometry."
            ),
            "P": {
                "worlds": ["W0", "W1", "W2", "W3"],
                "probs": ["1/2", "0", "1/2", "0"],
            },
            "Q": {
                "worlds": ["W0", "W1", "W2", "W3"],
                "probs": ["0", "1/2", "0", "1/2"],
            },
            "tree_encoding": {
                "note": "Abstract attributed worlds; FS reading: gate=list branch id; left/right=head in branch",
                "worlds": {
                    "W0": {"gate": 0, "payload": 0},
                    "W1": {"gate": 0, "payload": 1},
                    "W2": {"gate": 1, "payload": 0},
                    "W3": {"gate": 1, "payload": 1},
                },
            },
            "queries": [
                {"id": "gate", "type": "gate", "obs": [0, 0, 1, 1], "cost": 1},
                {"id": "left", "type": "head_left", "obs": [0, 1, 0, 0], "cost": 1},
                {"id": "right", "type": "head_right", "obs": [0, 0, 1, 0], "cost": 1},
            ],
            "costs": {"gate": "1", "left": "1", "right": "1"},
            "budget": 2,
            "D_adaptive": "1/1",
            "D_nonadaptive": "1/2",
            "advantage_gap": "1/2",
            "optimal_policy": {
                "first": "gate",
                "if_0": "left",
                "if_1": "right",
                "result": "full separation TV=1",
            },
            "claimed_policy": {
                "nonadaptive_best": "any 2-subset yields TV<=1/2",
            },
            "path_free_nonadaptive_D": frac_str(D_nonadaptive(inst, 2, path_free=True)),
            "notes": (
                "Exceeds CHARTER constants (claimed D_ad=1/2, D_na<=1/4); "
                "stronger witness D_ad=1, D_na=1/2. "
                "MIRROR: classical adaptive experimental design geometry."
            ),
            "verified_by": "EXPERIMENTS/enum_core.py adaptive_W / nonadaptive_W",
        },
    )

    inst2 = inst_list_then_head_topology()
    da2, dn2, g2 = gap(inst2, 2)
    save_witness(
        CE / "wit-A-list-then-head-B2.json",
        {
            "id": "wit-A-list-then-head-B2",
            "kills_or_witnesses": "M4-A",
            "role": "witness",
            "statement": (
                "Filesystem path-prefix legality: D_ad=1, D_na=1/2 at B=2 "
                "when head_* requires list. Path-free nonadaptive achieves D=1 "
                "(gap vanishes) — MIRROR stress model."
            ),
            "P": {"probs": ["1/2", "0", "1/2", "0"]},
            "Q": {"probs": ["0", "1/2", "0", "1/2"]},
            "tree_encoding": {
                "W0": "only child a bit0",
                "W1": "only child a bit1",
                "W2": "only child b bit0",
                "W3": "only child b bit1",
            },
            "queries": [
                {"id": "list", "obs": ["a", "a", "b", "b"], "cost": 1, "requires": []},
                {
                    "id": "head_a",
                    "obs": [0, 1, "na", "na"],
                    "cost": 1,
                    "requires": ["list"],
                },
                {
                    "id": "head_b",
                    "obs": ["na", "na", 0, 1],
                    "cost": 1,
                    "requires": ["list"],
                },
            ],
            "budget": 2,
            "D_adaptive": frac_str(da2),
            "D_nonadaptive": frac_str(dn2),
            "advantage_gap": frac_str(g2),
            "D_nonadaptive_path_free": frac_str(D_nonadaptive(inst2, 2, path_free=True)),
            "optimal_policy": {
                "first": "list",
                "if_a": "head_a",
                "if_b": "head_b",
            },
            "notes": "Primary FS-shaped witness under DEFINITIONS legality model.",
            "verified_by": "EXPERIMENTS/enum_core.py",
        },
    )

    inst3 = inst_adaptive_classic_chernoff_style()
    da3, dn3, g3 = gap(inst3, 2)
    save_witness(
        CE / "wit-A-three-pair-B2.json",
        {
            "id": "wit-A-three-pair-B2",
            "kills_or_witnesses": "M4-A",
            "role": "witness",
            "D_adaptive": frac_str(da3),
            "D_nonadaptive": frac_str(dn3),
            "advantage_gap": frac_str(g3),
            "budget": 2,
            "notes": "which-pair then bit_i; nonadaptive cannot cover all pairs in budget 2",
            "verified_by": "EXPERIMENTS/enum_core.py",
        },
    )

    # random search bonus (bounded)
    print("--- random search n=4 m=4 B=2 trials=800 ---")
    hits = random_search_gaps(4, 4, 2, 2, trials=800, seed=13)
    print(f"hits with gap>0: {len(hits)}")
    if hits:
        print(f"best random gap={hits[0][0]}")
        print(report_instance(hits[0][1]))


# ----- Claim B -----


def blown_score(sevs: list[str]) -> Fraction:
    w = {"bad": Fraction(55, 100), "warn": Fraction(25, 100), "info": Fraction(5, 100)}
    remain = Fraction(1)
    for s in sevs:
        remain *= 1 - w[s]
    return 1 - remain


def is_blown(sevs: list[str]) -> bool:
    if any(s == "bad" for s in sevs):
        return True
    return blown_score(sevs) >= Fraction(3, 5)


def hunt_B() -> None:
    print("\n######## CLAIM B ########\n")
    # B.3 dual gate
    sevs = ["bad"]
    print(f"one bad: score={blown_score(sevs)} blown={is_blown(sevs)}")
    assert blown_score(sevs) < Fraction(3, 5) and is_blown(sevs)

    # B.1 order reversal under O_full
    # Worlds as trees with latent defects -> findings
    # X0: one defect activates two warns (common cause) — score high-ish
    # X1: one bad — score 0.55 but refuse
    # Craft P,Q so Lambda(X0) > Lambda(X1) but S(X0) < S(X1)? 
    # S(two warns)=1-(0.75)^2=0.4375; S(one bad)=0.55 so S(X0)<S(X1)
    # Want Lambda(X0)>Lambda(X1) i.e. Q/P larger on X0 than X1

    # Three trees:
    # X0: findings [warn,warn] score 0.4375, not blown by score; not bad
    # X1: findings [bad] score 0.55 blown
    # X2: findings [] score 0 clean

    s0 = blown_score(["warn", "warn"])
    s1 = blown_score(["bad"])
    s2 = blown_score([])
    print(f"scores: X0 two-warn={s0}, X1 bad={s1}, X2 clean={s2}")
    assert s0 < s1

    # P,Q on {X0,X1,X2}
    # Want Lambda(X0) > Lambda(X1): Q0/P0 > Q1/P1
    # Example: P puts more mass on X1 than Q does relative to X0
    # P: X0=1/6, X1=2/3, X2=1/6
    # Q: X0=2/3, X1=1/6, X2=1/6
    p = (Fraction(1, 6), Fraction(2, 3), Fraction(1, 6))
    q = (Fraction(2, 3), Fraction(1, 6), Fraction(1, 6))
    lam = [q[i] / p[i] for i in range(3)]
    print(f"Lambda={lam}")
    assert s0 < s1 and lam[0] > lam[1]
    print("ORDER REVERSAL: S(X0)<S(X1) but Lambda(X0)>Lambda(X1)")

    # Also refuse policy vs LR: R(X1)=1, R(X0)=0 but X0 more Q-like
    assert is_blown(["bad"]) and not is_blown(["warn", "warn"])
    print("REFUSE REVERSAL: R(X1)=1 > R(X0)=0 but Lambda(X0)>Lambda(X1)")

    save_witness(
        CE / "wit-B-score-lr-reversal.json",
        {
            "id": "wit-B-score-lr-reversal",
            "kills_or_witnesses": "M4-B",
            "role": "witness",
            "statement": (
                "Trees X0 (two warn findings) and X1 (one bad): "
                "S(X0)=7/16 < S(X1)=11/20 but Lambda(X0)=4 > Lambda(X1)=1/4 "
                "under explicit equal-support rational P,Q."
            ),
            "findings": {
                "X0": ["warn", "warn"],
                "X1": ["bad"],
                "X2": [],
            },
            "scores": {
                "X0": frac_str(s0),
                "X1": frac_str(s1),
                "X2": frac_str(s2),
            },
            "P": ["1/6", "2/3", "1/6"],
            "Q": ["2/3", "1/6", "1/6"],
            "Lambda": [frac_str(x) for x in lam],
            "refuse": {
                "X0": is_blown(["warn", "warn"]),
                "X1": is_blown(["bad"]),
            },
            "latent_defect_cover": {
                "note": "X0: one defect d_common activates two warn codes; X1: one defect d_lie activates one bad",
                "Phi": {"d_common": ["warn_a", "warn_b"], "d_lie": ["bad_magic"]},
            },
            "comparison_oracle": "O_full",
            "notes": (
                "Kills Bayes-monotone reading of severity-only product score. "
                "Novelty of qualitative claim may be low (MIRROR); CHARM-specific constants locked."
            ),
        },
    )

    # equal score unequal evidence
    # three warns: S=1-(0.75)^3=0.578125
    # one warn + many info? hard to equal
    # two different multisets with same S: one bad vs ? 0.55 exactly
    # one bad = 0.55; cannot get with warns only easily
    # Use: [warn, warn, info, info, ...] 
    # Actually [bad] score 0.55; find other multiset
    # 1 - (0.75)^a * (0.95)^b = 0.55 => (0.75)^a*(0.95)^b = 0.45
    # Or two different finding sets with same sevs permuted - equal S equal everything
    # Better: Xa has findings that are functions of different defects but same severity multiset
    # Same S by construction - for B.2 need same S, different Lambda - trivial:
    # same findings on two trees? Then smell identical - LR can still differ if trees differ on unobserved features
    # Under O_full: two trees with identical σ (same findings) but different full attributes
    s_same = blown_score(["warn"])
    # Xa and Xb both one warn; P,Q differ on them via non-smell attributes
    p2 = (Fraction(1, 2), Fraction(1, 2))  # Xa, Xb
    q2 = (Fraction(3, 4), Fraction(1, 4))
    assert blown_score(["warn"]) == blown_score(["warn"])
    lam_a = q2[0] / p2[0]
    lam_b = q2[1] / p2[1]
    assert lam_a != lam_b
    print(f"B.2 equal score={s_same} but Lambda {lam_a} vs {lam_b}")
    save_witness(
        CE / "wit-B-equal-score-unequal-lr.json",
        {
            "id": "wit-B-equal-score-unequal-lr",
            "kills_or_witnesses": "M4-B",
            "role": "witness",
            "statement": "Identical severity multisets (hence equal S) with unequal full-tree LR.",
            "scores": {"Xa": frac_str(s_same), "Xb": frac_str(s_same)},
            "P": ["1/2", "1/2"],
            "Q": ["3/4", "1/4"],
            "Lambda": [frac_str(lam_a), frac_str(lam_b)],
            "notes": "Shows S is not a sufficient statistic for Bayes decisions under O_full.",
        },
    )


# ----- Claim C -----


def hunt_C() -> None:
    print("\n######## CLAIM C ########\n")
    # Local predicates φ1, φ2: each depends on one node attribute
    # Global ρ: parity of two bits
    # Worlds: bits (b1,b2) in {0,1}^2
    # P: uniform on even parity (00, 11)
    # Q: uniform on odd parity (01, 10)
    # Local φ1 = b1, φ2 = b2 — Law under P and Q: each bit Bern(1/2) for both
    # Global parity distinguishes perfectly with one query

    # As query model: only global_rel available for D_1, or include locals
    worlds = 4  # 00,01,10,11
    p = f(1, 0, 0, 1)
    q = f(0, 1, 1, 0)
    # local queries
    phi1 = Query("phi1", 1, (0, 0, 1, 1))  # b1
    phi2 = Query("phi2", 1, (0, 1, 0, 1))  # b2
    parity = Query("parity", 1, (0, 1, 1, 0))  # b1 xor b2

    # Matched locals: Law of phi1 under P: 0 on 00 (1/2), 1 on 11 (1/2) -> Bern(1/2)
    # under Q: 0 on 01 (1/2), 1 on 10 (1/2) -> Bern(1/2)
    inst_local_only = Instance("local_only", 4, p, q, (phi1, phi2))
    inst_with_global = Instance("with_global", 4, p, q, (phi1, phi2, parity))
    inst_global_only = Instance("global_only", 4, p, q, (parity,))

    print(report_instance(inst_local_only))
    print(report_instance(inst_global_only))
    print(report_instance(inst_with_global))

    # D_1 with only global = 1; with only locals at B=1 = 0; at B=2 locals = 1
    d1_g = D_adaptive(inst_global_only, 1)
    d1_l = D_adaptive(inst_local_only, 1)
    d2_l = D_adaptive(inst_local_only, 2)
    assert d1_g == 1
    assert d1_l == 0
    assert d2_l == 1
    print(f"D1(global)={d1_g} D1(locals)={d1_l} D2(locals)={d2_l}")
    print("LOCAL MATCH + GLOBAL D1=1 SEPARATION established (parity)")

    save_witness(
        CE / "wit-C-parity-local-global.json",
        {
            "id": "wit-C-parity-local-global",
            "kills_or_witnesses": "M4-C",
            "role": "witness",
            "statement": (
                "P=even parity, Q=odd parity on two bits. "
                "Each single-bit law is Bern(1/2) under both P and Q (locals matched). "
                "D_1 with parity query = 1; D_1 with only local bit queries = 0."
            ),
            "P": ["1/2", "0", "0", "1/2"],
            "Q": ["0", "1/2", "1/2", "0"],
            "local_predicates": ["b1", "b2"],
            "global_relation": "b1 XOR b2",
            "D1_global_only": frac_str(d1_g),
            "D1_locals_only": frac_str(d1_l),
            "D2_locals_only": frac_str(d2_l),
            "notes": (
                "Classical parity / local-vs-global. "
                "CHARM translation: checksum line items can each look fine while "
                "set-level parity/co-occurrence fails. Novelty residual is product export only."
            ),
            "verified_by": "EXPERIMENTS/enum_core.py",
        },
    )

    # CHARM-shaped sketch: companion co-occurrence
    # φ_magic_ok, φ_habitat_ok always 1 under P and Q
    # global: co-occurrence of two specialist families forbidden under P only
    # worlds: (famA, famB) present flags
    # P: only (1,0) and (0,1); Q: also (1,1)
    p_c = f(1, 1, 0)  # A only, B only, both — wait 3 worlds
    # worlds: 0=A, 1=B, 2=AB
    p_c = f(1, 1, 0)
    q_c = f(1, 1, 1)
    # renormalize q - f already
    # local φA: is A present - world0:1, world1:0, world2:1
    # Under P: P(φA=1)=1/2; under Q: 2/3 — NOT matched
    # Need matched locals carefully

    # Use two independent-looking markers with joint constraint
    # Already have parity as gold standard separation


def main() -> int:
    CE.mkdir(parents=True, exist_ok=True)
    hunt_A()
    hunt_B()
    hunt_C()
    print("\n######## HUNT COMPLETE ########\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
