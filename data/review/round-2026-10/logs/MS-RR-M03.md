# MS-RR-M03
Reviewer status: R1 none, R2 none (no MS-RR notes file in this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. All changes below are own findings and plan classes. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.chief_complaint` | Plan R asks to word the chief complaint to the exam's side. | DECLINED for this case: the exam is symmetric (4+/5 and 4/5 in both legs), so "both legs" is accurate; kept. |
| B | minor | `patient.neurological_exam.cranial_nerves` | "3-4 beats of horizontal nystagmus on sustained leftward gaze" with no infratentorial lesion on any study (a deficit no lesion explains). | FIXED: "2-3 unsustained beats of end-point nystagmus on extreme leftward gaze" (physiological). |
| D | major | `initial_tool_outputs.mri.findings[3]`, `.impression` item 4 | Brain MRI reported the C3-C4 cord lesion (non-enhancing, contradicting the spine report's enhancement) (plan H). | FIXED: deleted; "Spinal cord not assessed on this study." added; impression brain-only with final period. |
| C | major | `followup_outputs` `request_repeat_mri_3months` | Future scan with a new MCP lesion (plan F). | FIXED: deleted. |
| B | minor | `followup_outputs[0].output` (spine MRI) | Location "as seen on brain MRI sagittal sequences" (cross-study reference); empty descriptions. | FIXED: plain location; T2/enhancement descriptions; values unchanged. |
| B | major | `initial_tool_outputs.labs.panels.CBC` | Female reference ranges for haemoglobin (12.0-16.0) and haematocrit (36-46) in a man; with a male range Hb 13.1 would be low but was unflagged; no RBC count. | FIXED: male ranges (Hb 13.5-17.5, Hct 40-52); Hb 14.2 g/dL so the panel stays normal; RBC 4.60 x10^12/L added and MCV 92.4 fL so that Hct/RBC/MCV agree (Hct 42.5 unchanged). |
| B | minor | `initial_tool_outputs.labs` | "Autoimmune panel" held B12, TSH and vitamin D; ANA 1:40 flagged normal against "Negative (<1:40)"; vitamin D 29 ng/mL copied from M01 (plan E); HIV row with leaked significance; no liver tests; no AQP4/MOG result (A8). | FIXED: panels regrouped as in the batch; ANA `is_abnormal` true; vitamin D 24 ng/mL; HIV significance null; LFTs with male ranges added; AQP4-IgG CBA and MOG-IgG live CBA negative rows. |
| C | minor | `initial_tool_outputs.csf` | MBP (obsolete), IgG index above range unflagged, no kFLC, recital interpretation with "(N/A PMN/N/A lymph)" (plan J). | FIXED: MBP deleted, flags, kFLC 11.9 (reference < 6.1), pattern interpretation; cells, protein, glucose, 2 OCB unchanged. |
| C | major | `followup_outputs` literature `search_mcdonald_criteria` | Presented the 2017 criteria as current (4 regions, OCB substitute for DIT) (plan O). | FIXED: one general result for the 2024 revision (Montalban 2025); summary states it supersedes 2017. |
| C | minor | `followup_outputs` drug check | "Check JC virus antibody status before initiation" for dimethyl fumarate (a natalizumab requirement); codeine intolerance not listed (plan F11, O). | FIXED: JCV line deleted; codeine line added. |
| B | minor | `fallback_tool_outputs.ecg`, `.echo` | "Normal sinus rhythm" at rate 59; echo without `echo_type`. | FIXED: rate 64; `echo_type` "TTE". |
| A | major | `ground_truth.action_criteria`, `.stop_rule`, `.sequence_constraints` | Template criteria (plan A, P, 3.4). | FIXED: brain MRI, spine MRI, labs required; AQP4/MOG recommended; CSF, VEP, drug check, literature optional, literature last; stop rule = the three required, max 2; soft MRI-before-CSF. |
| C | major | `ground_truth.assessment` | T0/T1/T2 musts; generic relapse and lifestyle musts (smoking cessation in a never smoker); T10 teriflunomide-contraception prohibition in a man; JCV and fingolimod prohibitions without a case reason (plan B, K). | FIXED: formulation, relapse (dipstick/culture first, ibuprofen caution), DMT (no pregnancy clause), pre-DMT screening, bladder (PVR first for incomplete emptying); prohibitions T7, T11, T12, T13. |
| C | major | `ground_truth.differential` | NMOSD/MOGAD high, sarcoid moderate; codes D86.85, G04.81 (plan C). | FIXED: all low with case results; B12 and CNS lupus entries added (ANA row exists); D86.89, G04.00. |
| D | major | `ground_truth.key_clinical_evidence` | Template lines (plan D). | FIXED: six observable lines; DIS 4 of 5 (no infratentorial lesion). |
| B | minor | `ground_truth.red_herrings` | Vitamin D path pointed at the old panel; ANA and the carpal tunnel attribution not recorded. | FIXED: path updated; ANA and carpal-tunnel red herrings added. |
| E | minor | `metadata.clinical_notes`, `.difficulty_rationale` | "Borderline CSF findings" (2 restricted bands and raised kFLC are positive); CSF and AQP4/MOG called required. | FIXED. |
| B | minor | `ground_truth.avoided_actions` | Generic rationales (plan N). | FIXED: case-tied sentences, citations per plan. |

## Changes, in one paragraph a physician can read before re-reviewing

A 38-year-old man with two weeks of paraparesis, a band at the navel, urgency with incomplete emptying and Lhermitte sign, a right hand sensory episode 14 months ago and new right colour desaturation. The brain MRI no longer reports the cervical cord; the 3-month future MRI was deleted; the borderline left-gaze nystagmus is now physiological end-point nystagmus, since no study shows an infratentorial lesion. The blood count now uses male ranges (Hb 14.2, RBC added, indices consistent); ANA 1:40 is flagged; vitamin D 24 ng/mL; negative AQP4-IgG/MOG-IgG by CBA added. CSF adds kFLC 11.9 and drops MBP. The literature output now describes the 2024 McDonald revision. DIS is 4 of 5 (periventricular, juxtacortical, cord C3-C4 and T6-T7, optic nerve by VEP), so no separate DIT or CSF is needed. Pathway: brain MRI, spine MRI, labs required; AQP4/MOG recommended; CSF, VEP, drug check, literature optional. Musts: formulation, steroids after excluding UTI with an NSAID caution, DMT, pre-DMT screening, bladder with PVR first. The male-inappropriate teriflunomide prohibition was removed. All mimics low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan 5.1); synonym codes G35.B/G35.C and "demyelinating disease" (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None. OCT not added: the right optic nerve symptom is days old, so the library's normal OCT is what an acute optic neuritis shows (plan F7).
