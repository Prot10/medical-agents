# SAH-RM11
Reviewer status: R1 none, R2 approved | Approved before this round: yes

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| a60d0697-5c3c-494b-8000-3df16913057b | FIXED | Securing: both 24-72 h musts replaced by MUST-SECURE for the right MCA bifurcation aneurysm (joint neurosurgical and neurointerventional review, as early as feasible, preferably within 24 hours, `required_recommendations[3]`), pearl `key_clinical_evidence[8]` replaced. DSA: new recommended criterion `dsa-aneurysm-anatomy` and a diagnostic DSA follow-up (`followup_outputs[1]`). Timeline: the "day 6" TCD with moderate vasospasm is now a post-ictus day 0 baseline, so no result runs past the encounter. |
| 2ab931d5-3ccb-4696-80e7-b36636f6ec3a | FIXED | MUST-BP-B (presenting 154/92) and MUST-HOME "Continue propranolol unless bradycardia or hypotension (do not stop abruptly); withhold valsartan during the acute phase." (`required_recommendations[5]`, `[6]`); drug check rewritten with that content (no "hold propranolol"), criterion `recommended` with case-specific label, rationale and evidence. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | minor | `patient.history_present_illness` | "A CT was performed on arrival." (the CT is a scored action). | FIXED: deleted. |
| D | minor | `initial_tool_outputs.ct` | "CT sensitivity still approximately 93% at 6 hours" (teaching text) and "subtle at 6 hours from onset" in a finding (C14); no statement on intraventricular blood. | FIXED: deleted; "No intraventricular hemorrhage" added to observations and impression; LP avoided action stays `harm`. |
| B | minor | `followup_outputs[CTA]` | Differential relies on a neck CTA, but the report was silent on the cervical arteries. | FIXED: "Cervical vasculature: No dissection" added to findings and impression. |
| C | major | `followup_outputs[TCD]` | "Day 6" TCD with moderate right MCA vasospasm (MFV 144, Lindegaard 3.7) in a patient who presented 6 hours after onset (C2). | FIXED: baseline post-ictus day 0 with normal velocities (right MCA 78, left 72 cm/s, Lindegaard 1.9 and 1.8), canonical protocol and recommendation. |
| C | major | `followup_outputs[drug check]` | "Hold propranolol during nimodipine course" and "hold valsartan", nothing to replace them (C5, C10). | FIXED: interactions (propranolol, valsartan with nimodipine), no abrupt beta-blocker withdrawal, valsartan withheld, 30 mg every 2 h option, no parenteral nimodipine. |
| C | minor | `required_recommendations` | Familial aneurysm (she and her brother, two first-degree relatives) named in the diagnosis label, but no must; the family-screening literature that held this content is removed (C7). | FIXED: must for genetic counselling and screening MR or CT angiography of other first-degree relatives after recovery. |
| B | minor | `ground_truth.red_herrings[1]` | Template data point "migraines, chronic headaches, or fibromyalgia"; interpretation claimed a prior migraine diagnosis "raises" SAH risk (not established). The red herring itself is valid here (she has migraine). | FIXED: data point names her migraine and her own first attribution; interpretation corrected; field path to the HPI. |
| B | minor | `ground_truth.red_herrings[0]` | Template wording ("QTc prolongation", "apical ballooning") not matching this case (QTc 462, mild apical hypokinesis, LVEF 50%). | FIXED: values and echo result of this case. |
| B | minor | `initial_tool_outputs.labs` | No potassium, magnesium or PTT (C9); abnormal summary missing glucose and units; type-and-screen engineering sentence (C14). | FIXED: potassium 4.1 mEq/L, magnesium 2.2 mg/dL, PTT 27 s; summary and interpretation list the same four abnormal values; type-and-screen significance null. |
| B | minor | `followup_outputs[telemetry]` | Template telemetry (C12). | FIXED: 4-hour report, sinus rhythm 68-92 bpm, 5 isolated PACs, no sustained arrhythmia, no pauses. |
| D | major | `followup_outputs[literature]` | Family-screening literature with an unverifiable "AHA/ASA" attribution and a truncated summary; criterion recommended (C7). | FIXED: deleted; canonical literature last; criterion `optional`, last. |
| C | major | musts, prohibitions, pearls | Daily TCD must, BP target in the ICU must, "never IV" nimodipine, CT 98% and LP 6-12 h pearls (C4, C5). | FIXED: MUST-NIMO, MUST-ICU, MUST-DCI, sodium must kept; canonical prohibitions; CT, LP and DCI pearls replaced. |
| C | minor | `ground_truth.differential` | Template key features. | FIXED: case results cited (exertional trigger for RCVS; her migraine for thunderclap migraine). |
| A | minor | `ground_truth.action_criteria[*]`, `sequence_constraints`, `stop_rule` | Label-copied rationales, unbracketed citations, no constraints. | FIXED: canonical rationales and citations; order per plan 3.1; NCCT before CTA and CTA before DSA (soft); stop rule = four required criteria, `max_additional_actions` 1. |

## Changes, in one paragraph a physician can read before re-reviewing

A 47-year-old woman with migraine on propranolol, valsartan for hypertension, and a brother with an unruptured aneurysm, seen 6 hours after an exertional thunderclap headache; Fisher 2 SAH and a 5.6 mm lobulated right MCA bifurcation aneurysm. The HPI no longer says a CT was done; the CT loses its sensitivity remark and states no IVH; the CTA states no cervical dissection; a recommended DSA confirms the anatomy (5.8 x 4.8 mm, neck 3.0 mm, inferior M2 incorporated) without treatment content. The TCD is a normal admission baseline instead of a day-6 vasospasm study. The drug check continues propranolol (never stopped abruptly) and withholds valsartan, which the musts repeat. Musts: nimodipine, securing as early as feasible preferably within 24 hours, ICU, BP monitoring with treatment of sustained rises (154/92), home drugs, sodium, DCI surveillance, and family counselling and screening. Labs gain potassium, magnesium and PTT; telemetry is a real report; the literature step is optional and canonical; both red herrings now match this patient.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` used in the canonical literature output (plan section 5.1b allow-list request).
- Review UI: initial outputs and follow-ups in criterion order (plan section 5.5).

## Open questions for Andrea (judgment calls you could not settle)

- None. The family-screening must carries no bracketed citation because the AHA/ASA 2015 unruptured aneurysm guideline is not on the SAH allow-list; add `[Thompson_2015]` centrally if you want it cited.

## Verification

Adversarial check (24 Oct 2026). Read the log, the diff and the whole final case. Both note ids present and verified FIXED: MUST-SECURE with the Hoh window and joint review, DSA criterion and diagnostic-only report (5.8 x 4.8 mm vs CTA 5.6 x 4.8 mm), TCD day 0; MUST-BP-B for 154/92, MUST-HOME continuing propranolol and withholding valsartan, the drug check says the same (no "hold propranolol"). Also verified: HPI no longer says a CT was done; CT without the sensitivity remark, no IVH, LP `harm`; CTA states no dissection; both red herrings match this patient (migraine on propranolol; troponin 0.14, BNP 156, LVEF 50%); aspirin allergy does not conflict with any must; family-screening must is consistent with the case (patient and brother affected, two first-degree relatives); stop rule equals the four required criteria; guards pass.
Nothing found that needed a change.
perfect_agent.py SAH-RM11 -v: pass; case_io.py check: clean for SAH-RM11.

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `required_recommendations (family screening must cites [Thompson_2015])`: citation key added for the cited evidence (CENTRAL 5, keys allow-listed in the pack).
- `echo.findings[0]`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- `echo.wall_motion`: an echo reports the wall-motion pattern; a mild apical hypokinesis with preserved EF is not Takotsubo, grading labels such as 'classic' or 'severe Takotsubo' are diagnoses, and cardiology consultation is management (Q10).
- fallback_tool_outputs.mri: SAH-consistent brain MRI instead of the library normal report: an off-pathway brain MRI was answered by the library normal report (no blood on SWI), contradicting the CT; the case fallback now reports the CT's blood on FLAIR and SWI (CENTRAL 10).
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
