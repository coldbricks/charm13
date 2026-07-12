# M4 DEFINITIONS — Frozen symbols

**Status:** P0 freeze for theorem-search  
**Baseline:** CHARM13 v0.3.3  
**Supersedes informal wording in:** CHARTER §2 when conflict arises (this file wins for math)

All finite. Prefer rational probabilities. Continuous “real disks” are out of scope until reduced to finite models.

---

## 0. Global conventions

| Convention | Choice (default) |
|------------|------------------|
| Trees | Rooted, **path-labeled** (filesystem identity) |
| Observer knowledge | Knows mathematical `(P, Q, 𝒬, c, B)` unless a claim says otherwise |
| Policies | Deterministic allowed; randomized allowed when stated |
| Budget | **Worst-case** total query cost ≤ B unless “expected budget” stated |
| Query side effects | **Non-destructive** (observations do not alter X) |
| Directory enumeration | A query (`list(v)`), not free ambient knowledge, in math models |
| Divergence | Total variation unless another is named and related by a cited inequality |
| Prior for Bayes accuracy | Equal priors on {P, Q} when converting TV ↔ accuracy |

Forbidden silent moves: TV ↔ KL ↔ Chernoff without a stated bridge.

---

## 1. Attribute alphabet and trees

### 1.1 Attribute alphabet

A finite set `A`. Typical coordinates (product alphabet):

- `kind ∈ {dir, file}`
- `base` — basename token from a finite name set
- `ext` — extension class (opaque / specialist-family / other)
- `size` — size bucket from a finite partition of ℕ
- `magic` — header class (unknown / match-ext / mismatch / opaque-noise)
- `mtime` — coarse time bucket
- `ck_link` — checksum-relationship id or ⊥
- `fam` — specialist family tag or ⊥
- other finite marks as needed per experiment

Not all coordinates need appear in every toy instance.

### 1.2 Habitat tree

A **habitat tree** is a tuple

$$
X = (V, E, r, \alpha)
$$

where:

- `(V, E, r)` is a finite rooted tree (unique path from `r` to each node);
- `\alpha: V → A` assigns attributes;
- for filesystem interpretation, the map from nodes to path strings via edge basenames is injective.

Let `𝒳` be a finite set of habitat trees under consideration.

### 1.3 Habitat name

`H` is a discrete habitat label (e.g. `adobe_cache`, `wgs_lab`). It constrains:

- which `ext`/`fam` pairs are **at home** (ecology);
- which hard forge constraints apply (size bands, specialist policy).

---

## 2. Distributions P and Q

### 2.1 Reference law

$$
P_H \in \Delta(\mathcal{X}_H)
$$

Probability distribution on a finite set `𝒳_H` of habitat trees called the **reference** (genuine / synthetic-genuine) support for habitat `H`.

### 2.2 Generator law

$$
Q_{H,\theta,s} \in \Delta(\mathcal{X})
$$

Distribution induced by generator parameters `θ` and opaque payload size parameter `s` (size bucket or integer MB in product; discrete bucket in math).

### 2.3 CHARM-implemented generator (special case)

For CHARM13 v0.3.3 forge with fixed `(H, size_mb, mode)`:

| Component | Random? |
|-----------|---------|
| Tree topology / relative path skeleton | **No** — fixed by template |
| Identity fields, basename hashes, times | **Yes** — function of seed |
| Payload length | Parameter `s` (chosen, not random) |
| Payload content | VC ciphertext RNG (L0) / sparse placeholder / absent |
| Checksum file contents | Deterministic given file bytes |

Write this law as `Q^CHARM_{H,θ,s}` when a claim depends on implementation realism.

### 2.4 Synthetic laws (default for proofs)

Unless a claim says `Q^CHARM`, `P` and `Q` are **explicit rational** distributions written in experiment files. No claim may treat a tiny empirical sample as a population.

---

## 3. Queries, costs, legality

### 3.1 Query

A **query** is an object `q` equipped with:

- cost `c(q) ∈ ℚ_{>0}`;
- finite observation alphabet `Y_q`;
- observation map `o_q: 𝒳 → Y_q` (total function on the current model’s tree set);
- optional **guard** `g_q` on transcripts (query legal only if guard holds).

### 3.2 Default toy query family `𝒬₀` (path-prefix)

| Symbol | Meaning | Default cost |
|--------|---------|--------------|
| `list(v)` | children basenames of directory `v` | 1 |
| `stat(u)` | kind, size bucket, mtime bucket of node `u` | 1 |
| `head(u)` | magic class of file `u` | 1 |

Extended families used in claims:

| Symbol | Meaning | Default cost |
|--------|---------|--------------|
| `rel_ck(u)` | checksum consistency for declared relation involving `u` | 2 |
| `sib_sizes(v)` | multiset of child size buckets | 1 |
| `global_rel(ρ)` | evaluation of a named global relation `ρ` | 1 |

### 3.3 Legality

After transcript `τ`, query `q` is **legal** if:

1. total cost so far + `c(q) ≤ B` after selection rules of the policy class; and  
2. guard `g_q(τ)` holds (e.g. `u` was revealed by a prior `list` ancestor walk from root).

**Root is known** at cost 0 (observer is handed the habitat root path). Existence of non-root nodes is not free: they appear via `list`.

---

## 4. Policies and transcripts

### 4.1 Transcript

A **transcript** is a finite sequence

$$
\tau = \bigl((q_1,y_1),\ldots,(q_m,y_m)\bigr)
$$

with each `y_i = o_{q_i}(X)` and each `q_i` legal given the prefix.

### 4.2 Inspection policy

An **inspection policy** `π` is a (possibly randomized) rule that maps each partial transcript to either:

- a legal next query, or  
- `STOP`,

subject to total cost `∑ c(q_i) ≤ B` almost surely (worst-case budget).

After STOP, a **decision rule** `δ` maps the final transcript to `{genuine, generated}`.

When we write `T_π(X)`, we mean the full transcript including the decision bit if the claim’s TV is taken over decided transcripts; otherwise over observation transcripts only. **Default for `D_B`:** observation transcript only; optimal decision is applied when converting to Bayes risk (standard).

### 4.3 Nonadaptive policies

A policy is **nonadaptive** if the set (or multiset) of queries is fixed before seeing any `y`, up to legality that can be resolved without observations (e.g. only querying root). For `𝒬₀`, nonadaptive policies with unknown children are restricted: without adaptive `list`, deeper nodes may be unreachable.

Define

$$
D_B^{\mathrm{na}}(P,Q)
  := \sup_{\pi\ \mathrm{nonadaptive},\ \mathrm{cost}\le B}
     \mathrm{TV}\bigl(\mathrm{Law}_P(T_\pi),\mathrm{Law}_Q(T_\pi)\bigr).
$$

---

## 5. Distances and advantages

### 5.1 Total variation

For distributions `μ, ν` on a finite set `Z`:

$$
\mathrm{TV}(\mu,\nu) := \frac12 \sum_{z\in Z} \bigl|\mu(z)-\nu(z)\bigr|
\in [0,1].
$$

### 5.2 Budgeted adaptive distinguishing advantage

$$
D_B(P,Q)
  := \sup_{\pi:\ \mathrm{cost}(\pi)\le B}
     \mathrm{TV}\bigl(\mathrm{Law}_P(T_\pi),\ \mathrm{Law}_Q(T_\pi)\bigr).
$$

**Elementary properties (baseline; not main invention):**

- `0 ≤ D_B ≤ 1`
- `B ↦ D_B` nondecreasing
- `D_0 = 0` if no free observations
- `D_B^{na} ≤ D_B`
- Unrestricted full observation of `X` yields `TV(P,Q)` as an upper bound on all `D_B`

### 5.3 Bayes accuracy (equal priors)

If the terminal decision is optimal for the transcript law under equal priors on hypotheses `{P,Q}`:

$$
\mathrm{Acc}_B = \tfrac12 + \tfrac12 D_B.
$$

Do not mix this with Neyman–Pearson at asymmetric errors without restating.

### 5.4 Likelihood ratio on a tree

For fully observed `X` with `P(X)+Q(X)>0`:

$$
\Lambda(X) := \frac{Q(X)}{P(X)}
$$

(with the usual `+∞` convention when `P(X)=0 < Q(X)`).

---

## 6. Smell calculus objects (engineering + math bridge)

### 6.1 Finding

A **finding** is a tuple `(sev, code, detail, path_key)` with  
`sev ∈ {info, warn, bad}`.

### 6.2 Smell map

$$
\sigma: \mathcal{X} \times (\text{template option}) \to \mathrm{List}[\text{Finding}]
$$

as implemented by `charm.smell.smell_report`, after dedupe.

### 6.3 Severity weights and score

$$
w(\mathrm{bad})=11/20,\quad w(\mathrm{warn})=1/4,\quad w(\mathrm{info})=1/20
$$

(using v0.3.3 decimals 0.55, 0.25, 0.05).

$$
S(F) := 1 - \prod_{f\in F}\bigl(1-w(\mathrm{sev}(f))\bigr).
$$

### 6.4 Refuse policy (v0.3.3)

$$
R(F) := \mathbf{1}\bigl[\exists f\in F:\ \mathrm{sev}(f)=\mathrm{bad}\bigr]
       \ \vee\ 
       \mathbf{1}\bigl[S(F) \ge 3/5\bigr].
$$

Threshold `3/5 = 0.6`.

### 6.5 Latent defect cover model (for Claim B)

A finite set `𝔇` of defect labels. Each tree has `D(X) ⊆ 𝔇`.  
Each defect `d` activates a set `Φ(d)` of smell codes.  
Activated code multiset = image under monotone cover, then CHARM dedupe.

This model is a **research idealization** of correlated findings; it is not claimed to equal production `σ` until a explicit table maps defects → codes.

---

## 7. Local predicates and global relations (Claim C)

### 7.1 Local predicate

A Boolean map `φ: 𝒳 → {0,1}` has **locality ℓ** if there exists a set of at most ℓ node-attribute coordinates determining `φ` (precise support specified per experiment).

### 7.2 Global relation query

A query `global_rel(ρ)` evaluates a predicate `ρ` that is not ℓ-local for the ℓ under study (e.g. parity of a path, consistency of a full checksum manifest vs file set).

### 7.3 Local matching

Family `{φ_j}` is **matched** under `(P,Q)` if for all `j`:

$$
\mathrm{Law}_P(\phi_j(X)) = \mathrm{Law}_Q(\phi_j(X)).
$$

---

## 8. Capacity (secondary)

$$
C_H(B,\varepsilon,K)
  := \sup\Bigl\{
       s :\ \exists\,\theta\ 
       D_B(P_H, Q_{H,\theta,s}) \le \varepsilon,\ 
       \mathbb{E}[\mathrm{overhead}(\theta,s)] \le K,\ 
       \mathrm{Hard}(H,\theta,s)
     \Bigr\}.
$$

`Hard` includes ecology constraints, specialist policy, size-band ceilings unless unsafe flags, no GIAB tokens, checksum consistency when checksums are published.

`overhead` is a declared construction cost (bytes written, decoy count, time) — fixed per experiment.

**Novelty stance:** name not a claim of originality; reductions to known capacities are documented in PRIOR_ART / RESULT.

---

## 9. Repair and witnesses (tertiary; §7 of directive)

### 9.1 Distinguishing witness

A finite observation sequence (or decision tree of queries) that yields transcript TV contribution materially favoring Q under a stated `(P,Q,B)`.

### 9.2 Repair action

A permitted map `r: 𝒳 → 𝒳` with cost `κ(r)`, altering attributes/nodes within a declared repair class (add companion, rename ext class, fix checksum text, change size bucket, …).  
Out of scope: anti-forensic deletion, parser exploits, false trusted-format claims beyond existing smell-level honesty.

### 9.3 Repair objective (conjecture target, not asserted)

$$
\min\ \mathbb{E}_{X\sim Q}[\kappa(r(X))]\quad
\text{s.t.}\quad D_B(P, Q\circ r^{-1}) \le \varepsilon.
$$

Precise measure-pushforward notation fixed when a claim enters the ledger.

---

## 10. Complexity parameters (for algorithms / hardness)

| Symbol | Meaning |
|--------|---------|
| `n` | max \|V\| |
| `m` | \|Supp(P) ∪ Supp(Q)\| |
| `r` | max \|Y_q\| |
| `B` | budget |
| `\|𝒬\|` | number of abstract query templates (before grounding to nodes) |
| `d` | depth of tree |
| `b` | max branching factor |

---

## 11. Claim status labels (ledger)

Use exactly:

`KNOWN RESULT` · `KNOWN RESULT, NEW APPLICATION` · `ENGINEERING ADAPTATION` ·  
`CANDIDATE NOVEL DEFINITION` · `CANDIDATE NOVEL THEOREM` · `CANDIDATE NOVEL ALGORITHM` ·  
`CANDIDATE NOVEL COUNTEREXAMPLE` · `DISPROVED` · `PRIOR-ART COLLISION` ·  
`PROVED, NOVELTY UNRESOLVED` · `PROVED, CLOSEST PRIOR ART IDENTIFIED` ·  
`FORMALLY VERIFIED` · `WITHDRAWN`

Terminal RESULT.md statuses (mission success labels):

`PROVED AND FORMALLY CHECKED` · `PROVED, FORMALIZATION PARTIAL WITH AN EXPLICIT GAP` ·  
`NEW ALGORITHM WITH PROVED GUARANTEE` · `HARDNESS OR IMPOSSIBILITY RESULT PROVED` ·  
`MINIMAL COUNTEREXAMPLE ESTABLISHED` · `PRIOR-ART COLLISION ESTABLISHED, ORIGINAL CLAIM WITHDRAWN`

---

## 12. Scope and ethics constraints (binding)

- T0–T2 analysis only for product relevance; T3 not claimed; T4 never.  
- No optimization against named forensic/EDR/LE tooling.  
- No parser exploits, polyglots, malicious structures, stego loaders, anti-forensic deletion, evidence tampering.  
- Synthetic fixtures and public benign data only; no private user files.  
- Research framing: detection, oracles, claims — not concealment-from-inspection playbooks.

---

## 13. Notation quick reference

| Symbol | Meaning |
|--------|---------|
| `X` | habitat tree |
| `H` | habitat label |
| `P_H`, `Q_{H,θ,s}` | reference / generator laws |
| `𝒬`, `q`, `c(q)`, `o_q` | query system |
| `π`, `T_π`, `B` | policy, transcript, budget |
| `D_B`, `D_B^{na}` | adaptive / nonadaptive advantages |
| `σ`, `S`, `R` | smell map, score, refuse |
| `φ`, `ρ` | local predicate, global relation |
| `C_H` | camouflage capacity (secondary) |
