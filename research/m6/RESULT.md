# M6 RESULT — Gap_B → 1 for every fixed B ≥ 2

**Status:** `PROVED`  
**Novelty packaging:** KNOWN RESULT, NEW APPLICATION (strengthens M5 from B=2 to all B>=2)  
**Product scar:** Any fixed look-budget checklist is arbitrarily weak vs adaptive as branching grows

## Theorems

- D_ad(k,B)=1/k if B==1 else (0 if B==0 else 1 for B>=2)
- D_na(k,B)=min(B,k)/k
- for each B>=2: lim_k Gap_B(k)=1

## Samples / certificates

```json
[
  {
    "k": 1,
    "B": 0,
    "D_ad": "0",
    "D_na": "0",
    "gap": "0"
  },
  {
    "k": 3,
    "B": 1,
    "D_ad": "1/3",
    "D_na": "1/3",
    "gap": "0"
  },
  {
    "k": 5,
    "B": 2,
    "D_ad": "1",
    "D_na": "2/5",
    "gap": "3/5"
  },
  {
    "k": 7,
    "B": 3,
    "D_ad": "1",
    "D_na": "3/7",
    "gap": "4/7"
  },
  {
    "k": 9,
    "B": 4,
    "D_ad": "1",
    "D_na": "4/9",
    "gap": "5/9"
  },
  {
    "k": 11,
    "B": 5,
    "D_ad": "1",
    "D_na": "5/11",
    "gap": "6/11"
  },
  {
    "k": 13,
    "B": 6,
    "D_ad": "1",
    "D_na": "6/13",
    "gap": "7/13"
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
