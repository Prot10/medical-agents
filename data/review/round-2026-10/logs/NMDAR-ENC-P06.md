# NMDAR-ENC-P06
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for NMDAR-ENC) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: condition not reviewed | - | - |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A | blocker | `action-2-analyze-csf`, `action-4-interpret-labs`, `action-1-analyze-brain-mri`, `action-7-search-medical-literature`, `action-8-check-drug-interactions` | Non-schema and over-specified arguments, exact literature `query`, long panel list (C1). | FIXED: plan 3.2 arguments; labs alternatives A/B with `beta-hCG` (woman of 30); CSF alternatives with oligoclonal bands or IgG index; MRI `{contrast: true}`. |
| B | blocker | `initial_tool_outputs.csf.special_tests` | CSF anti-NMDAR "Pending" in two keys while the labs gave a CSF titer of 1:20; culture pending (C4). | FIXED: one key `NMDAR_antibodies` = "Positive, titer 1:20 (cell-based assay, IgG anti-GluN1; reference laboratory, resulted day 5)"; `anti_NMDAR_antibody` deleted; culture final (no growth at 48 hours); IgG index with its range; glucose ratio names the serum glucose. |
| B/D | major | `initial_tool_outputs.labs.panels` | CSF titer inside the labs, "Exclusion studies" and duplicated inflammatory block, anti-TPO twice, CK under Toxicology, no free T4 or beta-hCG (C4, C5). | FIXED: plan panels (CBC, BMP, coagulation, inflammatory markers, thyroid function with free T4, thyroid antibodies, serum anti-GluN1 1:40 once, neuronal-surface panel, onconeural panel, HIV, toxicology, beta-hCG negative, CK under Other); `clinical_significance` null; plain recital. |
| B | major | `patient.clinical_history.medications` | The HPI says primary care prescribed lorazepam 0.5 mg five days ago and the urine screen is positive for benzodiazepines, but lorazepam was missing from the medication list (C17). | FIXED: lorazepam 0.5 mg at night and as needed added. |
| E | minor | `patient.history_present_illness` | "anxiety and postpartum-equivalent stress" (no pregnancy in the history). | FIXED: "anxiety and stress" (plan). |
| D | major | `initial_tool_outputs.mri.impression` | "should be correlated with CSF analysis ... Clinical and CSF correlation essential" (C13). | FIXED: radiology impression with one hedged sentence (early inflammatory change versus artifact); signal characteristics and negatives filled. |
| D | minor | `initial_tool_outputs.eeg` | "possible epileptiform" wording, prose impression, interpretive findings (C13). | FIXED: "This is an ABNORMAL EEG due to:" numbered (sharp waves, temporal rhythmic delta, slowing; no seizures or extreme delta brush); background filled. |
| B/D | major | cEEG follow-up `request_continuous_eeg` | Empty background, prose impression (C7). | FIXED: background consistent with the routine EEG; findings list five left temporal subclinical seizures (5-6 Hz evolving theta), extreme delta brush from hour 18 and slowing; template impression. |
| D | major | `initial_tool_outputs.body_imaging` | "Complex cystic mass" without teratoma features; impression not in radiology voice (C12). | FIXED: Rokitansky nodule with acoustic shadowing, echogenic lines and dots, no vascularity; impression "consistent with a mature cystic teratoma (dermoid)"; uterus, right ovary and abdomen described. |
| B | major | `fallback_tool_outputs.ecg`, `.cardiac_monitoring` | Fallback ECG at 58 bpm and Holter average 79 against HR 114 (C14). | FIXED: fallback ECG null; `initial_tool_outputs.ecg` sinus tachycardia 114 with normal intervals; telemetry fallback (86-126, average 104). |
| C | major | `fallback_tool_outputs.advanced_imaging`, `.specialized_test` | Catch-all fallbacks (C14). | FIXED: null; `metadata.fallback_tool_kinds` updated; fallback DDI `proposed` "". The incidental CT granuloma fallback kept. |
| D | major | `initial_tool_outputs.literature_search`, `.drug_interactions` | Placeholder literature and a DDI text that repeated expected_evidence (C3). | FIXED: canonical literature plus Schmitt 2012 (extreme delta brush); DDI in report voice for her ibuprofen, sumatriptan and lorazepam (NSAID nephrotoxicity with IV acyclovir and bleeding with steroids, sedation, sulfonamide allergy checked, D2 class warning, valproate, HBV screen, cyclophosphamide fertility). Leak guard passes. |
| C | major | literature and DDI criteria | Both recommended (rulings 5, 6). | FIXED: optional, `{}`, last. |
| C | major | `assessment.required_recommendations` | Template musts (C9). | FIXED: M1 plus "hold ibuprofen and other NSAIDs during IV acyclovir", M2, teratoma removal with gynecology (ovary-sparing where feasible), M4 with the valproate clause (seizures on cEEG), M5, M6 ICU (labile blood pressure with diaphoresis meets the rule's trigger; recurrent seizures), M7 with fertility preservation, M8 titrated from her current lorazepam, M10. |
| C/E | minor | `assessment.prohibited_recommendations` | C9. | FIXED: canonical P1-P5. |
| C | major | `ground_truth.differential` | Templated likelihoods (C8). | FIXED: all low with this case's evidence: HSV encephalitis, other antibody-mediated encephalitis, primary psychiatric disorder, drug-related encephalopathy (benzodiazepine, serotonin toxicity), migraine-related confusional state. |
| C | major | `ground_truth.key_clinical_evidence` | Template (C15). | FIXED: six case-specific bullets. |
| C | minor | `ground_truth.red_herrings` | Hyponatremia template interpretation; benzodiazepine screen and migraine history not listed although the variant description names them as the puzzle (C15). | FIXED: canonical hyponatremia interpretation; two red herrings added (urine benzodiazepines from the prescribed lorazepam; migraine history with sumatriptan). |
| C | minor | criteria `rationale`, `citations`, `expected_evidence` | C16. | FIXED: bracketed keys; MRI rationale names the new right lower facial weakness as a reason to exclude a structural lesion. |
| A | minor | order, `sequence_constraints`, `stop_rule` | C6, C18. | FIXED: labs, MRI, CSF, EEG, pelvic US, cEEG, DDI, literature; soft MRI-before-CSF; five required ids, max 2. |
| B | minor | `metadata.difficulty_rationale`, `.difficulty_variant_description` | "1 red herrings". | FIXED: three red herrings, confounders named. |
| E | minor | whole case | American-spelled case; canonical texts British. | FIXED: new text in the case's spelling. |

## Changes, in one paragraph a physician can read before re-reviewing
NMDAR-ENC-P06 is a 30-year-old woman with a psychiatric onset, oromandibular automatisms and subtle left medial temporal FLAIR signal. The CSF report now gives the final result: anti-GluN1 positive at 1:20, with mild lymphocytic pleocytosis and negative HSV PCR. Serum (1:40) is the only antibody entry in the rebuilt labs, which add free T4 and a negative beta-hCG. Lorazepam 0.5 mg, prescribed five days earlier, is now on her medication list and explains the benzodiazepine screen; it and her migraine history are listed as red herrings. The MRI and EEG reports no longer point to the CSF. The pelvic ultrasound describes a 2.8 cm left mature cystic teratoma with its characteristic features. The continuous EEG shows five subclinical left temporal seizures and extreme delta brush from hour 18. An ECG at 114 bpm replaces the fallback at 58 bpm. The musts are the canonical set, with three case-specific points: ICU care for labile blood pressure with diaphoresis; no NSAIDs (her ibuprofen) during IV acyclovir; and ovary-sparing teratoma removal. Literature and drug interactions are optional.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys used and not yet in the allow-list: `[Gresa-Arribas_2014]`, `[Herman_2015]`, `[Venkatesan_2013]` (plan CENTRAL 1).
- The plan's criterion id `cEEG-escalation` fails the lowercase id pattern; the existing id `action-6-analyze-eeg` was kept.

## Open questions for Andrea (judgment calls you could not settle)
None. Level of care: HR 114 alone is below the M6 trigger of 130, but the examination records labile blood pressure with diaphoresis, which the rule lists as an ICU trigger, and the cEEG shows recurrent seizures; I wrote ICU. The new right lower facial droop is a central sign the MRI does not explain; I left it as documented (facial weakness and orofacial dyskinesia are both described in this disease) and used it in the MRI rationale.

## Verification
Adversarial verifier, 24 Oct 2026. Checked against the plan (sections 1-4 and the per-case bullet) and ROUND_POLICY: every own-finding row against the file; criterion tiers, minimal arguments, order and ids; soft MRI-before-CSF constraint and stop rule (five required ids, max 2); CSF report carries the only CSF titre and the labs only the serum titre; musts against allergies, medications and level-of-care rule; prohibitions P1-P5; differential and key evidence against the final reports; red-herring field paths; fallbacks; a word-level diff of every changed string against HEAD (to catch accidental edits in correct prose); citation format and new-text dashes. No reviewer notes exist for NMDAR-ENC, so the notes table is complete. `perfect_agent.py -v` passes and `case_io.py check` reports no failure naming the case (case guards included).

Found and changed:
- `ground_truth.differential` (migraine entry) asserted "no headache with this 12-day illness", which nothing in the patient block states. FIXED: key features now rest on what the case says (migraine without aura, husband says the illness is unlike her migraines, seizures, autonomic lability, CSF antibodies).
- `metadata.fallback_tool_kinds.cardiac_monitoring` FIXED to "sinus_tachycardia".
- Confirmed: lorazepam added to the medication list matches the HPI and the benzodiazepine screen; NSAID hold in M1 matches the DDI report; ICU by labile BP with diaphoresis. The new right lower facial droop is left as documented: it is contralateral to the left temporal seizure focus, and post-ictal weakness after the chewing episode is a plausible explanation, so it is not a deficit without a lesion.

## Close-out (24 Oct 2026)

- Synonyms (`diagnosis_synonyms.yaml`, applied with `--prune --conditions autoimmune_encephalitis_nmdar`): the generic G04.81 labels "autoimmune encephalitis", "antibody mediated encephalitis" and "autoimmune limbic encephalitis" and code G04.90 are no longer accepted, because every token of the first two occurs in "anti-LGI1 autoimmune encephalitis" or "seronegative autoimmune encephalitis" (alternatives the work-up excludes), limbic encephalitis is a different syndrome (Graus 2016) and G04.90 is unspecified encephalitis. Added "glun1 encephalitis", "nr1 encephalitis" and code G04.8. `accepted[0]` and `icd_codes[0]` unchanged. Decisions: `plans/NMDAR-ENC-decisions.md`.
