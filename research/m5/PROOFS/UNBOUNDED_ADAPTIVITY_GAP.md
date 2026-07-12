# Theorem M5-U — k-pair habitat adaptivity gap at budget 2

**Status:** PROVED (analytic) + machine-checked for k ∈ {2,…,12}  
**Role:** CHARM-shaped **application family** (which-then-bit with off-branch `na`).  
**Not** the sharp universal envelope — that is $G_2(K)=1-1/K$ in `SEED_THEOREMS.md` / `SHARP_ROOT_ARITY.md`.  
**Novelty posture:** `KNOWN RESULT, NEW APPLICATION` pending full MIRROR sweep  
  — the *phenomenon* (adaptivity helps) is classical; residual is an  
  **exact infinite family** with closed-form `D₂=1`, `D₂^{na}=2/k`, unbounded gap and  
  ratio, plus **unbounded greedy failure**, specialized to CHARM’s inspection language.  
**Do not claim:** a new statistical distance; do not claim $2/k$ is the best possible nonadaptive value under arity-$k$ queries (the sharp construction achieves $1/K$).

---

## Model

Support worlds: for each branch index `i ∈ {0,…,k−1}` and bit `b ∈ {0,1}`,

$$
w_{i,b}.
$$

Laws (equal priors on branches):

$$
P(w_{i,0})=\frac1k,\quad P(w_{i,1})=0;
\qquad
Q(w_{i,1})=\frac1k,\quad Q(w_{i,0})=0.
$$

**Filesystem reading:** `i` = which child/path the story points at; `b` = header/magic bit on that path.  
Under `P`, every live path has bit 0; under `Q`, bit 1. Branch is uniform.

**Queries** (unit cost, globally available):

| Query | Observation on `w_{i,b}` |
|-------|---------------------------|
| `which` | `i` |
| `bit_j` | `b` if `i=j`, else `na` |

Budget worst-case. Deterministic policies. `D_B` as in M4 DEFINITIONS (TV of transcripts).

---

## Theorem U1 (perfect adaptive separation at budget 2)

For every integer `k ≥ 1`,

$$
D_2(P_k,Q_k) = 1.
$$

### Proof

Policy π*: issue `which`, observe `i`, then issue `bit_i`.

Terminal atoms are single worlds `w_{i,b}`. Each has either pure P-mass `1/k` or pure Q-mass `1/k`.  
L1 sum of |P−Q| over atoms = 2 ⇒ TV = 1. ∎

---

## Theorem U2 (nonadaptive budget-2 ceiling)

For every integer `k ≥ 1`,

$$
D_2^{\mathrm{na}}(P_k,Q_k) = \min\Bigl(1,\frac2k\Bigr).
$$

In particular for `k ≥ 2`,

$$
D_2^{\mathrm{na}}(P_k,Q_k) = \frac2k.
$$

### Proof

Nonadaptive policies with total cost ≤ 2 are: empty; one query; or a pair of distinct queries.

**Case `which` alone.**  
Pushforward of `P` and of `Q` are both uniform on `{0,…,k−1}`. TV = 0.

**Case `bit_j` alone.**  
Observations `{0,1,na}`:

| obs | P-mass | Q-mass |
|-----|--------|--------|
| 0 | 1/k | 0 |
| 1 | 0 | 1/k |
| na | (k−1)/k | (k−1)/k |

L1 = 2/k ⇒ TV = 1/k.

**Case `{bit_j, bit_m}`, j≠m.**  
The two pairs are fully separated (mass 1/k each fully split P vs Q); remaining mass on `na,na` is matched.  
L1 = 4/k ⇒ TV = 2/k.

**Case `{which, bit_j}`.**  
Transcript `(i, o)`:

- If `i≠j`: `o=na` under both; mass 1/k each side matched per such `i`.  
- If `i=j`: `o=b` separates `w_{j,0}` from `w_{j,1}` (mass 1/k).  

L1 = 2/k ⇒ TV = 1/k.

**Case two copies:** only one `which`. No better pair exists.

Maximum is `2/k` for `k≥2` (achieved by any two distinct bit queries). For `k=1`, `2/k=2` but TV≤1 so max is 1 (also `D_2^{ad}=1`). ∎

---

## Theorem U3 (unbounded gap and unbounded ratio)

For `k ≥ 2`,

$$
\mathrm{Gap}_2(k) := D_2 - D_2^{\mathrm{na}} = 1 - \frac2k \xrightarrow{k\to\infty} 1,
$$

$$
\frac{D_2}{D_2^{\mathrm{na}}} = \frac{k}{2} \xrightarrow{k\to\infty} \infty.
$$

### Proof

Immediate from U1–U2. ∎

**Contrast to M4:** M4 exhibited a single gap of `1/2`. Here the gap is **arbitrarily close to the maximum possible TV advantage**, at **fixed** budget 2.

---

## Theorem U4 (unbounded nonadaptive budget separation)

Let `B_{\mathrm{na}}^*(k)` be the minimal budget such that `D_B^{na}(P_k,Q_k)=1`.  
Let `B_{\mathrm{ad}}^*(k)` be the same for adaptive policies.

Then for all `k ≥ 1`,

$$
B_{\mathrm{ad}}^*(k) = 2,
\qquad
B_{\mathrm{na}}^*(k) = k.
$$

Hence the ratio `B_na^*/B_ad^* = k/2` is unbounded.

### Proof

**Adaptive:** U1 gives ≤2; budget 1 cannot perfect for `k≥2` (single `which` TV 0; single `bit_j` TV 1/k < 1). So =2 for `k≥2`. For `k=1`, budget 1 (`bit_0`) already perfect; statement uses `B_ad^*=1` in that edge — restrict to `k≥2` for the equality `B_ad^*=2`.

**Nonadaptive =1:** Need TV=1. Any nonadaptive set of queries induces a partition.  
Using `t` distinct bit queries yields TV = t/k (same argument as U2 generalized).  
`which` does not increase beyond the bits chosen (pairs not hit by a bit remain matched under `(pair, na)`).  
Thus TV = (# of bit queries)/k. Need ≥ k bit queries for TV=1. Each costs 1 ⇒ `B_na^* = k`. ∎

---

## Theorem U5 (myopic greedy is unboundedly suboptimal)

Define the **myopic first query** as any `q` maximizing single-query TV, then continue optimally for the remaining budget 1 (adaptive second step).

For `k ≥ 3`:

1. Every `bit_j` has single-query TV `1/k > 0 = TV(which)`.  
2. Myopic first query is some `bit_j`.  
3. Optimal continuation after `bit_j` achieves total TV exactly `2/k`.  
4. Optimal unrestricted adaptive TV is 1.  
5. Approximation ratio `1 / (2/k) = k/2` is unbounded.

### Proof sketch of (3)

After `bit_j`:

- obs `0` or `1`: that `1/k` mass is already pure (contributes fully to TV);  
- obs `na`: remaining mass `(k−1)/k` is an identical `(k−1)`-pair problem; with budget 1 left, best TV on that subproblem is `1/(k−1)` relative to submass, i.e. absolute TV contribution `1/k` (one more bit), or `which` alone contributes 0.

Total TV = 1/k + 1/k = 2/k. ∎

**Interpretation:** “Always start with the currently strongest local check” **avoids the gate query forever** and is arbitrarily bad.

---

## Corollary U6 (no fixed nonadaptive checklist dominates adaptive T1)

For every fixed nonadaptive budget `B` and every `ε ∈ (0,1)`, there exists `k > B/ε` such that

$$
D_B^{\mathrm{na}}(P_k,Q_k) = \min\Bigl(1,\frac{B}{k}\Bigr) < ε,
\qquad
D_2(P_k,Q_k) = 1.
$$

So **no fixed-size nonadaptive smell suite** can keep budgeted distinguishability small uniformly over this habitat family, while an adaptive observer with two looks already achieves perfect separation.

---

## Machine checks

```text
research/m5/EXPERIMENTS/enum_core.py
research/m5/EXPERIMENTS/test_m5.py
```

For k=2..12: `D_ad=1`, `D_na=2/k` (k≥2), greedy first=`bit*`, greedy TV=`2/k`.

---

## Prior-art honesty

Related: fixed-horizon active hypothesis testing; adaptive vs nonadaptive experimental design; group-testing style “which then test” geometries; value-of-information for feature acquisition.

**MIRROR residual (if any):** closed-form unbounded family + greedy failure + CHARM product packaging — not the abstract existence of adaptivity gains.

---

## Product scar (CHARM13)

See `PRODUCT_DELTA.md`.
