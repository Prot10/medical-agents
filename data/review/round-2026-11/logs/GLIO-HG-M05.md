# GLIO-HG-M05

## Class changes
- MRI-CONTRAST: split initial_tool_outputs.mri into a plain study (contrast_used false, the initial slot) and the unchanged gadolinium study (contrast_used true, followup_outputs[0], trigger request_contrast_mri, first in the pathway as the core diagnostic study). Plain copy: removed the "Post-contrast T1" signal key, "No leptomeningeal enhancement", "enhancing" from the remaining-brain observation, "including patchy enhancement foci" from the tumour volume, and from the impression item 2 (faint enhancing foci, no ring, no necrosis; "no restricted diffusion" kept) and the higher-grade clause that rests on the enhancing foci; kept size, T2/FLAIR extent, callosal extension, DWI and 2 mm midline shift, and "Imaging differential: diffuse glioma" (supported by the non-contrast infiltrative T2/FLAIR features). Criterion action-1-analyze-brain-mri already required contrast true (EANO 2021 / RANO: in a largely non-enhancing infiltrative mass the faint enhancing foci, the biopsy target for the higher-grade component, are seen only after gadolinium; the plain study does not answer it), so arguments unchanged and no plain alternative; expected_evidence matches the gadolinium report it receives, unchanged.
- MRI-CONTRAST verified: checked the plain initial MRI (contrast_used false) for gadolinium residue in keys, findings, observations, impression and volumetrics (none; impression matches findings, sizes, laterality and midline shift unchanged), the gadolinium follow-up request_contrast_mri (contrast_used true, byte-identical to the base report otherwise), the criterion action-1-analyze-brain-mri (contrast true, tumour protocol, fits EANO 2021 / RANO; expected_evidence is text of the gadolinium report it receives), probe (plain, contrast and both orders served from the case, never the library), pathway order (contrast MRI first), case fallback MRI (null), no other field changed against 393c547e, perfect_agent.py -v passes. No error found.
- MRI-CONTRAST follow-up (orchestrator): red_herrings[0].field_path 'initial_tool_outputs.mri.findings[0].signal_characteristics.Post-contrast T1' no longer resolved after the MRI split (the gadolinium study became followup_outputs[0] and shifted the follow-ups); now 'followup_outputs[0].output.findings[0].signal_characteristics.Post-contrast T1'.

## Reviewer notes
No November 2026 note targets this case (data/review/round-2026-11/notes/GLIO-HG.md covers S02 to S06 only). The R2 annotation file for this case holds only October-round comments (618200ca, 0c310d30, 615481ca), all present in round-2026-10/notes/GLIO-HG.json and already ruled in October; per the addendum they are not redone. The current case still reflects those October fixes (checked). Rulings file: empty list.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none this round) | NO-ACTION | none |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | ground_truth.assessment.required_recommendations[0] | Plan class C6 (D8): the non-enhancing infiltrative mass has FLAIR infiltration to the posterior body of the corpus callosum (MRI and DTI), but the surgery must did not mention it. Added "recognising that the extension into the corpus callosum limits the safe extent of resection". The resection report (followup_outputs[6]) says "including the posterior enhancing foci" and claims no gross total removal, so it is unchanged. | FIXED |
| B | minor | ground_truth.red_herrings[0].data_point, .location | data_point said the lesion is 85% non-enhancing "on initial MRI" and location pointed at initial_tool_outputs.mri, but since the MRI split the initial study is the plain one with no enhancement information; the 85% figure is in the gadolinium study. Now "on the gadolinium MRI" and location followup_outputs[0].output.findings[0].signal_characteristics (field_path was already updated in the class change). | FIXED |

## Changes
One plan-class change and one consistency correction, no reviewer note this round. The neurosurgery must now states that the tumour's extension to the posterior body of the corpus callosum limits the safe extent of resection (plan C6, D8); the resection report, which describes removal including the posterior enhancing foci without a gross-total claim, is unchanged. The low-grade-appearance red herring now says its 85% non-enhancing figure comes from the gadolinium MRI and points there, since the initial study is now the plain MRI. No MRI, criterion argument, tier or sequence constraint changed.

## Verification
Checks after the edits: perfect_agent.py -v passes and every criterion receives its own report; test_case_guards (-k on the six worker cases) 48 passed; case_io.py check: schema OK, synonym guard OK, no test failure names this case.
Pass 1: 0 errors found
- Verified: C6 clause added to the surgery must, consistent with FLAIR extension to the posterior callosal body in both MRI studies and the DTI; the resection report makes no gross total claim; the 85% non-enhancing figure is in the gadolinium study the red herring now cites; fMRI 8 mm and DTI 3 mm match the criteria and key evidence.
- Checked by the independent verifier: perfect_agent.py -v passes and each criterion receives its own report; test_case_guards -k for the six cases 48 passed; case_io.py check schema and synonym guard OK, no test failure names this case; no literature output or criterion left (class LIT); MRI pair served from the case (mri_probe); no em dash in added text; rulings file is an empty list, correct because the R2 annotation file holds only October note ids for this case.
Cosmetic (not counted): none changed.
