"""Train→test leakage audit of the NeuroBench split (paper evidence).

Standard library only, so it runs in the base uv environment:

    uv run python scripts/paper/leakage_audit.py [--permutations 10000]

Writes ``outputs/paper/leakage/`` (gitignored): ``summary.json``, ``nn_similarity.csv``,
``top_pairs.json``, ``git_propagation.csv``, ``case_dates.csv``.

Checks
1. Split integrity: disjoint ids, held-out conditions absent from train, no train case whose
   accepted diagnosis or ICD code is a held-out diagnosis, and how often held-out diagnoses are
   mentioned in train (differential, red herrings, rejected labels, free text).
2. Near-duplicate text: nearest-neighbour similarity of each test case to the train cases,
   against the leave-one-out null train→train within the same condition (siblings written by the
   same condition-expert agent). Three field groups (narrative, tool outputs, policy) and three
   measures (TF-IDF cosine on word 1-2 grams, fraction of the case's word 8-grams found in its
   neighbour, longest shared word n-gram).
3. Git propagation: commits that changed test case files together with train case files.
4. Dates: first git appearance and last revision of each case, for the contamination argument.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
import statistics
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "neurobench"
OUT = ROOT / "outputs" / "paper" / "leakage"

# Words case-insensitive, acronyms case-sensitive ("mg" is a dose unit, "he" a pronoun).
HELDOUT_PATTERNS = {
    "myasthenia_gravis": re.compile(r"(?i:myasthen)|\bMG\b|\bG70\.0"),
    "hepatic_encephalopathy": re.compile(r"(?i:hepatic encephalopathy|portosystemic encephalopathy)|\bHE\b|\bK72\.|\bK76\.82"),
}
HELDOUT_ICD = {"myasthenia_gravis": ("G70.0",), "hepatic_encephalopathy": ("K72.", "K76.82")}
TOKEN = re.compile(r"[a-z0-9]+(?:[.\-/][a-z0-9]+)*")


# ---------------------------------------------------------------- loading


def load():
    manifest = json.loads((DATA / "splits" / "split_manifest.json").read_text())
    cases = {}
    for path in sorted((DATA / "cases").glob("*.json")):
        case = json.loads(path.read_text())
        cases[case["case_id"]] = case
    split = {}
    for cid in manifest["train_case_ids"]:
        split[cid] = "train"
    for cid in manifest["test_heldout_condition_case_ids"]:
        split[cid] = "test_heldout"
    for cid in manifest["test_stratified_case_ids"]:
        split[cid] = "test_stratified"
    return manifest, cases, split


def flatten(value) -> list[str]:
    if isinstance(value, dict):
        return [s for v in value.values() for s in flatten(v)]
    if isinstance(value, list):
        return [s for v in value for s in flatten(v)]
    if isinstance(value, str):
        return [value]
    return []


def field_texts(case) -> dict[str, str]:
    patient = case["patient"]
    narrative = [patient.get("chief_complaint", ""), patient.get("history_present_illness", "")]
    narrative += flatten(patient.get("clinical_history", {})) + flatten(patient.get("neurological_exam", {}))
    gt = case["ground_truth"]
    return {
        "narrative": " ".join(narrative),
        "tool_outputs": " ".join(flatten(case.get("initial_tool_outputs", {})) + flatten(case.get("followup_outputs", []))),
        "policy": " ".join(flatten(gt.get("action_criteria", [])) + flatten(gt.get("avoided_actions", []))),
    }


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


# ---------------------------------------------------------------- similarity


def tfidf_vectors(docs: dict[str, list[str]]) -> dict[str, dict[str, float]]:
    grams = {cid: toks + [a + " " + b for a, b in zip(toks, toks[1:])] for cid, toks in docs.items()}
    df = Counter(g for gs in grams.values() for g in set(gs))
    n = len(grams)
    vectors = {}
    for cid, gs in grams.items():
        tf = Counter(gs)
        vec = {g: (1 + math.log(c)) * (math.log((1 + n) / (1 + df[g])) + 1) for g, c in tf.items()}
        norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
        vectors[cid] = {g: v / norm for g, v in vec.items()}
    return vectors


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(v * b.get(g, 0.0) for g, v in a.items())


def shingles(toks: list[str], k: int = 8) -> set[tuple[str, ...]]:
    return {tuple(toks[i : i + k]) for i in range(len(toks) - k + 1)}


def containment(a: set, b: set) -> float:
    return len(a & b) / len(a) if a else 0.0


def longest_shared_ngram(a: list[str], b: list[str]) -> tuple[int, str]:
    """Longest common contiguous word sequence: binary search on the length over k-gram sets."""

    def shared(k: int):
        grams = {tuple(b[j : j + k]) for j in range(len(b) - k + 1)}
        for i in range(len(a) - k + 1):
            if tuple(a[i : i + k]) in grams:
                return a[i : i + k]
        return None

    lo, hi, found = 0, min(len(a), len(b)), []
    while lo < hi:
        mid = (lo + hi + 1) // 2
        hit = shared(mid)
        if hit:
            lo, found = mid, hit
        else:
            hi = mid - 1
    return lo, " ".join(found)


# ---------------------------------------------------------------- statistics


def describe(xs: list[float]) -> dict:
    xs = sorted(xs)
    if not xs:
        return {}
    p95 = xs[min(len(xs) - 1, math.ceil(0.95 * len(xs)) - 1)]
    return {"n": len(xs), "median": round(statistics.median(xs), 4), "p95": round(p95, 4), "max": round(xs[-1], 4), "mean": round(statistics.fmean(xs), 4)}


def mann_whitney_greater(x: list[float], y: list[float]) -> dict:
    """One-sided H1: x tends to be larger than y. Normal approximation with tie correction."""
    pooled = sorted([(v, 0) for v in x] + [(v, 1) for v in y])
    ranks = [0.0] * len(pooled)
    i = 0
    ties = 0.0
    while i < len(pooled):
        j = i
        while j + 1 < len(pooled) and pooled[j + 1][0] == pooled[i][0]:
            j += 1
        r = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[k] = r
        t = j - i + 1
        ties += t**3 - t
        i = j + 1
    n1, n2 = len(x), len(y)
    r1 = sum(r for r, (_, g) in zip(ranks, pooled) if g == 0)
    u = r1 - n1 * (n1 + 1) / 2
    n = n1 + n2
    sigma = math.sqrt(n1 * n2 / 12 * ((n + 1) - ties / (n * (n - 1))))
    z = (u - n1 * n2 / 2) / sigma if sigma else 0.0
    p = 0.5 * math.erfc(z / math.sqrt(2))
    return {"U": round(u, 1), "z": round(z, 3), "p_one_sided": round(p, 4), "auc_test_gt_null": round(u / (n1 * n2), 3)}


def permutation_mean_greater(x: list[float], y: list[float], n: int, rng: random.Random) -> float:
    observed = statistics.fmean(x) - statistics.fmean(y)
    pooled = x + y
    hits = 0
    for _ in range(n):
        rng.shuffle(pooled)
        if statistics.fmean(pooled[: len(x)]) - statistics.fmean(pooled[len(x) :]) >= observed:
            hits += 1
    return round((hits + 1) / (n + 1), 4)


# ---------------------------------------------------------------- checks


def split_integrity(manifest, cases, split) -> dict:
    train = set(manifest["train_case_ids"])
    test = set(manifest["test_heldout_condition_case_ids"]) | set(manifest["test_stratified_case_ids"])
    files_test = set((DATA / "splits" / "test_cases.txt").read_text().split())
    files_train = set((DATA / "splits" / "train_cases.txt").read_text().split())
    result = {
        "n_cases": len(cases),
        "n_train": len(train),
        "n_test": len(test),
        "train_and_test_overlap": sorted(train & test),
        "unassigned_cases": sorted(set(cases) - train - test),
        "txt_files_match_manifest": files_test == test and files_train == train,
        "heldout_conditions": manifest["heldout_conditions"],
    }
    by_condition = defaultdict(Counter)
    for cid, case in cases.items():
        by_condition[case["condition"]][split.get(cid, "?")] += 1
    result["split_by_condition"] = {k: dict(v) for k, v in sorted(by_condition.items())}
    result["heldout_conditions_in_train"] = {c: by_condition[c].get("train", 0) for c in manifest["heldout_conditions"]}

    mentions = {}
    for cond, pattern in HELDOUT_PATTERNS.items():
        primary_hits, counts = [], Counter()
        for cid in sorted(train):
            gt = cases[cid]["ground_truth"]
            accepted = gt["diagnosis"].get("accepted", [])
            codes = gt["diagnosis"].get("icd_codes", [])
            if any(pattern.search(a) for a in accepted) or any(c.startswith(HELDOUT_ICD[cond]) for c in codes):
                primary_hits.append(cid)
            if any(pattern.search(r) for r in gt["diagnosis"].get("rejected", [])):
                counts["rejected_label"] += 1
            if any(pattern.search(d.get("diagnosis", "")) or (d.get("icd_code") or "").startswith(HELDOUT_ICD[cond]) for d in gt.get("differential", [])):
                counts["differential"] += 1
            if any(pattern.search(s) for s in flatten(gt.get("red_herrings", []))):
                counts["red_herrings"] += 1
            if pattern.search(" ".join(flatten(cases[cid]["patient"]))):
                counts["patient_text_shown_to_agent"] += 1
            if pattern.search(json.dumps(cases[cid])):
                counts["anywhere_in_case_json"] += 1
        mentions[cond] = {"train_cases_with_heldout_primary_diagnosis": primary_hits, "train_cases_mentioning": dict(counts), "of_train": len(train)}
    result["heldout_diagnosis_in_train"] = mentions
    return result


def similarity(cases, split, permutations: int, rng: random.Random):
    texts = {cid: field_texts(c) for cid, c in cases.items()}
    train_ids = [cid for cid in cases if split[cid] == "train"]
    by_cond = defaultdict(list)
    for cid in train_ids:
        by_cond[cases[cid]["condition"]].append(cid)

    rows, summary, top = [], {}, {}
    for field in ("narrative", "tool_outputs", "policy"):
        toks = {cid: tokens(texts[cid][field]) for cid in cases}
        vecs = tfidf_vectors(toks)
        sh = {cid: shingles(t) for cid, t in toks.items()}

        def nn(cid, pool):
            best = None
            for other in pool:
                if other == cid:
                    continue
                cos = cosine(vecs[cid], vecs[other])
                if best is None or cos > best[1]:
                    best = (other, cos)
            other, cos = best
            return other, cos, containment(sh[cid], sh[other])

        groups = defaultdict(list)
        for cid in cases:
            kind = split[cid]
            if kind == "train":
                pool = by_cond[cases[cid]["condition"]]
                group = "null_train_loo_same_condition"
            elif kind == "test_stratified":
                pool = by_cond[cases[cid]["condition"]]
                group = "test_stratified_vs_train_same_condition"
            else:
                pool = train_ids
                group = "test_heldout_vs_all_train"
            other, cos, cont = nn(cid, pool)
            # Any-condition neighbour for stratified test cases too (a cross-condition near copy).
            if kind == "test_stratified":
                o2, c2, k2 = nn(cid, train_ids)
                groups["test_stratified_vs_all_train"].append((cid, o2, c2, k2))
            groups[group].append((cid, other, cos, cont))

        field_summary = {}
        for group, items in groups.items():
            field_summary[group] = {"tfidf_cosine": describe([i[2] for i in items]), "shingle8_containment": describe([i[3] for i in items])}
            for cid, other, cos, cont in items:
                rows.append({"field": field, "group": group, "case_id": cid, "split": split[cid], "condition": cases[cid]["condition"], "nn_train_case": other, "tfidf_cosine": round(cos, 4), "shingle8_containment": round(cont, 4)})

        test = groups["test_stratified_vs_train_same_condition"]
        null = groups["null_train_loo_same_condition"]
        for measure, idx in (("tfidf_cosine", 2), ("shingle8_containment", 3)):
            x, y = [i[idx] for i in test], [i[idx] for i in null]
            field_summary[f"test_vs_null_{measure}"] = {**mann_whitney_greater(x, y), "permutation_p_mean_greater": permutation_mean_greater(x, y, permutations, rng)}

        # Longest shared n-gram on the nearest-neighbour pairs (test) and on the null pairs.
        lsn = {}
        for group in ("test_stratified_vs_train_same_condition", "null_train_loo_same_condition", "test_heldout_vs_all_train"):
            lengths = []
            for cid, other, _, _ in groups[group]:
                n, text = longest_shared_ngram(toks[cid], toks[other])
                lengths.append(n)
                if group == "test_stratified_vs_train_same_condition":
                    for r in rows:
                        if r["field"] == field and r["group"] == group and r["case_id"] == cid:
                            r["longest_shared_ngram"] = n
                            r["longest_shared_text"] = text[:300]
            lsn[group] = describe(lengths)
        x = [r["longest_shared_ngram"] for r in rows if r["field"] == field and r["group"] == "test_stratified_vs_train_same_condition"]
        field_summary["longest_shared_ngram_words"] = lsn
        summary[field] = field_summary

        ranked = sorted((r for r in rows if r["field"] == field and r["group"] == "test_stratified_vs_train_same_condition"), key=lambda r: -r["tfidf_cosine"])[:5]
        top[field] = [
            {
                "test_case": r["case_id"],
                "train_case": r["nn_train_case"],
                "tfidf_cosine": r["tfidf_cosine"],
                "shingle8_containment": r["shingle8_containment"],
                "longest_shared_ngram": r["longest_shared_ngram"],
                "longest_shared_text": r["longest_shared_text"],
                "test_excerpt": texts[r["case_id"]][field][:400],
                "train_excerpt": texts[r["nn_train_case"]][field][:400],
            }
            for r in ranked
        ]
    return rows, summary, top


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout


def propagation(split) -> tuple[list[dict], dict]:
    log = git("log", "--format=@@%h|%ad|%s", "--date=short", "--name-only", "--", "data/neurobench/cases")
    commits, cur = [], None
    for line in log.splitlines():
        if line.startswith("@@"):
            h, d, s = line[2:].split("|", 2)
            cur = {"commit": h, "date": d, "subject": s, "files": []}
            commits.append(cur)
        elif line.strip() and cur is not None:
            cur["files"].append(Path(line.strip()).stem)
    rows = []
    for c in commits:
        kinds = Counter(split.get(cid, "not_in_current_dataset") for cid in c["files"])
        test_files = [cid for cid in c["files"] if split.get(cid, "").startswith("test")]
        if not test_files:
            continue
        # Held-out-condition terms added to train files by a commit that also edited held-out cases.
        heldout_terms_added_to_train = []
        if kinds.get("test_heldout", 0) and kinds.get("train", 0):
            train_paths = [f"data/neurobench/cases/{cid}.json" for cid in c["files"] if split.get(cid) == "train"]
            diff = git("show", "--format=", "--unified=0", c["commit"], "--", *train_paths)
            current = None
            for line in diff.splitlines():
                if line.startswith("+++ "):
                    current = Path(line[4:]).stem
                elif line.startswith("+") and any(p.search(line) for p in HELDOUT_PATTERNS.values()):
                    heldout_terms_added_to_train.append(f"{current}: {line[1:].strip()[:160]}")
        rows.append({
            "commit": c["commit"],
            "date": c["date"],
            "subject": c["subject"],
            "n_train": kinds.get("train", 0),
            "n_test_heldout": kinds.get("test_heldout", 0),
            "n_test_stratified": kinds.get("test_stratified", 0),
            "test_files": " ".join(sorted(test_files)),
            "co_modifies_train": kinds.get("train", 0) > 0,
            "n_heldout_term_lines_added_to_train": len(heldout_terms_added_to_train),
            "heldout_term_lines_added_to_train": " || ".join(heldout_terms_added_to_train[:20]),
        })
    summary = {
        "commits_touching_case_files": len(commits),
        "commits_touching_test_files": len(rows),
        "commits_touching_test_and_train": sum(r["co_modifies_train"] for r in rows),
        "commits_touching_only_test": sum(not r["co_modifies_train"] for r in rows),
        "commits_touching_heldout_and_train": sum(r["co_modifies_train"] and r["n_test_heldout"] > 0 for r in rows),
        "co_modifying_commits_with_few_train_files_le5": [r["commit"] for r in rows if r["co_modifies_train"] and r["n_train"] <= 5],
        "heldout_term_lines_added_to_train": {r["commit"]: r["n_heldout_term_lines_added_to_train"] for r in rows if r["n_heldout_term_lines_added_to_train"]},
    }
    return rows, summary


def case_dates(cases) -> tuple[list[dict], dict]:
    log = git("log", "--format=@@%ad", "--date=short", "--diff-filter=A", "--name-only", "--", "data")
    first = {}
    date = None
    for line in log.splitlines():
        if line.startswith("@@"):
            date = line[2:]
        elif line.endswith(".json"):
            stem = Path(line).stem
            if stem in cases and (stem not in first or date < first[stem]):
                first[stem] = date
    rows = [{"case_id": cid, "first_in_git": first.get(cid, ""), "last_revised": cases[cid]["metadata"].get("last_revised", "")} for cid in sorted(cases)]
    firsts = sorted(r["first_in_git"] for r in rows if r["first_in_git"])
    revised = sorted(r["last_revised"] for r in rows if r["last_revised"])
    return rows, {
        "first_in_git_min": firsts[0] if firsts else None,
        "first_in_git_max": firsts[-1] if firsts else None,
        "cases_without_git_date": sum(not r["first_in_git"] for r in rows),
        "last_revised_min": revised[0] if revised else None,
        "last_revised_max": revised[-1] if revised else None,
        "last_revised_counts_by_month": dict(Counter(d[:7] for d in revised)),
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("")
        return
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--permutations", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    rng = random.Random(args.seed)

    manifest, cases, split = load()
    OUT.mkdir(parents=True, exist_ok=True)
    summary = {"split_integrity": split_integrity(manifest, cases, split)}
    rows, sim, top = similarity(cases, split, args.permutations, rng)
    summary["similarity"] = sim
    prop_rows, prop = propagation(split)
    summary["git_propagation"] = prop
    date_rows, dates = case_dates(cases)
    summary["case_dates"] = dates

    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))
    (OUT / "top_pairs.json").write_text(json.dumps(top, indent=2))
    write_csv(OUT / "nn_similarity.csv", rows)
    write_csv(OUT / "git_propagation.csv", prop_rows)
    write_csv(OUT / "case_dates.csv", date_rows)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
