# M5 Seed Theorems

## Status

The statements below are proved inside the frozen finite model. Their literature novelty is unresolved. They are seed results for M5, not public novelty claims.

## 1. Frozen model

Let `W` be a finite world set. Let `P` and `Q` be probability distributions on `W`, and define the zero-sum signed measure

$$
\mu(w)=P(w)-Q(w), \qquad \sum_{w\in W}\mu(w)=0.
$$

A deterministic query is a total map

$$
q:W\to Y_q
$$

with finite output alphabet. Unless a theorem explicitly says otherwise, every query is globally addressable, non-destructive, and has unit cost.

An adaptive budget-`B` policy is a deterministic decision tree of worst-case depth at most `B`. Its internal nodes are queries and its outgoing arcs are query outputs. A nonadaptive budget-`B` policy fixes at most `B` queries before observing any output and receives their joint output.

The final binary decision is post-processing and is not included in the observation transcript.

For a partition `Pi` of `W`, define

$$
V_\mu(\Pi)
  =\frac12\sum_{C\in\Pi}|\mu(C)|,
\qquad
\mu(C)=\sum_{w\in C}\mu(w).
$$

Write `D_B^ad(P,Q)` and `D_B^na(P,Q)` for the optimal adaptive and nonadaptive transcript total-variation values.

The active signed support is

$$
S_\mu=\{w\in W:\mu(w)\ne0\},
\qquad r=|S_\mu|.
$$

Worlds outside `S_mu` may carry equal positive mass under `P` and `Q`; they contribute no signed mass.

---

## 2. Baseline lemmas

### Lemma 2.1 — signed leaf formula

If a deterministic policy induces transcript leaf partition `L`, then

$$
\operatorname{TV}(\operatorname{Law}_P T,
                   \operatorname{Law}_Q T)
 =\frac12\sum_{C\in L}|\mu(C)|.
$$

#### Proof

Every transcript value corresponds to one leaf cell `C`. Its probability under `P` is `P(C)` and under `Q` is `Q(C)`. Applying the finite total-variation formula to the transcript alphabet gives

$$
\frac12\sum_{C\in L}|P(C)-Q(C)|
 =\frac12\sum_{C\in L}|\mu(C)|.
$$

QED.

### Lemma 2.2 — refinement monotonicity

If `Pi'` refines `Pi`, then

$$
V_\mu(\Pi')\ge V_\mu(\Pi).
$$

#### Proof

For each cell `C` of `Pi`, let `C_1,...,C_m` be the cells of `Pi'` inside it. The triangle inequality gives

$$
|\mu(C)|
 =\left|\sum_j\mu(C_j)\right|
 \le\sum_j|\mu(C_j)|.
$$

Sum over `C` and divide by two. QED.

### Lemma 2.3 — deterministic policies suffice

Allowing internal randomization does not increase `D_B^ad` or `D_B^na` in this finite model.

#### Proof

Sample all policy randomness at time zero. Each random seed `u` selects a deterministic policy `pi_u`. Let `rho` be the seed law and let `P_u,Q_u` be the corresponding transcript laws. The randomized transcript laws are the common mixtures

$$
\bar P=\int P_u\,d\rho(u),
\qquad
\bar Q=\int Q_u\,d\rho(u).
$$

Convexity of the `L1` norm yields

$$
\operatorname{TV}(\bar P,\bar Q)
\le\int\operatorname{TV}(P_u,Q_u)\,d\rho(u)
\le\sup_u\operatorname{TV}(P_u,Q_u).
$$

Thus one deterministic component is at least as good as the randomized policy. The reverse inequality is immediate because deterministic policies are a special case. QED.

---

## 3. Exact bridge to weighted classification trees

### Theorem 3.1 — Bayes-error equivalence

Construct a weighted binary classification distribution `M` on `W x {0,1}` by

$$
M(w,0)=\frac12P(w),
\qquad
M(w,1)=\frac12Q(w).
$$

For any policy-induced partition `Pi`, let `R(Pi)` be the minimum classification error obtained by assigning the majority label separately in every cell. Then

$$
V_\mu(\Pi)=1-2R(\Pi).
$$

Consequently,

$$
D_B^{ad}(P,Q)=1-2R_B^{tree},
$$

where `R_B^tree` is the minimum weighted classification error among query decision trees of depth at most `B`; and

$$
D_B^{na}(P,Q)=1-2R_B^{static},
$$

where `R_B^static` is the minimum weighted error after acquiring a fixed set of at most `B` queries and applying the optimal joint-output classifier.

#### Proof

The Bayes error contributed by cell `C` is

$$
\min\{M(C,0),M(C,1)\}
 =\frac12\min\{P(C),Q(C)\}.
$$

Hence

$$
R(\Pi)=\frac12\sum_{C\in\Pi}\min\{P(C),Q(C)\}.
$$

Using

$$
\min(a,b)=\frac{a+b-|a-b|}{2}
$$

and `sum_C(P(C)+Q(C))=2`, we obtain

$$
\sum_C\min\{P(C),Q(C)\}
 =1-\frac12\sum_C|P(C)-Q(C)|
 =1-V_\mu(\Pi).
$$

Therefore `R(Pi)=(1-V_mu(Pi))/2`, which rearranges to the claimed identity. Optimizing over the two policy classes proves the consequences. QED.

### Interpretation

The adaptive half of M4 is an optimal weighted classification-tree problem. The nonadaptive comparator is fixed feature acquisition followed by the optimal classifier. This bridge is a prior-art warning: the generic optimization object belongs to established decision-tree and active-feature-acquisition territory.

---

## 4. Flattening theorem and true support minimality

### Theorem 4.1 — small active support kills adaptivity

Assume globally addressable unit-cost queries. If the active signed support has size

$$
r\le B+1,
$$

then

$$
D_B^{ad}(P,Q)=D_B^{na}(P,Q).
$$

#### Proof

Take any deterministic adaptive policy `T`. Delete every branch containing no active signed world and contract every internal node having only one active child. Neither operation changes the signed leaf value. In the resulting active tree, every internal node has at least two active children.

Let `L` be its number of active leaves and `I` its number of internal query occurrences. Because it is a finite rooted tree with every internal node of active outdegree at least two,

$$
I\le L-1\le r-1.
$$

Let `A` be the set of distinct query labels appearing in this reduced tree. Then

$$
|A|\le I\le r-1\le B.
$$

Ask every query in `A` nonadaptively. We claim that the resulting joint-output partition, restricted to active worlds, refines the leaf partition of `T`.

Indeed, if two active worlds terminate in different leaves of `T`, follow their common policy path until its first divergence. At that node the same query `q in A` is asked of both worlds and returns different outputs. Their joint `A`-output vectors are therefore different.

Thus every nonadaptive cell contains active worlds from at most one adaptive leaf. Worlds with zero signed mass do not affect `V_mu`, so refinement monotonicity gives a nonadaptive value at least that of `T`. Since every nonadaptive policy is also an adaptive policy, equality follows after optimizing. QED.

### Corollary 4.2 — M4 support minimality

At budget `B=2`, a strict adaptivity gap requires at least four active signed worlds. The M4 four-world example therefore has globally minimal active support in the unguarded model. This is stronger than bounded-denominator enumeration.

### Scope warning

The theorem can fail for guarded discovery queries because the static policy may not be legally allowed to ask every query appearing across different adaptive branches. That is an access restriction, not a counterexample to the unguarded theorem.

---

## 5. Sharp two-step adaptivity law

### Theorem 5.1 — root-arity bound

Consider any deterministic adaptive budget-two policy. Suppose its first query has `k` nonempty outcome cells on the active signed support. Then

$$
V(\pi)\le kD_2^{na}(P,Q).
$$

If every available query has at most `K` nonempty active outcomes, then

$$
D_2^{ad}(P,Q)\le K D_2^{na}(P,Q).
$$

#### Proof

Let the first-query cells be `C_1,...,C_k`. In cell `C_i`, the policy either stops or asks a continuation query `q_i`. Let

$$
v_i=\frac12\sum_z|\mu(C_i\cap q_i^{-1}(z))|
$$

with the obvious one-cell interpretation when the policy stops. The adaptive leaf value is

$$
V(\pi)=\sum_{i=1}^k v_i.
$$

Fix branch `i`. The nonadaptive pair consisting of the root query and `q_i` induces exactly the same refinement inside `C_i`. Its contributions from all other root cells are nonnegative. Therefore

$$
D_2^{na}(P,Q)\ge v_i
$$

for every `i`. Hence

$$
D_2^{na}\ge\max_i v_i
\ge\frac1k\sum_i v_i
=\frac1kV(\pi).
$$

Optimize over deterministic adaptive policies, which suffice by Lemma 2.3. QED.

### Corollary 5.2 — additive bound

Under the arity-`K` assumption,

$$
D_2^{ad}-D_2^{na}
\le\left(1-\frac1K\right)D_2^{ad}
\le1-\frac1K.
$$

For binary queries, the universal bounds are

$$
D_2^{ad}\le2D_2^{na},
\qquad
D_2^{ad}-D_2^{na}\le\frac12.
$$

### Theorem 5.3 — the arity bound is exactly sharp

For every integer `K>=2`, there is a finite unit-cost query system of maximum arity `K` such that

$$
D_2^{ad}=1,
\qquad
D_2^{na}=\frac1K.
$$

Therefore the worst possible additive budget-two adaptivity gap under arity at most `K` is exactly

$$
G_2(K)=1-\frac1K.
$$

#### Construction

Let

$$
W_K=\{(i,x):i\in\{1,\ldots,K\},\ x\in\{0,1\}^K\}.
$$

Define

$$
P(i,x)=
\begin{cases}
\frac{1}{K2^{K-1}},&x_i=0,\\
0,&x_i=1,
\end{cases}
$$

and

$$
Q(i,x)=
\begin{cases}
0,&x_i=0,\\
\frac{1}{K2^{K-1}},&x_i=1.
\end{cases}
$$

Use the `K`-ary gate

$$
g(i,x)=i
$$

and binary tests

$$
b_j(i,x)=x_j,
\qquad j=1,\ldots,K.
$$

#### Adaptive value

Ask `g`. If it returns `i`, ask `b_i`. Under `P`, `b_i=0` surely; under `Q`, `b_i=1` surely. The transcript supports are disjoint, so `D_2^ad=1`.

#### Nonadaptive value

A fixed policy can ask at most two queries from `{g,b_1,...,b_K}`.

For `(g,b_j)`, the hypotheses differ only in gate branch `j`, which has probability `1/K`; therefore the total variation is `1/K`.

For distinct `(b_j,b_l)`, direct calculation gives the signed output law

$$
\mu_{j,l}(0,0)=\frac1K,
\qquad
\mu_{j,l}(1,1)=-\frac1K,
\qquad
\mu_{j,l}(0,1)=\mu_{j,l}(1,0)=0.
$$

Its total variation is `1/K`. A single bit query also has value `1/K`, while the gate alone has value zero. Thus `D_2^na=1/K`.

The upper bound in Corollary 5.2 and this construction match. QED.

### Corollary 5.4 — global extremality of the M4 witness

Set `K=2`. Every query in the construction is binary, and

$$
D_2^{ad}=1,
\qquad
D_2^{na}=\frac12.
$$

Therefore the M4 four-world witness reaches the largest additive gap possible for any finite distribution pair and any family of globally addressable binary deterministic queries at budget two. Together with Corollary 4.2, it is both support-minimal and gap-maximal.

This is a mathematical strengthening of M4. It is not yet a literature-novelty claim.

---

## 6. Gain-sensitive support bound

### Proposition 6.1

For a budget-two adaptive policy with root cells `C_i`, define the root-only contribution

$$
b_i=\frac12|\mu(C_i)|,
$$

continuation contribution `v_i`, and gain

$$
g_i=v_i-b_i\ge0.
$$

Let `m` be the number of branches with `g_i>0`. Then

$$
D_2^{na}\ge V_0+\max_i g_i
\ge V_0+\frac{D_2(\pi)-V_0}{m},
$$

where `V_0=sum_i b_i`.

Every gain-bearing branch contains at least one positive and one negative active atom. Consequently,

$$
m\le\min\left\{K,\left\lfloor\frac r2\right\rfloor\right\}.
$$

#### Proof

The nonadaptive pair consisting of the root and branch-`i` continuation preserves the entire root partition, gains `g_i` inside branch `i`, and can only add nonnegative refinement value elsewhere. This proves the first inequality; averaging proves the second.

If all active signed atoms in a root cell have one sign, refinement cannot increase the absolute signed mass of that cell, so its gain is zero. Each positive-gain cell therefore contains both signs and hence at least two active atoms. QED.

### Open extremal problem

Determine the exact support-constrained curve

$$
G_2(K,r)
 =\sup\{D_2^{ad}-D_2^{na}:\text{arity}\le K,\ |S_\mu|\le r\}.
$$

The proposition gives a sharp-looking upper envelope, but matching constructions for every `(K,r)` are not established here.

---

## 7. Four-world butterfly classification

### Theorem 7.1 — unique support-minimal binary extremizer

Assume:

1. the active signed support consists of exactly four worlds;
2. all queries are binary and globally addressable;
3. a depth-two adaptive policy has value `1`;
4. every fixed pair of queries has value at most `1/2`.

Let `g` be the policy's root query, `l` its continuation in root branch zero, and `r` its continuation in root branch one. After applying the natural equivalences below, the active core is exactly

| world | P | Q | g | l | r |
|---|---:|---:|---:|---:|---:|
| A | 1/2 | 0 | 0 | 0 | 0 |
| B | 0 | 1/2 | 0 | 1 | 0 |
| C | 1/2 | 0 | 1 | 0 | 1 |
| D | 0 | 1/2 | 1 | 0 | 0 |

This is the M4 butterfly.

Natural equivalences are: relabeling worlds; swapping `P` and `Q`; swapping root branches together with `l` and `r`; complementing the output of any binary query; and renaming queries.

#### Proof

Because the gap is strict and there are four active worlds, Theorem 4.1's proof forces both root branches to contain at least two active worlds. Hence each contains exactly two.

Adaptive value one means the adaptive transcript laws are disjoint. Therefore `P` and `Q` are mutually singular on active worlds, and each root branch must contain one `P`-world and one `Q`-world; otherwise that branch needs no informative continuation and the adaptive tree can be flattened.

Let the `P` and `Q` masses in branch zero be `p` and `q`. The branch-one masses are `1-p` and `1-q`. The continuation `l` separates the two branch-zero worlds. Thus the fixed pair `(g,l)` has value at least

$$
\frac{p+q}{2}+\frac{|(1-p)-(1-q)|}{2}
=\max(p,q).
$$

Similarly `(g,r)` has value at least

$$
\frac{(1-p)+(1-q)}{2}+\frac{|p-q|}{2}
=1-\min(p,q).
$$

Both are at most `1/2`. Hence `p,q<=1/2` and `p,q>=1/2`, so

$$
p=q=\frac12.
$$

The pair `(g,l)` already obtains value `1/2` from the two singleton cells in branch zero. It may obtain no further value in branch one. Since the branch-one atoms have signed masses `+1/2` and `-1/2`, this forces `l` to give them the same output. Symmetrically, `r` is constant on branch zero.

Complement outputs so that `l(A)=0,l(B)=1` and `r(C)=1,r(D)=0`. Write the off-branch constants as

$$
l(C)=l(D)=c,
\qquad
r(A)=r(B)=d.
$$

If `c` and `d` select a same-sign collision in the joint `(l,r)` outputs, the pair `(l,r)` separates the signed mass with total variation one, contradicting the static bound. Therefore the only admissible geometry is a cross-sign collision. Up to branch swap and output complements this gives `c=d=0`, which is exactly the displayed table. QED.

### Consequence

Within the frozen four-active-world binary model, the M4 pattern is not one example among many unrelated extremizers. Its three-query core is the unique extremal geometry up to the stated symmetries.

The theorem's correctness is separate from whether an equivalent classification already appears in the decision-tree or active-feature literature.

---

## 8. First stability theorem

### Theorem 8.1 — near factor-two equality forces balance and locality

Let a binary-root depth-two adaptive policy have branch contributions `v_0,v_1` and total value

$$
V=v_0+v_1.
$$

Let `N=D_2^{na}(P,Q)`. Suppose

$$
N\le\frac V2+\varepsilon.
$$

Then

$$
|v_0-v_1|\le2\varepsilon.
$$

Moreover, let `e_{1-b}^{(b)}` be the extra signed-partition value created in the opposite root branch when the fixed pair `(g,q_b)` uses branch `b`'s continuation everywhere. Then

$$
e_{1-b}^{(b)}\le2\varepsilon
$$

for `b=0,1`.

#### Proof

The root-arity proof gives `N>=max(v_0,v_1)`. Also

$$
\min(v_0,v_1)=V-\max(v_0,v_1)\ge V-N.
$$

Therefore

$$
|v_0-v_1|
=\max(v_0,v_1)-\min(v_0,v_1)
\le N-(V-N)
=2N-V
\le2\varepsilon.
$$

The fixed pair `(g,q_b)` has value `v_b+e_{1-b}^{(b)}` and is at most `N`. Since

$$
v_b\ge V-N\ge\frac V2-\varepsilon,
$$

we obtain

$$
e_{1-b}^{(b)}\le N-v_b
\le\left(\frac V2+\varepsilon\right)
  -\left(\frac V2-\varepsilon\right)
=2\varepsilon.
$$

QED.

### Interpretation

Near saturation of the factor-two bound cannot be arbitrary. The two adaptive branches must contribute almost equally, and each continuation must create almost no value in the branch where it was not selected. A full distributional stability theorem would additionally quantify distance to the butterfly/extremizer polytope.

---

## 9. Guarded queries: accounting identity

Let `open` denote the globally addressable closure of a guarded query system. Define

$$
G_{info}=D_{open}^{ad}-D_{open}^{na},
$$

$$
G_{access}=D_{open}^{na}-D_{guarded}^{na},
$$

and

$$
G_{guard}=D_{open}^{ad}-D_{guarded}^{ad}.
$$

Then

$$
D_{guarded}^{ad}-D_{guarded}^{na}
=G_{info}+G_{access}-G_{guard}.
$$

This is algebra, not a novelty claim. It prevents discovery restrictions from being mislabeled as informational adaptivity.

---

## 10. Research frontier created by the seed package

The first genuinely difficult targets are now narrow:

1. determine the exact support-constrained curve `G_2(K,r)`;
2. classify all equality cases for `K>2`;
3. prove a quantitative distance-to-extremizer theorem beyond Theorem 8.1;
4. determine the sharp adaptivity law for budgets `B>=3`;
5. locate the complexity boundary for weighted Bayes-error decision trees under prefix/precedence constraints;
6. formalize Theorems 4.1, 5.1, 5.3, and 7.1;
7. complete the primary-source collision audit before using any novelty language.
