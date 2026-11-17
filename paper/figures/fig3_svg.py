"""Figure 3 as a hand-laid SVG: layout draft with invented data (17 Nov 2026).

Run:  uv run --no-project --with pillow python paper/figures/fig3_svg.py  (writes fig3-new.svg/.pdf)

Message (paper/decisions.md, Fig. 3): the same model trained on the policy reward learns the work-up
and keeps its accuracy; trained on accuracy and cost (outcome reward) it stops ordering tests. The
data below are invented only to place the marks; every number printed in the figure is "xx" until
the three-seed runs replace them.

Layout, two rows read a -> b, then c -> d:
  a  validation curves over training steps, mean and seed range (DeepSeek-R1, Nature 2025, Fig. 1:
     accuracy and response length over RL steps);
  b  the test results, one small dot plot per measure with 95% CIs (paired comparisons as in
     Nature Medicine clinical AI papers);
  c  the same measures for each of the four test conditions (only four conditions are held out,
     so a reviewer asks whether one of them carries the effect);
  d  why the outcome reward loses diagnoses: cases the untrained model solves from the story alone
     vs cases that need tests (the mechanism, with a measure that does not use the policy score).
The reward history and a single worked case moved to Extended Data (17 Nov): the history in the main
figure invites "the reward was tuned until it worked", and the case widget already appears in Figs 1-2.
"""

from __future__ import annotations

from pathlib import Path

import svgkit as k
from svgkit import BASE, INK, MODEL_A, MODEL_B, MUTED, ROW, S

XX = "xx"   # printed in place of every number until the real runs exist

# the three models, in the order they are drawn everywhere
SERIES = [("base", "Untrained", BASE), ("outcome", "Outcome reward", MODEL_B),
          ("policy", "Policy reward", MODEL_A)]
COL = {key: col for key, _, col in SERIES}

R1, R2 = 640, 640
A_W = 640
B_X, B_W = A_W + k.GAP, k.W - A_W - k.GAP
C_W = 1040
D_X, D_W = C_W + k.GAP, k.W - C_W - k.GAP
Y2 = R1 + k.GAP
GRIDC = "#EEF1F4"


def inner(x, y, w, h):
    """The white card inside a panel."""
    cx, cy, cw, ch = x + k.PAD, y + k.HEAD, w - 2 * k.PAD, h - k.HEAD - k.PAD
    k.card(cx, cy, cw, ch)
    return cx, cy, cw, ch


def legend(x, y, max_x, kind):
    """Keys for the three models: a short line (kind='line') or a dot. Wraps; returns the last row's y."""
    x0 = x
    for key, label, col in SERIES:
        w = 44 + 10 + k.width(label)
        if x + w > max_x:
            x, y = x0, y + ROW + 6
        ym = y - S * 0.36
        if kind == "line":
            k.line(x, ym, x + 44, ym, stroke=col, sw=3, dash="7 5" if key == "base" else None)
        else:
            k.marker(x + 22, ym, "circle", col, r=9.5)
        k.text(x + 54, y, label)
        x += w + 30
    return y


def band(xs, lo, hi, col):
    pts = [f"{x:.1f},{y:.1f}" for x, y in zip(xs, hi)] + [f"{x:.1f},{y:.1f}" for x, y in zip(xs[::-1], lo[::-1])]
    k.out.append(f'<polygon points="{" ".join(pts)}" fill="{col}" fill-opacity="0.18" stroke="none"/>')


def polyline(xs, ys, col, sw=2.6, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    k.out.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{sw}" '
                 f'stroke-linejoin="round" stroke-linecap="round"{d}/>')


def y_axis(px, y0, y1, ticks, Y, fmt, label_x=None, label=None):
    for v in ticks:
        k.line(px - 10, Y(v), px, Y(v))
        k.text(px - 16, Y(v) + S * 0.36, fmt(v), anchor="end")
    k.line(px, y0, px, y1)
    if label:
        k.text(label_x, (y0 + y1) / 2, label, anchor="middle", rotate=-90)


# ------------------------------------------------------------------ a  training curves
STEPS = list(range(0, 501, 50))
# validation mean and seed range -- INVENTED
CURVES = {
    "dx": {"policy": [88, 88, 89, 88, 89, 89, 89, 88, 89, 89, 89],
           "outcome": [88, 84, 70, 62, 58, 57, 56, 55, 55, 55, 55]},
    "tests": {"policy": [3.7, 4.5, 5.2, 5.6, 5.8, 5.9, 6.0, 6.0, 6.1, 6.1, 6.1],
              "outcome": [3.7, 1.6, .2, 0, 0, 0, 0, 0, 0, 0, 0]},
}
SPREAD = {"dx": 3, "tests": .5}
CHOSEN = {"policy": 10, "outcome": 1}          # index of the checkpoint kept on validation


def draw_a():
    k.panel(0, 0, A_W, R1, "a", "What each model learns in training")
    cx, cy, cw, ch = inner(0, 0, A_W, R1)
    ly = legend(cx + 28, cy + 44, cx + cw - 20, "line")
    px0, px1 = cx + 28 + 54, cx + cw - 34
    X = lambda s: px0 + s / 500 * (px1 - px0)
    title_h = S + 22                     # each small plot is titled above, not with a rotated label
    top, bottom = ly + 30 + title_h, cy + ch - 84
    gap = 40 + title_h
    h = (bottom - top - gap) / 2
    plots = [("dx", "Correct diagnoses on validation cases (%)", (40, 100), (40, 70, 100), lambda v: f"{v:.0f}"),
             ("tests", "Tests per validation case", (0, 8), (0, 4, 8), lambda v: f"{v:.0f}")]
    for i, (key, label, (lo, hi), ticks, fmt) in enumerate(plots):
        y0 = top + i * (h + gap)
        y1 = y0 + h
        Y = lambda v, y0=y0, y1=y1, lo=lo, hi=hi: y1 - (v - lo) / (hi - lo) * (y1 - y0)
        for v in ticks[1:]:
            k.line(px0, Y(v), px1, Y(v), stroke=GRIDC, sw=1.2)
        y_axis(px0, y0, y1, ticks, Y, fmt)
        k.text(cx + 28, y0 - 22, label)
        k.line(px0, y1, px1, y1)
        for s in (0, 100, 200, 300, 400, 500):
            k.line(X(s), y1, X(s), y1 + 10)
            if i == 1:
                k.text(X(s), y1 + 10 + S * 1.05, str(s), anchor="middle")
        base = CURVES[key]["policy"][0]
        k.line(px0, Y(base), px1, Y(base), stroke=BASE, sw=2.2, dash="7 5")
        xs = [X(s) for s in STEPS]
        for arm in ("outcome", "policy"):
            v = CURVES[key][arm]
            sp = SPREAD[key]
            band(xs, [Y(max(lo, a - sp)) for a in v], [Y(min(hi, a + sp)) for a in v], COL[arm])
            polyline(xs, [Y(a) for a in v], COL[arm])
            j = CHOSEN[arm]
            k.out.append(f'<circle cx="{xs[j]:.1f}" cy="{Y(v[j]):.1f}" r="9" fill="#FFFFFF" '
                         f'stroke="{COL[arm]}" stroke-width="3"/>')
    k.text((px0 + px1) / 2, bottom + 10 + S * 2.4, "Training step", anchor="middle")


# ------------------------------------------------------------------ b  test results
# (title, axis range, ticks, tick format, {model: (mean, ci_lo, ci_hi)}) -- INVENTED
MEASURES = [
    ("Correct diagnosis (%)", (0, 100), (0, 50, 100), lambda v: f"{v:.0f}",
     {"base": (80, 76, 84), "outcome": (62, 57, 67), "policy": (81, 77, 85)}),
    ("Required tests ordered (%)", (0, 100), (0, 50, 100), lambda v: f"{v:.0f}",
     {"base": (45, 41, 49), "outcome": (4, 2, 6), "policy": (78, 74, 82)}),
    ("Cases with an unsafe action (%)", (0, 20), (0, 10, 20), lambda v: f"{v:.0f}",
     {"base": (12, 9, 15), "outcome": (3, 1, 5), "policy": (6, 4, 8)}),
    ("Cost per case ($)", (0, 4000), (0, 2000, 4000), lambda v: f"{v:.0f}",
     {"base": (2400, 2200, 2600), "outcome": (40, 0, 90), "policy": (3100, 2900, 3300)}),
    ("Outcome score", (0, 1), (0, 0.5, 1), lambda v: f"{v:.1f}",
     {"base": (.72, .69, .75), "outcome": (.78, .75, .81), "policy": (.70, .67, .73)}),
    ("Policy score", (0, 1), (0, 0.5, 1), lambda v: f"{v:.1f}",
     {"base": (.41, .38, .44), "outcome": (.30, .27, .33), "policy": (.64, .61, .67)}),
]


def draw_b():
    k.panel(B_X, 0, B_W, R1, "b", "Results on the test cases")
    cx, cy, cw, ch = inner(B_X, 0, B_W, R1)
    legend(cx + 28, cy + 44, cx + cw - 20, "dot")
    n = len(MEASURES)
    slot = (cw - 40) / n
    title_top = cy + 44 + 40
    title_lines = [k.wrap(t, slot - 40) for t, *_ in MEASURES]
    n_lines = max(len(t) for t in title_lines)
    y0 = title_top + (n_lines - 1) * ROW + S + 66        # room for the bracket above the dots
    y1 = cy + ch - 40
    for i, (title, (lo, hi), ticks, fmt, vals) in enumerate(MEASURES):
        sx = cx + 20 + i * slot
        px0 = sx + 4 + max(k.width(fmt(v)) for v in ticks) + 22
        px1 = sx + slot - 18
        mid = (px0 + px1) / 2
        k.lines_at(mid, title_top, title_lines[i], anchor="middle")
        Y = lambda v, lo=lo, hi=hi: y1 - (v - lo) / (hi - lo) * (y1 - y0)
        for v in ticks[1:]:
            k.line(px0, Y(v), px1, Y(v), stroke=GRIDC, sw=1.2)
        y_axis(px0, y0, y1, ticks, Y, fmt)
        k.line(px0, y1, px1, y1)
        step = (px1 - px0) / 3
        xs = {key: px0 + step * (j + 0.5) for j, (key, _, _) in enumerate(SERIES)}
        for key, _, col in SERIES:
            m, a, b = vals[key]
            k.line(xs[key], Y(a), xs[key], Y(b), stroke=col, sw=2.4)
            k.marker(xs[key], Y(m), "circle", col, r=10.5)
        # paired test, policy vs outcome reward: bracket above the higher of the two
        top_v = max(vals["policy"][2], vals["outcome"][2])
        yb = min(Y(top_v) - 26, y0 - 6)
        xo, xp = xs["outcome"], xs["policy"]
        k.out.append(f'<path d="M{xo:.1f},{yb + 8:.1f} V{yb:.1f} H{xp:.1f} V{yb + 8:.1f}" fill="none" '
                     f'stroke="{INK}" stroke-width="1.4"/>')
        k.text((xo + xp) / 2, yb - 10, f"P = {XX}", anchor="middle")


# ------------------------------------------------------------------ c  by test condition
# (condition, {measure: {model: (mean, lo, hi)}}) -- INVENTED
CONDITIONS = [
    ("Bacterial meningitis", {"dx": {"base": (86, 78, 93), "outcome": (70, 60, 80), "policy": (88, 80, 95)},
                              "req": {"base": (52, 45, 59), "outcome": (5, 1, 9), "policy": (84, 78, 90)}}),
    ("High-grade glioma", {"dx": {"base": (82, 73, 90), "outcome": (66, 55, 76), "policy": (83, 74, 91)},
                           "req": {"base": (40, 33, 47), "outcome": (3, 0, 7), "policy": (75, 68, 82)}}),
    ("Hepatic encephalopathy", {"dx": {"base": (70, 60, 80), "outcome": (48, 37, 59), "policy": (74, 64, 84)},
                                "req": {"base": (38, 31, 45), "outcome": (4, 0, 8), "policy": (72, 65, 79)}}),
    ("Myasthenia gravis", {"dx": {"base": (80, 71, 89), "outcome": (62, 51, 72), "policy": (79, 70, 88)},
                           "req": {"base": (48, 41, 55), "outcome": (4, 0, 8), "policy": (80, 73, 87)}}),
]
C_AXES = [("dx", "Correct diagnosis (%)"), ("req", "Required tests ordered (%)")]
DODGE = {"base": -13, "outcome": 0, "policy": 13}


def x_axis(px0, px1, y, ticks, X, label):
    k.line(px0, y, px1, y)
    for v in ticks:
        k.line(X(v), y, X(v), y + 10)
        k.text(X(v), y + 10 + S * 1.05, str(v), anchor="middle")
    k.text((px0 + px1) / 2, y + 10 + S * 2.4, label, anchor="middle")


def draw_c():
    k.panel(0, Y2, C_W, R2, "c", "Results for each test condition")
    cx, cy, cw, ch = inner(0, Y2, C_W, R2)
    legend(cx + 28, cy + 44, cx + cw - 20, "dot")
    name_w = max(k.width(c[0]) for c in CONDITIONS)
    ax0 = cx + 28 + name_w + 30
    gap = 60
    aw = (cx + cw - 36 - ax0 - gap) / 2
    top, bottom = cy + 44 + 40, cy + ch - 96
    step = (bottom - top) / len(CONDITIONS)
    for i, (name, vals) in enumerate(CONDITIONS):
        ym = top + (i + 0.5) * step
        k.text(cx + 28, ym - 4, name)
        k.text(cx + 28, ym - 4 + ROW, f"n = {XX}", fill=MUTED)
        if i:
            k.line(cx + 28, top + i * step, cx + cw - 28, top + i * step, stroke=GRIDC, sw=1.2)
    for j, (key, label) in enumerate(C_AXES):
        px0 = ax0 + j * (aw + gap)
        px1 = px0 + aw
        X = lambda v, px0=px0, px1=px1: px0 + v / 100 * (px1 - px0)
        for v in (50, 100):
            k.line(X(v), top, X(v), bottom, stroke=GRIDC, sw=1.2)
        for i, (_, vals) in enumerate(CONDITIONS):
            ym = top + (i + 0.5) * step
            for model, _, col in SERIES:
                m, a, b = vals[key][model]
                y = ym + DODGE[model]
                k.line(X(a), y, X(b), y, stroke=col, sw=2.2)
                k.marker(X(m), y, "circle", col, r=8.5)
        x_axis(px0, px1, bottom, (0, 50, 100), X, label)


# ------------------------------------------------------------------ d  the mechanism
# cases the untrained model diagnoses from the story alone (no test) vs cases that need tests -- INVENTED
GROUPS = [("Solved from the story alone", {"base": (90, 85, 94), "outcome": (86, 80, 91), "policy": (91, 86, 95)}),
          ("Need tests to solve", {"base": (66, 58, 74), "outcome": (30, 22, 38), "policy": (70, 62, 78)})]


def draw_d():
    k.panel(D_X, Y2, D_W, R2, "d", "The outcome reward fails where tests are needed")
    cx, cy, cw, ch = inner(D_X, Y2, D_W, R2)
    px0, px1 = cx + 118, cx + cw - 34
    top, bottom = cy + 70, cy + ch - 120
    Y = lambda v: bottom - v / 100 * (bottom - top)
    for v in (50, 100):
        k.line(px0, Y(v), px1, Y(v), stroke=GRIDC, sw=1.2)
    y_axis(px0, top, bottom, (0, 50, 100), Y, lambda v: f"{v:.0f}", cx + 34, "Correct diagnosis (%)")
    k.line(px0, bottom, px1, bottom)
    gw = (px1 - px0) / len(GROUPS)
    for g, (label, vals) in enumerate(GROUPS):
        gx = px0 + (g + 0.5) * gw
        for j, (model, _, col) in enumerate(SERIES):
            x = gx + (j - 1) * 46
            m, a, b = vals[model]
            k.line(x, Y(a), x, Y(b), stroke=col, sw=2.4)
            k.marker(x, Y(m), "circle", col, r=10.5)
        lines = k.wrap(label, gw - 30)
        k.lines_at(gx, bottom + 22, lines, anchor="middle")
        k.text(gx, bottom + 22 + S * 0.72 + len(lines) * ROW, f"n = {XX}", fill=MUTED, anchor="middle")
        xo, xp = gx, gx + 46
        yb = min(Y(max(vals["policy"][2], vals["outcome"][2])) - 26, top - 4)
        k.out.append(f'<path d="M{xo:.1f},{yb + 8:.1f} V{yb:.1f} H{xp:.1f} V{yb + 8:.1f}" fill="none" '
                     f'stroke="{INK}" stroke-width="1.4"/>')
        k.text((xo + xp) / 2, yb - 10, f"P = {XX}", anchor="middle")


draw_a()
draw_b()
draw_c()
draw_d()
H = Y2 + R2
assert H <= 1700, H
pdf = k.save(Path(__file__).with_name("fig3-new.svg"), H)
print(f"wrote {pdf} · 180 x {H / 10:.0f} mm")
