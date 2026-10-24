# ISCH-STR-P03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 0f2a9dec-c636-4b95-a5bc-ec7694b45a40 | FIXED | `patient.neurological_exam.additional`: NIHSS 7 itemised (face 1, left arm 2, left leg 2, sensory 1, extinction 1, ataxia 0 because testing is limited by weakness); the total 7 is repeated in the LKW must and key evidence item 1. |
| b331962d-0b79-4ffa-91f4-8e501dcc8bb1 | FIXED | New TEE follow-up (`followup_outputs[4]`, trigger `request_tee_echocardiogram`, `echo_type` TEE): 1.8 x 0.7 cm pedunculated mobile vegetation, moderate AR without perforation, no perivalvular abscess, pseudoaneurysm or fistula, intact septum. TTE kept (`followup_outputs[3]`, trigger `request_tte_echocardiogram`). New criterion `tte-vegetation-screen` (TTE, required) before `action-9-order-echocardiogram` (TEE, required), soft constraint TTE before TEE. Pearl, must and key evidence reconciled on ESC 2023: TEE recommended even after a positive TTE, to detect perivalvular complications. |
| 0c5ef38d-d59a-4535-9fd0-8b2e8c3ad30a | FIXED | `past_medical_history[2]` and the HPI: a single 2 g amoxicillin dose was prescribed before the extraction and not taken; the 7-day course and the bleeding rationale removed. Key evidence item 7, pearl 3, red herring 1 and a must state that prophylaxis is not recommended for a bicuspid valve without previous IE (AHA 2021 statement) and that he is now in the highest-risk group. |
| 7d003b88-4040-4cdb-815a-694e2576d3d5 | FIXED | Pre-IVT BP and door-to-needle musts removed; template antiplatelet/anticoagulation/statin must replaced by "Do not start antiplatelet or anticoagulant therapy for the stroke ..."; telemetry must now gives the reason (new AV block or PR prolongation signals a perivalvular abscess). Telemetry criterion `monitor_type` telemetry (alternatives holter_24h, holter_48h). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness` | "His roommate, who was visiting" while he lives alone. | FIXED: "A friend who was visiting called 911." |
| B | major | `patient.physical_exam` (absent) | Differential and red herrings relied on a "new murmur" that no exam recorded. | FIXED: cardiovascular exam added (early diastolic murmur at the left sternal border, ejection systolic murmur, bounding pulses), consistent with moderate AR and mild AS on echo and BP 142/48. |
| B | minor | `initial_tool_outputs.ecg` | "Sinus tachycardia at 98 bpm" (below 100); interpretation attributed the rate to infection (cross-modality). | FIXED: normal sinus rhythm at 98 bpm; interpretation states PR 162 ms, no AV or bundle branch block. |
| A | major | `ground_truth.action_criteria` order, tiers | Pathway inverted (cultures, echo, autoimmune panel, drug check, Holter before the CTA); literature recommended. | FIXED per plan 3.1/3.2: NCCT, labs, ECG, CTA, MRI (optional), blood cultures, drug check (after CTA, informs IVT), TTE, TEE, telemetry (all required except MRI), literature optional last. Follow-ups reordered CTA, cultures, drug check, TTE, TEE, telemetry. |
| C | major | criterion `action-5-interpret-labs` (ESR, CRP, procalcitonin) and follow-up `request_autoimmune_panel` | Criterion answered by the initial labs (baseline warning); autoimmune panel orphan. | FIXED: both removed (plan C9). |
| B | minor | `initial_tool_outputs.labs.panels.Urinalysis`, `.interpretation`, `.abnormal_values_summary` | Urine rows named "RBC" and "WBC" duplicated CBC analyte names; summary interpretive ("anemia of chronic disease", "consistent with bacterial infection"). | FIXED: rows renamed Urine colour/protein/RBC/WBC/casts; factual summary and pattern-level interpretation. Values unchanged. |
| D | major | `initial_tool_outputs.ct` | NCCT template ("clinically implicated territory", "Nothing on this study contraindicates thrombolysis"), and "No ring-enhancing collection" on an unenhanced study. | FIXED: canonical normal impression with ASPECTS 10; "right MCA territory"; "No focal collection and no focal oedema". |
| B | minor | `initial_tool_outputs.mri.impression`, `.additional_observations` | Left occipital and cerebellar foci called "left anterior circulation"; "mycotic aneurysm" (a diagnosis) in the MRA line. | FIXED: numbered impression naming the territories (both hemispheres and the posterior circulation); "no intracranial aneurysm on MRA". |
| D | minor | CTA follow-up | Impression an interpretation ("the embolic material has fragmented or lodged distally"); teaching note in a finding. | FIXED: numbered impression opening with no occlusion, no aneurysm, no haemorrhage; cervical arteries named. `contrast_used` already true. |
| B | major | blood-culture follow-up | `susceptibility` null and `gram_stain` null while MICs were in `findings` and gram stain was ordered; two sets while the must asked for three. | FIXED: three sets (6/6 bottles positive), gram stain "Gram-positive cocci in chains", susceptibility dict (penicillin MIC 0.06 S, ceftriaxone 0.12 S, vancomycin 0.5 S, gentamicin 4, no high-level resistance); criterion label "three sets". |
| B | minor | TTE follow-up | Impression "Abnormal values: ... (H)"; LVEDD without unit. | FIXED: numbered echo impression; LVEF 55 percent not flagged; units. |
| D | minor | telemetry follow-up | Findings and impression interpreted the rhythm against infection and "ring abscess" (cross-modality); recommended actions; no recording time. | FIXED: opens "Recorded on the stroke unit after admission, 24 hours."; rhythm and conduction stated only; trigger `request_telemetry`. |
| C | major | drug-check follow-up and `action-8` | Cited AHA_ASA_2019 Class III; ibuprofen "not the limiting factor"; no allergy statement. | FIXED: contraindication "Infective endocarditis, suspected or confirmed ... (COR 3: Harm)"; ibuprofen stop (bleeding, aminoglycoside nephrotoxicity), paracetamol; NKDA so beta-lactams usable. Required (plan C7). New must "Stop ibuprofen". |
| C | major | `ground_truth.assessment.required_recommendations` | No antibiotic must; generic surgery must; "three sets" vs a stored two; Duke must with em dashes. | FIXED: decision must (no IVT, COR 3 Harm, no EVT); three culture sets; IV benzylpenicillin or ceftriaxone 4 weeks for the penicillin-susceptible streptococcus (ESC 2023); Duke definite; TEE; aneurysm screening; urgent endocarditis team with surgery (1.8 cm mobile embolising vegetation, ischaemic stroke without haemorrhage or coma does not delay surgery); telemetry with reason; no antithrombotic; stop ibuprofen; dental source; future prophylaxis. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Two generic tPA prohibitions, duplicated endocarditis tPA prohibitions, 140/90 template, large-infarct anticoagulation template. | FIXED: one IVT prohibition (COR 3 Harm), no anticoagulant or antiplatelet, no antibiotics before cultures, canonical C5 COR 3 No Benefit BP text (no IVT, no EVT), NCCT not delayed. |
| C | minor | `ground_truth.avoided_actions` CSF | LP marked `harm` (score cap 0.35) for a patient without mass effect or anticoagulation. | FIXED: severity `waste` (plan 3.4), id renamed `avoid-waste-3-analyze-csf`, rationale: no meningism, no abscess, CSF does not change management. |
| C | minor | `ground_truth.differential` | Haemorrhage/mycotic aneurysm left "moderate" after NCCT and CTA excluded it; other entries waiting for results the pathway returns. | FIXED: assessment-time likelihoods with case data; marantic endocarditis added (very low). |
| E | minor | `ground_truth.key_clinical_evidence` | Template lines, "Off-pathway modality" lines, "Tier per the July 2026 clinical review". | FIXED: rebuilt case-specific; sequencing line kept. |
| C | minor | `metadata.clinical_pearls` | Unverifiable figures (haemorrhage 20-40%, "20x" IE risk, aneurysm 2-10%); TEE pearl conditioned on a non-diagnostic TTE. | FIXED: figures removed except the 1-2% bicuspid prevalence; TEE pearl per ESC 2023. |
| A | minor | citations | Free-text guideline string; duplicate keys; AHA_ASA_2019. | FIXED: `[AHA_ASA_Stroke_2026]`, `[ESC_endocarditis_2023]`, one per list. |
| E | minor | `metadata.case_body_concerns`, `difficulty_description`, `difficulty_rationale` | Stale concerns; "incomplete dental antibiotic prophylaxis". | FIXED: concerns emptied; descriptions aligned. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway now reads NCCT, labs, ECG, CTA, blood cultures (three sets before antibiotics), the alteplase check, TTE, TEE and telemetry, all required, with MRI optional and literature optional last; the ESR/CRP criterion and the orphan autoimmune panel are gone. NIHSS is 7. The dental history now says a single amoxicillin dose was prescribed and not taken, and the case teaches that prophylaxis is not indicated for a bicuspid valve but will be after this episode. A cardiovascular exam with the aortic regurgitation murmur was added, the roommate contradiction fixed, and the ECG reads normal sinus rhythm at 98. The TEE report shows the 1.8 x 0.7 cm mobile vegetation with moderate AR and no perivalvular abscess; telemetry shows no conduction block. Musts state: no IV thrombolysis (suspected IE, COR 3 Harm) and no thrombectomy (no occlusion), blood cultures before antibiotics, IV benzylpenicillin or ceftriaxone for 4 weeks, Duke-definite IE, TEE, infectious aneurysm screening, urgent endocarditis-team and cardiac-surgery referral, telemetry for new AV block, no antithrombotic for the stroke, stop ibuprofen, dental source control and future prophylaxis. The LP avoided action is now waste rather than harm.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[ESC_endocarditis_2023]` (and `[AHA_ASA_Stroke_2026]`) used per plan section 1.1; `[AHA_IE_prophylaxis_2021]` is cited in prose and in the literature output.
- `echo_type` is not a field of `EchoReport`; TTE and TEE are routed by the trigger tokens `tte` and `tee`. Consider adding the field so the MockServer discriminator can route them.

## Open questions for Andrea (judgment calls you could not settle)

- The TEE was written without a perivalvular abscess, to stay consistent with the normal PR interval on ECG and telemetry. If R2 prefers the abscess teaching point, the TEE, ECG and telemetry must change together.
- The antibiotic must names benzylpenicillin or ceftriaxone for 4 weeks (ESC 2023, penicillin-susceptible oral streptococci, complicated native-valve IE); the 2-week gentamicin regimen was deliberately not offered because of the embolic complication.

## Verification

Adversarial verifier, 23 October 2026. Checked: NIHSS 7 against the exam (deltoid 3/5 gives arm 2, hip flexion 3/5 leg 2, ataxia 0 for weakness) and every repetition; the TEE follow-up, TTE then TEE criteria and the soft TTE-before-TEE constraint; the prophylaxis history in PMH, HPI, key evidence, red herring and pearl; the musts and prohibitions for IVT, antithrombotics, telemetry reason and antibiotics (ESC 2023 4-week regimen for penicillin-susceptible oral streptococci); blood-culture structured fields against the narrative; Osler node, splinter and Roth spot sites between HPI and exam; ECG rate 98 against vitals; lab arithmetic (Hct/Hb about 3, MCV from Hct/RBC, anion gap 15); `is_abnormal` against reference ranges.

Found and changed:
- `initial_tool_outputs.labs.interpretation` stated that glucose 104 mg/dL was within reference ranges, while the row (reference 70-100) and the abnormal-values summary flag it high. Now "Glucose 104 mg/dL, mildly above the reference range. Creatinine 1.3 mg/dL, INR 1.0 and troponin I within reference ranges."

No other error found. `perfect_agent.py ISCH-STR-P03 -v` passes; `case_io.py check` clean for the case.

## Condition audit
Condition auditor, 23 October 2026 (cross-case uniformity pass over all 30 ISCH-STR cases).
- Literature output moved out of the initial work-up (ruling 5, plan 3.2): `initial_tool_outputs.literature_search` is now null and the unchanged output is the last follow-up (trigger `search_endocarditis_stroke_thrombolysis_antithrombotic_surgery_evidence`); any literature query is still served it.
- Literature criterion `action-7-search-medical-literature`: exact-query `required_arguments` (unmatchable) replaced by {}, as in the other cases. Both checks clean.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
The I63 category no longer appends mechanism labels ("embolic", "cardioembolic", "lacunar") or the bare label "stroke" (which matched "haemorrhagic stroke" or "stroke mimic"); mechanism labels and code families now sit on the specific codes.
- labels removed: "cardioembolic stroke", "lacunar stroke", "lacunar infarct", "stroke"
- codes removed: I63.5, I63.3, I63.2, I63.0, I63.1, I63.8, I63.81, I63.89
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
