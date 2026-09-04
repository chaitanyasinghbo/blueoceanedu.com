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

## Analytics and the conversion

**One analytics block, on every page.** It sits between the `<!-- @analytics -->` sentinels at the top of every `<head>`: GA4 `G-2STB24PJGQ`, Meta pixel `754270597536586`, and PostHog. The only line that differs per page is the dataLayer pageview event, and the landing build swaps it. Keep the block byte-identical everywhere else or that swap silently stops matching. The build now fails if two root pages disagree.

**The funnel has two steps, and each fires its own event.** All three forms — `start.html`, `lp/`, `iblp/` — behave the same way:

| Step | Where | Meta | dataLayer |
| --- | --- | --- | --- |
| Form submitted | in place, on the page with the form | `Lead` | `LEAD_SUBMITTED` |
| Slot booked | `next-steps.html` | `Schedule` | `BOOKING_COMPLETED` |

On submit the scheduler opens inside the form card, as it always has. **Do not turn that into a redirect.** The lead fires in place precisely because there is no new URL: a family that fills the form and never picks a slot is still a lead, and waiting for a distinct URL to count it drops every one of those.

`next-steps.html` is reached two ways, and both mean a slot was picked: Calendly tells the page a booking happened and it advances by itself, or the family clicks the button under the scheduler.

**The scheduler is Calendly, mounted by `BOEvents.mountCalendly` on submit.** It is not in the markup — the frame is an empty `#bookingFrame` carrying the URL on `data-calendly-url`, so nothing is fetched from Calendly for a visitor who never fills the form, and by the time it mounts the family's name and address go in with it.

**Two things about that URL and that frame are load-bearing, not preferences.** `hide_gdpr_banner=1` stays on every copy of the Calendly URL: the banner is fixed inside Calendly's own iframe at `z-index: 2147483645`, in a phone-width frame it lands on the month grid, and because the iframe is taller than the phone the thing swallowing the taps is below the fold with nothing to dismiss. And `page_height` reports under 320px are ignored while the frame's floor is its own rendered opening height, because Calendly sends `26px` and `2px` before the real figure and a short frame clips the confirm button off with no way to scroll to it. Both are written up in `docs/site.md` under *The scheduler*. Calendly posts `calendly.event_scheduled` to the page the instant a slot is taken, which is what makes the booking observable at all; the Google appointment schedule this replaced published nothing, and the calendar poll that worked around it is gone.

**That message is now the only way off the page.** The `I have booked my slot` button and the line under it are gone from all three forms. Nothing renders below the scheduler. The cost is the failure it used to cover: if the message is blocked — a locked-down browser, an extension, a change at Calendly's end — the family books a real slot, the card does not change, and neither `Schedule` nor `BOOKING_COMPLETED` fires. The booking is still in Calendly's calendar; only the page and the pixel miss it. Do not put the button back without asking.

All of this lives in `lead-events.js`, loaded by every page that fires an event and copied into `lp/` and `iblp/` by the builder. Both events carry two guards:

- **No stored lead, no event.** Opening `next-steps.html` directly counts nothing.
- **One event per lead per step**, keyed to the lead's own timestamp, so a refresh or a second tab cannot count again while a genuine second submission still can.

`fbq` gets an `eventID` of `<step>-<timestamp>` so a server-side Conversions API event for the same step can be deduplicated against it later.

**PostHog's key and every capture option live in `posthog-init.js`, and nowhere else.** Each page carries two lines: an inline stub that queues, and a deferred tag for that file. The stub has to be inline and synchronous, because an inline script at the foot of the body runs *before* any deferred one and `next-steps.html` fires the booking from exactly there. It only queues, which is what lets the library be deferred and cost the render nothing.

It ships with no key. Until `PROJECT_KEY` is set it appends no script, requests nothing, and every call is a silent no-op. PostHog gets the same two funnel steps under the dataLayer's own name lowercased, `lead_submitted` and `booking_completed`, derived rather than written a second time so the two cannot drift. `lp-v2` adds `target_lead` and `non_target_lead` with the qualification reason on them.

**Session replay masks every input**, and that is not a preference. `maskAllInputs` is restated explicitly in `posthog-init.js` because it is the whole basis on which recording a page that collects a child's name, a parent's phone number and a school is acceptable. Do not set it false.

**`tools/posthog-daily.py` is the morning report**, and it needs a *Personal* API key, which is not the `phc_` key in `posthog-init.js`. That one is publishable and write-only; this one reads the project back out. Read-only, scoped to `query` and `project`, never committed.

**`privacy.html` is the page that has to keep up with all of this.** It is hand-written, no builder checks it, and it names the exact form fields we collect, the school fee band `school-fees.js` derives without the family typing it, the five companies that receive something (Google, Meta, PostHog, Calendly, Cloudflare), and the promise that session replay masks every input. A change to the form, to the lead sheet payload, to `posthog-init.js`, or to the third parties is a change to that page. It is written for the Digital Personal Data Protection Act, 2023 and the IT Act, 2000, not adapted from a US policy, and its section on students under 18 is what makes running a pixel on a site aimed at minors defensible. Full reasoning is in `docs/site.md` under *`privacy.html`*.

**Every `BOEvents` call is wrapped in a `try`, and must stay that way.** A missing script tag once left `BOEvents` undefined, and the bare call threw on the line before the scheduler is revealed — `Request Consultation` posted the lead and then did nothing visible. Analytics is always what gives way, never the booking. The build fails if a page calls `BOEvents` without loading `lead-events.js`.

## The landing pages are generated, not written

`lp/` and `iblp/` are **index.html with a different hero, and nothing else**. Same proof numbers, same method story, same outcomes, same team, same advisors, same admits wall, same right-fit block, same footer. The only thing that is theirs is the hero, which carries the consultation form instead of the framed campus picture.

Never hand-edit these files. All six are build output:

```
lp/lp.html      lp/index.html      lp/main.css      lp/next-steps.html
iblp/iblp.html  iblp/index.html    iblp/main.css    iblp/next-steps.html
```

Three sources feed them:

| To change | Edit |
| --- | --- |
| Anything below the hero, on all three pages | `index.html` |
| The submitted page, after the booking | `next-steps.html` |
| The landing hero, its form, the booking step | `tools/landing-hero.html` |
| The Lead and booking events, and the booking watch | `lead-events.js` |
| The scheduler link, the prefill, the booking message | `lead-events.js`, and the `data-calendly-url` on `#bookingFrame` |
| Where the lead row lands | `apps-script/lead-sheet.gs`, then redeploy it |
| Anything either page needs its own value for | the `PAGES` list in `tools/build-landing-pages.py` |

Then run the builder:

```
python3 tools/build-landing-pages.py
```

**Run it after any change to `index.html`, `next-steps.html`, `main.css`, or the hero partial**, in the same task as the change. Skipping it is what caused the drift it was written to fix: `index.html` gained a framed hero, a scrolling press strip and a retuned wash that neither landing page had, and `lp/main.css` fell 2,200 lines behind `main.css`.

Things the builder already handles, so do not do them by hand:

- Nav links, actions and the mobile panel are hidden by the hero partial's CSS rather than stripped from the markup, so a change to `index.html`'s nav cannot break the build
- Every `start.html` link becomes `#formCard`, because the form is already on the page
- Every other site link becomes absolute to `blueoceanedu.com`, because a landing page is often served on its own hostname. The build **fails** on any relative `.html` link it does not recognise; add it to `SITE_PAGES` or `SITE_PATH_PREFIXES`
- `main.css`, `school-fees.js`, `posthog-init.js` and every logo folder are copied into both directories, because each one is served self-contained and nothing in it may reach up to the repo root
- `lp-v2` is outside this build but is checked by it: the build **fails** if its copy of `lead-events.js` or `posthog-init.js` has drifted from the root. Copy the file across by hand

`lp` and `iblp` differ in exactly five strings: the title, the GA4 pageview event, the GA4 thank-you event, the h1, and the `form_source` on the lead payload. A sixth difference belongs in the `PAGES` list, never in a generated file.

**The hero partial holds its own copy of the form's CSS, and the build cannot tell when it falls behind `start.html`.** A missing `.field[hidden] { display: none; }` left three conditional fields on screen permanently on both landing pages and nowhere else. After any change to the form in `start.html`, run the selector diff in `docs/site.md` under *The form*.

## The head is generated too, and so is the FAQ

Four things are build output alongside the landing pages. None is hand-edited:

| Generated | Written by |
| --- | --- |
| The `@seo` block in every page's `<head>` | `tools/build-seo.py` |
| The `.faq-list` on `fit.html` | `tools/build-faq.py` |
| `sitemap.xml` | `tools/build-sitemap.py` |

```
python3 tools/build-seo.py
python3 tools/build-faq.py
python3 tools/build-landing-pages.py   # checks both, then rebuilds the sitemap
```

`build-landing-pages.py` **fails** if either of the first two is stale, because
the landing pages inherit `index.html`'s head wholesale and would otherwise
copy a stale canonical into four generated files.

**The problem the schema solves is a name collision, not a ranking problem.**
Four unrelated businesses trade as some form of *Blue Ocean*, and one of them, a
Vietnamese study-abroad agency, holds `linkedin.com/company/blue-ocean-education`
and `youtube.com/@blueoceaneducation`. Wikipedia carries two other men named
Sanjay Kumar. Two rules follow and neither is negotiable:

- **Every URL in `sameAs` resolves and belongs to us.** One wrong entry asserts,
  in machine-readable terms, that we are somebody else.
- **Every claim in the schema is visible on the page.** The footer gained an
  opening-hours line the same day `openingHoursSpecification` was added, and
  `hasOfferCatalog` ships on `index.html` alone because that is the one page
  naming the four service tracks.

**URLs have no `.html`.** Cloudflare Pages 308s `/founder.html` to `/founder`,
so canonicals, `og:url`, `@id` values and the sitemap all use the extensionless
form. The `href`s in the markup stay as they are; a 308 consolidates, and the
canonical is what decides the indexed URL.

**`404.html` is load-bearing.** Without it, Pages answers every unmatched path
with `index.html` at status 200, which is how `robots.txt` and `sitemap.xml`
both used to return the home page. It is a copy of `fit.html`'s shell and shares
no build step with it, so a nav or footer change has to be made in both.

Full reasoning, and the six off-site items no file in this repo can carry, are
in `docs/site.md` under *Search, answer engines, and the entity*.

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

## Asset weight and the phone

Nothing compresses assets on the way out. **Every file is served exactly as it
sits in the repo**, so the encoding of each one is a decision. The homepage was
9.0MB with a 41.8s mobile LCP; it is 1.76MB now, and the four things that did it
come straight back the moment someone drops in a new asset.

Full reasoning, measurements and settings are in `docs/site.md` under
*Performance and asset weight*. The rules that matter before you add anything:

- **No new PNG or JPEG for a photograph.** WebP, and measure the PSNR rather
  than looking at it. Keep the master in `unused/` at its original path and
  rebuild from that, never from the served copy.
- **A `.svg` over ~100KB is probably not a vector.** Every file in
  `blue-profile-arch/` was a base64 PNG in an SVG wrapper; one was 14.5MB for a
  card 600px wide. Check for `data:image` before trusting the extension.
- **`fonts/` is WOFF2.** Three faces are preloaded in every `<head>`, outside
  the `@analytics` sentinels because the block between them must stay
  byte-identical and these paths get rewritten per folder depth.
- **The hero photograph ships at two sizes**, switched by a `<picture>` `media`
  query at 900px, not by `sizes`. The frame crops 16:9 into 4:5, so the source
  costs about 2.2x the layout box and a `sizes` value would understate it.

**The viewport tag must never gain `maximum-scale` or `user-scalable`.** iOS
focus-zoom is fixed where it is caused: form controls go to 16px under
`@media (pointer: coarse)`, in **both** `start.html` and `tools/landing-hero.html`.
Suppressing pinch-zoom for every visitor to fix a font size is an accessibility
failure and Lighthouse scores it as one. `html, body` carry `overflow-x: clip`,
never `hidden`, because `hidden` makes a scroll container and unsticks every
`position: sticky` element on the site.

## `unused/` is the archive, not a source

Nothing in `unused/` is reachable from a page the site serves. It keeps its
original paths, so restoring a file means moving it back with the `unused/`
prefix removed. **Never reference anything from it, and never treat it as a
place to look for an asset** — if a page needs a file that lives there, move
the file out first.

```
python3 tools/find-unused.py
```

Walks outward from the real entry points and prints what is spare and what is
referenced but missing. Run it after deleting a section or swapping a theme.
Do not answer "is this used?" by grepping for the filename: `admits-green/` and
`admits-blue/` share every basename, so a dead folder reads as live.

## Keep the docs current

When you make a change that introduces a new convention, adds a section, changes a metric, revises copy rules, or updates product framing — update the relevant doc file before finishing the task.

- Design or tone changes → update `docs/brand.md`
- Product, service, or outcome changes → update `docs/product.md`
- Structural, layout, or convention changes → update `docs/site.md`
