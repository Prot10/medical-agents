# GLIO-HG-RM02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| a02b3fb0-497b-4b63-a4f2-d9d202b77622 | FIXED | `action-10-obtain-tissue-diagnosis` assays are now `IDH1_IHC`, `IDH1_IDH2_sequencing` (age 34), `ATRX_IHC`, `H3K27_status` and `MGMT_methylation`. 1p/19q, TERT and EGFR are no longer required (IDH-wildtype, with MVP and necrosis present). The tissue report (now a follow-up) states "H3 K27M not detected on immunohistochemistry and sequencing; H3K27me3 retained", so the entity stays glioblastoma, IDH-wildtype. The source case report does not give H3 status; see Open questions. The surgery must, key evidence and differential name H3 K27. |
| fea3f998-baca-4272-b96e-7a738a25df5a | FIXED | The CSF follow-up is deleted, so the test returns no diagnostic information. The `avoid-harm-1-analyze-csf` rationale and `prohibited_recommendations[0]` are rewritten for the spinal block (C17): "Lumbar puncture below an expanded cord with near-complete effacement of the subarachnoid space risks neurological deterioration (spinal coning)". The AQP4 and MOG results it carried move to a non-invasive serum serology follow-up (see own findings). |
| 7dbf817c-1aca-4945-8369-342feebad962 | FIXED | `action-1-analyze-brain-mri` is rewritten as neuraxis staging. Its expected evidence: "No intracranial lesion above the cervicomedullary junction, where the cranial pole of the cord lesion reaches the lower medulla; no hydrocephalus or leptomeningeal enhancement". The brain MRI report is rewritten. The first finding ("bilateral occipital, epicranial") matches the examination's occipital subcutaneous nodules, so it is kept as scalp neurofibromas, with the parotid plexiform lesion. A finding for the medullary pole is added. Thoracic-cord observations that a brain study cannot see are removed, and so is the impression's claim of "bulbar findings" (she has none). |
| 15ee9c7d-b3eb-4381-8cd2-7ab86addfc8d | FIXED | One contrast spine MRI remains: `request_spine_MRI_with_contrast` is first in `followup_outputs`, and `action-2-order-body-imaging` is first in the criteria. The non-contrast duplicate ("as previously described") is deleted, and its T1-T3 oedema and no-drop-metastasis content is merged into the contrast report. The stringified dict signal fields are now plain text, and the contradictory "homogeneous peripheral enhancement of the main mass" is removed. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.tissue_diagnosis` | Tissue sat in the initial work-up. The procedure was `stereotactic_biopsy`, which is not used in the cord. The site was "contrast-enhancing rim", histology parameters were listed as molecular findings, and the impression carried meta-text (C2, C3). | FIXED: group D. The follow-up `request_resection_open_biopsy_laminectomy` uses procedure `resection`, meaning open biopsy via laminectomy, and its site is C4-C5. Histology is now a row. Integrated diagnosis is "Glioblastoma, IDH-wildtype, CNS WHO grade 4", and the impression follows C2. CENTRAL `open_biopsy`. |
| A | major | `action-4-search-medical-literature`, two literature follow-ups | Required literature step in the stop rule (ruling 5). The NMOSD literature output served the differential to any query. | FIXED: both follow-ups, the criterion and its stop-rule id deleted. |
| C | major | criteria | No NMOSD exclusion. A longitudinally extensive lesion reaching the area postrema is an NMOSD presentation, and serum AQP4-IgG belongs before a cord biopsy. With the CSF deleted, nothing else carries it. | FIXED: recommended `action-aqp4-mog-serology` (`interpret_labs` `panels: [AQP4_IgG]` or `[NMO_MOG]`). Its follow-up is serum AQP4-IgG and MOG-IgG, both negative (the case's own CSF values). A soft constraint orders it before tissue. CENTRAL: `[Wingerchuk_2015]` for the GLIO-HG allow-list. |
| A | major | sequence constraints, stop rule | One soft template constraint, from brain MRI to tissue. | FIXED: hard constraints spine MRI to tissue and labs to tissue. Soft constraints brain MRI to tissue and serology to tissue. Stop rule: spine MRI, brain MRI, labs, tissue. |
| C | major | `assessment.required_recommendations` | Template Stupp must (60 Gy exceeds cord tolerance) and template steroid must. Interchangeable biopsy and resection. Labs and consult musts. Nothing on high cervical respiratory risk or on the estrogen contraceptive. | FIXED: group D surgery must; dexamethasone must for cord oedema; respiratory and bulbar monitoring (lesion from C2 to the medulla); stop the combined pill, with a pregnancy test. Entity must: radiotherapy with temozolomide at about 50.4 to 54 Gy for cord tolerance, plus a trial (deviation from the canonical 60 Gy, see Open questions). |
| A | minor | perfusion and MRS criteria and follow-ups | Recommended, although spinal DSC perfusion and MRS are technically limited and not standard practice. Grading thresholds were quoted, and the impressions read "See findings above". | FIXED: both made optional; thresholds removed; quantitative data and impressions written, each noting the technical limit. |
| B | major | DDI follow-up | Proposed temozolomide before tissue. Its warnings leaked "MGMT promoter unmethylated status in this case" (engineering text and leakage). It claimed that temozolomide induces enzymes and lowers contraceptive efficacy. | FIXED: the follow-up now checks dexamethasone against her medicines, including the estrogen VTE warning and the codeine intolerance. Added an optional `action-check-drug-interactions`, last (C13). The guard passes. |
| A | minor | criteria | No performance status (C7, age 34). | FIXED: recommended criterion; follow-up KPS 70, ECOG 2. |
| B | minor | `initial_tool_outputs.labs` | `type_and_screen` row carried meta-text. No pregnancy test in a woman on a combined pill facing surgery and chemoradiotherapy. | FIXED: Blood_Bank row; serum beta-hCG negative added; factual interpretation. Anion gap 13 and MCHC 33.3 checked. |
| B | minor | `patient.clinical_history.social_history.exercise` | Leg weakness "2 weeks ago" against a 4-day history. | FIXED: "until this week". |
| B | minor | `initial_tool_outputs.eeg` | Occipital amplitude asymmetry against "no focal slowing". The impression linked the EEG to "brainstem pathology". | FIXED: non-specific diffuse slowing only. EEG waste added (`avoid-waste-3-analyze-eeg`). |
| C | minor | `ground_truth.differential` | MPNST, ependymoma and NF1 low-grade glioma were all "moderate" at assessment time. Diffuse midline glioma, NMOSD and high-grade astrocytoma with piloid features were missing. "Staging negative" assumed an optional CT. | FIXED: seven entries at assessment time, each with what supports and what excludes it. |
| C | minor | red herrings, key evidence | The one red herring had an empty `field_path`. Key evidence asked for MRI "of the entire neuraxis" and listed molecular markers without H3 status. | FIXED: three red herrings (NF1, area postrema, TSH 5.8 with normal free T4). Key evidence rewritten from the case's findings. |
| A | minor | citations, avoided actions, CT CAP | Duplicate keys and `WHO_CNS5`; `[Stupp_2005]` on the MRI; template waste rationales; interpretive CT impression ("supports a primary CNS process"). | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 34-year-old woman with NF1 and a stable childhood optic pathway glioma. Over four days she has developed right arm weakness, a spastic paraparesis, a Lhermitte sign and a band-like sensory change. She has had no seizures and is on a combined oral contraceptive. Pathway:
- Contrast spine MRI, first: an expansile, heterogeneously enhancing intramedullary lesion from the lower medulla to C7 (about 12 cm), with an exophytic component, near-complete subarachnoid effacement and T1-T3 oedema.
- Brain MRI as neuraxis staging: no intracranial lesion above the cervicomedullary junction; scalp and parotid neurofibromas.
- Labs, with a negative beta-hCG.
- Serum AQP4-IgG and MOG-IgG: negative.
- Performance status: KPS 70.
- Open biopsy via cervical laminectomy: glioblastoma, IDH-wildtype, CNS WHO grade 4. MVP and necrosis are present, H3 K27M was not detected, H3K27me3 is retained, IDH is wildtype on IHC and sequencing, ATRX is retained and MGMT is unmethylated.

The lumbar puncture and its result are gone; LP is harm for a spinal block. Literature, the duplicate non-contrast spine MRI and the template Stupp must are gone. Perfusion and spectroscopy are optional. Musts:
- open biopsy;
- dexamethasone;
- respiratory and bulbar watch;
- stop the estrogen pill;
- after the diagnosis, temozolomide chemoradiotherapy at a cord-tolerant dose, plus a trial.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Vocabulary: `obtain_tissue_diagnosis` needs an `open_biopsy` procedure. Intramedullary tumours are sampled by open biopsy via laminectomy, which is scored here as `resection` (plan C3, group D).
- Criteria-pack allow-list: `[Wingerchuk_2015]` (NMOSD criteria; already in the MS-RR pack), and `[AIOM_brain]` for the prophylaxis prohibition (plan 5.1).
- The C17 spinal-block LP rationale has no citation in the pack; `[Hasbun_2001]` is kept on the entry but concerns intracranial herniation.
- Synonyms: accepted[0] "WHO grade 4 (cervical spinal cord)" should follow the CNS WHO wording (plan 5.3).

## Open questions for Andrea (judgment calls you could not settle)

- H3 status is authored. The source report (PMC7642760) does not give it. I wrote H3 K27M not detected with H3K27me3 retained, which keeps the accepted glioblastoma label (plan: "the report states H3 wildtype"). If the source tumour was H3-altered, the entity would be diffuse midline glioma, and the case would need a ruling-3 label change.
- In an adult with NF1, high-grade astrocytoma with piloid features is a WHO CNS5 differential that needs DNA methylation profiling. I added it to the differential as low. The vocabulary has no methylation-profiling assay, so it is not required.
- The entity must uses a cord-tolerant dose (about 50.4 to 54 Gy) instead of the canonical 60 Gy in 30 fractions, because the target is the cervical cord and medulla.
- Spinal perfusion and MRS were demoted to optional, since they are not standard practice in the cord.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the notes (a02b3fb0, fea3f998, 7dbf817c, 15ee9c7d) and the whole final case.
- Notes: all four are in the table and fixed. H3K27_status and IDH sequencing are required, and the report states H3 wildtype. No CSF follow-up remains, and the spinal-block rationale is in both the avoided action and the prohibition. Action-1 is neuraxis staging, with a plausible brain report (scalp and parotid neurofibromas matching the exam). There is one contrast spine MRI, first in both the criteria and the follow-ups, with a hard constraint to tissue.
- Cross-field checks: AQP4/MOG panels are in the vocabulary; the codeine intolerance and the combined pill are reflected in the DDI output and the musts; MCHC 33.3; anion gap 13; the cord-tolerant RT dose; the group D `resection` procedure in both the criterion and the follow-up.
- Found and fixed:
  1. Brain MRI. The new observation "Optic nerves and chiasm without enhancement or expansion" contradicted the known left optic pathway glioma, stable for over 20 years. It now reads "Mild fusiform enlargement of the intraorbital left optic nerve without enhancement, consistent with the known optic pathway glioma; chiasm normal".
  2. Brain MRI impression. "dedicated spinal MRI is needed" was management advice that steered the agent to a required criterion. Deleted; the report still says the lesion extends below the field of view.
  3. Spine MRI impression. "tissue diagnosis is recommended" was deleted (C9).
  4. The area postrema red herring states that she has no area postrema symptoms, but the HPI did not record that. The HPI negative now reads "no headache, visual changes, facial weakness, difficulty swallowing, nausea, vomiting or hiccups".
  5. The CT CAP criterion rationale was a copy of its label. It now reads "Optional: a solitary intramedullary metastasis is very unlikely at 34 without a known primary."
  6. `[Hasbun_2001]` (CT before LP in suspected meningitis) was cited on the spinal-block LP harm entry, which it does not support. The worker had flagged this. The citation is removed, so the entry now has none, as the pack has no source for spinal coning (CENTRAL, already logged).
- After the fixes: `perfect_agent.py` passes, `case_io.py check` reports no failure naming the case, and `test_case_guards` passes.

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4 (cervical spinal cord)' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4 (cervical spinal cord)' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- must removed: 'Obtain contrast-enhanced MRI of the spine, with brain MRI for neuraxis staging, before any invasive procedure.' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- fallback specialized_test (generic 'Study within normal limits.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- avoid-harm-1-analyze-csf: citation [Hollis_1986] added (LP below a spinal block); it had none
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['spinal cord glioma', 'intramedullary glioma']; added ['intramedullary glioblastoma', 'glioblastoma', 'GBM', 'high grade glioma', 'malignant glioma'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Central vocabulary wired (24 Oct 2026)

Terms added by commit e19131d6 (batch-2 review vocabulary), wired as the plan and this log intended. The earlier CENTRAL vocabulary request in this log is resolved by them.

- `action-10-obtain-tissue-diagnosis`: first alternative is now `open_biopsy` (the procedure the label, must and site always described); `resection` kept as the second alternative for a debulking where it can be done safely (both obtain diagnostic tissue; the choice is carried by the surgery must). Label and rationale updated. The tissue follow-up is now `procedure: open_biopsy` (trigger `request_open_biopsy_laminectomy`); a new follow-up `request_debulking_resection_laminectomy` (`procedure: resection`) has the same results with an "Extent of resection" row (subtotal debulking of the exophytic and enhancing C4-C5 component) so the second alternative is answered by the case.
- New recommended criterion `action-dna-methylation-profiling` (`obtain_tissue_diagnosis` with `DNA_methylation_profiling`, open biopsy or resection), after the tissue criterion. Reason: in an adult with NF1, high-grade astrocytoma with piloid features is the WHO CNS5 alternative and its essential criterion is a methylation profile; recommended, not required, because TERT mutation and EGFR amplification already meet the glioblastoma criteria. Both tissue reports carry the result: methylation class glioblastoma, IDH-wildtype, subclass RTK II (calibrated score 0.93), no match to HGAP, CNV EGFR amplification and +7/-10 (consistent with the stored EGFR amplification). Citations `[WHO_2021]`, `[Capper_2018]`.
- Differential: HGAP now very_low, with the methylation result in key features (was "DNA methylation profiling would settle it").
- Perfect-agent note: the methylation criterion is answered by the same stored tissue report as the tissue criterion (expected: one specimen, one report; a real agent orders both in one call, which matches both criteria).
- CENTRAL: pack group D ("scored as `resection` until an `open_biopsy` term exists") is obsolete; add `[Capper_2018]` (Capper D et al. DNA methylation-based classification of central nervous system tumours. Nature 2018;555:469-474) to the pack allow-list.

Checks after the change: `perfect_agent.py GLIO-HG-RM02 -v` ok, `case_io.py check` (schema and synonym guard OK, no failure names the case), `test_case_guards.py -k "GLIO-HG- or ALZ-EARLY-"` 120 passed.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
