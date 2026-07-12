"""Executable exact certificates for M5."""

from fractions import Fraction as F
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from m5_exact import (  # noqa: E402
    adaptive_depth2_value,
    four_world_extremal_cores,
    m4_butterfly,
    nonadaptive_value,
    sanity_small_support_no_gap,
    sharp_adaptive_policy_value,
    sharp_arity_instance,
)


def run() -> None:
    m4 = m4_butterfly()
    assert adaptive_depth2_value(m4) == F(1)
    assert nonadaptive_value(m4, 2) == F(1, 2)

    for k in range(2, 8):
        inst = sharp_arity_instance(k)
        assert sharp_adaptive_policy_value(k) == F(1)
        assert nonadaptive_value(inst, 2) == F(1, k)

    # Four raw triples remain after quotienting each binary cut by complement.
    # They are related by the theorem's remaining world/branch symmetries.
    cores = four_world_extremal_cores()
    assert len(cores) == 4

    checked = sanity_small_support_no_gap(max_n=3, denominator=3)
    assert checked > 0

    print("PASS: M4 extremal certificate")
    print("PASS: sharp K-ary construction for K=2..7")
    print("PASS: four-world binary core enumeration")
    print(f"PASS: small-support sanity sweep ({checked} exact P,Q instances)")


if __name__ == "__main__":
    run()
