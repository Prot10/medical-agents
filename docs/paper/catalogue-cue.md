# Does the tool catalogue tell the model the diagnosis? (4 Nov 2026)

Code: `scripts/paper/catalogue_cue.py`. Raw outputs: `outputs/paper/catalogue_cue/` (before),
`outputs/paper/catalogue_cue_terms/` (step A), `outputs/paper/catalogue_cue_neutral/` (step B),
`outputs/paper/catalogue_full/` (full policy runs), all gitignored. Model Qwen3.5-9B (vLLM on the
rockhopper A100), profile `policy-qwen3.5-9b`, seeds 1–3, 600 cases. All policies are still
`draft`: these are engineering measurements, not reportable benchmark scores.

## Question

The policy loop advertises the same 16-tool catalogue in every case; the agent is never told
"for this condition you may order these tests". The catalogue can still act as a menu of answers in
two ways: an enum term that only one condition needs (a single named neuronal antibody), and prose
that names what a study is for ("before and after a CSF tap test in suspected NPH"). The question is
how much of the diagnosis the model gets from the catalogue alone, before it has seen any result.

## Method

The model must submit on its first turn (`max_turns` 1), so no tool can be called and only what the
request advertises differs between variants. The system prompt is the policy prompt in all of them.

| Variant | What the request carries |
| --- | --- |
| `catalogue` | the catalogue as advertised |
| `no-prose` | every tool and parameter description removed; names, types, enums kept |
| `no-catalogue` | only `submit_assessment` |
| `narrative` | the `narrative-qwen3.5-9b` profile: no catalogue, its own system prompt |

Metric: the diagnosis component (scorer v2). Per case the mean over the three seeds, then the
difference between two variants paired by case, per condition and overall, with a bootstrap 95% CI
(4000 draws). `catalogue − no-prose` is the cue carried by the prose, `no-prose − no-catalogue` the
cue carried by the vocabulary, `no-catalogue − narrative` the effect of the framing.

## Before (catalogue at `06b74446`)

Overall the catalogue is a small cue: +0.027 [+0.004, +0.052] over no catalogue. It is
concentrated in four conditions, and in each it has one identifiable source.

| Condition | catalogue | no-catalogue | diff [95% CI] | Source |
| --- | --- | --- | --- | --- |
| NPH | 0.811 | 0.478 | +0.333 [+0.167, +0.500] | prose: catalogue − no-prose +0.433 (the tap test, the lumbar drain "after a negative tap test", the timed gait "in suspected NPH") |
| anti-NMDAR encephalitis | 0.867 | 0.600 | +0.267 [+0.111, +0.422] | vocabulary: no-prose − no-catalogue +0.211 (NMDAR the only neuronal-surface antibody with its own term) |
| high-grade glioma | 0.211 | 0.056 | +0.156 [+0.056, +0.267] | prose: +0.156 (the glioma molecular algorithm, "for a brain tumour this is the only route") |
| FND | 0.956 | 0.889 | +0.067 [+0.011, +0.133] | prose: +0.111 ("the positive signs of a functional disorder") |

The catalogue also lowers three conditions: bacterial meningitis −0.144 [−0.244, −0.056], early
Alzheimer's −0.089, migraine with aura −0.067. The framing has no effect: no catalogue and the
narrative profile differ by +0.008 [−0.009, +0.024].

## What changed

Each step was measured on its own.

- **Step A, vocabulary and serving.** The differentials that had no orderable test got their terms
  (`costs.yaml`, with library normal reports): the antibody-mediated encephalitides other than
  anti-NMDAR in serum and CSF (LGI1, CASPR2, GABA-B, AMPA, GAD65), anti-cN1A (inclusion body
  myositis, ALS), treponemal antibodies (neurosyphilis), the CSF Lyme antibody index (GBS),
  fluorescein angiography (Susac syndrome, MS) and the MRI `orbits` and `pituitary` protocols (thyroid
  eye disease in MG, pituitary apoplexy in SAH). New terms must never contradict a case's stored
  results, so the lab serving was audited order by order
  (`agent-platform/scripts/validation/lab_serving_audit.py`): every lab term alone and every policy
  lab order, in every case. The matcher served stored panels to orders they do not answer (the
  AQP4/MOG panel to clustered-AChR, NMDAR and botulinum orders in MS cases; the autoimmune
  encephalitis panel to antiphospholipid and immunoglobulin orders). The fix moved 1518 of 104 593
  orders: 1339 false positives now fall to the library normal, 108 stored results are now reached.
  Two policy orders changed, both correctly; the perfect-agent check is unchanged (600/600, same 16
  warnings).
- **Step B, prose.** Every description now says what a study measures (method, specimen, what the
  report contains), never which disease it is for, and gives no advice on when to order it
  (`docs/benchmark/tool-contract.md`, enforced by `tests/test_catalogue_prose.py`). The review-app
  mirror carries the same text.

## After: the cue

Same model, server, seeds and no-catalogue runs as before (rockhopper A100); report in
`outputs/paper/catalogue_cue/report_after.json`. Diagnosis rate, mean over 3 seeds:

| Condition | Before | Step A (terms) | Step B (terms + prose) | No catalogue |
| --- | --- | --- | --- | --- |
| NPH | 0.811 | 0.800 | **0.433** | 0.478 |
| high-grade glioma | 0.211 | 0.167 | **0.078** | 0.056 |
| FND | 0.956 | 0.933 | 0.933 | 0.889 |
| anti-NMDAR encephalitis | 0.867 | 0.856 | 0.800 | 0.600 |
| all, minus no catalogue | +0.027 [+0.004, +0.052] | +0.032 [+0.011, +0.056] | **+0.009 [−0.012, +0.031]** | — |

- **The prose was the cue for NPH and glioma, and it is gone.** Step B against step A: NPH −0.367
  [−0.544, −0.189], glioma −0.089 [−0.178, −0.011]; both now sit at the no-catalogue rate. Overall
  the catalogue is no longer a significant cue.
- **Step A changes nothing measurable on its own** (+0.006 [−0.007, +0.018] against the old
  catalogue), as expected: the new terms widen the differential, they do not answer it.
- **The NMDAR cue is a category cue, not an NMDAR cue.** It survived the sibling antibodies
  (vocabulary alone +0.222 over no catalogue, as before). An ablation on the 30 NMDAR cases with the
  neutral catalogue (`outputs/paper/catalogue_cue_drop/`, 3 seeds) separates it:

  | NMDAR cases | Diagnosis | minus no catalogue |
  | --- | --- | --- |
  | neutral catalogue | 0.800 | +0.200 [+0.033, +0.367] |
  | without the two NMDAR terms | 0.800 | +0.200 [+0.022, +0.378] |
  | without every neuronal antibody, the autoimmune-encephalitis and paraneoplastic panels, SOX1, VGCC and the testicular ultrasound | 0.589 | −0.011 [−0.156, +0.122] |

  The cases that move are the ones the model calls psychiatric without a catalogue (first-episode
  psychosis, bipolar mania, catatonia, neuroleptic malignant syndrome); with the antibody tests in
  view it answers "autoimmune encephalitis" and picks NMDAR among the siblings itself (one answer is
  anti-LGI1). The catalogue reminds the model that an antibody-mediated cause exists; it does not
  name which. Removing the antibody tests is not an option (they are the required work-up of 30
  cases and of the differentials of many more), so this residual is reported, not fixed: it is the
  reason the narrative profile, not a max-turns-1 policy run, is the no-tool baseline of the paper.
- Smaller moves, within noise: focal epilepsy +0.078 [+0.011, +0.156] from step A to step B,
  myasthenia −0.067 [−0.133, −0.011] (the RNS, single-fibre and thymoma prose named it).

## After: full policy runs

The three catalogues (`06b74446`, step A, step B) in the normal policy loop (12 turns), 600 cases,
seeds 1–3, same server; outputs and the reports per metric in `outputs/paper/catalogue_full/`
(`report_{metric}.json`, `criteria_change.txt` per required criterion, `tool_mix.txt`). Mean over the
seeds, paired by case:

| | Before | Step A | Step B | B − before [95% CI] | B − A [95% CI] |
| --- | --- | --- | --- | --- | --- |
| diagnosis | 0.871 | 0.873 | 0.868 | −0.003 [−0.017, +0.012] | −0.006 [−0.021, +0.009] |
| required coverage | 0.480 | 0.492 | 0.467 | −0.012 [−0.024, −0.001] | −0.025 [−0.037, −0.012] |
| tool accuracy | 0.514 | 0.518 | 0.497 | −0.017 [−0.035, −0.001] | −0.022 [−0.039, −0.005] |
| scalar | 0.498 | 0.506 | 0.488 | −0.010 [−0.019, −0.002] | −0.018 [−0.027, −0.010] |

Completion is 98.4% in all three; tool calls 3.82 / 3.81 / 3.74 per episode, mean cost $1987 /
$1967 / $2135.

- **The diagnosis does not depend on the catalogue once the agent can order tests.** No condition
  moves by more than 0.07 between the old catalogue and step B, and no move is significant; the
  largest, glioma −0.067 [−0.133, +0.011], follows the work-up below (fewer tissue diagnoses
  ordered, 0.96 → 0.86 per episode).
- **Step A helps the work-up a little** (+0.012 required coverage, +0.008 scalar): the new terms and
  the serving fix give the agent orders that now return the stored result.
- **Step B costs work-up, mostly where the old prose said what to order for which disease.** Most of
  the required criteria that fall from the old catalogue to step B (credit, mean over seeds) are the
  target of a sentence that was removed:

  | Condition (cases) | Required order | Before → B | Removed sentence said |
  | --- | --- | --- | --- |
  | NPH (30) | timed gait after the intervention | 0.86 → 0.49 | "run before and after a CSF tap test in suspected NPH", "the timed gait 2 to 24 hours after a CSF tap test" |
  | bacterial meningitis (16) | blood cultures before antimicrobials | 0.55 → 0.24 | "draw, then treat"; the meningococcal PCR and throat swab |
  | glioma (9) | resection with IDH1/ATRX IHC and MGMT | 0.96 → 0.65 | the molecular algorithm, "for a brain tumour this is the only route" |
  | myasthenia (26) | repetitive nerve stimulation | 0.63 → 0.35 | "neuromuscular junction (myasthenia)" |
  | early Alzheimer's (30) | cognitive screen | 0.78 → 0.53 | "the first step in suspected cognitive decline, before imaging" |
  | cardiac syncope (30) | 12-lead ECG | 0.92 → 0.68 | "part of the initial evaluation of any transient loss of consciousness" |
  | ischaemic stroke (30) | 12-lead ECG | 0.44 → 0.26 | Holter and loop recorder "(cryptogenic stroke, unexplained syncope)" |

  Three falls have no removed sentence that names their condition: GBS EMG/NCS 0.84 → 0.66 and
  respiratory function 0.61 → 0.43 (the old respiratory text named ALS and MG, not GBS), and the timed
  gait of vascular dementia 0.90 → 0.64 (the old gait text named NPH only). They may be the same
  sentences read across conditions, or a change in how the shorter catalogue is read; these runs do
  not tell. The gains: in NPH the CSF study (0.61 → 0.91) and the MRI (0.74 → 1.00) replace part of the
  repeated bedside assessments, in ALS the brain MRI (0.33 → 0.57), in Parkinson's the DaTscan.
- **Reading.** The old prose was a partial practice guideline inside the tools: it did not tell the
  model the diagnosis, but in about a third of the conditions it told the model which test that
  diagnosis calls for (NPH, meningitis, glioma, myasthenia, Alzheimer's, syncope, stroke). With it,
  part of the work-up score measured reading the catalogue; with step B
  the score measures what the model knows. The ECG sentence was replaced by a measurement sentence
  ("a normal one does not exclude an intermittent rhythm disturbance") rather than removed; the runs
  cannot separate the loss of the old link from an effect of the new wording.

The step B catalogue is the one to keep: its work-up score is the model's own, which is what the
policy reward is meant to measure and what training should change. The new prose has not been
reviewed by a physician (the molecular guidance of glioma, the tap test, the microbiology); it was
written to the rule above, not checked clinically.
