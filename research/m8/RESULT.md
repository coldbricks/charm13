# M8 RESULT — Fixed nonadaptive suite cannot dominate adaptive T1 (uniformly)

**Status:** `PROVED`  
**Novelty packaging:** KNOWN RESULT, NEW APPLICATION (checklist incompleteness theorem for CHARM)  
**Product scar:** Passing a fixed-size smell suite is not a uniform T1 risk certificate

## Theorems

- ∀B∀ε∈(0,1)∃k: D_B^na(P_k,Q_k)≤ε and D_2^ad(P_k,Q_k)=1
- min such k = min_k_nonadaptive_below_eps(B,ε)

## Samples / certificates

```json
[
  {
    "B": 1,
    "eps": "1/2",
    "k": 2,
    "D_na": "1/2",
    "D_ad_B2": "1"
  },
  {
    "B": 1,
    "eps": "1/10",
    "k": 10,
    "D_na": "1/10",
    "D_ad_B2": "1"
  },
  {
    "B": 1,
    "eps": "1/100",
    "k": 100,
    "D_na": "1/100",
    "D_ad_B2": "1"
  },
  {
    "B": 2,
    "eps": "1/2",
    "k": 4,
    "D_na": "1/2",
    "D_ad_B2": "1"
  },
  {
    "B": 2,
    "eps": "1/10",
    "k": 20,
    "D_na": "1/10",
    "D_ad_B2": "1"
  },
  {
    "B": 2,
    "eps": "1/100",
    "k": 200,
    "D_na": "1/100",
    "D_ad_B2": "1"
  },
  {
    "B": 3,
    "eps": "1/2",
    "k": 6,
    "D_na": "1/2",
    "D_ad_B2": "1"
  },
  {
    "B": 3,
    "eps": "1/10",
    "k": 30,
    "D_na": "1/10",
    "D_ad_B2": "1"
  },
  {
    "B": 3,
    "eps": "1/100",
    "k": 300,
    "D_na": "1/100",
    "D_ad_B2": "1"
  },
  {
    "B": 4,
    "eps": "1/2",
    "k": 8,
    "D_na": "1/2",
    "D_ad_B2": "1"
  },
  {
    "B": 4,
    "eps": "1/10",
    "k": 40,
    "D_na": "1/10",
    "D_ad_B2": "1"
  },
  {
    "B": 4,
    "eps": "1/100",
    "k": 400,
    "D_na": "1/100",
    "D_ad_B2": "1"
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
