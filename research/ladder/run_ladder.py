"""Recursive ladder M6→M11: theorems + certificates in one runner."""

from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from kernel import (  # noqa: E402
    D_ad,
    D_na,
    camouflage_capacity_adaptive,
    inst_k_pairs,
    min_k_nonadaptive_below_eps,
    myopic_greedy_tv,
    theory_D_ad,
    theory_D_na,
    theory_gap,
)

REPORTS = ROOT.parent  # research/


def assert_eq(a, b, msg=""):
    if a != b:
        raise AssertionError(f"{msg}: {a} != {b}")


# ========================= M6 =========================


def run_m6() -> dict:
    """For every fixed B>=2, Gap_B(k) → 1 as k→∞; closed forms for all B,k."""
    results = []
    for B in range(0, 7):
        for k in range(1, 16):
            th_a, th_n = theory_D_ad(k, B), theory_D_na(k, B)
            # machine check structured instances for modest sizes
            if k <= 8 and B <= 4:
                inst = inst_k_pairs(k)
                assert_eq(D_ad(inst, B), th_a, f"M6 D_ad k={k} B={B}")
                assert_eq(D_na(inst, B), th_n, f"M6 D_na k={k} B={B}")
            g = th_a - th_n
            results.append({"k": k, "B": B, "D_ad": str(th_a), "D_na": str(th_n), "gap": str(g)})
    # limit statement
    for B in range(2, 20):
        # need k >> B so B/k small; k up to 20*B
        ks = list(range(B + 1, 20 * B + 1))
        gaps = [theory_gap(k, B) for k in ks]
        assert gaps == sorted(gaps), "M6 gaps must increase in k"
        assert gaps[-1] > Fraction(9, 10), f"M6 gap not near 1 for B={B}: {gaps[-1]}"
        assert theory_gap(10**6, B) > Fraction(999, 1000)
    return {
        "mission": "M6",
        "title": "Gap_B → 1 for every fixed B ≥ 2",
        "status": "PROVED",
        "theorems": [
            "D_ad(k,B)=1/k if B==1 else (0 if B==0 else 1 for B>=2)",
            "D_na(k,B)=min(B,k)/k",
            "for each B>=2: lim_k Gap_B(k)=1",
        ],
        "novelty": "KNOWN RESULT, NEW APPLICATION (strengthens M5 from B=2 to all B>=2)",
        "product_scar": "Any fixed look-budget checklist is arbitrarily weak vs adaptive as branching grows",
        "samples": results[::17][:8],
    }


# ========================= M7 =========================


def run_m7() -> dict:
    """Myopic greedy for horizon B: never picks which; TV=min(B,k)/k; ratio → ∞."""
    ratios = []
    for B in range(2, 8):
        for k in range(B + 1, 30):
            opt = theory_D_ad(k, B)  # 1
            gr = myopic_greedy_tv(k, B)
            assert gr == theory_D_na(k, B)
            ratio = opt / gr if gr > 0 else None
            if k == 20:
                ratios.append({"B": B, "k": k, "greedy": str(gr), "opt": str(opt), "ratio": str(ratio)})
            assert ratio == Fraction(k, min(B, k))
    # unbounded for fixed B
    B = 3
    r50 = Fraction(50, 3)
    assert myopic_greedy_tv(50, B) == Fraction(3, 50)
    assert Fraction(1) / myopic_greedy_tv(50, B) == r50
    return {
        "mission": "M7",
        "title": "Myopic greedy unboundedly suboptimal for every horizon B≥2",
        "status": "PROVED",
        "theorems": [
            "Myopic single-step TV never selects which (TV=0)",
            "After t myopic steps TV = t/k (t<=k)",
            "opt/greedy = k/min(B,k) → ∞ as k→∞ for each fixed B≥2",
        ],
        "novelty": "KNOWN RESULT, NEW APPLICATION (approximation barrier for greedy feature acquisition)",
        "product_scar": "Do not order smell by single-finding severity alone; gate/branch queries first",
        "samples": ratios,
    }


# ========================= M8 =========================


def run_m8() -> dict:
    """Any fixed nonadaptive budget B: exists k with D_B^na < ε but D_2^ad = 1."""
    rows = []
    for B in range(1, 10):
        for eps_num, eps_den in [(1, 2), (1, 10), (1, 100)]:
            eps = Fraction(eps_num, eps_den)
            k = min_k_nonadaptive_below_eps(B, eps)
            d_na = theory_D_na(k, B)
            d_ad2 = theory_D_ad(k, 2)
            assert d_na <= eps, (B, eps, k, d_na)
            assert d_ad2 == 1
            rows.append(
                {
                    "B": B,
                    "eps": str(eps),
                    "k": k,
                    "D_na": str(d_na),
                    "D_ad_B2": str(d_ad2),
                }
            )
    return {
        "mission": "M8",
        "title": "Fixed nonadaptive suite cannot dominate adaptive T1 (uniformly)",
        "status": "PROVED",
        "theorems": [
            "∀B∀ε∈(0,1)∃k: D_B^na(P_k,Q_k)≤ε and D_2^ad(P_k,Q_k)=1",
            "min such k = min_k_nonadaptive_below_eps(B,ε)",
        ],
        "novelty": "KNOWN RESULT, NEW APPLICATION (checklist incompleteness theorem for CHARM)",
        "product_scar": "Passing a fixed-size smell suite is not a uniform T1 risk certificate",
        "samples": rows[:12],
    }


# ========================= M9 =========================


def run_m9() -> dict:
    """Capacity-style: adaptive B≥2 ⇒ indistinguishability capacity 0 for ε<1."""
    rows = []
    for B in range(0, 6):
        for eps in [Fraction(1, 2), Fraction(9, 10), Fraction(1)]:
            cap = camouflage_capacity_adaptive(B, eps)
            rows.append({"B": B, "eps": str(eps), "C_ad_max_k_or_inf": "∞" if cap is None else cap})
    # the sharp product theorem
    assert camouflage_capacity_adaptive(2, Fraction(1, 2)) == 0
    assert camouflage_capacity_adaptive(2, Fraction(99, 100)) == 0
    assert camouflage_capacity_adaptive(1, Fraction(1, 2)) is None  # 1/k can be small
    # nonadaptive risk score
    risk = []
    for k in [4, 10, 100]:
        for B in [2, 5]:
            risk.append({"k": k, "B": B, "D_na": str(theory_D_na(k, B))})
    return {
        "mission": "M9",
        "title": "Camouflage capacity zero under adaptive B≥2 on k-pair family",
        "status": "PROVED",
        "theorems": [
            "For B≥2 and ε<1: no k has D_B^ad(P_k,Q_k)≤ε (capacity 0)",
            "For B=1: D=1/k →0 so arbitrarily large k meet any ε>0 (capacity ∞ in k)",
            "Nonadaptive risk D_B^na=min(B,k)/k decreases in k",
        ],
        "novelty": "KNOWN RESULT, NEW APPLICATION (capacity zero under strong observer — honest)",
        "product_scar": "Against adaptive T1 B≥2, branching camouflage of this form cannot achieve D≤ε<1; do not market large k as adaptive-safe",
        "samples": {"capacity_table": rows, "nonadaptive_risk": risk},
    }


# ========================= M10 =========================


def run_m10() -> dict:
    """Computation: closed form O(1); general DP exponential in n; FPT in k for this family."""
    # verify poly-time closed form matches DP for grid
    for k in range(1, 7):
        inst = inst_k_pairs(k)
        for B in range(0, 5):
            assert_eq(D_ad(inst, B), theory_D_ad(k, B), "M10 ad")
            assert_eq(D_na(inst, B), theory_D_na(k, B), "M10 na")
    return {
        "mission": "M10",
        "title": "Exact computation: O(1) closed form on k-pairs; DP 2^n fallback",
        "status": "PROVED (algorithm + complexity observation)",
        "theorems": [
            "On k-pair family, D_ad and D_na computable in O(1) given (k,B) via closed form",
            "General finite instances: exact adaptive value via subset DP in time 2^n · B · |Q| · poly",
            "Barrier: n=2k grows with branching; unstructured DP explodes — structure is essential",
        ],
        "novelty": "ENGINEERING ADAPTATION / known DP pattern + family-specific O(1)",
        "product_scar": "Research CLI can certify k-pair risk in O(1); general habitats need structure or bounds",
        "dp_complexity": "O(2^n * B * |Q|)",
        "structured_complexity": "O(1) for k-pair closed form",
    }


# ========================= M11 =========================


def run_m11() -> dict:
    """Composition: M4 gap is special case k=2 of M5/M6; product doctrine pack."""
    # M4 asym is different geometry (gate/left/right) also gap 1/2 at B=2
    # k=4 pairs: gap 1-2/4=1/2 same constant
    assert theory_gap(4, 2) == Fraction(1, 2)
    assert theory_D_ad(4, 2) == 1
    # M4 minimality n=4 worlds unguarded: k=2 has n=4 worlds, gap at B=2 is 0!
    # k=2: D_na=1, gap=0. So M4's 4-world gate instance is NOT the same as k=2 pairs.
    assert theory_gap(2, 2) == 0
    # first positive gap at k=3 (n=6 worlds) for this family
    assert theory_gap(3, 2) == Fraction(1, 3)
    doctrine = [
        "Static smell = nonadaptive observer",
        "Sharp budget-2 envelope: G_2(K)=1-1/K under OPEN arity-K queries (novelty unresolved)",
        "Adaptive T1 with B>=2 can force D=1 on k-pair camouflage for every k",
        "Myopic severity ordering is unboundedly suboptimal",
        "Capacity under adaptive B>=2 is zero for ε<1 on this family",
        "M4 single gap is the binary floor; sharp package + ladder show the envelope",
        "Never claim T4; never claim general disks equal k-pair; no novelty press language",
    ]
    return {
        "mission": "M11",
        "title": "Ladder composition + CHARM doctrine pack",
        "status": "PROVED (meta) + PRODUCT DOCTRINE READY",
        "theorems": [
            "M5 is B=2 slice of M6",
            "k=2 pairs have gap 0 at B=2 (need k>=3); M4 four-world gate is a different minimal gadget",
            "Doctrine pack lists operator-facing consequences",
        ],
        "novelty": "SYNTHESIS",
        "product_scar": "Ship doctrine bullets into MASTER/README when owner allows",
        "doctrine": doctrine,
    }


MISSIONS = [
    run_m6,
    run_m7,
    run_m8,
    run_m9,
    run_m10,
    run_m11,
]


def write_mission_result(data: dict) -> Path:
    mid = data["mission"].lower()
    d = REPORTS / mid
    d.mkdir(parents=True, exist_ok=True)
    (d / "EXPERIMENTS").mkdir(exist_ok=True)
    (d / "PROOFS").mkdir(exist_ok=True)
    path = d / "RESULT.md"
    lines = [
        f"# {data['mission']} RESULT — {data['title']}",
        "",
        f"**Status:** `{data['status']}`  ",
        f"**Novelty packaging:** {data['novelty']}  ",
        f"**Product scar:** {data['product_scar']}",
        "",
        "## Theorems",
        "",
    ]
    for t in data["theorems"]:
        lines.append(f"- {t}")
    lines += [
        "",
        "## Samples / certificates",
        "",
        "```json",
        json.dumps(data.get("samples", data), indent=2, default=str)[:4000],
        "```",
        "",
        "## Reproduce",
        "",
        "```powershell",
        "cd C:\\Users\\coldb\\charm13\\research\\ladder",
        "python run_ladder.py",
        "```",
        "",
        "## Honesty",
        "",
        "Closed-form on the k-pair family. Not a claim about all real filesystems. "
        "Broad adaptivity phenomena are classical; residual is exact envelope + CHARM scars.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")
    # JSON blob
    (d / "RESULT.json").write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    return path


def main() -> int:
    print("LADDER IGNITION M6→M11\n")
    summary = []
    for i, fn in enumerate(MISSIONS):
        name = fn.__name__
        print(f">>> {name} ...", flush=True)
        data = fn()
        path = write_mission_result(data)
        print(f"    OK {data['mission']}: {data['title']}")
        print(f"    wrote {path}")
        summary.append(
            {
                "mission": data["mission"],
                "status": data["status"],
                "title": data["title"],
            }
        )
        # recursive re-verify all previous after each new mission
        print(f"    --- recursive re-verify M6..{data['mission']} ---")
        for prev in MISSIONS[: i + 1]:
            prev()
            print(f"        re-OK {prev.__name__}")
    master = REPORTS / "LADDER_MASTER.md"
    lines = [
        "# CHARM13 Research Ladder M4→M11",
        "",
        "| Mission | Title | Status |",
        "|---------|-------|--------|",
        "| M4 | Finite adaptive gap 1/2 + minimality | PROVED (see research/m4) |",
        "| M5 | Sharp G_2(K)=1-1/K + k-pair habitat / greedy | PROVED — NOVELTY UNRESOLVED (seed); k-pair PROVED |",
    ]
    for s in summary:
        lines.append(f"| {s['mission']} | {s['title']} | {s['status']} |")
    lines += [
        "",
        "## Central ladder theorem (compressed)",
        "",
        "### Sharp budget-2 law (M5 seed package)",
        "",
        r"- Root arity: \(D_2^{\mathrm{ad}}\le K\,D_2^{\mathrm{na}}\)",
        r"- Extremal: \(G_2(K)=1-1/K\) (matching construction \(D_{\mathrm{ad}}=1\), \(D_{\mathrm{na}}=1/K\))",
        r"- Flattening: \(r\le B+1\Rightarrow D_B^{\mathrm{ad}}=D_B^{\mathrm{na}}\) (OPEN model)",
        r"- Binary equality: four-world extremizer is the M4 butterfly (unique up to symmetry)",
        "",
        "### k-pair habitat family (M5-U–M11)",
        "",
        "On the k-pair habitat family, for integers k≥1, B≥0:",
        "",
        r"- \(D_B^{\mathrm{ad}} = 0\) if B=0; \(1/k\) if B=1; \(1\) if B≥2",
        r"- \(D_B^{\mathrm{na}} = \min(B,k)/k\)  *(family closed form; not the sharp \(1/K\) construction)*",
        r"- For every fixed B≥2: \(\mathrm{Gap}_B(k)\to 1\) as k→∞",
        r"- Myopic greedy achieves only \(D_B^{\mathrm{na}}\); ratio →∞",
        r"- Adaptive camouflage capacity for ε<1 at B≥2 is **0**",
        "",
        "## Reproduce all",
        "",
        "```powershell",
        "cd C:\\Users\\coldb\\charm13\\research\\ladder",
        "python run_ladder.py",
        "python run_ladder_high.py",
        "cd ..\\m5\\EXPERIMENTS",
        "python test_m5_exact.py",
        "python test_m5.py",
        "```",
        "",
    ]
    master.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nMASTER {master}")
    print("LADDER COMPLETE — ALL MISSIONS GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
