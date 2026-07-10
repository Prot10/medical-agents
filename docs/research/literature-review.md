# Literature Review: Agentic AI Systems for Clinical Decision Support in Neurology

## 1. Introduction

The convergence of large language models (LLMs), multi-agent systems, and medical imaging analysis has opened new frontiers in clinical decision support. This literature review examines the state of the art in agentic AI systems for healthcare, with a particular focus on neurology, to identify gaps and opportunities for a PhD research project building a comprehensive medical agent system.

---

## 2. LLM-Based Agentic Systems in Medicine

### 2.1 Foundational Frameworks

The seminal review by **Qiu et al. (2024)** in *Nature Machine Intelligence* established the conceptual framework for LLM-based agentic systems in medicine. They identify five core capabilities: processing input information, planning and deciding, recalling and reflecting, interacting and collaborating, and leveraging tools to act. This taxonomy has become the reference point for subsequent work.

A comprehensive follow-up review in *npj Artificial Intelligence* (2026) systematically examined applications across assisted diagnosis, clinical decision support, medical report generation, patient-facing chatbots, healthcare system management, and medical education. The authors propose seven critical future directions including integration with embodied systems, hybrid expert models, expanded evaluation paradigms, and safety/controllability assurance.

A systematic review of AI agents in clinical medicine (2024–2025) analyzed 20 studies meeting rigorous inclusion criteria and found that **multi-agent systems can mitigate clinical decision biases**, improving accuracy from 0% to 76% on bias-containing complex cases and surpassing human physicians by 21%.

### 2.2 MDAgents (NeurIPS 2024 — Oral)

**MDAgents** (Kim et al., MIT Media Lab) is the most prominent multi-agent medical framework to date, receiving an oral presentation at NeurIPS 2024. The framework introduces an adaptive collaboration structure with four stages:

1. **Medical Complexity Check** — categorizes queries as low, moderate, or high complexity
2. **Expert Recruitment** — activates a Primary Care Clinician (PCC) for simple cases, a Multi-disciplinary Team (MDT), or an Integrated Care Team (ICT) for complex cases
3. **Analysis and Synthesis** — uses Chain-of-Thought, Self-Consistency, and multi-agent consensus
4. **Decision-making** — synthesizes all inputs for a final answer

MDAgents demonstrated best performance on 7 out of 10 medical benchmarks, outperforming single-agent approaches by 7.2% and other multi-agent methods by 9.5% on DDXPlus. The moderator review plus external medical knowledge led to an average accuracy improvement of 11.8%.

**Relevance to our project**: MDAgents focuses on text-based reasoning and lacks multimodal tool use (imaging, signals). Our system extends this paradigm by incorporating specialized tool-calling for EEG, MRI, fMRI analysis.

### 2.3 Other Notable Agent Systems

- **KG4Diagnosis** — Hierarchical multi-agent LLM framework enhanced with Knowledge Graphs for structured medical diagnosis
- **Zodiac** — A cardiologist-level LLM framework for multi-agent cardiac diagnostics
- **Healthcare Agent** (npj AI, 2025) — Features three components: a dialogue component for planning safe conversations, a memory component for patient history, and a processing component for report generation. Closely related to our proposed architecture.
- **Agentic AI Framework for End-to-End Medical Data Inference** (arXiv 2025) — Automates the entire clinical data pipeline from ingestion to inference through modular, task-specific agents

### 2.4 Key Insights from Existing Work

| Aspect | Current State | Gap |
|--------|--------------|-----|
| Multi-agent collaboration | Well-established (MDAgents, KG4Diagnosis) | Most focus on text-only reasoning |
| Tool use | Emerging (web search, knowledge bases) | No integration with signal/imaging analysis tools |
| Memory systems | Basic (Healthcare Agent) | No longitudinal patient memory across encounters |
| Hospital-specific rules | Not addressed | No rule-based governance layer |
| Neurology-specific | Very limited | No dedicated neurology agent system |

---

## 3. Medical LLMs: Open-Source Landscape

### 3.1 MedGemma (Google, 2025)

MedGemma is Google's suite of open, medically-tuned vision-language models built on Gemma 3:

- **MedGemma 4B** (pre-trained and instruction-tuned variants)
- **MedGemma 27B Multimodal** — pre-trained on medical images, records, and comprehension tasks
- **MedGemma 27B Text-only** — optimized for inference-time reasoning
- **MedGemma 1.5 4B** (Jan 2026) — improved text reasoning and 2D image interpretation

Training data includes chest X-rays, dermatology, ophthalmology, histopathology images, FHIR-based EHR data, and lab reports. The 27B text variant scores **87.7% on MedQA** (within 3 points of DeepSeek R1 at ~1/10th inference cost). A board-certified radiologist review found 81% of MedGemma chest X-ray reports would lead to similar patient management.

**Strengths**: Multimodal (text + 2D/3D images), deployable on a single GPU, compatible with agent pipelines.
**Limitations**: No EEG/ECG time-series support, not fine-tuned for neurology specifically.

### 3.2 Qwen3 (Alibaba, 2025)

Qwen3 is a family of open-source LLMs spanning 0.6B to 235B parameters:

- **Qwen3-32B** achieves **87.1% on MedQA** when fine-tuned with supervised fine-tuning + reinforcement learning (Gazal-R1)
- Qwen3 reasoning models consistently outperform their weight class on medical benchmarks
- Parameter-efficient fine-tuning with DoRA and rsLoRA enables domain adaptation without full retraining

**Strengths**: Strong reasoning, efficient fine-tuning, multiple size options, excellent multilingual support.
**Limitations**: Not specifically medical-domain trained, no native multimodal medical capabilities.

### 3.3 BioMistral (2024)

Built on Mistral-7B, further pre-trained on PubMed Central:

- 9.6% and 11.1% improvement over MediTron-7B on MedQA (4 and 5 options)
- Competitive with larger proprietary models despite small size

**Strengths**: Lightweight, biomedical domain-specific pre-training.
**Limitations**: Only 7B parameters, text-only, not designed for agent use.

### 3.4 OpenBioLLM (2024)

Based on Llama-3, available in 8B and 70B variants:

- OpenBioLLM-70B achieves **86.06% average** across 9 biomedical datasets
- Outperforms GPT-4, Gemini, Meditron-70B, Med-PaLM-1 & Med-PaLM-2

**Strengths**: State-of-the-art open-source medical performance.
**Limitations**: Large model size (70B), text-only.

### 3.5 Model Comparison Summary

| Model | Size | MedQA Score | Multimodal | Open-Source | Medical Pre-training |
|-------|------|-------------|------------|-------------|---------------------|
| MedGemma 27B (text) | 27B | 87.7% | Yes (separate variant) | Yes | Yes (extensive) |
| Qwen3-32B (Gazal-R1) | 32B | 87.1% | No (native) | Yes | Fine-tuned |
| OpenBioLLM-70B | 70B | ~86% avg | No | Yes | Yes |
| BioMistral-7B | 7B | ~55% | No | Yes | Yes (PubMed) |
| Meditron-70B | 70B | ~70% | No | Yes | Yes |

---

## 4. Multimodal Medical AI: Imaging and Signals

### 4.1 LLMs for Brain MRI

A 2025 study in *Diagnostics* evaluated GPT-4o, Grok, and Gemini on 35,711 brain MRI slices. Performance was found to be "not yet adequate to rely on," with GPT-4o being superior. This motivates our approach of using **specialized models as tools** rather than relying on the LLM for direct image interpretation.

The **RadFM**, **MedBLIP**, and **M3D-LaMed** systems represent the state of the art in multimodal radiology models. M3D-LaMed combines a 3D ViT with a perceiver and downstream LLM for report generation, VQA, retrieval, and segmentation — functioning as a multitask agent.

### 4.2 LLMs for ECG Analysis

The ECG-LLM landscape is advancing rapidly (survey in *Artificial Intelligence Review*, June 2025):

- **ECGChat** — multimodal LLM bridging ECG waveforms and textual cardiology reports
- **Zero-shot retrieval-augmented diagnosis** — LLMs retrieve expert knowledge from curated databases to analyze ECG data without extensive prior training
- Contrastive learning approaches for zero-shot report retrieval

### 4.3 LLMs for EEG Analysis

A comprehensive survey and taxonomy (arXiv, June 2025) identifies four categories of LLM use in EEG:

1. **LLM-inspired foundation models for EEG** — pre-trained on large EEG corpora
2. **EEG-to-language decoding** — translating brain signals to text
3. **Cross-modal approaches** — aligning EEG representations with language embeddings
4. **Zero/few-shot prompting** — leveraging domain-specific cues for brain signal analysis

EEG foundation models have been trained on the full TUH corpus (541k channel-hours), using 22 channels in the standard 10-20 layout. Key benchmarks include AdaBrain-Bench and EEG-FM-Bench (both 2025).

### 4.4 Synthetic Medical Image Generation

Recent advances in synthetic generation relevant to our dataset creation:

- **Diffusion models for brain MRI**: DDPMs generate synthetic 3D T1-weighted brain MRI images; diffusion-generated images outperform GAN-generated for training segmentation models
- **EEG-to-fMRI generation**: Diffusion-based models significantly outperform GANs and transformers for cross-modal generation
- **DreamDiffusion** (2024): Pre-trained text-to-image diffusion conditioned on EEG temporal masking
- Brain studies represent 22% of GAN-based healthcare synthetic data research

---

## 5. Evaluation Benchmarks for Medical Agents

### 5.1 AgentClinic (2024)

A multimodal agent benchmark for simulated clinical environments featuring patient interactions, multimodal data collection under incomplete information, and tool usage across 9 medical specialties and 7 languages. Solving problems in AgentClinic's sequential decision-making format is considerably harder than static QA, with diagnostic accuracy dropping to below 1/10th of static accuracy.

Two variants exist:
- **AgentClinic-NEJM** — multimodal image and dialogue environment
- **AgentClinic-MedQA** — dialogue-only, grounded in USMLE cases

### 5.2 MedAgentBench (Stanford/NEJM AI, 2025)

Evaluates LLM agent capabilities within medical records contexts:
- 300 patient-specific clinically-derived tasks across 10 categories
- Realistic profiles of 100 patients with over 700,000 data elements
- FHIR-compliant interactive environment

### 5.3 MedAgentGym (2025)

The first publicly available training environment for coding-based medical reasoning in LLM agents, designed to enhance biomedical research capabilities.

---

## 6. Public Neurology Datasets

### 6.1 EEG Datasets

- **TUH EEG Corpus** — 14 years of clinical EEG data from Temple University Hospital with clinician reports
  - **TUAB** (Abnormal EEG Corpus): 3,000 EEGs labeled normal/abnormal by neurologists
  - **TUEP** (Epilepsy Corpus): 100 epilepsy + 100 control subjects
  - **TUAR** (Artifact Corpus): annotations of 5 artifact types
- **BCI Datasets** (2024-2025): Motor imagery datasets for stroke patients with portable EEG devices

### 6.2 Brain Imaging Datasets

- **ADNI** (Alzheimer's Disease Neuroimaging Initiative): Longitudinal multicenter study with MRI, PET, genetic, CSF biomarkers; 800+ subjects across MCI, early AD, and controls
- **OASIS-3**: 2,000+ MR sessions with structural and functional sequences (ASL, BOLD, DTI, SWI, FLAIR) for aging and Alzheimer's research
- **OASIS-4**: MR, clinical, cognitive, and biomarker data for memory complaint patients

### 6.3 Neurology EHR Data

- **NeuroDiscovery AI Database** (medRxiv, 2025): 355,791 patients from US outpatient neurology practices, with 14,797 diagnosis codes, spanning 15 years (2008-2024). One of the largest neurology-focused EHR datasets.
- **MIMIC-IV**: While not neurology-specific, contains ICU records including neurological assessments

---

## 7. Synthetic Data Generation in Healthcare

### 7.1 Current Approaches

- **LLM-based generation**: GPT-4o with zero-shot prompting for tabular clinical data (Barr et al., Frontiers in AI, 2025)
- **GAN-based approaches**: Deep-CTGANs with ResNet for robust minority class generation
- **Diffusion models**: DDPMs for 3D brain MRI, outperforming GANs in downstream tasks
- **Privacy-preserving pipelines**: DataSifter and Synthetic Data Vault (SDV) with CTGAN and Gaussian Copula methods

### 7.2 Neurology as a Target Domain

The scoping review by Rujas et al. (2025) identifies **neurology as one of the top three domains** for synthetic medical data generation, alongside oncology and cardiology. Key motivations include: privacy preservation, data augmentation for rare diseases, and balancing class distributions.

### 7.3 Gaps in Synthetic Neurology Data

- No end-to-end framework for generating coherent multi-modal patient profiles (EEG + MRI + clinical reports + diagnosis)
- Cross-modal consistency (e.g., EEG abnormalities matching MRI findings matching clinical reports) is an unsolved challenge
- Rare neurological conditions (e.g., Creutzfeldt-Jakob disease, autoimmune encephalitis) have virtually no synthetic data pipelines

---

## 8. Identified Research Gaps

Based on this review, we identify the following critical gaps that our PhD project aims to address:

1. **No comprehensive neurology-focused agentic system** — existing agent frameworks are either general-purpose (MDAgents) or cardiology-specific (Zodiac), with no dedicated neurology agent
2. **No tool-augmented agent for multimodal neurological data** — no system integrates EEG analysis, brain MRI interpretation, fMRI analysis, and clinical report understanding as callable tools within an agent framework
3. **No agent with longitudinal patient memory** — existing systems lack persistent memory across patient encounters
4. **No hospital-rule-aware agent** — no system incorporates institutional protocols and guidelines as constraints on reasoning
5. **No coherent synthetic neurology dataset** — while individual modalities can be generated synthetically, no framework produces cross-modally consistent patient profiles
6. **Limited evaluation in sequential clinical settings** — AgentClinic shows that agent performance drops dramatically in realistic sequential decision-making; neurology-specific evaluation is absent

---

## 9. Conclusion

The field of agentic medical AI is rapidly evolving, with multi-agent collaboration, tool use, and multimodal integration as key trends. However, significant gaps remain in neurology-specific systems, multimodal tool integration, longitudinal memory, and institutional rule compliance. Our proposed system — NeuroAgent — aims to address these gaps by building a comprehensive, tool-augmented, memory-enabled agent system for neurological decision support, powered by open-source LLMs.

**Evaluation approach**: Rather than training real specialized models for each modality (which is a separate research problem), we evaluate the agentic reasoning framework using mock tool outputs — clinically realistic, pre-generated results that simulate what real models would return. This decouples reasoning evaluation from model accuracy and enables controlled robustness testing through noise injection. See `nmi-paper-plan/` for the full paper strategy and implementation plan.
