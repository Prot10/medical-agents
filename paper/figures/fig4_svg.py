"""Figure 4 as a hand-laid SVG: revised after the two critical reviews of 18 Nov 2026, awaiting approval;
invented data.

Run:  uv run --no-project --with pillow python paper/figures/fig4_svg.py  (writes fig4-new.svg/.pdf)

Message (paper/decisions.md, Fig. 4): the physicians, on MIMIC-IV admissions they have not seen (the
neurologists reviewed the synthetic cases and their policies, so those cannot be used). Two questions,
one per row, and nothing that another figure already shows:
  a, b  does the policy score measure what neurologists value? (blind rating study)
        a  agreement of each automatic score with the ratings, against the agreement between two
           neurologists as the ceiling (the usual way to validate an automatic grader against
           physicians); the LLM-judge row answers the most frequent reviewer request, and the row
           "Number of tests ordered" (second review) answers "the neurologists just like more tests";
        b  the blind rating of each agent's work-ups (untrained, multi-agent panel, outcome reward,
           policy reward): the only test of the main effect that uses no score at all, so it answers
           the circularity objection. The multi-agent panel (second review) is the untrained model run
           as five roles, the baseline of Fig. 6. The ratings by work-up class moved to Extended Data
           Fig. 5;
  c     how close is each model to neurologists who solve the same admissions? Measures read against
        the neurologist of each admission (same diagnosis, same tests), plus the neurologists' own
        required tests and tests per case: the first shows the policy is attainable, the second is the
        number the models are read against ("about as many tests as physicians"). No P values: 20-30
        admissions describe, and the paper claims nothing about beating physicians.
The study design is in the legend and Methods, not in a text panel. Every row is a horizontal dot
plot with its labels on the left, so no label wraps. Grey marks are the untrained Qwen3.5-9B, however
it is run. The data are invented only to place the marks; every printed number is "xx".
"""

from __future__ import annotations

from pathlib import Path

import svgkit as k
from svgkit import BASE, INK, MODEL_A, MODEL_B, MUTED, PHYS, S

XX = "xx"
GRIDC = "#EEF1F4"

R1, R2 = 562, 470
A_W = 900
B_X, B_W = A_W + k.GAP, k.W - A_W - k.GAP
Y2 = R1 + k.GAP
ROW_H = 62                      # one dot-plot row


def inner(x, y, w, h):
    cx, cy, cw, ch = x + k.PAD, y + k.HEAD, w - 2 * k.PAD, h - k.HEAD - k.PAD
    k.card(cx, cy, cw, ch)
    return cx, cy, cw, ch


def diamond(cx, cy, col, r=10.5):
    d = r * 1.25
    k.out.append(f'<path d="M{cx:.1f},{cy - d:.1f} L{cx + d:.1f},{cy:.1f} L{cx:.1f},{cy + d:.1f} '
                 f'L{cx - d:.1f},{cy:.1f} Z" fill="{col}" stroke="#FFFFFF" stroke-width="1.5"/>')


def x_axis(px0, px1, y, ticks, X, label, fmt=lambda v: f"{v:g}"):
    k.line(px0, y, px1, y)
    for v in ticks:
        k.line(X(v), y, X(v), y + 10)
        k.text(X(v), y + 10 + S * 1.05, fmt(v), anchor="middle")
    k.text((px0 + px1) / 2, y + 10 + S * 2.45, label, anchor="middle")


def grid(xs, top, bottom):
    for x in xs:
        k.line(x, top, x, bottom, stroke=GRIDC, sw=1.2)


# ------------------------------------------------------------------ a  agreement with the ratings
# (score, rho, lo, hi) -- INVENTED
SCORES = [("Policy score", .62, .53, .70), ("Outcome score", .34, .22, .45),
          ("Correct diagnoses only", .29, .17, .40), ("Number of tests ordered", .31, .19, .42),
          ("LLM judge", .41, .30, .51)]
BETWEEN = (.66, .58, .73)          # rho between two neurologists rating the same work-ups -- INVENTED


def draw_a():
    k.panel(0, 0, A_W, R1, "a", "Which score agrees with the neurologists' rating")
    cx, cy, cw, ch = inner(0, 0, A_W, R1)
    label_w = max(k.width(s[0]) for s in SCORES)
    px0, px1 = cx + 28 + label_w + 44, cx + cw - 130
    X = lambda v: px0 + v * (px1 - px0)
    top = cy + 74
    bottom = top + ROW_H * len(SCORES)
    # key for the band, one line above the plot
    k.out.append(f'<rect x="{px0:.1f}" y="{cy + 26:.1f}" width="30" height="18" rx="4" fill="{PHYS}" '
                 f'fill-opacity="0.25"/>')
    k.line(px0 + 15, cy + 26, px0 + 15, cy + 44, stroke=PHYS, sw=2.4)
    k.text(px0 + 42, cy + 41, "Two neurologists with each other")
    m, lo, hi = BETWEEN
    k.out.append(f'<rect x="{X(lo):.1f}" y="{top:.1f}" width="{X(hi) - X(lo):.1f}" height="{bottom - top:.1f}" '
                 f'fill="{PHYS}" fill-opacity="0.25"/>')
    grid([X(v) for v in (0.25, 0.5, 0.75, 1.0)], top, bottom)
    k.line(X(m), top, X(m), bottom, stroke=PHYS, sw=2.4)
    ys = []
    for i, (name, r, a, b) in enumerate(SCORES):
        ym = top + (i + 0.5) * ROW_H
        ys.append(ym)
        k.text(cx + 28, ym + S * 0.36, name)
        k.line(X(a), ym, X(b), ym, stroke=INK, sw=2.4)
        k.marker(X(r), ym, "circle", INK, r=10.5)
    bx = px1 + 34
    k.out.append(f'<path d="M{bx - 8:.1f},{ys[0]:.1f} H{bx:.1f} V{ys[1]:.1f} H{bx - 8:.1f}" fill="none" '
                 f'stroke="{INK}" stroke-width="1.4"/>')
    k.text(bx + 12, (ys[0] + ys[1]) / 2 + S * 0.36, f"P = {XX}")
    x_axis(px0, px1, bottom, (0, 0.25, 0.5, 0.75, 1.0), X, "Spearman correlation")
    assert bottom + 10 + S * 2.45 < cy + ch - 8


# ------------------------------------------------------------------ b  blind rating of each model
# (agent, colour, mean rating, lo, hi) -- INVENTED; all rated work-ups, whatever the diagnosis
CLASSES = [("Untrained", BASE, 2.9, 2.6, 3.2), ("Multi-agent panel", BASE, 3.2, 2.9, 3.5),
           ("Outcome reward", MODEL_B, 2.6, 2.3, 2.9), ("Policy reward", MODEL_A, 3.9, 3.6, 4.2)]


def draw_b():
    k.panel(B_X, 0, B_W, R1, "b", "Blind rating of each agent's work-ups")
    cx, cy, cw, ch = inner(B_X, 0, B_W, R1)
    label_w = max(k.width(c[0]) for c in CLASSES) + 34
    n_w = k.width(f"n = {XX}")
    p_w = k.width(f"P = {XX}") + 34                 # room for the bracket between the plot and n
    px0, px1 = cx + 28 + label_w + 40, cx + cw - 28 - n_w - 30 - p_w
    X = lambda v: px0 + (v - 1) / 4 * (px1 - px0)
    top = cy + 74 + ROW_H / 2                        # four rows, centred against the five of a
    bottom = top + ROW_H * len(CLASSES)
    grid([X(v) for v in (2, 3, 4, 5)], top, bottom)
    for i, (name, col, m, a, b) in enumerate(CLASSES):
        ym = top + (i + 0.5) * ROW_H
        k.marker(cx + 28 + 14, ym, "circle", col, r=10)
        k.text(cx + 28 + 34, ym + S * 0.36, name)
        k.line(X(a), ym, X(b), ym, stroke=col, sw=2.6)
        k.marker(X(m), ym, "circle", col, r=11)
        k.text(cx + cw - 28, ym + S * 0.36, f"n = {XX}", fill=MUTED, anchor="end")
    # paired test, policy against outcome reward (the last two rows)
    y_o, y_p = top + 2.5 * ROW_H, top + 3.5 * ROW_H
    bx = px1 + 22
    k.out.append(f'<path d="M{bx - 8:.1f},{y_o:.1f} H{bx:.1f} V{y_p:.1f} H{bx - 8:.1f}" fill="none" '
                 f'stroke="{INK}" stroke-width="1.4"/>')
    k.text(bx + 12, (y_o + y_p) / 2 + S * 0.36, f"P = {XX}")
    x_axis(px0, px1, bottom, (1, 2, 3, 4, 5), X, "Neurologists' rating, 1 to 5")


# ------------------------------------------------------------------ c  models against the neurologists
SERIES = [("phys", "Neurologists", PHYS), ("base", "Untrained", BASE), ("outcome", "Outcome reward", MODEL_B),
          ("policy", "Policy reward", MODEL_A)]
# (title, range, ticks, {series: (mean, lo, hi) or None}) -- INVENTED; None: not defined for that series
MEASURES = [
    ("Agrees on the diagnosis (%)", (0, 100), (0, 50, 100),
     {"phys": None, "base": (80, 70, 88), "outcome": (81, 71, 89), "policy": (84, 75, 91)}),
    ("Neurologist's tests ordered (%)", (0, 100), (0, 50, 100),
     {"phys": None, "base": (44, 36, 52), "outcome": (30, 23, 37), "policy": (72, 64, 79)}),
    ("Required tests ordered (%)", (0, 100), (0, 50, 100),
     {"phys": (84, 77, 90), "base": (42, 34, 50), "outcome": (31, 24, 38), "policy": (79, 71, 86)}),
    ("Tests per case", (0, 10), (0, 5, 10),
     {"phys": (5.4, 4.8, 6.0), "base": (3.7, 3.2, 4.2), "outcome": (2.0, 1.6, 2.4), "policy": (5.9, 5.3, 6.5)}),
]


def draw_c():
    k.panel(0, Y2, k.W, R2, "c", f"Models against neurologists who solved the same {XX} MIMIC-IV admissions")
    cx, cy, cw, ch = inner(0, Y2, k.W, R2)
    label_w = max(k.width(s[1]) for s in SERIES)
    x0 = cx + 28 + 34 + label_w + 50
    gap = 70
    pw = (cx + cw - 36 - x0 - gap * (len(MEASURES) - 1)) / len(MEASURES)
    title_y = cy + 41
    top = cy + 74
    bottom = top + ROW_H * len(SERIES)
    for i, (key, label, col) in enumerate(SERIES):
        ym = top + (i + 0.5) * ROW_H
        if key == "phys":
            diamond(cx + 28 + 14, ym, col, r=9)
        else:
            k.marker(cx + 28 + 14, ym, "circle", col, r=10)
        k.text(cx + 28 + 34, ym + S * 0.36, label)
    for j, (title, (lo, hi), ticks, vals) in enumerate(MEASURES):
        px0 = x0 + j * (pw + gap)
        px1 = px0 + pw
        assert k.width(title) < pw + gap - 20, title
        k.text((px0 + px1) / 2, title_y, title, anchor="middle")
        X = lambda v, px0=px0, px1=px1, lo=lo, hi=hi: px0 + (v - lo) / (hi - lo) * (px1 - px0)
        grid([X(v) for v in ticks[1:]], top, bottom)
        for i, (key, _, col) in enumerate(SERIES):
            ym = top + (i + 0.5) * ROW_H
            if vals[key] is None:
                k.text((px0 + px1) / 2, ym + S * 0.36, "reference", fill=MUTED, anchor="middle")
                continue
            m, a, b = vals[key]
            k.line(X(a), ym, X(b), ym, stroke=col, sw=2.4)
            if key == "phys":
                diamond(X(m), ym, col)
            else:
                k.marker(X(m), ym, "circle", col, r=10)
        k.line(px0, bottom, px1, bottom)
        for v in ticks:
            k.line(X(v), bottom, X(v), bottom + 10)
            k.text(X(v), bottom + 10 + S * 1.05, f"{v:g}", anchor="middle")
    assert bottom + 10 + S * 1.05 < cy + ch - 8


draw_a()
draw_b()
draw_c()
H = Y2 + R2
assert H <= 1700, H
pdf = k.save(Path(__file__).with_name("fig4-new.svg"), H)
print(f"wrote {pdf} · 180 x {H / 10:.0f} mm")
