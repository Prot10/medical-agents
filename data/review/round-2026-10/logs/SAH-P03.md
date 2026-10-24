# SAH-P03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 6dcebd64-48c0-46a6-a73b-ee217f8282d3 | FIXED | Substance applied (secure urgently) with the governing window, not the note's "24-72 hours" ([Hoh_2023]: as early as feasible, preferably within 24 hours of onset, COR 1). Both 24-72 h musts were replaced by one MUST-SECURE naming the left posterior communicating artery aneurysm (`required_recommendations[3]`), and the securing pearl was replaced. A recommended DSA criterion `dsa-aneurysm-anatomy` was added with a diagnostic DSA follow-up. The TCD was re-dated from day 4 to an admission baseline (day 1), so no result post-dates an unsecured aneurysm. |
| 7e2fa463-1268-46d7-8024-5ab90b39acb0 | ALREADY-FIXED (LP required); numbers FIXED | `action-3-analyze-csf` was already `required` after the negative CT. The CT and LP pearls were replaced by the canonical text (close to 100% within 6 h, falling after 6 h; LP after a negative CT when presenting more than 6 hours after onset; bilirubin needs about 12 hours). The note's figure "80-85% by 24 hours" is not written as a number, per plan 1.2. The LP must now gives the 18 h timing and the 12 h bilirubin fact. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.mental_status` | "Alert and oriented x4; GCS 15 ... mildly drowsy" next to a Hunt-Hess 2 label (drowsiness is grade 3). | FIXED: "reports feeling tired after a poor night's sleep" (alert, GCS 15), consistent with grade 2. |
| B | major | `initial_tool_outputs.csf.appearance` | "no fresh blood" with 24,000 RBC/uL in tube 1 (visibly blood-stained at that count). | FIXED: "Uniformly blood-tinged in tubes 1 to 4; centrifuged supernatant yellow (xanthochromic)"; spectrophotometry as a value (net bilirubin absorbance 0.024 AU, oxyhemoglobin present); interpretation as a pattern, no "12-24 hours prior" verdict. |
| D | minor | `initial_tool_outputs.ct` | Sensitivity essay in the impression and observations (C14). | FIXED: plain negative impression ending "Lumbar puncture recommended if clinical suspicion persists."; the equivocal sulcal-effacement observation kept. |
| C | major | drug check | "Duloxetine has mild QT-prolonging effects" (the thorough QT study showed no clinically relevant QTc prolongation); "Current QTc 472 ms - monitor" (patient verdict); no codeine-allergy or serotonergic content. | FIXED: rewritten as `request_nimodipine_duloxetine_interaction_check`: no PK interaction, serotonergic cyclobenzaprine plus duloxetine, SNRI bleeding effect, withdrawal, sedation, codeine intolerance. Criterion accepts `drug: nimodipine` or `drug: duloxetine`, `recommended`. New home-drug must. |
| C | major | literature follow-up | "Ottawa SAH rule does not exclude patients with prior headache history" (wrong: recurrent similar headaches are an exclusion); literature `recommended`. | FIXED: deleted; criterion `optional`; canonical output last. |
| C | major | `ground_truth.red_herrings[0]` | Interpretation claims an echo with apical ballooning; this echo is normal (LVEF 58%). | FIXED: data point names the values; interpretation says the echo shows normal wall motion. |
| C | minor | `ground_truth.red_herrings[2]` | Template "in a known migraineur" (she has chronic headaches and fibromyalgia, not migraine). | FIXED: specific data point and interpretation (neck stiffness attributed to fibromyalgia). |
| B | minor | `ground_truth.red_herrings[3]` | Pointed to the appearance field; now the counts carry the evidence. | FIXED: field path `initial_tool_outputs.csf.cell_count`, values named. |
| D | major | MRI follow-up | One-line teaching sentence copied from the criterion's expected evidence. | FIXED: real report (FLAIR hyperintensity and susceptibility effect in the left Sylvian fissure and suprasellar cistern; no parenchymal lesion or hydrocephalus); criterion `optional` (C16). |
| B | major | TCD | "Day 4" with mild left MCA vasospasm, 18 hours after onset; protocol named MCA only. | FIXED: post-ictus day 1 baseline, normal velocities, canonical protocol. |
| C | major | telemetry | Template text, 24 h. | FIXED: 4 h of sinus rhythm with 9 PACs. |
| C | minor | echo follow-up | "Repeat echo in 4-6 weeks recommended" after a normal study. | FIXED: removed; `echo_type` TTE. |
| C | major | labs | No potassium, magnesium or PTT although the criterion orders coagulation; "Exclusion studies" BNP as text with engineering sentence; summary interpretive and missing glucose. | FIXED: potassium 3.9, magnesium 2.2, PTT 29 s added; BNP 64 pg/mL in Cardiac; factual summary; type and screen `clinical_significance` null. |
| C | major | musts | Two 24-72 h musts; CTA "after positive non-contrast CT" in a CT-negative case; ICU with an SBP target; TCD days 4-14. | FIXED: LP must, MUST-CTA (LP version), MUST-SECURE, MUST-NIMO, MUST-ICU, MUST-BP-B (158/94), home-drug must, sodium, MUST-DCI. |
| C | minor | differential | RCVS `moderate` after xanthochromia and an aneurysm; template key features. | FIXED: RCVS `low`; primary headache `very_low`; others cite the case's results. |
| A | minor | criteria, constraints, stop rule | No DSA; free-text citations; template rationales; labs before LP `hard` without coagulopathy; 0 extra actions. | FIXED: DSA follow-up (4.7 x 3.8 mm, neck 2.9 mm, patent non-fetal PComA, anterior choroidal separate); plan 1.3 rationales; labs before LP `soft`, NCCT before LP `hard` kept, NCCT before CTA and CTA before DSA `soft`; `max_additional_actions` 1; criteria reordered NCCT, labs, ECG, CSF, CTA, DSA, MRI, drug, echo, telemetry, TCD, literature. |
| E | minor | `metadata.difficulty_rationale` | Template list of other cases' features. | FIXED: case-specific. |

## Changes, in one paragraph a physician can read before re-reviewing

The exam is now consistent with Hunt-Hess 2 (tired but alert). The CT at 18 hours is a plain negative report recommending LP. The CSF is blood-tinged in all tubes with non-clearing counts (24,000 to 21,000/uL), a xanthochromic supernatant and a bilirubin peak. CTA then shows the left PComA aneurysm, and a new diagnostic DSA confirms it (patent non-fetal PComA at the neck base). MRI is optional and is now a real report. TCD is an admission baseline. The drug check is now correct: duloxetine has no meaningful QT effect but raises bleeding and serotonergic concerns with cyclobenzaprine, and codeine is not tolerated. The musts are: LP and CTA; securing as early as feasible, preferably within 24 hours; nimodipine; neuro-ICU; BP monitoring; continuing duloxetine, holding cyclobenzaprine, and analgesia without codeine or NSAIDs; sodium; and DCI surveillance. The red herrings match this patient: normal echo, chronic headache with fibromyalgia, and non-clearing blood.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `[Molyneux_2002]` in the canonical literature output needs the criteria-pack allow-list (plan 5.1).

## Open questions for Andrea (judgment calls you could not settle)

- None specific to this case.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, plan section 4 P03 and the whole final case.

Checked: both note ids present and fixed in the file (single MUST-SECURE with the Hoh window, which is still reachable at 18 h; LP required with the canonical CT and LP pearls; the LP must cites the 18 h timing and 12 h bilirubin fact). Exam now Hunt-Hess 2 (alert, GCS 15); CSF consistent (uniformly blood-tinged, 24,000 to 21,000/uL, xanthochromic, bilirubin 0.024 AU) and its traumatic-tap red herring matches the counts; Ottawa literature deleted; duloxetine check correct (no meaningful QT effect; serotonergic cyclobenzaprine; codeine intolerance consistent with the allergy list) and its alternative argument matches the trigger; home-drug must consistent with the check; MRI optional and a real report; CTA 4.6 mm and DSA 4.7 mm agree; TCD day 1 normal; PTT added for the coagulation panel the criterion orders; constraints and stop rule per plan 3.3 and 3.4; RCVS `low`; BP 158/94 gets MUST-BP-B. Leak guards pass.

Found: nothing requiring a change.

Re-ran `perfect_agent.py SAH-P03 -v` (pass) and `case_io.py check` (no failure names the case).

## Close-out (24 Oct 2026)

Condition close-out after Andrea's ruling of 24 Oct 2026 (open questions decided for dataset quality); decisions and sources in `plans/SAH-decisions.md`.

- `ground_truth.key_clinical_evidence` (late-presentation pearl removed): the 'Late presentation (>24 h) ... xanthochromia persists for weeks' pearl misstated the 6-hour threshold and the two-week persistence and duplicated the canonical CT and LP pearls (Q11).
- fallback_tool_outputs.cardiac_monitoring: 24 h Holter replaced by the case's own telemetry report: a 24-hour Holter cannot exist at assessment time; an off-pathway monitoring order now returns the case's own telemetry (CENTRAL 9).
- followup_outputs: MR angiography report added before the literature output (aneurysm site and size from the DSA, 0.2 mm smaller as TOF reads it; P02 negative): an MRA order was answered by a fallback reporting no abnormality, contradicting the CTA and DSA (CENTRAL 10). MRA stays a waste action after the CTA.
- `ground_truth.diagnosis` (synonyms re-expanded with `--prune`): diagnosis_synonyms.yaml: the I60 category no longer grants I60.8 (non-aneurysmal SAH), so the code was pruned from this aneurysmal case.
- Checks after the close-out: `perfect_agent.py` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards -k SAH-` pass.
