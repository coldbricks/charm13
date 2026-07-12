# M4 RESULT — Terminal research statement

**Mission:** Budgeted Habitat Indistinguishability  
**Baseline:** CHARM13 v0.3.3  
**Phase:** P1–P4 partial (finite-model certificates; no Lean formalization yet)  
**Date:** 2026-07-12  

---

## Terminal status (central deliverable)

### Primary labels

| Layer | Status |
|-------|--------|
| Flagship gap certificate | **`PROVED`** (hand + exact-rational machine cert; external scientist re-ran 8/8 tests) |
| Size minimality (unguarded depth-2) | **`PROVED`** — Lemma 3 in `PROOFS/A_adaptive_gap.md` (upgraded from search after scientist review) |
| Mission packaging label | **`MINIMAL COUNTEREXAMPLE ESTABLISHED`** now justified by Lemma 3, not by enumeration count |
| Novelty of broad phenomenon | **`KNOWN RESULT, NEW APPLICATION`** |
| Formalization | **`PROVED, FORMALIZATION PARTIAL WITH AN EXPLICIT GAP`** (no Lean yet) |

### Central statement

> For an explicit 4-world instance with unit-cost **globally available** queries `{gate, left, right}`,  
> **`D₂(P,Q) = 1`** and **`D₂^{na}(P,Q) = ½`**, hence a **strict adaptive gap of ½**.  
> Under the same unguarded deterministic unit-cost depth-2 model, **`D₂ = D₂^{na}` whenever the support has size ≤ 3`**, so the construction is **size-minimal**.  
> Proofs: `PROOFS/A_adaptive_gap.md`. Certificate: `COUNTEREXAMPLES/wit-A-asym-branch-B2.json`, `EXPERIMENTS/test_certificates.py`.  
> External review: `SCIENTIST_REVIEW.md`.

### Companion results (same mission)

| Id | Label | Statement (short) |
|----|-------|-------------------|
| **M4-B** | hygiene / demolition | Severity product `S` is not Bayes-monotone; kills “score = probability generated” |
| **M4-B3** | elementary lemma | one `bad` ⇒ S=11/20&lt;3/5 but R=1 |
| **M4-C** | classical warning label | Matched single-bit laws; XOR gives D₁=1 — local smells ≠ global ecology |
| **M4-DEF-DB** | `KNOWN RESULT` (definition) | `D_B` not claimed new |
| **FS path-prefix** | conditional application | Gap under list-before-head; **vanishes** path-free — load-bearing assumption documented |

### Honest hierarchy (external scientist — adopted)

1. Adaptive certificate is **real**.  
2. Minimality is a **clean theorem** (Lemma 3) in the unguarded model.  
3. Filesystem interpretation is **conditional** on access legality.  
4. Broad adaptive-vs-nonadaptive phenomenon is **known**.  
5. Score and parity are **valid demolition charges**, not discoveries.  
6. Lean formalization **absent**; literature review **incomplete** (entry points only).  
7. Press must **not** say “proves when” — only “exhibits a minimal finite case.”

### Novelty posture (binding honesty)

| Result | Novelty claim |
|--------|----------------|
| Existence of some adaptive gap | **Not new** (fixed-horizon active HT / costly feature acquisition) |
| Exact 4-world cert + proved n≤3 lower bound | **Pedagogical minimum + application packaging** — not a new adaptive-testing theorem |
| Path-prefix specialization | Application; assumption-honest |
| Score non-calibration | Product-specific hygiene |
| Parity local-global | Classical |

**Phrase “we invented D_B” is still forbidden.**  
**`PRESS_NOTE.md` is EMBARGOED** until human clears honest headlines.

### Formalization

**`PROVED, FORMALIZATION PARTIAL WITH AN EXPLICIT GAP`:**

- Human proof: Theorem A + Lemma 3.  
- Machine: 8/8 certificate tests (also run by external scientist).  
- **Gap:** no Lean/Coq/Isabelle formalization yet.

---

## What was believed before M4

1. `blown_score` could be read as union-style risk / soft probability.  
2. Local smell checks ≈ T1 naturalness.  
3. Naturalness is a property of a single tree, not (P,Q).  
4. Adaptive vs nonadaptive T1 structure was unformalized.  
5. Fixed-skeleton forge was casually treated as a rich habitat law.

---

## What is proved or disproved

### Proved (finite models)

1. **Strict adaptive gap** on the gate/left/right instance: D₂=1, D₂^{na}=½.  
2. **Size minimality:** no adaptive gap for support size ≤3 under unguarded deterministic unit-cost depth-2 (Lemma 3).  
3. **FS path-prefix gap** under list-requires-before-head: same constants; **vanishes** under path-free nonadaptive.  
4. **Score order reversal** vs Λ with CHARM weights (hygiene).  
5. **Equal score, unequal Λ** (S not sufficient for Bayes).  
6. **Dual gate** arithmetic.  
7. **Parity local-global** separation at budget 1 (classical).

### Disproved / rejected interpretations

1. “`blown_score` is P(generated)” without an extra generative model — **rejected**.  
2. “`is_blown` ⇔ score≥0.6” — **false** (any-bad).  
3. “Local predicate match ⇒ small D_B” without extra assumptions — **false**.  
4. Literal CHARTER A.1 constants (D₂^{na}≤¼ and D₂=½ simultaneously on one instance) — **not witnessed**; qualitative gap claim **held** with stronger adaptive TV.

### Not proved

- Full complexity classification of computing D_B.  
- Optimal greedy policy theorems.  
- Habitat camouflage capacity theorems.  
- Repair duality.  
- That n≤3 never admits any adaptive gap over all query models.  
- Lean formalization.

---

## Closest known results

See `PRIOR_ART.md`. Field-level closest:

- Fixed-horizon active hypothesis testing (entry: arXiv:1911.06912)  
- Costly feature acquisition / adaptive experiment selection  
- Classical parity / local consistency vs global joint  
- Noisy-OR under dependence (textbook)

**Full paper-by-paper collision table still incomplete.** Broad phenomenon is known; do not claim a new adaptive-testing theorem.

---

## What is genuinely different (residual)

1. In-repo **exact** four-world certificate + **proved** n≤3 size lower bound (unguarded depth-2).  
2. Path-prefix legality specialization with explicit path-free **stress kill**.  
3. Kill of **CHARM v0.3.3 score theology** with shipped weights (hygiene).  
4. Process: demote novelty, embargo press overclaim, invite external kill.

Not different: abstract existence of adaptive gaps or XOR counterexamples.

---

## Essential assumptions

- Finite known P, Q  
- Unit-cost deterministic queries  
- Worst-case budget  
- For FS claim: `head` requires prior `list`  
- For B: O_full likelihood ratios; findings as severity multisets  
- No private data; synthetic worlds only  

---

## Smallest reproducible examples

| Claim | Path |
|-------|------|
| A | `COUNTEREXAMPLES/wit-A-asym-branch-B2.json` |
| A-FS | `COUNTEREXAMPLES/wit-A-list-then-head-B2.json` |
| B | `COUNTEREXAMPLES/wit-B-score-lr-reversal.json` |
| C | `COUNTEREXAMPLES/wit-C-parity-local-global.json` |

Reproduce:

```powershell
cd C:\Users\coldb\charm13\research\m4\EXPERIMENTS
python hunt.py
python -c "from enum_core import inst_asymmetric_branch,gap; print(gap(inst_asymmetric_branch(),2))"
```

---

## What would falsify the remaining claim

- Bug in L1/TV DP (independent reimplementation disagrees).  
- Demonstration that the declared nonadaptive class incorrectly forbids feasible T1 nonadaptive inspections (path-free) **and** that product claims ignored that — already documented as conditional.  
- Prior-art paper with identical instance and constants → re-label to pure KNOWN RESULT (still scientifically fine).

---

## How CHARM13 should change (P6 product translation)

**Do now (docs / honesty only — no weight tuning as “research”):**

1. README / MASTER: state clearly that `blown_score` is an **engineering severity aggregate**, not a probability; refuse = **any bad OR score≥0.6**.  
2. Prefer reporting **finding sets** (and later witness transcripts) alongside the scalar.  
3. Do **not** claim adaptive T1 security bounds without specifying the query/legality model.

**Do later (optional research diagnostics, not v0.3.3 force):**

4. Research-only `charm research-dB` style tool under `research/` — not required for mission close.  
5. New global smell candidates inspired by C (co-occurrence / manifest-set relations) — separate small PR, with fixtures.  
6. Lean formalization of Lemma 1–2 in `FORMAL/`.

**Do not:**

- Retune weights and call it M4 success.  
- Add templates as research output.  
- Claim T3/T4.  
- Publish anti-forensics guidance.

---

## Directive §15 checklist

| Question | Answer |
|----------|--------|
| What was discovered? | Exact adaptive gap certificate; score non-monotonicity; local-global D₁ separation |
| Believed before? | Score≈risk; local≈global naturalness; no D_B |
| Proved/disproved? | See above |
| Closest known? | Active testing / parity / noisy-OR dependence (field level) |
| Genuinely different? | CHARM-specialized certificates + score kill; not new TV |
| Essential assumptions? | Finite models; list-before-head for FS gap |
| Smallest example? | wit-A-asym-branch-B2 |
| Falsifier? | DP bug or path-free model without disclosure |
| CHARM change? | Docs honesty now; optional global smells later |

---

## Role sign-off (draft for human)

| Role | Verdict |
|------|---------|
| CHARM13 | Central statement ready as finite-model result |
| HUNTER | Witnesses filed; n=3 restricted search gap=0 |
| MIRROR | Accept as **application certificates**; block pure novelty marketing |
| Human owner | Final arbiter |

**Mission success (finite-model counterexample track): YES under label `MINIMAL COUNTEREXAMPLE ESTABLISHED`.**  
**Mission success as Annals-grade new theorem: NO — not claimed.**
