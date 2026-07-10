"""What `diagnostic_accuracy_top1` is allowed to call correct.

The metric used to search the agent's entire final response for the ground-truth diagnosis.
A response that concluded the wrong disease but named the right one in its differential — or
merely shared 70% of its long words — scored a correct top-1. On the 1000 gold trajectories
that accepted 1898 wrong-condition responses; scoring the stated diagnosis instead accepts
338, and the remainder are dual diagnoses whose stated span genuinely names both diseases.

`top3` had a worse bug: it credited an agent for naming the *ground truth's* differential —
the diagnoses that are, by construction, wrong.
"""

from __future__ import annotations

import pytest

from neuroagent_schemas.enums import Likelihood
from neuroagent_schemas.evaluation import DifferentialDx, GroundTruth

from neuroagent.agent.reasoning import AgentTrace
from neuroagent.evaluation.metrics import (
    MetricsCalculator,
    diagnosis_head,
    stated_differential,
    stated_primary_diagnosis,
)

ALS = "Amyotrophic lateral sclerosis (ALS), bulbar-onset"


def _ground_truth(primary: str = ALS) -> GroundTruth:
    return GroundTruth(
        primary_diagnosis=primary,
        icd_code="G12.21",
        differential=[
            DifferentialDx(diagnosis="Cervical spondylotic myelopathy", likelihood=Likelihood.LOW),
            DifferentialDx(diagnosis="Multifocal motor neuropathy", likelihood=Likelihood.LOW),
        ],
    )


def _trace(final_response: str) -> AgentTrace:
    trace = AgentTrace(case_id="ALS-M01")
    trace.set_final_response(final_response)
    return trace


def _score(response: str, gt: GroundTruth | None = None):
    return MetricsCalculator().compute_all(_trace(response), gt or _ground_truth())


CONCLUDES_ALS = (
    "### Primary Diagnosis\n"
    "Amyotrophic lateral sclerosis (ALS), bulbar-onset (Confidence: 0.78)\n\n"
    "### Differential Diagnoses\n"
    "1. Cervical myelopathy — cord signal is preserved\n"
)

CONCLUDES_MS_DISCUSSES_ALS = (
    "### Primary Diagnosis\n"
    "Multiple sclerosis, relapsing-remitting type (Confidence: 0.72)\n\n"
    "### Differential Diagnoses\n"
    "1. Amyotrophic lateral sclerosis — bulbar onset remains possible\n\n"
    "### Key Evidence\n"
    "- Amyotrophic lateral sclerosis could not be fully excluded on this workup\n"
)


class TestStatedDiagnosisExtraction:
    def test_reads_the_mandated_section(self):
        assert stated_primary_diagnosis(CONCLUDES_ALS) == ALS

    def test_strips_the_confidence_annotation(self):
        assert "confidence" not in stated_primary_diagnosis(CONCLUDES_ALS).lower()

    @pytest.mark.parametrize(
        "response",
        [
            "**Primary Diagnosis:** Amyotrophic lateral sclerosis\n",
            "## Final Diagnosis\nAmyotrophic lateral sclerosis\n",
            "Diagnosis: Amyotrophic lateral sclerosis\n",
        ],
    )
    def test_accepts_cosmetic_variants_of_the_format(self, response: str):
        assert stated_primary_diagnosis(response) == "Amyotrophic lateral sclerosis"

    def test_reasoning_prose_is_not_a_diagnosis_statement(self):
        """`<think>` blocks say "Diagnosis is confirmed:" long before the agent concludes."""
        response = (
            "<think>\nDiagnosis is confirmed: the CTA shows a ruptured aneurysm\n</think>\n\n"
            "### Primary Diagnosis\nAneurysmal subarachnoid hemorrhage (Confidence: 0.9)\n"
        )
        assert stated_primary_diagnosis(response) == "Aneurysmal subarachnoid hemorrhage"

    def test_a_response_without_a_diagnosis_section_states_nothing(self):
        assert stated_primary_diagnosis("The workup is consistent with motor neuron disease.") is None

    def test_reads_the_agents_own_ranked_alternatives(self):
        response = (
            "### Primary Diagnosis\nALS\n\n"
            "### Differential Diagnoses\n"
            "1. Cervical myelopathy — spondylotic change\n"
            "2. Multifocal motor neuropathy / CIDP — normal sensory NCS\n"
            "3. Inflammatory myopathy — CK only mildly raised\n"
            "4. Kennedy disease\n\n"
            "### Key Evidence\n- Mixed UMN and LMN signs\n"
        )
        assert stated_differential(response) == [
            "Cervical myelopathy",
            "Multifocal motor neuropathy / CIDP",
            "Inflammatory myopathy",
        ]


class TestDiagnosisHead:
    @pytest.mark.parametrize(
        "diagnosis,expected",
        [
            (ALS, "amyotrophic lateral sclerosis"),
            ("Multiple sclerosis, relapsing-remitting type", "multiple sclerosis"),
            ("Migraine with aura (ICHD-3 1.2.1) — misdiagnosed as TIA", "migraine with aura"),
        ],
    )
    def test_strips_abbreviation_subtype_and_commentary(self, diagnosis: str, expected: str):
        assert diagnosis_head(diagnosis) == expected


class TestTop1ScoresTheConclusion:
    def test_the_right_conclusion_is_correct(self):
        assert _score(CONCLUDES_ALS).diagnostic_accuracy_top1 is True

    def test_naming_the_disease_without_the_subtype_is_correct(self):
        response = "### Primary Diagnosis\nAmyotrophic lateral sclerosis (Confidence: 0.7)\n"
        assert _score(response).diagnostic_accuracy_top1 is True

    def test_the_wrong_conclusion_is_wrong_however_much_it_discusses_the_right_one(self):
        """The regression this whole module exists for."""
        assert _score(CONCLUDES_MS_DISCUSSES_ALS).diagnostic_accuracy_top1 is False

    def test_a_different_disease_is_wrong(self):
        response = "### Primary Diagnosis\nMyasthenia gravis, generalised (Confidence: 0.8)\n"
        assert _score(response).diagnostic_accuracy_top1 is False

    def test_commentary_after_an_em_dash_does_not_make_a_correct_answer_wrong(self):
        gt = _ground_truth("Migraine with aphasic aura (ICHD-3 1.2.1) — misdiagnosed as TIA")
        response = "### Primary Diagnosis\nMigraine with aphasic aura (Confidence: 0.8)\n"
        assert _score(response, gt).diagnostic_accuracy_top1 is True

    def test_punctuation_does_not_make_a_correct_answer_wrong(self):
        gt = _ground_truth("Alzheimer's disease (mild dementia, amnestic presentation)")
        response = "### Primary Diagnosis\nAlzheimer's disease, mild dementia, amnestic\n"
        assert _score(response, gt).diagnostic_accuracy_top1 is True

    def test_without_a_diagnosis_section_the_diagnosis_must_appear_verbatim(self):
        gt = _ground_truth("Multiple sclerosis, relapsing-remitting type")
        near_miss = "The findings are consistent with sclerosis of multiple central lesions."
        verbatim = "I conclude this is multiple sclerosis, relapsing-remitting type."
        assert _score(near_miss, gt).diagnostic_accuracy_top1 is False
        assert _score(verbatim, gt).diagnostic_accuracy_top1 is True


class TestTop3RanksTheAgentsDifferential:
    def test_the_right_diagnosis_in_the_agents_differential_counts(self):
        assert _score(CONCLUDES_MS_DISCUSSES_ALS).diagnostic_accuracy_top3 is True

    def test_a_correct_top1_is_a_correct_top3(self):
        assert _score(CONCLUDES_ALS).diagnostic_accuracy_top3 is True

    def test_naming_the_ground_truths_distractors_earns_nothing(self):
        """These alternatives are wrong by construction; listing them is not a near-miss."""
        response = (
            "### Primary Diagnosis\nMyasthenia gravis (Confidence: 0.6)\n\n"
            "### Differential Diagnoses\n"
            "1. Cervical spondylotic myelopathy\n"
            "2. Multifocal motor neuropathy\n"
        )
        assert _score(response).diagnostic_accuracy_top3 is False

    def test_below_the_top_three_does_not_count(self):
        response = (
            "### Primary Diagnosis\nMyasthenia gravis (Confidence: 0.6)\n\n"
            "### Differential Diagnoses\n"
            "1. Cervical myelopathy\n2. Inclusion body myositis\n3. Kennedy disease\n"
            "4. Amyotrophic lateral sclerosis\n"
        )
        assert _score(response).diagnostic_accuracy_top3 is False
