# M10 RESULT — Exact computation: O(1) closed form on k-pairs; DP 2^n fallback

**Status:** `PROVED (algorithm + complexity observation)`  
**Novelty packaging:** ENGINEERING ADAPTATION / known DP pattern + family-specific O(1)  
**Product scar:** Research CLI can certify k-pair risk in O(1); general habitats need structure or bounds

## Theorems

- On k-pair family, D_ad and D_na computable in O(1) given (k,B) via closed form
- General finite instances: exact adaptive value via subset DP in time 2^n · B · |Q| · poly
- Barrier: n=2k grows with branching; unstructured DP explodes — structure is essential

## Samples / certificates

```json
{
  "mission": "M10",
  "title": "Exact computation: O(1) closed form on k-pairs; DP 2^n fallback",
  "status": "PROVED (algorithm + complexity observation)",
  "theorems": [
    "On k-pair family, D_ad and D_na computable in O(1) given (k,B) via closed form",
    "General finite instances: exact adaptive value via subset DP in time 2^n \u00b7 B \u00b7 |Q| \u00b7 poly",
    "Barrier: n=2k grows with branching; unstructured DP explodes \u2014 structure is essential"
  ],
  "novelty": "ENGINEERING ADAPTATION / known DP pattern + family-specific O(1)",
  "product_scar": "Research CLI can certify k-pair risk in O(1); general habitats need structure or bounds",
  "dp_complexity": "O(2^n * B * |Q|)",
  "structured_complexity": "O(1) for k-pair closed form"
}
```

## Reproduce

```powershell
cd C:\Users\coldb\charm13\research\ladder
python run_ladder.py
```

## Honesty

Closed-form on the k-pair family. Not a claim about all real filesystems. Broad adaptivity phenomena are classical; residual is exact envelope + CHARM scars.
