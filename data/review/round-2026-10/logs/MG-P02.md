# MG-P02
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MG) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for myasthenia_gravis, applied through the condition plan (LEMS pathway, plan 3.5). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | "Repeat EMG ... suggesting possible NMJ involvement" gives away the RNS result; a surveillance CT 6 weeks ago makes the required CT redundant (class K). | FIXED: EMG sentence replaced by "referred to neurology because the weakness kept progressing"; last surveillance CT now 6 months ago; lobectomy named. |
| D | major | `patient.neurological_exam.additional` | NIF -68 in the exam (class K). | FIXED: removed. Exam gains post-exercise strength and reflex facilitation (a LEMS sign named in key evidence but absent from the exam); `physical_exam.general` weight 83.5 kg, height 178 cm, irregular pulse. |
| B | major | `initial_tool_outputs.labs.panels` | CBC and BMP "All normal" stubs (class G); Hu, Yo and N-type VGCC rows outside the plan's LEMS set; AChR reference "<0.5". | FIXED: real CBC, BMP, CK, HbA1c, B12, TSH; P/Q VGCC 0.62 nmol/L and SOX1 positive in panels named for the ordered assays; AChR and MuSK negative with correct ranges; Hu, Yo, N-type removed. |
| B | major | `initial_tool_outputs.specialized_test` | Baseline CMAPs contradict between findings (peroneal 1.8, median 1.2) and impression (deltoid 0.8); 50 Hz in deltoid and trapezius; recommendations in the report. | FIXED: one consistent study: ADM 2.1 mV and APB 1.2 mV baseline, 14% decrement at 3 Hz, 152% and 142% increment after 10 s maximal contraction (60% and 100% cut-offs, Oh 2005), sural SNAP 4 uV; no recommendations. |
| C | major | `initial_tool_outputs.body_imaging`, `followup_outputs` (`request_pet_ct_malignancy`) | PET node 1.4 x 1.2 cm "not seen on standard CT" is implausible on a contrast CT; PET modality "PET-CT (FDG)" (H5) in a follow-up. | FIXED: CT shows an 8 mm left hilar node not enlarged by size criteria; region "chest mediastinum"; PET moved to `initial_tool_outputs.advanced_imaging`, modality `FDG_PET`, avid 10 x 8 mm node SUVmax 8.4, no distant lesion. |
| B | major | `followup_outputs` (`request_hilar_biopsy_result`) | Biopsy filed as labs (H7) with a stage row. | FIXED: `initial_tool_outputs.tissue_diagnosis` (lymph_node_biopsy, EBUS station 10L): small cell carcinoma, TTF-1, synaptophysin, chromogranin A positive, p40 negative, Ki-67 above 80%. Required criterion with TTF1_IHC and chromogranin_A_synaptophysin_IHC. |
| B | major | `followup_outputs` (`request_3damp_treatment_lems`) | Wrong fact "amifampridine + metoprolol: both may prolong QT"; dose "10 mg TID, max 80 mg/day"; narrative `proposed`. | FIXED: `initial_tool_outputs.drug_interactions["amifampridine"]`: no interaction with any current medicine (metoprolol is not QT-prolonging); EU SmPC contraindications; 15 mg/day start, EU max 60 mg/day; ECG at start and after titration. |
| B | major | `followup_outputs` (`request_apixaban_3dap_ecg`) | Rhythm "Normal sinus rhythm (atrial fibrillation controlled)" with a PR interval; QTc 448 "borderline". | FIXED: `initial_tool_outputs.ecg`: atrial fibrillation, rate 68, PR not measurable, QRS 92, QTc 438 ms normal. |
| B | minor | `followup_outputs` (`request_autonomic_testing`) | Prose `test_type` (H5); HRV LF/HF ratio reported in a patient in atrial fibrillation. | FIXED: `autonomic_testing`; QSART distal reduction, tilt 12/4 mmHg fall, cardiovagal tests not interpretable in AF. |
| D | major | `followup_outputs` (`request_literature_lems_nsclc`) | Unverifiable sources ("NEJM 2023", "Neurology 2022"). | FIXED: deleted; initial literature with Titulaer 2011 and EFNS 2011 and the canonical LEMS summary. |
| C | major | `ground_truth.action_criteria` | Labs required a five-assay set; CT only as mediastinum_CT; literature required; ECG recommended; no tissue criterion. | FIXED per plan 3.5: labs `["anti_VGCC_PQ","anti_SOX1"]`, RNS, chest_CT with contrast (alternatives chest_abdomen_pelvis_CT, mediastinum_CT), FDG_PET, tissue, amifampridine check, ECG all required; autonomic, brain MRI staging, literature optional. |
| C | major | `ground_truth.avoided_actions` (`avoid-waste-3-analyze-brain-mri`) | Brain MRI called waste, but it is part of small cell lung cancer staging. | FIXED: avoided action removed; optional criterion `action-brain-mri-staging` (served by the library normal MRI); staging named in a must. EEG and CSF avoided rationales rewritten, citations empty. |
| C | minor | `ground_truth.sequence_constraints`, `stop_rule` | `labs -> literature`; stop rule with literature, max 0. | FIXED: chest CT -> FDG_PET, chest CT -> tissue, FDG_PET -> tissue (soft); stop rule the seven required criteria, max 2. |
| C | major | `ground_truth.assessment` | Musts were tool steps ("Confirm anti-VGCC", "RNS ..."); telithromycin; process prohibitions. | FIXED: five musts (oncology referral with staging, amifampridine titration with ECG, pyridostigmine add-on and IVIG for severe weakness, QT review of new drugs, anesthesia warning); prohibitions: no attribution to neuropathy, deconditioning or MG; no amifampridine with seizures or QT drugs; canonical drug line; no stopping the tumor search on CT alone. |
| C | minor | `ground_truth.differential` | MG moderate after facilitation and VGCC; statin myopathy "not on a statin" while he takes atorvastatin. | FIXED: MG low; myopathy very low; neuropathy low (coexisting); statin myopathy very low with atorvastatin named. |
| E | minor | `ground_truth.key_clinical_evidence`, `red_herrings` | Design commentary ("the principal MG mimic the case is designed to test"); AF red herring weak. | FIXED: five clinical lines including DELTA-P 3; red herrings: negative AChR, negative CT, chemotherapy neuropathy. |
| D | minor | `fallback_tool_outputs.ct` | Class F wording. | FIXED: plain normal head CT. |
| D | minor | whole case | British spellings in new text in all six of my cases. | FIXED in M01 to P02 (tumor, fiber, paresthesias and others), canonical literature summaries left verbatim. |

## Changes, in one paragraph a physician can read before re-reviewing

A 72-year-old former heavy smoker with a resected squamous lung cancer, atrial fibrillation on apixaban and metoprolol, and 4 months of proximal leg weakness, hyporeflexia that improves after exercise, dry mouth and erectile dysfunction. The work-up is the LEMS pathway: P/Q-type VGCC antibodies 0.62 nmol/L and SOX1 positive (AChR, MuSK negative); RNS with low CMAPs and 142-152% post-exercise increment; contrast chest CT without a mass (8 mm hilar node); FDG-PET with an avid left hilar node; EBUS biopsy showing small cell carcinoma, a new primary; amifampridine checked against his medicines (no interaction); baseline ECG in rate-controlled AF with QTc 438 ms. Autonomic testing, staging brain MRI and literature are optional. Musts: oncology referral and staging, amifampridine 15 mg/day titrated to at most 60 mg/day with ECG monitoring, pyridostigmine add-on or IVIG as needed, QT review of new drugs, anesthesia warning.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Composition: LEMS (G73.1) under the MG condition (plan section 6, question 1).
- Guidance claims: chest CT, not mediastinum CT, in this case; FDG_PET and tissue diagnosis required (plan CENTRAL 5).
- Criteria pack keys `[Titulaer_2011]`, `[EFNS_paraneoplastic_2011]` (named in text only; criteria cite `[Gilhus_2016]`).
- Synonyms: "paraneoplastic Lambert-Eaton myasthenic syndrome" and "LEMS with small cell lung cancer" should be accepted.

## Open questions for Andrea (judgment calls you could not settle)

- The plan's per-case note says the CT shows a hilar mass, so PET would be recommended. In the case the CT is the planned red herring (no mass), so FDG_PET is required under the plan's own rule ("required only if the CT is negative or equivocal"). I kept the negative CT, made the node 8 mm (plausibly missed) and set PET required. Agree?
- DELTA-P is in key evidence, not a must: with biopsy-proven SCLC the score no longer changes management. Should it be a must anyway?
- Added `FDG_PET -> tissue` as a third soft constraint, because only PET identifies the node to sample.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the plan (P02 entry, LEMS pathway 3.5, fact 24), the diff and the whole final case. No notes file exists for MG. Every FIXED finding is in the file: HPI without the EMG result and with the last surveillance CT 6 months ago; NIF out; exam shows post-exercise strength and reflex facilitation; labs P/Q VGCC 0.62 nmol/L and SOX1 positive, Hu/Yo/N-type removed; one consistent RNS (low CMAPs, 14% decrement, 152% and 142% post-exercise increment); contrast chest CT negative apart from an 8 mm hilar node, FDG-PET (`FDG_PET`) with the avid node, EBUS biopsy under `obtain_tissue_diagnosis` with TTF-1 and neuroendocrine markers; amifampridine check without the metoprolol-QT error; ECG in AF with QTc 438 ms and no PR; autonomic testing routed by `autonomic_testing` and not reporting HRV in AF; brain MRI no longer waste (SCLC staging). DELTA-P 3 (bulbar speech, erectile dysfunction, age at onset 50 or more; not smoking at onset, no weight loss recorded) is correct and gives a high SCLC probability.

Found and changed:
- Fact error: the ECG criterion rationale, the amifampridine must and the drug-check warning said the EU SmPC requires an ECG "after titration". The Firdapse SmPC (section 4.4) requires clinical and ECG monitoring at initiation and yearly thereafter, and an immediate ECG if arrhythmia is suspected. Rewrote `action-8-analyze-ecg.rationale`, the amifampridine must and `initial_tool_outputs.drug_interactions.amifampridine.warnings` accordingly.
- Consistency: `fallback_tool_outputs.cardiac_monitoring` reported a normal Holter in sinus rhythm in a patient in atrial fibrillation (template carry-over). Rewritten as rate-controlled AF throughout, no significant pause or ventricular arrhythmia.
- Language: the CT hilar-node finding read "unchanged in appearance from soft tissue around the hilar vessels" (unclear); reduced to "Left hilar lymph node 8 mm in short axis, not enlarged by size criteria."

Open questions resolved (Andrea's rule): (1) Negative CT with FDG_PET required stays: it follows the plan's own rule (PET required when CT is negative) and the EFNS screening sequence. (2) DELTA-P stays in key evidence, not a must: with biopsy-proven SCLC it no longer changes management. (3) The FDG_PET -> tissue soft constraint stays (only the PET identifies the node to sample). Nothing is left for Andrea.

For the lead (outside this case): MG-RM13 carries the same "ECG after titration" wording in a must and in its drug-check warning, and plan fact 24 states it; it should read "at initiation and yearly thereafter" per the EU SmPC.

Checks after the change: `perfect_agent.py MG-P02 -v` passes, `case_io.py check` clean for the case, case guards and discriminator check pass.

## Condition audit (MG auditor, 24 Oct 2026)

- action_criteria citations: [Gilhus_2016] (an MG review) removed from 10 LEMS criteria; rationales cite Titulaer 2011, EFNS 2011, Oh 2005 and the EU SmPC in text (as RM13). FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.
