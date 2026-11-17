# SYNC-CARD-M03

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-6-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: split followup_outputs[6] (analyze_brain_mri, trigger request_brain_mri, an unflagged report whose only gadolinium content was negative enhancement statements) into the plain study (contrast_used false, same slot and trigger) and the unchanged gadolinium study (contrast_used true, trigger request_brain_mri_with_contrast, right after it). Plain copy: observation 'No enhancing lesions' removed; impression 'No acute infarction, hemorrhage, mass, or enhancing lesion' -> 'No acute infarction, hemorrhage, or mass'; white matter, DWI and volume findings kept. The case has no brain MRI criterion: the MRI is an off-pathway study scored by a waste avoided action with empty required_arguments (ESC 2018 Class III, brain imaging not indicated in syncope without focal signs), which matches plain and contrast orders alike, so no criterion, evidence, stop rule or sequence constraint changed. Probe: plain order gets the plain copy (gad_text=n), contrast order the gadolinium study, either order, no library answer; perfect_agent passes.
- MRI-CONTRAST verified: checked the plain copy free of gadolinium content and internally consistent, the gadolinium copy identical to the base report apart from contrast_used true, contrast_used per the decision (no stored gadolinium study left null), mri_probe (plain, contrast and both orders in either sequence answered by the case, never the library), pathway order sensible, nothing outside the MRI split changed versus 393c547e (programmatic diff), perfect_agent -v passes, case_io check clean for this case; no brain MRI criterion (waste avoided action with empty required_arguments, ESC 2018 Class III), so no criterion argument to set; case fallback MRI null. No error found.

## Reviewer notes
Reviewer status: R2 needs_changes | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| NB-87M:SYNC-CARD-M03:policy_verdict | FIXED (useless, not harmful, for coronary angiography) | Nomenclature (C4): `followup_outputs[1]` and `fallback_tool_outputs.cardiac_monitoring` findings/events[1], impression item 2, rhythm_summary: "2:1 second-degree AV block"; `followup_outputs[5]` (exercise) findings[5] and impression, `followup_outputs[10]` (exercise echo) findings[2] and impression: "high-grade AV block with 3:1 conduction in early recovery"; `assessment.required_recommendations[0]` "Recognise paroxysmal complete, high-grade and 2:1 AV block ..."; `action_criteria[5].expected_evidence` "intermittent 2:1 AV block". Labels (C3): new `avoid-waste-coronary-angiography` (waste, eGFR about 65, ACR-NKF 2020: not harm, D5), `avoid-waste-bubble-study`, `avoid-waste-exercise-echo` (waste, as `avoid-waste-5-exercise-stress-test`), `avoid-waste-emg-ncs`. accepted[0] already said "high-grade": unchanged. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | `ground_truth.avoided_actions` (new `avoid-waste-electrophysiology-study`, `avoid-waste-coronary-cta`, `avoid-waste-polysomnography`, `avoid-waste-tee`) | Class C3: the stored "not performed" EPS report and the fallback coronary CTA, polysomnography (OSA known, on CPAP) and TEE answered orders with no label | FIXED (waste, canonical rationales) |
| C | minor | `ground_truth.assessment.required_recommendations[5]` | Class C5: driving interval attributed to the ESC 2018 main text | FIXED (DR-PM text; CENTRAL C2 `[ESC_2018_PI]`) |
| C | minor | `ground_truth.diagnosis.accepted[1-3]` | Synonyms "mobitz ii", "mobitz type ii", "mobitz 2" credit an answer the case no longer supports | FLAGGED (CENTRAL C1a: remove for M03; a 2:1 AV block label would also help) |
| A | minor | `followup_outputs` order | Already diagnostic core first (TTE, telemetry, CMR, drug check), off-pathway last | no change |
| E | minor | `metadata.revision_reason`, `metadata.last_revised` | Updated | FIXED |

## Changes
AV block terms now follow the ACC/AHA/HRS 2018 definitions: telemetry (and its identical fallback) reports three episodes of 2:1 second-degree AV block alongside the transient complete heart block, and the exercise test and exercise echo report high-grade AV block with 3:1 conduction in early recovery; R0 now reads "Recognise paroxysmal complete, high-grade and 2:1 AV block on a background of trifascicular conduction disease as the cause of the syncope" and the monitoring evidence says "intermittent 2:1 AV block". The diagnosis label was already "high-grade" and is unchanged. Studies with no indication for this patient are now labelled waste: invasive coronary angiography and coronary CTA (no ischaemic feature; eGFR about 65 is not a material contrast risk, so waste rather than harm), bubble study, exercise echo (as the exercise test, which stays waste because only presyncope, not syncope, was exertional), nerve conduction studies, electrophysiology study, polysomnography (OSA known) and TEE. The driving must cites the ESC 2018 Practical Instructions (Group 1 after 1 week, Group 2 after device function is confirmed, national rules).

CENTRAL: C1a (remove or scope the Mobitz synonyms for M03); C2 `[ESC_2018_PI]`, `[ACR_NKF_2020]`.

## Verification
Pass 1: 0 errors found
- Checked C4 terms (telemetry 2:1, exercise and exercise echo high-grade 3:1), R0, monitoring evidence, the C3 labels (coronary waste at eGFR 65, bubble, exercise echo as the exercise test, EMG/NCS, EPS, CTA, polysomnography, TEE) and DR-PM; perfect_agent -v and test_case_guards pass.
Cosmetic (not counted): `avoid-waste-emg-ncs` rationale said "a known diabetic neuropathy" though no neuropathy is listed in the history; now "a length-dependent diabetic neuropathy" (the exam finding).
Pass 2: 0 errors found
- Focused verifier: no change was made after Pass 1 (0 errors), so nothing was left unverified. Re-ran perfect_agent -v and test_case_guards: both pass.
