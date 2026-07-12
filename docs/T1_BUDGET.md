# T1 observer model — budgeted inspection

**Status:** product doctrine (v0.3.7)  
**Audience:** operators and reviewers  
**Math source:** `research/` ladder M4–M18, especially M5 seed package (finite models; not a warranty on real disks)

---

## 1. What `charm smell` is

`charm smell` is **as-built service inspection**: a deterministic, nonadaptive
checklist that walks the tree, applies fixed local and habitat rules, aggregates
severities, and refuses under a dual gate. It is quality control on the cover
member — not a full model of an adaptive inspector’s demand envelope.

| Property | Smell today |
|----------|-------------|
| Observation order | Fixed (full walk) |
| Budget | Unbounded relative to a short T1 session (it reads what it needs) |
| Adaptivity | None — later checks do not depend on earlier answers in a policy sense |
| Output | Finding multiset + severity monoid `blown_score` + dual refuse |

## 2. Score semantics (binding)

```text
blown_score = 1 − ∏ (1 − w_sev)     w: bad=0.55, warn=0.25, info=0.05
refused     = (∃ bad finding)  ∨  (blown_score ≥ 0.6)
```

**`blown_score` is not a probability of generation.**  
Weights are ordinal severity knobs. The product formula is a commutative monoid
(noisy-OR algebra), not a calibrated likelihood or posterior.

**Any single `bad` finding refuses** even when `blown_score < 0.6`
(one bad alone scores 0.55). The threshold gate is load-bearing primarily for
**warn stacks**.

Research (M4-B, M15) exhibits explicit order reversals between score rank and
likelihood-ratio rank under synthetic laws. Operators should prefer the
**finding list** over the scalar.

## 3. Adaptive versus checklist (research envelope)

Two finite-model layers matter:

### 3a. Sharp budget-2 law (arity-constrained, OPEN queries)

Under globally addressable unit-cost queries of active arity at most $K$,

$$
D_2^{\mathrm{ad}}\le K\,D_2^{\mathrm{na}},
\qquad
G_2(K)=\sup\bigl(D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}\bigr)=1-\frac1K.
$$

Binary queries ($K=2$): additive gap at most $1/2$, and the M4 four-world
butterfly attains it. Flattening: if active signed support has size
$r\le B+1$, then adaptive and nonadaptive values coincide (no OPEN gap).

Reference: `research/m5/SEED_THEOREMS.md`, `research/m5/RESULT.md`.

### 3b. Habitat families (branching / parity)

On explicit infinite families (k-branch “which-then-bit” and m-bit parity):

| Statement | Reference |
|-----------|-----------|
| Adaptive budget 2 can achieve total-variation advantage 1 for every branching factor k | M5-U, M6 |
| Best nonadaptive budget B on the k-pair family achieves only min(B,k)/k | M5–M6 |
| Gap → 1 as k → ∞ for every fixed B ≥ 2 (on that family) | M6 |
| Myopic “strongest local first” is unboundedly suboptimal | M5-U, M7 |
| No fixed nonadaptive budget B uniformly keeps risk ≤ ε against adaptive T1 | M8 |
| Adaptive indistinguishability capacity is 0 for ε < 1 when B ≥ 2 on that family | M9 |
| Parity-style globals: adaptive cost 1+m vs nonadaptive k·m | M12–M13 |

**Packaging note:** k-pair nonadaptive value $2/k$ at budget 2 is a
**habitat** closed form. The **sharp universal** nonadaptive ceiling under
arity-$K$ queries is $1/K$, not $2/k$.

**Product reading (careful):**  
A cover that is **clean under the static smell suite** is not thereby proven
safe against every **adaptive** short inspection with the same number of
looks. Smell remains necessary refuse machinery; it is not a complete T1
risk certificate.

**Not claimed:** real filesystem distributions equal these families; T3/T4;
cryptographic novelty; literature novelty of the sharp law.

## 4. Operator guidance that follows

1. **Always pass `-t` / template** so habitat law applies.  
2. **Read findings**, not only the score.  
3. Prefer **opaque payload extensions**; never specialist magic lies.  
4. When a habitat has many branches (paths, IDs, cache buckets), ensure
   **manifest / pointer / which-path** coherence before relying on local
   magic alone (“gate before local”).  
5. Global relations (checksum *sets*, co-occurrence, parity-style invariants)
   matter; local OK does not imply global OK (M4-C, M12).  
6. Do not interpret clean smell as “adaptive T1 risk below ε.”  
7. Forge: default refuse on blown; `--i-know` is informed override only.

## 5. Reproducing the mathematics

```powershell
cd research\ladder
python run_ladder.py
python run_ladder_high.py
cd ..\m4\EXPERIMENTS
python test_certificates.py
cd ..\..\m5\EXPERIMENTS
python test_m5_exact.py
python test_m5.py
```

See `research/LADDER_MASTER.md` for the mission index. Sharp M5 seed package:
`PROVED — NOVELTY UNRESOLVED`. Broad adaptivity packaging remains
`KNOWN RESULT, NEW APPLICATION`.

## 6. Purdue note

This doctrine line was integrated under Boilermaker engineering standards:
measure twice, cut once; refuse theatrical novelty; keep the refuse loop honest.
