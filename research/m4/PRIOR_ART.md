# M4 PRIOR ART — Collision search log

**Owner:** MIRROR  
**Status:** structured scaffold + preliminary map (not a completed collision report)  
**Rule:** Search mathematical content, not CHARM vocabulary.  
**Rule:** Do not fabricate citations. Unopened sources = `UNVERIFIED`.  
**Rule:** Closest known result required, not distant vibe-related work.

---

## 0. How to use this file

For each **source entry** record:

| Field | Content |
|-------|---------|
| citation | Exact bibliographic identity |
| theorem_or_algorithm | Precise name/number if any |
| assumptions | As stated by source |
| observer_model | Adaptive? costed? |
| hidden_object | vector / graph / tree / process / distribution |
| complexity | If given |
| relation_to_claim | exact match / special case / weaker / orthogonal |
| verified | OPENED \| UNVERIFIED \| NOT_YET |
| claim_ids | e.g. M4-A, M4-DEF-DB |

Status tags for claims after search: ledger labels in `DEFINITIONS.md` §11.

---

## 1. Objects under collision watch

| Object | Claim ids | Presumption of novelty |
|--------|-----------|------------------------|
| `D_B` adaptive transcript TV | M4-DEF-DB | **None** — likely restricted statistical distance |
| Adaptive vs nonadaptive gap | M4-A | Low–medium as pure gap; maybe application geometry |
| Exact DP for budgeted testing | M4-A4 | Low — POMDP / active testing |
| Noisy-OR under dependence | M4-B | Very low for qualitative claim |
| Dual gate score vs any-bad | M4-B3 | N/A engineering lemma |
| Local marginals vs global TV | M4-C | Very low qualitatively |
| Capacity `C_H` | M4-CAP | Name ≠ novelty |
| Repair min-cost | M4-R | Hitting set / OT repair likely |

---

## 2. Search term batches (execute systematically)

### Batch S1 — Definition of D_B
- active hypothesis testing query costs  
- sequential binary hypothesis testing adaptive measurements  
- controlled sensing two hypotheses  
- finite-horizon POMDP hypothesis testing  
- observation-constrained total variation  
- restricted statistical distance  
- Le Cam deficiency restricted experiments  
- Blackwell comparison of experiments  
- budgeted feature acquisition classification  
- decision-tree value of information  

### Batch S2 — Adaptive vs nonadaptive
- adaptive vs nonadaptive experimental design gap  
- adaptivity helps hypothesis testing examples  
- sequential design strict improvement finite sample  
- adaptive property testing trees graphs  

### Batch S3 — Trees / graphical models
- distinguishing tree graphical models limited observations  
- active testing graphical models  
- inference with partial node observations on trees  
- junction tree observation selection  

### Batch S4 — Local to global
- marginal polytope inconsistency  
- local consistency global inconsistency CSP  
- pairwise marginals do not determine joint  
- Dobrushin condition uniqueness  
- sheaf theoretic contextuality probability (only if forced)  

### Batch S5 — Score / evidence combination
- noisy-OR model independence assumption  
- dependent evidence combination failure  
- common cause multiple alerts  

### Batch S6 — Capacity / repair
- steganographic capacity distribution matching  
- channel resolvability  
- minimum cost distribution projection  
- rate distortion side constraints  
- adversarial anomaly detection attributed trees  

---

## 3. Preliminary field map (no specific paper claims yet)

These are **fields**, not citations. Promote to §4 only when a concrete source is opened.

| Field | Relevance | Risk to novelty |
|-------|-----------|-----------------|
| Wald sequential analysis / SPRT | sequential decisions, often sample-size not filesystem queries | Medium for process, low for tree geometry |
| Active hypothesis testing (e.g. Chernoff-style active testing literature) | closest high-level sibling of D_B | **High** |
| Controlled sensing | costed adaptive observations | **High** |
| Bayesian experimental design / VoI | policy choice under budget | High |
| Adaptive feature acquisition / classification with costly features | algorithm + gap examples | High for A/A4 |
| Property testing (adaptive) | different goal (property vs two fixed measures) | Medium |
| Le Cam theory / experiment comparison | D_B as deficiency-like quantity under experiment class | **High for DEF-DB** |
| Graphical model testing | local vs global | High for C |
| Steganography / distribution matching | C_H reductions | High for CAP |
| Noisy-OR fault diagnosis | B qualitative | High kill on novelty |

---

## 4. Source entries

### SRC-001 — Fixed-horizon active hypothesis testing (entry point)

```text
id: SRC-001
citation: arXiv:1911.06912 — Fixed-horizon Active Hypothesis Testing
  (URL: https://arxiv.org/abs/1911.06912 ; PDF also circulated in scientist review)
theorem_or_algorithm: framework for selecting experiments adaptively under bounded horizon
assumptions: sequential experiment selection; hypothesis testing objective; finite horizon
observer_model: adaptive; cost/horizon bounded
hidden_object: hypothesis / distribution class (not filesystem trees specifically)
complexity: (see paper; not re-derived here)
relation_to_claim: CLOSEST FIELD for M4-A / M4-DEF-DB — adaptive selection of
  observations under a budget/horizon is standard; CHARM gap is a special case geometry
verified: OPENED_AS_ENTRY_POINT (full theorem-by-theorem comparison still TODO)
claim_ids: [M4-A, M4-DEF-DB]
notes: External scientist pointed here as representative of the known phenomenon.
  MIRROR status for broad claim: KNOWN RESULT. Residual: exact 4-world pedagogical
  certificate + proved n≤3 minimality under unguarded depth-2 + FS legality packaging.
```

### SRC-000 — template

```text
id: SRC-000
citation: 
theorem_or_algorithm: 
assumptions: 
observer_model: 
hidden_object: 
complexity: 
relation_to_claim: 
verified: NOT_YET
claim_ids: []
notes: 
```

**Still incomplete as a literature review.** Do not invent further papers. Open textbooks/papers on costly feature acquisition next.

---

## 5. Provisional closest-known guesses (UNVERIFIED hypotheses)

These are **search targets**, not established collisions:

| Claim | Provisional closest class | If exact match then ledger becomes |
|-------|---------------------------|------------------------------------|
| M4-DEF-DB | TV of laws of adaptive experiments / restricted deficiency | KNOWN RESULT (definition) |
| M4-A | Finite examples of adaptive gap in feature acquisition | KNOWN RESULT or NEW APPLICATION |
| M4-A4 | Belief-state DP for finite-horizon active testing | KNOWN RESULT or NEW APPLICATION |
| M4-B | Dependence breaks noisy-OR probability reading | KNOWN RESULT (+ ENGINEERING ADAPTATION for CHARM) |
| M4-C | Local consistency ⇏ global joint | KNOWN RESULT; possible NEW APPLICATION if habitat witness export is sharp |
| M4-CAP | Distribution matching with distortion/cost constraints | KNOWN RESULT under reduction |

---

## 6. Collision decision protocol

1. Open candidate source (PDF or standard textbook edition).  
2. Fill SRC entry.  
3. If theorem assumptions and conclusion match claim after renaming only → `PRIOR-ART COLLISION` or `KNOWN RESULT`.  
4. If claim is strict special case with new constants/geometry → `KNOWN RESULT, NEW APPLICATION` or keep candidate with explicit delta.  
5. If only motivational similarity → note as related, keep candidate.  
6. Update `CLAIM_LEDGER.json` and `MIRROR_REPORT.md` in the same change set.

---

## 7. What is explicitly *not* prior-art success

- Finding a blog that says “filesystems are graphs.”  
- Citing an abstract without theorem statement.  
- Matching only the English phrase “indistinguishability.”  
- Claiming absence of prior art because CHARM-specific keywords return zero hits.

---

## 8. MIRROR next actions (ordered)

1. S1: name the standard object closest to `D_B` (textbook + 1–2 modern papers).  
2. S2: locate smallest known adaptive-vs-nonadaptive gap examples; compare geometry to `𝒬₀`.  
3. S5: one authoritative noisy-OR / dependent evidence reference for B.  
4. S4: one classical local-global counterexample reference for C.  
5. Only then argue residual novelty for A’s filesystem path-prefix legality.

---

## 9. Post-P1 update (2026-07-12)

Finite certificates landed (see RESULT.md). Field-level collision stance:

| Claim | Post-certificate stance |
|-------|-------------------------|
| M4-A gap | Pattern known; label application + exact certificate |
| M4-B | Interpretive kill; not new probability theory |
| M4-C | Classical parity |
| DEF-DB | Known-style object |

**Still required before novelty upgrade:** open and file SRC-001+ with real bibliographic records (no fabrication). Search queries ready in §2.

---

## 10. Post–scientist-review stance (2026-07-12)

| Claim | Stance |
|-------|--------|
| M4-A broad phenomenon | **KNOWN RESULT** |
| M4-A exact certificate + Lemma 3 minimality | **NEW APPLICATION / pedagogical minimum** — not “new adaptive testing theorem” |
| M4-B score | Product hygiene |
| M4-C parity | **KNOWN RESULT** |
| DEF-DB | **KNOWN RESULT** (definition class) |

## 11. Sign-off

| Role | Status |
|------|--------|
| MIRROR | Scientist-aligned: known phenomenon; certificate real; press embargo |
| Novelty of pure adaptive gap existence | **None** |
| Literature review completeness | **Incomplete** (SRC-001 entry only) |
