# Lemma M4-B3 — Dual gate (elementary)

**Status:** PROVED BY DIRECT COMPUTATION  
**Ledger:** `M4-B3` · `KNOWN RESULT` / engineering documentation lemma  
**Not** the main M4 invention.

---

## Statement

Under CHARM13 v0.3.3 constants

$$
w(\mathrm{bad})=0.55,\quad \tau=0.6,
\quad
S(F)=1-\prod_{f\in F}(1-w(\mathrm{sev}(f))),
$$

and refuse rule

$$
R(F)=\mathbf{1}[\exists f:\mathrm{sev}(f)=\mathrm{bad}]\ \vee\ \mathbf{1}[S(F)\ge \tau],
$$

there exists a finding multiset F such that `S(F) < τ` and `R(F)=1`.

---

## Proof

Let F contain exactly one finding of severity `bad`.

$$
S(F)=1-(1-0.55)=0.55.
$$

Then `S(F)=0.55 < 0.6=τ`, so the score-threshold clause is false.

The any-bad clause is true. Hence `R(F)=1`.

∎

---

## Corollary (informal)

The operator refuse predicate is **not** identical to thresholding `S` at 0.6.  
Any prose that says “blown means score ≥ 0.6” without mentioning any-bad is false for v0.3.3.

---

## Formalization note

Eligible as a pipeline smoke test in `FORMAL/`; **does not** satisfy the nontrivial formalization requirement alone.
