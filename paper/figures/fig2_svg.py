"""Figure 2 as a hand-laid SVG: layout approved by Andrea on 18 Nov 2026, invented data (first drawn 17 Nov 2026).

Run:  uv run --no-project --with pillow python paper/figures/fig2_svg.py  (writes fig2-new.svg/.pdf)

Message (paper/decisions.md, Fig. 2): untrained models often reach the right diagnosis with wrong or
missing tests, so counting correct diagnoses alone hides the work-up and ranks models differently from the policy score.
The data below are invented only to place the marks; every number printed in the figure is "xx"
until the panel runs (scored with clinical-policy-v3) replace them.

Layout, two rows read a -> b, then c -> d:
  a  correct diagnoses vs policy score, one point per model with 95% CIs (SDBench Fig. 7 accuracy vs cost;
     npj Digit. Med. 2026 Fig. 2b accuracy vs tokens);
  b  the two rankings side by side (AgentClinic Fig. 3: one benchmark does not predict the other);
  c  100% stacked bars of what lies behind correct diagnoses (npj Digit. Med. 2026 Fig. 2a);
  d  the same correct diagnosis reached by three work-ups (the hook moved from the October Fig. 1e).
Models only (18 Nov): the neurologists left this figure for Fig. 4, where they are compared with the
models on the same cases; here they covered only xx of the cases the models solved.
"""

from __future__ import annotations

from pathlib import Path

import svgkit as k
from svgkit import BASE, BLACK, ERR, ERR_T, GREY_T, INK, LINE, MUTED, OK, OK_T, ROW, S, SKY, YELLOW

XX = "xx"   # printed in place of every number until the real runs exist

# (name, size class, correct diagnoses %, 95% CI, policy score, 95% CI) -- INVENTED, only to place the marks
MODELS = [
    ("GLM-5.3", "large", 93, (91, 95), 0.45, (0.43, 0.47)),
    ("Qwen3.8-27B", "large", 91, (89, 93), 0.58, (0.55, 0.61)),
    ("gpt-oss-20b", "large", 90, (87, 92), 0.41, (0.38, 0.43)),
    ("Qwen3.5-9B", "small", 88, (85, 91), 0.49, (0.46, 0.52)),
    ("Gemma 4 E4B", "small", 84, (81, 87), 0.27, (0.24, 0.29)),
    ("Granite 4.1 8B", "small", 79, (75, 82), 0.34, (0.31, 0.37)),
]
STYLE = {"small": ("circle", BASE), "large": ("square", BLACK)}
LEGEND = [("small", "Open models up to 9B"), ("large", "Larger models")]
# share of correct diagnoses (%): complete and lean, complete with useless tests, a required test missed,
# an unsafe action -- INVENTED. Over-ordering gets its own class because reviewers of a Nature test-ordering
# agent (MIRA, 2026) asked for precision and a penalty for unnecessary tests, not recall only.
HIDDEN = {"GLM-5.3": (30, 14, 46, 10), "Qwen3.8-27B": (40, 17, 36, 7), "gpt-oss-20b": (22, 16, 50, 12),
          "Qwen3.5-9B": (35, 12, 42, 11), "Gemma 4 E4B": (16, 8, 61, 15), "Granite 4.1 8B": (22, 8, 57, 13)}
HIDDEN_KEYS = [("Complete", OK), ("Complete, useless tests", SKY), ("Required test missed", YELLOW),
               ("Unsafe action", ERR)]

R1, R2 = 640, 620
A_W = 940
B_X, B_W = A_W + k.GAP, k.W - A_W - k.GAP
C_W = 640
D_X, D_W = C_W + k.GAP, k.W - C_W - k.GAP
Y2 = R1 + k.GAP
NAME_W = max(k.width(m[0]) for m in MODELS)


def inner(x, y, w, h):
    """The white card inside a panel."""
    cx, cy, cw, ch = x + k.PAD, y + k.HEAD, w - 2 * k.PAD, h - k.HEAD - k.PAD
    k.card(cx, cy, cw, ch)
    return cx, cy, cw, ch


def legend_models(x, y):
    for cls, label in LEGEND:
        shape, col = STYLE[cls]
        k.marker(x + 9, y - S * 0.36, shape, col, r=9)
        k.text(x + 26, y, label)
        x += 26 + k.width(label) + 36
    return x


# ------------------------------------------------------------------ a  correct diagnoses vs policy score
def draw_a():
    k.panel(0, 0, A_W, R1, "a", "Correct diagnoses and policy score")
    cx, cy, cw, ch = inner(0, 0, A_W, R1)
    legend_models(cx + 28, cy + 44)
    px0, px1 = cx + 116, cx + cw - 190      # room on the right for direct labels
    py0, py1 = cy + 86, cy + ch - 96
    xmin, xmax, ymin, ymax = 75, 95, 0.2, 0.7
    X = lambda v: px0 + (v - xmin) / (xmax - xmin) * (px1 - px0)
    Y = lambda v: py1 - (v - ymin) / (ymax - ymin) * (py1 - py0)
    for v in (0.3, 0.4, 0.5, 0.6, 0.7):
        k.line(px0, Y(v), px1, Y(v), stroke="#EEF1F4", sw=1.2)
    for v in (75, 80, 85, 90, 95):
        k.line(X(v), py1, X(v), py1 + 10)
        k.text(X(v), py1 + 10 + S * 1.05, str(v), anchor="middle")
    for v in (0.2, 0.3, 0.4, 0.5, 0.6, 0.7):
        k.line(px0 - 10, Y(v), px0, Y(v))
        k.text(px0 - 16, Y(v) + S * 0.36, f"{v:.1f}", anchor="end")
    k.line(px0, py1, px1, py1)
    k.line(px0, py0, px0, py1)
    k.text((px0 + px1) / 2, py1 + 10 + S * 2.4, "Correct diagnoses (%)", anchor="middle")
    k.text(cx + 34, (py0 + py1) / 2, "Policy score", anchor="middle", rotate=-90)
    # 95% CIs as thin lines, the point on top, the name just past the end of its CI
    left = {"Qwen3.5-9B"}           # labels that would cross a neighbour's CI go on the left
    for name, cls, acc, (a0, a1), sc, (s0, s1) in MODELS:
        shape, col = STYLE[cls]
        k.line(X(a0), Y(sc), X(a1), Y(sc), stroke=col, sw=1.6)
        k.line(X(acc), Y(s0), X(acc), Y(s1), stroke=col, sw=1.6)
        k.marker(X(acc), Y(sc), shape, col, r=10.5)
        if name in left:
            k.text(X(a0) - 12, Y(sc) + S * 0.36, name, anchor="end")
        else:
            k.text(X(a1) + 12, Y(sc) + S * 0.36, name)
            assert X(a1) + 12 + k.width(name) < cx + cw - 12, name


# ------------------------------------------------------------------ b  two rankings
def draw_b():
    k.panel(B_X, 0, B_W, R1, "b", "The two rankings differ")
    cx, cy, cw, ch = inner(B_X, 0, B_W, R1)
    by_acc = [m[0] for m in sorted(MODELS, key=lambda m: -m[2])]
    by_pol = [m[0] for m in sorted(MODELS, key=lambda m: -m[4])]
    cls = {m[0]: m[1] for m in MODELS}
    lx = cx + 40 + NAME_W + 20
    rx = cx + cw - 40 - NAME_W - 20
    top, bottom = cy + 96, cy + ch - 92
    step = (bottom - top) / (len(by_acc) - 1)
    k.text(lx + 10, cy + 44, "By correct diagnoses", bold=True, anchor="end")
    k.text(rx - 10, cy + 44, "By policy score", bold=True)
    for i, n in enumerate(by_acc):
        j = by_pol.index(n)
        shape, col = STYLE[cls[n]]
        y0, y1 = top + i * step, top + j * step
        k.line(lx, y0, rx, y1, stroke=col, sw=2.2, cap="round")
        k.marker(lx, y0, shape, col, r=9.5)
        k.marker(rx, y1, shape, col, r=9.5)
        k.text(lx - 20, y0 + S * 0.36, n, anchor="end")
        k.text(rx + 20, y1 + S * 0.36, n)
    k.line(cx + 28, cy + ch - 58, cx + cw - 28, cy + ch - 58, stroke=LINE, sw=1.2)
    k.text(cx + cw / 2, cy + ch - 24, f"Kendall's tau {XX} (95% CI {XX} to {XX})", anchor="middle")


# ------------------------------------------------------------------ c  what correct diagnoses hide
def draw_c():
    k.panel(0, Y2, C_W, R2, "c", "What correct diagnoses hide")
    cx, cy, cw, ch = inner(0, Y2, C_W, R2)
    lx, ky = cx + 28, cy + 44
    for label, col in HIDDEN_KEYS:
        if lx + 26 + k.width(label) > cx + cw - 20:
            lx, ky = cx + 28, ky + ROW + 6
        lx = k.key(lx, ky, col, label)
    n_w = k.width(f"n = {XX}")
    bx0, bx1 = cx + 28 + NAME_W + 20, cx + cw - 32 - n_w - 20
    top, bottom = ky + 34, cy + ch - 96
    rows = [m[0] for m in MODELS]
    step = (bottom - top) / len(rows)
    bar_h = step * 0.6
    for i, name in enumerate(rows):
        y = top + i * step + (step - bar_h) / 2
        k.text(bx0 - 20, y + bar_h / 2 + S * 0.36, name, anchor="end")
        k.text(cx + cw - 32, y + bar_h / 2 + S * 0.36, f"n = {XX}", fill=MUTED, anchor="end")
        x = bx0
        for share, (_, col) in zip(HIDDEN[name], HIDDEN_KEYS):
            w = (bx1 - bx0) * share / 100
            k.rect(x, y, w - 2, bar_h, col, rx=0)          # 2-unit white gap between segments
            if k.width(XX) + 16 < w:
                k.text(x + w / 2 - 1, y + bar_h / 2 + S * 0.36, XX, anchor="middle")
            x += w
    for v in (0, 25, 50, 75, 100):
        xv = bx0 + (bx1 - bx0) * v / 100
        k.line(xv, bottom, xv, bottom + 10)
        k.text(xv, bottom + 10 + S * 1.05, str(v), anchor="middle")
    k.line(bx0, bottom, bx1, bottom)
    k.text((bx0 + bx1) / 2, bottom + 10 + S * 2.4, "Share of correct diagnoses (%)", anchor="middle")


# ------------------------------------------------------------------ d  same diagnosis, three work-ups
CASE_D = "One case, fever, headache and neck stiffness; all three reach the right diagnosis"
# (model, [(test, kind)]) -- INVENTED; kind: req = required and in order, no = not needed, late = out of order
WORKUPS = [
    ("Qwen3.8-27B", [("Blood cultures", "req"), ("Head CT", "req"), ("Lumbar puncture", "req"),
                     ("Blood tests", "req")]),
    ("gpt-oss-20b", [("Brain MRI", "no"), ("EEG", "no"), ("Lumbar puncture", "late"),
                     ("Blood cultures", "late")]),
    ("Granite 4.1 8B", []),
]
CHIP = {"req": (OK_T, OK, "Required, in order"), "no": (GREY_T, "#9AA3AE", "Not needed"),
        "late": (ERR_T, ERR, "Out of order")}


def draw_d():
    k.panel(D_X, Y2, D_W, R2, "d", "Same correct diagnosis, three work-ups")
    cx, cy, cw, ch = inner(D_X, Y2, D_W, R2)
    k.text(cx + 28, cy + 44, CASE_D)
    lx = cx + 28
    for kind in ("req", "no", "late"):
        fill, stroke, label = CHIP[kind]
        lx = k.key(lx, cy + 44 + ROW + 12, fill, label, stroke=stroke, pill=True)
    col_cost, col_score = cx + cw - 150, cx + cw - 30
    head_y = cy + 44 + 2 * ROW + 44
    k.text(cx + 28, head_y, "Tests, in the order requested", bold=True)
    k.text(col_cost, head_y, "Cost ($)", bold=True, anchor="end")
    k.text(col_score, head_y, "Score", bold=True, anchor="end")
    k.line(cx + 28, head_y + 16, cx + cw - 28, head_y + 16, stroke=LINE, sw=1.2)
    top = head_y + 16
    step = (cy + ch - 16 - top) / len(WORKUPS)
    chip_h = 40
    for i, (name, tests) in enumerate(WORKUPS):
        y_name = top + i * step + 22
        k.text(cx + 28, y_name + S * 0.72, name, bold=True)
        ym = y_name + S + 12 + chip_h / 2          # chips under the name
        x = cx + 28
        if not tests:
            k.text(x, ym + S * 0.36, "No test ordered", fill=MUTED)
        for t, (test, kind) in enumerate(tests):
            fill, stroke, _ = CHIP[kind]
            w = k.width(test) + 30
            k.rect(x, ym - chip_h / 2, w, chip_h, fill, rx=chip_h / 2, stroke=stroke, sw=1.5)
            k.text(x + w / 2, ym + S * 0.36, test, anchor="middle")
            x += w
            if t < len(tests) - 1:
                k.out.append(f'<path d="M{x + 8:.1f},{ym - 6:.1f} l6,6 l-6,6" fill="none" stroke="{MUTED}" '
                             f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
                x += 22
        assert x < col_cost - 140, (name, x, col_cost)
        k.text(col_cost, ym + S * 0.36, XX, anchor="end")
        k.text(col_score, ym + S * 0.36, XX, bold=True, anchor="end")
        if i < len(WORKUPS) - 1:
            yl = top + (i + 1) * step
            k.line(cx + 28, yl, cx + cw - 28, yl, stroke="#EEF1F4", sw=1.2)


draw_a()
draw_b()
draw_c()
draw_d()
H = Y2 + R2
assert H <= 1700, H
pdf = k.save(Path(__file__).with_name("fig2-new.svg"), H)
print(f"wrote {pdf} · 180 x {H / 10:.0f} mm")
