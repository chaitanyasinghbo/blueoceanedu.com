#!/usr/bin/env python3
"""Generate 5 art-direction variants of the Blue Ocean brochure.

Mechanism: every design color in the source is an oklch() value belonging to a
hue family (blue primary, aqua accent, warm clay, neutrals). Each variant
remaps those families to a new palette, then appends a CSS identity layer
(typography, rules, component shapes) that wins the cascade.
"""
import re, os, sys

SRC = "/Users/chaitanyasingh/Desktop/brochure variations/blue-ocean-brochure-blue.html"
OUT_DIR = "/Users/chaitanyasingh/Desktop/brochure variations/five-directions"

OKLCH = re.compile(r"oklch\(\s*([\d.]+)%\s+([\d.]+)\s+([\d.]+)\s*(?:/\s*([\d.]+)\s*)?\)")


def clamp(x, lo, hi):
    return max(lo, min(hi, x))


def transform_color(L, C, H, cfg):
    """Return new (L, C, H) for one color, per-variant config."""
    if C < 0.001:
        return L, C, H  # pure neutral (oklch(98% 0 0) etc.) — leave
    if 190 <= H <= 225:          # aqua accent family (lime / lime-low / em washes)
        h, cm, lm = cfg["accent"]
        return clamp(L * lm, 0, 100), C * cm, h
    if 225 < H <= 285:           # blue primary family
        if C >= 0.03:            # saturated: ink, forest, moss, lines-dark
            h, cm = cfg["primary"]
            nl = L
            dk = cfg.get("darken")  # (L_threshold, mult) for noir-style deepening
            if dk and L < dk[0]:
                nl = L * dk[1]
            lt = cfg.get("lighten")  # (L_threshold, mult) for terra-style lifting
            if lt and L < lt[0]:
                nl = clamp(L * lt[1], 0, 100)
            return nl, C * cm, (H if h is None else h)
        else:                    # low-chroma neutrals: paper, lines, body bg
            h, cm = cfg["neutral"]
            return L, C * cm, (H if h is None else h)
    if 20 <= H < 65:             # clay family
        h, cm = cfg["clay"]
        return L, C * cm, (H if h is None else h)
    # everything else (diagnosis stream lanes 305/152/70 etc.)
    h, cm = cfg["other"]
    return L, C * cm, (H if h is None else h)


def make_replacer(cfg):
    def rep(m):
        L, C, H = float(m.group(1)), float(m.group(2)), float(m.group(3))
        a = m.group(4)
        L2, C2, H2 = transform_color(L, C, H, cfg)
        core = f"oklch({L2:.4g}% {C2:.4g} {H2:.4g}"
        return core + (f" / {a})" if a else ")")
    return rep


VARIANTS = {
    # 1 · HERITAGE — oxblood + antique gold, old university press
    "heritage-oxblood": dict(
        title="Blue Ocean Education · Prospectus · Heritage",
        cfg=dict(
            accent=(84, 0.95, 1.0),      # antique gold
            primary=(28, 1.0),           # oxblood
            neutral=(62, 1.6),           # warm cream paper
            clay=(45, 1.0),              # bronze
            other=(None, 1.0),
        ),
        css="""
:root{--display:'EB Garamond',Georgia,serif;}
h1.display{font-family:var(--serif);font-weight:500;font-size:28pt;letter-spacing:-.008em;}
.kicker{font-weight:700;letter-spacing:.3em;}
.kicker::after{background:var(--moss);height:1.3pt;opacity:.9;flex-basis:15mm;}
.page.forest .kicker::after,.page.forest-strong .kicker::after{background:var(--lime);}
.foot{border-top-width:1pt;border-top-color:oklch(55% .12 28);}
.page.forest .foot,.page.forest-strong .foot{border-top-color:oklch(70% .09 84);}
.pillar{border-top-width:.8pt;}
.pillar:last-child{border-bottom-width:.8pt;}
.rows dt{font-family:var(--serif);font-style:italic;font-weight:600;font-size:10.2pt;letter-spacing:0;text-transform:none;}
.chip{border-radius:0;background:transparent;border-color:oklch(72% .07 62);}
.quote .mark{color:var(--moss);}
.bigstat .n{font-family:var(--serif);}
.tl .yr{font-family:var(--serif);font-weight:600;}
.sig .nm{font-family:var(--serif);}
.layer h1.display{font-size:24.5pt;}
"""),

    # 2 · MODERNIST — graphite + signal orange, Swiss international style
    "modernist-graphite": dict(
        title="Blue Ocean Education · Prospectus · Modernist",
        cfg=dict(
            accent=(42, 1.3, 0.97),      # signal orange
            primary=(None, 0.10),        # graphite (keep hue, kill chroma)
            neutral=(None, 0.30),
            clay=(42, 1.15),             # unified into the orange
            other=(None, 0.30),
        ),
        css="""
:root{--serif:'Bricolage Grotesque',system-ui,sans-serif;--display:'Bricolage Grotesque',system-ui,sans-serif;}
h1.display{font-weight:800;letter-spacing:-.02em;text-transform:uppercase;font-size:22.5pt;line-height:1.06;}
h1.display em{font-style:normal;}
.lede em,p em,.rows dd em,blockquote em{font-style:normal;}
.kicker{color:var(--ink);font-weight:800;letter-spacing:.2em;}
.kicker::after{height:2.4pt;background:var(--clay);flex:1 1 auto;opacity:1;}
.page.forest .kicker,.page.forest-strong .kicker{color:var(--paper);}
.page.forest .kicker::after,.page.forest-strong .kicker::after{background:var(--lime);}
.page *{border-radius:0!important;}
.quote blockquote{font-style:normal;font-weight:500;font-family:var(--sans);font-size:11.4pt;}
.quote .mark{display:none;}
.sig .nm{font-style:normal;font-weight:800;font-family:var(--sans);font-size:13.5pt;}
.letter .salut{font-style:normal;font-weight:700;font-family:var(--sans);}
.bigstat .n{font-weight:800;letter-spacing:-.03em;}
.story .name,.toc-row .t,table.compare td:first-child,table.fees td:first-child{font-family:var(--sans);font-weight:600;}
.foot{border-top-width:1.8pt;border-top-color:var(--ink);}
.page.forest .foot,.page.forest-strong .foot{border-top-color:var(--paper);}
/* footnote rows sit just above the foot rule: keep it hairline there */
#problem .foot,.argpage .foot{border-top-width:.4pt;border-top-color:var(--line);}
.argpage p{font-size:9.7pt;line-height:1.5;}
.argpage .lede{font-size:11.6pt;}
.argpage p[style*="font-size:10.6pt"]{font-size:9.6pt!important;line-height:1.5!important;}
.stu-bleed .nm,.adv-bleed .nm,.sg .nm,.file .tab .nm{font-family:var(--sans);font-weight:700;}
#cover div[style*="font-size:40pt"]{text-transform:uppercase;font-weight:800!important;font-size:32pt!important;line-height:1.06!important;letter-spacing:-.015em!important;}
#cover div[style*="font-size:40pt"] em{font-style:normal;}
#back-cover div[style*="font-size:26pt"]{text-transform:uppercase;font-weight:800;font-size:21pt!important;}
/* sans runs ~9% wider than the Garamond it replaces: compensate so pagination holds */
p{font-size:10.1pt;}
.lede{font-size:11.9pt;}
.rows dt{font-size:8.3pt;}
.rows dd{font-size:9.7pt;}
.pillar p{font-size:9.3pt;}
.pillar h3{font-size:11.5pt;font-weight:700;}
.letter p{font-size:10.6pt;line-height:1.58;}
#founder-letter .letter p{font-size:10.9pt;line-height:1.6;}
#founder-letter .letter .salut{font-size:16pt;}
#founder-mission .letter p{font-size:10.7pt;line-height:1.56;}
.story p{font-size:9.3pt;}
.toc-row .t{font-size:10.4pt;}
.quote blockquote{font-size:10.6pt;}
.analogy p,#pyramid .analogy p{font-size:9.8pt;}
.tv-row p{font-size:10.4pt;}
.lesson p{font-size:9.6pt;}
.lesson h3{font-size:13pt;font-weight:700;}
#layer-diagnosis .rows dd,#layer-distinction .rows dd{font-size:9.5pt;}
.layer h1.display{font-size:20pt;}
#layer-presentation .rows dd{font-size:8.5pt;}
#layer-presentation .rows dt{font-size:7.9pt;}
#layer-presentation .rows{row-gap:3.2mm;}
#layer-presentation .lede{margin-bottom:4mm;}
#layer-management .rows dd{font-size:9pt;}
#layer-management .small-note{margin-top:2mm;}
#file-team .blk .bd p{font-size:9.8pt;}
#file-team .blk .bd li{font-size:9.4pt;}
#file-team .bench{font-size:10pt;}
table.compare td:first-child{font-size:11pt;}
table.fees td:first-child{font-size:9.9pt;}
.file .notes p{font-size:9pt;}
.file .tab .nm{font-size:12pt;}
.stu-bleed .nm{font-size:11pt;}
.adv-bleed .nm{font-size:11.5pt;}
.sg .nm{font-size:10pt;}
.arc h3,.role .rn{font-size:11pt;font-weight:700;}
.story .name{font-size:11.5pt;}
"""),

    # 3 · NOIR — charcoal + champagne, fashion-house editorial
    "noir-champagne": dict(
        title="Blue Ocean Education · Prospectus · Noir",
        cfg=dict(
            accent=(88, 0.52, 1.0),      # champagne
            primary=(None, 0.16),        # smoke the blues to charcoal
            neutral=(80, 0.75),          # faint warm ivory
            clay=(70, 0.55),             # quiet bronze
            other=(None, 0.55),
            darken=(35, 0.70),           # deepen dark grounds to near-black
        ),
        css="""
:root{--display:'EB Garamond',Georgia,serif;}
h1.display{font-family:var(--serif);font-weight:400;font-size:30pt;letter-spacing:-.004em;line-height:1.1;}
h1.display em{font-weight:400;}
.kicker{letter-spacing:.36em;font-weight:600;color:oklch(48% .055 85);}
.page.forest .kicker,.page.forest-strong .kicker{color:var(--lime);}
.kicker::after{display:none;}
.chip{border-radius:0;background:transparent;}
.bigstat .n{font-weight:400;}
.foot{letter-spacing:.22em;}
.rows dt{font-weight:500;letter-spacing:.04em;}
.quote .mark{color:oklch(60% .07 88);}
.sig .nm{color:oklch(35% .02 80);}
.tl .yr{color:var(--lime);}
.layer h1.display{font-size:24.5pt;}
"""),

    # 4 · TERRA — sand + espresso + terracotta, warm humanist
    "terra-sand": dict(
        title="Blue Ocean Education · Prospectus · Terra",
        cfg=dict(
            accent=(62, 1.0, 1.0),       # ochre gold
            primary=(38, 1.3),           # burnt sienna
            neutral=(78, 2.2),           # sand paper
            clay=(35, 1.15),             # full terracotta
            other=(None, 1.0),
            lighten=(35, 1.22),          # lift dark grounds toward warm sienna
        ),
        css="""
h1.display{font-weight:600;letter-spacing:-.015em;}
.kicker{color:var(--clay);}
.kicker::after{background:var(--clay);opacity:.55;}
.page.forest .kicker{color:var(--lime);}
.chip{border-radius:99mm;background:oklch(92.5% .035 78);border-color:transparent;padding:2mm 4.2mm;}
.page.forest .chip{background:oklch(30% .06 50);}
.quote .mark{color:var(--clay);}
.bigstat .n{font-family:var(--display);font-weight:560;}
.pillar .no,.mile .yr{color:var(--clay);}
.foot{border-top-color:oklch(80% .05 60);}
.layer h1.display{font-size:24.5pt;}
"""),

    # 5 · ORCHID — aubergine + rose, contemporary luxe
    "orchid-aubergine": dict(
        title="Blue Ocean Education · Prospectus · Orchid",
        cfg=dict(
            accent=(2, 0.82, 1.0),       # rose
            primary=(330, 0.95),         # aubergine
            neutral=(345, 1.4),          # blush-tinted paper
            clay=(350, 0.9),
            other=(None, 1.0),
        ),
        css="""
:root{--display:'Fraunces','EB Garamond',Georgia,serif;}
h1.display{font-family:var(--display);font-weight:460;font-size:27pt;}
h1.display em{font-weight:520;}
.kicker{font-weight:700;letter-spacing:.28em;}
.quote blockquote{font-family:var(--display);font-weight:420;font-size:11.8pt;}
.chip{border-radius:.8mm;}
.bigstat .n{font-family:var(--display);font-weight:480;}
.sig .nm{font-family:var(--display);}
.tl .yr{font-family:var(--display);}
.layer h1.display{font-size:24.5pt;}
"""),
}


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    src = open(SRC, encoding="utf-8").read()
    n_colors = len(OKLCH.findall(src))
    print(f"source: {len(src)/1e6:.1f} MB, {n_colors} oklch colors")
    for name, v in VARIANTS.items():
        out = OKLCH.sub(make_replacer(v["cfg"]), src)
        out = out.replace(
            "<title>Blue Ocean Education · Prospectus</title>",
            f"<title>{v['title']}</title>", 1)
        out += f'\n<style id="variant-{name}">\n{v["css"]}\n</style>\n'
        path = os.path.join(OUT_DIR, f"blue-ocean-brochure-{name}.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"wrote {path} ({len(out)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
