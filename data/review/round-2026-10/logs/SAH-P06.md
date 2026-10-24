# SAH-P06
Reviewer status: R1 none, R2 no notes and no status in the notes file (plan: probably approved) | Approved before this round: probably (not confirmed, plan section 6 question 6)

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | The notes file has no note for SAH-P06. All changes below are condition-wide classes (plan sections 2 to 4) or own findings. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `initial_tool_outputs.csf` | Appearance "Pink-tinged ... not grossly bloody due to anemia dilution effect" (serum anemia does not change CSF RBC; 68,000/uL is grossly bloody) and a bilirubin peak in an LP done within hours of a 1-hour-old headache (bilirubin needs about 12 hours) (C15); "WBC 82/uL corrected". | FIXED: "Grossly bloody, uniformly in tubes 1 to 4"; spectrophotometry "Oxyhemoglobin peak present; no bilirubin increment (sample obtained less than 12 hours after onset)"; counts kept (68,000 and 65,000/uL); WBC "82/uL (tube 4, uncorrected)"; interpretation restated as a pattern. |
| B | major | `ground_truth.red_herrings[2]` | Red herring relied on xanthochromia that cannot exist at this timing. | FIXED: data point and interpretation now rest on the non-clearing tube counts and on bilirubin needing about 12 hours. |
| D | major | `initial_tool_outputs.ct` | Lab value (Hgb 7.2) cited inside the CT report, "CRITICAL NOTE", "LP is essential regardless of CT result", sensitivity essay in the impression (C14). | FIXED: findings describe the subtle cistern effacement, a low blood-pool attenuation (dural sinuses about 36 HU, an imaging correlate of anemia) and normal ventricles; impression without the essay; LP recommendation kept as the diagnostic step. |
| B | minor | `ground_truth.red_herrings[1]` | Interpretation framed the CT as late ("declines after 6-24 hours") although it was done at 1 hour. | FIXED: CT at 1 hour, isodense blood from severe anemia, LP required. |
| C | major | `ground_truth.assessment.required_recommendations[1]` | LP must "at least 6-12 h after symptom onset", which contradicts the LP the case performs within hours and the reason the LP is indicated here (anemia, not timing). | FIXED: LP must tied to the anemia, with the tube comparison as the decisive test before 12 hours. |
| C | major | `followup_outputs[transfusion]`, `required_recommendations` | Transfusion of 2 units PRBC filed as a drug-interaction check with "Hgb target 8-10" (C8). | FIXED: follow-up deleted; must: transfuse for Hb 7.4 to keep it at or above 8 g/dL before securing, SAHaRA showed no benefit of a 10 g/dL threshold, investigate the iron deficiency once stable. |
| C | major | `followup_outputs[nimodipine check]` | "Hold metoprolol during nimodipine", "Target MAP >90 mmHg" (invented), and a warning citing anemia (C5, C10). | FIXED: interactions metoprolol-nimodipine (monitor), levothyroxine-nimodipine (none), ferrous sulfate-levothyroxine (separate by 4 h); warnings continue beta-blocker, 30 mg every 2 h option, no parenteral capsule contents, CYP3A4. Criterion `recommended` with case-specific label, evidence and rationale. |
| C | major | `followup_outputs[TCD]` | "Day 4 TCD" with mild vasospasm and "Hgb now 9.2 after transfusion 2 units PRBC" at an encounter 1 hour after onset (C2). | FIXED: baseline post-ictus day 0, normal velocities (left MCA 96, right 92 cm/s, Lindegaard 2.1 and 2.0), clinical note deleted, canonical protocol and recommendation. |
| C | major | `ground_truth.action_criteria`, `followup_outputs` | No DSA before securing (C3). | FIXED: `dsa-aneurysm-anatomy` (recommended), diagnostic DSA report matching the CTA (5.9 x 4.4 mm, daughter bleb, neck 3.1 mm, dome-to-neck 1.9, PComA from the neck, no other aneurysm, no vasospasm). |
| A | major | `ground_truth.action_criteria[action-11]` | MRI criterion required `sequences: [T1, T2, FLAIR, SWI, GRE]`, an argument the `analyze_brain_mri` tool schema does not offer (only `clinical_context`, `protocol`, `contrast`), so no real agent could match it; label said "CT timing is past sensitivity window" although the CT was at 1 hour. | FIXED: `required_arguments` `{}`, `optional` (C16), label and rationale about isodense blood, expected evidence from the report. |
| D | minor | `followup_outputs[MRI]` | One-line teaching sentence instead of a report (C16). | FIXED: report with FLAIR and SWI cisternal blood (suprasellar, left ambient, left Sylvian), no parenchymal lesion, no hydrocephalus. |
| D | minor | `initial_tool_outputs.ecg` | "Sinus tachycardia - consistent with anemia" (cross-modality) (C14). | FIXED: "Sinus tachycardia"; em dashes removed from the interpretation. |
| B | minor | `initial_tool_outputs.labs` | No potassium or magnesium (C9); BNP "Within reference range" in an "Exclusion studies" panel; type-and-screen engineering sentence; abnormal summary missing WBC, glucose, iron (C14). | FIXED: potassium 4.2 mEq/L, magnesium 2.1 mg/dL, BNP 58 pg/mL in Cardiac, type-and-screen significance null, summary and interpretation list the same seven abnormal values. |
| B | minor | `followup_outputs[telemetry]` | Template telemetry (C12). | FIXED: 4-hour report, sinus rhythm and sinus tachycardia 88-112 bpm, 12 isolated PACs, no sustained arrhythmia, no pauses. |
| D | major | `followup_outputs[literature]` | Anemia literature with "LP gold standard regardless of CT result" and "Hgb 8-10" target, empty summary; criterion recommended (C7). | FIXED: deleted; canonical literature last; criterion `optional`, last. |
| C | major | musts, prohibitions, pearls | 24-72 h securing musts, daily TCD must, generic CTA must, "never IV" nimodipine, BP in the ICU must, CT 98% and LP 6-12 h pearls (C1, C4, C5). | FIXED: MUST-CTA (after the LP), MUST-NIMO, MUST-SECURE left PComA, MUST-ICU, MUST-BP-A (168/98), MUST-HOME (continue metoprolol and levothyroxine, separate iron), transfusion must, sodium must kept, MUST-DCI; canonical prohibitions; CT, LP, securing and DCI pearls replaced, anemia pearl kept. |
| C | minor | `ground_truth.differential` | Template key features ("pituitary MRI", "CT venogram indicated if SAH excluded"). | FIXED: key features cite the CSF and CTA results; all low, migraine very low. |
| A | minor | `ground_truth.action_criteria[*]`, `sequence_constraints`, `stop_rule` | Label-copied rationales, unbracketed duplicate citations, labs-before-CSF constraint `hard` without coagulopathy. | FIXED: canonical rationales and citations (CSF `[Hoh_2023]`, `[Edlow_2008]`); order per plan 3.1; constraints NCCT before CSF hard (kept), labs before CSF soft, NCCT before CTA soft, CTA before DSA soft; stop rule = five required criteria, `max_additional_actions` 1. |

## Changes, in one paragraph a physician can read before re-reviewing

A 62-year-old man with severe iron-deficiency anemia (Hb 7.4 g/dL) and a thunderclap headache 1 hour before arrival. The CT, now written as an imaging report, shows no definite hyperdense blood, subtle basal-cistern effacement and a low blood-pool attenuation that reduces the conspicuity of blood; no lab value or LP advice sits in it. The LP is grossly bloody and non-clearing (68,000 to 65,000/uL) with an oxyhemoglobin peak and, correctly for an LP within hours of onset, no bilirubin yet; the traumatic-tap red herring is answered by the tube counts. CTA shows the 5.8 x 4.4 mm left PComA aneurysm; a recommended catheter DSA confirms its anatomy without treatment content. The TCD is an admission baseline (no transfusion, no day 4). The transfusion step became a must (keep Hb at or above 8 g/dL before securing, SAHaRA), the drug check continues metoprolol and adds the iron-levothyroxine spacing, MRI is optional and matchable, and the literature step is optional and canonical. Musts: LP justified by the anemia, CTA after the LP, nimodipine, securing as early as feasible preferably within 24 hours, ICU, lower BP now (168/98) with a titratable IV agent, home medicines, transfusion, sodium, DCI surveillance.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` is used in the canonical literature output (plan section 5.1b allow-list request).
- Class for the lead: criteria whose `required_arguments` use a parameter the tool schema does not have (`analyze_brain_mri.sequences` here) can never be matched by a real agent, while `perfect_agent.py` passes them because it sends the criterion's own arguments. Worth checking P01 and P03 (same MRI template), and adding a check to `perfect_agent.py` that every required argument key exists in the tool schema.
- Review UI: initial outputs and follow-ups in criterion order (plan section 5.5).

## Open questions for Andrea (judgment calls you could not settle)

- None that need Andrea. The SAHaRA reference (English SW et al., N Engl J Med, published online December 2024) is named in the transfusion must without a bracketed key because it is not on the allow-list; add a key if wanted.

## Verification

Adversarial check (24 Oct 2026). Read the log, the diff and the whole final case. No reviewer notes for this case (confirmed in the notes file). Verified in the file: CSF grossly bloody, non-clearing 68,000 to 65,000/uL, oxyhemoglobin without bilirubin under 12 hours, red herring [2] consistent; CT without lab values or LP essay; transfusion follow-up gone and its content a must (restrictive 8 g/dL threshold, SAHaRA); metoprolol continued, no MAP target; TCD day 0 without the transfusion note; MRI criterion `required_arguments` {} and optional; labs-before-CSF soft, NCCT-before-CSF hard; no `analyze_csf` exemption (CSF is required here); no LP avoided action; stop rule equals the five required criteria; guards pass.
Found and fixed: (1) `ground_truth.red_herrings[0]` was still the condition template ("apical ballooning confirms etiology", "30-40%") while this echo shows mild apical hypokinesis with LVEF 52%: data point now "Troponin I 0.12 ng/mL with T-wave inversions V1-V4 and QTc 468 ms", interpretation cites the echo. (2) The differential says "CTA of the neck shows no dissection" but the CTA report said nothing about the cervical arteries (the worker added this sentence in P07, P08, RM11 and RP11 but not here): added `angiography_findings["Cervical vasculature"] = "No dissection"` and "3. No cervical dissection." to the CTA impression.
perfect_agent.py SAH-P06 -v: pass; case_io.py check: clean for SAH-P06.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `required_recommendations (transfusion must cites [English_2024])`: citation key added for the cited evidence (CENTRAL 5, keys allow-listed in the pack).
- `echo.findings[0]`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `echo.impression (Takotsubo overcall and consultation advice removed)`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `echo.recommended_actions`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `action_criteria[echo].expected_evidence`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `echo.findings[1]`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- fallback_tool_outputs.cardiac_monitoring: 24 h Holter replaced by the case's own telemetry report: a 24-hour Holter cannot exist at assessment time; an off-pathway monitoring order now returns the case's own telemetry (CENTRAL 9).
- followup_outputs: MR angiography report added before the literature output (aneurysm site and size from the DSA, 0.2 mm smaller as TOF reads it; P02 negative): an MRA order was answered by a fallback reporting no abnormality, contradicting the CTA and DSA (CENTRAL 10). MRA stays a waste action after the CTA.
- `ground_truth.diagnosis` (synonyms re-expanded with `--prune`): diagnosis_synonyms.yaml: the I60 category no longer grants I60.8 (non-aneurysmal SAH), so the code was pruned from this aneurysmal case.
- Checks after the close-out: `perfect_agent.py` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards -k SAH-` pass.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- follow-up `request_echocardiogram`: `echo_type` set to `TTE` (was missing); the bedside study is transthoracic, and untyped it also answered a TEE or bubble-study order.
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'No diagnostic abnormality identified on this study.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
