"""The GRPO prompt dataset must describe the cases that exist, not the ones that used to.

The August 2026 composition change left the prompt files referencing 30 deleted cases and missing
30 new ones, and nothing in the suite noticed: the files are derived artifacts that no test read.
A GRPO run would have trained against prompts for cases that no longer exist.

These tests skip when the artifact is absent — it is regenerable, needs a tokenizer, and is not
committed fresh on every dataset change — and fail when it is present and disagrees with the split.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
CASES = REPO_ROOT / "data/neurobench/cases"
SPLITS = REPO_ROOT / "data/neurobench/splits"
GRPO = REPO_ROOT / "data/neurobench/grpo"


def _case_ids(path: Path) -> set[str]:
    return {json.loads(line)["case_id"] for line in path.read_text().splitlines() if line.strip()}


@pytest.mark.parametrize("split", ["train", "test"])
def test_prompts_match_the_split(split: str) -> None:
    prompts = GRPO / f"{split}_prompts.jsonl"
    split_file = SPLITS / f"{split}_cases.txt"
    if not prompts.exists():
        pytest.skip(f"{prompts.name} not built — regenerate with build_grpo_dataset")
    if not split_file.exists():
        pytest.skip("split file not present")

    in_prompts = _case_ids(prompts)
    in_split = {c for c in split_file.read_text().split() if c}
    on_disk = {p.stem for p in CASES.glob("*.json")}

    assert not (in_prompts - on_disk), (
        f"prompts reference cases that do not exist: {sorted(in_prompts - on_disk)[:10]}"
    )
    assert in_prompts == in_split, (
        f"missing from prompts: {sorted(in_split - in_prompts)[:10]}; "
        f"extra: {sorted(in_prompts - in_split)[:10]}"
    )
