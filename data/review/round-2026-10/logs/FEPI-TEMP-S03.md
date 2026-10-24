# FEPI-TEMP-S03
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for FEPI-TEMP) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance (plan 1.3), applied through the plan classes below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.history_present_illness` | Surname "Kapoor" in an African American patient, duplicated in M03 and S06 (class R). | FIXED: "Mr. Mosley" (no other case uses it). |
| B | minor | `patient.clinical_history.social_history.occupation`, `metadata.case_body_concerns[1]` | "insurance adjuster" against "elementary school teacher" in the HPI; the metadata flag recorded the contradiction. | FIXED: "elementary school teacher"; the resolved audit flag removed from `case_body_concerns`. |
| B | minor | `patient.history_present_illness` | Left-hand automatisms (usually ipsilateral, fact 12) against a right mesial lesion and right EEG focus in a concordant case. | FIXED: right-hand automatisms; nothing else in the HPI changed. |
| E | minor | `patient.history_present_illness` | "his fiance observed his staring" (social history says fiancee). | FIXED: "his fiancee observed him staring". |
| C | minor | `patient.clinical_history.allergies` | "Contrast dye (mild reaction)" leaves gadolinium use ambiguous. | FIXED: "Iodinated CT contrast (mild urticaria)" (plan). |
| C | major | `initial_tool_outputs.labs` (Prolactin 56.8) | Late prolactin (class M). | FIXED: row deleted; summary and interpretation now list only the isolated microcytosis. |
| B | minor | `initial_tool_outputs.labs.panels.CBC`, `.BMP` | Female reference ranges in a man (Hb 12.0-16.0, Hct 36-46, creatinine 0.6-1.1; template carry-over). | FIXED: Hb 13.5-17.5, Hct 38.0-50.0, creatinine 0.7-1.3 with value 0.94 mg/dL (0.66 would be below the male range). |
| B | minor | `initial_tool_outputs.eeg.findings` | "Frequent" at one discharge every 1-2 minutes; TIRDA "semi-rhythmic with notched morphology". | FIXED: "approximately 1-2 per minute"; "Sinusoidal, monomorphic rhythmic delta activity". |
| D | minor | `initial_tool_outputs.eeg.limitations`, `.impression` | Limitation recommended prolonged video-EEG (class K); impression not in report form. | FIXED: canonical routine limitation; numbered ABNORMAL EEG impression. |
| B | minor | `initial_tool_outputs.mri.impression`, `.additional_observations` | Impression "No mass effect" against the finding "Minimal ... remodeling of the adjacent temporal horn"; omitted the adjacent cortical FLAIR signal; no reason for contrast (class E). | FIXED: numbered impression with minimal temporal horn remodeling, DNET as most consistent, possible associated dysplasia; canonical post-contrast line. Size kept (S02 was changed instead, plan). |
| A | major | `followup_outputs[0]` (FDG-PET) | PET follow-up no criterion orders (class J); text cited "the known DNET lesion"; ratio 0.81 shared with P04. | FIXED: follow-up deleted; report moved to `fallback_tool_outputs.advanced_imaging` (FDG_PET) without MRI references, ratio 0.84; avoided action `avoid-waste-5-fdg-pet` (waste). |
| D | major | `followup_outputs` literature (now [1]) | Chassoux Neurology 2012 (plan class O), Bilginer 2009 and Lee 2018 unverifiable; empty summary. | FIXED: Blumcke NEJM 2017 and Engel 2003, general summary; last in the pathway. |
| D | minor | `followup_outputs` drug check (now [0]) | Warning cited "creatinine 0.66 mg/dL" (cross-modality and now outdated). | FIXED: generic renal dosing; vitamin D3 interaction line. |
| A | major | `ground_truth.action_criteria` | Literature, drug check and ECG required with template text (classes A, B, H, T). | FIXED: order labs, ECG, MRI, routine EEG, drug check, literature; MRI and routine EEG required; the rest optional; MRI `{protocol: epilepsy}`; one bracketed key each; case-specific text. |
| A | major | `ground_truth.sequence_constraints`, `stop_rule` | Shared MRI -> drug check constraint; stop rule with literature, drug check, ECG, max 0. | FIXED: constraint deleted (drug check optional); stop rule MRI and EEG, max 1. |
| C | major | `ground_truth.assessment` | Process musts (MRI with contrast; recognise the aura); first-line list with lacosamide; HLA prohibition in an African American patient (plan L). | FIXED: musts first-line ASM, surgical referral, driving, SUDEP; HLA prohibition deleted; valproate prohibition (MHRA 2024) added; ENT and LP prohibitions kept. |
| C | minor | `ground_truth.differential` | Ganglioglioma `high` (class P); the HPI raises panic attacks but the differential did not. | FIXED: ganglioglioma moderate; panic attacks very_low with the excluding findings; syncope very_low; MTS and FCD entries tied to the MRI. |
| E | minor | `ground_truth.key_clinical_evidence` | Engineering lines (class G); "AED therapy is bridging". | FIXED: two-seizure criterion from the prior auras, concordance, tumor surgery outcomes, ASM now with surgical evaluation. |
| C | minor | `ground_truth.avoided_actions` | Template rationales. | FIXED: case-specific; CT waste kept (back to baseline, no injury from the fall) with `[ILAE_MRI_2019]`. |
| A | minor | `fallback_tool_outputs.echo` | No `echo_type`. | FIXED: "TTE". |

## Changes, in one paragraph a physician can read before re-reviewing
Mr. Mosley (renamed from a duplicated surname), a 42-year-old left-handed teacher, has eight months of olfactory and epigastric auras, some with impaired awareness, and a first focal to bilateral tonic-clonic seizure; his manual automatisms are now right-sided, concordant with the right mesial temporal DNET and the right anterior temporal EEG focus. The labs now carry male reference ranges (creatinine 0.94 mg/dL) and no prolactin; the ECG is normal. Required: epilepsy-protocol MRI (18 x 14 x 12 mm multicystic non-enhancing lesion in the amygdala and anterior hippocampus, minimal temporal horn remodeling, possible adjacent dysplasia; contrast added because a lesion was seen) and routine EEG (frequent right anterior temporal spike-and-slow-wave at F8, TIRDA). Labs, ECG, interaction check (vitamin D only) and literature (Blumcke 2017, Engel 2003) are optional; FDG-PET is waste. Musts: lamotrigine or levetiracetam, surgical referral, driving, SUDEP; the HLA prohibition is gone (not indicated for his ancestry) and valproate is prohibited. Panic attacks, which he suspected, are now in the differential as excluded; ganglioglioma is moderate. The contrast allergy is specified as iodinated CT contrast.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Pack allow-list: `[ILAE_def_2014]`, `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[Blumcke_2017]`, `[NICE_NG217_2025]` (plan 5, request 2).
- Synonyms: tumor-associated lesion without hippocampal sclerosis; the inherited "mesial temporal sclerosis epilepsy" synonym is wrong here (plan 5, request 6).

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Verification
Adversarial check (24 Oct 2026) of the whole final case against this log and plan section 4 (S03); diff read against fa1d22e6.
- Confirmed: rename (Mosley) and occupation; right-hand automatisms concordant; allergy "iodinated CT contrast" (gadolinium MRI unaffected); male reference ranges and creatinine 0.94; prolactin gone; HLA prohibition removed (African American); valproate prohibition added; tiers, stop rule (MRI, EEG, max 1), no constraint; FDG_PET waste; panic attacks raised by the HPI now in the differential; literature sources real; case guards pass.
- Found: (1) the MRI put the DNET "bright rim sign" on T2 ("Bright ring sign" in T2, "bright T2 rim" in the impression); the sign is a FLAIR finding (S02 and S06 already report it on FLAIR). Changed `initial_tool_outputs.mri.findings[0].signal_characteristics.T2` (sentence removed), `.FLAIR` ("thin hyperintense peripheral rim (bright rim sign)") and `.impression` ("bright FLAIR rim"). (2) The fallback FDG-PET ratio 0.84 duplicated M03; changed to 0.86 in `fallback_tool_outputs.advanced_imaging.findings[0].signal` and `.impression` (consistent with "moderately reduced").
- `perfect_agent.py -v` and `case_io.py check` clean for the case.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- Literature follow-up trigger `search_literature_dnet_epilepsy_surgery` renamed `search_literature_dnet_dysembryoplastic_neuroepithelial`: it names the case's lesion or concurrent finding, so it is served only to a query that names it.
- `action-7-interpret-labs.rationale`: engineering prefix or tier wording removed (was "A first convulsion warrants a check for ...").
- `action-5-check-drug-interactions.rationale`: engineering prefix or tier wording removed (was "The only regular medicine is vitamin D3,...").
