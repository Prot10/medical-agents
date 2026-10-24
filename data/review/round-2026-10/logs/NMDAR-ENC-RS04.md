# NMDAR-ENC-RS04
Reviewer status: R1 not reviewed, R2 not reviewed (NMDAR-ENC has no notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | none: condition not reviewed. All changes below come from the condition plan (classes C1-C18, per-case index entry RS04) and my own reading. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[*].alternatives` | Plan C1: `basic`, `screen_for`, `protocol: standard`, 11-panel list, `contrast: false`, exact literature query. | FIXED: plan 3.2: labs alt A/B with `beta-hCG` (woman of 40), `MOG_IgG_cell_based`, `AQP4_IgG_cell_based` (plan RS04); MRI `{contrast: true}`; CSF HSV_PCR + NMDAR_antibodies + OCB or IgG_index; EEG routine/video/continuous_icu; `{study: pelvis_abdomen_ultrasound}`; DDI and literature `{}`. |
| B | major | `patient.clinical_history.medications`, `patient.history_present_illness` | Medication list empty although the HPI says levetiracetam was started at the outside ED after the first seizure; HPI says "no new medications". | FIXED: levetiracetam 500 mg twice daily listed (started 6 days ago); HPI "no new medications other than levetiracetam". |
| D | major | `initial_tool_outputs.labs` | Plan C4/C5: serum 1:128 and CSF 1:256 in several serum panels; anti-TPO and a combined onconeural line inside the encephalitis panel; AQP4/MOG in a generic "Autoantibodies" panel; HIV only in "Exclusion studies"; no beta-hCG. | FIXED: panels CBC, BMP, Hepatic, Coagulation, Inflammatory markers, Thyroid function, Thyroid autoantibodies, `Serum anti-GluN1 IgG (cell-based assay)` (1:128), neuronal-surface (5), onconeural (7), Demyelinating antibodies (MOG, AQP4 negative, cell-based), Systemic autoimmunity (ANA, dsDNA), Infection serology (HIV, VDRL), Toxicology, beta-hCG (negative), Other (CK). Plain recital. |
| B | minor | `initial_tool_outputs.csf.glucose`, `.glucose_ratio`, `.special_tests`, `.interpretation` | Ratio 0.59 (borderline low, against a lymphocytic autoimmune picture); two keys for the antibody. | FIXED: CSF glucose 62 mg/dL (ratio 0.63); one `NMDAR_antibodies` key in canonical form (1:256); pattern interpretation. |
| D | minor | `initial_tool_outputs.mri.impression` | Differential reasoning in the impression ("atypical for pure HSV encephalitis given bilateral symmetric involvement"). | FIXED: numbered descriptive impression (medial temporal, bilateral optic neuritis R > L, insular/opercular and leptomeningeal signal, dorsal pons); no diagnostic reasoning. |
| D | minor | `initial_tool_outputs.eeg.impression`, `.findings[1]` | Plan C13: "epileptogenic ... requiring urgent continuous EEG monitoring". | FIXED: "This is an ABNORMAL EEG due to:" list; seizures recorded with behavioral arrest (the staring episodes of the HPI); "Continuous EEG monitoring recommended." |
| B | major | `followup_outputs` (new cEEG), `ground_truth.action_criteria[ceeg-escalation]` | Plan C7: three seizures in 40 minutes on levetiracetam with no cEEG follow-up. | FIXED: 24-h cEEG (EDB, GRDA, eight left temporal seizures, five with behavioral arrest, no status); `ceeg-escalation` recommended. |
| D | minor | `initial_tool_outputs.body_imaging.impression` | Plan C12: "All values within normal limits." | FIXED: "Normal pelvic and abdominal ultrasound. Both ovaries normal in size and echotexture; no adnexal mass." |
| C | major | `followup_outputs` (literature) | Plan C3/RS04: three results (Martinez-Hernandez 2023, Chen 2022, Dubey 2021) I could not verify as cited. | FIXED: real sources only: Titulaer 2014 Ann Neurol (overlapping demyelinating syndromes, 23/691), Graus 2016, Titulaer 2013; summary does not repeat the expected evidence. |
| C | minor | `followup_outputs` (drug interactions) | "Methylprednisolone may lower seizure threshold" (not an established interaction); levetiracetam not addressed; no HBV screening or D2 class warning. | FIXED: levetiracetam no interaction; IVIG maltose/GDH-PQQ glucometer interference kept; levetiracetam dosing after plasma exchange; D2 class warning; HBV screening before rituximab. |
| C | major | `ground_truth.action_criteria[action-6...]`, `[action-7...]` | Ruling 5/6: literature and DDI `recommended`. | FIXED: both `optional` (her only medicine is levetiracetam); follow-ups ordered cEEG, DDI, literature. |
| B | minor | criteria order, `.sequence_constraints`, `.stop_rule`, rationales, evidence, citations | Plan C6/C16/C18. | FIXED: labs, MRI, CSF, EEG, ultrasound, cEEG, DDI, literature (ids unchanged); soft MRI-before-CSF; stop rule five ids, max 2; case-anchored text; bracketed keys. |
| C | major | `ground_truth.assessment.required_recommendations`, `.prohibited_recommendations` | Plan C9 template musts; no ophthalmology must or plasma-exchange consideration for severe bilateral optic neuritis (plan RS04); "levetiracetam or valproate" for a woman of 40 already on levetiracetam. | FIXED: M1 (fever 38.2), M2 with "consider early plasma exchange because of the severe bilateral optic neuritis", M3 negative-screen text, M4 (increase levetiracetam or add lacosamide, avoid valproate), M5 cEEG, M6, ophthalmology review with acuity, color, fields and fundoscopy, M7 with fertility discussion, M8 lorazepam, neurology with psychiatry and ophthalmology. Canonical P1-P5. |
| C | major | `ground_truth.differential` | Plan C8 template; MOGAD/NMOSD overlap missing (plan RS04); leptomeningeal enhancement with fever raises chronic meningitis, not listed. | FIXED: all `low`: HSV, MOGAD/NMOSD overlap (G36.0, MOG/AQP4 negative), TB/cryptococcal/syphilitic meningoencephalitis (CSF tests negative), other antibody encephalitis, NPSLE, psychiatric, drug-induced / NMS. |
| C | major | `ground_truth.key_clinical_evidence` | Plan C15 template. | FIXED: six case-specific bullets. |
| C | minor | `ground_truth.red_herrings` | Psychiatric herring "hallucinations ... young adult" not in this HPI; templated hyponatremia and CK interpretations. | FIXED: psychiatric herring for a 40-year-old with paranoia; canonical hyponatremia (131) and CK (`Other[0]`) interpretations; optic neuritis added as a fourth herring (`patient.neurological_exam.cranial_nerves`). |
| D | major | `fallback_tool_outputs.advanced_imaging`, `.specialized_test`, `.cardiac_monitoring`, `metadata.fallback_tool_kinds` | Plan C14: FDG-PET and neuropsychology catch-alls; Holter average 82 against HR 108-128. | FIXED: first two null; telemetry with sinus tachycardia to 128 bpm; kinds updated (echo kept `incidental`, trace MR). |
| E | minor | `metadata.difficulty_description`, `.difficulty_rationale` | "7 required tools", template text. | FIXED. |
| - | check | - | `perfect_agent.py -v`: ok; all required/recommended criteria answered by case data (cEEG by its follow-up). Guards 2 passed. `case_io.py check`: nothing names RS04. | - |

## Changes, in one paragraph a physician can read before re-reviewing

A 40-year-old woman with 16 days of painless bilateral visual loss (right afferent pupillary defect), then paranoia, word-finding difficulty, insomnia, two generalized seizures, orofacial dyskinesias, chorea and autonomic instability: anti-NMDAR encephalitis (CSF anti-GluN1 1:256, serum 1:128) with overlapping bilateral optic neuritis on MRI. Findings are unchanged except a normal CSF/serum glucose ratio (0.63); levetiracetam from the outside ED is now listed. The serum labs no longer carry the CSF antibody and now show MOG-IgG and aquaporin-4-IgG negative on cell-based assay, onconeural antibodies negative and beta-hCG negative. A 24-hour cEEG exists (eight left temporal seizures) and is a recommended escalation. Literature and drug checks are optional; the literature output cites only verifiable sources. Musts: acyclovir, steroids with IVIG or plasma exchange (early plasma exchange considered for the severe optic neuritis), repeat pelvic imaging only if the response is poor, increase levetiracetam or add lacosamide, cEEG, ward with cardiac monitoring, ophthalmology review, escalation, lorazepam. The differential is all low and adds MOGAD/NMOSD overlap and chronic infectious meningitis.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation registry (plan CENTRAL 1): new keys used here: `[Gresa-Arribas_2014]`, `[Herman_2015]`, `[Abboud_2021]`, `[Venkatesan_2013]`.

## Open questions for Andrea (judgment calls you could not settle)

- None. Decision: M6 is the ward wording, by the plan's rule: no GCS of 12 or less, no hypoventilation or desaturation, HR peaks at 128 (below 130) and the labile BP comes without diaphoresis.

## Verification

Adversarial verifier, 24 Oct 2026. No reviewer notes exist for NMDAR-ENC. Checked every own-finding row against the file and read the whole final case.
- Confirmed: levetiracetam now listed and the HPI timeline fits (seizure on day 10 of 16 = 6 days ago); MOG/AQP4 negative, beta-hCG negative, onconeural panel present, no CSF result in the serum labs; CSF ratio 62/98 = 0.63; MRI optic nerve enhancement right > left matches the right RAPD and worse right acuity; normal pelvic ultrasound matches the criterion and the negative-screen must (age 40); ophthalmology and early-plasma-exchange musts present; Titulaer 2014 Ann Neurol 75:411-428 (23 of 691) verified. M6 ward wording follows the plan's rule (HR max 128, no diaphoresis, no hypoventilation); acceptable, with cEEG monitoring as a separate must.
- Found: nothing requiring a change.
- Re-run: `perfect_agent.py NMDAR-ENC-RS04 -v` ok; `case_io.py check` nothing names RS04; case guards pass.

## Close-out (24 Oct 2026)

- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions autoimmune_encephalitis_nmdar`): the generic G04.81 labels "autoimmune encephalitis", "antibody mediated encephalitis" and "autoimmune limbic encephalitis" and code G04.90 are no longer accepted, because every token of the first two occurs in "anti-LGI1 autoimmune encephalitis" or "seronegative autoimmune encephalitis" (alternatives the work-up excludes), limbic encephalitis is a different syndrome (Graus 2016) and G04.90 is unspecified encephalitis. Added "glun1 encephalitis", "nr1 encephalitis" and code G04.8. `accepted[0]` and `icd_codes[0]` unchanged. Decisions: `plans/NMDAR-ENC-decisions.md`.
