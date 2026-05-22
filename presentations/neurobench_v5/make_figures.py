"""Generate figures + summary statistics for the NeuroBench v5 slide deck.

Run from repo root:
    uv run python presentations/neurobench_v5/make_figures.py
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

REPO = Path(__file__).resolve().parents[2]
CASES_DIR = REPO / "data" / "neurobench_v5" / "cases"
OUT_DIR = Path(__file__).resolve().parent / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

CONDITION_LABELS = {
    "als":                          "ALS",
    "alzheimers_early":             "Early Alzheimer's",
    "bacterial_meningitis":         "Bacterial meningitis",
    "focal_epilepsy_temporal":      "Temporal lobe epilepsy",
    "functional_neurological_disorder": "FND",
    "ftd":                          "FTD",
    "guillain_barre":               "Guillain-Barre",
    "brain_tumor_glioma":           "High-grade glioma",
    "hepatic_encephalopathy":       "Hepatic encephalopathy",
    "ischemic_stroke":              "Ischemic stroke",
    "myasthenia_gravis":            "Myasthenia gravis",
    "migraine_with_aura":           "Migraine w/ aura",
    "multiple_sclerosis":           "MS (relapsing-remitting)",
    "autoimmune_encephalitis_nmdar": "NMDAR encephalitis",
    "nph":                          "NPH",
    "parkinsons":                   "Parkinson's disease",
    "peripheral_neuropathy":        "Peripheral neuropathy",
    "subarachnoid_hemorrhage":      "SAH",
    "status_epilepticus":           "Status epilepticus",
    "syncope_cardiac":              "Cardiac syncope",
}

# CERN cafein palette (exact hex values from beamerthemeCERN.sty)
CERN = {
    "blue":      "#0033A0",
    "cyan":      "#61C4D3",
    "orange":    "#E15E32",
    "gray":      "#BEBECB",
    "purple":    "#6E2466",
    "navy":      "#1C446A",
    "textdark":  "#2F2F2F",
    "bodytext":  "#171717",
    "lightbg":   "#F8F8F8",
    "white":     "#FFFFFF",
}

DIFFICULTY_ORDER = ["straightforward", "moderate", "diagnostic_puzzle"]
DIFFICULTY_COLOR = {
    "straightforward":   CERN["cyan"],
    "moderate":          CERN["blue"],
    "diagnostic_puzzle": CERN["orange"],
}
DIFFICULTY_LABEL = {
    "straightforward":   "Straightforward",
    "moderate":          "Moderate",
    "diagnostic_puzzle": "Diagnostic puzzle",
}

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.titlecolor": CERN["blue"],
    "axes.labelcolor": CERN["textdark"],
    "axes.edgecolor":  CERN["textdark"],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color":   CERN["gray"],
    "grid.linewidth": 0.55,
    "grid.alpha":  0.45,
    "xtick.color": CERN["textdark"],
    "ytick.color": CERN["textdark"],
    "legend.frameon": False,
    "figure.facecolor": "white",
    "savefig.facecolor": "white",
    "figure.dpi": 140,
    "savefig.bbox": "tight",
})


def _style_axis(ax, *, x_grid: bool = False, y_grid: bool = True):
    """Apply a consistent CERN-themed grid to a single axes."""
    ax.set_axisbelow(True)
    ax.xaxis.grid(x_grid, color=CERN["gray"], linewidth=0.55, alpha=0.45)
    ax.yaxis.grid(y_grid, color=CERN["gray"], linewidth=0.55, alpha=0.45)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(CERN["textdark"])
        ax.spines[s].set_linewidth(0.8)


def load_cases() -> list[dict]:
    cases = []
    for p in sorted(CASES_DIR.glob("*.json")):
        with p.open() as f:
            cases.append(json.load(f))
    return cases


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

def fig_condition_distribution(cases: list[dict]):
    by_cond_diff = defaultdict(lambda: Counter())
    for c in cases:
        by_cond_diff[c["condition"]][c["difficulty"]] += 1

    conditions = sorted(by_cond_diff.keys(),
                        key=lambda k: -sum(by_cond_diff[k].values()))
    labels = [CONDITION_LABELS.get(k, k) for k in conditions]
    counts = {d: [by_cond_diff[k].get(d, 0) for k in conditions] for d in DIFFICULTY_ORDER}

    fig, ax = plt.subplots(figsize=(11.5, 6.4))
    bottoms = np.zeros(len(conditions))
    for d in DIFFICULTY_ORDER:
        vals = np.array(counts[d])
        ax.bar(labels, vals, bottom=bottoms,
               color=DIFFICULTY_COLOR[d],
               edgecolor="white", linewidth=0.9,
               label=DIFFICULTY_LABEL[d])
        bottoms += vals

    for i, k in enumerate(conditions):
        total = sum(by_cond_diff[k].values())
        ax.text(i, total + 0.7, str(total),
                ha="center", va="bottom",
                fontsize=9.5, color=CERN["textdark"],
                fontweight="bold")

    ax.set_ylabel("Cases", fontweight="bold")
    ax.set_title(f"{len(cases)} cases across {len(conditions)} neurological conditions",
                 pad=12)
    ax.set_ylim(0, max(sum(by_cond_diff[k].values()) for k in conditions) + 6)
    ax.tick_params(axis="x", rotation=45)
    for tick in ax.get_xticklabels():
        tick.set_ha("right")
    _style_axis(ax, x_grid=False, y_grid=True)
    leg = ax.legend(title="Difficulty", loc="upper right",
                    title_fontsize=10, fontsize=10,
                    handlelength=1.4, handleheight=1.1)
    leg.get_title().set_color(CERN["blue"])
    leg.get_title().set_fontweight("bold")
    fig.savefig(OUT_DIR / "condition_distribution.pdf")
    plt.close(fig)


def fig_difficulty_pie(cases: list[dict]):
    counts = Counter(c["difficulty"] for c in cases)
    labels = [DIFFICULTY_LABEL[d] for d in DIFFICULTY_ORDER]
    sizes = [counts[d] for d in DIFFICULTY_ORDER]
    colors = [DIFFICULTY_COLOR[d] for d in DIFFICULTY_ORDER]

    fig, ax = plt.subplots(figsize=(6.8, 5.4))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=labels,
        colors=colors,
        autopct=lambda pct: f"{pct:.0f}%\n({int(round(pct/100*sum(sizes)))})",
        startangle=90,
        pctdistance=0.74,
        labeldistance=1.08,
        wedgeprops=dict(linewidth=2.5, edgecolor="white"),
        textprops=dict(color=CERN["textdark"], fontsize=11),
    )
    # Donut hole
    centre = plt.Circle((0, 0), 0.55, fc="white", linewidth=0)
    ax.add_artist(centre)
    ax.text(0, 0.10, f"{sum(sizes)}",
            ha="center", va="center",
            fontsize=22, fontweight="bold", color=CERN["blue"])
    ax.text(0, -0.18, "cases",
            ha="center", va="center",
            fontsize=11, color=CERN["textdark"])
    for t in autotexts:
        t.set_color("white")
        t.set_fontweight("bold")
        t.set_fontsize(10)
    ax.set_title("Difficulty distribution", pad=14)
    ax.set(aspect="equal")
    # Remove grid/spines for pie
    ax.grid(False)
    for s in ax.spines.values():
        s.set_visible(False)
    fig.savefig(OUT_DIR / "difficulty_pie.pdf")
    plt.close(fig)


def fig_demographics(cases: list[dict]):
    ages = [c["patient"]["demographics"]["age"] for c in cases]
    sexes = [c["patient"]["demographics"]["sex"] for c in cases]

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.5),
                             gridspec_kw=dict(width_ratios=[1.6, 1.0]))

    # Age
    ax = axes[0]
    ax.hist(ages, bins=np.arange(0, 101, 5),
            color=CERN["blue"], edgecolor="white", linewidth=0.9)
    ax.axvline(np.median(ages), color=CERN["orange"], linewidth=2.0,
               linestyle="--", label=f"median {int(np.median(ages))} y")
    ax.set_xlabel("Age (years)", fontweight="bold")
    ax.set_ylabel("Cases", fontweight="bold")
    ax.set_title(f"Age distribution (range {min(ages)}-{max(ages)})", pad=10)
    ax.legend(loc="upper left", fontsize=10)
    _style_axis(ax)

    # Sex
    ax = axes[1]
    sex_counts = Counter(sexes)
    order = sorted(sex_counts, key=lambda x: -sex_counts[x])
    sex_palette = [CERN["blue"], CERN["purple"], CERN["gray"]]
    bars = ax.bar(order, [sex_counts[s] for s in order],
                  color=sex_palette[:len(order)],
                  edgecolor="white", linewidth=0.9)
    for b, s in zip(bars, order):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+3,
                f"{sex_counts[s]}\n({sex_counts[s]/len(cases)*100:.0f}%)",
                ha="center", va="bottom",
                fontsize=10, color=CERN["textdark"], fontweight="bold")
    ax.set_ylabel("Cases", fontweight="bold")
    ax.set_title("Sex distribution", pad=10)
    ax.set_ylim(0, max(sex_counts.values()) * 1.22)
    _style_axis(ax)

    fig.suptitle("Patient demographics",
                 fontsize=14, fontweight="bold", y=1.03,
                 color=CERN["blue"])
    fig.savefig(OUT_DIR / "demographics.pdf")
    plt.close(fig)


def fig_encounter_and_tools(cases: list[dict]):
    enc = Counter(c["encounter_type"] for c in cases)
    initial_tools = Counter()
    followup_tools = Counter()
    n_followups = []
    followup_alias = {
        "search_literature":  "search_medical_literature",
        "literature_search":  "search_medical_literature",
        "interpret_eeg":      "analyze_eeg",
        "run_eeg":            "analyze_eeg",
    }
    for c in cases:
        for k in c.get("initial_tool_outputs", {}) or {}:
            initial_tools[k] += 1
        ups = c.get("followup_outputs") or []
        n_followups.append(len(ups))
        for u in ups:
            raw = u.get("tool_name") or "(unspecified)"
            followup_tools[followup_alias.get(raw, raw)] += 1

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6),
                             gridspec_kw=dict(width_ratios=[1.0, 1.3]))

    # Encounter type
    ax = axes[0]
    enc_order = sorted(enc, key=lambda x: -enc[x])
    enc_palette = [CERN["blue"], CERN["cyan"], CERN["gray"]]
    bars = ax.bar(enc_order, [enc[e] for e in enc_order],
                  color=enc_palette[:len(enc_order)],
                  edgecolor="white", linewidth=0.9)
    for b, e in zip(bars, enc_order):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+4,
                f"{enc[e]}\n({enc[e]/len(cases)*100:.0f}%)",
                ha="center", va="bottom",
                fontsize=10, color=CERN["textdark"], fontweight="bold")
    ax.set_ylabel("Cases", fontweight="bold")
    ax.set_title("Encounter type", pad=10)
    ax.set_ylim(0, max(enc.values()) * 1.22)
    ax.tick_params(axis="x", rotation=15)
    _style_axis(ax)

    # Follow-ups histogram
    ax = axes[1]
    ax.hist(n_followups,
            bins=np.arange(min(n_followups), max(n_followups)+2)-0.5,
            color=CERN["purple"], edgecolor="white", linewidth=0.9)
    ax.axvline(np.median(n_followups), color=CERN["orange"],
               linewidth=2.0, linestyle="--",
               label=f"median {int(np.median(n_followups))}")
    ax.set_xlabel("Follow-up outputs per case", fontweight="bold")
    ax.set_ylabel("Cases", fontweight="bold")
    ax.set_title(f"Pre-generated follow-ups (total {sum(n_followups):,})",
                 pad=10)
    ax.legend(loc="upper right", fontsize=10)
    _style_axis(ax)

    fig.suptitle("Encounter and tool-output coverage",
                 fontsize=14, fontweight="bold", y=1.03,
                 color=CERN["blue"])
    fig.savefig(OUT_DIR / "encounter_and_followups.pdf")
    plt.close(fig)

    return initial_tools, followup_tools, n_followups


TOOL_LABELS = {
    "analyze_brain_mri":          "analyze_brain_mri",
    "analyze_eeg":                "analyze_eeg",
    "analyze_ecg":                "analyze_ecg",
    "interpret_labs":             "interpret_labs",
    "analyze_csf":                "analyze_csf",
    "order_ct_scan":              "order_ct_scan",
    "order_echocardiogram":       "order_echocardiogram",
    "order_cardiac_monitoring":   "order_cardiac_monitoring",
    "order_advanced_imaging":     "order_advanced_imaging",
    "order_specialized_test":     "order_specialized_test",
    "search_medical_literature":  "search_medical_literature",
    "check_drug_interactions":    "check_drug_interactions",
}
INITIAL_KEY_TO_TOOL = {
    "mri": "analyze_brain_mri",
    "eeg": "analyze_eeg",
    "ecg": "analyze_ecg",
    "labs": "interpret_labs",
    "csf": "analyze_csf",
    "ct": "order_ct_scan",
    "echo": "order_echocardiogram",
    "cardiac_monitoring": "order_cardiac_monitoring",
    "advanced_imaging": "order_advanced_imaging",
    "specialized_test": "order_specialized_test",
    "literature_search": "search_medical_literature",
    "drug_interactions": "check_drug_interactions",
}


def fig_tool_usage(initial: Counter, followup: Counter, n_cases: int):
    rows = sorted(TOOL_LABELS.keys())
    initial_counts = []
    for key in rows:
        c = 0
        for ik, tn in INITIAL_KEY_TO_TOOL.items():
            if tn == key:
                c += initial.get(ik, 0)
        initial_counts.append(c)
    followup_counts = [followup.get(k, 0) for k in rows]

    # Sort by total usage (initial+followup) descending so most-used tools rise
    order = np.argsort([-(a + b) for a, b in zip(initial_counts, followup_counts)])
    rows = [rows[i] for i in order]
    initial_counts = [initial_counts[i] for i in order]
    followup_counts = [followup_counts[i] for i in order]

    fig, ax = plt.subplots(figsize=(10.5, 6.4))
    y = np.arange(len(rows))
    h = 0.4
    b1 = ax.barh(y - h/2, initial_counts, height=h,
                 color=CERN["blue"], edgecolor="white", linewidth=0.8,
                 label="Initial output (cases)")
    b2 = ax.barh(y + h/2, followup_counts, height=h,
                 color=CERN["orange"], edgecolor="white", linewidth=0.8,
                 label="Follow-up uses")
    ax.set_yticks(y)
    ax.set_yticklabels(rows, fontsize=10, family="DejaVu Sans Mono")
    ax.set_xlabel("Count", fontweight="bold")
    ax.set_title(f"Tool output coverage (n = {n_cases} cases, 12 tools)",
                 pad=12)
    ax.legend(loc="lower right", fontsize=10)
    max_v = max(max(initial_counts), max(followup_counts))
    ax.set_xlim(0, max_v * 1.10)
    for i, (a, b) in enumerate(zip(initial_counts, followup_counts)):
        if a:
            ax.text(a + max_v * 0.008, i - h/2, str(a),
                    va="center", fontsize=9, color=CERN["textdark"])
        if b:
            ax.text(b + max_v * 0.008, i + h/2, str(b),
                    va="center", fontsize=9, color=CERN["textdark"])
    _style_axis(ax, x_grid=True, y_grid=False)
    ax.invert_yaxis()
    fig.savefig(OUT_DIR / "tool_usage.pdf")
    plt.close(fig)


def fig_groundtruth_structure(cases: list[dict]):
    n_optimal = [len((c.get("ground_truth") or {}).get("optimal_actions") or []) for c in cases]
    n_diff = [len((c.get("ground_truth") or {}).get("differential") or []) for c in cases]
    n_crit = [len((c.get("ground_truth") or {}).get("critical_actions") or []) for c in cases]
    n_contra = [len((c.get("ground_truth") or {}).get("contraindicated_actions") or []) for c in cases]
    n_red = [len((c.get("ground_truth") or {}).get("red_herrings") or []) for c in cases]
    n_reason = [len((c.get("ground_truth") or {}).get("key_reasoning_points") or []) for c in cases]

    data = [
        ("Optimal actions",         n_optimal,  CERN["blue"]),
        ("Differential entries",    n_diff,     CERN["cyan"]),
        ("Critical actions",        n_crit,     CERN["navy"]),
        ("Contraindicated actions", n_contra,   CERN["orange"]),
        ("Red herrings",            n_red,      CERN["purple"]),
        ("Reasoning points",        n_reason,   CERN["gray"]),
    ]
    labels = [d[0] for d in data]
    values = [d[1] for d in data]
    colors = [d[2] for d in data]

    fig, ax = plt.subplots(figsize=(10.5, 5.2))
    parts = ax.violinplot(values, showmeans=False, showmedians=True, widths=0.85)
    for pc, c in zip(parts["bodies"], colors):
        pc.set_facecolor(c)
        pc.set_edgecolor("white")
        pc.set_alpha(0.85)
        pc.set_linewidth(0.8)
    for key in ("cmedians", "cmins", "cmaxes", "cbars"):
        parts[key].set_color(CERN["textdark"])
        parts[key].set_linewidth(1.0)
    # median markers as filled dots
    for i, v in enumerate(values, start=1):
        ax.scatter([i], [np.median(v)],
                   color="white", edgecolor=CERN["textdark"],
                   zorder=4, s=28, linewidth=1.0)
    ax.set_xticks(range(1, len(labels)+1))
    ax.set_xticklabels(labels, rotation=15, ha="right")
    ax.set_ylabel("Count per case", fontweight="bold")
    ax.set_title(f"Ground-truth structure (distribution across {len(cases)} cases)",
                 pad=12)
    _style_axis(ax)
    fig.savefig(OUT_DIR / "groundtruth_structure.pdf")
    plt.close(fig)


def write_summary(cases: list[dict], initial: Counter, followup: Counter, n_followups: list[int]):
    n = len(cases)
    cond = Counter(c["condition"] for c in cases)
    diff = Counter(c["difficulty"] for c in cases)
    enc = Counter(c["encounter_type"] for c in cases)
    sex = Counter(c["patient"]["demographics"]["sex"] for c in cases)
    ages = [c["patient"]["demographics"]["age"] for c in cases]

    seeded = sum(1 for c in cases if c["case_id"].split("-")[-1].startswith("R"))
    synthetic = n - seeded
    total_followups = sum(n_followups)

    n_initial_total = sum(initial.values())
    avg_initial = n_initial_total / n

    summary = {
        "n_cases": n,
        "n_conditions": len(cond),
        "by_condition": dict(cond.most_common()),
        "by_difficulty": dict(diff),
        "by_encounter": dict(enc),
        "by_sex": dict(sex),
        "age": {"min": min(ages), "max": max(ages),
                "median": int(np.median(ages)), "mean": float(np.mean(ages))},
        "seeded_real_pmc": seeded,
        "synthetic": synthetic,
        "total_followup_outputs": total_followups,
        "median_followups_per_case": int(np.median(n_followups)),
        "avg_initial_tool_outputs_per_case": round(avg_initial, 2),
        "initial_tool_outputs": dict(initial.most_common()),
        "followup_tool_uses": dict(followup.most_common()),
    }
    (OUT_DIR.parent / "v5_stats.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


def main():
    cases = load_cases()
    fig_condition_distribution(cases)
    fig_difficulty_pie(cases)
    fig_demographics(cases)
    initial, followup, n_followups = fig_encounter_and_tools(cases)
    fig_tool_usage(initial, followup, len(cases))
    fig_groundtruth_structure(cases)
    write_summary(cases, initial, followup, n_followups)
    print(f"\nWrote figures to {OUT_DIR}")


if __name__ == "__main__":
    main()
