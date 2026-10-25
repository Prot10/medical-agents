# ALZ-EARLY-RS05
Reviewer status: R1 none, R2 none (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | The notes file has no note for ALZ-EARLY-RS05. The plan's classes (C1 to C16) were applied as class rulings (ROUND_POLICY ruling 2); each change is listed under Own findings. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C | major | ground_truth.action_criteria (new action-11-interpret-labs-mma), followup_outputs[request_mma] | B12 214 pg/mL (low-normal, plan 1.2) in a man with prior deficiency, supplements stopped 18 months ago and metformin 2 g/day, without MMA (C7.2) | FIXED: recommended criterion `interpret_labs {"panels": ["MMA"]}` placed after labs; follow-up MMA 0.58 umol/L (raised, decided from the metformin and the stopped supplements as the plan leaves to the worker); B12 replacement must with [BSH_B12_2014]; red herring, differential and key evidence updated (functional deficiency present, a contributor, not the explanation) |
| C | major | ground_truth.avoided_actions[avoid-harm-1-analyze-brain-mri] | MRI severity `harm` (score cap 0.35) for a relative contraindication: claustrophobia with sedation declined, not a device or a fragment (C14 asks to confirm the contraindication) | FIXED: severity `waste`, rationale "MRI has already failed ... reordering it does not produce images"; see Open questions. Panel exemption already present |
| B | minor | fallback_tool_outputs.mri | null, so an MRI order would have been answered by the library with a normal MRI, contradicting the case | FIXED: non-diagnostic report (stopped after the localiser because of claustrophobia); `metadata.fallback_tool_kinds.mri` "not_completed" |
| B | minor | fallback_tool_outputs.ct | "Bifrontal and bitemporal sulcal prominence" contradicts the index CT (temporoparietal greater than frontal); this fallback answers a contrast CT order | FIXED: medial temporal and temporoparietal-predominant volume loss |
| D | minor | initial_tool_outputs.ct.impression | "The limitations of CT ... are explicit" (authoring language) | FIXED: numbered impression with the canonical pattern sentence; limitation kept as a technique observation |
| C | major | ground_truth.key_clinical_evidence, red_herrings[0] | "Scheltens MTA 3/2" quoted from a CT report that has only qualitative volume loss (plan 1.2 imaging); six items including APOE and A+T+ asserted as part of the syndrome although CSF is optional (C2.6, C10) | FIXED: four items (NIA-AA 2011, B12 with MMA, what CT can and cannot show, AChEI/memantine); red herring reworded without MTA |
| B | major | patient.neurological_exam.mental_status, clinical_assessment | MMSE 21/30 but listed losses sum to 8; "MoCA not formally recorded ... estimated by examiner at 17-18" (an estimated MoCA is not a score) | FIXED: one point on the three-stage command (the exam records difficulty with three-step commands); MoCA estimate removed (the battery reports MoCA 17/30) |
| B/D | major | initial_tool_outputs.clinical_assessment | Template impression with engineering sentence; findings copied the HPI and were truncated ("sent...", ending in ";") (C3) | FIXED: impression and findings from the case; cueing field false grounded in the exam |
| B | minor | followup_outputs[neuropsych].impression | No staging statement | FIXED: canonical mild dementia sentence appended (C4) |
| B/D | major | followup_outputs[CSF] | NfL not ordered (C6); mechanistic interpretation ("reduced amyloid clearance and elevated tau phosphorylation"); interpretive text inside the glucose value | FIXED: NfL removed; vocabulary keys; values and pattern only |
| C | major | ground_truth.action_criteria[action-8-analyze-csf] | "single optional route"; amyloid PET answered by the negative library default (C2) | FIXED: CSF and amyloid_PET alternatives, canonical texts; new follow-up `order_amyloid_pet` (18F-flutemetamol PET-CT, positive, Centiloid 70) |
| C | major | ground_truth.action_criteria[action-9-search-medical-literature], followup_outputs[search_alzheimer_biomarker_management] | Literature `recommended` as a clinical step (ruling 5, C8) | FIXED: criterion and follow-up deleted |
| C | minor | followup_outputs[check_donepezil_interactions], action-10 | Content correct; criterion matched any drug | FIXED: {"drug": "donepezil"}, optional, last; warnings tidied (heart rate 74 matches the vitals) |
| D | minor | initial_tool_outputs.labs | Interpretive summary ("suboptimal glycaemic control", supplement history inside a lab report) (C7.1); CMP without albumin and total protein; reviewed-panel additions identical to other cases | FIXED: values only; albumin 4.3, total protein 7.1 added; magnesium 1.8, homocysteine 13.8, ESR 10, CRP 2.6 |
| C | major | ground_truth.differential | DLB and FTD moderate (C11); B12 entry ignored the functional deficiency | FIXED: low with excluding features; B12 entry names the raised MMA as a treatable contributor |
| C | major | ground_truth.assessment | Musts restating criteria and the "single case-designated" must; generic prohibitions (anticholinergic, benzodiazepine, antipsychotic) with no indication in this case (C12, C2.5) | FIXED: six musts (disclosure with the B12 explanation; B12 replacement; safety with medicines, finances, flooding and a driving assessment; AChEI trial; biomarker canonical; glycaemic and vascular risk); two prohibitions (attributing to B12 or deferring the diagnosis; memantine at the mild stage) |
| A/B | minor | ground_truth.action_criteria[*] | Duplicated citations; rationale = label (C13) | FIXED |
| C | minor | ground_truth.sequence_constraints, stop_rule | C16 | FIXED: clinical assessment before biomarker (soft); max_additional_actions 1; CT-before-CSF kept |
| E | minor | all new text | Case uses British spelling | kept (haemorrhage, characterise, glycaemic, localiser) |
| C | check | 3.6 check | every alternative probed on a fresh environment | CSF <- `request_csf_biomarkers`; amyloid PET <- `order_amyloid_pet`; MMA <- `request_mma`; drug check <- `check_donepezil_interactions`; MRI order <- the case fallback (non-diagnostic); contrast CT <- case fallback CT; no library answer on the pathway |

## Changes, in one paragraph a physician can read before re-reviewing
The low-normal B12 (214 pg/mL in a man with prior deficiency who stopped supplements and takes metformin) now has a recommended methylmalonic acid step, which is raised; B12 replacement is a must, and the case teaches that the deficiency is a treatable contributor, not the cause of the amnestic dementia. Ordering MRI is now penalised as waste rather than harm (claustrophobia with sedation declined is a relative contraindication), and an MRI order returns a non-diagnostic report instead of a library normal MRI. The CT impression stays within imaging and the key evidence no longer quotes an MTA grade a CT cannot give. The MMSE arithmetic is fixed and the estimated MoCA removed. The CSF report drops NfL and the mechanistic text; amyloid status can come from CSF or a positive amyloid PET. The literature step is gone. Musts: disclosure, B12 replacement, safety (medicines, finances, flooding, driving assessment), a cholinesterase inhibitor trial, biomarker testing only if it changes management, glycaemic and vascular risk; prohibitions: attributing the decline to B12 alone, and memantine at the mild stage. DLB and FTD are low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Citation keys used before they exist centrally (plan 5.2): `[NICE_NG97]`, `[BSH_B12_2014]`.
- Synonyms (plan 5.1): `accepted` carries "posterior cortical atrophy", "benson syndrome" and "early onset alzheimer" for a 68-year-old with onset at about 66 (G30.1), granted through G30.0 in `icd_codes`.
- Vocabulary: `metadata.fallback_tool_kinds.mri` uses the new kind "not_completed"; if the kinds are an enumerated list somewhere centrally, add it.

## Open questions for Andrea (judgment calls you could not settle)
- Decided, for the record: the plan (C14) keeps the MRI avoided action at `contraindicated` or `harm` only if the contraindication is confirmed. Here it is severe claustrophobia with sedation declined, which is relative (an open-bore scanner could be tried), so I set it to `waste`. If you prefer the agent not to be penalised at all for proposing an open-bore MRI, the avoided action can be deleted.

## Verification
Method: read the log, the full git diff and the whole final case (large rewrite, no reviewer notes); checked every Own-findings claim against the file; MMSE item arithmetic against the exam and the clinical assessment; CSF Abeta42/40 and glucose ratios against Abeta40 and serum glucose; heart rate in the drug check against the vitals; labels, ICD, staging field, both impressions and musts for one staging; differential against the final evidence; red-herring field paths; avoided actions against criteria and musts; fallbacks for case consistency. Probed on a fresh environment that CSF, amyloid PET and the donepezil check are answered by case-authored outputs (no library answer). perfect_agent.py -v: ok. case_io.py check: schema OK, synonym guard OK, no test failure names this case. Not a reviewed or approved case; no note ids exist for it in the notes file (none missing from the table). Also probed: an MRI order returns the case's non-diagnostic MRI fallback, not a library normal MRI.

Findings: none requiring a change.
- Checked: MMSE losses 2+1+3+1+1+1 = 9 (21/30); B12 214 low-normal with MMA 0.58 raised and homocysteine 13.8 normal, creatinine 0.99 (no renal cause of a raised MMA); B12 replacement must, red herring (path Dementia_workup[0] is B12) and differential agree; CSF 360/8050 = 0.045 and glucose 64/128 = 0.50 with serum glucose matching the labs; HR 74 in vitals, drug check and fallback ECG; the driving must matches the exam ("no longer driving for longer journeys"); onset at about 66.5 supports G30.1.
- Agreed with the worker's decision to set the MRI avoided action to `waste`: claustrophobia with sedation declined is a relative contraindication. The id still reads "avoid-harm-1-analyze-brain-mri"; ids are left unchanged by policy, the severity field governs scoring.
- The em dashes in the drug check alternatives and interactions are pre-existing in sentences the worker did not rewrite; left as is.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium_homocysteine_ESR_CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (the labs criterion label), the wording the other six cases already use.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`--prune --conditions alzheimers_early`): removed "posterior cortical atrophy" and "benson syndrome"; "early onset alzheimer" and code G30.0 (onset at 65 or later); code G30.8 (atypical presentations only). Added "late onset alzheimer". Now: codes ['G30.1', 'G30.9', 'F00']; labels after accepted[0]: ['alzheimer disease', "alzheimer's disease", 'alzheimers disease', 'alzheimer dementia', 'dementia due to alzheimer', 'late onset alzheimer'].
- Added follow-up `order_advanced_imaging` FDG_PET (trigger `order_fdg_pet`, no criterion), after the amyloid-status follow-ups: a case-specific Alzheimer-type metabolic report concordant with the MRI and stage. Before, an FDG order returned the library's normal scan, contradicting the case (summary Q4). Probed: FDG and amyloid PET orders each return their own report, in either order.
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence, normal results (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited normal results its own order (the first alternative) did not return; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-11-interpret-labs-mma]`.expected_evidence: was "Raised methylmalonic acid confirming functional B12 deficiency, a treatable contributor that does not explain the amnestic dementia profile"; now "Raised methylmalonic acid confirming a functional deficiency, a treatable contributor that does not explain the amnestic dementia profile".
- Decision: reword evidence (cited result comes from another criterion's order). The criterion is the MMA order: the B12 level comes from the dementia screen order, so the evidence now reads only the MMA result and what it means.
- Scoring: none (evidence only; the reward does not read it).

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case; the normal-row probe reports nothing for this criterion.
