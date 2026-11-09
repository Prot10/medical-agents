<!-- Copied on 9 Nov 2026 from the credentialed workspace (report/07_methods.md on EOS). Aggregates only: no record content, no MIMIC identifiers; the one 8-digit number is the selection seed. Paths starting with $W or ~/projects/ma-mimic refer to the rockhopper workspace. -->

# NeuroBench-MIMIC: conversion of MIMIC-IV admissions into executable neurology cases (methods)

Task 07, 9 Nov 2026. This document replaces `06_methods.md` and stands alone. It gives counts and rules only and contains no record content.

Every number below comes from a script in `~/projects/ma-mimic/agent-platform/scripts/external_datasets/`. The commands are in `07_pilot.md`; the machine-readable aggregates are in `07_flow.json`.

## 1. Data sources and data use

### Sources

| Source | Version | Used for |
|---|---|---|
| MIMIC-IV | 3.1 (`hosp`, `icu`) | admissions, diagnoses, labs, microbiology, medications, ICU charting |
| MIMIC-IV-ED | 2.2 | triage, ED vitals and rhythm, ED medications |
| MIMIC-IV-Note | 2.2 | discharge notes, radiology reports |
| MIMIC-IV-ECG | 1.0 | machine measurements and machine statements (after checksum verification) |

MIMIC-IV-ECHO is not on the storage used; echocardiography comes only from echo results written in the discharge note.

### Credentialing and data rules

- All data were accessed under a PhysioNet credentialed-access Data Use Agreement.
- All processing ran on one CERN machine under a zero-data-retention model account:
  - record content was stored only in the credentialed workspace;
  - no record content left the machine;
  - no model outside this account read records;
  - every reader and reviewer subagent ran under the same data rules and wrote only inside the workspace.
- Reports and this document carry aggregates only.

## 2. Cohort

### Inclusion and exclusion

Inclusion:
- a principal discharge diagnosis mapped to one of 20 NeuroBench conditions (ICD-9/10 map, `mimic_neuro.py`);
- the admission came through the ED;
- a discharge note exists;
- the patient's first admission for the condition.

Exclusions by rule:
- inter-hospital transfers, including hidden ones: coded thrombolysis elsewhere, V45.88 / Z92.82, treatment, intubation or work-up at an outside facility (decisions 8, 21);
- chief complaints that name a test result, a transfer or "s/p" (decision 7);
- age above 89 (decision 11).

### Strict pool

An admission enters the strict pool when:
1. every required step of the condition's transferred policy has a real result in the record, with the lab-panel rule of decision 3; and
2. the record supports the code: the discharge diagnosis names the condition, or the note documents its defining evidence (decision 10).

### Reading

Drawn candidates are read by reader subagents against the source. They exclude on:
- outside work-up, evaluation or treatment, also when it is stated only in a radiology report indication;
- an exam charted after ED thrombolysis;
- status that began during the stay;
- record support not established;
- thin EEG (decision 32);
- a non-temporal focus (decision 33);
- possible focal status (decision 34);
- SAH aneurysm status not established (decision 42);
- a core step without a servable result.

### CONSORT-style flow per condition

| Condition | Principal dx | New ED admissions with note, not transfer | Hidden transfers dropped | CC dropped | Usable | Core steps servable | Strict | Read | Excluded on reading (main reason) | Selected |
|---|---|---|---|---|---|---|---|---|---|---|
| ISCH | 6,216 | 2,223 | 225 | 346 | 1,652 | 389 | 356 | 60 | 22 (transfer after outside work-up, 16) | 38 |
| SYNC | 4,327 | 1,115 | 0 | 222 | 893 | 229 | 40 | 40 | 40 (not cardiac syncope, 34) | 0 |
| GLIO | 1,127 | 179 | 0 | 37 | 142 | 1 | 1 | 1 | 1 (core step without a servable result) | 0 |
| SAH | 989 | 347 | 1 | 273 | 73 | 30 | 23 | 23 | 11 (aneurysm status not established, 5) | 12 |
| MIG | 971 | 286 | 3 | 25 | 258 | 0 | 0 | 0 | not ED-servable | 0 |
| FEPI | 952 | 148 | 0 | 23 | 125 | 28 | 10 | 28 | 26 (transfer, 8; non-temporal focus, 6; core step, 6) | 2 |
| HEP | 568 | 103 | 0 | 12 | 91 | 37 | 22 | 15 | 5 (transfer after outside work-up, 3) | 10 |
| MS | 455 | 106 | 0 | 14 | 92 | 42 | 39 | 32 | 10 (outside work-up, 5) | 22 |
| SE | 411 | 132 | 1 | 29 | 102 | 35 | 11 | 35 | 26 (record does not support the code, 14) | 9 |
| PD | 392 | 41 | 0 | 11 | 30 | 6 | 1 | 0 | not ED-servable | 0 |
| ALZ | 328 | 73 | 0 | 6 | 67 | 0 | 0 | 0 | not ED-servable | 0 |
| GBS | 218 | 83 | 0 | 4 | 79 | 5 | 5 | 5 | 2 (whole-stay respiratory/telemetry summaries) | 3 |
| FND | 216 | 61 | 0 | 5 | 56 | 22 | 19 | 19 | 17 (transfer, 8; no admission functional signs, 5) | 2 |
| MG | 191 | 44 | 0 | 3 | 41 | 0 | 0 | 0 | required mediastinal imaging / RNS not in record | 0 |
| NPH | 153 | 9 | 0 | 3 | 6 | 0 | 0 | 0 | not ED-servable | 0 |
| VASC | 123 | 27 | 0 | 4 | 23 | 0 | 0 | 0 | not ED-servable | 0 |
| ALS | 77 | 21 | 0 | 5 | 16 | 1 | 1 | 0 | not ED-servable | 0 |
| BACT | 74 | 20 | 0 | 4 | 16 | 4 | 3 | 3 | 1 (diagnosis not supported) | 2 |
| NMDAR | 61 | 12 | 0 | 3 | 9 | 0 | 0 | 0 | required pelvic imaging / antibody panel not in record | 0 |
| FTD | 54 | 20 | 0 | 0 | 20 | 0 | 0 | 0 | not ED-servable | 0 |
| **Total** | 17,903 | 5,050 | 230 | 1,029 | 3,791 | | | | | **100** |

Notes:
- **Not ED-servable** means the required work-up is a clinic or longitudinal act with no recorded admission result: MIG (structured ICHD-3 history), ALZ and FTD (neuropsychological battery), VASC (cognitive screen and course), PD (course plus outpatient DaT imaging), NPH (elective tap-test admissions), ALS (EMG plus course). Decision 51 puts these seven out of scope for an ED-admission source.
- **SYNC** is ED-servable, but all 40 strict candidates were excluded on reading (34 not cardiac syncope, 6 transfers). Decision 50 puts SYNC out of scope for this source.
- **SAH, SE, FND and FEPI** have no strict candidates left after reading. Their replacements came from ISCH (section 3).

## 3. Selection

### Allocation

1. Six task-04 conditions are kept: ISCH, SAH, SE, MS, FEPI, GBS. GBS stays limited by MIMIC (decision 20).
2. Further conditions are added in order of strict-pool size while the required work-up is servable from an ED admission: HEP, FND, BACT.
3. An exclusion is replaced from the same condition's pool in seed order. When that pool is exhausted, the replacement comes from ISCH, then SAH, then MS (task-07 instruction).

Final allocation: **ISCH 38, MS 22, SAH 12, HEP 10, SE 9, GBS 3, FND 2, FEPI 2, BACT 2.**

Changes from task 06:
- 11 cases were removed: 6 SAH, 2 SE, 1 FND, 1 FEPI, 1 ISCH.
- 11 ISCH cases were added in seed order.
- Reasons for the task-07 exclusions:
  - SAH aneurysm status not established: 5;
  - transfer after an outside evaluation: 1 SAH;
  - possible transfer stated in a radiology indication: 1 SE;
  - defining evidence of status only in the ED course: 1 SE;
  - outside work-up: an earlier visit to another ED, 1 FND;
  - frontal focus (decision 49): 1 FEPI;
  - exam charted after ED thrombolysis: 1 ISCH.
- 6 further ISCH draws were excluded on reading (4 transfers, 1 not an ischaemic stroke, 1 chief complaint naming an ECG result) before the next draws were kept.

### Draw

- Task-04 cases are taken first.
- The rest of each strict pool is shuffled once with seed 20261108 and taken in order.
- Every drawn admission and its exclusion are recorded in `$W/out/07_selection.csv` (`case_id`, `exclusion`). The 100 cases are the rows with a `case_id` and no exclusion.

## 4. Case construction

### 4.1 Decision point and time window

- Times are hours from ED arrival.
- **Extra studies** (ECG, imaging, serial labs, microbiology) are served up to admission + 48 h.
- **First policy studies** of the stay (brain MRI, spine MRI, CSF, EEG, EMG) follow the task-04 rule: the first result of the stay answers the policy step, even after admission + 48 h (decision 44). Every policy study's hours from ED arrival are stored in hidden metadata (`policy_study_hours`). Distribution:
  - 392 timed policy results: median 2.3 h, 90th percentile 25.8 h, maximum 129.8 h; 15 later than 48 h after ED arrival;
  - 12 after admission + 48 h: MS spine MRI 3, MS brain MRI 2, MS CSF 2, SE brain MRI 3, GBS respiratory function 1, FEPI brain MRI 1;
  - 46 policy results are note-extracted with no recorded time.
- **A first study that is not a policy step** and falls after admission + 48 h is not served: 4 MRIs, 3 CSFs and 2 spine MRIs.
- **Brain imaging after a definitive procedure** of the stay (coiling, embolization, thrombectomy, stenting, craniotomy) that is not a policy step is not served: 1 MRI, 3 follow-up studies.
- Only the first policy microbiology specimen may fall after the decision point.

### 4.2 Record-to-tool mapping

The case serves 16 tools.

| Tool | Record source | Rule |
|---|---|---|
| `interpret_labs` | `hosp/labevents` | First value per item from ED arrival − 1 h to admission + 24 h, in panels. An item whose first draw has no recorded result is not served at all. An analyte already served is not served again from another item code. Decision 23 withholds a first value drawn after a treatment of that analyte. Decision 30: prophylactic anticoagulation does not block coagulation. Decision 38: numeric-column values are served with range checks. Repeats are a follow-up (decision 47, 4.3). |
| `analyze_csf` | `hosp/labevents` CSF; discharge note | First LP sample. Note-stated results of the same LP are added as note-extracted fields: appearance, opening pressure with its unit, named special tests. A disease name inside a test label or result is removed (as decision 24 does for reports). A drain sample is served only with its true `source`, never for a `lumbar_puncture` order (decision 44). |
| `order_ct_scan` | radiology reports | Plain CT: the NCCT report, or the explicitly described non-contrast part of a CTA report (decision 2). This includes a paragraph that opens on the non-contrast images. CTA: the angiographic part only. Non-contrast sentences and perfusion-section sentences are left out. Vessel narrowing and atherosclerosis stay with the CTA. |
| `analyze_brain_mri` | radiology MR head reports | The orbit section of a combined brain/orbit study is part of the answer (`orbits` protocol). MRA/MRV sections and spine sections of combined reports go elsewhere, split by section headers after the FINDINGS label. Contrast follows the exam title when the technique's contrast belongs to a neck MRA. |
| `order_body_imaging` | radiology | Spine MRI (policy) with brain-section sentences removed. Chest X-ray, chest CT, abdomen/pelvis CT/US, spine CT and venous duplex up to 48 h. The first film of a kind keeps its other sentences when it mentions an earlier procedure; a later film that shows a procedure of the stay is not served. |
| `order_advanced_imaging` | radiology | CT perfusion, MRA, MRV, carotid duplex: each answer keeps only its own modality's sentences. |
| `analyze_ecg` | MIMIC-IV-ECG | First machine read in the window; rate from RR (decisions 1, 14). An interval outside a plausible range is not served (PR 80–400 ms, QRS 40–250 ms, QT 200–700 ms). No PR interval or P axis on a tracing read as atrial fibrillation or flutter. Up to 3 later reads as follow-ups. |
| `order_cardiac_monitoring` | ICU chartevents rhythm, ED vitalsign rhythm | Summary over the work-up window when ≥ 12 h are covered (decision 5). |
| `analyze_eeg` | discharge note | Must state the decisive finding (decision 32); true `eeg_type`; first EEG initial, later ones in time order (decision 41). The `limitations` field states the drugs of the ED medication record given before the recording (decision 46), and inpatient infusions only when timed before it. |
| `order_echocardiogram` | discharge note | Echo results. An EF range stays in the text with an empty numeric field (decision 29). |
| `order_specialized_test` | discharge note | EMG/NCS and respiratory function, first recording only (decisions 19, 20). |
| `order_microbiology` | `hosp/microbiologyevents` | One output per specimen and time, one result per test. A urinary antigen test does not answer a urine-culture order. `collected_before_antimicrobials` is set as follows: from ED and ward antibiotic times; false when an antibacterial is on the home list; null when only an antiviral is, or when the HPI names antibiotics without a time. |
| `perform_clinical_assessment` | discharge note | Documented admission signs (FND: functional signs). |
| `obtain_tissue_diagnosis` | discharge note | Procedure and result (no GLIO case selected). |
| `check_drug_interactions`, `search_medical_literature` | MockServer knowledge base | Not record content; transferred at the template's level (decisions 17, 28, 37). |

### 4.3 Repeat lab values (decision 47)

- Repeat values (second value per item, up to admission + 48 h) are withheld only for the analytes a stated treatment changes:
  - insulin or dextrose: glucose and potassium;
  - red cells: haemoglobin, haematocrit and red-cell count;
  - platelets: platelets;
  - plasma or vitamin K: INR, PT, PTT;
  - therapeutic anticoagulation: coagulation. This covers a heparin infusion or procedural heparin, and an oral anticoagulant or a therapeutic-dose LMWH given or started in hospital (decision 30).
- A timed treatment blocks only later draws. A treatment stated in the note without a time blocks every repeat of that analyte. The note is searched whole, minus its medication lists.
- Repeat blood gases and drug levels stay withheld.
- Counts over the 100 cases:
  - repeat values served: 2,260;
  - withheld because a treatment was timed: glucose 40, coagulation 24 (heparin), coagulation 6 (plasma/vitamin K);
  - withheld because the note states a treatment without a time: glucose 12, coagulation 27 (anticoagulant), red-cell indices 27, coagulation 5 (plasma/vitamin K), platelets 1;
  - repeat gas and level values withheld: 102;
  - implausible electrolyte sets dropped (decision 38): 7.
- Like for like, on the 89 cases common to the task-06 and task-07 selections, repeat values rose from 1,681 to 2,003 (+322): this many came back under decision 47.

### 4.4 Presentation

- **Demographics** come from the record (OMR or the note).
- **Chief complaint:** the triage chief complaint. A symptom-derived label or `UNKNOWN-CC` is rewritten from the kept HPI, with the original kept in the audit (decisions 7, 9).
- **HPI:** cut by readers and by rule. Cut:
  - the ED and outside work-up, treatment and response;
  - the hospital course;
  - this episode's diagnosis;
  - prior episodes' work-up results (decision 12).

  Kept: EMS care (decision 31) and a known disease in the history (decision 25).
- **Medications:** the note's pre-admission list. Where the parse broke, a reader extracted it verbatim (10 cases), leaving out header lines and held items. A blanked brand name is served by its intact generic name. 31 list fragments without dose or frequency were dropped.
- **Social history:** the note's Social History section when intact (6 cases), without sentences holding a blank. MIMIC blanks the section entirely in the other 94.
- **Exam:** the admission exam as charted, with state and devices kept and treatment-naming items cut (decision 15).
- **Exam grids** (decisions 35, 45):
  - A row is served cell by cell by column position only when every row of the grid fits the header.
  - A row shortened by its own blank serves only the cells before that blank.
  - A row shorter than its header with no blank of its own is not attributable.
  - A two-word column name and a footnote mark are read as cells.
  - Counts: 110 rows served whole, 87 as an attributable prefix, 32 not attributable, 641 cells not attributable.
- **Vitals:** the first triage set, else the first ED vitalsign row. When the ED record holds fewer than 3 values, the admission exam's vitals line of the note is used (8 cases). Vitals are empty in 3 cases.

### 4.5 Reports: findings plus impression (decisions 6, 13, 24)

Kept:
- what the study shows, including pattern words;
- comparisons with earlier studies.

Removed:
- recommendations, including "correlation with" another study, labs or CSF, "would be more sensitive", and "attention in follow-up is advised";
- result communication;
- references to later studies and to other studies of the stay (only the pointer clause goes);
- procedures, lines and tubes of the stay;
- differential clauses of the form ", although X should be considered", and "clinical significance is uncertain";
- an aneurysm inference in a plain CT, together with its "a distribution …" clause;
- disease names the study cannot establish (the pattern stays).

A sentence left broken by a cut is dropped whole: one ending on a function word, a lone "but/and …" clause, or a leading "The remainder of …". A "CONCLUSION" section and a header-only "IMPRESSION" line both count as the impression.

### 4.6 De-identification (decisions 16, 27)

- A blank that makes a negation or an exception list ambiguous is never served.
- Blanked values are not served; the rest is.
- If a core element of a required step is then missing, the step is not covered.

### 4.7 "Not available"

- A study never done, or done outside the window, answers "not available" with `provenance: record`.
- Every served answer records its origin (`table`, `note_extracted`) and source in hidden metadata.

### 4.8 Completeness (100 cases)

| Condition | Cases | Tools with a result (mean, range) |
|---|---|---|
| BACT | 2 | 6.0 (5–7) |
| FEPI | 2 | 4.5 (4–5) |
| FND | 2 | 5.0 (4–6) |
| GBS | 3 | 7.0 (5–8) |
| HEP | 10 | 4.7 (4–6) |
| ISCH | 38 | 6.7 (5–8) |
| MS | 22 | 4.5 (3–8) |
| SAH | 12 | 5.5 (4–7) |
| SE | 9 | 7.4 (5–10) |

- Required criteria with a served result: 289 / 289. Recommended: 96 / 96.
- Extras served:
  - later ECGs: 34;
  - later EEGs: 11;
  - extra imaging reports: 165;
  - repeat lab values: 2,260;
  - microbiology specimens: 138.
- Fields left empty:
  - social history 94 (blanked by MIMIC);
  - handedness 66;
  - height 49 and weight 36;
  - family history 10;
  - medications 10;
  - allergies 6;
  - vitals 3;
  - past medical history 3;
  - physical exam 3.

## 5. Policies and labels

### 5.1 Policy transfer

- Each condition's policy is transferred from its 30 NeuroBench template cases. A step is required or recommended when at least half of the templates make it so.
- Lab panels resulted in under 50 % of a condition's cohort are dropped (decision 3): troponin (ISCH), B12/TSH/HIV (MS), CK (GBS), ammonia (HEP), procalcitonin/CRP/HIV (BACT).
- Adaptations, applied to every case of the condition:
  - the microbiology specimen is required without `before_antimicrobials`;
  - the clinical assessment is answered from documented signs;
  - a recommended CSF criterion is dropped when the only CSF is a drain sample (3 SAH cases).
- Within each condition every case has the modal required set (`06_policy_alignment.csv`).

### 5.2 Knowledge tools (decisions 17, 28, 37)

- Transferred at the template's level: required when at least half of the templates require it.
- For SE, 14 of 30 templates require `check_drug_interactions`, so it is recommended.
- SAH cases coded I60.8 keep the condition's aneurysmal knowledge criteria (decision 28).
- The perfect agent accepts the knowledge-base answer: 71 such answers.

### 5.3 Avoided actions and assessment (decision 18)

- Drafted per case from the template condition, keeping only items that the case's documented facts support, with a pointer into the audit.
- The differential is empty.

### 5.4 Diagnosis labels (decisions 40, 42, 43, 48)

**Accepted labels.**
- They come from `agent-platform/config/policies/diagnosis_synonyms.yaml` for the case's codes.
- They are expanded with `apply_diagnosis_synonyms.py --cases-dir $W/out/06_cases --overlay $W/out/07_synonyms_overlay.yaml --prune`, and `--check` with the same flags passes.
- The repository file is not edited.

**SAH (decision 42).** The aneurysm status is read from the angiography and the note:
- aneurysm shown: 6 cases, which keep I60.x (I60.9 5, I60.6 1);
- angiography negative: 5 cases, primary code I60.8;
- non-aneurysmal other cause: 1 case, primary code I60.8;
- status not established: 5 cases excluded and replaced.

I60.8 cases accept only the non-aneurysmal labels. A rejected label never shares all its words with an accepted one. Traumatic SAH stays excluded.

**Overlay (decision 43).** `07_synonyms_overlay.yaml` has 13 entries. Each `except_cases` entry is paired, where needed, with a case-scoped entry whose labels are copied verbatim from the repository's own entries:

| Entry | Cases | Reason | Belongs in the repository file? |
|---|---|---|---|
| `I63.40` except + `I63.40+mimic-embolic` [embolic stroke] | 3 ISCH | I63.40 grants septic-embolism and endocarditis labels to every embolic stroke; these records show no infection | yes: restrict the septic labels to cases with infection |
| `I63.412` except + `I63.412+mimic-embolic` [embolic stroke] | 1 ISCH | I63.41x grants "cardioembolic stroke"; the record shows no cardiac source | yes: the cardioembolic label needs a cardiac source |
| `F44+seizures` except | 2 FND (1 now excluded) | the category entry grants functional-seizure labels to functional weakness or sensory FND | yes: limit to F44.5 |
| `G61.0+aidp` except | 1 GBS | AIDP labels where the EMG shows no demyelinating polyradiculoneuropathy | yes: AIDP labels need an AIDP EMG |
| `G35` except + `G35+mimic-progressive` [multiple sclerosis, MS] | 1 MS | G35 grants relapsing-remitting labels to a primary progressive course | yes: course-specific labels need the course |
| `G40` except + `G40+mimic-unlocalised` [focal epilepsy] | 1 FEPI | temporal-lobe labels where the record does not localise the focus | yes |
| `I60.8` except + `I60.8+mimic-nonperimesencephalic` / `I60.8+mimic-avm` (non-aneurysmal labels only) | 3 SAH (1 now excluded) | the I60.8 entry also grants perimesencephalic labels to convexity, sulcal or AVM-related bleeds | yes: split I60.8 by pattern |

**Rejected labels (decision 48).**
- The synonyms file grants none, so each case gets the labels carried by at least half of its condition's templates.
- When that gives none, the threshold drops to one third. SE also gets its clinical mimics, PNES and syncope, with strings the repository uses.
- Labels that overlap an accepted label, or that a sentence of the case's own note names as a diagnosis of the stay, are left out.
- Per-case removals are listed in `07_rejected_removals.json`: CIS in 2 MS cases, a documented comorbidity in 1 MS case, PPMS labels in 1 MS case, PNES labels in 1 FEPI case, a dissection label in 1 SAH case.
- The one-third rule applies to all 9 SE cases and 1 HEP case. Every case has at least one rejected label.

### 5.5 Approval status

All policies, labels and drafts are marked `draft` until two physicians approve them.

## 6. Validation

### 6.1 Automatic checks (final build)

| Check | Result |
|---|---|
| Schema (`NeuroBenchCase`) | 100 / 100 |
| Build errors (verbatim checks of every served text against the note or report, including reader extractions) | 0 |
| Synonyms `--check` (overlay, prune) | 0 changes |
| Cases without a rejected label | 0 |
| Timing: no extra study after admission + 48 h except the first policy microbiology specimen; follow-ups in time order | 0 errors |
| Perfect agent on the MockServer | 100 / 100 pass, 0 warnings, 71 knowledge-base answers |
| Policy alignment: required criteria without a served result | 0 |

### 6.2 Independent field-by-field re-read

**Protocol** (`REREAD6_PROTOCOL.md`, "Round 3 and later").
- Each case file holds:
  - the case as built, with every follow-up, the hidden flags, the policy and the labels;
  - the source: triage, ED medication times, discharge note, radiology reports and machine ECG reads.
- Reader subagents who had not built the cases check every field against the source.
- Severity: `error` means wrong, leaking or misattributed content, or a required item that is wrong or missing. `minor` means cosmetic, a non-core omission, a faithful source inconsistency, or a settled rule; each minor finding states why it is minor.
- Lab values are checked by script.
- Rules settled during the task are added to the protocol: decisions 42–48, the grid, vitals, CSF, social-history, EEG-statement, post-treatment-imaging, medication and lab-source rules. Each later round reads them.

**Stopping rule.**
- Round 3 re-reads all 100 cases.
- After fixes, every case is re-read that had an error or whose served content changed since its last reading. Changes are found by an order-free comparison of the built case (`mimic_case_diff7.py`).
- A round that changed almost every case is a full round.
- The loop ends when a round finds 0 errors and no code change follows it unread.

| Round | Cases | Fields | Errors (cases) | Error rate per field | Minor |
|---|---|---|---|---|---|
| 3 (all) | 100 | 4,399 | 62 (48) | 1.41 % | 545 |
| 4 (all) | 100 | 4,359 | 24 (21) | 0.55 % | 534 |
| 5 | 50 | 2,179 | 22 (16) | 1.01 % | 245 |
| 6 | 93 | 3,924 | 11 (7) | 0.28 % | 424 |
| 7 | 40 | 1,669 | 6 (6) | 0.36 % | 187 |
| 8 | 19 | 787 | 1 (1) | 0.13 % | 77 |
| 9 | 29 | 1,228 | 9 (7) | 0.73 % | 136 |
| 10 | 16 | 752 | 4 (4) | 0.53 % | 70 |
| 11 | 8 | 406 | 0 (0) | 0 | 33 |
| 12 (cases changed after round 11) | 3 | 123 | 0 (0) | 0 | 20 |

Notes on the rounds:
- Rounds 5, 9 and 10 rose because fixes changed many cases, including 3 new replacement cases in round 9. Some errors were regressions from the previous round's fixes, which the next round found.
- The residual measured over all 100 cases in the last full round (round 4) is **0.55 % of fields** (24 errors in 21 cases). Every case was later re-read whenever its content changed. The final two rounds found 0 errors.

### 6.3 Blind leakage rounds

**Protocol.**
- Each case is rendered as the harness shows it, under a shuffled code with no id, condition, diagnosis or policy.
- Reviewers who did not build the cases classify every presentation and tool-output issue as `leak` or `borderline`.

**Stopping rule.**
- Round 1 covers all 100 cases.
- Each later round covers the cases that leaked, every case changed since the last round, and 10 random controls not used before.
- The loop repeats until a round finds 0 leaks.

| Round | Cases | Seed | Leaks: presentation / tool | Cases with a leak | Leak classes |
|---|---|---|---|---|---|
| B1 | 100 | 6701 | 0 / 8 | 7 | broken text 6, recommendation 2 |
| B2 | 40 | 6702 | 0 / 4 | 4 | recommendation 2, other study 2 |
| B3 | 26 | 6703 | 0 / 1 | 1 | broken text 1 |
| B4 | 19 | 6704 | 0 / 1 | 1 | broken text 1 (the B3 fix had not applied) |
| B5 | 13 | 6705 | 0 / 0 | 0 | stopping rule met |

No presentation leak was found in any round. The blind rounds also caught 3 transfers that reading had missed: 2 were stated in the HPI, 1 only in a radiology indication. All 3 were excluded and replaced.

## 7. Decision log (decisions 1–51, one-line rationale each)

### Sources and results
- **1.** ECG from MIMIC-IV-ECG machine reads only: a reproducible source independent of the notes.
- **14.** ECG rate from the machine measurements; no rate, no ECG: a rate is never invented.
- **2.** The plain CT inside a CTA counts only when the non-contrast part is explicit: a plain-CT order must not return the angiogram.
- **5.** Telemetry from structured rhythm data with ≥ 12 h coverage: a written order is not a result.
- **19, 20.** Whole-stay telemetry or EEG summaries serve only the first recording; GBS stays at 3 cases.
- **32.** A thin EEG counts only when it states the decisive finding.
- **41.** Every EEG is stored with its true type, in time order.
- **29.** An echo EF range stays in the text with the numeric field empty.
- **38.** Numeric-column values are recorded values, range-checked.
- **44.** The first result of the stay answers a policy step; its hours are recorded; drain CSF is not a lumbar puncture.

### Labs and treatment
- **3.** A lab panel resulted in < 50 % of the cohort is dropped from the policy.
- **23.** A first value drawn after a treatment of that analyte is not served.
- **30.** Prophylactic anticoagulation does not block coagulation; therapeutic doses do.
- **47.** Repeat values are withheld per analyte the treatment changes, by time when timed and wholly when only stated: the repeat values carry the patient's course.
- **27.** Blanked values are not served; the rest is.

### Reports and wording
- **6.** Reports are findings plus impression.
- **13, 24.** The impression keeps the entity the study shows; disease names the study cannot establish go; pattern words stay.
- **36, 46.** EEG treatment wording stays; the ED drugs given before the recording are stated, inpatient ones only when timed.
- **16.** A blank that makes a negation ambiguous is never served.
- **35, 45.** Grids are served cell by cell where the alignment is certain; otherwise only the attributable prefix.

### Presentation
- **7, 9.** Symptom-derived triage labels are rewritten from the HPI; labels that need a test drop the admission.
- **12.** Prior episodes stay; their work-up results are cut.
- **15.** The exam after ED treatment keeps state and devices and cuts diagnosis-chosen treatment.
- **25.** A known disease in the history stays and is flagged (29 cases).
- **31.** EMS care is pre-hospital and stays.

### Cohort and selection
- **8, 21.** Hidden and treatment-only transfers are excluded: an outside work-up leaks into the presentation.
- **10.** A case needs record support for its code.
- **11.** Age above 89 is excluded.
- **26.** A clinical diagnosis without test confirmation stays, flagged `clinical_only` (21 cases); an unruptured aneurysm with a parenchymal bleed is ICH.
- **33, 34, 49.** FEPI keeps temporal or unlocalised foci; possible focal status and frontal foci are excluded.
- **4.** BACT is reported as limited by MIMIC.
- **39.** Task-03 cases are superseded.
- **50.** SYNC is out of scope for this source (0 of 40 strict admissions were cardiac syncope).
- **51.** MIG, ALZ, FTD, VASC, PD, NPH and ALS are out of scope for an ED-admission source.

### Policies and labels
- **17, 28, 37.** Knowledge-tool criteria follow the template level; the perfect agent accepts the knowledge-base answer.
- **18.** Avoided actions are drafted only from documented facts.
- **40.** Labels come from the repository synonyms file, expanded by its own script.
- **42.** SAH aneurysm status comes from the record; non-aneurysmal SAH is I60.8; status not established excludes the case.
- **43.** Other label errors are fixed by a workspace overlay that reuses only labels the repository already grants; each entry has a reason (5.4).
- **48.** Rejected labels use one third of the templates when half gives none; SE adds its mimics; every case has at least one.

## 8. Limitations

1. **Condition coverage.**
   - 9 of 20 conditions yield cases.
   - 7 are out of scope for an ED-admission source (decision 51), and SYNC is out of scope (decision 50).
   - GLIO, MG and NMDAR have no admission with every required step.
   - GBS (3), FND (2), FEPI (2) and BACT (2) are limited by MIMIC. SE (9) and SAH (12) exhausted their strict pools.
2. **Allocation.** ISCH (38) and MS (22) are over-represented, to reach 100 under the replacement rule.
3. **Late policy studies.** 12 policy results come after admission + 48 h (4.1); the decision point therefore differs by tool.
4. **Labels.**
   - The synonyms file needs the fixes listed in 5.4; until then the overlay carries them.
   - Rejected labels are template-derived and draft.
5. **De-identification.**
   - Grids lose cells: 641 cells and 32 rows are not attributable. Weakness grading is lost where only a one-cell prefix survives.
   - Social history is blanked in 94 cases.
   - Many dates are blanked, so some EEG times (12) and comparisons are unknown.
6. **Note-extracted content.** EEG, echo, EMG, respiratory function, clinical assessment, CSF special tests (30 fields), social history and 10 medication lists come from reader extraction, checked verbatim by the builder. Their recording times are often unknown.
7. **Conservative removals.**
   - Repeat values of treated analytes, repeat gases and levels are withheld (4.3).
   - Non-policy brain imaging after a definitive procedure is not served.
   - Follow-up imaging that shows a procedure of the stay is not served.
   - DSA and embolization reports are not served.
8. **Text repair by rule.** Broken fragments are detected with patterns. The last blind round found none in 13 cases, but the pattern set is not exhaustive.
9. **Residual error.** The last full re-read measured 0.55 % of fields in error. Later rounds re-read only error and changed cases, and the final two found 0 errors. Minor findings remain at about 10 % of fields checked, each with a stated reason.
10. **Rendering.** The harness shows an empty indication as "()" after each medication, and the grid marker "(remaining cells not attributable)" is visible to the agent. Harness code was not changed here.
11. **Echo.** MIMIC-IV-ECHO is not available; echo comes only from the note.
12. **Approval.** Policies, labels and drafts await approval by two physicians.
