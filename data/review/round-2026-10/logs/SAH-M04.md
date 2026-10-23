# SAH-M04
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 03a9ce4b-c764-4ad9-8a57-d602ddd39600 | FIXED | Option "score the reasoning" taken. RCVS key feature now names the coital trigger and the discriminators in this case (basal-cistern blood, saccular right PComA aneurysm on CTA) (`ground_truth.differential[0]`); new red herring "Headache onset during sexual intercourse" (`patient.history_present_illness`) whose correct interpretation is that coital onset also triggers aneurysmal rupture and that the cisternal blood plus saccular aneurysm without segmental vasoconstriction establish aneurysmal SAH. Likelihood kept `low`: ruling 7 makes the differential the assessment-time view, and the work-up (cisternal SAH, saccular aneurysm, DSA without segmental narrowing) excludes RCVS. |
| 53d4e407-16bc-4eec-ac9f-b80ac3b63e99 | FIXED | Both 24-72 h securing musts replaced by one MUST-SECURE (right PComA, as early as feasible, preferably within 24 h [Hoh_2023]); the 24-72 h pearl replaced by the canonical securing pearl. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `initial_tool_outputs.ct.impression`, `.recommended_actions` | A positive CT recommended lumbar puncture (LP is an avoided action once CT shows SAH). | FIXED: impression ends "CT angiography of the head and neck recommended"; recommended action changed to CTA. |
| D | minor | `initial_tool_outputs.ct.additional_observations` | "Blood may be near-isodense in higher Hgb patient - but Hgb normal here" cites labs (cross-modality) and is commentary. | FIXED: removed; added "No parenchymal hematoma", sella and venous-sinus negatives, and the comparison line for the outside CT reported in the HPI. |
| C | major | `ground_truth.action_criteria` | No catheter angiography before securing (C3). | FIXED: new recommended `dsa-aneurysm-anatomy` and follow-up `request_digital_subtraction_angiography` (6.3 x 5.1 mm lobulated right PComA-origin aneurysm, neck 3.4 mm, dome-to-neck 1.9, PComA from the neck, anterior choroidal separate, no other aneurysm, no vasospasm or segmental narrowing); soft constraint CTA before DSA. |
| B | major | `followup_outputs` TCD | "Day 6" TCD with borderline right MCA vasospasm in a patient 5 h from onset. | FIXED: day-0 baseline, normal velocities, canonical text. |
| C | major | drug-check output | "Hold metoprolol if ... bradycardia" only, "Never give IV" wording; metformin and contrast not addressed although the plan expects it. | FIXED: metoprolol additive hypotension and bradycardia with no abrupt withdrawal; metformin around iodinated contrast with creatinine 1.1 (no need to stop for contrast alone, commonly held while acutely ill or nil by mouth); atorvastatin no interaction; parenteral-injection and 30 mg every 2 h statements. Tier recommended; rationale and evidence case-specific. |
| C | major | `ground_truth.assessment` | No BP action (SBP 182), no home-drug decision, misworded nimodipine and BP prohibitions, TCD days 4-14 must. | FIXED: MUST-NIMO, MUST-SECURE, MUST-ICU, MUST-BP-A (default agents), MUST-HOME "Continue metoprolol succinate unless bradycardia or hypotension, without abrupt withdrawal", sodium kept, MUST-DCI; canonical prohibitions. |
| D | major | literature follow-up `request_family_screening` and criterion | Family-screening output as a pathway step; literature recommended. | FIXED: follow-up deleted; canonical output last; criterion optional, last, canonical text. |
| B | major | telemetry output | Template text, 24 h. | FIXED: 4 h, sinus 80-108 bpm, 11 PVCs, no sustained arrhythmia or pauses, QTc 488 ms without torsades. |
| B | minor | `followup_outputs` echo `findings[1]` | "EF mildly reduced 54%"; 54% is within the normal male range (ASE). | FIXED: "LVEF 54% (low-normal)"; impression (mild apical hypokinesis, stress pattern) unchanged. |
| B | minor | `ground_truth.red_herrings` | The HPI's outside negative CT and near-discharge are a real anchoring trap with no entry; metadata named it. | FIXED: red herring added (outside read negative; repeat NCCT shows the blood, so CTA next, no LP). |
| C | minor | `initial_tool_outputs.labs` | No magnesium; type-and-screen engineering sentence. | FIXED: magnesium 2.0 mg/dL; significance null. |
| B | minor | CTA | No neck-vessel statement. | FIXED: cervical vessels patent, no dissection. |
| C | minor | differential, pearls | Generic key features; outdated pearls. | FIXED: canonical C11 entries; canonical pearls. |
| A | minor | citations, rationales, order, constraints, stop rule, `metadata.difficulty_rationale` | As in the condition template. | FIXED: bracketed keys; canonical rationales and case evidence; criteria NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD, literature; NCCT before CTA and CTA before DSA (soft); stop rule four required, allowance 1; rationale rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing
55-year-old man with poorly controlled hypertension, diabetes and a sister with an unruptured aneurysm; explosive coital headache 5 h before arrival, outside CT read negative, HH2, very subtle Fisher 2 SAH here, 6.2 mm lobulated right PComA aneurysm, SBP 182. The CT no longer recommends LP (it recommends CTA). The coital trigger is now in the RCVS key features and a red herring that scores the discriminating reasoning; RCVS stays low because the work-up excludes it. The pathway is NCCT, labs (magnesium added), ECG, CTA, a new diagnostic DSA, the nimodipine check (metoprolol continued, metformin around contrast), echo, 4 h telemetry, a day-0 baseline TCD, and the canonical literature last (optional). Musts follow the plan: enteral nimodipine with the 30 mg every 2 h rule, securing as early as feasible and preferably within 24 h, neurocritical care, IV titratable BP lowering, continue metoprolol, sodium and DCI surveillance.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- As plan section 5 (allow-list `[Molyneux_2002]`).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial check (24 Oct 2026): diff, full final case, perfect-agent `-v`, `case_io.py check`, `test_case_guards -k SAH-M04`.
- Note 03a9ce4b: confirmed FIXED (coital trigger in the RCVS key features, new red herring with the plan's wording, RCVS kept `low` per ruling 7). Note 53d4e407: confirmed FIXED (one MUST-SECURE, canonical pearl, no 24-72 h text).
- Confirmed: CT now recommends CTA, not LP; Hgb commentary removed; DSA 6.3 x 5.1 mm vs CTA 6.2 x 5.1 mm, ratio 6.3/3.4 = 1.9; TCD day 0 with a right extracranial ICA velocity that gives the stated right Lindegaard ratio (88/38 = 2.3); metoprolol continued (MUST-HOME) consistent with the drug check; MUST-BP-A fits SBP 182 and LVEF 54%.
- Found and FIXED: `initial_tool_outputs.ecg` called a rate of 98 "Sinus tachycardia" (same template error as SAH-M01; vitals HR 96): rhythm and interpretation now "Sinus rhythm, rate 98"; ECG criterion evidence updated.
- Found and FIXED: the RCVS red herring and DSA rely on "no segmental vasoconstriction", but the required CTA was silent on it: added `angiography_findings["Intracranial arteries"]` "No segmental narrowing or beading" to the CTA output, so the discriminator is available from the required work-up.
- Both checks clean after the edits.


## Condition audit (auditor, 24 Oct 2026)

- `ground_truth.red_herrings[0].correct_interpretation` still carried the condition template "echocardiogram showing apical ballooning confirms etiology", while this echo shows only mild apical hypokinesis (LVEF 54%). Now ends "...the echocardiogram shows only mild apical hypokinesis with an LVEF of 54% and no primary cardiac lesion, and the focus remains on aneurysm securing." Same fix as the verifiers made in S01, S04, P05 and P06.
- MUST-HOME now "Continue metoprolol succinate unless bradycardia or hypotension, without abrupt withdrawal; hold metformin while in critical care and treat hyperglycemia (glucose 198 mg/dL) with insulin, avoiding hypoglycemia; continue atorvastatin." The must decided only metoprolol although the patient also takes metformin and atorvastatin and has glucose 198; the wording matches the home-drug musts of S02, RS12 and S09 (metformin held for critical illness, not for contrast alone).
- Checks after the audit: `perfect_agent.py` 30/30 pass; `case_io.py check` schema and synonym guard OK, no test failure names an SAH case; `test_case_guards -k SAH` 60 passed.
