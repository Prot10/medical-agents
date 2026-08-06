"""Build the NeuroBench train/test split used for agent distillation.

The test set is deliberately two-part:

1. **Held-out conditions** — every case of 2 conditions is removed from training.
   This measures generalisation to a pathology the student has never seen, which a
   random split cannot measure at all.
2. **Stratified in-distribution remainder** — the rest of the test set is drawn from
   the remaining conditions, balanced across condition, difficulty and encounter type,
   so in-distribution accuracy stays measurable.

Gold trajectories are only generated for the TRAIN split, so no test case ever appears
in a teacher trajectory.

Usage:
    uv run python -m neuroagent.training.data.make_train_test_split \
        --dataset data/neurobench \
        --output data/neurobench/splits \
        --test-size 100
"""

from __future__ import annotations

import argparse
import json
import logging
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Held out entirely from training. Chosen because neither has a near-duplicate
# sibling condition in the remaining 18 (unlike e.g. SAH/ischemic_stroke or
# alzheimers/ftd), so the student cannot solve them by analogy to a trained
# pathway, and they exercise different tool families (NMJ antibody/specialized
# testing vs. toxic-metabolic labs + EEG).
DEFAULT_HELDOUT_CONDITIONS = ["myasthenia_gravis", "hepatic_encephalopathy"]


def load_case_metadata(dataset_path: Path) -> list[dict[str, str]]:
    """Read (case_id, condition, difficulty, encounter_type) for every case."""
    cases_dir = dataset_path / "cases"
    if not cases_dir.exists():
        raise FileNotFoundError(f"Cases directory not found: {cases_dir}")

    meta = []
    for cf in sorted(cases_dir.glob("*.json")):
        data = json.loads(cf.read_text())
        meta.append(
            {
                "case_id": data["case_id"],
                "condition": data["condition"],
                "difficulty": data["difficulty"],
                "encounter_type": data["encounter_type"],
            }
        )
    return meta


def _quota_per_condition(conditions: list[str], n: int) -> dict[str, int]:
    """Spread n picks as evenly as possible across conditions (largest-remainder)."""
    base, extra = divmod(n, len(conditions))
    quota = {c: base for c in conditions}
    for c in conditions[:extra]:
        quota[c] += 1
    return quota


def _target_ratios(cases: list[dict[str, str]], key: str) -> dict[str, float]:
    counts = Counter(c[key] for c in cases)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}


def select_stratified(
    pool: list[dict[str, str]],
    n: int,
    seed: int,
) -> list[dict[str, str]]:
    """Pick n cases, even across conditions and matching difficulty/encounter ratios.

    Greedy: walk conditions round-robin; within each pick the candidate that moves the
    running difficulty/encounter distribution closest to the pool's own distribution.
    """
    rng = random.Random(seed)

    by_condition: dict[str, list[dict[str, str]]] = defaultdict(list)
    for c in pool:
        by_condition[c["condition"]].append(c)

    conditions = sorted(by_condition)
    rng.shuffle(conditions)  # which conditions get the +1 is seed-determined
    quota = _quota_per_condition(conditions, n)

    for c in conditions:
        rng.shuffle(by_condition[c])

    diff_target = _target_ratios(pool, "difficulty")
    enc_target = _target_ratios(pool, "encounter_type")

    chosen: list[dict[str, str]] = []
    diff_have: Counter[str] = Counter()
    enc_have: Counter[str] = Counter()

    def deficit(case: dict[str, str]) -> float:
        """Lower is better: how far this pick leaves us from the target ratios."""
        total = len(chosen) + 1
        d = diff_have + Counter([case["difficulty"]])
        e = enc_have + Counter([case["encounter_type"]])
        d_err = sum(abs(d[k] / total - v) for k, v in diff_target.items())
        e_err = sum(abs(e[k] / total - v) for k, v in enc_target.items())
        return d_err + e_err

    # Round-robin over conditions so no condition is exhausted before others start.
    remaining = dict(quota)
    while sum(remaining.values()) > 0:
        for cond in conditions:
            if remaining[cond] <= 0:
                continue
            candidates = by_condition[cond]
            if not candidates:
                remaining[cond] = 0
                continue
            best = min(candidates, key=deficit)
            candidates.remove(best)
            chosen.append(best)
            diff_have[best["difficulty"]] += 1
            enc_have[best["encounter_type"]] += 1
            remaining[cond] -= 1

    return chosen


def build_split(
    meta: list[dict[str, str]],
    heldout_conditions: list[str],
    test_size: int,
    seed: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """Return (train, test_heldout_condition, test_stratified)."""
    known = {c["condition"] for c in meta}
    unknown = set(heldout_conditions) - known
    if unknown:
        raise ValueError(f"Unknown held-out conditions: {sorted(unknown)}")

    heldout = [c for c in meta if c["condition"] in heldout_conditions]
    pool = [c for c in meta if c["condition"] not in heldout_conditions]

    n_stratified = test_size - len(heldout)
    if n_stratified < 0:
        raise ValueError(
            f"Held-out conditions contribute {len(heldout)} cases, exceeding test_size={test_size}"
        )

    stratified = select_stratified(pool, n_stratified, seed)
    stratified_ids = {c["case_id"] for c in stratified}
    train = [c for c in pool if c["case_id"] not in stratified_ids]

    return train, heldout, stratified


def build_split_preserving(
    meta: list[dict[str, str]],
    prior: dict[str, Any],
    heldout_conditions: list[str],
    test_size: int,
    seed: int,
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    """Rebuild the split without reshuffling cases that were already assigned.

    A change in dataset composition — a condition retired, a condition added — otherwise
    reshuffles the whole split, because the stratified pick is seeded over the case set. That
    has two costs that are easy to miss: every published number stops being comparable, and the
    gold trajectory corpus (generated for the train split only) is invalidated for cases that
    merely moved sides. Preserving prior membership confines both costs to the cases that
    actually changed.

    Cases the prior manifest never saw are placed here: enough of them go to the stratified
    test set to restore `test_size`, chosen with the same stratified selector, and the rest go
    to train. Held-out conditions are recomputed from the argument, so changing that list still
    works.
    """
    prior_train = set(prior.get("train_case_ids") or [])
    prior_test = set(prior.get("test_stratified_case_ids") or []) | set(
        prior.get("test_heldout_condition_case_ids") or []
    )

    known = {c["condition"] for c in meta}
    unknown = set(heldout_conditions) - known
    if unknown:
        raise ValueError(f"Unknown held-out conditions: {sorted(unknown)}")

    heldout = [c for c in meta if c["condition"] in heldout_conditions]
    pool = [c for c in meta if c["condition"] not in heldout_conditions]

    n_stratified = test_size - len(heldout)
    if n_stratified < 0:
        raise ValueError(
            f"Held-out conditions contribute {len(heldout)} cases, exceeding test_size={test_size}"
        )

    carried_test = [c for c in pool if c["case_id"] in prior_test]
    carried_train = [c for c in pool if c["case_id"] in prior_train]
    fresh = [
        c for c in pool if c["case_id"] not in prior_test and c["case_id"] not in prior_train
    ]

    need = n_stratified - len(carried_test)
    if need > 0:
        promoted = select_stratified(fresh, min(need, len(fresh)), seed)
        promoted_ids = {c["case_id"] for c in promoted}
        stratified = carried_test + promoted
        train = carried_train + [c for c in fresh if c["case_id"] not in promoted_ids]
        logger.info(
            "preserved %d prior assignments; placed %d new cases (%d to test, %d to train)",
            len(carried_test) + len(carried_train), len(fresh), len(promoted),
            len(fresh) - len(promoted),
        )
    elif need < 0:
        demoted = select_stratified(carried_test, -need, seed)
        demoted_ids = {c["case_id"] for c in demoted}
        stratified = [c for c in carried_test if c["case_id"] not in demoted_ids]
        train = carried_train + demoted + fresh
        logger.warning(
            "prior test set exceeds test_size by %d after the composition change; "
            "moved %s to train", -need, sorted(demoted_ids),
        )
    else:
        stratified = carried_test
        train = carried_train + fresh
        logger.info("preserved all prior assignments; %d new cases to train", len(fresh))

    return train, heldout, stratified


def _distribution_report(name: str, cases: list[dict[str, str]]) -> str:
    diff = Counter(c["difficulty"] for c in cases)
    enc = Counter(c["encounter_type"] for c in cases)
    ncond = len({c["condition"] for c in cases})
    return (
        f"{name:<22} n={len(cases):<4} conditions={ncond:<3} "
        f"difficulty={dict(sorted(diff.items()))} encounter={dict(sorted(enc.items()))}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build NeuroBench train/test split")
    parser.add_argument("--dataset", default="data/neurobench")
    parser.add_argument("--output", default="data/neurobench/splits")
    parser.add_argument("--test-size", type=int, default=100)
    parser.add_argument("--heldout-conditions", nargs="+", default=DEFAULT_HELDOUT_CONDITIONS)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--preserve",
        default=None,
        metavar="MANIFEST",
        help=(
            "Path to a previous split_manifest.json. Cases it already assigned keep their side; "
            "only cases it never saw are placed. Use this whenever dataset composition changes, "
            "so published numbers stay comparable and existing gold trajectories stay valid."
        ),
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    meta = load_case_metadata(Path(args.dataset))
    if args.preserve:
        prior = json.loads(Path(args.preserve).read_text())
        train, heldout, stratified = build_split_preserving(
            meta, prior, args.heldout_conditions, args.test_size, args.seed
        )
    else:
        train, heldout, stratified = build_split(
            meta, args.heldout_conditions, args.test_size, args.seed
        )
    test = heldout + stratified

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    (out / "train_cases.txt").write_text(
        "\n".join(sorted(c["case_id"] for c in train)) + "\n"
    )
    (out / "test_cases.txt").write_text("\n".join(sorted(c["case_id"] for c in test)) + "\n")

    manifest = {
        "seed": args.seed,
        "test_size": args.test_size,
        "heldout_conditions": args.heldout_conditions,
        "n_train": len(train),
        "n_test": len(test),
        "n_test_heldout_condition": len(heldout),
        "n_test_stratified": len(stratified),
        "train_case_ids": sorted(c["case_id"] for c in train),
        "test_heldout_condition_case_ids": sorted(c["case_id"] for c in heldout),
        "test_stratified_case_ids": sorted(c["case_id"] for c in stratified),
    }
    (out / "split_manifest.json").write_text(json.dumps(manifest, indent=2))

    print(_distribution_report("TRAIN", train))
    print(_distribution_report("TEST (heldout cond)", heldout))
    print(_distribution_report("TEST (stratified)", stratified))
    print(_distribution_report("TEST (total)", test))
    print(f"\nHeld-out conditions: {', '.join(args.heldout_conditions)}")
    print(f"Written to {out}/  (train_cases.txt, test_cases.txt, split_manifest.json)")


if __name__ == "__main__":
    main()
