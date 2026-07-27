# Blue Ocean Education: five identity directions

Five original, one-page enterprise identity explorations built from the strategy and proof in the existing Blue Ocean Education brochure. These are identity systems, not recoloured brochure themes.

## Start here

- [Combined five-direction PDF](output/Blue-Ocean-Five-Identity-Directions.pdf)
- [Interactive / printable HTML](index.html)
- [Strategic product brief](../PRODUCT.md)

Each direction also has its own PDF, print-matched PNG preview, and editable SVG logo lockup in the `output/` and `logos/` folders.

## Direction summary

| No. | Direction | Strategic lens | Best when | Watch-out |
|---|---|---|---|---|
| 01 | Long Horizon | Multi-year navigation and calm institutional confidence | The brand should feel like a precise, enduring private advisory | It retains a light directional metaphor, so it is evolution rather than total rejection of the current compass idea |
| 02 | Field Notes | Founder-led scholarship, authentic student work, and close reading | Human trust, intellectual depth, and “serious work, done properly” should lead | Requires disciplined access to real artifacts and candid photography |
| 03 | Proof Standard | Evidence, measurement, documented process, and operational rigor | Blue Ocean wants maximum differentiation from coaching and luxury-consulting clichés | The system must be warmed by people and student work in longer applications |
| 04 | Open Futures | Student agency, optimism, growth, and kinetic digital expression | The brand needs to connect strongly with students while staying premium | High-energy colour needs firm governance in formal parent and legal communications |
| 05 | Delhi Modern | Indian origin, global fluency, and architectural cultural confidence | Blue Ocean wants the most ownable and geographically rooted story | Expressive geometry and palette should be production-tested across photography and print |

## What each board includes

- Strategic idea and brand posture
- Original primary mark and wordmark behavior
- Five-colour working palette with HEX values
- Display, reading, and utility typography direction
- Graphic language or pattern system
- Voice attributes and a live headline
- Example application behavior
- Clear-space / minimum-size cue and trademark note

## Canonical files

The PDFs are the visual source of truth for review and office printing. The PNG previews are rendered directly from those PDFs at 144 DPI, so they match the print output. The HTML is the editable source.

The HTML bundles the selected open-licensed typefaces locally, so exact rendering works offline. The individual SIL Open Font License files are included in `assets/fonts/licenses/`. The exported PDFs also retain their rendered typography and have no external dependency.

## Production notes

- Format: A4 landscape, 297 × 210 mm
- Digital master: RGB
- Colour values: working exploration values, not final press specifications
- Before launch: select one direction, conduct trademark and similarity clearance, draw the final wordmark as outlines, define full lockup and monochrome suites, test accessibility, and specify CMYK / spot-colour conversions with physical proofs
- Safe contrast pairings:
  - Long Horizon: Abyss on Air or Signal, Air on Abyss
  - Field Notes: Carbon on Paper or Leaf, Paper on Carbon or Margin Blue; Red Pencil is an accent
  - Proof Standard: Graphite on Fog, Verify, or Flag; Fog on Graphite or Data
  - Open Futures: Ink on Sun, Coral, or Chalk; Chalk on Cobalt or Ink
  - Delhi Modern: Jamun on Stone or Haldi; Stone on Jamun or Indigo

## Brand governance items discovered in the source

Resolve these before rollout:

1. Choose the official brand form: `Blue Ocean Education`, `Blue Ocean Education Consulting`, or `Blue Ocean Education Consultants`.
2. Standardise Dr. Sanjay Kumar’s public title.
3. Reconcile the two website domains, email addresses, and phone numbers currently used across the brochure and founder page.
4. Approve a claim ledger with denominator, time period, source, and required qualifier for every admissions outcome.
5. Keep university and Harvard marks as third-party proof assets, never as components of the Blue Ocean logo.

## Re-rendering

Run:

```bash
./render.sh
```

This uses local Google Chrome to generate the combined and individual PDFs, then Poppler to produce matching PNG previews.
