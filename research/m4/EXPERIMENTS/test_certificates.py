"""Property tests for M4 certificates — run: python test_certificates.py"""

from __future__ import annotations

from fractions import Fraction

from enum_core import (
    D_adaptive,
    Instance,
    Query,
    f,
    gap,
    inst_asymmetric_branch,
    inst_list_then_head_topology,
    inst_adaptive_classic_chernoff_style,
)


def test_asym_gap():
    da, dn, g = gap(inst_asymmetric_branch(), 2)
    assert da == 1
    assert dn == Fraction(1, 2)
    assert g == Fraction(1, 2)


def test_list_then_head_gap_and_pathfree():
    inst = inst_list_then_head_topology()
    da, dn, g = gap(inst, 2)
    assert da == 1
    assert dn == Fraction(1, 2)
    assert g == Fraction(1, 2)
    from enum_core import D_nonadaptive

    assert D_nonadaptive(inst, 2, path_free=True) == 1


def test_three_pair_gap():
    da, dn, g = gap(inst_adaptive_classic_chernoff_style(), 2)
    assert da == 1
    assert dn == Fraction(2, 3)
    assert g == Fraction(1, 3)


def test_PQ_equal_zero():
    inst = inst_asymmetric_branch()
    inst2 = Instance("eq", inst.n, inst.p, inst.p, inst.queries)
    assert D_adaptive(inst2, 3) == 0


def test_monotone_B():
    inst = inst_asymmetric_branch()
    prev = Fraction(0)
    for b in range(0, 4):
        d = D_adaptive(inst, b)
        assert d >= prev
        prev = d


def test_symmetry():
    inst = inst_asymmetric_branch()
    swap = Instance("sw", inst.n, inst.q, inst.p, inst.queries)
    for b in range(0, 4):
        assert D_adaptive(inst, b) == D_adaptive(swap, b)


def test_parity_local_global():
    p = f(1, 0, 0, 1)
    q = f(0, 1, 1, 0)
    phi1 = Query("phi1", 1, (0, 0, 1, 1))
    phi2 = Query("phi2", 1, (0, 1, 0, 1))
    parity = Query("parity", 1, (0, 1, 1, 0))
    assert D_adaptive(Instance("L", 4, p, q, (phi1, phi2)), 1) == 0
    assert D_adaptive(Instance("G", 4, p, q, (parity,)), 1) == 1


def test_score_reversal():
    w = {"bad": Fraction(55, 100), "warn": Fraction(25, 100)}

    def S(sevs):
        r = Fraction(1)
        for s in sevs:
            r *= 1 - w[s]
        return 1 - r

    assert S(["warn", "warn"]) < S(["bad"])
    p = (Fraction(1, 6), Fraction(2, 3))
    q = (Fraction(2, 3), Fraction(1, 6))
    assert q[0] / p[0] > q[1] / p[1]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("OK", name)
    print("all certificate tests passed")
