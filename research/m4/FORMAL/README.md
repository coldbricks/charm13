# FORMAL — Proof assistant artifacts

**Status:** stub (P0)  
**Requirement (directive §10):** at least one **nontrivial** finite-model lemma formalized in Lean 4, Coq, Isabelle, or team-accepted assistant.  
Formalizing only `D_B` monotonicity does **not** satisfy the requirement.

---

## Planned layout (when P4 opens)

```text
FORMAL/
  README.md
  lean/          # or isabelle/ or coq/
    lakefile / README
    HabitatTree.lean
    BudgetTV.lean
    MainLemma.lean
```

---

## Candidates for formalization (priority order)

1. **If M4-A witnesses:** exact TV values for a fixed finite (P,Q,B,π) instance (computable certificate).  
2. **M4-B3 dual gate:** elementary but good pipeline smoke test (not sufficient alone).  
3. **If M4-A4:** correctness of DP recurrence against brute force on a finite class (statement + proof of recurrence).  
4. **If M4-B.1:** existence of order-reversing pair under explicit defect table (finite check).

---

## Tooling default

Prefer **Lean 4** if the team has no strong prior preference.  
Record version pins in this README when initialized.

---

## Non-goals

- Formalizing the entire CHARM Python codebase.  
- Claiming FORMALLY VERIFIED on a claim without checking assumptions against DEFINITIONS.md.
