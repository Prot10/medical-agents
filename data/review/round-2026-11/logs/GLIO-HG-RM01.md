# GLIO-HG-RM01

## Class changes
- MRI-CONTRAST: split initial_tool_outputs.mri (mri_split initial). The gadolinium study (contrast_used true, text unchanged) is now followup[0] request_contrast_mri, first in the pathway because it is the core diagnostic study. The plain copy (contrast_used false) lost the 'Post-contrast T1' key, the 'no leptomeningeal enhancement' observation and volumetrics.estimated_tumor_volume (the enhancing component). The 'no additional enhancing lesions' observation, the DWI 'enhancing periphery', the type 'Enhancing intra-axial mass' and the impression were reworded without enhancement; measurements, fourth-ventricle compression, edema volume and MRA are kept. action-1-analyze-brain-mri keeps contrast: true, protocol tumor, with no plain alternative: EANO 2021 and RANO require gadolinium-enhanced MRI to define the enhancing target and plan biopsy or resection, and a plain study cannot answer that. Its expected_evidence is unchanged because it already matches the unchanged gadolinium report the criterion now receives (perfect_agent: followup request_contrast_mri). The stop rule and the hard MRI-before-tissue constraint are unchanged.
- MRI-CONTRAST verified: checked the plain initial copy for residual gadolinium keys, findings, observations and impression clauses and for impression/findings consistency (sizes, laterality, numbering); the gadolinium follow-up equals the base report plus contrast_used true; contrast_used true/false per decision, no stored brain MRI left null, case fallback MRI is null; action-1-analyze-brain-mri contrast true per EANO 2021/RANO with expected_evidence matching the gadolinium report it receives; mri_probe: plain, contrast and both orders in either sequence answered by the case, never the library; pathway and criterion order sensible; nothing outside the MRI split changed versus 393c547e; perfect_agent -v passes. No error found.

## Reviewer notes
No November 2026 note targets this case (data/review/round-2026-11/notes/GLIO-HG.md covers S02 to S06 only). The R2 annotation file for this case holds only October-round comments (16e1c115, 61968ced), all present in round-2026-10/notes/GLIO-HG.json and already ruled in October; per the addendum they are not redone. The current case still reflects those October fixes (checked). Rulings file: empty list.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none this round) | NO-ACTION | none |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | ground_truth.assessment.required_recommendations[3] | Plan class C3 variant A (D5): "Hold aspirin, taken for primary prevention, before the stereotactic biopsy" gave no interval. Replaced with the variant-A must: stop the primary-prevention aspirin now and schedule the stereotactic biopsy at least 7 days after the last dose because intracranial neurosurgery carries a high bleeding risk (ESC 2022); if neurological deterioration forces earlier surgery, operate with platelet function testing where available and platelet transfusion ready (Frontera 2016). | FIXED |
| B | minor | followup_outputs[7].output.findings[0].result and .site (trigger obtain_resection) | Template garble: "Resection specimen from the Right pons, enhancing solid component (MRI-guided stereotactic target) lesion". Now "Resection specimen from the right pontine lesion, multiple fragments, aggregate 3.5 cm", site "Right pons, open resection". The off-pathway report is kept unchanged otherwise. | FIXED |
| B | minor | fallback_tool_outputs.tissue_diagnosis.findings[0].result and .site | Same garble in the open-biopsy fallback; now "Open biopsy fragments from the enhancing solid component of the right pontine lesion, aggregate 1.4 cm; frozen section concordant", site "Right pons, open biopsy". | FIXED |

## Changes
One plan-class change and two text corrections, no reviewer note this round. The aspirin must now follows ESC 2022: stop the primary-prevention aspirin now and schedule the stereotactic biopsy at least 7 days after the last dose, operating earlier only if he deteriorates, with platelet function testing where available and platelet transfusion ready (Frontera 2016) (plan C3 variant A, D5). The off-pathway resection and open-biopsy reports had a garbled specimen line copied from the stereotactic target description; both now name the specimen and site plainly, with histology and molecular results unchanged. No MRI, criterion, tier or sequence constraint changed.

## Verification
Checks after the edits: perfect_agent.py -v passes and every criterion receives its own report; test_case_guards (-k on the six worker cases) 48 passed; case_io.py check: schema OK, synonym guard OK, no test failure names this case.
Pass 1: 0 errors found
- Verified: the C3 variant-A must matches D5 (stereotactic biopsy, 7 days, earlier only with deterioration, platelet function testing and transfusion ready) and agrees with the stored interaction output (aspirin bleeding warning) and the medication list; specimen/site wording changes in the resection and open-biopsy reports leave the results unchanged; KPS 40 is consistent across the performance-status report and the treatment must.
- Checked by the independent verifier: perfect_agent.py -v passes and each criterion receives its own report; test_case_guards -k for the six cases 48 passed; case_io.py check schema and synonym guard OK, no test failure names this case; no literature output or criterion left (class LIT); MRI pair served from the case (mri_probe); no em dash in added text; rulings file is an empty list, correct because the R2 annotation file holds only October note ids for this case.
Cosmetic (not counted): none changed.
