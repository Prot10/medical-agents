# GLIO-HG-M03
Reviewer status: R1 not reviewed, R2 needs_changes (5 notes) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 6defe1f8-aa47-4d01-b17f-ccbdfedca922 | FIXED | Allergy specified as "Iodinated contrast medium (urticaria after a contrast-enhanced CT)" (`patient.clinical_history.allergies[0]`); nothing in the history contradicts it. New must `required_recommendations[1]` (plan text): iodinated reaction is not a contraindication to gadolinium; contrast CT needs corticosteroid and antihistamine premedication or an alternative [ACR_contrast]. The optional CT CAP criterion label adds the premedication. The drug check (`followup_outputs[8].warnings`) names the allergy and states it does not affect dexamethasone. |
| 881deadb-46f0-436c-acac-94b0a2aaf0f7 | FIXED | Na 129 kept and flagged with a clinical significance (volume status, serum and urine osmolality, urine sodium before dexamethasone and surgery); chloride 95 (low, flagged), bicarbonate 24, anion gap 10. New hyponatraemia work-up must `required_recommendations[2]` with a correction limit of 8 to 10 mmol/L in 24 h. Labs expected evidence states the sodium; summary and interpretation recomputed. |
| f535a55b-8065-440c-b0e2-125383ef3b05 | FIXED | No-seizure class: the levetiracetam must is deleted; prohibition `prohibited_recommendations[1]` against prophylaxis (AIOM); the drug check proposes dexamethasone only. The teaching-pearl clause is ALREADY-FIXED (pearls no longer in the case); the same claim in `key_clinical_evidence` ("New-onset ... seizure mandates AED therapy") is replaced by "She has had no seizure, so antiseizure prophylaxis is not indicated (AIOM)". |
| 0bcfaf79-aec2-4de0-9410-62dff4e52ebc | FIXED | One occupation, IT project manager (social history kept): HPI "during her lectures", "As an English teacher known for ... literary references" and "grading papers" rewritten as work meetings, client presentations and project documents. The penicillin text in the drug check is deleted (the output is rewritten). |
| aed4aacd-f3de-4be3-ad53-cb002e4423ad | FIXED (assays) / ALREADY-FIXED (empty tool fields) | Tissue criterion `action-10` requires IDH1_IHC, IDH1_IDH2_sequencing (age 54), ATRX_IHC, MGMT_methylation in both alternatives; the report gains IDH1 R132H IHC, IDH1/IDH2 sequencing and ATRX IHC rows (ATRX retained). Required actions 4 and 5 with an empty tool field were v1 consult steps removed by the v2 migration; the referrals they stood for are musts (neurosurgery `required_recommendations[0]`, neuro-oncology MDT `[5]`). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | "he ordered a brain MRI which revealed a left temporal lesion" (C8). | FIXED: non-contrast CT with left temporal hypodensity, oedema, slight shift. |
| B | minor | `initial_tool_outputs.labs.panels.CBC` Hematocrit | Hct 39.6 with Hb 14.5 (MCHC 36.6), RBC 4.97 and MCV 90.1 (derived 44.8). | FIXED: Hct 44.8 (MCHC 32.4). |
| B | minor | labs type_and_screen significance | Template text. | FIXED: null. |
| B | minor | `initial_tool_outputs.mri.findings[0].mass_effect` | "2 mm leftward falx deviation" for a left-sided mass. | FIXED: rightward. |
| D | minor | `initial_tool_outputs.mri.additional_observations[4]`, `.impression` | "correlating with potential visual field deficit" (cross-modality); impression an essay with "anaplastic astrocytoma (WHO grade 3)". | FIXED: anatomic statement (Meyer loop course); numbered imaging-only impression. |
| E | minor | `initial_tool_outputs.eeg` impression, background | Not ACNS form; dash. | FIXED. |
| D | minor | `followup_outputs[0]`, `[1]` perfusion, MRS | Threshold teaching text; "despite absence of classic ring" commentary; MRS impression "See findings above". | FIXED: plain metrics, numbered impressions, peritumoral perfusion finding row added to match the impression. |
| D | minor | `followup_outputs[2]` CT CAP | Thyroid nodule text with management advice ("no urgent workup required in this oncological context"), duplicated row. | FIXED: one descriptive row (6 mm, smooth margins). |
| B | major | old `followup_outputs[3]` | fMRI tagged perfusion_MRI with a DTI sentence (C6). | FIXED: functional_MRI follow-up and new DTI_tractography follow-up (arcuate, Meyer loop, CST), both recommended criteria with soft constraints. |
| A/D | major | `initial_tool_outputs.tissue_diagnosis` | Tissue in the initial work-up, meta-text, histology items in molecular findings, "WHO grade 4". | FIXED (C2): two follow-ups (resection, biopsy), Histology row, "CNS WHO grade 4". |
| A | major | literature criterion, follow-up and fallback | Literature as a required step; leak-guard failure. | FIXED (C1): removed. |
| C | major | criteria, constraints, stop rule | No performance status; single soft constraint; template labels. | FIXED: plan 3.1, KPS 80/ECOG 1, hard MRI and labs constraints, soft fMRI/DTI. |
| C | major | musts | Interchangeable procedures, MRI and labs musts, Stupp template, ibuprofen not addressed. | FIXED: C3 surgery must, contrast must, hyponatraemia must, C11 dexamethasone, stop ibuprofen, MDT with 60 Gy/30 and temozolomide (unmethylated MGMT: trials discussed). |
| C | minor | drug check | Bevacizumab offered as an alternative before any tissue diagnosis; atorvastatin and sumatriptan unaddressed. | FIXED: alternative methylprednisolone only; atorvastatin (CYP3A4 induction) and sumatriptan lines added. |
| C | major | differential | Retired "anaplastic astrocytoma" at moderate; pre-tissue likelihoods; demyelination features from another MRI. | FIXED: assessment-time view (all very_low); migraine/stress-related complaints added since the red herring raises it. |
| C | minor | `avoided_actions` | Generic rationales. | FIXED: C17 rationale (2 mm shift, ambient cistern compression); cardiac waste rationale. |
| B | minor | `red_herrings[0]` | Empty field path. | FIXED: `past_medical_history[2]`, interpretation from her headache description. |

## Changes, in one paragraph a physician can read before re-reviewing

She is an IT project manager throughout; her allergy is now urticaria to iodinated contrast, addressed by a must (gadolinium not contraindicated; premedicate or avoid contrast CT). The HPI cites a non-contrast CT, not the MRI. Electrolytes are now possible (Na 129, Cl 95, HCO3 24, gap 10), with a hyponatraemia work-up must and a safe correction limit. Pathway: MRI (solid enhancement without necrosis, ambient cistern compression, 2 mm rightward shift), perfusion, MRS, optional CT CAP, labs, performance status (KPS 80), fMRI (Wernicke 0.8 cm), DTI (arcuate 5 mm, Meyer loop 3 mm), tissue by resection or biopsy (Glioblastoma, IDH-wildtype, CNS WHO grade 4: IDH-wildtype by IHC and sequencing, ATRX retained, TERT mutant, EGFR amplified, MGMT unmethylated), optional dexamethasone check last. No levetiracetam (no seizure; prophylaxis prohibited). Musts: resection with fMRI, DTI and mapping; contrast precautions; hyponatraemia work-up; dexamethasone; stop ibuprofen; MDT, 60 Gy/30 with temozolomide and trial discussion. Literature is gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[ACR_contrast]` and `[AIOM_brain]` (plan section 5.1).
- Synonym "astrocytoma grade 4" wrong for IDH-wildtype glioblastoma (plan section 5.2).

## Open questions for Andrea (judgment calls you could not settle)

None. The allergy was specified as iodinated contrast with urticaria (the plan's option); nothing in the case contradicted it.

## Verification

Adversarial check (24 Oct 2026). All five notes verified in the file: the allergy is specified (urticaria to iodinated contrast) and addressed by the plan's contrast must, the CT CAP label and the drug-check warning, and the ACR statement (an iodinated reaction is not a contraindication to gadolinium) is correct; Na 129 is flagged with a clinical significance, Cl 95 and HCO3 24 give a gap of 10, and the hyponatraemia must gives a safe correction limit; no levetiracetam anywhere (prohibition of prophylaxis, drug check proposes dexamethasone only, key evidence restated); one occupation (IT project manager) in HPI and social history, no penicillin text; the four assays are in both alternatives and in both reports, and the referrals of the old empty-tool steps are musts. Hct 44.8 with Hb 14.5 (MCHC 32.4) agrees with RBC x MCV. Found and fixed one pre-existing fallback error: `fallback_tool_outputs.ecg` gave rate 59 as "normal sinus rhythm" (that is sinus bradycardia); rate set to 62. "Tissue diagnosis recommended" kept in the MRI impression (allowed by the style guide). perfect_agent and case_io check clean after the edit.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `initial_tool_outputs.mri.impression`: trailing sentence "Tissue diagnosis recommended." removed, for uniformity with the other 25 GLIO-HG MRI impressions (imaging-only, plan C9); the style guide allows it, so this is consistency, not an error fix.
- `metadata.difficulty_description`: "to confirm high-grade etiology and differentiate from other enhancing lesions" now "that support a high-grade neoplasm and target sampling; tissue establishes the diagnosis" (imaging does not confirm the entity).
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4 (left temporal lobe)' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4 (left temporal lobe)' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic 'Minor non-specific finding.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
