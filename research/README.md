# Research — CHARM13

Finite-model mathematics for **budgeted habitat indistinguishability** and
honest product doctrine. Detection / oracles / claim validity framing only.
No concealment-from-inspection operations guidance. No T4 claims.

## Start here

| Path | Content |
|------|---------|
| [LADDER_MASTER.md](LADDER_MASTER.md) | Mission index M4–M18 |
| [ladder/](ladder/) | Exact-rational kernel + recursive runners |
| [m4/](m4/) | Adaptive gap certificate + minimality + score hygiene |
| [m5/](m5/) | Unbounded gap at budget 2 |
| [m6/](m6/)–[m18/](m18/) | Envelope, capacity zero, parity, query complexity, doctrine |

## Reproduce

```powershell
cd ladder
python run_ladder.py
python run_ladder_high.py
cd ..\m4\EXPERIMENTS
python test_certificates.py
cd ..\..\m5\EXPERIMENTS
python test_m5.py
```

## Novelty posture

Broad adaptive-versus-nonadaptive phenomena are classical (active hypothesis
testing, costly feature acquisition). Residual contributions are exact closed
forms, finite certificates, assumption hygiene (path-prefix legality), and
**product scars** integrated into CHARM13 docs and smell reporting as of v0.3.4.

## Product mapping

See `../docs/T1_BUDGET.md`. Smell report text and catalog codes
`score_semantics`, `adaptive_t1`, `gate_before_local` carry operator-facing
consequences of the ladder.
