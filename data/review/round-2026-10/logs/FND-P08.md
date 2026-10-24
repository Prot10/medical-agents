# FND-P08
Reviewer status: no reviewer notes for FND (R1 and R2 never reviewed this condition) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input is the July 2026 tool guidance (plan 1.3), applied through the plan. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | blocker | `patient.neurological_exam.motor`, `.additional`, `initial_tool_outputs.clinical_assessment` | "Upward drift" was counted as a functional sign; upward drift with hemisensory loss is a parietal (or cerebellar) sign, so the case rested its diagnosis on an organic sign. A 2/5 arm also cannot be drift-tested unless it is held against gravity. | FIXED: the arm is 2/5 on testing yet held outstretched against gravity and drifts downward without pronation (two rule-in findings: drift without pronation, inconsistency), plus the dragging left leg. |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.additional` | HPI reported an examination finding ("the affected arm drifts upward..."); the exam said "Capillary glucose was checked at presentation" (the scored test). | FIXED: both removed; duplicated celiac sentence merged. |
| C | major | `ground_truth.action_criteria[action-5-interpret-labs]` | Glucose optional (with CMP) in a focal deficit 3 hours after an insulin bolus. | FIXED: required, `["glucose"]`, first in the list; soft constraint glucose -> imaging; row renamed "Capillary glucose (on arrival)", value 92 kept. |
| C | major | `ground_truth.action_criteria[action-4-analyze-brain-mri]`, `initial_tool_outputs.ct`, `avoided_actions` | Imaging optional and CT scored as waste in an acute hemiparesis within 3 hours. | FIXED: required "Emergency brain imaging" with alternatives MRI `{}` and non-contrast CT; the CT report moved from the fallback to `initial_tool_outputs.ct`; CT waste deleted. |
| C | major | `ground_truth.avoided_actions[avoid-waste-1-analyze-ecg]`, `fallback_tool_outputs.ecg` | ECG scored as waste although a baseline ECG is part of the acute stroke pathway; the fallback ECG gave rate 63 against a heart rate of 108. | FIXED: waste deleted; ECG moved to `initial_tool_outputs.ecg` as sinus tachycardia 106; new optional `action-ecg`. |
| C | minor | `ground_truth.action_criteria` | No vessel imaging in an acute stroke pathway. | FIXED: optional `action-ct-angiography` with a normal CTA follow-up (`request_ct_angiography`); routing checked (non-contrast CT orders still receive the non-contrast report). |
| C | major | `followup_outputs[0]` (`insulin_pump_cgm_education`) | Drug check used as diabetes education (CGM alarms, glucagon kit). | FIXED: deleted. |
| D | major | `initial_tool_outputs.literature_search` | Summary equal to the criterion's expected evidence (leak guard failed). | FIXED: canonical motor literature output (plan 2B); criterion optional, last. |
| B | minor | `initial_tool_outputs.drug_interactions` | No initial output. | FIXED: insulin + sertraline (minor glucose-lowering interaction) in report voice; criterion optional. |
| D | major | `initial_tool_outputs.clinical_assessment` | Meta keys; impression leak "No further investigation is required...". | FIXED: canonical shape, 2 rule-in signs, reflexes, hemisensory loss supportive. |
| B | minor | `initial_tool_outputs.labs` | One panel named "T1DM_Celiac_Neurology_Workup". | FIXED: split into Point of care, Diabetes, Celiac serology, Vitamins, Thyroid; all values kept. |
| B | minor | `initial_tool_outputs.mri`, `initial_tool_outputs.ct` | MRI listed "Normal" as an observation and had no technique; CT had no technique line. | FIXED: technique lines, pertinent negatives, one-line impressions. |
| C | major | `ground_truth.assessment` | Template musts and prohibitions; no acute-stroke-pathway must. | FIXED: M-DX, stroke-pathway must (glucose, imaging; no thrombolysis with positive signs and a normal DWI), M-COMM, M-PHYSIO; P1, P2, P3, P7. |
| C | major | `ground_truth.differential` | Template MS, stroke ("positive Hoover sign", not in the case), structural and autoimmune encephalitis rows; hypoglycemia absent. | FIXED: hypoglycemia with focal deficit low (glucose 92), acute ischemic stroke or structural lesion low. |
| E | major | `ground_truth.key_clinical_evidence` | Template items with the "Interim composition decision" and OPTIONAL leaks. | FIXED: five case-specific items. |
| B | minor | `ground_truth.red_herrings` | Generic items. | FIXED: insulin bolus, celiac disease, anxiety on sertraline, rejected thesis. |
| A | minor | `ground_truth.avoided_actions[*]`, `fallback_tool_outputs` | `[Stone_2018]`; specialized_test leak fallback, advanced_imaging `MRI_brain_functional`, literature fallback; echo without `echo_type`. | FIXED: `[Espay_2018]` / `[Stone_2016]` with patient-specific rationales; three fallbacks nulled and removed from `metadata.fallback_tool_kinds` (with ct and ecg, now on the pathway); echo `echo_type: TTE`. |
| E | minor | `metadata.notes` | "Arm drifts UPWARD - pathognomonic FND. Celiac neurological panel needed." Both wrong. | FIXED: rewritten, with `difficulty_rationale`. |

## Changes, in one paragraph a physician can read before re-reviewing

A 24-year-old woman with type 1 diabetes on a pump presents 3 hours after the sudden onset of left arm weakness and numbness, 3 hours after an insulin bolus. The required pathway is now the acute stroke pathway: fingerstick glucose first (92 mg/dL), then the examination, then emergency brain imaging (MRI with DWI or non-contrast CT, both normal); ECG (sinus tachycardia 106) and CT angiography (normal) are optional. The examination was corrected: the case previously relied on "upward drift", which is a parietal sign; the arm is now 2/5 on testing yet held against gravity and drifts downward without pronation, with a dragging left leg. Musts: positive diagnosis of functional arm weakness, management as a suspected stroke until glucose and imaging are back (no thrombolysis once positive signs and a normal DWI establish the diagnosis), explanation and specialist physiotherapy. The CGM-education "drug check" was deleted. Differential: hypoglycemia with focal deficit and acute ischemic stroke, both low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms (plan 5.2): this motor-only case accepts "psychogenic non-epileptic seizures", "PNES", "functional seizures" and F44.5.
- `diagnosis.accepted[0]` says "celiac neurological complications excluded"; the stored celiac serology supports it, but nothing in the policy requires testing for them. A label without that clause would fit the case better (not changed: label edits are reserved to a reviewer ruling).
- Citation `[AHA_ASA_Stroke_2026]` (from the ISCH-STR pack) used in an FND case; add it to the FND pack's allowed citations.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken and their reasons:
- The exam change from upward drift to drift without pronation is a change of patient data, made because the plan rules upward drift is not a functional sign and the case otherwise had only a mild leg drag to rest on.
- MRI alternative `{}` instead of `{contrast: false, protocol: stroke}`: the tool has no default for `contrast`, and a stroke MRI ordered as `standard` is still the right study. CT alternative `{contrast: false}` (the CT tool defaults it).
- ECG removed from waste and CTA added as optional: both belong to the AHA/ASA acute stroke pathway, so ordering them is justified, but neither bears on the functional diagnosis.

## Verification

Adversarial check (24 Oct 2026) of the log against the case and against the pre-round version (`b8be2153^`). What I checked: the patient diff (upward drift replaced by drift without pronation in motor and additional; HPI exam finding and "Capillary glucose was checked" removed; onset 3 hours after the bolus matches the chief complaint); the pathway order (glucose, exam, imaging) and the glucose -> imaging constraint; the CT moved to `initial_tool_outputs.ct` and the CT waste removed; MockServer routing with a call script: `order_ct_scan {contrast: false}` and `{}` receive the non-contrast report, `{angiography: true, contrast: true}` receives the CTA follow-up, `interpret_labs ["glucose"]` receives the panel with the capillary glucose 92; the ECG (sinus tachycardia 106 against HR 108); the stroke-pathway must against the prohibitions (no contradiction); signs count 2 and the exam text; every log claim marked FIXED.

Found and changed:
- `initial_tool_outputs.labs.panels["Celiac serology"]`: values carried the unit inside the value ("<1 U/mL", "3.2 U/mL") with the unit also in `unit`; now "<1" and 3.2.
- `initial_tool_outputs.literature_search...summary`: same mismatch as in M09; replaced with a summary of the four motor rows returned.

Left as is (already in the log's CENTRAL): `accepted[0]` names "celiac neurological complications excluded"; the stored celiac serology supports it and any lab order returns it. Checks re-run after the changes: `perfect_agent.py -v` ok, `case_io.py check` clean for this case (schema, synonym guard, no failing test names it), `test_case_guards.py -k` passed. The diagnosis label, `icd_codes` and synonyms are unchanged from before the round; no new em dashes or `Stone_2018` strings.
