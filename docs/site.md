# Blue Ocean Education — Site Architecture and Conventions

## Stack

Multi-page static site. Working file: `index.html` (landing page). Ocean Ember rebrand mock: `mock-index.html`. Sub-pages: `method.html`, `results.html`, `founder.html`, `fit.html`, `team.html`. Shared CSS lives in `main.css` (linked by all pages). Shared scroll behavior in `scroll-story.js`. School and fee reference data in `school-fees.js`, used by `start.html` and by both landing pages. No framework, self-hosted fonts only.

**There is one build step, and it is the landing pages.** `lp/` and `iblp/` are generated from `index.html` by `tools/build-landing-pages.py` and must never be hand-edited. See [The landing pages are generated](#the-landing-pages-are-generated) below.

Nav is five items in this order: Method, Founder, Results, Right Fit, Team. Every root page carries the same list three times, in `.nav-links`, `.mobile-panel-links`, and the footer `Explore` column. `lp/` and `iblp/` carry the footer list only, with absolute `https://blueoceanedu.com/` URLs. `case-studies/` carry a minimal `.case-nav` with no link list.

---

## Page Structure

### Landing page (`mock.html`)

Overview / scrollable summary of all content areas. Nav links go to sub-pages.

1. **Nav** — sticky, cream bg, logo left, links center (hidden mobile), phone + CTA right, hamburger on mobile. Logo links back to `mock.html`. Nav links: `method.html`, `results.html`, `fit.html`, `team.html`.
2. **Hero** — cream bg, sized by the framed picture rather than by the viewport, italic EB Garamond h1, the framed campus-and-student picture right, the alumni strip under the lede, the press strip at bottom
3. **Results / Numbers** — acceptance rate stats, 6x figure, bar chart. Section id: `results`
4. **Profile Architecture** — dark bg, 7-pillar sticky-left scrolling layout. Section id: `method`
5. **Outcomes carousel** — student admit cards with photos and badge grid. Section id: `outcomes`
6. **Team** — founder + advisory council with photos and credential badges. Section id: `team`
7. **Universities** — the admits wall, thirty brand-colour tiles showing where students were admitted
8. **Right Fit** — dark bg, two-col for/not-for lists. Section id: `fit`
9. **CTA** — dark bg, email + phone actions
10. **Footer** — 4-col grid with nav links to all sub-pages
11. **Sticky CTA bar** — fixed bottom, hidden until hero exits viewport

### `method.html` — The Method

Organised on the pyramid, not the old 7-pillar list. See `docs/product.md` for the model and how the pillars fold into it.

1. Page header (eyebrow + h1 + subtitle)
2. **What families are up against** — three data bands (`.problem-band`), each with a figure and an `.problem-implication` panel: the admit-rate decline line chart, the Harvard SFFA court figures as to-scale bars (`.scale-row`), and the guidance before/after pair (`.guidance-pair`). Citations in `.problem-notes`
3. **Our answer is the Spike** — the pyramid diagram (`.spike-layout`, inline SVG) plus the colour-keyed `.spike-legend` and the two-column `.spike-argument`
4. The five layers, scroll story (`id="method"`) — Diagnosis, Foundations, Distinction, Presentation, Management, each row scrolling on the left against the scroll-linked `.pyramid` held sticky on the right
5. **Why start early** — the ACT *Forgotten Middle* chart (`.early-layout`) with an HTML `.chart-key`
6. **The whole student** — `.breadth-grid` plus the `.breadth-feeds` strip
7. **What a year looks like** — `.year-grid`, five streams by twelve months, three diagnosis months shaded, horizontally scrollable in `.year-scroll` below 900px
8. CTA, Footer, Sticky CTA bar

### `results.html` — Results

1. Page header
2. Numbers proof (`id="results"`) — the `.proof-stat-stack` (the single `6x` card) + 13-row acceptance chart + `.acceptance-source`
3. Outcomes carousel (`id="outcomes"`) — student cards
4. **Student voices** — `.voices` / `.voice-row`, four students, alternating photo side
5. **Parent voices** — same component, three parents
6. **Distinction, proven** — `.program-wall` (12 summer programs) and `.journal-wall` (4 journals), tiles from `proof-logos/`
7. Universities — the admits wall (`.universities`)
8. Student Stories (`id="stories"`) — hidden/archived, references images that do not exist
9. CTA, Footer, Sticky CTA bar

### `founder.html` — Dr. Sanjay Kumar

**This page has no page header.** It is the one root page that opens straight into its content, because the letter is the page.

1. The letter spread (`.letter-spread`) — `.letterhead` over `.letter` in the left column, the evidence rail (`.founder-rail`) beside both
2. In print, and on camera (`id="press"`, `.section.dark.press-shelf`) — the three-column clippings index (`.clipping-cols`), then the full-width `.book-strip`
3. The record (`id="record"`, `.section.paper-low`) — the photo strip (`.founder-strip`) as matted prints, then `.founder-timeline` with the `.milestones` list
4. CTA, Footer, Sticky CTA bar

The dark header it lost carried the eyebrow *A note from our founder*, the headline *Develop the student. Admissions follow.*, and the byline *Dr. Sanjay Kumar, PhD. Founder, Blue Ocean Education.* All three were already in the letter: the six words are the letter's eighth paragraph and are set in bold there, and the byline is the signature. A letter that announces itself before it starts is a brochure page about a letter.

**The h1 moved into the letterhead.** `.letterhead h1` is the sender, `Dr. Sanjay Kumar, PhD`, which is what `<title>` already says and what a letter names at the top. Do not put a page title back above it. A letter has a sender, not a headline.

The sticky CTA bar watches `.letterhead` rather than `main > section:first-child`, because the first section is now the whole letter and the bar would not appear until a visitor had scrolled past all eleven paragraphs.

The photographs and the milestones are one section, not two. They are the same thirty years shown twice, and as two sections they carried two headings that meant the same thing (*The work, outside the office.* over *Katihar to Kennedy, and back.*). The section now takes the second heading, the eyebrow reads `The record`, and `Milestones` is demoted to a `.method-kicker` label over the list.

Built on the shared shell, not adapted from `brochure variations/dr-sanjay-kumar.html`. That file is a standalone page with its own palette (`--yellow: #FACC15`) and Google Fonts and shares no components with the site. The clippings shelf takes its **link list** from that file and nothing else. Every URL was re-checked before it shipped, and two of them were dropped for returning 404.

## Letter form

The letter is set as a letter, not as an article. Four things carry it.

**The measure.** `--letter-measure` on `.letter-spread` is `min(100%, 566px)`, and `.letter p`, `.letter-spread .letterhead`, and `.letter-signature` all take it. At the top of the body clamp (19px) that is about 66 characters a line, which is the brand's ceiling. Filling the column instead ran past 85, and eleven paragraphs at that width lose the reader on every carriage return. The letterhead rule and the signature rule close the same width the paragraphs are set to, so the letter reads as one sheet rather than as text floating in a wider column.

State the measure in **px, not `ch`**. Neue Haas Text has a wide zero, so its `ch` is about 0.57em while running lowercase averages 0.44em, and `62ch` overshot the target by a fifth and had no effect at all inside the column.

Body copy is `--ink` at `clamp(16.5px, 1.32vw, 19px)` on `line-height: 1.72`. It was `--ink-soft` at 16px to 18px, which is the site's caption and secondary-line colour, one step down from the 13.5:1 pairing the brand asks for on body text.

**The letterhead** (`.letterhead`) runs above the letter at the letter's own measure, not the page's: sender and role left, office address right, a `--line` hairline under both. It is a grid item of `.letter-spread` rather than a child of `.letter`, so that one column on a phone can open on the letterhead and still reach the portrait before the first paragraph.

**The salutation** (`.letter .letter-salutation`) is Display, sentence case, 22px to 27px. It was 14px tracked caps, which is the site's eyebrow treatment and put a section label where the letter says hello. The selector needs both classes: `.letter p` at (0,1,1) beats a bare `.letter-salutation`, and the salutation is a `<p>`.

**The signature** (`.letter-signature`) closes it over a rule. It repeats the name the letterhead opened with, which is correct in a letter and not a duplication to remove.

There is no paper sheet under the letter. The mats beside it already carry the physical-object idiom, and a shadowed card under a thousand words of body copy is one metaphor too many.

## The founder page images

Both image sections are ported from prospectus pages 3 and 4, which are the one spread in the print piece that pairs a letter with the record behind it. The letter alone left the right half of a 1248px page empty for its whole length.

### The evidence rail

`.founder-rail` runs beside the letter and carries three things in this order: the commencement portrait, the Ford Foundation Mason Fellowship certificate, and the Harvard MPA degree. The letter's third and fourth paragraphs make the Harvard claim; the rail is where a parent can see it. Nothing else belongs in the rail, because a fourth object turns a piece of evidence into a gallery.

The rail flows, it is not sticky. At `clamp(276px, 28vw, 392px)` its three items run about as tall as the letter beside them, so a sticky rail would have nothing to travel.

The two documents fall below the portrait rather than over it. In the prospectus they lie on the dark lower half of a full-page portrait, over empty ground. The web portrait is a 2:3 frame with no such band, so an overlap covers the scrim caption instead.

**Placement is explicit, not source order.** The source runs letterhead, rail, letter; `.letter-spread` then pins the letterhead to row 1 column 1, the letter to row 2 column 1, and the rail to `grid-row: 1 / span 2` in column 2. One column on a phone therefore falls out as letterhead, portrait, documents, letter, with no `order` needed. Source order alone would put the rail after the letter on a phone, and an `order: -1` on the rail would put the portrait above the letterhead.

Below 1080px the grid drops to one column, the explicit placements are reset to `auto`, and the rail turns landscape, portrait left and the two documents as a pair beside it. Stacked in a column at that width the rail ran most of a screen before the salutation. Below 560px it goes to one column at 340px.

### Matted prints

`.print-mat` is a photograph or a document on a mat, tilted a degree or two, with a hard shadow under it. It is the prospectus's device for showing a physical object rather than a picture, and it is scoped to this page.

The site now has two ways of captioning a photograph, and the split is by subject, not by section:

- **Portraits are captioned on the photograph**, under the counsel-wall scrim. `.counsel-wall`, `.founder-portrait`.
- **Snapshots and documents are captioned on the mat**, in tracked caps under the image. `.print-mat`.

The mat sets in `--paper` with a `--line` hairline. On a `--paper` section the mat is the same colour as the ground, so the border and the shadow are what draw the edge, and neither is optional.

`.founder-strip` replaced a five-across grid of 3:4 scrim tiles. Group photographs cropped to a narrow portrait frame lost everyone but the middle two people, and the `Katihar to Kennedy` cover was cropped through its own title. Aspect ratio is now set per photograph, 4:3 for the event shots and 3:4 on `.founder-shot.is-portrait` for the book cover, and the mats are staggered with `translateY` so an uneven row reads as a pile of prints rather than a broken grid. Columns step 5 / 3 / 2.

Rotations stay between 0.8 and 1.5 degrees. Past about two the row stops reading as prints on a table and starts reading as a scrapbook.

## The clippings index

`.press-shelf` sits between the letter and the record. It answers the one thing the letter cannot: everything above it is a claim in the founder's own voice, and this is where a parent checks it against someone else's byline.

**It is one object on Core, not three lists on Surface.** The first build set it on Surface with two ruled columns and a book card floated beside a third list, and it read as scattered: four stacks whose rules never lined up, on the same ground as the letter above them. The section is now `.section.dark`, which is the ground the landing-page press strip already gives every third-party masthead, and the three lists are one bordered table.

`.clipping-cols` draws that table the way `.join-steps` draws its cells: `gap: 1px` over a `--line-dark` background, each `.clipping-col` filled with `--forest`, so the single pixel showing through is the column divider. `border-radius: 8px` with `overflow: hidden` closes the corners.

Three columns of four, in this order: `Written by Dr. Sanjay` (op-eds in The Hindu and the Times of India edit page), `Written about him` (the Harvard Mittal announcement, the Economic Times and MediaBrief appointment stories, the Times LitFest speaker profile), and `On camera` (four talks). A podcast column was cut because the only links available point at `open.spotify.com` and `networkcapital.tv` rather than at episodes.

**The mastheads are type, not marks.** `press-logos/` holds eight knockouts and this section names twelve outlets. A wall with four gaps in it reads as a build error, so every row sets its publication as a tracked-caps `.clipping-pub` label over a `.clipping-title` headline, and the hairline between rows does the work a tile edge would have done. `.clipping-pub` is in the `--support-light` list in `ocean-ember.css`, because Support at full value on Core is too dark to carry an 11.5px label.

**A row is two lines in one column with the chevron spanning both.** The label and the headline are siblings, not a wrapped pair, so `.clipping-pub` and `.clipping-title` are pinned to `grid-column: 1` and `.clipping::after` to `grid-row: 1 / span 2`. Without the explicit placement the headline lands in the 8px chevron track and the row collapses to a vertical string of letters.

**The chevron is the mobile panel's**, a `::after` square with two borders rotated 45 degrees, drawn once for `.clipping` and `.book-link` together so the section has one affordance rather than two.

`.book-strip` runs the full width under the table on `--forest-soft`, the same Core lift `.team-founder.is-wide` uses, with the copy left and the two links right. It carries the citation the Harvard Kennedy School library page gives (Vani Book Company, New Delhi, 2019). It does **not** repeat `founder/book.jpg`: the cover is already a matted print in the record below, and the same photograph twice on one page reads as an oversight.

The classes are `.clipping*`, not `.clip*`. `.clip`, `.clip-mast`, `.clip-by`, and `.clip-strip` already exist in `main.css` from the retired press-headline grid, and `.clip` is defined later in the file, so a `.clip` here silently loses its padding and gap to it.

### The ladder is 3 / 2 / 1

Three into two leaves an empty cell, and an empty cell inside a bordered table reads as a rendering fault rather than as space. At 1080px the grid drops to two columns and `.clipping-col:last-child` takes `grid-column: 1 / -1`, so `On camera` becomes the full-width bottom row. The book strip stacks at 900px and the table goes to one column at 760px.

## Links in the letter

`.letter a` and `.milestones a` keep the body colour and are drawn by a Support underline at `text-underline-offset: 3px`. Colour arrives on hover only.

A letter is the one page on the site where a link is a citation rather than a call to action, and eight blue phrases in eleven paragraphs turn a letter into an encyclopedia entry. The underline is enough to say the phrase leads somewhere.

Every institution named on the page is linked to itself: Delhi University, JNU, the Institute of Social Studies, the Harvard Kennedy School, upGrad, and Blue Ocean's own home page. Two links are to a document rather than a homepage, because the institution has none that resolves. The Mittal South Asia Institute link goes to the 2016 SAI announcement that names him. The Harvard Club of India link goes to the club's own journal, *Journal of the Harvard Club of India: India at 75*, hosted on `niti.gov.in`.

**EdJustice Foundation is deliberately unlinked.** `edjustice.in` returns 404 across the whole domain. `sanjaykumar.in` is dead the same way and is used nowhere. **Check that a URL resolves before adding it**, and do not restore either of these from `brochure variations/dr-sanjay-kumar.html`, which still carries both.

## Search and answer engines

`founder.html` is the first page on the site to carry a full head block, and it is the pattern for the rest.

- `<link rel="canonical">` on `https://blueoceanedu.com/`, which is the domain `lp/` and `iblp/` already use in their absolute footer links. The brochure files use `blueocean.education`, which is a different property and is not the canonical host.
- Open Graph as `og:type: profile`, with `founder/commencement.jpg` at its real 900 by 1350 as the card image, plus the Twitter summary card.
- One `application/ld+json` block holding a six-node `@graph`: `ProfilePage`, `WebSite`, `BreadcrumbList`, `Person`, `Book`, and `Organization`.

The `Person` node is the one that matters and it is stable IDed as `https://blueoceanedu.com/#sanjay-kumar`, so other pages can reference the same person without redefining him. It carries `alumniOf` with a URL each, `hasCredential` for the MPA and the PhD, `award` for the Mason Fellowship, `knowsAbout`, `birthPlace`, and a `sameAs` list of seven third-party pages that name him. `Book` describes *Katihar to Kennedy* with the library's own citation and points at both the Amazon listing and the Harvard Kennedy School collection page.

Two rules for anything added here. **Every claim in the schema has to be visible on the page**, because a `Person` node that outruns its own page is what an audit flags. And **every URL in `sameAs` has to resolve**, which is why neither `edjustice.in` nor `sanjaykumar.in` is in the list.

### `fit.html` — Right Fit and how to join

1. Page header
2. Right Fit / Selective by design (`id="fit"`)
3. **How to join** — three numbered `.join-step` blocks (diagnostic call, student essay, strategy call), the `.join-pair` panels (after a yes, what we never do), and the `.join-fee` panel
4. CTA, Footer, Sticky CTA bar

Fees are deliberately not published. The `.join-fee` panel says one fee covers everything and that it scales with program length; the figures live in `docs/product.md` and are shared on the strategy call.

### `start.html` — Request a Consultation (CTA landing page)

All "Get Started" and primary hero CTA buttons link here.

**The page is the form and nothing else.** One hero, then the footer.

1. Hero (dark bg, grid pattern), sized `min-height: calc(100svh - 74px)` so the form owns the first screen. Left col: eyebrow + h1 "Work 1-1 with our team." + `.consul-hero-byline` + `.consul-steps`. Right col: 3-step form card embedded directly in the hero grid.
2. Form card — Step 1, *Request a Consultation*: role toggle (Student / Guardian), First Name, Last Name, Email, Continue →
3. Form card — Step 2, *Where the Student Studies*: Phone (+91 prefix), Grade, School City, School Name, Board, Back / Continue →
4. Form card — Step 3, *Where You Are Aiming*: Residence Pincode, Country Preference ranking, Scholarship dropdown, Back / Request Consultation, privacy note
5. Form card — Success state: confirmation, then the Calendly scheduler
6. Footer (same as other pages)
7. No sticky CTA bar (this page IS the CTA destination)

Form step transition: titles animate with `out` class (translateX + opacity). Steps use `hidden-step` + `fade-in` CSS classes. All three steps are driven by one `goToStep(n)` over parallel `panels` / `titles` / `pips` arrays, so a fourth step is a markup edit plus one entry in `firstFocus`.

**The split is by who reads the answer.** Step 2 tells the counsellor what the student is working with. Step 3 tells us, before anyone picks up the phone, whether we are the right team. That is what the diagnostic call is for, and the more of it the form settles, the less of the call is spent on qualification.

### The school cascade

School is two dropdowns, not a text field: **School City**, then **School Name** filtered to that city. A family picks from about ten names instead of typing one we then have to guess at, and the fee lookup gets an exact key.

Both dropdowns carry an **Other** option and so does Board. Choosing it reveals a text field (`#schoolCityOtherField`, `#schoolOtherField`, `#boardOtherField`) via the `hidden` attribute. `.field` is `display: grid`, which beats the UA rule for `[hidden]`, so `.field[hidden] { display: none }` has to be stated.

Picking **Other city** hides the school dropdown entirely rather than showing an empty one, because a city we hold no schools for has no list to offer.

`school-fees.js` holds 112 schools across 30 cities from `Indian_Schools_Fees_Complete_Reviewed_2026.csv`. The list is a sample of the schools our families come from, not a register, which is why Other is on every one of these fields.

### Fees are collected, never shown

The form never renders a fee. `BOSchools.resolveFee(school, city, board)` runs at submit time and the result goes to the lead sheet only, so the team can read affordability off the row without the form asking a family about money.

**The exact published figures ship, not a band.** Three fee columns go to the sheet, all in whole rupees:

| Column | What |
|---|---|
| `school_ib_fee_inr` | The CSV's IB figure for the matched school, verbatim. Blank where the source says NA |
| `school_general_fee_inr` | The CSV's general figure, same rule |
| `school_fee_annual_inr` | The one that applies to this student's board |

Both raw columns ship on every row so the sheet always holds the source numbers and never only a derived one. `school_fee_band` is a convenience for scanning and sits beside them, not in place of them. A round-trip test asserts all 112 rows resolve to their exact CSV figures.

**The CSV stays the source of truth.** `school-fees.js` is generated from it, not maintained by hand:

```
python3 tools/build-school-fees.py           # rewrite the data block
python3 tools/build-school-fees.py --check   # exit 1 if a rebuild is pending
```

Only the block between the `generated:begin` and `generated:end` markers is rewritten; the matching logic around it is hand-written and never touched. Editing the rows by hand is the one thing not to do, because the next rebuild silently reverts it. The generator stops rather than ships if two rows share a school name, since that makes both the dropdown and the exact match ambiguous.

- **Board picks the resolved column.** The source has two, an IB one and a general one. IB, IGCSE, A Levels and AP resolve to the IB figure; CBSE, ICSE, State and Other to the general one. Where the applicable one is NA the other is used and `school_fee_basis` says `only stream published for this school`, with both raw columns on the row showing exactly what was and was not published.
- **Nothing is ever invented.** No match means all three fee columns are blank, not zero and not a guess.
- **A typed school is still matched.** Exact first, then a token match with generic words (`school`, `international`, `the`, `public`, `academy`, and so on) and the city name stripped, scored both directions so "Doon" and "The Doon School Dehradun" both land. Threshold 0.62, city is a tiebreaker rather than a filter, ties break on raw shared-token count. Below threshold it returns no match rather than a wrong one.
- **The match is auditable.** `school_fee_matched_name`, `school_fee_match_method` (`exact` / `fuzzy` / `none` / `lookup-unavailable`) and `school_fee_match_score` ship beside the number.
- `boys` and `girls` are deliberately **not** stopwords. With them stripped, "Welham Girls" matched Welham Boys'.

If `school-fees.js` fails to load, a shim in the inline script leaves both dropdowns with nothing but their Other option, which the existing change handler turns into plain text fields, and the sheet gets `lookup-unavailable`. The form still takes the lead.

### The country ranking

`.rank-grid` is six `.rank-chip` buttons and **tap order is the ranking**. Tap for first choice, tap again for second, third; tap a picked chip to remove it and the rest renumber. A fourth tap does nothing and the unpicked chips dim (`.is-full`).

Not a drag list, which is unusable on a phone, and not three parallel dropdowns, which ask the same question three times. Three taps is the whole interaction and it is the single most diagnostic answer on the form.

**The six are countries, not university tiers**: US, UK, Canada, Germany, Europe other, Singapore / HK / Australia. A family knows where it wants to send a child long before it can name a band of universities, so the question is answerable on the first read. Only the first choice is required.

The grid is the control, so the error state sits on `.rank-grid.field-error` rather than on any one chip, and the label is a `.field-label` span rather than a `<label>` with nothing to point `for` at.

### `target_audience`

One computed column on the sheet, and it says `Target` or `Non-target`. Nothing in between, because a four-way triage label gets argued with and a binary gets acted on.

Two conditions, both required:

1. **The US is the first or second choice.** Third does not count.
2. **The school charges 5L a year or more**, on the stream the student's board actually puts them in.

Board is load-bearing here. Shiv Nadar School Sector 26A is 10.36L on IB and 4.21L on CBSE, so the same school reads `Target` for an IB student and `Non-target` for a CBSE one. That is the intended behaviour, not a rounding problem.

**An unknown fee does not fail the test.** A school outside the 112 returns `Target` if the US condition holds, because the list is a sample and dropping a US-first parent over a missing CSV row is the expensive mistake. `school_fee_match_method` reads `none` on those rows, so they are easy to spot and easy to spot-check.

The floor is `TARGET_FEE_FLOOR` in the inline script, and every input behind the verdict ships on the same row.

Every input behind it ships on the same row, so it is always checkable. **Do not let it become a filter in the sheet.** It is there to order a callback list, and a family whose school is simply not in the 112 will read as unknown.

### The scheduler

On success the card shows the confirmation, then Calendly. The family books the diagnostic call in the same breath as submitting, instead of waiting on a callback.

`.consul-hero-grid.is-booking` drops the hero to one column at `max-width: 900px` and hides `.consul-hero-copy`. A scheduling grid inside the 440px form column renders a week as a column of hairlines, and the pitch on the left has done its job by the time anyone sees this.

**The frame starts empty.** `#bookingFrame` holds a placeholder line and the booking URL on `data-calendly-url`; `BOEvents.mountCalendly` fills it on submit. Nothing is fetched from Calendly for a visitor who reads the page and leaves, not even `widget.js`, which is loaded on demand by the same call.

Height sits on `.booking-frame`, not on the iframe, because Calendly reports the height its own content needs through a `calendly.page_height` message and `lead-events.js` writes that here. `700px` is the opening value, `900px` under 640px wide, held until that message arrives. It renders blank in headless Chrome; that is the harness, not the embed.

**Not every `page_height` is a height.** Calendly sends `26px`, then `2px`, then the real figure about a second and a half later, and for a while the handler wrote all three. The floor was a constant `560px`, which is under both CSS openings, so the first junk report shrank every frame it touched and a phone lost 340px of scheduler until the real height landed. Two rules now, both in `listen()`:

- Anything under `MIN_CREDIBLE_HEIGHT` (320px) is a document that has not rendered yet, and is ignored rather than written.
- The floor is the frame's own rendered height, measured at mount, so it is whatever the stylesheet opened it at. A fixed number in the script cannot know which breakpoint is live.

A frame left short is not a cosmetic problem. `.booking-frame` clips its overflow and the iframe is `height: 100%`, so the dates and the confirm button end up below the cut with nothing to scroll.

### `hide_gdpr_banner=1` is load-bearing

Calendly renders a OneTrust cookie banner **inside its own iframe**, at `position: fixed; z-index: 2147483645`. On a desktop frame it is a small card in the bottom-left corner and misses the calendar entirely. In a phone-width frame it becomes a 300×328 floating panel over the bottom half of the month grid, and on a real booking page that is exactly where the dates with slots in them are. Hit-tested at 390px: the centre of `Monday, July 27 - Times available` resolved to `div#onetrust-policy-text`, and a click on any available date was refused as covered.

What made it invisible for so long is that the banner is fixed to the bottom of an iframe taller than the phone. The thing swallowing the taps sits below the fold, so there is nothing to dismiss and no way to tell anything is in the way. The calendar looks perfect and does nothing.

The parameter belongs in three places and all three have to carry it: `CALENDLY_URL` in `lead-events.js`, and the `data-calendly-url` on `#bookingFrame` in `start.html` and in `tools/landing-hero.html`. The plain-iframe fallback and the last-resort `catch` in the form script both build their `src` from that attribute, so they inherit it.

`lp/next-steps.html` and `iblp/next-steps.html` do **not** carry the scheduler. Those pages are a resource list, and the two landing pages still run their own 2-step copies of this form.

### The lead sheet endpoint

`start.html`, `lp/`, and `iblp/` all POST to the same Apps Script Web App. **The script does not run from this repo.** It is bound to the leads spreadsheet and lives at Extensions > Apps Script from inside it. `apps-script/lead-sheet.gs` is the versioned source; paste it over `Code.gs` there and redeploy a new version, or nothing changes.

The script is **header-driven**: row 1 is the schema, a posted key with no column gets one appended on the right, and a column no page posts to stays blank. That is why the three pages can send different field sets without the script knowing about any of them. `setUpSheet()` is a run-once helper that pins the timezone, formats the timestamp column, and back-fills `PREFERRED_ORDER` onto a sheet that already holds rows.

**Timestamps are IST.** The forms send a UTC instant, which is the correct thing for a browser to send, and the script pins the spreadsheet timezone to `Asia/Kolkata` so every row reads in IST. The value stays a real date, not a preformatted string, so the column still sorts and filters; `dd-MMM-yyyy HH:mm:ss` is display only. The timezone is checked before it is written, because setting it on every submission is an API call for nothing.

The forms post with `mode: 'no-cors'` and never read the response, so a misconfigured deployment fails silently. The deployment has to stay on **Execute as: Me** and **Who has access: Anyone**.

`.consul-steps` names the same three-step join process `fit.html` carries as `.join-steps`: diagnostic call, student essay, strategy call. Here each step is a number, a name, and **one line**, set as a hairline-ruled list on the dark hero ground rather than the bordered panel grid. It sits beside the form in a narrow column, and the full paragraphs ran the column past the fold on desktop and pushed the form most of a screen down on a phone. `fit.html` remains the full-length version and is where the reasoning belongs. **Keep the two in agreement on what the three steps are.** The older `.consul-assurances` list it replaced is gone.

The list carries **two scales**. Desktop runs 18px name over 15.5px body in a 42px number gutter, which puts each step on one line at 580px. The 860px block cuts it to 14.5px / 13.5px in a 30px gutter, because on a phone the list sits above the form and every pixel it takes pushes the first field down. Raising the phone scale to match desktop undoes that. `.consul-hero-byline` under the h1 gives the reason for the limited intake, that a capped cohort is what lets every plan be built around one student, then hands off to the list in a short second sentence. Two lines at 540px. It replaced a line that led with the founder reviewing every enquiry "himself" and closed on "Here is how joining works", which read as a small-business boast followed by filler. **Say what is scarce and why, then stop.**

The page previously carried the full landing-page stack below the form: numbers proof, the seven-pillar services story, the outcomes carousel, founder, counsel wall, admits wall, and right fit. All of it was removed, along with `scroll-story.js` and the inline reveal, bar-chart, sticky-services, sticky-CTA, and carousel scripts, which now have nothing to observe. A visitor who has already clicked Get Started does not need the pitch re-run at them. Those sections still ship on `index.html`, which is where they belong. Do not re-add them here.

### `team.html` — Team

1. Page header
2. Team section (`id="team"`) — **Dr. Sanjay alone**, in a full-width horizontal card (`.team-people-grid.is-solo` + `.team-founder.is-wide`, portrait left, copy right)
3. **Four people on every file** — `.bench-grid`, the cadence-led 2×2
4. **Board of advisors** (`.section.dark.counsel-section`) — the `.counsel-wall` as a grid, all seven plus the claim tile, over the Harvard campus photograph
5. CTA, Footer, Sticky CTA bar

The page no longer carries a `.clip-grid` of press headlines. Nothing in the repo holds those eleven headlines, so the coverage claim is made by the press strip in the landing-page hero instead, where it is eight mastheads and no invented copy. The `.clip-source` line under the counsel wall is the only survivor of that section.

Rajat Sethi and Rajiv Gupta moved out of the old `.team-support-stack` and into the board grid, so all seven advisors are presented identically instead of two of them getting a different card. `.team-support-stack` still exists in `main.css` and is still used by `index.html`.

`index.html` splits the same material into **two sections**, in this order:

1. **The founder** (`.team-section`, dark) — Dr. Sanjay alone in `.team-founder.is-wide`
2. **The counsel** (`.section.dark.counsel-section`) — `.counsel-wall` over the Harvard campus photograph

## The counsel wall

`.counsel-wall` is the one portrait treatment on the site. It is used by `index.html` and `team.html`, and the same scrim is reused by `.founder-shot` on `founder.html`.

Ported from the prospectus advisor spread: 3:4 tiles, each a cutout portrait on Harvard crimson with the alma mater's mark top right, the name in Display over a bottom gradient scrim, and the credential in tracked caps beneath.

### Two layouts share the tile

`.counsel-wall` on its own is the four-across grid. `team.html` uses it, because there the board is the point of the section and every face should be visible without interaction. It carries a `.counsel-intro` Core tile in place of a portrait, so the wall stays a clean grid of eight.

Wrap the wall in `.counsel-carousel` and it becomes a horizontal rail instead. `index.html` uses that, with the claim tile dropped, so the seven portraits stay on one line rather than wrapping to a half-empty second row. Rail mechanics are the outcome rail's: native `overflow-x`, `scroll-snap-type: x mandatory`, chevrons that step one card, no auto-advance. Cards per view comes off a single `--counsel-per-view` custom property, so the breakpoints change one number: 4, then 3 under 1080px, 2 under 900px, 1.3 under 640px, where the fractional card is the scroll affordance and the chevrons are hidden.

This is a scroll rail, not a carousel in the sense `docs/site.md` rules out elsewhere. Nothing moves on its own and nothing is fixed while content swaps behind it.

The crimson is a third-party colour used exactly the way the admits wall uses each university's own, and it is what makes "all Harvard alumni" land before a word is read. `--counsel-ground` on `.counsel-wall` sets it, so an advisor whose mark needs its own ground can override it per tile.

It replaced a pale Support ground the cutouts floated on. Two of the seven carried a painted blue backdrop baked into the SVG that the other five did not, so the wall never read as one set.

The scrim runs transparent to 0.96 Ink through 0.34 at 38% and 0.86 at 74%. Over a photograph a single midpoint was enough; over flat crimson it darkened half the tile and the ground stopped reading as crimson at all, so the ramp moved late and the band's top padding came down to 48px.

### The marks on the tiles

`counsel-logos/` holds three files, not seven: `harvard.png` for five advisors, `lse.png` for Ishira, `mit.png` for Rajat. The prospectus shows each advisor's second institution where they have one, which is what keeps five identical Harvard shields from reading as filler.

The mark sits top right rather than beside the name as it does in the prospectus. Those were landscape cells; in a 3:4 tile the portrait is anchored to the foot, which leaves the top third empty, and putting the mark there fills dead space and never lands on a face.

Sized by the same fixed-box rule as the admits wall, `100 x 38` with `object-fit: contain`. The Harvard lockup is about 4:1 and the LSE plate is square, so capping one axis alone would leave the square mark a third of the lockup's presence.

Two alternatives were tried in place of these and both reverted. A per-tile Harvard watermark flattened the board to one institution and cost Ishira's LSE and Rajat's MIT their marks, which is the opposite of what the per-advisor treatment is for. A Harvard wordmark tinted into the section's paper read as a logo laid on a page rather than a ground. The campus photograph below does the shared-institution job instead, and leaves the tiles alone.

### The Harvard ground

`.counsel-section` puts Harvard Hall behind the whole section, from `harvard-hall.webp`. The board is all Harvard alumni, and the campus says that ahead of the copy in a way a wordmark cannot. Both `index.html` and `team.html` carry the class.

### Where `harvard-hall.webp` comes from

| | |
|---|---|
| Source | [Harvard Hall - Harvard University - DSC00655.jpg](https://commons.wikimedia.org/wiki/File:Harvard_Hall_-_Harvard_University_-_DSC00655.jpg) on Wikimedia Commons |
| Original | 5472x3648, photographed 2015-04-11 |
| Author | Daderot |
| Licence | **CC0** — Creative Commons Zero, public domain dedication |
| Attribution | Not required. No credit line is owed and none ships. |

CC0 was the deciding factor over three other candidates. A CC BY Harvard Yard shot was larger and warmer but would have put a permanent credit obligation on a commercial page for a background image, which is not a trade worth making.

**Build recipe**, from the Commons original, not from the file in this repo:

1. Crop to `(800, 330, 4680, 2620)` — 3880x2290, about 1.69:1. This drops the cluttered foreground (fences, signage, a pushchair) and keeps the cupola, the balustrade and the arched windows, which are the parts that read at background scale.
2. Saturation to `0.88`.
3. Resize to 1900px wide, Lanczos.
4. Gaussian blur `0.45`. Sub-pixel at display size and invisible under the scrim, but it removes the bare-branch high-frequency noise that WebP spends most of its bitrate on.
5. WebP quality 70, method 6. Lands at 371KB.

**The treatment is baked into the file, not applied in CSS.** Saturation and framing both live in the asset, so `::before` needs no `filter` and no clever `background-size`. That is deliberate: `filter` on a full-bleed layer costs a compositing pass on every paint, and sharpening before encoding fights the encoder. The cost of baking is that changing the look means rebuilding the asset from the Commons original. Do that rather than re-encoding the repo copy, which is already lossy.

Weight went **down**, from the 601KB `institution-harvard.jpg` to 371KB, while the source resolution went up 4.5x. Encodings that were tried and rejected: a Lanczos-sharpened 2x of the old photo (920KB), unsharp masking before encode (adds ~25% for detail the scrim hides), and 2560px wide (1.4MB, since bare branches are close to worst-case for WebP).

**The section runs `dark` because of it.** This is the one structural consequence and it is not optional. A photograph strong enough to be recognised cannot be pushed far enough back to sit under Ink type, so the type goes to Paper and the scrim carries the contrast instead of the opacity. The section dropped `paper-low` for `dark`, which brings `.section.dark .section-title` and `.dark .section-copy` with it, and the eyebrow takes `.light` for Lime.

Two layers, both on the section:

- **`::before` is the photograph**, `center 42% / cover`, with **no `filter`**. Saturation is baked into the asset. Position barely matters now that the framing is baked, which is the point: the crop is not something CSS has to get right at every viewport.
- **`::after` is the scrim**, opening at `0.94` over the head, easing to `0.86` at 50%, closing at `0.95` under the wall.

**The scrim hue is near-neutral, `oklch(13% 0.018 200)`, not Core.** A Core teal scrim over red brick turns the building olive, and the warmth is most of what makes it read as a campus rather than a texture. This is the one place on the site where a Core surface is deliberately not Core.

### Measure the scrim, do not eyeball it

The head band is the only place the photograph is really visible, because the wall covers everything below it. That makes it also the only place any type sits, so the building and the words compete over the same 300px. Every value above came out of measuring that band, not looking at it.

| | title | section copy | busyness behind title |
|---|---|---|---|
| First pass | 8.4:1 | 5.5:1 | 0.0095 |
| Now | **13.5:1** | **6.4:1** | **0.0033** |

The first pass already cleared AA on both and still read as busy, because a contrast ratio cannot see texture. Local variance behind the title is the number that had to move.

**If the scrim, the crop, or the photograph changes, re-measure rather than trusting the look.** Composite the real background at about 1440x820, sample the actual pixels in the title box and the copy box, and take the **worst** pixel, not the mean. A mean will pass while a bright patch of sky sits under one word.

Two traps this section already fell into:

- **The photograph is chosen under the scrim, not above it.** Harvard Hall looked far better than Memorial Hall as a picture, and worse in the first composite, because a pale building with bare branches loses its shape under cover while a dark tower keeps it. Composite every candidate before choosing.
- **A photograph swap invalidates the scrim.** Dropping Harvard Hall into the scrim tuned for Memorial Hall put the section copy at 4.3:1, right on the AA floor, because this photograph has bright sky exactly where that copy sits. The scrim was re-solved for it.

Two knock-on fixes the photo ground forced:

- `.counsel-nav .outcome-btn` is ghosted and fills to Paper on hover. The outcome rail's chevron is a Paper disc that fills to Core, which inverts to invisible against the photograph.
- `.counsel-section .clip-source`, the credit line under the wall on `team.html`, goes to a Paper mix. `--muted` is an Ink grey and disappears.

**It puts two dark sections back to back on `index.html`**, since the founder section above it is `.team-section`. That is deliberate. The photograph reads as a different surface from flat Core, and the run of dark ends at the admits wall below. If a light break is ever wanted between them, move it above the founder rather than into the counsel section, which needs the dark to hold its own ground.

### The portraits are pre-normalised, not CSS-fitted

`counsel-portraits/*.webp` are built, not raw. The sources run from a 500x400 head-and-shoulders crop to a 1200x1650 full torso, and no single `object-fit` rule survives that spread: `contain` leaves half the board floating in the middle of the tile, `cover` crops through chins.

Each cutout is trimmed to its alpha bounding box, scaled so the head is the same width in every tile, clamped so the subject occupies 66% to 76% of the frame, then anchored to the foot and centred on the head. Faces come out the same size and at the same height, and the hard bottom edge of each cutout lands under the scrim. Ishira's is the one visible compromise: her source is a much tighter crop, so the clamp scales her up and her face reads larger than the rest. The prospectus has the same characteristic.

They ship as WebP at quality 86. The seven cutouts are 236KB together against 9.5MB for the `exec-team-pics-blue/` SVGs they replaced on these pages. Those SVGs stay in the repo: `sanjay.svg`, `rajat.svg`, and `rajiv.svg` still carry `.team-founder` and `.team-support-stack` on `mock-index.html`, `lp/`, and `iblp/`, which were not converted.

To rebuild them, re-extract from the prospectus and re-run the normalisation. The raw cutouts are the `<img>` inside each `.adv-bleed .a` tile on the board-of-advisors page.

It replaced two weaker things, both worth not rebuilding:

- `.team-support-stack` on the landing pages, which showed Rajat and Rajiv only. The intro claimed a board of seven and the section showed two, with no explanation of why those two, and it cropped both cutouts badly in a narrow card.
- `.advisor-grid` on `team.html`, a flat photo-above-text card that read as a directory listing.

`.advisor-card`, `.advisor-photo`, `.advisor-body`, `.advisor-cred`, `.board-strip`, and `.board-mini` are all retired. `.team-support-stack` remains in `main.css` but no page uses it.

## The founder card

`.team-founder.is-wide` on `index.html` and `team.html` is built to the same rule as the counsel wall below it: a pre-normalised cutout on a solid ground with the alma mater's mark top right. `founder/sanjay.webp` comes off the same pipeline as `counsel-portraits/`, so his head lands at the same width and the same height in the frame as every advisor's.

The ground is `--forest-soft`, Core-lift. Core-deep was tried first and vanished into the section, which is Core, taking the card's left edge with it. Crimson was tried second and lost: the source photo carries a red NDTV microphone that fights it, and it would have put the founder in Harvard's colour directly above a board already in Harvard's colour. A lighter slate reads as a panel, keeps the founder in Blue Ocean's palette, and still carries a white mark at 9:1.

Stacked below 860px the panel turns landscape, and a 3:4 cutout cropped to `cover` loses the head. Below that width the portrait switches to `contain` on a 300px floor, so he sits centred on the slate with ground either side.

`.team-founder.is-wide` carries a `min-height` of `clamp(330px, 32vw, 430px)`. Without it the card collapses to content height and reads as a squat byline banner rather than the section that carries the founder-led positioning.

### The record replaced the badges

`.team-creds` is a two-column list of qualification over institution, sitting under a rule in the space the card used to leave empty. It replaced `.team-inst-badges`, five Google favicons at 38px, which at that size rendered as three indistinguishable crimson blobs, and which claimed affiliations with the University of Toronto and SEWA Bharat that appear nowhere else on the site.

The four entries are the ones the milestones on `founder.html` support: MPA Harvard Kennedy School, PhD Jawaharlal Nehru University, India Country Director at the Harvard Mittal South Asia Institute, and author of *Katihar to Kennedy*. **upGrad is a documented 2022 milestone and is deliberately not in this list**, because no usable upGrad mark exists in the repo and the list is four entries wide. If a mark turns up, it belongs here.

`.team-inst-badges` and `.team-inst-badge` stay in `main.css`. `mock-index.html`, `lp/`, and `iblp/` still use them for Sanjay, Rajat, and Rajiv in `.team-support-stack`, and those pages carry their own copies of `main.css`.

`.team-li-btn` lost LinkedIn's `#0a66c2` for `--forest-strong`. A platform blue chip beside the name was the one colour on the card that belonged to neither palette. The change applies to every card that carries the button, including the landing pages.


## The admits wall

`.universities` is the second component ported from the prospectus, taken from its full-bleed logo spread. It is used by `index.html`, `results.html`, `mock-index.html`, `lp/`, and `iblp/`, all carrying the same thirty tiles under the `Admits / Where students go.` heading.

Each tile is a solid block of that university's own colour with its white knockout mark centred, set gutterless so thirty admits read as one field of colour rather than thirty cards. Marks live in `uni-logos/`, extracted from the prospectus base64, with copies in `lp/uni-logos/` and `iblp/uni-logos/` because those folders are self-contained. The colour is passed per tile as `--tile`, the same custom property `.program-tile` uses.

No caption sits under a tile. Every mark is a wordmark or a crest-and-name lockup, so the tile names itself; the full name ships as `alt` text.

It replaced a bordered grid of Google favicons beside a short name, which put a 16px icon upscaled to 52px next to real wordmarks elsewhere on the same page and made the wall look sourced rather than earned. It also meant thirty requests to `google.com/s2/favicons` on every page load.

Three things hold it together, and all three are load-bearing:

- **The logo box.** Each mark sits in a fixed `82% × 54%` box with `object-fit: contain`. Aspect ratios run from about 2:1 (Columbia's crest) to 8:1 (Cornell's wordmark). A wide mark is held by the width, a tall one by the height, and both land at the same optical weight. Capping only one axis makes half the wall look shrunken.
- **The marks are absolutely positioned.** Otherwise an image's intrinsic height feeds the grid's row sizing, one row grows past the tile's `aspect-ratio` height, and every tile in that row leaves a band of Surface under it. Out of flow, the row height comes from `aspect-ratio` alone and the rows stay equal.
- **A one-pixel shadow bleed.** `box-shadow: 0 0 0 1px var(--tile)` in the tile's own colour closes the hairline seams left by sub-pixel column widths. The container clips the overhang.

Column counts step 6 / 5 / 3 / 2, and the ladder lives with the component rather than in the shared width blocks. Only counts that divide thirty are usable: four across leaves a two-tile orphan row, which on a gutterless mosaic reads as a rendering fault rather than a layout.

## The landing pages are generated

`lp/` and `iblp/` are **`index.html` with a different hero, and nothing else.** Same proof numbers, same method story, same outcomes rail, same team, same counsel wall, same admits wall, same right-fit block, same footer. The hero is the only part that is theirs: it carries the consultation form where `index.html` carries the framed campus picture.

That was always the intent. It stopped being true because it was maintained by hand. By the time the builder was written, `index.html` had a framed hero, a scrolling press strip, a retuned wash and a rebuilt hero measure that neither landing page had; `lp/main.css` was 2,240 lines behind `main.css`; the landing pages had no counsel wall at all; and their form was still the two-step version that `start.html` had already replaced.

### What is generated

Six files, none of them hand-edited:

```
lp/lp.html      lp/index.html      lp/main.css      lp/next-steps.html
iblp/iblp.html  iblp/index.html    iblp/main.css    iblp/next-steps.html
```

The named file and `index.html` in each folder are byte-identical. The named one is what campaigns link; `index.html` is what makes the bare directory URL serve the same page.

Three sources feed the build:

- **`index.html`** — everything below the hero
- **`next-steps.html`** — the submitted page, generated per landing folder with its own thank-you event
- **`tools/landing-hero.html`** — the hero, in three marked sections. `@style` is appended to `index.html`'s inline style so it wins on anything both set, `@markup` replaces the `.hero-grid` and leaves the press strip under it alone, `@script` goes in before `</body>` after `school-fees.js`
- **`tools/build-landing-pages.py`** — the transforms, and the `PAGES` list of per-page values

Run it after any change to `index.html`, `next-steps.html`, `main.css`, or the hero partial:

```
python3 tools/build-landing-pages.py
```

### The transforms, and why each exists

- **Nav links, actions and the mobile panel are hidden in CSS, not stripped from the markup.** The header keeps one shape across all four pages, and a change to `index.html`'s nav cannot break the build.
- **`start.html` links become `#formCard`.** The form is already on the page.
- **Every other site link becomes absolute** to `https://blueoceanedu.com/`, because a landing page is often served on its own hostname. **The build fails on any relative `.html` link it does not recognise**, which is the check that would have caught the four `case-studies/` links that were about to ship dead.
- **Assets are copied, not linked.** `main.css`, `school-fees.js`, `back copy.png` and every logo folder go into both directories. The landing folders are served self-contained and nothing in them may reach up to the repo root. The two exceptions are `../ocean-ember.css` and `../brand/favicon.svg`, which the pages climb for.
- **Missing assets warn, they do not fail.** `index.html` ships four dead references inside the archived student-stories section; a build that refuses to run until an unrelated archived section is cleaned up is a build nobody runs.

### The four strings that differ

`lp` and `iblp` differ in the title, the GA4 pageview event, the GA4 thank-you event, the h1, and the `form_source` on the lead payload. Nothing else. **A fifth difference belongs in the `PAGES` list, never in a generated file.**

### The form

Both landing pages run the same three-step form `start.html` runs: contact, then school and board off the `school-fees.js` city list, then destination ranking and funding. On submit the lead posts to the same Apps Script webhook with the fee columns resolved, goes into `sessionStorage`, and the page redirects to `next-steps.html`.

It replaced a two-step form that took a typed school name and resolved no fees.

**The hero partial carries its own copy of the form's CSS, and that copy drifts.** Three rules went missing from it and only the third was cosmetic:

- `.field[hidden] { display: none; }`. `.field` is `display: grid`, which beats the UA rule for the attribute, so the three fallback fields behind Other city, Other school and Other board all rendered whether or not they were revealed. Step 2 on both landing pages opened with `Which city`, `Which school` and `Which board` sitting empty under the questions meant to reveal them, 246px of fields nobody was asked to fill, and picking Other city never hid the school dropdown. The step measured 778px against `start.html`'s 532px.
- `.field .field-label` beside `.field label`. The ranking grid has no single control to point a `<label for>` at, so its label is a span, and without the second selector it was the one label on the form set as 16px body copy.
- `.field .label-note` rather than `.field label .label-note`, so the note inside that span is styled too.

**When something changes in `start.html`'s form, diff the selector lists before assuming the partial has it.** The two are meant to be the same form and the build cannot tell that they are not:

```
python3 - <<'PY'
import re
sel = lambda css: {' '.join(m.group(1).split())
                   for m in re.finditer(r'([^{}]+)\{[^{}]*\}',
                                        re.sub(r'/\*.*?\*/', '', css, flags=re.S))
                   if not m.group(1).strip().startswith('@')}
S = open('start.html').read(); H = open('tools/landing-hero.html').read()
a = sel(S[S.find('<style>'):S.rfind('</style>')])
b = sel(H[H.find('<!-- @style -->'):H.find('<!-- @markup -->')])
print('\n'.join(sorted(a - b)))
PY
```

`.consul-*` selectors are expected in that output: those are `start.html`'s own hero and its step list, which the landing hero does not have. Anything starting `.field`, `.form-`, `.rank-`, `.role-`, `.btn-`, `.phone-` or `.booking-` is drift.

The in-page success block is where the scheduler opens. It is empty markup until submit, so it costs no request unless a family gets that far.

## Analytics and the conversion

**One analytics block, on every page**, between the `<!-- @analytics -->` sentinels at the top of every `<head>`: GA4 `G-2STB24PJGQ` and Meta pixel `754270597536586`. Before this, the pixel and GA4 were on `lp/` and `iblp/` only. `index.html`, `start.html` and every sub-page had no tracking at all, which meant the pixel never saw the main site's traffic and could not attribute anything that started there.

The only line that differs per page is the dataLayer pageview event: `SITE_PAGEVIEW` at the root, `EVALUATION_PAGEVIEW` on `lp`, `IB_EVALUATION_PAGEVIEW` on `iblp`, and the matching `*_THANKYOUPAGE` on the submitted pages. `tools/build-landing-pages.py` swaps that one string. **Keep the block byte-identical everywhere else** or the swap silently stops matching and both landing pages ship with the site's own event name.

### The funnel has two steps and two events

On submit the scheduler opens inside the form card and the hero drops to one column via `.is-booking`, which is how it has always worked. `next-steps.html` comes after the booking, not instead of it.

| Step | Fired where | Meta | dataLayer |
| --- | --- | --- | --- |
| Form submitted | in place, on the page holding the form | `Lead` | `LEAD_SUBMITTED` |
| Slot booked | `next-steps.html`, on arrival | `Schedule` | `BOOKING_COMPLETED` |

**The Lead fires in place, and that is deliberate.** There is no new URL at submit, and there should not be: a family that fills the form and never picks a slot is still a lead, so waiting for a distinct URL to count it would silently drop every one of those. A standard event fired from JS is what Meta expects here; a URL-based custom conversion is not the only way to define one.

**Calendly announces the booking.** It posts `calendly.event_scheduled` to the page the instant a slot is taken and the family moves on by itself. That message is the only route to `next-steps.html`, so the booking is counted exactly once. A time-on-page or focus heuristic would count people who never booked.

Both events live in `lead-events.js`, loaded by `start.html`, both landing heroes and all three copies of `next-steps.html`, and copied into `lp/` and `iblp/` by the builder. One file rather than three inline copies, because three hand-maintained copies of a conversion is three chances for one to stop firing quietly.

Two guards on both events:

- **No stored lead, no event.** Anyone can open `next-steps.html`; only someone who submitted arrives with a payload in `sessionStorage`. A direct visit fires `PageView` and nothing else.
- **One event per lead per step**, keyed to the lead's own `timestamp`. A refresh, a back-and-forward or a second tab would otherwise each count again, while a genuine second submission carries a new timestamp and still counts.

If `sessionStorage` is denied the event fires anyway. Counting a lead twice is the cheaper failure.

`fbq` carries `content_name` (the `form_source`), `content_category` (the grade), and an `eventID` of `<step>-<timestamp>` so a server-side Conversions API event for the same step can be deduplicated against it later.

Verified in a browser with `fbq` stubbed: one `Lead` and one `Schedule` from a full run, doubles suppressed on repeat calls, and nothing at all with no stored lead.

### `next-steps.html` after the booking

The page opens on `Call Booked` rather than `Submission Received`, and its status line promises the calendar invitation instead of a callback. It carries no scheduler of its own — the booking is done by the time anyone arrives.

### The booking card says one thing

The success card carried a `Consultation Requested` heading with a thank-you line, and directly under it a second heading asking for a time. It said the thing was finished and then asked for one more step. It is now a single block: `Pick your time`, and one sentence that carries the receipt and the ask together. The tick mark went with the heading it belonged to.

**The scheduler frame is taller on a phone, not shorter.** It was `640px` dropping to `560px` under 640px wide, on the usual assumption that a phone needs less. A scheduler stacks the month grid above the slot list on a narrow frame, so it needs more: at 560 it scrolled inside its own iframe, which on a touch screen fights the page scroll. The opening values are `700px` and `900px`, and Calendly's own height message overrides both.

**And it runs to the card edges on a phone, with no `min-width`.** Calendly's own snippet carries `min-width: 320px`, which is a recommendation about their content, not a width the frame can hold: inside a card whose opening is 276px it stops the frame shrinking, so the frame overflows to the right and `.consul-form-card { overflow: hidden }` cuts it off. The clipped strip is the right-hand side — the times column and the confirm button — so the scheduler rendered in full and could not be used, on every phone under about 400px. It is full-bleed there now, `.form-success` padding down to 18px with a matching negative margin, which also buys the scheduler 40-50px it did not have.

**`#formCard` carries `scroll-margin-top: 90px`.** `.site-header` is sticky, so scrolling the card to the top of the viewport put its heading underneath it and the first thing a family saw after submitting was the sentence under a `Pick your time` that was not on screen.

### Knowing when the booking happens

Calendly posts a message to the page the instant a slot is taken:

```
{ event: 'calendly.event_scheduled', payload: { ... } }
```

`BOEvents.mountCalendly` listens for it and sends the family to `next-steps.html`. Two conditions before it acts: the message origin has to be `calendly.com`, and the event name has to be exactly that one. `calendly.page_height` is the only other message it uses, to size the frame.

**This is why the scheduler was changed.** The Google appointment schedule it replaced was a cross-origin iframe that publishes nothing, so the booking was invisible from the page and the only way to know was to ask the calendar for it afterwards. `apps-script/lead-sheet.gs` answered `?booked=<email>` from the operations calendar over JSONP and `BOEvents.watchBooking` polled it every few seconds. That worked only if the family booked under the address they typed, cost about 48 Apps Script executions per lead against a quota shared with every form post, and needed a Calendar scope the deployed web app had never been granted. All of it is gone. A deployment still carrying the old `doGet` simply answers a question nothing asks.

**The scheduler is mounted, not written into the page.** `#bookingFrame` is an empty div with the booking URL on `data-calendly-url`; `mountCalendly` loads `widget.js` on demand and calls `initInlineWidget` into it. Two things follow from mounting it at submit rather than at page load. Nothing is requested from Calendly for a visitor who never fills the form. And the family's name and address are known by then, so the scheduler opens with both already in it — `widget.js` sends prefill by postMessage rather than in the URL, so the values never appear in the iframe `src`.

`utm_source` carries `form_source`, `utm_campaign` carries the target verdict. The lead row and the Calendly booking are two records of the same family, and those are what let them be matched later.

**There is a path for `widget.js` not arriving.** After six seconds `mountCalendly` builds the iframe itself, with `embed_domain` and `embed_type=Inline` on the URL — those two parameters are what make Calendly post its messages to the parent window, so the booking is still detected on that path. Prefill goes in the query string there, since there is no widget to hand it to.

**Nothing sits under the scheduler.** The card ends at the frame: the `I have booked my slot` button, the `If nothing here suits you` line, and the `.btn-booked` and `.booked-note` rules behind them are gone from `start.html` and from `tools/landing-hero.html`, and the click handler with them.

It was there as a fallback, and removing it removes the case it covered. If `calendly.event_scheduled` does not reach the page — a locked-down browser, an extension, a change at Calendly's end — the family books a real slot and the card does not move. The slot is in the calendar and the team still sees it; what is lost is the confirmation screen and the count, since `Schedule` and `BOOKING_COMPLETED` both fire on arrival at `next-steps.html` and nobody arrives. That is the trade, made deliberately. **Do not restore the button without asking**, and if bookings in Calendly start running ahead of `BOOKING_COMPLETED` in GA4, this is the first thing to look at.

### Analytics must never be able to stop a booking

Every `BOEvents` call is wrapped in a `try`. This is not defensive habit, it is a fix: the `<script src="lead-events.js">` tag went missing from `start.html`, `BOEvents` was undefined, and the bare call threw on the line immediately before the scheduler is revealed. `Request Consultation` posted the lead to the sheet and then did nothing visible at all — no scheduler, no confirmation, no error. A lead that lands in the sheet but never gets a slot is a far worse outcome than an uncounted event, so the event is always the thing that gives way.

`check_scripts_present` fails the build if a page calls `BOEvents` without loading `lead-events.js`, so the tag cannot go missing quietly a second time.

### The build fails on an unbalanced brace

`check_css_balance` counts braces in the hero partial's `@style` and refuses to build if they do not match. An unclosed rule does not error in a browser, it silently eats every rule after it: a missing `}` on a `@media (max-width: 640px)` block took out the entire tail of the landing hero's style and left the booking button rendering as an unstyled browser default. The partial is assembled by slicing other files, so this is a class of bug worth a guard rather than a careful eye.

## What the site does not use

`unused/` holds 322 files that no page reaches, at their original paths. 622MB
of the repo, most of it the brochure project and its Neue Haas Grotesk trials.
`unused/README.md` lists what is in it and why.

The most recent additions are the **masters the served assets were built from**,
archived when the site moved to WebP and WOFF2: `back copy.png`,
`Untitled design.png`, the two `institution-*.jpg`, the fifteen
`blue-profile-arch/` and `admits-blue/` SVGs, and the nine `fonts/NHG*.otf`.
Those are not dead weight, they are the only lossless copies left, and
*Performance and asset weight* says to rebuild from them rather than from the
served file. `exec-team/` and `hero-logos/`, which the two logo `build.py`
scripts read, were already here.

The list came from `tools/find-unused.py`, which walks outward from the 18 pages
the site actually serves and follows every `src`, `href` and `url()` until
nothing new appears. **Reachability, not filename search.** `admits-green/` and
`admits-blue/` share every basename, so grepping for `adya.svg` finds a hit
either way; and `mock-index.html` is itself unreachable while being the only
thing left pointing at half the green theme. Both read as live to anything that
greps, which is how five superseded folders survived a theme change.

Also removed: 84 files under `lp/` and `iblp/` that were copies of those
folders, left from before the two pages were generated. The builder no longer
copies any of them.

The tool exits non-zero while any page references a file that is not there. It
does now: `anushka_cambridge.png`, `bhakti.png`, `manya_brown.png` and
`prateek_harvard.png` are the four success-story photographs, referenced from
`index.html`, both landing pages and the four case studies, and present nowhere
in the repo. That gap predates the archive and no file in `unused/` fills it.

## The press strip

`.trust-band` sits at the foot of the hero on `index.html`, `mock-index.html`, `lp/`, and `iblp/`, under the label `In print, and on air`. It is the admits wall's colour rule applied to media marks, with one difference that carries the whole component: **the admits wall gives every tile the institution's own colour, and the press strip gives every tile the same one.** Thirty universities in thirty colours read as a field of achievement. Eight mastheads in eight brand colours read as a banner ad.

Structure is `.trust-band` → `.trust-inner` (the Core panel, a flex row) → `.trust-head` (a fixed 236px column holding `.trust-label` plus `.trust-note`) → `.trust-wall` (the viewport) → `.trust-track` (the moving rail) → sixteen `.trust-tile`, being the eight marks twice. The ground is Core on the hero's Core-deep, which is what separates the panel without a second colour.

**`.trust-band` takes `--max` first and pads inside it,** the same order `.hero-grid` uses. Padding an unbounded band and capping the panel within it made the strip a full `--pad` wider than the hero content on each side, so it overhung the h1 above it by 56px at desktop width.

### From an 8-tile wall to a 62px feed

It was a 4 × 2 grid of 3.2:1 tiles, gutterless, each mark centred at 66% of its box. Eight small marks in about 210px of panel, which made the closing note of the hero its heaviest object. It is now one 62px band: the label holds a fixed left column and the marks scroll past it. Below 720px the panel stacks, because at 236px of a 400px panel the label leaves no feed to run.

`.trust-track` carries the set twice and `@keyframes trust-marquee` travels exactly `-50%` of the track's own width, so the second set arrives where the first started and the loop has no seam. **That holds at any tile count, as long as the markup keeps duplicating the set exactly once.** `.trust-wall` masks both ends with a `linear-gradient` so a mark fades rather than appearing and vanishing on a hard edge, and `.trust-inner:hover` pauses the animation.

This is a return to a component that was removed once, so the difference matters. The original marquee ran **the outlets' own logos**: eight brand colours and eight cap heights in a 34px strip, no per-mark sizing, the whole thing `aria-hidden` because the duplicate marks made it unreadable to a screen reader. This one keeps everything the wall was built for. The marks are still the white knockouts from `press-logos/`, still optically sized per mark by `--mark`, and only the duplicate set is `aria-hidden`, so the first eight keep real `alt` text and are read once each. `prefers-reduced-motion` stops the rail and turns `.trust-wall` into an `overflow-x: auto` scroller, so the duplicate set is reachable rather than stranded off-panel.

**Do not re-add the outlets' own colours here, and do not drop `--mark`.** Those were the two faults that made the first marquee fail; the motion was not one of them.

### The marks are pre-built knockouts

`press-logos/` holds the white knockouts, with copies in `lp/press-logos/` and `iblp/press-logos/` because those folders are self-contained. `press-logos/build.py` regenerates all of them from `exec-team/`, which stays in the repo as the source.

They are not CSS filters. `filter: brightness(0) invert(1)` looks like it should do this in one line, and it does for the five marks that ship on transparency. Three do not: Hindustan Times, The Times of India, and the Harvard Mittal lockup ship on an opaque plate, and a filter turns a plate into a white slab. The build keys each plate out on the modal luminance of its opaque pixels rather than on pure white, because two of the three sit on `#F7F7F7`, and it samples the mode rather than a corner pixel because one of them carries a one-pixel transparent border that reads as black.

Two marks needed their own handling:

- **Penguin** is a filled orange oval with a black bird and a white belly. Knocked out on alpha it becomes a white blob. The build erodes the oval to a ring, keeps the dark bird, and drops the belly, which is how the reversed colophon is drawn anyway.
- **The Indian Express** is the one vector source, and its `viewBox` is `924 × 641` around a masthead occupying `750 × 75` of it. Left alone, `object-fit: contain` fits the empty box and the mark renders at an eighth of its neighbours. The build recolours the fills and tightens the `viewBox` in the same pass.

### `--mark` is not optional

A fixed box plus `object-fit: contain` normalises the *bitmap*, not the *mark*. Forbes and NDTV fill their bounding box edge to edge; the Penguin colophon is an outline, and the Times of India lockup stacks an ornament over a small wordmark. Fitted to one box, the first two read twice the weight of the last two, and the wall looks like a mistake.

Each tile therefore carries `--mark` inline, the same way `.university` carries `--tile`, and it multiplies the `76% × 23px` box. The values are tuned from the ink area each mark actually covers once fitted, not from its bounding box. Current set: NDTV 0.78, Times of India 1.22, Hindustan Times 0.97, The Indian Express 1.05, Mint 0.95, Business Standard 1.08, Forbes 0.90, Penguin 1.45. **Adding a mark means measuring it, not guessing.** They carry over unchanged from the 4 × 2 wall, because they are ratios of ink to box and both terms scaled together.

The box is height-bound rather than width-bound, so every masthead lands on the same cap height instead of every mark reaching the same width.

### The tile is a fixed box, not a fraction

`134 × 62`, dropping to `112 × 54` below 720px. A scrolling rail has no column count to divide into, so the divisibility rule the 4 × 2 wall lived by is gone with it: the strip takes any number of marks now, and adding one costs 134px of rail rather than a new row. What it must not lose is the duplicate. The set has to appear exactly twice for the `-50%` travel to loop cleanly.

### What is deliberately not on this wall

The Harvard Mittal South Asia Institute. It is an affiliation, not coverage, and it is already stated on the founder card in `.team-creds`. It is also a three-line lockup that is illegible at tile size, where the rest are single-line mastheads. The knockout is built and sits in `press-logos/harvard-mittal.png` if it is ever wanted somewhere with room for it.

## The alumni strip

`.hero-alumni` sits in the hero copy column above the press strip and takes the same treatment at inline scale: one Core ground, five marks knocked out in white, from `alumni-logos/`. It was a cream pill carrying the marks in their own colours, which put two crimson shields, a red wordmark and a blue crest in a 34px row directly above a second multi-coloured strip. Two credibility panels in one hero, in seven brand colours between them.

`alumni-logos/build.py` regenerates all five from `hero-logos/`, which stays as the source. Three of them are shields with white detail inside a crimson field, and an alpha knockout turns a Harvard shield into a white blob with the VERITAS books gone. Every mark is therefore keyed on luminance: **opaque and not near-white becomes mark, opaque and near-white becomes a hole.** That one rule covers the shields, the plated HBS lockup, and the flat red and blue wordmarks alike, which is why this script is shorter than `press-logos/build.py` rather than longer.

**The label sits above the marks, not beside them.** Set inline, it ate a third of a 604px panel and left five marks about 70px each, at which width the Kennedy School shield renders 23px wide. Stacked, each mark gets about 112px. The `≤860px` media query that used to do this stacking is now just padding. The press strip below it made the opposite call, and the reason is width: it has 1136px to spend on a label column and this panel has 620px.

`--mark` applies here for the same reason it does on the press strip, and `.logo-wide` and `.logo-seal` are gone. They were two buckets approximating in three steps what a measured per-mark value does exactly. Current set: HBS 0.70, Kennedy School 0.93, Harvard 0.73, MIT 0.65, IIT Kharagpur 1. All values sit at or below 1 and the box is `88% × 28px`, so a mark can never spill into its neighbour's column.

Copies live in `lp/alumni-logos/` and `iblp/alumni-logos/`. Those pages carry the strip twice each, in both their hero and their mid-page repeat.

## The hero frame

`.campus-frame` holds both pictures, and it is built as a frame rather than a bleed. Three members, outside in: the moulding (`.campus-frame`, Core ground, `--line-dark` hairline, 12px radius, 14px mat), the mat's inner edge (`.campus-frame::before`, `inset: 7px`, a 10% paper hairline), and the picture plate (`.campus-plate`, `overflow: hidden`, 6px radius). Both pictures live inside the plate.

The student cutout used to sit outside all of it, 48px past the right edge and 74px below the bottom, with the campus photo inset `26px 0 96px 0` to leave her room. That read as two objects with two edges, and the cutout's hard waist crop ended in mid-air over the page background. Inside the plate the waist crop lands on the plate's bottom edge, which is where a cutout is meant to end, the same rule the counsel-wall portraits follow.

**The frame carries a fixed `aspect-ratio: 4 / 5`,** capped at `max-width: 520px` and centred in its column. It was `position: absolute; inset: 0` inside a `min-height` box, which meant the frame's proportions were whatever the grid row happened to be that viewport: a 620px slab on desktop, a 430px one on a phone, neither of them a shape anyone chose. A fixed ratio makes it the same object on both, which is the whole point of framing it.

**The campus photo runs untinted.** The `.campus-frame::after` scrim and the `saturate(0.86) contrast(0.98)` pass on the photo are both gone. The hero's own wash of the same picture sits behind the section, and dimming the framed copy left it reading as a darker version of the background rather than the one place the photograph is shown at full strength. The frame is the only place the picture is clean, and the wash is the only place it is tinted.

One selector to keep: **`.campus-frame img:not(.student-figure)`** carries the `100% / cover` sizing. Plain `.campus-frame img` matches both and stretches the cutout to fill the plate.

`.student-figure` steps its width at 860px and 640px. The 640px block also thins the mat to 10px and drops the cap to 420px, because a 335px plate should not lose an eighth of its width to moulding.

## The hero wash and its scrim

`.hero::before` lays `back copy.png` over the section at `mix-blend-mode: luminosity`, which contributes the photograph's luminance and keeps Core-deep's hue. **It runs at `opacity: 0.46`.** At the `0.13` it started on, the campus read as a texture rather than as a building. It went to `0.32` and then to `0.46`, where the dome, the colonnade and the winter trees all read.

That brightness has to be paid for, because the sky is the bright end of the picture and it sits directly under the h1. `.hero::after` is the scrim: **one flat `color-mix` at 82% Core-deep, over the whole hero, with no gradient and no media query.**

It got there by elimination. It was a `96deg` ramp, then a `180deg` ramp on phones, then a flat value that cleared at 70% to leave the far side untouched. **Every partial version had the same fault:** the picture came through at different strengths in different places, so a line of type was legible in one band and sitting on a lit dome in the next. Uneven ground under type is what makes it hard to read, more than any single value is. One value everywhere means the copy has one background. 72% is where cream at 18px first holds on the brightest part of the picture; 82% is where it sits, clear of that margin, which leaves the campus as a ground rather than a subject. The frame is where the picture is the subject.

There is no breakpoint on it either. A phone and a desktop show the same picture at the same strength, and nothing about a narrower screen changes what type needs underneath it.

**If the wash goes up again, this goes up with it.** They are one control in two properties, and moving `opacity` alone is what puts cream type back on a lit sky.

**The scrim is what the opacity is spent against.** Both went up together, and raising the wash alone is what puts cream type on a lit sky. Both layers are `z-index: 0` and `.hero-grid` is `z-index: 1`, so **the scrim darkens the hero's ground only; the framed photograph sits above it and is unaffected.** That is what keeps the tinted copy and the clean copy of the same picture distinct at any opacity, and it means raising the wash never touches the frame.

Both rules are inline in `index.html`, not in `main.css`, because the wash is that page's hero and no other page carries it.

## The hero copy runs on one measure

Three elements in the copy column used to stop in three different places down the right-hand side: the h1 at `720px`, the lede at `630px`, and the alumni strip at whatever the grid column gave it. **`.hero-copy` now caps at `620px` and the children inherit it.** One right edge, three stacked blocks.

The rest of the tightening is vertical rhythm and it is all in `main.css`:

- `.hero-grid` gap `48px` → `34px`, padding `44/36` → `32/26`, columns `0.98fr / minmax(420px, 0.78fr)` → `1fr / minmax(400px, 0.72fr)`
- `.hero-lede` margin-top `28px` → `18px`, size `20px` → `18px` at `1.5`
- `.hero-alumni` margin-top `42px` → `26px`; the label pad drops to `10/16/9`, the slot from `60px` to `48px`, the mark cap from `34px` to `28px`
- `.hero h1` line-height `0.92` → `0.94` with `-0.015em` tracking, which is the trade a tighter column asks for

**Neither `.hero` nor `.hero-grid` carries a viewport minimum any more.** `.hero` held `min-height: calc(100vh - 74px)` and `.hero-grid` held `calc(100vh - 250px)` with `flex: 1 0 auto`, so on any screen where the content came in under a full viewport the difference was handed to the row and spent as slack. On a 900px display that was about 50px of empty ground between the alumni strip and the press strip, and it grew with the screen.

The frame is now what sets the height: 4:5 at up to 520px wide is 612px, plus the row's own padding and a 63px strip. On a laptop that lands a little short of one screen, which reads as intentional and gives the section below it a visible edge.

**The breathing room lives in the padding, at the section's edges.** `.hero-grid` opens with `clamp(44px, 5vw, 72px)` and closes with `clamp(26px, 3vw, 40px)`; `.trust-band` carries `clamp(40px, 4.5vw, 64px)` under the strip. That is deliberate space at the top and bottom of the hero, which is a different thing from the slack the viewport minimums used to open in the middle of the row. The `≤920px` block no longer overrides the top value, so a phone scales down the same clamp rather than jumping to a flat 24px. **Do not put the viewport minimum back.** A hero pinned to `100vh` with content that does not fill it has to spend the difference somewhere, and centred rows spend it as a gap in the middle.

The alumni strip keeps its label **above** the marks while the press strip moved its label beside them. Both were tried both ways. At `620px` the label eats a third of the panel and leaves five marks about 70px each, at which width the Kennedy School shield is 23px wide. The press strip has `1136px` to spend and can afford the column.

## Two Ocean Ember overrides had to move

Both are the trap `ocean-ember.css` already documents, hit for real:

- `.trust-inner` and `.hero-alumni` were in the list of panels set to `background: var(--surface)`. Both are Core grounds now, so they had to come out of that list or each renders as a Surface slab with white marks on it, which is to say blank.
- `.trust-label` and `.hero-alumni-label` were grouped at `color: var(--core)`, which is Core on Core. Both are now reversed, and both move up to Text Bold, because a Medium cut at 11px recedes on Core whatever its contrast ratio measures. `.trust-note` takes `--label-on-core`.

---

## Performance and asset weight

The site is a static multi-page build with no bundler, so nothing compresses an
asset on the way out. **Every file in the repo is served exactly as it sits**,
which makes the encoding of each one a decision rather than a build setting.

The homepage once shipped **9.0MB** and measured a **41.8s LCP** on
PageSpeed's mobile profile. It ships 1.76MB now. Almost all of that was four
mistakes, and all four are the kind that reappear the moment someone drops a
new asset in:

| | Was | Now |
|---|---|---|
| `back copy.png`, the hero photograph | 4.2MB PNG | `hero-campus.webp` 525KB, `hero-campus-1200.webp` 195KB |
| `Untitled design.png`, the student cutout | 1.3MB PNG | `hero-student.webp` 101KB |
| `blue-profile-arch/*.svg`, the seven pillar cards | 36MB | 972KB WebP |
| `admits-blue/*.svg`, the outcome photographs | 6.1MB | 864KB WebP |
| `fonts/NHG*.otf`, nine faces | 647KB | 175KB WOFF2 |
| `press-logos/` + `alumni-logos/` | 332KB | 160KB |

Everything superseded is in `unused/` at its original path, because each one is
the master the served file was built from. **Rebuild from the master, never
from the served copy**, which is already lossy. That is the same rule
`harvard-hall.webp` has always carried.

### A .svg is not necessarily a vector

`blue-profile-arch/6.svg` was 14.5MB. It was a `750 × 750` wrapper around a
`3876 × 2579` base64 PNG, and so were the other fourteen files in those two
folders: a photograph, a luminance mask of the same photograph, and a
`feColorMatrix` and clip path assembling them into a wave-shaped cutout. The
extension said vector and the payload was a raster at four times the size it is
ever displayed at.

They are re-rendered rather than unpacked, because the mask and the clip path
are what produce the shape and reproducing that by hand is how you ship a
subtly different picture. Headless Chrome renders the SVG at `1200 × 1200` on a
transparent ground, and `cwebp -q 84 -alpha_q 100` encodes it:

```
<img> at 1200x1200 in a page with a transparent body
  -> --screenshot --default-background-color=00000000
  -> cwebp -q 84 -m 6 -alpha_q 100 -sharp_yuv
```

**Check any new `.svg` over about 100KB for a `data:image` before trusting the
extension**, and check what the browser actually paints it at. `.service-card-svg
img` is `object-fit: cover` on a card no wider than about 600px, so 1200 is
already a 2x source.

### Quality is measured, not eyeballed

Every encode above was checked before it shipped, and the numbers are the
reason these settings and not lower ones:

| | PSNR | Note |
|---|---|---|
| `hero-campus.webp` q82 | 34.4 dB | q78 was 456KB at 33.3 dB, not worth the 70KB |
| `hero-student.webp` q86 | 38.4 dB over the opaque region | alpha is bit-exact, `-alpha_q 100` |
| WOFF2 faces | lossless | glyph count and cmap identical to the OTF, all nine |
| `press-logos/`, `alumni-logos/` | lossless | all twelve measured at max chroma 0, so `LA` is exact |

PSNR on a cutout has to be masked to `alpha > 0`. Measured over the whole
frame, `hero-student.webp` reads 27 dB, because RGB under a fully transparent
pixel is undefined and the encoder is free to put anything there. That number
means nothing and it is not a quality problem.

### The photograph ships at two sizes and the viewport picks

The campus photograph is used twice on `index.html`: full-bleed as the hero
wash (`.hero::before`), and inside the 4:5 frame. Both resolve to one file per
viewport, so the second use is a cache hit:

- **Above 900px**, `hero-campus.webp` at 1920px
- **900px and below**, `hero-campus-1200.webp` at 1200px, 195KB against 525KB

It is a `<picture>` with a `<source media>` rather than `srcset` and `sizes`,
and that is deliberate. A `sizes` value describes the **layout box**, and this
box lies about what the image costs: the plate is 492px wide and crops a 16:9
photograph into a 4:5 frame, so the source is scaled to about **2.2x the box**
before anything is cropped away. `sizes="492px"` would pick a file less than
half the resolution the crop actually spends. The media switch states which
file each viewport gets instead of inferring it from a number that does not
describe the situation.

`.campus-plate picture { display: block; width: 100%; height: 100% }` in
`main.css` is load-bearing. A `<picture>` is inline by default and would size
to the image rather than to the plate, which drops the `<img>` out of the
`100% / 100%` box under it.

**The institution fader takes the 1200px copy, on every viewport.** It is a
decorative cross-fade in a card about 360px tall, and pointing it at the 1920px
file meant a phone downloaded both sizes: 1200 for the hero and 1920 for a card
nobody looks at.

### Resource hints, and why they sit outside the sentinels

Every page opens the same way, **before** the `<!-- @analytics -->` block:

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="preconnect" href="https://www.googletagmanager.com">
  <link rel="preconnect" href="https://connect.facebook.net">
  <link rel="preload" href="fonts/NHGDisplay-Bold.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/NHGText-Roman.woff2"  as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="fonts/NHGText-Medium.woff2" as="font" type="font/woff2" crossorigin>
```

Three things about that block are not preference:

- **It is outside the sentinels.** The block between `<!-- @analytics -->` and
  `<!-- /@analytics -->` has to stay byte-identical on every page or the
  builder's one-line pageview swap stops matching. These lines also differ per
  folder depth, which is the other reason they cannot live inside it.
- **`charset` and `viewport` lead the document.** They used to sit *after* the
  analytics block, which is 1.4KB of script, so `<meta charset>` was found
  outside the first 1KB and the parser had grounds to restart.
- **Three faces, not nine.** Display Bold sets every heading, Text Roman the
  body, Text Medium the nav and the labels. The other six load from
  `ocean-ember.css` when something needs them. That file is the **last**
  stylesheet in the head, so without these the first-screen faces are not
  discovered until it parses.

`localise()` in the builder rewrites `href="fonts/` to `href="../fonts/`, the
same climb `ocean-ember.css` makes. `fonts/` is deliberately **not** in
`ASSET_DIRS`: `url()` inside `ocean-ember.css` resolves against the stylesheet,
which is at the root, so both landing folders already share one copy of the
faces. A preload left relative would fetch `/lp/fonts/` and 404, and it would
fail *quietly*, because the real load still comes from the stylesheet.

`start.html` additionally preconnects to `assets.calendly.com` and
`calendly.com`. The scheduler is still mounted on submit and nothing is fetched
from Calendly before then; warming the connection just takes about 300ms off
the mount at the one moment a family is waiting on it.

### The phone must not zoom, pan, or reflow

Three separate iOS behaviours, three separate answers, none of them the
viewport tag.

**Focus zoom.** iOS Safari zooms the whole viewport whenever a text input,
select, or textarea is focused with a computed `font-size` under 16px, and it
does not zoom back out on blur. The form ran at 14.5px, and the phone prefix at
13.5px, so the first tap on First Name zoomed the page in and left it there for
the rest of the form: every later field sat outside the viewport and had to be
panned to, and the Calendly frame that opens on submit inherited the same
zoomed viewport. Both copies of the form CSS now carry:

```css
@media (pointer: coarse) {
  .field input, .field select, .field textarea,
  .phone-row .phone-prefix-select { font-size: 16px; }
  .rank-chip { font-size: 14px; }
}
```

**The fix is the font size, not the viewport.** `maximum-scale=1` and
`user-scalable=no` stop the zoom too, by taking pinch-zoom away from every
visitor for the whole page. That is an accessibility failure, Lighthouse scores
it as one, and it is not needed here. The viewport tag stays
`width=device-width, initial-scale=1.0` on every page and **must not gain
`maximum-scale` or `user-scalable`.**

Scoped to `pointer: coarse`, not to a width: an iPad in landscape is 1024px
wide and zooms exactly the same way, while a 900px desktop window does not zoom
at all and keeps the 14.5px the design was drawn at. `.rank-chip` is a
`<button>` and never triggers focus zoom; it moves to 14px for the thumb.

**Sideways pan.** `html, body { overflow-x: clip; max-width: 100% }` in
`main.css`. **`clip`, never `hidden`** — `overflow-x: hidden` makes the element
a scroll container, and a `position: sticky` child stops sticking to the
viewport once it has one, which would unstick the site header, the sticky
services column, and `method.html`'s pyramid all at once.

Note that `clip` also makes `scrollWidth` report the padding box, so
**`document.documentElement.scrollWidth` can no longer detect overflow on this
site.** To check, lift the clip first:

```js
document.head.insertAdjacentHTML('beforeend',
  '<style>html,body{overflow-x:visible!important;max-width:none!important}</style>');
document.documentElement.scrollWidth        // now the true extent
```

The designed horizontal rails (`.trust-track`, the outcome rail, the counsel
carousel) are wider than the viewport on purpose and are not overflow. Any
audit has to skip elements inside an ancestor whose `overflow-x` is `auto`,
`scroll`, `hidden`, or `clip`.

**Text inflation.** `-webkit-text-size-adjust: 100%` on `html`. iOS enlarges
the text of any block it decides is too narrow, per block, so two columns of
the same copy come back at two sizes. This is not `user-scalable`; pinch-zoom
is untouched.

**Tap delay.** `touch-action: manipulation` on `a, button, input, select,
textarea, label, summary, [role="button"]`, which drops the ~300ms the browser
holds a tap in case a second one arrives to double-tap-zoom.

### The knockout marks are `LA`, not `RGBA`

`press-logos/build.py` and `alumni-logos/build.py` cap the long side at
**320px** and save `mark.convert("LA")` with `optimize=True`. Both strips sit
in the hero, so this is critical-path weight, and both were paying for it
twice: 600px sources for a `134 × 62` tile, in four channels for a mark that
has one. Every visible pixel is white where there is ink and transparent where
there is not, and the one mark that keeps a dark detail, Penguin's bird, is
grey rather than coloured. Measured across all twelve, **max chroma is 0**, so
`LA` carries them exactly.

`object-fit: contain` in a fixed box means source resolution changes nothing
about layout, so `--mark` and every tuned value carry over untouched. 320px is
over 3x the longest box dimension, which covers a 3x phone and stops there.

**Both scripts read from `unused/`**, where `exec-team/` and `hero-logos/` were
archived. They take their paths relative to the working directory, so run them
from a directory where `exec-team`, `hero-logos`, `press-logos` and
`alumni-logos` all resolve, rather than editing the paths to reach into the
archive.

### What is left, and what it would cost

Both remaining items are deliberate, not oversights:

- **~440KB of third-party JavaScript** (`gtag/js` 186KB, `fbevents.js` 103KB,
  the pixel's config 150KB). Both tags are already `async` so neither blocks
  render, but they are most of the main-thread work before first paint. Cutting
  it means changing when the pixel initialises, and *Analytics and the
  conversion* is emphatic that the lead must never be what gives way. **Do not
  defer these without deciding what happens to the `Lead` event first.**
- **`main.css` is 149KB raw, 30KB gzipped**, and render-blocking along with
  `ocean-ember.css`. Minifying saves about 16KB *after* compression, and the
  file is a documented source whose comments carry most of the reasoning in
  this document. The honest fix is critical CSS, which is a real refactor.

### Measuring it

`pagespeed.web.dev`'s public API is quota-limited and will refuse anonymous
runs. Lighthouse is the same engine:

```
npx lighthouse@12 https://blueoceanedu.com/ --only-categories=performance \
  --form-factor=mobile --screenEmulation.mobile --throttling-method=simulate
```

**Serve the site with gzip when comparing locally, or the numbers are fiction.**
`python3 -m http.server` sends nothing compressed, which puts 149KB of `main.css`
on the wire instead of 30KB and invents an "Enable text compression" opportunity
worth 1.2s that does not exist in production. Local runs also understate image
cost badly, because there is no real network between the two processes: the
homepage measured 41.8s LCP live and 5.8s from `localhost` on the *same* 9MB
build. **Page weight is the honest local number; take LCP from a real run.**

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
- `720px` — the press strip stacks: the label column becomes a head band above the scrolling marks
- `600px` — finer: footer collapses, outcome rows simplify

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

**Two versions of this section ship, deliberately.** Do not "fix" one to match the other.

`index.html` and `mock-index.html` carry the original **seven pillars** (Academic Project Development, Competition Strategy, Community Impact, Unique Skill Development, Language and Argumentation, Admissions Strategy, Ongoing Mentorship). This is the landing-page version and it stays.

`method.html` carries the **five pyramid layers**, in build order:

1. Diagnosis, "Measure First, So the Plan Fits the Actual Student"
2. Foundations, "Keep Every Door Open Before You Choose One"
3. Distinction, "Build the Work That Makes the File Rare"
4. Presentation, "Present Years of Work Without Wasting a Word"
5. Management, "Hold the Whole Plan Together, Week After Week"

The two index-family pages must stay in sync with each other. `method.html` is independent.

**The two versions no longer share a layout either.** On the index family the copy is sticky on the left and a column of illustration cards scrolls past it on the right. On `method.html` that is reversed and the cards are gone: each layer carries its own copy and scrolls on the left, and the right holds the pyramid alone, sticky, lighting the layer being read. The reversal is scoped to a `.services-pyramid-right` class on the section, overridden from `method.html`'s own `<style>` block, so `main.css` stays the index-family layout and neither generated landing page is affected.

The section has no separate init call. On the index family the inline sticky-services script derives everything from DOM order over `.service-text-block` and `.service-card`; on `method.html` it reads DOM order over `.services-pyramid-right .service-row` instead. Either way, changing the row count is a markup-only edit. `.services-dot` and `#servicesActive` are referenced defensively by the index-family script but no page contains them.

### Restoring this section from git

The seven-pillar markup lives in `git show HEAD:index.html`. Two things come back with it that Ocean Ember had removed, and both must be stripped again in the same edit:

- `src="green-profile-arch/N.svg" data-blue="blue-profile-arch/N.svg"` reverts to the old theme-swap pattern. Pin `src` to the blue variant and delete `data-blue`, or a stale `boTheme` value in a returning visitor's `localStorage` brings the green assets back.
- The original pillar copy contains eight em dashes, which the content rules ban. They are currently still there on the three index-family pages, because the request was for the original section verbatim.

### The scroll-linked pyramid (`method.html` only)

`.pyramid` is the whole sticky right column, and it is the only visual the section has. The band matching the row nearest the viewport centre lights up: `setActive(index)` sets `data-active` on `#methodPyramid` and CSS does the rest. The same index dims every row but the one being read, which is what replaced the card images as the section's sense of movement. Layer 4 is Management, which lights the dashed outline instead of a band.

It cannot reuse the Spike legend's fills, because that section is on Surface and this one is on Core, where a Core band would vanish. Every band sits dim; the active one lifts to Support, and the apex to Highlight with its number flipped to Ink. One colour lit at a time, so position carries the meaning rather than four competing hues. Hidden below 981px, where the sticky column goes with it and the rows drop to a single full-width stack separated by rules.

`scroll-story.js` is linked by `index.html` and `method.html` but `initVerticalScrollStory` is never called. `start.html` dropped the link when its services section was removed. The section's motion comes from CSS plus the inline script.

---

## Ocean Ember brand layer (`ocean-ember.css`)

`ocean-ember.css` carries the Ocean Ember identity for the entire site. Structure, layout, and copy are untouched everywhere. Only the palette, the type, and the mark are new. See the Ocean Ember section in `docs/brand.md` for the colour and type rules it implements.

### Coverage

| Area | Pages |
|---|---|
| Root | `index`, `method`, `results`, `founder`, `fit`, `team`, `start`, `mock-index` |
| `lp/` | `index`, `lp`, `next-steps` |
| `iblp/` | `iblp`, `index`, `next-steps` |
| `case-studies/` | `manya`, `prateek`, `anushka`, `bhakti` |

Not covered: `mockup.html`, a standalone scratch file with about 1,700 lines of bespoke inline CSS that links no shared stylesheet and is not in the nav. `email/intro-enquiry.html` is also untouched, because email is a different medium with no webfonts, no CSS mask, and images that are often blocked.

### How it works

Every page links `ocean-ember.css` **last in `<head>`**, after `main.css` and after the page's own inline `<style>`. `main.css` and `case-study.css` are almost entirely token-derived and share the same token names, so remapping the tokens re-skins every section of every page at once.

Link order matters and so does selector shape. The pages carry an older `html[data-theme="blue"]` palette block in their inline styles, at specificity (0,1,1). The token block in `ocean-ember.css` is written as `:root, html[data-theme="blue"], html[data-theme="green"]` so it matches that specificity and, being later, wins. Linking the file before the inline `<style>` would lose.

`url()` inside the file resolves against the stylesheet, not the document, so one copy at the repo root serves every folder depth. Root pages link `ocean-ember.css`; `lp/`, `iblp/`, and `case-studies/` link `../ocean-ember.css`.

The file does five things, in this order:

1. `@font-face` for Neue Haas Grotesk Display and Text, from `fonts/`
2. The six Ocean Ember hex values, then `main.css` and `case-study.css` token names mapped onto them
3. Type corrections, because Neue Haas has no italic display cut
4. Colour corrections where a token served two roles that Ocean Ember separates
5. The mark, masked onto the existing markup

### Token map

| `main.css` token | Ocean Ember |
|---|---|
| `--paper` | Surface |
| `--ink` | Ink |
| `--forest` | Core |
| `--forest-strong` | Core deepened toward Ink |
| `--moss` | Support |
| `--lime` | Signal |
| `--clay` | Highlight |
| `--serif` | NHG Display |
| `--sans` | NHG Text |

`--lime` carried both the primary button fill and accent text on dark grounds. Ocean Ember splits these: the button keeps Signal with Ink text at 4.9:1, and accent text on Core moves to `--support-light`, a Support tint mixed toward Surface.

### Do not color-mix near-neutrals in oklch

`color-mix(in oklch, ...)` between two low-chroma colours drifts hue and renders visibly pink. Surface plus Ink produced mauve section backgrounds and pink chart tracks. The surface steps are therefore stated as hex, not mixed:

```
--surface-lift:  #DDD5C8
--surface-deep:  #D3C9B9
--surface-rule:  #CDC3B3
```

Any `main.css` rule that mixes `--paper` with another near-neutral is overridden with a flat value in the mock. Mixes involving Core, Support, or Signal are chromatic enough to stay safe in oklch. Where a neutral pair genuinely needs mixing, use `in srgb`.

There are thirteen of these mixes in `main.css`. The ones this page renders are overridden: `.numbers-proof`, `.section.paper-low`, `.proof-stat-card`, `.proof-stat-stack`, `.institution-proof-card`, `.acceptance-card`, `.outcome-card`, `.hero-alumni`, `.trust-inner`, `.team-person`, `.advisor-card`, and `.service-card`. The rest sit in archived or other-page sections. Any new section pulled onto this page needs the same check, because the drift is subtle on a small swatch and obvious on a full-width panel.

`.advisor-card` was added to that list after it shipped mauve: it copied `.team-person`'s `color-mix(in oklch, var(--paper) 76%, var(--paper-low))` background, and `.team-person`'s override did not cover the new class. **Any new card that copies a background from an existing card must be added to the override list in the same commit.** Borders that mix `--line` with `transparent` are safe and were measured, so they need no override.

Two more on-dark traps, same family as the eyebrow list:

- `--muted` is an on-Surface value. On Core it lands dark on dark. `.section.dark .problem-src` answers this for the source lines; any new small print on a dark ground needs the same treatment.
- `.proof-stat-stack` holds exactly one card (`6x`), and `.proof-stat-card strong` is unscoped Signal. The stack briefly carried four figures and every one of them went orange. If it grows again, scope Signal to the headline card first. See the Signal rule in `docs/brand.md`.

### Type conversions

- Headings use `--serif` with `font-style: normal`. Every italic serif moment becomes Display Bold, upright.
- Weight mapping: Display Bold at 600 to 700, Display Black at 800 to 900. Text Medium at 500 to 600, Text Bold at 700 to 900.

### Display never goes below 20px

Every heading rule in `main.css` is 23px or larger except `.footer h3` at 13px. That one is handed back to `--sans` and set as a label. Display at 13px is visibly a different typeface from the Text around it, which reads as a leftover font rather than a deliberate choice.

Before adding a heading selector to the Display list, check its `font-size`. If it is under 20px it belongs in the label scale, not in Display.

### Label scale

All Text Bold, all uppercase. A label set thin at wide tracking recedes no matter what its contrast ratio measures, so weight carries these, not colour. Tracking loosens as size drops, not as it grows.

| Use | Size | Weight | Tracking | Colour |
|---|---|---|---|---|
| Section eyebrow (`.eyebrow`, `.numbers-proof-kicker`) | 16px | 700 | 0.11em | Core on light, Support tint on Core |
| Footer column label (`.footer h3`) | 14px | 700 | 0.14em | Surface at 88% |
| Inline label (`.method-kicker`, `.team-role`) | 14px | 700 | 0.14em | Support tint on Core, Support on light |

`.eyebrow` and `.numbers-proof-kicker` were 28px to 43px italic serif before Ocean Ember. They are labels now, so the display weight moved to the headline underneath them.

### Footer hierarchy

Four levels, told apart by brightness and letterform rather than size alone:

| Level | Size | Colour |
|---|---|---|
| Column label | 12px, Text Bold, tracked caps | Surface 88% |
| Links | 14px, Text Medium | Surface 78% |
| Prose and address lines | 14px, Text Roman | Surface 56% |
| Fine print | 12px | Surface 54% |

Two bugs this replaced. The `h3` column headings were 13px while the links under them were 14px, so the heading was smaller than its own list. And plain address `<li>` text had no size rule at all, so it inherited 16px from the body and became the largest thing in the column. Links are now the brightest text in the list, so what is clickable is legible as clickable.

### The mark on the page

The pages still contain the old circle-and-triangle placeholder SVG and a "Blue Ocean / Education" text wordmark. Neither is edited. `ocean-ember.css` hides the inner `<svg>` and the wordmark, then masks `.brand-mark` with `brand/logo-lockup.svg`:

```css
background-color: currentColor;
mask: url("brand/logo-lockup.svg") no-repeat center / contain;
```

The mask keeps the geometry exact at any size, takes any colour, and needs no markup change on any page. It works over `file://` as well as HTTP. It sets in Surface on Core in both the header and the footer, which is the approved reversed pairing.

The case studies carry a text-only brand instead of `.brand-mark`, so the same mask is applied to `.case-nav .brand` with the text pushed off with `text-indent`.

The `.brand-word` text stays in the DOM as a visually hidden span for screen readers, since the lockup carries the wordmark.

### Mark sizes

| Where | Mark | Size |
|---|---|---|
| Nav, above 720px | Lockup | 40px tall, 187px wide |
| Nav, 720px and below | BO mark | 38px tall, 74px wide (34 by 66 below 640px) |
| Footer | Lockup | 46px tall, 215px wide (40 by 187 below 920px, 36 by 169 below 640px) |

The nav swaps to the BO mark on a phone because the lockup would drop under its 120px minimum once the nav tightens. The footer keeps the lockup at every width, since there is room for the full name.

### Size marks through `.brand-mark`, never by class alone

`main.css` pins `.brand-mark svg` to 34px square at 920px and 32px square at 640px. Those rules were written for the old 32×32 placeholder mark. `.brand-mark svg` is specificity (0,1,1) and beats a bare `.brand-lockup` at (0,1,0), so a class-only rule loses at exactly the widths that matter and both marks get crushed into a square.

Every mark rule in the mock is written as `.brand-mark .brand-lockup` or `.brand-mark .brand-bo`, at (0,2,0), so it wins. Media queries add no specificity, so source order alone will not save a class-only rule here.

### Assets

| Path | What |
|---|---|
| `ocean-ember.css` | The brand layer. Linked last in `<head>` on every page |
| `brand/logo-lockup.svg` | Mark plus wordmark. Site default |
| `brand/logo-bo.svg` | The BO mark alone |
| `brand/logo-b.svg` | The B alone |
| `brand/favicon.svg` | The B in Surface on a Core rounded square |
| `fonts/NHG*.woff2` | Neue Haas Grotesk, trial licence. The `.otf` masters are in `unused/fonts/` |

Source of truth is `Blue Ocean new assets/`. The repo copies exist so the page can reference short paths.

### Eyebrows on dark grounds

`main.css` colours `.team-section .eyebrow`, `.services-section .eyebrow`, and `.cta-section .eyebrow` with `--lime`, which under Ocean Ember resolves to Signal. Signal is not a label colour. Several other dark sections carry a plain `.eyebrow` with no `.light` modifier, which lands Core on Core and disappears entirely.

Both are answered by one rule listing every dark container, at equal specificity and later in the cascade. If a new dark section is added, its `.eyebrow` must join that list or it will render invisible.

### What the rebrand drops

The green and blue theme toggle, and the `data-blue` image swapping that went with it. Ocean Ember is one palette.

The toggle markup and its JS are left in place so nothing throws; `ocean-ember.css` hides the button. The `data-blue` attributes were removed and each `src` pinned to its blue variant, so a stale `boTheme` value in a returning visitor's `localStorage` cannot bring the green assets back. Pages now point directly at `blue-profile-arch/`, `admits-blue/`, and `exec-team-pics-blue/`.

The Google Fonts `<link>` and its preconnects were removed from every page. `main.css` and `case-study.css` still name EB Garamond and Bricolage Grotesque in their `:root`, but those declarations are overridden and nothing requests them.

### Known issues, inherited

Neither of these was introduced by the rebrand.

- ~~Pages overflow horizontally below about 420px.~~ Answered in `main.css` by the `overflow-x: clip` rule on `html, body`. Measured at 390px, 360px and 320px on `index.html`, `start.html` and `lp/` with the clip lifted, and the true `scrollWidth` equals the viewport at every one. See *Performance and asset weight* → *The phone must not zoom, pan, or reflow*.
- `manya_brown.png`, `prateek_harvard.png`, `anushka_cambridge.png`, and `bhakti.png` are referenced by the hidden `#stories` section in `index.html` and by the case studies, but have never existed in the repo.

Fixed in passing: the case studies linked `../mock.html`, a filename that no longer exists, from both the brand and the "Back to student stories" link. Both now point at `../index.html`.

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

- No em dashes, use commas, periods, or restructure
- No AI filler: no "holistic," "passionate," "transformative," "tailored," "curated"
- No generic claims without data
- Student outcomes: real names, real admits, real scholarships (approximate, INR)
- Metrics come from the prospectus, never from an older doc. The admit-chart footnote is `.acceptance-source`: "General admit rates are the figures each university publishes for its most recent cycles. Blue Ocean rates are the admit rates of our students applying to that university across recent cycles."
- Quoted testimony is a record and is never edited to fit the voice rules. The parent quotes contain "journey" and "tailored", both on the avoid-list, because that is what the parents wrote. The avoid-list governs Blue Ocean's own prose only.

## Known copy still to reconcile

Not blocking, but wrong if shipped as-is:

- `mockup.html` still says "Seven disciplines" and uses `hello@blueoceanedu.in`. It is a scratch file, links no shared stylesheet, and is not in the nav.
- `index.html` and `mock-index.html` carry eight em dashes each in the restored seven-pillar copy. They came back with the original section and are a known open item, not an oversight. `method.html`, `results.html`, `team.html`, `fit.html`, and `founder.html` are clean.
- The prospectus names Palakshi, Randitya, Seema, Shaurya, and Shreejeet in its student wall. Their admits are not confirmed in `docs/product.md`, so they are not yet in site copy.
- Photo captions on `founder.html` that name public figures (Anand Mahindra, the Union Education Minister, the Chief Justice of India) come from the source filenames in `brochure variations/dr-sanjay-assets/`, not from anything verifiable in the image. Confirm before the page goes public.

---

## Print prospectus

`brochure.html` and `brochure.css` are deleted. The current print piece is the 26-page 2026-27 prospectus in `brochure variations/`, which is untracked scratch and is **the source of truth for every metric on the site**:

| Path | What |
|---|---|
| `brochure variations/blue-ocean-brochure.html` | The prospectus. ~19MB, images inlined as base64 data URIs |
| `brochure variations/Blue Ocean Brochure.pdf` | Rendered output, plus Blue Theme and Ocean Ember variants |
| `brochure variations/dr-sanjay-kumar.html` | Standalone founder page, own palette and fonts, not used by the site |

It was built against the site's **older oklch green palette**, so nothing ports without re-tokenising: `--forest` to Core, `--moss` to Support, `--lime` to Signal, `--clay` to Highlight, `--paper` to Surface. Its geometry is mm and pt on a fixed A4 page and its headings run 6.6pt to 10.6pt, well under the 20px Display floor, so ported headings become labels.

To read it, strip the data URIs first, or the file is unusable:

```
python3 -c "import re; s=open('brochure variations/blue-ocean-brochure.html',encoding='utf-8',errors='ignore').read(); \
open('/tmp/b.html','w').write(re.sub(r'data:[^\"\')]{200,}','DATAURI',s))"
```

Assets already lifted out of it: `proof-logos/` (12 summer programs + 4 journals, extracted from base64), `uni-logos/` (30 white knockout university marks for the admits wall, with copies in `lp/` and `iblp/`), `counsel-portraits/` and `counsel-logos/` (the seven advisor cutouts and their three institution marks), `founder/sanjay.webp` (composited from the two layers inside `exec-team-pics-blue/sanjay.svg`, photo plus luminance mask, then normalised), `founder/commencement.jpg` (the page-3 rail portrait, cropped to 2:3 off the top of a 1040x4413 source whose lower two thirds are a baked fade to the print ground), `founder/cred-mason.jpg` and `founder/cred-mpa.jpg` (the two documents on the same page), `parent-voices/`, `founder/`, `exec-team-pics-blue/{ashokmittal,adwait,amit,ishira,sunita}.svg`, `admits-blue/anushka.png`.

## Screenshotting these pages

Several sections size themselves in viewport units: `.service-card` is `min-height: clamp(460px, 68svh, 640px)` on the index family, and `method.html`'s layer rows are `min-height: 52svh`. A tall headless window makes those units enormous, so a `--window-size=1440,6000` capture shows one section and then thousands of pixels of nothing. Neutralise the spacers in a throwaway copy rather than concluding the page is broken:

```
python3 -c "s=open('method.html').read(); \
open('_shot.html','w').write(s.replace('</head>','<style>.service-card{min-height:120px!important}.services-pyramid-right .service-row{min-height:0!important;opacity:1!important}</style></head>',1))"
```

---

## When to Update This File

Update `docs/site.md` when:
- A new section is added to the page
- A layout or CSS convention changes
- New responsive breakpoints are introduced
- Content rules are revised
