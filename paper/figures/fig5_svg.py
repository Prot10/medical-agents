"""Figure 5 as a hand-laid SVG: layout approved by Andrea on 18 Nov 2026, invented data.

Run:  uv run --no-project --with pillow python paper/figures/fig5_svg.py  (writes fig5-new.svg/.pdf)

Message (claim C4, R5): the gain of the policy reward carries over from synthetic cases to 100 real
MIMIC-IV emergency admissions. Three questions, one per panel, none answered by another figure:
  a  does the difference between the two rewards keep its direction on real records? The paired
     difference (policy reward minus outcome reward) for three measures, NeuroBench test and MIMIC-IV
     side by side (Fig. 3b shows levels on NeuroBench only; the levels on MIMIC-IV are in ED Table 1);
  b  is the MIMIC-IV result carried by conditions the models trained on? Only 12 of the 100 admissions
     come from conditions kept out of training (HEP 10, BACT 2), so the two groups are drawn apart,
     as Fig. 3c draws the test conditions;
  c  what do the agents order against what the clinicians who treated the same patients actually did?
     Only real records allow this: a test never done answers "not available". Same layout as Fig. 4c
     (neurologists on synthetic cases), so the two human references read the same way.
The cohort flow is an Extended Data CONSORT diagram, not a panel. The data are invented only to place
the marks; every printed number is "xx" except the fixed cohort counts (12 and 88).
"""

from __future__ import annotations

from pathlib import Path

import svgkit as k
from svgkit import BASE, INK, MODEL_A, MODEL_B, MUTED, PHYS, ROW, S

XX = "xx"
GRIDC = "#EEF1F4"

R1, R2 = 500, 470
A_W = 760
B_X, B_W = A_W + k.GAP, k.W - A_W - k.GAP
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


def open_circle(cx, cy, r=10):
    k.out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="2.4"/>')


def x_axis(px0, px1, y, ticks, X, label=None):
    k.line(px0, y, px1, y)
    for v in ticks:
        k.line(X(v), y, X(v), y + 10)
        k.text(X(v), y + 10 + S * 1.05, f"{v:g}".replace("-", "\u2212"), anchor="middle")
    if label:
        k.text((px0 + px1) / 2, y + 10 + S * 2.45, label, anchor="middle")


def grid(xs, top, bottom):
    for x in xs:
        k.line(x, top, x, bottom, stroke=GRIDC, sw=1.2)


# ------------------------------------------------------------------ a  the difference on both test sets
# (measure, NeuroBench (diff, lo, hi), MIMIC-IV (diff, lo, hi)) in percentage points -- INVENTED
DIFFS = [("Correct diagnoses", (20, 14, 26), (12, 3, 21)),
         ("Required tests ordered", (74, 68, 80), (58, 49, 67)),
         ("Cases with an unsafe action", (3, 0, 6), (2, -3, 7))]
DODGE = 13


def draw_a():
    k.panel(0, 0, A_W, R1, "a", "Policy reward minus outcome reward, on both test sets")
    cx, cy, cw, ch = inner(0, 0, A_W, R1)
    label_w = max(k.width(d[0]) for d in DIFFS)
    px0, px1 = cx + 28 + label_w + 40, cx + cw - 30
    lo, hi = -20, 80
    X = lambda v: px0 + (v - lo) / (hi - lo) * (px1 - px0)
    # key, one line above the plot
    x = cx + 28
    k.marker(x + 10, cy + 33, "circle", INK, r=9)
    k.text(x + 28, cy + 41, "NeuroBench test cases")
    x += 28 + k.width("NeuroBench test cases") + 34
    open_circle(x + 10, cy + 33, r=8)
    k.text(x + 28, cy + 41, "MIMIC-IV admissions")
    assert x + 28 + k.width("MIMIC-IV admissions") < cx + cw - 20
    top = cy + 74
    bottom = top + ROW_H * 1.25 * len(DIFFS)
    grid([X(v) for v in (20, 40, 60, 80)], top, bottom)
    k.line(X(0), top, X(0), bottom, stroke=INK, sw=1.4, dash="6 5")
    for i, (name, nb, mm) in enumerate(DIFFS):
        ym = top + (i + 0.5) * ROW_H * 1.25
        k.text(cx + 28, ym + S * 0.36, name)
        m, a, b = nb
        k.line(X(a), ym - DODGE, X(b), ym - DODGE, stroke=INK, sw=2.4)
        k.marker(X(m), ym - DODGE, "circle", INK, r=10)
        m, a, b = mm
        k.line(X(a), ym + DODGE, X(b), ym + DODGE, stroke=INK, sw=2.4)
        open_circle(X(m), ym + DODGE, r=9)
    x_axis(px0, px1, bottom, (-20, 0, 20, 40, 60, 80), X, "Difference (percentage points)")
    assert bottom + 10 + S * 2.45 < cy + ch - 8


# ------------------------------------------------------------------ b  MIMIC-IV by condition group
# (label lines, n, {measure: {series: (mean, lo, hi)}}) -- INVENTED; n is the fixed allocation
GROUPS = [(("Kept out of training",), 12,
           {"dx": {"base": (58, 33, 80), "outcome": (42, 18, 67), "policy": (67, 42, 88)},
            "req": {"base": (40, 28, 52), "outcome": (6, 0, 14), "policy": (70, 57, 82)}}),
          (("Seen in training", "or validation"), 88,
           {"dx": {"base": (70, 61, 78), "outcome": (55, 45, 65), "policy": (72, 63, 80)},
            "req": {"base": (44, 39, 49), "outcome": (5, 3, 8), "policy": (76, 72, 80)}})]
MEASURES = [("dx", "Correct diagnoses (%)"), ("req", "Required tests ordered (%)")]
MDODGE = {"base": -17, "outcome": 0, "policy": 17}


def draw_b():
    k.panel(B_X, 0, B_W, R1, "b", "MIMIC-IV admissions, by condition group")
    cx, cy, cw, ch = inner(B_X, 0, B_W, R1)
    # model key
    x = cx + 28
    for _, label, col in SERIES:
        k.marker(x + 10, cy + 33, "circle", col, r=9)
        k.text(x + 26, cy + 41, label)
        x += 26 + k.width(label) + 30
    assert x < cx + cw
    label_w = max(k.width(s) for g in GROUPS for s in g[0])
    x0 = cx + 28 + label_w + 40
    gap = 44
    pw = (cx + cw - 30 - x0 - gap) / 2
    top = cy + 74
    step = (ROW_H * 1.25 * 3) / len(GROUPS)
    bottom = top + step * len(GROUPS)
    for i, (label, n, _) in enumerate(GROUPS):
        ym = top + (i + 0.5) * step
        y = ym - len(label) * ROW / 2 + S * 0.36   # name lines, then n, centred on the row
        for line in label:
            k.text(cx + 28, y, line)
            y += ROW
        k.text(cx + 28, y, f"n = {n}", fill=MUTED)
        if i:
            k.line(cx + 20, top + i * step, cx + cw - 20, top + i * step, stroke=GRIDC, sw=1.2)
    for j, (key, label) in enumerate(MEASURES):
        px0 = x0 + j * (pw + gap)
        px1 = px0 + pw
        assert k.width(label) < pw + gap - 10, label
        X = lambda v, px0=px0, px1=px1: px0 + v / 100 * (px1 - px0)
        grid([X(v) for v in (50, 100)], top, bottom)
        for i, (_, _, vals) in enumerate(GROUPS):
            ym = top + (i + 0.5) * step
            for model, _, col in SERIES:
                m, a, b = vals[key][model]
                y = ym + MDODGE[model]
                k.line(X(a), y, X(b), y, stroke=col, sw=2.2)
                k.marker(X(m), y, "circle", col, r=8.5)
        x_axis(px0, px1, bottom, (0, 50, 100), X, label)
    assert bottom + 10 + S * 2.45 < cy + ch - 8


# ------------------------------------------------------------------ c  models against the clinicians
ROWS = [("clin", "Clinicians", PHYS)] + SERIES
# (title, range, ticks, {series: (mean, lo, hi) or None}) -- INVENTED; None: the reference itself
C_MEASURES = [
    ("Tests the clinicians also did (%)", (0, 100), (0, 50, 100),
     {"clin": None, "base": (71, 66, 76), "outcome": (88, 70, 97), "policy": (64, 60, 68)}),
    ("Clinicians' tests ordered (%)", (0, 100), (0, 50, 100),
     {"clin": None, "base": (38, 34, 42), "outcome": (3, 1, 5), "policy": (55, 51, 59)}),
    ("Tests per case", (0, 12), (0, 6, 12),
     {"clin": (9.4, 8.8, 10.0), "base": (3.6, 3.2, 4.0), "outcome": (.1, 0, .3), "policy": (6.2, 5.8, 6.6)}),
]


def draw_c():
    k.panel(0, Y2, k.W, R2, "c", "Models against the clinicians who treated the same 100 patients")
    cx, cy, cw, ch = inner(0, Y2, k.W, R2)
    label_w = max(k.width(s[1]) for s in ROWS)
    x0 = cx + 28 + 34 + label_w + 50
    gap = 90
    pw = (cx + cw - 36 - x0 - gap * (len(C_MEASURES) - 1)) / len(C_MEASURES)
    title_y = cy + 41
    top = cy + 74
    bottom = top + ROW_H * len(ROWS)
    for i, (key, label, col) in enumerate(ROWS):
        ym = top + (i + 0.5) * ROW_H
        if key == "clin":
            diamond(cx + 28 + 14, ym, col, r=9)
        else:
            k.marker(cx + 28 + 14, ym, "circle", col, r=10)
        k.text(cx + 28 + 34, ym + S * 0.36, label)
    for j, (title, (lo, hi), ticks, vals) in enumerate(C_MEASURES):
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
draw_c()
H = Y2 + R2
assert H <= 1700, H
pdf = k.save(Path(__file__).with_name("fig5-new.svg"), H)
print(f"wrote {pdf} · 180 x {H / 10:.0f} mm")
