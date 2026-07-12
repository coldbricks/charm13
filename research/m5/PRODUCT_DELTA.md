# M5 PRODUCT DELTA — scars on CHARM13

**North star:** Make the refuse loop harder to fool under adaptive T1, and harder for us to lie about checklist power.

M5 math does **not** ship a new cipher or T4 claim. It changes how we treat **inspection order**, **local vs gate checks**, and **what bench must encode**.

---

## Monday changes (priority order)

### 1. Docs honesty (SHIP now — no code risk)

**Surfaces:** `README.md`, `docs/MASTER.md`, `docs/NATURAL.md` (when owner allows product edit)

**Text to add (substance):**

- A fixed checklist of smell-style checks is a **nonadaptive** observer.  
- An adaptive T1 with the same number of looks can be **arbitrarily stronger** (M5-U: gap → 1 at budget 2).  
- Therefore: **passing a static smell suite does not upper-bound adaptive T1 risk.**  
- Myopic “run the strongest local check first” can be **arbitrarily bad** vs asking a gate/branch question first.

**T-tiers:** T1 clarification. Not T3/T4.

### 2. Catalog / explain (SHIP small)

**Surfaces:** `charm explain` / `catalog.py`

Add conceptual codes (docs-level or info findings later):

| Code sketch | Meaning |
|-------------|---------|
| `adaptive_gap_warning` | (docs) static suite ≠ adaptive T1 |
| `gate_before_local` | (doctrine) list/branch before local magic when structure branches |

### 3. Bench fixtures (SHIP research → product)

**Surfaces:** `charm bench` / `fixtures.py` (later PR)

Add synthetic **k-branch** fixtures where:

- Local per-file checks look fine in isolation  
- Global which-then-bit structure is the real distinguisher  

M5 exports sketches under `SMELL_EXPORTS/` first; product merge after HUNTER games them.

### 4. Smell rule candidates (DEFER implement, SHIP sketch)

From U-family:

- **Gate/branch coherence:** path indicated by metadata vs path that holds the payload bit  
- Prefer **one relational check** over stacking more local mags when fanout grows  

HUNTER must try to game any new rule before merge.

### 5. Forge (DEFER)

No automatic repair from M5 yet (duality not crowned).  
Doctrine only: when forge builds multi-branch habitats, **decoys must not create free which-then-bit separates** against the claimed natural law — research note only until fixtures exist.

---

## Acceptance tests for this delta

- [ ] Docs no longer imply static smell = full T1  
- [ ] RESULT/M5 linked from research README  
- [ ] Product tests still green  
- [ ] No “undetectable under budget B” language  
- [ ] No weight retune presented as M5  

---

## What operators should feel

Before M5: “We have N smell rules; if clean, cover is ok for a quick look.”  
After M5: “Clean under a **fixed** suite is not the same as safe under a **curious adaptive** look with the same budget — especially as the habitat branches.”
