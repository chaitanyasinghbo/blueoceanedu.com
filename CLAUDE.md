# Blue Ocean Education — Claude Instructions

Before making any website changes, read:
- [docs/brand.md](docs/brand.md)
- [docs/product.md](docs/product.md)
- [docs/site.md](docs/site.md)

Always keep the site aligned with Blue Ocean's premium, founder-led, student talent-development positioning.

Do not make the site sound like a generic college consultancy.

## Required before any change

1. Read the three docs above
2. Check that the proposed change is consistent with the voice and positioning in `docs/brand.md`
3. Check that the product framing is accurate per `docs/product.md`
4. Follow all conventions in `docs/site.md` (colors, typography, copy rules, what not to do)

## Scroll services/outcomes pattern

When the user asks for a Crimson-style "Everything Your Child Needs. All in One Place." section, build it as a vertical scrolling services/outcomes story, not a carousel.

Use this structure:
- Section heading at the top
- A vertical stack of feature rows
- Each row is a two-column layout on desktop: left copy, right visual card or image collage
- Each row is approximately one viewport tall, or slightly less
- Text is vertically centered in the row
- The visual moves with the page flow and is not fixed while content swaps
- Include a fixed bottom CTA bar when the reference asks for it: left message, right `Get Started` action
- Mobile stacks normally: heading, copy, visual, next row

Expected sequence when recreating the referenced services/outcomes section:
- Get in With a Winning Strategy
- Showcase Leadership With a High-Impact Capstone Project
- Conduct Research That Stands Out
- Win Prestigious Honors & Awards
- Write Essays That Seal the Deal
- Top-Scoring Tutors That Lift Grades and Test Scores
- Former Ivy League Admissions Officers, Now Working for You

Use this motion:
- Mostly normal vertical scrolling
- As a row enters, text moves from low opacity to full opacity
- As a row enters, the image or visual card fades in and moves slightly upward
- As a row leaves, it fades slightly and continues moving naturally with page scroll
- The effect must be smooth and subtle
- Respect `prefers-reduced-motion`

Do not build:
- horizontal sliders
- carousels
- image areas that stay fixed while only the content swaps
- random fade-only reveal animations
- flashy parallax

Implementation note: use `scroll-story.js` for this behavior. Wire the row selector and CSS custom property prefix into `BlueOceanScrollStory.initVerticalScrollStory(...)`.

## Keep the docs current

When you make a change that introduces a new convention, adds a section, changes a metric, revises copy rules, or updates product framing — update the relevant doc file before finishing the task.

- Design or tone changes → update `docs/brand.md`
- Product, service, or outcome changes → update `docs/product.md`
- Structural, layout, or convention changes → update `docs/site.md`
