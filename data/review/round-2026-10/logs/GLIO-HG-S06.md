# GLIO-HG-S06
Reviewer status: R1 not reviewed, R2 not reviewed (no notes for this case) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | The notes file has no note for GLIO-HG-S06. The condition classes of the plan were applied (below). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | "An urgent outpatient MRI revealed a left occipital mass with surrounding edema": the HPI gives the result of the MRI the agent must order (plan C8). | FIXED: an outside non-contrast CT showing a left occipital mass with surrounding hypodensity and about 5 mm rightward shift (the MRI value); no enhancement, necrosis or tumour type named. |
| C | major | must 5, `followup_outputs` drug check | "Prophylactic levetiracetam may be initiated given seizure risk" in a patient with no seizure, against AIOM (plan C5, no-seizure class); levetiracetam in the drug check `proposed`. | FIXED: must deleted; canonical no-prophylaxis prohibition added; drug check now dexamethasone only (calcium, cholecalciferol, amlodipine and valsartan interactions), trigger `check_dexamethasone_interactions`; criterion label and expected evidence updated; optional, last; guard passes. |
| C | major | `action-3-search-medical-literature`, literature follow-up, `fallback_tool_outputs.literature_search` | Required literature step in the stop rule (ruling 5, plan C1). | FIXED: criterion, follow-up, stop-rule entry and fallback removed. |
| D | major | `initial_tool_outputs.tissue_diagnosis` | Tissue served upfront; template impression; site inside the integrated diagnosis (plan C2). | FIXED: initial null; resection and stereotactic-biopsy follow-ups with identical diagnosis "Glioblastoma, IDH-wildtype, CNS WHO grade 4"; `Histology` row; impression with MGMT unmethylated. |
| C | major | `action-10-obtain-tissue-diagnosis` | Biopsy only; assay list without IDH or ATRX and with 1p/19q (plan C3, C4; age 67). | FIXED: `resection` then `stereotactic_biopsy`, each `IDH1_IHC`, `ATRX_IHC`, `MGMT_methylation`; separate IDH1 R132H IHC, sequencing and ATRX rows in both reports. |
| C | major | `ground_truth.action_criteria`, follow-ups | No tractography although the edema involves the left optic radiation (plan C6: DTI only). | FIXED: MRI confirms optic-radiation involvement with no motor or language cortex within about 1 cm, so DTI only. New `DTI_tractography` output (optic radiation continuous to the anterior enhancing margin with markedly reduced FA in its edematous segment; ILF 5 mm; reduced FA in the forceps major) and recommended `action-dti-tractography`, soft constraint to tissue; surgery must names DTI. |
| C | major | `ground_truth.action_criteria`, `stop_rule` | No performance status at 67 (plan C7). | FIXED: required and in the stop rule; KPS 80, ECOG 1. |
| C | major | `required_recommendations` | Test musts (MRI, labs), a localisation statement filed as a must, no treatment must, generic surgery and loading-dose musts (ruling 4, plan C3, C11). | FIXED: canonical group A surgery must with DTI; canonical dexamethasone; must not to drive with a dense homonymous hemianopia; entity-specific treatment must (67, KPS 80: 60 Gy in 30 fractions with temozolomide). The localisation reasoning stays in key evidence and in the cataract prohibition. |
| D | major | `initial_tool_outputs.mri` | "FLAIR signal involves the left optic radiation, consistent with the patient's right homonymous hemianopia" (observation and impression item 2) and "tissue diagnosis recommended" (plan C9). | FIXED: clinical clauses deleted; numbered imaging-only impression including the early obstructive dilatation of the occipital horn. |
| D | minor | perfusion follow-up | Grading sentence against the 1.75 threshold; "above the low-grade threshold" with an em dash in the peritumoral row (plan C12). | FIXED: numbered impression "consistent with a high-grade neoplasm"; row states the value only. |
| D | minor | `initial_tool_outputs.labs.interpretation` | "No coagulopathy. Pre-operative parameters acceptable." in a routine panel interpretation. | FIXED: "All values within reference ranges."; action-2 expected evidence states the actual result. |
| B | minor | `fallback_tool_outputs.csf` | Opening pressure 16 cm H2O with bilateral papilledema. | FIXED: 25 cm H2O. |
| C | minor | `ground_truth.differential` | Metastasis, lymphoma and PCA infarct left low after negative staging and glial tissue; "Lower-grade glioma (IDH-mutant, WHO grade 2-3)" (ruling 7, plan C12). | FIXED: all very_low with the excluding results; lower-grade entry replaced by "Astrocytoma, IDH-mutant", excluded by IDH and ATRX. |
| E | minor | key evidence, prohibitions, red herring, HPI, cranial nerves | Engineering wording ("analyze_csf is a harmful tool for this case"), em dashes, "mandates". | FIXED: rewritten in clinical voice without dashes; red herring (cataract misattribution) kept with the same meaning. |
| C | minor | criteria 1, 2, 6, 7, 8, 9; constraints; avoided actions | `[Stupp_2005]` on the MRI, template rationales and expected evidence, "guides biopsy needle trajectory", single soft constraint (plan 1.1, 3.3). | FIXED: rationales and expected evidence from this case; one bracketed key; hard MRI and labs to tissue, soft DTI to tissue; cardiac waste canonical; EEG waste canonical `[EANO_2021]`; CSF harm canonical with shift, trapped horn and papilledema. |
| B | minor | `metadata.difficulty_rationale` | "5 required tools". | FIXED: 4 required actions. |

## Changes, in one paragraph a physician can read before re-reviewing
The HPI no longer reveals the MRI: the outside study is now a non-contrast CT showing a left occipital mass with edema and 5 mm shift. Literature is gone, and the prophylactic levetiracetam must is replaced by a prohibition, since she has had no seizure (AIOM). The pathway reads contrast MRI, perfusion, spectroscopy, optional CT staging, labs, a required performance status (KPS 80, ECOG 1), DTI of the left optic radiation, then resection or stereotactic biopsy with IDH1 IHC, ATRX and MGMT, giving Glioblastoma, IDH-wildtype, CNS WHO grade 4, MGMT unmethylated; after it, 60 Gy in 30 fractions with temozolomide. A must advises against driving with the dense hemianopia. The MRI impression reports imaging only, and the LP harm cites the shift, the trapped occipital horn and the papilledema. The cataract red herring stays.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- `[AIOM_brain]` citation key needs the pack allow-list (plan 5.1).
- Synonym "astrocytoma grade 4" is wrong for this IDH-wildtype GBM (plan 5.2).
- `accepted[0]` "Glioblastoma, IDH-wildtype, WHO grade 4 (left occipital)" uses "WHO grade" (plan 5.3); unchanged per ruling 3.

## Open questions for Andrea (judgment calls you could not settle)
- None. With a dense hemianopia already present, DTI is kept recommended because the optic radiation is edematous and continuous on tractography (recovery possible if spared), which is the plan's decision for this case.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the git diff and the whole final case.
- No reviewer notes. Checked: HPI now gives an outside non-contrast CT with 5 mm shift and no MRI result; no-seizure prohibition, levetiracetam absent from musts and drug check; DTI-only criterion (optic radiation; no motor or language cortex within about 1 cm) with soft constraint; required performance status in the stop rule (age 67), KPS 80 / ECOG 1 matching an independent retired patient who cannot drive; Stupp must valid at 67 with KPS 80; LP prohibition and harm naming shift, trapped occipital horn and papilledema; CSF fallback 25 cm H2O; labs all in range with female reference ranges; MRI impression imaging only; cataract red herring consistent with the exam and history; differential at the assessment-time view.
- Nothing found that needed a change. perfect_agent.py and case_io.py check clean.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `fallback_tool_outputs.eeg`: the normal "no focal slowing" study replaced by focal polymorphic slowing over the lesion (continuous delta at O1, T5, with left posterior dominant rhythm attenuation), no epileptiform discharges, in the RS06 format; a normal EEG contradicts a hemispheric mass with oedema (same class as M04, RS05, RS06).
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4 (left occipital)' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4 (left occipital)' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Library contradictions (25 Oct 2026)

Case-specific reports stored where the benchmark library's normal report contradicted the case. Why: the stored MRI shows a mass in the left occipital lobe (cuneus and lingual gyrus), extending into the posterior temporal lobe (4.9 x 4.1 x 3.8 cm) with an abnormal routine EEG and a focal history and exam; the library reports a normal head CT, a non-diagnostic biopsy, normal brain metabolism, perfusion and vessels, a normal prolonged EEG, no headache and normal bedside and neurophysiological tests where the exam is abnormal.

- order_ct_scan: CT showing the stored lesion(s) instead of a normal head CT (fallback_tool_outputs.ct)
- obtain_tissue_diagnosis open_biopsy: the stored integrated diagnosis on this procedure's specimen (fallback_tool_outputs.tissue_diagnosis)
- FDG_PET: hypermetabolic lesion(s) (fallback_tool_outputs.advanced_imaging)
- amino_acid_PET: FET-avid lesion(s) (followup request_amino_acid_pet)
- CT_perfusion: lesion perfusion matching the stored perfusion MRI (followup request_ct_perfusion)
- perfusion_SPECT: regional hypoperfusion over the lesion (followup request_perfusion_spect)
- cerebral_angiography: mass effect and lesion vascularity (followup request_cerebral_angiography)
- video EEG: the stored routine EEG's abnormalities over 24 h (followup request_video_eeg)
- ambulatory EEG: the stored routine EEG's abnormalities over 48 h (followup request_ambulatory_eeg)
- structured_headache_history_ichd3: the case's headache, prior primary headache and red flags (fallback_tool_outputs.clinical_assessment)

Checks: `perfect_agent.py` pass; `test_case_guards.py -k GLIO-HG-S06` pass; no fixed order still answered by the library (`lib4.source`); no 60-character window of any criterion's expected_evidence in the added text, except tissue copies that repeat the stored tissue report verbatim; every criterion's served output unchanged (snapshot diff against the baseline).
