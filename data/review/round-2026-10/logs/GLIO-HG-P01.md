# GLIO-HG-P01
Reviewer status: R1 not reviewed, R2 needs_changes (3 notes) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| d3ff3f30-423f-43d0-bd20-50eee7bd3995 | FIXED | `ground_truth.red_herrings[0].correct_interpretation` rewritten from the printed data: the thin smooth ring with central restricted diffusion keeps abscess open, the WBC 11.2 within hours of a tonic-clonic seizure with normal procalcitonin and no fever does not indicate infection, rim rCBV 2.8 and absent amino-acid peaks favour tumour, and the sterile aspirate with glioblastoma histology decides. The differential's abscess entry, `red_herrings[1]` and key evidence no longer claim rim restriction or a necrotic thick ring. |
| e25c4336-c148-4b60-a14a-2fcbf6f6c227 | FIXED | `patient.history_present_illness`: the non-contrast CT now shows "a hypodense lesion in the right frontotemporal region with surrounding oedema and mild mass effect" (C8). |
| 83979d94-72e2-4266-b069-6cfedb60e3f0 | FIXED | `initial_tool_outputs.labs.panels.BMP`: sodium 140, chloride 103, bicarbonate 25 (anion gap 12), both now normal; CBC haemoglobin 13.8 with haematocrit 41.0 (MCHC 33.7, was 31.4); abnormal summary and interpretation rebuilt. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `followup_outputs[3]` | Follow-up tagged `perfusion_MRI` returned BOLD fMRI and DTI content (C6). Group B (aspiration first), so no functional imaging criterion. | FIXED: deleted. |
| A | major | `followup_outputs[4]`, `[5]` | Infectious-disease consult and dental evaluation filed as `interpret_labs` outputs, with management advice (C14). | FIXED: both deleted and turned into musts; blood cultures moved out of the lab panel into a new recommended `action-blood-cultures` (`order_microbiology`, `blood_culture`) with an authored follow-up (sterile at 5 days, drawn one week after the amoxicillin-clavulanate course). |
| C | major | tissue criterion `action-10-obtain-tissue-diagnosis` | Biopsy only, assays missing ATRX, TERT/EGFR/+7-10 listed as required. | FIXED (C3 group B, C4): stereotactic aspiration and biopsy with frozen section, Gram stain and culture first, then resection; assays IDH1_IHC, IDH1_IDH2_sequencing, ATRX_IHC, MGMT_methylation (age 48). |
| A/D | major | `initial_tool_outputs.tissue_diagnosis` | Tissue in the initial work-up; meta-text impression; Gram stain and culture listed as molecular findings; site "as targeted on the contrast-enhancing rim"; "WHO grade 4". | FIXED (C2): two follow-ups (biopsy with frozen section, resection), Gram stain and culture as finding rows, ATRX retained added, `molecular_findings` molecular only, integrated diagnosis "Glioblastoma, IDH-wildtype, CNS WHO grade 4", impression with MGMT. |
| A | major | literature criterion and fallback | Literature as a scored step. | FIXED (C1): deleted; `metadata.case_body_concerns` about it cleared. |
| D | minor | `initial_tool_outputs.mri.impression` | Dental speculation and teaching text ("diagnostic dilemma", "particularly given the clinical history of recent dental infection"). | FIXED: numbered findings and a two-item imaging differential. Mass effect reworded to a 4 mm leftward shift. |
| D | minor | `followup_outputs[0]`, `[1]` | Perfusion and MRS concluded the diagnosis ("consistent with high-grade neoplasm", "suggesting tumor infiltration"). | FIXED: metric-only impressions. |
| D | minor | `initial_tool_outputs.eeg.impression`, `limitations` | Teaching text and management advice ("Clinical correlation with imaging is essential", extended EEG recommended). | FIXED: findings only, including the right frontotemporal attenuation. |
| B | major | `patient.neurological_exam.additional` | Said the seizure happened "during the initial assessment", against the HPI (at home at breakfast). | FIXED: rewritten consistent with the HPI, staring spells kept. |
| B | minor | `social_history.occupation` | "accountant", against the lesson plan, his class and end-of-semester grading. | FIXED: secondary school teacher. |
| B | minor | `past_medical_history` | Diabetes "diet-controlled" while on metformin. | FIXED: "on metformin". |
| C | major | musts | Template musts (MRI and labs duplicating criteria, generic surgery), no treat-class seizure wording, no ibuprofen, no abscess handling. | FIXED: group B surgery must, ID review with timing of antibiotics around aspiration, dental review, canonical dexamethasone, levetiracetam as treatment (GTC plus staring spells) with no enzyme inducers, glucose monitoring on metformin, stop ibuprofen, C11 Stupp at age 48, KPS 80, MGMT unmethylated. Enzyme-inducer prohibition added. |
| C | major | criteria, constraints | No performance status; only a soft MRI constraint; no labs constraint. | FIXED: plan order, KPS 80/ECOG 1 follow-up, hard MRI and labs constraints before tissue. |
| C | major | `ground_truth.differential` | Two abscess entries (moderate and very_low) with contradictory DWI reasoning; others at the pre-tissue view. | FIXED: one abscess entry; all very_low at assessment time. |
| C | minor | drug check | Generic expected evidence; no output authored for the patient. | FIXED: follow-up for dexamethasone and levetiracetam against metformin, ibuprofen and lisinopril, sulfonamide allergy noted; leak guard passes. |
| C | minor | `avoided_actions` CSF, cardiac | Generic rationales. | FIXED: C17 (4 mm shift, subfalcine herniation); cardiac canonical. |
| D | minor | `fallback_tool_outputs.drug_interactions.general.proposed` | Engineering text "(agent not specified on this case's pathway)" served to the agent (C16). | FIXED: "Not specified". The same string is in 126 case files (CENTRAL). |
| B | minor | labs `type_and_screen` | Template clinical significance (C9). | FIXED: null. |

## Changes, in one paragraph a physician can read before re-reviewing

The emergency CT is now a hypodense lesion with oedema, the electrolytes and red-cell indices are physiological, the occupation is teacher and the exam note matches the HPI. The pathway is MRI, perfusion, spectroscopy, optional staging CT, blood cultures (sterile), labs, performance status (KPS 80), then stereotactic aspiration and biopsy with frozen section, Gram stain and culture, or resection, and an optional drug check. Both tissue reports show no organisms, sterile cultures and Glioblastoma, IDH-wildtype, CNS WHO grade 4 (IDH1 R132H negative, IDH1/IDH2 wildtype, ATRX retained, TERT mutant, EGFR amplified, +7/-10, MGMT unmethylated). The ID consult and dental evaluation are now musts rather than tools; the other musts are dexamethasone with glucose monitoring, levetiracetam as treatment for the seizure, stopping ibuprofen, and Stupp after the MDT. The red herring now argues from the printed MRI and labs.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `action-blood-cultures` has no citation: no brain abscess guideline key exists. Please add one (ESCMID guideline on brain abscess, Bodilsen et al., Clin Microbiol Infect 2024) and cite it here and in P03 and P04.
- `fallback_tool_outputs.drug_interactions.general.proposed` "(agent not specified on this case's pathway)" is engineering text in 126 case files; a generator-level fix is needed.
- Synonyms "astrocytoma grade 4" (plan section 5.2) and accepted[0] "WHO grade 4" to "CNS WHO grade 4" (plan section 5.3). Not hand-edited.
- `[AIOM_brain]` key (plan section 5.1).

## Open questions for Andrea (judgment calls you could not settle)

None.

## Verification

Adversarial check (24 Oct 2026). All three notes verified: the red herring now argues from the printed thin smooth ring, central restricted diffusion and WBC 11.2 (with normal procalcitonin, no fever, post-ictal timing) and lets the aspirate decide; the HPI CT shows a hypodense lesion with oedema, no enhancement; Na 140, Cl 103, HCO3 25 (gap 12) and MCHC 33.7 are physiological. Checked group B order (aspiration and biopsy first, then resection), one follow-up per procedure with identical integrated diagnosis, the ID and dental musts replacing the consult tools, the recommended blood cultures, the treat-class must, the sulfonamide allergy in the drug check, and the LP harm with the 4 mm shift. Found and fixed: (1) both `red_herrings[].field_path` were empty; set to `patient.clinical_history.past_medical_history[1]` (dental abscess) and `patient.clinical_history.family_history[1]` (maternal MS); (2) the blood-culture output listed `gram_stain` in `tests` with `gram_stain: null` (no Gram stain is reported on sterile bottles); `tests` is now `["culture"]`; (3) the tissue rationale attributed "frozen section, Gram stain and culture separate abscess from necrotic tumour" to EANO 2021, which does not address brain abscess; the attribution now sits only on the integrated-diagnosis sentence (the abscess guideline key is already requested under CENTRAL). perfect_agent, case_io check and the case guards are clean after the edits.

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- antibiotic-timing text: ESCMID 2024 qualifier (within about 24 hours) added (Q10: the withholding rule is conditional on neurosurgery within about 24 hours, ESCMID 2024)
- fallback specialized_test (generic 'Study within normal limits.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Central vocabulary wired (24 Oct 2026)

Terms added by commit e19131d6 (batch-2 review vocabulary), wired as the plan and this log intended. The earlier CENTRAL vocabulary request in this log is resolved by them.

- New required criterion `action-aspirate-microbiology` (`order_microbiology` `{"specimen": "brain_aspirate"}`), after the tissue criterion, with a soft constraint tissue before it (the aspirate comes from the procedure) and added to the stop rule. Reason: the abscess is a live differential of this ring-enhancing mass until the aspirate is examined; Gram stain and culture of the aspirate are its microbiological test (ESCMID 2024, `[ESCMID_BA_2024]`, aspiration with microbiology strong). Blood cultures stay recommended (decision Q6).
- New follow-up `request_brain_aspirate_gram_stain_culture` (specimen `brain_aspirate`, after the tissue follow-ups): no organisms, no neutrophils; no growth on aerobic or anaerobic culture at 5 days; collected before empirical antimicrobials (the 14-day amoxicillin-clavulanate course ended one week earlier, as in the blood-culture report). The Gram stain and culture rows were removed from both tissue reports (the tissue tool returns histology and molecular assays; the frozen section stays), and the tissue expected evidence no longer cites them; the tissue label now says the aspirate goes to microbiology.
- Fungal culture dropped from the aspirate (immunocompetent host; not part of the `brain_aspirate` term) and from the surgery must ("Gram stain and aerobic and anaerobic culture"). `metadata.difficulty_rationale` updated to the 5 required criteria.

Checks after the change: `perfect_agent.py GLIO-HG-P01 -v` ok, `case_io.py check` (schema and synonym guard OK, no failure names the case), `test_case_guards.py -k "GLIO-HG- or ALZ-EARLY-"` 120 passed.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-2-interpret-labs]`.alternatives: was [CBC, BMP, coagulation, type_and_screen]; now [CBC, BMP, coagulation, type_and_screen, CRP, ESR, procalcitonin, HbA1c] | [CBC, BMP, coagulation, type_and_screen].
- Decision: serve: new first alternative (old order kept as an alternative). Recent dental abscess with an abscess differential: CRP and procalcitonin weigh it (as in GLIO-HG-P04, where they are in the order); HbA1c frames dexamethasone in his type 2 diabetes.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.

## Library contradictions (25 Oct 2026)

Case-specific reports stored where the benchmark library's normal report contradicted the case. Why: the stored MRI shows a mass in the right frontal operculum and superior temporal gyrus, extending into the insula (3.8 cm) with an abnormal routine EEG and a focal history and exam; the library reports a normal head CT, a non-diagnostic biopsy, normal brain metabolism, perfusion and vessels, a normal prolonged EEG, no headache and normal bedside and neurophysiological tests where the exam is abnormal.

- order_ct_scan: CT showing the stored lesion(s) instead of a normal head CT (fallback_tool_outputs.ct)
- obtain_tissue_diagnosis open_biopsy: the stored integrated diagnosis on this procedure's specimen (fallback_tool_outputs.tissue_diagnosis)
- FDG_PET: hypermetabolic lesion(s) (fallback_tool_outputs.advanced_imaging)
- amino_acid_PET: FET-avid lesion(s) (followup request_amino_acid_pet)
- CT_perfusion: lesion perfusion matching the stored perfusion MRI (followup request_ct_perfusion)
- perfusion_SPECT: regional hypoperfusion over the lesion (followup request_perfusion_spect)
- cerebral_angiography: mass effect and lesion vascularity (followup request_cerebral_angiography)
- DTI_tractography: tracts displaced or infiltrated by the lesion (followup request_dti_tractography_tracts)
- video EEG: the stored routine EEG's abnormalities over 24 h (fallback_tool_outputs.eeg)
- ambulatory EEG: the stored routine EEG's abnormalities over 48 h (followup request_ambulatory_eeg)
- structured_headache_history_ichd3: the case's headache, prior primary headache and red flags (fallback_tool_outputs.clinical_assessment)
- cognitive_screen: MoCA matching the exam (followup request_cognitive_screen)
- neuropsych_battery: domain deficits matching the exam (fallback_tool_outputs.specialized_test)

Checks: `perfect_agent.py` pass; `test_case_guards.py -k GLIO-HG-P01` pass; no fixed order still answered by the library (`lib4.source`); no 60-character window of any criterion's expected_evidence in the added text, except tissue copies that repeat the stored tissue report verbatim; every criterion's served output unchanged (snapshot diff against the baseline).
