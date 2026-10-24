# GLIO-HG-M02
Reviewer status: R1 not reviewed, R2 needs_changes (2 notes) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 695c1dcf-5246-4112-ba35-cde96c72512a | FIXED | Tissue criterion `action-9-obtain-tissue-diagnosis` now requires `IDH1_IHC`, `IDH1_IDH2_sequencing` (age 47, under 55), `ATRX_IHC`, `MGMT_methylation` in both alternatives (`resection`, `stereotactic_biopsy`); 1p/19q, TERT and EGFR are no longer required (the report still gives them). The tissue report gains separate IDH1 R132H IHC, IDH1/IDH2 sequencing and ATRX IHC rows (ATRX retained), one findings row and one `molecular_findings` entry per assay. |
| 152c009f-c9ca-464b-91e9-01758c896f94 | FIXED | The temozolomide check (penicillin-but-not-sulfa sentence, pregnancy test for a "52, perimenopausal" patient) is replaced by a dexamethasone/levetiracetam check against his own medicines, stating NKDA (`followup_outputs[8]`). `action-1` expected evidence is rewritten from his MRI: thick nodular enhancement and no central necrosis; `key_clinical_evidence[1]` likewise. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.neurological_exam.motor`, `.coordination`, `patient.history_present_illness` | Left deltoid and left ankle weakness and slowed left RAM, "subtle left-sided motor findings", with a left temporal lesion and a right-hand seizure: ipsilateral deficits no lesion explains. | FIXED: subtle right pronator drift with 5/5 strength, RAM mildly slowed on the right; HPI "subtle right-sided motor signs". The left-leg deficit was removed rather than moved, since a temporal lesion does not explain leg weakness. |
| D | major | `patient.history_present_illness` | "ordered an urgent MRI ... The MRI revealed a left temporal lobe lesion" (C8). | FIXED: urgent non-contrast CT showing a left temporal hypodensity with oedema. |
| B | major | `initial_tool_outputs.labs.panels.CBC` | Female reference ranges (Hb 12-16, Hct 36-46) in a man, which left Hb 13.4/Hct 38 unflagged though below male limits; MCV 79 flagged with no other microcytic index and nothing in the case using it. | FIXED: male ranges (13.5-17.5, 41-53), Hb 14.2, Hct 42.0 (MCHC 33.8), MCV 86; summary and interpretation recomputed. Sodium 134, glucose 105 and ESR 22 kept. |
| B | minor | labs type_and_screen `clinical_significance` | Template text (C9). | FIXED: null. |
| B | minor | `initial_tool_outputs.mri.findings[0].mass_effect` | "2 mm leftward falx deviation" for a left-sided mass. | FIXED: 2 mm rightward shift; volumetrics `midline_shift` added. |
| D | minor | `initial_tool_outputs.mri` DWI and impression | DWI compared with abscess; impression an essay naming glioblastoma and the retired "anaplastic astrocytoma (WHO grade 3)". | FIXED: DWI reports the ADC; numbered impression with "most consistent with a high-grade glial neoplasm", no necrosis stated, tissue recommended. |
| E | minor | `initial_tool_outputs.eeg.impression` | Not in ACNS form. | FIXED: numbered (temporal polymorphic delta, lateralized rhythmic delta in drowsiness), no epileptiform discharges. |
| C | major | `assessment.required_recommendations` | Documented right-hand focal clonic seizure with no antiseizure must (C5). | FIXED: treat-class levetiracetam must; prohibition of enzyme inducers. |
| A/D | major | `initial_tool_outputs.tissue_diagnosis` | Tissue served initially; meta-text; histology "Diffuse astrocytoma, WHO grade 4" (retired term); site "as targeted on the contrast-enhancing rim"; histology items listed as molecular findings. | FIXED (C2): two follow-ups (resection, stereotactic biopsy), site left temporal lobe, histology in `histological_diagnosis` and one Histology row, integrated diagnosis "Glioblastoma, IDH-wildtype, CNS WHO grade 4". |
| B | major | `followup_outputs[3]` (old) | fMRI tagged `perfusion_MRI` and carrying a DTI sentence (C6). | FIXED: `functional_MRI` follow-up (the 8 mm Wernicke distance moved into its finding) and a new `DTI_tractography` follow-up (arcuate, Meyer loop, CST); recommended criteria with soft constraints before tissue. |
| A | major | literature criterion, follow-up and fallback | Literature as a required step; output echoed expected evidence (guard failure). | FIXED (C1): all removed. |
| C | major | `action_criteria`, constraints, stop rule | No performance status, single soft constraint, template labels = rationales, duplicate citation keys. | FIXED: plan 3.1 order and tiers, KPS 80/ECOG 1 follow-up, hard MRI and labs constraints, soft fMRI/DTI constraints, canonical labels. New optional `action-drug-interactions` (the case had none). |
| C | major | musts | Interchangeable biopsy/resection, MRI and labs musts, template Stupp. | FIXED: C3 surgery must, C11 dexamethasone, seizure treatment, stop ibuprofen (with sertraline), MDT with 60 Gy/30 and temozolomide, noting the smaller benefit with unmethylated MGMT and trial options. MRI/labs musts removed (scored criteria). |
| C | major | `ground_truth.differential` | Retired "Anaplastic astrocytoma" at moderate; lymphoma/demyelination features from another MRI; pre-tissue likelihoods. | FIXED: assessment-time view, all very_low; worsening depression added (the red herring raises it). |
| C | minor | `avoided_actions` | Generic CSF and cardiac rationales. | FIXED: C17 rationale (2 mm shift, temporal horn effacement); "No cardiac question in this presentation". |
| B | minor | `red_herrings[0].field_path`, `metadata.difficulty_rationale` | Empty field path; "5 required tools". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The patient now has right-sided soft signs (pronator drift, slowed right RAM) to match the left temporal mass and the right-hand seizure; the HPI cites an outside non-contrast CT, not the MRI. The CBC uses male ranges with normal values. The MRI reports a rightward 2 mm shift, thick nodular enhancement without necrosis, and an imaging-only impression. The pathway is MRI, perfusion, spectroscopy, optional CT staging, labs, performance status (KPS 80), fMRI (Wernicke displaced, 8 mm), DTI (arcuate deviated, 5 mm; Meyer loop in oedema), tissue by resection or biopsy (Glioblastoma, IDH-wildtype, CNS WHO grade 4, IDH-wildtype by IHC and sequencing, ATRX retained, TERT mutant, EGFR amplified, MGMT unmethylated), and an optional drug check (ibuprofen with dexamethasone and sertraline; levetiracetam and mood; NKDA). Musts: resection with fMRI, DTI and mapping; dexamethasone; levetiracetam for the documented seizure, no enzyme inducers; stop ibuprofen; MDT, 60 Gy/30 with temozolomide, trials discussed given unmethylated MGMT. Literature is gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- accepted[0] "Glioblastoma, IDH-wildtype, WHO grade 4 (high-grade glioma)": the suffix is not a site; change to "(left temporal lobe)" (plan section 5.3). Not edited here (ruling 3).
- Synonym "astrocytoma grade 4" is wrong for an IDH-wildtype glioblastoma (plan section 5.2).
- `[AIOM_brain]` key (plan section 5.1).

## Open questions for Andrea (judgment calls you could not settle)

None.

## Verification

Adversarial check (24 Oct 2026). Both notes fixed: the tissue criterion requires IDH1_IHC, IDH1_IDH2_sequencing, ATRX_IHC and MGMT_methylation in both alternatives and each has a findings row and a `molecular_findings` entry (ATRX retained, consistent with IDH-wildtype); the drug check states NKDA with no penicillin, sulfonamide or pregnancy text; action-1 expected evidence and key evidence say no central necrosis, matching the MRI. Checked the patient-block edit (right pronator drift and slowed right RAM in place of ipsilateral left deficits): consistent with the left temporal mass, the right-hand seizure, the HPI and the DTI (corticospinal tract 1.2 cm from the FLAIR margin). Male CBC ranges, MCHC 33.8, anion gap 12, rightward shift, treat-class levetiracetam must plus the enzyme-inducer prohibition, unmethylated MGMT with trial discussion, no literature, guards pass. KPS 80 while on leave from work is borderline with KPS 70; either value keeps the standard 60 Gy/30 regimen, so it was left. No change made; perfect_agent and case_io check clean.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `initial_tool_outputs.mri.impression`: trailing sentence "Tissue diagnosis recommended." removed, for uniformity with the other 25 GLIO-HG MRI impressions (imaging-only, plan C9); the style guide allows it, so this is consistency, not an error fix.
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4 (high-grade glioma)' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4 (left temporal lobe)' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic 'Study within normal limits.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
