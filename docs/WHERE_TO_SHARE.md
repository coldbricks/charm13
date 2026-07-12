# Where can you put this? (serious answer)

You already have a real home: **GitHub**  
https://github.com/coldbricks/charm13

That is a legitimate place for **code + reproducible research notes**.  
Below are independent venues people use for math/CS-adjacent work, with honesty about fit.

---

## Tier A — respectable & free (good defaults)

| Venue | What it is | Fit for CHARM13 | Catch |
|-------|------------|-----------------|--------|
| **[Zenodo](https://zenodo.org/)** | CERN-backed open archive; **DOI** for a zip of code/paper | **Excellent** for a versioned “research release” of `research/` + PDF note | Uploads are essentially permanent; write carefully first |
| **[OSF](https://osf.io/)** (Open Science Framework) | Project + preprints + files | Good for organizing paper + data + code | Less “math prestige” than arXiv; still legitimate |
| **GitHub Releases** | Tagged source tarball | You should do this anyway (v0.3.4) | Not a DOI by itself (Zenodo can auto-mirror GitHub) |
| **Personal site / GitHub Pages** | Your landing page with charts | Perfect for the “wait wtf” visual story | Not peer review |

**Practical path most independents use:**  
GitHub (source of truth) → Zenodo DOI for a frozen snapshot → optional PDF note.

---

## Tier B — math/CS preprint culture

| Venue | Fit | Catch |
|-------|-----|--------|
| **[arXiv](https://arxiv.org/)** | Gold standard for math/CS/physics preprints | Needs **endorsement** for new authors in a category; moderators reject cranky claims; your work must be framed as *application of sequential testing to a systems model*, not “new encryption theory” |
| **[HAL](https://hal.science/)** | Strong open archive (esp. Europe) | Account setup; good arXiv alternative/complement |
| **Optimization Online** | Only if you recast as optimization | Narrow topical fit |

arXiv is possible **after** a clean short paper with:

- precise theorems (you have them),  
- novelty humility (`KNOWN RESULT, NEW APPLICATION`),  
- no overclaim headlines,  
- reproducible code link.

Without affiliation, arXiv is harder but not impossible (endorsement network / coauthor).

---

## Tier C — use carefully

| Venue | Note |
|-------|------|
| **ResearchGate / Academia.edu** | Social sharing; not a substitute for DOI archives |
| **viXra** | Open to everyone; **reputation is poor** (crank magnet). Avoid as first choice |
| **Random “journals” that email you** | Almost always predatory. Ignore |

---

## What *not* to expect

- Uploading to Zenodo/arXiv ≠ “peer reviewed journal paper.”  
- Specialists will smell novelty inflation instantly; your docket’s honesty is an asset.  
- MathOverflow / MathStackExchange are for **questions**, not dumping a manifesto.  
- Crypto conferences will bounce “camouflage” work that looks operational; frame as **detection / evaluation**.

---

## Recommended next step for you

1. Keep improving the **GitHub landing** (charts, field guide) — done continuously.  
2. Write a **6–10 page technical note** (LaTeX or even Typst): problem, definitions, theorems U1–U6 / M6–M13, product mapping, limitations.  
3. Tag **v0.3.4** on GitHub.  
4. Deposit that tag on **Zenodo** → get a DOI.  
5. Only then consider arXiv (cs.IT / stat.ML / cs.CR *evaluation* framing — pick with care).

---

## Field name to put on a cover page

> Budgeted adaptive hypothesis testing on attributed filesystem habitats,  
> with an engineering system for cover construction and refuse-on-detection.

Or shorter:

> Finite-model adaptive inspection gaps for habitat camouflage evaluation.
