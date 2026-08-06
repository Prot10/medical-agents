# Clinical tool review — round 1 (July 2026)

Status of the external clinical review of the NeuroBench **tool catalog** (not the cases),
performed by Flavia and Antonio on https://review.andreaprotani.com.

Raw data: `data/review/tool_reviews/neurobench/{reviewer_code}.json` (gitignored;
pulled from the VPS 2026-08-05). Verbatim dump: see `Reviewer comments` section below.

## What they did

| Reviewer | Code | Scope | Annotations | Conditions | Last edit | `completed_at` |
|---|---|---|---|---|---|---|
| Reviewer 1 | `NB-KSC3-…` | chronic | 43 | 10 | 2026-07-25 | **not set** |
| Reviewer 2 | `NB-87MF-…` | acute | 48 | 10 | 2026-07-27 | **not set** |
| Reviewer 3 | `NB-C87F-…` | — | 0 | 0 | 2026-07-10 | not set |

91 annotations: 38 `error`, 29 `issue`, 24 `note`. Every comment is guideline-anchored
(McDonald 2024, AHA/ASA 2023 & 2026, WHO meningitis 2025, EASL 2022 / ACG 2026,
WHO CNS5 / EANO 2021, EAN-PNS 2023, ESC 2018, ACNS, NICE, ILAE, MDS).

**Case-level review has not started** — 0 field annotations across all 8 case files touched.

### Coverage

Reviewer 1 (chronic): `multiple_sclerosis`, `migraine_with_aura`, `alzheimers_early`,
`ftd`, `parkinsons`, `als`, `nph`, `focal_epilepsy_temporal`,
`functional_neurological_disorder`, `peripheral_neuropathy`.

Reviewer 2 (acute): `subarachnoid_hemorrhage`, `autoimmune_encephalitis_nmdar`,
`ischemic_stroke`, `bacterial_meningitis`, `hepatic_encephalopathy`,
`brain_tumor_glioma`, `guillain_barre`, `peripheral_neuropathy`, `syncope_cardiac`,
`status_epilepticus`.

**Gap: `myasthenia_gravis` was never reviewed.** Reviewer 2's five
`peripheral_neuropathy` annotations are, in content, entirely about myasthenia gravis —
AChR/MuSK antibody ordering, single-fibre EMG, thymic imaging, Evoli 2019 and Jacob 2025
as sources. They belong under `myasthenia_gravis` and should be re-filed there.
Reviewer 1's only `peripheral_neuropathy` comment is `SOSTITUIRE PATOLOGIA`.

## Important caveat: they reviewed a stale catalog

`review_api/services/tool_io.py` carries a hand-maintained mirror of the agent's tool
schemas (`tools/` is deliberately not shipped to the review VPS). Commit `9a0636c`
(2026-07-10) made `costs.yaml` the single source of the closed vocabulary and regenerated
the real tool enums from it, but in the mirror it only renamed `imaging_type` → `modality`
and left the stale enum lists behind. The reviewers worked 07-19 → 07-27, so they assessed
the catalog through that stale mirror:

| Parameter | Values shown to reviewers | Values the agent actually had |
|---|---|---|
| `order_specialized_test.test_type` | 9 | 21 |
| `order_advanced_imaging.modality` | 6 | 12 |
| `order_cardiac_monitoring.monitor_type` | 4 | 6 |

20 values were invisible, and six of them are studies the reviewers reported as missing:
`respiratory_function` (GBS), `emg_single_fiber` (MG), `optical_coherence_tomography` (MS),
`transcranial_doppler` (SAH), `MR_venography` (status epilepticus), `cardiac_MRI` and
`implantable_loop_recorder` (cardiac syncope). Reviewer 2's remark that single-fibre EMG is
"folded into EMG/NCS" and can be "neither requested nor scored" describes the stale mirror,
not the tool.

Resolution: the vocabulary predates the review and retiring it would undo the reviewers'
own requests, so the vocabulary stands and the mirror was fixed — the enum-bearing
parameters are now injected from `costs.yaml`, and
`agent-platform/tests/test_tool_io_schemas.py` fails CI on any future drift. The reviewers
are not asked to re-review. Two values with zero case references that nobody requested
(`mslt`, `pure_tone_audiometry`) were retired to shrink unreviewed surface; pure-tone
audiometry has a WHO 2025 post-meningitis indication and can be reinstated with a case
that needs it.

Separately, the VPS copy of `costs.yaml` was itself a 07-10 snapshot missing ~146 lab-panel
prices. Impact on the review was minimal — the catalog shows a cost *floor*, so labs read
"from €9" instead of "from €5", and the per-study prices the reviewers quoted (€294 MRI,
€230 advanced imaging) were unaffected. It is fixed by a redeploy; `deploy.sh` already
ships the file.

## Breakdown of the asks

| Type | Count |
|---|---|
| Rewrite the tool description for this condition | 37 |
| Change the required/optional tier | 18 |
| Remove the tool from this condition entirely | 13 |
| **Add a tool/item that does not exist** | 12 |
| Confirmed as published, description-only note | 11 |

### Tier changes requested

REQUIRED → OPTIONAL: `analyze_csf` (MS), `analyze_brain_mri` (migraine),
`interpret_labs` (migraine, parkinsons, nph, focal_epilepsy_temporal, syncope_cardiac),
`order_advanced_imaging` (ftd), `analyze_brain_mri` (ischemic_stroke),
`analyze_eeg` (hepatic_encephalopathy), `order_ct_scan` (hepatic_encephalopathy).

OPTIONAL → REQUIRED: `analyze_csf` (SAH, conditional on negative CT),
`order_ct_scan` (ischemic_stroke), `order_cardiac_monitoring` (guillain_barre),
`order_cardiac_monitoring` (syncope_cardiac).

### Outright removals

`analyze_eeg` + `analyze_ecg` from MS, migraine, alzheimers_early, parkinsons;
`analyze_csf` + `order_echocardiogram` from migraine;
`order_echocardiogram` + `order_cardiac_monitoring` from focal_epilepsy_temporal;
`order_advanced_imaging` from nph.

### New items proposed (12) — these do not fit the current 12-tool action space

| Condition | Proposed item | Tier |
|---|---|---|
| autoimmune_encephalitis_nmdar | Tumour screening imaging (occult ovarian teratoma) | REQUIRED |
| ischemic_stroke | Perfusion / tissue-based selection imaging (CTP, DWI-PWI, DWI-FLAIR) | OPTIONAL |
| bacterial_meningitis | Microbiological studies — blood cultures, whole-blood PCR, throat swab | REQUIRED |
| hepatic_encephalopathy | Infection screen + diagnostic paracentesis | REQUIRED |
| hepatic_encephalopathy | Abdominal cross-sectional imaging for portosystemic shunts | OPTIONAL |
| brain_tumor_glioma | Tissue acquisition — resection or stereotactic biopsy | REQUIRED |
| brain_tumor_glioma | Integrated histomolecular diagnosis (IDH, 1p/19q, MGMT, …) | REQUIRED |
| brain_tumor_glioma | Perfusion MRI + amino-acid PET | OPTIONAL |
| guillain_barre | Respiratory function monitoring (FVC, single breath count) | REQUIRED |
| guillain_barre | Spinal and peripheral nerve imaging | OPTIONAL |
| myasthenia_gravis (filed under peripheral_neuropathy) | Mediastinal / thymic imaging | REQUIRED |
| syncope_cardiac | Advanced cardiac imaging (cardiac MRI/CT, coronary angiography) | OPTIONAL |

Reviewer 1 adds four clinical-assessment items with no tool at all behind them:

- Structured cognitive/behavioural assessment with informant history and validated
  neuropsychological testing — REQUIRED for `alzheimers_early` and `ftd`
- Structured ICHD-3 headache/aura history + neurological exam — the *only* true required
  "test" for `migraine_with_aura`
- Objective gait and cognitive assessment before/after CSF tap test — REQUIRED for `nph`
- FDG-PET / perfusion SPECT and amyloid PET — OPTIONAL for `alzheimers_early`, `ftd`
  (arguably reachable through `order_advanced_imaging`)

This is the structural finding of the review: for several conditions the mandatory
diagnostic step is **not expressible** in the current action space, so those cases are
unsolvable by construction. Reviewer 2 states it explicitly for glioma ("with imaging,
blood tests, EEG and ECG the best attainable output is a suspicion") and for GBS
("the panel cannot represent the single process that kills in this disease").

### Recurrent cross-condition defects

1. **Shared generic buckets.** `interpret_labs` carries the same string everywhere —
   "CBC, metabolic, coagulation, thyroid, inflammatory, autoimmune/paraneoplastic,
   genetic" — flagged in 9 conditions. Same for `analyze_csf`
   ("oligoclonal bands, PCR, antibodies, 14-3-3/RT-QuIC" appearing in SAH, meningitis,
   GBS, NPH, MG) and `analyze_brain_mri` (protocol list offering dementia/MS protocols
   in acute conditions).
2. **`order_specialized_test`** is an undifferentiated 21-value bucket; flagged as
   "too broad" in MS, FTD, parkinsons, ALS, NPH, GBS, MG.
3. **Cost without yield.** Several comments cite the euro cost of a misdirected order —
   the reviewers are using the cost registry as intended.

## Dataset composition changes requested (from their email, 2026-08-05)

| Action | Condition | Enum status | Cases |
|---|---|---|---|
| Remove | `peripheral_neuropathy` — "too broad a category" | exists | 30 to delete |
| Replace with | **Vascular dementia** | **missing from enum** | 30 to generate |
| Remove | `functional_neurological_disorder` — purely clinical diagnosis | exists | 30 to delete |
| Replace with | **Dementia with Lewy bodies** | **missing from enum** | 30 to generate |
| Add | **Spontaneous intracerebral haemorrhage** | `hemorrhagic_stroke` exists, unused | 30 to generate |
| Add | **Herpes simplex encephalitis** | `viral_encephalitis` exists, unused | 30 to generate |

Their reasoning: DLB + vascular dementia complete the four major dementias
(with AD and FTD) and let the benchmark test differential diagnosis among them; ICH
completes the cerebrovascular emergencies (with ischaemic stroke and SAH) and has a
distinct therapeutic pathway (BP control, anticoagulation reversal, neurosurgical
indication); HSV encephalitis completes CNS infection (with bacterial meningitis) and
tests MRI + EEG + LP use plus timely empirical aciclovir.

They keep FND only if the project also wants to measure **diagnostic overuse**, in which
case every diagnostic tool for it must be optional. They recommend against that and
prefer DLB. Their FND annotation reads
`DISCUTERE SE TENERE PATOLOGIA, SE VOGLIAMO CONTROLLARE SE L'AGENTE AI FA OVERTESTING`.

Net effect: **20 conditions → 22** (two swaps, which are net-neutral, plus two straight
additions). **120 cases to generate, 60 to retire, 660 total** — up from 600, which
changes the train/test split (currently 500/100).

`hemorrhagic_stroke` and `viral_encephalitis` already exist as enum values with no cases
and no `conditions.yaml` entry, so they can host ICH and HSV encephalitis — but the
labels are broader than what the reviewers asked for and may be worth renaming to
`intracerebral_hemorrhage` and `hsv_encephalitis`. `vascular_dementia` and
`dementia_with_lewy_bodies` have to be added to `NeurologicalCondition`.

## Reviewer comments

Full verbatim text: `data/review/tool_reviews/neurobench/*.json`, or regenerate the
readable dump with:

```bash
python3 - <<'PY'
import json
for code, name in [('NB-KSC3-TWUA-QDTM', 'REVIEWER 1'), ('NB-87MF-FBTV-TPWE', 'REVIEWER 2')]:
    d = json.load(open(f'data/review/tool_reviews/neurobench/{code}.json'))
    print(f'\n\n# {name} ({len(d["field_annotations"])} annotations)\n')
    for a in d['field_annotations']:
        print(f'## [{a["severity"].upper()}] {a["field_path"]}\n_{a["field_snippet"]}_\n{a["comment"]}\n')
PY
```

---

## Implementation status (2026-08-05)

Done, in four commits:

| Commit | What |
|---|---|
| `84af853` | Killed the stale mirror. `tool_io.py` now injects enums from `costs.yaml`; `tests/test_tool_io_schemas.py` fails CI on drift, covering both a reintroduced literal enum and description drift. Retired `mslt` and `pure_tone_audiometry`. |
| `22c1d4a` | Per-study scoring. `interpret_labs`/`analyze_csf` were credited on tool name alone; the action metrics were sets of tool *names*, collapsing 61% of cases. Measured on a parameter-blind agent: required coverage 0.885 → 0.544, cases at full coverage 336 → 78. |
| `61dbcce` | The four tools: `order_body_imaging`, `order_microbiology`, `obtain_tissue_diagnosis`, `perform_clinical_assessment`, plus `CT_perfusion`. 12 → 16 tools. |
| `827c1d4` | 18 tier changes + removals in `conditions.yaml`; VaD and DLB in the enum; FND kept as the restraint probe. |
| `ee33f83` | Item 1 of the per-condition passes: `amino_acid_PET` for high-grade glioma, the tracer EANO names, and `obtain_tissue_diagnosis` replacing the `tool_name: null` referral in `GLIO-HG.md`. |

Gates after all five: `validate_cases.py` 600/600 clean, perfect agent 1.0 on 600/600,
1567 tests pass (5 skipped need `--extra training`).

### Item 2: cardiac syncope, end to end

Reviewer 2 left five annotations on this panel. Half of the "advanced cardiac imaging" ask
was already satisfied — `cardiac_MRI` existed and 18 of the 30 cases pin it — so the work was
the other half plus the four defects the audit turned up.

**Vocabulary added** (`costs.yaml`, and therefore the enums, the catalog and the cost tracker):
`chest_CT` 276 / `chest_CTA` 368 on `order_body_imaging`; `coronary_CTA` 460,
`coronary_angiography` 2760 and `cardiac_FDG_PET` 2300 on `order_advanced_imaging`;
`exercise_echo` 460 on `order_echocardiogram`; `lymph_node_biopsy` 1840 on
`obtain_tissue_diagnosis`; `ASO` 18 on `interpret_labs`. All EUR.

**Three cases were modelling a study with the wrong tool:**

| Case | Was | Now | Why it mattered |
|---|---|---|---|
| RM04 | CT pulmonary angiogram via `order_ct_scan{contrast, angiography}` plus a phantom `region: chest` the schema ignores | `order_body_imaging{study: chest_CTA, contrast: true}` | The head tool's discriminators are identical for a head-and-neck CTA, so imaging the brain of a patient with a pulmonary embolism scored the required action — the misdirected escalation the reviewer predicted |
| RP05 | `FDG_PET` for a cardiac PET/CT with dietary preparation; histology as a `tool_name: null` referral | `cardiac_FDG_PET`; `obtain_tissue_diagnosis{lymph_node_biopsy}` | One token meant two studies at different prices; and the mandatory histological step had no callable act — the glioma pattern again |
| P02 | Exercise echocardiography as `order_specialized_test{exercise_stress_test}` | `order_echocardiogram{echo_type: exercise_echo}` | A treadmill test scored a study whose whole answer is an imaged, provoked outflow gradient (ESC 2018 Class I) |

**The laboratory directive, applied to all 30.** TSH was in the required panel of 29 cases
and BNP of 27, against a reviewer annotation stating in terms that untargeted thyroid,
inflammatory, autoimmune and paraneoplastic panels have no established role here and that
natriuretic peptides do not establish the cause of syncope. Thyroid survives in the 4 cases
where a thyroid mechanism is on the differential (SVT, atrial flutter, sinus node
dysfunction, QT prolongation), BNP in the 3 where a guideline risk-stratifies with it. The
step is `required` in 11 cases and `recommended` in 19. Mandated laboratory spend over the 30
cases: EUR 6108 → 4686, about EUR 47 per case; required actions 204 → 185.

Two case-level inconsistencies surfaced while doing it: RP04's ground truth asserted a
therapeutic antiepileptic level without ordering `AED_levels`, and RM02's asserted rheumatic
activity from an ASO titre that its lab report contains but `costs.yaml` did not price — so
the agent could not name it and no optimal action could ask for it.

**A hard sequence constraint contradicted the directive.** 28 cases required
`interpret_labs` *before* `order_cardiac_monitoring` at `hard` severity. With the labs no
longer mandatory, an agent that correctly skipped an untargeted panel and went to monitoring
took a hard sequence violation. Removed from the 18 cases where the labs step is no longer
`required`; kept where a named assay gates the decision. No gate would have caught this: the
perfect agent orders every optimal action regardless of tier, so it never triggers the
violation.

**Four defects found in the machinery, each latent because nothing exercised it:**

1. `FollowUpToolOutput.output` — the union never gained the four post-review models, so a case
   authoring a follow-up for one of them failed validation outright.
2. `validate_cases.py` — checked `study`, `specimen`, `procedure` and `assessment_type` against
   the *specialized-test* vocabulary. RM04 and RP05 are the first two cases in the dataset to
   use those parameters and both were reported as out of vocabulary while being legal.
   `test_every_case_value_is_priced` had the mirror-image blind spot.
3. `_classification_matches` compared parameters by equality, so a `useless`/`harmful` entry
   carrying a list could never match a real call. Seven were dead, five of them on
   `analyze_csf.basic` — a parameter that does not exist. Set-valued parameters now match by
   intersection, which is what makes "this one assay is untargeted here" scoreable at all.
4. `order_echocardiogram`, `analyze_eeg` and `analyze_brain_mri` still wrote their enums out by
   hand — in the tool class *and* in the review-app mirror, so each could drift from
   `costs.yaml` independently. All three now derive.

**Measurement worth recording: the panel lists are a generation input, not a per-case
contract.** Comparing `conditions.yaml` against the 600 cases, 360 case actions are absent
though the panel marks the tool required, and 588 are `required` in a case though the panel
marks the tool optional. Both numbers pre-date the review (157 / 278 before the tier changes)
and `validate_cases.py` does not check either, by design. The syncope labs entry was the one
place where the gap produced the behaviour a reviewer had explicitly objected to, which is why
it was closed there and nowhere else.

### The same defect classes, swept across all 600 cases

Cardiac syncope is one condition of twenty, and it was the only one audited at close range.
Running its four defect classes over the whole dataset found each of them again, in numbers. All
are now closed. None of them broke a gate: `validate_cases.py` checks that ground truth is legal
and reachable, not that it names the study it means.

| Defect | Scale | Resolution |
|---|---|---|
| A study priced under two tools | blood cultures under `interpret_labs` *and* `order_microbiology`; 123 laboratory actions in 108 cases ordering blood, urine or ascitic-fluid microbiology through the laboratory tool | All on `order_microbiology`. 43 reports already existed as `interpret_labs` follow-ups — organism, bottles, susceptibility — and were transplanted, not reinvented |
| The head-CT tool asked to image a body region | 89 actions: myasthenia 30 (mediastinum), anti-NMDAR 30 (teratoma search), glioma 27 (staging), status epilepticus 2. `order_ct_scan` has no region parameter, so its discriminators were identical to a head-and-neck study | All on `order_body_imaging`, with `chest_abdomen_pelvis_CT` added as the single study it actually is. Reports moved with the actions; 6 were authored from the cases' own stated findings; 33 gold-trajectory calls retargeted with their tool responses |
| Required labs / CSF actions naming no assay | 246, so any call satisfied them and the per-study scoring was inert exactly where the reviewers aimed | 153 pinned from the assays their own text names. 95 left as wildcards on purpose — an `analyze_csf` answered by the always-reported cell count and protein has no sub-selection to make |
| Two priced names for one assay that did not compare equal | `syphilis` in 30 actions vs `RPR` in 118; paraneoplastic 37 vs 1; liver function 33 vs 2; inflammatory bundle 31 vs 1 | `normalize_analyte` resolves synonyms as well as spellings, and 69 case terms were rewritten to the canonical name. `lactate` and `ABG` are priced — 100+ actions named them and no agent could order either |
| An aggregate label required while the finding names its components | 31 actions requiring `inflammatory_markers` while the expected finding names procalcitonin and CRP, so an agent ordering precisely the right assay failed | Replaced by the components. Where the case names no component (GBS and 3 others) the bundle label is what it means and stays |
| A `hard` sequence constraint on a prerequisite the case does not require | 8: five gating a lumbar puncture on imaging the case only recommended, three gating drug selection on an ECG — one case never ordering it at all | Prerequisites raised to required; the four hepatic MRIs promoted from their fallback (a normal scan is the case truth and is what the gate needs), and three status-epilepticus ECGs authored, since the generic normal fallback contradicted a patient on amiodarone and one at potassium 6.8. New `SEQ_PREREQ_NOT_REQUIRED` check |

Two closed a gap that was on the handover list as case-authoring work: the missing
`order_microbiology` step in bacterial meningitis and hepatic encephalopathy (60 cases) and the
missing `order_body_imaging` step in myasthenia and anti-NMDAR (60) **already existed, on the
wrong tool**. Required steps still absent from cases: 240, down from 360 —
`perform_clinical_assessment` 150, `obtain_tissue_diagnosis` 30, `analyze_csf` 29 in SAH,
`order_cardiac_monitoring` 30 in GBS, and one echo.

**And the MockServer was answering one question with another study's report.** A tool that stands
in for several studies served whatever it had stored: a cardiac PET for a brain FDG order, a blood
culture for an ascitic-fluid order, a tilt-table report for an ergometry request. It now checks the
discriminator, and prefers the follow-up that *is* the study asked for — the token matcher scored
trigger slugs, and family tokens like `pet` are not discriminating. The guard applies only where
the stored report itself speaks the closed vocabulary, and only where variants answer different
questions; `order_cardiac_monitoring` is exempt, because a 48-hour and a 24-hour recording report
the same rhythm. It immediately found two gold trajectories ordering a neuropsychological battery
in FND and receiving the EMG report.

`report_panel_case_tiers.py` now prints the panel-versus-case gap on demand, so a tier change that
drifts from the cases is visible instead of merely true.

### Remaining work

**1. Redeploy the review app** — pair with sending the reply, since it changes what the
reviewers see. `bash deployment/hostinger/deploy.sh`. The VPS is running a 2026-07-10
snapshot.

**2. Author four `conditions.yaml` entries** — vascular dementia, DLB, spontaneous ICH,
HSV encephalitis. Each needs `name`, `abbreviation`, `icd_code`, `description`,
`typical_demographics`, `encounter_type`, `required_modalities`, `optional_modalities`,
`key_findings` per difficulty, `differential_diagnoses`, `difficulty_variants`,
`common_followups` — ~90 lines, modelled on `functional_neurological_disorder`. Source
from the guidelines the reviewers cited. DLB needs `MIBG_scan` and `DaTscan`, both already
priced.

**3. Generate 120 cases** (4 × 30) and retire the 30 `PERI-NEURO-*`:

```bash
for c in vascular_dementia dementia_with_lewy_bodies hemorrhagic_stroke viral_encephalitis; do
  bash dataset-generation/scripts/generate_batch.sh "$c"   # calls `claude -p` per case
done
git rm data/neurobench/cases/PERI-NEURO-*.json
```

**4. Author the new required steps into 327 existing cases.** The tier changes opened this
gap by design — `conditions.yaml` now marks a step REQUIRED that no case's ground truth
contains yet:

| Missing tool | Cases | Conditions |
|---|---|---|
| `perform_clinical_assessment` | 150 | FTD, migraine, Alzheimer's, NPH, FND |
| `order_microbiology` | 60 | bacterial meningitis, hepatic encephalopathy |
| `order_body_imaging` | 60 | NMDAR encephalitis, myasthenia gravis |
| `obtain_tissue_diagnosis` | 30 | high-grade glioma |
| `analyze_csf` | 29 | subarachnoid haemorrhage (conditional REQUIRED) |

Each needs an `optimal_actions` step with `tool_parameters`, `expected_finding`, `citation`
and `guideline_source`, plus the matching pre-generated output in `initial_tool_outputs` or
`followup_outputs` and a `metadata.fallback_tool_kinds` entry. Reviewer 2's annotations
contain most of the clinical text needed, verbatim.

Re-derive the gap after any batch with:

```bash
uv run python - <<'EOF'
import json, glob, yaml, collections
from neuroagent.review_api.services.tool_catalog import _MODALITY_TO_TOOL, _CONDITION_ALIAS
spec = yaml.safe_load(open('dataset-generation/config/conditions.yaml'))
gap = collections.Counter()
for f in glob.glob('data/neurobench/cases/*.json'):
    d = json.load(open(f)); cond = d['condition']
    e = spec.get(_CONDITION_ALIAS.get(cond, cond))
    if not e: continue
    req = {_MODALITY_TO_TOOL[t] for t in e['required_modalities']}
    have = {a.get('tool_name') for a in d['ground_truth']['optimal_actions']}
    for m in req - have: gap[m] += 1
print(gap.most_common())
EOF
```

**5. Regenerate the GRPO prompts** — they bake the tool schemas in and are stale:

```bash
uv run python -m neuroagent.training.data.build_grpo_dataset --split train \
  --output data/neurobench/grpo/train_prompts.jsonl
uv run python -m neuroagent.training.data.build_grpo_dataset --split test \
  --output data/neurobench/grpo/test_prompts.jsonl
```

**6. Re-baseline.** `clinical_reward.py` feeds `(action_precision + action_recall)/2` into
GRPO, so every published number and trained adapter predates the scoring fix.
