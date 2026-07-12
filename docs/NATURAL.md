# Naturalness

CHARM13 is not a genomics tool. Sequencing packs were an early calibration
fixture because they fail loudly when faked.

**Law:** a cover is blown if it does not look *natural* for the habitat it claims.

## Habitats (templates)

| Habitat | Looks like |
|---------|------------|
| adobe_cache | media cache debris |
| steam_depot | local depot fragment |
| vm_disk | VM files + disk |
| photo_library | managed library store |
| sql_backup | DB dump handoff |
| docker_cache | overlay/layer junk |
| mail_store | mailbox export |
| iso_mirror | install media slice |
| incomplete_download | interrupted transfer |
| wgs_lab | lab pack (optional) |
| generic | untyped bulk |

## Rules of thumb

1. **Magic matches extension** — or the extension is opaque (`.dat`, `.bin`, …).
2. **Size fits the story** — a “cache file” the size of a datacenter is a tell.
3. **Families stay in habitat** — `.cram` does not live next to Steam manifests.
4. **No famous public sample IDs** as decoration.
5. **Checksums match bytes** if you publish checksums.
6. **Gate before local** — if the story has many branches (paths, IDs, buckets),
   the pointer/manifest that says *which* path is live must cohere before local
   magic on one leaf is trusted. Static local stacks miss adaptive “which then
   check” inspections (see `docs/T1_BUDGET.md`).
7. **Local OK ≠ global OK** — every small check can pass while a set-level
   relation (manifest completeness, co-occurrence, parity-style invariants) fails.

There are thousands of file types. We do not enumerate the universe.
We enforce: *claimed type ⇒ checkable nature*, and *claimed habitat ⇒ no foreign specialists*.
