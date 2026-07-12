# M13 RESULT — Unbounded adaptive/nonadaptive budget separation (parity family)

**Status:** `PROVED`  
**Novelty packaging:** KNOWN RESULT, NEW APPLICATION  
**Product scar:** Checklist length must scale with branches×depth; adaptive policy length scales with depth only

## Theorems

- B_ad^*=1+m, B_na^*=k·m for perfect TV=1
- B_na^*/B_ad^* = k·m/(m+1) → ∞ as k→∞ (any fixed m≥1)
- Absolute gap B_na^*−B_ad^* = m(k−1)−1 → ∞

## Samples / certificates

```json
[
  {
    "k": 2,
    "m": 1,
    "B_ad_star": 2,
    "B_na_star": 2,
    "sep": 0,
    "ratio": "1"
  },
  {
    "k": 3,
    "m": 3,
    "B_ad_star": 4,
    "B_na_star": 9,
    "sep": 5,
    "ratio": "9/4"
  },
  {
    "k": 4,
    "m": 5,
    "B_ad_star": 6,
    "B_na_star": 20,
    "sep": 14,
    "ratio": "10/3"
  },
  {
    "k": 6,
    "m": 2,
    "B_ad_star": 3,
    "B_na_star": 12,
    "sep": 9,
    "ratio": "4"
  },
  {
    "k": 7,
    "m": 4,
    "B_ad_star": 5,
    "B_na_star": 28,
    "sep": 23,
    "ratio": "28/5"
  },
  {
    "k": 9,
    "m": 1,
    "B_ad_star": 2,
    "B_na_star": 9,
    "sep": 7,
    "ratio": "9/2"
  },
  {
    "k": 10,
    "m": 3,
    "B_ad_star": 4,
    "B_na_star": 30,
    "sep": 26,
    "ratio": "15/2"
  },
  {
    "k": 11,
    "m": 5,
    "B_ad_star": 6,
    "B_na_star": 55,
    "sep": 49,
    "ratio": "55/6"
  },
  {
    "k": 13,
    "m": 2,
    "B_ad_star": 3,
    "B_na_star": 26,
    "sep": 23,
    "ratio": "26/3"
  },
  {
    "k": 14,
    "m": 4,
    "B_ad_star": 5,
    "B_na_star": 56,
    "sep": 51,
    "ratio": "56/5"
  },
  {
    "k": 16,
    "m": 1,
    "B_ad_star": 2,
    "B_na_star": 16,
    "sep": 14,
    "ratio": "8"
  },
  {
    "k": 17,
    "m": 3,
    "B_ad_star": 4,
    "B_na_star": 51,
    "sep": 47,
    "ratio": "51/4"
  },
  {
    "k": 18,
    "m": 5,
    "B_ad_star": 6,
    "B_na_star": 90,
    "sep": 84,
    "ratio": "15"
  }
]
```

## Reproduce

```powershell
cd C:\Users\coldb\charm13\research\ladder
python run_ladder.py
```

## Honesty

Closed-form on the k-pair family. Not a claim about all real filesystems. Broad adaptivity phenomena are classical; residual is exact envelope + CHARM scars.
