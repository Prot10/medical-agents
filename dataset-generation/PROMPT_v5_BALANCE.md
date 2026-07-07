# NeuroBench v5 — balance under-represented conditions to 30 cases each

Paste this entire file as the **first message** of a fresh Claude Code session
in this repo (`/home/aprotani/projects/medical-agents`). The assistant should
treat everything in this file as binding instructions.

---

## Context

NeuroBench v5 is a clinical reasoning benchmark for medical AI agents. The
dataset lives at `data/neurobench_v5/cases/<CASE_ID>.json` — currently 516
cases across 20 neurological conditions, with known good audit + realism
sweeps already applied. See `data/neurobench_v5/CHANGELOG_v4_to_v5.md` and
`data/review/CLINICIAN_REVIEW_FLAGS.md` for the current state.

You are picking up after the baseline benchmark on 6 base models was run and
showed the dataset is class-imbalanced. The decision now is to bring 12
under-represented conditions up to **exactly 30 cases each** by generating
**100 new cases total**. A separate pass will trim FND (40→30) and NMDAR
(36→30); that is *not* your job here.

## Mission

For each of the 12 under-represented conditions, generate enough new cases
to reach 30. Cases must satisfy four hard rules:

1. **Schema-valid** — pass `NeuroBenchCase.model_validate_json(...)` from
   `packages/neuroagent-schemas/src/neuroagent_schemas/case.py`.
2. **Clinically realistic** — read like a real patient encounter; tool
   reports describe findings, not diagnoses.
3. **No answer leakage** — diagnosis cannot be inferred from the tool
   outputs alone unless that's the explicit point of a "straightforward"
   case; even then, no language giving away management decisions in
   reports. Follow `dataset-generation/TOOL_REPORT_STYLE_GUIDE.md` to the
   letter.
4. **Diverse vs existing** — different from the cases already present in
   the same condition (different demographics, subtypes, red herrings,
   chief-complaint phrasing). No copy-paste contamination — see the
   patterns flagged in `data/review/CLINICIAN_REVIEW_FLAGS.md` section 3.

## Conditions and target counts

| # | Condition | Current | Add | Target | Current S/M/P |
|---|---|---|---|---|---|
| 1 | FTD | 25 | **+5** | 30 | 0/18/7 |
| 2 | HEP-ENC | 25 | **+5** | 30 | 5/12/8 |
| 3 | MG | 25 | **+5** | 30 | 0/18/7 |
| 4 | NPH | 25 | **+5** | 30 | 6/8/11 |
| 5 | ALZ-EARLY | 20 | **+10** | 30 | 8/6/6 |
| 6 | BACT-MEN | 20 | **+10** | 30 | 0/9/11 |
| 7 | FEPI-TEMP | 20 | **+10** | 30 | 5/7/8 |
| 8 | GLIO-HG | 20 | **+10** | 30 | 8/6/6 |
| 9 | ISCH-STR | 20 | **+10** | 30 | 1/8/11 |
| 10 | MS | 20 | **+10** | 30 | 8/4/8 |
| 11 | PD | 20 | **+10** | 30 | 5/9/6 |
| 12 | SYNC-CARD | 20 | **+10** | 30 | 8/5/7 |

Process them **in that exact order** — the four +5 conditions first
(cheapest feedback cycle), then the eight +10 conditions.

## Strict workflow

You MUST follow this loop. **Do not skip the human-checkpoint step.**

```
FOR each condition in the list above:
   1. Pre-flight investigation (you, in the main loop, no subagents):
      a. Read dataset-generation/criteria_packs/<COND>.md
      b. Read all existing data/neurobench_v5/cases/<COND>-*.json (note
         demographics, subtype mix, red herrings already used, chief
         complaint phrasing patterns, tool-report idioms)
      c. Read 3 high-quality reference cases of this condition to use as
         structural templates (pick ones with no flags in
         data/review/CLINICIAN_REVIEW_FLAGS.md)
      d. Read dataset-generation/TOOL_REPORT_STYLE_GUIDE.md
         (mandatory — the de-leak rules)
      e. Read dataset-generation/GOLD_TRAJECTORY_AUTHORING_GUIDE.md
      f. Read dataset-generation/TOOL_PARAMETER_VOCABULARY.md
      g. Skim data/review/CLINICIAN_REVIEW_FLAGS.md for known-bad
         patterns to AVOID introducing

   2. Propose a generation plan for this condition (5 or 10 cases):
      - Per-case: case_id, difficulty (S/M/P), subtype/variant,
        demographic envelope (age/sex/race/SES/comorbidity),
        red-herring strategy, what makes it different from existing
        cases, real-seeded vs synthetic
      - Show the target S/M/P after adding
      - Justify any deviation from the suggested split below

   3. STOP. Wait for the user to type "ok" (or equivalent). Do not
      dispatch subagents until told to.

   4. On approval:
      - Dispatch N parallel subagents (N = +5 or +10 = exactly one
        subagent per new case)
      - Each subagent uses model: sonnet (resolve to the latest Sonnet
        available, target Sonnet 4.7 if accessible)
      - Each subagent generates exactly ONE case JSON, writes it to
        data/neurobench_v5/cases/<NEW_CASE_ID>.json
      - Per the project memory feedback (feedback_claude_subagent_preference):
        use Claude Code subagents (Task tool), not the API directly

   5. When all N subagents return:
      - Validate every new case with the Pydantic schema
      - Run the field-by-field consistency checks (see "Per-case
        validation" below) and produce a per-case status table
      - Regenerate (just that one case) if validation fails
      - Report a summary: N new, valid, flagged, judgment-calls

   6. STOP. Wait for user "ok" before moving to the next condition.
END
```

**The user explicitly does not want all 12 conditions running in parallel.**
One condition at a time. Human approval gates each condition.

## Suggested S/M/P split per condition (deviate with clinical justification)

| Condition | New S | New M | New P | Resulting S/M/P |
|---|---:|---:|---:|---:|
| FTD | 2 | 2 | 1 | 2 / 20 / 8 |
| HEP-ENC | 1 | 2 | 2 | 6 / 14 / 10 |
| MG | 2 | 2 | 1 | 2 / 20 / 8 |
| NPH | 1 | 2 | 2 | 7 / 10 / 13 |
| ALZ-EARLY | 4 | 3 | 3 | 12 / 9 / 9 |
| BACT-MEN | 3 | 3 | 4 | 3 / 12 / 15 |
| FEPI-TEMP | 3 | 3 | 4 | 8 / 10 / 12 |
| GLIO-HG | 4 | 3 | 3 | 12 / 9 / 9 |
| ISCH-STR | 3 | 3 | 4 | 4 / 11 / 15 |
| MS | 4 | 2 | 4 | 12 / 6 / 12 |
| PD | 3 | 4 | 3 | 8 / 13 / 9 |
| SYNC-CARD | 4 | 3 | 3 | 12 / 8 / 10 |

Reasoning: these splits introduce a few straightforward cases for
conditions that currently have none (FTD, MG, BACT-MEN) since classical
presentations CAN be straightforward, while keeping most growth in the
moderate/puzzle tiers where the benchmark is most discriminative. If you
find a clinical reason to disagree (e.g. there is no realistic
straightforward bvFTD presentation), propose a different split with the
rationale.

## Case ID convention

Use the next free integer in the right prefix family. Check existing case
IDs in `data/neurobench_v5/cases/` first.

| Prefix | Type | Example next free |
|---|---|---|
| `{COND}-S{NN}` | Synthetic straightforward | `MG-S05` |
| `{COND}-M{NN}` | Synthetic moderate | `MG-M04` |
| `{COND}-P{NN}` | Synthetic puzzle | `MG-P04` |
| `{COND}-RS{NN}` | Real-seeded straightforward | `MG-RS17` |
| `{COND}-RM{NN}` | Real-seeded moderate | `MG-RM16` |
| `{COND}-RP{NN}` | Real-seeded puzzle | `MG-RP15` |

For conditions currently 100% synthetic (FTD, HEP-ENC, NPH): default to
synthetic IDs unless you find appropriate real seeds in
`dataset-generation/seeds/`. For the others: prefer a 50/50 split between
synthetic and real-seeded, matching the existing mix.

## Per-subagent generation prompt (template)

When dispatching each parallel subagent, use this exact prompt template,
filling in the bracketed slots:

```
You are an expert neurologist + medical educator authoring ONE simulated
patient case for the NeuroBench v5 benchmark. Output a single JSON object
matching the NeuroBenchCase Pydantic schema. NO markdown fences, no
commentary before or after.

# Reading order (read these first, do not skip)
1. dataset-generation/criteria_packs/[COND].md
   — the clinical truth for this condition
2. dataset-generation/TOOL_REPORT_STYLE_GUIDE.md
   — the de-leak rules; tool reports are descriptive, not diagnostic
3. dataset-generation/GOLD_TRAJECTORY_AUTHORING_GUIDE.md
   — what good clinical reasoning looks like
4. dataset-generation/TOOL_PARAMETER_VOCABULARY.md
   — closed vocabulary for catchall tool parameters
5. packages/neuroagent-schemas/src/neuroagent_schemas/case.py
   — authoritative schema
6. THREE reference cases (read in full):
   - data/neurobench_v5/cases/[REF_1].json
   - data/neurobench_v5/cases/[REF_2].json
   - data/neurobench_v5/cases/[REF_3].json
7. data/review/CLINICIAN_REVIEW_FLAGS.md
   — known-bad patterns to NOT introduce

# Your case spec
- case_id: [NEW_CASE_ID]
- condition: [COND_ENUM]  e.g. "ftd", "alzheimers_early"
- difficulty: [S|M|P]  → "straightforward" / "moderate" / "diagnostic_puzzle"
- encounter_type: [emergency | inpatient | outpatient]
- subtype / variant: [SUBTYPE — be specific, e.g. "bvFTD with GRN
  splice-site variant; predominant right-hemisphere CBS overlap"]
- demographic envelope: [age range, sex, race, comorbidity, SES — must
  differ from the 3 reference cases]
- red-herring strategy: [what distractors, where embedded, intended
  cognitive bias they exploit, correct interpretation]
- what makes it different from existing cases: [explicit list — e.g.
  "younger onset than any existing FTD case; first FTD case with
  comorbid bipolar disorder masking behavioral changes"]

# Hard rules
A. Match the criteria pack's diagnostic criteria precisely. Required tools,
   useless_tools, harmful_tools, and sequence_constraints must reflect the
   pack's standards for this condition.
B. Tool reports describe findings, never diagnoses. No "consistent with
   ALS" — say "active denervation in three body regions including bulbar".
   No "treat with riluzole" in any tool output.
C. The ground_truth.primary_diagnosis is the disease label ONLY — no
   narrative descriptors (do NOT write "Left ICA dissection presenting
   with painful Horner syndrome — high stroke risk without completed
   cerebral infarct"; write "Left internal carotid artery dissection").
D. The differential is sorted by likelihood, descending. Each entry has
   diagnosis + likelihood + key_features.
E. Patient demographics, medications, allergies, family history, vitals,
   neuro exam must form a self-consistent clinical picture. Cross-check
   for laterality (left/right must agree between imaging, exam, and
   reasoning — see CLINICIAN_REVIEW_FLAGS.md section 1).
F. red_herrings must specify location (which field/tool output), intended
   effect (what bias it triggers), correct_interpretation.
G. critical_actions and contraindicated_actions are free-text clinical
   instructions, written from the criteria pack (must-do and must-not-do).
H. key_reasoning_points are 3-6 bullet points naming what good reasoning
   looks like for THIS case — clinical pearls that distinguish it from
   the differentials.
I. If real-seeded (RS/RM/RP), root the case in a published case report
   when available (PubMed Central CC-BY 4.0 preferred); cite the PMID in
   the metadata field if available.
J. No copy-paste contamination. Re-derive every field for this specific
   patient — do not transplant text from another case.

# Output destination
Write the JSON to: data/neurobench_v5/cases/[NEW_CASE_ID].json

Return only a brief 2-3 line confirmation. The JSON file IS the work.
```

## Per-case validation (you run, after subagents return)

For each new `<NEW_CASE_ID>.json`:

```bash
# 1. Schema validation
uv run python -c "
from pathlib import Path
from neuroagent_schemas import NeuroBenchCase
c = NeuroBenchCase.model_validate_json(
    Path('data/neurobench_v5/cases/<NEW_CASE_ID>.json').read_text()
)
print(f'{c.case_id}  cond={c.condition.value}  diff={c.difficulty.value}  dx={c.ground_truth.primary_diagnosis}')
"
```

```bash
# 2. Sanity checks beyond schema (run on each new case):
#    a. Sex consistency: NMDAR-style "ovarian teratoma" text not in male patient
#    b. Laterality: any imaging finding side matches exam side
#    c. Allergies vs drug-interaction text: no fabricated allergies
#    d. Vital signs in physiological range for age
#    e. ICD code matches primary_diagnosis at the disease-category level
#    f. useless_tools and harmful_tools subset of the 12-tool roster (see
#       CLAUDE.md and config/tools/costs.yaml)
#    g. sequence_constraints reference tools that exist
#    h. tool_parameters in optimal_actions use the closed vocabulary
#       (TOOL_PARAMETER_VOCABULARY.md)
```

Use the `neurobench-case-audit` skill if available — it already encodes
many of these checks. Invoke as `/neurobench-case-audit <NEW_CASE_ID>`
once per case.

If any check fails for a case, **regenerate just that one case** with a
fresh subagent and the specific failure pasted into the prompt. Do not
touch the cases that passed.

## What to do RIGHT NOW

1. Read this entire file end-to-end. Confirm you understand the workflow.
2. Then for **condition #1 (FTD)** — and ONLY for FTD:
   a. Read the FTD criteria pack
   b. Read all existing FTD cases under `data/neurobench_v5/cases/FTD-*.json`
   c. Read the style guides
   d. Read `data/review/CLINICIAN_REVIEW_FLAGS.md`
   e. Pick 3 reference cases (no flags)
3. Propose a concrete plan for the 5 new FTD cases:
   - case_ids (next free FTD-S/M/P numbers)
   - difficulty per case
   - subtype/variant per case (differentiate explicitly from existing)
   - demographic envelope per case
   - red-herring strategy per case
   - real-seeded vs synthetic
   - target S/M/P after adding (e.g. 2/20/8)
4. **STOP** and wait for the user to type "ok" before dispatching
   subagents.

Do NOT generate any cases yet. The first deliverable is the FTD plan.

## Reminders / footguns

- The repo's tool count is **12** (see CLAUDE.md). Do not invent tools.
- `consult_medical_specialist` is in current ambiguous-tier territory
  (CLINICIAN_REVIEW_FLAGS section 5). When in doubt, mark it
  `recommended` not `required`.
- The `R` prefix in case IDs (RS/RM/RP) historically meant "real-seeded
  mimic" per the criteria pack template, but most R-cases are actually
  real-seeded confirmed cases of the index disease. Honor what the
  existing data does (real-seeded confirmed), not the stale doc.
- For NMDAR cases (you are NOT generating NMDAR, but for context): male
  patients must NEVER carry "ovarian teratoma" text. The audit found 7
  copy-paste victims of exactly this bug.
- The tool reports must not synthesize the case. Radiology reports talk
  about ring-enhancing lesions and edema, not glioblastoma. Lab
  interpretations note CK elevation and anti-GM1 negativity, not "rules
  out MMN."
- Do not write tool outputs that include reasoning chains or management
  recommendations. That is the AGENT's job at eval time.
- Maintain commit-friendly behavior: do not auto-commit. The user
  reviews and commits at their cadence.
