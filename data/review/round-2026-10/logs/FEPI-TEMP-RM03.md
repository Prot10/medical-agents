# FEPI-TEMP-RM03
Reviewer status: no reviewer notes for FEPI-TEMP (R1 and R2 never reviewed this condition in a notes round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input is the July 2026 tool guidance (plan 1.3), applied through the condition plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria` | No head CT after a fall during a convulsion with a parietal abrasion and GCS 8 on arrival, while CT was scored as waste (plan class I, section 4). | FIXED: new required `action-ct-head` (`order_ct_scan {}`) with a stored `initial_tool_outputs.ct` (minimally depressed linear right parietal fracture, no hemorrhage, contusion or pneumocephalus; intracranial and scalp lipomas, calcifications, porencephalic cyst, hemiatrophy); soft CT -> MRI constraint; `avoid-waste-4-order-ct-scan` deleted; contradictory normal `fallback_tool_outputs.ct` set to null and removed from `metadata.fallback_tool_kinds`. |
| C | major | `initial_tool_outputs.mri` | Stored MRI described "equivocal" hippocampal signal "could represent artifact" while the label rests on definite right HS (class F). | FIXED: dedicated 3T epilepsy-protocol MRI (technique line), definite right HS (volume loss, T2/FLAIR hyperintensity, loss of internal architecture, temporal horn enlargement); post-contrast T1 added because lesions were seen, no enhancement (excludes tumor and the leptomeningeal enhancement of Sturge-Weber); numbered impression. |
| B | minor | `initial_tool_outputs.mri.volumetrics` | Volumes 2.1 / 3.4 identical to S01 (plan: no shared numbers). | FIXED: right 2.3 cm3, left 3.6 cm3, asymmetry index 0.22 ((L-R)/(L+R)), finding says 36% smaller. |
| C | minor | `initial_tool_outputs.mri.findings[Calvarial remodeling]`, `[Cortical calcification]` | "Inward remodeling" of the calvarium over a porencephalic cyst is implausible; SWI "blooming confirming calcification" (blooming alone does not separate calcium from blood). | FIXED: "focal thinning of the right parietal calvarium"; SWI "blooming foci with phase characteristics of calcification". |
| C | major | `ground_truth.action_criteria[action-7-interpret-labs]` | Labs optional with template evidence in a breakthrough convulsion from phenytoin non-adherence. | FIXED: required, `{panels: ["AED_levels"]}`, evidence names the total and free phenytoin levels and normal electrolytes; panel key renamed `AED Levels` so the order names its payload (`test_no_required_order_receives_nothing_it_names`). |
| D | major | `initial_tool_outputs.labs` | Prolactin 42.6 drawn at an unknown interval after the event (class M). | FIXED: row, summary and interpretation entries deleted; interpretation states the normal sodium, calcium, magnesium, renal and hepatic values. |
| B | minor | `initial_tool_outputs.ecg.findings[0]`, `.interpretation` | "Sinus tachycardia, rate 98" (class T). | FIXED: "Normal sinus rhythm, 98/min"; ECG criterion optional with the actual result as evidence. |
| D | minor | `initial_tool_outputs.eeg.limitations` | "Prolonged video-EEG monitoring is recommended" (class K). | FIXED: the recording's own limits (post-ictal, drowsiness and light sleep, no HV, muscle artifact, no habitual event); final period added to the impression. |
| C | major | `followup_outputs` (FDG-PET) | FDG-PET follow-up that no criterion orders, first in the pathway (class J). | FIXED: deleted (not moved to fallback: the case is not presurgical); `avoid-waste-fdg-pet` added. |
| D | major | `followup_outputs` (literature) | Literature required and in the stop rule; unverifiable sources (Moog 2018, Cerminara 2020, Jayalakshmi 2019) (classes A, O). | FIXED: optional, last; output rewritten with NICE NG217, SANAD II, Kwan 2010 and Engel 2003 (plan 1.1), general evidence only; leak guard passes. |
| C | major | `followup_outputs` (drug check), `action-5-check-drug-interactions` | Drug check required with template evidence; output omitted the real interactions (folic acid lowers phenytoin; phenytoin induction of lamotrigine and lacosamide) and quoted the patient's creatinine. | FIXED: recommended (class B); output lists the levetiracetam, folic acid and induction interactions, gradual phenytoin withdrawal, renal dosing as a rule, HLA-B*15:02 before oxcarbazepine as a category warning; evidence names the actual interactions. |
| C | major | `ground_truth.assessment` | Process musts (3T MRI, video-EEG), "initiate AED after diagnostic confirmation" in a man already on treatment, and surgical referral without drug resistance (non-adherence is not an ASM trial). | FIXED: musts are status-epilepticus treatment of a recurrence, restoring ASM therapy (phenytoin reload or levetiracetam switch), a reliable ASM supply (social work), neurosurgical review of the fracture, SUDEP. Prohibitions: canonical valproate line, "do not label drug-resistant", "do not delay restarting ASM therapy"; the LP-before-imaging line deleted (CSF is waste and no LP is indicated). |
| C | major | `ground_truth.differential` | HS-negative focal epilepsy and status epilepticus left `moderate` after the work-up; Sturge-Weber (calcification and hemiatrophy) and post-traumatic seizure not considered (class P). | FIXED: assessment-time likelihoods with the excluding finding; Sturge-Weber, NCSE and acute symptomatic seizure after head injury added as `low`; tumor `very_low`. |
| E | minor | `ground_truth.key_clinical_evidence` | Generic items and two July-review engineering lines (class G). | FIXED: five case-specific items. |
| B | minor | `ground_truth.red_herrings` | Empty, although `metadata.difficulty_description` names the TSH as a red herring. | FIXED: TSH 5.8 (`initial_tool_outputs.labs.panels.Additional Labs[2]`) and the parietal fracture (`initial_tool_outputs.ct.impression`). |
| B | minor | `patient.neurological_exam.reflexes` | Plantar "flexor on left, equivocal on right" in a right hemispheric syndrome with left arm weakness and left facial droop. | FIXED: "flexor on right, equivocal on left". |
| B | minor | `patient.history_present_illness` | Surname Khatri also used in SYNC-CARD-RM03, also a grocery-store worker (template carry-over). | FIXED: renamed Mr. Bhattarai (South Asian, unused in the dataset). |
| A | minor | `fallback_tool_outputs.echo` | No `echo_type` (class I, Q). | FIXED: `TTE`. |
| E | minor | criteria `citations`, `rationale`, `label` | Every key listed twice, rationale repeating the label (class H). | FIXED: one bracketed key per criterion and avoided action, case-specific rationales. |
| E | minor | `metadata.difficulty_description`, `difficulty_rationale` | Described a "subtle" HS and five required tools with video-EEG. | FIXED: rewritten to the current pathway. |

## Changes, in one paragraph a physician can read before re-reviewing

A 27-year-old South Asian man with childhood epilepsy, developmental delay and three months of missed phenytoin refills has two months of mesial temporal focal impaired-awareness seizures, then a 4-5 minute focal to bilateral tonic-clonic seizure with a fall, a parietal abrasion and GCS 8 after lorazepam. The required pathway is now: phenytoin level with glucose and electrolytes (total 4.2, free 0.5 mcg/mL, no provoking abnormality; prolactin removed), an immediate non-contrast head CT (new: minimally depressed right parietal fracture without hemorrhage, intracranial and scalp lipomas, calcifications, porencephalic cyst), a dedicated 3T epilepsy-protocol MRI showing definite right hippocampal sclerosis with the ECCL lesions and no enhancement, and the routine EEG (right F8/T4 sharp waves, right temporal slowing). The ECG (normal sinus rhythm, 98/min) and literature are optional, the drug check recommended and the FDG-PET is waste. Musts: treat a recurrence as status epilepticus, restore ASM therapy now (reload phenytoin or switch to levetiracetam with a gradual phenytoin taper), secure the ASM supply through social work, neurosurgical review of the fracture, SUDEP counselling; no valproate, no "drug-resistant" label (the failure was non-adherence), no delay of treatment while waiting for MRI or EEG. Sturge-Weber, NCSE and a post-traumatic seizure are in the differential as low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys used that are not yet in the pack allow-list (plan CENTRAL 2): `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[NICE_NG217_2025]`.
- Synonyms (plan CENTRAL 6): the inherited `G40.009`/`G40.019` (idiopathic localization-related) codes do not fit this structural epilepsy.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken and their reasons:
- No surgical referral must: the plan lists RM03 for the drug-resistance referral only "if section 4 says so", and it does not; the breakthrough followed non-adherence with subtherapeutic levels, which ILAE 2010 does not count as an ASM failure. The literature output still gives the general surgery evidence.
- Post-contrast MRI line kept (plan class E, malformation cases): with cortical calcification and hemiatrophy, enhancement is what separates Sturge-Weber and tumor from ECCL; the criterion requires only `{protocol: epilepsy}`.
- No HLA-B*15:02 must (plan: the switch is to levetiracetam or lamotrigine, and he has tolerated phenytoin long term); the drug output carries the screening warning against its oxcarbazepine alternative.
- CT cited `[ILAE_MRI_2019]` (fact 3: CT in an emergency such as head injury or failure to return to baseline); a NICE head-injury key would be more specific but is not in the plan's source list.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the diff against master and the whole final case. Checked every log claim against the file: CT criterion and stored CT, soft CT -> MRI and MRI -> drug check constraints (ids exist, direction correct), labs required `{panels: [AED_levels]}` against the `AED Levels` panel, volumes 2.3 / 3.6 cm3 (index 0.22 and 36% both correct), prolactin absent, ECG "Normal sinus rhythm, 98/min", EEG limitations, FDG-PET waste, literature sources (NICE NG217, SANAD II, Kwan 2010, Engel 2003: authors, titles, pages correct), red-herring paths (`Additional Labs[2]` is the TSH; `ct.impression` exists), plantar laterality now fits the right hemispheric syndrome, tiers and stop rule per plan section 4.
Found and fixed:
- `avoid-waste-2-order-echocardiogram.rationale` cited "no murmur", but the case has no physical examination: reworded to rest on the seizure features and the normal ECG.
- `action-6-analyze-eeg.rationale` said the EEG was done "after recovery" while the stored report is a post-ictal recording: now "in the post-ictal period".
Nothing left for close-out beyond the log's CENTRAL items. perfect_agent, case_io check and the case guards are clean.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- Literature follow-up trigger `search_encephalocraniocutaneous_lipomatosis_epilepsy` renamed `search_encephalocraniocutaneous_lipomatosis_eccl`: it names the case's lesion or concurrent finding, so it is served only to a query that names it.
- Differential "Nonconvulsive status epilepticus after the convulsion": ICD-10-CM G41.8 -> G40.201.
