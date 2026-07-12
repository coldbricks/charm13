# M4 REPRODUCE — How to rebuild the research state

**Baseline product:** CHARM13 v0.3.3 at `C:\Users\coldb\charm13`  
**Research root:** `research/m4/`  
**Constraint:** product tests stay green; research code stays out of `src/charm` until P3.

---

## 1. Product baseline (must stay green)

```powershell
cd C:\Users\coldb\charm13
python -m pip install -e .
python -m pytest -q
python -m charm.cli bench
```

Expected (last known handoff): **18** tests passed; **bench 4/4**.

If red, stop research integration and fix product regressions first.

---

## 2. Document graph (P0)

| Path | Role |
|------|------|
| `CHARTER.md` | P0 formulation, score audit, claim ranking |
| `DEFINITIONS.md` | Frozen symbols |
| `CONJECTURES.md` | Exact killable statements |
| `CLAIM_LEDGER.json` | Machine-readable claim statuses |
| `PRIOR_ART.md` | Collision search log |
| `HUNTER_REPORT.md` | Adversarial enumeration status |
| `MIRROR_REPORT.md` | Methodology / novelty integrity |
| `RESULT.md` | Terminal statement (empty success) |
| `REPRODUCE.md` | This file |
| `COUNTEREXAMPLES/` | JSON witnesses/kills |
| `PROOFS/` | Human-readable proofs |
| `FORMAL/` | Proof assistant stubs |
| `EXPERIMENTS/` | Exact enumerators / notebooks |

---

## 3. Reproduce the dual-gate lemma (M4-B3)

No special harness required:

```python
# one bad finding
w_bad = 0.55
score = 1 - (1 - w_bad)  # 0.55
threshold = 0.6
any_bad = True
blown = any_bad or score >= threshold  # True even though score < threshold
```

Matches `charm.smell.is_blown` / `SmellReport.blown` in v0.3.3.

---

## 4. Reproduce forge randomness description

```powershell
cd C:\Users\coldb\charm13
python -c "from charm.forge import forge; from pathlib import Path; import tempfile; d=tempfile.mkdtemp(); r=forge(Path(d)/'t', template='adobe_cache', size_mb=1, placeholder=True, tree_only=True, force=True, i_know=True); print(r.seed, r.template, r.blown)"
```

Re-run with fixed `--` seed via API `seed=` to confirm identity stability (topology fixed).

---

## 5. Research experiments (P1+; not shipped in P0)

Planned layout:

```text
research/m4/EXPERIMENTS/
  README.md
  enum_policies.py      # exact rational D_B vs D_B^na
  defect_score.py       # Claim B order checks
  local_global.py       # Claim C toys
  fixtures/             # JSON (P,Q,queries)
```

Run (once implemented):

```powershell
cd C:\Users\coldb\charm13\research\m4\EXPERIMENTS
python enum_policies.py --fixture fixtures/H-A1.json
```

Requirements: Python 3.10+; stdlib preferred (`fractions`, `json`, `itertools`).  
No neural nets. No dependency on private data.

---

## 6. Counterexample artifacts

```powershell
# validate schema informally
Get-ChildItem C:\Users\coldb\charm13\research\m4\COUNTEREXAMPLES\*.json
```

Each file must include P, Q, queries, costs, B, policies, exact Fraction strings (see `COUNTEREXAMPLES/SCHEMA.md`).

---

## 7. Formalization (P4+)

```text
research/m4/FORMAL/
  README.md
  # lean/ or isabelle/ later
```

P0 contains only a README stub. A nontrivial lemma (not bare monotonicity) is required for formalization credit per directive.

---

## 8. Proof writeups

```text
research/m4/PROOFS/
  README.md
  # A_gap.md etc. when proved
```

---

## 9. Ledger hygiene

After any verdict:

1. Update claim status in `CLAIM_LEDGER.json`  
2. Note artifact path in HUNTER or MIRROR report  
3. If terminal, rewrite `RESULT.md` central statement  
4. Never claim novelty without PRIOR_ART SRC entry opened and verified  

---

## 10. Out of scope for reproduction

- Private genome files / Drive CRAM  
- Venmo OSINT packs  
- Inspecting user home directories as “real P_H”  
- Named forensic tool benchmarking  
- Weight tuning as research success  

---

## 11. Scientist protocol reminder

Compete via proofs, counterexamples, reproducible experiments.  
Falsifiable novelty only.  
No operational guidance for concealing encrypted data from inspection.
