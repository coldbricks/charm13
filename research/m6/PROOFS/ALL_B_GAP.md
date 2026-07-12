# M6 — Gap_B → 1 for every fixed B ≥ 2

See `research/ladder/kernel.py` closed forms and `research/m6/RESULT.md`.

**Theorem.** On the k-pair family, \(D_B^{\mathrm{ad}}=1\) for all \(B\ge 2\), \(D_B^{\mathrm{na}}=\min(B,k)/k\). Hence for each fixed \(B\ge 2\), \(\mathrm{Gap}_B(k)\to 1\) as \(k\to\infty\).

**Proof idea.** Adaptive: which then bit (budget 2 suffices). Nonadaptive: each bit query contributes mass \(1/k\); `which` alone has TV 0; best B queries pick B distinct bits ⇒ TV \(B/k\) for \(k\ge B\).
