from __future__ import annotations
import logging
from typing import Any
from .base import BaseTool
from .vocabulary import genetic_panels, is_valid_test_type, specialized_test_types

logger = logging.getLogger(__name__)


class SpecializedTestTool(BaseTool):
    name = "order_specialized_test"
    description = (
        "Order specialized neurological tests: nerve/muscle studies (emg_ncs, "
        "emg_single_fiber, repetitive_nerve_stimulation, nerve_biopsy, muscle_biopsy, "
        "skin_biopsy_iencf), evoked potentials (vep, ssep, baep), cognitive testing "
        "(neuropsych_battery), sleep studies (polysomnography, mslt), autonomic and "
        "cardiac workup (tilt_table, autonomic_testing, exercise_stress_test), "
        "ophthalmic tests (optical_coherence_tomography, visual_field_perimetry), "
        "respiratory_function (FVC/MIP/MEP, for ALS and MG), ice_pack_test, "
        "and targeted gene panels via 'genetic_panel:<panel>'."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the specialized test.",
            },
            # Enum derived from costs.yaml (see tools/vocabulary.py). JSON Schema `enum`
            # cannot express the `genetic_panel:<panel>` family, so it is documented here
            # and enforced by tools/vocabulary.py::is_valid_test_type.
            "test_type": {
                "type": "string",
                "enum": specialized_test_types(),
                "description": (
                    "Type of specialized test. Also accepts 'genetic_panel:<panel>' where "
                    f"<panel> is one of: {', '.join(genetic_panels())}. "
                    "'emg_ncs': nerve conduction + needle EMG. 'emg_single_fiber' and "
                    "'repetitive_nerve_stimulation': neuromuscular junction (myasthenia). "
                    "'respiratory_function': FVC, MIP/MEP, NIF (ALS monitoring, MG crisis "
                    "risk). 'neuropsych_battery': comprehensive cognitive testing. "
                    "'vep'/'ssep'/'baep': evoked potentials. 'tilt_table': syncope. "
                    "'optical_coherence_tomography': retinal RNFL (MS, optic neuritis)."
                ),
            },
        },
        "required": ["clinical_context", "test_type"],
    }

    def _validate_parameters(self, parameters: dict[str, Any]) -> None:
        """Warn (only) when `test_type` is outside the closed vocabulary.

        Covers both the fixed test types and the `genetic_panel:<panel>` form
        (see tools/vocabulary.py). Out-of-vocabulary values silently get the
        off-pathway fallback output and the default cost tier; that behavior
        is intentionally preserved (changing it would change agent behavior
        mid-benchmark), but it must be visible in the logs.
        """
        test_type = parameters.get("test_type")
        if isinstance(test_type, str) and not is_valid_test_type(test_type):
            logger.warning(
                "order_specialized_test called with out-of-vocabulary test_type %r "
                "(known test types: %s; known genetic panels: %s). "
                "Proceeding unchanged — fallback output/cost will apply.",
                test_type,
                ", ".join(specialized_test_types()),
                ", ".join(genetic_panels()),
            )
