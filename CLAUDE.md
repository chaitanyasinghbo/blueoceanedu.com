# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Static single-page landing site for Blue Ocean Education Consulting — a private admissions advisory for Indian families targeting top US/UK/global universities.

## Development

No build system. To preview locally:

```bash
npx serve .          # or: python3 -m http.server 8080
open http://localhost:8080
```

There are no tests, no linters, and no npm dependencies.

## Architecture

The entire site lives in **[index.html](index.html)** — all CSS is inline in `<style>` tags in `<head>`, all JavaScript is inline at the bottom of `<body>`. There are no external JS libraries or CSS files.

Image assets (student/university PNGs) sit in the project root alongside `index.html`.

### Page sections (in DOM order)

1. Announcement bar
2. Navigation (sticky, `z-index: 100`)
3. Hero — background image + overlay gradient + auto-scrolling ticker
4. Results — metrics + bar chart
5. Services
6. Services split CTA
7. Impact table
8. University logos
9. Student proof points
10. Press / Featured In
11. Discovery CTA
12. Testimonials
13. Counselors strip CTA
14. Footer
15. Three inline JS blocks: logo loader, photo rotator, sticky CTA bar

### Design tokens (CSS custom properties)

```
--navy: #0C2D5E     --navy-dark: #071B3E
--blue: #1557BE     --blue-mid: #1E6DD5
--blue-pale: #EBF3FD  --gold: #B8892A
--font-sans: 'Plus Jakarta Sans'   --font-serif: 'Libre Baskerville'
```

Max content width: `1240px` via `.section-inner` and `.nav-inner`.

## Impeccable skill

The `impeccable` UI design skill is installed at [.agents/skills/impeccable/](.agents/skills/impeccable/). Use `$impeccable <command>` for design work (craft, shape, polish, audit, live, etc.). It requires a `PRODUCT.md` at the project root for brand context — run `$impeccable teach` if missing.
