from __future__ import annotations
from .base import BaseTool


class CTScanTool(BaseTool):
    name = "order_ct_scan"
    description = (
        "Order a CT scan of the head and neck — this tool images nothing else. CT is faster "
        "and cheaper than MRI: use it for emergency neuroimaging (hemorrhage exclusion, acute "
        "trauma), or CT angiography (CTA) for cervical and intracranial vascular assessment. "
        "Cost: EUR 184 base, +EUR 92 contrast, +EUR 184 CTA. For a CT of the chest, abdomen, "
        "pelvis or spine — including a CT pulmonary angiogram — use order_body_imaging; "
        "for a coronary study use order_advanced_imaging."
    )
    parameter_schema = {
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
                "description": "Whether CT angiography (CTA) is needed for vascular assessment.",
                "default": False,
            },
        },
        "required": ["clinical_context"],
    }
