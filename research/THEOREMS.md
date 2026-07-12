# Theorem catalog

This catalog records the statements proved in the CHARM13 finite-model ladder (missions M4–M18). It is intended as a reference sheet for the notes, not as a survey of the sequential-testing literature.

**Status.** Each statement is relative to the frozen model named in its section. The M5 sharp seed package is proved in that model; its novelty with respect to prior literature is unresolved. That adaptivity can improve upon nonadaptive experiments in the abstract is classical. Residual items collected here: exact envelopes, equality classification, rational certificates, assumption hygiene, and engineering corollaries.

**Notation.** Finite world set $W$. Distributions $P,Q$ on $W$. Signed measure $\mu=P-Q$ with $\sum_w\mu(w)=0$. Active support $S_\mu=\\{w:\mu(w)\ne0\\}$, $r=|S_\mu|$. A query is a total map $q:W\to Y_q$ of finite alphabet. Unless marked otherwise, queries are **OPEN**: globally addressable, non-destructive, unit cost. Adaptive budget-$B$ policies are deterministic decision trees of depth $\le B$. Nonadaptive budget-$B$ policies fix $\le B$ queries before any observation. Objectives:

$$
D_B^{\mathrm{ad}}(P,Q)=\sup_{\pi\in\mathrm{Ad}_B}\mathrm{TV}(\mathrm{Law}_P T_\pi,\mathrm{Law}_Q T_\pi),
\qquad
D_B^{\mathrm{na}}(P,Q)=\sup_{\sigma\in\mathrm{Na}_B}\mathrm{TV}(\mathrm{Law}_P T_\sigma,\mathrm{Law}_Q T_\sigma).
$$

Leaf formula: if $\Pi$ is the transcript partition of $W$, then $\mathrm{TV}=\tfrac12\sum_{C\in\Pi}|\mu(C)|$. Write $V_\mu(\Pi)$ for that quantity.

---

## A. Baseline identities (known / classical)

### A.1 Signed leaf formula
For any deterministic policy inducing leaf partition $\Pi$,
$$
\mathrm{TV}(\mathrm{Law}_P T,\mathrm{Law}_Q T)=V_\mu(\Pi).
$$

### A.2 Refinement monotonicity
If $\Pi'$ refines $\Pi$, then $V_\mu(\Pi')\ge V_\mu(\Pi)$.

### A.3 Deterministic policies suffice
Internal randomization does not increase $D_B^{\mathrm{ad}}$ or $D_B^{\mathrm{na}}$ in this finite model (convexity of $\\|\cdot\\|_1$).

### A.4 Bayes-error bridge
With $M(w,0)=\tfrac12 P(w)$, $M(w,1)=\tfrac12 Q(w)$,
$$
V_\mu(\Pi)=1-2R(\Pi),
$$
where $R(\Pi)$ is majority-label Bayes error on cells of $\Pi$. Thus adaptive inspection is weighted classification-tree error at depth $B$; nonadaptive inspection is fixed feature acquisition then optimal classification. **Prior-art warning:** the optimization object is classical.

---

## B. Flattening and support minimality (M5 seed)

### B.1 Flattening theorem
Assume OPEN unit-cost queries. If $r\le B+1$, then
$$
D_B^{\mathrm{ad}}(P,Q)=D_B^{\mathrm{na}}(P,Q).
$$
**Idea.** Reduce an adaptive tree to active worlds; every internal node has active outdegree $\ge 2$, so the number of internal nodes satisfies $I\le r-1\le B$. Ask those query labels nonadaptively: joint outputs refine adaptive leaves on $S_\mu$.

**Scope.** Can fail for guarded discovery queries (legality of asking a query depends on path history). That is access restriction, not a counterexample to OPEN flattening.

### B.2 Support minimality at budget two
A strict adaptivity gap at $B=2$ in the OPEN model requires $r\ge 4$. The M4 four-world butterfly is therefore **support-minimal**.

---

## C. Sharp budget-two envelope (M5 crown)

### C.1 Root-arity bound
Let a depth-two adaptive policy open with a query whose active outcome cells are $C_1,\ldots,C_k$. Write $V(\pi)=\sum_i v_i$ for branch contributions after optimal continuations. Then for each $i$,
$$
D_2^{\mathrm{na}}(P,Q)\ge v_i,
$$
hence $V(\pi)\le k\\,D_2^{\mathrm{na}}$. If every available query has active arity $\le K$,
$$
D_2^{\mathrm{ad}}\le K\\,D_2^{\mathrm{na}}.
$$

### C.2 Additive corollary
$$
D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}\le\Bigl(1-\frac1K\Bigr)D_2^{\mathrm{ad}}\le 1-\frac1K.
$$
Binary case $K=2$: $D_2^{\mathrm{ad}}\le 2D_2^{\mathrm{na}}$ and additive gap $\le 1/2$.

### C.3 Sharpness — exact extremal constant
For every integer $K\ge 2$ there exists a finite OPEN query system of maximum arity $K$ with
$$
D_2^{\mathrm{ad}}=1,\qquad D_2^{\mathrm{na}}=\frac1K.
$$
Therefore
$$
\boxed{G_2(K)\\,:=\\,\sup\bigl(D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}\bigr)\\,=\\,1-\frac1K.}
$$
**Matching construction (address family).** Worlds $(i,x)$ with $i\in\\{1,\ldots,K\\}$, $x\in\\{0,1\\}^K$; gate $g(i,x)=i$; bits $b_j(i,x)=x_j$; $P$ and $Q$ mutually singular on the coordinate $x_i$. Adaptive: ask $g$ then $b_i$. Nonadaptive: any fixed pair yields TV $=1/K$.

### C.4 Binary extremizer uniqueness
Under four active worlds, binary OPEN queries, adaptive value $1$, and every fixed pair $\le 1/2$, the three-query core is unique up to natural symmetries and coincides with the **M4 butterfly**. Thus that witness is simultaneously **support-minimal** and **gap-maximal** among binary OPEN queries at budget two.

### C.5 First stability statement
Near factor-two equality forces branch balance and locality of continuation value (quantitative $\varepsilon$-control on $|v_0-v_1|$ and off-branch leakage). See `m5/SEED_THEOREMS.md` §8.

**Status label for B–C:** `PROVED — NOVELTY UNRESOLVED`.

---

## D. Habitat families (application geometry)

These are **closed-form models of filesystem-shaped query structure**, not replacements for the sharp $G_2(K)$ law.

### D.1 $k$-pair family (which-then-bit)
Uniform random branch $J\in\\{1,\ldots,k\\}$. Under $H_0$ vs $H_1$, the payload bit on branch $J$ differs; off-branch bits return $\mathtt{na}$.

| Budget | $D_B^{\mathrm{ad}}$ | $D_B^{\mathrm{na}}$ |
|--------|------------------------|------------------------|
| $0$ | $0$ | $0$ |
| $1$ | $1/k$ | $1/k$ |
| $\ge 2$ | $1$ | $\min(B,k)/k$ |

Gap at $B=2$: $1-2/k\to 1$ as $k\to\infty$. **Not** the sharp universal $1-1/K$ construction (gate arity $k$ yields habitat gap $1-2/k$).

### D.2 Myopic greedy failure
Local-first myopic policy never opens with the branch query; approximation ratio vs optimal adaptive is $k/2\to\infty$.

### D.3 All-$B$ envelope
For every fixed $B\ge 2$ on the $k$-pair family,
$$
\mathrm{Gap}_B(k)=1-\frac{\min(B,k)}{k}\to 1\quad(k\to\infty).
$$
A fixed-size checklist cannot uniformly dominate adaptive risk across branching factors.

### D.4 Adaptive capacity zero
On the $k$-pair family with $B\ge 2$, adaptive advantage is $1$ for every $k$. Capacity for $\varepsilon$-indistinguishability under that adaptive class is **zero** for all $\varepsilon<1$. Large $k$ helps checklists; it does not help against which-then-bit.

### D.5 Parity payloads
Local bit marginals matched; global parity differs per branch. Perfect adaptive separation: budget $B^\star_{\mathrm{ad}}=1+m$. Perfect nonadaptive separation: $B^\star_{\mathrm{na}}=k\cdot m$. Ratio $km/(m+1)\to\infty$.

### D.6 Query-complexity form
Constant TV advantage: nonadaptive $\Omega(k)$ vs adaptive $O(1)$ on the stated families (M16).

### D.7 Nesting
$k$-pair is the parity family at $m=1$ (M14).

**Status label for D:** `PROVED` as closed forms on named families; product mapping `KNOWN RESULT, NEW APPLICATION`.

---

## E. Score / oracle hygiene (product mathematics)

### E.1 Severity monoid is not Bayes
$S=1-\prod_i(1-w_{\mathrm{sev}(i)})$ with ordinal weights is a commutative monoid, not a likelihood or posterior. Explicit synthetic reversals exist between score rank and likelihood-ratio rank (M4-B, M15).

### E.2 Dual refuse gate
$$
\mathrm{refused}=(\exists\\,\mathrm{bad})\ \lor\ (S\ge 0.6).
$$
One bad finding alone scores $0.55$ and still refuses.

### E.3 Static smell vs adaptive T1
Smell is a deterministic nonadaptive checklist. Finite models show that clean static smell is **necessary machinery**, not a certificate against every adaptive policy of similar look length.

---

## F. Open problems (honest frontier)

1. Exact support-constrained curve $G_2(K,r)$ for all arity/support pairs.  
2. Equality classification for $K>2$.  
3. Quantitative metric stability beyond the first $\varepsilon$-statement.  
4. Sharp $G_B(K)$ for $B\ge 3$.  
5. Guarded-vs-OPEN compilation theorems (path-prefix legality).  
6. Lean formalization of B.1–C.4.  
7. Completed primary-source collision matrix for residual novelty language.

---

## G. Machine certificates

| Package | Command | Asserts |
|---------|---------|---------|
| Sharp $G_2(K)$ | `python research/m5/EXPERIMENTS/test_m5_exact.py` | $K=2..7$: $\mathrm{ad}=1$, $\mathrm{na}=1/K$; butterfly cores |
| $k$-pair | `python research/m5/EXPERIMENTS/test_m5.py` | closed forms + greedy ratio |
| Ladder M4–M18 | `python research/ladder/run_ladder.py` | exact rationals / envelopes |
| High ladder | `python research/ladder/run_ladder_high.py` | parity / QC / doctrine pack |
| M4 witnesses | `python research/m4/EXPERIMENTS/test_certificates.py` | adaptive gap certificates |

Full proofs: `m5/SEED_THEOREMS.md`, `m5/PROOFS/`, `m4/PROOFS/`, mission `RESULT.md` files. Index: `LADDER_MASTER.md`.

---

## H. What is deliberately not claimed

- Literature novelty of $G_2(K)=1-1/K$ or butterfly uniqueness.  
- New statistical distance, new cipher, or T4 laboratory hardness.  
- That real disks equal either extremal family.  
- That `blown_score` is $\mathbb{P}(\text{forged})$.  
- Operational guidance for concealing material from forensic process.

The mathematics is finite, falsifiable, and intentionally cold. The product inherits scars from the theorems, not the reverse.
