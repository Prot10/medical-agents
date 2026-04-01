"""Stratified k-fold splitting for NeuroBench dataset.

Splits cases into k folds stratified by condition AND difficulty,
ensuring balanced representation in each fold.

Usage:
    python -m neuroagent.training.data.split_dataset \
        --dataset data/neurobench_v4 \
        --output data/neurobench_v4/splits \
        --k 5
"""

from __future__ import annotations

import argparse
import json
import logging
from collections import defaultdict
from pathlib import Path

from neuroagent_schemas import NeuroBenchCase

logger = logging.getLogger(__name__)


def load_case_metadata(dataset_path: Path) -> list[dict[str, str]]:
    """Load case IDs with condition and difficulty metadata."""
    cases_dir = dataset_path / "cases"
    metadata = []
    for cf in sorted(cases_dir.glob("*.json")):
        data = json.loads(cf.read_text())
        metadata.append({
            "case_id": data["case_id"],
            "condition": data["condition"],
            "difficulty": data["difficulty"],
        })
    return metadata


def stratified_kfold(
    metadata: list[dict[str, str]],
    k: int = 5,
    seed: int = 42,
) -> list[dict[str, list[str]]]:
    """Create k stratified folds.

    Stratifies by (condition, difficulty) tuple to ensure balanced
    representation across all folds.

    Returns list of k dicts, each with 'train' and 'val' case ID lists.
    """
    import random
    rng = random.Random(seed)

    # Group by stratification key
    groups: dict[str, list[str]] = defaultdict(list)
    for m in metadata:
        key = f"{m['condition']}_{m['difficulty']}"
        groups[key].append(m["case_id"])

    # Shuffle within each group
    for key in groups:
        rng.shuffle(groups[key])

    # Assign each case to a fold
    case_to_fold: dict[str, int] = {}
    for key, case_ids in groups.items():
        for i, case_id in enumerate(case_ids):
            case_to_fold[case_id] = i % k

    # Build fold splits
    all_case_ids = [m["case_id"] for m in metadata]
    folds = []
    for fold_idx in range(k):
        val_ids = [cid for cid in all_case_ids if case_to_fold[cid] == fold_idx]
        train_ids = [cid for cid in all_case_ids if case_to_fold[cid] != fold_idx]
        folds.append({"train": sorted(train_ids), "val": sorted(val_ids)})

    return folds


def save_splits(
    folds: list[dict[str, list[str]]],
    output_dir: Path,
    metadata: list[dict[str, str]],
) -> None:
    """Save fold splits as text files and a summary JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build condition/difficulty lookup
    meta_by_id = {m["case_id"]: m for m in metadata}

    summary = {"k": len(folds), "folds": []}

    for i, fold in enumerate(folds):
        # Save train/val lists
        train_path = output_dir / f"fold{i}_train.txt"
        val_path = output_dir / f"fold{i}_val.txt"
        train_path.write_text("\n".join(fold["train"]) + "\n")
        val_path.write_text("\n".join(fold["val"]) + "\n")

        # Compute distribution stats
        val_conditions = defaultdict(int)
        val_difficulties = defaultdict(int)
        for cid in fold["val"]:
            m = meta_by_id[cid]
            val_conditions[m["condition"]] += 1
            val_difficulties[m["difficulty"]] += 1

        fold_info = {
            "fold": i,
            "train_size": len(fold["train"]),
            "val_size": len(fold["val"]),
            "val_conditions": dict(val_conditions),
            "val_difficulties": dict(val_difficulties),
        }
        summary["folds"].append(fold_info)

        logger.info(
            "Fold %d: train=%d, val=%d, conditions=%s",
            i, len(fold["train"]), len(fold["val"]),
            dict(val_conditions),
        )

    # Save summary
    summary_path = output_dir / "splits_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2))
    logger.info("Saved %d-fold splits to %s", len(folds), output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create stratified k-fold splits")
    parser.add_argument("--dataset", required=True, help="Path to NeuroBench dataset")
    parser.add_argument("--output", default=None, help="Output directory (default: dataset/splits)")
    parser.add_argument("--k", type=int, default=5, help="Number of folds")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    dataset_path = Path(args.dataset)
    output_dir = Path(args.output) if args.output else dataset_path / "splits"

    metadata = load_case_metadata(dataset_path)
    logger.info("Loaded %d cases", len(metadata))

    folds = stratified_kfold(metadata, k=args.k, seed=args.seed)
    save_splits(folds, output_dir, metadata)


if __name__ == "__main__":
    main()
