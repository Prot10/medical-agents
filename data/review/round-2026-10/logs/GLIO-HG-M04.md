# GLIO-HG-M04
Reviewer status: R1 not reviewed, R2 needs_changes (2 notes) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 457ccd8f-c786-43fa-8ec1-fa45af285fa4 | FIXED | One procedure policy, group A: the tissue criterion `action-9-obtain-tissue-diagnosis` accepts `resection` first and `stereotactic_biopsy` only if resection is not safely feasible (AIOM Q1), with one follow-up per procedure; the surgery must `required_recommendations[0]` is the C3 text with preoperative functional MRI, DTI tractography and intraoperative mapping. New recommended `action-fmri-functional-mapping` (hand motor area 9 mm, right SMA 6 mm from the enhancing margin) and `action-dti-tractography` (CST 7 mm, genu, frontal aslant tract) with authored outputs and soft constraints before tissue. |
| af437c8f-f3fc-48e0-a463-4c73ba1a77ba | FIXED | `CDKN2A_B_deletion` added to the required assays (with IDH1_IHC, IDH1_IDH2_sequencing, ATRX_IHC, 1p_19q_codeletion, MGMT_methylation) and to both tissue reports: "No homozygous deletion"; grade 4 rests on the microvascular proliferation and necrosis already in the histology. The literature fact (CDKN2A/B deletion confers grade 4) moved into the tissue criterion rationale; the literature step is deleted (C1). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | Outpatient MRI result in the HPI (C8). | FIXED: referring ED non-contrast CT with a right frontal hypodensity, oedema and slight leftward shift. |
| B | minor | `patient.clinical_history.medications` | HPI says he takes over-the-counter ibuprofen; not in the medication list. | FIXED: ibuprofen 400 mg as needed added; must to stop it before surgery and dexamethasone; drug check covers it. |
| E | minor | `patient.neurological_exam.additional` | Author aside "The subtle left pronator drift is the most localizing finding". | FIXED: deleted. |
| C | major | `assessment.required_recommendations` | "Continue levetiracetam for post-operative seizure prophylaxis" although he had two focal seizures, the second on levetiracetam 500 mg twice daily. | FIXED: treat class, continue form with dose increase (for example 1000 mg twice daily), no enzyme inducers. |
| C | major | `avoided_actions` EEG waste | Penalised EEG in a patient with seizures (C5). | FIXED: removed. The case fallback EEG was a normal study, which contradicts a right frontal tumour with focal seizures; replaced by right frontal polymorphic slowing without epileptiform discharges (`fallback_tool_outputs.eeg`, kind "case-specific"). |
| C | major | musts | Template Stupp must for an IDH-mutant tumour; molecular must listing EGFR and TERT; MRI and labs musts. | FIXED: C11 IDH-mutant grade 4 "managed like glioblastoma" with 60 Gy/30 and temozolomide (EANO 2021); assays folded into the surgery must (IDH, ATRX, 1p/19q, CDKN2A/B, MGMT); MRI/labs musts removed (scored criteria). Dexamethasone must per C11. |
| A/D | major | `initial_tool_outputs.tissue_diagnosis` | Tissue in initial work-up; meta-text impression; "Integrated Diagnosis" and histology items listed as molecular findings; "WHO grade 4". | FIXED (C2): two follow-ups, Histology row, `molecular_findings` holds the seven assays only, integrated diagnosis "Astrocytoma, IDH-mutant, CNS WHO grade 4". |
| A | major | literature criterion, follow-up and fallback | Literature as a required step. | FIXED (C1). |
| D | minor | `followup_outputs[0]`, `[1]` | Threshold teaching text in perfusion and MRS; MRS impression concluded the tumour type. | FIXED: numbered metric impressions. |
| C | major | criteria, constraints, stop rule | No performance status; MRI expected evidence fine but perfusion and MRS labels "confirm high-grade features". | FIXED: plan 3.1 order, KPS 80/ECOG 1 follow-up, hard MRI and labs constraints, canonical perfusion and MRS wording (support, not confirm). |
| C | major | `ground_truth.differential` | IDH-wildtype GBM "high", lower-grade and oligodendroglioma "moderate" after tissue excludes them; "WHO grade" names. | FIXED: assessment-time view, all very_low, CNS WHO names. |
| C | minor | `key_clinical_evidence` | Literature-derived survival figures, "features all present in this case", em dashes. | FIXED: rewritten from the case. |
| C | minor | `red_herrings[0].correct_interpretation` | Said perfusion and spectroscopy "confirm grade 4". | FIXED: histology assigns grade; imaging does not grade. |
| C | minor | `avoided_actions` CSF, cardiac | Generic rationales. | FIXED: C17 (4 mm shift, frontal horn effacement); cardiac canonical. |
| C | minor | drug check | Output fine in substance; expected evidence echoed the template. | FIXED: adds ibuprofen, dose-increase review, NKDA; expected evidence rewritten (leak guard passes). |

## Changes, in one paragraph a physician can read before re-reviewing

The HPI now cites a non-contrast CT, and the ibuprofen he takes is in the medication list. The pathway is MRI, perfusion, spectroscopy, labs, performance status (KPS 80), fMRI (hand motor 9 mm, SMA 6 mm), DTI (corticospinal tract 7 mm), then resection or, if not feasible, stereotactic biopsy, and an optional drug check. Both tissue reports give Astrocytoma, IDH-mutant, CNS WHO grade 4: IDH1 R132H mutant by IHC and sequencing, ATRX lost, 1p/19q intact, CDKN2A/B without homozygous deletion (grade 4 from MVP and necrosis), MGMT methylated, TERT wildtype. Musts: resection with fMRI, DTI and mapping and the full IDH-mutant panel; dexamethasone at the lowest effective dose; continue and uptitrate levetiracetam for the two seizures (treatment, not prophylaxis), no enzyme inducers; stop ibuprofen; MDT, 60 Gy/30 with temozolomide as for glioblastoma. The EEG is no longer penalised. The differential is at the assessment-time view.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms "glioblastoma", "GBM" and "astrocytoma grade 4" are appended to this IDH-mutant astrocytoma; "glioblastoma" and "GBM" are wrong for the entity (plan section 5.2). Not hand-edited.
- accepted[0] "Astrocytoma, IDH-mutant, WHO grade 4 (right frontal lobe)": "CNS WHO grade" normalisation (plan section 5.3).
- `[AIOM_brain]` key (plan section 5.1).

## Open questions for Andrea (judgment calls you could not settle)

None.

## Verification

Adversarial check (24 Oct 2026). Both notes fixed: one scored procedure policy (resection first, biopsy only if not feasible) consistent across criterion, must 1 and the two follow-ups, with fMRI (hand motor 9 mm) and DTI (CST 7 mm) justified by the MRI's extension toward the precentral gyrus; CDKN2A_B_deletion is in both alternatives and both reports ("No homozygous deletion"), and grade 4 rests on the MVP and palisading necrosis printed in the histology. Checked the treat-class must (two focal seizures, recurrence on 500 mg twice daily, uptitration), the removed EEG waste entry with a fallback EEG that now fits a right frontal tumour, ibuprofen added to the medication list as the HPI describes, the IDH-mutant grade 4 treatment must (no Stupp citation, managed like glioblastoma per EANO 2021), ATRX loss and TERT wildtype consistent with the entity, differential all at the assessment-time view, leftward shift for a right mass, labs arithmetic (MCHC 34.2). The MRI impression's hedged "lower-grade glioma with anaplastic transformation cannot be excluded" is a single imaging hedge, allowed by the style guide, not a retired entity name. No change made; perfect_agent and case_io check clean.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `initial_tool_outputs.mri.impression`: trailing sentence "Tissue diagnosis is recommended for definitive characterization." removed, for uniformity with the other 25 GLIO-HG MRI impressions (imaging-only, plan C9); the style guide allows it, so this is consistency, not an error fix.
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).
