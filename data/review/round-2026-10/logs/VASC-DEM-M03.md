# VASC-DEM-M03
Reviewer status: R1 not reviewed, R2 not reviewed (VASC-DEM has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | VASC-DEM was never annotated; no note ids exist for this case. All changes below come from the condition plan and my own reading. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1: non-schema `sequences` key made the required MRI unmatchable. | FIXED: `analyze_brain_mri {}`. |
| D | major | `action-8-search-medical-literature`, `initial_tool_outputs.literature_search`, `fallback_tool_outputs.literature_search` | Plan C2 leak. | FIXED: criterion deleted; initial null; fallback deleted. |
| C | major | `action-9-check-drug-interactions`, `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | Plan C3 group R: a concrete interaction changes management (aspirin with the anticoagulant she needs), but the criterion was optional `{}` with generic evidence and the fallback said "no prohibitive interaction". | FIXED: criterion `recommended`, five alternatives (`drug` warfarin, apixaban, rivaroxaban, edoxaban, dabigatran); case-specific initial outputs keyed by each drug: warfarin with aspirin (additive bleeding, avoid without separate indication), atorvastatin (minor INR effect), alendronate and the others none, supervised dosing warning; DOAC entries with aspirin and their dosing rules (apixaban: no reduction criterion at age 77, creatinine 0.96). Generic fallback deleted. Placed last in the pathway. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: MoCA total and item losses in the exam. | FIXED: bedside observation only. |
| B | major | `initial_tool_outputs.clinical_assessment.findings`, `.impression`, `.criteria_met` | MoCA arithmetic: the listed losses (trail, cube, clock 1/3, digit span, serial sevens, recall 3/5, month) give 21 raw and 22 with the education point, not 20; impression concluded "points to a multi-infarct mechanism"; `stepwise_course_with_dateable_events` is history, not a test result. | FIXED: item-level findings adding letter fluency 0/1 and abstraction 1/2 (19 raw + 1 for 10 years = 20/30); impression lists the losses only; the history key removed from `criteria_met`. |
| D | major | `initial_tool_outputs.mri.impression`, `.additional_observations` | Plan C5: "requires a proximal source", "explains the transient anomia" (cross-reference to history), "absence of microbleeds supports the safety of anticoagulation" (management). | FIXED: numbered impression with territories and sizes, hedged within-imaging "a distribution suggestive of embolism" (Kind 2), SWI negative stated as a finding; WMH grade made explicit "periventricular 2, deep 1" (caps and smooth halo). |
| D | major | `initial_tool_outputs.echo.impression`, `.echo_type` | Echo impression prescribed anticoagulation ("an indication for anticoagulation independently of any arrhythmia"); `echo_type` missing on the answer to a TTE criterion. | FIXED: numbered cardiac findings (aneurysm 32 x 24 mm, laminated thrombus 14 x 9 mm non-mobile, EDD 58 mm, EF 38%, LA 40 mm, mild functional MR); `echo_type` TTE. |
| D | minor | `initial_tool_outputs.ecg.interpretation` | Told the reader the next study ("an echocardiographic question rather than a rhythm question"). | FIXED: categorical ECG read only. |
| D | minor | `initial_tool_outputs.advanced_imaging.impression` | Duplex stated a mechanism verdict ("a large-artery mechanism cannot explain infarcts in both hemispheres"). | FIXED: stenosis grades and vertebral flow only. |
| B | minor | `initial_tool_outputs.labs` | Plan C6: Hct 41.6 against Hb 12.6; template values; female HDL range ">40" (46 unflagged); eGFR ">60"; interpretation with targets and "renal function adequate for anticoagulant dosing". | FIXED: Hct 38.1; WBC 7.1, Plt 221, MCV 86, Na 140, K 4.6, ALT 19, albumin 4.0, folate 9.6; HDL ">50" and flagged low; eGFR ">=60" (62 not flagged); summary rebuilt; interpretation "Flagged: ..." only. |
| D | minor | `fallback_tool_outputs.advanced_imaging`, `.labs`, `.specialized_test`, `.ct` | Plan C7 "non-contributory" fallbacks; CT "already obtained". | FIXED: three deleted; CT fallback shows this patient's three chronic infarcts. Holter fallback kept (sinus, consistent). |
| A | minor | `action_criteria[*]` | Plan C13. | FIXED: rationales and expected evidence case-specific (duplex rationale notes her contrast allergy); one bracketed key each. |
| B | minor | `stop_rule` | `max_additional_actions` 0 (C16). | FIXED: 1; required set unchanged (screen, labs, MRI, ECG, duplex, TTE). Order screen, labs, MRI, ECG, duplex, TTE, drug check. |
| B | minor | `avoided_actions` | Plan C18. | FIXED: CT canonical rationale; EEG and monitoring rationales name this patient's reasons. |
| C | major | `ground_truth.assessment.required_recommendations` | Musts restated diagnostic steps (ECG, MRI, carotid) and lacked warfarin specifics, LDL, HbA1c, BP, supervision. | FIXED (C19): warfarin INR 2-3 for at least 3 months and heart failure referral for EF 38%; stop aspirin (no stent or ACS); supervised medicines and INR monitoring; LDL below 70 (106 on atorvastatin 20); BP below 130/80 from 142/78 with orthostatic checks; HbA1c individualised about below 8.0% (7.4%) [ADA_2025_older_adults]. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Wording "already been demonstrated", "new anticoagulant". | FIXED: reworded; contrast-allergy prohibition kept (plan). |
| C | major | `ground_truth.differential[0]` | Plan C8: occult AF `moderate` after a structural source and sinus rhythm. | FIXED: `low`, features without the em dash. |
| E | minor | `ground_truth.key_clinical_evidence[2]` | Em dash in a sentence rewritten anyway. | FIXED: colon. Label `accepted[0]` dash FLAGGED only (ruling 3). |
| - | check | plan 3.6 | perfect_agent ok; probe: all seven criteria and all five drug alternatives answered by case data; CT and Holter answered by the case fallbacks; `case_io.py check` and test_case_guards list no failure naming M03. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case stays multi-infarct vascular dementia in a 77-year-old woman with three chronic embolic-pattern infarcts (left MCA, right MCA, right PICA), sinus rhythm with an old anterior infarct, and an apical LV aneurysm with laminated thrombus (EF 38%). Reports now describe their own modality only: the echo no longer prescribes anticoagulation, the ECG no longer points to the echo, the MRI no longer argues the source or anticoagulation safety, the duplex gives grades only, and the MoCA items now add up to 20/30 with the education point. The drug check is now recommended and case-specific (warfarin or any DOAC against her aspirin, statin and alendronate). The musts are management: warfarin INR 2-3 for at least 3 months with a heart failure referral, stop aspirin, supervised medicines and INR monitoring, LDL below 70, BP below 130/80, individualised HbA1c. Occult AF is low on the differential. Labs corrected (Hct, HDL range and flag).

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation key `[ADA_2025_older_adults]` used in the HbA1c must (plan 5.4).
- Synonyms (plan 5.1): `F06.7` appended to this dementia case's codes.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the diff and the whole final case. Checked: MoCA arithmetic (11 lost, 19 raw + 1 = 20/30); group R drug check (warfarin first, four DOACs, each keyed output names aspirin and the real medicines; apixaban no-reduction statement correct at 77 years and creatinine 0.96); musts (warfarin INR 2-3 for at least 3 months, heart failure referral, stop aspirin: stable CAD more than 12 months after the MI, LDL below 70 justified by coronary and carotid atherosclerosis, HbA1c individualised); contrast allergy vs duplex choice and the contrast prohibition; `echo_type: TTE` in the TTE criterion (schema default TTE, so a bare call matches); female ranges, HDL flag; monitoring waste vs prohibition consistent; differential low for occult AF.

Found and changed:
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.mri.findings[0].location` | A 22 x 16 mm infarct "including Wernicke's area" with naming 3/3, repetition 2/2 and no aphasia on examination: a deficit the lesion should produce is absent. | FIXED: "Left posterior middle temporal gyrus (left middle cerebral artery territory)", compatible with a transient anomia that recovered. |
| A | minor | `action_criteria[action-5-analyze-ecg].label` | Label asked for LVH of chronic hypertension; the criterion's evidence and rationale are AF and the old anterior infarction. | FIXED: label "look for atrial fibrillation and characterise the old anterior infarction found three years ago". |

perfect_agent ok (all five drug alternatives served by case data); `case_io.py check` and test_case_guards list no failure naming M03.

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels.Vascular_risk[Total cholesterol]` | Total cholesterol 188 mg/dL did not equal LDL + HDL + TG/5 (181.6); the same lab-arithmetic class was fixed in M07-M10, P01, P02 and S06-S11 but not here. | FIXED: total cholesterol 182 mg/dL (flag unchanged; LDL, HDL and TG, which the musts and evidence quote, unchanged). |
| C | minor | `ground_truth.avoided_actions[avoid-waste-3-order-advanced-imaging].rationale`, `[avoid-waste-4-interpret-labs].rationale` | Plan C18: the MIBG and paraneoplastic/autoimmune rationales were still the August template text shared by M01-M06; the autoimmune one described "a chronic stepwise decline with a hypertensive imaging burden", which is wrong for this case. | FIXED: case-specific one-liners (no Lewy features; stepwise decline dated to two focal events). |
| D | major | `initial_tool_outputs.clinical_assessment.criteria_met` | Plan 1.2 and C5 (no report states the severity): the screen's structured fields still carried independence_in_iadl_lost, i.e. the mild-versus-major threshold, the profile verdict or history items. Workers removed these keys in the other 19 cases; here they survived (the P03 worker flagged the question for a condition-wide decision). | FIXED: keys removed; `criteria_met` keeps domain impairment and cue-responsive recall. The informant FAQ score stays in the report as an instrument score. |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.
