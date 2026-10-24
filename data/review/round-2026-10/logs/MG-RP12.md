# MG-RP12
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MG) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. July 2026 tool guidance (Reviewer 2) applied through the plan: fixed serology order, RNS technique, SFEMG only when RNS is normal, mediastinal imaging in every case, no CSF, no paraneoplastic panel. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness`, `patient.physical_exam.respiratory` | HPI reported the chest CT result (bronchiectasis, aspiration changes) while the chest/mediastinal CT is a required criterion; "aspiration changes on imaging" in the exam. | FIXED: HPI now has a chest radiograph with patchy lower-zone opacities; exam lists crackles only. |
| C | major | `patient.history_present_illness`, `patient.neurological_exam.cranial_nerves` | Nothing in the patient block described fluctuation or fatigability, although the differential and key evidence rested on a "fatigable diurnal pattern". | FIXED: symptoms worse towards the end of meals and in the evening, better after rest; speech more nasal on sustained counting; full eye movements and no tongue wasting stated. |
| B | minor | `patient.history_present_illness`, `demographics.bmi`, `physical_exam.general` | BMI 20.8 in the HPI vs 20.9 in demographics; "down from 24.2 two years ago" against 11 kg lost in 2 months; no weight or height for the respiratory report. | FIXED: weight 66 kg, height 178 cm, BMI 20.8 in both places, down from 77 kg two months earlier. MMSE "consistent with PD" interpretation removed. |
| A | major | `initial_tool_outputs.labs`, follow-up `request_achr_musk_lrp4_antibodies` | Serology behind a TSH stub (plan H6); TSH without units; AChR reference <0.4 with MuSK <0.4; blocking antibody in nmol/L (plan L). | FIXED: initial labs: AChR binding 4.2 nmol/L (<=0.02), blocking 38% (<=15%), MuSK <0.02, TSH 1.6, free T4 13.8, albumin 3.2 g/dL (weight loss), sodium, potassium, creatinine. Follow-up deleted. |
| C | major | `followup_outputs` RNS | 50 Hz high-rate study (plan fact 8); no technique; nothing addressing bulbar ALS, which the differential kept moderate. | FIXED: technique; facial and trapezius decrements; ADM normal; brief-exercise facilitation 3%; normal NCS; needle EMG of genioglossus, FDI, tibialis anterior and thoracic paraspinals without denervation or fasciculations. |
| D | major | `followup_outputs` respiratory_function (two), ice pack | NIF -62 called "meets threshold for adequate"; second respiratory and ice pack follow-ups were stubs repeating the expected evidence (plan H2, I); ice pack criterion in a man with no ptosis (plan 3.2). | FIXED: one respiratory report (FVC 3.2 L, 82%, 48.5 mL/kg; MIP -62; MEP 96; mouth seal caveat); stub and ice pack follow-up deleted; ice pack criterion (`action-8`) deleted (library answers an ice pack order with a normal no-ptosis report). |
| D | major | `followup_outputs` literature | Patient-specific summary ("dysphagia disproportionate to PD severity is the key diagnostic clue", plan B). | FIXED: deleted; one initial literature output in report voice (Sanders 2016 / Narayanaswami 2021, Gilhus 2016); criterion optional `{}`. |
| C | minor | `followup_outputs` drug check | `proposed` a trigger slug; prednisone and mycophenolate interactions as if already planned. | FIXED: trigger `check_pyridostigmine_levodopa_interactions`, `proposed` pyridostigmine; levodopa, amlodipine, aspirin; anticholinergics; steroid effects in PD; metoclopramide; levodopa not to be stopped. Criterion optional (no concrete interaction, plan 3.2). |
| D | minor | `initial_tool_outputs.body_imaging`, `.ecg` | CT impression said aspiration changes were "consistent with severe dysphagia" (clinical cross-reference); ECG indication "atrial fibrillation screening in progressive dysphagia workup" and "LVH (consistent with hypertension history)". | FIXED: CT reworded to imaging terms, numbered impression, region "chest and mediastinum" (answers `chest_CT` too); ECG indication "Baseline", LVH stated without the clinical link. |
| A | major | `ground_truth.action_criteria` | Template criteria (labs with MuSK and LRP4; SFEMG recommended although RNS is diagnostic; literature and generic pyridostigmine check required; ice pack without ptosis; labels equal rationales). | FIXED: labs `["anti_AChR","TSH"]` (or `thyroid`) required; RNS required; mediastinum or chest CT with contrast required; respiratory recommended; SFEMG, drug check and literature optional. New labels and rationales. |
| A | minor | `sequence_constraints`, `stop_rule` | `labs -> RNS` with an SFEMG reason; max 0 with literature and drug check required. | FIXED: `RNS -> SFEMG` soft; stop rule labs, RNS, CT; max 2. |
| C | major | `ground_truth.assessment` | Musts were tests ("Confirm AChR", "CT chest", "Single-fiber EMG to disambiguate from ALS", which SFEMG cannot do, fact 7); no treatment of severe bulbar MG. | FIXED: seven musts: admission with IVIG 2 g/kg or PLEX for severe bulbar weakness (fact 21); pyridostigmine before meals; low-dose prednisolone titrated inpatient with azathioprine after TPMT; nil by mouth for thin liquids, SLT, NG feeding and dietitian; serial bulbar and respiratory monitoring; levodopa without interruption; MG-safe antibiotic if aspiration pneumonia. No thymectomy must (age 74, no thymoma, plan RP12). Prohibitions: canonical drug and steroid texts, metoclopramide (kept, reworded), canonical attribution text with Parkinson disease. |
| C | major | `ground_truth.differential` | Recurrent NSCLC, PD bulbar progression and bulbar ALS all moderate after a negative CT, decrement, AChR+ and no fasciculations (plan M); LEMS "smoker" in a non-smoker; oesophageal entry argued from "fatigable ptosis" he does not have. | FIXED: PD, ALS and recurrence low; LEMS, brainstem lesion and oesophageal disorder very_low; each with the excluding data from the case. |
| E | major | `ground_truth.red_herrings`, `key_clinical_evidence` | Red herrings cited a "borderline anti-VGCC 0.04 nmol/L" and a "paraneoplastic panel negative" that exist nowhere in the case; template evidence (telithromycin, "SFEMG distinguishes NMJ from motor neuron disease", wrong). | FIXED: two red herrings with paths (PD; resected lung cancer with weight loss); evidence rebuilt from the case. |
| C | minor | `fallback_tool_outputs.advanced_imaging`, `.ct`, avoided actions | FDG-PET fallback describing carotid plaque; head CT fallback "does not address the question"; `[Wolfe_2016]` on waste items; extra patient keys. | FIXED: neutral advanced-imaging fallback; plain head CT; case rationales, citations cleared; ethnicity "Japanese" in `demographics`, duplicates dropped. |

## Changes, in one paragraph a physician can read before re-reviewing

A 74-year-old Japanese man with mild, stable Parkinson disease on levodopa and a lung adenocarcinoma resected 7 years ago has two months of fluctuating dysphagia, hypophonic nasal speech, nasal regurgitation and 11 kg weight loss, with weak palate and tongue but no ptosis. The history now describes the fatigability the diagnosis rests on, and no longer gives away the chest CT. The pathway: AChR antibody and thyroid function in one initial panel (required; AChR 4.2 nmol/L), RNS with needle EMG (required; cranial and trapezius decrement without facilitation, no denervation, which now argues against bulbar ALS), contrast CT of the chest and mediastinum (required; no recurrence, fatty thymus, aspiration damage), respiratory function (recommended, normal), and optional SFEMG, drug check and literature. The ice pack test is gone (no ptosis). Musts treat severe bulbar MG (admission, IVIG or plasma exchange, pyridostigmine before meals, cautious steroids, nasogastric feeding and swallow assessment, levodopa continued). Parkinson progression, ALS and cancer recurrence are now low, and the red herrings no longer cite a VGCC result that the case never had.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[Jacob_2025]`, `[Narayanaswami_2021]` (plan 5.1); cited by name until they exist.
- Synonyms (plan 5.3): "ocular myasthenia gravis" is accepted for this bulbar generalized case.
- ICD (plan 5.2): `icd_codes[0]` G70.01 for a non-crisis presentation; left unchanged pending the batch decision.

## Open questions for Andrea (judgment calls you could not settle)

- None that need information only Andrea has. Decisions taken: fluctuation added to the history (the case's own reasoning required it and the source picture is bulbar MG); needle EMG added to the RNS session so the ALS exclusion is supported by data in the case.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the plan (RP12 entry) and the whole final case. Checked: no reviewer notes exist; every FIXED own finding is in the file (chest CT result out of the HPI, fatigability now described, weight 66 kg / height 178 cm / BMI 20.8 consistent in HPI, demographics and exam, serology in the initial labs, one respiratory report, ice pack criterion and stub removed with no ptosis on exam, needle EMG added to the RNS report supporting the ALS exclusion, invented VGCC red herring removed). Arithmetic: FVC 3.2 L / 66 kg = 48.5 mL/kg. Musts are correct for severe bulbar MG at 74 (IVIG or PLEX, pyridostigmine before meals, cautious steroids, NG feeding with levodopa continued, no thymectomy without thymoma); the metoclopramide prohibition is valid. Differential matches the final evidence (PD, ALS, recurrence low after CT, EMG and serology).

Found and fixed: E minor, `metadata.difficulty_rationale` (5 required, 1 red herring) updated to 3 required, 2 red herrings. No clinical change needed.

Re-ran `perfect_agent.py MG-RP12 -v` (pass), `case_io.py check` (clean for the case) and the case guards (pass).

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
