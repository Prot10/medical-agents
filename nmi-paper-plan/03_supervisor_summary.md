# NeuroAgent — Project Summary for Supervisor and Clinical Collaborators

## What We Want to Build

An AI system that acts as an intelligent clinical assistant for neurologists. The system doesn't replace the doctor — it reasons through patient cases the way a junior neurologist would: reviewing the clinical history, ordering the right tests in the right sequence, interpreting results across modalities (EEG, MRI, labs, etc.), synthesizing everything into a coherent clinical picture, and suggesting a diagnosis with recommended next steps. The doctor always has the final word.

The system is built on open-source large language models (Qwen3 and/or MedGemma) and is designed to be transparent — every decision comes with a full reasoning chain explaining why.

---

## What Makes This Different from Existing Work

Current AI systems for medicine are either chatbots that answer questions from text (like ChatGPT answering medical queries), or specialized models that analyze one data type (an AI that reads chest X-rays, or an AI that classifies EEG). Nobody has built a system that does what a real neurologist does: look at the EEG, look at the MRI, read the lab results, remember what happened at the last visit, follow the hospital's protocols, and put it all together.

Our system is the first to combine all of these in one integrated agent:

| Capability | Current AI Systems | NeuroAgent |
|---|---|---|
| Answer medical questions from text | Yes (ChatGPT, Med-PaLM) | Yes |
| Analyze brain imaging | Separate specialized models | Integrated as a tool the agent calls |
| Analyze EEG | Separate specialized models | Integrated as a tool the agent calls |
| Reason across multiple data types simultaneously | No | Yes — the core contribution |
| Decide what test to order next | No — they analyze what they're given | Yes — the agent actively requests information |
| Remember prior patient encounters | No | Yes — longitudinal patient memory |
| Follow hospital-specific protocols | No | Yes — configurable rules engine |

---

## How It Works (Non-Technical Summary)

Think of the system as a very organized junior doctor that has access to specialist consultants:

1. **The patient arrives.** The doctor gives the system the basic information — chief complaint, history, whatever data is available.

2. **The system reviews and plans.** It reads the clinical information and thinks: "This looks like it could be X, Y, or Z. To distinguish them, I need an EEG, an MRI, and these lab tests."

3. **The system calls specialists (tools).** It sends the EEG to an EEG specialist, the MRI to a radiologist, the labs to a pathologist. Each specialist returns a detailed report.

4. **The system synthesizes.** It reads all the reports together and reasons: "The EEG shows a right temporal focus, the MRI shows a right temporal lesion, and the labs are normal. These all point to the same thing — focal epilepsy from a structural lesion."

5. **The system recommends.** It suggests a diagnosis (with confidence level and alternatives), recommends treatment (checking the hospital's formulary and drug interactions), and flags what to do next.

6. **The system remembers.** When the patient comes back in 3 months, the system recalls everything from the first visit and tracks whether the patient is getting better or worse.

The "specialists" (tools) in our research prototype are simulated — we pre-generate realistic reports that match the patient's condition. This lets us test whether the reasoning system works correctly without needing to build perfect EEG or MRI analysis models (which is a separate, much harder problem).

---

## Why Neurology?

Neurology is an ideal testing ground for this kind of system for several reasons. It is inherently multimodal — a typical neurology workup involves EEG, MRI, clinical examination, lab tests, and sometimes fMRI, EMG, or CSF analysis. There is no single test that gives the answer; the diagnosis emerges from integrating multiple data sources. Neurology cases often require sequential reasoning, where each test result changes what the next step should be. And the field has excellent public datasets (Temple University Hospital EEG Corpus, ADNI for Alzheimer's imaging, OASIS for brain MRI) that we can use for validation.

---

## What We Need from Clinical Collaborators

We need neurologist involvement at three levels:

**Level 1 — Case Validation (minimal, ~2 hours/month):**
Review a sample of our generated patient cases. Are they clinically realistic? Would a real patient present this way? Are the mock tool outputs (EEG reports, MRI reports) what you'd actually see?

**Level 2 — Agent Output Evaluation (~4 hours/month):**
Review the agent's reasoning chains and recommendations on a sample of cases. Is the reasoning sound? Would you agree with the diagnosis? Are the recommendations safe? Where does it go wrong?

**Level 3 — Co-authorship and Deep Collaboration (ongoing):**
Help design the clinical scenarios. Provide clinical expertise for the paper's introduction and discussion. Review the paper draft for clinical accuracy. Potentially: provide de-identified real cases for validation (with IRB approval).

Any level of involvement is valuable. Level 1 alone would significantly strengthen the work.

---

## Research Target

We aim to publish in **Nature Machine Intelligence** — one of the top journals at the intersection of AI and its applications. This journal has published the foundational papers on medical AI agents, and our work would be a direct and significant advance on that body of work.

The paper will include the full system design, a benchmark of 500+ neurology cases, comprehensive evaluation (diagnostic accuracy, robustness analysis, memory evaluation, protocol compliance), and detailed clinical case walkthroughs.

---

## Timeline

- **Months 1-5**: Build the system and generate the benchmark
- **Months 6-10**: Run all experiments and analysis
- **Month 11**: Expert clinical validation (this is where neurologist involvement is most critical)
- **Months 12-14**: Write and submit the paper
- **Months 15-20**: Review process, revisions, acceptance

---

## Frequently Asked Questions

**Q: Does this system use real patient data?**
No. All patient cases are synthetically generated. If we later validate on real cases (with a hospital partnership), that would require IRB approval and full de-identification.

**Q: Could this actually be used in a hospital?**
Not in its current form — this is a research prototype. But the architecture is designed so that real analysis models (for EEG, MRI, etc.) can be plugged in later. The path from research to deployment would require extensive clinical validation, regulatory approval, and real-world testing.

**Q: What if the AI makes a wrong diagnosis?**
The system always presents a ranked differential diagnosis with confidence levels, never a single definitive answer. It explicitly flags uncertainty. And critically, the doctor always makes the final decision — the system is a support tool, not an autonomous actor.

**Q: Why simulate the specialist tools instead of using real AI models?**
Two reasons. First, it lets us test the reasoning system in isolation — we can tell whether errors come from bad reasoning or bad tools. Second, it lets us systematically study how the system behaves when tools give imperfect results, by injecting controlled amounts of noise. This would be impossible with a black-box real model.

**Q: What open-source models are you using?**
We plan to compare several open-source large language models as the core reasoning engine: Qwen3-32B (Alibaba, strong reasoning), MedGemma 27B (Google, medical-domain pre-trained), and OpenBioLLM-70B (Llama-3 based, biomedical fine-tuned). All are freely available for research.

**Q: How is this different from just asking ChatGPT about a patient?**
Three fundamental differences. First, ChatGPT doesn't call specialized tools — it guesses based on text. Our system calls dedicated models for EEG, MRI, etc., and reasons over their structured outputs. Second, ChatGPT has no memory — every conversation starts from scratch. Our system maintains a longitudinal patient record. Third, ChatGPT doesn't follow hospital protocols — our system has a configurable rules engine that ensures compliance with institutional guidelines. And fourth, our system decides what information it needs and actively requests it, rather than passively answering questions about data it's been given.
