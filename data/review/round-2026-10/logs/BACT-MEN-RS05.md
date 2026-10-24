# BACT-MEN-RS05
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| b31acc34-bc1e-4e06-95ec-a642788726a4 | FIXED | Dexamethasone must replaced by the plan C5 canonical sentence plus "Stop dexamethasone on identification of Listeria monocytogenes (WHO 2025; NICE NG240 1.8.3)" (empirical dexamethasone for possible pneumococcal disease, stopped on Listeria, as the reviewer asked); new prohibition "Do not continue adjunctive dexamethasone after Listeria monocytogenes is identified"; the canonical sentence also in key evidence. Because the patient has taken prednisone for 4 years, a new must keeps glucocorticoid cover when dexamethasone stops (the reviewer's point about chronic prednisone). |
| b760f9e4-ea41-474b-bd8b-5c886f0e75ea | FIXED | Imaging C (plan 4.0): `action-4-order-ct-scan`, the HARD constraint and the CT follow-up deleted; CT id removed from `stop_rule`; must "Proceed to lumbar puncture without prior cranial imaging ... (GCS 12, no focal signs, no new cranial nerve deficit (the reduced hearing is longstanding presbycusis), no papilloedema, no new seizure, not severely immunocompromised: prednisone 7.5 mg daily with weekly methotrexate)"; C prohibition; waste avoided action `avoid-waste-6-order-ct-scan`; the "three independent imaging-first criteria per IDSA 2004" key evidence line replaced by the C must. |
| 44bb31ec-78d2-41bf-bec1-ddc7c92d6884 | FIXED | Blood culture follow-up (trigger renamed `request_blood_cultures`): findings list all four bottles (aerobic bottles of both sets positive at 22 and 26 hours, anaerobic bottles no growth at 5 days) plus the identification row; impression "Listeria monocytogenes isolated from 2 of 4 bottles (the aerobic bottles of both sets) at 22 and 26 hours; susceptibilities as listed." MICs moved to `susceptibility`; `gram_stain` filled; the "interpretable" boilerplate deleted. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A/D | major | initial_tool_outputs.csf | Index CSF in the initial work-up (C1), with the culture already reporting Listeria at the time of the LP | FIXED: moved to follow-up `request_lumbar_puncture` (initial `csf` null); culture "Pending"; perfect agent confirms action-3 receives it |
| B/D | major | index CSF | "RBC 8 (likely traumatic tap artifact)", "normal >0.6" ratio, lactate reference "normal <3.5", "consistent with bacterial infection" interpretation; panel listing S. aureus, which the multiplex panel does not target (C7) | FIXED: RBC value only, canonical ratio (22/112 = 0.20) and lactate strings, interpretation values and pattern only, panel result with the real target list (key renamed `Meningitis_PCR_panel`) |
| C | major | action-5 literature, followup | Literature criterion expecting IDSA 2004 and ESCMID 2016, first pathway step (C9, ruling 5) | FIXED: deleted |
| C | major | assessment.required_recommendations | Template regimen "ampicillin + vancomycin 15-20 mg/kg + ceftriaxone"; AUC-guided vancomycin must (C4) | FIXED: canonical base and Listeria musts (age 78; prednisone and methotrexate); vancomycin conditional; vancomycin monitoring kept only as a drug-check warning |
| C | major | action-6 check_drug_interactions | Recommended; output and expected evidence missed the penicillin-methotrexate interaction and the co-trimoxazole-methotrexate hazard; template vancomycin; dexamethasone timing text | FIXED: required (plan 4.0); output checks the real regimen against methotrexate (penicillins reduce its clearance; co-trimoxazole additive antifolate), prednisone (adrenal suppression), renal dosing (eGFR about 42), gentamicin caution, the other medicines; added to `stop_rule` |
| C | major | assessment | No plan for chronic glucocorticoid once dexamethasone is stopped after 4 years of prednisone | FIXED: must for continued glucocorticoid cover with stress dosing |
| C | minor | assessment | Methotrexate must tied to the dexamethasone course; targeted must "ampicillin monotherapy ... 21 days" without renal review; droplet must phrased "until Listeria confirmed (not droplet-transmitted ...)" | FIXED: methotrexate must with the interaction and monitoring; targeted must with MIC, renal review, stop ceftriaxone, 21 days (NICE NG240); droplet must in the condition's wording |
| B | major | patient.clinical_history.past_medical_history | "CKD stage 2 (baseline creatinine 1.1)": CKD-EPI 2021 for a 78-year-old woman gives eGFR about 52, stage 3a | FIXED: "Chronic kidney disease stage 3a (baseline creatinine 1.1 mg/dL, eGFR about 52 mL/min/1.73m2)"; current eGFR about 42 used throughout |
| B | major | initial_tool_outputs.labs.panels.CBC | Differential 106% (neutrophils 88, bands 8, lymphocytes 4, monocytes 6) | FIXED: neutrophils 82; summary and interpretation updated |
| B | minor | initial_tool_outputs.labs | HIV and albumin ordered by action-1 (HIV, CMP) but absent (C12) | FIXED: HIV-1/2 Ag/Ab non-reactive, albumin 3.6 g/dL |
| C | major | red_herrings[0], key_clinical_evidence, differential, prohibition | Drug-induced aseptic meningitis described as "sterile lymphocytic CSF"; it is often neutrophilic, and methotrexate meningitis follows intrathecal or high-dose use | FIXED: corrected in all four places (sterile CSF with normal glucose; not low-dose oral therapy) |
| C | minor | ground_truth.differential | Viral meningitis "moderate" after a bacterial CSF; endocarditis entry citing a "vegetation on echo" that the pathway never performs (C10) | FIXED: six entries, all low with excluding data; endocarditis replaced by pneumococcal meningitis (the empirical target), HSV encephalitis added |
| D | minor | patient.history_present_illness | Undeclared "worst headache of her life" (C11) | FIXED: "a severe, rapidly worsening diffuse headache" |
| D | minor | red_herrings | Undeclared distractor: a week of nasal congestion attributed to a viral illness | FIXED: declared as `red_herrings[1]` |
| B | minor | key_clinical_evidence | "vancomycin + ceftriaxone backbone"; culture-confirmed CSF claim; WHO line | FIXED: ceftriaxone backbone; organism established by CSF PCR and blood cultures with the Listeria Gram stain sensitivity (Brouwer 2012); C17 timing line; empirical line added |
| B | minor | fallback_tool_outputs.eeg | "This is a NORMAL EEG" with a mildly slow background | FIXED: classification abnormal, impression "Mild diffuse slowing", limitation "Recorded in a drowsy patient" |
| C | minor | citations | `[IDSA_2004]`, free-text duplicates, De Gans on the drug check | FIXED: `[WHO_Meningitis_2025]` |
| B | minor | metadata.difficulty_rationale | Counted CT and literature; "age>60" as a CT criterion | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
The pathway is blood cultures, then lumbar puncture without prior CT (GCS 12, no focal or new cranial nerve signs, no papilloedema, no seizure; low-dose prednisone with weekly methotrexate is not severe immunocompromise, so CT is a waste action), then a required drug check. The literature step is gone. The index CSF reports values only (Gram-positive rods, Listeria on the panel with its real targets, culture pending); the blood culture report gives all four bottles with times, MICs and a matching impression. Management: ceftriaxone within 60 minutes with ampicillin (age 78, immunosuppression), dexamethasone started empirically and stopped on Listeria, continued glucocorticoid cover after 4 years of prednisone, methotrexate held (penicillin interaction, eGFR about 42), droplet precautions, ampicillin for 21 days with renal review, audiology. The methotrexate red herring now gives correct facts, and the nasal congestion is declared. Record fixes: CKD stage 3a, CBC differential 100%, HIV and albumin, headache wording, EEG fallback.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Diagnosis code (plan section 5 item 5, Q8): Listeria meningitis is A32.1; this case carries G00.8. Not changed here (no reviewer ruling on the label).
- Citation keys `[WHO_Meningitis_2025]`, `[Brouwer_2012]` (cited in key evidence text) for the allow-list.

## Open questions for Andrea (judgment calls you could not settle)
- Plan Q2: CT as `waste` in this no-criterion case.
- The GCS 12 (E3 V4 M5) is kept as recorded; she converses coherently when awake, so M6 (obeys) is possible, which would make 13. Either way it is above the WHO threshold.
- Gentamicin synergy is mentioned only as a caution in the drug check, not as a must, given eGFR about 42.

## Verification
Adversarial check (23 October 2026) of the log against the case file, the plan (4.0 row RS05: imaging C, Listeria yes, stop dexamethasone on Listeria, DDI required for penicillin-methotrexate) and notes b31acc34, b760f9e4, 44bb31ec (all in the table). Read the whole final case. Confirmed: dexamethasone must stops on Listeria with the matching prohibition, and glucocorticoid cover after 4 years of prednisone is a must; CT criterion, constraint and follow-up deleted with C must, prohibition and waste action; blood culture impression and findings agree on 2 of 4 bottles; index CSF served to action-3 by `request_lumbar_puncture`, culture pending; drug check required with the real methotrexate interaction; CKD stage 3a and eGFR about 52 (baseline creatinine 1.1) and about 42 (creatinine 1.3, woman, 78) recomputed and correct; CBC differential 100%; anion gap 11; `collected_before_antimicrobials` true is correct (no antimicrobials); Listeria duration 21 days per NICE NG240.
Found and changed: (1) The worker's open question on the GCS is a real inconsistency: M5 (localises) was recorded while the motor text graded strength 4/5, which needs a patient who obeys commands (M6). The recorded GCS 12 is kept (it is used in the must, the waste rationale and key evidence, and either value is above the WHO threshold); `patient.neurological_exam.mental_status` now states "Does not follow commands; localises a painful stimulus with either hand." and `motor` says strength appears grossly 4/5 but cannot be formally tested because she does not follow commands. (2) `metadata.difficulty_description` "age >60" reworded "age over 60" (plan CENTRAL item 9 string). (3) `fallback_tool_outputs.eeg` called the background "mildly slow for age" with an 8-9 Hz posterior rhythm, which is normal at 78; the posterior rhythm is now 7 Hz, matching the abnormal classification and the "mild diffuse slowing" impression. `perfect_agent.py -v` passes; `case_io.py check` clean for the case.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
Label change (CENTRAL 5): `icd_codes[0]` G00.8 -> A32.11 (listerial meningitis; ICD-10-CM G00 excludes Listeria), since `accepted[0]` already names Listeria monocytogenes. Listeria labels now come from a new A32 entry.
- labels removed: "pyogenic meningitis"
- labels added: "listerial meningitis"
- codes removed: G00.8
- codes added: A32.11, A32.1, A32.12
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (4 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients
- 'Annex A.4' renamed 'section A.4' in metadata text as well

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'MRI', impression 'No abnormality identified.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
