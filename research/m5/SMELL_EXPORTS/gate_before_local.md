# Smell export sketch — gate before local

**Source:** M5-U k-pair family  
**Status:** sketch only — not merged into `src/charm`

## Idea

When a habitat has many plausible branches (paths, sample IDs, cache buckets), a local magic/header check on one branch is a `bit_j` query. An adaptive T1 asks **which branch is live** first (`which` / list / manifest pointer), then checks that branch.

## Proposed future finding (not implemented)

- code: `checklist_nonadaptive_limit` (info/docs)  
- or relational: `branch_bit_mismatch` if metadata points at path A but payload/header story is only consistent on path B under claimed law  

## Fixture outline

- k directories `branch_0 .. branch_{k-1}`  
- only one “live” according to manifest  
- local headers all “plausible” in isolation  
- distinguisher: read manifest (which), then header of named branch  

## HUNTER note

Any shipped rule must not BLOWN clean adobe_cache habitat audit.
