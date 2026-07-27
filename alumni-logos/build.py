"""Build white-knockout alumni marks from hero-logos/.

Same rule as press-logos/: one solid ground, one white mark, no third
colour. These five are harder than the mastheads because three of them
are shields with white detail inside a crimson field. A plain alpha
knockout turns a Harvard shield into a white blob and loses the VERITAS
books entirely, so the mark is keyed on luminance in every case: opaque
and not near-white becomes mark, opaque and near-white becomes a hole.
That one rule covers the shields, the plated HBS lockup, and the flat
red and blue wordmarks alike.
"""
import os
from PIL import Image

SRC = "hero-logos"
OUT = "alumni-logos"
os.makedirs(OUT, exist_ok=True)


def knockout(im, cut=0.12):
    """Mark = opaque and darker than white by more than `cut`."""
    r, g, b, a = im.split()
    lum = Image.merge("RGB", (r, g, b)).convert("L")
    px, ap = lum.load(), a.load()
    w, h = im.size
    out = Image.new("L", (w, h))
    op = out.load()
    span = 255.0 * cut
    for y in range(h):
        for x in range(w):
            d = (255 - px[x, y]) / span
            v = 255 if d >= 1 else (0 if d <= 0 else int(255 * d))
            op[x, y] = min(v, ap[x, y])
    return out


JOBS = [
    ("HBS.png", "hbs.png"),
    ("HKS.png", "hks.png"),
    ("harvard.png", "harvard.png"),
    ("MIT-Logo.png", "mit.png"),
    ("Iit-Kharagpur-Logo.webp", "iit-kharagpur.png"),
]

for src, dst in JOBS:
    im = Image.open(os.path.join(SRC, src)).convert("RGBA")
    a = knockout(im)
    mark = Image.new("RGBA", im.size, (255, 255, 255, 0))
    mark.putalpha(a)
    mark = mark.crop(a.point(lambda v: 255 if v > 12 else 0).getbbox())
    w, h = mark.size
    # 320px on the long side, not 600. The tile these land in is 134x62 on the
    # press strip and 88% x 28px on the alumni strip, and `object-fit: contain`
    # means the source resolution changes nothing about the layout. 320 is over
    # 3x the longest box dimension, which covers a 3x phone and stops there.
    s = 320.0 / max(w, h)
    if s < 1:
        mark = mark.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
    # Every mark is a knockout: white where there is ink, transparent where
    # there is not, and the one that keeps a dark detail (Penguin's bird) is
    # still grey rather than coloured. Measured across all twelve, max chroma
    # is 0, so LA carries them exactly and drops two of the four channels.
    # Both strips sit in the hero, so this is critical-path weight.
    mark = mark.convert("LA")
    mark.save(os.path.join(OUT, dst), optimize=True)
    print(dst, mark.size)
