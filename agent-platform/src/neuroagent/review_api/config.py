"""Paths and dataset registry for the review API."""

from __future__ import annotations

from pathlib import Path

# Paths are resolved relative to this file:
# agent-platform/src/neuroagent/review_api/config.py
# parents[0] = review_api/
# parents[1] = neuroagent/
# parents[2] = src/
# parents[3] = agent-platform/
# parents[4] = medical-agents/   (repo root)
_REPO_ROOT = Path(__file__).resolve().parents[4]

DATA_ROOT = _REPO_ROOT / "data"
REVIEW_DATA_DIR = DATA_ROOT / "review"
ANNOTATIONS_DIR = REVIEW_DATA_DIR / "annotations"

REVIEW_CONFIG_DIR = _REPO_ROOT / "agent-platform" / "config" / "review"
REVIEWER_CODES_PATH = REVIEW_CONFIG_DIR / "reviewer_codes.yaml"

WEB_DIST = _REPO_ROOT / "web-review" / "dist"


AVAILABLE_DATASETS: dict[str, dict[str, str | Path]] = {
    "v3": {
        "path": DATA_ROOT / "neurobench_v3",
        "name": "NeuroBench v3",
        "description": "200 cases (v1+v2 combined) with realistic/stripped tool outputs",
    },
    "v4": {
        "path": DATA_ROOT / "neurobench_v4",
        "name": "NeuroBench v4",
        "description": "200 cases with 12-tool schema and cost tracking (v3 migrated)",
    },
    "v5": {
        "path": DATA_ROOT / "neurobench_v5",
        "name": "NeuroBench v5",
        "description": "516 cases across 20 conditions (10 new + 10 v4 carryovers)",
    },
}

DEFAULT_DATASET_VERSION = "v5"
