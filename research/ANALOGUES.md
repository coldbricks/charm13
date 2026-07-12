# Analogues (non-normative)

Pedagogical correspondences only. They do not extend the theorems and do not
assert results in music theory, mythology, or astrology. The mathematics remains
the finite OPEN model of the seed package.

---

## 1. Cyclic gate / circle of fifths

In the matching construction for $G_2(K)=1-1/K$, the gate

$$
g(i,x)=i,\qquad i\in\\{1,\\\ldots,K\\}
$$

is a **closed cyclic menu** of branches. An adaptive policy of budget two

1. names a degree on the cycle (asks $g$),
2. sounds the local coordinate on that degree (asks $b_i$).

A nonadaptive policy of budget two may fix at most two stations on the cycle and
therefore captures signed mass of order $1/K$.

When $K=12$, the classical circle of fifths supplies a familiar labeling of the
stations. The labeling is mnemonic. The law holds for every integer $K\\\ge 2$.

Figure: `assets/figures/cyclic_gate_ouroboros.png`  
Animation: `assets/figures/anim_cyclic_gate.gif`

**Visual lineage (local only).** User inspiration plates under `assets/inspiration/`
(gitignored): dual-head geometric ouroboros, gold radial wheel, slate void.
Local personal faces under `assets/fonts/` (gitignored binaries; see that README)
may be used when rendering; they are not redistributed with the repository.

---

## 2. Ouroboros (bounds that close on themselves)

The ouroboros is the image of a proof that **eats its own tail**:

- an upper bound $D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}\\\le 1-1/K$,
- a matching construction with $D_2^{\mathrm{ad}}=1$ and $D_2^{\mathrm{na}}=1/K$,

hence

$$
G_2(K)=1-\\\frac1K.
$$

As $K\\\to\\\infty$, the gap tends to $1$: the serpent lengthens and the mouth
approaches the tip of the tail. The figure `ouroboros_gap` plots that approach.

Separately, the product loop `forge → smell → refuse` is a practical cycle, not
a mathematical ouroboros; do not conflate the two.

---

## 3. What these analogues are not

- Not a claim that \(G_2\) is a theorem of music theory.
- Not a claim about astrology, alchemy, or myth as evidence.
- Not a substitute for `SEED_THEOREMS.md` or the rational certificates.
