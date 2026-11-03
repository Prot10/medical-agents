"""Collect the numbers of the case diversity figure and tables into data/diversity.json.

Run from the repository root after `scripts/paper/case_diversity.py` (its outputs are read from
outputs/paper/diversity/; the split enumeration and the family tests are recomputed here):
    uv run --no-project --python 3.12 --with numpy --with scipy --with scikit-learn \
        python paper/figures/data/prepare_diversity.py
"""

from __future__ import annotations

import csv
import itertools
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/paper"))
import case_diversity as cd  # noqa: E402
from leakage_audit import field_texts, load  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from prepare import GROUPS, NAMES  # noqa: E402

DIV = ROOT / "outputs/paper/diversity"
OUT = Path(__file__).resolve().parent / "diversity.json"
SEED = 20261103
PERMUTATIONS = 9999

TEXT_VIEWS = ["narrative_tfidf", "narrative_embedding", "narrative_style", "reports_tfidf", "reports_embedding"]
WORK_VIEWS = ["required_tools", "required_tokens", "workup_tokens", "avoided_tokens", "order_pairs_tool", "order_pairs_token", "order_sequence"]
VIEW_NAMES = {
    "narrative_tfidf": "Narrative, words", "narrative_embedding": "Narrative, meaning", "narrative_style": "Narrative, style",
    "reports_tfidf": "Tool reports, words", "reports_embedding": "Tool reports, meaning",
    "required_tools": "Required tools", "required_tokens": "Required studies", "workup_tokens": "Required + recommended",
    "avoided_tokens": "Actions to avoid", "order_pairs_tool": "Order, tool pairs", "order_pairs_token": "Order, study pairs",
    "order_sequence": "Order, full sequence",
}


def condition_matrix(view: str, members: list[str]) -> np.ndarray:
    with open(DIV / f"condition_distance_{view}.csv") as f:
        rows = list(csv.reader(f))
    header = rows[0][1:]
    m = {r[0]: dict(zip(header, map(float, r[1:]))) for r in rows[1:]}
    return np.array([[m[a][b] for b in members] for a in members])


def main() -> None:
    summary = json.loads((DIV / "summary.json").read_text())
    rng = np.random.default_rng(SEED)
    _, by_id, _ = load()
    cases = [by_id[i] for i in sorted(by_id)]
    members = sorted(cd.FAMILIES)
    labels = np.array([members.index(c["condition"]) for c in cases])
    order = [c for g in GROUPS.values() for c in g]
    group_of = {c: g for g, cs in GROUPS.items() for c in cs}

    views = []
    for key in TEXT_VIEWS + WORK_VIEWS:
        v = summary["views"][key]
        views.append({
            "key": key, "name": VIEW_NAMES[key], "kind": "text" if key in TEXT_VIEWS else "work", "n": v["n"],
            "r2": v["permanova_R2"], "r2_given_encounter": v["R2_condition_given_encounter"], "r2_difficulty": v["R2_difficulty"],
            "auc": v["auc_between_gt_within"], "knn1": v["knn1"], "silhouette": v["silhouette"],
            "shuffled_r2": v["shuffled_R2"], "shuffled_knn1": v["shuffled_knn1"], "sibling_r2_p95": v["sibling_R2_p95"],
            "pair_r2_min": v["pair_R2_min"], "pairs_holm": v["pairs_holm_significant"], "permdisp_p": v["permdisp_p"],
            "p": v["permanova_p"], "closest": v["closest_pairs"][0],
        })

    # Two a-priori taxonomies of the conditions: the script's FAMILIES and the paper's GROUPS (Fig. 2b).
    families = {}
    for taxonomy, mapping in (("families", cd.FAMILIES), ("paper_groups", group_of)):
        names = sorted(set(mapping.values()))
        f = np.array([names.index(mapping[m]) for m in members])
        families[taxonomy] = {key: cd.family_test(condition_matrix(key, members), f, PERMUTATIONS, rng) for key in TEXT_VIEWS + WORK_VIEWS}

    # Pairwise PERMANOVA R2 (0-1 in every view, so text and work-up share one colour scale).
    heat = {}
    for key in TEXT_VIEWS + WORK_VIEWS:
        m = np.full((len(order), len(order)), np.nan)
        for r in csv.DictReader(open(DIV / f"pairwise_{key}.csv")):
            i, j = order.index(r["a"]), order.index(r["b"])
            m[i, j] = m[j, i] = float(r["R2"])
        heat[key] = [[None if np.isnan(v) else round(float(v), 4) for v in row] for row in m]

    with open(DIV / "copy_baseline.csv") as f:
        copy = [r | {"mean": float(r["mean"]), "ci_low": float(r["ci_low"]), "ci_high": float(r["ci_high"])} for r in csv.DictReader(f)]

    # Every choice of four test conditions: mean over their cases of the nearest other-condition
    # narrative similarity and of the token F1 of copying that case's required work-up.
    narrative = [field_texts(c)["narrative"] for c in cases]
    x = cd.tfidf_matrix(narrative)
    sim = (x @ x.T).toarray()
    tokens = [cd.criterion_tokens(c, ("required",)) for c in cases]
    valid = np.array([c["case_id"] not in cd.SPLIT_EXCLUDED for c in cases])
    k = len(members)
    best_sim, best_f1 = np.full((len(cases), k), -np.inf), np.zeros((len(cases), k))
    for g in range(k):
        idx = np.nonzero((labels == g) & valid)[0]
        s = sim[:, idx].copy()
        s[labels == g, :] = -np.inf
        j = s.argmax(1)
        best_sim[:, g] = s[np.arange(len(cases)), j]
        best_f1[:, g] = [cd.f1(tokens[i], tokens[idx[jj]]) for i, jj in enumerate(j)]
    combos = []
    for combo in itertools.combinations(range(k), 4):
        rest = np.array([g for g in range(k) if g not in combo])
        q = np.isin(labels, combo) & valid
        pick = rest[best_sim[q][:, rest].argmax(1)]
        rows = np.nonzero(q)[0]
        combos.append([round(float(best_sim[rows, pick].mean()), 4), round(float(best_f1[rows, pick].mean()), 4), [members[g] for g in combo]])
    proposed = sorted(cd.TEST)
    mine = next(c for c in combos if sorted(c[2]) == proposed)
    assert abs(mine[1] - summary["split_enumeration"]["proposed_copy_f1"]) < 1e-3, "enumeration differs from case_diversity.py"

    per_condition = []
    pc = {r["condition"]: r for r in csv.DictReader(open(DIV / "per_condition.csv"))}
    by_cond = summary["copy"]["tfidf/by_condition"]
    work = summary["views"]["required_tokens"]["by_condition"]
    style = summary["views"]["narrative_style"]["by_condition"]
    emb = summary["views"]["narrative_embedding"]["by_condition"]
    # Closest work-up: for every case, the condition of the most similar required work-up outside its
    # own condition (ties broken by narrative similarity). The energy distance between conditions is
    # not used here because it shrinks for the most dispersed condition (HE) and names it for nearly all.
    d = cd.set_distance(tokens)
    np.fill_diagonal(d, np.inf)
    neighbour = []
    for i in range(len(cases)):
        row = np.where(labels == labels[i], np.inf, d[i])
        best = np.nonzero(row == row.min())[0]
        # -1: no required study in common with any case of another condition
        neighbour.append(labels[best[np.argmax(sim[i, best])]] if row.min() < 0.999 else -1)
    neighbour = np.array(neighbour)
    for c in order:
        g = members.index(c)
        mine = neighbour[labels == g]
        counts = np.bincount(mine[mine >= 0], minlength=k)
        per_condition.append({
            "id": c, "name": NAMES[c], "group": group_of[c], "family": cd.FAMILIES[c],
            "split": "test" if c in cd.TEST else "validation" if c in cd.VALIDATION else "train",
            "distinct_required_sets": int(pc[c]["unique_required_sets"]), "mean_required": float(pc[c]["mean_required"]),
            "silhouette_workup": work[c]["silhouette"], "knn1_workup": work[c]["knn1"],
            "knn1_style": style[c]["knn1"], "knn1_meaning": emb[c]["knn1"],
            "copy_siblings": by_cond[c]["siblings"], "copy_other": by_cond[c]["loco"],
            "nearest_workup": members[int(counts.argmax())] if counts.max() else None, "nearest_workup_cases": int(counts.max()),
            "no_shared_study": int((mine < 0).sum()),
        })

    out = {
        "n_cases": summary["n_cases"], "permutations": summary["permutations"], "views": views, "families": families,
        "heat_order": order, "groups": GROUPS, "names": NAMES, "heat": heat, "copy": copy, "copy_tests": {k: summary["copy"][k] for k in ("tfidf/tests", "embedding/tests")},
        "split": {"proposed": proposed, "validation": list(cd.VALIDATION), "combos": combos, "summary": summary["split_enumeration"], "detail": summary["proposed_split"]},
        "per_condition": per_condition, "specificity": summary["specificity"], "order_conflicts": summary["order_conflicts"],
    }
    OUT.write_text(json.dumps(out, indent=1))
    print("wrote", OUT.relative_to(ROOT), f"{OUT.stat().st_size / 1024:.0f} kB")
    for taxonomy, t in families.items():
        print(taxonomy, {k: (round(v["gap"], 3), v["p"], round(v["ari"], 2), v["ari_p"]) for k, v in t.items()})


if __name__ == "__main__":
    main()
