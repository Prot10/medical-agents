# BACT-MEN-RS05

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed fallback literature_search output; removed metadata.fallback_tool_kinds.literature_search. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: case fallback brain MRI (no MRI criterion, no stored brain MRI): removed T1_post_contrast and the 'post-contrast images' venous sinus observation, finding renamed sulcal FLAIR hyperintensity, impression without enhancement wording; contrast_used stays null (decision 3). No criterion change.
- MRI-CONTRAST verified: checked case fallback MRI free of post-contrast keys, findings and observations, impression consistent with its findings, contrast_used null (decision 3); no stored brain MRI and no brain-MRI criterion; probe plain and contrast orders get the fallback, not the library; no other field changed; perfect_agent -v passes. No error found.
