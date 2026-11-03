"""How different NeuroBench cases are across conditions and clinical families (paper evidence).

    uv run --no-project --with numpy --with scipy --with scikit-learn \
        python scripts/paper/case_diversity.py [--permutations 9999] [--no-embeddings]

Writes ``outputs/paper/diversity/`` (gitignored): ``summary.json``, ``views.csv``, ``pairwise_<view>.csv``,
``condition_distance_<view>.csv``, ``per_condition.csv``, ``copy_baseline.csv``, ``tool_by_condition.csv``.

Every view is a case × case distance, Euclidean-embeddable so PERMANOVA's partition is exact:
chord distance for vectors, sqrt(1 - Jaccard) for sets.

Text (what the agent reads): narrative and tool reports, TF-IDF and EmbeddingGemma vectors, plus a
style-only view of function words and punctuation that detects each condition's authoring agent.
Work-up (the answer): required tools, required tool+argument tokens, required+recommended tokens,
avoided tokens. Order: directed precedence pairs from the sequence constraints, and the edit
distance of one canonical sequence (cases without a constraint leave the precedence views).

Tests per view: PERMANOVA (also within difficulty strata), PERMDISP, leave-one-out k-NN purity,
silhouette, all 190 pairwise PERMANOVAs with Holm and BH against a sibling-halves null. Families are
compared by moving whole conditions, the exchangeable unit. The functional test copies the work-up
of the nearest case under each reference set, which measures what similarity is worth to an agent.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import os
import re
import sys
import time
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import squareform
from scipy.stats import rankdata, spearmanr, wilcoxon
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS, TfidfVectorizer
from sklearn.metrics import adjusted_rand_score, silhouette_samples

sys.path.insert(0, str(Path(__file__).resolve().parent))
from leakage_audit import field_texts, flatten, load  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs" / "paper" / "diversity"
SEED = 20261103

# Written before looking at any distance, as clinical teaching groups. Physicians should confirm it.
FAMILIES = {
    "als": "neuromuscular",
    "guillain_barre": "neuromuscular",
    "myasthenia_gravis": "neuromuscular",
    "alzheimers_early": "cognitive",
    "ftd": "cognitive",
    "nph": "cognitive",
    "vascular_dementia": "cognitive",
    "parkinsons": "movement",
    "ischemic_stroke": "acute_vascular",
    "subarachnoid_hemorrhage": "acute_vascular",
    "multiple_sclerosis": "cns_inflammatory",
    "autoimmune_encephalitis_nmdar": "cns_inflammatory",
    "focal_epilepsy_temporal": "paroxysmal",
    "status_epilepticus": "paroxysmal",
    "migraine_with_aura": "paroxysmal",
    "syncope_cardiac": "paroxysmal",
    "bacterial_meningitis": "infectious",
    "brain_tumor_glioma": "neoplastic",
    "hepatic_encephalopathy": "toxic_metabolic",
    "functional_neurological_disorder": "functional",
}
TEST = ("myasthenia_gravis", "hepatic_encephalopathy", "bacterial_meningitis", "brain_tumor_glioma")
# FND left validation on 3 Nov 2026: 2 distinct required sets in 30 cases cannot rank configurations.
# Its replacement is the training condition with the lowest copy F1 among those with at least 15
# distinct required sets (dataset criteria only, the same kind used for the test set).
VALIDATION = ("multiple_sclerosis", "syncope_cardiac")
# Mimics whose answer crosses the split boundary (answer FND no longer does: FND is in training).
SPLIT_EXCLUDED = {"SE-P07", "HEP-ENC-P06"}
MENTION = {
    "als": r"amyotrophic lateral|motor neuron disease|\bALS\b",
    "guillain_barre": r"guillain|\bGBS\b|\bAIDP\b",
    "myasthenia_gravis": r"myasthen|lambert",
    "alzheimers_early": r"alzheimer",
    "ftd": r"frontotemporal|\bFTD\b|primary progressive aphasia",
    "nph": r"normal[- ]pressure hydroceph|\bNPH\b",
    "vascular_dementia": r"vascular (dementia|cognitive)",
    "parkinsons": r"parkinson",
    "ischemic_stroke": r"ischa?emic stroke|cerebral infarct|\bTIA\b|transient ischa?emic",
    "subarachnoid_hemorrhage": r"subarachnoid|\bSAH\b",
    "multiple_sclerosis": r"multiple sclerosis|\bMS\b",
    "autoimmune_encephalitis_nmdar": r"autoimmune encephalitis|NMDA",
    "focal_epilepsy_temporal": r"focal (epilepsy|seizure)|temporal lobe epilepsy",
    "status_epilepticus": r"status epilepticus|\bNCSE\b",
    "migraine_with_aura": r"migraine",
    "syncope_cardiac": r"syncope|arrhythmi",
    "bacterial_meningitis": r"bacterial meningitis|meningococc|pneumococcal mening",
    "brain_tumor_glioma": r"glioma|glioblastoma|brain tumou?r",
    "hepatic_encephalopathy": r"hepatic encephalopathy|portosystemic encephalopathy",
    "functional_neurological_disorder": r"functional neurological|conversion disorder|psychogenic|\bPNES\b",
}


# ---------------------------------------------------------------- views


def token(alt: dict) -> str:
    args = alt.get("required_arguments") or {}
    return alt["tool_name"] + "".join(f"|{k}={json.dumps(args[k], sort_keys=True)}" for k in sorted(args))


def criterion_tokens(case: dict, importance: tuple[str, ...]) -> set[str]:
    return {token(a) for c in case["ground_truth"]["action_criteria"] if c["importance"] in importance for a in c["alternatives"]}


def required_tools(case: dict) -> set[str]:
    return {t.split("|")[0] for t in criterion_tokens(case, ("required",))}


def avoided_tokens(case: dict) -> set[str]:
    return {token(a) for c in case["ground_truth"]["avoided_actions"] for a in c["alternatives"]}


def precedence(case: dict, level: str) -> set[tuple[str, str]]:
    """Directed pairs of the transitive closure of the sequence constraints, without self-pairs."""
    gt = case["ground_truth"]
    label = {}
    for c in gt["action_criteria"]:
        t = token(c["alternatives"][0])
        label[c["criterion_id"]] = t.split("|")[0] if level == "tool" else t
    nodes = list(label)
    index = {n: i for i, n in enumerate(nodes)}
    reach = np.zeros((len(nodes), len(nodes)), bool)
    for s in gt["sequence_constraints"]:
        a, b = s["before_criterion_id"], s["after_criterion_id"]
        if a in index and b in index:
            reach[index[a], index[b]] = True
    for k in range(len(nodes)):
        reach |= np.outer(reach[:, k], reach[k, :])
    return {(label[nodes[i]], label[nodes[j]]) for i, j in zip(*np.nonzero(reach)) if label[nodes[i]] != label[nodes[j]]}


def canonical_sequence(case: dict) -> list[str]:
    """Required tools in a topological order of the constraints, ties in authoring order."""
    gt = case["ground_truth"]
    crit = [c for c in gt["action_criteria"] if c["importance"] == "required"]
    ids = [c["criterion_id"] for c in crit]
    before = defaultdict(set)
    for s in gt["sequence_constraints"]:
        if s["before_criterion_id"] in ids and s["after_criterion_id"] in ids:
            before[s["after_criterion_id"]].add(s["before_criterion_id"])
    order, left = [], list(ids)
    while left:
        ready = next((i for i in left if not before[i] & set(left)), left[0])  # a cycle falls back to authoring order
        order.append(ready)
        left.remove(ready)
    tool = {c["criterion_id"]: c["alternatives"][0]["tool_name"] for c in crit}
    return [tool[i] for i in order]


def edit_distance(a: list[str], b: list[str]) -> float:
    row = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        prev, row[0] = row[0], i
        for j, y in enumerate(b, 1):
            prev, row[j] = row[j], min(row[j] + 1, row[j - 1] + 1, prev + (x != y))
    return row[-1] / max(len(a), len(b), 1)


def chord(x: np.ndarray) -> np.ndarray:
    """Chord distance of L2-normalised rows."""
    sim = np.clip(x @ x.T, -1, 1)
    d = np.sqrt(np.clip(2 - 2 * sim, 0, None))
    np.fill_diagonal(d, 0)
    return d


def jaccard_matrix(sets: list[set]) -> np.ndarray:
    vocab = {t: i for i, t in enumerate(sorted({t for s in sets for t in s}, key=str))}
    m = np.zeros((len(sets), len(vocab)), np.float32)
    for i, s in enumerate(sets):
        m[i, [vocab[t] for t in s]] = 1
    inter = m @ m.T
    size = m.sum(1)
    union = size[:, None] + size[None, :] - inter
    return np.where(union > 0, inter / np.maximum(union, 1), 1.0).astype(float)


def set_distance(sets: list[set]) -> np.ndarray:
    d = np.sqrt(np.clip(1 - jaccard_matrix(sets), 0, 1))
    np.fill_diagonal(d, 0)
    return d


def tfidf_matrix(docs: list[str]):
    return TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True, min_df=2, token_pattern=r"[a-z0-9]+(?:[.\-/][a-z0-9]+)*").fit_transform(docs)


def style_matrix(docs: list[str]) -> np.ndarray:
    """Function words, punctuation and sentence length, with every clinical word out of the vocabulary."""
    words = sorted(ENGLISH_STOP_WORDS)
    index = {w: i for i, w in enumerate(words)}
    rows = []
    for doc in docs:
        toks = re.findall(r"[a-z']+", doc.lower())
        counts = np.zeros(len(words))
        for t in toks:
            if t in index:
                counts[index[t]] += 1
        sentences = max(len(re.findall(r"[.;:!?]\s", doc)), 1)
        punct = [doc.count(c) / max(len(doc), 1) for c in ",;:()-/."]
        rows.append([*(counts / max(len(toks), 1)), *punct, len(toks) / sentences, np.mean([len(t) for t in toks] or [0])])
    x = np.array(rows)
    x = x[:, x.std(0) > 0]
    x = (x - x.mean(0)) / x.std(0)
    return x / np.linalg.norm(x, axis=1, keepdims=True)


def embed(texts: list[str], name: str, model: str = "embeddinggemma-300m", chunk_words: int = 400) -> np.ndarray:
    """Mean of L2-normalised chunk embeddings. CERN-hosted model, synthetic cases only, cached on disk."""
    cache = OUT / f"embeddings_{name}.npz"
    digest = hashlib.sha256("\0".join([model, str(chunk_words), *texts]).encode()).hexdigest()
    if cache.exists():
        saved = np.load(cache)
        if str(saved["digest"]) == digest:
            return saved["x"]
    key = Path("~/.config/cern-ml/aigw.key").expanduser().read_text().strip()
    chunks, owner = [], []
    for i, text in enumerate(texts):
        words = text.split()
        for start in range(0, max(len(words), 1), chunk_words):
            chunks.append("title: none | text: " + " ".join(words[start : start + chunk_words]))
            owner.append(i)

    def post(batch: list[str]) -> list[list[float]]:
        body = json.dumps({"model": model, "input": batch}).encode()
        request = urllib.request.Request(
            "https://aigw.cern.ch/v1/embeddings", body, {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        )
        for attempt in range(5):
            try:
                with urllib.request.urlopen(request, timeout=120) as response:
                    return [row["embedding"] for row in json.load(response)["data"]]
            except OSError:
                if attempt == 4:
                    raise
                time.sleep(2**attempt)
        raise AssertionError

    batches = [chunks[i : i + 32] for i in range(0, len(chunks), 32)]
    with ThreadPoolExecutor(8) as pool:
        vectors = np.array([v for part in pool.map(post, batches) for v in part], float)
    vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)
    x = np.zeros((len(texts), vectors.shape[1]))
    np.add.at(x, owner, vectors)
    x /= np.linalg.norm(x, axis=1, keepdims=True)
    np.savez(cache, x=x, digest=digest)
    return x


# ---------------------------------------------------------------- tests


def permanova(d: np.ndarray, labels: np.ndarray, permutations: int, rng, strata: np.ndarray | None = None) -> dict:
    n = len(labels)
    iu, ju = np.triu_indices(n, 1)
    d2 = d[iu, ju] ** 2
    total = d2.sum() / n
    groups, counts = np.unique(labels, return_counts=True)
    a = len(groups)
    inverse = np.zeros(int(groups.max()) + 1)
    inverse[groups] = 1 / counts

    def within(y: np.ndarray) -> float:
        same = y[iu] == y[ju]
        return float((d2[same] * inverse[y[iu][same]]).sum())

    def stat(ssw: float) -> float:
        return ((total - ssw) / (a - 1)) / (ssw / (n - a))

    observed = within(labels)
    f = stat(observed)
    hits = 0
    y = labels.copy()
    for _ in range(permutations):
        if strata is None:
            y = rng.permutation(labels)
        else:
            for s in np.unique(strata):
                idx = np.nonzero(strata == s)[0]
                y[idx] = rng.permutation(labels[idx])
        hits += stat(within(y)) >= f
    return {"F": f, "R2": 1 - observed / total, "p": (hits + 1) / (permutations + 1)}


def permdisp(d: np.ndarray, labels: np.ndarray, permutations: int, rng) -> dict:
    """Anderson 2006: ANOVA on distances to the group centroid, residuals permuted."""
    z = np.zeros(len(labels))
    for g in np.unique(labels):
        idx = np.nonzero(labels == g)[0]
        block = d[np.ix_(idx, idx)] ** 2
        grand = block.sum() / (2 * len(idx) ** 2)
        z[idx] = np.sqrt(np.clip(block.mean(1) - grand, 0, None))

    def anova(values: np.ndarray) -> float:
        means = {g: values[labels == g].mean() for g in np.unique(labels)}
        between = sum((labels == g).sum() * (m - values.mean()) ** 2 for g, m in means.items())
        within_ss = sum(((values[labels == g] - m) ** 2).sum() for g, m in means.items())
        k = len(means)
        return (between / (k - 1)) / (within_ss / (len(values) - k))

    f = anova(z)
    fitted = np.array([z[labels == g].mean() for g in labels])
    residual = z - fitted
    hits = sum(anova(fitted + rng.permutation(residual)) >= f for _ in range(permutations))
    return {"F": float(f), "p": (hits + 1) / (permutations + 1), "by_group": {int(g): float(z[labels == g].mean()) for g in np.unique(labels)}}


def gower(d: np.ndarray) -> np.ndarray:
    a = -0.5 * d**2
    return a - a.mean(0, keepdims=True) - a.mean(1, keepdims=True) + a.mean()


def explained(g: np.ndarray, *factors: np.ndarray) -> float:
    """Share of the distance variance explained by categorical factors, as tr(HG) / tr(G)."""
    columns = [np.ones((len(g), 1))]
    for factor in factors:
        columns.append(np.eye(int(factor.max()) + 1)[factor][:, 1:])
    q, r = np.linalg.qr(np.hstack(columns))
    keep = np.abs(np.diag(r)) > 1e-10
    q = q[:, keep]
    return float(np.trace(q.T @ g @ q) / np.trace(g))


def knn_purity(d: np.ndarray, labels: np.ndarray, k: int) -> tuple[float, np.ndarray]:
    work = d.copy()
    np.fill_diagonal(work, np.inf)
    nearest = np.argsort(work, axis=1)[:, :k]
    votes = labels[nearest]
    correct = np.zeros(len(labels), bool)
    for i, row in enumerate(votes):
        count = Counter(row.tolist())
        top = max(count.values())
        correct[i] = next(v for v in row.tolist() if count[v] == top) == labels[i]  # a tie goes to the nearest
    return float(correct.mean()), correct


def pairwise(d: np.ndarray, labels: np.ndarray, permutations: int, rng) -> list[dict]:
    rows = []
    for a, b in itertools.combinations(np.unique(labels), 2):
        ia, ib = np.nonzero(labels == a)[0], np.nonzero(labels == b)[0]
        idx = np.r_[ia, ib]
        d2 = d[np.ix_(idx, idx)] ** 2
        n, na, nb = len(idx), len(ia), len(ib)
        total = np.triu(d2, 1).sum() / n
        keys = rng.random((permutations + 1, n))
        keys[0] = np.r_[np.zeros(na), np.ones(nb)]
        mask = (np.argsort(np.argsort(keys, 1), 1) < na).astype(np.float32)
        ssw = (((mask @ d2.astype(np.float32)) * mask).sum(1) / na + (((1 - mask) @ d2.astype(np.float32)) * (1 - mask)).sum(1) / nb) / 2
        with np.errstate(divide="ignore"):  # two conditions each with one repeated profile: F is infinite, R2 is 1
            f = (total - ssw) / (ssw / (n - 2))
        rows.append({"a": int(a), "b": int(b), "R2": float(1 - ssw[0] / total), "F": float(f[0]), "p": float((f >= f[0]).mean())})
    order = np.argsort([r["p"] for r in rows])
    m = len(rows)
    holm, running = {}, 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, rows[i]["p"] * (m - rank)))
        holm[i] = running
    bh, running = {}, 1.0
    for rank, i in reversed(list(enumerate(order))):
        running = min(running, rows[i]["p"] * m / (rank + 1))
        bh[i] = running
    for i, row in enumerate(rows):
        row["p_holm"], row["p_bh"] = holm[i], bh[i]
    return rows


def sibling_null(d: np.ndarray, labels: np.ndarray, rng, repeats: int = 200) -> dict:
    """R2 of random halves of one condition: the size of 'no difference' at this sample size."""
    values = []
    for g in np.unique(labels):
        idx = np.nonzero(labels == g)[0]
        d2 = d[np.ix_(idx, idx)] ** 2
        n = len(idx)
        total = np.triu(d2, 1).sum() / n
        if total == 0:  # every case of the condition has the same profile: nothing to split
            continue
        for _ in range(repeats):
            half = rng.permutation(n)[: n // 2]
            other = np.setdiff1d(np.arange(n), half)
            ssw = np.triu(d2[np.ix_(half, half)], 1).sum() / len(half) + np.triu(d2[np.ix_(other, other)], 1).sum() / len(other)
            values.append(1 - ssw / total)
    return {"median": float(np.median(values)), "p95": float(np.quantile(values, 0.95)), "max": float(np.max(values))}


def condition_distance(d: np.ndarray, labels: np.ndarray, k: int) -> np.ndarray:
    """Energy distance between conditions: 2·between − within − within. Zero for identical distributions."""
    means = np.zeros((k, k))
    for a in range(k):
        for b in range(k):
            ia, ib = np.nonzero(labels == a)[0], np.nonzero(labels == b)[0]
            if not len(ia) or not len(ib):
                means[a, b] = np.nan
                continue
            block = d[np.ix_(ia, ib)]
            means[a, b] = block.sum() / (len(ia) * (len(ia) - 1)) if a == b and len(ia) > 1 else block.mean()
    e = 2 * means - np.diag(means)[:, None] - np.diag(means)[None, :]
    np.fill_diagonal(e, 0)
    return e


def family_test(e: np.ndarray, family: np.ndarray, permutations: int, rng) -> dict:
    """Are conditions of one family closer than others? Whole conditions are the exchangeable units."""
    iu, ju = np.triu_indices(len(e), 1)
    values = e[iu, ju]
    ok = ~np.isnan(values)

    def gap(f: np.ndarray) -> float:
        same = f[iu] == f[ju]
        return float(values[~same & ok].mean() - values[same & ok].mean())

    observed = gap(family)
    hits = sum(gap(rng.permutation(family)) >= observed for _ in range(permutations))
    linked = squareform(np.nan_to_num(np.clip(e, 0, None), nan=float(np.nanmax(e))), checks=False)
    clusters = fcluster(linkage(linked, "average"), len(set(family.tolist())), "maxclust")
    ari = adjusted_rand_score(family, clusters)
    null = [adjusted_rand_score(rng.permutation(family), clusters) for _ in range(permutations)]
    return {
        "within_family": float(values[(family[iu] == family[ju]) & ok].mean()),
        "across_family": float(values[(family[iu] != family[ju]) & ok].mean()),
        "gap": observed,
        "p": (hits + 1) / (permutations + 1),
        "ari": float(ari),
        "ari_p": (sum(v >= ari for v in null) + 1) / (permutations + 1),
    }


def mantel_conditions(a: np.ndarray, b: np.ndarray, permutations: int, rng) -> dict:
    iu = np.triu_indices(len(a), 1)
    x, y = a[iu], b[iu]
    ok = ~(np.isnan(x) | np.isnan(y))
    r = spearmanr(x[ok], y[ok]).statistic
    hits = 0
    for _ in range(permutations):
        p = rng.permutation(len(a))
        yp = b[np.ix_(p, p)][iu]
        hits += spearmanr(x[ok], yp[ok]).statistic >= r
    return {"spearman": float(r), "p": (hits + 1) / (permutations + 1)}


def mantel_within(a: np.ndarray, b: np.ndarray, labels: np.ndarray, permutations: int, rng) -> dict:
    """Inside one condition, does similar text mean a similar work-up? Cases move within their condition."""
    groups = [np.nonzero(labels == g)[0] for g in np.unique(labels)]
    iu = np.triu_indices(len(groups[0]), 1)

    def mean_r(shuffle: bool) -> float:
        rs = []
        for idx in groups:
            order = rng.permutation(idx) if shuffle else idx
            x, y = a[np.ix_(idx, idx)][iu], b[np.ix_(order, order)][iu]
            if x.std() and y.std():
                rs.append(np.corrcoef(rankdata(x), rankdata(y))[0, 1])
        return float(np.mean(rs))

    r = mean_r(False)
    hits = sum(mean_r(True) >= r for _ in range(permutations))
    return {"mean_spearman": r, "p": (hits + 1) / (permutations + 1)}


# ---------------------------------------------------------------- copying the nearest case


def f1(pred: set, gold: set) -> float:
    hit = len(pred & gold)
    return 2 * hit / (len(pred) + len(gold)) if hit else 0.0


def violations(pred: set[str], case: dict, severities: tuple[str, ...]) -> bool:
    for c in case["ground_truth"]["avoided_actions"]:
        if c.get("severity") not in severities:
            continue
        for alt in c["alternatives"]:
            exact = token(alt)
            if exact in pred or (not alt.get("required_arguments") and any(p.split("|")[0] == alt["tool_name"] for p in pred)):
                return True
    return False


def copy_baseline(cases: list[dict], labels: np.ndarray, family: np.ndarray, sim: np.ndarray, rng) -> dict:
    """Copy the required work-up of the nearest allowed case, for each reference set."""
    n = len(cases)
    tokens = [criterion_tokens(c, ("required",)) for c in cases]
    tools = [required_tools(c) for c in cases]
    icd = [{code[:3] for code in c["ground_truth"]["diagnosis"]["icd_codes"]} for c in cases]
    token_f1 = np.array([[f1(tokens[i], tokens[j]) for j in range(n)] for i in range(n)])
    tool_f1 = np.array([[f1(tools[i], tools[j]) for j in range(n)] for i in range(n)])
    same = labels[:, None] == labels[None, :]
    same_family = family[:, None] == family[None, :]
    off = ~np.eye(n, dtype=bool)
    masks = {"siblings": same & off, "all_others": off, "leave_condition_out": ~same, "leave_family_out": ~same_family}
    rows = {}
    for name, mask in masks.items():
        s = np.where(mask, sim, -np.inf)
        nn = s.argmax(1)
        rows[name] = {
            "token_f1": token_f1[np.arange(n), nn],
            "tool_f1": tool_f1[np.arange(n), nn],
            "diagnosis": np.array([bool(icd[i] & icd[j]) for i, j in enumerate(nn)], float),
            "harm": np.array([violations(tokens[j], cases[i], ("harm", "contraindicated")) for i, j in enumerate(nn)], float),
            "any_avoided": np.array([violations(tokens[j], cases[i], ("harm", "contraindicated", "waste")) for i, j in enumerate(nn)], float),
        }
    for name, mask in (("siblings", masks["siblings"]), ("leave_condition_out", masks["leave_condition_out"])):
        rows[f"random_{name}"] = {
            "token_f1": (token_f1 * mask).sum(1) / mask.sum(1),
            "tool_f1": (tool_f1 * mask).sum(1) / mask.sum(1),
        }
        rows[f"oracle_{name}"] = {"token_f1": np.where(mask, token_f1, 0).max(1), "tool_f1": np.where(mask, tool_f1, 0).max(1)}
    k = int(np.median([len(t) for t in tokens]))
    popular_token, popular_tool = np.zeros(n), np.zeros(n)
    for g in np.unique(labels):
        reference = np.nonzero(labels != g)[0]
        top_token = {t for t, _ in Counter(t for i in reference for t in tokens[i]).most_common(k)}
        top_tool = {t for t, _ in Counter(t for i in reference for t in tools[i]).most_common(k)}
        for i in np.nonzero(labels == g)[0]:
            popular_token[i], popular_tool[i] = f1(top_token, tokens[i]), f1(top_tool, tools[i])
    rows["popular_leave_condition_out"] = {"token_f1": popular_token, "tool_f1": popular_tool}
    return {"rows": rows, "token_f1": token_f1, "tool_f1": tool_f1}


def condition_bootstrap(values: np.ndarray, labels: np.ndarray, rng, repeats: int = 10000) -> list[float]:
    means = np.array([values[labels == g].mean() for g in np.unique(labels)])
    draws = rng.integers(0, len(means), (repeats, len(means)))
    return [float(v) for v in np.quantile(means[draws].mean(1), [0.025, 0.975])]


def enumerate_test_sets(sim: np.ndarray, token_f1: np.ndarray, labels: np.ndarray, members: list[str], valid: np.ndarray) -> dict:
    """Where the proposed test conditions sit among all C(20,4) choices."""
    k = len(members)
    best_sim = np.full((len(labels), k), -np.inf)
    best_f1 = np.zeros((len(labels), k))
    for c in range(k):
        idx = np.nonzero((labels == c) & valid)[0]
        s = sim[:, idx].copy()
        s[np.arange(len(labels))[labels == c], :] = -np.inf  # a case never retrieves its own condition
        j = s.argmax(1)
        best_sim[:, c] = s[np.arange(len(labels)), j]
        best_f1[:, c] = token_f1[np.arange(len(labels)), idx[j]]
    results = {}
    for combo in itertools.combinations(range(k), 4):
        rest = [c for c in range(k) if c not in combo]
        q = np.isin(labels, combo) & valid
        pick = best_sim[q][:, rest].argmax(1)
        results[combo] = (float(best_sim[q][np.arange(q.sum()), np.array(rest)[pick]].mean()), float(best_f1[q][np.arange(q.sum()), np.array(rest)[pick]].mean()))
    proposed = tuple(sorted(members.index(c) for c in TEST))
    sims = np.array([v[0] for v in results.values()])
    f1s = np.array([v[1] for v in results.values()])
    return {
        "n": len(results),
        "proposed_similarity": results[proposed][0],
        "proposed_copy_f1": results[proposed][1],
        "similarity_percentile": float((sims <= results[proposed][0]).mean()),
        "copy_f1_percentile": float((f1s <= results[proposed][1]).mean()),
        "similarity_range": [float(sims.min()), float(sims.max())],
        "copy_f1_range": [float(f1s.min()), float(f1s.max())],
    }


# ---------------------------------------------------------------- main


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--permutations", type=int, default=9999)
    parser.add_argument("--no-embeddings", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(SEED)
    P = args.permutations

    _, by_id, _ = load()
    ids = sorted(by_id)
    cases = [by_id[i] for i in ids]
    members = sorted(FAMILIES)
    family_names = sorted(set(FAMILIES.values()))
    labels = np.array([members.index(c["condition"]) for c in cases])
    family = np.array([family_names.index(FAMILIES[c["condition"]]) for c in cases])
    condition_family = np.array([family_names.index(FAMILIES[m]) for m in members])
    difficulty_names = sorted({c["difficulty"] for c in cases})
    difficulty = np.array([difficulty_names.index(c["difficulty"]) for c in cases])
    encounter = np.unique([c["encounter_type"] for c in cases], return_inverse=True)[1]

    texts = [field_texts(c) for c in cases]
    narrative, reports = [t["narrative"] for t in texts], [t["tool_outputs"] for t in texts]
    narrative_tfidf = tfidf_matrix(narrative)
    views: dict[str, tuple[np.ndarray, np.ndarray]] = {}
    everyone = np.arange(len(cases))
    views["narrative_tfidf"] = (chord(narrative_tfidf.toarray()), everyone)
    views["reports_tfidf"] = (chord(tfidf_matrix(reports).toarray()), everyone)
    views["narrative_style"] = (chord(style_matrix(narrative)), everyone)
    narrative_sim = (narrative_tfidf @ narrative_tfidf.T).toarray()
    retrievers = {"tfidf": narrative_sim}
    if not args.no_embeddings:
        narrative_emb = embed(narrative, "narrative")
        views["narrative_embedding"] = (chord(narrative_emb), everyone)
        views["reports_embedding"] = (chord(embed(reports, "reports")), everyone)
        retrievers["embedding"] = narrative_emb @ narrative_emb.T
    views["required_tools"] = (set_distance([required_tools(c) for c in cases]), everyone)
    views["required_tokens"] = (set_distance([criterion_tokens(c, ("required",)) for c in cases]), everyone)
    views["workup_tokens"] = (set_distance([criterion_tokens(c, ("required", "recommended")) for c in cases]), everyone)
    views["avoided_tokens"] = (set_distance([avoided_tokens(c) for c in cases]), everyone)
    for level in ("tool", "token"):
        pairs = [precedence(c, level) for c in cases]
        keep = np.array([i for i, p in enumerate(pairs) if p])
        views[f"order_pairs_{level}"] = (set_distance([pairs[i] for i in keep]), keep)
    sequences = [canonical_sequence(c) for c in cases]
    seq = np.array([[edit_distance(a, b) for b in sequences] for a in sequences])
    views["order_sequence"] = (seq, everyone)

    summary: dict = {"n_cases": len(cases), "seed": SEED, "permutations": P, "families": FAMILIES, "views": {}}
    view_rows, condition_matrices = [], {}
    for name, (d, keep) in views.items():
        y = labels[keep]
        strata = difficulty[keep]
        main_test = permanova(d, y, P, rng)
        stratified = permanova(d, y, P, rng, strata)
        dispersion = permdisp(d, y, P, rng)
        g = gower(d)
        r2_cond, r2_diff, r2_enc = explained(g, y), explained(g, strata), explained(g, encounter[keep])
        r2_full = explained(g, y, strata)
        r2_cond_enc = explained(g, y, encounter[keep])
        purity1, correct1 = knn_purity(d, y, 1)
        purity5, _ = knn_purity(d, y, 5)
        silhouette = silhouette_samples(d, y, metric="precomputed")
        family_y = family[keep]
        family_sil = silhouette_samples(d, family_y, metric="precomputed")
        iu = np.triu_indices(len(keep), 1)
        within = y[iu[0]] == y[iu[1]]
        pairs_within, pairs_between = d[iu][within], d[iu][~within]
        ranks = rankdata(np.r_[pairs_within, pairs_between])[: len(pairs_within)]
        auc = 1 - (ranks.sum() - len(ranks) * (len(ranks) + 1) / 2) / (len(pairs_within) * len(pairs_between))
        pair_rows = pairwise(d, y, P, rng)
        null = sibling_null(d, y, rng)
        write_csv(OUT / f"pairwise_{name}.csv", [{**r, "a": members[r["a"]], "b": members[r["b"]]} for r in pair_rows])
        e = condition_distance(d, y, len(members))
        condition_matrices[name] = e
        with (OUT / f"condition_distance_{name}.csv").open("w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["", *members])
            writer.writerows([[m, *row] for m, row in zip(members, e.round(5).tolist())])
        shuffled = rng.permutation(y)
        pair_r2 = np.array([r["R2"] for r in pair_rows])
        closest = sorted(pair_rows, key=lambda r: r["R2"])[:5]
        row = {
            "view": name,
            "n": len(keep),
            "within_median": float(np.median(pairs_within)),
            "between_median": float(np.median(pairs_between)),
            "auc_between_gt_within": float(auc),
            "permanova_R2": main_test["R2"],
            "permanova_F": main_test["F"],
            "permanova_p": main_test["p"],
            "stratified_p": stratified["p"],
            "permdisp_F": dispersion["F"],
            "permdisp_p": dispersion["p"],
            "R2_difficulty": r2_diff,
            "R2_condition_given_difficulty": r2_full - r2_diff,
            "R2_encounter": r2_enc,
            "R2_condition_given_encounter": r2_cond_enc - r2_enc,
            "R2_encounter_given_condition": r2_cond_enc - r2_cond,
            "knn1": purity1,
            "knn5": purity5,
            "silhouette": float(silhouette.mean()),
            "silhouette_negative_share": float((silhouette < 0).mean()),
            "family_silhouette": float(family_sil.mean()),
            "pair_R2_median": float(np.median(pair_r2)),
            "pair_R2_min": float(pair_r2.min()),
            "pairs_holm_significant": int(sum(r["p_holm"] < 0.05 for r in pair_rows)),
            "pairs_bh_significant": int(sum(r["p_bh"] < 0.05 for r in pair_rows)),
            "pairs_below_sibling_p95": int((pair_r2 <= null["p95"]).sum()),
            "sibling_R2_median": null["median"],
            "sibling_R2_p95": null["p95"],
            "shuffled_R2": explained(g, shuffled),
            "shuffled_knn1": knn_purity(d, shuffled, 1)[0],
        }
        view_rows.append(row)
        summary["views"][name] = {
            **row,
            "closest_pairs": [{"a": members[r["a"]], "b": members[r["b"]], "R2": r["R2"], "p_holm": r["p_holm"]} for r in closest],
            "families": family_test(e, condition_family, P, rng),
            "knn1_by_difficulty": {difficulty_names[s]: float(correct1[strata == s].mean()) for s in np.unique(strata)},
            "silhouette_by_difficulty": {difficulty_names[s]: float(silhouette[strata == s].mean()) for s in np.unique(strata)},
            "by_condition": {
                members[g_]: {"silhouette": float(silhouette[y == g_].mean()), "knn1": float(correct1[y == g_].mean()), "spread": dispersion["by_group"][int(g_)]}
                for g_ in np.unique(y)
            },
        }
        print(f"{name:22s} n={len(keep)} R2={row['permanova_R2']:.3f} AUC={row['auc_between_gt_within']:.3f} knn1={purity1:.3f} sil={row['silhouette']:.3f}", flush=True)
    write_csv(OUT / "views.csv", view_rows)

    links = [("narrative_tfidf", "required_tokens"), ("reports_tfidf", "required_tokens"), ("required_tokens", "avoided_tokens"), ("required_tools", "order_sequence"), ("narrative_style", "required_tokens")]
    if "narrative_embedding" in views:
        links.append(("narrative_embedding", "required_tokens"))
    summary["cross_view"] = {}
    for a, b in links:
        entry = {"between_conditions": mantel_conditions(condition_matrices[a], condition_matrices[b], P, rng)}
        if len(views[a][1]) == len(views[b][1]) == len(cases):
            entry["within_condition"] = mantel_within(views[a][0], views[b][0], labels, 999, rng)
        summary["cross_view"][f"{a} ~ {b}"] = entry

    # What an agent gains from similarity.
    summary["copy"] = {}
    copy_rows = []
    for retriever, sim in retrievers.items():
        result = copy_baseline(cases, labels, family, sim, rng)
        for reference, metrics in result["rows"].items():
            for metric, values in metrics.items():
                low, high = condition_bootstrap(values, labels, rng)
                row = {"retriever": retriever, "reference": reference, "metric": metric, "mean": float(values.mean()), "ci_low": low, "ci_high": high}
                copy_rows.append(row)
                summary["copy"][f"{retriever}/{reference}/{metric}"] = row
        rows = result["rows"]
        per = lambda key, metric="token_f1": np.array([rows[key][metric][labels == g].mean() for g in np.unique(labels)])
        summary["copy"][f"{retriever}/tests"] = {
            "loco_vs_random_token": wilcoxon(per("leave_condition_out"), per("random_leave_condition_out"), alternative="greater").pvalue,
            "siblings_vs_loco_token": wilcoxon(per("siblings"), per("leave_condition_out"), alternative="greater").pvalue,
            "loco_vs_popular_token": wilcoxon(per("leave_condition_out"), per("popular_leave_condition_out"), alternative="greater").pvalue,
        }
        summary["copy"][f"{retriever}/by_condition"] = {
            members[g]: {"siblings": float(rows["siblings"]["token_f1"][labels == g].mean()), "loco": float(rows["leave_condition_out"]["token_f1"][labels == g].mean()), "lofo": float(rows["leave_family_out"]["token_f1"][labels == g].mean())}
            for g in np.unique(labels)
        }
        if retriever == "tfidf":
            valid = np.array([c["case_id"] not in SPLIT_EXCLUDED for c in cases])
            summary["split_enumeration"] = enumerate_test_sets(sim, result["token_f1"], labels, members, valid)
            train = np.isin(labels, [members.index(c) for c in members if c not in TEST + VALIDATION]) & valid
            detail = {}
            for name in TEST + VALIDATION:
                q = (labels == members.index(name)) & valid
                s = np.where(train[None, :], sim[q], -np.inf)
                nn = s.argmax(1)
                near = Counter(members[labels[j]] for j in nn)
                detail[name] = {
                    "nearest_similarity": float(s.max(1).mean()),
                    "token_f1": float(result["token_f1"][np.nonzero(q)[0], nn].mean()),
                    "tool_f1": float(result["tool_f1"][np.nonzero(q)[0], nn].mean()),
                    "nearest_conditions": near.most_common(3),
                }
            summary["proposed_split"] = detail
    write_csv(OUT / "copy_baseline.csv", copy_rows)

    # Vocabulary specificity and how much each tool is shared.
    tokens_by_condition: dict[str, set] = defaultdict(set)
    pairs_by_condition: dict = defaultdict(set)
    instance = Counter()
    for case, g in zip(cases, labels):
        required = criterion_tokens(case, ("required",))
        tokens_by_condition[members[g]] |= required
        instance.update(required)
        pairs_by_condition[members[g]] |= precedence(case, "token")
    spread = Counter(t for s in tokens_by_condition.values() for t in s)
    pair_spread = Counter(p for s in pairs_by_condition.values() for p in s)
    summary["specificity"] = {
        "required_tokens": len(spread),
        "tokens_in_one_condition": sum(v == 1 for v in spread.values()),
        "instances_of_exclusive_tokens": sum(instance[t] for t, v in spread.items() if v == 1) / sum(instance.values()),
        "most_shared": [(t, v) for t, v in spread.most_common(8)],
        "precedence_pairs": len(pair_spread),
        "pairs_in_one_condition": sum(v == 1 for v in pair_spread.values()),
    }
    tool_rows = []
    tools = sorted({t for c in cases for t in required_tools(c)})
    for g, name in enumerate(members):
        idx = np.nonzero(labels == g)[0]
        tool_rows.append({"condition": name, **{t: round(float(np.mean([t in required_tools(cases[i]) for i in idx])), 3) for t in tools}})
    write_csv(OUT / "tool_by_condition.csv", tool_rows)

    # Order given the same tools: reversed pairs, not just different sets. A pair ordered both ways in
    # one case is a repeated tool (the NPH tap test: assessment, CSF drainage, assessment), not an order.
    summary["order_conflicts"] = {}
    for level in ("tool", "token"):
        pairs = []
        for c in cases:
            p = precedence(c, level)
            pairs.append({(a, b) for a, b in p if (b, a) not in p})
        keep = [i for i, p in enumerate(pairs) if p]
        tally = {True: [0, 0], False: [0, 0]}
        for i, j in itertools.combinations(keep, 2):
            shared = {frozenset(p) for p in pairs[i]} & {frozenset(p) for p in pairs[j]}
            if shared:
                bucket = tally[bool(labels[i] == labels[j])]
                bucket[0] += sum((b, a) in pairs[j] for a, b in pairs[i])
                bucket[1] += len(shared)
        summary["order_conflicts"][level] = {
            "cases_with_constraints": len(keep),
            "reversed_share_within_condition": tally[True][0] / max(tally[True][1], 1),
            "reversed_share_between_conditions": tally[False][0] / max(tally[False][1], 1),
            "shared_pairs_within": tally[True][1],
            "shared_pairs_between": tally[False][1],
        }

    # Is a condition really one answer, and who names whom in the differential?
    # A condition's codes: the most frequent ICD-10 categories until they cover 80% of its cases
    # (syncope spreads over I44, I45, I47, I49, so a fixed count threshold would flag all of it).
    modal = {}
    for g, name in enumerate(members):
        sets = [{x[:3] for x in cases[i]["ground_truth"]["diagnosis"]["icd_codes"]} for i in np.nonzero(labels == g)[0]]
        chosen: set[str] = set()
        for code, _ in Counter(code for s in sets for code in s).most_common():
            if sum(bool(s & chosen) for s in sets) >= 0.8 * len(sets):
                break
            chosen.add(code)
        modal[name] = chosen
    foreign = [c["case_id"] for c in cases if not {x[:3] for x in c["ground_truth"]["diagnosis"]["icd_codes"]} & modal[c["condition"]]]
    shared_codes = {f"{a} / {b}": sorted(modal[a] & modal[b]) for a, b in itertools.combinations(members, 2) if modal[a] & modal[b]}
    named = np.zeros((len(members), len(members)))
    for case, g in zip(cases, labels):
        text = " ".join(flatten(case["ground_truth"]["differential"]))
        for h, name in enumerate(members):
            if h != g and re.search(MENTION[name], text, re.I):
                named[g, h] += 1 / 30
    symmetric = (named + named.T) / 2
    summary["answers"] = {
        "condition_codes": {name: sorted(codes) for name, codes in modal.items()},
        "cases_outside_their_condition_codes": foreign,
        "conditions_sharing_a_modal_code": shared_codes,
        "top_differential_mentions": {members[g]: [(members[h], round(float(named[g, h]), 2)) for h in np.argsort(-named[g])[:3]] for g in range(len(members))},
    }
    summary["cross_view"]["differential_mentions ~ required_tokens"] = {
        "between_conditions": mantel_conditions(-symmetric, condition_matrices["required_tokens"], P, rng)
    }
    summary["answers"]["narrative_names_own_diagnosis"] = sum(
        any(len(label) >= 6 and re.search(re.escape(label), text, re.I) for label in case["ground_truth"]["diagnosis"]["accepted"])
        for case, text in zip(cases, narrative)
    )
    unique_sets = {}
    for g, name in enumerate(members):
        idx = np.nonzero(labels == g)[0]
        unique_sets[name] = len({frozenset(criterion_tokens(cases[i], ("required",))) for i in idx})
    write_csv(
        OUT / "per_condition.csv",
        [
            {
                "condition": name,
                "family": FAMILIES[name],
                "unique_required_sets": unique_sets[name],
                "mean_required": round(float(np.mean([len(criterion_tokens(cases[i], ("required",))) for i in np.nonzero(labels == g)[0]])), 2),
                "difficulty": dict(Counter(cases[i]["difficulty"] for i in np.nonzero(labels == g)[0])),
                "encounter": dict(Counter(cases[i]["encounter_type"] for i in np.nonzero(labels == g)[0])),
            }
            for g, name in enumerate(members)
        ],
    )
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, default=float))
    print(f"done, {OUT}; embeddings {'on' if 'narrative_embedding' in views else 'off'}; pid {os.getpid()}")


if __name__ == "__main__":
    main()
