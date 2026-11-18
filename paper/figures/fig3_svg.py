"""Figure 3 as a hand-laid SVG: revised after the two critical reviews of 18 Nov 2026, awaiting approval;
invented data.

Run:  uv run --no-project --with pillow python paper/figures/fig3_svg.py  (writes fig3-new.svg/.pdf)

Message (paper/decisions.md, Fig. 3): the same model trained on the policy reward orders the tests each
case requires and few others, with as many correct diagnoses and a cost close to that of the required
work-up; trained on diagnosis and cost (outcome reward) it keeps the diagnoses and orders fewer tests.
The data below are invented only to place the marks, near the first real numbers (seed 1, validation
cases, draft policies); every number printed in the figure is "xx" until the three-seed runs replace
them.

Layout, two rows read a -> b, then c -> d:
  a  validation curves over training steps, mean and seed range (DeepSeek-R1, Nature 2025, Fig. 1:
     accuracy and response length over RL steps); the open circle is the checkpoint each model keeps,
     chosen on validation by its own reward (for the outcome reward an early one, before it stops
     ordering tests);
  b  the test results, one small dot plot per measure with 95% CIs. Second critical review (18 Nov):
     "useless tests per case" became the share of ordered tests the policy asks for, "cost per case"
     became the cost relative to the required work-up, and tests per case is read against the number
     the case policies ask for (pink dashed lines: the policy is the reference). Cases with an unsafe
     action left the figure (about 2% of cases, unchanged by training; Extended Data Table 1). The
     control trained on the outcome reward without its cost term stays (open orange circle);
  c  correct diagnoses and required tests for each of the four test conditions (only four conditions
     are held out, so a reviewer asks whether one of them carries the effect);
  d  right tests, or just more tests: required tests ordered against tests per case, with a scripted
     agent that orders the same k tests in every case for every k. It replaces the earlier mechanism
     panel (cases solved from the history alone against cases that need tests): with the outcome-reward
     model kept by the selection rule the diagnoses do not drop, and among the test conditions only
     glioma needs tests for the diagnosis, so that panel repeated c.
The reward history and a single worked case moved to Extended Data (17 Nov): the history in the main
figure invites "the reward was tuned until it worked", and the case widget already appears in Figs 1-2.
"""

from __future__ import annotations

from pathlib import Path

import svgkit as k
from svgkit import BASE, BLACK, INK, MODEL_A, MODEL_B, MUTED, PHYS, ROW, S

XX = "xx"   # printed in place of every number until the real runs exist

# the three models, in the order they are drawn everywhere
SERIES = [("base", "Untrained", BASE), ("outcome", "Outcome reward", MODEL_B),
          ("policy", "Policy reward", MODEL_A)]
COL = {key: col for key, _, col in SERIES}
# panel b adds the control that answers "the outcome reward is a straw man": the same outcome reward
# without its cost term (critical review, 18 Nov), drawn as an open orange circle
SERIES_B = [SERIES[0], SERIES[1], ("nocost", "Outcome reward, no cost", MODEL_B), SERIES[2]]

R1, R2 = 640, 640
A_W = 560
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


def dot(cx, cy, key, col, r=10.5):
    """A filled circle, or an open one for the outcome reward without cost."""
    if key == "nocost":
        k.out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r - 1.2}" fill="#FFFFFF" stroke="{col}" '
                     f'stroke-width="3"/>')
    else:
        k.marker(cx, cy, "circle", col, r=r)


def legend(x, y, max_x, kind, series=SERIES):
    """Keys for the models: a short line (kind='line') or a dot. Wraps; returns the last row's y."""
    x0 = x
    for key, label, col in series:
        w = 44 + 10 + k.width(label)
        if x + w > max_x:
            x, y = x0, y + ROW + 6
        ym = y - S * 0.36
        if kind == "line":
            k.line(x, ym, x + 44, ym, stroke=col, sw=3, dash="7 5" if key == "base" else None)
        else:
            dot(x + 22, ym, key, col, r=9.5)
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
    "dx": {"policy": [88, 88, 89, 90, 91, 91, 91, 90, 91, 91, 91],
           "outcome": [88, 89, 70, 62, 58, 57, 56, 55, 55, 55, 55]},
    "tests": {"policy": [3.7, 4.2, 4.8, 5.3, 5.7, 5.9, 5.9, 6.0, 5.9, 5.9, 5.9],
              "outcome": [3.7, 2.0, .2, 0, 0, 0, 0, 0, 0, 0, 0]},
}
SPREAD = {"dx": 3, "tests": .5}
CHOSEN = {"policy": 6, "outcome": 1}          # index of the checkpoint kept on validation


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
# (title, axis range, ticks, tick format, {model: (mean, ci_lo, ci_hi)}, reference value or None)
# -- INVENTED. The reference is what the case policies ask for, drawn as a pink dashed line.
F0 = lambda v: f"{v:.0f}"
F1 = lambda v: f"{v:.1f}"
MEASURES = [
    ("Correct diagnoses (%)", (0, 100), (0, 50, 100), F0,
     {"base": (88, 84, 92), "outcome": (89, 85, 93), "policy": (91, 87, 95)}, None),
    ("Required tests ordered (%)", (0, 100), (0, 50, 100), F0,
     {"base": (42, 38, 46), "outcome": (31, 27, 35), "policy": (80, 76, 84)}, None),
    ("Ordered tests the policy asks for (%)", (0, 100), (0, 50, 100), F0,
     {"base": (46, 42, 50), "outcome": (52, 46, 58), "policy": (74, 70, 78)}, None),
    ("Tests per case", (0, 8), (0, 4, 8), F0,
     {"base": (3.7, 3.4, 4.0), "outcome": (2.0, 1.8, 2.2), "policy": (5.9, 5.6, 6.2)}, 5.5),
    ("Cost relative to the required work-up", (0, 2), (0, 1, 2), F0,
     {"base": (.85, .78, .92), "outcome": (.35, .30, .40), "policy": (1.05, .98, 1.12)}, 1.0),
    ("Outcome score", (0, 1), (0, 0.5, 1), F1,
     {"base": (.84, .81, .87), "outcome": (.89, .86, .92), "policy": (.85, .82, .88)}, None),
    ("Policy score", (0, 1), (0, 0.5, 1), F1,
     {"base": (.42, .39, .45), "outcome": (.40, .37, .43), "policy": (.66, .63, .69)}, None),
]
# the outcome reward without cost, same measures in the same order -- INVENTED
NOCOST = [(88, 84, 92), (37, 33, 41), (48, 43, 53), (3.0, 2.7, 3.3), (.65, .58, .72), (.85, .82, .88),
          (.41, .38, .44)]
for (_, _, _, _, vals, _), v in zip(MEASURES, NOCOST):
    vals["nocost"] = v


KEY_REF = "What the case policies ask for"


def draw_b():
    k.panel(B_X, 0, B_W, R1, "b", "Results on the test cases")
    cx, cy, cw, ch = inner(B_X, 0, B_W, R1)
    legend(cx + 28, cy + 44, cx + cw - 20, "dot", SERIES_B)
    ly = cy + 44 + ROW + 6                     # second key line: the reference of the case policies
    k.line(cx + 28, ly - S * 0.36, cx + 28 + 44, ly - S * 0.36, stroke=PHYS, sw=2.4, dash="6 4")
    k.text(cx + 28 + 54, ly, KEY_REF)
    n = len(MEASURES)
    slot = (cw - 40) / n
    title_top = ly + 34
    title_lines = [k.wrap(t, slot - 40) for t, *_ in MEASURES]
    n_lines = max(len(t) for t in title_lines)
    y0 = title_top + (n_lines - 1) * ROW + S + 66        # room for the bracket above the dots
    y1 = cy + ch - 40
    for i, (title, (lo, hi), ticks, fmt, vals, ref) in enumerate(MEASURES):
        sx = cx + 20 + i * slot
        px0 = sx + 4 + max(k.width(fmt(v)) for v in ticks) + 16
        px1 = sx + slot - 6
        mid = (px0 + px1) / 2
        k.lines_at(mid, title_top, title_lines[i], anchor="middle")
        Y = lambda v, lo=lo, hi=hi: y1 - (v - lo) / (hi - lo) * (y1 - y0)
        for v in ticks[1:]:
            k.line(px0, Y(v), px1, Y(v), stroke=GRIDC, sw=1.2)
        y_axis(px0, y0, y1, ticks, Y, fmt)
        k.line(px0, y1, px1, y1)
        if ref is not None:          # what the case policies ask for
            k.line(px0, Y(ref), px1, Y(ref), stroke=PHYS, sw=2.4, dash="6 4")
        step = (px1 - px0) / len(SERIES_B)
        assert step > 22, (title, step)
        xs = {key: px0 + step * (j + 0.5) for j, (key, _, _) in enumerate(SERIES_B)}
        for key, _, col in SERIES_B:
            m, a, b = vals[key]
            k.line(xs[key], Y(a), xs[key], Y(b), stroke=col, sw=2.2)
            dot(xs[key], Y(m), key, col, r=9)
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
    ("Bacterial meningitis", {"dx": {"base": (95, 88, 99), "outcome": (93, 85, 98), "policy": (96, 90, 99)},
                              "req": {"base": (48, 41, 55), "outcome": (32, 25, 39), "policy": (84, 78, 90)}}),
    ("High-grade glioma", {"dx": {"base": (84, 75, 92), "outcome": (80, 70, 89), "policy": (86, 77, 93)},
                           "req": {"base": (38, 31, 45), "outcome": (27, 20, 34), "policy": (76, 69, 83)}}),
    ("Hepatic encephalopathy", {"dx": {"base": (78, 68, 87), "outcome": (77, 67, 86), "policy": (80, 70, 89)},
                                "req": {"base": (40, 33, 47), "outcome": (30, 23, 37), "policy": (74, 67, 81)}}),
    ("Myasthenia gravis", {"dx": {"base": (90, 82, 96), "outcome": (89, 81, 95), "policy": (91, 83, 97)},
                           "req": {"base": (44, 37, 51), "outcome": (33, 26, 40), "policy": (82, 75, 88)}}),
]
C_AXES = [("dx", "Correct diagnoses (%)"), ("req", "Required tests ordered (%)")]
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


# ------------------------------------------------------------------ d  right tests, or just more tests
# required tests ordered (%) by a scripted agent that orders the same k tests in every case, the k most
# often required in the training cases, for k = 0..11 -- INVENTED (its end, every test, is near the
# 50% the order-everything agent reaches on the 600 cases)
FIXED = [0, 14, 25, 33, 39, 43, 46, 48, 49, 50, 50, 50]
# {model: (tests per case (mean, lo, hi), required tests ordered (mean, lo, hi))} -- INVENTED
POINTS_D = {"base": ((3.7, 3.4, 4.0), (42, 38, 46)), "outcome": ((2.0, 1.8, 2.2), (31, 27, 35)),
            "policy": ((5.9, 5.6, 6.2), (80, 76, 84))}
REQUIRED = (5.5, 100)          # the required work-up of the case policies -- INVENTED number of tests
KEY_FIXED, KEY_REQ = "Same k tests in every case", "Required work-up"


def diamond(cx, cy, col, r=10.5):
    d = r * 1.25
    k.out.append(f'<path d="M{cx:.1f},{cy - d:.1f} L{cx + d:.1f},{cy:.1f} L{cx:.1f},{cy + d:.1f} '
                 f'L{cx - d:.1f},{cy:.1f} Z" fill="{col}" stroke="#FFFFFF" stroke-width="1.5"/>')


def draw_d():
    k.panel(D_X, Y2, D_W, R2, "d", "Right tests, or just more tests")
    cx, cy, cw, ch = inner(D_X, Y2, D_W, R2)
    ly = legend(cx + 28, cy + 44, cx + cw - 20, "dot")
    y2 = ly + ROW + 6                         # second key line: the scripted agent and the policy
    ym = y2 - S * 0.36
    x = cx + 28
    k.line(x, ym, x + 44, ym, stroke=BLACK, sw=2.4)
    k.marker(x + 22, ym, "circle", BLACK, r=5, stroke="none", sw=0)
    k.text(x + 54, y2, KEY_FIXED)
    x += 54 + k.width(KEY_FIXED) + 30
    diamond(x + 12, ym, PHYS, r=8)
    k.text(x + 32, y2, KEY_REQ)
    assert x + 32 + k.width(KEY_REQ) < cx + cw - 16, x
    px0, px1 = cx + 118, cx + cw - 40
    top, bottom = y2 + 44, cy + ch - 96
    X = lambda v: px0 + v / 12 * (px1 - px0)
    Y = lambda v: bottom - v / 100 * (bottom - top)
    for v in (50, 100):
        k.line(px0, Y(v), px1, Y(v), stroke=GRIDC, sw=1.2)
    y_axis(px0, top, bottom, (0, 50, 100), Y, lambda v: f"{v:.0f}", cx + 34, "Required tests ordered (%)")
    x_axis(px0, px1, bottom, (0, 4, 8, 12), X, "Tests per case")
    polyline([X(i) for i in range(len(FIXED))], [Y(v) for v in FIXED], BLACK, sw=2.2)
    for i, v in enumerate(FIXED):
        k.marker(X(i), Y(v), "circle", BLACK, r=4.5, stroke="none", sw=0)
    diamond(X(REQUIRED[0]), Y(REQUIRED[1]) + 2, PHYS)
    for model, _, col in SERIES:
        (tm, t0, t1), (rm, r0, r1) = POINTS_D[model]
        k.line(X(t0), Y(rm), X(t1), Y(rm), stroke=col, sw=2.2)
        k.line(X(tm), Y(r0), X(tm), Y(r1), stroke=col, sw=2.2)
        k.marker(X(tm), Y(rm), "circle", col, r=10.5)


draw_a()
draw_b()
draw_c()
draw_d()
H = Y2 + R2
assert H <= 1700, H
pdf = k.save(Path(__file__).with_name("fig3-new.svg"), H)
print(f"wrote {pdf} · 180 x {H / 10:.0f} mm")
