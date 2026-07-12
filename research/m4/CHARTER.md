# M4 CHARTER — Budgeted Habitat Indistinguishability

**Status:** P0 FORMULATION (no success claimed; no novelty claimed)  
**Baseline:** CHARM13 v0.3.3  
**Date:** 2026-07-12  
**Phase:** formulation only — no product code changes  

Binding: `docs/MASTER.md`, `docs/NATURAL.md`, `docs/SKUNKWORKS.md`, `SECURITY.md`, README, tests, M1/M2 history.  
Scientist constraint: proofs / counterexamples / experiments; detection-and-claims framing; no operational concealment-from-inspection guidance.

---

## 0. Audit of mathematical content implicit in v0.3.3

### 0.1 What exists as code (not as math)

| Object in prose | Object in code | Status |
|-----------------|----------------|--------|
| Habitat / naturalness | Template name + `HABITAT` specialist sets + decoy trees | Engineering ontology |
| Cover story | Seeded `CoverIdentity` + fixed tree shape per template | Deterministic given seed |
| Detection oracle | Fixed checklist `smell_report` | Non-adaptive, non-budgeted |
| `blown_score` | Severity noisy-OR product | Ordinal engineering score |
| Blown | `any(bad)` OR `score ≥ 0.6` | Operator policy (dual gate) |
| P_H | *absent* | No genuine-habitat measure |
| Q_H,θ,s | *partial* | Seed → identity fields; payload size s; structure fixed |
| Adaptive T1 | *absent* | Smell always runs full tree pass |
| D_B | *absent* | No transcript / budget model |
| Capacity C_H | *absent* | Size bands only (hard constraints) |

### 0.2 Randomness actually present in forge (Q as implemented)

Given fixed `(template, size_mb, mode ∈ {tree_only, placeholder, veracrypt})`:

1. **Seed** `seed ∈ {0,…,2^31−1}` (or system-random if omitted).  
2. **Identity fields** derived by seeded PRNG: sample/project ids, lab/site/pipeline/analyst strings, timestamps, vendor, short hashes used in basenames.  
3. **Payload bytes:** VeraCrypt ciphertext (L0 RNG outside CHARM), or sparse placeholder (zeros / sparse allocation — deterministic structure), or tree-only (no payload file body).  
4. **Checksums** of decoys/payload when template requests them (deterministic given bytes).  
5. **Tree topology and relative paths** are **not** random: fixed per template function in `props.py`.

**Consequence:** Q is *not* a rich generative model of habitats. It is a **seeded labeling of a fixed skeleton**, plus an opaque blob of size s. Any theorem about Q must state this explicitly or use **synthetic** richer Q for math.

### 0.3 What smell actually computes

Smell is a **deterministic map**  
`σ: Tree × (template?) → list[SmellFinding]`  
with codes such as: magic lies, GIAB tokens, size band, toy siblings, monolith, habitat_clash, checksum mismatch, zero_fill, tool_fingerprint, high_entropy, …

Dedupe: one finding per `(code, path_key)`, higher severity wins.

Observations used are **implicit and free**: recursive file walk, basenames, sizes, header bytes, optional MD5 verify, habitat membership. There is **no cost model** and **no early stopping**.

### 0.4 Implicit (unproved) assumptions in v0.3.3 doctrine

1. Local checks (magic, habitat family, sizes, checksums) ≈ T1 naturalness.  
2. Severity weights compose by independence-style product.  
3. Any single `bad` is decisive for operator refusal.  
4. Warn stacks can become decisive near threshold 0.6.  
5. Fixture separation (bad GIAB/cram vs clean opaque/adobe) calibrates the score.  
6. Naturalness is a property of a **single tree**, not of a **distribution**.

M4 treats (1)–(6) as research subjects, not axioms.

---

## 1. Interpretation of `blown_score` (can / cannot)

### Implementation (v0.3.3)

```text
WEIGHTS = {bad: 0.55, warn: 0.25, info: 0.05}
blown_score(F) = 1 − ∏_{f ∈ F} (1 − w_{sev(f)})
is_blown(F)    = (∃ f: sev(f)=bad)  ∨  (blown_score(F) ≥ 0.6)
```

### What the weights **are**

| Candidate reading | Valid? |
|-------------------|--------|
| Probabilities of independent “generation events” | **No** — no generative event model; findings are deterministic functions of the tree |
| Likelihood ratios | **No** — not log-odds; not calibrated to P vs Q |
| Softmax / posterior mass | **No** |
| Ordinal engineering severities with a commutative monoid | **Yes** |
| Union-bound style risk under independence fantasy | **Only if** one invents independent Bernoullis with success probs w_i **after** findings fire — circular |

**Verdict:** `w_i` are **severity-class engineering weights**, not probabilities. The product is the **noisy-OR algebraic form** used as a **severity aggregator**, not a calibrated probability of generation.

### What `blown_score` **can** mean

1. A **scalar monoid** on multisets of severities: associative, commutative, order-preserving in the sense that adding a finding never decreases the score.  
2. An **operator ranking** among warn/info stacks (e.g. three warns ≈ 0.578 < 0.6; four warns ≈ 0.684 ≥ 0.6).  
3. A **debug / report field** coexisting with the hard rule `any bad blows`.  
4. A **gate input** for forge refusal when combined with threshold and `--i-know`.

### What `blown_score` **cannot** mean (without new assumptions)

1. **P(at least one finding would fire under random inspection)** — findings are not random; the tree is fixed.  
2. **P(human says “generated”)** — no human model.  
3. **Likelihood ratio Λ = dQ/dP** or any Neyman–Pearson statistic for habitat discrimination.  
4. **Posterior P(generated | tree)** — no prior, no P_H.  
5. **Expected loss** under a stated decision theory.  
6. **Worst-case distinguishing advantage D_B** — no observer budget, no transcript law.  
7. A quantity that **automatically accounts for dependence**: one latent defect (fake `.cram` + GIAB name + habitat clash) can emit multiple correlated findings and **inflate** the product; two redundant path tokens can double-count before dedupe keys differ.

### Dual-gate fact (exact, elementary)

- One `bad` ⇒ score = 0.55 < 0.6, yet `is_blown = True` via the **logical** any-bad rule.  
- Therefore **score threshold alone does not implement any-bad**.  
- Any-bad is an **operator policy** (hard refusal), not a consequence of the product formula at τ = 0.6.  
- Warn-stack blow is the only path where the product gate is load-bearing.

### Dependence pathologies (for HUNTER; not claimed as novel theorems yet)

1. **Common-cause inflation:** one specialist lie → `format_magic` + possible `habitat_clash` + path tokens → multiple findings, score rises without independent evidence.  
2. **Redundant warns:** distinct codes for overlapping phenomena (e.g. size notes + caliper) can stack.  
3. **Missing joint witnesses:** two weak local facts that are only decisive **together** (global consistency) never form a finding; noisy-OR cannot invent that interaction.  
4. **Dedupe asymmetry:** dependence is partially mitigated by `(code, path_key)` dedupe, but not by latent-defect identity.

### Separation of concepts (binding vocabulary for M4)

| Symbol / phrase | Meaning |
|-----------------|--------|
| Finding fire set F(X) | Deterministic smell output on tree X |
| Score S(F) | Noisy-OR severity aggregate |
| Refuse policy R | `any bad ∨ S≥τ` (current) |
| Union probability | Needs a probability space on findings — **not present** |
| LR / posterior | Needs P,Q — **not present** in product |
| D_B(P,Q) | Budgeted adaptive TV on transcripts — **research object** |
| Engineering refusal | What CHARM ships today |

---

## 2. Formal objects (working definitions)

Domain is finite and fully explicit for theorem-search. Continuous “real filesystems” are out of scope for proofs until reduced to finite models.

### 2.1 Habitat tree

A **habitat instance** is a finite rooted tree  
`X = (V, E, r, α)`  
where:

- `V` — nodes (files or directories);  
- `E` — parent edges; unique root `r`;  
- `α: V → A` — attributes from a finite alphabet `A` (type, basename token, extension class, size bucket, magic class, checksum-link id, habitat-family tag, …).

Isomorphism: unless stated, trees are **labeled by path-from-root basenames** (filesystem identity), not unlabeled combinatorial trees.

### 2.2 Habitat distributions

For habitat name `H` (template):

- **P_H** — probability distribution on a finite set `𝒳_H` of habitat trees (reference / genuine / synthetic-genuine).  
- **Q_{H,θ,s}** — distribution on `𝒳_H` (or a larger set) induced by generator parameters `θ` and opaque payload size `s`.

**CHARM-implemented Q (special case):**  
`θ = (template, mode, password-policy, write_seed, …)`, randomness = seed (and L0 ciphertext if VeraCrypt). Topology fixed; only `α` on a subset of nodes is random.

**Math default for M4:** use **explicit rational** P, Q on small `𝒳`, not empirical disk samples, unless a later phase imports public corpora under a stated sampling model.

### 2.3 Queries

A **query** is `q` with:

- cost `c(q) ∈ ℚ>0`;  
- observation map `o_q: 𝒳 → Y_q` (finite codomain).

Query set `𝒬` may be **state-dependent**: some queries only legal after existence of a node is revealed (directory listing required before child header).

**Default T1 toy query classes (synthetic):**

| Query | Reveals | Typical cost |
|-------|---------|--------------|
| `list(v)` | children basenames of directory v | 1 |
| `stat(u)` | type, size bucket, mtime bucket | 1 |
| `head(u)` | magic class / first-k sketch | 1 |
| `rel_checksum(u,v)` | equality of declared vs bytes | 2 |
| `sib_sizes(v)` | multiset of child size buckets | 1 |
| `habitat_tag(u)` | specialist family vs claimed H | 1 |

No adversarial parsers, no polyglots, no anti-forensic ops.

### 2.4 Transcript, policy, budget

An **inspection policy** `π` is a (possibly randomized) rule that, given past transcript, selects next legal query or STOP, subject to total cost ≤ `B` (worst-case budget unless stated **expected** budget).

Transcript `T_π(X)` = sequence of (query, observation) pairs then decision `δ ∈ {genuine, generated}`.

Observer is assumed to **know** the mathematical objects `(P, Q, 𝒬, c, B)` in theory problems (Bayes setting), unless a claim explicitly uses composite or misspecified observers.

### 2.5 Budgeted distinguishing advantage

$$
D_B(P,Q)
  := \sup_{\pi:\\; \mathrm{cost}(\pi)\le B}
     \mathrm{TV}\bigl(\mathrm{Law}_P(T_\pi),\\; \mathrm{Law}_Q(T_\pi)\bigr)
$$

with total variation $\mathrm{TV}(\mu,\nu)=\tfrac12\sum |μ−ν|$.

**Notes (non-novelty):**

- This is **restricted statistical distance** under an adaptive experiment class; related to active/sequential hypothesis testing, controlled sensing, Le Cam deficiency for restricted experiment classes, Blackwell comparison.  
- MIRROR owns collision search; **do not rename** if exact match found — cite and specialize.  
- Decision error form: for equal priors, max Bayes accuracy = $\tfrac12 + \tfrac12 D_B$ when the policy’s terminal decision is optimal for the transcript law (standard).

Nonadaptive variant $D_B^{\mathrm{na}}$: sup over fixed query sets of total cost ≤ B (order may still matter if queries are destructive — default: non-destructive, order irrelevant for nonadaptive).

### 2.6 Habitat camouflage capacity (secondary object)

$$
C_H(B,\varepsilon,K)
  := \sup\bigl\\{ s : \exists\\,θ \text{ with }
        D_B(P_H, Q_{H,θ,s}) \le \varepsilon,
        \mathbb{E}[\mathrm{overhead}(θ,s)] \le K,
        \text{hard constraints}(H)\bigr\\}
$$

Hard constraints include: specialist extension policy, size-band ceilings unless unsafe, no GIAB tokens, checksum consistency when published.

Treat $C_H$ as **analysis object**. Honest reduction to distribution matching / rate-distortion / stego capacity when applicable is success, not failure.

### 2.7 Smell as nonadaptive policy (bridge)

CHARM smell ≈ a **single fixed nonadaptive policy** with large effective B (full walk) producing transcript = finding multiset, then decision via refuse policy R.

Therefore:

- Fixture “BLOWN” ≠ proved $D_B > 0$ for all adaptive π;  
- Fixture “clean” ≠ proved $D_B \le ε$.

---

## 3. Three candidate research claims

Status for all three: **CANDIDATE** — not proved, not novel until MIRROR/HUNTER finish.

### Claim A — Adaptive gap for path-prefix filesystem queries

**Form:** Separation theorem / minimal counterexample (target status: MINIMAL COUNTEREXAMPLE ESTABLISHED or PROVED).

**Statement (candidate):**  
There exist explicit finite distributions P, Q on rooted attributed trees with |V| ≤ 6, attribute alphabet |A| ≤ 4, and unit-cost query family  
`𝒬₀ = {list(v), stat(u), head(u)}`  
such that for budget B = 2:

1. $D_2^{\mathrm{na}}(P,Q) \le 1/4$,  
2. $D_2(P,Q) = 1/2$,  

and no instance with |V| ≤ 3 achieves a strict adaptive gap under `𝒬₀` with unit costs and rational masses with denominator ≤ 12.

**Interpretation:** Directory-first adaptive inspection strictly beats the best nonadaptive pair of queries on a filesystem-shaped query model.

**Essential assumptions:** Observer knows P,Q; queries non-destructive; budget worst-case; policies may be deterministic (randomization allowed if needed — must be stated in final theorem).

### Claim B — Severity-only noisy-OR is not Bayes-monotone under CHARM finding dependence

**Form:** Impossibility / non-calibration theorem (target: HARDNESS OR IMPOSSIBILITY RESULT PROVED, or MINIMAL COUNTEREXAMPLE).

**Statement (candidate):**  
Let findings be produced by a **latent defect cover model**: each tree has a set of defects D(X); each defect d activates a nonempty set Φ(d) of smell codes (monotone). Severity weights depend only on `sev(code)`. Let S be the product score on the activated finding multiset after CHARM-style dedupe.

Then there exist finite (P, Q) and trees X₀, X₁ in the support such that:

1. S(σ(X₀)) < S(σ(X₁)), yet the optimal single-observation likelihood ratio for distinguishing P vs Q ranks X₀ as **more** Q-like than X₁; **or**  
2. S(σ(X₀)) = S(σ(X₁)) but the Bayes-optimal decisions differ,

and both (1) and (2) occur already for |Φ(d)| ≤ 3, ≤ 2 defects, and the actual CHARM severity map {0.55, 0.25, 0.05}.

**Interpretation:** The shipped score cannot be interpreted as a monotone transform of distinguishing evidence once CHARM’s correlated findings are admitted. Complements the dual-gate fact (any-bad ≠ product).

**Essential assumptions:** Explicit latent-defect activation table; P,Q known; comparison is Bayes LR on the full tree (unrestricted observer) **or** on the smell transcript — **must pick one in P2 and stick to it**.

### Claim C — Local smell predicates do not control budgeted global distinguishability

**Form:** Local-to-global separation (target: MINIMAL COUNTEREXAMPLE ESTABLISHED + optional composition theorem under extra assumptions).

**Statement (candidate):**  
For every finite family of predicates {φⱼ} each depending on at most ℓ nodes/attributes (a model of smell rule supports), there exist distributions P, Q on trees with O(ℓ) nodes such that:

1. Law_P(φⱼ(X)) = Law_Q(φⱼ(X)) for all j (identical local pass rates),  
2. yet $D_1(P,Q) ≥ 1/2$ via a single cost-1 **global relation query** (e.g. parity of a path attribute, or checksum-of-declared-companions consistency not in {φⱼ}).

Moreover, under the extra assumption that P and Q are **tree-Markov** with known factorization and all maximal-clique marginals matched, $D_B$ can be small — **state the positive companion carefully** so the negative result is sharp, not vague.

**Interpretation:** Passing every implemented local smell does not imply small D_B; global ecological invariants are first-class.

---

## 4. Closest fields and search terms (per claim)

### Claim A
- Active / sequential binary hypothesis testing with query costs  
- Controlled sensing; finite-horizon POMDP hypothesis testing  
- Adaptive vs nonadaptive experimental design; value of information  
- Decision-tree testing; feature acquisition for classification  
- Property testing (adaptive) on trees/graphs  
- Le Cam deficiency; Blackwell experiments (restricted)  
- “distinguishing two distributions with limited adaptive measurements”

### Claim B
- Noisy-OR models; belief networks; explaining away  
- Probability calibration; proper scoring rules  
- Dependent evidence combination; Dempster–Shafer (collision risk — do not adopt casually)  
- Sufficient statistics; Blackwell garbling (score as garbling of finding vector)  
- Multiple testing dependence; one-factor latent variable models

### Claim C
- Graphical models; marginal polytopes; inconsistency of marginals  
- Junction trees / treewidth; Gibbs / MRF local specs  
- CSP / database join consistency; parity and XOR global constraints  
- Local-to-global principles; Dobrushin uniqueness (positive side)  
- Pseudodistributions; sheaf contextuality (only if forced)  
- “locally consistent globally impossible” finite counterexamples

### Capacity C_H (background, not a claim yet)
- Steganographic capacity; distribution matching; channel resolvability  
- Rate-distortion with side constraints; privacy–utility frontiers  
- Minimum-cost distribution projection / repair

---

## 5. Smallest instances HUNTER should enumerate first

### Shared toy grammar
- Nodes: 2..8; binary or 3-ary attributes; rational masses denominator ≤ 12.  
- Budgets B ∈ {0,1,2,3}; unit costs first; then cost-2 decisive queries.  
- Exact rational TV; enumerate deterministic policies; LP if randomization needed.

### Against Claim A
1. Star: root + 2 children; attrs on children differ under P vs Q only in which child is “hot.”  
2. Path of length 3: intermediate list reveals which leaf to head.  
3. Two disjoint subtrees; first list chooses branch.  
4. Point masses (should give D=1 when supports differ and a cheap witness exists).  
5. Identical P=Q (D_B=0).  
6. Nonadaptive optimum that already achieves adaptive value (gap 0 — kills overclaim).  
7. Randomization: cases where mixed policies beat pure (if any at this size).

### Against Claim B
1. Single defect activating two `warn` findings vs two independent defects each one `warn`.  
2. One `bad` (score 0.55, blown) vs three `warn` (score ~0.578, not blown) — LR order vs refuse policy.  
3. Duplicate codes different path_keys vs same path_key dedupe.  
4. Habitat_clash + format_magic common cause.  
5. Equal scores, unequal LR.  
6. Opposite score order vs LR order (kill Bayes-monotone reading).

### Against Claim C
1. Two nodes, local magic OK, global “companion size ratio” differs.  
2. Checksum file matches each named file locally under both P and Q, but **which** files are listed in the checksum set differs by a parity rule.  
3. Habitat family tags all legal locally; co-occurrence of two legal families forbidden under P only.  
4. All φⱼ identical; D_B>0 via relation query not in smell set.  
5. Tree-Markov matched cliques → check whether D_B collapses (companion positive claim).

---

## 6. MIRROR preliminary novelty objections

### Claim A
- **Objection:** Adaptive vs nonadaptive gaps in hypothesis testing and feature acquisition are classical; a 6-node filesystem costume may be KNOWN RESULT, NEW APPLICATION only.  
- **What would save it:** (i) sharp minimal n for **path-prefix / list-then-head** query geometry; (ii) tight gap value with complete enumeration; (iii) complexity corollary for computing D_B under `𝒬₀` that is not a generic POMDP restatement; (iv) explicit export of optimal transcript → CHARM smell rule.

### Claim B
- **Objection:** “Correlated evidence breaks naive independence aggregation” is textbook; noisy-OR under dependence is known not to be a probability of union without independence. Dual-gate fact is elementary.  
- **What would save it:** A **tight characterization** for the CHARM finding algebra (which score orderings are realizable as LR orderings; which refuse policies are NP tests for some (P,Q); minimal sufficient statistic for defect covers) — not a sermon about independence.

### Claim C
- **Objection:** Local vs global consistency is one of the oldest themes in graphical models and CSP; parity counterexamples are standard.  
- **What would save it:** Habitat-specific **witness extraction**: minimal global relation not implied by a stated smell support family, with proved D_1 gap and a repair cost interpretation; or a sharp positive theorem: under treewidth ≤ k and clique-marginal matching, D_B ≤ f(…).

### Definition D_B itself
- **Presumption of novelty: forbidden.** Treat as restricted TV under adaptive experiments until MIRROR names the closest match.

---

## 7. Ranking

Scores: 1 (low) – 5 (high). Subjective P0 prior only.

| Claim | Scientific value | Chance of truth | Chance of novelty | Implementability (exact toys) | Relevance to CHARM13 | Notes |
|-------|------------------|-----------------|-------------------|-------------------------------|----------------------|-------|
| **A** Adaptive gap | 5 | 4 | 3 | 5 | 4 | Core §5 problem; high product map to inspection order |
| **B** Score non-monotone | 3 | 5 | 2 | 5 | 5 | Likely true; novelty bar high; still kills false score theology |
| **C** Local≠global | 5 | 5 | 2–3 | 4 | 5 | Doctrine-critical; collision risk with classical local-global |

**Composite priority (P0):** A ≥ C > B for “main invention” track; B remains mandatory **side lemma** for honesty of `blown_score` regardless of primary.

---

## 8. Provisional primary claim

**Primary: Claim A** — *Adaptive gap for path-prefix filesystem queries*  
(with Claim B as required score-semantics lemma; Claim C as secondary theorem-search track).

**Rationale:**

1. Aligns with M4 §5 primary problem (budgeted adaptive inspection).  
2. Falsifiable on tiny instances before any prose inflation.  
3. Negative or tight-gap outcomes both publishable under mission rules.  
4. Success condition can be MINIMAL COUNTEREXAMPLE ESTABLISHED without renaming TV.  
5. If MIRROR collapses A to known adaptive testing, fall back to: (A′) complexity of exact D_B under `𝒬₀`, or (C) habitat-shaped local-to-global witness extraction.

**Not primary:** tuning weights, new templates, capacity marketing names, cipher work.

---

## 9. P0 artifact checklist and next gates

### This file
`research/m4/CHARTER.md` ← **you are here**

### Immediate next artifacts (P0→P1, still no product edits)
| Path | Purpose |
|------|---------|
| `research/m4/DEFINITIONS.md` | Freeze symbols from §2 with quantifiers |
| `research/m4/CLAIM_LEDGER.json` | A,B,C entries + statuses |
| `research/m4/CONJECTURES.md` | Exact formal statements for hunt |
| `research/m4/PRIOR_ART.md` | MIRROR collision notes (start empty structured) |
| `research/m4/COUNTEREXAMPLES/` | Machine-readable kills |
| `research/m4/RESULT.md` | Empty stub until terminal status |

### Process gate
- **P1 KILL:** HUNTER enumerates §5 instances against A,B,C; MIRROR starts collision search using §4 terms.  
- **No implementation** of research algorithms in `src/charm/` until P3 closes.  
- Optional later: `research/m4/EXPERIMENTS/` exact rational policy enumerator — research-only module.

### Success (mission-level, not claimed now)
One central statement in `RESULT.md` with an allowed terminal status from the directive. Code green (18 tests / bench 4/4) preserved throughout.

---

## 10. Explicit non-claims (P0)

- We do **not** claim D_B is a new distance.  
- We do **not** claim habitat camouflage capacity is a new capacity theorem.  
- We do **not** claim `blown_score` is a probability.  
- We do **not** claim T3/T4.  
- We do **not** claim success of M4.

---

## 11. One-paragraph state

M4 P0 audits v0.3.3 as an engineering refuse loop (seeded fixed-skeleton forge + deterministic full-walk smell + severity noisy-OR + any-bad policy) without P_H, adaptive budgets, or calibrated score semantics. Formal objects P, Q, queries, transcripts, and D_B are defined for finite synthetic habitats. Three candidates are posed: adaptive path-prefix gap (primary), score Bayes non-monotonicity under defect coupling (honesty lemma), and local-smell vs global D_B separation (secondary). HUNTER/MIRROR kill phase is next; no novelty and no mission success are asserted.
