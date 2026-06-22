# Glossary — NeuroAgent / NeuroBench collaboration deck

Plain-language definitions for the terms used in `collab_prop.tex`, grouped by
theme. Written so a clinician needs no machine-learning background and an
ML reader needs no neurology background.

---

## Project terms

- **NeuroAgent** — the AI system we are building: a large language model that
  works a case like a clinician, ordering tests one at a time and reasoning
  toward a diagnosis.
- **NeuroBench** — our benchmark: 600 neurology cases used to measure how well
  NeuroAgent (or any model) performs.
- **Agent** — an AI model that can take actions (here, order tests) rather than
  only answer a question in one shot.
- **Tool** — one callable diagnostic action available to the agent (e.g. order
  an MRI, interpret labs). The deck uses 12 tools.
- **Tool-augmented** — a model that can call external tools/actions instead of
  relying only on what it already "knows".
- **ReAct loop** — "Reason + Act": the agent alternates between thinking and
  taking one action, repeating until it reaches a diagnosis (up to 15 steps in
  our setup). Shown as the reason → order → read → revise diagram.
- **Turn / step** — one cycle of the loop (one thought plus one action).
- **360° patient / "complete picture"** — every case pre-computes a realistic
  result for *any* test the agent might order, so it never hits a dead end even
  when it picks the wrong test.
- **Ground truth** — the reference-correct answer for a case (the true
  diagnosis, the ideal test pathway, the unsafe actions), against which the
  agent is scored.
- **Difficulty tiers** — three levels of case difficulty, from straightforward
  to diagnostic puzzle.
- **Setting** — the clinical context of a case: emergency, inpatient, or
  outpatient.

---

## Evaluation & machine-learning terms

- **USMLE** — United States Medical Licensing Examination: the standard
  multiple-choice medical exam. We use it as the example of the "question
  answering" style of testing that we argue is not enough.
- **Question answering (Q&A)** — the common way AI is tested today: a
  self-contained question with all clues included and one correct option. We
  contrast this with a full diagnostic workup.
- **Red herring** — a misleading finding that points toward the wrong
  diagnosis (e.g. incidental cervical spondylosis in an ALS case). Good
  reasoning recognises and sets it aside.
- **ICD-10** — International Classification of Diseases, 10th revision: the
  standard diagnosis codes (e.g. *G12.21* = bulbar-onset ALS).
- **Top-1 / top-3** — whether the correct diagnosis is the model's single best
  guess (top-1) or appears among its first three (top-3).
- **Precision** — of the tests the agent ordered, the fraction that were
  actually appropriate.
- **Recall** — of the tests that *should* have been ordered, the fraction the
  agent actually ordered.
- **F1** — a single score combining precision and recall (their harmonic mean).
- **Coverage** — the fraction of the case's required tests that the agent
  obtained.
- **Contraindicated** — a test or action that is medically inadvisable or
  unsafe in that patient's context; ordering one is a safety penalty.
- **Cost / cost efficiency** — the money spent on tests versus the optimal
  workup, plus penalties for useless or repeated orders (priced with Medicare
  reference rates).
- **AI reasoning judge / LLM judge** — a separate language model that scores
  the agent's reasoning against a rubric, on eight 0–5 dimensions.
- **Composite reasoning score** — the eight judge dimensions combined into one
  weighted overall score.
- **Differential reasoning** — weighing competing diagnoses (the "differential
  diagnosis") against the evidence.
- **Uncertainty calibration** — whether the model's stated confidence matches
  how often it is actually right.
- **Inter-rater agreement** — how consistently independent reviewers reach the
  same judgement on the same case.
- **Cohen's κ (kappa)** — a statistic for inter-rater agreement that corrects
  for agreement expected by chance (0 = chance, 1 = perfect).
- **Fine-tuning** — further training a model on task-specific examples to
  specialise it; the reason we need a large synthetic dataset.
- **Synthetic case** — a case generated entirely by AI from clinical templates,
  with no single source report (versus real-report-seeded cases).

---

## Data & licensing terms

- **MedCaseReasoning** — the public dataset our real-seeded cases are built
  from (Wu et al., arXiv:2505.11733, 2025); clinician-written case reports.
- **PMC (PubMed Central)** — the open-access archive of biomedical literature
  from which those case reports originate.
- **PMCID** — the unique identifier of an article in PMC; we log one per
  seeded case for traceability.
- **CC-BY 4.0** — a Creative Commons licence permitting reuse, including
  modification, as long as the source is credited.

---

## Clinical terms (from the worked ALS example and the 12 tools)

- **ALS (amyotrophic lateral sclerosis)** — a progressive motor neuron disease
  affecting both upper and lower motor neurons.
- **Bulbar-onset ALS** — ALS that begins in the bulbar muscles, so the first
  symptoms are speech and swallowing problems.
- **Dysarthria** — slurred or effortful speech from impaired muscle control.
- **Dysphagia** — difficulty swallowing.
- **Fasciculations** — visible involuntary muscle twitches (a lower motor
  neuron sign).
- **Hyperreflexia** — abnormally brisk reflexes (an upper motor neuron sign).
- **Babinski sign** — an upgoing big toe when the sole is stroked; an upper
  motor neuron sign.
- **Cervical spondylosis** — age-related degeneration of the neck spine; here a
  red herring that can mimic ALS.
- **EMG / NCS** — electromyography and nerve conduction studies: tests of
  muscle and nerve electrical activity, key to confirming ALS.
- **CSF (cerebrospinal fluid)** — the fluid around the brain and spinal cord,
  sampled by lumbar puncture.
- **Lumbar puncture** — the procedure ("spinal tap") used to collect CSF.
- **Neurofilament light (NfL)** — a CSF/blood biomarker of nerve-cell damage;
  elevated in ALS.
- **Oligoclonal bands** — antibody bands in CSF indicating inflammation inside
  the central nervous system (e.g. multiple sclerosis).
- **CK (creatine kinase)** — a muscle enzyme; mild elevation can accompany
  motor neuron disease.
- **CT scan** — computed tomography; fast X-ray cross-sectional imaging.
- **MRI** — magnetic resonance imaging; detailed soft-tissue imaging of brain
  or spine.
- **Advanced imaging (MRA / MRV / CTA / PET / DaT-SPECT)** — specialised scans:
  MR/CT angiography (arteries), MR venography (veins), PET (metabolic imaging),
  and DaT-SPECT (dopamine imaging for parkinsonism).
- **EEG (electroencephalography)** — recording of the brain's electrical
  activity; used for seizures and encephalopathy.
- **ECG (electrocardiography)** — recording of the heart's electrical activity.
- **Echocardiogram** — ultrasound of the heart.
- **Ejection fraction** — the percentage of blood the left ventricle pumps out
  per beat; a measure of heart function.
- **Cardiac monitoring (telemetry / Holter / loop recorder)** — ways to record
  heart rhythm over time, from inpatient telemetry to implantable loop
  recorders.
- **Drug interactions** — checking whether prescribed medications conflict or
  are contraindicated together.
