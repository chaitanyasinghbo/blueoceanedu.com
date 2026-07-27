# Blue Ocean Education — Brand

## Core Positioning

Blue Ocean Education helps create India's most unique student profiles. We are a student talent-development and global admissions company for hardworking, ambitious Indian students in Grades 9 to 12 who want to compete for the world's best universities.

Our belief is simple: the strongest admissions outcomes come from genuine development.

We do not believe in robotic consulting, generic extracurricular lists, fake profile-building, or last-minute application packaging. We help students develop holistically and deeply, so they become more intellectually alive, more skilled, more empathetic, more articulate, and more capable of doing meaningful work in the world. Admissions become the result of that transformation.

## What We Are Not

- A generic counseling service
- An essay-editing shop
- A shortcut to guaranteed admissions
- A mass-market, template-based operation
- For students who will not work

## One-Line Brand

Blue Ocean Education helps hardworking Indian students build the most unique profiles in the country, so they can become globally competitive for Harvard, Yale, Oxford, Cambridge, and the world's best universities.

## The Core Belief

When students are developed to the height of their potential, admissions follow.

---

## Voice

Three words: **earned, rigorous, rare.**

Physical object: a letter from a Harvard admissions office, a competitive exam notice in an elite school hallway, a serious academic monograph from the 1960s. Authoritative, warm, precise.

**Confident, not boastful.** Let outcomes speak. Avoid superlatives without evidence.

**Direct, not vague.** "4 to 7 times more likely to be admitted" beats "dramatically improved chances."

**Personal, not institutional.** Write like a trusted advisor, not a brochure.

**Premium through restraint.** The quality signal comes from precision and selectivity, not from adjectives.

### Words to avoid
holistic, passionate, dedicated, committed, transformative, best-in-class, end-to-end, journey, seamless, empowering, tailored, bespoke, curated, comprehensive

### Rules
- No em dashes
- No mid-sentence colons used rhetorically
- No "it is not X, it is Y" pivots
- No AI-sounding filler
- No emojis

---

## Ocean Ember (Brand Guidelines v1.0, July 2026)

The identity below is the new brand system, delivered as `Blue Ocean new assets/Blue Ocean Brand Guide.pdf`. It is live across the whole site, carried by `ocean-ember.css`. The visual identity documented further down is what it replaced, kept for reference only. Do not mix the two.

The voice does not change under Ocean Ember. Everything in the Voice section above still holds.

### The name

`Blue Ocean Education Consulting` is the full name and appears in the logo lockup, legal documents, and letterheads. In prose, write `Blue Ocean Education` on first mention and `Blue Ocean` after that. Never write BOE where a family can see it.

### The six colours

| Colour | Hex | Job |
|---|---|---|
| Core | `#243747` | The anchor. Covers, the mark, headings, dark grounds |
| Support | `#5089B5` | The second voice. Charts, links, secondary panels |
| Signal | `#E0600E` | The accent. The action, the number that matters |
| Surface | `#E5DED3` | The paper. Default background for everything |
| Ink | `#13171B` | Body copy. Always Ink on Surface |
| Highlight | `#F49904` | Chart fills and highlights, never text |

Surface carries the page, Core anchors it, Signal stays rare. Trusted pairs: Ink on Surface at 13.5:1, headings and the mark at 9.2:1, reversed panels at 9.2:1, Ink on Highlight at 8.1:1. Signal on Surface is 2.7:1, so it is allowed only at 18px bold and up, or as a graphic.

On the site, Signal carries three things and nothing else: the primary button, the accented word in a display headline, and the single key number. Support and its light tints carry every other accent, including labels on Core and the qualifying checkmarks.

### Third-party marks

Two walls on the site are built from other organisations' logos, and they take opposite treatments on purpose.

The **admits wall** gives each university its own colour, because thirty different colours are the point: the wall reads as thirty separate institutions before a single name is read.

The **press strip** and the **alumni strip** give every mark the same ground, Core, with the mark knocked out in white. Eight mastheads in eight brand colours read as a banner ad, not as coverage, and the same is true of five university marks in five. One ground, one mark colour, no exceptions.

The rule that separates them: **borrowed colour is allowed only where the count is the claim.** Everywhere else a third-party mark appears, it sets in one colour on a Blue Ocean ground. This is why the counsel wall carries Harvard crimson (the claim is that all seven are Harvard alumni) and why `.team-li-btn` gave up LinkedIn's blue.

**Signal never carries a data series.** Charts, diagram fills, and stat rows use Core, Support, its tints, and Highlight. This is the rule that keeps a page from reading as orange: the moment two figures in one panel are Signal, neither is an accent.

`.proof-stat-card strong` is the one Signal figure on the results pages, and there is exactly one such card (`6x`). If that stack ever grows, Signal has to be scoped to the headline figure and the rest moved to Support, or four orange numbers turn the accent into the background.

### Type

Neue Haas Grotesk, two cuts. Display for 20px and up, Text below 20px. Display never goes below 20px. Light weights never go below 14px. Body copy is sentence case, never longer than about 65 characters a line. Caps are for labels only. The Round cuts stay unused.

The 20px floor is not a preference. Display at 13px sitting beside Text at 14px reads as two unrelated typefaces on the same line, which is how a stale font gets noticed. Any heading under 20px becomes a label in Text, not a small Display heading.

Labels are Text Bold, uppercase, tracked. Weight is what gives a label presence on a dark ground. Lightening the colour alone leaves it thin and recessive even when the contrast ratio passes.

Fallback when Haas is not installed: Arial, or Helvetica Neue on a Mac. Nothing else.

The Neue Haas files in `fonts/` are trial versions. Buy the Display and Text licences before anything public ships.

### The mark

Three versions. The lockup is the default for websites. The BO mark is for square and social spaces where the name is already nearby. The B is for avatars, favicons, and app icons.

The mark sets in one colour at a time, solid, never outlined, rotated, stretched, shadowed, or recoloured to Signal or Highlight. Both counters stay open, because the counters carry the two stories: a student in profile under a whale tail in the B, and the whale in the O. Clear space is at least half the O's height on every side. On photographs, place it on a solid panel first.

Minimum sizes: lockup 120px, BO mark 36px, B 24px.

### What Ocean Ember retires

EB Garamond, Bricolage Grotesque, the italic serif display voice, the large italic eyebrow, oklch brand tokens, the green and blue theme toggle, and the circle-and-triangle placeholder mark.

## Visual Identity

| Token | Value |
|---|---|
| Ink (deepest) | `oklch(16% 0.022 218)` |
| Ink mid | `oklch(42% 0.020 218)` |
| Ink soft | `oklch(55% 0.018 218)` |
| Cream (bg) | `oklch(96.5% 0.01 78)` |
| Cream alt | `oklch(93% 0.013 78)` |
| Blue (brand) | `oklch(46% 0.130 218)` |
| Blue dark | `oklch(22% 0.090 218)` |
| Blue pale | `oklch(91% 0.040 218)` |
| Amber accent | `oklch(72% 0.14 75)` |
| Rule | `oklch(87% 0.014 78)` |

**Color strategy:** Committed. Deep navy blue carries the brand sections. Warm cream is the ground. All brand colors use hue 218 (true blue, not teal).

**Spot illustrations and icons:** Thin-stroke SVG icons (`stroke-width: 1.75`, `fill: none`, `stroke-linecap: round`) used in three ways:
- Wave mark (`nav-logo-mark`): teal wave beside the nav logo
- Section ornament (`manifesto-mark`): three-wave line above the manifesto blockquote
- Pillar icons (`arch-icon`): 16×16 thematic icons stacked under the pillar number in the architecture grid
- List icons (`serve-icon`): checkmarks (yes list) and X marks (no list) replacing CSS dots
- Grade icons (`prog-icon`): 11×11 inline icons within program grade labels

**Typefaces**
- Display: `EB Garamond` (Google Fonts, serif, italic for hero moments; wght 400-800 variable)
- UI / body: `Bricolage Grotesque` (Google Fonts, variable, wght 300-700)

**What was retired:** Gloock (too fashion-editorial), Plus Jakarta Sans, Libre Baskerville, hex color vars, navy + gold palette.

**Layout**
- Max width: 1280px
- Padding: `clamp(20px, 4vw, 48px)`
- Section rhythm: generous and varied, not uniform
