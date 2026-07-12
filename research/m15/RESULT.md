# M15 RESULT — Severity stack vs adaptive D: order can reverse across habitats

**Status:** `PROVED (construction)`  
**Novelty packaging:** ENGINEERING / hygiene (extends M4-B to ladder parameters)  
**Product scar:** Never treat warn-count as adaptive T1 risk; report policy/budgeted advantage language in research notes

## Theorems

- There exist habitat parameters where S(findings) ranks opposite to D_B^ad
- S(2 warns)<S(5 warns) but D_2(k=3)=1 > D_1(k=100)=1/100

## Samples / certificates

```json
{
  "S2": "7/16",
  "S5": "781/1024",
  "D_ad_k3_B2": "1",
  "D_ad_k100_B1": "1/100"
}
```

## Reproduce

```powershell
cd C:\Users\coldb\charm13\research\ladder
python run_ladder.py
```

## Honesty

Closed-form on the k-pair family. Not a claim about all real filesystems. Broad adaptivity phenomena are classical; residual is exact envelope + CHARM scars.
