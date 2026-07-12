# M9 RESULT — Camouflage capacity zero under adaptive B≥2 on k-pair family

**Status:** `PROVED`  
**Novelty packaging:** KNOWN RESULT, NEW APPLICATION (capacity zero under strong observer — honest)  
**Product scar:** Against adaptive T1 B≥2, branching camouflage of this form cannot achieve D≤ε<1; do not market large k as adaptive-safe

## Theorems

- For B≥2 and ε<1: no k has D_B^ad(P_k,Q_k)≤ε (capacity 0)
- For B=1: D=1/k →0 so arbitrarily large k meet any ε>0 (capacity ∞ in k)
- Nonadaptive risk D_B^na=min(B,k)/k decreases in k

## Samples / certificates

```json
{
  "capacity_table": [
    {
      "B": 0,
      "eps": "1/2",
      "C_ad_max_k_or_inf": "\u221e"
    },
    {
      "B": 0,
      "eps": "9/10",
      "C_ad_max_k_or_inf": "\u221e"
    },
    {
      "B": 0,
      "eps": "1",
      "C_ad_max_k_or_inf": "\u221e"
    },
    {
      "B": 1,
      "eps": "1/2",
      "C_ad_max_k_or_inf": "\u221e"
    },
    {
      "B": 1,
      "eps": "9/10",
      "C_ad_max_k_or_inf": "\u221e"
    },
    {
      "B": 1,
      "eps": "1",
      "C_ad_max_k_or_inf": "\u221e"
    },
    {
      "B": 2,
      "eps": "1/2",
      "C_ad_max_k_or_inf": 0
    },
    {
      "B": 2,
      "eps": "9/10",
      "C_ad_max_k_or_inf": 0
    },
    {
      "B": 2,
      "eps": "1",
      "C_ad_max_k_or_inf": "\u221e"
    },
    {
      "B": 3,
      "eps": "1/2",
      "C_ad_max_k_or_inf": 0
    },
    {
      "B": 3,
      "eps": "9/10",
      "C_ad_max_k_or_inf": 0
    },
    {
      "B": 3,
      "eps": "1",
      "C_ad_max_k_or_inf": "\u221e"
    },
    {
      "B": 4,
      "eps": "1/2",
      "C_ad_max_k_or_inf": 0
    },
    {
      "B": 4,
      "eps": "9/10",
      "C_ad_max_k_or_inf": 0
    },
    {
      "B": 4,
      "eps": "1",
      "C_ad_max_k_or_inf": "\u221e"
    },
    {
      "B": 5,
      "eps": "1/2",
      "C_ad_max_k_or_inf": 0
    },
    {
      "B": 5,
      "eps": "9/10",
      "C_ad_max_k_or_inf": 0
    },
    {
      "B": 5,
      "eps": "1",
      "C_ad_max_k_or_inf": "\u221e"
    }
  ],
  "nonadaptive_risk": [
    {
      "k": 4,
      "B": 2,
      "D_na": "1/2"
    },
    {
      "k": 4,
      "B": 5,
      "D_na": "1"
    },
    {
      "k": 10,
      "B": 2,
      "D_na": "1/5"
    },
    {
      "k": 10,
      "B": 5,
      "D_na": "1/2"
    },
    {
      "k": 100,
      "B": 2,
      "D_na": "1/50"
    },
    {
      "k": 100,
      "B": 5,
      "D_na": "1/20"
    }
  ]
}
```

## Reproduce

```powershell
cd C:\Users\coldb\charm13\research\ladder
python run_ladder.py
```

## Honesty

Closed-form on the k-pair family. Not a claim about all real filesystems. Broad adaptivity phenomena are classical; residual is exact envelope + CHARM scars.
