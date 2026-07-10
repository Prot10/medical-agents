from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer
from .vocabulary import genetic_panels, specialized_test_types


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

    def __init__(self, mock_server: MockServer | None = None):
        self.mock_server = mock_server

    def execute(self, parameters: dict[str, Any]) -> ToolResult:
        if self.mock_server:
            return self.mock_server.get_output(self.name, parameters)
        raise NotImplementedError(f"Real {self.name} model not yet connected")
