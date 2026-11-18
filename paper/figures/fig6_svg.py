"""Figure 6 as a hand-laid SVG: redrawn after the second critical review of 18 Nov 2026, awaiting
approval; invented data.

Run:  uv run --no-project --with pillow python paper/figures/fig6_svg.py  (writes fig6-new.svg/.pdf)

Message (claim C5, R6): the gain comes from the reward. The same Qwen3.5-9B, told the rules in its
prompt, fine-tuned to imitate reference episodes, or run as a panel of five roles that discuss each
step (in the style of MAI-DxO), orders fewer of the required tests than the model trained on the
policy reward, and the panel uses several times the tokens. Two questions, one per panel:
  a  what else could have produced the gain on the same model? Qwen3.5-9B used in five ways. Grey marks
     are the model without reinforcement learning, blue the policy-reward model of Fig. 3;
  b  does a larger model close the gap without training? One larger untrained model alone, with the
     rules in its prompt and as a multi-agent panel (black squares, as the larger models of Fig. 2).
Both panels share their four measures: three of Fig. 3b, none of them the policy score itself, and the
tokens per case, the compute a hospital pays for (prompt and completion tokens over the whole episode,
summed over the roles for the panel).
The second review replaced the earlier figure (policy score against model size and against wall time
per case): both of its panels plotted the reward the model was trained on, and neither answered "why
not just a better prompt or a panel of agents". Wall time and GPU memory stay in Supplementary
Table 10. The data are invented only to place the marks; every printed number is "xx". The larger
model is a placeholder (Qwen3.8-27B) until the choice is made.
"""

from __future__ import annotations

from pathlib import Path

import svgkit as k
from svgkit import BASE, BLACK, MODEL_A, ROW, S

GRIDC = "#EEF1F4"
ROW_H = 62

# (title, range, ticks) -- the columns of both panels
COLUMNS = [("Correct diagnoses (%)", (0, 100), (0, 50, 100)),
           ("Required tests ordered (%)", (0, 100), (0, 50, 100)),
           ("Ordered tests the policy asks for (%)", (0, 100), (0, 50, 100)),
           ("Tokens per case (thousands)", (0, 400), (0, 200, 400))]
# (label, shape, colour, one (mean, lo, hi) per column) -- INVENTED
ROWS_A = [
    ("Untrained", "circle", BASE, [(88, 84, 92), (42, 38, 46), (46, 42, 50), (55, 50, 60)]),
    ("Rules in the prompt", "circle", BASE, [(88, 84, 92), (52, 48, 56), (52, 48, 56), (62, 57, 67)]),
    ("Supervised fine-tuning", "circle", BASE, [(87, 83, 91), (60, 56, 64), (58, 54, 62), (55, 50, 60)]),
    ("Multi-agent panel", "circle", BASE, [(90, 86, 94), (58, 54, 62), (55, 51, 59), (240, 222, 258)]),
    ("Policy reward", "circle", MODEL_A, [(91, 87, 95), (80, 76, 84), (74, 70, 78), (95, 88, 102)]),
]
ROWS_B = [
    ("Untrained", "square", BLACK, [(91, 87, 95), (64, 60, 68), (60, 56, 64), (70, 64, 76)]),
    ("Rules in the prompt", "square", BLACK, [(91, 87, 95), (70, 66, 74), (64, 60, 68), (78, 72, 84)]),
    ("Multi-agent panel", "square", BLACK, [(92, 88, 96), (74, 70, 78), (66, 62, 70), (310, 288, 332)]),
]
LABEL_W = max(k.width(r[0]) for r in ROWS_A + ROWS_B)


def inner(x, y, w, h):
    cx, cy, cw, ch = x + k.PAD, y + k.HEAD, w - 2 * k.PAD, h - k.HEAD - k.PAD
    k.card(cx, cy, cw, ch)
    return cx, cy, cw, ch


def draw(y, h, letter, title, rows):
    """One panel: a row per way of using the model, a small dot plot per measure."""
    k.panel(0, y, k.W, h, letter, title)
    cx, cy, cw, ch = inner(0, y, k.W, h)
    x0 = cx + 28 + 34 + LABEL_W + 50
    gap = 80
    pw = (cx + cw - 36 - x0 - gap * (len(COLUMNS) - 1)) / len(COLUMNS)
    titles = [k.wrap(t, pw + 30) for t, *_ in COLUMNS]
    n_lines = max(len(t) for t in titles)
    assert n_lines <= 2, titles
    title_top = cy + 26
    top = title_top + n_lines * ROW + 14
    bottom = top + ROW_H * len(rows)
    for i, (label, shape, col, _) in enumerate(rows):
        ym = top + (i + 0.5) * ROW_H
        k.marker(cx + 28 + 14, ym, shape, col, r=10)
        k.text(cx + 28 + 34, ym + S * 0.36, label)
    for j, (ctitle, (lo, hi), ticks) in enumerate(COLUMNS):
        px0 = x0 + j * (pw + gap)
        px1 = px0 + pw
        lines = titles[j]
        k.lines_at((px0 + px1) / 2, title_top + (n_lines - len(lines)) * ROW, lines, anchor="middle")
        X = lambda v, px0=px0, px1=px1, lo=lo, hi=hi: px0 + (v - lo) / (hi - lo) * (px1 - px0)
        for v in ticks[1:]:
            k.line(X(v), top, X(v), bottom, stroke=GRIDC, sw=1.2)
        for i, (_, shape, col, vals) in enumerate(rows):
            ym = top + (i + 0.5) * ROW_H
            m, a, b = vals[j]
            k.line(X(a), ym, X(b), ym, stroke=col, sw=2.4)
            k.marker(X(m), ym, shape, col, r=10)
        k.line(px0, bottom, px1, bottom)
        for v in ticks:
            k.line(X(v), bottom, X(v), bottom + 10)
            k.text(X(v), bottom + 10 + S * 1.05, f"{v:g}", anchor="middle")
    assert bottom + 10 + S * 1.05 < cy + ch - 8, (bottom, cy + ch)


def height(n_rows):
    return k.HEAD + 26 + ROW + 14 + ROW_H * n_rows + 10 + S * 1.05 + 46 + k.PAD


R1, R2 = round(height(len(ROWS_A))), round(height(len(ROWS_B)))
draw(0, R1, "a", "Qwen3.5-9B used in five ways", ROWS_A)
draw(R1 + k.GAP, R2, "b", "A larger untrained model, Qwen3.8-27B", ROWS_B)
H = R1 + k.GAP + R2
pdf = k.save(Path(__file__).with_name("fig6-new.svg"), H)
print(f"wrote {pdf} · 180 x {H / 10:.0f} mm")
