"""Figure 1 as a hand-laid SVG (17 Nov 2026).

Run:  uv run --no-project --with pillow python paper/figures/fig1_svg.py
Then: rsvg-convert -f pdf -o paper/figures/fig1-new.pdf paper/figures/fig1.svg

Units: 1 unit = 0.1 mm, so the 1800-unit width is Nature's 180 mm double column.
Text is measured with Pillow on Arial/Menlo so wrapping and box heights fit the real glyphs.
Palette (Okabe-Ito) and the decisions behind each panel: paper/decisions.md.
Schematic roles: sky blue = cases and their results, pink = physicians and policy,
dark slate = what the agent writes, grey = the untrained model, green/vermilion = verdicts.
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from PIL import ImageFont

OUT = Path(__file__).with_name("fig1.svg")

# Okabe-Ito roles, fixed for the whole paper (paper/decisions.md)
BASE = "#999999"
PHYS = "#CC79A7"
OK = "#009E73"
ERR = "#D55E00"
SKY = "#56B4E9"
YELLOW = "#F0E442"
# tints and darker shades derived from them for schematic use
SKY_T, SKY_LINE, SKY_D = "#EAF5FC", "#CFE6F5", "#2F8FC9"
PINK_T, PINK_LINE, PINK_D = "#FBF0F6", "#F0D3E4", "#B0508C"
SLATE, SLATE_T = "#27313F", "#F2F4F7"
INK, MUTED, LINE = "#1F2328", "#69707A", "#5B6573"

ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
ARIAL_I = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"
MENLO = "/System/Library/Fonts/Menlo.ttc"
SANS = "Arial, Helvetica, sans-serif"
MONO = "Menlo, 'Courier New', monospace"

S_BODY, S_SMALL, S_TITLE, S_LETTER, S_CODE = 23, 19.5, 27, 34, 20.5
LH = 1.3

_fonts: dict[tuple[str, int | float], ImageFont.FreeTypeFont] = {}


def font(path: str, size: float) -> ImageFont.FreeTypeFont:
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def width(s: str, size: float = S_BODY, bold: bool = False, mono: bool = False, italic: bool = False) -> float:
    path = MENLO if mono else ARIAL_B if bold else ARIAL_I if italic else ARIAL
    return font(path, size).getlength(s)


def wrap(s: str, max_w: float, size: float = S_BODY, bold: bool = False, italic: bool = False) -> list[str]:
    lines, cur = [], ""
    for word in s.split(" "):
        trial = f"{cur} {word}".strip()
        if width(trial, size, bold, italic=italic) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


out: list[str] = []


def text(x, y, s, size=S_BODY, bold=False, fill=INK, anchor="start", spacing=0.0, italic=False):
    w = ' font-weight="bold"' if bold else ""
    w += ' font-style="italic"' if italic else ""
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    out.append(
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="{SANS}" font-size="{size}"{w}{ls} '
        f'fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>'
    )


def code(x, y, segments):
    """One line of syntax-coloured code: segments are (text, colour)."""
    spans = "".join(f'<tspan fill="{c}">{escape(t)}</tspan>' for t, c in segments)
    out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{MONO}" font-size="{S_CODE}" xml:space="preserve">{spans}</text>')


def rect(x, y, w, h, fill, rx=16, stroke="none", sw=0):
    out.append(
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    )


def icon(kind, cx, cy, color, s=1.0, sw=2.4):
    """Flat line icons drawn on a 24-unit grid centred on (cx, cy)."""
    paths = {
        "person": "M0,-9.5 a4.6,4.6 0 1,1 0,9.2 a4.6,4.6 0 1,1 0,-9.2 z M-8.5,10 a8.5,8 0 0,1 17,0",
        "people": "M-4,-9 a4,4 0 1,1 0,8 a4,4 0 1,1 0,-8 z M-11.5,9.5 a7.5,7 0 0,1 15,0 "
                  "M5.5,-7 a3.5,3.5 0 1,1 0,7 M5,3 a7,6.5 0 0,1 7.5,6.5",
        "docs": "M-6,-10 h9 l5,5 v15 h-14 z M3,-10 v5 h5 M-3,0 h8 M-3,4.5 h8 M-10,-6 v18 h12",
        "hospital": "M-10,10 v-15 h20 v15 z M-4,10 v-6 h8 v6 M0,-12 v8 M-4,-8 h8",
        "scan": "M0,-10 a10,10 0 1,1 0,20 a10,10 0 1,1 0,-20 z M0,-4.5 a4.5,4.5 0 1,1 0,9 a4.5,4.5 0 1,1 0,-9 z",
        "flask": "M-4,-10 h8 M-2.5,-10 v7 l-6.5,11.5 a1.8,1.8 0 0,0 1.6,2.5 h14.8 a1.8,1.8 0 0,0 1.6,-2.5 "
                 "l-6.5,-11.5 v-7 M-5.5,4 h11",
        "clipboard": "M-8,-8 h16 v19 h-16 z M-4,-11 h8 v5 h-8 z M-4,-1 h8 M-4,4 h8",
        "chip": "M-7,-7 h14 v14 h-14 z M-2.5,-2.5 h5 v5 h-5 z M-3,-11 v4 M3,-11 v4 M-3,7 v4 M3,7 v4 "
                "M-11,-3 h4 M-11,3 h4 M7,-3 h4 M7,3 h4",
        "stetho": "M-7,-10 v7 a7,7 0 0,0 14,0 v-7 M0,4 v2 a5,5 0 0,0 10,0 v-3 M10,0 a2.5,2.5 0 1,1 0,0.01",
    }
    out.append(
        f'<g transform="translate({cx:.1f},{cy:.1f}) scale({s})"><path d="{paths[kind]}" fill="none" '
        f'stroke="{color}" stroke-width="{sw / s:.2f}" stroke-linecap="round" stroke-linejoin="round"/></g>'
    )


def badge(cx, cy, kind, r=19, fill=SKY_T, color=SKY_D):
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"/>')
    icon(kind, cx, cy, color, s=r / 19 * 0.95)


def mark(cx, cy, kind, r=13):
    if kind == "ok":
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{OK}"/>')
        out.append(f'<path d="M{cx-6},{cy+0.5} l4.5,4.5 l8,-9" fill="none" stroke="#fff" stroke-width="3" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
    elif kind == "err":
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{ERR}"/>')
        out.append(f'<path d="M{cx-5},{cy-5} l10,10 M{cx+5},{cy-5} l-10,10" stroke="#fff" stroke-width="3" '
                   f'stroke-linecap="round"/>')
    else:
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r-1.25}" fill="#fff" stroke="{OK}" stroke-width="2.5"/>')
        out.append(f'<path d="M{cx},{cy-r+1.25} a{r-1.25},{r-1.25} 0 0,0 0,{2*r-2.5} z" fill="{OK}"/>')


def panel(x, y, w, h, letter, title, tint):
    rect(x, y, w, h, tint, rx=24)
    text(x + 26, y + 50, letter, S_LETTER, bold=True)
    text(x + 26 + width(letter, S_LETTER, bold=True) + 14, y + 49, title, S_TITLE, bold=True)


def next_arrow(cx, cy):
    out.append(f'<circle cx="{cx}" cy="{cy}" r="19" fill="#FFFFFF" stroke="#D5DAE1" stroke-width="1.5"/>')
    out.append(f'<path d="M{cx-7},{cy} h13 M{cx+1},{cy-6} l6,6 l-6,6" fill="none" stroke="{LINE}" '
               f'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')


W, H, GAP, PAD, HEAD = 1800, 830, 44, 24, 92
A_W, C_W = 400, 560
B_W = W - A_W - C_W - 2 * GAP
AX, BX, CX = 0, A_W + GAP, A_W + GAP + B_W + GAP

# ------------------------------------------------------------------ b  (drawn first to size the figure)
FN, KEY, VAL, PUN = "#8FD0F5", "#E8EDF3", YELLOW, "#9AA7B8"
THINK_FILL, ENV_LINE = "#E6EAF0", "#D9E1EA"
AV_R, TAIL = 21, 11
# The tool calls and results are the real episode (catalogue_full/B-s1, ISCH-STR-S01). The thinking
# lines are ILLUSTRATIVE until the thinking run gives a real trace (paper/decisions.md).
TURNS = [
    ("env", "person", "72-year-old man, atrial fibrillation off anticoagulation. "
                      "Sudden right-sided weakness and aphasia; NIHSS\u00a023."),
    ("agt", "Sudden deficit, NIHSS 23, inside the window: exclude haemorrhage and look for a "
            "large-vessel occlusion.",
     [[("order_ct_scan", FN), ("(", PUN), ("contrast", KEY), ("=", PUN), ("true", VAL), (",", PUN)],
      [("    angiography", KEY), ("=", PUN), ("true", VAL), (")", PUN)]]),
    ("env", "scan", "CT angiography: occlusion of the left ICA terminus and MCA\u00a0M1\u00a0…"),
    ("agt", "Carotid-T occlusion, a thrombectomy candidate. Bloods and coagulation before reperfusion.",
     [[("interpret_labs", FN), ("(", PUN), ("panels", KEY), ("=[", PUN), ("CBC", VAL), (",", PUN)],
      [("    coagulation", VAL), (", ", PUN), ("CMP", VAL), ("])", PUN)]]),
    ("env", "flask", "Glucose 174\u00a0mg/dL, creatinine 1.1\u00a0mg/dL, INR\u00a00.9\u00a0…"),
    ("final", "Left MCA large-vessel occlusion; atrial fibrillation off anticoagulation points to "
              "a cardioembolic source.", "Acute ischaemic stroke, left MCA territory"),
]


def bubble(x, y, w, h, side, fill, stroke="none", sw=0, r=18):
    """Rounded speech bubble whose tail points at the avatar on `side` (left or right)."""
    t0, tm, t1 = y + 16, y + 27, y + 38
    if side == "left":
        d = (f"M{x+r},{y} H{x+w-r} A{r},{r} 0 0 1 {x+w},{y+r} V{y+h-r} A{r},{r} 0 0 1 {x+w-r},{y+h} "
             f"H{x+r} A{r},{r} 0 0 1 {x},{y+h-r} V{t1} L{x-TAIL},{tm} L{x},{t0} V{y+r} A{r},{r} 0 0 1 {x+r},{y} Z")
    else:
        d = (f"M{x+r},{y} H{x+w-r} A{r},{r} 0 0 1 {x+w},{y+r} V{t0} L{x+w+TAIL},{tm} L{x+w},{t1} "
             f"V{y+h-r} A{r},{r} 0 0 1 {x+w-r},{y+h} H{x+r} A{r},{r} 0 0 1 {x},{y+h-r} V{y+r} "
             f"A{r},{r} 0 0 1 {x+r},{y} Z")
    out.append(f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"/>')


def avatar_env(cx, cy, kind):
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{AV_R}" fill="{SKY_T}" stroke="{SKY_LINE}" stroke-width="1.5"/>')
    icon(kind, cx, cy, SKY_D, s=0.95)


def avatar_agent(cx, cy):
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{AV_R}" fill="{SLATE}"/>')
    icon("chip", cx, cy, "#FFFFFF", s=0.9, sw=2.2)


def thinking(x, y, w, s):
    """Thinking label plus italic lines; returns the y below them."""
    for k in range(3):
        out.append(f'<circle cx="{x + 4 + k * 9}" cy="{y - 6}" r="3" fill="{MUTED}" opacity="{0.45 + 0.25 * k}"/>')
    text(x + 32, y, "THINKING", S_SMALL - 4, bold=True, fill=MUTED, spacing=1.2)
    lines = wrap(s, w, S_SMALL, italic=True)
    yy = y + 30
    for i, ln in enumerate(lines):
        text(x, yy + i * S_SMALL * LH, ln, S_SMALL, fill="#4A515B", italic=True)
    return yy + (len(lines) - 1) * S_SMALL * LH


def draw_b():
    bx0, bx1 = BX + PAD, BX + B_W - PAD
    bub_w = 520
    env_x = bx0 + 2 * AV_R + 14
    agt_x = bx1 - 2 * AV_R - 14 - bub_w
    hy = HEAD + 6
    out.append(f'<circle cx="{bx0 + AV_R}" cy="{hy - 7}" r="7" fill="{SKY}"/>')
    text(bx0 + AV_R + 15, hy, "Case", S_SMALL, bold=True, fill=MUTED)
    pill = "Qwen3.5-9B · untrained"
    pw = width(pill, S_SMALL - 1.5, bold=True) + 28
    rect(bx1 - pw, hy - 23, pw, 31, BASE, rx=15.5)
    text(bx1 - pw / 2, hy - 1.5, pill, S_SMALL - 1.5, bold=True, fill="#FFFFFF", anchor="middle")
    text(bx1 - pw - 12, hy, "Agent", S_SMALL, bold=True, fill=MUTED, anchor="end")
    out.append(f'<circle cx="{bx1 - pw - 12 - width("Agent", S_SMALL, bold=True) - 16}" cy="{hy - 7}" r="7" fill="{SLATE}"/>')

    y = HEAD + 36
    for t in TURNS:
        kind = t[0]
        if kind == "env":
            lines = wrap(t[2], bub_w - 44, S_BODY)
            h = 30 + S_BODY + (len(lines) - 1) * S_BODY * LH
            bubble(env_x, y, bub_w, h, "left", "#FFFFFF", ENV_LINE, 1.5)
            avatar_env(bx0 + AV_R, y + 27, t[1])
            for i, ln in enumerate(lines):
                text(env_x + 22, y + 15 + S_BODY * 0.86 + i * S_BODY * LH, ln, S_BODY)
        else:
            inner_x, inner_w = agt_x + 20, bub_w - 40
            # measure first: thinking block, then the code or the final card
            n_think = len(wrap(t[1], inner_w, S_SMALL, italic=True))
            if kind == "agt":
                card_h = 26 + S_CODE + (len(t[2]) - 1) * S_CODE * 1.45
            else:
                n_dx = len(wrap(t[2], inner_w - 70, S_BODY, bold=True))
                card_h = 62 + (n_dx - 1) * S_BODY * LH + 20
            h = 22 + S_SMALL * 0.6 + 30 + (n_think - 1) * S_SMALL * LH + 22 + card_h + 16
            bubble(agt_x, y, bub_w, h, "right", THINK_FILL)
            avatar_agent(bx1 - AV_R, y + 27)
            ty = thinking(inner_x, y + 22 + S_SMALL * 0.6, inner_w, t[1])
            cy0 = ty + 22
            if kind == "agt":
                rect(inner_x - 6, cy0, inner_w + 12, card_h, SLATE, rx=12)
                for i, segs in enumerate(t[2]):
                    assert width("".join(s for s, _ in segs), S_CODE, mono=True) < inner_w - 20
                    code(inner_x + 12, cy0 + 13 + S_CODE * 0.86 + i * S_CODE * 1.45, segs)
            else:
                rect(inner_x - 6, cy0, inner_w + 12, card_h, "#FFFFFF", rx=12, stroke=SLATE, sw=2.5)
                icon("stetho", inner_x + 26, cy0 + card_h / 2, SLATE, s=1.0)
                text(inner_x + 58, cy0 + 32, "FINAL ASSESSMENT", S_SMALL - 4, bold=True, fill=MUTED, spacing=1.2)
                for i, ln in enumerate(wrap(t[2], inner_w - 70, S_BODY, bold=True)):
                    text(inner_x + 58, cy0 + 62 + i * S_BODY * LH, ln, S_BODY, bold=True)
            assert abs((cy0 + card_h + 16 - y) - h) < 0.01
        y += h + 16
    return y - 16


_saved, out = out, []
b_bottom = draw_b()
b_items, out = out, _saved
H = max(H, round(b_bottom + PAD))

# ------------------------------------------------------------------ a  cases
panel(AX, 0, A_W, H, "a", "Cases", SKY_T)
ix, iw = AX + PAD, A_W - 2 * PAD
SPLITS = [("Train", 419, ["14 conditions"], "#BFE2F6"),
          ("Validation", 60, ["multiple sclerosis,", "cardiac syncope"], "#7DC3EC"),
          ("Test", 119, ["myasthenia gravis, hepatic", "encephalopathy, bacterial",
                         "meningitis, high-grade glioma"], "#2F8FC9")]
MIMIC = [("Ischaemic stroke", 38), ("Multiple sclerosis", 22), ("Subarachnoid haem.", 12),
         ("Hepatic enceph.", 10), ("Status epilepticus", 9), ("4 other conditions", 9)]
LEG_GAP, SUB_LH, ROW_M = 34, S_SMALL * 1.25, 34
# natural heights: title block 92, number block 88, then the box's own rows
nb_rows = sum(28 + len(sub) * SUB_LH + LEG_GAP for _, _, sub, _ in SPLITS)
nb_nat = 92 + 88 + 28 + 46 + nb_rows
mm_nat = 92 + 88 + 20 + len(MIMIC) * ROW_M + 10
spare = (H - PAD - HEAD - 20) - nb_nat - mm_nat
assert spare >= 0, spare
nb_h, mm_h = nb_nat + spare * 0.5, mm_nat + spare * 0.5
pad_nb, pad_mm = spare * 0.5 / 2, spare * 0.5 / 2  # half the extra above the body, half below


def box_head(x, y, kind, title, sub):
    badge(x + 42, y + 44, kind)
    text(x + 76, y + 41, title, S_TITLE, bold=True)
    text(x + 76, y + 68, sub, S_SMALL, fill=MUTED)


y = HEAD
rect(ix, y, iw, nb_h, "#FFFFFF", stroke=SKY_LINE, sw=1.5)
box_head(ix, y, "docs", "NeuroBench", "synthetic · 20 conditions")
by0 = y + 92 + pad_nb
text(ix + 24, by0 + 62, "600", 60, bold=True)
text(ix + 24 + width("600", 60, bold=True) + 12, by0 + 62, "cases", S_BODY + 4, fill=MUTED)
bx, bw, by, bh = ix + 24, iw - 48, by0 + 92, 28
total = sum(n for _, n, _, _ in SPLITS)
cx = bx
for i, (_, n, _, col) in enumerate(SPLITS):
    seg = bw * n / total
    rect(cx, by, seg - (3 if i < 2 else 0), bh, col, rx=6)
    cx += seg
ly = by + bh + 46
for name, n, sub, col in SPLITS:
    rect(bx, ly - 17, 18, 18, col, rx=5)
    text(bx + 30, ly, name, S_BODY, bold=True)
    text(bx + 30 + width(name, S_BODY, bold=True) + 10, ly, str(n), S_BODY, fill=MUTED)
    for k, ln in enumerate(sub):
        assert width(ln, S_SMALL) < iw - 48 - 30, ln
        text(bx + 30, ly + 28 + k * SUB_LH, ln, S_SMALL, fill=MUTED)
    ly += 28 + len(sub) * SUB_LH + LEG_GAP

y2 = y + nb_h + 20
rect(ix, y2, iw, mm_h, "#FFFFFF", stroke=SKY_LINE, sw=1.5)
box_head(ix, y2, "hospital", "MIMIC-IV", "real emergency admissions")
my0 = y2 + 92 + pad_mm
text(ix + 24, my0 + 62, "100", 60, bold=True)
text(ix + 24 + width("100", 60, bold=True) + 12, my0 + 62, "admissions", S_BODY + 4, fill=MUTED)
text(ix + 24, my0 + 96, "9 conditions · test only", S_SMALL, fill=MUTED)
ry = my0 + 88 + 20 + 26
label_w = max(width(c, S_SMALL - 1) for c, _ in MIMIC)
bar_x0, bar_max = ix + 24 + label_w + 14, iw - 48 - label_w - 14 - 40
for cond, n in MIMIC:
    text(ix + 24, ry, cond, S_SMALL - 1, fill=INK)
    rect(bar_x0, ry - 15, bar_max * n / 38, 17, "#7DC3EC", rx=4)
    text(bar_x0 + bar_max * n / 38 + 8, ry, str(n), S_SMALL - 1, fill=MUTED)
    ry += ROW_M

# ------------------------------------------------------------------ b  agent at work
panel(BX, 0, B_W, H, "b", "The agent works up the case, one test per turn", SLATE_T)
out.extend(b_items)

# ------------------------------------------------------------------ c  policy scores it
panel(CX, 0, C_W, H, "c", "The physicians' policy scores it", PINK_T)
cx0, cw = CX + PAD, C_W - 2 * PAD
y = HEAD
card_h = H - HEAD - PAD
rect(cx0, y, cw, card_h, "#FFFFFF", stroke=PINK_LINE, sw=1.5)
badge(cx0 + 42, y + 44, "clipboard", fill=PINK_T, color=PINK_D)
text(cx0 + 76, y + 41, "Case policy", S_TITLE, bold=True)
icon("people", cx0 + 88, y + 63, PINK_D, s=0.62, sw=2)
text(cx0 + 104, y + 69, "reviewed by two neurologists", S_SMALL, bold=True, fill=PINK_D)

sections = [
    ("REQUIRED TESTS", [("err", "Non-contrast head CT first"), ("ok", "CT angiography"),
                        ("part", "Labs (troponin missing)"), ("err", "12-lead ECG")]),
    ("AVOID", [("ok", "No EEG, no lumbar puncture")]),
    ("STOP", [("err", "Diagnosis before the required tests")]),
    ("DIAGNOSIS", [("ok", "Acute ischaemic stroke")]),
]
ROW_C, TITLE_C = 50, 40
sy = y + card_h - 64
n_rows = sum(len(r) for _, r in sections)
room = (sy - 52 - 44) - (y + 132)
fixed = len(sections) * TITLE_C + (n_rows - 1) * ROW_C
GAP_C = min(62, (room - fixed) / (len(sections) - 1))  # sections share the height, capped
assert GAP_C >= 30, GAP_C
yy = y + 132 + (room - fixed - GAP_C * (len(sections) - 1)) / 2
for title, rows in sections:
    text(cx0 + 24, yy, title, S_SMALL - 3, bold=True, fill=PINK_D, spacing=1.2)
    yy += TITLE_C
    for kind, label in rows:
        mark(cx0 + 37, yy - 8, kind)
        text(cx0 + 62, yy, label, S_BODY)
        yy += ROW_C
    yy += GAP_C

rect(cx0 + 14, sy - 52, cw - 28, 96, "#F6F7F9", rx=14)
text(cx0 + 32, sy - 14, "Case score", S_BODY, bold=True)
text(cx0 + 32, sy + 16, "correct diagnosis, incomplete work-up", S_SMALL - 1.5, fill=MUTED)
score, bar_w = 0.54, 150
bar_x = cx0 + cw - 32 - bar_w
text(bar_x - 14, sy - 12, f"{score:.2f}", S_TITLE + 6, bold=True, anchor="end")
rect(bar_x, sy - 25, bar_w, 16, "#E3E6EA", rx=8)
rect(bar_x, sy - 25, bar_w * score, 16, BASE, rx=8)

# ------------------------------------------------------------------ flow between panels
next_arrow(A_W + GAP / 2, H / 2)
next_arrow(BX + B_W + GAP / 2, H / 2)

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="180mm" height="{H / 10}mm">',
    f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
    *out,
    "</svg>",
]
OUT.write_text("\n".join(svg) + "\n")
print(f"wrote {OUT} · b ends {b_bottom:.0f}/{H}, c list ends {yy:.0f}, score box from {sy - 52:.0f}")
