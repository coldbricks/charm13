# M16 RESULT — Query complexity: nonadaptive Ω(k) vs adaptive O(1) for constant TV

**Status:** `PROVED`  
**Novelty packaging:** KNOWN RESULT, NEW APPLICATION (query complexity packaging)  
**Product scar:** Bench should stress high-k branching habitats; fixed short checklists fail systematically

## Theorems

- For 1-bit k-pair: D_ad reaches 1 at B=2 for all k
- D_na ≥ 1/2 requires B ≥ ceil(k/2)
- Nonadaptive query complexity for constant advantage is Θ(k); adaptive is O(1)

## Samples / certificates

```json
[
  {
    "k": 4,
    "B_na_for_TV_half": 2,
    "B_ad_for_TV_1": 2,
    "ratio": "1"
  },
  {
    "k": 10,
    "B_na_for_TV_half": 5,
    "B_ad_for_TV_1": 2,
    "ratio": "5/2"
  },
  {
    "k": 50,
    "B_na_for_TV_half": 25,
    "B_ad_for_TV_1": 2,
    "ratio": "25/2"
  },
  {
    "k": 100,
    "B_na_for_TV_half": 50,
    "B_ad_for_TV_1": 2,
    "ratio": "25"
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
