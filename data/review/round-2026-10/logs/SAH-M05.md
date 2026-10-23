# SAH-M05
Reviewer status: R1 none, R2 approved | Approved before this round: yes

Approved case: every change below corrects a real error (plan classes C1 to C14, or a contradiction inside the case).

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| e38a8460-0826-4c02-b86b-27cb655aea7a | FIXED | Magnesium measured: 1.6 mg/dL (L, 1.7-2.2) in `initial_tool_outputs.labs.panels.BMP`, abnormal list and interpretation updated (potassium 3.4, previously missing from the list, added). MUST-QT added: "QTc 524 ms with potassium 3.4 mmol/L, magnesium 1.6 mg/dL and U waves: replete potassium to at least 4.0 mmol/L and magnesium to at least 2.0 mg/dL, avoid adding QT-prolonging drugs ..., continuous ECG monitoring with daily QTc [Drew_2010]". MUST-HOME withholds furosemide (and ramipril). The drug check (`action-7-check-drug-interactions`) is now `required` and its output states the furosemide K/Mg loss with QTc 524 ms and the QT-drug caution. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.mental_status`, `.additional`, `patient.history_present_illness` | Label HH3 while the exam read "Alert and oriented x4; GCS 15 ... mild confusion resolved", the grade was justified by a resolved LOC, and the HPI said "now alert and fully oriented" (C13). | FIXED: HPI "In the ED, she is awake but remains mildly confused."; exam "Awake but confused: oriented to person and place, not to date; GCS 14 (E4V4M6)"; additional "Hunt-Hess Grade 3 (confusion, headache, nuchal rigidity)". |
| D | major | `initial_tool_outputs.ct.additional_observations` | "Multiple PKD-related renal cysts visible on lower cuts": a head CT does not image the kidneys (impossible, C14); "Fisher grade 3-4" contradicts the impression (grade 3, no IVH). | FIXED: kidney line deleted; "Fisher grade 3"; sella and venous-sinus negatives added. |
| B | major | `followup_outputs` TCD | "Day 7" TCD with severe ACA and moderate MCA vasospasm and "new bifrontal headache and mild confusion" in a patient seen hours after onset. | FIXED: day-0 baseline, normal velocities, clinical note removed, canonical text. |
| B | major | `followup_outputs` `request_hyponatremia_management` | "Serum sodium Day 3" panel (128, urine Na 92) cannot exist at assessment time (C2). | FIXED: follow-up deleted; the sodium must stays. |
| C | major | `ground_truth.assessment` | Two 24-72 h musts; ICU must with inline SBP; no BP must (SBP 176) or agent choice for LVEF 38%; generic EVD must; no QT, LVEF or home-drug must; TCD days 4-14 must; misworded nimodipine and BP prohibitions. | FIXED: MUST-NIMO; MUST-SECURE for the AComA aneurysm "first, managing the small unruptured left PComA aneurysm separately"; MUST-ICU; MUST-EVD-NOW "with depressed consciousness"; MUST-BP-A with "nicardipine or clevidipine infusion" (LVEF 38%); MUST-HOME (withhold furosemide and ramipril); MUST-QT; MUST-LVEF (38%); sodium kept; MUST-DCI; canonical prohibitions. |
| C | major | `ground_truth.avoided_actions` `avoid-harm-1-analyze-csf` | `harm` although the CT shows hydrocephalus. | FIXED: `contraindicated`, rationale updated. |
| C | major | `ground_truth.action_criteria` | No DSA before securing (C3). | FIXED: `dsa-aneurysm-anatomy` recommended, follow-up with the AComA aneurysm (8.5 x 6.2 mm, neck 3.4 mm, dome-to-neck 2.5, irregular apical lobule, right A2 at the neck) and the 3.1 mm left PComA aneurysm; CTA before DSA (soft). |
| C | minor | drug-check output | Content was partly management prose ("Furosemide on hold given cerebral salt wasting"). | FIXED: rewritten as interaction findings (see note row) plus contrast and creatinine caution, parenteral warning, 30 mg every 2 h rule. |
| D | minor | `followup_outputs` CTA | "Large" for an 8.4 mm aneurysm (C13); "creatinine 1.2 - contrast nephropathy risk low" cites labs (cross-modality). | FIXED: "Large" removed in findings and impression; observation reduced to "IV contrast CTA"; neck-vessel statement added. |
| D | minor | `initial_tool_outputs.ecg.findings[3]` | "U-waves visible (hypokalemia component)" attributes a lab cause inside the ECG. | FIXED: "U-waves visible". |
| B | major | telemetry output | Template text, 24 h. | FIXED: 4 h, sinus tachycardia 96-122 bpm, 64 PVCs with one couplet, no sustained arrhythmia or pauses, QTc 524 ms without torsades. |
| D | major | literature follow-up `request_pkd_aneurysm_literature`, criterion | Empty summary, recommended literature step. | FIXED: deleted; canonical output last; criterion optional. |
| C | minor | `ground_truth.key_clinical_evidence[-1]` | PKD pearl recommended screening for all first-degree relatives; screening applies to relatives with ADPKD (and family history). | FIXED: "... screening MR angiography is warranted in first-degree relatives who also have ADPKD." |
| C | minor | labs type and screen; differential; pearls; citations; rationales; order; constraints; stop rule; metadata | Template items (C9, C11, C14, section 3). | FIXED: significance null; canonical differential; canonical pearls; bracketed citations; canonical rationales and case evidence; criteria NCCT, labs, ECG, CTA, DSA, drug check, echo, telemetry, TCD, literature; NCCT before CTA and CTA before DSA (soft); stop rule = five required, allowance 1; stale CSF concern emptied; difficulty rationale rewritten. |

## Changes, in one paragraph a physician can read before re-reviewing
50-year-old woman with ADPKD, father died of aneurysmal SAH, on ramipril and furosemide; thunderclap headache with witnessed LOC this morning, now confused with GCS 14 (the exam previously said GCS 15 oriented, which contradicted the HH3 label), Fisher 3 SAH with communicating hydrocephalus, 8.4 mm multilobulated AComA aneurysm plus a 3.1 mm left PComA aneurysm, QTc 524 ms with U waves, potassium 3.4, magnesium now measured at 1.6, LVEF 38% stress cardiomyopathy. The impossible day-7 vasospasm TCD and day-3 sodium panel are gone; the kidney cysts on a head CT are deleted. The pathway adds a diagnostic DSA and a required drug check (furosemide K/Mg loss with QTc 524, ramipril hypotension). Musts now include enteral nimodipine, securing the AComA aneurysm first as early as feasible and preferably within 24 h, neurocritical care, EVD for hydrocephalus with depressed consciousness, nicardipine or clevidipine for BP (LVEF 38%), withholding furosemide and ramipril, K and Mg repletion with QT precautions, a cardiology and neuroanesthesia plan for LVEF 38%, sodium and DCI surveillance. LP is now `contraindicated`.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- As plan section 5 (allow-list `[Drew_2010]`, `[Molyneux_2002]`).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial check (24 Oct 2026), approved case: diff, full final case, perfect-agent `-v`, `case_io.py check`, `test_case_guards -k SAH-M05`.
- Note e38a8460: confirmed FIXED (magnesium 1.6 mg/dL flagged low in BMP, abnormal list and interpretation; potassium 3.4 listed; MUST-QT with K, Mg and U waves; drug check required, in the stop rule, with furosemide K/Mg content).
- Confirmed each change corrects a real error: HPI and exam now support HH3 (GCS 14, confused); kidney cysts on a head CT deleted; Fisher 3 consistent with no IVH; future-dated TCD and sodium panel removed; MUST-EVD-NOW "with depressed consciousness" matches the hydrocephalus; LP `contraindicated`; BP agents without labetalol for LVEF 38%; MUST-LVEF 38%; MUST-SECURE names the ruptured AComA aneurysm first; DSA 8.5 x 6.2 mm vs CTA 8.4 x 6.2 mm, ratio 8.5/3.4 = 2.5, second aneurysm 3.1 mm on both; sulfa allergy compatible with long-standing furosemide; PKD screening pearl correctly narrowed to relatives with ADPKD. No prose churn beyond these.
- No error found; no change made.
