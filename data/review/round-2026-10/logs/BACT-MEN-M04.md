# BACT-MEN-M04
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| efd95172-e71d-43de-8adf-eb84bec994d1 | FIXED | `patient.clinical_history.past_medical_history[3]` = "Chronic kidney disease stage 3a, estimated GFR 54 mL/min/1.73m2" (CKD-EPI 2021 from creatinine 1.4, 71, male: 53.7). Drug check re-derived from it: ampicillin 2 g every 4 hours needs no reduction at eGFR 54, reduce frequency below 50 mL/min, neurotoxicity watch; vancomycin is no longer in the regimen (conditional alternative "dosed to renal function"); gentamicin warning if added. |
| 89cd41ac-a333-4a79-806c-af6985404bfb | FIXED | HPI sentence on soft cheeses and deli meat deleted; the exposure stays only in `social_history.diet`. |
| 2b68c562-0b82-4234-ba73-93cb134c3c4d | FIXED | HARD constraint reason now rests on the left abducens palsy (WHO 2025 A.4 cranial nerve deficit; NICE NG240 1.4.7 new focal feature) and states that age, altered mental status and prednisone 7.5 mg are not criteria. The same correction in the CT criterion label, the CT must (`required_recommendations[6]`) and the LP prohibition (`prohibited_recommendations[4]`). |
| 4b70b40c-2d2f-4cdc-99bf-a31d0ccdcaf2 | FIXED | Pathway reordered: blood cultures, CT, index LP, CSF culture final report, MRI, drug check. SOFT constraint blood cultures before CT; the CT must says cultures and the first antibiotic dose with dexamethasone precede imaging. CT "No contraindication to lumbar puncture identified on this study" deleted. Treatment timing is a must (no treatment tool exists, ruling 4), so the arrival-to-first-dose interval cannot be scored as an action. |
| 40333f34-5eb6-42f3-9683-ecab5d1cb9f0 | FIXED | Blood culture follow-up (trigger renamed `request_blood_cultures`) now reports "no growth at 12 hours; final report at 5 days", no organism or susceptibilities (plan C6 item 6). Listeria is established by the CSF multiplex PCR in the index LP report and by the CSF culture final report (`request_csf_culture_final_report`, 48 hours). Narrowing sentence deleted. |
| 7efcfd89-6216-478e-818b-1f1e222d3abe | FIXED | MRI moved from `initial_tool_outputs.mri` to `followup_outputs[4]` (`request_mri_brain_contrast`), answering `action-4-analyze-brain-mri`; impression reduced to imaging findings (demyelination and "infarction is excluded" sentences removed; DWI finding kept). |
| add8da9a-5e0f-4bf3-bd35-2e177edf1022 | FIXED | Dexamethasone must with the stop rule and "Stop dexamethasone on identification of Listeria monocytogenes (WHO 2025; NICE NG240 1.8.3)"; prohibition "Do not continue adjunctive dexamethasone after Listeria monocytogenes is identified." added. |
| 7d5f57bb-28fb-4126-975f-02c61f457f20 | FIXED | Literature criterion (`action-7-search-medical-literature`) and its follow-up deleted (ruling 5; plan C9, condition-wide decision) rather than re-keyed to WHO/NICE; Brouwer 2012 is kept only for the 33% Gram-stain figure in a must and key evidence. |
| 0bea8222-5baa-445f-abd1-6c0b876388c6 | FIXED | Index CSF `glucose_ratio` = "0.17 (CSF 38 mg/dL / blood 218 mg/dL; reference 0.5 to 0.8, 0.4 or less abnormally low)". |
| fe5ef318-b083-4055-bd5e-b55ec2a47390 | FIXED | RBC "3 cells/microL (within normal limits)". |
| dbadc9d1-3fcb-4106-b891-cd410cf24a9d | FIXED | Duplicate of 0bea8222; same edit. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.csf`, CSF follow-up | index CSF given upfront; the "culture result" follow-up repeated the whole CSF with an interpretive essay | FIXED: index CSF is `followup_outputs[2]` (`request_lumbar_puncture`) with the PCR result and culture pending; the culture follow-up holds only the 48-hour identification and susceptibilities |
| C | major | `required_recommendations`, drug check | template vancomycin + ceftriaxone + ampicillin with IDSA "age >50"; nothing on 3 years of prednisone once dexamethasone stops | FIXED: canonical base and Listeria musts; new must to continue prednisone with stress-dose cover (adrenal suppression); glucose must; targeted ampicillin 21 days; public health notification of listeriosis; hearing must |
| C | major | `check_drug_interactions` tier | concrete renal dosing and steroid issues | FIXED: `action-6` raised to required (plan 4.0) and added to the stop rule; output rewritten to the real regimen (oral-contraceptive filler and formulary text removed) |
| B | minor | `patient.neurological_exam.mental_status` | GCS 13 written E4 V4 M5 while lethargic, arousable to voice and obeying one-step commands | FIXED: E3 V4 M6 (total unchanged) |
| D | minor | `patient.neurological_exam.coordination` | dysmetria "attributed to encephalopathy and diffuse weakness" pre-empts the rhombencephalitis reasoning | FIXED: attribution removed, finding kept |
| B | minor | `past_medical_history` | hypertension "controlled on amlodipine" while also on metoprolol | FIXED |
| B | minor | `labs` | abnormal summary omitted haematocrit, chloride and bicarbonate that the interpretation lists; HIV and liver tests ordered but absent | FIXED |
| B | minor | index CSF lactate, Gram stain | reference "normal <3.5" | FIXED: canonical local reference |
| C | minor | `differential` | viral meningoencephalitis high, stroke and other bacteria moderate after Listeria is identified; "Bickerstaff" misnamed as viral rhombencephalitis | FIXED: all low or very low with the excluding result |
| B | minor | `key_clinical_evidence` | "age >50", "age >71", vancomycin regimen, WHO cultures line | FIXED: WHO 2025 risk factors, canonical CT, dexamethasone and timing lines |
| B | minor | `red_herrings` | field paths into the initial CSF and MRI | FIXED: point at `followup_outputs[2]` and `[4]` |
| B | minor | avoided actions | `[IDSA_2004]` citations | FIXED |

## Changes, in one paragraph a physician can read before re-reviewing
Only labs are given upfront. The pathway is blood cultures (no growth at 12 hours, final at 5 days), CT before LP because of the left abducens palsy (HARD; after cultures, SOFT), the index LP (mixed pleocytosis, ratio 0.17, Gram stain negative, Listeria on multiplex PCR, culture pending), a CSF culture final report at 48 hours with susceptibilities, a contrast MRI for the brainstem signs (findings only), and a required drug check for CKD 3a (eGFR 54), insulin-treated diabetes and 3 years of prednisone. The literature step is gone. The exposure history appears once (social history). Musts: ceftriaxone plus ampicillin from the start, dexamethasone stopped once Listeria is identified with prednisone continued under stress-dose cover, glucose control, ampicillin for 21 days, public health notification, hearing assessment. The differential is updated to the results.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Diagnosis code: Listeria meningitis is A32.1, but the case is coded G00.8 and the G00.8 synonym entry carries the Listeria labels (plan section 5 item 5, Q8). Not changed here (ruling 3: no reviewer ruling on the label).
- Citation keys `[NICE_NG240]`, `[Brouwer_2012]` used in text.

## Open questions for Andrea (judgment calls you could not settle)
- NICE NG240 scope excludes people on immunosuppressive therapy; prednisone 7.5 mg may place him outside it. The constraint text follows the reviewer ("NICE 1.4.7 agrees") but cites only WHO 2025.
- Gentamicin for the first days of Listeria treatment is left as an option with renal caution rather than a must, given age 71 and CKD 3a.

## Verification
Adversarial verifier, 23 October 2026. Read the whole final case, the notes file and the plan entry.
- All 11 note ids are in the table and each FIXED claim holds: CKD 3a eGFR 54 (CKD-EPI 2021 from creatinine 1.4, 71, male = 53.7) in history, drug check, criterion and musts; exposure only in `social_history.diet`; WHO A.4 cranial nerve deficit reason in constraint, CT label, must and prohibition; blood cultures before CT (SOFT) and CT before LP (HARD) in the pathway; blood cultures "no growth at 12 hours; final at 5 days", no organism; MRI is a follow-up with findings only; dexamethasone stop rule as must and prohibition; literature criterion gone; CSF ratio and RBC strings canonical.
- Cross-field checks: GCS 13 = E3 V4 M6 consistent with exam text; left abducens palsy, left middle cerebellar peduncle signal and left-predominant dysmetria agree on side; ratio 38/218 = 0.17; anion gap 130 - 95 - 21 = 14; `collected_before_antimicrobials` true agrees with "no recent antibiotics"; the CSF culture final report holds only identification and susceptibilities at 48 hours; the differential is low or very low for every excluded entity; prednisone continuation with stress-dose cover does not conflict with the dexamethasone stop prohibition.
- No change made. ICD G00.8 for Listeria stays a CENTRAL item (plan Q8).
- `perfect_agent.py` ok (CT, then index LP, then MRI, then the required drug check); `case_io.py check` clean for this case.

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

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (6 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.
