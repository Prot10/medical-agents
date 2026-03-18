from __future__ import annotations
from typing import Any
from .base import BaseTool, ToolResult
from .mock_server import MockServer


class SpecializedTestTool(BaseTool):
    name = "order_specialized_test"
    description = (
        "Order specialized neurological tests. Types: "
        "neuropsych_battery (~$1,200, cognitive assessment for dementia), "
        "emg_ncs (~$600, nerve conduction/electromyography for neuropathy), "
        "vep (~$200, visual evoked potentials for MS/optic neuritis), "
        "ssep (~$200, somatosensory evoked potentials), "
        "baep (~$200, brainstem auditory evoked potentials), "
        "tilt_table (~$300, syncope workup), "
        "polysomnography (~$1,000, sleep disorders), "
        "autonomic_testing (~$400, dysautonomia), "
        "exercise_stress_test (~$250, cardiac workup)."
    )
    parameter_schema = {
        "type": "object",
        "properties": {
            "clinical_context": {
                "type": "string",
                "description": "Clinical indication for the specialized test.",
            },
            "test_type": {
                "type": "string",
                "enum": [
                    "neuropsych_battery", "emg_ncs", "vep", "ssep", "baep",
                    "tilt_table", "polysomnography", "autonomic_testing",
                    "exercise_stress_test",
                ],
                "description": (
                    "Type of specialized test. 'neuropsych_battery': comprehensive "
                    "cognitive testing (MMSE, MoCA, RAVLT, etc.). 'emg_ncs': "
                    "electromyography and nerve conduction studies. 'vep'/'ssep'/'baep': "
                    "evoked potentials. 'tilt_table': orthostatic syncope evaluation. "
                    "'polysomnography': overnight sleep study. 'autonomic_testing': "
                    "autonomic reflex screen. 'exercise_stress_test': cardiac stress test."
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
