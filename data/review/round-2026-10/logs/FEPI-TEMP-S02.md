# FEPI-TEMP-S02
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for FEPI-TEMP) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance (plan 1.3), applied through the plan classes below. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.clinical_history.social_history.occupation` | "restaurant manager" while the HPI and driving history say elementary school teacher (class R). | FIXED: "elementary school teacher". |
| B | minor | `patient.history_present_illness` | Early head turn to the left and left-hand automatisms both point to a left onset (early non-forced head turn and unilateral manual automatisms are usually ipsilateral, fact 12), against a right mesial lesion and right EEG focus in a case meant to be concordant. | FIXED: head turn and manual automatisms made right-sided; no other HPI change. |
| E | minor | `patient.history_present_illness` | "prior convulsions other than the childhood absence seizures" (absences are not convulsions). | FIXED: "prior seizures other than ...". |
| B | minor | `patient.clinical_history.past_medical_history[1]` | "Iron deficiency anemia, corrected" while Hb 11.9 and MCV 79.1 are low on maintenance iron. | FIXED: "on maintenance iron supplementation". |
| C | major | `initial_tool_outputs.labs` (Prolactin 53.1) | Prolactin drawn hours after the event (class M, fact 11). | FIXED: row deleted; summary and interpretation now list only the mild microcytic anemia; beta-hCG and urine drug screen negative stated. |
| B | minor | `initial_tool_outputs.eeg.findings[0].frequency` | "Frequent" at 8-10 per hour (ACNS "occasional"). | FIXED: "Occasional"; impression no longer says frequent. |
| D | minor | `initial_tool_outputs.eeg.limitations`, `.impression`, `.findings[1].morphology` | Limitation recommended prolonged video-EEG (class K); impression not in report form, no period; TIRDA called "semi-rhythmic". | FIXED: "Routine 45-minute recording with drowsiness and stage II sleep; no habitual event captured."; numbered ABNORMAL EEG impression; "Sinusoidal, monomorphic rhythmic delta activity". |
| B | major | `initial_tool_outputs.mri` | Report identical to S03 (18 x 14 x 12 mm, same wording); "scalloping of the overlying inner table" is impossible for a lesion in the amygdala and anterior hippocampus; no statement of why contrast was given (class E). | FIXED: size 21 x 15 x 13 mm, lesion volume about 2.1 cm3, own T1/T2/FLAIR wording, scalloping removed, canonical post-contrast line, SWI line; impression numbered with "most consistent with a DNET; ganglioglioma cannot be excluded". |
| A | major | `followup_outputs[0]` (FDG-PET) | PET follow-up that no criterion orders (class J); its text cited the MRI (cross-modality). | FIXED: follow-up deleted; report moved to `fallback_tool_outputs.advanced_imaging` (modality FDG_PET) without the MRI reference; avoided action `avoid-waste-5-fdg-pet` (waste, `[Willmann_2007]`). |
| D | major | `followup_outputs` literature (now [1]) | Sources Chassoux 2022, Blumcke Brain Pathol 2021 and Englot 2012 not verifiable or not on the allow-list (class O); empty summary. | FIXED: Blumcke NEJM 2017 and Engel 2003 with real titles; general summary; last in the pathway. |
| C | minor | `followup_outputs` drug check (now [0]) | Capitalised "does NOT"; missing the inducer-contraceptive interaction and the ferrous sulfate line. | FIXED: interactions list rewritten (ethinylestradiol lowers lamotrigine; lamotrigine leaves the pill effective; enzyme inducers reduce pill efficacy; no ferrous sulfate interaction). |
| A | major | `ground_truth.action_criteria` | Literature and ECG required, drug check with template evidence, duplicated citations, label = rationale (classes A, B, H, T). | FIXED: order labs, ECG, MRI, routine EEG, drug check, literature; MRI, routine EEG and drug check (combined pill, fact 8) required; labs, ECG, literature optional; one bracketed key each, case-specific text. |
| A | minor | `ground_truth.action_criteria[action-3-analyze-brain-mri]` | Required `{contrast: true, protocol: epilepsy}` (class E). | FIXED: `{protocol: epilepsy}`. |
| A | minor | `ground_truth.sequence_constraints[0]` | Shared "low-grade tumor -> CYP-neutral" reason (class C). | FIXED: canonical reason, kept soft (drug check required). |
| A | major | `ground_truth.stop_rule` | Listed literature and ECG, max 0 (class D). | FIXED: MRI, EEG, drug check; max 1. |
| C | major | `ground_truth.assessment` | Process musts ("Obtain MRI with contrast", recognise the aura); first-line list with lacosamide; the enzyme-inducer prohibition mentioned chemotherapy; no contraception or valproate counselling in a woman of 27. | FIXED: musts first-line ASM with the pill interaction, contraception and folic acid, surgical referral of the DNET, driving, SUDEP; prohibitions surgical delay (kept), enzyme inducers with the combined pill, valproate (MHRA 2024), LP. |
| C | minor | `ground_truth.differential` | Ganglioglioma `high` (class P); childhood absence epilepsy in the history raised no generalized-epilepsy entry; cavernoma low without the SWI finding. | FIXED: ganglioglioma moderate, genetic generalized epilepsy low added, cavernoma very_low, every entry cites the finding that decides it. |
| E | minor | `ground_truth.key_clinical_evidence` | Engineering lines (class G); "MRI with contrast plus epilepsy protocol is the central study". | FIXED: rewritten (two-seizure criterion from the prior auras, concordance, contrast only once a lesion is seen, DNET WHO grade 1, pill interaction). |
| C | minor | `ground_truth.avoided_actions` | Template rationales; CT cited AAN 2007. | FIXED: case-specific rationales; CT waste kept (back to baseline, no head injury, fact 3) with `[ILAE_MRI_2019]`. |
| A | minor | `fallback_tool_outputs.echo` | No `echo_type`. | FIXED: "TTE". |

## Changes, in one paragraph a physician can read before re-reviewing
A 27-year-old left-handed teacher on a combined pill has 14 months of olfactory auras with dread and a first focal to bilateral tonic-clonic seizure; the head turn and manual automatisms are now right-sided, concordant with the right mesial temporal lesion. The work-up reads optional labs (normal glucose, sodium, calcium, negative beta-hCG, mild microcytic anemia; the late prolactin is gone) and ECG (normal), then the required epilepsy-protocol MRI, rewritten so it no longer duplicates S03 (21 x 15 x 13 mm multicystic non-enhancing lesion in the amygdala and anterior hippocampus, most consistent with DNET, ganglioglioma not excluded, post-contrast added because a lesion was seen), the required routine EEG (right anterior temporal spike-and-wave at F8, now "occasional" at 8-10/h, with TIRDA), and the required interaction check with the pill (ethinylestradiol halves lamotrigine; inducers make the pill unreliable). The literature search is optional and last (Blumcke 2017, Engel 2003). FDG-PET is waste. Musts: lamotrigine or levetiracetam with the pill interaction, contraception and folic acid, epilepsy surgery referral, driving, SUDEP; prohibitions: no surgical delay, no enzyme inducer with the pill, no valproate, no LP. Genetic generalized epilepsy (childhood absences) is now a low differential.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Pack allow-list: `[ILAE_def_2014]`, `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[Sabers_2003]`, `[Blumcke_2017]`, `[NICE_NG217_2025]` (plan 5, request 2).
- Synonyms: this is a tumor-associated mesial temporal lesion without hippocampal sclerosis, so the inherited "mesial temporal sclerosis epilepsy" synonym is wrong here (plan 5, request 6).

## Open questions for Andrea (judgment calls you could not settle)
- None.

## Verification
Adversarial check (24 Oct 2026) of the whole final case against this log and plan section 4 (S02); diff read against fa1d22e6.
- Confirmed: occupation teacher in both fields; HPI head turn and manual automatisms right-sided (early non-forced version and manual automatisms usually ipsilateral, fact 12), concordant with the right lesion and F8 focus; prolactin gone; "occasional" at 8-10/h fits ACNS 2021; MRI distinct from S03 (21 x 15 x 13 mm, ellipsoid volume about 2.1 cm3 as stated), canonical post-contrast line, FLAIR bright rim, no impossible scalloping; drug check required with correct fact 8 content (ethinylestradiol halves lamotrigine; inducers make the pill unreliable), soft MRI -> drug check with the canonical reason; stop rule MRI, EEG, drug check, max 1; Hb 11.9 with Hct 39.6 and MCV 79.1 plausible for iron deficiency, PMH now "maintenance"; folic acid and contraception must; differential (ganglioglioma moderate, GGE low) matches the evidence; Blumcke 2017 figures correct; case guards pass.
- Found: nothing to change.
- `perfect_agent.py -v` and `case_io.py check` clean for the case.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- Literature follow-up trigger `search_literature_dnet_epilepsy_surgery` renamed `search_literature_dnet_dysembryoplastic_neuroepithelial`: it names the case's lesion or concurrent finding, so it is served only to a query that names it.
- `action-7-interpret-labs.rationale`: engineering prefix or tier wording removed (was "A first convulsion warrants a check for ...").

## Close-out (24 Oct 2026)

Condition close-out (`plans/FEPI-TEMP-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G40 entries, re-applied with `--prune --conditions focal_epilepsy_temporal`): labels now focal epilepsy, temporal lobe epilepsy, TLE, epilepsy temporal lobe, mesial temporal lobe epilepsy, MTLE (added); removed mesial temporal sclerosis epilepsy (no hippocampal sclerosis on MRI); focal seizures; focal onset seizures; focal impaired awareness seizures (seizure-type labels, retired: their tokens occur in an acute symptomatic or functional-seizure answer). Codes: G40.2, G40.1, G40.9 plus G40.209, G40.109, G40.909 (not intractable); the idiopathic G40.009 and G40.019 removed and the intractable codes removed.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FEPI-TEMP-` passes, now with the discriminator guard and the FEPI-TEMP banned strings.

## Library contradictions (25 Oct 2026)

Orders the benchmark library answered with a normal report that contradicts this case now get a case-specific report (term: gist, where stored):

- analyze_eeg ambulatory: This is an ABNORMAL 48-hour ambulatory EEG due to: 1. Right anterior temporal spike-and-wave complexes (phase reversal at F8), maximal in NREM sleep.  (fallback_tool_outputs.eeg)
- analyze_eeg video: This is an ABNORMAL 72-hour video-EEG due to: 1. Right anterior temporal spike-and-wave complexes (phase reversal at F8), maximal in NREM sleep. 2. Ri (followup request_video_eeg)
- obtain_tissue_diagnosis resection: Dysembryoplastic neuroepithelial tumour, CNS WHO grade 1 (fallback_tool_outputs.tissue_diagnosis)
- obtain_tissue_diagnosis stereotactic_biopsy: Dysembryoplastic neuroepithelial tumour, CNS WHO grade 1 (followup request_stereotactic_biopsy)
- obtain_tissue_diagnosis open_biopsy: Dysembryoplastic neuroepithelial tumour, CNS WHO grade 1 (followup request_open_biopsy)
- order_specialized_test neuropsych_battery: Mild Weakness in visual learning and delayed visual recall (T-scores 39 and 37) with verbal memory and naming within the average range and intellectua (fallback_tool_outputs.specialized_test)
- interpret_labs AED_levels: No levetiracetam, valproate, carbamazepine, phenytoin, lamotrigine or lacosamide detected. (fallback_tool_outputs.labs[AED_levels], also answers valproate_level)
- interpret_labs iron_studies: Low serum iron, ferritin and transferrin saturation with raised TIBC: an iron-deficiency pattern. (fallback_tool_outputs.labs[iron_studies])

Checks: `perfect_agent.py` passes; the criterion snapshot of the case is unchanged; `pytest agent-platform/tests -k FEPI-TEMP` (case guards included), `test_reports_do_not_fabricate.py` and `apply_diagnosis_synonyms.py --check` pass; no new report repeats a 60-character window of any criterion's expected evidence.
