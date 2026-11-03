# External datasets for NeuroAgent: validation of four candidates

21 October 2026. Follows the first look in the PhD hub
(`~/Documents/PhD/UPF/Presentazioni/2026_10_21_phd-narrative/NeuroAgent_datasets.md`).

**Part 1** answers the current question. Under narrative 2 of today's UPF deck ("Learning and
Reasoning under Information Constraints"), the cases need not be neurological. What matters is
that a source can be turned into episodes that work like NeuroAgent's. Part 1 grades each source
on that, with effort, time and completeness. **Part 2** is the first, neurology-only pass. Its
tool mapping, prototype and governance notes still apply.

An episode needs:

1. a presentation that does not already state the answer;
2. results the agent discovers by calling tools, coming from the record;
3. a reference for the trajectory;
4. a final diagnosis to score, ideally with a differential and with safety constraints;
5. permission to process the data with our models and to share the result.

# Part 1: any domain

## Verdict

| Source | Episodes (measured → estimated) | Completeness | Work, days | Calendar | Verdict |
|---|---|---|---|---|---|
| **MIMIC-IV** own cohort (+ Note, ED, ECG) | Demo: 49 clean of 275 admissions (18 %). Full: ≈30,000–50,000, **estimate** | ≈75 % | 15–20, plus 7–10 shared | Work 4–5 weeks; plus the credentialing wait, unknown (PhysioNet warns of significant delays since June 2026) | **Yes, main real source** |
| MIMIC-IV-Ext-CDM (a curated MIMIC derivative) | 2,400 (four abdominal diseases) | ≈65 % | 4–6, plus shared | 2–5 weeks, same access | **Yes, first step**: fastest real split, with published baselines |
| MedMemoryBench | 20 personas (+ the aligned ZH set); 14 with a full diagnostic arc | ≈65 % per case | 4–6, plus shared | 1–2 weeks, no access needed | **Yes, as a small longitudinal/privacy testbed**, not as a benchmark |
| MedLoCoMo | 304 episodes in 2,981 admissions | ≈60 % | 6–9, plus shared | Blocked | **No for now**: no licence, and a subset of MIMIC-IV-Note |
| CPRD GOLD | Not measurable without access | ≈35 % | 10–15 | 2–4 months for approvals, if they are granted | **No**: codes only; £20,600 a year; CPU-only enclave with aggregate-only exports |

**Completeness** scores the five requirements above as eight fields, each counted 0, ½ or 1:
presentation narrative, exam, vitals, served results, trajectory reference, final diagnosis,
differential or red herrings, and safety constraints. **Work** is days of implementation with
coding agents. **Shared** is the one-off harness work below, paid once whichever sources are
used.

## Measured, one case at a time

Scripts: `agent-platform/scripts/external_datasets/general_audit.py` writes one row per admission
to `outputs/external_datasets/{mimic_demo,medlocomo}_general.csv`.

An admission counts as a **diagnostic episode** when it is:

- an unplanned admission (not elective), not a transfer;
- with a chief complaint that does not name the diagnosis (`SDH`, `PNA`, `CVA`, `Transfer`, …);
- with a principal diagnosis whose three-character ICD family is new to the patient;
- with at least five labs in 24 h and at least one diagnostic order or culture.

In MedLoCoMo the lab criterion is replaced by an HPI, a physical exam, "Pertinent Results" and a
radiology or microbiology report.

### MIMIC-IV demo

**59 of 275** admissions pass the filters (21.5 %). I then read each one: diagnosis, triage
complaint, labs and the kinds of orders. **10 are weak**:

- the diagnosis is already known: leukaemia relapse;
- iatrogenic events: two postoperative infections, an insulin-pump complication;
- coding noise: hyperhidrosis for "weakness", iatrogenic hypotension, unspecified anaemia, malnutrition;
- trauma protocols with an intubated patient.

That leaves **49 clean episodes (18 %)**. They span 12 ICD chapters:

| ICD chapter | Episodes |
|---|---|
| Infectious | 12 |
| Digestive | 10 |
| Injury | 8 |
| Circulatory | 7 |
| Neoplasm | 5 |
| Respiratory | 5 |
| Nervous | 5 |
| Other | 6 |

Good diagnostic puzzles among them:

- "Chest pain, N/V" that ends as a perforated duodenal ulcer;
- "Left hand pains" that ends as an intracranial abscess;
- "Hypothermia" from insulin poisoning;
- "SOB" from acute cor pulmonale;
- "R leg pain, weakness" from lung cancer;
- "Dizziness" from thiamine deficiency;
- "Lower-extremity pain" from aortic dissection;
- "Chest pain" from pericarditis.

The demo has no notes, so the HPI and exam criteria cannot be tested there. MedLoCoMo, built
from the same notes, has an HPI in 99 % of admissions, an exam in 96 % and results in 96 %. Notes
are not the binding filter.

### MedLoCoMo

- **304 of 2,981** admissions are episodes (10.2 %). The rate is low because each patient has 30
  admissions on average, so most diagnoses are already known: only 893 are new.
- The chief complaint names the diagnosis in 594 admissions.
- 31 of the 304 HPIs already state results ("CT showed…").
- By ICD chapter:

  | ICD chapter | Episodes |
  |---|---|
  | Infectious | 49 |
  | Injury | 49 |
  | Digestive | 45 |
  | Respiratory | 45 |
  | Circulatory | 36 |
  | Symptoms | 17 |
  | Musculoskeletal | 15 |
  | Genitourinary | 14 |
  | Other | 34 |

### Full MIMIC-IV, estimate

Applying the 10–18 % range to the 331,794 discharge summaries gives **≈30,000–50,000 candidate
episodes**. The demo is a cohort where every patient has an ICU stay, and MedLoCoMo is
repeat-heavy, so the range is wide. Scale is not the constraint: at this size the cost is in
references and review, not in finding cases. `mimic_cohort.py` counts the real number on the
first day of access, by condition or, with `--all-domains`, by ICD chapter.

### MedMemoryBench

Read persona by persona: the opening health events, plus a script that finds the event with
the correct diagnosis. 18 of the 20 personas are written as a **diagnostic delay**:

1. symptoms;
2. one to four wrong attributions by a primary-care doctor ("occupational strain",
   "perimenopause", "IBS", "hypertensive nephropathy");
3. tests with values;
4. the correct diagnosis, typically after 6–12 test events.

The exceptions are persona 2, already diagnosed, which shows treatment intensification, and
persona 3, where the hypertension is already known.

About **14 personas have a full arc**: 2–4 wrong attributions and at least 6 test events before
the diagnosis. Examples:

| Persona | Diagnosis | Results before the diagnosis |
|---|---|---|
| 10 | ADPKD | renal ultrasound, eGFR, UPCR |
| 12 | Lupus nephritis | urinalysis, creatinine |
| 14 | Ulcerative colitis | occult blood, calprotectin 182 µg/g, CRP |
| 19 | Graves' disease | heart rate, TSH/FT4 |
| 20 | PCOS | HOMA-IR, Ferriman–Gallwey |

The format maps onto ours:

- The wrong attributions map to `red_herrings`.
- Each persona has **6 trap events** (allergies, interacting drugs, swallowing problems) that map
  to contraindicated or harmful actions, i.e. our safety caps. Examples: cefuroxime anaphylaxis;
  iodinated-contrast reaction; propranolol allergy in a patient taking warfarin.
- The later phases give `followup_outputs`.

The limits:

- Results exist only for the tests the synthetic doctor ordered. Anything else must return
  "not available".
- There are no full vitals and no structured exam.
- n = 20, all outpatient chronic disease.

On the positive side, the personas carry rich private details (job, mortgage, family), which
narrative 2's privacy router needs. The licence is CC-BY-NC-SA-4.0 and the data are synthetic,
so cloud models may be used for the conversion.

### CPRD GOLD and MedLoCoMo access

Nothing changes without the neurology filter:

- **CPRD.** It is coded GP data. It does have dated tests and referrals, i.e. a real primary-care
  trajectory, but no narrative, exam, imaging or reports. The presentation would have to be
  written by an LLM from codes. Access is the blocker:
  - the real data need a licence fee and the offline CPRD Safe environment;
  - the synthetic sample needs a due-diligence check and a data-sharing agreement.

  The enclave is decisive (CPRD Safe features page, read 21 Oct 2026):
  - virtual machines have at most 8 CPUs and 256 GB of RAM, with no GPU and no internet, so the
    model panel could not run there at a useful speed;
  - only checked, non-disclosive outputs leave through the airlock (for example, counts under 10
    are flagged), so patient-level episodes could never be moved into our harness or released.
- **MedLoCoMo.** It has no licence, and it redistributes MIMIC-IV-Note. Its only unique asset
  after MIMIC access is the generated doctor–patient dialogue: a possible patient simulator, or a
  memory test.

## How to request access

**MIMIC-IV (PhysioNet), free.** Checked on physionet.org on 21 Oct 2026.

1. Create a PhysioNet account with an institutional e-mail (CERN or UPF) as the primary address.
2. Take the CITI course "Data or Specimens Only Research" (free):
   - register on citiprogram.org with the affiliation "Massachusetts Institute of Technology
     Affiliates", not as an independent learner (that costs money);
   - answer questions 1, 2 and 3 to get the course, and "Yes" to question 5 for the Conflicts of
     Interest module;
   - complete both modules; under Records → View-Print-Share, download the **completion report**,
     not the certificate.
3. Apply for credentialed access (PhysioNet → Settings → Credentialing). Describe the research
   and name a reference, normally the supervisor, who will be contacted and should answer
   quickly. Upload the CITI report (Settings → Training).
4. Once approved, sign the DUA on each project page: MIMIC-IV 3.1, MIMIC-IV-Note 2.2,
   MIMIC-IV-ED 2.2 and, for the first step, MIMIC-IV-Ext-CDM 1.1. MIMIC-IV-ECG is open and
   needs nothing.
5. Download onto CERN storage, with `wget -r -N -c -np --user <user> --ask-password
   https://physionet.org/files/mimiciv/3.1/`, and the same for the other projects.

Timing: the course takes a few hours (my estimate, not stated by CITI). The review time is not
published, and PhysioNet's notice of 18 June 2026 warns of significant delays from staffing
changes, handled in order of arrival. Users at institutions in the countries covered by the US
DOJ Data Security Program (China, Russia, Iran, North Korea, Cuba, Venezuela) are blocked, which
matters only for collaborators.

**CPRD GOLD, paid.** Checked on cprd.com on 21 Oct 2026.

1. **Organisation approval.** UPF (or CERN) fills in the "New client request" form with its Data
   Protection Officer and IT or governance office, signed by an authorised signatory. CPRD reviews
   it within 7 working days.
2. **Accounts.** Every researcher registers on CPRD Gateway and is approved for eRAP.
3. **Study protocol.** It is submitted on eRAP and must show public-health benefit. CPRD aims to
   give feedback within 4 weeks; resubmissions are allowed within 6 months.
4. **Licence.** A Single Study Licence (Standard) costs £20,600 for 12 months, excluding VAT.
   The licence agreement is signed by the sponsor.
5. **Training.** Compulsory training, and from 1 April 2027 ONS researcher accreditation.
6. **Work.** Only inside CPRD Safe, under the limits above.

The synthetic GOLD sample is free but still needs the organisation check and a data-sharing
agreement (application to enquiries@cprd.com).

## How the estimates were made

- **Episode counts** for the demo, MedLoCoMo and MedMemoryBench are measured by the scripts and,
  for the demo and the personas, read one by one. The full-MIMIC range (30,000–50,000) is an
  extrapolation of those rates to 331,794 discharge summaries; it is not a count.
- **Completeness** is the eight-field rubric above, scored by me from the tables and the files.
  It is a judgement, useful to rank the sources rather than as a measurement.
- **Work days** add up the listed steps, each sized from comparable work already in this
  repository: `mimic_to_neurobench.py` and the audits took part of one day, and the tool
  vocabulary changes earlier this year needed the mirror and test updates too. They assume the
  data are in hand and coding agents help. They do not include waiting for access or for a
  physician.
- **Calendar times** are work plus waiting. The waiting is the uncertain part: PhysioNet does not
  publish review times; CPRD publishes 7 working days for the organisation and 4 weeks for the
  protocol, plus contracting, which I estimate at a few weeks.

## What the adaptation costs

**Shared harness work (7–10 days, once).** The harness is less neurology-bound than it looks.
The system prompt is already generic, and the only enum is `NeurologicalCondition` in the case
schema and the review catalogue.

| Change | Days |
|---|---|
| Open the case schema: a `domain` and `source`, a free condition label, provenance | 1–2 |
| Render the general physical exam and history in `harness/context.py`, which today prints the neurological exam only | 0.5 |
| **General-medicine tool pack** in `costs.yaml` (see the list below), mirrored in `review_api/services/tool_io.py` and its test | 2–3 |
| **Reference reward mode** for external cases (see below) | 3–4 |

The tool pack adds what general medicine needs and the vocabulary lacks:

- imaging: chest and abdominal X-ray, DXA;
- procedures: endoscopy and colonoscopy, ABPM;
- biopsies beyond the nervous system;
- microbiology specimens: sputum, stool, wound, joint;
- prices for all of them.

The reference reward mode scores:

- the diagnosis;
- the cost;
- concordance with the real clinicians' orders (precision, recall, order);
- safety from documented allergies and contraindications.

For a real record, steps without a result return "not available", never the fallback library's
normal report. This mode is reportable without physician approval, because its reference is the
record. The approved-policy rule in CLAUDE.md stays for NeuroBench policies.

**MIMIC-IV own cohort (15–20 days after access):**

- staging on CERN storage and the domain-agnostic cohort: 1–2;
- the converter with notes: section parsing, radiology mapped by `exam_name`, lab items mapped to
  our panels: 4–5;
- a local-model step that strips results from the HPI and structures the reports, run on the
  panel models or CERN-hosted gateway models: 3–4, plus about 1–2 GPU days for ~10k cases;
- accepted-diagnosis label sets for the ICD codes in scope: 1–2;
- a hand audit of 100 cases by Andrea, who as a credentialed user may read them: 2–3;
- a pilot with the panel: 1–2.

**MIMIC-IV-Ext-CDM (4–6 days after access).** CDM is already sectioned: HPI, exam, labs with
names, microbiology, radiology findings, diagnoses and procedures. It needs mapping only. It is
keyed by `hadm_id`, so the real `poe` trajectory can be joined. It also gives a comparison with
the published numbers of Hager et al.

**MedMemoryBench (4–6 days, startable now):** extraction of the diagnostic window, results →
tool outputs, red herrings and traps → policy fields. Synthetic data, so a cloud model can do it.

**Completeness by field** (✔ 1, ◐ ½, ✗ 0):

| Field | MIMIC own | CDM | MedMemoryBench | MedLoCoMo | CPRD |
|---|---|---|---|---|---|
| Presentation narrative | ✔ HPI | ✔ | ✔ patient narrative | ✔ | ✗ codes only |
| Exam | ✔ admission exam | ✔ | ◐ fragments | ✔ | ✗ |
| Vitals | ✔ ED triage | ◐ in the exam text | ◐ some BP/HR | ◐ in the exam text | ◐ BP, BMI |
| Served results | ◐ labs, cultures, imaging, ECG; not EEG, echo text, endoscopy, pathology | ◐ labs, cultures, imaging findings | ◐ only tests performed | ◐ imaging, cultures; labs as text | ◐ labs only |
| Trajectory reference | ✔ timed `poe`, ED partly missing | ◐ via join | ◐ the doctor's path, errors included | ◐ radiology times only | ✔ dated tests and referrals |
| Final diagnosis | ✔ ICD + discharge diagnosis | ✔ | ✔ | ✔ | ✔ code |
| Differential or red herrings | ✗ | ✗ | ✔ wrong attributions | ✗ | ✗ |
| Safety constraints | ◐ allergies, medications | ◐ | ✔ 6 traps per persona | ◐ | ◐ |
| **Score** | **≈75 %** | **≈65 %** | **≈65 %** | **≈60 %** | **≈35 %** |

## Is the adaptation a contribution?

**Turning MIMIC into an interactive diagnostic environment is not new by itself.** At least five
works already did it:

- MIMIC-IV-Ext-CDM: 2,400 cases, *Nature Medicine* 2024.
- AgentClinic-MIMIC: 200 encounters, *npj Digital Medicine* 2026.
- DiagGym / DiagBench: 2.2k cases with physician rubrics, built on MIMIC with an EHR world model
  that generates results; arXiv, Oct 2025.
- CDPR: cost-aware RL on 23k MIMIC-IV cases; arXiv, Jun 2026.
- Cros: risk-constrained stopping, 1,834 MIMIC-IV-ED abdominal episodes; arXiv, Sep 2026.

Outside MIMIC, SDBench turns 304 NEJM cases into cost-scored sequential diagnosis (Microsoft,
2025).

What the adaptation can add, and what I did not find in that set:

1. **Executable typed policies on real records**: required, avoided and sequence criteria with
   safety caps, checked deterministically. The others use accuracy, cost, F1 against the orders,
   or LLM-judged rubrics; DiagBench's rubrics are the closest.
2. **Two references side by side**: the guideline policy and the clinicians' real, timed
   trajectory. This shows where agents, guidelines and practice disagree.
3. **One harness, one transcript codec, three provenances**: synthetic NeuroBench, real MIMIC,
   and synthetic longitudinal MedMemoryBench. Training on one and testing on another is then a
   controlled generalisation study.
4. For narrative 2, **costly and sensitive information on the same episodes**:
   - real prices per study and a budget as input;
   - clinically sensitive facts marked per step (HIV status, psychiatric history, substance use,
     the family details of MedMemoryBench), so a local/cloud router can be scored on exposure.

   A quick search found privacy benchmarks for medical QA (MedPriv-Bench) and for edge–cloud
   memory (MemPrivacy), but none on multi-step clinical diagnostic episodes. This needs a proper
   search before it is claimed.

Sources: [MIMIC-IV-Ext-CDM](https://physionet.org/content/mimic-iv-ext-cdm/1.1/),
[AgentClinic](https://www.nature.com/articles/s41746-026-02674-7),
[DiagGym](https://arxiv.org/abs/2510.24654), [CDPR](https://arxiv.org/abs/2608.28599),
[Cros](https://arxiv.org/abs/2609.09678), [SDBench](https://arxiv.org/abs/2506.22405),
[MedPriv-Bench](https://arxiv.org/abs/2603.14265), [MemPrivacy](https://arxiv.org/abs/2605.09530).
Abstracts read for DiagGym, CDPR and Cros; the others from their pages or search results only.

Points 1 and 4 are the defensible contribution. The conversion alone, or only accuracy and cost,
would be incremental.

## Recommended order

1. **Now, no access needed.** The shared harness work, plus MedMemoryBench as the first external
   source: about 2 weeks. It is the testbed for the format change, and for the privacy marking.
2. **In parallel, today.** Andrea applies for PhysioNet credentialing (CITI course, reference,
   DUA for MIMIC-IV, Note and ED; see "How to request access"). The wait is the critical path:
   PhysioNet announced significant review delays on 18 June 2026, so no date can be promised.
3. **After access.** CDM first (4–6 days, comparable with published results), then the
   cross-specialty MIMIC cohort (3–4 weeks), with the sensitive-fact marking done by a local model.
4. **Not to pursue.** CPRD; and MedLoCoMo unless its authors add a licence.

# Part 2: first pass, neurology only

| Dataset | Downloaded | Unit checked | Neuro cases usable as diagnostic episodes | Verdict for neurology |
|---|---|---|---|---|
| MIMIC-IV (+ Note, ED, ECG) | Open demo (100 patients) and MIMIC-IV-ECG tables | 39 demo admissions with a neuro diagnosis in the first two positions; 2 converted end to end | ≈6 in the demo; estimated 2,000–6,000 in the full database | Yes, as a second, real-world split |
| MedLoCoMo | Full repository (101 patients, 2,982 admissions) | All 2,982 admissions, structural checks only | 20 (11 in our 20 conditions) | No |
| MedMemoryBench | Full HF dataset (EN + ZH) | All 20 personas | 2 (PD, AD), each with a thin work-up | No |
| CPRD GOLD | Not possible | Data specification and access pages | 0 | No |

## MIMIC-IV

### What each tool can be served from

| NeuroBench tool | Source in MIMIC-IV | Status |
|---|---|---|
| `interpret_labs` | `hosp/labevents` (first instance per test, as in CDM) | Real, structured |
| `analyze_csf` | `labevents` with fluid = CSF, plus CSF `microbiologyevents` | Real, structured. No opening pressure; some values are masked (`___`) by de-identification |
| `order_microbiology` | `hosp/microbiologyevents` | Real, structured |
| `analyze_ecg` | MIMIC-IV-ECG `machine_measurements` (open access, machine reading, 800k ECGs) | Real, but read by the machine, not by a cardiologist |
| `order_ct_scan`, `analyze_brain_mri`, `order_advanced_imaging`, `order_body_imaging` | MIMIC-IV-Note `radiology` (2.3 M reports) with the exam name in `radiology_detail` | Real text, credentialed. Needs structuring into our report models |
| `perform_clinical_assessment` | Admission exam in the discharge summary; GCS, pupils and strength charted in `icu/chartevents` | Real text, credentialed |
| `order_echocardiogram` | MIMIC-IV-Echo structured measurements (4,572 patients); otherwise text in the discharge summary | Partial |
| `analyze_eeg` | **Only the order** (`poe` Neurology/EEG). No EEG reports in any module | Missing. Can only be extracted from the hospital-course text |
| `order_cardiac_monitoring`, `order_specialized_test` (EMG), `obtain_tissue_diagnosis` | Orders only; no telemetry, EMG or pathology reports | Missing |
| `check_drug_interactions`, `search_medical_literature` | Knowledge tools; home medications from `ed/medrecon` | Not patient data |

The gap that matters is the **EEG**. Every seizure and encephalopathy condition (SE, FEPI, NMDAR,
HEP) has an EEG step in its policy. A real EEG result exists only as a sentence in the discharge
summary.

### Case-by-case: the demo

Audit: `agent-platform/scripts/external_datasets/mimic_demo_audit.py` →
`outputs/external_datasets/mimic_demo.csv` (one row per admission).

- 275 admissions. 97 carry a neuro code anywhere, 28 have it as the principal diagnosis and 39
  in the first two positions.
- Of the 39: 25 came through ED triage, 28 have GCS charted in the ICU, 4 have CSF labs and 12
  have an EEG order. CT was ordered in 27, MRI in 16, ECG in 12 and echo in 12.
- **Leakage at presentation.** In 8 of the 25 triaged admissions the chief complaint names the
  diagnosis: "SDH/SAH", "HEAD BLEED" twice, "ICH", "Transfer, CVA", "Headache, SAH, Transfer",
  "s/p Fall, SDH" and "Transfer, MVC". BIDMC is a tertiary centre, and many acute neuro
  admissions are transfers whose diagnosis is already made. They have to be filtered, as CDM
  did by dropping cases whose HPI named the pathology.
- About 6 demo admissions are usable diagnostic episodes in our conditions: 2 ISCH, SE, 2 SYNC
  and FND (dizziness and diplopia, CT and two MRIs, discharged as conversion disorder, a good
  puzzle). The rest are not in our 20 conditions (SDH, aneurysm, abscess, toxic encephalopathy),
  are transfers, or carry the neuro code only as a comorbidity.

### Prototype conversion

`agent-platform/scripts/external_datasets/mimic_to_neurobench.py` takes one admission and writes
a NeuroBench v2 case plus a gap report. The policy is transferred from a NeuroBench case of the
same condition and stays `draft`; the clinicians' real orders are stored as a reference
trajectory. Both demo cases **validate against `NeuroBenchCase`**:
`outputs/external_datasets/cases/MIMIC-ISCH-22484749.json` and `MIMIC-SE-25809882.json`.

**MIMIC-ISCH-22484749**: 70-year-old woman, walk-in, "L weakness, unable to ambulate", BP
165/79. The real trajectory, timed from ED arrival:

| Time from ED arrival | Orders |
|---|---|
| 1.6 h | labs and chest X-ray |
| 1.8 h | three CTs, most likely NCCT plus CTA head and neck; the exam names are in the Note module |
| 4.5 h | MRI |
| 9 h | echo and telemetry |
| 15.8 h | repeat MRI |
| 40 h | carotid duplex |

This is close to the AHA pathway in our ISCH policy. The ECG is served from MIMIC-IV-ECG (sinus,
PVC, LVH). Of the five data tools the policy requires, two already have a real result in the demo
(labs, ECG). Two more come with the Note module (both CT criteria). Echo is partial and telemetry
has no result.

**MIMIC-SE-25809882**: 60-year-old woman, triage complaint "SEIZURE", triage vitals not recorded.
The real trajectory:

| Time from ED arrival | Orders |
|---|---|
| 0.2 h | CT |
| 0.5 h | labs |
| 4.1 h | EEG order |
| 17 h | ECG |
| 3.5 d | MRI |

The CSF shows protein 75 and glucose 66 mg/dL, 52 % lymphocytes, negative cultures; the nucleated
cell count is masked by de-identification. Blood, urine and sputum cultures grew *S. aureus*. Of
the policy's required data tools, labs, CSF and microbiology have real results. CT, MRI and chest
imaging need the Note module, and **EEG has none anywhere**.

What the prototype shows:

- The structured part works today.
- The narrative part (HPI, exam, imaging) needs the Note module.
- A required step without a real result must return "not available". It must not get the
  fallback library's normal report, which would be wrong for a real patient (a normal EEG for
  status epilepticus).

### Expected yield in the full database (estimate, not counted)

MIMIC-IV-Note has 331,794 discharge summaries. Two of our measurements bound the share of
usable cases, meaning a neuro principal diagnosis that is new to the patient and has an HPI, a
neuro exam and results:

- 0.7 % in MedLoCoMo: 20 of 2,982 admissions, a chronic, hepatology-heavy cohort;
- about 2 % in the demo: about 6 of 275, a cohort where every patient has an ICU stay.

That gives **about 2,000–6,000 candidate cases**. They are concentrated in the conditions acute
care sees: ISCH, SAH, SE/FEPI, SYNC, HEP, BACT, MIG and GLIO. MS, GBS, MG and NPH should be in
the tens to low hundreds. ALS, FTD, ALZ, PD and VASC will mostly appear as admissions for
complications of a known disease, so they will be scarce as diagnostic cases. NMDAR will be very
rare.

`agent-platform/scripts/external_datasets/mimic_cohort.py` gives the exact numbers per condition
and per filter on the first day of access. It reads the compressed CSVs with DuckDB and was
tested on the demo.

### How cases would be scored

- **Final answer.** The principal ICD code plus the discharge diagnosis text feed our
  `DiagnosisCriterion`, with labels from `diagnosis_synonyms.yaml`. The source has no
  differential; it can be drafted from the condition packs and reviewed.
- **Trajectory, two complementary references.**
  1. The NeuroBench condition policy, transferred and reviewed, scored with the existing reward,
     with unserved steps returning "not available".
  2. Concordance with what the clinicians actually ordered (`poe`, timestamped): precision,
     recall and order, as in Hager et al.

  The second needs no review, but it is noisy:
  - `poe` misses ED orders: the stroke ECG exists in MIMIC-IV-ECG but not in `poe`;
  - it bundles routine order sets;
  - real practice is not always guideline practice.
- **Leakage controls.**
  - Drop transfers, and chief complaints that name the diagnosis.
  - The HPI is written after the work-up (for example "In the ED, CT showed…"), so ED results
    must be removed from it.
  - Decide whether imaging tools return the radiologist's impression or, like CDM, only the
    findings section.

### Access and governance

- **Credentialing.** MIMIC-IV, Note and ED are credentialed; see "How to request access" in
  Part 1. Andrea has to apply in person.
  MIMIC-IV-ECG and the demos are open.
- **LLM processing.** PhysioNet's notice of 24 Sept 2025 says that sending credentialed data
  through an API breaks the DUA unless the service keeps no data, does not train on it and has
  no human review; locally deployed models are "strongly recommended". Structuring HPI, exams and
  reports must therefore run on our vLLM panel or on CERN-hosted gateway models, not on the
  gateway's Vertex models. It must also not run through Claude or Codex sessions unless a
  zero-retention agreement is verified. This audit never read MIMIC note text: MedLoCoMo was
  checked with scripts that print counts only.
- **Release.** A derived benchmark can be released only on PhysioNet, under the same credentialed
  licence, as MIMIC-IV-Ext-CDM was. The paper would then have an open synthetic NeuroBench (600)
  and a credentialed real-world split (MIMIC-NeuroBench).

## MedLoCoMo

Audit: `agent-platform/scripts/external_datasets/medlocomo_audit.py` →
`outputs/external_datasets/medlocomo.csv`, one row per admission (2,982).

- Each admission packet holds the MIMIC-IV-Note discharge summary, the radiology reports, ICD
  diagnoses and procedures, and microbiology. **It has no lab table**: labs exist only as text
  pasted into "Pertinent Results".
- **Neuro coverage.**
  - 74 admissions (46 patients) have a neuro principal diagnosis, 45 of them in one of our
    conditions: SYNC 13, MIG 12, FEPI 11, ISCH 5, HEP 2, SE 1, MS 1.
  - Many repeat a known diagnosis. Only 33 are new to the patient.
  - 20 of those 33 also have an HPI over 200 characters, neuro exam lines and results. 11 of the
    20 are in our 20 conditions: SYNC 5, ISCH 3, and one each of FEPI, MIG and SE.
  - 12 of the 20 have a head or spine imaging report, and 6 already state results in the HPI.
- **Studies mentioned** in the 74 notes: EEG in 14, CSF in 13, ECG in 34, echo in 16, EMG in 0.
- **Blockers.**
  - The repository has no licence.
  - It republishes credentialed MIMIC-IV-Note text.
  - Its generation pipeline defaults to the OpenAI API, and the release does not say which model
    produced the dialogues.

  Everything useful in it comes from MIMIC-IV-Note, which we can get under the DUA ourselves.

## MedMemoryBench

Audit: `agent-platform/scripts/external_datasets/medmemorybench_audit.py` →
`outputs/external_datasets/medmemorybench.csv`, one row per persona (20).

- These are synthetic one-year chronic-care chats, built for memory questions (1,939 queries).
  For each persona, the audit isolates the diagnostic window before the first treatment and
  lists the studies in it.
- **Persona 7, Parkinson's disease, tremor-dominant.**
  - The patient is 34. That is young-onset, which would call for a genetic and Wilson
    work-up; the persona has neither.
  - Before rasagiline the only study is a UPDRS-III of 22. The DAT-SPECT is recommended and then
    postponed, so it has no result.
- **Persona 8, Alzheimer's disease.** MMSE 27, MoCA 24, MRI with hippocampal volume loss, and CSF
  with Aβ42 654 pg/mL, Aβ42/40 0.083 and p-tau181 21 pg/mL. This one could become a thin
  outpatient case.
- **The other 18 personas.** Depression and anxiety are psychiatric. None of the others is
  neurological.
- **Format.** The results are narrated by the patient in the chat, not returned by a tool. There
  are no vitals, no structured exam and no differential. The licence is CC-BY-NC-SA-4.0.

## CPRD GOLD

- **Not downloadable.** The real data need a licence and a study protocol. CPRD's pricing page
  (read 21 Oct 2026) lists the Standard Single Study Licence at £20,600 for 12 months, with work
  only inside the offline CPRD Safe environment.
- **The synthetic "GOLD sample" too.** It requires an organisational due-diligence check, an
  application to enquiries@cprd.com and a signed data-sharing agreement (free). Checked on the
  CPRD synthetic-data page, 21 Oct 2026.
- **Content.** It is the blocker even with access. Data specification v2.9 describes coded GP
  records only, with no free text since v2.0: symptoms and diagnoses as Read/SNOMED codes, test
  values, prescriptions, referrals without letters. There is no presentation narrative,
  neurological exam, imaging, EEG or CSF report, and no hospital work-up. It suits a different
  task, prediction over primary-care timelines.

## Next steps (neurology-only pass, superseded by "Recommended order")

1. Andrea applies for PhysioNet credentialed access: CITI course, reference, then the DUA for
   MIMIC-IV, MIMIC-IV-Note and MIMIC-IV-ED.
2. Download them to CERN storage, not to this Mac, and run `mimic_cohort.py` for the exact
   counts per condition.
3. Extend the converter with the Note module:
   - section parsing of HPI and exam (code already in `mimic_neuro.py`);
   - radiology reports mapped by `exam_name`;
   - a local-model step that removes results from the HPI and structures the reports into our
     Pydantic models.
4. Decide three design points:
   - impression versus findings-only for imaging tools;
   - "not available" versus extracted text for EEG and telemetry;
   - how the transferred condition policy is reviewed (a sample per condition, by the same
     physicians).
5. Pilot 20 cases per frequent condition (ISCH, SAH, SE, SYNC, HEP, BACT) through the harness
   with the panel models, and compare scores with the synthetic split.

## Reproduce

```bash
# Raw downloads live in data/external/ (gitignored): hf download, git clone, wget from physionet.org/files/<project>/<version>/
uv run --no-project --with pandas --with pyarrow python -I agent-platform/scripts/external_datasets/medmemorybench_audit.py data/external/medmemorybench/data/en outputs/external_datasets/medmemorybench.csv
uv run --no-project --with pandas python -I agent-platform/scripts/external_datasets/general_audit.py data/external outputs/external_datasets
python3 -I agent-platform/scripts/external_datasets/medlocomo_audit.py data/external/medlocomo/repo/MedLoCoMo outputs/external_datasets/medlocomo.csv
uv run --no-project --with pandas python -I agent-platform/scripts/external_datasets/mimic_demo_audit.py data/external outputs/external_datasets/mimic_demo.csv
uv run --no-project --with duckdb --with pandas python -I agent-platform/scripts/external_datasets/mimic_cohort.py --hosp data/external/mimic-iv-demo/hosp --ed data/external/mimic-iv-ed-demo/ed
uv run --no-project --with pandas python -I agent-platform/scripts/external_datasets/mimic_to_neurobench.py --root data/external --hadm 22484749 --template data/neurobench/cases/ISCH-STR-M01.json --out outputs/external_datasets/cases
```

Run from the repository root. On the full database, `mimic_cohort.py` also takes `--note` and
`--ecg`, and `mimic_to_neurobench.py` takes `--notes` and `--full`.
