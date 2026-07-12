# CHARM13 Research Ladder M4→M18

| Mission | Title | Status |
|---------|-------|--------|
| M4 | Finite adaptive gap + minimality | PROVED |
| M5 | Unbounded gap at B=2 | PROVED |
| M6 | Gap_B→1 for all B≥2 | PROVED |
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

### 1-bit k-pair (M5–M11, M14–M17)
- \(D_B^{\mathrm{ad}}=0,1/k,1\) for B=0,1,≥2
- \(D_B^{\mathrm{na}}=\min(B,k)/k\)

### m-bit parity (M12–M13)
- \(D_B^{\mathrm{ad}}=1\) if B≥1+m; \(1/k\) if m≤B<1+m; else 0
- \(D_B^{\mathrm{na}}=\min(\lfloor B/m\rfloor,k)/k\); perfect at B≥k·m

## Reproduce

```powershell
cd C:\Users\coldb\charm13\research\ladder
python run_ladder.py
python run_ladder_high.py
```
