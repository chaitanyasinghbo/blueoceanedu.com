from __future__ import annotations

import html
import subprocess
import tempfile
from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent
FONT = ROOT.parent / "brand-identity-one-pagers" / "assets" / "fonts" / "AnekLatin-VF.ttf"
HB_VIEW = "/opt/homebrew/bin/hb-view"
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
INK = "#123B8F"


def outline_text(text: str, weight: int) -> tuple[str, float]:
    with tempfile.NamedTemporaryFile(suffix=".svg") as target:
        subprocess.run(
            [
                HB_VIEW,
                str(FONT),
                text,
                f"--variations=wght={weight}",
                "--font-size=1000",
                "--margin=0",
                "--background=ffffff00",
                "--foreground=123b8f",
                "--output-format=svg",
                f"--output-file={target.name}",
            ],
            check=True,
        )
        root = ET.parse(target.name).getroot()

    view_box = [float(value) for value in root.attrib["viewBox"].split()]
    width = view_box[2]

    glyphs: dict[str, list[str]] = {}
    for group in root.iter(f"{{{SVG_NS}}}g"):
        glyph_id = group.attrib.get("id")
        if glyph_id:
            glyphs[glyph_id] = [path.attrib["d"] for path in group.iter(f"{{{SVG_NS}}}path")]

    paths: list[str] = []
    for use in root.iter(f"{{{SVG_NS}}}use"):
        href = use.attrib.get(f"{{{XLINK_NS}}}href", "").lstrip("#")
        x = use.attrib.get("x", "0")
        y = use.attrib.get("y", "0")
        for path_data in glyphs.get(href, []):
            paths.append(
                f'<path d="{html.escape(path_data, quote=True)}" transform="translate({x} {y})"/>'
            )
    return "".join(paths), width


EDUCATION_PATHS, _ = outline_text("Education", 520)
LUE_PATHS, LUE_WIDTH = outline_text("lue", 630)
CEAN_PATHS, CEAN_WIDTH = outline_text("cean", 630)


CONCEPTS = [
    {
        "file": "01-whole-student.svg",
        "title": "Whole Student",
        "desc": "One silhouette holds Ocean's O and Blue's B: the whole person contains the structure built over time.",
        "mark": """
<path fill-rule="evenodd" d="M16 1C24.35 1 30.6 7.05 30.6 16C30.6 24.95 24.35 31 16 31C7.65 31 1.4 24.95 1.4 16C1.4 7.05 7.65 1 16 1ZM8.2 6.5V15.4H14.8C19 15.4 21.5 13.7 21.5 11C21.5 8.3 19 6.5 14.8 6.5ZM8.2 17.7V28.4H16.2C20.8 28.4 23.3 26.3 23.3 23.1C23.3 19.8 20.8 17.7 16.2 17.7Z"/>
""",
    },
    {
        "file": "02-development-within.svg",
        "title": "Development Within",
        "desc": "The complete O remains visible while the structure of B and E is built inside it.",
        "mark": """
<path fill-rule="evenodd" d="M16 1C24.6 1 31 7.2 31 16C31 24.8 24.6 31 16 31C7.4 31 1 24.8 1 16C1 7.2 7.4 1 16 1ZM16 7C10.7 7 7 10.7 7 16C7 21.3 10.7 25 16 25C21.3 25 25 21.3 25 16C25 10.7 21.3 7 16 7Z"/>
<path d="M6.4 7H11.4V25H6.4ZM8.8 14H24.2V18H8.8Z"/>
""",
    },
    {
        "file": "03-open-horizon.svg",
        "title": "Open Horizon",
        "desc": "A lowercase b opens its O-shaped bowl at the horizon: close guidance that leaves the future open.",
        "mark": """
<g fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="butt" stroke-linejoin="round">
  <path d="M7 2V19"/>
  <path d="M7 19C7 11.8 12 7 18.5 7C24.8 7 29.4 11.2 30 17.2"/>
  <path d="M7 19C7 26 12 30 18.5 30C24.8 30 29.4 26.2 30 21.8"/>
</g>
""",
    },
    {
        "file": "04-boe-glyph.svg",
        "title": "BOE Glyph",
        "desc": "Blue, Ocean, and Education resolve into one B: O in the bowls, E in the spine and three arms.",
        "mark": """
<g fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="square" stroke-linejoin="round">
  <path d="M5 29V3H16C23 3 27 5.6 27 10.2C27 14.2 23.7 16 17 16H5M17 16C24.5 16 29 18.5 29 23.2C29 27.2 25.4 29 17 29H5"/>
</g>
""",
    },
    {
        "file": "05-continuous-counsel.svg",
        "title": "Continuous Counsel",
        "desc": "One uninterrupted line becomes both b and O, reflecting direct counsel that compounds over several years.",
        "mark": """
<g fill="none" stroke="currentColor" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
  <path d="M7 2V18C7 25.18 11.82 30 18 30C25.18 30 30 25.18 30 18C30 10.82 25.18 6 18 6C11.82 6 7 10.82 7 18"/>
</g>
""",
    },
]


WORD_SCALE = 0.12
WORD_TOP = 4.0
CUSTOM_Y = 32.0
B_WIDTH = 64.0
LUE_X = B_WIDTH + 4.0
LUE_RENDERED_WIDTH = LUE_WIDTH * WORD_SCALE
O_X = LUE_X + LUE_RENDERED_WIDTH + 18.0
O_WIDTH = 64.0
CEAN_X = O_X + O_WIDTH + 4.0


def custom_wordmark() -> str:
    return f'''<g>
      <g transform="translate(0 {CUSTOM_Y:g})">
        <path fill-rule="evenodd" d="M0 0H30C49 0 62 7 62 20C62 29 56 35 46 39C58 42 64 49 64 60C64 74 51 80 31 80H0ZM16 14V33H30C40 33 46 30 46 23.5C46 17 40 14 30 14ZM16 47V66H31C42 66 48 63 48 56.5C48 50 42 47 31 47Z"/>
      </g>
      <g transform="translate({LUE_X:g} {WORD_TOP:g}) scale({WORD_SCALE:g})">{LUE_PATHS}</g>
      <g transform="translate({O_X:g} {CUSTOM_Y:g})">
        <path fill-rule="evenodd" d="M32 0C52 0 64 15 64 40C64 65 52 80 32 80C12 80 0 65 0 40C0 15 12 0 32 0ZM32 15C22 15 16 24 16 40C16 56 22 65 32 65C42 65 48 56 48 40C48 24 42 15 32 15Z"/>
      </g>
      <g transform="translate({CEAN_X:g} {WORD_TOP:g}) scale({WORD_SCALE:g})">{CEAN_PATHS}</g>
      <g transform="translate(0 102) scale(.045)">{EDUCATION_PATHS}</g>
    </g>'''


CUSTOM_WORDMARK = custom_wordmark()


def standard_lockup(concept: dict[str, str]) -> str:
    return f'''<svg xmlns="{SVG_NS}" width="620" height="170" viewBox="0 0 620 170" role="img" aria-labelledby="title desc">
  <title id="title">Blue Ocean Education, {concept["title"]} logo</title>
  <desc id="desc">{concept["desc"]}</desc>
  <g color="{INK}" fill="{INK}">
    <g transform="translate(22 18) scale(4.2)">{concept["mark"]}</g>
    <g transform="translate(184 -1) scale(.72)">{CUSTOM_WORDMARK}</g>
  </g>
</svg>
'''


for concept in CONCEPTS:
    (ROOT / concept["file"]).write_text(standard_lockup(concept), encoding="utf-8")


left = 34.0

wordmark_dna = f'''<svg xmlns="{SVG_NS}" width="680" height="170" viewBox="0 0 680 170" role="img" aria-labelledby="title desc">
  <title id="title">Blue Ocean Education, Name Is the Mark logo</title>
  <desc id="desc">A custom B and O are drawn from one parent geometry and integrated directly into the company name.</desc>
  <g color="{INK}" fill="{INK}">
    <g transform="translate({left:g} 0)">{CUSTOM_WORDMARK}</g>
  </g>
</svg>
'''
(ROOT / "06-name-is-the-mark.svg").write_text(wordmark_dna, encoding="utf-8")
