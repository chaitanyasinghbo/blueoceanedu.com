# unused/

Nothing in here is reachable from a page the site serves.

It was found by walking outward from the 18 real entry points — `index.html`,
`start.html`, `next-steps.html`, `method.html`, `results.html`, `fit.html`,
`team.html`, `founder.html`, the four case studies, and the six generated files
in `lp/` and `iblp/` — following every `src`, `href` and `url()` through the
HTML, CSS and JS until nothing new turned up. 290 files are reachable. These 293
are not.

**Paths are preserved.** `unused/admits-green/adya.svg` came from
`admits-green/adya.svg`. To put anything back, move it to the same path with
the `unused/` prefix removed.

## What is in here, and why it is not in use

| | |
| --- | --- |
| `brochure variations/`, `Blue Ocean new assets/` | The brochure project and its brand source files — Neue Haas Grotesk trials, logo vectors, the brand guide PDF, five design directions, the one-pager identities, and the Python that generated them. `brochure.html` and `brochure.css` were already deleted from the repo; this is the rest of it. 560MB of the 573MB here. |
| `admits-green/`, `green-profile-arch/`, `exec-team-pics/`, `hero-logos/`, `exec-team/` | The green theme, superseded folder for folder: `admits-blue/`, `blue-profile-arch/`, `counsel-portraits/`, `alumni-logos/`, `press-logos/`. The names inside are identical, which is why a search for `adya.svg` still finds a hit and the folder looks live. |
| `mock-index.html`, `mockup.html` | Prototypes. Nothing links to them, and they are the only remaining reference to most of the green theme. |
| `email/` | An enquiry email template and its two logos. Not part of the site — **check this one before deleting it**, it may still be pasted into Gmail by hand. |
| `admits-blue/*.svg`, `exec-team-pics-blue/` | Blue-theme variants that were produced but never wired in. The admits wall uses PNGs; the team page uses `counsel-portraits/`. |
| `bocconi.png`, `cambridge.png`, `essec.png`, `manchester.png`, `nyu.png` | Loose copies at the repo root of marks that are used from `uni-logos/`. |
| `Screenshot 2026-04-24 at 10.37.29 AM.png`, `brand/logo-b.svg`, `proof-logos/index.json` | Strays. |

## Also removed, not archived

84 files under `lp/` and `iblp/` that were copies of the folders above, left
from before those two pages were generated. The originals are here, so the
copies were duplicates of an archive. `tools/build-landing-pages.py` no longer
copies any of those folders, so they will not come back.

## Rebuilding this list

```
python3 tools/find-unused.py
```

It prints what is reachable and what is not without moving anything.
