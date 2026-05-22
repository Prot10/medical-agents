# NeuroBench v5 — Tool Report Style Guide

Reference for writing the **interpretive text** of simulated tool outputs so each
report reads like the real hospital report it imitates. Derived from real report
standards: ACR/RSNA structured reporting, ACNS (EEG/EP), AANEM (EMG/NCS),
ASE (echo), AHA/ACC/HRS (ECG), CAP (lab), Mayo/ARUP (CSF & antibody panels),
UpToDate/Lexicomp (literature & drug interactions).

## Why this exists

A tool output must report **what that one test observed** — nothing more. The
agent under test is responsible for integrating tests, resolving the
differential, and choosing management. When a report does that work for the
agent, it is both unrealistic and leaks the answer. This guide makes every
report faithful to its modality; modality-faithfulness closes the leak by
construction.

The benchmark stays fair: the agent must still order the right tests, combine
them, work through the red herrings, and decide treatment — because no single
real report does any of that.

---

## The three universal prohibitions

No report — of any modality — may do these:

1. **No cross-modality synthesis.** A report interprets only its own modality's
   data. It must NOT cite the patient's genetics, MRI, other labs, exam
   findings, vital signs, or "the overall clinical picture." It may reference
   only (a) the brief clinical indication as written on the requisition, and
   (b) a *prior study of the same modality* for comparison. Phrases to delete:
   "combined with…", "taken together with…", "in the context of the [other
   test]…", "given the patient's [diagnosis]…".

2. **No differential-refutation essays.** A report never argues a competing
   diagnosis away with numbered points ("NOT lead neuropathy because (1)… (2)…").
   At most ONE hedged sentence may note an alternative: "findings could also be
   seen with X; clinical correlation required." Delete numbered rebuttals,
   "this excludes…", "the prior diagnosis of … was erroneous", "the … is
   incidental/a red herring".

3. **No management or treatment prescription.** A report never names a drug,
   dose, or therapy, never says "start/initiate/add…", "pacemaker indicated",
   "admit", or "refer to…". The only forward-looking statement allowed is a
   recommendation for a further **diagnostic** step within reason ("recommend
   MRI with contrast", "recommend repeat study in 3 months", "tissue diagnosis
   recommended"). **Exception:** `check_drug_interactions` legitimately gives
   category-level management ("monitor INR", "avoid combination").

The standard close — **"Clinical correlation recommended."** — is the formal
hand-off. Use it *instead of* doing the synthesis yourself.

## Universal voice

Terse, declarative, impersonal. A NORMAL study's impression is 1–2 lines. An
ABNORMAL study's impression is a short numbered list, one finding per line,
ordered by clinical importance. No prose paragraphs of reasoning.

---

## Per-tool specifications

### `analyze_brain_mri` (MRIReport) and `order_ct_scan` (CTReport)

- **Structure** (real): Indication → Technique → Comparison → Findings (by
  anatomic region, with pertinent negatives) → Impression.
- **Impression — how far it goes:** Names the diagnosis when imaging is clear
  ("acute left MCA territory infarct"; "subarachnoid hemorrhage"; "large
  heterogeneously enhancing mass with central necrosis"). When the appearance
  is ambiguous, gives a *worded imaging differential*: "most consistent with X;
  Y cannot be excluded." Hedging scale: *is → indicative of → consistent with
  → suggestive of → cannot be excluded*.
- **KEEP:** the morphologic description; a diagnosis the imaging genuinely
  shows; comparison to a prior MRI/CT; a recommendation for further imaging.
- **STRIP:** any reference to labs/EEG/genetics/exam; statements like "does not
  exclude early ALS (MRI is insensitive…)" → reduce to "No abnormality
  identified." or "Normal study."; teaching parentheticals; management.
- **`differential_by_imaging`:** allowed and good — but it is an *imaging*
  differential (entities that look like this on the scan), not the case answer
  ranked first with the red herrings dismissed.
- **Normal example:** "No acute intracranial abnormality. No mass, hemorrhage,
  midline shift, or restricted diffusion."
- **Abnormal example:** "1. Large heterogeneously enhancing right frontal mass
  with central necrosis and surrounding vasogenic edema; 8 mm leftward midline
  shift. Imaging features are consistent with a high-grade neoplasm. 2. No
  additional intracranial lesion. Tissue diagnosis recommended."

### `analyze_eeg` (EEGReport)

- **Structure:** Clinical history → recording conditions → description of
  background and abnormalities → Impression → (clinical correlation).
- **Impression — how far it goes:** Opens "This is a NORMAL/ABNORMAL EEG."
  Names the **electrographic pattern** in ACNS terms ("left anterior temporal
  spike-and-wave discharges", "generalized periodic discharges",
  "burst-suppression"). It must **NOT say "epilepsy"** — EEG cannot diagnose
  epilepsy. It may note electrographic seizures / status electrographically.
- **KEEP:** normal/abnormal call; named patterns; "no epileptiform discharges";
  "no electrographic seizures recorded."
- **STRIP:** "epilepsy"/disease names; "pathognomonic for …"; references to
  MRI/labs; management. Per-finding `clinical_correlation` should be empty `""`
  or a brief electrographic note — never "highly suggestive of anti-NMDAR
  encephalitis; start immunotherapy."
- **Normal example impression:** "This is a NORMAL EEG. No epileptiform
  discharges and no electrographic seizures. Clinical correlation recommended."
- **Abnormal example:** "This is an ABNORMAL EEG due to: 1. Frequent right
  anterior temporal sharp-and-slow-wave discharges. 2. Intermittent right
  temporal focal slowing. No electrographic seizures were recorded."

### `analyze_ecg` (ECGReport)

- **Impression (`interpretation`) — how far it goes:** Maximally definitive,
  categorical. Names rhythm and conduction precisely ("sinus bradycardia with
  trifascicular block"; "atrial fibrillation with rapid ventricular response").
  Only acute ischemia is hedged ("probable acute inferior STEMI").
- **KEEP:** the categorical rhythm/conduction/morphology diagnosis; comparison
  to a prior ECG.
- **STRIP:** any non-cardiac reference ("given her ALS…"); management
  ("pacemaker indicated"). Top-level `clinical_correlation`: empty `""` or a
  brief within-cardiology note.
- **Example:** "Sinus bradycardia, rate 48. First-degree AV block with
  bifascicular block (RBBB and left anterior fascicular block) — trifascicular
  pattern. No acute ST-T changes."

### `interpret_labs` (LabResults)

- **Real routine panels (CBC, BMP/CMP, LFTs, thyroid) carry NO narrative.**
  Just value + flag + reference range.
- **`clinical_significance` (per LabValue):** set to `null` for routine panel
  values. (Do not write "consistent with …" under a result.)
- **`interpretation` (required field):** keep brief and pattern-level — a plain
  recital of which values are abnormal and the direction, e.g. "Mild
  normocytic anemia (Hb 10.8). Sodium 152 (elevated). Remaining indices within
  normal limits." No disease names, no causal claims, no management.
- **`abnormal_values_summary`:** factual list of out-of-range values; no
  interpretation.
- **Specialized serology / antibody panels:** these *do* carry a short
  templated interpretive comment that names the disease **heavily hedged**:
  "Anti-NMDA receptor IgG antibody is found in a subset of patients with
  autoimmune encephalitis; a negative result does not exclude the diagnosis.
  Clinical correlation recommended." Templated, not patient-individualized.

### `analyze_csf` (CSFResults)

- **Values** (appearance, opening pressure, cell count, protein, glucose,
  special tests) — factual, untouched.
- **`interpretation` — how far it goes:** describes the **pattern**, does not
  declare the final clinical diagnosis. "Neutrophilic pleocytosis with markedly
  elevated protein and low glucose — a pattern consistent with bacterial
  infection." Culture/Gram-stain/PCR results are stated as fact ("Gram-positive
  diplococci seen"; "HSV-1/2 PCR not detected"). End with clinical correlation.
- **STRIP:** cross-modality references; management; "the prior diagnosis of …".

### `order_echocardiogram` (EchoReport)

- **Impression — how far it goes:** Names cardiac diagnoses directly ("severe
  aortic stenosis, valve area 0.7 cm²"; "LVEF 35% with global hypokinesis").
  May compare to a prior echo and may recommend repeat *imaging* or specialist
  referral framed as "consider".
- **STRIP:** non-cardiac references; drug therapy; "pacemaker indicated."

### `order_cardiac_monitoring` (CardiacMonitoringReport)

- **Impression — how far it goes:** Characterizes the rhythm and the
  **arrhythmia burden** quantitatively ("paroxysmal atrial fibrillation,
  longest episode 4 h 22 min"; "PVCs 14% of total beats"); states
  symptom–rhythm correlation. **No management** (no pacemaker, ablation, or
  anticoagulation advice). No cross-modality references.

### `order_advanced_imaging` (AdvancedImagingReport)

Modality-specific naming limits — **important**:
- **Amyloid PET:** strictly **binary**. "Positive — moderate-to-frequent
  amyloid neuritic plaque density" / "Negative — sparse-to-no amyloid." It must
  **NOT** say "Alzheimer's disease."
- **DaTscan:** strictly **binary**. "Normal striatal dopamine transporter
  uptake" / "Abnormal — reduced putaminal uptake, consistent with a
  presynaptic dopaminergic deficit." It must NOT distinguish PD vs MSA/PSP.
- **FDG-PET:** names the **metabolic pattern**, hedged: "temporoparietal and
  posterior cingulate hypometabolism — a pattern consistent with an
  Alzheimer-type metabolic profile." Not "diagnostic of AD."
- **MR perfusion / spectroscopy:** report the metric and a within-imaging
  read ("elevated rCBV, consistent with high-grade neoplasm").
- **Carotid duplex:** stenosis grade by velocity criteria.
- Per-finding `interpretation` fields: keep within-imaging; strip cross-modality.

### `order_specialized_test` (SpecializedTestReport)

Covers EMG/NCS, evoked potentials, neuropsychometry, tilt-table, etc.
- **EMG/NCS:** report the **electrophysiological pattern + localization**
  ("active denervation and chronic reinnervation in bulbar, cervical, thoracic
  and lumbosacral regions; sensory NCS normal; no conduction block"). The
  impression may reach a hedged within-modality conclusion ("findings indicate
  a widespread disorder of anterior horn cells, consistent with a motor neuron
  disease"). It must **NOT** be a diagnostic essay: no numbered rebuttal of
  mimics, no citing genetics/MRI, no "the MGUS is incidental", no management.
- **Evoked potentials:** name the physiological abnormality ("prolonged P100
  latency, consistent with optic-nerve conduction delay") — not "MS."
- **Neuropsychometry:** this report *does* legitimately commit to a named,
  confidence-qualified diagnosis ("profile consistent with amnestic mild
  cognitive impairment"; "probable behavioral-variant FTD") — keep that, but
  still no cross-modality citation or management.
- **Tilt-table:** state positive/negative + VASIS subtype.

### `search_medical_literature` (LiteratureSearchResult)

- **`results[]` and `summary`:** general, **population-keyed** evidence — never
  a case-specific verdict. Correct: "IVIG within two weeks of onset shortens
  time to recovery in Guillain-Barré syndrome (RCT evidence)." Wrong: "This
  patient has GBS; start IVIG." Delete any sentence that diagnoses *this*
  patient, resolves *this* differential, or prescribes *this* plan.
- Keep `evidence_level` tags and generic findings.

### `check_drug_interactions` (DrugInteractionResult)

- Legitimately gives category-level management. Keep `interactions`,
  `contraindications`, `warnings`, `alternatives`, `formulary_status` — but they
  describe the **interaction**, not the case diagnosis. Delete any sentence that
  uses the drug check to announce or confirm the patient's diagnosis.

---

## Fields to rewrite vs. leave

**Rewrite (interpretive text):** `impression`, `interpretation`,
`clinical_correlation` (ECG top-level and per EEG finding), `clinical_significance`
(per lab value → usually `null`), `summary` and `results[].finding`
(literature), `recommended_actions`, `differential_by_imaging`,
`findings[].interpretation` (advanced imaging). Apply in
`initial_tool_outputs`, every `followup_outputs[].output`, and
`fallback_tool_outputs`.

**Leave untouched (objective data):** all structured `findings` objects,
`signal_characteristics`, `panels`/lab values/units/ranges/`is_abnormal`, CSF
values, ECG `rhythm`/`rate`/`intervals`/`findings`, echo
`chambers`/`valves`/`ejection_fraction`, monitoring `events`/`heart_rate_range`,
`classification`, `background`, `confidence`.

Never change the *substance* of a finding — only the voice of the interpretation.
If the underlying findings genuinely are equivocal, the impression stays
equivocal; if they are diagnostic within that modality, the impression may say
so within that modality.
