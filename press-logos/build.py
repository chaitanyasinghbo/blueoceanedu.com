"""Build white-knockout press marks from exec-team/ sources.

Same rule as uni-logos/: one solid ground, one white mark, no third colour.
"""
import os
from PIL import Image, ImageFilter

SRC = "exec-team"
OUT = "press-logos"
os.makedirs(OUT, exist_ok=True)

LUM = (0.2126, 0.7152, 0.0722)


def luminance(im):
    r, g, b, _ = im.split()
    return Image.merge("RGB", (r, g, b)).convert("L")


def knockout_from_alpha(im):
    """Transparent-ground source: the alpha channel already is the mark."""
    return im.split()[3]


def knockout_from_white(im, cut=0.12):
    """Opaque light-ground source. The ground is sampled from the top-left
    corner, because two of these ship on #F7F7F7 rather than pure white, and
    a fixed white cut leaves the whole plate as a translucent block."""
    lum = luminance(im)
    a = im.split()[3]
    px = lum.load()
    ap = a.load()
    w, h = im.size
    # The ground is the modal luminance of the opaque pixels, not the corner
    # pixel: one of these plates carries a 1px transparent border, and a
    # corner sample there reads as black and kills the whole mark.
    hist = [0] * 256
    for y in range(h):
        for x in range(w):
            if ap[x, y] > 200:
                hist[px[x, y]] += 1
    ground = max(range(256), key=lambda v: hist[v])
    span = max(1.0, ground * cut)
    out = Image.new("L", (w, h))
    op = out.load()
    for y in range(h):
        for x in range(w):
            d = (ground - px[x, y]) / span
            v = 255 if d >= 1 else (0 if d <= 0 else int(255 * d))
            op[x, y] = min(v, ap[x, y])
    return out


def knockout_penguin(im, erode_px=16):
    """Filled-oval source: keep the oval as a ring, keep the dark bird."""
    a = im.split()[3].point(lambda v: 255 if v > 128 else 0)
    inner = a
    for _ in range(erode_px // 4):
        inner = inner.filter(ImageFilter.MinFilter(9))
    lum = luminance(im)
    dark = lum.point(lambda v: 255 if v < 90 else 0)
    ring = Image.eval(inner, lambda v: 255 - v)
    ring = Image.composite(a, Image.new("L", im.size, 0), ring.point(lambda v: 255 if v > 128 else 0))
    bird = Image.composite(dark, Image.new("L", im.size, 0), a)
    return Image.composite(Image.new("L", im.size, 255), bird, ring.point(lambda v: 255 if v > 128 else 0))


JOBS = [
    ("Forbes.png", "forbes.png", knockout_from_alpha),
    ("NDTV.png", "ndtv.png", knockout_from_alpha),
    ("business-standard-logo-2.png", "business-standard.png", knockout_from_alpha),
    ("mint.webp", "mint.png", knockout_from_alpha),
    ("harvard-lakshmi.png", "harvard-mittal.png", knockout_from_white),
    ("hindustan-times.png", "hindustan-times.png", knockout_from_white),
    ("times-of-india.png", "times-of-india.png", knockout_from_white),
    ("penguin.png", "penguin.png", knockout_penguin),
]

for src, dst, fn in JOBS:
    im = Image.open(os.path.join(SRC, src)).convert("RGBA")
    a = fn(im)
    mark = Image.new("RGBA", im.size, (255, 255, 255, 0))
    mark.putalpha(a)
    # Crop on a thresholded bbox: several sources carry near-invisible noise
    # out at the edges, and a raw getbbox() pads the mark inside its tile.
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

# The Indian Express ships as vector; recolour the fills rather than raster it.
svg = open(os.path.join(SRC, "The Indian Express.svg"), encoding="utf-8").read()
svg = svg.replace("fill:#FF1204", "fill:#FFFFFF")
svg = svg.replace('<svg version="1.0"', '<svg fill="#FFFFFF" version="1.0"', 1)
# The source viewBox is 924x641 around a masthead that occupies 750x75 of it.
# Left alone, object-fit: contain sizes the empty box and the mark renders at
# an eighth of its neighbours.
svg = svg.replace('viewBox="0 0 924 641.1"', 'viewBox="82 278 760 85"')
open(os.path.join(OUT, "indian-express.svg"), "w", encoding="utf-8").write(svg)
print("indian-express.svg")
