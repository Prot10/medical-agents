# External Medical Case Sources for NeuroBench Expansion

*Research compiled March 2026 for NeuroBench / NeuroAgent (Nature Machine Intelligence submission)*

---

## Table of Contents

1. [Why Use External Case Sources](#1-why-use-external-case-sources)
2. [NeuroBench Schema Requirements](#2-neurobench-schema-requirements)
3. [Tier 1: Immediately Usable Sources](#3-tier-1-immediately-usable-sources)
4. [Tier 2: High-Value Restricted Sources](#4-tier-2-high-value-restricted-sources)
5. [Tier 3: Component-Specific & Format Models](#5-tier-3-component-specific--format-models)
6. [Not Recommended (with Reasons)](#6-not-recommended-with-reasons)
7. [AI Medical Benchmark Landscape](#7-ai-medical-benchmark-landscape)
8. [Recommended Pipeline: Real Cases to NeuroBench Format](#8-recommended-pipeline-real-cases-to-neurobench-format)
9. [Reference Table: All Sources at a Glance](#9-reference-table-all-sources-at-a-glance)
10. [Citations & URLs](#10-citations--urls)

---

## 1. Why Use External Case Sources

### The Problem with Purely Synthetic Cases

NeuroBench v1 contains 100 cases generated entirely by Claude. While these pass Pydantic validation and clinical plausibility checks, purely synthetic cases have inherent limitations for a Nature Machine Intelligence publication:

1. **Circular evaluation risk**: An LLM-generated benchmark evaluated by LLM agents creates a closed loop. Reviewers will flag this — the agent may perform well simply because it shares the same distributional biases as the generator.

2. **Limited clinical diversity**: LLMs tend toward "textbook" presentations. Real cases have messy histories, incidental findings, medication interactions, and social factors that are harder to simulate.

3. **No provenance for clinical accuracy**: We cannot cite a source for the clinical accuracy of a synthetic case. With real cases, we can point to peer-reviewed publications.

4. **Benchmark contamination**: If the generating LLM has seen similar cases in its training data, the benchmark tests memorization rather than reasoning.

### What External Sources Give Us

- **Clinical grounding**: Cases rooted in real patient presentations from published case reports
- **Citability**: "NeuroBench cases derived from N peer-reviewed case reports published in M journals" (for the Methods section)
- **Diversity**: Real cases include atypical presentations, comorbidities, and complications that LLMs don't naturally generate
- **Robustness**: A benchmark mixing synthetic and real-sourced cases is harder to game
- **Scale**: Access to thousands of neurology cases allows expansion to 200-500 cases for statistical power

### How This Works with Our Pipeline

The key insight is that we don't use external cases directly — we use them as **seeds**. The pipeline is:

```
Real case report (text) → Extract clinical scenario → Generate structured tool outputs → Assemble NeuroBench case → Validate
```

This preserves the clinical realism of the source while adding the structured tool outputs (EEG, MRI, labs, CSF, ECG) that make NeuroBench unique. The agent still needs to use diagnostic tools — it just does so on cases grounded in real clinical presentations rather than purely synthetic ones.

---

## 2. NeuroBench Schema Requirements

For a case to be usable in NeuroBench, it must contain all of the following (defined in `packages/neuroagent-schemas/`):

### Required Fields

| Component | Key Fields | Source Mapping Difficulty |
|-----------|-----------|-------------------------|
| **Patient Profile** | age, sex, PMH, medications, allergies, family/social history, chief complaint, HPI (150+ words), full neuro exam (mental status, cranial nerves, motor, sensory, reflexes, coordination, gait), vitals | Medium — most case reports include these |
| **Tool Outputs** | EEG, MRI, labs, CSF, ECG (condition-dependent, typically 2-4 required) | Hard — must be generated as structured specialist reports with findings, impressions, confidence scores |
| **Follow-up Outputs** | 5-8 conditional outputs triggered by agent actions (e.g., repeat MRI, DaTscan, VEP) | Hard — must be generated, rarely in source material |
| **Ground Truth** | Primary diagnosis + ICD code, 3-5 differential diagnoses with likelihood, 10-15 optimal action steps, critical actions, contraindicated actions, key reasoning points | Medium — diagnosis available in source, actions must be generated |
| **Metadata** | case_id, condition enum, difficulty level, encounter type, expected_agent_confidence | Easy — assigned during assembly |

### What Makes a Case "Tool-Use Ready"

The critical design constraint: cases must be structured so the agent **needs to use diagnostic tools** to reach the diagnosis. This means:

- The patient presentation alone should not reveal the diagnosis (it should narrow the differential to 3-5 possibilities)
- Tool outputs (EEG, MRI, labs, etc.) must contain the discriminating evidence
- Follow-up outputs should reveal additional evidence the agent can request
- The difficulty level controls how much the initial tool outputs reveal vs. require follow-up

This is why we can't just import case reports verbatim — we must restructure them to separate the "what the doctor sees initially" from "what the diagnostic tests show."

---

## 3. Tier 1: Immediately Usable Sources

These sources are **open access with permissive licenses**, contain **structured or semi-structured cases**, and can be downloaded and processed today.

---

### 3.1 MedCaseReasoning (Stanford, 2025)

**The single best source for NeuroBench expansion.**

| Field | Details |
|-------|---------|
| **What** | First open-access dataset for evaluating diagnostic reasoning from clinical case reports |
| **Authors** | Kevin Wu, James Zou (Stanford / Zou Lab) |
| **Paper** | arXiv:2505.11733 (May 2025) |
| **GitHub** | https://github.com/kevinwu23/Stanford-MedCaseReasoning |
| **HuggingFace** | `zou-lab/MedCaseReasoning` |
| **Size** | **14,489 diagnostic QA cases** (13,092 train + 897 high-quality test) |
| **Specialties** | 30+ medical specialties |
| **License** | Code: **MIT**. Dataset: **CC-BY 4.0** |
| **Access** | Direct download via HuggingFace `datasets` library |

**Structure per case:**
```
case_prompt:         Full patient presentation before diagnosis is revealed
                     (~2.5x longer than typical MedQA vignettes)
diagnostic_reasoning: Numbered clinician reasoning statements with article quotes
final_diagnosis:     Gold-standard diagnostic label
```

**Why it works for NeuroBench:**
- `case_prompt` maps directly to our HPI + clinical history + exam findings (needs NLP extraction to separate these)
- `diagnostic_reasoning` maps to `key_reasoning_points` in our ground truth
- `final_diagnosis` maps to `primary_diagnosis`
- Cases are derived from **PMC Open Access** articles, so they represent real published clinical presentations
- CC-BY 4.0 license allows derivative works with attribution
- Long case prompts (avg ~2.5x MedQA length) contain enough detail to extract demographics, medications, exam findings, and often diagnostic test results mentioned in the text

**What's missing (must be generated):**
- Structured tool outputs (EEG/MRI/labs/CSF/ECG as specialist reports)
- Follow-up outputs
- Differential diagnosis list with likelihoods
- Optimal action steps, critical/contraindicated actions
- Structured vitals

**Estimated neurology yield:** With 14,489 cases across 30+ specialties, expect **400-700 neurology cases** (filtering by keywords: stroke, epilepsy, seizure, multiple sclerosis, Parkinson, meningitis, encephalitis, glioma, neuropathy, dementia, headache, syncope, tremor, etc.).

**How to access:**
```python
from datasets import load_dataset
ds = load_dataset("zou-lab/MedCaseReasoning")
# Filter for neurology
neuro_keywords = ["stroke", "epilepsy", "seizure", "multiple sclerosis", ...]
neuro_cases = [c for c in ds["train"] if any(k in c["case_prompt"].lower() for k in neuro_keywords)]
```

---

### 3.2 MultiCaRe Dataset (2024)

**Largest open-source clinical case collection with images.**

| Field | Details |
|-------|---------|
| **What** | Multimodal case report dataset from open-access PubMed Central articles (1990-2023) |
| **Authors** | Mauro Nievas Offidani et al. |
| **Paper** | Data in Brief (2024), https://doi.org/10.1016/j.dib.2023.109825 |
| **GitHub** | https://github.com/mauro-nievoff/MultiCaRe_Dataset |
| **HuggingFace** | `openmed-community/multicare-cases` |
| **Zenodo** | https://zenodo.org/records/10079370 |
| **Size** | **96,428 clinical cases** from 75,382 articles; **135,596 images** with labels and captions |
| **License** | **CC-BY 4.0** (derived from PMC Open Access Subset) |
| **Access** | Direct download from HuggingFace, Zenodo, or GitHub |

**Structure per case:**
```
PMID, title, abstract, journal, publication_date, keywords, MeSH_terms
case_text:     Full narrative case text
images:        Associated medical images with NLP-generated labels and captions
taxonomy:      Hierarchical 140+ category disease classification
```

**Why it works for NeuroBench:**
- 96K cases is a massive pool — even 2-5% neurology yield gives 2,000-5,000 cases to choose from
- CC-BY 4.0 is the most permissive license possible
- **Images**: neuroimaging (MRI, CT) images could supplement our MRI report descriptions
- Hierarchical taxonomy allows systematic filtering for neurological conditions
- Already has a Python extraction package (`multiversity`) for creating custom subsets
- Cases from real peer-reviewed publications (citable)

**What's missing:**
- Cases are free-text narratives (need NLP parsing for structured fields)
- No separate tool outputs, no ground truth actions
- Images are in the paper, not structured as diagnostic reports

**Estimated neurology yield:** Filtering by MeSH terms (Nervous System Diseases [C10]) should yield **2,000-5,000+ neurology cases**.

**How to access:**
```python
from datasets import load_dataset
ds = load_dataset("openmed-community/multicare-cases")
# Or use the multiversity package for filtered subsets
# pip install multiversity
```

---

### 3.3 MedR-Bench (Nature Communications, 2025)

**Closest structural alignment with NeuroBench's multi-stage evaluation.**

| Field | Details |
|-------|---------|
| **What** | Clinical reasoning benchmark with 3-stage evaluation from PMC case reports |
| **Authors** | MAGIC-AI4Med group (Shanghai AI Lab) |
| **Paper** | Nature Communications (2025), https://doi.org/10.1038/s41467-025-64769-1 |
| **GitHub** | https://github.com/MAGIC-AI4Med/MedRBench |
| **Size** | **1,453 cases** (957 diagnosis + 496 treatment), 656 rare disease cases |
| **Body systems** | 13 body systems including nervous system |
| **License** | Not explicitly stated (PMC-OA derived, likely CC-BY) |

**Structure per case:**
```
patient_case:               Structured patient information
examination_recommendation: What tests should be ordered
diagnostic_reasoning:       Step-by-step reasoning to diagnosis
treatment_plan:             Recommended treatment
reference_reasoning:        Expert reasoning chain
```

**Why it works for NeuroBench:**
- **3-stage evaluation** (examination → diagnosis → treatment) closely mirrors NeuroBench's action-oriented approach
- `examination_recommendation` is directly analogous to our `optimal_actions` (which tools to order)
- Cases include rare diseases, which could serve as puzzle-difficulty cases
- Published in Nature Communications — high credibility for our NMI paper
- Already structured as JSON files

**What's missing:**
- Actual diagnostic tool outputs (EEG/MRI/labs as structured reports)
- Follow-up outputs
- Hospital-specific protocol compliance
- Difficulty stratification

**Estimated neurology yield:** ~100-150 nervous system cases (1/13 body systems, enriched by rare neurological conditions).

**How to access:**
```bash
git clone https://github.com/MAGIC-AI4Med/MedRBench
# Cases in data/MedRbench/ as JSON files
```

---

### 3.4 Journal of Medical Case Reports (BioMed Central)

**Fully open-access, peer-reviewed neurology case reports.**

| Field | Details |
|-------|---------|
| **What** | World's first PubMed-listed journal devoted exclusively to case reports |
| **Publisher** | BioMed Central (Springer Nature) |
| **URL** | https://jmedicalcasereports.biomedcentral.com/ |
| **Founded** | 2007 |
| **License** | **Fully open access** under BioMed Central terms |
| **Format** | CARE-compliant: Background, Case Presentation, Discussion, Conclusion |
| **Access** | Free browsing; available in PMC as JATS XML |

**Why it works for NeuroBench:**
- **100% open access** — every article is freely available
- Follows CARE (CAse REport) guidelines, which provide semi-structured format
- Available in PMC as machine-readable JATS XML
- Hundreds of neurology case reports since 2007
- Peer-reviewed with editorial oversight

**How to extract:**
```bash
# Use NCBI E-utilities to search for neurology cases
# Example: search JMCR for neurology case reports
esearch -db pmc -query '"J Med Case Rep"[journal] AND "neurology"[MeSH]' | efetch -format xml
```

Or use `pubget` (neuroquery) for bulk download:
```bash
pip install pubget
pubget run --query '"J Med Case Rep"[journal] AND "Nervous System Diseases"[MeSH]' output_dir/
```

---

### 3.5 PMC Open Access Subset (Bulk Neurology Case Reports)

**The foundational raw material — all open-access medical case reports.**

| Field | Details |
|-------|---------|
| **What** | Full-text XML of all open-access articles in PubMed Central |
| **Maintainer** | NIH National Library of Medicine |
| **URL** | https://pmc.ncbi.nlm.nih.gov/tools/openftlist/ |
| **Size** | Millions of articles; neurology case reports in thousands |
| **License** | Individual article licenses (mostly CC-BY or CC-BY-NC) |
| **Formats** | JATS XML, PDF |
| **Access** | FTP bulk download, OAI-PMH API (3 req/sec), BioC API |

**Why it matters:**
- This is the upstream source for MultiCaRe, MedCaseReasoning, and PMC-Patients
- Direct access to full-text XML allows custom extraction pipelines
- Can target specific neurology journals: *Neurology*, *JNNP*, *Journal of Neurology*, *Frontiers in Neurology*, *BMC Neurology*, etc.
- JATS XML has structured sections (case-presentation, discussion, etc.) that can be parsed programmatically

**Access methods:**
```bash
# FTP bulk download (all open-access articles)
wget -r ftp://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/

# OAI-PMH API (targeted queries, 3 requests/second)
curl "https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi?verb=ListRecords&set=neurology&metadataPrefix=pmc"

# BioC API (structured document format)
curl "https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC{id}/unicode"

# pubget (neuroquery) — specialized for neuroscience articles
pip install pubget
pubget run --query '"case report"[pt] AND "Nervous System Diseases"[MeSH]' output_dir/
```

---

### 3.6 PMC-Patients (Tsinghua, 2023)

**Largest structured patient summary dataset.**

| Field | Details |
|-------|---------|
| **What** | Patient summaries extracted from PubMed Central case reports |
| **Authors** | Zhengyun Zhao et al. (Tsinghua University) |
| **Paper** | Scientific Data (2023), arXiv:2202.13876 |
| **GitHub** | https://github.com/pmc-patients/pmc-patients |
| **HuggingFace** | `zhengyun21/PMC-Patients` |
| **Size** | **250,294 patient summaries** + 3.1M patient-article relevance annotations |
| **License** | **CC-BY-NC-SA 4.0** |
| **Access** | Direct download from HuggingFace or Figshare |

**Structure per case:**
```json
{
  "patient_id": "...",
  "patient_uid": "PMID-index",
  "PMID": "...",
  "title": "...",
  "patient": "Free-text patient summary (1-3 paragraphs)",
  "age": [{"value": 45, "unit": "year"}],
  "gender": "M",
  "relevant_articles": {"PMID": score},
  "similar_patients": {"uid": score}
}
```

**Why it works:**
- 250K patient summaries — massive pool for filtering
- Age and gender already extracted
- Patient-patient similarity annotations could help find cases with similar presentations
- Patient-article relevance links back to source literature

**Limitations:**
- **CC-BY-NC-SA** license (non-commercial, share-alike) — more restrictive than CC-BY
- Patient summaries are free text, not structured into exam/history/findings
- No diagnostic test results separated out
- No ground truth actions

**Estimated neurology yield:** ~12,000-25,000 cases (5-10% of 250K).

---

## 4. Tier 2: High-Value Restricted Sources

These sources have excellent clinical depth but require credentialed access, licensing agreements, or careful legal review.

---

### 4.1 MIMIC-IV + Extensions (PhysioNet)

**Richest real-world clinical data — but access-restricted.**

| Field | Details |
|-------|---------|
| **What** | De-identified ICU/hospital EHR data from Beth Israel Deaconess Medical Center |
| **URL** | https://physionet.org/content/mimiciv/3.1/ |
| **Paper** | Scientific Data (2022) |
| **Size** | **364,627 patients**, 546,028 hospitalizations, 94,458 ICU stays |
| **License** | PhysioNet Credentialed Health Data License 1.5.0 |
| **Access** | Requires CITI training + DUA signing (~1-2 weeks approval) |

**What it contains:**
- Demographics, vital signs, lab results (with reference ranges), medications, ICD diagnoses
- Discharge summaries and radiology reports (MIMIC-IV-Note: 331K discharge summaries + 2.3M radiology reports)
- Procedures, microbiology, billing codes

**Neurology-relevant extensions:**
- **DiReCT** (NeurIPS 2024): 511 MIMIC-IV clinical notes with **physician-annotated reasoning chains** — observation text spans linked to diagnoses. https://physionet.org/content/mimic-iv-ext-direct/1.0.0/
- **ER-REASON** (UC Berkeley, 2025): 3,984 ER patients with **longitudinal clinical notes** and 72 expert-authored rationales including rule-out logic. https://physionet.org/content/er-reason/1.0.0/
- **MIMIC-IV-ECG**: ECG waveform data (separate dataset)

**Why it would be valuable:**
- Real ICU neurology cases (stroke, seizures, meningitis, encephalitis, altered mental status)
- Structured labs with reference ranges map directly to our `LabResults` schema
- DiReCT's reasoning annotations map to `key_reasoning_points`
- ER-REASON's multi-stage workflow maps to our action sequence evaluation

**Challenges:**
- Credentialed access (takes 1-2 weeks, requires IRB-like process)
- Heavy ETL required (relational database → NeuroBench JSON)
- Free-text notes need NLP parsing
- No structured EEG/MRI specialist reports (only radiology report text)
- Results cannot be redistributed (would need to share code, not data)

---

### 4.2 Neurology Clinical Reasoning Book (AAN)

**Free PDF, 100% neurology, gold-standard clinical reasoning format.**

| Field | Details |
|-------|---------|
| **What** | Compiled case-based reasoning articles from Neurology journal's Resident & Fellow Section |
| **Editors** | Aaron Berkowitz, Sashank Prasad, Mitchell Elkind |
| **URL** | https://www.neurology.org/pb-assets/rfs-documents/CRbook-1694718270590.pdf |
| **Size** | Hundreds of cases (compiled from submissions: 481 in 2013 → 967 in 2023) |
| **Coverage** | **100% neurology** — uncommon presentations of common disorders + typical presentations of exotic disorders |
| **Access** | **Free PDF download** from neurology.org |
| **License** | Openly distributed by AAN; individual articles have journal copyright but many become open access on PMC after embargo |

**Why it's valuable:**
- **The most directly relevant source** — 100% neurology, focused on diagnostic reasoning
- Cases are designed to teach clinical reasoning, not just present diagnoses
- Format closely mirrors what NeuroBench tests: staged information gathering → differential narrowing → diagnosis
- Free and officially distributed by the American Academy of Neurology
- Used universally in neurology residency training programs

**Challenges:**
- PDF format requires parsing (not machine-readable)
- License for derivative use needs verification with AAN
- Cases are narrative text, not structured JSON

---

### 4.3 JAMA Clinical Challenge (AMA)

**Structured MCQ format with ground truth, already used in LLM benchmarks.**

| Field | Details |
|-------|---------|
| **What** | Interactive diagnostic cases from JAMA Network journals |
| **URL** | https://jamanetwork.com/collections/44038/clinical-challenge |
| **Size** | **1,524 total cases** (815 diagnostic); **~56 from JAMA Neurology** |
| **Structure** | Clinical vignette + MCQ + expert discussion + correct answer |
| **License** | AMA copyright; NOT openly licensed |
| **Access** | Institutional JAMA subscription; researchers have scraped for LLM benchmarks |

**JAMA Neurology cases specifically:**
- Published ~4x/year since May 2015
- Cover: epilepsy, cerebrovascular disease, neurodegeneration, CNS infections, vasculitis
- CME/MOC accredited
- Include imaging and lab values within vignettes

**Precedent for research use:**
- Researchers at Harvard (ChallengeClinicalQA, arXiv:2402.18060) successfully extracted 815 JAMA Clinical Challenge cases for LLM evaluation
- A multi-agent conversational framework study (medRxiv 2025) adapted these cases into agent dialogue format
- GitHub scraper: https://github.com/HanjieChen/ChallengeClinicalQA

**Limitations:**
- Not openly licensed — requires negotiation with AMA for formal research use
- MCQ format (correct answer from choices, not open-ended)
- Only ~56 neurology-specific cases

---

### 4.4 NEJM Case Records of MGH (CPCs)

**The gold standard — but legally inaccessible for direct use.**

| Field | Details |
|-------|---------|
| **What** | Weekly clinicopathological conferences since 1924 |
| **Publisher** | Massachusetts Medical Society |
| **Size** | ~5,000+ total cases; ~302 curated for LLM benchmarks |
| **Quality** | The absolute gold standard in medical case-based learning |
| **License** | **Explicitly prohibits use for AI/ML training without express permission** |

**Why we mention it:**
- Format model for case design (staged reasoning with expert discussion)
- The MedCaseReasoning dataset (Tier 1) was specifically built to avoid NEJM licensing issues while covering similar clinical ground
- Referenced in paper positioning: "Unlike benchmarks derived from NEJM CPCs, NeuroBench cases are sourced from CC-BY licensed PMC case reports..."

**Do NOT use directly.** Reference for format design only.

---

## 5. Tier 3: Component-Specific & Format Models

These sources are useful for specific aspects of NeuroBench cases or as design references.

---

### 5.1 AgentClinic (ICLR 2025)

| Field | Details |
|-------|---------|
| **What** | Multi-agent medical benchmark with doctor-patient dialogue |
| **GitHub** | https://github.com/SamuelSchmidgall/AgentClinic |
| **Paper** | arXiv:2405.07960 |
| **Size** | ~335 cases (215 MedQA + 120 NEJM) |
| **License** | MIT |
| **Use for NeuroBench** | **Format reference** for agent evaluation design. Their bias injection mechanism (cognitive biases for doctor agent) could inform difficulty calibration. Not usable as case source (general medicine, no structured tool outputs). |

### 5.2 DDXPlus (NeurIPS 2022)

| Field | Details |
|-------|---------|
| **What** | 1.3M synthetic patients with differential diagnosis lists |
| **GitHub** | https://github.com/mila-iqia/ddxplus |
| **License** | CC-BY |
| **Use for NeuroBench** | **Differential diagnosis format reference**. Their `[pathology, probability]` pair format for DDx lists is similar to our ground truth differential. Not usable as case source (no neurological conditions in the 49-disease set, fully synthetic). |

### 5.3 BraTS — Brain Tumor Segmentation (CC-BY 4.0)

| Field | Details |
|-------|---------|
| **What** | Annual brain tumor segmentation challenge with multi-parametric MRI |
| **URL** | https://www.synapse.org/brats |
| **Paper** | arXiv:2405.18368 (BraTS 2024) |
| **Size** | 4,500+ MRI cases (glioma, meningioma, metastases, pediatric) |
| **License** | CC-BY 4.0 (BraTS-Africa subset) |
| **Use for NeuroBench** | Could supplement **GLIO-HG cases** with real MRI finding descriptions. Segmentation masks provide ground truth for tumor location, size, and enhancement characteristics that could inform our MRIReport generation. |

### 5.4 EEG-Bench / EEG-FM-Bench (2024-2025)

| Field | Details |
|-------|---------|
| **What** | Benchmarks for EEG foundation models across 14 datasets |
| **Paper** | arXiv:2512.08959 (EEG-Bench), arXiv:2508.17742 (EEG-FM-Bench) |
| **GitHub** | https://github.com/xw1216/EEG-FM-Bench |
| **Use for NeuroBench** | Constituent datasets include clinical EEG from epilepsy, Parkinson's, and other neurological conditions. Could inform realistic EEG finding descriptions for our EEGReport generation. Not directly usable (signal data, not text reports). |

### 5.5 Radiopaedia (CC-BY-NC-SA)

| Field | Details |
|-------|---------|
| **What** | World's largest free radiology resource with 60,000+ cases |
| **URL** | https://radiopaedia.org/ |
| **API** | https://api-docs.radiopaedia.org/ |
| **License** | CC-BY-NC-SA (most content) |
| **Use for NeuroBench** | Excellent neuroradiology reference for realistic MRI finding descriptions. Thousands of brain MRI cases with structured findings, differential, and diagnosis. API available for programmatic access. Limited by NC-SA license and imaging-only scope. |

### 5.6 MedAgentBench (Stanford, NEJM AI 2025)

| Field | Details |
|-------|---------|
| **What** | FHIR-compliant EHR environment for benchmarking medical agents |
| **GitHub** | https://github.com/stanfordmlgroup/MedAgentBench |
| **Paper** | NEJM AI 2025, arXiv:2501.14654 |
| **Size** | 600 tasks, 100 patient profiles, 700K+ data elements |
| **License** | MIT |
| **Use for NeuroBench** | **Competitive positioning reference**. Tests EHR workflow, not diagnostic reasoning. Highlights the gap NeuroBench fills: tool-augmented clinical investigation. |

### 5.7 HealthBench (OpenAI, 2025)

| Field | Details |
|-------|---------|
| **What** | 5,000 health conversations with physician-created evaluation rubrics |
| **HuggingFace** | `openai/healthbench` |
| **Paper** | arXiv:2505.08775 |
| **License** | MIT |
| **Use for NeuroBench** | **Evaluation methodology reference**. Their physician-created rubric approach (48,562 criteria across 7 themes) could inform NeuroBench evaluation design. Not usable as case source (conversational format, no structured cases). |

### 5.8 MedXpertQA (Tsinghua, ICML 2025)

| Field | Details |
|-------|---------|
| **What** | Expert-level board exam questions across 17 specialties |
| **GitHub** | https://github.com/TsinghuaC3I/MedXpertQA |
| **HuggingFace** | `TsinghuaC3I/MedXpertQA` |
| **Size** | 4,460 questions |
| **License** | MIT |
| **Use for NeuroBench** | Multimodal subset includes clinical images + patient records. Could mine neurology questions for case inspiration. Expert-level difficulty aligns with our puzzle-tier cases. |

### 5.9 DiagnosisArena (2025)

| Field | Details |
|-------|---------|
| **What** | 1,113 structured clinical cases from 10 top-tier medical journals (2022-2024) |
| **Paper** | arXiv:2505.14107 |
| **Use for NeuroBench** | Recent, verified, structured cases with **final diagnosis as ground truth**. Expert-AI collaborative verification. ~40 neurology cases. Could serve as additional seed material. Check license terms. |

### 5.10 CaseReportBench (2025)

| Field | Details |
|-------|---------|
| **What** | Benchmark specifically for evaluating LLMs on case report diagnosis |
| **Paper** | arXiv:2505.17265 |
| **Use for NeuroBench** | Recent benchmark from case reports with structured diagnostic evaluation. Could inform our evaluation methodology. |

---

## 6. Not Recommended (with Reasons)

| Source | Why Not |
|--------|---------|
| **CRAFT-MD** | Dermatology only; no neurology cases |
| **MedBench** | Chinese language; exam Q&A format |
| **ClinicalBench** | Prediction tasks (mortality, readmission), not diagnostic reasoning |
| **DermNet** | Dermatology images only |
| **SymCAT** | Knowledge base of symptom-disease probabilities, not patient cases |
| **Path-VQA / SLAKE / VQA-RAD** | Image QA format; small scale; not clinical reasoning |
| **BMJ Case Reports** | Mostly behind paywall (750 GBP APC for OA); some available via PMC |
| **Commercial Q-banks** (UWorld, AMBOSS, Lecturio) | Proprietary, no API, no data export |
| **USMLE Official** | ~100 sample questions (too few); not redistributable |
| **Textbooks** (Case Files, PreTest, Blueprints, etc.) | Commercial copyright; cannot extract or redistribute |
| **Aquifer** | Proprietary platform; only 15 cases; institutional subscription |
| **RITE / ABPN exams** | Proprietary exam content; not accessible |
| **MultiMedBench** (Google) | Not released as a unified dataset; must assemble from components |
| **MedMCQA** | MCQ format; no structured cases; Indian exam focus |
| **PubMedQA** | Literature comprehension, not clinical reasoning |
| **BioASQ** | Information retrieval, not clinical cases |
| **MMLU (medical)** | Knowledge recall MCQs; saturated as a benchmark |

---

## 7. AI Medical Benchmark Landscape

### Positioning NeuroBench in the Field

The field has evolved through four generations:

| Generation | Period | Benchmarks | Tests | Limitation |
|-----------|--------|-----------|-------|-----------|
| **Static MCQ** | 2020-2022 | MedQA, MedMCQA, MMLU | Knowledge recall | No reasoning process; no interaction |
| **Conversational** | 2023-2024 | AgentClinic, CRAFT-MD | Dialogue + diagnosis | No tool use; no structured investigation |
| **EHR Workflow** | 2025 | MedAgentBench | FHIR task completion | No diagnostic reasoning; workflow only |
| **Tool-Augmented Investigation** | 2025 | **NeuroBench (ours)** | Full clinical process | — |

### Detailed Comparison

| Dimension | NeuroBench | AgentClinic | MedAgentBench | CRAFT-MD | HealthBench | MedQA | MedR-Bench |
|-----------|-----------|-------------|---------------|----------|-------------|-------|-----------|
| Agent interaction | ReAct loop (15 turns) | Multi-turn dialogue | FHIR API calls | Dialogue | No | No | No |
| Structured tool use | 7 diagnostic tools | None | FHIR resources | None | None | None | None |
| Specialty depth | Neurology (10 conditions x 3 difficulties) | General (9 specialties) | General medicine | General (12 specialties) | General health | General | General (13 body systems) |
| Protocol compliance | 5 hospitals, 5 countries | No | No | No | No | No | No |
| Reasoning trace evaluation | Full THINK/ACT/OBSERVE/REFLECT | Diagnosis accuracy only | Task completion rate | Diagnosis + history quality | Physician rubric | Answer correctness | Reasoning chain scoring |
| Patient memory | ChromaDB longitudinal | No | No | No | No | No | No |
| Diagnosis format | Open-ended + differential | Open-ended | N/A (not diagnostic) | Open-ended | Open-ended | 4-5 option MCQ | Open-ended |
| Ground truth actions | Optimal + critical + contraindicated | Diagnosis only | Task completion | Diagnosis | Rubric criteria | Correct option | Exam + diagnosis + treatment |
| Difficulty calibration | S/M/P per condition | None | None | None | Consensus/Hard | None | None |
| Case count | 100 (expanding) | ~335 | 600 tasks | ~140 | 5,000 convos | 12,723 | 1,453 |
| License | TBD (CC-BY target) | MIT | MIT | MIT | MIT | MIT | Check |

### What NeuroBench Does That No Other Benchmark Does

1. **Tool-augmented diagnostic investigation** — The agent must call diagnostic tools (EEG, MRI, labs, CSF, ECG, literature search, drug interactions) to gather evidence. No other benchmark has structured tool use for clinical diagnosis.

2. **Hospital-specific protocol compliance** — 5 hospital rule sets (US Mayo, UK NHS, DE Charite, JP Todai, BR HCFMUSP) evaluate whether the agent follows institution-specific clinical pathways. Completely unique.

3. **Longitudinal patient memory** — ChromaDB-based memory system tests whether the agent integrates prior encounters. No other benchmark evaluates this.

4. **Process + outcome evaluation** — Ground truth includes not just the correct diagnosis but optimal action sequences, critical actions, and contraindicated actions. This evaluates HOW the agent reasons, not just WHAT it concludes.

5. **Difficulty stratification within a specialty** — Straightforward/moderate/puzzle cases for each condition test performance across the full difficulty spectrum, not just average accuracy.

### Narrative for the NMI Paper (Methods/Related Work)

> Existing medical AI benchmarks fall into three categories: static knowledge assessments (MedQA, MMLU), conversational evaluations (AgentClinic, CRAFT-MD), and EHR workflow benchmarks (MedAgentBench). None evaluates the complete tool-augmented clinical investigation process — from initial presentation through structured diagnostic tool use to evidence-based diagnosis and treatment planning — within a specialty domain. NeuroBench addresses this gap with 100 neurology cases spanning 10 conditions and 3 difficulty levels, each equipped with 7 diagnostic tool interfaces, 5 hospital-specific protocol engines, and comprehensive ground truth including optimal action sequences, critical actions, and contraindicated actions. Cases are grounded in peer-reviewed clinical case reports from the PMC Open Access Subset, augmented with structured diagnostic outputs to enable tool-based investigation.

---

## 8. Recommended Pipeline: Real Cases to NeuroBench Format

### Overview

```
Step 1: Source Acquisition     → Download neurology cases from Tier 1 sources
Step 2: Filtering              → Select cases matching our 10 conditions
Step 3: Clinical Extraction    → Parse case text into structured patient fields
Step 4: Tool Output Generation → Generate EEG/MRI/labs/CSF/ECG as structured reports
Step 5: Ground Truth Assembly  → Build differential, actions, reasoning points
Step 6: Case Assembly          → Combine into NeuroBench JSON schema
Step 7: Validation             → Run validate_case.py + clinical plausibility checks
```

### Step 1: Source Acquisition

**Primary source: MedCaseReasoning** (best structure, CC-BY)
```python
from datasets import load_dataset

ds = load_dataset("zou-lab/MedCaseReasoning")

# Neurology keyword filter
neuro_keywords = [
    "stroke", "ischemic stroke", "hemorrhagic stroke", "TIA",
    "epilepsy", "seizure", "convulsion",
    "multiple sclerosis", "demyelinating",
    "parkinson", "tremor", "bradykinesia",
    "meningitis", "encephalitis",
    "glioma", "glioblastoma", "brain tumor", "brain mass",
    "alzheimer", "dementia", "cognitive decline",
    "syncope", "loss of consciousness",
    "functional neurological", "conversion disorder",
    "neuropathy", "headache", "migraine",
]

neuro_cases = []
for case in ds["train"]:
    text = (case["case_prompt"] + " " + case.get("final_diagnosis", "")).lower()
    if any(kw in text for kw in neuro_keywords):
        neuro_cases.append(case)

print(f"Found {len(neuro_cases)} neurology cases")
```

**Secondary source: MultiCaRe** (largest volume, CC-BY)
```python
ds = load_dataset("openmed-community/multicare-cases")
# Filter by MeSH terms or taxonomy for nervous system
```

### Step 2: Filtering & Condition Mapping

Map source cases to our 10 NeuroBench conditions:

```python
CONDITION_KEYWORDS = {
    "ischemic_stroke": ["ischemic stroke", "cerebral infarction", "MCA", "basilar", "vertebral"],
    "focal_epilepsy_temporal": ["temporal lobe epilepsy", "focal seizure", "mesial temporal"],
    "multiple_sclerosis": ["multiple sclerosis", "demyelinating", "optic neuritis", "myelitis"],
    "alzheimers_early": ["alzheimer", "early-onset dementia", "amnestic MCI"],
    "parkinsons": ["parkinson", "parkinsonism", "substantia nigra", "lewy body"],
    "brain_tumor_glioma": ["glioma", "glioblastoma", "astrocytoma", "brain tumor", "brain mass"],
    "bacterial_meningitis": ["bacterial meningitis", "pneumococcal meningitis", "meningococcal"],
    "autoimmune_encephalitis_nmdar": ["anti-NMDA", "autoimmune encephalitis", "limbic encephalitis"],
    "functional_neurological_disorder": ["functional neurological", "conversion disorder", "psychogenic"],
    "syncope_cardiac": ["cardiac syncope", "arrhythmia syncope", "cardiogenic syncope"],
}
```

### Step 3: Clinical Extraction

Use Claude to extract structured fields from case text. The prompt:

```
Given this clinical case report, extract the following into JSON:

1. demographics: age, sex, handedness (if mentioned), ethnicity (if mentioned), BMI (if mentioned)
2. chief_complaint: 1-sentence presenting problem
3. history_present_illness: detailed narrative (preserve from source, 150+ words)
4. past_medical_history: list of prior conditions
5. medications: list of {drug, dose, frequency, indication}
6. allergies: list
7. family_history: list
8. social_history: dict of key-value pairs
9. neurological_exam: {mental_status, cranial_nerves, motor, sensory, reflexes, coordination, gait, additional}
10. vitals: {bp_systolic, bp_diastolic, hr, temp, rr, spo2}
11. primary_diagnosis: from the case conclusion
12. key_findings: list of most important clinical and diagnostic findings

If information is not in the source text, generate clinically appropriate values
consistent with the diagnosis and presentation.

Case text:
{case_text}
```

### Step 4: Tool Output Generation

This is the critical step that makes cases "tool-use ready." For each case, generate structured specialist reports that:
- Contain the diagnostic evidence the agent needs
- Are internally consistent with the patient presentation
- Follow the difficulty calibration (straightforward = obvious findings, puzzle = subtle/absent)

This uses the same prompt-based generation we already use for synthetic cases (see `dataset-generation/config/prompt_template.md`), but seeded with the real clinical scenario.

### Step 5: Ground Truth Assembly

From the source case + extracted findings:
- `primary_diagnosis`: from case conclusion
- `icd_code`: lookup from diagnosis
- `differential`: generate 3-5 alternatives with likelihood and distinguishing features
- `optimal_actions`: ordered sequence of clinical steps
- `critical_actions`: must-do actions
- `contraindicated_actions`: must-not-do actions
- `key_reasoning_points`: from MedCaseReasoning's `diagnostic_reasoning` field (if available) or generated

### Step 6: Case Assembly

Combine all components into `NeuroBenchCase` JSON:
```python
from neuroagent_schemas import NeuroBenchCase

case = NeuroBenchCase(
    case_id=f"{condition_abbrev}-{difficulty}{number}",
    condition=condition_enum,
    difficulty=difficulty_enum,
    encounter_type=encounter_type,
    patient=patient_profile,       # from Step 3
    initial_tool_outputs=tool_set, # from Step 4
    followup_outputs=followups,    # from Step 4
    ground_truth=ground_truth,     # from Step 5
    metadata={
        "source": "MedCaseReasoning",
        "source_pmid": pmid,
        "source_license": "CC-BY 4.0",
        ...
    }
)

# Write to file
with open(f"data/neurobench_v1/cases/{case.case_id}.json", "w") as f:
    f.write(case.model_dump_json(indent=2))
```

### Step 7: Validation

```bash
# Pydantic schema validation + clinical plausibility checks
uv run --project dataset-generation python -m neurobench_gen.validate_case data/neurobench_v1/cases/NEW-CASE.json

# Batch validation
for f in data/neurobench_v1/cases/*.json; do
    uv run --project dataset-generation python -m neurobench_gen.validate_case "$f"
done
```

### Metadata Tracking

Each case sourced from external data should include metadata:
```json
{
    "metadata": {
        "version": "1.0",
        "source": "MedCaseReasoning",
        "source_id": "MCR-12345",
        "source_pmid": "PMC7654321",
        "source_license": "CC-BY 4.0",
        "generation_method": "real_case_seed + llm_augmented",
        "generator": "claude-opus-4-6",
        "condition_name": "Relapsing-remitting multiple sclerosis",
        "difficulty_description": "Atypical presentation with OCB-negative CSF",
        "expected_agent_confidence": 0.45
    }
}
```

---

## 9. Reference Table: All Sources at a Glance

| # | Source | Size | Neuro Cases | License | Format | Mapping | Tier |
|---|--------|------|------------|---------|--------|---------|------|
| 1 | **MedCaseReasoning** | 14,489 | ~500+ | CC-BY 4.0 | Structured JSON | HIGH | 1 |
| 2 | **MultiCaRe** | 96,428 | ~3,000+ | CC-BY 4.0 | Structured + images | HIGH | 1 |
| 3 | **MedR-Bench** | 1,453 | ~100+ | PMC-derived | Structured JSON | HIGH | 1 |
| 4 | **JMCR (BioMed Central)** | 1000s | ~200+ | Open Access | PMC XML | MEDIUM | 1 |
| 5 | **PMC OA Subset** | Millions | 1000s | CC-BY/NC | JATS XML | MEDIUM | 1 |
| 6 | **PMC-Patients** | 250,294 | ~15,000+ | CC-BY-NC-SA | JSON | MEDIUM | 1 |
| 7 | **MIMIC-IV** | 364,627 pts | 1000s | PhysioNet | Relational DB | HIGH | 2 |
| 8 | **DiReCT** | 511 | ~50+ | PhysioNet | Annotated notes | HIGH | 2 |
| 9 | **ER-REASON** | 3,984 | ~500+ | PhysioNet | Longitudinal notes | MEDIUM | 2 |
| 10 | **AAN Clinical Reasoning** | 100s | **ALL** | Free PDF | PDF | HIGH | 2 |
| 11 | **JAMA Clinical Challenge** | 1,524 | ~56 | Copyright | Web/scraped | MEDIUM | 2 |
| 12 | **NEJM CPCs** | 5,000+ | ~300+ | Copyright | Web | HIGH (format only) | 2 |
| 13 | **AgentClinic** | 335 | Few | MIT | JSONL | LOW | 3 |
| 14 | **DDXPlus** | 1.3M | 0 | CC-BY | CSV/JSON | LOW | 3 |
| 15 | **BraTS** | 4,500+ MRIs | ALL | CC-BY 4.0 | NIfTI | LOW (MRI only) | 3 |
| 16 | **EEG-Bench** | 14 datasets | Some | Various | Signal data | LOW (EEG only) | 3 |
| 17 | **Radiopaedia** | 60,000+ | 1000s | CC-BY-NC-SA | Web/API | LOW (imaging only) | 3 |
| 18 | **MedAgentBench** | 600 tasks | Few | MIT | FHIR | Positioning only | 3 |
| 19 | **HealthBench** | 5,000 convos | Few | MIT | JSON | Methodology only | 3 |
| 20 | **MedXpertQA** | 4,460 | Some | MIT | JSON | LOW | 3 |
| 21 | **DiagnosisArena** | 1,113 | ~40 | Check | JSON | MEDIUM | 3 |
| 22 | **DeepRare** | 6,401 | Some | Check | — | Positioning only | 3 |

---

## 10. Citations & URLs

### Tier 1 Sources

- **MedCaseReasoning**: Wu K, Zou J. "MedCaseReasoning: Evaluating Diagnostic Reasoning in Clinical Case Reports." arXiv:2505.11733 (2025). GitHub: https://github.com/kevinwu23/Stanford-MedCaseReasoning | HF: `zou-lab/MedCaseReasoning`

- **MultiCaRe**: Nievas Offidani M, et al. "MultiCaRe: A multimodal case report dataset." Data in Brief (2024). GitHub: https://github.com/mauro-nievoff/MultiCaRe_Dataset | HF: `openmed-community/multicare-cases` | Zenodo: https://zenodo.org/records/10079370

- **MedR-Bench**: MAGIC-AI4Med. "MedR-Bench: Benchmarking LLM reasoning abilities on clinical cases." Nature Communications (2025). https://doi.org/10.1038/s41467-025-64769-1 | GitHub: https://github.com/MAGIC-AI4Med/MedRBench

- **PMC-Patients**: Zhao Z, et al. "PMC-Patients: A Large-scale Dataset of Patient Summaries and Relations for Benchmarking Retrieval-Based Clinical Decision Support Systems." Scientific Data (2023). arXiv:2202.13876. HF: `zhengyun21/PMC-Patients` | GitHub: https://github.com/pmc-patients/pmc-patients

- **PMC Open Access Subset**: https://pmc.ncbi.nlm.nih.gov/tools/openftlist/ | OAI-PMH: https://pmc.ncbi.nlm.nih.gov/tools/oai/ | FTP: https://pmc.ncbi.nlm.nih.gov/tools/ftp/

- **Journal of Medical Case Reports**: https://jmedicalcasereports.biomedcentral.com/

### Tier 2 Sources

- **MIMIC-IV**: Johnson A, et al. "MIMIC-IV, a freely accessible electronic health record dataset." Scientific Data (2023). https://physionet.org/content/mimiciv/3.1/

- **DiReCT**: Wang B, et al. "DiReCT: Diagnostic Reasoning for Clinical Notes." NeurIPS 2024 D&B. https://physionet.org/content/mimic-iv-ext-direct/1.0.0/ | GitHub: https://github.com/wbw520/DiReCT

- **ER-REASON**: Alaa Lab (UC Berkeley). "ER-REASON: Emergency Room Clinical Reasoning." https://physionet.org/content/er-reason/1.0.0/ | GitHub: https://github.com/AlaaLab/ER-Reason | arXiv:2505.22919

- **Neurology Clinical Reasoning Book**: AAN Resident & Fellow Section. Free PDF: https://www.neurology.org/pb-assets/rfs-documents/CRbook-1694718270590.pdf

- **JAMA Clinical Challenge**: https://jamanetwork.com/collections/44038/clinical-challenge | Scraper: https://github.com/HanjieChen/ChallengeClinicalQA | arXiv:2402.18060

- **NEJM CPCs**: https://www.nejm.org/browse/nejm-article-type/case-records-of-the-massachusetts-general-hospital

### Tier 3 Sources

- **AgentClinic**: Schmidgall S, et al. "AgentClinic: a multimodal agent benchmark to evaluate AI in simulated clinical environments." arXiv:2405.07960 (ICLR 2025). GitHub: https://github.com/SamuelSchmidgall/AgentClinic

- **MedAgentBench**: Chen E, et al. "MedAgentBench: Benchmarking Medical LLM Agents." NEJM AI (2025). arXiv:2501.14654. GitHub: https://github.com/stanfordmlgroup/MedAgentBench

- **CRAFT-MD**: Rajpurkar Lab. "CRAFT-MD." Nature Medicine (2025). GitHub: https://github.com/rajpurkarlab/craft-md

- **MedAgentsBench**: Gerstein Lab, Yale. arXiv:2503.07459. GitHub: https://github.com/gersteinlab/medagents-benchmark

- **HealthBench**: OpenAI. arXiv:2505.08775. HF: `openai/healthbench`

- **MedXpertQA**: Tsinghua C3I. arXiv:2501.18362 (ICML 2025). GitHub: https://github.com/TsinghuaC3I/MedXpertQA

- **DDXPlus**: Tchango A, et al. "DDXPlus." NeurIPS 2022 D&B. arXiv:2205.09148. GitHub: https://github.com/mila-iqia/ddxplus

- **BraTS**: arXiv:2405.18368 (BraTS 2024). https://www.synapse.org/brats

- **EEG-Bench**: arXiv:2512.08959. **EEG-FM-Bench**: arXiv:2508.17742. GitHub: https://github.com/xw1216/EEG-FM-Bench

- **Radiopaedia**: https://radiopaedia.org/ | API: https://api-docs.radiopaedia.org/

- **DiagnosisArena**: arXiv:2505.14107

- **DeepRare**: Nature (2025). https://doi.org/10.1038/s41586-025-10097-9

- **CaseReportBench**: arXiv:2505.17265

- **CSEDB**: npj Digital Medicine (2025). https://doi.org/10.1038/s41746-025-02277-8

- **MedQA**: Jin D, et al. "What Disease Does This Patient Have?" Applied Sciences (2021). arXiv:2009.13081. GitHub: https://github.com/jind11/MedQA

- **MedMCQA**: Pal A, et al. arXiv:2203.14371. HF: `openlifescienceai/medmcqa`

- **RareBench**: Chen X, et al. KDD 2024. GitHub: https://github.com/chenxz1111/RareBench

### Tools

- **pubget** (neuroquery): https://github.com/neuroquery/pubget — bulk download neuroscience articles from PMC
- **multiversity** (MultiCaRe): Python package for creating custom subsets from MultiCaRe dataset
- **BioC API**: https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/ — structured document access for PMC articles
