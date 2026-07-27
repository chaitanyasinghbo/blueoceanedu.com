#!/usr/bin/env python3
"""Build the Ocean Ember brochure from the blue source.

Three things change, in this order:

1. Colour   every oklch() in the document is remapped onto the six Ocean Ember
            colours from Brand Guidelines v1.0, then the :root token block is
            replaced outright so the named tokens land exactly on the hexes.
2. Type     Bricolage Grotesque and EB Garamond are dropped. Neue Haas Grotesk
            Display and Text are embedded as base64 OTF and wired to the
            guide's scale: Display for 20px and up, Text for everything below.
3. Mark     the old compass glyph and the typeset wordmark are replaced with
            the real lockup, BO and B vectors, set in one colour at a time.
"""
import base64
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "blue-ocean-brochure-blue.html")
ASSETS = os.path.join(HERE, "Blue Ocean new assets")
FONTS = os.path.join(ASSETS, "neue-haas-grotesk-font-fanily")
OUT = os.path.join(HERE, "blue-ocean-brochure-ocean-ember.html")


# ---------------------------------------------------------------- 1 · colour

OKLCH = re.compile(r"oklch\(\s*([\d.]+)%\s+([\d.]+)\s+([\d.]+)\s*(?:/\s*([\d.]+)\s*)?\)")

# Ocean Ember, converted from the guide's hexes
#   Core #243747  L 32.8  C .038  H 245      Surface   #E5DED3  L 90.3  C .017  H  79
#   Support #5089B5  L 60.9  C .090  H 243   Ink       #13171B  L 20.2  C .010  H 248
#   Signal #E0600E  L 64.1  C .178  H  45    Highlight #F49904  L 75.8  C .166  H  68
H_CORE, H_SURFACE, H_SIGNAL, H_HIGHLIGHT = 245, 79, 45, 68


def transform_color(L, C, H):
    if C < 0.001:
        return L, C, H                                   # true neutral, leave it
    if 190 <= H <= 225:                                  # aqua accent -> Highlight
        return L, min(C * 1.05, 0.175), H_HIGHLIGHT
    if 225 < H <= 300:
        if C >= 0.06:                                    # the real blues
            # dark grounds settle on Core's chroma, lighter ones on Support's
            return L, C * (0.42 if L < 45 else 0.62), H_CORE
        if C >= 0.028:
            # muted mid-tones: light ones are greys on a dark ground, so they
            # follow Surface; dark ones are still structure, so they follow Core
            if L > 55:
                return L, C * 0.45, H_SURFACE
            return L, C * 0.50, H_CORE
        # papers and hairlines -> Surface, which is warmer than the blue paper was
        return L, min(C * 3.0, 0.020), H_SURFACE
    if 20 <= H < 66:                                     # warm clay -> Signal
        return L, min(C * 1.10, 0.180), H_SIGNAL
    if 66 <= H < 100:                                    # stream lane -> Highlight
        return L, C, H_HIGHLIGHT
    if 100 <= H < 200:                                   # stream lane -> Support
        return L, C * 0.75, H_CORE
    return L, C * 0.95, H_SIGNAL                         # stream lane -> Signal


def recolor(m):
    L, C, H = float(m.group(1)), float(m.group(2)), float(m.group(3))
    a = m.group(4)
    L2, C2, H2 = transform_color(L, C, H)
    out = f"oklch({L2:.4g}% {C2:.4g} {H2:.4g}"
    return out + (f" / {a})" if a else ")")


TOKENS = """
/* ============ OCEAN EMBER · Brand Guidelines v1.0, July 2026 ============
   Core #243747 · Support #5089B5 · Signal #E0600E
   Surface #E5DED3 · Ink #13171B · Highlight #F49904
   The token names below are inherited from the source file. What they hold
   is the Ocean Ember palette, one brand colour per token wherever a token
   maps cleanly onto a brand role.
   ====================================================================== */
:root{
  /* --- the six --- */
  --core:      oklch(32.8% 0.038 245);   /* #243747 */
  --support:   oklch(60.9% 0.090 243);   /* #5089B5 */
  --signal:    oklch(64.1% 0.178 45);    /* #E0600E */
  --surface:   oklch(90.3% 0.017 79);    /* #E5DED3 */
  --brandink:  oklch(20.2% 0.010 248);   /* #13171B */
  --highlight: oklch(75.8% 0.166 68);    /* #F49904 */

  /* --- working tokens --- */
  --ink:            oklch(20.2% 0.010 248);  /* Ink. Body copy, always on Surface */
  --ink-soft:       oklch(32%   0.016 248);  /* Ink, lifted, for secondary prose */
  --muted:          oklch(46%   0.018 248);  /* 4.9:1 on Surface */
  --paper:          oklch(90.3% 0.017 79);   /* Surface. The page */
  --paper-low:      oklch(87%   0.019 79);
  --paper-deep:     oklch(83%   0.021 79);
  --forest:         oklch(32.8% 0.038 245);  /* Core. Interior dark grounds */
  --forest-strong:  oklch(23%   0.030 246);  /* Core deepened toward Ink. Covers */
  --forest-soft:    oklch(42%   0.055 244);  /* Support darkened, 6.6:1 on Surface */
  --moss:           oklch(60.9% 0.090 243);  /* Support. Charts, panels, graphics */
  --moss-ink:       oklch(45%   0.075 244);  /* Support darkened, for small text */
  --lime:           oklch(75.8% 0.166 68);   /* Highlight. Accent on Core, 5.5:1 */
  --lime-low:       oklch(93.5% 0.032 74);  /* Highlight at wash strength */
  --clay:           oklch(64.1% 0.178 45);   /* Signal. Large text and graphics only */
  --signal-ink:     oklch(50%   0.155 45);   /* Signal darkened, 5.2:1 on Surface */
  --line:           oklch(80%   0.016 79);
  --line-dark:      oklch(45%   0.028 246);
  --display: "Haas Grot Disp", "Helvetica Neue", Arial, sans-serif;
  --serif:   "Haas Grot Text", "Helvetica Neue", Arial, sans-serif;
  --sans:    "Haas Grot Text", "Helvetica Neue", Arial, sans-serif;
}
"""


# ------------------------------------------------------------------ 2 · type

FACES = [
    ("Haas Grot Disp", "neuehaasgrotdisp-45light-trial.otf", 300, "normal"),
    ("Haas Grot Disp", "neuehaasgrotdisp-55roman-trial.otf", 400, "normal"),
    ("Haas Grot Disp", "neuehaasgrotdisp-65medium-trial.otf", 500, "normal"),
    ("Haas Grot Disp", "neuehaasgrotdisp-75bold-trial.otf", 700, "normal"),
    ("Haas Grot Text", "neuehaasgrottext-55roman-trial.otf", 400, "normal"),
    ("Haas Grot Text", "neuehaasgrottext-56italic-trial.otf", 400, "italic"),
    ("Haas Grot Text", "neuehaasgrottext-65medium-trial.otf", 500, "normal"),
    ("Haas Grot Text", "neuehaasgrottext-75bold-trial.otf", 700, "normal"),
]


def font_faces():
    out = ["/* Neue Haas Grotesk · trial licence. License Display and Text",
           "   before anything public ships (Brand Guidelines, p.02 and p.06). */"]
    for fam, fn, wt, style in FACES:
        b64 = base64.b64encode(open(os.path.join(FONTS, fn), "rb").read()).decode()
        out.append(
            "@font-face{font-family:'%s';font-style:%s;font-weight:%d;"
            "font-display:block;src:url(data:font/otf;base64,%s) format('opentype');}"
            % (fam, style, wt, b64))
    return "\n".join(out) + "\n"


# ------------------------------------------------------------------ 3 · mark

def svg(name, **attrs):
    s = open(os.path.join(ASSETS, name)).read().strip()
    a = " ".join(f'{k.replace("_","-")}="{v}"' for k, v in attrs.items())
    return s.replace("<svg ", "<svg " + a + " ", 1)


def logos(s):
    lock_cover = svg("logo-lockup-vector.svg", width="205", style="display:block;")
    lock_back = svg("logo-lockup-vector.svg", width="170", style="display:block;")

    # the typeset wordmark is now inside the vector, so the .brand span carries
    # the lockup alone
    s = re.sub(
        r'<span class="brand" style="color:var\(--paper\);">\s*<svg width="46".*?</span>\s*</span>',
        '<span class="brand" style="color:var(--paper);">%s</span>' % lock_cover,
        s, count=1, flags=re.S)
    s = re.sub(
        r'<span class="brand" style="color:var\(--paper\);">\s*<svg width="34".*?</span>\s*</span>',
        '<span class="brand" style="color:var(--paper);">%s</span>' % lock_back,
        s, count=1, flags=re.S)

    # the compass geometry is not ours any more. The mark takes its place, kept
    # whole and kept quiet: one colour, both counters open, nothing filled in.
    # Never cropped, because a cropped mark stops being the mark.
    b_cover = svg("logo-b-vector.svg", height="340",
                  style="position:absolute;right:14mm;top:34mm;opacity:.085;"
                        "color:var(--moss);")
    bo_back = svg("logo-bo-vector.svg", width="530",
                  style="position:absolute;left:16mm;top:152mm;opacity:.075;"
                        "color:var(--moss);")
    s = re.sub(r'<svg style="position:absolute;right:-60mm;top:-40mm;.*?</svg>',
               b_cover, s, count=1, flags=re.S)
    s = re.sub(r'<svg style="position:absolute;left:-70mm;bottom:-70mm;.*?</svg>',
               bo_back, s, count=1, flags=re.S)
    return s


# ------------------------------------------------- 4 · the identity stylesheet

IDENTITY = r"""
/* ==========================================================================
   OCEAN EMBER IDENTITY LAYER
   Neue Haas Grotesk on the guide's scale, Ocean Ember on the guide's jobs.
   Appended last so it wins the cascade over the source and the blue overlay.
   ========================================================================== */

/* ---------- the scale (Brand Guidelines, p.06) ----------------------------
   Display  Disp 75 Bold      44/48   report covers, one line only
   Headline Disp 75 Bold      28/34   page and section titles
   Subhead  Disp 45 Light     20/26   supporting line under a headline
   Label    Text 65 Medium    10/14   caps, +8 tracking
   Body     Text 55 Roman     13/20   everything readers actually read
   Strong   Text 75 Bold      13/20   emphasis inside body text
   Caption  Text 56 Italic    11/15   notes, sources, asides
   Display never goes below 20px. Light weights never below 14px.
   -------------------------------------------------------------------------- */

body{font-family:var(--serif);background:oklch(26% 0.03 246);}
.page{background:var(--paper);}

/* Headline · Disp 75 Bold. Sentence case, never caps. */
h1.display{
  font-family:var(--display);font-weight:700;font-size:22pt;line-height:1.14;
  letter-spacing:-.019em;
}
.layer h1.display{font-size:20pt;}

/* Signal underlines the one thing that matters, once a page. Nothing else
   on the page carries Signal. */
h1.display em{
  font-style:normal;font-weight:700;background:none;padding:0;border-radius:0;
  color:inherit;
  box-shadow:inset 0 -.10em 0 0 var(--clay);
}
.page.forest h1.display em,.page.forest-strong h1.display em{
  background:none;color:inherit;box-shadow:inset 0 -.10em 0 0 var(--lime);
}

/* Strong · Text 75 Bold. Emphasis inside body copy is weight, not a wash. */
p em,.lede em,.rows dd em,blockquote em,.letter em{
  font-style:normal;font-weight:700;background:none;padding:0;border-radius:0;
}
.page.forest p em,.page.forest .lede em,.page.forest .rows dd em,
.page.forest-strong p em,.page.forest-strong .lede em{background:none;}
#problem .fnotes em{font-style:italic;font-weight:400;}   /* Caption · case names */

/* Subhead · Disp 45 Light, never under 14px */
.lede{font-family:var(--display);font-weight:300;font-size:12.4pt;line-height:1.44;
      letter-spacing:-.004em;}

/* Label · Text 65 Medium, caps, +8 tracking */
.kicker{
  font-family:var(--sans);font-weight:500;font-size:7.5pt;letter-spacing:.08em;
  text-transform:uppercase;color:var(--forest);
}
.page.forest .kicker,.page.forest-strong .kicker{color:var(--lime);}
/* the letterhead head rule, borrowed: Core hairline, last fifth in Signal */
.kicker::after{
  flex:0 0 26mm;height:.6pt;opacity:1;
  background:linear-gradient(90deg,var(--forest-soft) 0 80%,var(--clay) 80% 100%);
}
.page.forest .kicker::after,.page.forest-strong .kicker::after{
  background:linear-gradient(90deg,var(--line-dark) 0 80%,var(--lime) 80% 100%);
}
.foot{font-family:var(--sans);font-weight:500;letter-spacing:.08em;}

/* Body · Text 55 Roman. Ink on Surface on light pages, Surface on Core on dark
   ones, both inherited from the page, so no colour is set here. */

/* ---------- display face on the things that are actually display sized ---- */
.bigstat .n,.pillar h3,.story .name,.lesson h3,.arc h3,.role .rn,.sig .nm,
.file .tab .nm,.stu-bleed .nm,.adv-bleed .nm,.letter .salut{
  font-family:var(--display);font-weight:700;font-style:normal;
  letter-spacing:-.016em;
}
.bigstat .n{font-size:52pt;line-height:.94;letter-spacing:-.035em;}
.pillar h3{font-size:11.6pt;}
.story .name{font-size:11.6pt;}
.letter .salut{font-size:15pt;}
.sig .nm{font-size:13pt;}

/* below 20px the Text cut carries it, per the guide */
.quote blockquote{
  font-family:var(--serif);font-style:normal;font-weight:400;font-size:11.4pt;
  line-height:1.5;
}
.quote .mark{font-family:var(--display);font-weight:700;color:var(--clay);}
.toc-row .t{font-family:var(--serif);font-weight:500;font-size:10.9pt;}
table.compare td:first-child,table.compare2 td:first-child{
  font-family:var(--serif);font-weight:500;font-size:11.4pt;}
table.fees td:first-child{font-family:var(--serif);font-weight:500;font-size:10.2pt;}

/* ---------- Signal and Highlight are rare, so give them one job each ------ */
/* key numbers carry Signal, darkened where the type is small (Signal on
   Surface is 2.7:1, which the guide reserves for 18px bold and up) */
#problem .band h3 .no,.argpage .band h3 .no,.pillar .no,.mile .yr,.letter .cont,
.toc-row .no{color:var(--signal-ink);font-family:var(--sans);font-weight:500;}
.tl .yr{color:var(--lime);}
.story .adm{color:var(--moss-ink);font-weight:500;letter-spacing:.08em;}
.page.forest .story .adm{color:var(--lime);}
table.compare td.bo{color:var(--lime);font-weight:700;}
/* the admit-rate column is Ink on Highlight, one of the guide's own pairs */
table.compare2 th.hd-bo,table.compare2 td.bo{
  background:var(--lime);color:var(--brandink);font-weight:700;}
.page.forest .bigstat .n,.page.forest-strong .bigstat .n{color:var(--lime);}

/* Callouts sit on a Soft-tinted panel with a Core edge (Guidelines, p.09).
   Highlight is a fill for charts and chips, never a whole panel of prose. */
#problem .impl,.argpage .impl{
  background:var(--paper-low);border-radius:0;
  border-left:1.2mm solid var(--forest);padding:4mm 4.2mm 4mm 5mm;}
#problem .impl .tag,.argpage .impl .tag{color:var(--signal-ink);font-weight:500;}
#problem .impl p,.argpage .impl p{color:var(--ink-soft);}

/* Marked phrases in testimonials: Signal underlines the thing that matters,
   rather than a highlighter pen laid over three sentences a page. */
mark,.tv-row mark{
  background:none;color:inherit;padding:0;border-radius:0;font-weight:700;
  box-shadow:inset 0 -.11em 0 0 var(--clay);}
#stu-voices .tv-row mark,.page.forest mark,.page.forest-strong mark{
  background:none;color:inherit;box-shadow:inset 0 -.11em 0 0 var(--lime);}
.rows dt{font-family:var(--sans);font-weight:500;color:var(--forest-soft);}
.page.forest .rows dt{color:var(--lime);}
.chip{font-family:var(--sans);font-weight:400;border-radius:.8mm;}

/* the mark sets in one colour at a time, never two inside one mark */
.brand svg{display:block;color:inherit;}
.brand svg *{fill:currentColor;}

/* ---------- size compensation ---------------------------------------------
   Neue Haas Grotesk Text has a far larger x-height and a wider set than the
   EB Garamond it replaces, so the sizes the blue overlay tuned for Garamond
   overflow these fixed A4 pages. Everything below is that correction, not a
   design choice, and it holds the original pagination.
   -------------------------------------------------------------------------- */
p{font-size:9.9pt;line-height:1.54;}
.rows dt{font-size:8.1pt;line-height:1.3;}
.rows dd{font-size:9.5pt;line-height:1.46;}
.pillar p{font-size:9.2pt;}
.pillar .no{font-size:8.8pt;}
.bigstat .cap{font-size:8.3pt;}
table.fees th{font-size:6.6pt;}
table.fees td{font-size:9pt;}
table.compare th,table.compare2 th{font-size:6.9pt;letter-spacing:.1em;}
table.compare td,table.compare2 td{font-size:10.6pt;}
table.compare2 td.bo{font-size:12pt;}
.chip{font-size:8.4pt;}
.quote .who{font-size:7.5pt;letter-spacing:.08em;}
.story p{font-size:9.2pt;}
.story .adm{font-size:7.1pt;}
.small-note{font-size:7.6pt;line-height:1.5;}
.foot{font-size:6.5pt;}
.foot .pn{font-size:8pt;letter-spacing:.04em;}
.letter p{font-size:10.4pt;line-height:1.55;}
#founder-letter .letter p{font-size:10.7pt;line-height:1.57;}
#founder-mission .letter p{font-size:10.5pt;line-height:1.54;}
.letter .cont{font-size:7pt;}
.sig .role{font-size:7.4pt;}
.mile .what{font-size:9pt;}
.mile .yr{font-size:8.6pt;}
.tl .what{font-size:9.1pt;}
#founder-letter .ph .cap,#founder-mission .ph .cap{font-size:7.1pt;}
.toc-row .no{font-size:8pt;}
#problem .impl .tag,.argpage .impl .tag{font-size:6.5pt;letter-spacing:.1em;}
#problem .impl p,.argpage .impl p{font-size:8.4pt;}
#problem .src,.argpage .src{font-size:6.3pt;}
#problem .fnotes{font-size:6pt;line-height:1.5;}
#problem .ba .ml{font-size:6.8pt;}
#problem .ba .cap{font-size:7.7pt;}
.argpage p{font-size:9.4pt;line-height:1.5;}
.argpage .lede{font-size:11.8pt;}
.argpage p[style*="font-size:10.6pt"]{font-size:9.4pt!important;line-height:1.5!important;}
#file-team .blk .bd p{font-size:9.6pt;}
#file-team .blk .bd li{font-size:9.2pt;}
#file-team .blk .hd .clk{font-size:6.9pt;}
#file-team .blk .bd .sh{font-size:6.9pt;letter-spacing:.08em;}
#file-team .bench{font-size:9.8pt;}
#fees .step p{font-size:9.2pt;}
.tv-row p{font-size:10.4pt;}
.tv-row .meta{font-size:7.5pt;}
.lesson p{font-size:9.4pt;}
.arc h3,.role .rn{font-size:10.8pt;}
.file .notes p{font-size:8.8pt;}
.file .tab .nm{font-size:11.4pt;}
.stu-bleed .nm{font-size:11pt;}
.adv-bleed .nm{font-size:11pt;}
.sg .nm{font-size:9.6pt;font-family:var(--display);font-weight:700;}
#layer-diagnosis .rows dd,#layer-distinction .rows dd{font-size:9.2pt;}
#layer-distinction .small-note{font-size:7.4pt;}
#layer-presentation .rows dd{font-size:8.5pt;}
#layer-presentation .rows dt{font-size:7.7pt;}
#layer-presentation .rows{row-gap:3.4mm;}
#layer-management .rows dd{font-size:9.3pt;}

/* the two cover statements */
#cover div[style*="font-size:40pt"]{
  font-family:var(--display)!important;font-weight:700!important;
  font-size:33pt!important;line-height:1.08!important;letter-spacing:-.028em!important;
}
#cover div[style*="font-size:40pt"] em{
  font-style:normal;font-weight:700;color:inherit;background:none;
  box-shadow:inset 0 -.09em 0 0 var(--lime);
}
#back-cover div[style*="font-size:26pt"]{
  font-family:var(--display)!important;font-weight:700!important;
  font-size:22pt!important;letter-spacing:-.02em!important;line-height:1.16!important;
}

/* Type rule: display never below 20px, so the small caption faces stay Text */
#pyramid svg text,.page svg text{font-family:var(--sans);}
"""


def main():
    src = open(SRC, encoding="utf-8").read()
    print(f"source {len(src)/1e6:.1f} MB, {len(OKLCH.findall(src))} oklch colours")

    out = OKLCH.sub(recolor, src)

    # swap the whole @font-face run for Neue Haas Grotesk
    start = out.index("@font-face")
    end = out.index("/* ============ DESIGN TOKENS")
    out = out[:start] + font_faces() + "\n\n" + out[end:]

    # the v2 block ships Fraunces and repoints --display at it. Drop both.
    out, n = re.subn(r"@font-face\{font-family:'Fraunces'.*?\}\n?", "", out, flags=re.S)
    assert n == 2, n
    out = out.replace(
        ":root{--display:'Fraunces','EB Garamond',Georgia,serif;}\n"
        "h1.display{font-family:var(--display);font-weight:540;"
        "letter-spacing:-.02em;font-size:25.5pt;}",
        "h1.display{font-family:var(--display);font-weight:700;"
        "letter-spacing:-.019em;font-size:22pt;}", 1)
    assert "Fraunces" not in out

    # replace the :root token block outright
    r0 = out.index("/* ============ DESIGN TOKENS")
    r1 = out.index("*{margin:0;padding:0;box-sizing:border-box;}")
    out = out[:r0] + TOKENS.strip() + "\n" + out[r1:]

    # a handful of colours in the source are hard-coded rather than oklch. The
    # university and press hexes are other people's brands and stay untouched;
    # these four are ours.
    out = out.replace("#f4f8fd", "#E5DED3")          # pyramid labels -> Surface
    out = out.replace("rgb(3,10,22)", "rgb(19,23,27)")        # scrims -> Ink
    out = out.replace("rgb(3 10 22 / ", "rgb(19 23 27 / ")
    out = out.replace("rgb(38,42,34)", "rgb(19,23,27)")

    out = logos(out)
    out = out.replace("<title>Blue Ocean Education · Prospectus</title>",
                      "<title>Blue Ocean Education · Prospectus · Ocean Ember</title>", 1)
    out += '\n<style id="ocean-ember">\n' + IDENTITY + "\n</style>\n"

    open(OUT, "w", encoding="utf-8").write(out)
    print(f"wrote {OUT} ({len(out)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
