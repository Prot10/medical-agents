# MG-RP13
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MG) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. July 2026 tool guidance (Reviewer 2) applied through the plan: fixed serology order, RNS technique, SFEMG only when RNS is normal, mediastinal imaging in every case, no CSF. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `patient.physical_exam.neurological` | The now-positive ice pack result (4 mm bilaterally) was stated in the HPI and exam while the ice pack test is a scored criterion; "SLURP test" is not a recognised bedside test name. | FIXED: ice pack result removed from the patient block (the prior negative test stays in the history); fatigable palatal elevation on sustained phonation; em dashes in the edited HPI removed. |
| B | minor | `patient.physical_exam.extremities`, `.general` | "Posterior subcapsular lens opacity noted by patient" under extremities after cataract surgery (incoherent); no weight or height for the respiratory report. | FIXED: extremities "No edema"; general notes pseudophakia, no proptosis or lid retraction, weight 79 kg, height 160 cm (BMI 30.9 as stored). |
| A | major | `initial_tool_outputs.labs`, follow-ups `request_achr_musk_lrp4_antibodies`, `request_mitochondrial_workup` | Serology behind a TSH stub (plan H6); a labs stub with a "borderline lactate/pyruvate ratio" that no order could reach. | FIXED: initial labs hold AChR binding 5.8 nmol/L (<=0.02), blocking 41% (<=15%), MuSK <0.02, TSH 1.9, free T4 14.6, creatinine and eGFR (contrast with metformin), HbA1c 7.4%, CK and lactate normal. Both follow-ups deleted. |
| C | minor | `followup_outputs` RNS, SFEMG | No technique, facilitation or NCS; SFEMG without fibre-pair count. | FIXED: technique, 16/13/11% decrements (orbicularis oculi, nasalis, deltoid), no facilitation, normal NCS; SFEMG 14 of 20 pairs, blocking 18%. |
| D | major | `followup_outputs` respiratory, ice pack, mitochondrial panel | Stubs whose findings repeated the expected evidence (plan I). | FIXED: respiratory FVC 2.6 L (87%, 32.9 mL/kg), MIP -58, MEP 74, all normal; ice pack MRD1 values before and after (4 mm each side, prior negative noted); mitochondrial panel with a real negative nuclear and mtDNA result and the caveat that deletions may be confined to muscle. |
| D | major | `followup_outputs` literature `search_cpeo_vs_mg_distinction` | Patient-specific summary (plan B). | FIXED: deleted; one initial literature output in report voice (Sanders 2016 / Narayanaswami 2021, Wolfe 2016), any-query safe; criterion optional `{}`. |
| C | major | `followup_outputs` drug check | Timolol called "contraindicated" in MG (it is a caution); `proposed` a trigger slug; generic pyridostigmine criterion with telithromycin in `screen_for`. | FIXED: trigger `check_timolol_pyridostigmine_interactions`, `proposed` timolol; systemic absorption and beta-blocker caution, additive bradycardia with pyridostigmine, steroid glucose warning, latanoprost and dorzolamide alternatives. Criterion recommended, drug timolol or pyridostigmine (plan 3.2). |
| A | major | `ground_truth.action_criteria` | Template criteria: labs with MuSK and LRP4; SFEMG recommended though RNS is diagnostic; literature and drug check required with fixed arguments. | FIXED: labs `["anti_AChR","TSH"]` (or `thyroid`) required; RNS required; mediastinum or chest CT with contrast required; ice pack, respiratory and timolol check recommended; SFEMG, mitochondrial panel and literature optional. |
| A | minor | `sequence_constraints`, `stop_rule` | Stop rule with literature and drug check required; max 0. | FIXED: `RNS -> SFEMG` soft; stop rule labs, RNS, CT; max 2. |
| D | minor | `initial_tool_outputs.body_imaging`, `.ecg` | CT region "mediastinum" would let a `chest_CT` order fall to the library; ECG indication "Cardiac evaluation". | FIXED: region "chest and mediastinum"; ECG indication "Baseline", interpretation text filled. |
| C | major | `ground_truth.assessment` | Musts were tests; template prohibitions with telithromycin. | FIXED: revise the label and explain it; replace timolol with latanoprost or dorzolamide via ophthalmology; pyridostigmine titration; low-dose prednisone with glucose monitoring and azathioprine after TPMT; thymectomy per MGTX (53, AChR+, no thymoma). Prohibitions: canonical drug and steroid texts; canonical attribution text with CPEO or mitochondrial cause. |
| C | major | `ground_truth.differential` | CPEO moderate after AChR+ and decrement (plan M). | FIXED: CPEO, OPMD and KSS low; timolol-induced weakness, LEMS and thyroid eye disease very_low; each with the excluding data. |
| E | minor | `ground_truth.red_herrings`, `key_clinical_evidence` | Red herrings with empty paths, one duplicate of the CPEO label, one citing the L/P ratio stub; timolol "contraindicated"; template evidence. | FIXED: three red herrings with paths (CPEO label, orbital MRI muscle volume, timolol); evidence rebuilt from the case. |
| C | minor | `fallback_tool_outputs.ct`, `.advanced_imaging`, avoided actions, patient extra keys | Head CT fallback "does not address the question" (F); FDG-PET modality label; template waste rationales; duplicate patient keys. | FIXED: plain head CT text; neutral advanced-imaging fallback; case rationales for EEG, CSF, FDG-PET, echo, cardiac monitoring; ethnicity "West African (Ghanaian)" in `demographics`, duplicates dropped; `metadata.difficulty_rationale` updated. |

## Changes, in one paragraph a physician can read before re-reviewing

A 53-year-old Ghanaian woman with hypertension, type 2 diabetes and ocular hypertension on timolol drops, labelled CPEO for ptosis since age 20, has eight months of new fatigability: diurnal ptosis, diplopia, bulbar fatigue, choking on liquids and fatigable hip flexor weakness. The positive ice pack result is no longer given in the history, so the test is ordered and scored. The pathway: AChR antibody and thyroid function in one initial panel (required; AChR 5.8 nmol/L, blocking 41%), RNS (required; facial and deltoid decrement without facilitation), contrast CT of the chest and mediastinum (required; no thymoma), ice pack test, respiratory function and a timolol drug check (recommended), and SFEMG, a mitochondrial panel (real negative result) and literature as optional. Musts revise the CPEO label, switch timolol to a prostaglandin analogue, start pyridostigmine, use cautious steroids with closer glucose control, and refer for thymectomy by MGTX criteria. CPEO is now low, and timolol is described as a caution, not a contraindication.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[Jacob_2025]`, `[Narayanaswami_2021]` (plan 5.1); cited by name until they exist.
- Synonyms (plan 5.3): "ocular myasthenia gravis" is accepted for this generalized case.
- ICD (plan 5.2): `icd_codes[0]` G70.01 for a non-crisis presentation; left unchanged pending the batch decision.

## Open questions for Andrea (judgment calls you could not settle)

- None that need information only Andrea has. Decisions taken: the mitochondrial panel is kept optional with a negative result because CPEO stays in the differential (plan 3.5); KSS kept low per the plan although onset at 20 without conduction defect makes it close to very_low.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the plan (RP13 entry) and the whole final case. Checked: no reviewer notes exist; every FIXED own finding is in the file (ice pack result out of the patient block, serology in the initial labs, labs stub and literature follow-up deleted, real mitochondrial panel kept optional, timolol described as a caution with prostaglandin and CAI alternatives, criterion recommended, CT region answers `chest_CT`). Arithmetic: FVC 2.6 L / 79 kg = 32.9 mL/kg, BMI 79/1.60^2 = 30.9; MRD1 -1 to 3 and 0.5 to 4.5 mm both 4 mm. Tiers follow plan 3.2 and 3.5; no allergy issue.

Found and fixed: C minor, the thymectomy must and `key_clinical_evidence[4]` stated thymectomy is "indicated by MGTX criteria". MGTX enrolled patients within 5 years of disease onset; if her ptosis since age 20 was myasthenic, her disease duration is over 30 years, outside the trial population. The must now asks to discuss elective thymectomy once stable as a consensus-guidance option (non-thymomatous AChR-positive generalized MG aged 18-65), stating that the expected benefit is less certain after a long ocular history; the key evidence was reworded to match.

Re-ran `perfect_agent.py MG-RP13 -v` (pass), `case_io.py check` (clean for the case) and the case guards (pass).

## Condition audit (MG auditor, 24 Oct 2026)

- fallback_tool_outputs.echo.echo_type set to TTE. FIXED.
  Why: the discriminator guard (PATTERNS.md section 5) requires an exact vocabulary value on every case fallback; an empty echo_type answered every echo variant. The RS11-RS16 verifiers fixed this only in their own cases.
- fallback_tool_outputs.advanced_imaging (empty modality) set to null; metadata.fallback_tool_kinds.advanced_imaging removed. FIXED.
  Why: a fallback with an empty modality answers every advanced-imaging study with one generic report; the benchmark library now serves the normal report for the study actually ordered.
- sequence constraint added: action-1-interpret-labs -> action-3-order-specialized-test (soft). FIXED.
  Why: plan MG.md 3.3 sets soft labs -> SFEMG and RNS -> SFEMG wherever an SFEMG criterion exists; these were missing here and present in the sibling cases.
- action-1-interpret-labs.citations: [Sanders_2016] (management guidance) -> [Punga_2022] (antibody biomarkers), plan 1.1. FIXED.
  Why: plan 1.1 reserves [Sanders_2016] for management; antibody testing cites the biomarker key [Punga_2022].
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` G70.01 -> G70.00. ICD-10-CM G70.01 is myasthenia gravis with (acute) exacerbation, including crisis; this is a new or stable presentation, not an exacerbation. G70.01 stays accepted as a secondary code (plans/MG-decisions.md, Q2).
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
