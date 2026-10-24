from __future__ import annotations
from .base import BaseTool
from .vocabulary import GENETIC_PANEL_PREFIX, genetic_panels, specialized_test_types


def type_enum(packs: tuple[str, ...] = ()) -> list[str]:
    """The fixed test types plus one `genetic_panel:<panel>` member per priced panel."""
    return specialized_test_types(packs=packs) + [
        GENETIC_PANEL_PREFIX + panel for panel in genetic_panels(packs=packs)
    ]


class SpecializedTestTool(BaseTool):
    name = "order_specialized_test"
    description = (
        "Order specialized neurological tests: nerve/muscle studies (emg_ncs, "
        "emg_single_fiber, repetitive_nerve_stimulation, nerve_biopsy, muscle_biopsy, "
        "skin_biopsy_iencf), evoked potentials (vep, ssep, baep), cognitive testing "
        "(neuropsych_battery), sleep studies (polysomnography), autonomic and "
        "cardiac workup (tilt_table, autonomic_testing, exercise_stress_test), "
        "ophthalmic tests (optical_coherence_tomography, visual_field_perimetry), "
        "respiratory_function (FVC/MIP/MEP, for ALS and MG), ice_pack_test, audiometry, "
        "speech_language_evaluation (primary progressive aphasia), "
        # `mslt` and `pure_tone_audiometry` were retired 2026-08-05: priced and orderable
        # but referenced by zero cases and never requested in the clinical tool review, so
        # they were unreviewed action-space surface. Audiometry came back on 2026-10-24 as
        # `audiometry`, requested by the October 2026 review of bacterial meningitis (WHO
        # 2025 post-meningitis hearing test); `mslt` stays retired.
        "and targeted gene panels via 'genetic_panel:<panel>'."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the specialized test.",
            },
            # Enum derived from costs.yaml (see tools/vocabulary.py): the fixed test types
            # plus one `genetic_panel:<panel>` member per priced panel.
            "test_type": {
                "type": "string",
                "enum": type_enum(),
                "description": (
                    "Type of specialized test; targeted gene panels are 'genetic_panel:<panel>'. "
                    "'emg_ncs': nerve conduction + needle EMG. 'emg_single_fiber' and "
                    "'repetitive_nerve_stimulation': neuromuscular junction (myasthenia). "
                    "'respiratory_function': FVC, MIP/MEP, NIF (ALS monitoring, MG crisis "
                    "risk). 'neuropsych_battery': comprehensive cognitive testing. "
                    "'vep'/'ssep'/'baep': evoked potentials. 'tilt_table': syncope. "
                    "'optical_coherence_tomography': retinal RNFL (MS, optic neuritis). "
                    "'audiometry': pure-tone and speech audiometry with tympanometry "
                    "(hearing loss after bacterial meningitis). 'speech_language_evaluation': "
                    "speech-language pathology assessment of motor speech, grammar, naming, "
                    "repetition and comprehension, which classifies a primary progressive aphasia "
                    "(a full cognitive battery is 'neuropsych_battery'). "
                    "'electrophysiology_study': invasive EP study — HV interval, sinus node recovery, "
                    "programmed stimulation for inducible arrhythmia, accessory-pathway refractory period. "
                    "'sodium_channel_blocker_challenge': ajmaline, flecainide or procainamide under "
                    "12-lead ECG with high precordial leads, to unmask a type 1 Brugada pattern. "
                    "'genetic_panel:inherited_arrhythmia': long QT, Brugada and CPVT genes; "
                    "'genetic_panel:cardiomyopathy': arrhythmogenic, hypertrophic, dilated and "
                    "laminopathy genes."
                ),
            },
        },
        "required": ["clinical_context", "test_type"],
    }
    vocabulary = {"test_type": type_enum}
    pack_notes = {
        "general_medicine": {
            "": (
                "In general medicine it also orders endoscopy, pulmonary function tests, "
                "ambulatory blood pressure monitoring and bone densitometry."
            ),
            "test_type": (
                "'upper_endoscopy', 'colonoscopy': direct inspection of the upper "
                "gastrointestinal tract or the colon; histology of any biopsy is ordered "
                "through obtain_tissue_diagnosis with procedure 'endoscopic_biopsy'. "
                "'pulmonary_function_tests': spirometry, lung volumes and DLCO, not the bedside "
                "'respiratory_function'. 'ABPM': 24-hour ambulatory blood pressure. 'DXA': bone "
                "densitometry."
            ),
        },
    }
