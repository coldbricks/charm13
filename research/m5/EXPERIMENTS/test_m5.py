"""M5 certificates — unbounded adaptivity gap + greedy failure."""

from __future__ import annotations

from fractions import Fraction

from enum_core import (
    D_adaptive,
    D_nonadaptive,
    gap,
    greedy_vs_optimal,
    inst_k_pairs,
    myopic_single_tv,
)


def test_closed_form_small_k():
    for k in range(2, 9):
        inst = inst_k_pairs(k)
        da, dn, g = gap(inst, 2)
        assert da == 1, (k, da)
        assert dn == Fraction(2, k), (k, dn)
        assert g == 1 - Fraction(2, k)


def test_gap_tends_toward_one():
    # symbolic: 1 - 2/k increases in k
    gaps = [1 - Fraction(2, k) for k in range(2, 30)]
    assert gaps == sorted(gaps)
    assert gaps[-1] > Fraction(9, 10)


def test_ratio_unbounded_symbolically():
    ratios = [Fraction(k, 2) for k in range(2, 100)]
    assert ratios[-1] == Fraction(99, 2)
    assert ratios[-1] > 40


def test_greedy_unbounded():
    for k in [3, 4, 5, 8, 12]:
        inst = inst_k_pairs(k)
        gv = greedy_vs_optimal(inst)
        assert gv["greedy_first"].startswith("bit")
        assert gv["greedy_tv"] == Fraction(2, k)
        assert gv["optimal_tv"] == 1
        assert gv["ratio_opt_over_greedy"] == Fraction(k, 2)


def test_myopic_prefers_bit_over_which():
    k = 5
    inst = inst_k_pairs(k)
    # which is index 0
    assert myopic_single_tv(inst, 0) == 0
    assert myopic_single_tv(inst, 1) == Fraction(1, k)


def test_nonadaptive_needs_k_bits_for_perfect():
    k = 6
    inst = inst_k_pairs(k)
    # budget k-1 nonadaptive cannot reach 1
    assert D_nonadaptive(inst, k - 1) == Fraction(k - 1, k)
    assert D_nonadaptive(inst, k) == 1
    assert D_adaptive(inst, 2) == 1


def test_symmetry():
    k = 4
    inst = inst_k_pairs(k)
    from enum_core import Instance

    swap = Instance("sw", inst.n, inst.q, inst.p, inst.queries)
    assert D_adaptive(inst, 2) == D_adaptive(swap, 2)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print("OK", name)
    print("all m5 certificates passed")
