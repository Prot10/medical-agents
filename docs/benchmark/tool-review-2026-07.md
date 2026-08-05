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
