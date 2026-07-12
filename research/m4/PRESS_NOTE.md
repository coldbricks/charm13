# Press note — CHARM13 Mission M4 (lay summary)

**STATUS: EMBARGO — DO NOT PUBLISH AS-IS WITHOUT HUMAN OWNER SIGN-OFF**  
**Reason:** External scientist review (2026-07-12) flagged overclaim risk on headlines.  
**Accurate framing only below.**

**For:** general / technical press (when cleared)  
**Project:** CHARM13  
**Mission:** M4 — Budgeted Habitat Indistinguishability  
**Tone:** plain language; no novelty cosplay; no “proves when”

---

## Headline options (approved-tone)

1. **CHARM13 exhibits a minimal finite case where adaptive inspection beats a fixed checklist**  
2. **CHARM13 Mission M4: exact toy certificates for cover-story detection math — not a new cipher**  
3. **Research note: order of inspection can matter; the tool’s “blown score” is not a probability**

### Rejected headlines (do not use)

- ~~“proves when a quick look can still tell real folders from faked ones”~~ — we did **not** characterize *when* in general; we exhibited a tiny exact case  
- ~~“new mathematics of indistinguishability”~~ — broad phenomenon is known  
- ~~“undetectable covers” / anything T4-adjacent~~

---

## The short version (≈150 words)

CHARM13 is not a new encryption algorithm. Encryption already hides the *bytes*. CHARM13 is about the *story* those bytes tell on disk — folder trees meant to look ordinary at a glance.

In Mission M4, the team built small, exact mathematical models of a **budgeted look**: only a few checks, possibly chosen in sequence. They exhibited a **four-situation toy** where a fixed two-check checklist is only half as powerful as an adaptive two-check policy that picks the second check from the first answer — and they proved that, in the simple unguarded model, you need at least four situations for that gap to appear.

They also used math to **kill bad internal stories**: the product’s severity score is not a probability of fakery, and passing every local check does not guarantee global consistency.

No “unbreakable” claims. No new cipher. A modest, correct certificate — and explicit honesty about what is classical versus what is product-specific.

---

## What CHARM13 is (one paragraph)

Think of an encrypted volume as a locked safe. The lock is someone else’s job (for example VeraCrypt). CHARM13 works on the *camouflage around the safe* — the folder names, sizes, companion files, and habitat rules that make a curious tech pause and think “boring project junk” instead of “vault.” The product loop is simple: **build a cover → smell-test it → refuse if it’s blown.**

---

## What Mission M4 set out to do

Earlier versions had habitats, smell rules, and a score that combined warnings. That was engineering.

M4 was a **research mission**: produce something you can reproduce, attack, and either prove or kill — not weight theater and not marketing names for old math.

---

## Who was on the field

| Role | Job |
|------|-----|
| **CHARM13** | Lead construction and math |
| **HUNTER** | Kill claims with smallest counterexamples |
| **MIRROR** | Prior art / “are we renaming something known?” |
| **Human owner** | Final arbiter |
| **External scientist** | Independent read of proof + certificates (2026-07-12) |

---

## What they found (accurate three hits)

### 1. A minimal toy where order matters

In one explicit four-world example with three simple queries:

- Best **fixed** two-check strategy: distinguishing power **½**  
- Best **adaptive** strategy: distinguishing power **1**  
- Gap **½**, with exact arithmetic and machine-checked certificates  

Under the simple model where every query is always allowed, they also **proved** no such gap exists with three or fewer worlds — so the example is size-minimal there.

**Filesystem reading is conditional:** if you must list a directory before you can name a child file, a related gap appears; if paths may be addressed freely, that version of the gap can disappear. The project documents both.

**What this is not:** a general law of “when folders look fake.” It is a **pedagogical minimum case** that forces the product to treat T1 inspection as a *policy*, not only a static checklist. The broad adaptive-vs-nonadaptive idea is already studied in active hypothesis testing and feature acquisition.

### 2. The old score is not a probability (hygiene)

`blown_score` can rank two trees opposite to a simple likelihood-ratio ranking under explicit (P,Q). Combined with the dual gate (any hard “bad” finding blows even when the score is below threshold), this **permanently kills** describing the score as “probability this is generated.”

Valid product discipline — not a deep new theorem of statistics.

### 3. Local OK ≠ globally OK (classical warning label)

Individual local features can match under real vs generated laws while a global relation (classic parity) separates them. Architecture warning for smell rules — classical content, CHARM packaging.

---

## What they did *not* claim

- Not a new encryption algorithm  
- Not a characterization of all adaptive advantages on real disks  
- Not “new adaptive testing theory” without a completed literature review  
- Not lab-proof / T4  
- Not a cookbook for hiding data from investigators  

---

## Pull quotes (safe)

> “We exhibited a minimal finite case where adaptive inspection beats a fixed checklist — and we proved the size lower bound in the simple model.”

> “The score is an engineering monoid, not a probability. That is hygiene, and it stays.”

> “If the press needs a villain, the villain is overconfident cover scores — not mathematics, and not law enforcement.”

---

## Fact box

| Item | Detail |
|------|--------|
| Project | CHARM13 |
| Mission | M4 |
| Flagship | D₂=1 vs D₂^{na}=½ on 4 worlds; gap ½ |
| Minimality | Proved: no gap for ≤3 worlds (unguarded depth-2) |
| Novelty posture | Known phenomenon; exact certificate + CHARM packaging |
| Score / parity | Valid demolition of bad assumptions |
| Formalization | Not yet (Lean etc.) |
| Embargo | Yes until owner clears |

---

## Closing

Mission M4’s real story is not that a model “became Erdős.” It is that a small adversarial process produced a **correct modest result**, named its assumptions, demoted novelty marketing, and invited external kill. That is the product culture CHARM13 wants.

**Do not publish this note without removing the embargo banner and a final human read.**
