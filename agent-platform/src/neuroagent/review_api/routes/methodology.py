"""Methodology endpoint — powers the dataset showcase tab."""

from __future__ import annotations

from collections import Counter
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request, status
from neuroagent.datasets import normalize_dataset_version

from ..dependencies import current_reviewer
from ..schemas.reviewers import ReviewerCode

router = APIRouter(tags=["methodology"])


# Hand-written prose, keyed by dataset version. Edit this file to update the
# methodology copy — no template engine needed.
_METHODOLOGY_PROSE: dict[str, dict[str, Any]] = {
    "neurobench": {
        "title": "NeuroBench",
        "tagline": "A benchmark across 20 neurological conditions.",
        "overview": (
            "NeuroBench is a benchmark for tool-augmented LLM agents on "
            "neurological diagnostic reasoning. Each case is a self-contained "
            "clinical encounter — a patient profile, available tool outputs, "
            "and an expert-curated ground truth — designed to test diagnostic "
            "accuracy, workup efficiency, and clinical safety in a single shot."
        ),
        "pipeline": [
            {
                "label": "Real-case seeds",
                "icon": "Library",
                "description": (
                    "Cases anchored on de-identified case reports from PubMed Central "
                    "(CC-BY 4.0). Demographics, presentation, and key findings are "
                    "preserved to keep the case clinically realistic."
                ),
            },
            {
                "label": "Synthetic augmentation",
                "icon": "Sparkles",
                "description": (
                    "Severity variants (straightforward, moderate, diagnostic puzzle) "
                    "and red-herring inserts are added to stress-test the agent's "
                    "reasoning, while keeping pathophysiology faithful to the seed."
                ),
            },
            {
                "label": "Tool outputs",
                "icon": "Activity",
                "description": (
                    "Initial and follow-up outputs are generated for the 16 supported "
                    "modalities (MRI, EEG, ECG, labs, CSF, etc.). Reports are written "
                    "to mirror real clinical documentation in style and content."
                ),
            },
            {
                "label": "Ground truth",
                "icon": "ShieldCheck",
                "description": (
                    "Each case carries a primary diagnosis, differential, required and "
                    "contraindicated actions, key reasoning points, and red herrings. "
                    "Cases are reviewed end-to-end by a clinical neurologist."
                ),
            },
        ],
        "citation_bibtex": (
            "@article{neurobench2026,\n"
            "  title={NeuroBench: A benchmark for tool-augmented LLM agents in neurology},\n"
            "  author={Protani, Andrea and Collaborators},\n"
            "  journal={Nature Machine Intelligence},\n"
            "  year={2026}\n"
            "}"
        ),
    },
}


def _condition_breakdown(case_objects: dict) -> list[dict[str, Any]]:
    by_condition: Counter[str] = Counter()
    severity_per_condition: dict[str, Counter[str]] = {}
    for case in case_objects.values():
        condition = case.condition.value
        by_condition[condition] += 1
        severity_per_condition.setdefault(condition, Counter())[case.difficulty.value] += 1
    return [
        {
            "condition": condition,
            "count": count,
            "by_difficulty": dict(severity_per_condition[condition]),
        }
        for condition, count in by_condition.most_common()
    ]


@router.get("/datasets/{version}/methodology")
def get_methodology(
    version: str,
    request: Request,
    _reviewer: ReviewerCode = Depends(current_reviewer),
) -> dict[str, Any]:
    version = normalize_dataset_version(version)
    all_datasets = request.app.state.all_datasets
    if version not in all_datasets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dataset '{version}' not found",
        )

    case_objects = all_datasets[version][1]
    prose = _METHODOLOGY_PROSE.get(version)
    if prose is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No methodology copy registered for dataset '{version}'",
        )

    by_difficulty: Counter[str] = Counter()
    by_encounter: Counter[str] = Counter()
    pathway_depth: list[int] = []
    for case in case_objects.values():
        by_difficulty[case.difficulty.value] += 1
        by_encounter[case.encounter_type.value] += 1
        pathway_depth.append(len(case.followup_outputs or []))

    avg_depth = sum(pathway_depth) / len(pathway_depth) if pathway_depth else 0.0

    return {
        "version": version,
        "prose": prose,
        "stats": {
            "total_cases": len(case_objects),
            "conditions": len({c.condition for c in case_objects.values()}),
            "by_difficulty": dict(by_difficulty),
            "by_encounter": dict(by_encounter),
            "avg_pathway_depth": round(avg_depth, 2),
        },
        "by_condition": _condition_breakdown(case_objects),
    }
