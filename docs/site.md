# Blue Ocean Education — Site Architecture and Conventions

## Stack

Multi-page static site. Working file: `mock.html` (landing page). Sub-pages: `method.html`, `results.html`, `fit.html`, `team.html`. Shared CSS lives in `main.css` (linked by all pages). Shared scroll behavior in `scroll-story.js`. No build system, no framework, Google Fonts only.

---

## Page Structure

### Landing page (`mock.html`)

Overview / scrollable summary of all content areas. Nav links go to sub-pages.

1. **Nav** — sticky, cream bg, logo left, links center (hidden mobile), phone + CTA right, hamburger on mobile. Logo links back to `mock.html`. Nav links: `method.html`, `results.html`, `fit.html`, `team.html`.
2. **Hero** — cream bg, full viewport height, italic EB Garamond h1, student photo right, press ticker at bottom
3. **Results / Numbers** — acceptance rate stats, 6x figure, bar chart. Section id: `results`
4. **Profile Architecture** — dark bg, 7-pillar sticky-left scrolling layout. Section id: `method`
5. **Outcomes carousel** — student admit cards with photos and badge grid. Section id: `outcomes`
6. **Team** — founder + advisory council with photos and credential badges. Section id: `team`
7. **Universities** — chip grid with favicons showing where students were admitted
8. **Right Fit** — dark bg, two-col for/not-for lists. Section id: `fit`
9. **CTA** — dark bg, email + phone actions
10. **Footer** — 4-col grid with nav links to all sub-pages
11. **Sticky CTA bar** — fixed bottom, hidden until hero exits viewport

### `method.html` — The Method

1. Page header (eyebrow + h1 + subtitle)
2. Philosophy / Core Belief (`id="about"`) — the "Most admissions companies start with the application" section
3. Profile Architecture (full 7-pillar sticky-left layout, `id="method"`)
4. Programs (`id="programs"`) — 4 tracks with tab navigation (Early Architecture, Strategic Build, Final Year, Masters/MBA)
5. CTA, Footer, Sticky CTA bar

### `results.html` — Results

1. Page header
2. Numbers proof (`id="results"`) — 6x stat + acceptance chart
3. Outcomes carousel (`id="outcomes"`) — student cards
4. Student Stories (`id="stories"`) — grid of 4 case studies with photos and links
5. Universities chip grid
6. CTA, Footer, Sticky CTA bar

### `fit.html` — Right Fit

1. Page header
2. Right Fit / Selective by design (`id="fit"`)
3. CTA, Footer, Sticky CTA bar

### `start.html` — Request a Consultation (CTA landing page)

All "Get Started" and primary hero CTA buttons link here.

1. Compact hero (dark bg, grid pattern): eyebrow + h1 "Work 1-1 with our team." + lede + 3 stat chips. Right col: 2-step form card embedded directly in the hero grid.
2. Form card — Step 1: role toggle (Student / Guardian), First Name, Last Name, Email, Continue →
3. Form card — Step 2: Phone (+91 prefix), Grade / Graduation Year, School Name, Pincode, Scholarship dropdown, Back / Request Consultation, privacy note
4. Form card — Success state: replaces card content on submit
5. "What to expect" section (cream-low bg, 3-col): Honest assessment, Gap analysis, What engagement looks like
6. CTA section (dark): phone + email actions
7. Footer (same as other pages)
8. No sticky CTA bar (this page IS the CTA destination)

Form step transition: titles animate with `out` class (translateX + opacity). Steps use `hidden-step` + `fade-in` CSS classes.

### `team.html` — Team

1. Page header
2. Team section (`id="team"`) — founder + advisory council
3. Quote band — Ritu Verma parent testimonial
4. CTA, Footer, Sticky CTA bar

---

## Design Conventions

### Colors

All colors use OKLCH. Never use hex or rgb for brand colors.

```
--ink:       oklch(16% 0.022 218)   deep navy (almost black)
--ink-500:   oklch(42% 0.020 218)   body text
--ink-400:   oklch(55% 0.018 218)   secondary text
--cream:     oklch(96.5% 0.01 78)   main background
--cream-100: oklch(93% 0.013 78)    alternate section background
--teal:      oklch(46% 0.130 218)   brand blue, links, CTAs
--teal-900:  oklch(22% 0.090 218)   dark sections: manifesto, arch, team, cta, footer
--teal-50:   oklch(95% 0.020 218)   pale blue tint for chips, hover states
--amber:     oklch(72% 0.14 75)     rare accent (sticky bar CTA only)
--rule:      oklch(87% 0.014 78)    borders on cream sections
--rule-dark: oklch(32% 0.018 218)   borders on dark sections
```

All hues use 218 (true blue). The `--teal` variable is retained as the CSS custom property name for compatibility but now renders as blue, not teal.

### Typography

- **Display headings (h1):** `font-family: var(--serif); font-style: italic` — Gloock italic. Hero and manifesto only.
- **Section headings (h2, h3):** `font-family: var(--serif); font-weight: 400` — Gloock regular.
- **Everything else:** `font-family: var(--sans)` — Bricolage Grotesque variable.
- **Eyebrow labels:** `font-size: 11px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: var(--teal)`
- **Body copy line length:** max 65-75ch.

### Layout

- Max width: `1280px`
- Horizontal padding: `clamp(20px, 4vw, 48px)` via `--pad`
- Section vertical padding: `clamp(72px, 9vw, 116px)` for major sections; less for compact ones
- No uniform padding — vary for rhythm

### Responsive breakpoints

- `1024px` — grid adjustments for architecture section
- `860px` — main mobile breakpoint: nav collapses, hero stacks, most grids go to single column
- `600px` — finer: ticker hides, footer collapses, outcome rows simplify

### Buttons

Three variants via `.btn` base class:
- `.btn-teal` — teal bg, cream text. Primary CTA.
- `.btn-outline` — transparent, ink border. Secondary on light bg.
- `.btn-outline-light` — transparent, dark rule border. Secondary on dark bg.
- `.btn-sticky` — amber bg, ink text. Sticky bar only.

### Sections on dark blue

Use `.eyebrow-light` for section labels on dark blue backgrounds. Body text uses `oklch(68% 0.020 218)`.

### Icons and spot illustrations

All icons use `fill: none; stroke: currentColor; stroke-width: 1.75; stroke-linecap: round; stroke-linejoin: round`.

- `.nav-logo-mark` — 24×16 wave SVG beside the nav wordmark. Color: `var(--teal)`.
- `.manifesto-mark` — 56×16 three-wave SVG above the manifesto blockquote. Color: `oklch(38% 0.08 218)`.
- `.arch-num-col` — flex column wrapper for the pillar number + `.arch-icon` in the architecture grid. Each of the 7 pillars has a unique thematic 16×16 icon.
- `.arch-icon` — 16×16 thematic icon stacked below the pillar number. Color: `oklch(38% 0.080 218)`.
- `.serve-icon` — 15×15 inline SVG in each serve-list `<li>`. Checkmark for the yes-list (teal), X for the no-list (ink-200). Replaces the former CSS `::before` dot.
- `.prog-icon` — 11×11 inline SVG within `.program-grade` labels. Color: `var(--teal)`, opacity 0.85.

### Animations

- `.reveal` class: opacity 0 + translateY(22px), toggled to `.visible` by IntersectionObserver
- Hero text/image: CSS `@keyframes fadeUp` on page load (no JS needed)
- Bar chart bars: `width: 0` by default, animated to `data-w` value when chart enters viewport
- Sticky bar: `transform: translateY(100%)` hidden, `.visible` removes it; toggles when hero exits viewport

### Scrolling services/outcomes story

Use this pattern for Crimson-style "Everything Your Child Needs. All in One Place." sections.

- Build a normal vertical stack of feature rows, not a slider or carousel
- Desktop rows use two columns: copy on the left, visual card or image collage on the right
- Each row should be close to a viewport tall, with text aligned near the vertical middle
- The right-side visual belongs to the row and moves with the page flow
- Do not keep one fixed visual area and swap content inside it
- If the reference includes a fixed bottom CTA bar, keep it fixed at the bottom with a left message and right `Get Started` action
- Use subtle scroll-linked opacity and translate effects only
- As a row enters, text moves from low opacity to full opacity
- As a row enters, the visual fades in and moves slightly upward
- As a row leaves, it fades slightly and exits naturally with the page
- Mobile should stack normally and remain readable
- Respect `prefers-reduced-motion`

Implementation: use `scroll-story.js` and call `BlueOceanScrollStory.initVerticalScrollStory(...)` with the row selector, copy selector, visual selector, ready class, and CSS custom property prefix for the section. The utility should remain behavior-only and should not define colors.

Reference service sequence for this pattern:

1. Get in With a Winning Strategy
2. Showcase Leadership With a High-Impact Capstone Project
3. Conduct Research That Stands Out
4. Win Prestigious Honors & Awards
5. Write Essays That Seal the Deal
6. Top-Scoring Tutors That Lift Grades and Test Scores
7. Former Ivy League Admissions Officers, Now Working for You

---

## Absolute Bans (from impeccable skill)

- No `border-left` or `border-right` as colored accents on cards or list items
- No gradient text (`background-clip: text`)
- No glassmorphism as decoration
- No hero-metric template (big number + tiny label + accent). Stats go in context (`.stat-row` format)
- No identical card grids with icon + heading + text repeated
- No large rounded icons above headings
- No star ratings (too generic, replaced by admit badge + attribution)

## Content Rules

- No em dashes — use commas, periods, or restructure
- No AI filler: no "holistic," "passionate," "transformative," "tailored," "curated"
- No generic claims without data
- Student outcomes: real names, real admits, real scholarships (approximate, INR)
- Metrics footnote: "3-year average acceptance rates across all Blue Ocean students who applied. Individual results vary. Data updated annually."

---

## When to Update This File

Update `docs/site.md` when:
- A new section is added to the page
- A layout or CSS convention changes
- New responsive breakpoints are introduced
- Content rules are revised
