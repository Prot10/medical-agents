# HEP-ENC-S08

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed fallback literature_search output; removed metadata.fallback_tool_kinds.literature_search. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: case fallback MRI had contrast_used false (no gadolinium content), so a contrast order was answered by the library normal MRI, contradicting the stored pallidal T1 hyperintensity; set to null (decision 3) so the fallback answers plain and contrast orders. Found by the orchestrator probe over all 600 cases.
