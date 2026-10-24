# HEP-ENC-M10
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| fea3c98c-d147-438b-99d9-9af32922ae04 | FIXED | Deleted the `interpret_labs` follow-up `request_upper_endoscopy_gi_consult`, which held the post-transfusion CBC and the ammonia "6 h post-lactulose" of 84 (C1, C2). One admission ammonia (112, range 11-51) stays in `panels.Ammonia`. The red herring, the pearls and the prohibitions no longer use ammonia as proof of HE, and K-AMM was added. The literature output that quoted the AASLD finding was deleted with the literature step. |
| f4f73be0-a9ec-4bf5-ba94-dd96506e7aee | FIXED | The lactulose must targets 2-3 soft bowel movements per day (ACG 2026 rec. 10; EASL 2022), given by NG tube or enema (`required_recommendations[3]`). |
| fed6c71c-77b3-4526-a49f-1a2d5cd320e8 | FIXED | Blood and urine cultures (`action-7-`, `action-9-order-microbiology`) are `recommended`, with C7 labels and arguments `{"specimen": ...}` only, and are removed from the stop rule. The rationale states that the bleed gets ceftriaxone prophylaxis (MUST-VB), not culture gating. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `action-5-interpret-labs`, `action-8-order-microbiology`, `followup_outputs[0]` | The paracentesis was duplicated (an `interpret_labs` `{}` criterion, C6). The ascitic culture was "Pending" beside a templated impression. | FIXED: a5 deleted. a8 kept with the canonical label and expected evidence (PMN 74, below 250). The output is renamed `request_diagnostic_paracentesis` and reports one time point (no growth at 48 h), cell counts, and an ascitic albumin of 0.7 consistent with SAAG 1.9 and serum albumin 2.6. |
| D | major | `action-3-search-medical-literature`, `followup_outputs[2]` | A required literature search (C4). | FIXED: deleted. |
| C | major | `ground_truth.diagnosis.accepted[0]`, HPI, PMH | No score in the label, while the history gave "Child-Pugh B, MELD 16" (undated). Computed: MELD 22, MELD-Na 24, Child-Pugh C 14. The label grade was a "II-III" range (C10, plan 1.2). | FIXED: label "West Haven grade III ... (Child-Pugh C, MELD-Na 24)". Grade III is supported by lethargy, gross disorientation to time, place and situation, and incoherent speech. Scores removed from the HPI and PMH; score pearl added. |
| C | major | `followup_outputs[3]` (DI) | Haloperidol and acetaminophen dosing given as alternatives; "standard SBP prophylaxis regardless of paracentesis"; no octreotide-insulin interaction. | FIXED: real content (hold propranolol and diuretics in bleeding with hypotension; octreotide alters glucose with insulin; no ceftriaxone interaction; NSAIDs; sedatives; lactulose route). Recommended, placed last, trigger `check_octreotide_ceftriaxone_propranolol_insulin`. |
| B | minor | `initial_tool_outputs.labs` | Urine culture "Pending" in the admission panel (C7); template TSH 2.1 and zinc 82; INR and ammonia under LFTs; no CRP; dash in the summary (C9). | FIXED: culture row deleted. TSH 1.4, zinc 68, CRP 4.6 mg/L added. INR moved to Coagulation, ammonia to its own panel. Summaries list only flagged values. |
| B | minor | `initial_tool_outputs.ct` | Empty findings (C8). | FIXED: normal finding plus the case's own mild cortical volume loss; impression unchanged in substance. |
| B | minor | `initial_tool_outputs.microbiology`, `followup_outputs[1]` | Template "No organism isolated to date". | FIXED: no growth at 48 h. `collected_before_antimicrobials` stays true because the case gives ceftriaxone after sampling. |
| A | minor | `action-1-interpret-labs` | Eleven panels demanded, including iron studies (C9). | FIXED: the C9 alternatives plus `type_and_screen`. Iron studies stay in the report but leave the arguments (plan). |
| C | major | `assessment.required_recommendations` | Diagnostic steps (CT, paracentesis, endoscopy) listed as musts; "2-4"; rifaximin at a first episode; no airway plan despite GCS 11, a diminished gag and haematemesis; no insulin plan while NPO on octreotide; no transplant referral; thiamine with no alcohol or malnutrition indication. | FIXED: MUST-VB (with the octreotide dose), airway must (Baveno VII), hold NSBB and diuretics, lactulose must (NG or enema, 2-3), insulin must, MUST-TX, and long-term norfloxacin prophylaxis (stored ascitic protein 1.1 with Child-Pugh C and bilirubin above 3; EASL 2018). Rifaximin and thiamine removed. |
| C | minor | `assessment.prohibited_recommendations` | Benzodiazepine line recommending haloperidol; generic LP line; acetaminophen dose not stated; shock line resting on "ammonia 112" (C12). | FIXED: PROHIB-BZD, opioid line (acetaminophen up to 2 g per day), shock line reworded on clinical signs, BUN and overtransfusion lines kept (dashes removed). LP line deleted. |
| C | major | `ground_truth.differential` | ICH and uraemia moderate after a normal CT and Cr 1.3 (C14); shock encephalopathy "high" as an alternative; the hypoglycemia ICD meant "with coma". | FIXED: ICH, uraemia and SBP low with the excluding results; shock moderate as a concurrent contributor; E11.649. |
| D | minor | `key_clinical_evidence[2,4]`, `red_herrings[1]` | Ammonia used as evidence; "CT mandatory before LP" with no LP in the case. | FIXED: reworded on clinical signs and the CT indication. |
| A | minor | all `action_criteria` | Rationales repeated the labels; mixed citations; `before_antimicrobials` arguments (C17). | FIXED: per plan 3.1. Order: labs, blood (recommended), tap (required), urine (recommended), CT (required), DI (recommended). Stop rule: labs, tap, CT. |
| E | minor | `metadata.difficulty_*` | "CT before LP"; "5 required tools ... consult". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

This is a first episode of overt HE (now grade III) after a variceal bleed with shock, in a patient with haemochromatosis cirrhosis (Child-Pugh C 14, MELD-Na 24).

The work-up requires core labs with group and screen, a diagnostic paracentesis (PMN 74, culture negative) and a non-contrast CT. The CT is indicated by the first overt episode with INR 2.0, platelets 72 and extensor plantars; it shows no haemorrhage and mild atrophy. Blood and urine cultures are a recommended screen, and the medication review is recommended. The post-transfusion and serial-ammonia panel and the literature step are gone.

The musts are:
- the Baveno VII bleeding bundle (octreotide, ceftriaxone 1 g for up to 7 days, transfusion to 7-8 g/dL, endoscopy within 12 hours);
- airway protection before endoscopy;
- holding propranolol and the diuretics;
- lactulose by NG tube or enema to 2-3 stools a day;
- adjusting insulin while he is nil by mouth on octreotide;
- transplant referral;
- later norfloxacin prophylaxis.

The differential keeps shock as a concurrent contributor and moves uraemia, ICH and SBP to low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation keys per plan 1.1 (`[Baveno_VII]` is used by the DI criterion).
- `accepted[0]` changed under ruling 3 (C10, grade III; plan CENTRAL 6). No ICD or synonym change.

## Open questions for Andrea (judgment calls you could not settle)

- The HPI says phlebotomy was stopped 8 months ago "when ferritin fell below therapeutic targets, though he never returned to normal ferritin", and the admission ferritin is 2840 ng/mL with transferrin saturation 93%. Re-accumulation to that level in 8 months is fast. Ferritin is also raised by hepatocellular injury and inflammation, so I left the values unchanged. Confirm, or lower the ferritin.
- Pre-emptive TIPS is not in the musts: Child-Pugh C 14 is outside the Baveno VII pre-emptive TIPS window (Child-Pugh C below 14). Confirm.
- Thiamine and rifaximin were removed from the musts. There is no alcohol or malnutrition history, and this is a first episode.

## Verification

Adversarial verifier, 23 Oct 2026. Read the log, the full diff and the final case.
- The three notes are confirmed fixed:
  - There is one ammonia and no post-lactulose value.
  - The lactulose target is 2-3.
  - The cultures are `recommended` and out of the stop rule.
- Scores were recomputed: MELD 22, MELD-Na 24 (Na 133), and Child-Pugh C 14. Grade III fits gross disorientation to time, place and situation.
- The ascitic protein is 1.1 g/dL, which supports the norfloxacin primary prophylaxis must (EASL 2018). MUST-VB agrees with Baveno VII. Leaving pre-emptive TIPS out is correct at Child-Pugh 14.
- The red-herring path `labs.panels.CMP[3]` is BUN. The drug-interaction check routes correctly for "octreotide", "ceftriaxone" and "propranolol".
- Found and fixed:
  - **GCS.** `neurological_exam.mental_status` gave GCS 11 (E3V3M5), but asterixis is elicited on sustained arm extension, so he obeys a command (M6). This is the class the worker corrected in M07, M08, M09 and P01. It is now GCS 12 (E3V3M6). Grade III and the airway must are unchanged. The own-findings row that cites "GCS 11" describes the pre-fix state.
  - **Fallback EEG.** `fallback_tool_outputs.eeg` was a normal EEG in grade III HE with myoclonus, against `fallback_tool_kinds.eeg` "abnormal_metabolic". It is replaced by generalized delta-theta slowing at 3-5 Hz with intermittent bifrontal triphasic waves, no epileptiform discharges, and myogenic artefact from the jerks. No criterion was added.
  - **Lab interpretation.** `initial_tool_outputs.labs.interpretation` omitted the flagged TIBC 214 µg/dL (low), which is now listed.
- The worker's open questions (ferritin re-accumulation, TIPS, thiamine and rifaximin) stand.
- `perfect_agent.py HEP-ENC-M10 -v` passes; `case_io.py check` reports no failure naming the case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"hepatic coma" (grade IV only) and the coma/no-coma code of the other grade are no longer granted at category level; K76.82 stays as the generic code.
- labels removed: "hepatic coma"
- codes removed: K72.91
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

- `ground_truth.key_clinical_evidence[0]`: inserted the canonical "HE is a clinical diagnosis" pearl carried by the other 28 cases (auditor flag). M10 no pre-emptive TIPS at Child-Pugh C 14 confirmed (Baveno VII: pre-emptive TIPS for Child-Pugh C 10-13 or B 8-9 with active bleeding).

Checks: `perfect_agent.py` pass; `case_io.py check` schema and synonym guard OK, no test failure names this case; leak guard clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.specialized_test` set to null: a generic report (test_type '', impression 'Study within normal limits.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality '', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
