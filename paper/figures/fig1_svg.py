"""Figure 1 as a hand-laid SVG (17 Nov 2026).

Run:  uv run --no-project --with pillow python paper/figures/fig1_svg.py
PDF:  paper/figures/fig1_pdf.sh (builds the SVG, prints it with headless Chrome: TrueType
      fonts, no Type 3, as the Nature figure guide asks)

Units: 1 unit = 0.1 mm, so the 1800-unit width is Nature's 180 mm double column.
Nature figure guide (research-figure-guide.nature.com, read 17 Nov 2026): text 5-7 pt, Arial or
Helvetica, panel letters 8-pt bold lowercase upright. Here every text is 7 pt (24.6 units) and the
letters 8 pt (28.2 units). No italics: rsvg-convert fakes them with a slanted Arial whose glyphs
collide. Text is measured with Pillow on the same Arial files, so boxes fit the glyphs.
Layout as in NMI overview figures: full width (NMI maximum 180 mm), one row read left to right,
cases (a) -> the episode (b, wide) -> the policy (c). Nature guide: black text only (no coloured
text) and no decorative icons; colour stays in fills, outlines and the verdict marks. Palette (Okabe-Ito) and the decisions behind each panel: paper/decisions.md.
Roles: sky blue = cases, blue = NeuroAgent, slate = the simulated hospital, pink = physicians and
policy, green/vermilion = verdicts.

Panel b is a real episode: NeuroAgent (Qwen3.5-9B RL-trained with the policy reward v3, seed 1,
checkpoint 300, validation seed 1) on SYNC-CARD-RS03, a validation case it never trained on.
Every step is shown. Each "Reason" is the `clinical_context` the model wrote in that call, quoted
with ellipses only; the drug check has no such field, so it shows none. Answers are shortened
from the served reports. The model runs with thinking off (thinking test, 17 Nov).
"""

from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

from PIL import ImageFont

OUT = Path(__file__).with_name("fig1.svg")

# Okabe-Ito roles, fixed for the whole paper (paper/decisions.md)
MODEL_A = "#0072B2"
OK = "#009E73"
ERR = "#D55E00"
SKY_T, SKY_LINE, SKY_D, SKY_BAR, SKY_PALE = "#EAF5FC", "#CFE6F5", "#2F8FC9", "#7DC3EC", "#BFE2F6"
A_T, A_LINE, A_D = "#E4EFF7", "#C4DBEC", "#00588A"
PINK_T, PINK_LINE, PINK_D = "#FBF0F6", "#F0D3E4", "#B0508C"
SLATE, SLATE_T, ANS_T, ANS_LINE = "#27313F", "#F2F4F7", "#F5F7FA", "#D3DAE3"
INK, MUTED = "#1F2328", "#5F6670"

ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIAL_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
SANS = "Arial, Helvetica, sans-serif"

PT = 3.5278            # units per point
S = 24.6               # all text: 7.0 pt
S_LETTER = 28.2        # panel letters: 8.0 pt
LH = 1.3
ROW = S * LH

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


out: list[str] = []


def text(x, y, s, bold=False, fill=INK, anchor="start", size=S):
    assert 5 * PT <= size <= 7.01 * PT or size == S_LETTER, (size, s)
    w = ' font-weight="bold"' if bold else ""
    out.append(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{SANS}" font-size="{size}"{w} '
               f'fill="{fill}" text-anchor="{anchor}">{escape(s)}</text>')


def lines_at(x, top, lines, bold=False, fill=INK):
    """Lines whose cap height starts at `top`; returns the bottom of the last line's glyphs."""
    for i, ln in enumerate(lines):
        text(x, top + S * 0.72 + i * ROW, ln, bold, fill)
    return top + S * 0.72 + (len(lines) - 1) * ROW + S * 0.22


def block_h(n):
    return S * 0.94 + (n - 1) * ROW


def rect(x, y, w, h, fill, rx=14, stroke="none", sw=0):
    out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
               f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')


def icon(kind, cx, cy, color, s=1.0, sw=2.3):
    """Flat line icons drawn on a 24-unit grid centred on (cx, cy)."""
    paths = {
        "person": "M0,-9.5 a4.6,4.6 0 1,1 0,9.2 a4.6,4.6 0 1,1 0,-9.2 z M-8.5,10 a8.5,8 0 0,1 17,0",
        "people": "M-4,-9 a4,4 0 1,1 0,8 a4,4 0 1,1 0,-8 z M-11.5,9.5 a7.5,7 0 0,1 15,0 "
                  "M5.5,-7 a3.5,3.5 0 1,1 0,7 M5,3 a7,6.5 0 0,1 7.5,6.5",
        "docs": "M-6,-10 h9 l5,5 v15 h-14 z M3,-10 v5 h5 M-3,0 h8 M-3,4.5 h8 M-10,-6 v18 h12",
        "report": "M-7,-11 h9 l6,6 v16 h-15 z M2,-11 v6 h6 M-3,-1 h7 M-3,3.5 h7 M-3,8 h4",
        "hospital": "M-10,10 v-15 h20 v15 z M-4,10 v-6 h8 v6 M0,-12 v8 M-4,-8 h8",
        "clipboard": "M-8,-8 h16 v19 h-16 z M-4,-11 h8 v5 h-8 z M-4,-1 h8 M-4,4 h8",
        "chip": "M-7,-7 h14 v14 h-14 z M-2.5,-2.5 h5 v5 h-5 z M-3,-11 v4 M3,-11 v4 M-3,7 v4 M3,7 v4 "
                "M-11,-3 h4 M-11,3 h4 M7,-3 h4 M7,3 h4",
        "pulse": "M-11,1 h5 l3,-8 l4,15 l3,-7 h7",
        "monitor": "M-11,-8 h22 v14 h-22 z M-4,10 h8 M0,6 v4 M-8,0 h4 l2,-4 l3,7 l2,-3 h5",
        "echo": "M0,-10 L-10,7 A14,14 0 0,0 10,7 Z M-4,3 a5,5 0 0,0 8,0",
        "flask": "M-4,-10 h8 M-2.5,-10 v7 l-6.5,11.5 a1.8,1.8 0 0,0 1.6,2.5 h14.8 a1.8,1.8 0 0,0 1.6,-2.5 "
                 "l-6.5,-11.5 v-7 M-5.5,4 h11",
        "pill": "M-9,3 l8,-8 a5,5 0 0,1 7,7 l-8,8 a5,5 0 0,1 -7,-7 z M-5,-1 l6,6",
        "check": "M-7,0 l4.5,4.5 l9,-9",
    }
    out.append(
        f'<g transform="translate({cx:.1f},{cy:.1f}) scale({s})"><path d="{paths[kind]}" fill="none" '
        f'stroke="{color}" stroke-width="{sw / s:.2f}" stroke-linecap="round" stroke-linejoin="round"/></g>'
    )


def disc(cx, cy, r, fill, kind, color="#FFFFFF", s=None, sw=2.1):
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{fill}"/>')
    icon(kind, cx, cy, color, s=s or r / 21, sw=sw)


def mark(cx, cy, kind, r=12.5):
    out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{OK if kind == "ok" else ERR}"/>')
    if kind == "ok":
        out.append(f'<path d="M{cx-6:.1f},{cy+0.5:.1f} l4,4 l8,-9" fill="none" stroke="#fff" stroke-width="3" '
                   f'stroke-linecap="round" stroke-linejoin="round"/>')
    else:
        out.append(f'<path d="M{cx-4.5:.1f},{cy-4.5:.1f} l9,9 M{cx+4.5:.1f},{cy-4.5:.1f} l-9,9" stroke="#fff" '
                   f'stroke-width="3" stroke-linecap="round"/>')


def panel(x, y, w, h, letter, title, tint):
    rect(x, y, w, h, tint, rx=20)
    text(x + 22, y + 42, letter, bold=True, size=S_LETTER)
    tx = x + 22 + width(letter, True, S_LETTER) + 12
    assert tx + width(title, True) < x + w - 16, title
    text(tx, y + 41, title, bold=True)


W, GAP, PAD, HEAD = 1800, 28, 22, 66
# one row, read left to right: cases (a) -> the agent at work (b, wide) -> the policy scores it (c)
A_W, C_W = 370, 370
B_W = W - A_W - C_W - 2 * GAP
AX, BX, CX = 0, A_W + GAP, A_W + GAP + B_W + GAP

# ------------------------------------------------------------------ b  the episode
CASE = ("72-year-old man with coronary artery disease after bypass surgery and mild aortic stenosis, "
        "on atenolol. Sudden collapse at home, unresponsive for 15–20 s, no jerking. "
        "Heart rate 35 /min.")
# (icon, test, arguments as ordered, reason = the model's clinical_context or None, answer)
STEPS = [
    ("pulse", "12-lead ECG", None,
     "“…Concern for bradycardia/conduction abnormality causing syncope.”",
     "Complete AV block, escape 35 /min, wide QRS"),
    ("monitor", "Cardiac monitoring", "telemetry",
     "“…Requires urgent cardiology evaluation and consideration for pacemaker implantation.”",
     "Block throughout 24 h, pauses up to 5.2 s"),
    ("echo", "Echocardiogram", "transthoracic",
     "“…Evaluate valve severity, ventricular function…”",
     "Ejection fraction 45%, mild aortic stenosis"),
    ("flask", "Blood tests", "CMP, CBC, TSH, troponin…",
     "“Evaluate electrolytes, renal function, cardiac enzymes…”",
     "Potassium normal, creatinine 1.5 mg/dL, troponin I 0.05 ng/mL (mildly raised)"),
    ("pill", "Drug check", "atenolol", None,
     "Atenolol is contraindicated in complete heart block"),
]
FINAL_DX = "Complete heart block (third-degree AV block) with symptomatic syncope"
FINAL_PLAN = "Hold atenolol; urgent cardiology for a permanent pacemaker; continue telemetry"
STEP_R = 18
# name of each report the hospital sends back, in step order
REPORTS = ["ECG report", "Monitoring report", "Echo report", "Lab results", "Interaction check"]
NO_REASON = "This tool takes no reason"
ANS_HEAD_T = "#E8ECF1"


def card(x, y, w, h, head_h, head_fill, line):
    """A widget: white body, tinted header strip, rounded outline."""
    rect(x, y, w, h, "#FFFFFF")
    out.append(f'<path d="M{x},{y + head_h} V{y + 14} A14,14 0 0 1 {x + 14},{y} '
               f'H{x + w - 14} A14,14 0 0 1 {x + w},{y + 14} V{y + head_h} Z" fill="{head_fill}"/>')
    out.append(f'<path d="M{x},{y + head_h} H{x + w}" stroke="{line}" stroke-width="1.2"/>')
    rect(x, y, w, h, "none", stroke=line, sw=1.5)


def draw_b():
    bx0, bx1 = BX + PAD, BX + B_W - PAD
    y = HEAD + 4

    # who talks to whom
    text(bx0, y + 15, "NeuroAgent", bold=True)
    pill = "Qwen3.5-9B, RL-trained"
    px = bx0 + width("NeuroAgent", True) + 10
    rect(px, y - 10, width(pill) + 22, 32, A_T, rx=16)
    text(px + 11, y + 15, pill)
    text(bx1, y + 15, "Simulated hospital", bold=True, anchor="end")
    y += 44

    # initial case
    case_lines = wrap(CASE, bx1 - bx0 - 40)
    ch = 16 + block_h(1) + 8 + block_h(len(case_lines)) + 16
    rect(bx0, y, bx1 - bx0, ch, "#FFFFFF", stroke=SKY_LINE, sw=1.5)
    lines_at(bx0 + 20, y + 16, ["Initial case"], bold=True)
    lines_at(bx0 + 20, y + 16 + block_h(1) + 8, case_lines)
    y += ch + 22

    # one row per turn, two widgets of the same shape: the request NeuroAgent sends (left, blue:
    # test as ordered, then its reason) and the report the hospital sends back (right, slate:
    # report name, then the result); the numbered line on the left keeps the order
    node_x = bx0 + STEP_R
    req_x = bx0 + 2 * STEP_R + 14
    # as narrow as the widest header allows, so the hospital's reports keep their room
    req_w = max(470, max(18 + width(t, True) + (8 + width(f"· {a}") if a else 0) + 16
                         for _, t, a, _, _ in STEPS))
    arr = 40
    ans_x = req_x + req_w + arr
    ans_w = bx1 - ans_x
    head_h = 44
    lab_w = width("Reason", True) + 14
    r_txt_w = req_w - 18 - lab_w - 16
    a_txt_w = ans_w - 36
    nodes = []
    for i, ((ico, test, args, reason, answer), report) in enumerate(zip(STEPS, REPORTS), 1):
        r_lines = wrap(reason, r_txt_w) if reason else wrap(NO_REASON, req_w - 36)
        a_lines = wrap(answer, a_txt_w)
        h = head_h + 10 + max(block_h(len(r_lines)), block_h(len(a_lines))) + 12
        mid = y + head_h / 2
        # request widget
        card(req_x, y, req_w, h, head_h, A_T, A_LINE)
        text(req_x + 18, mid + S * 0.36, test, bold=True)
        if args:
            ax = req_x + 18 + width(test, True) + 8
            assert ax + width(f"· {args}") < req_x + req_w - 12, args
            text(ax, mid + S * 0.36, f"· {args}", fill=MUTED)
        top = y + head_h + 10
        if reason:
            lines_at(req_x + 18, top, ["Reason"], bold=True)
            lines_at(req_x + 18 + lab_w, top, r_lines)
        else:  # check_drug_interactions has no clinical_context field
            lines_at(req_x + 18, top, r_lines, fill=MUTED)
        # out and back
        out.append(f'<path d="M{req_x + req_w + 6},{mid - 6} H{ans_x - 8} M{ans_x - 14},{mid - 11} l6,5 l-6,5" '
                   f'fill="none" stroke="{A_D}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
        out.append(f'<path d="M{ans_x - 6},{mid + 7} H{req_x + req_w + 8} M{req_x + req_w + 14},{mid + 2} l-6,5 l6,5" '
                   f'fill="none" stroke="{SLATE}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>')
        # report widget
        card(ans_x, y, ans_w, h, head_h, ANS_HEAD_T, ANS_LINE)
        assert ans_x + 18 + width(report, True) < ans_x + ans_w - 12, report
        text(ans_x + 18, mid + S * 0.36, report, bold=True)
        lines_at(ans_x + 18, top, a_lines)
        nodes.append((mid, str(i)))
        y += h + 14

    # final assessment
    fx, fw = req_x, bx1 - req_x
    cw2 = (fw - 56) / 2
    dx_l, pl_l = wrap(FINAL_DX, cw2, bold=True), wrap(FINAL_PLAN, cw2)
    fh = head_h + 6 + block_h(1) + 6 + block_h(max(len(dx_l), len(pl_l))) + 16
    rect(fx, y, fw, fh, "#FFFFFF", stroke=MODEL_A, sw=2.4)
    text(fx + 18, y + head_h / 2 + S * 0.36, "Final assessment", bold=True)
    for k, (head, lines, bold) in enumerate((("Diagnosis", dx_l, True), ("Plan", pl_l, False))):
        x0 = fx + 18 + k * (cw2 + 20)
        lines_at(x0, y + head_h + 6, [head], fill=MUTED)
        lines_at(x0, y + head_h + 6 + block_h(1) + 6, lines, bold=bold)
    nodes.append((y + head_h / 2, "check"))

    out.append(f'<path d="M{node_x},{nodes[0][0]} V{nodes[-1][0]}" stroke="{A_LINE}" stroke-width="4"/>')
    for cy, label in nodes:
        out.append(f'<circle cx="{node_x}" cy="{cy}" r="{STEP_R}" fill="{MODEL_A}"/>')
        if label == "check":
            icon("check", node_x, cy, "#FFFFFF", s=0.9, sw=3)
        else:
            text(node_x, cy + S * 0.36, label, bold=True, fill="#FFFFFF", anchor="middle")
    return y + fh


_saved, out = out, []
b_bottom = draw_b()
b_items, out = out, _saved
H = round(b_bottom + PAD)

# ------------------------------------------------------------------ a  cases (left column)
SPLITS = [("Train", 419, "14 conditions", SKY_PALE),
          ("Validation", 60, "multiple sclerosis, cardiac syncope", SKY_BAR),
          ("Test", 119, "myasthenia gravis, hepatic encephalopathy, bacterial meningitis, high-grade glioma",
           SKY_D)]
MIMIC = [("Ischaemic stroke", 38), ("Multiple sclerosis", 22), ("Subarachnoid haem.", 12),
         ("Hepatic enceph.", 10), ("Status epilepticus", 9), ("4 others", 9)]


def box_title(x, y, w, kind, title, sub):
    text(x + 18, y + 30 + S * 0.36, title, bold=True)
    sub_l = wrap(sub, w - 36)
    lines_at(x + 18, y + 56, sub_l, fill=MUTED)
    return y + 56 + block_h(len(sub_l)) + 18


def neurobench(x, y, w, extra=0.0):
    yy = box_title(x, y, w, "docs", "NeuroBench", "600 synthetic cases, 20 conditions") + extra
    bx, bwid = x + 18, w - 36
    total = sum(n for _, n, _, _ in SPLITS)
    cx = bx
    for k, (_, n, _, col) in enumerate(SPLITS):
        seg = bwid * n / total
        rect(cx, yy, seg - (3 if k < 2 else 0), 20, col, rx=5)
        cx += seg
    yy += 20 + 22 + extra
    for name, n, sub, col in SPLITS:
        rect(bx, yy + 2, 16, 16, col, rx=4)
        text(bx + 26, yy + S * 0.72, name, bold=True)
        text(bx + 26 + width(name, True) + 8, yy + S * 0.72, str(n), fill=MUTED)
        sub_l = wrap(sub, bwid - 26)
        lines_at(bx + 26, yy + ROW, sub_l, fill=MUTED)
        yy += ROW + block_h(len(sub_l)) + 14 + extra
    return yy + 4 - extra


def mimic(x, y, w, extra=0.0):
    yy = box_title(x, y, w, "hospital", "MIMIC-IV", "100 real admissions, 9 conditions, test only") + 4 + extra
    full = w - 36
    for cond, n in MIMIC:
        assert width(cond) + width("38") + 12 < full, cond
        text(x + 18, yy + S * 0.72, cond)
        text(x + w - 18, yy + S * 0.72, str(n), fill=MUTED, anchor="end")
        rect(x + 18, yy + S + 6, full, 7, "#EEF3F7", rx=3.5)
        rect(x + 18, yy + S + 6, full * n / 38, 7, SKY_BAR, rx=3.5)
        yy += S + 6 + 7 + 14 + extra
    return yy + 4 - extra


def draw_a(h):
    """Two white boxes stacked; the spare height goes between and around them."""
    x, w = AX + PAD, A_W - 2 * PAD
    global out
    saved, out = out, []
    nb_h = neurobench(x, 0, w)
    mm_h = mimic(x, 0, w)
    out = saved
    between = 16
    spare = h - PAD - HEAD - between - nb_h - mm_h
    assert spare >= 0, spare
    # NeuroBench has 4 gaps between its rows, MIMIC 6 (+ 1 under each title)
    ex = spare / 11
    y = HEAD
    nb_full, mm_full = nb_h + 4 * ex, mm_h + 7 * ex
    rect(x, y, w, nb_full, "#FFFFFF", stroke=SKY_LINE, sw=1.5)
    neurobench(x, y, w, ex)
    y2 = y + nb_full + between
    rect(x, y2, w, mm_full, "#FFFFFF", stroke=SKY_LINE, sw=1.5)
    mimic(x, y2, w, ex)
    return HEAD + nb_h + mm_h + between + PAD


# ------------------------------------------------------------------ c  policy (right column)
# Verdicts from ClinicalPolicyReward on this episode (scalar 0.965; recommended coverage 2/3)
SECTIONS = [("Required", [("ok", "12-lead ECG, first"), ("ok", "Cardiac monitoring"),
                          ("ok", "Echocardiogram")]),
            ("Recommended", [("ok", "Bloods with troponin"), ("ok", "Medication review"),
                             ("err", "Head CT after the fall")]),
            ("Avoid", [("ok", "No EEG"), ("ok", "No brain MRI"), ("ok", "No tilt test")]),
            ("Diagnosis", [("ok", "Complete heart block")]),
            # reward components of the same episode: unjustified_actions 0, stopping 1.0
            ("Also scored", [("ok", "No useless test"), ("ok", "Stops when done")])]
ROW_C, TITLE_C = 40, ROW + 4
SCORE_H = 138


def draw_c(h, draw=True):
    x, w = CX + PAD, C_W - 2 * PAD
    y = HEAD
    n_rows = sum(len(r) for _, r in SECTIONS)
    rev_l = wrap("reviewed by two neurologists", w - 36)
    head = 64 - S * 0.47 + block_h(len(rev_l)) + 26
    fixed = head + len(SECTIONS) * TITLE_C + n_rows * ROW_C + SCORE_H + 22
    need = HEAD + fixed + 3 * 12 + PAD
    if not draw:
        return need
    gap = (h - PAD - y - fixed) / (len(SECTIONS) + 1)
    assert gap >= 12, gap
    rect(x, y, w, h - PAD - y, "#FFFFFF", stroke=PINK_LINE, sw=1.5)
    text(x + 18, y + 30 + S * 0.36, "Case policy", bold=True)
    lines_at(x + 18, y + 64 - S * 0.47, rev_l, fill=MUTED)
    yy = y + head
    for title, rows in SECTIONS:
        text(x + 18, yy + S * 0.72, title, bold=True)
        yy += TITLE_C
        for kind, label in rows:
            assert 34 + width(label) < w - 36, label
            mark(x + 30, yy + S * 0.36, kind)
            text(x + 52, yy + S * 0.72, label)
            yy += ROW_C
        yy += gap
    sx, sw_, sy = x + 12, w - 24, h - PAD - 12 - SCORE_H
    rect(sx, sy, sw_, SCORE_H, "#F6F7F9", rx=12)
    text(sx + 16, sy + 34, "Case score", bold=True)
    text(sx + sw_ - 16, sy + 34, "0.96", bold=True, anchor="end")
    rect(sx + 16, sy + 50, sw_ - 32, 12, "#E3E6EA", rx=6)
    rect(sx + 16, sy + 50, (sw_ - 32) * 0.96, 12, MODEL_A, rx=6)
    text(sx + 16, sy + 88, "one test missed", fill=MUTED)
    text(sx + 16, sy + 122, "Cost of the tests", fill=MUTED)   # total_cost_usd, Medicare rates
    text(sx + sw_ - 16, sy + 122, "$524", anchor="end")
    return yy


# all three panels as tall as the tallest
_saved, out = out, []
a_need = draw_a(10_000)        # height a needs: its boxes plus the minimum gap
out = _saved
H = max(H, round(a_need), round(draw_c(0, draw=False)))
panel(AX, 0, A_W, H, "a", "Cases", SKY_T)
draw_a(H)
panel(BX, 0, B_W, H, "b", "NeuroAgent works up a case, one test per turn", SLATE_T)
out.extend(b_items)
panel(CX, 0, C_W, H, "c", "The policy scores it", PINK_T)
draw_c(H)

svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="180mm" height="{H / 10}mm">',
    f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
    *out,
    "</svg>",
]
OUT.write_text("\n".join(svg) + "\n")
print(f"wrote {OUT} \u00b7 {W / 10:.0f} x {H / 10:.0f} mm, b ends {b_bottom:.0f}")
