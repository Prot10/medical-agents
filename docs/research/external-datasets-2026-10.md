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

**Status, 28 Oct 2026.** Andrea's account (`aprotani`) was credentialed on 27 Oct 2026 without
any training on file: today credentialing and training are separate reviews, and the files stay
locked until the CITI report is accepted. The four DUAs (all Credentialed Health DUA 1.5.0) are
signed; the "Sign DUA" page keeps showing the form until training is approved, which looks like
an unsaved signature but is not (Settings → Agreements lists them). CITI: enrolled under MIT
Affiliates (the UPF affiliation on the same CITI account has no "Data or Specimens Only
Research" course); both courses passed on 28 Oct 2026 and the completion report was submitted
the same day (PhysioNet: "Under review"), with the CITI login e-mail (UPF) added and verified
on the PhysioNet account. The data go to `/eos/user/a/aprotani/physionet` (mode 700; only the CERN backup
service `cback` has read access), not to `/eos/project-d/diagbox`, which the diagbox group can
read. Download with `agent-platform/scripts/external_datasets/physionet_download.sh aprotani` on
lxplus. **Update, 5 Nov 2026:** training approved; downloaded as HTCondor jobs
(`physionet_download.sub`, one per folder) because tmux on lxplus dies with the SSH login. Note,
ED and CDM are complete with checksums OK; MIMIC-IV hosp and icu were still downloading that
night (≈0.37 MB/s each). See Part 3.

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

# Part 3: first look at the full data (5 Nov 2026)

What was on EOS that evening: MIMIC-IV-Note 2.2, MIMIC-IV-ED 2.2 and MIMIC-IV-Ext-CDM 1.1,
complete and checksum-verified; MIMIC-IV 3.1 hosp up to `hcpcsevents` (plus `admissions`,
`diagnoses_icd`, the dictionaries) and icu up to `caregiver`. `labevents`, `poe`,
`microbiologyevents`, `patients`, `prescriptions` and `chartevents` were still downloading, so the
CSF, EEG-order, lab and trajectory numbers below are still to come.

Every number here comes from scripts run on lxplus that print counts, shares and medians only;
no row or note text left EOS (PhysioNet DUA, see "Access and governance").

## What the tables hold

| Table | Rows | Unit | What it gives a case |
|---|---|---|---|
| `hosp/admissions` | 546,028 | admission (223,452 patients) | arrival (`admission_location`, `edregtime`), type, outcome |
| `hosp/diagnoses_icd` | 6.36 M | coded diagnosis, `seq_num` 1 = principal | the final diagnosis and comorbidities |
| `note/discharge` | 331,793 | one per admission (61 % of admissions) | HPI, exam, results, course, discharge diagnosis; median 9,847 characters |
| `note/radiology` | 2.32 M (49 % with an `hadm_id`) | report | imaging tools; `radiology_detail` gives `exam_name` |
| `ed/edstays`, `ed/triage` | 425,087 | ED stay (48 % lead to an admission) | chief complaint, triage vitals and acuity |
| `ed/vitalsign`, `ed/medrecon`, `ed/pyxis` | 1.6 M, 3.0 M, 1.6 M | timed rows | repeat vitals, home medications, ED drugs given |
| CDM, 10 tables | 2,400 admissions | admission | see below |

## MIMIC-IV-Ext-CDM: mapping only

CDM is 2,400 abdominal admissions: appendicitis 957, cholecystitis 648, pancreatitis 538,
diverticulitis 257 (`pathology_ids.json`). Each has one HPI (median 832 characters), one
physical exam (median 347), a discharge diagnosis, ICD codes (median 5), labs (median 56 items),
microbiology (median 2 rows) and radiology reports (median 2; 5,960 in all).

| CDM table | NeuroBench field or tool | Note |
|---|---|---|
| `history_of_present_illness` | `patient.history_present_illness` | CDM already removed cases whose HPI names the pathology |
| `physical_examination` | `patient.physical_exam` (general, not the neuro exam) | vitals are inside this text; triage vitals can be joined from ED by `hadm_id` |
| `laboratory_tests` + `lab_test_mapping` | `interpret_labs`: CBC, BMP/CMP, LFT, `lipase` (pack), urinalysis | blood in 2,400, urine in 1,982 admissions; other fluids in < 35 |
| `microbiology` | `order_microbiology`: blood culture, urine | ids only; names come from hosp `microbiologyevents` |
| `radiology_reports`: CT abdomen/pelvis (1,622 admissions) | `order_body_imaging` `pelvis_abdomen_CT` | |
| RUQ / gallbladder ultrasound (≈950) | pack `hepatobiliary_ultrasound` | |
| chest X-ray (855), abdominal X-ray (258) | `chest_xray`, pack `abdomen_xray` | |
| MRCP (220) | `pelvis_abdomen_MRI` | MRCP as a protocol is missing |
| ERCP (93) | **missing** | a procedure; add to `order_specialized_test` in the pack |
| CT head (59), MRI head (11) | `order_ct_scan`, `analyze_brain_mri` | |
| `discharge_diagnosis`, `icd_diagnosis` | `ground_truth.diagnosis` | four labels; synonyms per pathology |
| — | demographics | not in CDM: join `hosp/patients` by `hadm_id` (still downloading) |
| — | trajectory | not in CDM: join `poe` by `hadm_id` |

**Blocking gap:** `NeuroBenchCase.condition` is the neurological enum, so a
`domain: general_medicine` case cannot name appendicitis. The schema needs a condition label for
general-medicine cases (an enum of the four CDM pathologies, or a free label with an ICD code)
before the first CDM case validates.

## MIMIC-IV neurology: the real counts

`mimic_cohort.py` on the full database, after fixing the seizure codes (below). Each filter
column counts the principal-diagnosis admissions passing that filter alone; the usable cohort is
their intersection, computed once `poe` and `labevents` are in.

| Condition | Principal dx | New, not a transfer | Via ED | Discharge note | Head imaging report |
|---|---|---|---|---|---|
| ISCH | 6,216 | 4,120 | 3,221 | 4,588 | 4,471 |
| SYNC (R55, any cause) | 4,327 | 3,536 | 2,191 | 2,478 | 1,529 |
| GLIO | 1,127 | 539 | 390 | 788 | 769 |
| SAH | 989 | 656 | 495 | 742 | 730 |
| MIG | 971 | 664 | 490 | 711 | 581 |
| FEPI (focal only) | 952 | 512 | 327 | 763 | 337 |
| HEP | 568 | 208 | 283 | 537 | 219 |
| MS | 455 | 249 | 208 | 352 | 256 |
| SE | 411 | 223 | 215 | 279 | 221 |
| PD | 392 | 191 | 114 | 241 | 186 |
| ALZ | 328 | 200 | 155 | 199 | 152 |
| GBS | 218 | 157 | 105 | 163 | 115 |
| FND | 216 | 140 | 92 | 135 | 81 |
| MG | 191 | 92 | 91 | 138 | 46 |
| NPH | 153 | 97 | 22 | 119 | 114 |
| VASC | 123 | 76 | 51 | 82 | 52 |
| ALS | 77 | 45 | 30 | 58 | 21 |
| BACT | 74 | 48 | 30 | 66 | 53 |
| NMDAR | 61 | 31 | 17 | 30 | 23 |
| FTD | 54 | 41 | 27 | 43 | 31 |

Neurological but outside the 20: traumatic bleeds 4,415, other cerebrovascular 3,791, ICH 3,269,
generalized or unspecified epilepsy 2,474, encephalopathy 2,184, TIA 1,130, convulsions that are
not epilepsy 995, CNS infection 637, other dementia 567.

The estimate of Part 2 (2,000–6,000 candidate cases) holds: the 20 conditions give 17,900
principal admissions, 11,800 of them new and not transfers. Half of that is ISCH and SYNC; ALS,
BACT, NMDAR and FTD have fewer than 50 each before the note and leakage filters.

**Three mapping problems found and what was done:**

- **Status epilepticus was undercounted.** US ICD-10-CM has no G41; it codes "epilepsy with
  status epilepticus" as a six-character G40 code ending in 1 (259 admissions), and ICD-9 345.2
  was missing. Fixed in `mimic_neuro.py`: SE 150 → 411.
- **FEPI held every seizure.** All G40/345 codes and the R56/780.3 convulsions (995, mostly
  provoked or unexplained seizures) counted as focal temporal epilepsy. Fixed: FEPI keeps
  localization-related codes only (G40.0–G40.2, 345.4–345.5), 4,682 → 952; generalized and
  unspecified epilepsy is a separate group, from which the converter could recover focal cases by
  reading the EEG and MRI in the note.
- **SYNC is not cardiac syncope.** R55 as principal is syncope of any or unknown cause. Cardiac
  syncope is better found as a principal arrhythmia or structural cause with syncope as a
  secondary code: ≈660 admissions (conduction/arrhythmia 472, AF/flutter 89, aortic stenosis
  82, cardiomyopathy 21; ICD-9 AF partly falls in the first group). Not yet in `mimic_neuro.py`:
  it changes what SYNC means and needs Andrea's decision.

## What the discharge notes give

`mimic_note_sections.py`, share of discharge summaries carrying each section:

| | All notes | Neuro range across the 20 |
|---|---|---|
| Chief complaint, HPI, PMH, allergies | 96–100 % | 91–100 % |
| Physical exam | 95.6 % | 89–99 % |
| Pertinent results | 96.2 % | 97–100 % |
| Discharge diagnosis | 95.9 % | 88–100 % |
| HPI median length | 1,255 characters | 598 (SAH) – 2,378 (FND) |

Structure is not the problem. Two things are:

1. **The HPI often tells the result.** A study named with a finding verb ("CT showed…",
   "LP revealed…") appears in 22 % of all HPIs and in 13–50 % of neuro ones: SAH 49 %, BACT 50 %,
   GLIO 44 %, NMDAR 43 %, ISCH 35 %. And 13–66 % mention the ED or an outside hospital
   (SYNC 66 %, ALZ 66 %, HEP 64 %, BACT 64 %). The conversion must cut the HPI at the
   presentation, with a local model, and a sample must be checked by Andrea.
2. **EEG, LP and EMG results exist as text only.** The hospital course mentions an EEG in 77 % of
   SE, 64 % of FEPI, 62 % of FND and 37 % of NMDAR notes; an LP in 77 % of BACT, 68 % of GBS, 63 %
   of NMDAR and 40 % of NPH; an EMG in 44 % of GBS, 36 % of ALS and 21 % of MG. So for most
   seizure, encephalitis and neuromuscular cases the result of the tool that defines the policy
   can be extracted from the course; without that, those cases cannot be scored on the policy.

## How to process the data: the pipeline

1. **Cohort (SQL, DuckDB, counts only).** Principal diagnosis in the 20 conditions with the
   fixed map; new to the patient; not a transfer; with a discharge note; a triage chief complaint
   that does not name the diagnosis (the regex of the demo audit).
2. **Presentation (deterministic).** Demographics from `patients`/`admissions`; chief complaint
   and vitals from ED triage; PMH, medications on admission, allergies, social and family history
   from the note sections; the *admission* exam (the note's exam section holds admission and
   discharge exams), split into `neurological_exam` fields where the headings allow.
3. **Presentation (local model).** Cut the HPI at presentation: remove ED course, outside
   results and anything a tool would return. Runs on vLLM at CERN; the output records what was
   removed, for audit.
4. **Tool outputs (`provenance: record`).**
   - `interpret_labs`, `analyze_csf`: first value per test from `labevents`, mapped item → panel
     with a table like CDM's `lab_test_mapping` (to be built for our panel names).
   - `order_microbiology`: `microbiologyevents`.
   - Imaging tools: radiology reports routed by `exam_name` to the tool and protocol; decide
     findings only (CDM) or findings plus impression.
   - `analyze_ecg`: MIMIC-IV-ECG machine measurements.
   - `analyze_eeg`, LP narrative, `emg_ncs`, echo: extracted from the hospital course by the local
     model, marked as extracted text.
   - Everything else: "not available", never a library normal.
5. **References.** Diagnosis from the principal ICD code plus the discharge diagnosis, labels from
   `diagnosis_synonyms.yaml`; the real trajectory from `poe` (+ ED); the condition policy
   transferred as `draft`.
6. **Checks before use.** Every case validates against `NeuroBenchCase`; Andrea hand-audits 100
   (presentation leakage, wrong tool routing); a pilot with the panel.

CDM follows the same steps 2, 4 and 5 with no local model, once the condition label exists.

## Decisions needed

1. The condition label for general-medicine cases (blocks CDM).
2. What SYNC means in MIMIC: R55 of any cause (≈4,300, mostly not cardiac) or cardiac syncope by
   cause (≈660).
3. Whether extracted text counts as a tool result (EEG, LP, EMG, echo), or those cases are left
   out of the policy score.
4. Findings only or findings plus impression for imaging.

**Update, 6 Nov 2026: download complete** (hosp 22 files 5.9 GB, icu 9 files 4.1 GB, all
checksums OK). CSF labs and EEG orders (`poe`) per condition, admissions with a principal
diagnosis:

| Condition | EEG ordered | CSF labs |
|---|---|---|
| SE | 339 of 411 (82 %) | 100 (24 %) |
| FEPI | 696 of 952 (73 %) | 52 (5 %) |
| FND | 129 of 216 (60 %) | 9 |
| NMDAR | 34 of 61 (56 %) | 32 (52 %) |
| BACT | 29 of 74 | 41 (55 %) |
| GBS | 9 of 218 | 110 (50 %) |
| SAH | 250 of 989 | 253 (26 %) |
| NPH | 8 of 153 | 47 (31 %) |
| MS | 25 of 455 | 95 (21 %) |
| ISCH | 881 of 6,216 | 138 |

The EEG is ordered in most seizure cases, so the policy step was really taken; its result is
still text only (see above). CSF has structured values where the policy needs it (BACT, GBS,
NMDAR, SAH).

## Next

- The intersection of the filters per condition.
- Lab item → panel table for our `interpret_labs` and `analyze_csf` vocabulary.
- `poe` trajectory coverage per condition, and GCS/strength in `chartevents`.

# Part 4: how SDBench turned MIMIC into interactive cases (6 Nov 2026)

The Science version of SDBench (Nori et al., *Science* 394:423, 22 Oct 2026) adds MIMIC to the
304 NEJM cases. Sources read: the public repository `microsoft/sdbench` (commit `304ce96`, 21
Oct 2026: `case_data.py`, the MIMIC gatekeeper prompt `gatekeeper_synthetic_tests/v13_mimic`),
the PhysioNet page of MIMIC-IV-Ext-SDBench 1.0.0, and the arXiv v2 preprint. The Science full
text was paywalled; its physician numbers (56 physicians, 36.1 % on NEJM, 46.8 % on ED cases)
come from a third-party summary and are unverified.

## What they built

- **488 cases** from MIMIC-IV 3.1 + ED 2.2 + Note 2.2: ED-originated admissions, no direct-to-ICU
  admissions, one note per patient. Split 163 train / 254 validation / 71 test; the 71 test cases
  were reviewed by clinicians, who corrected 13 ground-truth diagnoses (18 %). Published results
  use validation + test (325 cases): GPT-5 baseline 76.6 % at ≈$4,240, DxO without budget 80.3 %
  at ≈$4,980.
- **LLM curation**: Claude Opus 4.1 screened cases (clear presenting complaint, key findings,
  definitive diagnosis) and extracted the ground-truth diagnosis; GPT-5 mini wrote the
  diagnosis-free vignette and extracted test names and the number of clinician visits. Calls go
  to zero-retention providers, citing PhysioNet's LLM guidance.
- **Schema**: one JSON object per case: `case_id`, `mimic_note_id`, `final_diagnosis`,
  `case_title`, `case_summary` (the vignette), `full_text` (the **whole discharge summary**),
  `estimated_clinician_visits`, `tests` (names only), `case_sets`.
- **No structured MIMIC tables at run time.** The agent asks free-text questions and orders tests;
  a **gatekeeper LLM reads the discharge summary** (and knows the diagnosis) and answers each
  request. Its MIMIC prompt sets the rules:
  - answer as if the patient were still in hospital: nothing about the course, discharge,
    outcome or definitive surgery;
  - give **pre-intervention** values; when the note only has post-treatment values, reconstruct a
    plausible baseline;
  - imaging: **objective findings only, never the radiologist's impression**;
  - a test not in the note gets a **synthetic result**, "boring is better": normal or mildly
    non-specific for screening tests; confirmatory tests positive only for conditions documented
    in the note (diagnosis, history), negative for everything else, and never more specific than
    the documentation; a documented negative is never contradicted;
  - re-ordering a test returns the identical report; vague or umbrella orders are refused;
  - every answer is tagged `is_synthetic`, hidden from the agent.
- **Why synthetic and not "not available"** (preprint, Sec. 2): they started with "not
  available" and found that it told the agent its order was off the clinicians' path. A physician
  panel reviewed 508 gatekeeper answers, real and synthetic, and flagged 8; none leaked the
  diagnosis.
- Cost: CPT lookup by an LLM against a public chargemaster (Kaiser Permanente Washington), $300
  per visit of questions. Judge: o3 with a 5-point physician rubric, ≥4 correct.

## What it means for us

| | SDBench MIMIC | NeuroAgent on MIMIC (proposed) |
|---|---|---|
| Source of answers | the discharge summary, read live by an LLM | the structured tables (labs, micro, radiology, ECG, triage) compiled offline; the note only for what has no table (EEG, LP narrative, EMG, echo) |
| Timing | reconstructed by the gatekeeper | real: `charttime` and `poe` give the value before treatment and the order times |
| Actions | free text, any test name | typed tool calls over a closed vocabulary |
| Off-path orders | synthetic, generated live | **to decide**: today "not available"; proposed: synthetic, generated **offline** for every vocabulary item with the same rules, stored in the case, tagged, spot-checked |
| Determinism | LLM at every step | a lookup: the same order always gives the same answer, so GRPO rollouts cost nothing extra and runs replicate |
| Reference | diagnosis only (+ cost) | diagnosis, the transferred policy, and the clinicians' timed trajectory |

Our closed vocabulary is what makes the offline route possible: a case can hold an answer for
every orderable item, written once, checked once, then served deterministically. SDBench needs a
live gatekeeper because its agents may order anything in free text.

**The design point this changes.** The harness answers an unrecorded order on a
`provenance: record` case with "not available", and the case schema forbids authored fallbacks
on recorded cases. SDBench measured that this tells the agent which orders the clinicians did
not place. Options: (a) keep "not available" and report it as a known leak; (b) precompute
tagged synthetic results under SDBench's rules, served like a fallback but flagged, excluded
from any claim about real data, and checked by a physician on a sample.

The 488 SDBench cases are also a ready comparison: signing the MIMIC-IV-Ext-SDBench DUA gives
their `mimic_note_id`s, which map to `hadm_id`, so we can count how many fall in our conditions
and run our agents on the same admissions.

## Overlap with SDBench (6 Nov 2026)

MIMIC-IV-Ext-SDBench 1.0.0 is on EOS (`/eos/user/a/aprotani/physionet/mimic-iv-ext-sdbench`,
checksums OK). `sdbench_overlap.py`: 487 of the 488 cases link to a principal diagnosis; 36 fall
in our 20 conditions (ISCH 23, SYNC 4, GLIO 2, one each of ALZ, GBS, HEP, MS, SAH, SE), 21 of
them in SDBench's validation + test sets. Their chapters: circulatory 114, injury 85, digestive
75, nervous only 11. A small head-to-head set, not a neurology benchmark.

# Part 5: tool catalogue and a first precomputed MIMIC set (6 Nov 2026)

## What MIMIC clinicians ordered, against our vocabulary

`mimic_order_catalogue.py` counted, for the 17,903 admissions with a principal diagnosis in the
20 conditions, every radiology exam, provider order, microbiology test and lab item seen in at
least 10 admissions. `mimic_tool_map.py` routes them to our tools:

| Source | Core term | Pack term only | Approximate | Missing | Not a diagnostic order | Unmatched |
|---|---|---|---|---|---|---|
| Radiology exams | 72.1 % | 4.5 % | 1.2 % | 1.4 % | 19.5 % | 1.3 % |
| Microbiology | 78.5 % | 6.3 % | 2.5 % | 0 | 11.4 % | 1.3 % |
| Lab items (by fluid) | 99.5 % | 0.1 % | 0.4 % | 0 | 0 | 0 |
| Provider orders | 12.5 % | 0 | 1.5 % | 0.8 % | 85.2 % | 0 |

(Shares of admission × item pairs. "Not diagnostic": billing modifiers, line placement,
embolization steps, sedation, nursing, diet, drugs.)

- **The core catalogue already serves almost every diagnostic order** of a neuro admission:
  head CT and CTA, brain MRI and MRA, CT perfusion, carotid duplex, chest X-ray and CT, spine
  imaging, venous duplex, echo, ECG, EEG, TCD, EMG, Holter, telemetry, cultures, CSF, labs.
- **Pack-only items** are complications, not the neuro diagnosis: gallbladder ultrasound (477
  admissions), abdominal X-ray (382 + 141 + 82), BAL (209), renal ultrasound (164), extremity
  X-ray.
- **Missing**: consults (369 neurology, 336 ID, 304 cardiology, …), which the harness leaves out
  on purpose (`consult_medical_specialist` does not exist); upper-limb venous duplex (≈250),
  abdominal Doppler (356), plain spine X-ray (≈180). **Approximate**: the swallow evaluation (4,009
  speech consults, 458 videofluoroscopic swallows) only as `speech_language_evaluation`.
- **The other direction.** All 16 tools are required somewhere in NeuroBench, but 128 of the 388
  vocabulary terms are never named in any of the 600 policies, and some are common in MIMIC:
  arterial blood gas (`ABG`, ≈3,000 neuro admissions), `spine_CT` (≈890 C-spine CTs), `sputum`
  culture (≈870). A policy reward trained on NeuroBench alone never rewards them.

## Recommendation

1. **One catalogue per experiment, the same at training and test, written down with the run.**
   For the MIMIC-neuro pilot it is the **core catalogue**, plus at most the few missing terms a
   pilot case needs (spine X-ray, upper-limb duplex, abdominal Doppler, a swallow study), added to
   the core as CLAUDE.md asks for terms NeuroBench needs. The `general_medicine` pack stays off:
   no neuro diagnosis needs it, and a longer catalogue changes the small models' behaviour, so
   every NeuroBench baseline would have to be re-run.
2. **GRPO and never-rewarded tools.** GRPO only moves the probability of actions the model
   samples. A term that is never justified in training is penalized whenever it is tried (waste,
   unjustified actions, cost), so the model can learn to avoid it everywhere, including on MIMIC
   cases where it is right. Countermeasures, cheapest first:
   - a coverage table per run: for every catalogue term, the training cases where it is required
     (from the policies) and the probe cases where it is needed;
   - keep the KL term to the base model, and track per-term call rates during training on a fixed
     probe set (the September collapse already showed tool-skipping);
   - put MIMIC training cases in the GRPO mix as soon as they exist, so ABG, spine CT and sputum
     cultures are rewarded somewhere; the outcome-vs-policy comparison stays clean if both arms
     get the same mix.
3. **Unrecorded orders get a precomputed normal report, never "not available".** Built from what
   we already have:
   - the base is `fallback_library.yaml`, the same normal report NeuroBench serves, so a MIMIC
     case reads like a NeuroBench case;
   - a per-case contradiction pass (the `library_contradictions.yaml` idea, case by case): where a
     normal would contradict the record (documented diabetes and a normal HbA1c, documented CKD
     and a normal creatinine, a documented negative), the case stores its own consistent report,
     written by a local model under SDBench's rules and checked;
   - every served answer carries its origin (`table`, `note`, `synthetic`) in the case metadata,
     hidden from the agent, so results can be reported on real answers only.
   The schema today forbids fallbacks on `provenance: record` cases and `mock_server.py:650`
   answers "not available"; both change.
4. **Pick pilot cases where the synthetic part cannot matter.** Keep only admissions where every
   step the transferred policy requires has a real result (table or note): synthetic reports then
   answer only off-path orders, where a normal result is plausible. This is the existing
   perfect-agent check, applied to real data.
5. **Pilot size: 50 cases, 10 in each of five conditions** that exercise different tools: ISCH
   (CT, CTA, MRI, echo, telemetry), SAH (CT, CTA, CSF), SE (EEG from the note, CSF), BACT (CSF,
   cultures) and GBS (CSF, EMG from the note). Andrea reads all 50. Then the panel models run on
   them with the current harness, and the 21 SDBench cases in our conditions give a direct
   comparison.

## A free-order baseline (proposed 6 Nov 2026)

SDBench gives its agents no menu: they ask for any test in free text and a gatekeeper LLM answers.
Our agents pick from 16 tools whose enums list 388 terms, and `docs/paper/catalogue-cue.md`
(4 Nov) showed the catalogue itself carries a cue (the NMDAR antibody tests, for one). A baseline with one tool,
`request_test(test: str, details: str)`, measures how much the menu helps or steers the panel.

Design, so that only the interface changes:

1. **Translate, then serve as today.** A translator model maps each free-text order to one typed
   action of the vocabulary (`"MRI brain with diffusion"` → `analyze_brain_mri(sequence=DWI)`),
   or to `off_catalogue`. A mapped order goes through `NeuroBenchEnvironment.execute` unchanged:
   same MockServer answer, same cost, and the policy reward scores the translated actions, so the
   menu and free-order runs are directly comparable.
2. **Generate only what has no answer.** An `off_catalogue` order gets a report from the
   gatekeeper, written from the case under SDBench's rules: findings without impression, a normal
   result unless the case documents otherwise, never naming the diagnosis. Its price comes from
   the same Medicare table when a code is found, else a fixed off-catalogue price. The reward
   counts it as not justified (it can satisfy no criterion), which is the same treatment a
   needless order gets today.
3. **Vague orders get a clarification, not a result.** "Blood tests" returns "which tests?", a
   turn spent inside the step budget (SDBench does the same).
4. **Deterministic answers.** Temperature 0, and every translation and generated report cached
   per (case, normalized order) and stored with the run, so a re-run or a second model sees the
   identical answer. The translator and gatekeeper (model, prompt version) are recorded in the
   run manifest.
5. **Checks before any number is reported.** A translation table audited by hand on a sample
   (wrong mappings change the reward), and a leak scan of generated reports for the diagnosis,
   its synonyms (`diagnosis_synonyms.yaml`) and their ICD codes.

Where it runs: GLM-5.3 (`GLM-5.3-FP8-VERTEX`) through the CERN AI gateway. On 6 Nov 2026 Andrea
reported that CERN confirmed by email that the gateway retains and logs nothing, Vertex models
included, so it can also serve MIMIC later; the first run is on NeuroBench only. On MIMIC the calls
would run from a CERN host, never through a Claude session.

First run (6 Nov 2026): Qwen3.5-9B, profile `free-order-qwen3.5-9b`, 600 cases, seeds 1–3,
concurrency 16, draft policies, on rockhopper. The settings match `outputs/paper/catalogue_full/B-s*`
(the menu arm with the neutral catalogue prose), so the two can be compared case by case. Outputs
in `outputs/paper/free_order/` on rockhopper, translation cache in `outputs/free_order/cache`.
A 30-order probe before the run: after one prompt fix (a missing optional argument is never
vague), all 30 translations were right, including vague ("basic labs", "PET scan"), multiple
("CT head and MRI brain"), not-a-test (consult, lorazepam) and off-catalogue (upper-limb duplex,
lumbar spine X-ray, NIHSS, swallow evaluation). A second fix after the first 57 episodes
(prompt v3): a test offered only inside a panel (single paraneoplastic antibodies) maps to the
panel, and a lab order with some uncovered items maps the covered ones; the run was restarted.

Results (6 Nov 2026, draft policies, engineering only), free order minus menu, paired by case:

| Seed | Diagnosis | Required coverage | Scalar |
|---|---|---|---|
| 1 | 0.850 → 0.845 (−0.005 [−0.033, +0.025]) | 0.461 → 0.249 (−0.211 [−0.236, −0.184]) | 0.478 → 0.364 (−0.114) |
| 2 | 0.872 → 0.843 | 0.475 → 0.245 | 0.492 → 0.361 |
| 3 | 0.882 → 0.850 | 0.467 → 0.262 | 0.494 → 0.373 |

- Without the menu Qwen orders half as much (1.9 against 3.7 tests per case, seed 1) and finds
  the diagnosis about as often (−0.005 to −0.032): the menu changes the work-up, not the answer.
- The coverage loss is tests never ordered, not translation: required criteria whose tool was
  never ordered rise from 44% to 64%, while "same tool, other arguments" falls (24% → 19%). The
  largest rise is `perform_clinical_assessment` (78 → 236 missed): bedside assessments such as
  functional signs, orthostatic blood pressure or a cognitive screen are ordered when the menu
  lists them, not otherwise. Functional disorder falls from 0.68 to 0.03, NPH 0.81 → 0.27, FTD
  0.57 → 0.16, migraine 0.39 → 0.07; MS, SAH and cardiac syncope do not fall.
- Orders (seed 1): 1,087 mapped, 27 off-catalogue, 49 several tests at once (not placed), 3 vague,
  2 not a test. 2,983 translations and 105 generated reports are cached.
- Still owed before any of this is reported: the same run for Granite and Gemma (running, see
  below).

Hand audit of the translations (7 Nov 2026). From the 2,778 distinct orders of the three seeds
(2,522 mapped, 169 several tests, 74 off-catalogue, 10 vague, 3 not a test) I read 169 by hand
(100 mapped, 25 several tests, 30 off-catalogue, all the vague and not-a-test orders) and then
all 74 off-catalogue orders against the catalogue enums.

- Mapped: 97 of 100 right. One dropped items the order named (a CSF order with Gram stain,
  culture and an autoimmune panel became NMDAR antibodies only); two set an MRI protocol the order
  did not name (dementia, epilepsy).
- Off-catalogue: about 12 of 74 wrong, and one class is systematic. 10 of the 21 NPH tap-test
  orders ("large-volume lumbar puncture", "CSF tap test") were called off-catalogue, while the other
  11 were mapped to `analyze_csf`; the policy requires `analyze_csf`, so those episodes lost a
  required criterion through the translator. Also missed: an ictal SPECT (`perfusion_SPECT`) and a
  JC virus antibody index (`anti_JCV_antibody`).
- Vague and several tests: inconsistent twins. "VGCC antibody" was mapped to the P/Q assay once
  and called vague twice; "routine EEG with prolonged monitoring" was mapped once and called vague
  once; a conditional step ("if negative, MRI"; "CSF if a lumbar puncture is done") made an order
  "several tests" and cost the turn.
- Effect on the Qwen numbers above: small. The tap test touches about 10 of 1,800 episodes, and the
  coverage loss is tests never ordered. Even so, the panel run is redone with the fixed prompt.

Prompt v4 fixed these cases (a catalogue procedure with extra purpose or volume is still that
procedure; one assay split into subtypes maps to all of them; conditional steps are ignored; look
for synonyms before calling an order off-catalogue). In a 227-order probe it changed 33 orders. It
fixed all 10 tap tests, VGCC, the EEG twins and the conditional steps, but the synonym rule let
GLM substitute related tests (APOE → early-onset AD panel, serum benzodiazepine → AED levels,
"Holter or event recorder" → Holter, "hypercoagulable panel" → a list of assays). Prompt v5 says a
related or broader test is not the same test, and that an order leaving alternatives open is vague.
On the same 227 orders v5 kept every v4 fix, dropped all seven substitutions, and changed none of
the 80 correct mappings. Still open in v5: the JC virus antibody index stays off-catalogue (the
order asked for serum and CSF), and "brain MRI including orbits" is sometimes one call, sometimes
two. Probe outputs: rockhopper
`outputs/paper/free_order_panel/probe_v{4,5}.txt`.

Panel run (started 7 Nov 2026, 14:03): `scripts/paper/free_order_queue.sh` on rockhopper in tmux
`panel`. Granite, Gemma, then Qwen: each gets the menu profile (`policy-*`) and the free-order
profile, 600 cases × seeds 1–3, concurrency 16, draft policies, prompt v5, all on the same code.
Outputs go to `outputs/paper/free_order_panel/<model>/`, with `compare.txt` per model and progress
in `status.txt`; the staged Granite and Gemma weights are deleted from `/dev/shm` when each model
finishes. In the first 80 Granite menu episodes, half failed on invalid actions. There were 90
prose answers instead of a tool call and 72 calls to invented tools (`order_brain_mri`,
`order_lumbar_puncture`, `order_csf`). Its September base evaluation failed 16%. The free-order
arm has a single tool, so the two arms' completion rates will differ; the comparison script
prints both.

What it does not do: replace the typed catalogue for GRPO. A live LLM in every rollout step is
slow and adds noise to the reward; the cache makes it affordable for evaluation, and only later,
if it matters, for training. It is a third arm of the evaluation (menu, no tools, free order),
run on the same cases and seeds.

Panel result (finished 7 Nov 2026, 20:08; prompt v5, 600 cases × 3 seeds per arm; free minus menu,
range over seeds):

| Model | Diagnosis | Required coverage | Scalar | Tests per case (menu → free) |
|---|---|---|---|---|
| Qwen3.5-9B | −0.02 / −0.03 | −0.20 / −0.22 | −0.11 / −0.12 | 3.7 → 1.9 |
| Gemma 4 E4B | −0.06 / −0.08 | −0.23 / −0.25 | −0.15 / −0.17 | 5.1 → 3.0 |
| Granite 4.1 8B | see below | −0.09 | +0.002 | 3.6 → 1.0 |

Granite's pooled diagnosis difference (+0.086) is an artefact: its menu arm fails 28-33% of
episodes on invalid actions. On menu-completed cases, menu diagnosis is 0.69-0.74 against
0.59-0.61 free. Without the menu, every model orders about half the tests and covers less of the
work-up.

# Part 6: the MIMIC pilot, built and evaluated (7-9 Nov 2026)

Cases are built on rockhopper by a Claude Code session under Andrea's CERN account (zero data
retention), which is the only agent that reads MIMIC records. Everything record-derived stays in
`/eos/user/a/aprotani/physionet/work/mimic-neuro`. This document, like the Mac session, sees only
aggregate reports. The formal method (cohort flow, record-to-tool mapping, decision log 1-51,
validation, limitations) is [`docs/benchmark/mimic-neuro-methods.md`](../benchmark/mimic-neuro-methods.md),
copied from the workspace's `report/07_methods.md`.

**Final set (task 07, 9 Nov 2026): 100 cases.**
- Allocation: ISCH 38, MS 22, SAH 12, HEP 10, SE 9, GBS 3, FND 2, FEPI 2, BACT 2.
- Changes from the task-06 set (8 Nov):
  - 12 cases were excluded and replaced, all of them by ISCH, because the SAH, SE, FND and FEPI pools were exhausted;
  - the exclusions: SAH aneurysm status not established 5, transfers 3, SE evidence only in the ED course 1, frontal FEPI focus 1, exam after thrombolysis 1.
- Coverage of the 20 conditions: 9 conditions gave cases.
  - Seven are out of scope for an ED-admission source: MIG, ALZ, FTD, VASC, PD, NPH, ALS.
  - SYNC is out of scope too: 0 of 40 strict admissions were cardiac syncope.
  - GLIO, MG and NMDAR have no admission with every required step.
- SAH labels come from the record. 6 cases have an aneurysm and keep I60.x. 6 are non-aneurysmal and coded I60.8, and they accept only non-aneurysmal labels.
- Label errors inherited from the synonyms file are fixed by a 13-entry overlay (`apply_diagnosis_synonyms.py --overlay`). Each entry reuses labels the repository already grants. Methods 5.4 lists the repository fix each entry stands in for; these fixes are not applied yet.
- Every case has rejected labels: half of the templates, or one third when half gives none. SE also gets its mimics (PNES, syncope).
- Required criteria with a served result: 289/289, recommended 96/96.
- Checks on the final build:
  - schema, build errors, synonyms `--check`, timing, perfect agent: all clean, 100/100;
  - independent field-by-field re-read: 1.41% of fields wrong in round 3, 0.55% in round 4 (the last full round), 0.28% in round 6 (93 cases);
  - after round 4, each round re-read every case with an error or a content change; rounds 11 and 12 found 0 errors;
  - blind leakage: 8 leaks, then 4, 1, 1 and 0. No presentation leak in any round.

**Evaluation on the final set** (`eval_20261109`; Qwen3.5-9B, seeds 1-3, draft policies, engineering only; GRPO adapters from the 2 Nov sweep; paired against the tool-using base model, 95% bootstrap CI):

| Arm | Scalar | Diagnosis | Required coverage | Tools per case | Completed |
|---|---|---|---|---|---|
| no tools (narrative) | 0.132 | 0.510 (−0.100 [−0.187, −0.013]) | 0 | 0 | 100% |
| tools, base model | 0.358 | 0.610 | 0.378 | 6.2 | 95% |
| GRPO, default config | +0.105 [+0.065, +0.141] | +0.080 [+0.020, +0.140] | +0.151 | 7.3 | 95% |
| GRPO, best validation arm | +0.025 [−0.013, +0.057] | +0.030 [−0.033, +0.090] | +0.062 [+0.015, +0.107] | 5.8 | 95% |

- The default GRPO configuration beats the base model on all three sets: 53 cases (7 Nov), the task-06 set and the final set.
- The best-validation arm still covers more of the required work-up. Its diagnosis and scalar gains (significant on the task-06 set) are not significant on the final set.
- Per condition (scalar, tools → GRPO default):
  - ISCH 0.28 → 0.47 (n=38);
  - MS 0.38 → 0.51 (n=22, a condition held out of GRPO training);
  - SE 0.29 → 0.42 (n=9);
  - SAH 0.34 → 0.40 (n=12);
  - HEP 0.52 → 0.54 (n=10).
- FND (n=2) gets worse: 0.89 → 0.23. The gain is broad, but ISCH carries the most weight.
- On this set the narrative arm now loses diagnoses as well (−0.10), unlike on NeuroBench.
- On NeuroBench validation no sweep arm beat the base.
- Not yet reportable: the policies, labels and drafts are draft until two physicians approve them.

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

Part 3 ran on lxplus against `/eos/user/a/aprotani/physionet` (`P` below), with
`UV_CACHE_DIR=/tmp/<user>-uv` and `uv run -q --no-project --python 3.12 --with duckdb --with pandas python -I`:

```bash
mimic_profile.py $P/mimic-iv-ext-cdm/1.1 $P/mimic-iv-ed/2.2 $P/mimic-iv-note/2.2 $P/mimiciv/3.1/hosp
mimic_cohort.py --hosp $P/mimiciv/3.1/hosp --ed $P/mimic-iv-ed/2.2/ed --note $P/mimic-iv-note/2.2/note
mimic_note_sections.py --hosp $P/mimiciv/3.1/hosp --note $P/mimic-iv-note/2.2/note
# Parts 4 and 5
sdbench_overlap.py --sdbench $P/mimic-iv-ext-sdbench/1.0.0/dataset.json --hosp $P/mimiciv/3.1/hosp --note $P/mimic-iv-note/2.2/note
mimic_order_catalogue.py --hosp $P/mimiciv/3.1/hosp --note $P/mimic-iv-note/2.2/note --out orders_neuro.csv
mimic_tool_map.py orders_neuro.csv   # reads only the counts CSV (test names and admission counts)
```
