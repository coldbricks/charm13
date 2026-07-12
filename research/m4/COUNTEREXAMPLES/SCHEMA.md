# Counterexample / witness JSON schema

Each file: `COUNTEREXAMPLES/<id>.json`

## Required fields

| Field | Type | Meaning |
|-------|------|---------|
| `id` | string | Unique id, e.g. `wit-A-star-001` |
| `kills_or_witnesses` | string | Claim id, e.g. `M4-A` |
| `role` | string | `kill` or `witness` |
| `P` | object | `{ "trees": [...], "probs": ["1/2", ...] }` |
| `Q` | object | same |
| `tree_encoding` | string or object | How trees are represented |
| `queries` | array | Query descriptors |
| `costs` | object | query_id → cost string |
| `budget` | int or string | B |
| `D_adaptive` | string | Fraction, e.g. `"1/2"` |
| `D_nonadaptive` | string | Fraction |
| `optimal_policy` | object | enough to reproduce |
| `claimed_policy` | object | policy under attack, if kill |
| `advantage_gap` | string | Fraction `D - D_na` or other gap |
| `notes` | string | free text |

## Tree encoding (recommended)

```json
{
  "nodes": [
    {"id": "r", "parent": null, "attrs": {"kind": "dir", "base": "root"}},
    {"id": "a", "parent": "r", "attrs": {"kind": "file", "magic": 1}}
  ]
}
```

## Probability rules

- `probs[i]` is a string rational `"p/q"`.  
- Sum under P and under Q must be `1`.  
- Prefer denominators ≤ 12 for hunt instances.

## Example skeleton

See `_template.json` in this directory.
