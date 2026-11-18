"""Figure 5 as a hand-laid SVG: redrawn after the second critical review of 18 Nov 2026, awaiting
approval; invented data.

Run:  uv run --no-project --with pillow python paper/figures/fig5_svg.py  (writes fig5-new.svg/.pdf)

Message (claim C4, R5): on 100 real MIMIC-IV emergency admissions the policy-reward model orders more
of the tests the admission requires than the untrained model, and its tests are close to those the
treating clinicians did. Two questions, one per panel:
  a  do the three models keep their order on real records? The levels of the three models on the 100
     admissions, with four measures of Fig. 3b, and the paired test of the claim (policy reward
     against untrained). The pink dashed line marks a cost equal to that of the required work-up, as
     in Fig. 3b;
  b  what do the models order against what the clinicians who treated the same patients actually did?
     Only real records allow this: a test never done answers "not available". Same layout as Fig. 4c
     (neurologists who solved the same admissions), so the two human references read the same way.
The second review removed two panels. The paired differences on both test sets (old a) were drawn
around a large gap between the two trained models; the outcome-reward model kept by the selection rule
keeps its diagnoses, so the levels say more than the differences. The split by condition group (old b)
had 12 admissions in one group and intervals too wide to read; it stays in Supplementary Table 1. The
cohort flow is an Extended Data CONSORT diagram, not a panel. The data are invented only to place the
marks; every printed number is "xx".
"""

from __future__ import annotations

from pathlib import Path

import svgkit as k
from svgkit import BASE, INK, MODEL_A, MODEL_B, MUTED, PHYS, ROW, S

XX = "xx"
GRIDC = "#EEF1F4"

R1, R2 = 470, 470
Y2 = R1 + k.GAP
ROW_H = 62

SERIES = [("base", "Untrained", BASE), ("outcome", "Outcome reward", MODEL_B),
          ("policy", "Policy reward", MODEL_A)]


def inner(x, y, w, h):
    cx, cy, cw, ch = x + k.PAD, y + k.HEAD, w - 2 * k.PAD, h - k.HEAD - k.PAD
    k.card(cx, cy, cw, ch)
    return cx, cy, cw, ch


def diamond(cx, cy, col, r=10.5):
    d = r * 1.25
    k.out.append(f'<path d="M{cx:.1f},{cy - d:.1f} L{cx + d:.1f},{cy:.1f} L{cx:.1f},{cy + d:.1f} '
                 f'L{cx - d:.1f},{cy:.1f} Z" fill="{col}" stroke="#FFFFFF" stroke-width="1.5"/>')


def x_axis(px0, px1, y, ticks, X):
    k.line(px0, y, px1, y)
    for v in ticks:
        k.line(X(v), y, X(v), y + 10)
        k.text(X(v), y + 10 + S * 1.05, f"{v:g}", anchor="middle")


def grid(xs, top, bottom):
    for x in xs:
        k.line(x, top, x, bottom, stroke=GRIDC, sw=1.2)


def row_labels(cx, top, rows):
    for i, (key, label, col) in enumerate(rows):
        ym = top + (i + 0.5) * ROW_H
        if key == "clin":
            diamond(cx + 28 + 14, ym, col, r=9)
        else:
            k.marker(cx + 28 + 14, ym, "circle", col, r=10)
        k.text(cx + 28 + 34, ym + S * 0.36, label)


# ------------------------------------------------------------------ a  the three models on the admissions
# (title, range, ticks, {series: (mean, lo, hi)}, reference value or None) -- INVENTED
A_MEASURES = [
    ("Correct diagnoses (%)", (0, 100), (0, 50, 100),
     {"base": (70, 61, 78), "outcome": (71, 62, 79), "policy": (74, 65, 82)}, None),
    ("Required tests ordered (%)", (0, 100), (0, 50, 100),
     {"base": (43, 38, 48), "outcome": (30, 25, 35), "policy": (74, 69, 79)}, None),
    ("Ordered tests the policy asks for (%)", (0, 100), (0, 50, 100),
     {"base": (45, 40, 50), "outcome": (50, 43, 57), "policy": (70, 65, 75)}, None),
    ("Cost relative to the required work-up", (0, 2), (0, 1, 2),
     {"base": (.80, .72, .88), "outcome": (.35, .29, .41), "policy": (1.05, .97, 1.13)}, 1.0),
]
KEY_REF = "Cost of the required work-up"


def draw_a():
    k.panel(0, 0, k.W, R1, "a", "The three models on 100 MIMIC-IV admissions")
    cx, cy, cw, ch = inner(0, 0, k.W, R1)
    label_w = max(k.width(s[1]) for s in SERIES)
    x0 = cx + 28 + 34 + label_w + 50
    p_w = 26 + 12 + k.width(f"P = {XX}")              # the bracket and its P value, right of each plot
    gap = p_w + 44
    pw = (cx + cw - 30 - p_w - x0 - gap * (len(A_MEASURES) - 1)) / len(A_MEASURES)
    # key for the reference line, top right
    kx = cx + cw - 28 - k.width(KEY_REF)
    k.text(kx, cy + 41, KEY_REF)
    k.line(kx - 54, cy + 41 - S * 0.36, kx - 10, cy + 41 - S * 0.36, stroke=PHYS, sw=2.4, dash="6 4")
    titles = [k.wrap(t, pw + 40) for t, *_ in A_MEASURES]
    n_lines = max(len(t) for t in titles)
    assert n_lines <= 2, titles
    title_top = cy + 66
    top = title_top + n_lines * ROW + 14
    bottom = top + ROW_H * len(SERIES)
    row_labels(cx, top, SERIES)
    ys = {key: top + (i + 0.5) * ROW_H for i, (key, _, _) in enumerate(SERIES)}
    for j, (title, (lo, hi), ticks, vals, ref) in enumerate(A_MEASURES):
        px0 = x0 + j * (pw + gap)
        px1 = px0 + pw
        lines = titles[j]
        k.lines_at((px0 + px1) / 2, title_top + (n_lines - len(lines)) * ROW, lines, anchor="middle")
        X = lambda v, px0=px0, px1=px1, lo=lo, hi=hi: px0 + (v - lo) / (hi - lo) * (px1 - px0)
        grid([X(v) for v in ticks[1:]], top, bottom)
        if ref is not None:
            k.line(X(ref), top, X(ref), bottom, stroke=PHYS, sw=2.4, dash="6 4")
        for key, _, col in SERIES:
            m, a, b = vals[key]
            k.line(X(a), ys[key], X(b), ys[key], stroke=col, sw=2.4)
            k.marker(X(m), ys[key], "circle", col, r=10)
        # paired test of the claim: policy reward against untrained
        bx = px1 + 26
        k.out.append(f'<path d="M{bx - 8:.1f},{ys["base"]:.1f} H{bx:.1f} V{ys["policy"]:.1f} H{bx - 8:.1f}" '
                     f'fill="none" stroke="{INK}" stroke-width="1.4"/>')
        k.text(bx + 12, (ys["base"] + ys["policy"]) / 2 + S * 0.36, f"P = {XX}")
        x_axis(px0, px1, bottom, ticks, X)
    assert bottom + 10 + S * 1.05 < cy + ch - 8, (bottom, cy + ch)


# ------------------------------------------------------------------ b  models against the clinicians
ROWS = [("clin", "Clinicians", PHYS)] + SERIES
# (title, range, ticks, {series: (mean, lo, hi) or None}) -- INVENTED; None: the reference itself
B_MEASURES = [
    ("Tests the clinicians also did (%)", (0, 100), (0, 50, 100),
     {"clin": None, "base": (71, 66, 76), "outcome": (78, 71, 85), "policy": (76, 72, 80)}),
    ("Clinicians' tests ordered (%)", (0, 100), (0, 50, 100),
     {"clin": None, "base": (36, 32, 40), "outcome": (21, 18, 24), "policy": (58, 54, 62)}),
    ("Tests per case", (0, 12), (0, 6, 12),
     {"clin": (7.2, 6.6, 7.8), "base": (3.6, 3.2, 4.0), "outcome": (1.9, 1.6, 2.2), "policy": (6.1, 5.7, 6.5)}),
]


def draw_b():
    k.panel(0, Y2, k.W, R2, "b", "Models against the clinicians who treated the same 100 patients")
    cx, cy, cw, ch = inner(0, Y2, k.W, R2)
    label_w = max(k.width(s[1]) for s in ROWS)
    x0 = cx + 28 + 34 + label_w + 50
    gap = 90
    pw = (cx + cw - 36 - x0 - gap * (len(B_MEASURES) - 1)) / len(B_MEASURES)
    title_y = cy + 41
    top = cy + 74
    bottom = top + ROW_H * len(ROWS)
    row_labels(cx, top, ROWS)
    for j, (title, (lo, hi), ticks, vals) in enumerate(B_MEASURES):
        px0 = x0 + j * (pw + gap)
        px1 = px0 + pw
        assert k.width(title) < pw + gap - 20, title
        k.text((px0 + px1) / 2, title_y, title, anchor="middle")
        X = lambda v, px0=px0, px1=px1, lo=lo, hi=hi: px0 + (v - lo) / (hi - lo) * (px1 - px0)
        grid([X(v) for v in ticks[1:]], top, bottom)
        for i, (key, _, col) in enumerate(ROWS):
            ym = top + (i + 0.5) * ROW_H
            if vals[key] is None:
                k.text((px0 + px1) / 2, ym + S * 0.36, "reference", fill=MUTED, anchor="middle")
                continue
            m, a, b = vals[key]
            k.line(X(a), ym, X(b), ym, stroke=col, sw=2.4)
            if key == "clin":
                diamond(X(m), ym, col)
            else:
                k.marker(X(m), ym, "circle", col, r=10)
        x_axis(px0, px1, bottom, ticks, X)
    assert bottom + 10 + S * 1.05 < cy + ch - 8


draw_a()
draw_b()
H = Y2 + R2
assert H <= 1700, H
pdf = k.save(Path(__file__).with_name("fig5-new.svg"), H)
print(f"wrote {pdf} · 180 x {H / 10:.0f} mm")
