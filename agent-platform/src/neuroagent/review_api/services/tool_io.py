"""Per-tool I/O schemas for the Tool Catalog view.

The review_api ships isolated from ``agent-platform/src/neuroagent/tools/`` —
the deploy script only rsyncs ``review_api/`` and the workspace ``__init__.py``.
So the agent-facing ``parameter_schema`` dicts that live next to each tool's
``execute()`` method aren't importable here. We mirror them verbatim below.

**KEEP IN SYNC** with ``agent-platform/src/neuroagent/tools/*.py``. The truth is
the tool class's ``parameter_schema`` attribute, and
``tests/test_tool_io_schemas.py::test_tool_io_schemas_match`` diffs this mirror
against the real classes so drift fails CI.

That test exists because the mirror *did* drift, silently, and it mattered. The
catchall tools' vocabularies are generated from ``costs.yaml`` in the real tools
(see ``tools/vocabulary.py``); commit 9a0636c moved them onto that single source
but only renamed ``imaging_type`` -> ``modality`` here, leaving the stale enum
lists behind. Between 2026-07-19 and 2026-07-27 the clinical reviewers therefore
assessed the tool catalog against 9 of 21 specialized tests, 6 of 12 imaging
modalities and 4 of 6 cardiac monitors, and reported as "missing" six studies the
agent could already order. The vocabulary-bearing parameters are consequently no
longer written out here at all: they are injected from ``costs.yaml``, which the
review_api already loads, so this file cannot go stale on them again.

Return shapes are derived from the Pydantic models in
``neuroagent_schemas.tool_outputs`` — those ARE shipped, so no mirror is needed
for outputs.
"""

from __future__ import annotations

import copy
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any, get_args, get_origin

import yaml
from neuroagent_schemas.case import _TOOL_OUTPUT_MODEL
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from ..config import TOOL_COSTS_PATH

logger = logging.getLogger(__name__)

# --- Vocabularies derived from costs.yaml -----------------------------
#
# `(tool, parameter) -> costs.yaml block` for every parameter whose enum is a
# closed vocabulary priced in costs.yaml. Mirrors tools/vocabulary.py, which the
# real tool classes use; kept separate only because tools/ is not shipped to the
# review VPS. Sorted, so enum order matches the real schema exactly.
_COSTS_DERIVED_ENUMS: dict[tuple[str, str], tuple[str, str]] = {
    ("order_advanced_imaging", "modality"): ("order_advanced_imaging", "by_type"),
    ("order_specialized_test", "test_type"): ("order_specialized_test", "by_type"),
    ("order_cardiac_monitoring", "monitor_type"): ("order_cardiac_monitoring", "by_type"),
    # These three were still written out by hand in their tool class as well, so both copies
    # could drift from costs.yaml independently. Now neither does: `exercise_echo` became
    # orderable, catalogued and scoreable the moment it was priced.
    ("order_echocardiogram", "echo_type"): ("order_echocardiogram", "by_type"),
    ("analyze_eeg", "eeg_type"): ("analyze_eeg", "by_type"),
    # `protocols`, not `by_type`: protocol selection does not change what is billed, so every
    # row is priced at 0 — but the block is still the source of the enum.
    ("analyze_brain_mri", "protocol"): ("analyze_brain_mri", "protocols"),
    # Array-valued: the enum belongs on `items`, and spelling aliases priced in costs.yaml
    # are collapsed so one assay is advertised once (see tools/vocabulary.py).
    ("interpret_labs", "panels"): ("interpret_labs", "by_panel"),
    ("analyze_csf", "special_tests"): ("analyze_csf", "by_special_test"),
    # Scalar, priced at 0 like the MRI protocols (October 2026 review: shunt tap / EVD sample).
    ("analyze_csf", "source"): ("analyze_csf", "sources"),
    # Tools added after the July 2026 clinical tool review.
    ("order_body_imaging", "study"): ("order_body_imaging", "by_type"),
    ("order_microbiology", "specimen"): ("order_microbiology", "by_type"),
    ("obtain_tissue_diagnosis", "procedure"): ("obtain_tissue_diagnosis", "by_type"),
    ("obtain_tissue_diagnosis", "molecular_assays"): (
        "obtain_tissue_diagnosis",
        "by_molecular_assay",
    ),
    ("perform_clinical_assessment", "assessment_type"): (
        "perform_clinical_assessment",
        "by_type",
    ),
    # Scalar, priced at 0 (24 Oct 2026, NPH: baseline vs post-tap reassessment).
    ("perform_clinical_assessment", "timing"): ("perform_clinical_assessment", "timings"),
}

# Array-valued parameters: the enum sits on `items`, and their vocabularies carry spelling
# aliases at identical prices (the 600 cases were authored with free text), so one assay is
# advertised once. Mirrors tools/vocabulary.py::normalize_analyte / _canonical_analytes,
# duplicated here only because tools/ is not shipped to the review VPS.
_ARRAY_VALUED: frozenset[tuple[str, str]] = frozenset(
    {
        ("interpret_labs", "panels"),
        ("analyze_csf", "special_tests"),
        ("obtain_tissue_diagnosis", "molecular_assays"),
    }
)


# Mirror of tools/vocabulary.py::_ANALYTE_SYNONYMS — distinct *names* for one assay, which
# punctuation folding cannot reconcile. Duplicated here only because tools/ is not shipped to
# the review VPS; tests/test_tool_io_schemas.py fails if the two lists disagree.
_ANALYTE_SYNONYMS: dict[str, str] = {
    "syphilis": "RPR",
    "lft": "LFTs",
    "lipid": "lipid_panel",
    "lipids": "lipid_panel",
    "ua": "urinalysis",
    "paraneoplastic": "paraneoplastic_panel",
    "paraneoplastic_antibodies": "paraneoplastic_panel",
    "autoimmune_encephalitis": "autoimmune_encephalitis_panel",
    "inflammatory": "inflammatory_markers",
    "esr_crp": "inflammatory_markers",
    "toxicology": "tox_screen",
    "drug_screen": "tox_screen",
    "adamts13_activity": "ADAMTS13",
    "complement_c3/c4": "complement",
    "smear": "peripheral smear",
    "blood_cultures_x3": "blood_cultures",
    # October 2026 review (VASC-DEM): 140 case actions said `B12`, 62 `vitamin_B12`, priced as
    # two rows that did not compare equal. One assay; the named spelling is advertised.
    "b12": "vitamin_B12",
}


def _canonical_analytes(names: list[str]) -> list[str]:
    """Collapse aliases to one advertised name per assay, snake_case preferred."""
    def fold(value: str) -> str:
        return value.strip().lower().replace(" ", "_").replace("-", "_")

    candidates: dict[str, set[str]] = {}
    for name in names:
        display = _ANALYTE_SYNONYMS.get(fold(name), name)
        candidates.setdefault(fold(display), set()).add(display)
    return sorted(
        min(group, key=lambda d: (" " in d, "-" in d, d)) for group in candidates.values()
    )


@lru_cache(maxsize=4)
def _load_tool_costs(costs_path: Path = TOOL_COSTS_PATH) -> dict[str, Any]:
    if not costs_path.exists():  # pragma: no cover — misconfiguration
        logger.warning("Tool costs config not found at %s", costs_path)
        return {}
    with open(costs_path) as f:
        return (yaml.safe_load(f) or {}).get("tools", {})


def _vocabulary(tool_name: str, parameter: str) -> list[str] | None:
    """The enum for a costs-derived parameter, or None if not one."""
    block = _COSTS_DERIVED_ENUMS.get((tool_name, parameter))
    if block is None:
        return None
    tool_block, key = block
    values = list(_load_tool_costs().get(tool_block, {}).get(key, {}))
    if (tool_name, parameter) in _ARRAY_VALUED:
        return _canonical_analytes(values)
    return sorted(values)


# --- Parameter schemas (verbatim mirror of tools/*.py) ----------------
#
# Parameters listed in `_COSTS_DERIVED_ENUMS` intentionally carry no `enum` key
# here — `parameters_for()` injects it from costs.yaml.

_TOOL_PARAMETERS: dict[str, dict[str, Any]] = {
    "analyze_brain_mri": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context and indication for the MRI.",
            },
            "protocol": {
                "type": "string",
                "description": (
                    "MRI protocol to use. 'epilepsy': thin coronal hippocampal cuts (ILAE HARNESS-MRI). "
                    "'stroke': DWI emphasis + MRA. 'tumor': includes perfusion-weighted sequences. "
                    "'ms': sagittal FLAIR + post-contrast T1. 'dementia': volumetric with hippocampal assessment. "
                    "'orbits': fat-suppressed thin coronal and axial sections of the orbits and optic nerves. "
                    "'pituitary': thin sagittal and coronal sections of the sella. "
                    "'standard': general brain screen."
                ),
            },
            "contrast": {
                "type": "boolean",
                # Gadolinium is given on an indication, not by default (ACR Manual on Contrast
                # Media): an order that does not ask for it is a non-contrast study, as the
                # scorer and the cost model already read it (24 Oct 2026).
                "default": False,
                "description": "Whether gadolinium contrast is given.",
            },
        },
        "required": ["clinical_context"],
    },
    "analyze_eeg": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for the EEG interpretation.",
            },
            "eeg_type": {
                "type": "string",
                "description": (
                    "Type of EEG study. 'routine': 20-40 min outpatient. "
                    "'ambulatory': 24-72 hr home monitoring. "
                    "'video': inpatient video-EEG monitoring with time-locked video of the events. "
                    "'continuous_icu': continuous EEG in the intensive care unit."
                ),
                "default": "routine",
            },
            "patient_age": {
                "type": "integer",
                "description": "Patient age in years.",
            },
            "focus_areas": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Specific areas or patterns to focus on.",
            },
        },
        "required": ["clinical_context"],
    },
    "analyze_ecg": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for the ECG interpretation.",
            },
        },
        "required": ["clinical_context"],
    },
    "interpret_labs": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for lab interpretation.",
            },
            "panels": {
                "type": "array",
                "description": (
                    "Individual assays or named panels to interpret. Each entry is billed "
                    "separately, from EUR 5 (glucose, sodium) to EUR 2300 "
                    "(`paraneoplastic_panel`). Prefer the specific assay the question needs."
                ),
            },
            "patient_age": {
                "type": "integer",
                "description": "Patient age in years.",
            },
            "patient_sex": {
                "type": "string",
                "description": "Patient sex (e.g., male, female).",
            },
        },
        "required": ["clinical_context"],
    },
    "analyze_csf": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical context for CSF interpretation.",
            },
            "special_tests": {
                "type": "array",
                "description": (
                    "Additional CSF assays to run, billed separately from the EUR 230 "
                    "lumbar puncture: from EUR 18 (IgG index) to EUR 1840 (autoimmune "
                    "panel). Each entry is one assay; order the ones the question calls for."
                ),
            },
            "source": {
                "type": "string",
                "description": (
                    "Where the CSF is drawn. 'lumbar_puncture' (default). 'shunt_tap': "
                    "aspiration from the reservoir of an implanted ventricular shunt. "
                    "'external_ventricular_drain': a sample "
                    "from the drain's sampling port in a patient with an EVD in place. "
                    "'lumbar_drain': extended lumbar drainage through an indwelling catheter "
                    "(about 10 mL/h over 72 hours)."
                ),
                "default": "lumbar_puncture",
            },
        },
        "required": ["clinical_context"],
    },
    "order_ct_scan": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the CT scan.",
            },
            "contrast": {
                "type": "boolean",
                "description": "Whether IV contrast is needed.",
                "default": False,
            },
            "angiography": {
                "type": "boolean",
                "description": "Whether CT angiography (CTA) of the cervical and intracranial arteries is added.",
                "default": False,
            },
        },
        "required": ["clinical_context"],
    },
    "order_echocardiogram": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the echocardiogram.",
            },
            "echo_type": {
                "type": "string",
                "description": (
                    "Type of echocardiogram. 'TTE': transthoracic — the standard study, "
                    "non-invasive. 'TEE': transesophageal — close views of the atria, the "
                    "left atrial appendage, the valves and the thoracic aorta that the "
                    "transthoracic window cannot give. 'bubble_study': agitated-saline "
                    "contrast for a right-to-left shunt. 'exercise_echo': imaging during or "
                    "immediately after graded exercise, standing, sitting or semi-supine — "
                    "the answer is a provoked outflow-tract gradient or an exercise-induced "
                    "wall-motion or rhythm change that the resting study cannot show."
                ),
                "default": "TTE",
            },
        },
        "required": ["clinical_context"],
    },
    "order_cardiac_monitoring": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for cardiac monitoring.",
            },
            "monitor_type": {
                "type": "string",
                "description": (
                    "Type of monitoring. 'holter_24h'/'holter_48h': continuous recording. "
                    "'event_monitor_14d'/'event_monitor_30d': patient-activated, captures "
                    "infrequent events. 'implantable_loop_recorder': months to years of "
                    "monitoring. "
                    "'telemetry': inpatient continuous monitoring. 'device_interrogation': "
                    "the stored rhythm diagnostics of a pacemaker, ICD or loop recorder already "
                    "implanted (atrial high-rate episodes, AF burden)."
                ),
                "default": "holter_24h",
            },
        },
        "required": ["clinical_context"],
    },
    "order_advanced_imaging": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the advanced imaging study.",
            },
            "modality": {
                "type": "string",
                "description": (
                    "Imaging modality. 'amyloid_PET'/'tau_PET': cerebral amyloid / tau deposition. "
                    "'FDG_PET': cerebral glucose metabolism; normal grey matter takes up FDG "
                    "avidly. 'amino_acid_PET': 11C-methionine or 18F-FET — amino-acid transport, "
                    "low in normal cortex. 'cardiac_FDG_PET': myocardial FDG uptake after dietary "
                    "suppression of myocardial glucose uptake — a different study from the brain "
                    "scan, not the same scan read differently. 'DaTscan': striatal dopamine "
                    "transporter binding. 'MIBG_scan': cardiac sympathetic (postganglionic) "
                    "innervation, as the heart-to-mediastinum ratio. 'perfusion_MRI': cerebral "
                    "blood flow and rCBV. 'CT_perfusion': cerebral blood flow, blood volume and "
                    "transit-time maps, with automated volumes of reduced flow. 'MR_spectroscopy': "
                    "the brain metabolite spectrum (NAA, choline, creatine, lactate, lipids, "
                    "myo-inositol). 'MR_angiography'/'MR_venography': arterial / venous sinus "
                    "imaging. 'cardiac_MRI': cardiac function and myocardial tissue "
                    "characterisation, with T1/T2 mapping and late gadolinium enhancement. "
                    "'coronary_CTA': non-invasive coronary anatomy. 'coronary_angiography': "
                    "invasive catheter coronary angiography; an angiographic finding alone does "
                    "not establish the cause of a symptom. 'carotid_duplex': extracranial carotid "
                    "and vertebral flow velocities and plaque. 'transcranial_doppler': "
                    "intracranial arterial flow velocities. 'functional_MRI': BOLD motor and "
                    "language mapping and hemispheric language lateralisation. 'DTI_tractography': "
                    "diffusion tractography of the corticospinal tract, arcuate fasciculus and "
                    "optic radiations. 'whole_body_FDG_PET': whole-body 18F-FDG PET/CT, skull base "
                    "to mid-thigh (a different acquisition from the cerebral 'FDG_PET')."
                ),
            },
        },
        "required": ["clinical_context", "modality"],
    },
    "order_specialized_test": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the specialized test.",
            },
            # The enum is the fixed test types plus one `genetic_panel:<panel>` member per
            # priced panel, both filled from costs.yaml by parameters_for().
            "test_type": {
                "type": "string",
                "description": (
                    "Type of specialized test; targeted gene panels are 'genetic_panel:<panel>'. "
                    "'emg_ncs': nerve conduction + needle EMG. 'emg_single_fiber': jitter and "
                    "blocking of single muscle fibre pairs. 'repetitive_nerve_stimulation': "
                    "decrement or increment of the compound muscle action potential on repeated "
                    "stimulation. 'respiratory_function': FVC, MIP/MEP, NIF. 'neuropsych_battery': "
                    "comprehensive cognitive testing. 'vep'/'ssep'/'baep': evoked potentials. "
                    "'tilt_table': head-up tilt with continuous beat-to-beat blood pressure and "
                    "heart rate. 'optical_coherence_tomography': retinal nerve fibre and ganglion "
                    "cell layer thickness. 'fluorescein_angiography': fundus fluorescein "
                    "angiography — retinal arterial and venous filling, occlusions and vessel-wall "
                    "leakage. 'audiometry': pure-tone and speech audiometry with tympanometry. "
                    "'speech_language_evaluation': speech-language pathology assessment of motor "
                    "speech, grammar, naming, repetition and comprehension, with the profile of "
                    "the deficit (a full cognitive battery is 'neuropsych_battery'). "
                    "'electrophysiology_study': invasive EP study — HV interval, sinus node "
                    "recovery, programmed stimulation for inducible arrhythmia, accessory-pathway "
                    "refractory period. 'sodium_channel_blocker_challenge': ajmaline, flecainide "
                    "or procainamide under 12-lead ECG with high precordial leads, reporting "
                    "whether a type 1 Brugada pattern appears. "
                    "'genetic_panel:inherited_arrhythmia': long QT, Brugada and CPVT genes; "
                    "'genetic_panel:cardiomyopathy': arrhythmogenic, hypertrophic, dilated and "
                    "laminopathy genes. 'olfactory_test': quantitative smell test (UPSIT or "
                    "Sniffin' Sticks) scored against age and sex norms."
                ),
            },
        },
        "required": ["clinical_context", "test_type"],
    },
    # --- Tools added after the July 2026 clinical tool review -----------------------------
    # Generated from the tool classes rather than hand-written; kept in sync by
    # tests/test_tool_io_schemas.py.
    "order_body_imaging": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the study.",
            },
            "study": {
                "type": "string",
                "description": (
                    "Region and modality. 'pelvis_abdomen_CT'/'_MRI'/'_ultrasound': the abdominal "
                    "and pelvic organs and vessels. 'testicular_ultrasound': scrotal ultrasound of "
                    "both testes. 'chest_CT': lung parenchyma, pleura and mediastinum. "
                    "'chest_CTA': CT angiography of the pulmonary arteries and the thoracic aorta. "
                    "'chest_abdomen_pelvis_CT': chest, abdomen and pelvis in one acquisition. "
                    "'mediastinum_CT'/'_MRI': dedicated mediastinal imaging. 'spine_MRI'/'_CT': "
                    "spinal cord, nerve roots, vertebrae and epidural space. "
                    "'peripheral_nerve_MRI'/'_ultrasound': calibre, signal and enhancement of "
                    "nerve roots, plexus and peripheral nerves. 'lower_extremity_venous_duplex': "
                    "compression and Doppler ultrasound of the leg veins. 'chest_xray': two-view "
                    "chest radiograph. 'temporal_artery_ultrasound': wall thickness and lumen of "
                    "the superficial temporal arteries."
                ),
            },
            "contrast": {
                "type": "boolean",
                "description": "Whether IV contrast is needed.",
                "default": False,
            },
        },
        "required": ["clinical_context", "study"],
    },
    "order_microbiology": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the specimen.",
            },
            "specimen": {
                "type": "string",
                "description": (
                    "What to sample. 'blood_culture': two sets, with susceptibility testing. "
                    "'whole_blood_pcr': EDTA whole-blood multiplex PCR for bacterial and viral "
                    "pathogens. 'throat_swab': pharyngeal swab for culture, antigen testing and "
                    "PCR. 'urine': urinalysis and culture. 'ascitic_fluid': diagnostic "
                    "paracentesis with PMN count, protein and culture. 'sputum': Gram stain and "
                    "culture (acid-fast smear and mycobacterial culture on request). 'stool': C. "
                    "difficile toxin PCR. 'wound_swab': culture of a wound or ulcer. "
                    "'brain_aspirate': Gram stain and aerobic and anaerobic culture of material "
                    "aspirated from a brain lesion; the aspiration itself is ordered through "
                    "obtain_tissue_diagnosis. 'tracheal_aspirate': Gram stain and culture of a "
                    "lower-airway sample aspirated through the endotracheal tube of a ventilated "
                    "patient."
                ),
            },
            "tests": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Assays to run on the specimen (e.g. culture, gram_stain, "
                    "susceptibility, pcr, cell_count, protein)."
                ),
            },
            "before_antimicrobials": {
                "type": "boolean",
                "description": (
                    "Whether the specimen is being taken before the first antimicrobial "
                    "dose. Yield of culture, stain and PCR falls sharply once treatment "
                    "has started, so the report states this either way."
                ),
                "default": True,
            },
        },
        "required": ["clinical_context", "specimen"],
    },
    "obtain_tissue_diagnosis": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication, and the lesion's site and appearance.",
            },
            "procedure": {
                "type": "string",
                "description": (
                    "How tissue is obtained. 'resection': surgical resection, which is also "
                    "therapeutic. 'stereotactic_biopsy': needle biopsy with serial samples along a "
                    "stereotactic trajectory. 'lymph_node_biopsy': endobronchial needle aspiration "
                    "or surgical nodal sampling. 'temporal_artery_biopsy': a segment of the "
                    "superficial temporal artery. 'open_biopsy': open surgical biopsy through a "
                    "laminectomy or craniotomy, without resection."
                ),
            },
            "site": {
                "type": "string",
                "description": "Anatomical target of the procedure.",
            },
            "molecular_assays": {
                "type": "array",
                "description": (
                    "Assays to run on the specimen. 'IDH1_IHC': IDH1 R132H immunohistochemistry. "
                    "'ATRX_IHC': ATRX nuclear expression. 'IDH1_IDH2_sequencing': IDH1 and IDH2 "
                    "hotspot sequencing. '1p_19q_codeletion': whole-arm 1p/19q codeletion. "
                    "'CDKN2A_B_deletion': homozygous CDKN2A/B deletion. 'TERT_promoter': TERT "
                    "promoter mutation. 'EGFR_amplification': EGFR gene amplification. "
                    "'chr7_gain_chr10_loss': combined gain of chromosome 7 and loss of chromosome "
                    "10. 'H3K27_status': H3 K27M mutation and H3K27me3 loss. 'MGMT_methylation': "
                    "MGMT promoter methylation by PCR, pyrosequencing or array (not "
                    "immunohistochemistry). 'BRAF_V600': BRAF V600E mutation. 'CD20_IHC': B-cell "
                    "lineage. 'EBER_ISH': Epstein-Barr virus-encoded RNA. 'SOX10_IHC' and "
                    "'Melan_A_HMB45_IHC': melanocytic markers. 'chromogranin_A_synaptophysin_IHC': "
                    "neuroendocrine markers. 'PAX8_IHC', 'TTF1_IHC', 'thyroglobulin_IHC': "
                    "epithelial lineage markers (renal or Mullerian, lung, thyroid). "
                    "'H3G34_status': H3 G34 mutation. 'DNA_methylation_profiling': genome-wide DNA "
                    "methylation classification."
                ),
            },
        },
        "required": ["clinical_context", "procedure"],
    },
    "perform_clinical_assessment": {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "What the assessment is meant to establish or exclude.",
            },
            "assessment_type": {
                "type": "string",
                "description": (
                    "'cognitive_screen': MoCA / MMSE at the bedside, with informant history (a "
                    "full battery is order_specialized_test{neuropsych_battery}). "
                    "'structured_headache_history_ichd3': the headache history and its "
                    "accompanying neurological symptoms, taken against ICHD-3 criteria — onset, "
                    "evolution, duration, red flags. 'gait_and_balance_timed': Timed Up and Go and "
                    "timed walk test. 'functional_neuro_signs': Hoover's sign, entrainment and the "
                    "other positive functional neurological signs. 'performance_status': Karnofsky "
                    "and ECOG scored at the visit. 'orthostatic_blood_pressure': blood pressure "
                    "and heart rate supine and at 1 and 3 minutes of active standing. "
                    "'levodopa_challenge': MDS-UPDRS part III in the OFF state and again at peak "
                    "effect of a supra-threshold levodopa dose, with the percent improvement; one "
                    "assessment that reports both states."
                ),
            },
            "timing": {
                "type": "string",
                "description": (
                    "When the assessment is made relative to an intervention whose effect it "
                    "measures. 'baseline' (default): before it. 'post_intervention': the same "
                    "assessment repeated after it, to be compared with the baseline."
                ),
                "default": "baseline",
            },
        },
        "required": ["clinical_context", "assessment_type"],
    },
    "search_medical_literature": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Clinical question or search query.",
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of results to return.",
                "default": 5,
            },
        },
        "required": ["query"],
    },
    "check_drug_interactions": {
        "type": "object",
        "properties": {
            "drug": {
                "type": "string",
                "description": "The proposed medication to check.",
            },
            "current_medications": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of patient's current medications.",
            },
            "patient_conditions": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of patient's medical conditions.",
            },
        },
        "required": ["drug"],
    },
}


# --- Output field summary (derived from Pydantic models) --------------


def _format_type(annotation: Any) -> str:
    """Best-effort one-line type label for a Pydantic field annotation.

    Intentionally lossy — reviewers don't need full union/recursion details,
    just a recognisable shape: `str`, `list[str]`, `dict[str, str]`,
    `list[<Object>]`, `<Object>`, `<A | B>`.
    """
    if annotation is None or annotation is type(None):
        return "null"
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin is list:
        if args and isinstance(args[0], type) and issubclass(args[0], BaseModel):
            return f"list[{args[0].__name__}]"
        if args:
            return f"list[{_format_type(args[0])}]"
        return "list"
    if origin is dict:
        if len(args) == 2:
            return f"dict[{_format_type(args[0])}, {_format_type(args[1])}]"
        return "dict"
    # Optional[X] / X | None
    if origin is not None and args:
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return _format_type(non_none[0])
        return " | ".join(_format_type(a) for a in non_none)
    if isinstance(annotation, type):
        if issubclass(annotation, BaseModel):
            return annotation.__name__
        return annotation.__name__
    return str(annotation).replace("typing.", "")


def _describe_field(name: str, info: FieldInfo) -> dict[str, Any]:
    return {
        "name": name,
        "type": _format_type(info.annotation),
        "required": info.is_required(),
        "description": info.description or "",
    }


def output_fields_for(tool_name: str) -> list[dict[str, Any]] | None:
    """Return a flat list of top-level fields for the tool's output Pydantic model.

    None if the tool has no registered output model (shouldn't happen for the
    13 current tools, but defensive).
    """
    model = _TOOL_OUTPUT_MODEL.get(tool_name)
    if model is None:
        return None
    return [_describe_field(name, info) for name, info in model.model_fields.items()]


def parameters_for(tool_name: str) -> dict[str, Any] | None:
    """Return the agent-facing JSON schema for the tool's parameters.

    Closed vocabularies (`_COSTS_DERIVED_ENUMS`, plus the genetic-panel members of
    `order_specialized_test.test_type`) are filled from costs.yaml, so what a
    reviewer sees is what the agent can actually order. None if the tool isn't in the mirror — call site
    should treat missing metadata as "unknown" rather than rendering an empty
    form.
    """
    schema = _TOOL_PARAMETERS.get(tool_name)
    if schema is None:
        return None
    schema = copy.deepcopy(schema)
    for parameter, spec in schema.get("properties", {}).items():
        vocabulary = _vocabulary(tool_name, parameter)
        if (tool_name, parameter) == ("order_specialized_test", "test_type"):
            panels = sorted(_load_tool_costs().get("order_specialized_test", {}).get("genetic_panels", {}))
            vocabulary = list(vocabulary) + [f"genetic_panel:{panel}" for panel in panels]
        if vocabulary:
            if (tool_name, parameter) in _ARRAY_VALUED:
                spec.setdefault("items", {"type": "string"})["enum"] = vocabulary
            else:
                spec["enum"] = vocabulary
    return schema
