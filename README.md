<p align="center">
  <img src="assets/boilermaker-banner.svg" alt="CHARM13" width="920"/>
</p>

<p align="center">
  <img src="assets/figures/landing_hero.png" alt="CHARM13 overview" width="920"/>
</p>

<p align="center"><em>
Camouflage factory and detection oracle for encrypted-volume habitats.<br/>
Construct a cover. Smell it. Refuse if blown. Measure the limits of that oracle.
</em></p>

---

## Abstract

Encrypted volumes solve confidentiality of **bytes**. They do not solve the problem of **narrative**. A multi-gigabyte high-entropy blob named like a lab product, dropped beside toy decoys, does not fail cryptanalysis—it fails *plausibility*. CHARM13 treats that failure mode as an engineering object: habitats are constructed, measured by a detection oracle, and **refused** when the cover is blown.

The system is deliberately layered. Layer 0 (cipher) is borrowed—VeraCrypt or an equivalent volume tool. CHARM13 owns cover construction (templates, identities, decoys, size bands, checksums), ecological constraints (which specialist formats belong in which habitat), and the refuse loop. The product promise is not “undetectable encryption.” The product promise is a **detection-backed camouflage workflow** with honest threat-model tiers and an explicit refusal path.

Alongside the tool sits a finite-model research program on **budgeted adaptive inspection**. A short inspection is not necessarily a fixed checklist. An adaptive policy may choose the next observation from the transcript so far. On explicit synthetic habitat families, the gap between adaptive and nonadaptive distinguishing power can be driven arbitrarily close to its theoretical maximum at fixed look-budget. That fact is packaged as doctrine for operators: clean static smell is necessary machinery, not a certificate against every curious adaptive look of similar length.

```text
pip install -e .
charm doctor
charm bench
charm templates
charm forge -o D:\packs\demo -t photo_library --placeholder -s 1024 --force
charm smell D:\packs\demo -t photo_library
charm explain score_semantics
charm explain adaptive_t1
charm explain gate_before_local
```

<p align="center">
  <img src="assets/figures/anim_loop.gif" alt="FORGE → SMELL → REFUSE" width="720"/>
</p>

---

## Design thesis

Three commitments structure the project.

**1. Naturalness is habitat-relative.**  
A cover is blown if it is unnatural *for the habitat it claims*—not if it fails an encyclopedia of every file type on Earth. Genomics packs were an early calibration fixture because they fail loudly when faked; they are not the product identity. Habitats include media caches, steam depots, VM disks, photo libraries, SQL handoffs, docker layers, mail stores, ISO mirrors, incomplete downloads, optional WGS lab packs, and untyped bulk.

**2. Detection is first-class.**  
Forge without smell is cosplay. Smell without refuse is advisory theater. The default path is: construct, measure, exit non-zero when blown unless the operator explicitly overrides with `--i-know`.

**3. Claims are tiered and finite.**  
T0–T1 are the product-facing inspection regimes. T2 depends on borrowed crypto. T3 waits on CELLAR. T4 is never claimed. Research results are finite-model statements with assumptions named; they are not laboratory warranties.

---

## The mathematical spine (animated)

**Sharp finite law (budget 2, OPEN queries, active arity ≤ K):**

\[
G_2(K)=\sup\bigl(D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}\bigr)=1-\frac1K.
\]

Binary case: gap at most **1/2**, attained by the M4 four-world butterfly (support-minimal and gap-maximal). Proof package: [`research/m5/`](research/m5/). Novelty of the sharp law is **unresolved** pending primary-source collision; do not read this as a claim of invention.

**Habitat application (k-pair family)**—uniform random branch, payload bit differs under the two hypotheses, off-branch bits return `na`—an adaptive policy with budget two (observe branch identity, then the bit on that branch) achieves total-variation advantage **1**. The best nonadaptive suite of budget two achieves **2/k**. The gap is **1 − 2/k**, which tends to **1** as branching grows. Myopic “pick the locally strongest single check first” never opens with the branch query and suffers approximation ratio **k/2**. (This \(2/k\) is a habitat closed form, not the sharp universal \(1/K\).)

<p align="center">
  <img src="assets/figures/anim_gap_growth.gif" alt="Adaptive vs nonadaptive advantage as k grows" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/anim_gap_to_one.gif" alt="Gap approaching one" width="860"/>
</p>

On the k-pair family the same envelope extends to every fixed budget B ≥ 2: nonadaptive advantage is min(B,k)/k while adaptive advantage saturates at 1 once B ≥ 2. A fixed-size checklist therefore cannot uniformly bound adaptive risk across all branching factors.

<p align="center">
  <img src="assets/figures/gap_all_B.png" alt="Gap for multiple budgets" width="860"/>
</p>

For **parity-style payloads** (local bit marginals matched; global parity differs per branch), adaptive perfect separation costs **1+m** looks (select branch, then read m bits). Nonadaptive perfect separation requires instrumenting every branch fully: budget **k·m**. The ratio grows without bound in k.

<p align="center">
  <img src="assets/figures/anim_budget_race.gif" alt="Adaptive vs nonadaptive budget race" width="860"/>
</p>

Under adaptive inspection with B ≥ 2 on the k-pair family, indistinguishability capacity for any ε &lt; 1 is **zero**: no branching factor reduces adaptive advantage below one. Large k helps checklists; it does not help against that adaptive policy class.

<p align="center">
  <img src="assets/figures/anim_capacity_zero.gif" alt="Capacity zero under adaptive inspection" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/formula_sheet.png" alt="Closed-form board" width="860"/>
</p>

Static charts and SVG sources live in [`assets/figures/`](assets/figures/). Regenerate:

```powershell
python assets/render_figures.py
python assets/render_animations.py
```

Research index: [`research/LADDER_MASTER.md`](research/LADDER_MASTER.md) (missions M4–M18, exact rational certificates).

```powershell
cd research\ladder
python run_ladder.py
python run_ladder_high.py
```

**Novelty packaging.** The abstract phenomenon that adaptivity can dominate nonadaptive experiments is classical (sequential hypothesis testing, costly feature acquisition). The M5 sharp seed package (\(G_2(K)=1-1/K\), flattening, butterfly uniqueness) is **proved in the frozen model; literature novelty unresolved**. Residual repository contribution includes exact closed forms on filesystem-shaped query models, reproducible certificates, assumption hygiene (including path-prefix legality), and **product scars**—doctrine that changes how the tool describes itself.

---

## Score semantics (binding)

<p align="center">
  <img src="assets/figures/score_dual_gate.png" alt="Dual refuse gate" width="860"/>
</p>

```text
blown_score = 1 − Π_i (1 − w_sev(i))     # bad=0.55, warn=0.25, info=0.05
refused     = (∃ finding with severity bad)  ∨  (blown_score ≥ 0.6)
```

| Fact | Implication |
|------|-------------|
| Weights are ordinal | Not calibrated likelihoods or posteriors |
| Product is a monoid | Commutative severity aggregation, not P(generated) |
| Dual gate | One bad finding alone scores 0.55 and still refuses |
| Clean report | Necessary for refuse automation—not a full adaptive T1 bound |

Operator doctrine: [`docs/T1_BUDGET.md`](docs/T1_BUDGET.md) · field positioning: [`docs/FIELD_GUIDE.md`](docs/FIELD_GUIDE.md) · dissemination: [`docs/WHERE_TO_SHARE.md`](docs/WHERE_TO_SHARE.md)

```text
charm explain score_semantics
charm explain adaptive_t1
charm explain gate_before_local
```

---

## Threat model

| Tier | Adversary | CHARM13 claim |
|------|-----------|----------------|
| **T0** | Glancing human | Strong on implemented tells |
| **T1** | Curious technical peer, short session | Improves cost of casual tells; static smell is nonadaptive; see T1_BUDGET |
| **T2** | Offline stolen disk | Crypto holds if L0 holds; cover may affect prioritization only |
| **T3** | Compelled password | Not a product claim until CELLAR |
| **T4** | Laboratory process + time | **No claim. Ever.** |

---

## Habitats

| Template | Narrative |
|----------|-----------|
| `adobe_cache` | Media cache debris (default) |
| `steam_depot` | Local depot fragment |
| `vm_disk` | VM metadata + disk-like blob |
| `photo_library` | Managed library store |
| `sql_backup` | Database dump handoff |
| `docker_cache` | Overlay / layer residue |
| `mail_store` | Mailbox export slice |
| `iso_mirror` | Install media fragment |
| `incomplete_download` | Interrupted transfer |
| `wgs_lab` | Optional sequencing pack habitat |
| `generic` | Untyped bulk |

Naturalness law and ecology rules: [`docs/NATURAL.md`](docs/NATURAL.md).  
Payloads use **opaque** extensions when the volume is not a genuine public format. Specialist names are checked for magic and habitat membership. Famous public sample IDs are forbidden as decoration. Published checksums must match bytes.

---

## Commands

| Command | Purpose |
|---------|---------|
| `charm forge` | Build habitat tree + optional volume / placeholder |
| `charm smell` | Findings, severity score, dual refuse |
| `charm bench` | Calibration fixtures (known-bad must blow) |
| `charm explain [code]` | Finding catalog |
| `charm doctor` | Environment + doctrine pointers |
| `charm templates` | List habitats |
| `charm which-vc` | Locate VeraCrypt |

Forge refuses blown covers by default. `--i-know` is an informed override. `--write-seed` is off by default (operator receipt is T1-visible). Size ceilings require `--unsafe-size` when deliberately exceeded.

---

## Architecture (abbreviated)

```text
charm
├── forge      constructor + refuse gate
├── smell      findings + severity monoid + dual gate
├── props      habitat decoy trees
├── caliper    size bands / opaque payload policy
├── ecology    specialist families + habitat membership
├── forgery    seeded identity fields
├── kernel     VeraCrypt create (L0)
├── bench      fixtures
└── catalog    explain surface
```

Binding doctrine: [`docs/MASTER.md`](docs/MASTER.md) · process: [`docs/SKUNKWORKS.md`](docs/SKUNKWORKS.md) · security notes: [`SECURITY.md`](SECURITY.md)

---

## Research program (M4–M18)

The ladder under `research/` develops, in increasing strength:

- exact adaptive-versus-nonadaptive gap certificates  
- size-minimality under unguarded depth-two policies  
- unbounded gap envelopes for every fixed B ≥ 2  
- myopic greedy failure with unbounded ratio  
- checklist incompleteness theorems  
- adaptive capacity-zero statements on the k-pair family  
- parity payload budget separation B*_ad = 1+m vs B*_na = k·m  
- query-complexity form (nonadaptive Ω(k) vs adaptive O(1) for constant advantage)  
- product doctrine mapping math → smell/docs  

Reproduce certificates with the ladder runners and `research/m4` / `research/m5` test suites. Static and animated figures are first-class artifacts of that program, not decoration.

---

## Explicit non-goals

- Inventing or “improving” ciphers  
- Probability-of-generation marketing for `blown_score`  
- Operational guidance for concealing material from forensic inspection  
- Exhaustive file-type encyclopedias  
- T4 claims under any packaging  

---

## Colors

**Purdue black** `#000000` / `#0A0A0A` · **old gold** `#CFB991` · Boiler Up.

## License & version

MIT · **v0.3.5**
