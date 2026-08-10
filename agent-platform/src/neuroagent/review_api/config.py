"""Paths and dataset registry for the review API."""

from __future__ import annotations

from neuroagent.datasets import (
    DATA_ROOT,
    DATASETS as AVAILABLE_DATASETS,
    DEFAULT_DATASET_VERSION,
    REPO_ROOT as _REPO_ROOT,
)

# Paths are resolved relative to this file:
# agent-platform/src/neuroagent/review_api/config.py
# parents[0] = review_api/
# parents[1] = neuroagent/
# parents[2] = src/
# parents[3] = agent-platform/
# parents[4] = medical-agents/   (repo root)
REVIEW_DATA_DIR = DATA_ROOT / "review"
ANNOTATIONS_DIR = REVIEW_DATA_DIR / "annotations"
TOOL_REVIEWS_DIR = REVIEW_DATA_DIR / "tool_reviews"

REVIEW_CONFIG_DIR = _REPO_ROOT / "agent-platform" / "config" / "review"
REVIEWER_CODES_PATH = REVIEW_CONFIG_DIR / "reviewer_codes.yaml"

# Sources for the tool catalog (existing 12-tool list + per-condition mapping).
TOOL_COSTS_PATH = _REPO_ROOT / "agent-platform" / "config" / "tools" / "costs.yaml"
CONDITIONS_YAML_PATH = (
    _REPO_ROOT / "dataset-generation" / "config" / "conditions.yaml"
)
# The clinical reviewers' per-condition guidance for each tool: their own revised
# descriptions, which are condition-specific and therefore cannot live in the one-per-tool
# `ToolMeta.description`, nor in the agent-facing schema without leaking the diagnosis.
# Review-app only — see tests/test_condition_tool_guidance.py.
CONDITION_TOOL_GUIDANCE_PATH = REVIEW_CONFIG_DIR / "condition_tool_guidance.yaml"

WEB_DIST = _REPO_ROOT / "web-review" / "dist"
