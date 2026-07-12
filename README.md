<p align="center">
  <img src="assets/boilermaker-banner.svg" alt="CHARM13 — Purdue black and gold" width="880"/>
</p>

# CHARM13

**Camouflage factory and detection oracle for encrypted-volume cover stories.**

Ciphertext conceals content. It does not conceal *intent*.  
A cover is **blown** if it is not natural for the habitat it claims.

This is not a new cipher. Layer-0 confidentiality is borrowed (e.g. VeraCrypt).  
CHARM13 owns **cover construction**, **habitat ecology**, and **refuse-if-blown** detection.

```text
pip install -e .
charm doctor
charm bench
charm templates
charm forge -o D:\packs\demo -t photo_library --placeholder -s 1024 --force
charm smell D:\packs\demo -t photo_library
charm explain score_semantics
charm explain adaptive_t1
```

## Loop

```text
construct cover → measure smell → refuse if blown
```

| Layer | Job |
|-------|-----|
| Cipher (L0) | VeraCrypt or equivalent |
| Cover / habitat (L2–L3) | `forge` + templates |
| Detection (L4) | `smell` + dual refuse gate |

## Threat model

| Tier | Adversary | Claim |
|------|-----------|--------|
| T0 | Glancing human | Strong on implemented tells |
| T1 | Curious tech, short look | Helps on implemented checks; **not** a general adaptive warranty — see [docs/T1_BUDGET.md](docs/T1_BUDGET.md) |
| T2 | Stolen disk | Crypto holds; cover may reduce prioritization |
| T3 | Password demand | Not a product claim until CELLAR |
| T4 | Lab + process | **No claim. Ever.** |

## Habitats

`adobe_cache` (default) · `steam_depot` · `vm_disk` · `photo_library` ·  
`sql_backup` · `docker_cache` · `mail_store` · `iso_mirror` ·  
`incomplete_download` · `wgs_lab` · `generic`

See [docs/NATURAL.md](docs/NATURAL.md). Payloads use **opaque** names when the
volume is not a real public format. Specialist extensions are checked for magic
and habitat membership.

## Commands

| Command | Purpose |
|---------|---------|
| `charm forge` | Build habitat tree + optional volume |
| `charm smell` | Findings + severity score + dual refuse |
| `charm bench` | Calibration fixtures |
| `charm explain [code]` | Catalog (try `score_semantics`, `adaptive_t1`) |
| `charm doctor` | Environment |
| `charm templates` | List habitats |
| `charm which-vc` | Locate VeraCrypt |

Forge refuses when the cover is **blown** unless `--i-know`.

## Score (read carefully)

```text
blown_score = 1 − Π (1 − w_i)     # bad=0.55, warn=0.25, info=0.05
refused     = (any bad finding)  ∨  (blown_score ≥ 0.6)
```

| Fact | Meaning |
|------|---------|
| Weights | Ordinal **engineering severities**, not calibrated probabilities |
| Product formula | Severity monoid (noisy-OR algebra), **not** P(generated) |
| Dual gate | One `bad` alone scores 0.55 but still **blows** |
| Clean smell | Necessary refuse machinery — **not** a complete adaptive T1 bound |

`charm bench` must keep scoring classic fake-specialist packs as BLOWN.

## Research (finite-model doctrine)

Budgeted adaptive inspection of synthetic habitats is developed under
[`research/`](research/LADDER_MASTER.md) (missions M4–M18): exact total-variation
certificates, unbounded adaptivity gaps at fixed look-budgets, capacity-zero
results under adaptive observers on the k-pair/parity families, and score hygiene.

**Packaging:** broad adaptivity phenomena are classical
(`KNOWN RESULT, NEW APPLICATION`); the residual is exact envelopes, assumptions,
and product scars. See [docs/T1_BUDGET.md](docs/T1_BUDGET.md).

```powershell
cd research\ladder
python run_ladder.py
python run_ladder_high.py
```

## Not this

- New cipher  
- T4 guarantees  
- Probability-of-fakery marketing for `blown_score`  
- Operational playbooks for concealing data from forensic inspection  
- Exhaustive file-type encyclopedia (impossible); naturalness rules instead  

## Docs

| Document | Role |
|----------|------|
| [docs/MASTER.md](docs/MASTER.md) | Binding doctrine |
| [docs/NATURAL.md](docs/NATURAL.md) | Habitats |
| [docs/T1_BUDGET.md](docs/T1_BUDGET.md) | Score semantics + adaptive T1 |
| [docs/SKUNKWORKS.md](docs/SKUNKWORKS.md) | Process |
| [SECURITY.md](SECURITY.md) | Security notes |
| [research/LADDER_MASTER.md](research/LADDER_MASTER.md) | Math ladder index |

## Colors

Boilermaker **black** (`#000000`) and Purdue **old gold** (`#CFB991`). Boiler Up.

## License

MIT. Version **0.3.4**.
