# M17 RESULT — Randomized nonadaptive ≤ deterministic nonadaptive (TV mixtures)

**Status:** `PROVED`  
**Novelty packaging:** KNOWN RESULT (convexity of TV) applied to CHARM checklists  
**Product scar:** Shuffling smell rule order / random subsets doesn't beat the best fixed subset of size B

## Theorems

- TV(∑α μ_i, ∑α ν_i) ≤ ∑α TV(μ_i,ν_i) ≤ max_i TV(μ_i,ν_i)
- Hence randomizing the nonadaptive checklist cannot beat best fixed checklist on any family
- On k-pairs: randomized nonadaptive still ≤ min(B,k)/k

## Samples / certificates

```json
{
  "inequality": "TV mixture bound"
}
```

## Reproduce

```powershell
cd C:\Users\coldb\charm13\research\ladder
python run_ladder.py
```

## Honesty

Closed-form on the k-pair family. Not a claim about all real filesystems. Broad adaptivity phenomena are classical; residual is exact envelope + CHARM scars.
