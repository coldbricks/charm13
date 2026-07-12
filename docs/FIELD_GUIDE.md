# Field guide — CHARM13 and budgeted inspection

## Positioning

Encrypted volumes already solve confidentiality of **bytes**. They do not solve the **on-disk story**. A high-entropy object that fails the habitat it claims is not a crypto break — it is a cover failure. That is the problem CHARM13 is built for.

CHARM13 is an engineering system for **habitat camouflage evaluation and construction** around encrypted volumes, together with a finite-model research program on **budgeted adaptive distinguishability** of attributed filesystem trees. Construct, measure, refuse. Static inspection is necessary QC; it is not a full adaptive T1 certificate. T4 is unclaimed.

It does not introduce a new cipher. Confidentiality of bytes is **L0** (external, e.g. VeraCrypt). CHARM13 owns cover naturalness, detection, and refuse-on-blown.

## Two layers people conflate

| Layer | Role | Owner |
|-------|------|--------|
| Cryptographic ciphertext | Foundation — secrecy of content | External L0 (VeraCrypt, etc.) |
| Cover / habitat story | Superstructure — on-disk narrative | CHARM13 forge + inspect |

Most tools stop at the foundation. CHARM13 draws a continuous load path: **construct → measure → refuse**.

## Research neighborhood

The mathematical work is closest to:

- active / sequential hypothesis testing under a look budget  
- costly feature acquisition for binary discrimination  
- total variation between transcript laws under restricted observation maps  

Results are stated for **explicit finite synthetic families** (k-branch which-then-bit; m-bit parity habitats), with exact rational certificates. Broad “adaptivity can help” is classical; residual contributions are closed-form envelopes, assumption hygiene, and product doctrine.

## Product oracle vs adaptive T1

`charm smell` is the **inspection** command: service-level QC — a deterministic nonadaptive checklist (fixed rules, full walk, severity monoid, dual refuse gate).

A human T1 inspector may be **adaptive**: the next observation depends on prior answers. On the synthetic families in `research/`, adaptive advantage at fixed budget can strictly dominate any nonadaptive suite of the same cost, with gap approaching one as branching grows. A clean inspection report is necessary detailing; it is not the ultimate-capacity envelope for every adaptive demand of similar length.

## Score semantics

```text
blown_score = 1 − ∏ (1 − w_sev)
refused     = (∃ bad) ∨ (blown_score ≥ 0.6)
```

Weights are ordinal engineering severities. The product is a monoid, not a calibrated posterior probability of generation. One `bad` finding refuses even when the scalar sits below 0.6.

## Non-claims

- No T4 laboratory guarantees  
- No operational guidance for concealing material from inspection workflows  
- No assertion that empirical disk populations equal the synthetic k-pair family  
- No novelty claim for total variation or for the abstract existence of adaptive gains  

## Reproduction

See `research/LADDER_MASTER.md` and `docs/T1_BUDGET.md`.
