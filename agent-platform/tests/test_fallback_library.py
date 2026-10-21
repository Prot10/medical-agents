"""The benchmark-level fallback library answers every legal order the case cannot, identically in every case."""

from __future__ import annotations

from pathlib import Path

import pytest

from neuroagent.datasets import load_dataset
from neuroagent.harness.environment import NeuroBenchEnvironment
from neuroagent.tools.fallback_library import OUTPUT_MODELS, default_library
from neuroagent.tools.mock_server import MockServer
from neuroagent.tools.tool_registry import ToolRegistry
from neuroagent_schemas import ToolAction

ROOT = Path(__file__).resolve().parents[2]


def _probes():
    registry = ToolRegistry.create_default_registry(None)
    for name, tool in registry.tools.items():
        props = tool.parameter_schema["properties"]
        required = tool.parameter_schema.get("required", [])
        base = {k: "probe" for k in required if props[k].get("type") == "string" and "enum" not in props[k]}
        scalar_enums = [k for k in props if "enum" in props[k]]
        if scalar_enums:
            key = scalar_enums[0]
            for value in props[key]["enum"]:
                yield name, {**base, key: value}
        else:
            yield name, base
        for key, prop in props.items():
            members = prop.get("items", {}).get("enum") if prop.get("type") == "array" else None
            if members:
                yield name, {**base, key: members[:3]}


def test_library_loads_and_covers_every_tool():
    library = default_library()
    assert set(library.tools) == set(OUTPUT_MODELS)
    assert library.status == "draft"  # physician review pending


def test_every_legal_order_is_answered_in_every_case():
    _, cases = load_dataset(ROOT / "data" / "neurobench")
    probes = list(_probes())
    unanswered = []
    for case in cases.values():
        server = MockServer(case)
        for tool, arguments in probes:
            result = server.get_output(tool, arguments)
            if not result.success:
                unanswered.append((case.case_id, tool, arguments))
    assert not unanswered, unanswered[:10]


def test_library_result_is_flagged_and_reads_as_the_ordered_study():
    _, cases = load_dataset(ROOT / "data" / "neurobench")
    case = next(iter(cases.values()))
    env = NeuroBenchEnvironment(case)
    # No case authors a throat swab: the answer can only come from the library.
    result = env.execute(ToolAction(tool_name="order_microbiology", arguments={"clinical_context": "x", "specimen": "throat_swab"}))
    assert result.success and result.from_fallback and result.library
    assert result.output["specimen"] == "throat_swab" and result.cost_usd and result.cost_usd > 0
    study = default_library().resolve("order_body_imaging", {"study": "mediastinum_CT"}).model_dump()
    assert "mediastin" in (study["region"] + study["impression"]).lower() and study["modality"].upper().startswith("CT")
    labs = default_library().resolve("interpret_labs", {"panels": ["CBC", "Vitamin B12"]}).model_dump()
    assert set(labs["panels"]) == {"CBC", "Vitamin B12"} and len(labs["panels"]["CBC"]) >= 5
    assert all(not v["is_abnormal"] for rows in labs["panels"].values() for v in rows)
    csf = default_library().resolve("analyze_csf", {"special_tests": ["HSV PCR", "oligoclonal bands"]}).model_dump()
    assert list(csf["special_tests"]) == ["HSV_PCR", "oligoclonal_bands"]
    tissue = default_library().resolve("obtain_tissue_diagnosis", {"procedure": "stereotactic_biopsy", "molecular_assays": ["IDH1_IHC"]}).model_dump()
    assert tissue["procedure"] and list(tissue["molecular_findings"]) == ["IDH1_IHC"]


def test_body_imaging_guard_reads_region_and_modality():
    from neuroagent_schemas.tool_outputs import BodyImagingReport

    spine_mri = BodyImagingReport(region="cervical and thoracic spine", modality="MRI", impression="Normal.")
    assert MockServer._body_study_matches("spine_MRI", spine_mri)
    assert not MockServer._body_study_matches("mediastinum_CT", spine_mri)
    assert not MockServer._body_study_matches("spine_CT", spine_mri)
    testes = BodyImagingReport(region="testes", modality="ultrasound", impression="Normal.")
    assert MockServer._body_study_matches("testicular_ultrasound", testes)
    assert MockServer._body_study_matches("chest_CT", BodyImagingReport(region="thorax", modality="CT", impression="."))
    assert MockServer._body_study_matches("pelvis_abdomen_MRI", BodyImagingReport(region="pelvic", modality="MRI", impression="."))
    prose = BodyImagingReport(region="", modality="cross-sectional", impression="Normal.")
    assert MockServer._body_study_matches("chest_CTA", prose)  # prose report: not adjudicated
