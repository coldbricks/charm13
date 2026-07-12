# M12 RESULT — Parity payload: adaptive B=1+m perfect; nonadaptive needs B=k·m

**Status:** `PROVED`  
**Novelty packaging:** KNOWN RESULT, NEW APPLICATION (parity + adaptivity; strengthens M5 with locality)  
**Product scar:** Global parity/manifest relations need adaptive path selection; static local magic is weak

## Theorems

- Even/odd parity per branch; single bits matched under P,Q
- D_ad=1 for B≥1+m; D_ad=1/k for m≤B<1+m; D_ad=0 for B<m
- D_na=min(⌊B/m⌋,k)/k; perfect nonadaptive only at B≥k·m
- Budget separation adaptive vs nonadaptive grows as k·m − (1+m) →∞ with k

## Samples / certificates

```json
[
  {
    "k": 1,
    "m": 1,
    "B": 0,
    "D_ad": "0",
    "D_na": "0",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 1,
    "B": 1,
    "D_ad": "1",
    "D_na": "1",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 1,
    "B": 2,
    "D_ad": "1",
    "D_na": "1",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 1,
    "B": 3,
    "D_ad": "1",
    "D_na": "1",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 2,
    "B": 0,
    "D_ad": "0",
    "D_na": "0",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 2,
    "B": 1,
    "D_ad": "0",
    "D_na": "0",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 2,
    "B": 2,
    "D_ad": "1",
    "D_na": "1",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 2,
    "B": 3,
    "D_ad": "1",
    "D_na": "1",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 2,
    "B": 4,
    "D_ad": "1",
    "D_na": "1",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 3,
    "B": 0,
    "D_ad": "0",
    "D_na": "0",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 3,
    "B": 1,
    "D_ad": "0",
    "D_na": "0",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 3,
    "B": 2,
    "D_ad": "0",
    "D_na": "0",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 3,
    "B": 3,
    "D_ad": "1",
    "D_na": "1",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 3,
    "B": 4,
    "D_ad": "1",
    "D_na": "1",
    "gap": "0"
  },
  {
    "k": 1,
    "m": 3,
    "B": 5,
    "D_ad": "1",
    "D_na": "1",
    "gap": "0"
  },
  {
    "k": 2,
    "m": 1,
    "B": 0,
    "D_ad": "0",
    "D_na": "0",
    "gap": "0"
  },
  {
    "k": 2,
    "m": 1,
    "B": 1,
    "D_ad": "1/2",
    "D_na": "1/2",
    "gap": "0"
  },
  {
    "k": 2,
    "m": 1,
    "B": 2,
    "D_ad": "1",
    "D_na": "1",
    "gap": "0"
  },
  {
    "k": 2,
    "m": 1,
    "B": 3,
    "D_ad": "1",
    "D_na": "1",
    "gap": "0"
  },
  {
    "k": 2,
    "m": 2,
    "B": 0,
    "D_ad": "0",
    "D_na": "0",
    "gap": "0"
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
