# CHARM13 Research Ladder M4→M18

| Mission | Title | Status |
|---------|-------|--------|
| M4 | Finite adaptive gap + minimality | PROVED |
| M5 | Sharp G_2(K)=1-1/K + k-pair habitat / greedy | PROVED — NOVELTY UNRESOLVED (seed); k-pair PROVED |
| M6 | Gap_B→1 for all B≥2 (k-pair family) | PROVED |
| M7 | Myopic greedy unbounded failure | PROVED |
| M8 | Fixed checklist incompleteness | PROVED |
| M9 | Adaptive capacity 0 for ε<1 | PROVED |
| M10 | O(1) closed form vs 2^n DP | PROVED |
| M11 | Doctrine pack v1 | PROVED |
| M12 | Parity payload: adaptive B=1+m perfect; nonadaptive needs B=k·m | PROVED |
| M13 | Unbounded adaptive/nonadaptive budget separation (parity family) | PROVED |
| M14 | Nesting: M5 k-pair ≡ parity family at m=1 | PROVED |
| M15 | Severity stack vs adaptive D: order can reverse across habitats | PROVED (construction) |
| M16 | Query complexity: nonadaptive Ω(k) vs adaptive O(1) for constant TV | PROVED |
| M17 | Randomized nonadaptive ≤ deterministic nonadaptive (TV mixtures) | PROVED |
| M18 | Doctrine mega-pack + full closed-form regression | PROVED (meta) + DOCTRINE READY |

## Compressed theory

### Sharp budget-2 law (M5 seed package)
- Root arity: \(D_2^{\mathrm{ad}}\le K\,D_2^{\mathrm{na}}\)
- Extremal: \(G_2(K)=1-1/K\) (matching construction \(D_{\mathrm{ad}}=1\), \(D_{\mathrm{na}}=1/K\))
- Flattening: \(r\le B+1\Rightarrow D_B^{\mathrm{ad}}=D_B^{\mathrm{na}}\) (OPEN model)
- Binary equality: four-world extremizer is the M4 butterfly (unique up to symmetry)

### 1-bit k-pair habitat (M5-U–M11, M14–M17)
- \(D_B^{\mathrm{ad}}=0,1/k,1\) for B=0,1,≥2
- \(D_B^{\mathrm{na}}=\min(B,k)/k\)  *(family closed form; not the sharp \(1/K\) construction)*
- Greedy myopic first-query ratio \(k/2\to\infty\)

### m-bit parity (M12–M13)
- \(D_B^{\mathrm{ad}}=1\) if B≥1+m; \(1/k\) if m≤B<1+m; else 0
- \(D_B^{\mathrm{na}}=\min(\lfloor B/m\rfloor,k)/k\); perfect at B≥k·m

## Reproduce

```powershell
cd C:\Users\coldb\charm13\research\ladder
python run_ladder.py
python run_ladder_high.py
cd ..\m5\EXPERIMENTS
python test_m5_exact.py
python test_m5.py
```
