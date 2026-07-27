#!/usr/bin/env python3
"""Generate lp/ and iblp/ from index.html.

The landing pages were always meant to be index.html with a different hero:
same proof, same method story, same outcomes, same team, same advisors, same
admits wall, same right-fit block, same footer. Kept by hand, they drifted --
by the time this script was written index.html had a framed hero picture, a
scrolling press strip and a retuned wash that neither landing page had, and
lp/main.css was 2,200 lines behind main.css.

So the rule is enforced rather than remembered:

    index.html            the source of everything below the hero
    tools/landing-hero.html   the one part that differs, in three marked parts
    this script           applies the per-page transforms and writes the pages

Outputs, all generated, none hand-edited:

    lp/lp.html      lp/index.html      lp/main.css      lp/next-steps.html
    iblp/iblp.html  iblp/index.html    iblp/main.css    iblp/next-steps.html

Run it after any change to index.html, next-steps.html, main.css or the
hero partial:

    python3 tools/build-landing-pages.py

Why each folder gets its own main.css and its own copy of the logo folders:
the landing pages are served as self-contained directories, so nothing in them
may reach up to the repo root. That is why the script copies rather than links.
"""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ── Per-page configuration ───────────────────────────────────────────
# lp and iblp differ in three strings and nothing else. Keeping that
# literally true is the point: a fourth difference belongs in this dict,
# not in one of the generated files.
PAGES = [
    {
        "dir": "lp",
        "named_file": "lp.html",
        "title": "Admissions | Blue Ocean Education",
        "pageview_event": "EVALUATION_PAGEVIEW",
        "thankyou_event": "EVALUATION_THANKYOUPAGE",
        "form_source": "lp_landing_page",
        "h1": "Building the most <span>unique</span> Indian profiles "
              "for college admissions",
    },
    {
        "dir": "iblp",
        "named_file": "iblp.html",
        "title": "IBDP Admissions | Blue Ocean Education",
        "pageview_event": "IB_EVALUATION_PAGEVIEW",
        "thankyou_event": "IB_EVALUATION_THANKYOUPAGE",
        "form_source": "iblp_landing_page",
        "h1": "Building the most <span>unique</span> Indian IBDP&reg; profiles "
              "for college admissions",
    },
]

DESCRIPTION = ("Blue Ocean helps ambitious Indian students develop the depth, "
               "originality, and discipline required to compete for the "
               "world's most selective universities.")

# Analytics lives in index.html now, inside the @analytics sentinels, so the
# main site and both landing pages carry one identical block. The only line
# that differs is the dataLayer pageview event, swapped below. Injecting a
# second block here instead would give the landing pages two pixels and count
# every visit twice.
PAGEVIEW_MARKER = 'dataLayer.push({ "event": "SITE_PAGEVIEW" });'
THANKYOU_MARKER = 'dataLayer.push({ "event": "SITE_THANKYOUPAGE" });'

# Site pages a landing page links out to. A landing page is often served on its
# own hostname, so every one of these has to be absolute or it 404s.
SITE_PAGES = ["method.html", "founder.html", "results.html", "fit.html",
              "team.html", "index.html"]

# Directories that exist only at the repo root and are not copied down. The
# case-study pages are linked from the student-stories section, which ships
# archived and hidden; the links are still rewritten, because a section that
# gets un-archived should not take four dead links with it.
SITE_PATH_PREFIXES = ["case-studies/"]

SITE_ORIGIN = "https://blueoceanedu.com/"

# Folders each landing directory needs its own copy of, because it is
# self-contained. Source is the repo root.
ASSET_DIRS = ["alumni-logos", "press-logos", "uni-logos", "admits-blue",
              "blue-profile-arch", "counsel-logos", "counsel-portraits"]

# Single files, same reason. `founder/sanjay.webp` is the only file used out of
# a 944KB folder, so it is named rather than copied wholesale.
#
# Both sizes of the hero photograph ship. The landing hero has no framed
# picture, but it carries the same wash, and the wash swaps to the 1200px copy
# under 900px. `hero-student.webp` is deliberately absent: the cutout lives in
# index.html's framed hero, which is the one part of the page these folders
# replace.
ASSET_FILES = ["school-fees.js", "lead-events.js",
               "hero-campus.webp", "hero-campus-1200.webp",
               "institution-harvard.webp", "institution-oxford.webp",
               "founder/sanjay.webp", "harvard-hall.webp"]


def fail(msg):
    sys.exit("build-landing-pages: " + msg)


def read_partial(path):
    """Split tools/landing-hero.html on its three markers."""
    text = path.read_text()
    parts = {}
    for name in ("style", "markup", "script"):
        marker = "<!-- @%s -->" % name
        start = text.find(marker)
        if start == -1:
            fail("%s has no %s marker" % (path.name, marker))
        start += len(marker)
        ends = [text.find("<!-- @%s -->" % other)
                for other in ("style", "markup", "script")]
        ends = [e for e in ends if e > start]
        parts[name] = text[start:min(ends) if ends else len(text)].strip("\n")
    return parts


def check_css_balance(css, where):
    """Fail on an unbalanced brace instead of shipping a swallowed stylesheet.

    An unclosed rule does not error in a browser. It silently eats every rule
    after it, which is how a missing `}` on a `@media (max-width: 640px)` block
    took out the whole tail of the landing hero's style and left a submit
    button rendering as an unstyled browser default.
    """
    stripped = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    stripped = re.sub(r'"[^"]*"', '""', stripped)
    stripped = re.sub(r"'[^']*'", "''", stripped)
    depth = stripped.count("{") - stripped.count("}")
    if depth:
        fail("%s has %d unclosed %s; every rule after it is dead"
             % (where, abs(depth), "brace" if abs(depth) == 1 else "braces"))


def check_scripts_present(html, where):
    """Every page that calls BOEvents must actually load lead-events.js.

    This is the check for the failure it did not catch the first time: the tag
    went missing from start.html, BOEvents was undefined, and Request
    Consultation threw on the line before the scheduler is revealed, so the
    button did nothing at all. The call sites are wrapped now so a repeat
    would only lose the event, but a page that silently stops counting leads
    is still worth failing the build over.
    """
    calls = "BOEvents." in re.sub(r"/\*.*?\*/", "", html, flags=re.S)
    loads = '<script src="lead-events.js"></script>' in html
    if calls and not loads:
        fail("%s calls BOEvents but never loads lead-events.js" % where)


def localise(html):
    """Transforms every generated page in a landing folder needs.

    One level down from the root, and often on its own hostname, so the two
    files a landing folder shares rather than copies have to climb, and every
    link back to the site has to be absolute.
    """
    html = html.replace('href="brand/favicon.svg"', 'href="../brand/favicon.svg"')
    html = html.replace('href="ocean-ember.css"', 'href="../ocean-ember.css"')
    # The font preloads climb for the same reason ocean-ember.css does. `fonts/`
    # is not in ASSET_DIRS: url() inside ocean-ember.css resolves against the
    # stylesheet, which is at the root, so both folders already share one copy
    # of the faces. A preload left relative would fetch /lp/fonts/ and 404,
    # which costs the preload silently rather than loudly, since the real load
    # still comes from the stylesheet.
    html = html.replace('href="fonts/', 'href="../fonts/')
    html = html.replace('href="start.html"', 'href="#formCard"')
    for page in SITE_PAGES:
        html = html.replace('href="%s"' % page, 'href="%s%s"' % (SITE_ORIGIN, page))
    for prefix in SITE_PATH_PREFIXES:
        html = html.replace('href="%s' % prefix, 'href="%s%s' % (SITE_ORIGIN, prefix))
    html = html.replace('href="#top"', 'href="%s"' % SITE_ORIGIN)

    check_scripts_present(html, "generated landing page")

    leftover = sorted(set(re.findall(
        r'href="(?!https?:|#|tel:|mailto:)([^"]+\.html[^"]*)"', html)))
    if leftover:
        fail("these links would 404 from a landing directory, add them to "
             "SITE_PAGES or SITE_PATH_PREFIXES: " + ", ".join(leftover))
    return html


def build_next_steps(source_html, cfg):
    """The submitted page, per landing folder.

    Identical to the root one but for the thank-you event name and the title.
    It is generated rather than kept by hand for the same reason the landing
    pages are: it carries the conversion, and three hand-maintained copies of
    a conversion is three chances for one of them to stop firing quietly.
    """
    html = source_html
    if THANKYOU_MARKER not in html:
        fail("next-steps.html has no @analytics thank-you marker to swap")
    html = html.replace(THANKYOU_MARKER,
                        THANKYOU_MARKER.replace("SITE_THANKYOUPAGE",
                                                cfg["thankyou_event"]), 1)
    html = re.sub(r"<title>[^<]*</title>",
                  "<title>Next Steps | %s</title>" % cfg["title"], html, count=1)
    return localise(html)


def build_page(index_html, partial, cfg):
    html = index_html

    # ── head ─────────────────────────────────────────────────────────
    if PAGEVIEW_MARKER not in html:
        fail("index.html has no @analytics pageview marker to swap; the "
             "landing pages would ship with the site's own event name")
    html = html.replace(PAGEVIEW_MARKER,
                        PAGEVIEW_MARKER.replace("SITE_PAGEVIEW",
                                                cfg["pageview_event"]), 1)
    html = re.sub(r"<title>[^<]*</title>",
                  "<title>%s</title>" % cfg["title"], html, count=1)
    html = re.sub(r'(<meta name="description" content=")[^"]*(")',
                  lambda m: m.group(1) + DESCRIPTION + m.group(2), html, count=1)

    # ── hero ─────────────────────────────────────────────────────────
    # The partial's style goes at the end of index.html's own inline style, so
    # it wins on anything they both set. The markup replaces the hero-grid and
    # leaves the trust strip below it alone, which is how the press strip stays
    # in sync without being duplicated here.
    check_css_balance(partial["style"], "tools/landing-hero.html @style")

    style_end = html.rfind("</style>")
    if style_end == -1:
        fail("index.html has no inline <style> to append the hero style to")
    html = (html[:style_end] + "\n" + partial["style"] + "\n  "
            + html[style_end:])

    grid_start = html.find('      <div class="hero-grid">')
    trust_start = html.find('      <div class="trust-band">')
    if grid_start == -1 or trust_start == -1 or trust_start < grid_start:
        fail("could not find the hero-grid / trust-band pair in index.html")
    html = (html[:grid_start]
            + partial["markup"].replace("{{H1}}", cfg["h1"])
            + "\n\n" + html[trust_start:])

    # ── scripts ──────────────────────────────────────────────────────
    body_end = html.rfind("</body>")
    script = partial["script"].replace("{{FORM_SOURCE}}", cfg["form_source"])
    html = (html[:body_end]
            + '  <script src="school-fees.js"></script>\n'
            + '  <script src="lead-events.js"></script>\n'
            + "  <script>\n" + script + "\n  </script>\n\n"
            + html[body_end:])

    # ── links ────────────────────────────────────────────────────────
    # Done after the hero is grafted in, so the hero's own markup is covered
    # by the same pass.
    html = localise(html)



    # The nav's links, actions and mobile panel are hidden by the hero
    # partial's CSS rather than stripped from the markup, so the header keeps
    # one shape across all four pages and a change to index.html's nav cannot
    # break the build. The panel is inert with nothing able to open it.
    return html


def sync_assets(target, report):
    for name in ASSET_DIRS:
        src = ROOT / name
        if not src.is_dir():
            report.append("  missing source dir, skipped: %s" % name)
            continue
        dst = target / name
        dst.mkdir(parents=True, exist_ok=True)
        for f in sorted(src.iterdir()):
            if f.is_file() and not f.name.startswith("."):
                if f.suffix.lower() in (".py", ".md", ".txt"):
                    continue
                shutil.copy2(f, dst / f.name)
    for name in ASSET_FILES:
        src = ROOT / name
        if not src.is_file():
            report.append("  missing source file, skipped: %s" % name)
            continue
        dst = target / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def audit_assets(html, target, report):
    """Warn, do not fail, on references the landing folder cannot serve.

    A warning rather than an error because index.html itself ships four dead
    references inside the archived student-stories section. The landing pages
    inherit exactly what index.html has, and a build that refuses to run until
    an unrelated archived section is cleaned up is a build nobody runs.
    """
    refs = set(re.findall(
        r'(?:src|data-blue|data-green)="([^"]+\.(?:png|jpg|jpeg|svg|webp|js))"', html))
    missing = sorted(r for r in refs
                     if not r.startswith(("http", "//", "data:"))
                     and not (target / r).exists())
    for m in missing:
        report.append("  ! %s/%s is referenced but not present "
                      "(index.html has the same gap)" % (target.name, m))


def main():
    index_path = ROOT / "index.html"
    next_steps_path = ROOT / "next-steps.html"
    partial_path = ROOT / "tools" / "landing-hero.html"
    for p in (index_path, next_steps_path, partial_path, ROOT / "main.css"):
        if not p.is_file():
            fail("cannot find %s" % p)

    index_html = index_path.read_text()
    next_steps_html = next_steps_path.read_text()
    partial = read_partial(partial_path)
    report = []

    for cfg in PAGES:
        target = ROOT / cfg["dir"]
        target.mkdir(exist_ok=True)

        html = build_page(index_html, partial, cfg)

        # The named file and index.html in each folder are byte-identical. The
        # named one is what gets linked in campaigns; index.html is what makes
        # the bare directory URL serve the same page.
        (target / cfg["named_file"]).write_text(html)
        (target / "index.html").write_text(html)
        (target / "next-steps.html").write_text(
            build_next_steps(next_steps_html, cfg))
        shutil.copy2(ROOT / "main.css", target / "main.css")
        sync_assets(target, report)

        report.append("  %s/%s and %s/index.html  (%d lines)"
                      % (cfg["dir"], cfg["named_file"], cfg["dir"],
                         html.count("\n") + 1))
        report.append("  %s/next-steps.html" % cfg["dir"])
        audit_assets(html, target, report)

    print("build-landing-pages: wrote")
    for line in report:
        print(line)


if __name__ == "__main__":
    main()
