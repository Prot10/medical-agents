# NeuroBench v5 Expansion — TODO Tracker

**Goal**: Complete v5 dataset (516 cases, 20 conditions) and retrain models.
**Started**: 2026-03-29 | **Last updated**: 2026-03-29

---

## Phase 1: Dataset & Trajectories

- [x] Generate 316 new NeuroBench cases (10 new conditions + supplements)
- [x] Validate all 516 cases (Pydantic schema — 516/516 pass)
- [x] Strip diagnostic leakage from tool outputs (v3-style)
- [x] Assemble v5 dataset at `data/neurobench/cases/` (516 cases)
- [ ] **Generate gold trajectories for 316 new cases** (1580 trajectories = 316 × 5 styles)
  - [ ] Prepare trajectory prompts (generate_gold_trajectories.py --prepare-prompts)
  - [ ] Generate trajectories via Sonnet subagents (batches of ~50)
    - [x] Batch 1: 50 cases — done (ALS 30/30 + FND 20/20 partial)
    - [x] Batch 2: 50 cases — done (FTD 25/25 + GBS partial)
    - [~] Batch 3: 50 cases — partially done before stop (GBS remainder + HEP-ENC + MG)
    - [ ] Batch 3: 50 cases (250 trajectories)
    - [ ] Batch 4: 50 cases (250 trajectories)
    - [ ] Batch 5: 50 cases (250 trajectories)
    - [ ] Batch 6: 16 cases (80 trajectories) — remainder
  - [ ] Validate & parse all new trajectories into trajectories.jsonl
  - [ ] QA audit sample of new trajectories

## Phase 2: Training Data Pipeline

- [ ] Re-run `split_dataset.py` for 516 cases (5-fold stratified)
- [ ] Rebuild `trajectories.jsonl` (2580 total: 1000 existing + 1580 new)
- [ ] Re-format for SFT (`format_for_grpo.py --mode gold`)
- [ ] Update training data splits for GRPO

## Phase 3: Model Training

- [ ] Retrain SFT on 2580 trajectories (QLoRA, Qwen3.5-9B)
- [ ] Run GRPO training from SFT checkpoint (15 epochs, 6-component reward)
- [ ] Run DAPO training from SFT checkpoint (10 epochs, if token-level loss fixed)
- [ ] Merge best adapter into base model for deployment

## Phase 4: Evaluation

- [ ] Run full evaluation: base vs SFT vs GRPO on all 516 cases
- [ ] Per-condition accuracy breakdown (20 conditions)
- [ ] Cost efficiency analysis across conditions
- [ ] Generate paper figures (Pareto front, radar charts, ablations)

## Phase 5: Codebase Updates

- [ ] Update CLAUDE.md with v5 dataset version
- [ ] Update evaluation scripts to point to v5
- [ ] Add new conditions to `tool_costs.yaml` (EMG/NCS costs for GBS/MG/ALS/PERI-NEURO)
- [ ] Update `format_patient_info()` for new conditions if needed
- [ ] Update condition enum references in evaluation code

---

## Progress Log

| Date | What | Result |
|------|------|--------|
| 2026-03-29 | Completed 1000/1000 v4 gold trajectories | QA'd, 89 fixes applied |
| 2026-03-29 | Generated 316 new v5 cases | 10 new conditions, all validated |
| 2026-03-29 | Applied v3 stripping, assembled v5 | 516/516 valid, 0 leaks |
| 2026-03-30 | Validated all 316 new cases (Pydantic) | 316/316 valid after normalization |
| 2026-03-30 | v5 trajectory generation progress | 555/1580 done — ALS, FND, FTD complete; GBS/HEP-ENC/MG partial |
