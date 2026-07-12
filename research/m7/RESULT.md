# M7 RESULT — Myopic greedy unboundedly suboptimal for every horizon B≥2

**Status:** `PROVED`  
**Novelty packaging:** KNOWN RESULT, NEW APPLICATION (approximation barrier for greedy feature acquisition)  
**Product scar:** Do not order smell by single-finding severity alone; gate/branch queries first

## Theorems

- Myopic single-step TV never selects which (TV=0)
- After t myopic steps TV = t/k (t<=k)
- opt/greedy = k/min(B,k) → ∞ as k→∞ for each fixed B≥2

## Samples / certificates

```json
[
  {
    "B": 2,
    "k": 20,
    "greedy": "1/10",
    "opt": "1",
    "ratio": "10"
  },
  {
    "B": 3,
    "k": 20,
    "greedy": "3/20",
    "opt": "1",
    "ratio": "20/3"
  },
  {
    "B": 4,
    "k": 20,
    "greedy": "1/5",
    "opt": "1",
    "ratio": "5"
  },
  {
    "B": 5,
    "k": 20,
    "greedy": "1/4",
    "opt": "1",
    "ratio": "4"
  },
  {
    "B": 6,
    "k": 20,
    "greedy": "3/10",
    "opt": "1",
    "ratio": "10/3"
  },
  {
    "B": 7,
    "k": 20,
    "greedy": "7/20",
    "opt": "1",
    "ratio": "20/7"
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
