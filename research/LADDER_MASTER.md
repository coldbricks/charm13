# CHARM13 Research Ladder M4→M18

| Mission | Title | Status |
|---------|-------|--------|
| M4 | Finite adaptive gap + minimality + score hygiene | PROVED |
| M5 | Flattening + sharp \(G_2(K)=1-1/K\) + butterfly + \(k\)-pair | PROVED — NOVELTY UNRESOLVED (seed); \(k\)-pair PROVED |
| M6 | \(\mathrm{Gap}_B\to 1\) for all \(B\ge 2\) (\(k\)-pair) | PROVED |
| M7 | Myopic greedy unbounded failure | PROVED |
| M8 | Fixed checklist incompleteness | PROVED |
| M9 | Adaptive capacity \(0\) for \(\varepsilon<1\) | PROVED |
| M10 | \(O(1)\) closed form vs \(2^n\) DP | PROVED |
| M11 | Doctrine pack v1 | PROVED |
| M12 | Parity: adaptive \(B=1+m\) perfect; nonadaptive \(B=k\cdot m\) | PROVED |
| M13 | Unbounded adaptive/nonadaptive budget separation | PROVED |
| M14 | Nesting: M5 \(k\)-pair ≡ parity at \(m=1\) | PROVED |
| M15 | Severity stack vs adaptive \(D\): order reversals | PROVED (construction) |
| M16 | Query complexity: NA \(\Omega(k)\) vs AD \(O(1)\) for constant TV | PROVED |
| M17 | Randomized nonadaptive ≤ deterministic nonadaptive (TV) | PROVED |
| M18 | Doctrine mega-pack + full closed-form regression | PROVED (meta) + DOCTRINE READY |

Canonical formal statements: [`THEOREMS.md`](THEOREMS.md).

## Compressed theory

### Sharp budget-2 law (M5 seed package)

\[
r\le B+1\Rightarrow D_B^{\mathrm{ad}}=D_B^{\mathrm{na}}
\qquad\text{(OPEN flattening)}
\]

\[
D_2^{\mathrm{ad}}\le K\,D_2^{\mathrm{na}},
\qquad
G_2(K)=1-\frac1K
\quad\text{(matching construction \(D_{\mathrm{ad}}=1\), \(D_{\mathrm{na}}=1/K\))}
\]

Binary equality: four-world extremizer is the M4 butterfly (unique up to symmetry).

### 1-bit \(k\)-pair habitat (M5-U–M11, M14–M17)

- \(D_B^{\mathrm{ad}}=0,1/k,1\) for \(B=0,1,\ge 2\)
- \(D_B^{\mathrm{na}}=\min(B,k)/k\) *(family closed form; not the sharp \(1/K\) construction)*
- Greedy myopic first-query ratio \(k/2\to\infty\)
- Capacity zero under adaptive \(B\ge 2\) for all \(\varepsilon<1\)

### \(m\)-bit parity (M12–M13)

- \(D_B^{\mathrm{ad}}=1\) if \(B\ge 1+m\); \(1/k\) if \(m\le B<1+m\); else \(0\)
- \(D_B^{\mathrm{na}}=\min(\lfloor B/m\rfloor,k)/k\); perfect at \(B\ge k\cdot m\)

### Open frontier

\(G_2(K,r)\); \(K>2\) equality class; sharp \(G_B(K)\) for \(B\ge 3\); guarded compilation; Lean; primary-source collision.

## Reproduce

```powershell
cd research\ladder
python run_ladder.py
python run_ladder_high.py
cd ..\m5\EXPERIMENTS
python test_m5_exact.py
python test_m5.py
```
