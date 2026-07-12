# Guarded versus informational adaptivity

## Accounting identity

Let `open` be the globally addressable closure of a guarded query system. Define

\[
G_{\mathrm{info}}=D_{\mathrm{open}}^{\mathrm{ad}}-D_{\mathrm{open}}^{\mathrm{na}},
\qquad
G_{\mathrm{access}}=D_{\mathrm{open}}^{\mathrm{na}}-D_{\mathrm{guarded}}^{\mathrm{na}},
\qquad
G_{\mathrm{guard}}=D_{\mathrm{open}}^{\mathrm{ad}}-D_{\mathrm{guarded}}^{\mathrm{ad}}.
\]

Then

\[
D_{\mathrm{guarded}}^{\mathrm{ad}}-D_{\mathrm{guarded}}^{\mathrm{na}}
=G_{\mathrm{info}}+G_{\mathrm{access}}-G_{\mathrm{guard}}.
\]

This is algebra. It prevents discovery restrictions from being mislabeled as informational adaptivity.

## Scope

- Flattening (Theorem 4.1) and the sharp arity law are proved in the **OPEN** model.  
- Guarded systems may force static policies to include predecessors, changing legality of the flattening argument.  
- No real-world evasion compilation is derived from this identity.

## Open

Nontrivial compilation theorems under rooted-prefix guards (abstract decision-tree form only).
