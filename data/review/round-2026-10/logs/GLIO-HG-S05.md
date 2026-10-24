# GLIO-HG-S05
Reviewer status: R1 not reviewed, R2 not reviewed (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | The notes file has no note for GLIO-HG-S05. The condition classes of the plan were applied (below). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| E | blocker | `initial_tool_outputs.tissue_diagnosis` (findings, molecular_findings, impression) | Engineering text in the clinical report: "IDH-wildtype, as stated in this case's diagnosis", "This case does not record the value", "This case does not state which molecular markers were positive"; MGMT never reported (plan C16). | FIXED: real results in report voice: IDH1 R132H IHC negative, IDH1/2 sequencing wildtype, ATRX retained, MGMT methylated, TERT C250T, EGFR not amplified, +7/-10 present, 1p/19q intact; one `Histology` row; impression "Integrated diagnosis: Glioblastoma, IDH-wildtype, CNS WHO grade 4. MGMT promoter methylated." |
| D | major | `initial_tool_outputs.tissue_diagnosis` | Tissue served upfront (plan C2). | FIXED: initial null; resection and stereotactic-biopsy follow-ups with identical diagnosis. |
| C | major | `action-10-obtain-tissue-diagnosis` | Biopsy only; assay list without IDH IHC or ATRX (plan C3, C4; age 60). | FIXED: `resection` then `stereotactic_biopsy`, each `IDH1_IHC`, `ATRX_IHC`, `MGMT_methylation`; canonical label and rationale. |
| C | major | `action-3-search-medical-literature`, literature follow-up, `fallback_tool_outputs.literature_search` | Required literature step whose output repeated the criterion's expected evidence (condition-wide guard failure) (ruling 5, plan C1). | FIXED: criterion, follow-up, stop-rule entry and fallback removed; the leak guard now passes for S05. |
| C | major | `ground_truth.action_criteria`, follow-ups | No functional imaging although the tumour compresses the trigone (optic radiation, right inferior quadrantanopia) and its edema reaches the dominant parietal white matter and the posterior limb (plan C6, "apply the rule"). | FIXED: by the rule, DTI only: the superior parietal lobule and precuneus are not primary motor or language cortex, so fMRI does not apply, but the optic radiation, arcuate fasciculus and corticospinal tract are at risk. New `DTI_tractography` output (optic radiation 4 mm from the inferior margin, arcuate and SLF 7 mm, CST 12 mm) and recommended `action-dti-tractography`, soft constraint to tissue; surgery must names DTI and subcortical mapping. |
| C | major | `ground_truth.action_criteria` | No performance status (plan C7). | FIXED: recommended; KPS 80, ECOG 1 (still working with effort). |
| C | major | `required_recommendations`, `prohibited_recommendations` | No-seizure case without the prophylaxis prohibition (plan C5); test and consult musts; no treatment must (plan C11). | FIXED: canonical no-prophylaxis prohibition; MRI, labs and generic consult musts replaced by the canonical group A surgery must (with DTI), canonical dexamethasone and the entity-specific Stupp must (age 60, KPS 80). |
| B | major | `patient.clinical_history.medications` (aspirin), musts | Aspirin listed for "cardiovascular risk reduction" while the HPI says it was given two days earlier for presumed TIA; no must stops it before craniotomy. | FIXED: indication "Started two days before admission by primary care for presumed TIA"; must to stop it; DDI warning on the platelet effect. |
| C | major | `ground_truth.differential` | Metastasis "moderate" after negative staging and glial tissue; the infarct that the TIA red herring raises absent; "Lower-grade glioma (WHO grade 2 or 3)" (ruling 7, plan C12). | FIXED: all very_low with the excluding results; "Subacute ischemic infarct (the provisional TIA diagnosis)" added; lower-grade entry replaced by "Astrocytoma, IDH-mutant", excluded by IDH and ATRX. |
| D | minor | `initial_tool_outputs.mri.impression` | "tissue diagnosis recommended" (plan C9); posterior limb and trigone involvement not in the impression. | FIXED: numbered imaging-only impression. |
| D | minor | MRS and perfusion follow-ups | MRS impression "Perilesional spectral changes are present" without values; em dash in a region; descriptions carried interpretation. | FIXED: numbered impressions with values (perilesional Cho/NAA 1.6 from 1.9/1.2); em dash removed. |
| D | minor | `initial_tool_outputs.labs.interpretation` | "Coagulation profile acceptable for surgical planning" in a routine panel interpretation (style guide). | FIXED: pattern-level interpretation. |
| C | minor | criteria 1, 2, 6, 7, 8, 9, avoided actions | Rationale copied the label; `[Stupp_2005]` on MRI; em dashes in expected evidence; uncited EEG and ECG waste entries. | FIXED: rationales and expected evidence from this case; one bracketed key; EEG waste canonical rationale `[EANO_2021]`; ECG waste kept (plan) with `[EANO_2021]`; cardiac waste canonical; CSF canonical harm. |
| E | minor | prohibitions, key evidence, red herring | Em dashes; TIA prohibition worded "mandates". | FIXED: rewritten without dashes; red herring kept (it is the case's designed trap) with a cleaner interpretation. |
| B | minor | `sequence_constraints`, `stop_rule`, `metadata` | Single soft constraint; literature in stop rule; `difficulty_rationale` named consults as tools and a "right parietal" mass. | FIXED: hard MRI and labs to tissue, soft DTI to tissue; stop rule MRI, labs, tissue; rationale corrected (left parietal, 3 required tools). |

## Changes, in one paragraph a physician can read before re-reviewing
The tissue report no longer contains engineering sentences: it gives Glioblastoma, IDH-wildtype, CNS WHO grade 4 with IDH1 R132H negative, IDH sequencing wildtype, ATRX retained, MGMT methylated, TERT mutated and +7/-10, and is served only after a resection or stereotactic biopsy order. Literature is gone. The pathway reads contrast MRI, perfusion, spectroscopy, optional CT staging, labs, performance status (KPS 80, ECOG 1), DTI tractography (the tumour presses on the optic radiation at the trigone and approaches the dominant arcuate fasciculus; fMRI is not added because no primary motor or language cortex is involved), then tissue. He has had no seizure, so antiseizure prophylaxis is prohibited. The aspirin started for the presumed TIA is stopped before surgery; dexamethasone at the lowest effective dose; after the integrated diagnosis, 60 Gy in 30 fractions with temozolomide. The provisional TIA stays as the red herring, and a subacute infarct now sits in the differential, excluded by the MRI.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- `[AIOM_brain]` citation key needs the pack allow-list (plan 5.1).
- Synonym "astrocytoma grade 4" is wrong for this IDH-wildtype GBM (plan 5.2).
- `accepted[0]` "Glioblastoma, IDH-wildtype, WHO grade 4 (left parietal)" uses "WHO grade" (plan 5.3); unchanged per ruling 3.

## Open questions for Andrea (judgment calls you could not settle)
- None. The fMRI decision follows the plan's rule (no primary motor or language cortex within about 1 cm on the MRI); if a reviewer prefers language fMRI for any dominant parietal resection, it can be added as a second recommended criterion.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the git diff and the whole final case.
- No reviewer notes. Checked: tissue reports now in report voice with every C4 assay (IDH1 IHC, ATRX, MGMT) in both procedures; DTI-only decision (superior parietal lobule and precuneus, no primary motor or language cortex within about 1 cm; inferior quadrantanopia matches superior optic radiation fibres on DTI); no-seizure prohibition and no levetiracetam anywhere; aspirin indication and stop must agree with the HPI timeline; KPS 80 / ECOG 1; differential at the assessment-time view with the infarct the TIA herring raises; labs (gap 11, MCHC 33.3, CRP 3.1 within 0-5).
- Found and fixed:
  - (C, minor) `ground_truth.avoided_actions` `avoid-waste-4-analyze-ecg` penalised a pre-operative ECG in a 60-year-old with hypertension, type 2 diabetes, hyperlipidaemia and prior smoking who is listed for craniotomy. ESC 2022 guidelines on non-cardiac surgery (Halvorsen S et al. Eur Heart J 2022;43:3826-3924) recommend a pre-operative 12-lead ECG in patients with cardiovascular risk factors before intermediate- or high-risk surgery (class I), and craniotomy is at least intermediate risk. The entry is removed; ordering an ECG is now neutral (the case fallback answers it). This departs from the plan line "The ECG waste entry stays": flag for the lead.
  - (D, minor) `fallback_tool_outputs.ecg.findings` "consistent with long-standing hypertension" is a clinical attribution outside the modality (style guide; the worker removed the same clause from S01). Now "Left ventricular hypertrophy by voltage criteria".
- perfect_agent.py and case_io.py check clean after the edits.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `fallback_tool_outputs.eeg`: the normal "no focal slowing" study replaced by focal polymorphic slowing over the lesion (continuous delta at P3, C3, Pz), no epileptiform discharges, in the RS06 format; a normal EEG contradicts a hemispheric mass with oedema (same class as M04, RS05, RS06).
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4 (left parietal)' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4 (left parietal)' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic '', test_type 'neuropsych_battery') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).
