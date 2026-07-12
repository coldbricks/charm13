# Theorem M4-A — Adaptive gap (finite model)

**Status:** PROVED (exact arithmetic) + **minimality PROVED** for unguarded unit-cost depth-2 model  
**Novelty:** `KNOWN RESULT, NEW APPLICATION` (external scientist review 2026-07-12; see PRIOR_ART.md)  
**Machine check:** `python research/m4/EXPERIMENTS/test_certificates.py`  
**Artifacts:** `COUNTEREXAMPLES/wit-A-asym-branch-B2.json`, `wit-A-list-then-head-B2.json`  
**External review:** independent check of proof + certificate suite; minimality upgraded from search to lemma (below)

---

## Setup

Finite world set `W = {0,1,2,3}` with masses:

| World | P | Q | gate | left | right |
|------:|--:|--:|-----:|-----:|------:|
| 0 | 1/2 | 0 | 0 | 0 | 0 |
| 1 | 0 | 1/2 | 0 | 1 | 0 |
| 2 | 1/2 | 0 | 1 | 0 | 1 |
| 3 | 0 | 1/2 | 1 | 0 | 0 |

Queries (unit cost): `gate`, `left`, `right` — **globally available** (no path guards)  
(see `inst_asymmetric_branch` in `enum_core.py`).

Budget `B = 2`. Policies **deterministic**, non-destructive. Observer knows `(P,Q)`.

`D_B` and `D_B^{na}` as in `DEFINITIONS.md` (½ of optimal leaf L1 mass).

---

## Lemma 1 (nonadaptive upper bound at B=2)

For every set of queries with total cost ≤ 2,

$$
\mathrm{TV}(\mathrm{Law}_P(T),\mathrm{Law}_Q(T)) \le \tfrac12.
$$

### Proof by cases

**Empty / single query.**

- `gate`: under P, obs 0 and 1 each with mass 1/2 (worlds 0 vs 2). Under Q, same (1 vs 3). TV = 0.  
- `left`: obs table (0,1,0,0). P-mass on obs0 = 1, on obs1 = 0. Q-mass on obs0 = 1/2 (world 3), obs1 = 1/2 (world 1).  
  TV = ½(|1−½|+|0−½|) = ½.  
- `right`: symmetric TV = ½.

**Two queries.**

- `{gate,left}`: observation pairs  
  - (0,0): world 0 — P=½, Q=0  
  - (0,1): world 1 — P=0, Q=½  
  - (1,0): worlds 2 and 3 — P=½, Q=½  
  - (1,1): empty  
  L1 sum = ½+½+0 = 1 ⇒ TV = ½.  
- `{gate,right}`: symmetric TV = ½.  
- `{left,right}`: pairs  
  - (0,0): worlds 0 and 3 — P=½, Q=½  
  - (1,0): world 1 — Q=½  
  - (0,1): world 2 — P=½  
  L1 = 0+½+½ = 1 ⇒ TV = ½.

Hence `D_2^{na} = 1/2`. ∎

---

## Lemma 2 (adaptive achieves TV = 1 at B=2)

Policy π*:

1. Issue `gate`.  
2. If obs = 0, issue `left`. If obs = 1, issue `right`.

### Transcript partition

| path | worlds | P | Q |
|------|--------|--:|--:|
| gate0·left0 | {0} | ½ | 0 |
| gate0·left1 | {1} | 0 | ½ |
| gate1·right1 | {2} | ½ | 0 |
| gate1·right0 | {3} | 0 | ½ |

L1 sum = ½+½+½+½ = 2 ⇒ TV = 1.

Hence `D_2 ≥ 1`. Combined with `D_B ≤ 1`, `D_2 = 1`. ∎

---

## Theorem A (finite-model adaptive gap)

Under the instance above,

$$
D_2(P,Q) = 1, \qquad D_2^{\mathrm{na}}(P,Q) = \tfrac12,
\qquad D_2 - D_2^{\mathrm{na}} = \tfrac12.
$$

In particular adaptivity **strictly** increases distinguishing power at budget 2.

### Relation to CHARTER A.1

CHARTER asked for `D_2 ≥ 1/2` and `D_2^{na} ≤ 1/4`.  
This witness is **stronger** on the adaptive side and weaker on the nonadaptive upper bound (½ not ≤¼).  
A.1 as literally written is **not** witnessed by this instance; the **qualitative** claim “strict adaptive gap at B=2 with n≤6” **is**.

---

## Lemma 3 (minimality: no adaptive gap for ≤3 worlds)

**Model for this lemma only:**

- Finite support size `n ≤ 3` (at most three worlds with positive mass under `P+Q`).  
- Deterministic adaptive policies of depth at most 2 (budget 2, unit-cost queries).  
- Queries are **globally available**: any query may be issued at any time (no observation-dependent legality / path guards).  
- Nonadaptive class = fixed set of at most two queries applied to every world.  
- Non-destructive observations; terminal TV is that of the partition of worlds induced by the transcript.

**Claim:** For every such instance,

$$
D_2(P,Q) = D_2^{\mathrm{na}}(P,Q).
$$

In particular adaptivity cannot strictly help.

### Proof

Let `π` be any deterministic adaptive policy of depth ≤ 2. Let `q₁` be its first query. The observation map of `q₁` partitions the support into cells.

With at most three worlds, **at most one cell can be non-singleton**: two disjoint cells of size ≥ 2 would require ≥ 4 worlds.

- If every nonempty cell is a singleton, the first query already separates all worlds. Further queries cannot increase TV. Then the nonadaptive policy that issues only `q₁` matches `π`.  
- If there is a unique non-singleton cell `C`, then only paths that land in `C` can benefit from a second query. Let `q₂` be the second query that `π` issues on that cell (if `π` stops on `C`, take any query; refinement is optional). On singleton cells, a second query cannot split a single world further, so it cannot change those atoms’ contribution to TV.

Consider the **nonadaptive** pair `{q₁, q₂}` (or `{q₁}` if no second query is used on `C`). Its joint observation partition of the support **refines** (is at least as fine as) the terminal partition induced by `π`:

- Worlds separated by `q₁` remain separated.  
- Worlds inside `C` are split exactly by `q₂`, matching `π`’s refinement of `C`.  
- Singleton cells remain single worlds.

For any two measures on a finite set, refining a partition cannot decrease total variation of the pushforwards. Therefore

$$
\mathrm{TV}(\mathrm{Law}_P(T_{\pi}),\mathrm{Law}_Q(T_{\pi}))
  \le
\mathrm{TV}(\mathrm{Law}_P(T_{\{q_1,q_2\}}),\mathrm{Law}_Q(T_{\{q_1,q_2\}}))
  \le D_2^{\mathrm{na}}(P,Q).
$$

Taking the supremum over adaptive `π` yields `D_2 ≤ D_2^{na}`. The reverse inequality is always true. ∎

### Corollary (four-world construction is size-minimal)

Under the unguarded deterministic unit-cost depth-2 model of Lemma 3, no adaptive gap exists for `n ≤ 3`, while Theorem A exhibits a gap at `n = 4`.  
Hence the four-world instance is **minimal in support size** for a strict adaptive gap in that model.

### Qualifier (filesystem / path-prefix)

Lemma 3 **does not** automatically apply when observation-dependent **legality** means a query cannot be named before a path is discovered (e.g. `head_a` requires prior `list`).  
In that guarded model, nonadaptive policies may be weaker for structural reasons unrelated to the three-world partition argument.

The docket’s `list_then_head` instance remains a valid gap **under requires**, and correctly notes that the gap **vanishes** under path-free addressing (`D_2^{na}=1`). That assumption is load-bearing; it is not a free upgrade of Theorem A.

### Note on earlier computational search

`hunt.py` reported gap 0 on 156672 restricted three-world binary-query instances. That is **supporting evidence only**. Lemma 3 is the minimality proof; the search count is not required for the theorem and was not independently re-certified in the external review window.

---

## Filesystem specialization (path-prefix)

Instance `list_then_head` (`wit-A-list-then-head-B2.json`):

- `list` reveals child name `a` or `b`  
- `head_a` / `head_b` require `list` (DEFINITIONS legality)  
- Same P/Q pattern on bits  

Then `D_2 = 1`, `D_2^{na} = 1/2` under the requires model.

**Stress:** if nonadaptive may issue `head_a`/`head_b` without prior `list` (path-free), then `D_2^{na}=1` and the gap **vanishes**.

---

## Machine verification

```text
W(S,b) DP: adaptive_W in enum_core.py
nonadaptive: all cost-feasible query subsets
assert gap(asym_branch, 2) == 1/2
python test_certificates.py  # 8/8
```

External scientist review independently ran the certificate suite (8/8) and inspected the hand proof for Theorem A.

---

## Prior-art honesty (binding)

The gate→branch pattern is standard “which experiment next” geometry in fixed-horizon active hypothesis testing and costly feature acquisition.  
**Not a new theorem of adaptive testing.** Residual contribution: exact four-world certificate, proved size-minimality under unguarded depth-2, CHARM path-prefix legality specialization with explicit path-free stress, reproducible code.

See `PRIOR_ART.md` (Kartik, Kartik, et al.–style active testing literature; arXiv:1911.06912 as entry point).
