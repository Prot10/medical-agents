# VASC-DEM-P03
Reviewer status: R1 none, R2 none (VASC-DEM has no notes file; never reviewed) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note exists for this case or condition. All changes below come from the condition plan (classes C1-C19) and from my own audit. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | blocker | `ground_truth.action_criteria[action-4-analyze-brain-mri].alternatives` | Plan C1: `required_arguments` held `contrast`, `protocol` and the non-schema key `sequences`, so no real call could match the required MRI. | FIXED: one alternative, `analyze_brain_mri {}`; label, rationale and expected evidence rewritten (STRIVE-2 terms, SWI, Boston v2.0). |
| D | major | `initial_tool_outputs.literature_search`, `fallback_tool_outputs.literature_search`, criterion `action-7-search-medical-literature` | Plan C2: literature output repeated the criterion's expected evidence (failed `test_case_guards` leak test). | FIXED: criterion deleted, initial output null, fallback deleted. |
| B | minor | criterion `action-8-check-drug-interactions`, `fallback_tool_outputs.drug_interactions` | Plan C3 group D: generic optional drug check and a generic "no prohibitive interaction" fallback. | FIXED: criterion and fallback deleted; initial stays null. The aspirin decision is a must, not a drug check. |
| D | major | `patient.neurological_exam.mental_status` | Plan C4: stated the MoCA total and item losses, i.e. the result of the required screen. | FIXED: bedside observation only, ending "Formal cognitive screening reported separately". |
| D | major | `initial_tool_outputs.mri.impression`, `.additional_observations` | Plan C5: impression named the cognitive syndrome ("vascular cognitive disorder on this substrate") and called the episodes TFNE; observations argued against hypertensive arteriopathy and stated the TFNE/TIA conclusion. | FIXED: numbered modality-only impression keeping the Boston v2.0 sentence (Kind 2); observations now pertinent negatives (no deep/infratentorial microbleed, no acute haemorrhage or restricted diffusion, basal ganglia PVS not enlarged). |
| B | major | `initial_tool_outputs.mri.findings[Cortical superficial siderosis].location` | Laterality: the episodes are right hand and face, but siderosis was placed over the right central sulcus (left parietal convexity second). | FIXED: "Left central sulcus and right parietal convexity" (still two sulci, focal); impression and differential agree. |
| C | minor | `initial_tool_outputs.mri.findings[Enlarged perivascular spaces]`, `ground_truth.key_clinical_evidence[3]`, `metadata.key_educational_points[2]` | Grade 2 centrum semiovale PVS and "posteriorly weighted white matter change" were presented as Boston v2.0 supportive markers; v2.0 counts only severe CSO-PVS (>20 in one hemisphere) and a multispot WMH pattern, and only for a single lobar haemorrhagic lesion. | FIXED: PVS signal text descriptive; KCE and educational point state the actual v2.0 white matter features and that the haemorrhagic lesions alone meet the criteria here. |
| D | major | `initial_tool_outputs.advanced_imaging` (amyloid PET) | Plan C5/C9: impression "consistent with cerebral amyloid angiopathy ... Management is already determined by the MRI findings"; finding "Less typical of parenchymal Alzheimer distribution"; caveat field in quantitative data. | FIXED: binary "Positive amyloid PET" impression with SUVr; findings descriptive; caveat removed. |
| D | major | `initial_tool_outputs.clinical_assessment.impression` | Plan C5: "Instrumental independence is lost. The profile is compatible with a vascular cognitive disorder; the mechanism is the question the imaging must answer." | FIXED: totals and item losses only (MoCA 20/30, no education correction, recall 2/5 to 4/5 with cueing, fluency, FAQ 16/30, GDS-15 3/15). MoCA arithmetic checked: 10 points lost = 20/30. |
| D | major | `initial_tool_outputs.specialized_test.impression` | Plan C5: "a functional scale confirming lost independence" (the dementia threshold). | FIXED: profile statement per plan with premorbid estimate and FAQ value. |
| B | major | `initial_tool_outputs.labs` | Plan C6: female Hb/Hct ranges in a man; INR in the CMP with interpretive `clinical_significance`; eGFR range ">60"; template values (WBC 6.8, Hct 41.6, MCV 88, Na 139, K 4.2, ALT 22, albumin 4.1, folate 11.8); interpretation drew conclusions ("excluding reversible causes", "not iatrogenic or haematological"). | FIXED: Hb 13.5-17.5, Hct 41.0-53.0 (Hct 41.3 with Hb 13.8); eGFR ">=60"; new `Coagulation` panel (PT 12.1 s, INR 1.0, aPTT 29 s); values varied within range (WBC 7.3, MCV 91, Na 141, K 4.5, ALT 18, albumin 4.0, folate 9.6); interpretation "No flagged values. All results within reference ranges." |
| B | major | `fallback_tool_outputs.advanced_imaging`, `.labs`, `.ct`, `.echo` | Plan C7: fallbacks revealed off-pathway status ("non-contributory", "better characterised on the MRI already obtained"); echo impression "No cardioembolic source identified". | FIXED: advanced_imaging and labs fallbacks deleted; CT fallback rewritten as this patient's CT (right parietal chronic haemorrhage cavity, posterior WM hypodensity, atrophy, CT cannot show microbleeds or siderosis); echo impression descriptive. EEG and Holter fallbacks consistent, kept. `metadata.fallback_tool_kinds` updated to the remaining fallbacks. |
| B | minor | `followup_outputs` | Library CSF would return normal Abeta42 (980 pg/mL) if a model ordered an LP anyway, contradicting the positive amyloid PET and the CAA biology. | FIXED: case-authored CSF follow-up (trigger `request_csf_biomarkers`): no pleocytosis, Abeta42 290 and Abeta40 4300 pg/mL both decreased, ratio 0.067, p-tau181 and total tau normal (the reported CAA pattern of reduced Abeta40 and Abeta42). Probed: `analyze_csf {}` and with special tests return it. |
| C | major | `ground_truth.avoided_actions[avoid-harm-1-analyze-csf]` | Plan C9: LP is not harmful in chronic CAA without acute haemorrhage; rationale claimed CSF cannot separate vascular from parenchymal amyloid. | FIXED: severity `waste`, rationale "Boston v2.0 diagnosis rests on MRI; CSF would not change management." Id kept (referenced nowhere else; ids are stable). |
| C | minor | `ground_truth.avoided_actions[*].rationale` | Plan C18: CT rationale "already obtained"; echo/monitoring rationales said "small-vessel burden"; generic EEG/DaTscan/MIBG/autoimmune text. | FIXED: case-specific rationales (CT per plan wording; echo and monitoring: no ischaemic infarct, non-ischaemic episodes, regular pulse). |
| A | minor | `ground_truth.action_criteria[*].citations`, `.rationale` | Plan C13: rationale identical to label; unbracketed duplicate keys. | FIXED: one-sentence case-specific rationales; bracketed keys only (labs adds `[AHA_ASA_2011_VCI]`, MRI adds `[Boston_v2]`, PET cites `[Boston_v2]`). Expected evidence made case-specific (screen, labs, MRI, neuropsych, PET). |
| B | minor | `ground_truth.action_criteria` order | Plan C16 order: screen, neuropsych, labs, MRI, biomarker. | FIXED: reordered, ids kept. PET label now "only if coexisting Alzheimer pathology would change management" (optional; the old label described CSF being declined, which is not this case). |
| B | minor | `ground_truth.stop_rule.max_additional_actions` | 0 everywhere (plan C16). | FIXED: 1. Required set unchanged (screen, labs, MRI). Existing soft constraint screen before MRI kept. |
| C | major | `ground_truth.assessment.required_recommendations` | Plan C19: two musts restated tool steps (obtain MRI with SWI, exclude reversible causes); no BP target although BP is 134/76 after an ICH; no LAAO pathway; no citations. | FIXED: six musts: TFNE recognition and explanation [Boston_v2]; diagnosis by Boston v2.0 with dementia-severity VCI [Boston_v2] [VASCOG_2014]; stop aspirin [AHA_ASA_2022_ICH]; avoid anticoagulation, LAAO if AF is found [AHA_ASA_2022_ICH]; BP below 130/80 (now 134/76 on ramipril 5 mg) [AHA_ASA_2022_ICH]; counselling on recurrence, emergency warning signs, dementia support. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | LP prohibition partly wrong (Abeta40 is reduced in CAA); thrombolysis prohibition ("without reconsidering this diagnosis") not checkable and outside this encounter. | FIXED: LP prohibition per plan wording [Boston_v2]; thrombolysis prohibition removed; anticoagulation prohibition reworded; antiplatelet and hypertension-attribution prohibitions kept. |
| C | major | `ground_truth.differential[0]`, `[1]` | Plan C8: TIA and hypertensive arteriopathy left `moderate` although the MRI excludes them. | FIXED: both `low`, key features cite the MRI (no infarct, siderosis over the left central sulcus; all eleven microbleeds lobar, no deep microbleed). Mixed AD entry key features no longer assume the optional PET was done. |
| B | minor | `ground_truth.red_herrings[*].field_path` | Empty field paths. | FIXED: `patient.clinical_history.past_medical_history[0]` and `[3]`. |
| E | minor | `initial_tool_outputs.clinical_assessment.findings[*].performance` | Em dashes in three untouched finding strings. | FLAGGED: left (plan: replace a dash only in a sentence rewritten anyway). |
| D | minor | `initial_tool_outputs.clinical_assessment.criteria_met.independence_in_iadl_lost` | Structured flag states the functional threshold. | FLAGGED: kept; it records the informant FAQ (16/30) and the HPI's lost finances, objective data the agent still has to weigh; same template field exists in all 30 cases, for the lead to decide condition-wide. |
| - | check | plan 3.6 | perfect_agent.py ok (screen, neuropsych, labs, MRI from case outputs; `-v` shows "?" for three because the stored dicts differ only by None fields; probed separately: none from fallback or library). `test_case_guards -k VASC-DEM-P03` 2 passed. `case_io.py check`: schema OK, no failure names P03. `sequences` count 0. | - |

## Changes, in one paragraph a physician can read before re-reviewing

The case is unchanged in substance: a 76-year-old former headmaster with stereotyped right hand-to-face spreading paraesthesias treated as TIAs with aspirin, two years of decline with lost finances, and a prior right lobar haemorrhage; MRI shows eleven strictly lobar microbleeds, focal cortical superficial siderosis and the old lobar cavity, meeting Boston v2.0 for probable CAA. The siderosis now sits over the left central sulcus (and right parietal convexity) so it matches the right-sided episodes. The exam no longer gives the MoCA; the screen, neuropsychology, MRI and amyloid PET reports now describe only their own findings (no diagnosis of the cognitive syndrome, no TFNE verdict, no management), with the MRI keeping its Boston v2.0 statement and the PET read simply as positive. Labs use male ranges, INR sits in a coagulation panel, and the interpretation lists no flagged values. The literature and drug-check steps are gone, the MRI criterion can now be matched by a real call, LP is waste rather than harm (a case CSF result showing reduced Abeta40 and Abeta42 is there if one is ordered anyway), and TIA and hypertensive arteriopathy are low in the differential. Musts now ask to stop aspirin, avoid anticoagulation with LAAO if AF appears, bring BP below 130/80 (134/76 now), recognise and explain TFNE, and counsel the family.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- New citation key used: `[AHA_ASA_2022_ICH]` (plan 5.4, allow-list in the criteria pack).
- Synonyms (plan 5.1): add CAA labels and I68.0 for this case; `F06.7` should not be accepted for a dementia-severity case.
- Library: the `analyze_csf` library default returns a normal Abeta42 (980 pg/mL) for any case; harmless here now that the case authors its own CSF, but worth knowing for other CAA or mixed cases.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the diff and the whole final case (patient, ground truth, every initial, follow-up and fallback output, metadata). Verified: siderosis laterality (left central sulcus) now matches the right hand-to-face episodes in impression, finding, differential and musts; old right parietal cavity consistent in MRI, CT fallback and history; MoCA arithmetic (10 points lost = 20/30) and exam orientation (date incorrect) agree; CSF follow-up arithmetic (290/4300 = 0.067) and CAA pattern; musts and prohibitions consistent (aspirin stopped, no anticoagulation, LP waste, no statin prohibition, atorvastatin continued); C2, C3 group D, C5, C6, C7, C8, C9, C13, C16, C18 applied; no `sequences` key; no dashes in new text; no diagnosis or management statement left in any report beyond the Boston v2.0 Kind 2 sentence.
Found and changed: eGFR 72 did not match creatinine 0.94 mg/dL in a 76-year-old man (CKD-EPI 2021 about 84; plan C6 lab arithmetic, same class the worker fixed in P06 and P08). Set `initial_tool_outputs.labs.panels.CMP[eGFR].value` to 84 (not flagged). Nothing else changed. perfect_agent.py pass; case_io.py check: schema OK, no failure names P03; test_case_guards pass.

## Condition audit
Condition auditor, 24 Oct 2026. Scripted checks over all 30 VASC-DEM cases (plan classes C1-C21, PATTERNS.md, lab arithmetic) found the stragglers below in this case; changed through `case_io`.

| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels.Vascular_risk[Total cholesterol]` | Total cholesterol 156 mg/dL did not equal LDL + HDL + TG/5 (151.6); the same lab-arithmetic class was fixed in M07-M10, P01, P02 and S06-S11 but not here. | FIXED: total cholesterol 152 mg/dL (flag unchanged; LDL, HDL and TG, which the musts and evidence quote, unchanged). |
| D | minor | `initial_tool_outputs.clinical_assessment.findings[Memory].performance` | Plan C5 (screen gives scores only): "— retrieval pattern" was an interpretive label left in the screen, removed in the other cases' screens. | FIXED: "2/5 unaided, 4/5 cued" (scores only; also removes the em dash). |
| D | major | `initial_tool_outputs.clinical_assessment.criteria_met` | Plan 1.2 and C5 (no report states the severity): the screen's structured fields still carried independence_in_iadl_lost, executive_predominant_profile, i.e. the mild-versus-major threshold, the profile verdict or history items. Workers removed these keys in the other 19 cases; here they survived (the P03 worker flagged the question for a condition-wide decision). | FIXED: keys removed; `criteria_met` keeps domain impairment and cue-responsive recall. The informant FAQ score stays in the report as an instrument score. |

perfect_agent.py, case_io.py check and test_case_guards re-run on all 30 VASC-DEM ids: clean.

## Close-out (24 Oct 2026)

Condition close-out per `plans/VASC-DEM-decisions.md`.

- Synonyms (diagnosis_synonyms.yaml, applied with `--prune --conditions vascular_dementia`): F06.7, I67.3 and the umbrella "vascular cognitive impairment" no longer accepted (mild-VCI answers must not score in a dementia case); subtype labels scoped by mechanism, here "cerebral amyloid angiopathy", "CAA" and I68.0. Generic labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0-C0.
- `action-3-interpret-labs`: RPR and HIV removed from `required_arguments.panels` and the label; `[AAN_dementia_2001]` added. AAN 2001: syphilis screening "is not justified unless clinical suspicion for neurosyphilis is present"; NICE NG97 does not test routinely; this case has no risk factor. The stored labs output keeps its RPR and HIV results, so an agent that orders them still receives them (decision Q1).
- `metadata.revision_reason`: the stale August literature/interaction audit text replaced by the round's (summary CENTRAL 9; not read by the harness).
- `metadata.fallback_tool_kinds`: ct normal->case (the fallback describes this patient, not a library normal; summary CENTRAL 9).

Checks after the close-out: `perfect_agent.py` and `case_io.py check` clean for this case; `test_case_guards -k VASC-DEM-` clean; `apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-3-interpret-labs]`.alternatives: was [CBC, CMP, TSH, B12, folate, HbA1c, lipid_panel]; now [CBC, CMP, TSH, B12, folate, HbA1c, lipid_panel, coagulation] | [CBC, CMP, TSH, B12, folate, HbA1c, lipid_panel].
- Decision: serve: new first alternative (old order kept as an alternative). The rationale says blood count and coagulation matter for the antithrombotic decision after a prior haemorrhage, and the evidence reads the INR; the order did not return coagulation.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.
