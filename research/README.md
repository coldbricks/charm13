# Research — CHARM13

Finite-model theory of **budgeted adaptive inspection** on habitat-shaped query systems: exact capacity envelopes, equality classification, and product scars that change how the tool is detailed. Think stress analysis for inspection budgets — demand vs capacity under named load cases — not theater. Detection / claim-validity framing only. No concealment-from-inspection operations guidance. No T4 claims. No literature-novelty press for the sharp seed package.

## Start here

| Path | Content |
|------|---------|
| **[THEOREMS.md](THEOREMS.md)** | Canonical theorem catalog (notation, crown laws, open problems) |
| [LADDER_MASTER.md](LADDER_MASTER.md) | Mission index M4–M18 |
| [m5/SEED_THEOREMS.md](m5/SEED_THEOREMS.md) | Full analytic seed proofs |
| [m5/RESULT.md](m5/RESULT.md) | Crown status table + correction to habitat packaging |
| [ladder/](ladder/) | Exact-rational kernel + recursive runners |
| [m4/](m4/) | Adaptive gap certificates, minimality, score hygiene |
| [m5/](m5/) | Flattening, \(G_2(K)=1-1/K\), butterfly, \(k\)-pair |
| [m6/](m6/)–[m18/](m18/) | Envelopes, capacity zero, parity, query complexity, doctrine |

## Crown statements (one screen)

\[
r\le B+1 \;\Rightarrow\; D_B^{\mathrm{ad}}=D_B^{\mathrm{na}}
\qquad\text{(OPEN flattening)}
\]

\[
D_2^{\mathrm{ad}}\le K\,D_2^{\mathrm{na}},
\qquad
G_2(K)=\sup\bigl(D_2^{\mathrm{ad}}-D_2^{\mathrm{na}}\bigr)=1-\frac1K
\]

Binary extremizer: M4 four-world butterfly — support-minimal and gap-maximal among OPEN binary queries at budget two (unique up to symmetry).

Habitat closed forms (\(k\)-pair, parity) are **application geometry**, not the sharp universal envelope.

## Reproduce

```powershell
cd ladder
python run_ladder.py
python run_ladder_high.py
cd ..\m4\EXPERIMENTS
python test_certificates.py
cd ..\..\m5\EXPERIMENTS
python test_m5_exact.py
python test_m5.py
```

## Novelty posture

| Layer | Label |
|-------|-------|
| Adaptive > nonadaptive in abstract | Classical |
| M5 sharp seed package | **PROVED — NOVELTY UNRESOLVED** |
| Habitat closed forms + product scars | Known geometry, residual packaging |
| Real-disk warranty / T4 | **Not claimed** |

## Product mapping

See `../docs/T1_BUDGET.md`. Catalog codes `score_semantics`, `adaptive_t1`, `gate_before_local` carry operator-facing consequences of the ladder.
