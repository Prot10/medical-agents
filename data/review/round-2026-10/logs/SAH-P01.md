# SAH-P01
Reviewer status: R1 none, R2 approved | Approved before this round: yes

Approved case: every change below corrects a real error (a condition-wide class of plan section 2, or a fact that is wrong in this file); correct prose was left as it was.

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 532566ea-2694-40ee-9bf0-47b36a5faeb9 | FIXED | The misattributed thunderclap headache is the lesson of the case: pearl added at `key_clinical_evidence[1]`: "A sudden, peak-in-seconds headache needs immediate non-contrast CT even in a known migraineur; attributing it to migraine delays the diagnosis by days, when CT is far less sensitive." The migraine red herring is kept (valid here; she has migraine with aura) and made specific (`red_herrings[1].data_point`). The differential entry for primary headache now cites the instantaneous onset unlike her usual migraines. |
| 348b8e71-1c5a-4836-9f2c-85fa43775648 | FIXED | CT sensitivity pearl replaced by the canonical text (close to 100% within 6 h; falls after 6 h and markedly by days 5 to 7). The note's figure "50 to 85% by days 5 to 7" is not written as a number, because the plan's canonical fact avoids unverifiable point estimates. The CT report keeps a plain negative impression ending with the LP recommendation; the sensitivity essay in its impression and `additional_observations[3]` was removed (C14). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | minor | `patient.history_present_illness` | "asked her to come to the ED for CT and LP" tells the agent the work-up. | FIXED: "for urgent evaluation". |
| B | major | `initial_tool_outputs.csf.appearance`, `.cell_count`, `.interpretation` | "Xanthochromic (yellow-tinged) ... clear in all 4 tubes" is self-contradictory; RBC "consistent with xanthochromia" and an interpretive comment inside the cell counts. | FIXED: appearance "Clear in all 4 tubes, without visible blood; centrifuged supernatant faintly yellow"; plain counts; spectrophotometry stated as a value (net bilirubin absorbance 0.038 AU, positive above 0.007); interpretation as a pattern statement. |
| C | minor | `ground_truth.red_herrings[2]` | "Bloody CSF in tube 1" contradicts a tube 1 RBC of 12/uL. | FIXED: replaced by the near-normal RBC red herring (plan), field path `initial_tool_outputs.csf.cell_count`. |
| C | minor | MRI follow-up | "Hemosiderin staining" at day 5 (hemosiderin takes longer to form); teaching sentence on FLAIR sensitivity. | FIXED: susceptibility effect on GRE/SWI with FLAIR hyperintensity, consistent with subacute SAH; teaching sentence removed. MRI criterion `optional` (the LP is diagnostic, C16). |
| D | minor | CTA `angiography_findings` | "likely the ruptured aneurysm given late-presentation SAH" (clinical synthesis). | FIXED: removed; cervical arteries line added (no dissection). |
| B | major | TCD follow-up | Lindegaard ratio quoted for the ACA (the ratio is MCA/ICA); protocol named MCA only; "Daily TCD monitoring". | FIXED: admission baseline, post-ictus day 5, MCA 98/104 cm/s, Lindegaard 2.4/2.6, ACA borderline, basilar normal; canonical protocol. |
| C | major | telemetry follow-up | Template "neurogenic changes; rare malignant arrhythmias warrant intervention", 24 h. | FIXED: 3 h of sinus rhythm 61 to 88/min, no ectopy. |
| C | major | labs | No potassium or magnesium; "Exclusion studies" BNP and "Mimic exclusion" troponin as text with engineering sentences ("which is what this case's diagnosis rests on"). | FIXED: potassium 4.1 and magnesium 2.0 added; panels deleted; Cardiac panel with troponin I <0.01 ng/mL and BNP 38 pg/mL; type and screen `clinical_significance` null. |
| C | major | drug check | Answered a sumatriptan request but the criterion ordered nimodipine; the topiramate, lorazepam and NSAID points were not tied to a decision. | FIXED: one follow-up `request_nimodipine_sumatriptan_interaction_check` (triptan avoided after SAH, NSAIDs avoided, sedation, topiramate taper); criterion accepts `drug: nimodipine` or `drug: sumatriptan`, stays `recommended`. |
| C | major | musts | Two 24-72 h securing musts; CTA must "after positive non-contrast CT" although the CT is negative; LP must "6-12 h"; no securing step; TCD days 4-14 must; no home-drug decision. | FIXED: LP must with the 12 h bilirubin fact; MUST-CTA (LP version); MUST-SECURE (AComA); MUST-NIMO; MUST-ICU; MUST-BP-B (118/72); triptan/analgesia must; sodium; MUST-DCI. |
| C | minor | differential | RCVS `moderate` after xanthochromia and an aneurysm; template key features. | FIXED: RCVS `low`; primary headache `very_low`; dissection, CVST and SIH cite this case's results. |
| A | minor | criteria | No DSA; literature `recommended`; rationale copied from labels; free-text citations. | FIXED: `dsa-aneurysm-anatomy` (recommended) with a diagnostic DSA follow-up (3.5 x 2.8 mm, neck 2.1 mm, dominant right A1, single aneurysm, no vasospasm); literature `optional`, canonical output last; xanthochromia literature (which said LP is mandatory "regardless of time") deleted; criteria reordered NCCT, labs, ECG, CSF, CTA, DSA, MRI, drug check, telemetry, TCD, literature. |
| B | minor | `sequence_constraints`, `stop_rule` | Labs before LP `hard` without a coagulopathy; no CTA constraints; stop rule allowed 0 extra actions. | FIXED: labs before LP `soft`; NCCT before CTA and CTA before DSA `soft`; NCCT before LP stays `hard`; `max_additional_actions` 1. |
| E | minor | `metadata.difficulty_rationale` | Template listing other cases' features ("perimesencephalic, ... postpartum/eclampsia, IIH overlap"). | FIXED: case-specific. |

## Changes, in one paragraph a physician can read before re-reviewing

The case still turns on a thunderclap headache misattributed to migraine, with a negative CT on day 5. The CSF report is now internally consistent: clear tubes with a faintly yellow supernatant, RBC 12 and 8/uL, and a spectrophotometric bilirubin peak (0.038 AU). It is followed by CTA of a small irregular AComA aneurysm and a new diagnostic DSA. MRI is optional and describes susceptibility effect rather than hemosiderin. TCD is an admission baseline on day 5 with borderline velocities and no vasospasm, and telemetry shows 3 hours of sinus rhythm. The labs gain potassium, magnesium and numeric troponin and BNP. The musts now secure the AComA aneurysm as early as feasible, preferably within 24 hours, and give nimodipine, neuro-ICU, BP monitoring, no triptan or NSAID, sodium and DCI surveillance. A new pearl states the migraine-misattribution lesson. RCVS is now `low`.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` in the canonical literature output needs the criteria-pack allow-list (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, plan C1 to C16 and section 4 P01, and the whole final case (approved case: checked that every change corrects a real error).

Checked: both note ids present and fixed in the file (migraine-misattribution pearl and specific red herring; canonical CT pearl, plain negative CT impression ending with the LP recommendation). CSF now internally consistent (clear tubes, faintly yellow supernatant, RBC 12 and 8/uL, net bilirubin absorbance 0.038 AU against the 0.007 AU threshold); red herring on near-normal RBC matches the counts; HPI no longer prescribes CT and LP; MRI optional and without day-5 hemosiderin; CTA (3.4 mm) and DSA (3.5 mm) agree; TCD day 5 borderline without vasospasm; labs add potassium, magnesium, numeric troponin and BNP; drug check with sumatriptan alternative matches its trigger; constraints (NCCT before LP hard, labs before LP soft, CTA before DSA soft) and stop rule correct; RCVS `low`. Leak guards pass.

Found and fixed: MUST-SECURE told the agent to secure "preferably within 24 hours of onset" in a patient who presents on day 5, an instruction that cannot be followed. Reworded (`ground_truth.assessment.required_recommendations[3]`): "... secure the ruptured anterior communicating artery aneurysm by endovascular coiling or microsurgical clipping as early as feasible once it is identified [Hoh_2023]; she presents on day 5, beyond the preferred 24-hour window and within the vasospasm period, which does not justify deferring treatment; the technique is chosen jointly from the aneurysm anatomy and the patient's condition."

Re-ran `perfect_agent.py SAH-P01 -v` (pass) and `case_io.py check` (no failure names the case).

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `patient.neurological_exam.additional (Hunt-Hess grade removed)`: the Hunt-Hess grade is a SAH grading scale, so stating it in the patient block presupposes the diagnosis and does the agent's grading (decision Q8).
- `ground_truth.key_clinical_evidence` (late-presentation pearl removed): the 'Late presentation (>24 h) ... xanthochromia persists for weeks' pearl misstated the 6-hour threshold and the two-week persistence and duplicated the canonical CT and LP pearls (Q11).
- fallback_tool_outputs.cardiac_monitoring: 24 h Holter replaced by the case's own telemetry report: a 24-hour Holter cannot exist at assessment time; an off-pathway monitoring order now returns the case's own telemetry (CENTRAL 9).
- followup_outputs: MR angiography report added before the literature output (aneurysm site and size from the DSA, 0.2 mm smaller as TOF reads it; P02 negative): an MRA order was answered by a fallback reporting no abnormality, contradicting the CTA and DSA (CENTRAL 10). MRA stays a waste action after the CTA.
- `ground_truth.diagnosis` (synonyms re-expanded with `--prune`): diagnosis_synonyms.yaml: the I60 category no longer grants I60.8 (non-aneurysmal SAH), so the code was pruned from this aneurysmal case.
- Checks after the close-out: `perfect_agent.py` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards -k SAH-` pass.
