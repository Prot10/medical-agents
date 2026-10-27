# Train→test leakage audit (26 Oct 2026)

Code: `scripts/paper/leakage_audit.py` (standard library only; `uv run python scripts/paper/leakage_audit.py`).
Raw outputs: `outputs/paper/leakage/` (gitignored): `summary.json`, `nn_similarity.csv`,
`top_pairs.json`, `git_propagation.csv`, `case_dates.csv`. Dataset state: commit `4221abb6`.

## Verdicts

| Check | Verdict |
|---|---|
| 1. Split integrity | **ISSUE (one case)**: ids disjoint, but train case SE-P07's answer is hepatic encephalopathy |
| 2. Near-duplicate text | **CLEAN** relative to the sibling null; stratified test cases are in-condition siblings by design |
| 3. Code paths | **CLEAN but unguarded**: nothing in the prompt names diagnoses; no trainer refuses test cases |
| 4. Review-feedback propagation | **CLEAN for held-out conditions** (their review fixes touched only their own files); class-level by construction elsewhere |
| 5. Training-run evidence | **ISSUE (July runs)**: test split used as GRPO eval set and for checkpoint promotion; **UNKNOWN (September runs)**: rollouts not on EOS |
| 6. Pretraining contamination | **CLEAN for the panel**: every model was released before the cases' final content; the repository is public, which matters for later frontier models |

## 1. Split integrity

- 600 cases: 500 train, 100 test (60 from two held-out conditions, 40 stratified, 2–3 per remaining
  condition). Train ∩ test = ∅. No case is unassigned. `train_cases.txt`/`test_cases.txt` match
  `split_manifest.json`.
- The split was fixed on 2026-07-10 (`1ff3046c`, "before any trajectory generation"). The only later
  change (`94cc9499`, 2026-08-06) swapped retired PERI-NEURO cases for VASC-DEM cases (2 in test, 28 in
  train). The 98 surviving test ids are unchanged.
- Held-out conditions in train, by condition label: myasthenia_gravis 0, hepatic_encephalopathy 0.
- **Leak:** **SE-P07** (condition `status_epilepticus`, in train) has hepatic encephalopathy as its
  accepted diagnosis (K72.90/K76.82; an HE mimic of NCSE). It has carried this answer since at least
  2026-07-10, so every training run could have seen one HE-answer case with its HE work-up.
- Held-out diagnoses mentioned in train cases, as competing hypotheses only (acceptable, reported):
  - MG: 20 rejected labels, 20 differentials, 3 red herrings; 25 cases in total, all ALS, GBS, FND or
    SYNC-CARD mimics.
  - HE: 5 differentials, 4 rejected labels, 1 red herring, 3 patient texts; 6 cases in total.

## 2. Nearest-neighbour similarity, test vs sibling null

The null is leave-one-out train→train within the same condition. Stratified test cases are compared
with the train cases of their own condition; held-out test cases with all 500 train cases. The table
gives the median (p95, max).

| Field | Measure | Stratified test (n=40) | Null train (n=500) | Held-out test (n=60) | One-sided Mann-Whitney p |
|---|---|---|---|---|---|
| Narrative | TF-IDF cosine | 0.205 (0.308, 0.416) | 0.193 (0.332, 0.391) | 0.098 (0.165, 0.196) | 0.34 |
| Narrative | 8-gram containment | 0.017 (0.116, 0.120) | 0.017 (0.091, 0.187) | 0.000 (0.006, 0.017) | 0.29 |
| Narrative | Longest shared run (words) | 13 (30, 56) | 12 (29, 53) | 5 (10, 15) | – |
| Tool outputs | TF-IDF cosine | 0.475 (0.721, 0.845) | 0.452 (0.639, 0.879) | 0.114 (0.145, 0.160) | 0.19 |
| Tool outputs | 8-gram containment | 0.247 (0.549, 0.730) | 0.252 (0.504, 0.783) | 0.008 (0.016, 0.037) | 0.28 |
| Policy | TF-IDF cosine | 0.599 (0.862, 0.937) | 0.577 (0.827, 0.971) | 0.109 (0.157, 0.167) | 0.38 |
| Policy | 8-gram containment | 0.443 (0.848, 0.920) | 0.417 (0.788, 0.957) | 0.000 (0.000, 0.011) | 0.50 |

Permutation p-values (10,000 permutations, mean greater) agree: between 0.12 and 0.48.

Reading:
- Test cases are **no closer** to the train set than train siblings are to each other: AUC 0.50–0.54
  and no p-value below 0.1, so the split adds no near-copies beyond the condition template.
- The template itself is strong. Within a condition, policies share a median 42% of 8-grams and up to
  441-word verbatim runs (criterion text, citations). Tool reports share up to 428 words, for example
  the identical ALS deltoid biopsy report in ALS-S04 (test) and ALS-S03 (train), with 187 shared words.
- The 40 stratified cases therefore measure **in-condition** generalisation, and the 60 held-out cases
  measure **new-condition** generalisation (narrative cosine 0.10, policy 8-gram overlap 0). Report
  the two subsets separately.

Top pairs, with their text, are in `outputs/paper/leakage/top_pairs.json`. The closest pairs are
ISCH-STR-S03↔S04 (narrative), ALS-S04↔ALS-S03 (tool outputs, policy) and ALS-RS11↔ALS-S03 (policy).

## 3. Code paths

- Benchmark selection: `agent-platform/src/neuroagent/evaluation/benchmark.py:39-50`. `--split` reads
  `splits/{split}_cases.txt`. **With neither `--split` nor `--cases` it runs all 600 cases**
  (`:50`).
- GRPO: `agent-platform/src/neuroagent/training/train_grpo.py:942-969`. `--split`/`--cases` is
  required, but `--split test` and arbitrary `--cases` are accepted. The current trainer has no eval
  set and no best-checkpoint selection.
- SFT: `train_sft.py:55-70` trains on any episode file, and `training/data/export_episodes.py:21-39`
  exports every completed episode of a run directory. Neither checks the split.
- Prompt: `harness/context.py:25-30` and the submit schema (`neuroagent_schemas/actions.py:35-43`,
  free-text `primary_diagnosis`) enumerate no conditions or diagnoses. Vocabulary terms such as
  `anti_AChR`, `anti_MuSK`, `repetitive_nerve_stimulation` and `ammonia` (`costs.yaml:100,188-190,509`)
  are orderable tests, not diagnoses. The YAML comments naming MG/HE (`costs.yaml:663,675`) are not
  served.

## 4. Review-feedback propagation (git)

- Commits that edited case files: 98. Of these, 87 touched test files and 83 also touched train files.
- The held-out conditions' review rounds touched **only** held-out files:
  - `65349689` (MG round: 0 train files);
  - `f347d6b5` (HEP-ENC round: 0);
  - `46a2f5ec` (HE CT: 0);
  - `44fabae7` (MG antibody: 0).
- The mixed commits are global schema or tool sweeps (`b5a46c7c`, `7d9bbe3e`, `317e46db`, `4221abb6`)
  or multi-condition batches applied condition by condition (`bbf644ac`, `e9550a5b`, `5c900ea3`,
  `e2893688`).
- Scan of held-out terms on lines these commits **added** to train files: every hit is a pre-existing
  mimic entry. Examples: MG in ALS and GBS differentials and rejected labels (`265396d8`, `d1246ff3`,
  `7d9bbe3e`); HE in NPH-M08, ISCH-STR-RP01 and GBS-RM13 differentials. The only answer-level hit is
  SE-P07 (see 1).
- `f5a714b6` ("comply with the reviewers on the hepatic-encephalopathy CT") also edited 1 train file,
  MIG-AURA-RM11. The change is unrelated migraine guidance (CSF downgraded to optional) with no HE
  content.
- Limit: for the 18 stratified conditions, review comments and fixes were applied to all 30 cases of
  a condition. Git cannot tell whether a given fix was prompted by a test-case comment. That evidence
  is in the per-case annotations on the review VPS (`data/review/annotations/neurobench/`), not read
  here.
- Shared resources: `config/policies/diagnosis_synonyms.yaml:443-462` has MG entries and is scorer-side
  only. `config/tools/fallback_library.yaml` (`ammonia` :2650, `anti_AChR` :3543) serves the same
  normal result to any case that orders the test. Neither appears in prompts or training rows.

## 5. Training runs on EOS (`/eos/project-d/diagbox/dvc/NeuroAgent/`)

- July runs (`checkpoints/grpo_Qwen3.5-9B`, `grpo_Qwen3.5-4B`, `sft_Qwen3.5-*`; results in
  `results/grpo_eval`, `results/definitive_eval`):
  - Training prompts were the 500 train cases (stale `train_prompts.stale-2026-08-05.jsonl` in
    `1a755cdb^`: 0 test ids).
  - **The GRPO eval set was the test split**: `eval_data: data/neurobench/grpo/test_prompts.jsonl`,
    which holds 98 of today's test ids.
  - 9B: `best_eval_step` 240 was monitored; the final adapter is step 250.
  - 4B: **promoted checkpoint-200 "the best held-out reward"**, which is checkpoint selection on test.
  - SFT 9B logged 100 eval trajectories of unknown provenance.
  - These runs also predate the current dataset, scorer v2 and harness. **Do not report them.**
- September runs (`checkpoints/grpo-long-2026-09/{qwen3.5-9b,granite-4.1-8b,gemma-4-e4b}`): the
  trainer states contain no eval entries and no `best_model_checkpoint`. Qwen was promoted at step 425
  after an OOM, Gemma has an extra `-ck75`, Granite stopped at 500.
  - **The training case list could not be verified.** The rollouts (`rollouts/step-*.jsonl`) and
    `run_config.json` were written to the VM's local `--output` (`outputs/grpo/long/<model>/train/`),
    not to EOS. `training_args.bin` holds no case ids.
  - `ssh a100` failed (no session) and kubectl needs a new SSO login. The VM's
    `outputs/grpo/scripts/paired_eval.py` results are also there.
  - These runs trained on September case versions, so evaluation must use the current dataset.

## 6. Pretraining contamination

Release dates (Hugging Face `createdAt`): Qwen3.5-9B 2026-02-27, Gemma-4-E4B-it 2026-03-02,
Granite-4.1-8b 2026-04-06.

Case files first appeared on 2026-03-14 (198 in March, 272 in April, 100 in June, 30 in August). Every
case's current content was last revised on or after 2026-05-26 (389 in August, 194 in October).

Qwen and Gemma predate every case. Granite predates the final content of every case.

The GitHub repository `Prot10/medical-agents` is **public** (created 2026-03-13), cases and answers
included. Frontier or future models evaluated later could have been trained on it: keep the test
answers out of public view before release, or report the crawl risk.

## Before reporting results

1. Remove SE-P07 from train, or move it to a held-out bucket, then retrain. Alternatively, report the
   HE held-out results with and without the condition, and state the leak.
2. Re-run every reported training on the frozen dataset. Keep the persisted rollouts and
   `run_config.json` with the adapter on EOS, and intersect their case ids with the test split (this
   script can be extended to read them).
3. Add guards: the trainers and episode export should refuse test-split cases unless explicitly
   overridden, and `benchmark.py` should require `--split` or `--cases`.
