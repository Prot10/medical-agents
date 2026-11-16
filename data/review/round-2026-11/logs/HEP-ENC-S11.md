# HEP-ENC-S11

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed fallback literature_search output; removed metadata.fallback_tool_kinds.literature_search. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: no brain MRI on the pathway and no MRI criterion; case fallback brain MRI (contrast_used stays null, answers any order): removed the additional observation 'No abnormal post-gadolinium enhancement' and impression item 6 'No abnormal enhancement' (a one-slot fallback cannot be split, decision 3). The abdomen/pelvis MRI body imaging already states contrast: true. perfect_agent ok.
- MRI-CONTRAST verified: Checked the case fallback brain MRI (null, no gadolinium content left, impression renumbered 1-5 cleanly), no brain MRI on the pathway and no MRI criterion, body-imaging contrast flags, no other field changed; mri_probe, perfect_agent -v and case_io check clean. No error found.
