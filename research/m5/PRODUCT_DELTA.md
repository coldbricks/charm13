# M5 PRODUCT DELTA — scars on CHARM13

**North star:** Make the refuse loop harder to fool under adaptive T1, and harder for us to lie about checklist power.

M5 math does **not** ship a new cipher or T4 claim. It changes how we treat **inspection order**, **local vs gate checks**, **sharp finite envelopes**, and **what bench must encode**.

---

## Mathematical packaging (binding for docs)

| Fact | Use in product language |
|------|-------------------------|
| \(G_2(K)=1-1/K\) | Sharp universal budget-2 gap under active arity \(\le K\) |
| Binary case gap \(\le 1/2\) | M4 witness is gap-maximal among binary OPEN queries |
| Flattening \(r\le B+1\) | Small signed support cannot create OPEN adaptivity gaps |
| k-pair \(D_{\mathrm{na}}=2/k\) | Habitat / branching story; greedy “local first” failure |
| Static smell | Nonadaptive observer — not adaptive T1 |

Do **not** present \(2/k\) as the universal extremal constant. Prefer:

- “On an explicit branching habitat, gap \(1-2/k\to 1\)” for operator narrative.  
- “Under arity-\(K\) queries the sharp additive envelope is \(1-1/K\)” for research accuracy.

---

## Monday changes (priority order)

### 1. Docs honesty (SHIP)

**Surfaces:** `README.md`, `docs/T1_BUDGET.md`, `docs/MASTER.md`, `docs/FIELD_GUIDE.md`, `research/LADDER_MASTER.md`

**Substance:**

- A fixed checklist of smell-style checks is a **nonadaptive** observer.  
- An adaptive T1 with the same number of looks can be **arbitrarily stronger** as branching / arity grows.  
- **Passing a static smell suite does not upper-bound adaptive T1 risk.**  
- Myopic “run the strongest local check first” can be **arbitrarily bad** vs asking a gate/branch question first.  
- Sharp finite law: \(G_2(K)=1-1/K\) (proved in-model; novelty unresolved).

**T-tiers:** T1 clarification. Not T3/T4.

### 2. Catalog / explain (SHIP)

Codes already present: `adaptive_t1`, `gate_before_local`, `score_semantics`. Keep doctrine aligned with the dual packaging (sharp law + k-pair habitat).

### 3. Bench fixtures (DEFER implement)

Synthetic **k-branch** fixtures where local per-file checks look fine but which-then-bit is the distinguisher. Sketches: `SMELL_EXPORTS/`.

### 4. Smell rule candidates (DEFER)

Gate/branch coherence; prefer one relational check over stacking local mags when fanout grows. HUNTER must game any new rule before merge.

### 5. Forge (DEFER)

No automatic repair from M5. Doctrine only until fixtures exist.

---

## Acceptance tests for this delta

- [x] Docs distinguish sharp \(1-1/K\) vs k-pair \(2/k\)  
- [x] RESULT/M5 linked from research README  
- [ ] Product tests still green (run at ship)  
- [x] No “undetectable under budget B” language  
- [x] No weight retune presented as M5  
- [x] Novelty unresolved language held  

---

## What operators should feel

Before M5: “We have N smell rules; if clean, cover is ok for a quick look.”  
After M5: “Clean under a **fixed** suite is not the same as safe under a **curious adaptive** look with the same budget — especially as the habitat branches. The math even has a sharp finite envelope under arity constraints.”
