# NMDAR-ENC-RS03
Reviewer status: R1 not reviewed, R2 not reviewed (NMDAR-ENC has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | none: condition not reviewed. All changes below come from the condition plan (classes C1-C18, per-case index entry RS03) and my own reading. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[*].alternatives` | Plan C1: `basic`, `screen_for`, `protocol: standard`, 11-panel list, exact literature query; `contrast: false` on the testicular ultrasound. | FIXED: plan 3.2 verbatim (labs alt A/B, no beta-hCG (male), MRI `{contrast: true}`, CSF HSV_PCR + NMDAR_antibodies + OCB or IgG_index, EEG routine/video/continuous_icu, `{study: testicular_ultrasound}`, DDI and literature `{}`). |
| D | major | `initial_tool_outputs.labs` | Plan C4/C5: CSF anti-NMDAR 1:128 in two serum panels; serum antibody twice; anti-TPO inside the encephalitis panel; "Exclusion studies"; duplicate inflammatory panel; no onconeural panel. | FIXED: panels CBC, BMP, Hepatic, ABG, Coagulation, Inflammatory markers, Thyroid function, Thyroid autoantibodies, `Serum anti-GluN1 IgG (cell-based assay)` (1:64), neuronal-surface (LGI1, CASPR2, GABA-B, AMPA), onconeural (7), Systemic autoimmunity (ANA), Infection serology (HIV, SARS-CoV-2 PCR and IgG), Toxicology (UDS, ethanol added), Other (CK first). Plain recital. |
| D | minor | `initial_tool_outputs.csf.special_tests`, `.interpretation`, `.cell_count.WBC` | Two keys for the antibody; "(N/A PMN/85% lymph)" template junk; "(normal, no pleocytosis)" inside the value. | FIXED: one `NMDAR_antibodies` key in canonical form (1:128); pattern interpretation listing the HHV-7 PCR result as fact. HHV-7 stays a CSF special test (plan RS03). |
| D | minor | `initial_tool_outputs.mri.impression`, `.additional_observations` | Differential reasoning ("makes HSV encephalitis less likely") and a cross-modality line ("Prior CT brain (outside hospital) reportedly normal"). | FIXED: numbered impression with one hedged sentence ("an infectious encephalitis cannot be excluded on imaging"); CT line removed. |
| D | minor | `initial_tool_outputs.eeg.impression`, `.limitations`, `.findings[2]` | Plan C13: "active epileptogenic activity", "superimposed focal pathology", "to guide management". | FIXED: "This is an ABNORMAL EEG due to:" list; "Continuous EEG monitoring recommended."; seizure correlate recorded (unresponsiveness, oral automatisms). |
| B | major | `followup_outputs` (new cEEG), `ground_truth.action_criteria[ceeg-escalation]` | Plan C7: cEEG must without a cEEG follow-up (the library's normal cEEG would contradict the routine seizure). | FIXED: 24-h cEEG (EDB, left frontal slowing, seven left frontotemporal seizures, two evolving to bilateral tonic seizures as seen in the ED, no status); `ceeg-escalation` recommended. |
| D | minor | `initial_tool_outputs.body_imaging` | Plan C12: findings without measurements; "no germ-cell tumour identified". | FIXED: testicular sizes, echotexture, Doppler, epididymides; "Normal scrotal ultrasound. No testicular mass." |
| C | major | `followup_outputs` (literature) | Plan C3/RS03: three unattributed results (no authors) whose titles and figures I could not verify ("5-10% of routine CSF samples", "case series of 5"), and "molecular mimicry" as established mechanism. | FIXED: real sources only: Armangue 2018 (HSV as an established trigger), Dalmau 2011 (prodrome ~70%), Graus 2016; summary states that no cohort data link HHV-7 to the disease. |
| C | minor | `followup_outputs` (drug interactions) | "Monitor closely given patient's stress hyperglycemia" (cross-reference to labs); ibuprofen not checked; no HBV screening or D2 class warning. | FIXED: ibuprofen-acyclovir and ibuprofen-steroid; levetiracetam none; D2 class warning; HBV screening before rituximab. |
| C | major | `ground_truth.action_criteria[action-6...]`, `[action-7...]` | Ruling 5/6: literature and DDI `recommended`. | FIXED: both `optional`; follow-ups ordered cEEG, DDI, literature. |
| B | minor | criteria order, `.sequence_constraints`, `.stop_rule`, rationales, evidence, citations | Plan C6/C16/C18. | FIXED: labs, MRI, CSF, EEG, ultrasound, cEEG, DDI, literature (ids unchanged); soft MRI-before-CSF; stop rule five ids, max 2; case-anchored text; bracketed keys. |
| C | major | `ground_truth.assessment.required_recommendations`, `.prohibited_recommendations` | Plan C9/RS03: "testicular US + CAP CT", urology/oncology consult, "levetiracetam or valproate", "paired CSF and serum" diagnostic must; no ICU must despite GCS 9 and desaturation to 71%. | FIXED: M1 (no NSAIDs), M2, M3 male-negative, M4 with benzodiazepine for seizures over 5 minutes, M5, M6 ICU with airway assessment, M7, M8, M10. Canonical P1-P5 plus "Do not attribute the encephalitis to HHV-7 or treat it with antivirals alone". |
| C | major | `ground_truth.differential` | Plan C8 template; HHV-7 (a mimic the case raises) and the tick-borne serologies the CSF reports were absent; "primary psychiatric" entry for a presentation that is seizures, not psychiatric. | FIXED: all `low`: HSV, HHV-7 encephalitis (B10.09), TBE / Lyme (serologies negative), other antibody encephalitis, new-onset epilepsy with post-ictal encephalopathy, toxic seizures / NMS (UDS, ethanol, CK 412 from seizures). |
| C | major | `ground_truth.key_clinical_evidence` | Plan C15 template. | FIXED: six case-specific bullets (five Graus groups; CSF 1:128 despite a non-inflammatory CSF; MRI; EEG; HHV-7; negative scrotal US and timing). |
| C | minor | `ground_truth.red_herrings` | Psychiatric herring ("paranoia, hallucinations") not in this HPI; hyponatremia and CK templated; HHV-7 herring missing although `metadata.difficulty_description` names it. | FIXED: first-seizure herring; mild hyponatremia (134) with canonical text; CK canonical (`Other[0]`); HHV-7 herring added (`initial_tool_outputs.csf.special_tests.HHV-7 PCR`). |
| D | major | `fallback_tool_outputs.advanced_imaging`, `.specialized_test`, `.cardiac_monitoring`, `metadata.fallback_tool_kinds` | Plan C14: catch-all fallbacks; Holter average 70 against HR 115-120. | FIXED: first two null; telemetry with sinus tachycardia to 120 bpm and rare PVCs; kinds updated. |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale` | "7 required tools, 3 red herrings", "reverse/mimic". | FIXED. |
| - | check | - | `perfect_agent.py -v`: ok; all required/recommended criteria answered by case data. Guards 2 passed. `case_io.py check`: nothing names RS03. | - |

## Changes, in one paragraph a physician can read before re-reviewing

A 19-year-old man with a gastrointestinal prodrome, then generalized and focal seizures, orofacial dyskinesias, chorea, GCS 9 with post-ictal desaturation to 71% and autonomic instability: anti-NMDAR encephalitis confirmed by CSF anti-GluN1 1:128 (serum 1:64) in an otherwise non-inflammatory CSF, with an incidental HHV-7 CSF PCR. Findings are unchanged; the serum labs no longer carry the CSF antibody and now list onconeural antibodies and ethanol; reports are in modality voice. A 24-hour cEEG exists (seven left frontotemporal seizures) and is a recommended escalation. Literature and drug checks are optional; the literature output no longer cites unverifiable HHV-7 papers. Musts: acyclovir, steroids with IVIG or PLEX, no further tumour imaging after a normal scrotal ultrasound, antiseizure treatment, cEEG, ICU with airway assessment, escalation, lorazepam, neurology with psychiatry; a new prohibition against treating this as HHV-7 encephalitis. The differential is all low and adds HHV-7 encephalitis, tick-borne disease and new-onset epilepsy.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation registry (plan CENTRAL 1): new keys used here: `[Gresa-Arribas_2014]`, `[Armangue_2018]`, `[Herman_2015]`, `[Abboud_2021]`, `[Venkatesan_2013]`.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for NMDAR-ENC. Checked every own-finding row against the file and read the whole final case.
- Confirmed: patient unchanged; serum labs hold serum 1:64 only, ABG consistent with a post-ictal mixed acidosis, CK 412 attributed to seizures; CSF non-inflammatory with HHV-7 PCR as a `special_tests` key (plan RS03) and the canonical antibody key (1:128), ratio 77/124 = 0.62; scrotal ultrasound normal with measurements and matching criterion; cEEG consistent with routine (left frontotemporal onset, EDB); ICU must justified (GCS 9, desaturation to 71%). The HHV-7 literature output no longer claims unverifiable sources or molecular mimicry. Differential all low with case evidence (HHV-7, TBE/Lyme, new-onset epilepsy). No testicular-plus-CAP-CT or urology must remains.
- Found: nothing requiring a change.
- Re-run: `perfect_agent.py NMDAR-ENC-RS03 -v` ok; `case_io.py check` nothing names RS03; case guards pass.

## Close-out (24 Oct 2026)

- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions autoimmune_encephalitis_nmdar`): the generic G04.81 labels "autoimmune encephalitis", "antibody mediated encephalitis" and "autoimmune limbic encephalitis" and code G04.90 are no longer accepted, because every token of the first two occurs in "anti-LGI1 autoimmune encephalitis" or "seronegative autoimmune encephalitis" (alternatives the work-up excludes), limbic encephalitis is a different syndrome (Graus 2016) and G04.90 is unspecified encephalitis. Added "glun1 encephalitis", "nr1 encephalitis" and code G04.8. `accepted[0]` and `icd_codes[0]` unchanged. Decisions: `plans/NMDAR-ENC-decisions.md`.
