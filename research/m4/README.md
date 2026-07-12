# research/m4 — Budgeted Habitat Indistinguishability

Research mission M4 for CHARM13. **Not product surface.**  
No mission success claimed. No novelty claimed.

## Start here

1. `CHARTER.md` — P0 formulation  
2. `DEFINITIONS.md` — symbols  
3. `CONJECTURES.md` — killable claims  
4. `CLAIM_LEDGER.json` — statuses  
5. `RESULT.md` — terminal slot (empty success)

## Adversaries

- `HUNTER_REPORT.md`  
- `MIRROR_REPORT.md`  
- `PRIOR_ART.md`

## Evidence dirs

- `COUNTEREXAMPLES/`  
- `PROOFS/`  
- `FORMAL/`  
- `EXPERIMENTS/`

## Reproduce

See `REPRODUCE.md`. Keep product tests green:

```powershell
cd C:\Users\coldb\charm13
python -m pytest -q
```

## Primary track

**M4-A** adaptive gap (proved) + size minimality Lemma 3 (unguarded).  
Status: **known phenomenon, exact certificate, CHARM packaging.**  
Side: **M4-B** score hygiene; **M4-C** classical local≠global.  
External review: `SCIENTIST_REVIEW.md`.  
Press: `PRESS_NOTE.md` **EMBARGOED**.

## Binding constraints

T0–T2 research framing; no T4; no anti-forensics cookbook; synthetic/public data only.
