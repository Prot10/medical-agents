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

### Item 4: the spine hiding inside the brain, in 63 actions

Reviewer 1 asked for brain **and spinal cord** MRI with an MS protocol. The note in this file said
the spinal imaging existed and was simply not attached to MS. It was worse than that, and the same
shape as the cardiac-syncope CT.

All 30 MS cases already had two required MRI actions: the brain, and the cervico-thoracic cord. Both
were `analyze_brain_mri{protocol: ms, contrast: true}`, the cord one marked by a
`region: cervical_thoracic_spine` annotation the brain schema has no parameter for and drops. So the
two actions had the **same action identity and collapsed into one**: imaging only the brain scored
full required coverage for MS, and the cord study — which counts toward dissemination in space, and
whose short-segment lesions are what separate MS from NMOSD — was unscoreable.

Searching the whole dataset for that shape found it twice more:

* **All 30 ALS cases** carried `include_cervical_spine: true` on the brain MRI, with the cervical
  findings written into the brain report. So the exclusion of compressive myelopathy — the mimic
  that must be ruled out before a motor neuron disease diagnosis — was neither separately orderable
  nor scoreable. Split into a brain MRI and `order_body_imaging{spine_MRI}`, with the report's
  cervical findings, observations and numbered impression clauses moved to the spine study.
* **3 more**: a paraneoplastic chest-abdomen-pelvis CT on the head-CT tool in SE-P01 (missed by the
  region-based sweep because it pinned no region at all), and a cord and a lumbosacral-plexus MRI on
  the brain tool in two peripheral-neuropathy cases.

Two other collision shapes came out of the same search, and were real:

* **Nine ischaemic-stroke cases** ordered `MR_angiography` and then "considered" the same study
  again. One study, two actions; the duplicate is gone.
* **Six actions were attached to a tool that does not perform them** and so collapsed onto a real
  study's identity: a benzodiazepine trial read on the ongoing EEG, continuing acyclovir filed as a
  drug-interaction check, an extended lumbar drainage trial as a second CSF analysis, a bone-marrow
  evaluation and a haematology consultation as literature searches. All are clinical actions with
  `tool_name: null`, which is what that field is for.

Guards added, both verified against a reintroduced defect: `ACTION_KEY_COLLISION` (scoped to tools
that name a study — `search_medical_literature` and `check_drug_interactions` are excluded, since
they cost nothing, have no discriminator, and "consulted the evidence" is fairly one act), and
`REGION_NOT_INTRACRANIAL`, which keeps `region` usable for a real intracranial sub-region while
refusing the values that smuggled a body study into a head order. `include_cervical_spine` is
retired.

Both panels now say what the cases do: cord MRI is REQUIRED for MS and for ALS, not optional.

### A further pass: the gold workup was asking for studies the cases could not report

With the discriminator guard in place, the question worth asking became: does every action in every
gold workup actually get an answer? It did not.

**194 optimal actions across the 600 cases could not be answered as ordered.** 98 returned nothing
at all — 12 of them at `required` tier — and 96 more were answered by the off-pathway *fallback*
tier, which by construction says "this study was not on the pathway and did not contribute" while
the action carried its own expected finding. Before the guard, all of them were served **another
study's report**: an agent ordering a transcranial Doppler received a carotid duplex, one ordering an
MR angiogram received a duplex, one ordering an ice-pack test received a repetitive-stimulation
study. `validate_cases.py` was satisfied throughout, because its check asked only whether the tool
had *any* stored output.

All 194 now have their own report, authored from what each action already declares in its
`expected_finding` — "intramural haematoma and luminal narrowing confirm cervical arterial
dissection", "improvement of ptosis after two minutes of cooling supports MG" — put into the report's
shape, with the study named in the field both the scoring layer and the MockServer read. Nothing was
invented: the case had already committed to the result.

Three further findings on the way:

* **20 cardiac-MRI reports were labelled `perfusion_MRI`**, the cerebral study. The content was a
  cardiac MRI — late gadolinium enhancement in a coronary territory — so the label was wrong, and it
  was what the ground truth's `cardiac_MRI` was being compared against. 8 gold trajectories had
  inherited the mislabel and ordered the cerebral study for a cardiac question.
* **The discriminator comparison was word-order sensitive.** A report saying `"Single-fiber EMG"` did
  not match a call for `emg_single_fiber`, so the case's own SFEMG report was refused and its
  repetitive-stimulation report offered instead. Comparison is now on token sets, which is safe: no
  two terms in any of the ten vocabularies share one.
* **Ten cases have a gold workup that costs nothing** — the migraine cases whose only required steps
  are the two free tools, because the reviewers correctly demoted imaging and labs and the required
  `perform_clinical_assessment` step is still in the 150-case authoring block. `cost_efficiency`
  handles a zero-cost optimum without dividing by zero (1.0 if the agent also spent nothing, else
  0.0), so this is a pending gap, not a live defect.

`validate_cases.py` now resolves every optimal action through the MockServer instead of asking
whether the tool has any output at all: `ACTION_NO_RESULT` and `ACTION_ONLY_FALLBACK`, both verified
against a stripped report. Only `search_medical_literature` and `check_drug_interactions` may still
answer from the fallback tier — they carry no diagnostic finding, so a generic answer is a fair
simulation of one.

One judgement recorded rather than changed: in 15 cases a tool the case condemns outright still
returns an abnormal report — an LP in a subarachnoid haemorrhage with hydrocephalus shows the raised
pressure it was condemned for risking. That is clinically true, and the safety metric is what
penalises the act, so the content stands. Six were already declared red herrings; NPH-S10's
paroxysmal atrial fibrillation was a deliberate distractor that had never been declared, and now is.

### The first composition change, end to end: peripheral neuropathy out, vascular dementia in

Their first two composition asks were a single swap, and it is now complete rather than partly
landed. Reviewer 1 filed the removal as an `error` reading `SOSTITUIRE PATOLOGIA` on
`condition_tool:peripheral_neuropathy:interpret_labs`; Reviewer 2's e-mail gave the reason —
too broad a category to score — and the replacement, vascular dementia, which completes the four
major dementias so that the differential *among* them becomes scoreable.

What landed:

| | |
|---|---|
| `conditions.yaml` | `vascular_dementia` panel, in the slot the retired condition occupied. REQUIRED = structured cognitive assessment, MRI reported in STRIVE-2 terms, and the named reversible-cause plus vascular-risk laboratory panel. The embolic workup (ECG, monitoring, echocardiography, carotid duplex) is OPTIONAL at panel level and required per case only where the lesion pattern is embolic — the same rule the reviewers applied to syncope |
| `criteria_packs/VASC-DEM.md` | New, from VASCOG 2014, NINDS-AIREN 1993, AHA/ASA 2011 (Gorelick), STRIVE-2 2023, Boston criteria v2.0, AAN 2018 and AHA/ASA 2021 secondary prevention |
| Cases | **30 authored** — 11 straightforward, 10 moderate, 9 puzzle — across seven vascular mechanisms: subcortical small-vessel, multi-infarct, strategic single infarct, post-stroke (ischaemic and haemorrhagic), mixed Alzheimer-and-vascular, cerebral amyloid angiopathy, hereditary (CADASIL) and global hypoperfusion |
| Retired | 30 `PERI-NEURO-*` cases, 7 real seeds, the criteria pack, the README row, the MedCaseReasoning filter entry, the enum value, and the review app's label |
| Split | Rebuilt with the new `--preserve` option: **no surviving case changed sides**, only the 30 new ones were placed (28 train, 2 test) |

Two design points worth stating, because both are deliberate and a reviewer will otherwise read
them as defects. `VASC-DEM-M01` has an executive profile and a Fazekas 2 burden but has *not*
lost instrumental independence, so its ground-truth diagnosis is **mild** vascular cognitive
impairment (F06.7) and an agent that answers "vascular dementia" is wrong: the mild/major
threshold is functional, and that is what the case tests. `VASC-DEM-P08` has a
non-MR-conditional pacemaker, so the diagnosis is reached on CT, carotid duplex and pacemaker
interrogation, and the ground truth requires the agent to state what CT cannot exclude —
microbleeds, siderosis, and therefore amyloid angiopathy.

These are also the first 30 cases in the benchmark to use `perform_clinical_assessment`, the
tool added because the reviewers named validated cognitive testing as a required step with
nothing behind it. Gold workup cost runs 1 177–7 185 EUR (median 2 217), so no case is free.

Gates after the swap: `validate_cases.py` 600/600 clean, perfect agent 1.0 on 600/600,
944/944 trajectories satisfy the contract, 1 591 tests pass.

`report_panel_case_tiers.py` shows two deliberate panel↔case divergences for this condition, and
both are the design rather than drift. One case lacks the panel-required brain MRI: that is
`VASC-DEM-P08`, where MRI is contraindicated. And 35 actions across the set raise a
panel-OPTIONAL tool to REQUIRED in a specific case — carotid duplex and ECG where the infarcts
are embolic, CSF or amyloid PET where mixed pathology is the question, NOTCH3 where the
phenotype is hereditary. That is the reviewers' own rule applied per case, which is what makes
the mechanism scoreable instead of the label.

The one downstream consequence, stated rather than hidden: the 28 new train cases have no gold
trajectory, so the SFT corpus covers 472 of 500 train cases. They are named in
`tests/test_sft_inference_parity.py::AWAITING_DISTILLATION` with the reason, which keeps the
coverage guard sharp for every other case. The corpus was already due for regeneration —
required coverage of the existing traces fell to 0.566 when the required set became
study-specific — and these cases are covered by that run.

### FND: their option 2 was recorded, not implemented — now it is

The register accepted their option 2 (keep FND, every diagnostic tool optional, scored on
restraint) and `conditions.yaml` said so. The cases said the opposite, and the gap is worth
recording because it is the same failure mode as the stale catalog: a decision that lives only in
the place nobody scores.

| | before | after |
|---|---|---|
| Cases requiring brain MRI **with gadolinium** | 30/30 | 0 — OPTIONAL in 23, RECOMMENDED once and without contrast in the 7 with a specific alternative question |
| Cases requiring a laboratory battery | 30/30 | 0 — OPTIONAL in 27, RECOMMENDED and narrowed to named assays in 3 |
| `perform_clinical_assessment` actions | 0 | 30/30, REQUIRED |
| Actions tiered `optional` anywhere in the condition | 0 | present in every case |
| EMG/NCS and evoked potentials | prohibited in prose only | scored `useless_tools` entries in all 30 |
| Required-workup cost | 1 303 EUR mean, above bacterial meningitis (1 204) and Guillain-Barré (1 223) | **138 EUR** in the 8 non-paroxysmal cases and 1 242 in the 22 with events — against 2 426 EUR for the whole defensible path, which is the overuse gap the metric can now see |

The examination report is built from each case's own examination text, so nothing is invented:
Hoover sign was already documented in 23 cases, improvement with attentional distraction in 20,
collapsing (give-way) weakness in 17, a dragging monoplegic gait in 16, internal inconsistency on
repeat testing in 15, non-anatomical sensory loss in 14, midline splitting in 10 and tremor
entrainment in 9. Three cases have no limb sign to quote (FND-M04, FND-M06, FND-RP01, all
paroxysmal phenotypes); their reports carry the event semiology instead and say explicitly that
the positive diagnostic act for that phenotype is the recorded event, not a bedside sign.

Extraction is guarded, because a keyword is not a sign and the first pass proved it: `"CN XII:
Tongue midline, no fasciculations"` had been quoted as midline-splitting sensory loss, `"CN XI:
Sternocleidomastoid and trapezius strength 5/5 bilaterally"` as the sternocleidomastoid sign
(which requires weakness), `"No give-way weakness at this time"` as collapsing weakness, and
`"Reflexes are symmetric and normal, inconsistent with upper or lower motor neuron lesion"` as
internal inconsistency — the last of these being exclusion reasoning, the very model this pass
removes. Every sign now carries a required pattern plus a guard, negations and descriptions of the
patient's *other* condition are refused, an equivocal sign is labelled equivocal and excluded from
the positive tally, and a tripwire re-reads every quoted sentence for normality markers so the
next false positive is visible rather than silent.

Beyond the metric, the old tiers wrote the discredited diagnosis-of-exclusion model into the
ground truth: requiring imaging in every case is precisely what the FND literature argues against.
Fixing the tiers removed a clinical error, not just a scoring one.

Scoring EMG/NCS surfaced the same defect one layer down, in the trajectory corpus. Eighteen of the
25 `order_specialized_test` calls across the FND gold trajectories carry a clinical context that
asks for *functional signs* — "characterize atypical upward arm drift", "assess for positive
non-organic examination signs" — while the parameter says `neuropsych_battery` or, in one case,
`emg_ncs`. The teacher was reaching for the bedside examination and routing it through whichever
tool existed, because none performed it. That is the reviewers' structural finding again, this time
in the training data.

One of the eighteen was scored as a useless call and is repaired here (FND-P08,
`differential_reasoned`): the call becomes `perform_clinical_assessment{functional_neuro_signs}`,
and the observation becomes the case's own report — the teacher's version had asserted a positive
Hoover sign and distraction-induced improvement that FND-P08's examination does not document, so
the following turn's reasoning is re-anchored on the two signs the case does record. The other
seventeen are not scored as errors, because the battery is a legitimate optional study, but they
teach the student to reach for a 1 104 EUR battery when the answer is an examination. That is a
regeneration item, not a patch: **the corpus rewrite must route the functional-signs examination
through `perform_clinical_assessment` in FND, and the cognitive screen likewise in the dementias,
migraine and NPH.**

The battery itself is now an explicit OPTIONAL action in all 30 cases with a report derived from
each case's own history, which is also what un-bans `order_specialized_test` for the trajectory
gate: that gate bans a tool by name unless the case's own `optimal_actions` name it, so condemning
two of its studies had banned all of them.

**One deliberate departure from their wording, flagged for confirmation** (§8.5 of the register):
video-EEG is REQUIRED, not optional, in the 22 cases with paroxysmal events. A recorded habitual
event without ictal EEG correlate is the positive diagnostic act for psychogenic non-epileptic
seizures at the ILAE 2013 *documented* level of certainty; no bedside sign substitutes for it, and
all 30 cases are inpatient admissions made for exactly that purpose. That keeps the required set
at 1 242 EUR in those 22 cases, which is honest rather than tidy: restraint is not diagnostic
nihilism. `EMG_NCS` was also removed from the panel's optional list, since a panel cannot offer as
defensible what every case now scores as waste.

### Remaining work

**1. Redeploy the review app** — pair with sending the reply, since it changes what the
reviewers see. `bash deployment/hostinger/deploy.sh`. The VPS is running a 2026-07-10
snapshot.

**2. Author three more `conditions.yaml` entries** — DLB, spontaneous ICH, HSV encephalitis
(vascular dementia is done, see the section above). Each needs `name`, `abbreviation`,
`icd_code`, `description`, `typical_demographics`, `encounter_type`, `required_modalities`,
`optional_modalities`, `key_findings` per difficulty, `differential_diagnoses`,
`difficulty_variants`, `common_followups` — ~90 lines, modelled on `vascular_dementia`. Source
from the guidelines the reviewers cited. DLB needs `MIBG_scan` and `DaTscan`, both already
priced.

**3. Generate 90 cases** (3 × 30) for those three conditions. The 30 `PERI-NEURO-*` cases are
already retired and vascular dementia's 30 are already in. Note that
`generate_batch.sh` calls `claude -p` and refuses to run inside a Claude Code session; the
vascular-dementia set was authored in-conversation against the same criteria pack, then
validated through `NeuroBenchCase`, the MockServer and both release gates. Rebuild the split
afterwards with:

```bash
uv run python -m neuroagent.training.data.make_train_test_split \
  --dataset data/neurobench --output data/neurobench/splits --test-size 100 \
  --preserve data/neurobench/splits/split_manifest.json
```

so the added cases are placed without reshuffling anything already assigned.

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

**7. Migraine's required set is vacuous, and the FND pass is what exposed it.** Measuring the FND
required pathway made the comparison possible: **15 of the 30 migraine-with-aura cases have a
required workup that costs nothing**, because their only required tool calls are the two zero-cost
universal tools (`search_medical_literature`, `check_drug_interactions`). An agent scores 1.0
required coverage in those cases without performing a single diagnostic act. This is the same defect
FND had, one step worse, and it is Reviewer 1's own annotation: the ICHD-3 structured history is the
*only* true required test for this condition, `perform_clinical_assessment
{structured_headache_history_ichd3}` exists and is priced at 138 EUR, and no case calls it. Fixing it
is the migraine slice of item 4 above and should be done in the same shape as the FND pass.

**8. The GRPO prompt datasets were broken, not merely stale, and are now renamed.** The 2026-08-05
build referenced 30 deleted `PERI-NEURO` cases (28 train, 2 test) and lacked the 30 new vascular
dementia ones. They are preserved as `*.stale-2026-08-05.jsonl` so the training script fails to find
its input rather than silently using a broken one, `data/neurobench/grpo/README.md` records why, and
`agent-platform/tests/test_grpo_prompt_dataset.py` now fails if a present artifact disagrees with the
split. Regeneration needs the training extra and a tokenizer.

**9. One reviewer annotation is now orphaned, by design.** Reviewer 1's `SOSTITUIRE PATOLOGIA` on
`condition_tool:peripheral_neuropathy:interpret_labs` points at a condition that no longer exists in
the catalog, because we did what it asked. The annotation file is untouched — it is their record, not
ours to rewrite — and the catalog simply no longer has a row to render it against.

**6. Re-baseline.** `clinical_reward.py` feeds `(action_precision + action_recall)/2` into
GRPO, so every published number and trained adapter predates the scoring fix.
