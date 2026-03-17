# NeuroAgent Improvement Plan

Status: March 2026 — post-v3 audit and initial Qwen3.5-9B benchmark results.

## Current State

### What's Working
- **Tool-augmented reasoning provides clear benefit**: +18% top-1 accuracy (56% vs 38%) and +0.17 composite score (0.73 vs 0.56) across all difficulty levels
- **v3 realistic tool outputs successfully test genuine reasoning**: stripping interpretive fields forced the agent to synthesize findings rather than read answers
- **Hospital protocol system is well-structured**: 5 hospitals × 5 pathways, rules injected into system prompt
- **LLM judge evaluation correlates with clinical assessment**: 8-dimension rubric captures nuances that automated metrics miss
- **Evidence identification is strong** (4.20/5 in react mode): the agent reads tool outputs well
- **Safety failures are omissions, not commissions**: the model rarely recommends harmful actions

### What Needs Improvement
- **40% consistency** (6/15 cases produce same diagnosis across 3 repeats) — insufficient for clinical deployment
- **Red herring handling** is the weakest dimension (2.71/5) — the model is easily misled by confounders
- **Dual pathology blind spot**: FND-P03 (FND on MS) scored 0/3 in both modes — the model cannot hold two diagnoses simultaneously
- **Atypical presentations of common diseases** are more dangerous than rare diseases with classic presentations (BACT-MEN-RS01)
- **Negative result interpretation**: the model treats negative tests (normal OCBs, nonspecific MRI) as disconfirming rather than weighting against base rates
- **Protocol compliance is measured but not optimized**: the metric is now wired up but performance hasn't been evaluated systematically
- **Automated metrics have a critical bug**: `safety_score` is always 0.0 because `critical_actions` are free-text descriptions, not tool names — the set intersection is empty

---

## Priority 1: Blocking for NMI Submission

### 1.1 Fix automated safety/critical action metrics — DONE
**Problem**: `MetricsCalculator._compute_safety_score()` compared tool names against free-text descriptions, producing 0.0 on every case.

**Solution implemented**: Semantic matching in `metrics.py` using two complementary strategies:
1. **Tool-to-action mapping**: A keyword dictionary maps each tool name to clinical terms (e.g., `analyze_csf` → ["lumbar puncture", "spinal tap", "csf"]). If a critical action mentions LP and the agent called `analyze_csf`, it counts as a hit.
2. **Response-text matching**: Extracts distinctive clinical terms from the action description and checks if ≥50% appear in the agent's final response. This catches actions like "administer IV alteplase" that aren't tool calls but recommendations.
3. **Contraindicated action detection**: Sentence-level analysis that distinguishes positive recommendations ("I recommend starting heparin") from negations ("defer anticoagulation", "avoid heparin"). Only positive mentions trigger a violation.

New fields added to `CaseMetrics`: `critical_actions_detail` and `contraindicated_actions_detail` (dict mapping each action text to hit/violated bool) for transparency.

### 1.2 Complete the 4-model benchmark on v3
**Status**: Qwen3.5-9B complete (90 runs). MedGemma-4B and Qwen3.5-27B pending.

**Action**: Run `./agent-platform/scripts/run_v3_full.sh --skip-phase qwen9b`

**Effort**: ~8 hours GPU time
**Impact**: Enables the paper's main results table

### 1.3 Run v1-vs-v3 ablation
**Problem**: Need to quantify how much interpretive tool outputs inflate accuracy.

**Action**: Run the same 15 cases with `--dataset v1` and compare to v3 results.

**Effort**: ~4 hours GPU time
**Impact**: Key ablation result for the paper — demonstrates why realistic tool outputs matter

### 1.4 LLM judge all model results
**Action**: After each model completes, run the LLM judge evaluation (as done for Qwen3.5-9B).

**Effort**: 2-3 hours per model (Claude API calls)
**Impact**: Enables per-dimension analysis across models

---

## Priority 2: Improving Agent Performance

### 2.1 Improve consistency via self-consistency decoding
**Problem**: 40% consistency rate means the model gives different diagnoses to the same patient on different runs.

**Approach**: Run N independent inferences (N=3-5), extract the primary diagnosis from each, and select by majority vote. This is an inference-time technique that doesn't require retraining.

**How to implement**:
1. Add a `self_consistency_runs: int = 1` parameter to `AgentConfig`
2. In `AgentOrchestrator.run()`, when `self_consistency_runs > 1`:
   - Run the case N times with the same inputs (temperature sampling provides diversity)
   - Extract `### Primary Diagnosis` from each trace
   - Use majority vote: pick the diagnosis that appears most frequently
   - Return the trace corresponding to the majority diagnosis (preserving the full reasoning chain)
3. For ties, prefer the diagnosis with higher stated confidence
4. Add `consistency_score: float` to `CaseMetrics` = (majority count / N)

**Where in the code**: `agent-platform/src/neuroagent/agent/orchestrator.py`, method `run()`
**Expected impact**: +10-15% consistency, +5-10% accuracy based on self-consistency literature (Wang et al., 2023)
**Effort**: 1 day implementation + testing

### 2.2 Train on dual pathology cases
**Problem**: The model cannot diagnose two conditions simultaneously (e.g., FND-P03: FND on MS, FEPI-TEMP-P03: PNES + real epilepsy).

**How to implement**:
1. Create 15-20 dual-pathology training cases across conditions:
   - FND + organic disease (MS, epilepsy, stroke)
   - PNES + true epilepsy (the case exists: FEPI-TEMP-P03)
   - Dementia + delirium
   - Drug-induced parkinsonism + idiopathic PD
2. For each training case, the GRPO reward function should require:
   - Both diagnoses mentioned in `### Primary Diagnosis` (e.g., "FND superimposed on stable RRMS")
   - Explicit distinction between old stable findings and new acute findings
   - The differential should NOT contain only one of the two diagnoses
3. Add these to the GRPO training pipeline at `agent-platform/src/neuroagent/training/`

**Where in the code**: `agent-platform/src/neuroagent/training/rewards/` for reward functions; `data/training/` for training cases
**Expected impact**: Directly addresses 0/3 failure on FND-P03 and FEPI-TEMP-P03
**Effort**: 3-5 days (case creation + reward function + training run)

### 2.3 Red herring resistance training
**Problem**: Confounders systematically mislead the model. Evidence from the Qwen3.5-9B evaluation:
- MS-RR-P01: topiramate side effects attributed as the diagnosis (0/3 react)
- ALZ-EARLY-RM03: vascular risk factors caused overcall of mixed dementia (0/3 both modes)
- GLIO-HG-P01 (prior run): dental abscess history led to brain abscess diagnosis

**How to implement**:
1. Use the `red_herrings` field already present on 16+ puzzle cases to build training signal:
   ```python
   for rh in case.ground_truth.red_herrings:
       # Penalize if agent's reasoning chain treats rh.data_point as supporting the wrong diagnosis
       # Reward if agent explicitly identifies it as a confounder
   ```
2. Add a **red herring awareness reward** to the GRPO training:
   - +0.5 reward if the agent mentions the red herring AND correctly dismisses it
   - -0.5 penalty if the agent's primary diagnosis is driven by the red herring
3. Optionally add to the system prompt: "Be aware of cognitive biases. When a finding seems to strongly suggest a diagnosis, consider whether it could be coincidental or misleading."

**Where in the code**: `agent-platform/src/neuroagent/training/rewards/` + `config/system_prompts/orchestrator.txt`
**Expected impact**: Improve red_herring_handling from 2.71/5 to 3.5+/5
**Effort**: 2-3 days

### 2.4 Negative result interpretation (Bayesian reasoning)
**Problem**: MS-RR-P01 — negative OCBs (present in 5-10% of MS patients) treated as disconfirming rather than incorporated with base rate. The agent committed to the wrong diagnosis after one negative test.

**How to implement**:
1. **System prompt addition** to `orchestrator.txt`:
   ```
   ## Interpreting Negative Results
   A negative test result does NOT rule out a diagnosis. Consider:
   - Test sensitivity: how often is it negative in patients who HAVE the disease?
   - Pre-test probability: how likely was the diagnosis BEFORE the test?
   - Example: CSF oligoclonal bands are negative in 5-10% of confirmed MS patients.
   Always consider the full clinical picture, not just a single test result.
   ```
2. **Training examples**: Include 5-10 cases where a key test is falsely negative but the diagnosis is still correct. Train the reward function to penalize premature closure after a single negative result.

**Where in the code**: `config/system_prompts/orchestrator.txt` for prompt; `agent-platform/src/neuroagent/training/` for training
**Expected impact**: Targeted improvement on MS-RR-P01 and similar puzzle cases with misleading negatives
**Effort**: 1 day for prompt change, 2-3 days for training examples

### 2.5 Etiological completion training
**Problem**: ISCH-STR-M03 — correctly identifies ischemic stroke but fails to pursue the mechanism (paroxysmal AF found on Holter). The agent stops at "stroke" without determining cardioembolic vs. large-vessel vs. cryptogenic.

**How to implement**:
1. **System prompt addition** (condition-specific guidance injected via hospital rules):
   ```yaml
   # In stroke_code.yaml
   clinical_pearls:
     - "For every stroke case, determine the mechanism: cardioembolic, large-vessel atherosclerosis, small-vessel lacunar, or cryptogenic"
     - "Always order: ECG/Holter for AF, carotid imaging for ICA stenosis, echocardiogram for structural heart disease"
   ```
2. **Training signal**: Add etiological specificity to the GRPO reward — "ischemic stroke, cardioembolic from atrial fibrillation" scores higher than just "ischemic stroke"
3. **Metric enhancement**: The `diagnostic_accuracy_top1` check could weight etiological specificity: partial credit for correct disease + bonus for correct mechanism

**Where in the code**: `config/hospital_rules/*/stroke_code.yaml` for rules; `evaluation/metrics.py` for scoring
**Expected impact**: Better action_recall and protocol_compliance on stroke cases. More specific diagnoses.
**Effort**: 1-2 days

---

## Priority 3: Infrastructure Improvements

### 3.1 Semantic critical action matching — DONE
**Implemented** in `metrics.py` alongside the safety score fix (see 1.1). Uses keyword-based tool matching + response-text analysis instead of an LLM call, keeping evaluation fast and deterministic.

### 3.2 Protocol compliance evaluation
**Status**: Wired up (`PathwayChecker.check_case()` now called in `MetricsCalculator`) but not yet evaluated systematically.

**Action**: Run the benchmark with all 5 hospitals and compare protocol compliance rates. Identify which pathways agents fail to follow.

**Expected impact**: Enables the hospital-rules ablation for the paper

### 3.3 Output format enforcement — DONE
**Problem**: Some repeats (MS-RR-RS02, FND-S03) produce THINK blocks without resolving to a final diagnosis.

**Solution implemented**: Added re-prompting logic in `orchestrator.py` `run()` method. When the agent's final turn contains reasoning text but no `### Primary Diagnosis` heading, the orchestrator sends one additional message:

> "You provided reasoning but did not include a structured diagnosis. Please provide your final assessment now using the required format starting with: ### Primary Diagnosis"

The retry response is parsed for the assessment. If it still lacks structure, the original text is used as fallback. This adds at most 1 extra LLM call, only when needed (~5% of cases).

### 3.4 Token budget optimization — DONE (compact format, no leakage)
**Problem**: With Qwen3.5-9B at 8K max_tokens, the system prompt + hospital rules + patient info + tool definitions consume ~2000+ tokens before the first tool result.

**Rejected approach**: Selectively injecting only the matching pathway based on the case's condition. This would leak the diagnosis by telling the model "this is a stroke case" before it starts reasoning — defeating the purpose of the benchmark.

**Solution implemented**: `RulesEngine.get_context()` injects ALL pathways (no filtering) but in a **compact format**:
- Only mandatory steps are listed (optional steps omitted — saves ~30% of rule tokens)
- One-line-per-pathway format instead of multi-line with descriptions
- Framing changed from "You MUST follow these protocols" to "Follow the protocol that matches the clinical presentation" — the agent must choose which pathway applies

**Before** (~600 tokens):
```
- **Acute Stroke Code (AHA/ASA Guidelines)**: AHA/ASA stroke protocol. Door-to-needle <60 min...
  - interpret_labs (immediate, MANDATORY)
  - analyze_brain_mri (immediate, MANDATORY)
  - analyze_ecg (immediate, MANDATORY)
  - check_drug_interactions (before_treatment, MANDATORY)
  - search_medical_literature (within_24h, optional)      ← now omitted
  - CONTRAINDICATED: ...
```

**After** (~400 tokens):
```
- **Acute Stroke Code** (triggers: stroke, stroke_code, ischemic_stroke)
  MANDATORY: interpret_labs (immediate), analyze_brain_mri (immediate), analyze_ecg (immediate), check_drug_interactions (before_treatment)
  CONTRAINDICATED: ...
```

**Savings**: ~200 tokens across all 5 pathways — modest but meaningful for small models. More importantly, NO diagnostic leakage.

---

## Priority 4: Paper-Specific Tasks

### 4.1 Figure: Tool benefit by difficulty
Bar chart showing react vs no-tools accuracy at each difficulty level. Include error bars from 3 repeats.

### 4.2 Figure: v1 vs v3 ablation
Show how interpretive tool outputs inflate accuracy. This is the "cheating" figure.

### 4.3 Table: 4-model comparison
Rows: Qwen3.5-9B, MedGemma-4B, Qwen3.5-27B (react + no-tools). Columns: top-1, top-3, composite, consistency, safety.

### 4.4 Table: Per-condition accuracy
Heatmap of accuracy across 10 conditions × 4 models.

### 4.5 Case study: When tools hurt
MS-RR-P01 detailed analysis — negative OCBs increased confidence in wrong diagnosis. This is a compelling narrative for the paper.

### 4.6 Case study: Dual pathology failure
FND-P03 analysis — the model's inability to diagnose two conditions simultaneously.

---

## Appendix: Known Bugs

| Bug | Severity | Status |
|-----|----------|--------|
| `safety_score` always 0.0 (string matching vs free text) | High | Known, workaround: use LLM judge safety score |
| `diagnostic_accuracy_top1` false negative on SYNC-CARD (correct diagnosis, wrong string match) | Medium | Known, workaround: manual review |
| Some v1 moderate cases still have templated similarity within tiers | Low | Documented, not blocking |
| `report_generation.txt` prompt is loaded but never used | Low | Cleanup needed |
