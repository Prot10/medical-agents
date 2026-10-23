# GLIO-HG-M05
Reviewer status: R1 not reviewed, R2 needs_changes (3 notes) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 618200ca-b876-485e-acbf-d85e4d56add0 | FIXED | `CDKN2A_B_deletion` added to the required assays of `action-9-obtain-tissue-diagnosis` (IDH1_IHC, IDH1_IDH2_sequencing, ATRX_IHC, 1p_19q_codeletion, CDKN2A_B_deletion, MGMT_methylation) and to both tissue reports ("No homozygous deletion"); the criterion rationale states that the deletion alone assigns grade 4 (WHO 2021, EANO 2021); expected evidence, key evidence and differential (grade 4 entry) cite the result instead of "lacks all grade-4 features". |
| 0c310d30-7992-4682-8be6-81c16b915225 | FIXED | No-seizure class (C5): levetiracetam must deleted, the canonical prohibition of antiseizure prophylaxis added (AIOM Q23), levetiracetam removed from the drug check (now dexamethasone against propranolol and sumatriptan); key evidence states that prophylaxis is not indicated; the EEG waste entry keeps the canonical rationale. |
| 615481ca-f4b2-4948-92dd-9a3f63f7af66 | FIXED | Group A: tissue criterion accepts `resection` first and `stereotactic_biopsy` of the enhancing, highest-rCBV foci if resection is not safely feasible, one follow-up per procedure; must 1 is the C3 surgery must with functional MRI, DTI and intraoperative mapping. New recommended `action-fmri-functional-mapping` (hand motor 8 mm, SMA 5 mm, premotor activation within the lesion, LI 0.75) and `action-dti-tractography` (CST through the corona radiata FLAIR, 3 mm from the enhancing focus) with authored outputs and soft constraints before tissue. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | Outpatient MRI result in the HPI twice, including "the radiologist raised concern for a glioma" (C8). | FIXED: non-contrast CT with an ill-defined left frontoparietal hypodensity and mild mass effect. |
| B | major | `initial_tool_outputs.mri.findings[0].mass_effect`, impression | "2 mm leftward falcine deviation" for a left-sided mass. | FIXED: rightward shift; impression rewritten as numbered findings without grading claims. |
| A/D | major | `initial_tool_outputs.tissue_diagnosis` | Tissue in the initial work-up; site "ATRX-loss, left frontoparietal"; meta-text impression; "WHO grade 3". | FIXED (C2): two follow-ups, site "left frontoparietal lobe", `molecular_findings` holds the nine assays only, integrated diagnosis "Astrocytoma, IDH-mutant, CNS WHO grade 3", impression with MGMT. |
| A | major | literature criterion, follow-up and fallback | Literature as a scored step. | FIXED (C1): deleted. |
| D | minor | `followup_outputs[0]`, `[1]` | Perfusion and MRS impressions graded the tumour ("below the level most characteristic of glioblastoma", "WHO grade 2 not supported"). | FIXED: metric-only numbered impressions. |
| E | minor | `patient.neurological_exam.additional` | Author aside ("easily attributed ... by a casual examiner"). | FIXED: deleted. |
| C | major | criteria, constraints, stop rule | No performance status; labels said imaging "confirms" grade. | FIXED: plan order, KPS 80/ECOG 1 follow-up, hard MRI and labs constraints, canonical perfusion and MRS wording. |
| C | major | `assessment.required_recommendations` | Must 6 duplicated the "no therapy before tissue" prohibition; MRI and labs musts duplicated scored criteria; molecular must listed TERT, EGFR and +7/-10 without CDKN2A/B; no post-diagnosis treatment must. | FIXED: surgery must with the IDH-mutant panel, canonical dexamethasone must, and the C11 grade 3 must (radiotherapy followed by adjuvant temozolomide, EANO 2021); the duplicate stays only as a prohibition. The enzyme-inducer prohibition is dropped with the antiseizure drug (no seizure). |
| C | major | `ground_truth.differential` | Grade 2 astrocytoma "high", GBM and oligodendroglioma "moderate" after tissue excludes them; old WHO names. | FIXED: assessment-time view, all very_low, CNS WHO names, grade 4 astrocytoma entry added. |
| C | minor | `red_herrings[0]` | Imaging said to "establish" high-grade physiology. | FIXED: imaging supports and targets; tissue with CDKN2A/B grades. |
| C | minor | drug check | Proposed levetiracetam; sumatriptan "hold, resolved headache etiology". | FIXED: dexamethasone against propranolol (blood pressure, fluid retention) and sumatriptan (no interaction); NKDA noted. |
| C | minor | `avoided_actions` CSF, cardiac | Generic rationales. | FIXED: C17 (2 mm shift, left ventricular compression); cardiac canonical. |
| C | minor | `metadata.clinical_pearls[0]`, `[2]` | "Anaplastic astrocytoma"; imaging "critical for grading"; grade 3 without CDKN2A/B. | FIXED: rewritten; em dashes in HPI, exam and pearls replaced. |
| B | minor | labs | Type and screen with a clinical-significance string (C9). | FIXED: null; values otherwise consistent (anion gap 11, Hct = RBC x MCV). |

## Changes, in one paragraph a physician can read before re-reviewing

The HPI now cites a non-contrast CT, and the MRI shift is rightward for this left-sided mass. The pathway is MRI, perfusion, spectroscopy, labs, performance status (KPS 80), fMRI (hand motor 8 mm, SMA 5 mm), DTI (corticospinal tract 3 mm from the enhancing focus), then resection or, if not feasible, stereotactic biopsy of the enhancing foci, and an optional drug check. Both tissue reports give Astrocytoma, IDH-mutant, CNS WHO grade 3: IDH1 R132H mutant, ATRX lost, 1p/19q intact, no CDKN2A/B homozygous deletion, no necrosis or MVP, MGMT methylated. Musts: resection with fMRI, DTI and mapping and the full IDH-mutant panel; dexamethasone at the lowest effective dose; MDT, radiotherapy followed by adjuvant temozolomide. He has had no seizure, so prophylaxis is now prohibited rather than required. The differential is at the assessment-time view.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Synonyms "glioblastoma", "GBM", "glioma who grade 4", "grade 4 glioma" and "astrocytoma grade 4" are appended to this grade 3 IDH-mutant astrocytoma; all are wrong for the entity and grade (plan section 5.2). Not hand-edited.
- accepted[0] "Astrocytoma, IDH-mutant, CNS WHO grade 3 (ATRX-loss, left frontoparietal)": the "ATRX-loss" qualifier is not part of the WHO name (plan section 5.3).
- `metadata.condition_name` still reads "anaplastic astrocytoma, WHO grade 3" with an em dash; it is condition-level text.
- `[AIOM_brain]` key (plan section 5.1).

## Open questions for Andrea (judgment calls you could not settle)

None.

## Verification

Adversarial check (24 Oct 2026). All three notes fixed: CDKN2A/B is required and reported "No homozygous deletion", and with no MVP or necrosis and 9 mitoses per 10 HPF grade 3 is now established; the "lacks all grade-4 features" claim is gone from key evidence and the differential; no levetiracetam anywhere, the prophylaxis prohibition is present, and the EEG waste entry is coherent with "no seizures" in the HPI; resection first with fMRI (hand motor 8 mm, premotor within the lesion) and DTI (CST 3 mm) as recommended criteria with outputs and soft constraints. The grade 3 must (radiotherapy then adjuvant temozolomide, EANO 2021) matches the entity; the HPI now cites a non-contrast CT only; rightward shift for a left mass; labs arithmetic correct (gap 11, MCHC 33.7). Synonyms with "glioblastoma" and grade 4 terms remain under CENTRAL, correctly not hand-edited. No change made; perfect_agent and case_io check clean.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `initial_tool_outputs.mri.impression`: trailing sentence "Tissue diagnosis recommended for grading." removed, for uniformity with the other 25 GLIO-HG MRI impressions (imaging-only, plan C9); the style guide allows it, so this is consistency, not an error fix.
- `fallback_tool_outputs.eeg`: the normal "no focal slowing" study replaced by focal polymorphic slowing over the lesion (intermittent theta-delta at F3, C3), no epileptiform discharges, in the RS06 format; a normal EEG contradicts a hemispheric mass with oedema (same class as M04, RS05, RS06).
  `metadata.fallback_tool_kinds.eeg` updated to match.
- `metadata.condition_name`: retired "anaplastic astrocytoma, WHO grade 3" now "astrocytoma, IDH-mutant, CNS WHO grade 3" (WHO CNS5 terminology).
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).
