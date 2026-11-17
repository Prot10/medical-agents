"""Shared drawing kit for the hand-laid paper figures (17 Nov 2026).

Units: 1 unit = 0.1 mm, so 1800 units = 180 mm, the NMI maximum width. Text is measured with Pillow
on the same Arial files the PDF embeds, so boxes fit their glyphs. Rules followed (NMI "AIP and
formatting" page and the Nature figure guide, read 17 Nov 2026): sans-serif text 5-7 pt (here all
7 pt), panel letters 8-pt bold lowercase, black text only (colour lives in marks, fills and lines),
no decorative icons, axes with lines, ticks and units, height at most 170 mm, PDF with TrueType
fonts (printed by headless Chrome; rsvg-convert leaves a Type 3 font). Palette: Okabe-Ito roles
fixed in paper/decisions.md.
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import ImageFont

# Okabe-Ito roles, fixed for the whole paper (paper/decisions.md)
MODEL_A, MODEL_B, BASE, PHYS = "#0072B2", "#E69F00", "#999999", "#CC79A7"
OK, ERR, SKY, YELLOW, BLACK = "#009E73", "#D55E00", "#56B4E9", "#F0E442", "#000000"
INK, MUTED = "#1F2328", "#5F6670"
SLATE_T, LINE, GRID = "#F2F4F7", "#D3DAE3", "#E6EAEF"
OK_T, ERR_T, GREY_T = "#DDF1EA", "#F9E3D6", "#ECEEF1"

ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
SANS = "Arial, Helvetica, sans-serif"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PT = 3.5278            # units per point
S = 24.6               # all text: 7.0 pt
S_LETTER = 28.2        # panel letters: 8.0 pt
LH = 1.3
ROW = S * LH
AXIS_W = 1.6           # 0.45 pt
W, GAP, PAD, HEAD = 1800, 28, 22, 66

out: list[str] = []
_fonts: dict[tuple[str, float], ImageFont.FreeTypeFont] = {}


def font(bold: bool, size: float) -> ImageFont.FreeTypeFont:
    key = (ARIAL_B if bold else ARIAL, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(*key)
    return _fonts[key]


def width(s: str, bold: bool = False, size: float = S) -> float:
    return font(bold, size).getlength(s)


def wrap(s: str, max_w: float, bold: bool = False) -> list[str]:
    lines, cur = [], ""
    for word in s.split(" "):
        trial = f"{cur} {word}".strip()
        if width(trial, bold) <= max_w:
            cur = trial
        else:
            assert cur, f"word wider than the box: {word}"
            lines.append(cur)
            cur = word
    return lines + [cur]


def text(x, y, s, bold=False, fill=INK, anchor="start", size=S, rotate=0):
    assert 5 * PT <= size <= 7.01 * PT or size == S_LETTER, (size, s)
    assert fill in (INK, MUTED, "#FFFFFF"), f"coloured text is not allowed: {s}"
    w = ' font-weight="bold"' if bold else ""
    rot = f' transform="rotate({rotate} {x:.1f} {y:.1f})"' if rotate else ""
    out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{SANS}" font-size="{size}"{w} '
               f'fill="{fill}" text-anchor="{anchor}"{rot}>{escape(s)}</text>')


def lines_at(x, top, lines, bold=False, fill=INK, anchor="start"):
    """Lines whose cap height starts at `top`; returns the bottom of the last line's glyphs."""
    for i, ln in enumerate(lines):
        text(x, top + S * 0.72 + i * ROW, ln, bold, fill, anchor)
    return top + S * 0.72 + (len(lines) - 1) * ROW + S * 0.22


def block_h(n):
    return S * 0.94 + (n - 1) * ROW


def rect(x, y, w, h, fill, rx=14, stroke="none", sw=0, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>')


def line(x1, y1, x2, y2, stroke=INK, sw=AXIS_W, dash=None, cap="butt"):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    out.append(f'<path d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}" stroke="{stroke}" stroke-width="{sw}" '
               f'stroke-linecap="{cap}"{d} fill="none"/>')


def marker(cx, cy, shape, fill, r=10, stroke="#FFFFFF", sw=1.5):
    if shape == "circle":
        out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    else:  # square
        rect(cx - r * 0.9, cy - r * 0.9, r * 1.8, r * 1.8, fill, rx=2, stroke=stroke, sw=sw)


def mark(cx, cy, kind, r=12.5):
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{OK if kind == "ok" else ERR}"/>')
    if kind == "ok":
        out.append(f'<path d="M{cx-6:.1f},{cy+0.5:.1f} l4,4 l8,-9" fill="none" stroke="#fff" stroke-width="3" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        out.append(f'<path d="M{cx-4.5:.1f},{cy-4.5:.1f} l9,9 M{cx+4.5:.1f},{cy-4.5:.1f} l-9,9" stroke="#fff" '
                   f'stroke-width="3" stroke-linecap="round"/>')


def key(x, y, fill, label, stroke="none", pill=False):
    """Legend key: a coloured box (or pill) and black text (Nature: keys, not coloured text).
    Returns the x where the next key can start."""
    bw = 30 if pill else 18
    rect(x, y - 15, bw, 18, fill, rx=9 if pill else 4, stroke=stroke, sw=1.5 if stroke != "none" else 0)
    text(x + bw + 8, y, label)
    return x + bw + 8 + width(label) + 26


def panel(x, y, w, h, letter, title, tint=SLATE_T, tag=None):
    rect(x, y, w, h, tint, rx=20)
    text(x + 22, y + 42, letter, bold=True, size=S_LETTER)
    tx = x + 22 + width(letter, True, S_LETTER) + 12
    end = x + w - 16
    if tag:  # a dashed box on the right of the header, e.g. "fake values"
        tw = width(tag) + 20
        rect(end - tw, y + 16, tw, 34, "none", rx=6, stroke=INK, sw=1.2, dash="5 4")
        text(end - 10, y + 41, tag, anchor="end")
        end -= tw + 12
    assert tx + width(title, True) < end, title
    text(tx, y + 41, title, bold=True)


def card(x, y, w, h):
    rect(x, y, w, h, "#FFFFFF", rx=14, stroke=LINE, sw=1.2)


def save(svg_path: Path, height: float) -> Path:
    """Write the SVG, print it to a PDF next to it with headless Chrome, refuse Type 3 fonts."""
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height:.0f}" width="180mm" '
           f'height="{height / 10:.1f}mm">', f'<rect width="{W}" height="{height:.0f}" fill="#FFFFFF"/>',
           *out, "</svg>"]
    svg_path.write_text("\n".join(svg) + "\n")
    pdf = svg_path.with_suffix(".pdf")
    h_mm = f"{height / 10:.1f}"
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "fig.html"
        page.write_text(f'<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:180mm {h_mm}mm;'
                        f'margin:0}}html,body{{margin:0;padding:0}}svg{{display:block;width:180mm;height:{h_mm}mm}}'
                        f'</style></head><body>{"".join(svg)}</body></html>')
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf}", page.as_uri()], check=True, capture_output=True)
    fonts = subprocess.run(["pdffonts", str(pdf)], capture_output=True, text=True, check=True).stdout
    assert "Type 3" not in fonts, f"Type 3 font in {pdf}"
    return pdf
