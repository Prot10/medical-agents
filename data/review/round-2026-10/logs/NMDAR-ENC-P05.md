# NMDAR-ENC-P05
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for NMDAR-ENC) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: condition not reviewed | - | - |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| A | blocker | `action-2-analyze-csf`, `action-8-check-drug-interactions`, `action-7-search-medical-literature`, `action-1-analyze-brain-mri`, `action-4-interpret-labs` | Non-schema keys (`basic`, `screen_for`), exact `query`, `protocol: standard`, 11-panel list (C1). | FIXED: plan 3.2 arguments, labs alternatives with `beta-hCG` (woman of 19). |
| B | blocker | `initial_tool_outputs.csf.special_tests` | CSF antibody "pending" in two keys while the labs gave the CSF titre 1:16 (C4). | FIXED: `NMDAR_antibodies` = "Positive, titer 1:16 (cell-based assay, IgG anti-GluN1; reference laboratory, resulted day 6)"; `anti_NMDAR_CSF` deleted; culture final; glucose ratio names the serum glucose (88 mg/dL); "1 cells" corrected. |
| B | blocker | `initial_tool_outputs.labs.panels` | CSF titre in the labs; serum titre twice (C4). | FIXED: CSF entry deleted; serum positive 1:32 once. |
| D | major | `initial_tool_outputs.labs.panels` | "Exclusion studies" leak, duplicate inflammatory panel, anti-TPO twice, no free T4, beta-hCG or CK; "(SIADH pattern)" in the summary (C5). | FIXED: plan panels (CBC, BMP, coagulation, inflammatory markers, thyroid function with free T4 1.0, thyroid antibodies, serum anti-GluN1, neuronal-surface panel, onconeural panel, HIV, toxicology, beta-hCG negative, CK 164 U/L normal). Plain recital. CK added because rigidity, catatonia and refusal to eat make NMS and rhabdomyolysis questions the labs must answer. |
| B/D | major | cEEG follow-up `request_continuous_eeg` | "2-3 Hz rhythmic theta" (2-3 Hz is delta); empty background; prose impression (C7). | FIXED: seizure evolution 5-6 Hz theta to 2-3 Hz sharp-wave; background filled and consistent with the routine EEG; FIRDA and slowing listed; template impression (three right temporal subclinical seizures, EDB absent). |
| D | minor | `initial_tool_outputs.eeg` | Interpretive text inside findings ("consistent with encephalopathy of uncertain etiology", "non-specific encephalopathic finding"); limitation inside the impression; prose impression (C13). | FIXED: "This is an ABNORMAL EEG due to:" numbered; limitation moved to `limitations`; background filled. |
| D | major | `initial_tool_outputs.body_imaging.impression` | "All values within normal limits." (lab template, C12). | FIXED: "Normal pelvic and abdominal ultrasound. Both ovaries normal in size and echotexture; no adnexal mass."; findings state no adnexal mass and free fluid, and include the abdomen. |
| B | major | `fallback_tool_outputs.ecg`, `.cardiac_monitoring` | ECG at 61 bpm and normal Holter (average 69) against HR 112 (C14). | FIXED: fallback ECG deleted, `initial_tool_outputs.ecg` sinus tachycardia 112 with normal intervals; telemetry fallback with sinus tachycardia to 118 bpm (range 84-118, average 100). |
| C | major | `fallback_tool_outputs.advanced_imaging`, `.specialized_test` | Catch-all fallbacks (C14). | FIXED: null; `fallback_tool_kinds` updated (also ecg). Fallback DDI `proposed` "". |
| D | major | `initial_tool_outputs.literature_search`, `.drug_interactions` | Placeholder literature and DDI repeating expected_evidence (C3). | FIXED: canonical literature plus Lejuste 2016; DDI in report voice for a patient on no medications (lorazepam, acyclovir with poor intake, IVIG, steroid, levetiracetam; D2 class warning; valproate avoided in women able to become pregnant; HBV screen; cyclophosphamide fertility). |
| C | major | literature and DDI criteria | Both recommended (rulings 5, 6). | FIXED: optional, `{}`, last. |
| C | major | `assessment.required_recommendations` | Template musts (C9); no supportive care for catatonia with refusal to eat. | FIXED: M1, M2, M3 negative screen, M4 (seizures on cEEG; valproate avoided), M5, M6 ICU (the plan rule's trigger "catatonia with refusal of food/fluids" applies; she also needs cEEG and is agitated), M7 with fertility preservation, M8 lorazepam, a supportive must (IV fluids, intake and electrolytes, nasogastric feeding if needed, VTE prophylaxis for immobility), M10. |
| C/E | minor | `assessment.prohibited_recommendations` | C9. | FIXED: canonical P1-P5. |
| C | major | `ground_truth.differential` | Templated likelihoods (C8). | FIXED: all low, with this case's evidence; the psychiatric entry names the clinic's adjustment-disorder label; NMS entry gives temperature and CK. |
| C | major | `ground_truth.key_clinical_evidence` | Template with wrong claims (C15). | FIXED: six bullets (four Graus groups once cEEG is included; definite on the CSF assay; normal MRI; EEG; negative tumor screen; outcome and benzodiazepines). |
| C/B | minor | `ground_truth.red_herrings` | Prodrome said "URI, fever, cough" (the HPI has sore throat and low-grade fever) and "should redirect"; psychiatric red herring named hallucinations not described; hyponatremia template (C15). | FIXED: data points as in the HPI; canonical interpretations; the clinic's adjustment-disorder label named as the anchor. |
| C | minor | criteria `rationale`, `citations`, `expected_evidence` | C16. | FIXED. |
| A | minor | order, `sequence_constraints`, `stop_rule` | C6, C18. | FIXED: labs, MRI, CSF, EEG, pelvic US, cEEG, DDI, literature; soft MRI-before-CSF; five required ids, max 2. |
| B | minor | `metadata.difficulty_rationale`, `.difficulty_variant_description` | "no seizures" although the cEEG captures three; "severe multistage syndrome". | FIXED: "no clinical seizures ... subclinical seizures only on continuous EEG". |
| E | minor | whole case | American-spelled case; canonical texts British. | FIXED: new text in the case's spelling. |

## Changes, in one paragraph a physician can read before re-reviewing
NMDAR-ENC-P05 (19-year-old woman with catatonia) now has the final CSF anti-GluN1 result in the CSF report: positive 1:16, with an otherwise bland CSF. Serum (1:32) is the only antibody entry in the labs. The labs were rebuilt without the leaky blocks and duplicates; free T4, a negative beta-hCG and a normal CK were added. The pelvic ultrasound and both EEG reports are written in report voice. The continuous EEG keeps its three subclinical right temporal seizures with a corrected frequency band. An ECG showing sinus tachycardia at 112 replaces the fallback ECG at 61 bpm. Literature and drug interactions are optional. The musts are the canonical set: ICU admission, because of catatonia with refusal of food; lorazepam first; seizure treatment without valproate; and a negative tumor screen with repeat imaging if she responds poorly. A supportive must was added for hydration, nutrition and VTE prophylaxis.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys used and not yet in the allow-list: `[Gresa-Arribas_2014]`, `[Lejuste_2016]`, `[Herman_2015]` (plan CENTRAL 1).

## Open questions for Andrea (judgment calls you could not settle)
None. Level of care: the plan's P05 bullet asks for ICU only with dehydration or autonomic instability, while its general M6 rule lists catatonia with refusal of food or fluids as an ICU trigger. I applied the general rule. She refuses to eat, bites staff and needs cEEG and benzodiazepine titration; her vitals alone (HR 112) would not meet it.

## Verification
Adversarial verifier, 24 Oct 2026. Checked against the plan (sections 1-4 and the per-case bullet) and ROUND_POLICY: every own-finding row against the file; criterion tiers, minimal arguments, order and ids; soft MRI-before-CSF constraint and stop rule (five required ids, max 2); CSF report carries the only CSF titre and the labs only the serum titre; musts against allergies, medications and level-of-care rule; prohibitions P1-P5; differential and key evidence against the final reports; red-herring field paths; fallbacks; a word-level diff of every changed string against HEAD (to catch accidental edits in correct prose); citation format and new-text dashes. No reviewer notes exist for NMDAR-ENC, so the notes table is complete. `perfect_agent.py -v` passes and `case_io.py check` reports no failure naming the case (case guards included).

Found and changed:
- `metadata.fallback_tool_kinds.cardiac_monitoring` FIXED to "sinus_tachycardia".
- Confirmed: four Graus groups with the cEEG seizures; ICU via catatonia with refusal of food (general M6 rule, worker's open-question note accepted); supportive hydration/feeding/VTE must appropriate; NMS excluded with stored temperature and CK; negative screen M3. No other error found.
