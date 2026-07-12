# CHARM13 — Master Plan

**Status:** binding doctrine for the project  
**Mark:** CHARM / CHARM13  
**Code:** `C:\Users\coldb\charm13`  
**Version this plan assumes:** 0.3.4 (`forge`, `smell`, `bench`, habitats, any-bad blows, T1 budget doctrine)

This document is how the work is understood. Not marketing. Not a feature wishlist.
If a choice conflicts with this file, this file wins until it is deliberately revised.

---

## 0. One sentence

**CHARM13 makes strong ciphertext boring to find.**

Encryption already randomizes bits. CHARM13 randomizes the *story those bits tell on disk* so the first hypothesis is not “vault.”

**Naturalness law:** blown if the tree does not look natural for the *habitat* it claims. Genomics was a calibration accident (fails loudly when faked), not the product’s center of mass. See `docs/NATURAL.md`. File-type space is huge; we enforce *claimed type ⇒ checkable nature* and *claimed habitat ⇒ no foreign specialists*, not an encyclopedia of every extension.

We do not claim a new cipher. We claim a better answer to:

> Given that encrypted volumes exist and look like noise or like tools, how do you reduce the chance that a human or a short automated pass *targets* the right blob?

That is the product.

---

## 1. What “best in the world” means here

Not: beat AES. Not: beat Signal. Not: “military grade” adjectives.

**Best means:**

1. **Clearest threat model** in the category (honest T0–T4).  
2. **Strongest cover science** — invariants, smell calculus, counterexamples, not vibes.  
3. **Tightest loop** from “this cover is blown” → automated detection → forge refuses or repairs.  
4. **Least embarrassing public surface** — docs and UX that a skeptical cryptographer does not dismiss as theater or LLM sludge.  
5. **Operational usefulness** on real machines (Windows + Linux), real VeraCrypt (or successor), real sizes, real mistakes people make.

If we only ship templates and a wrapper, we failed.  
If we ship a **detection-backed camouflage system** with deniability hooks and no false promises, we are in the right game.

---

## 2. Layers (never confuse them)

| Layer | Name | Job | Solved? |
|-------|------|-----|---------|
| L0 | Cipher | Confidentiality of bytes | Borrow (VeraCrypt / later own format) |
| L1 | CELLAR | Password games, hidden volume, multi-surrender | Partial (manual VC today; automate later) |
| L2 | PROPS / FORGERY | Narrative tree, IDs, times, checksums | v0.1 started |
| L3 | CALIPER / PEEL | Size bands, extensions, outer skin | v0.1 partial |
| L4 | MIRROR | Smell / blown_score / refuse bad covers | v0.1 smell started |
| L5 | NEST | Placement in a host filesystem story | Not built |
| L6 | OPSEC surface | How the *tool itself* looks and is documented | Doctrine only |

**Most tools stop at L0.**  
VeraCrypt hidden volume is L0+L1.  
MP4 stego is a narrow L3 trick.  
**CHARM13 owns L2–L4 as first-class science**, with L1 as a first-class product goal, L0 as dependency.

“Encrypt the encryption” = **L2–L4 + honest L1**, not double-AES.

---

## 3. Threat model (axioms)

| Tier | Adversary | Goal of CHARM13 | Claim |
|------|-----------|-----------------|-------|
| T0 | Shoulder, roommate, thief glancing | Not interesting | Strong |
| T1 | Curious tech, ~10 min, `file`, sizes, tree | Raise cost / fail casual tells | Strong if smell is sharp |
| T2 | Stolen disk, offline | Crypto holds; cover reduces prioritization | Crypto-dependent |
| T3 | Compelled password | Outer story password only | Only with CELLAR done right |
| T4 | Lab + legal process + time | — | **No claim. Ever.** |

Every feature must list **tiers helped** and **failure mode**.  
Features that only help T0 and add complexity are optional templates, not core.

---

## 4. Research posture (how work is done)

Work like the session is proving lemmas, not filling tickets.

### 4.1 Definitions (keep precise)

- **Cover story** — claimed identity of a path tree + payload (template + forgery fields).  
- **Payload** — the large file that is or will be the volume.  
- **Smell** — observable that raises P(vault | observation).  
- **Blown** — smell set crosses threshold under a stated oracle.  
- **Narrative consistency** — decoys, sizes, mtimes, checksums, names cohere.  
- **Size band** — allowed payload size range for a template.  
- **Detection oracle** — procedure an adversary runs (human checklist or tool).  
- **Re-skin** — change L2–L3 without re-encrypting L0.

### 4.2 Session rules

1. Definitions before features.  
2. Adversary tier on every change.  
3. Counterexamples: try to blow every cover.  
4. Invariants preferred over aesthetics.  
5. One novel contribution per serious session (not just flags).  
6. Discard cute.  
7. Public text is dry operator English.  
8. Prove by the smallest test or `smell` rule.  
9. End with: argued / open / next lemma.

### 4.3 What counts as a “holy fuck” result

- Smell calculus with composition rules  
- `blown_score` that separates known-bad covers from boring trees  
- Forge that **refuses** high blown_score by default  
- CELLAR that changes the password game, not a thin CLI wrap  
- Re-skin that preserves L0  
- Template algebra (compose covers without breaking invariants)  
- Empirical sibling-size models from real project trees (optional research track)

Glue code alone is not a win.

---

## 5. Invariants (v1 target — enforce in code)

Forge output **must** satisfy (or warn/refuse):

1. `size(payload) ∈ band(template)` unless `--unsafe-size`.  
2. No specialist extension (`.cram`, `.bam`, …) without a stated policy:  
   - either valid magic (hard), or  
   - non-specialist extension, or  
   - explicit `--lie-extension` with smell=bad.  
3. No well-known reference corpus IDs in paths (GIAB, etc.).  
4. Checksums in cover files match the decoy files that exist (byte-stable).  
5. mtime window coherent with README “created/revised” story.  
6. Payload share of tree bytes not absurd without a story (monolith warn).  
7. No cluster of sub-512B “toy” siblings next to multi-GB payload without incomplete-download template.  
8. Seed recorded for cover reproducibility (not the volume password).

`charm smell` is the predicate.  
`charm forge` is the constructor that should not emit known-blown trees.

---

## 6. Smell calculus (draft)

Severity: `info` < `warn` < `bad`.

Examples (implement and extend):

| Rule | Severity | Idea |
|------|----------|------|
| specialist_ext ∧ ¬valid_magic | bad | .cram that is not CRAM |
| size ∉ band | warn/bad | band ceiling → bad |
| giab_token in path | bad | famous samples |
| toy_siblings ∧ huge_payload | warn | placeholder theater |
| monolith share > 99.5% ∧ huge | warn | single blob pack |
| high_entropy ∧ huge ∧ random name | info | normal for crypto; not alone decisive |

**blown_score (implemented):**

```text
blown_score = 1 - Π (1 - w_i)  over triggered findings
weights: bad=0.55, warn=0.25, info=0.05
refuse   = (∃ bad)  ∨  (blown_score ≥ 0.6)
```

**Semantics (binding, v0.3.4+):**

- Weights are **ordinal engineering severities**, not calibrated probabilities.
- The product is a severity monoid (noisy-OR algebra), not P(generated | tree).
- One `bad` alone scores 0.55 but still refuses via the any-bad clause.
- Prefer the finding list over the scalar. See `docs/T1_BUDGET.md`.

**T1 / adaptive inspection (research-backed doctrine):**

- `charm smell` is a **nonadaptive** checklist.
- Finite-model research (`research/LADDER_MASTER.md`, M4–M18) shows adaptive
  short policies can strictly dominate fixed checklists of equal budget on
  explicit branch/parity habitat families; camouflage “capacity” under adaptive
  B≥2 can be zero for ε<1 on those families.
- Product rule: clean smell is **necessary refuse machinery**, not a complete
  adaptive T1 risk certificate. No T4 claim. No new cipher.

Calibration fixtures:

- A: old decoy 436GB “CRAM” + Nebula toys → score ~1  
- B: real small CRAM/BAM if available → low specialist failure  
- C: boring adobe_cache 1–2 GiB tree → low  
- D: raw random file named `.dat` → info entropy only  

Default: `forge` exits non-zero if predicted blown (any bad or score ≥ 0.6) unless `--i-know`.

---

## 7. Architecture

```text
charm
├── cli          user entry
├── forge        constructor
├── smell        detection predicate + blown_score
├── forgery      RNG identity fields
├── props        decoy trees (templates)
├── caliper      size bands / extensions
├── kernel       VeraCrypt (L0) create/mount
├── cellar       hidden volume / dual password (later)
├── peel         outer skin / wrappers (later)
└── nest         placement suggestions (later)
```

Templates live as data (YAML later); v0.1 code is fine if structure stays swappable.

### 7.1 CLI surface (stable names)

| Command | Purpose |
|---------|---------|
| `charm forge` | Build cover + optional volume |
| `charm smell` | Report findings + score |
| `charm templates` | List covers |
| `charm which-vc` | Locate VeraCrypt |
| `charm mount` | Later: mount helper |
| `charm skin` | Later: re-skin L2–L3 |
| `charm burn` | Later: destroy cover / secure delete helpers (careful) |
| `charm cellar` | Later: hidden volume recipe |

---

## 8. Roadmap

### Phase 0 — Done

- Name CHARM13, doctrine, anti-slop rules  
- Package layout, MIT, dry README  
- `forge` / `smell` / templates  
- VeraCrypt detection  
- Placeholder + tree-only modes  

### Phase 1 — Smell becomes law (done in 0.2.0)

1. `blown_score` + exit codes (smell 2 if blown)  
2. Synthetic tests (fake CRAM+GIAB fixture in tests)  
3. `forge` post-smell; refuse if score ≥ 0.6 unless `--i-know`  
4. wgs_lab opaque `.pack.dat/.bin/.img` — no fake `.cram`/`.bam`  
5. Real md5/sha256 of written files  
6. Unit tests for score, forge, invariants  
7. `--force` rebuilds clean tree (no leftover specialist files)

**Exit criteria:** met — classic fake CRAM+GIAB scores ~0.98 BLOWN; clean pack scores ~0.

### Phase 2 — CELLAR (deniability)

1. Document outer/hidden volume procedure with VeraCrypt.  
2. Automate what the CLI allows safely (outer create, decoy fill, guidance for hidden).  
3. Never log passwords.  
4. Optional: two-password checklists for T3.

**Exit criteria:** one command path produces outer decoy data + instructions/automation for hidden volume without breaking L2 invariants.

### Phase 3 — Cover quality

1. Templates as YAML (community later).  
2. More templates: corporate backup, phone export, game depot, “Windows.old fragment”.  
3. mtime/atime strategies per OS.  
4. `charm skin` re-story without touching ciphertext when payload is opaque file.  
5. NEST: suggest parent paths.

### Phase 4 — Hard covers (optional research)

1. Real format wrappers only if they buy T1 (sparse VHDX, etc.).  
2. No fake CRAM magic that pretends to be sequence data.  
3. Stego (MP4) only as optional PEEL profile with size limits and clear docs.

### Phase 5 — Product hardening

1. Linux CI + Windows smoke.  
2. Signed releases if distributed.  
3. Threat model frozen in README.  
4. Audit pass: dependency minimalism.

---

## 9. Anti-slop doctrine (public surface is OPSEC)

Presentation is part of the threat model.

1. No AI provenance anywhere in the public tree.  
2. Dry operator voice. No Product Hunt, no emoji storms, no “seamless/robust/leverage.”  
3. Commits: small, boring, human-paced.  
4. Code: no decorative abstractions.  
5. README: threat model → install → examples → what this is not.  
6. If a skeptical reader smells LLM toy, rewrite until they don’t.

Private assistance is fine. **Public tree reads as a competent human tool.**

---

## 10. Ethics and dual-use

Frame and design for:

- privacy on shared machines  
- journalists / travelers / sensitive personal data  
- reducing casual discovery of encrypted backups  

Do not market as anti-forensics against lawful process.  
Do not promise deniability under torture or lab analysis.  
Do not help hide evidence of violent crime; refuse that use case in docs by silence and honest scope, not cartoon villain README.

---

## 11. Relationship to the user’s real systems

| Asset | Role |
|-------|------|
| VeraCrypt | L0 engine today |
| Manual “CRAM” container + Nebula tree | Prototype of L2–L3; calibration target for smell |
| Real WGS CRAM/VCF (NG1KGP8JUJ) | Separate project; not CHARM payload by default |
| CHARM13 repo | The tool |

Smell should score the *prototype mistakes* as blown. That is success.

---

## 12. Success metrics

| Metric | Target |
|--------|--------|
| Casual glance (T0) | Payload not obviously “vc container” |
| Ten-minute tech (T1) | No free wins from magic/size/GIAB/toy siblings |
| Self-test | `blown_score` high on known-bad fixtures, low on good ones |
| Docs | Zero false T4 claims |
| Taste | Skeptical crypto reader does not laugh |

---

## 13. Open problems (honest)

1. Specialized formats without lying: hard. Prefer non-specialist outer types.  
2. True deniability under T3 is a protocol + discipline problem, not only software.  
3. OS and app leakage (MRU, thumbnails, Defender) can betray volumes regardless of cover — document, don’t ignore.  
4. Quantitative sibling models need data.  
5. Re-skin of mounted filesystems differs from re-skin of a single file payload.

---

## 14. Immediate next build order (when implementing again)

1. `blown_score` + forge gate  
2. Payload extension policy (containers are `.dat`/`.hc`/`.img` by default; lab story in text)  
3. Real md5/sha of decoy files  
4. Fixtures + tests  
5. CELLAR design doc (still dry)  
6. Only then more templates  

---

## 15. Callsign

**CHARM13** — soft word, hard job. Luck and thirteen. Radio, not SaaS.

Tagline for humans who get it:

> Lucky callsign. Heavy payload.

Tagline for the README (drier):

> Camouflage factory for encrypted volumes.

---

## 16. Closing standard

Every session should leave the repo more able to **answer**:

> Is this cover blown, and can we stop shipping blown covers?

When that loop is tight, CHARM13 is no longer a script. It is a small, sharp instrument.

End of master plan.
