# FEPI-TEMP-M04
Reviewer status: R1 none, R2 none (no notes file for FEPI-TEMP) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case. The physician input for FEPI-TEMP is the July 2026 tool guidance (plan 1.3), applied through the plan.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.key_clinical_evidence` (plan N) | "Right-hand automatisms (contralateral to the dominant hemisphere lesion) ... are lateralizing": unilateral manual automatisms are usually ipsilateral; and "the left anterior temporal EEG focus (F7/T3) and the left posterior superior temporal FCD are anatomically concordant". | FIXED: localization rests on the left temporal EEG focus and the left temporal lesion; automatisms described as a weak, usually ipsilateral sign; the left-handed patient's lesion is "probably" in the language-dominant hemisphere. Engineering lines deleted (plan G). |
| D | major | `initial_tool_outputs.mri` (plan E) | Gadolinium line and "absence of enhancement argues against higher-grade lesion" in an FCD study; the comparison with the outside MRI repeated as a teaching note in every signal field; lesion placed in a "supramarginal transitional zone" (parietal) for a temporal-lobe label. | FIXED: technique and comparison lines once in `additional_observations`; signal fields describe findings only; location "posterior superior temporal gyrus"; numbered impression with the imaging differential (FCD most consistent, low-grade tumor not excluded); no gadolinium. |
| C | major | `initial_tool_outputs.labs` (plan M) | Prolactin 34.8 ng/mL "drawn 45 minutes post-event" after a focal impaired-awareness seizure, with interpretive text. | FIXED: row and interpretation deleted; "All values within normal limits." |
| B | minor | `initial_tool_outputs.ecg` | Interval set identical to M02 (rate 76, PR 154, QRS 86, QTc 416); non-cardiac references in `clinical_correlation` and interpretation. | FIXED: rate 80, PR 146, QRS 90, QTc 404; cardiology-only interpretation; `clinical_correlation` empty. |
| D | minor | `followup_outputs[*]` FDG-PET | Finding text cross-references the MRI ("corresponding to the cortical abnormality identified on the epilepsy-protocol MRI"); "asymmetry index" for a ratio. | FIXED: within-modality wording, uptake ratio 0.88. PET criterion stays optional (plan). |
| D | major | `followup_outputs[*]` literature (plans A, O) | Required; Bernasconi N Brain 2019 (does not exist), Blumcke 2011 with a wrong title, "Glauser 2017 Epilepsia 58:1235-1268" (does not exist) with lacosamide and oxcarbazepine as supported first line. | FIXED: optional, last; Bernasconi A 2019, Blumcke 2011 (real title), Glauser 2013 with Level A stated per plan fact 6. |
| C | minor | `followup_outputs[*]` drug check (plan B) | Driving advice inside the drug check; a creatinine value quoted from labs the agent may not have ordered; carbamazepine and oxcarbazepine offered without HLA-B*15:02 in a South Asian patient. | FIXED: HLA-B*15:02 in the alternatives; renal note without the number; driving line deleted. Criterion optional (`[CPIC_2018]`), canonical evidence. |
| A | major | `ground_truth.action_criteria` (plans E, H, T) | MRI `contrast: true`; literature, drug check, ECG required; doubled citations; template EEG and labs evidence. | FIXED: MRI `{protocol: epilepsy}`, EEG required; labs, ECG, PET, drug check, literature optional; one key each; evidence from the stored reports; order MRI, EEG, labs, ECG, PET, drug check, literature. |
| A | major | `ground_truth.sequence_constraints`, `stop_rule` (plans C, D) | Template MRI -> drug check constraint; stop rule with literature, drug check, ECG, max 0. | FIXED: constraint deleted; stop rule MRI + EEG, max 2. |
| C | major | `ground_truth.assessment` (plan L) | Two "teaching point" musts and an "order epilepsy-protocol MRI" must (work-up, not management); ASM list with lacosamide and oxcarbazepine as first line; no HLA-B*15:02 or SUDEP. | FIXED: musts first-line lamotrigine or levetiracetam, surgical referral of the FCD with language mapping (left-handed, lesion near posterior language cortex), HLA-B*15:02, driving, SUDEP (possible nocturnal convulsions); prohibitions kept (reworded without "clinical integration"), valproate added. |
| C | major | `ground_truth.differential` (plans P, S) | "MRI-negative focal epilepsy" `high` and left MTS `moderate` after the MRI shows FCD and normal hippocampi; PNES entry cites prolactin and video-EEG not served. | FIXED: both `low` with the excluding findings; PNES rewritten from the case's own data; tumor kept `moderate` (the MRI itself cannot exclude it). |
| C | minor | `ground_truth.avoided_actions` | Template rationales. | FIXED: case-specific; CT waste kept. |
| A | minor | `fallback_tool_outputs.echo` | No `echo_type`. | FIXED: `TTE`. |
| E | minor | `metadata` | Template difficulty text ("five required tools"). | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The policy now requires the epilepsy-protocol MRI and the routine EEG; labs, ECG, FDG-PET, drug check and literature are optional. The MRI report reads as a dedicated non-contrast epilepsy study that shows the left posterior superior temporal focal cortical dysplasia (cortical thickening, gray-white blurring, transmantle sign) with normal hippocampi, compares once with the outside standard MRI, and keeps a hedged imaging differential with a low-grade tumor. The prolactin drawn 45 minutes after a focal seizure is gone. The lateralization claim was corrected: right-hand automatisms are not "contralateral" evidence; localization rests on the left temporal EEG focus and the left temporal lesion, and in this left-handed man language dominance is only probable. Musts: lamotrigine or levetiracetam, surgical evaluation with language mapping, HLA-B*15:02 before carbamazepine or oxcarbazepine, driving, SUDEP; valproate is prohibited. MRI-negative epilepsy and left MTS are now `low`. Literature sources are real and state the Glauser 2013 evidence levels correctly.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys outside the pack allow-list used per plan 1.1: `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[NICE_NG217_2025]`, `[CPIC_2018]`, `[ILAE_FCD_2011]`.
- Synonyms (plan 5.6): this FCD case inherits "mesial temporal lobe epilepsy" and "mesial temporal sclerosis epilepsy", which are wrong for a lateral temporal dysplasia; also `G40.219` and idiopathic `G40.009`/`G40.019`.

## Open questions for Andrea (judgment calls you could not settle)

None. Decision: the low-grade tumor stays `moderate` in the differential because the MRI report itself says it cannot be excluded and histology is pending; the dysplasia is the labelled diagnosis.

## Verification

Adversarial check, 24 Oct 2026 (case committed in b8be2153; read in full).
- Checked: KCE lateralization rewritten per fact 12 (no "contralateral" claim; left-handed, probable dominance only); MRI is non-contrast with the lesion in the posterior superior temporal gyrus, index 0.02 matches 3.1/3.0 cm3; prolactin absent; ECG values match the criterion; PET follow-up optional with within-modality wording; literature uses Bernasconi A 2019, Blumcke 2011 and Glauser 2013 with the correct Level A statement; HLA-B*15:02 must (South Asian); MRI-negative and MTS differentials `low`; tiers and stop rule per plan.
- Found: no error. The low-grade tumor stays `moderate`; the MRI itself leaves it open and only histology settles it, so this is consistent with ruling 7. Em dashes in the HPI, the PMH and the red herring are original text, not new text.
- Changed: nothing. Checks clean for this case.
