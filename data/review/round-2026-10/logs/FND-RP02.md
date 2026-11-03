# FND-RP02
Reviewer status: R1 none, R2 none (FND was never reviewed; no notes file) | Approved before this round: no

## Reviewer notes
No reviewer notes for this case.

| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `ground_truth.action_criteria` | Template criteria (plan A): literature and drug check `recommended` with shared labels, labs `optional`, labels equal to rationales, template citations. | FIXED: order exam (required), labs `["CMP","magnesium","phosphate","thiamine_B1"]` (recommended, plan 3.2), drug check (recommended), new optional `action-neuropsych-battery`, literature (optional, last); case-specific labels, rationales, expected evidence, citations. Stop rule stays the exam only (the only required criterion). |
| B | major | `patient.history_present_illness` | "Laboratory studies, including thyroid function and basic metabolic panel, were unremarkable" contradicts the stored BMP (K 3.3, Cl 94, BUN 22, Ca 8.2) and gives the result of the recommended labs. | FIXED: "Thyroid function tests were reported as normal." |
| C | major | `initial_tool_outputs.clinical_assessment` | "Sternocleidomastoid weakness ipsilateral to the hemiparesis" with no hemiparesis; meta keys in `criteria_met`; non-dermatomal sensory loss counted; key-leak impression "No further investigation is required...". | FIXED: canonical shape; 3 validated signs (bilateral Hoover, collapsing weakness, distractibility/inconsistency); sensory loss supportive; wasting and reflexes reported; SCM row removed. |
| C | minor | `patient.neurological_exam.additional` | Hoover described vaguely ("involuntary hip extension is detected on the opposite side ... suggesting functional weakness", an interpretation). | FIXED: "Hoover sign is positive on both sides: hip extension is 1/5 on direct testing but becomes strong during flexion of the opposite hip against resistance." |
| D | major | `initial_tool_outputs.labs` | Management text in `clinical_significance` ("replace", "replace empirically before any glucose load", "not Wernicke encephalopathy") and in `interpretation` (plan K); magnesium missing from the interpretation; a "Targeted assays for protracted vomiting" panel name that states the clinical question. | FIXED: `clinical_significance` null; interpretation a plain recital of abnormal values; panels regrouped (Thyroid, Hematinics, Magnesium_phosphate_thiamine, Muscle) with every value unchanged. |
| D | major | `followup_outputs[0]` (literature) | Unverifiable sources and the Hallett 2022 paper attributed to "Espay ... Lancet Neurol 2018" (plan B). | FIXED: deleted; canonical `initial_tool_outputs.literature_search` without the LaFrance and Goldstein rows (motor-only case). |
| C | major | `followup_outputs[1]` (drug check) | Proposed sertraline 50 mg, which she does not take, with fluoxetine and escitalopram alternatives; real issues (ondansetron QT with vomiting-related hypokalemia and hypomagnesemia, omeprazole with iron) not stated as such. | FIXED: deleted; `initial_tool_outputs.drug_interactions.general` lists her four medicines verbatim, omeprazole with ferrous sulfate, ondansetron QT risk with low K and Mg; no dose or new drug. |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts; no thiamine, refeeding, electrolyte or eating-disorder action in a 19-year-old with BMI 14.8 and four months of vomiting; primary amenorrhea with absent puberty never addressed. | FIXED: M-DX, M-COMM (interpreter if needed, father with consent), M-PHYSIO, M-PSY (depression, prolonged grief), thiamine before glucose with K and Mg replacement and refeeding monitoring, eating-disorder assessment with endocrine and gynecological evaluation of the primary amenorrhea. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | "per Stone 2018"; repeat-study item generic. | FIXED: P1 naming the repeat head CT and spine MRI, P2, P3, P7, "Give glucose-containing fluids before thiamine". |
| C | major | `ground_truth.differential` | MS and structural lesion cited a brain MRI not in the case; neuropathy cited "(when obtained)" EMG, which is avoided; encephalitis and malingering template rows; the referral diagnosis (schizophrenia) and the nutritional mimics missing. | FIXED: thiamine deficiency (Wernicke or dry beriberi) `low`, hypokalemic or malnutrition myopathy `low`, spinal cord lesion `low`, schizophrenia `low`, eating disorder (possibly coexisting) `moderate`, each with the case's data. |
| B | major | `ground_truth.red_herrings[0]` | "Family history of epilepsy" while the family history says "No family history of epilepsy". | FIXED: deleted. Red herrings now: bereavement, the 'moving creature' complaint with the schizophrenia referral, wasting with reduced ankle reflexes, raised ESR and CRP. |
| A | minor | `ground_truth.avoided_actions` | No repeat-study waste although a spine MRI was already normal (plan L). | FIXED: added `avoid-waste-repeat-spine-mri` (`order_body_imaging {study: spine_MRI}`); existing waste items cite `[Espay_2018]`/`[Stone_2016]` with patient-specific rationales. |
| E | major | `ground_truth.key_clinical_evidence` | Template items with the "Interim composition decision" leak, OPTIONAL item and Stone 2018. | FIXED: 5 case-specific items. |
| B | minor | `fallback_tool_outputs` | specialized_test and advanced_imaging untyped with the leak sentence; echo "benign incidental finding" without naming it and no `echo_type`. | FIXED: specialized_test and advanced_imaging nulled and removed from `fallback_tool_kinds`; echo impression names trace physiological mitral regurgitation, `echo_type: TTE`. |
| B | minor | `metadata.difficulty_description`, `.difficulty_rationale` | Description cited "incidental MRI findings that could suggest demyelinating disease" that do not exist; rationale a template. | FIXED: both rewritten from the case's data; `last_revised` 2026-10-24. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway is the functional-signs examination (required), then electrolytes with magnesium, phosphate and thiamine (recommended), the medication review (recommended), and optional neuropsychology and literature. The examination report counts the Hoover sign on both sides (now described correctly), collapsing arm weakness, distractibility (retching and proprioceptive loss that disappear with distraction) and strong leg use when repositioned against 1/5 on testing, records the leg wasting and 1+ ankle reflexes, and no longer lists a sternocleidomastoid sign for a hemiparesis she does not have. The HPI no longer says her metabolic panel was normal, which contradicted the stored potassium 3.3 and chloride 94. Lab values are unchanged; the management text about replacement and Wernicke was removed from the report. The drug check now covers ondansetron QT risk with low potassium and magnesium and omeprazole reducing iron absorption, instead of a sertraline she does not take. Musts add thiamine before glucose with potassium and magnesium replacement and refeeding monitoring, an eating-disorder assessment and endocrine and gynecological evaluation of her primary amenorrhea with absent puberty; prohibitions add glucose before thiamine and name the repeat CT and spine MRI. The differential now holds the referral diagnosis of schizophrenia, thiamine deficiency, a malnutrition or hypokalemic myopathy and a cord lesion (all low) and a possibly coexisting eating disorder (moderate). A repeat spine MRI is scored as waste.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1: `[Daum_2014]`, `[Stone_2016]`. Free-text: "NICE CG32 Nutrition support for adults", "Ondansetron SmPC, QT prolongation".
- Synonyms (plan CENTRAL 2): this motor-only case accepts "psychogenic non-epileptic seizures", "PNES", "functional seizures" and F44.5.

## Open questions for Andrea (judgment calls you could not settle)

None open. Decisions taken:
- Must on primary amenorrhea with absent pubertal development (my addition, not in the plan): at 19 this needs endocrine evaluation whatever the cause (undernutrition or another disorder), and the case documents it without acting on it.
- The eating disorder is in the differential as "possibly coexisting", `moderate`, per plan 4 ("as a comorbidity to assess"); it does not compete with the labelled diagnosis.
- RS01 shares this source patient (plan 6.3); the RS01 decisions mirror these.

## Verification

`perfect_agent.py FND-RP02 -v`: ok; the lab call gets the stored panel (BMP, magnesium, phosphorus, thiamine), the drug check gets `initial_tool_outputs.drug_interactions.general`. `case_io.py check FND-RP02`: schema and synonym guard OK; the only FND failures are the literature leaks of FND-P08 and S10 (other workers' cases). `test_case_guards.py -k FND-RP02`: 2 passed. Lab values compared with the original: none changed (Hct/Hb 3.07, MCHC 32.5; calcium corrected for albumin 9.2).

## Condition audit

2026-10-24, FND condition auditor.

- `action-neuropsych-battery.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `action-1-search-medical-literature.rationale`: removed engineering text (round/pack references, credit or tier wording); clinical content unchanged.
- `initial_tool_outputs.literature_search`: the summary still named video-EEG confirmation of functional seizures and psychological-treatment trials whose rows this motor-only output omits; set to the motor-only output of M09, P07, P08 and RM02 (Espay, Daum, Nielsen 2024, Stone 2005, motor summary); the functional-seizure guideline row (Tolchin 2026) was dropped with it, as the patient has no seizures.

After the edit: `perfect_agent.py` 30/30 FND pass; `case_io.py check` schema and synonym guard OK, the only suite failure is `test_guidance_claims` (expected); `test_case_guards.py -k FND` 60 passed.

## Close-out (24 Oct 2026)

Andrea's FND ruling of 24 Oct 2026 and the close-out decisions (`plans/FND-decisions.md`). What changed and why:

- Diagnosis synonyms scoped by phenotype (`diagnosis_synonyms.yaml` F44 entries; a label or code naming another presentation must not score): removed "functional movement disorder", "psychogenic non-epileptic seizures", "PNES", "functional seizures"; added "functional limb weakness", "functional motor disorder"; codes removed F44.5.
- Checks: `perfect_agent.py -v` and `case_io.py check` clean; `test_case_guards.py -k FND-` passes, now including the discriminator guard.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-4-interpret-labs]`.expected_evidence: was "Potassium 3.3, magnesium 1.5 and low-normal thiamine 74 nmol/L with normal phosphate and iron deficiency, from vomiting and starvation; none explains the weakness"; now "Potassium 3.3, magnesium 1.5 and low-normal thiamine 74 nmol/L with normal phosphate, from vomiting and starvation; none explains the weakness".
- Decision: trim evidence. Iron deficiency is a haematinics result, incidental to the refeeding and thiamine question this order answers.
- Scoring: none.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

Orders that reached the benchmark library's normal report although the case contradicts it now get a case-specific report (library answers stay for everything else).

- `perform_clinical_assessment assessment_type=gait_and_balance_timed` -> `fallback_tool_outputs.clinical_assessment`: timed gait and balance: not completed TUG, unable to take a step; legs gave way on standing with a controlled descent. Why: the exam documents an abnormal gait; the library reports a normal timed gait (TUG 9.1 s).
- `perform_clinical_assessment assessment_type=performance_status` -> `followup_outputs[request_performance_status]`: Karnofsky 40, ECOG 3. Why: the history documents limited activity; the library reports Karnofsky 100, ECOG 0, working.
- `order_specialized_test test_type=neuropsych_battery` -> `followup_outputs[request_neuropsych_battery]`: cognition within normal limits; moderate depressive and anxiety symptoms with a high somatic symptom burden; validity passed. Why: the history documents anxiety, depression or trauma-related symptoms; the library reports no significant mood or anxiety symptoms.

Checks: `perfect_agent.py` pass; `test_case_guards.py -k FND-RP02` pass; map verify (map_FND) problems 0; criterion-answer snapshot unchanged except `action-neuropsych-battery`, which the library answered before and the new report now answers.
