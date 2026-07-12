<p align="center">
  <img src="assets/boilermaker-banner.svg" alt="CHARM13" width="920"/>
</p>

<p align="center">
  <img src="assets/figures/landing_hero.png" alt="CHARM13 — finite-model inspection geometry" width="920"/>
</p>

<p align="center"><em>
Exact envelopes for budgeted adaptive inspection.<br/>
Finite models. Matching constructions. Machine certificates.<br/>
Product doctrine is a scar of the theorems — not the other way around.
</em></p>

---

## Stance

This repository is a **finite-model research spine** with an engineering scar.

The primary object is the worst-case additive gap between adaptive and nonadaptive total variation under a look budget, in an OPEN unit-cost query model. The sharp budget-two law is proved in-model:

$$
G_2(K)=\sup\bigl(D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}\bigr)=1-\frac1K.
$$

Literature novelty of that seed package is **unresolved**. Abstract adaptivity gains are classical. What is carried here, coldly: support flattening, root-arity, matching constructions, equality classification of the binary extremizer, habitat closed forms, exact rational certificates, and the product consequences that follow if one refuses to lie about static checklists.

No T4 claims. No new cipher. No score-as-probability marketing. If a statement is not sealed, it is left blank.

Catalog · proofs · ladder:  
[`research/THEOREMS.md`](research/THEOREMS.md) · [`research/m5/SEED_THEOREMS.md`](research/m5/SEED_THEOREMS.md) · [`research/LADDER_MASTER.md`](research/LADDER_MASTER.md)

---

## Objects

Let $W$ be finite. Distributions $P,Q$. Signed mass $\mu=P-Q$. Query $q:W\to Y_q$. Adaptive policies: decision trees of depth $\le B$. Nonadaptive policies: at most $B$ queries fixed in advance. Objectives $D_B^{\mathrm{ad}}$, $D_B^{\mathrm{na}}$ = optimal transcript total variation. Active support:

$$
r=\bigl|\\{w:\mu(w)\ne 0\\}\bigr|.
$$

**OPEN** means globally addressable, unit cost, non-destructive — unless a theorem says otherwise.

---

## Crown theorems (proved in the frozen OPEN model)

### Flattening

If $r\le B+1$, then

$$
D_B^{\mathrm{ad}}(P,Q)=D_B^{\mathrm{na}}(P,Q).
$$

A budget-two adaptivity gap therefore requires at least **four** active worlds.

### Root-arity and sharp law

If every query has active arity at most $K$, then at budget two

$$
D_2^{\mathrm{ad}}\le K\\,D_2^{\mathrm{na}},
\qquad
D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}\le 1-\frac1K.
$$

Both bounds are **exactly sharp**: there exists a finite construction with $D_2^{\mathrm{ad}}=1$ and $D_2^{\mathrm{na}}=1/K$. Hence the exact worst-case additive gap is

$$
\boxed{G_2(K)=1-\dfrac{1}{K}.}
$$

Binary case $K=2$: additive gap at most $1/2$, attained by the four-world **butterfly**, which is unique up to natural symmetries among support-minimal binary extremizers.

**Novelty of the sharp seed package is unresolved.** The abstract fact that adaptivity can dominate nonadaptive experiments is classical (sequential testing, costly feature acquisition, classification trees). Residual value: support flattening, exact root-arity envelope, equality classification of the butterfly, first stability statement, habitat closed forms, and product scars.

<p align="center">
  <img src="assets/figures/equation_wall.png" alt="Identity wall" width="920"/>
</p>

<p align="center">
  <img src="assets/figures/formalism_board.png" alt="Signed-measure formalism" width="720"/>
</p>

<p align="center">
  <img src="assets/figures/theorem_board.png" alt="Flattening and sharp budget-two law" width="720"/>
</p>

<p align="center">
  <img src="assets/figures/address_construction.png" alt="Address matching construction" width="720"/>
</p>

<p align="center">
  <img src="assets/figures/butterfly_board.png" alt="Four-world butterfly extremizer" width="720"/>
</p>

<p align="center">
  <img src="assets/figures/formula_sheet.png" alt="Closed-form board" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/adaptivity_gap_B2.png" alt="Budget-2 adaptivity envelope" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/anim_gap_growth.gif" alt="Gap growth" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/anim_gap_to_one.gif" alt="G2 approaches 1" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/anim_dual_envelope.gif" alt="Dual envelopes" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/anim_gap_surface_3d.gif" alt="3D Gap_B(k) surface" width="720"/>
</p>

<p align="center">
  <img src="assets/figures/anim_g2_support_3d.gif" alt="3D G2(K,r) envelope sketch" width="720"/>
</p>

---

## Formal apparatus

$$
\mu:=P-Q,\quad
\sum_{w\in W}\mu(w)=0,\quad
S_\mu=\\{w:\mu(w)\ne0\\},\quad
r=|S_\mu|.
$$

$$
V_\mu(\Pi)=\frac12\sum_{C\in\Pi}|\mu(C)|
=\mathrm{TV}(\mathrm{Law}_P T,\mathrm{Law}_Q T).
$$

Bayes bridge (weighted classification trees):

$$
M(w,0)=\tfrac12 P(w),\\;
M(w,1)=\tfrac12 Q(w),\qquad
V_\mu(\Pi)=1-2R(\Pi),
$$

$$
D_B^{\mathrm{ad}}=1-2R_B^{\mathrm{tree}},\qquad
D_B^{\mathrm{na}}=1-2R_B^{\mathrm{static}}.
$$

Root-arity proof core: $V(\pi)=\sum_{i=1}^k v_i$ and $D_2^{\mathrm{na}}\ge\max_i v_i$, hence

$$
D_2^{\mathrm{ad}}\le K\\,D_2^{\mathrm{na}},\qquad
D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}\le\Bigl(1-\frac1K\Bigr)D_2^{\mathrm{ad}}\le 1-\frac1K.
$$

Matching address family $W_K=\\{(i,x):i\le K,\\;x\in\\{0,1\\}^K\\}$:

$$
P(i,x)=\frac{\mathbf{1}_{x_i=0}}{K\\,2^{K-1}},\quad
Q(i,x)=\frac{\mathbf{1}_{x_i=1}}{K\\,2^{K-1}},\quad
g(i,x)=i,\\; b_j(i,x)=x_j.
$$

Gain-sensitive support bound and open curve:

$$
D_2^{\mathrm{na}}\ge V_0+\max_i g_i,\qquad
m\le\min\Bigl\\{K,\Big\lfloor\tfrac r2\Big\rfloor\Bigr\\},
$$

$$
G_2(K,r)=\sup\bigl\\{D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}:\mathrm{arity}\le K,\\;|S_\mu|\le r\bigr\\}.
$$

Known anchors: $G_2(K,r)=0$ for $r\le 3$; $G_2(2,4)=1/2$; $G_2(K,\infty)=1-1/K$. Exact intermediate surface mostly open.

<p align="center">
  <img src="assets/figures/stability_board.png" alt="Stability and G2(K,r)" width="720"/>
</p>

<p align="center">
  <img src="assets/figures/support_curve.png" alt="Support-constrained envelope sketch" width="860"/>
</p>

Full write-up: [`research/THEOREMS.md`](research/THEOREMS.md) · analytic proofs: [`research/m5/SEED_THEOREMS.md`](research/m5/SEED_THEOREMS.md).

---

## Habitat geometry (application families)

Filesystem-shaped query models—not replacements for $G_2(K)$.

**$k$-pair (which-then-bit).** Uniform random branch; payload bit differs under the two hypotheses; off-branch bits return $\mathtt{na}$. Adaptive with budget two achieves TV $=1$; best nonadaptive suite of budget two achieves $2/k$. Gap $1-2/k\to 1$. Myopic “strongest local check first” never opens with the branch query; ratio $k/2\to\infty$.

**All fixed budgets.** On the same family, for every $B\ge 2$:

$$
D_B^{\mathrm{ad}}=1,\qquad D_B^{\mathrm{na}}=\frac{\min(B,k)}{k},\qquad \mathrm{Gap}_B(k)\to 1\ (k\to\infty).
$$

A fixed-size checklist cannot uniformly bound adaptive risk across branching factors.

<p align="center">
  <img src="assets/figures/gap_all_B.png" alt="Gap for multiple budgets" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/habitat_forms.png" alt="Habitat closed forms" width="720"/>
</p>

**Parity payloads.** Local bit marginals matched; global parity differs per branch. Perfect adaptive separation costs $B^\star_{\mathrm{ad}}=1+m$; perfect nonadaptive separation costs $B^\star_{\mathrm{na}}=k\cdot m$. Ratio unbounded in $k$:

$$
\frac{B^\star_{\mathrm{na}}}{B^\star_{\mathrm{ad}}}=\frac{km}{m+1}\to\infty.
$$

<p align="center">
  <img src="assets/figures/anim_budget_race.gif" alt="Adaptive vs nonadaptive budget race" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/anim_parity_ratio_3d.gif" alt="3D parity budget ratio surface" width="720"/>
</p>

**Capacity zero.** Under adaptive inspection with $B\ge 2$ on the $k$-pair family, indistinguishability capacity for any $\varepsilon<1$ is **zero**. Large branching helps checklists; it does not help against which-then-bit.

<p align="center">
  <img src="assets/figures/anim_capacity_zero.gif" alt="Capacity zero under adaptive inspection" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/anim_greedy_blowup.gif" alt="Myopic greedy blowup" width="860"/>
</p>

<p align="center">
  <img src="assets/figures/greedy_ratio.png" alt="Myopic greedy unbounded ratio" width="860"/>
</p>

| Family | Role | Gap / separation |
|--------|------|------------------|
| Address construction (arity $K$) | **Extremal law** | $G_2(K)=1-1/K$ |
| $k$-pair | Habitat + greedy scar | $1-2/k$ at $B=2$ |
| Parity ($m$-bit) | Budget race | $B^\star_{\mathrm{ad}}=1+m$ vs $B^\star_{\mathrm{na}}=km$ |

---

## Machine certificates

```powershell
pip install -e .
cd research\m5\EXPERIMENTS
python test_m5_exact.py    # G_2(K)=1-1/K, butterfly, support
python test_m5.py          # k-pair closed forms + greedy
cd ..\..\ladder
python run_ladder.py
python run_ladder_high.py
cd ..\m4\EXPERIMENTS
python test_certificates.py
```

Expected: all green; sharp table $K=2..7$ gives $\mathrm{ad}=1$, $\mathrm{na}=1/K$; $k$-pair $k=2..12$ gives $\mathrm{na}=2/k$.

Figures:

```powershell
python assets/render_figures.py
python assets/render_animations.py
```

---

## Implementation scar (secondary)

Encrypted volumes solve confidentiality of **bytes**. They do not solve **narrative**. The engineering layer constructs habitat cover trees, measures them, and **refuses** when the cover is blown. Cipher capacity (L0) is borrowed. Cover construction and the refuse joint are owned here.

**Design basis (compressed).** Name the loads. Draw the load path (`forge → smell → refuse`). Size members for controlling cases. Detail connections (dual gate; severity monoid ≠ posterior). Leave T4 unstamped. As-built checks: `charm bench`, known-bad must fail.

**Static smell is nonadaptive.** Clean reports are necessary QC — not an adaptive demand certificate at comparable look length. That is the theorem speaking through the tool.

```text
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

### Score semantics (binding)

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
| Product is a monoid | Commutative severity aggregation, not $\mathbb{P}(\text{generated})$ |
| Dual gate | One bad finding alone scores 0.55 and still refuses |
| Clean report | Necessary for refuse automation—not a full adaptive T1 bound |

Doctrine: [`docs/T1_BUDGET.md`](docs/T1_BUDGET.md) · naturalness: [`docs/NATURAL.md`](docs/NATURAL.md) · master: [`docs/MASTER.md`](docs/MASTER.md)

---

## Load cases (threat model)

| Case | Adversary | Design stance |
|------|-----------|---------------|
| **T0** | Glancing human | Service — strong on implemented tells |
| **T1** | Curious technical peer, short session | Service — raise cost of casual tells; smell is nonadaptive; see T1_BUDGET |
| **T2** | Offline stolen disk | Foundation governs if L0 holds; cover may shift prioritization only |
| **T3** | Compelled password | Not stamped until CELLAR is detailed |
| **T4** | Laboratory process + time | **Unclaimed. No stamp. Ever.** |

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

Naturalness is **habitat-relative**. Opaque extensions for non-genuine formats. Specialist names require magic and membership. Famous public sample IDs forbidden as decoration. Published checksums must match bytes.

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

Forge refuses blown covers by default. `--i-know` is an informed override. `--write-seed` is off by default. Size ceilings require `--unsafe-size` when deliberately exceeded.

---

## Research ladder (M4–M18)

| Band | Content |
|------|---------|
| M4 | Finite adaptive gap certificates, score hygiene, witnesses |
| M5 | Flattening, root-arity, $G_2(K)=1-1/K$, butterfly uniqueness, $k$-pair |
| M6–M9 | All-$B$ envelopes, greedy failure, checklist incompleteness, capacity zero |
| M10–M13 | Closed forms vs DP, doctrine pack, parity budgets, unbounded separation |
| M14–M18 | Nesting, score–LR reversals, query complexity, randomized NA, mega-pack |

Reproduce: ladder runners + M4/M5 test suites. Static and animated figures are first-class artifacts of the certificates, not decoration.

**Open frontier.** Support-constrained curve $G_2(K,r)$; equality for $K>2$; sharp $G_B(K)$ for $B\ge 3$; guarded compilation; Lean formalization of the seed package; completed primary-source collision.

---

## Explicit non-goals

- Inventing or “improving” ciphers  
- Probability-of-generation marketing for `blown_score`  
- Operational guidance for concealing material from forensic inspection  
- Exhaustive file-type encyclopedias  
- T4 claims under any packaging  
- Literature-novelty press language for the sharp seed package  

---

## System sections (abbreviated)

```text
charm
├── forge      construction sequence + refuse joint
├── smell      as-built inspection + severity monoid + dual gate
├── props      habitat members (decoy trees)
├── caliper    size bands / opaque payload policy
├── ecology    specialist families + habitat membership
├── forgery    seeded identity fields
├── kernel     foundation L0 (VeraCrypt create)
├── bench      known-bad load tests
└── catalog    detail catalog (explain surface)
```

Process: [`docs/SKUNKWORKS.md`](docs/SKUNKWORKS.md) · security: [`SECURITY.md`](SECURITY.md) · field notes: [`docs/FIELD_GUIDE.md`](docs/FIELD_GUIDE.md)

---

## Colors

**Purdue black** `#000000` / `#0A0A0A` · **old gold** `#CFB991` · Boiler Up.

## Author · license · version

**David Lombardo** · MIT · **v0.3.8**  
[github.com/coldbricks/charm13](https://github.com/coldbricks/charm13)

Statements are finite, falsifiable, and deliberately cold.
