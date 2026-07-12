# CHARM13 Skunkworks

Process doctrine. Same loop as the product:

```text
construct → measure → refuse if blown → patch → re-measure
```

## Roles

| Callsign | Seat | Mission |
|----------|------|---------|
| CHARM13 | Lead / forge | Smallest correct code, tests, dry docs |
| HUNTER | Adversary A | Blow covers and claims (T1 oracle) |
| MIRROR | Adversary B | Blow process, composition, public surface |

Human is final arbiter.

## Round

1. **P0** CHARM13 brief (claim, tier, invariants, what blown looks like)
2. **P1** HUNTER then MIRROR kill pass (≥3 attacks each)
3. **P2** CHARM13 defense (accept / partial / reject → artifact)
4. **P3** Re-hunt residual
5. **Gate** SHIP / DEFER / SCRAP

```text
round_blown = 1 - Π(1 - w_i)   # bad=0.55 warn=0.25 info=0.05
refuse ship if ≥ 0.6 unless human override
```

## Law

- Natural for habitat or BLOWN
- MASTER binds until deliberately revised
- Private help OK; public tree reads human
- No T4 claims
- Cap 4 passes; no theater without fixtures

## Missions (order)

1. Smell calculus stress test
2. Habitat naturalness audit
3. L6 surface + CELLAR honesty

## Grade

- **meh** — talk only
- **solid** — attack closed with test or honesty fix
- **oh def** — new invariant + fixture + re-hunt clean + dry surface

See also: MASTER.md, NATURAL.md.
