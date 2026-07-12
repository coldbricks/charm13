<p align="center">
  <img src="assets/boilermaker-banner.svg" alt="CHARM13" width="920"/>
</p>

<p align="center">
  <img src="assets/figures/landing_hero.png" alt="CHARM13 — wait, what is this" width="920"/>
</p>

<p align="center">
  <em>Camouflage factory + refuse-if-blown detector for encrypted-volume habitats.<br/>
  Not a new cipher. Not T4. Finite-model math included.</em>
</p>

---

### Install & try

```text
pip install -e .
charm doctor
charm bench
charm forge -o D:\packs\demo -t photo_library --placeholder -s 1024 --force
charm smell D:\packs\demo -t photo_library
charm explain score_semantics
charm explain adaptive_t1
```

<p align="center">
  <img src="assets/figures/charm_loop.png" alt="forge → smell → refuse" width="780"/>
</p>

---

## The result that should make you sit up

On an explicit family of synthetic habitats (*k* branches: ask *which*, then check that branch):

| Quantity | Value |
|----------|------:|
| Adaptive advantage at budget 2 | **1** (perfect) |
| Best fixed checklist of budget 2 | **2 / k** |
| Gap as *k* → ∞ | **→ 1** |
| Myopic “strongest local first” ratio | **k / 2 → ∞** |
| Adaptive camouflage capacity (ε &lt; 1) | **0** |

<p align="center">
  <img src="assets/figures/adaptivity_gap_B2.png" alt="Adaptivity gap at B=2" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/capacity_zero.png" alt="Capacity zero under adaptive inspection" width="860"/>
</p>

---

## Formula board

<p align="center">
  <img src="assets/figures/formula_sheet.png" alt="Closed forms" width="860"/>
</p>

| Symbol | Meaning |
|--------|---------|
| \(D_B^{\mathrm{ad}}\) | Best **adaptive** distinguishing advantage with look-budget *B* |
| \(D_B^{\mathrm{na}}\) | Best **fixed checklist** of total cost *B* |
| \(\mathrm{Gap}_B\) | How much curiosity beats a script |
| `blown_score` | Severity monoid — **not** \(P(\text{fake})\) |
| refuse | **any bad** **or** score ≥ 0.6 |

<p align="center">
  <img src="assets/figures/score_dual_gate.png" alt="Dual refuse gate" width="860"/>
</p>

| Guide | Link |
|-------|------|
| Operator doctrine | [docs/T1_BUDGET.md](docs/T1_BUDGET.md) |
| “What field is this?” | [docs/FIELD_GUIDE.md](docs/FIELD_GUIDE.md) |
| Where to publish / DOI | [docs/WHERE_TO_SHARE.md](docs/WHERE_TO_SHARE.md) |

---

## More charts

<p align="center">
  <img src="assets/figures/gap_all_B.png" alt="Gap for all B" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/budget_separation.png" alt="Budget separation adaptive vs nonadaptive" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/greedy_ratio.png" alt="Greedy approximation ratio" width="860"/>
</p>

Regenerate: `python assets/render_figures.py`  
Research ladder: [`research/LADDER_MASTER.md`](research/LADDER_MASTER.md)

```powershell
cd research\ladder
python run_ladder.py
python run_ladder_high.py
```

**Novelty packaging:** broad adaptivity phenomena are classical (`KNOWN RESULT, NEW APPLICATION`). Residual work is exact envelopes, assumptions, and product scars.

---

## Threat model

| Tier | Adversary | Claim |
|------|-----------|--------|
| T0 | Glancing human | Strong on implemented tells |
| T1 | Curious tech, short look | Helps; not a general adaptive warranty |
| T2 | Stolen disk | Crypto holds |
| T3 | Password demand | Not until CELLAR |
| T4 | Lab + process | **No claim. Ever.** |

## Habitats

`adobe_cache` (default) · `steam_depot` · `vm_disk` · `photo_library` ·  
`sql_backup` · `docker_cache` · `mail_store` · `iso_mirror` ·  
`incomplete_download` · `wgs_lab` · `generic`  

→ [docs/NATURAL.md](docs/NATURAL.md)

## Not this

New cipher · probability-of-fakery marketing · anti-forensics cookbook · T4  

## Docs

[MASTER](docs/MASTER.md) · [T1_BUDGET](docs/T1_BUDGET.md) · [FIELD_GUIDE](docs/FIELD_GUIDE.md) · [WHERE_TO_SHARE](docs/WHERE_TO_SHARE.md) · [SECURITY](SECURITY.md)

---

**Purdue black** `#000000` / `#0A0A0A` · **old gold** `#CFB991` · Boiler Up  

MIT · **v0.3.4**
