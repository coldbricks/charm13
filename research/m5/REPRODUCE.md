# Reproduce M5

No third-party Python packages required (stdlib only for exact certificates).

## Sharp seed package

```powershell
cd research\m5\EXPERIMENTS
python test_m5_exact.py
python m5_exact.py
```

Expected:

- M4 adaptive $1$, nonadaptive $1/2$
- For each $K\in\\{2,\ldots,7\\}$: adaptive $1$, nonadaptive $1/K$
- Four raw four-world extremal cores (symmetry class of the butterfly)
- Small-support sanity sweep checks $>0$ instances with no adaptivity gap at $B=2$

## k-pair habitat package

```powershell
cd research\m5\EXPERIMENTS
python test_m5.py
python enum_core.py
```

Expected: for $k=2..12$, $D_{\mathrm{ad}}=1$, $D_{\mathrm{na}}=2/k$, greedy first query is a bit, greedy TV $2/k$.

## Ladder regression

```powershell
cd research\ladder
python run_ladder.py
python run_ladder_high.py
```

## Rational arithmetic

All certificates use `fractions.Fraction`. Floating-point is not authoritative.
