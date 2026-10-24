# NMDAR-ENC: condition summary, October 2026 review round

Condition auditor, 24 Oct 2026. Scope: the 30 anti-NMDA receptor encephalitis cases (M01-M05,
P01-P08, RM01-RM03, RP01-RP03, RS01-RS04, S01-S04, S06, S09, S10), after workers and adversarial
verifiers. Inputs read: `ROUND_POLICY.md`, `PATTERNS.md`, `plans/NMDAR-ENC.md` and the 30 case logs.
There is no `notes/NMDAR-ENC.md`: no physician reviewed this condition in this round.

## Final state

- `perfect_agent.py` (30 ids): 30/30 pass. The only warnings are by design. They are the 7 SIADH
  osmolality criteria and the P02 germ-cell marker criterion, which the initial labs report
  answers (plan 3.2).
- `case_io.py check` (30 ids): schema OK for all 30, synonym guard OK, no test failure names an
  NMDAR-ENC case.
- `test_case_guards.py -k NMDAR`: 60 passed. At baseline 18 cases failed the any-query leak guard.
- Audit scripts over the 30 files found these fields uniform:
  - Criteria order: labs, MRI, CSF, routine EEG, tumour, cEEG, extras, DDI, literature.
  - Tiers and minimal `required_arguments` follow plan 3.2. No `basic`, `screen_for`, `query`
    or `protocol` key remains.
  - Labs criteria: beta-hCG in women 12-50 (RS02 is excepted, see below). Patients 45 or older
    have the onconeural and autoimmune panels. RM02, RS02 and RS04 have MOG/AQP4.
  - Imaging and CSF criteria: MRI `{contrast: true}`. CSF has the HSV PCR, anti-GluN1 and
    OCB/IgG-index alternatives, plus RT-QuIC in RP01. Tumour imaging is chosen by age and sex.
  - The cEEG criterion is recommended in 29 cases and absent in RP01. All 30 cases have a cEEG
    follow-up that agrees with the routine EEG.
  - DDI tiers follow C10. Literature is optional with `{}` and always last.
  - Every case has one soft MRI-before-CSF constraint. No constraint is hard.
  - Stop rule: the five required ids and `max_additional_actions: 2`.
  - CSF reports: one `NMDAR_antibodies` key with a final titre. Labs reports: one serum entry
    in `Serum anti-GluN1 IgG (cell-based assay)`, no CSF row, and `clinical_significance` null.
    No analyte is duplicated.
  - CSF/serum glucose ratios are all between 0.57 and 0.68 and agree with the stored values.
  - All differential entries are `low` and the mimics the plan names are present.
  - Musts and prohibitions: P1-P5 are present. The cEEG must appears only with its criterion.
  - Fallbacks: the advanced-imaging and specialised-test fallbacks are null. Every case has an
    initial ECG within 5 bpm of the vitals heart rate. The cardiac-monitoring maximum is at or
    above the vitals heart rate.
  - Red-herring field paths all resolve. Hyponatraemia grades match the sodium value.
  - Literature and DDI outputs are in report voice with real sources, checked against plan 1.2.

## Error classes found and how each was fixed

The class ids are the plan's (section 2). Workers applied each one to every case it names;
verifiers checked each case against the file.

| class | what was wrong | fix | cases |
| --- | --- | --- | --- |
| C1 unreachable criteria | `analyze_csf.basic`, `check_drug_interactions.screen_for`, exact literature `query`, MRI `protocol: standard` and an 11-panel labs list. A schema-conformant agent could not satisfy the required CSF criterion | minimal arguments of plan 3.2 | 30 |
| C2 literature as a clinical step | `search_medical_literature` recommended | optional, `{}`, last, general expected evidence | 30 |
| C3 scoring key and placeholders in any-query outputs | placeholder literature findings; DDI summaries repeating expected evidence; fallback DDI "(agent not specified...)" | canonical literature output and case-specific literature checked against facts (S09 bilateral-resection claim deleted, RP03 "27%"); DDI rewritten from each patient's medicines; fallback `proposed` empty | 30 (18 failing the guard) |
| C4 CSF result in the serum report | CSF anti-NMDAR in the labs, sometimes inside the serum panel; CSF report "Pending" against a titre in labs (14); P02/P03 both pending and positive; S10 titre 1:56 | final titre in one CSF key; one serum entry in labs; S10 CSF 1:64 | 30 |
| C5 labs template | duplicates, leaky "Exclusion studies" panel, "Reviewed inflammatory markers", narrative parentheticals, missing beta-hCG, HIV, onconeural panel, SIADH values | panels rebuilt with the case's values; plain recital; SIADH osmolalities where Na < 130 | 30 |
| C6 pathway order | follow-ups began with literature or DDI in 18 cases | reordered per plan 3.1, ids kept | 30 |
| C7 cEEG must without a study | 17 cases had no cEEG follow-up, so the library's normal cEEG contradicted routine EEGs with seizures | cEEG follow-up consistent with the routine EEG in all 30; criterion recommended in 29 | 30 |
| C8 templated differential | HSV `high` and the other entries left unchanged after negative results | assessment-time likelihoods. Mimics added: SREAT, MOGAD/ADEM, CJD, leptomeningeal disease, bipolar relapse, drug-induced hyponatraemia, valproate encephalopathy, NPSLE, Wernicke | 30 |
| C9 templated musts and prohibitions | seven template musts, a diagnostic "paired CSF and serum" must, "levetiracetam or valproate", "in a young patient" | canonical M1-M10 with case cautions (renal dosing, lamotrigine, diabetes, allergies, pregnancy potential); P1-P5. Case-specific musts: nivolumab withdrawal (RP02), orchiectomy (P02), ovary-sparing bilateral cystectomy (S09), ophthalmology and early PLEX (RS04), thiamine and LP timing after enoxaparin (RS02), stopping oestrogen contraception with IVIG (RS01, S01, S03) | 30 |
| C10 DDI tier and content | DDI recommended everywhere with empty interactions | required only in P07 and RP02; recommended in M02, M04, RM02, RM03, RS02; optional elsewhere; real pairs from the medication list | 30 |
| C11 wrong study for tumour imaging | CAP CT through `order_ct_scan` (P02, P03); pelvic ultrasound at 50 and 62 (RS02, RM03); testicular-ultrasound musts at 63 and 76 | women 12-44 pelvic US, men < 45 scrotal US, age 45 or more contrast CAP CT. P02 staging CT moved to `order_body_imaging`; P03 dead follow-ups deleted | 5 |
| C12 body-imaging impressions in lab voice | "Abnormal values: ... (H)" | radiology voice. Characteristic teratoma features where removal is planned. M03 equivocal lesion characterised by a new pelvic MRI criterion and follow-up | 24 |
| C13 cross-modality and management text | "correlate with CSF", "requiring urgent cEEG", ECG causal tails, CSF interpretive values | stripped per the style guide | many |
| C14 contradicting fallbacks | catch-all FDG-PET and neuropsychological (S10: EMG) fallbacks; fallback ECG 58-88 bpm against HR 91-138; Holter averages 68-82 | catch-alls null; initial ECG at the vitals HR; telemetry matching the exam | 30 |
| C15 red herrings and key evidence | "Mild hyponatremia" at 122-129; prodrome red herring without a prodrome (RP02); "previously well young adult" with psychiatric history or at 62; identical key evidence with false claims ("100% sensitive", "30-50%") | graded sodium; canonical interpretations; 4-6 case-specific key-evidence bullets | 30 |
| C16 rationale = label | every rationale repeated its label | one clinical sentence with the case anchor; case-specific tumour evidence | 30 |
| C17 template carry-over | copied CSF numbers, titres, lesion sizes and ECG rates; diagnosis leaks in medication indications (M04, M05); medication lists disagreeing with the HPI (P07, RM02, RS02, M05, M01/M02 sertraline) | distinct plausible values; prescriber indications; lists reconciled | 12 + audit |
| C18 stop rule and sequence | no sequence constraints; `max_additional_actions: 0` | soft MRI-before-CSF in all 30; allowance 2 | 30 |

Classes found by workers and verifiers beyond the plan:
- Low CSF/serum glucose ratios. They were corrected wherever they were below 0.5 or did not
  match the stored values (RP01, RP02, S10 and others).
- Laterality flips. P08 and RP03 were aligned with the examination, and RS02 was aligned with
  its left-sided deficits.
- Impossible timelines:
  - RP03 calendar dates became relative.
  - RP02 smoking-cessation date.
  - P07 cannabis timing against a positive screen.
- Haematocrit inconsistent with haemoglobin (S01 and others).
- Swapped structured EEG fields (S09, S10).
- Interpretation inside a lab reference range (S09, S10 urine sodium).
- Fallback echo normal against LVH on ECG (RP01, RP03).
- Postmenopausal status unstated at 50 (RS02).

## Straggler fixes made by this audit (logged in each case's "Condition audit" section)

- **Canonical P2/P4 prohibitions still contained an em dash and an en dash** (12 cases: P08,
  RM01, RM02, RM03, RP01, RP02, S02, S03, S04, S06, S09, S10). Changed to the dash-free canonical
  wording already used in the other 18 cases. Meaning is unchanged.
- **cEEG follow-up report without `eeg_type`** (P08, RM01, RM02, RM03, RP01). Set to
  `continuous_icu`, which the MockServer discriminator reads.
- **Follow-ups without `tool_parameters`.** P02 (cEEG and staging CT) and P04 (cEEG) now have
  them.
- **P07 stop rule listed the required DDI as a sixth id.** Removed, to match plan 3.5 and RP02.
  The stop rule names the evidence needed before the diagnosis is submitted. Required coverage
  already penalises a missing DDI, so the criterion stays required.
- **RM03, 62 years old:**
  - The amyloid-PET waste rationale still said "in a young patient". It now names her age and
    course.
  - The AMT of 7/10 contradicted an exam that fails at least five items. It is now 5/10.
- **RM01, RM02.** "Previously well young adult" in women with treated hypothyroidism now reads
  "young adult with no psychiatric history".
- **C17 carry-over left after the workers:**
  - S10 had the same antibody pair as S06 (CSF 1:64, serum 1:512). S10 serum is now 1:256.
  - RS01 had the same pair as S01 (CSF 1:320, serum 1:160). RS01 serum is now 1:80.
  - M03's lesion was the same size as M01's (1.2 cm left ovarian). It is now 1.5 cm on
    ultrasound and 1.5 x 1.2 cm on MRI.
- **RP01, RP02 cEEG impressions** lacked the template closing "Clinical correlation recommended."
  It has been added.

## Counts

| item | count |
| --- | --- |
| Reviewer notes FIXED / ALREADY-FIXED / DECLINED / BLOCKED | 0 / 0 / 0 / 0 (no notes exist; all 30 logs say so) |
| Own findings FIXED (worker tables, 30 logs) | 650 |
| Own findings FLAGGED and kept (worker tables) | 6: M01 (CSF titre above serum), M03 and M04 (MRI side differs from EEG focus), M04 (one US spelling in British prose), P01 (two serum glucose values from different times), P01 (clock-drawing clustering) |
| Further fixes by verifiers, outside the tables | about 30, in 17 cases |
| Fixes by this audit | 29 edits in 17 cases (M03, P02, P04, P07, P08, RM01, RM02, RM03, RP01, RP02, RS01, S02, S03, S04, S06, S09, S10) |
| Cases changed in this round | 30 of 30 |
| Approved cases changed | 0 (no NMDAR-ENC case was approved) |
| Label changes | 1: RP01 (plan decision, CENTRAL 3) |

## DECLINED and BLOCKED notes

None. The condition has no reviewer notes, and no own finding was left BLOCKED.

## Judgment calls settled by this audit (no input needed)

- **Mixed titre series** (10 cases: M01, M02, P01, P07, P08, RM01, RM02, RM03, RP03, and earlier
  S06/S10). Serum on the 1:10 series with CSF on the 1:2 series is kept.
  - Reason: reference laboratories titrate serum and CSF from different starting dilutions (serum
    usually from 1:10, CSF undiluted or from 1:2).
  - What plan 1.2 forbids is a value outside any series (S10 "1:56"). No value now falls outside
    a series.
- **CSF titre above the serum titre** in most cases. This is kept. With separate
  starting dilutions the numbers are not directly comparable, and the CSF-decisive pattern is
  the teaching point of the condition (P5, Gresa-Arribas 2014).
- **M03 and M04 MRI side differs from the EEG focus.** This is kept. The disease is diffuse, and
  the two findings are different phenomena, not one finding with its side flipped. M03's left
  facial droop matches its right-sided MRI signal.
- **RS02 without beta-hCG.** This is accepted. She is documented postmenopausal since age 48,
  which agrees with the atrophic endometrium. Pregnancy testing is not indicated, although the
  plan's age rule (12-50) would include her.
- **RP01 without amyloid-PET and DaTscan waste entries.** This is accepted. The entries never
  existed in this case; plan 3.3 keeps existing entries and does not require adding them.
- **RP01 without a seizure must.** This is correct. There are no seizures and no epileptiform
  activity on either EEG, and prophylactic antiseizure treatment is not indicated.
- **RP02 open questions** (the baclofen/clorazepate must; steroids with IVIG or PLEX from the
  start). The verifier resolved both, with ASCO 2021 and CKD 3 pharmacology. I agree.
- **Level of care by the plan's M6 rule** (ward with ICU triggers in RM01, RS04, S01 and S10;
  ICU in P05, P06 and S06 by the listed triggers). The workers applied the rule case by case, and
  their reasons are logged. Not changed.
- **Plan inconsistency.** The SIADH row of plan 3.2 lists P08, but P08's sodium is 130 and the
  rule is "below 130". P08 correctly has no SIADH criterion and no M9.
- **Criterion ids.** The cEEG criterion keeps its old id in some cases and is `ceeg-escalation`
  in others. The plan's `cEEG-escalation` fails the schema id pattern. The new SIADH criteria use
  either `siadh-osmolality-workup` or `siadh-workup`. These ids are referenced only inside their
  own case, so they were not unified.

## Consolidated CENTRAL requests

1. **Citation registry.** Add the following to the NMDAR-ENC allow-list (criteria pack
   section 8):
   - `[Titulaer_late_2013]`, `[Gresa-Arribas_2014]`, `[Abboud_2021]`, `[Dalmau_2019]`,
     `[Lejuste_2016]`, `[Armangue_2018]`;
   - `[Venkatesan_2013]`, `[Solomon_2012]`, `[Herman_2015]`, `[Spasovski_2014]`,
     `[ASCO_irAE_2021]`, `[Graus_2021]`;
   - `[EAU_Testicular_2024]`, which only P02 uses, for its germ-cell markers and staging CT
     criteria.
2. **Non-schema criterion keys (dataset-wide).** `analyze_csf.basic` (63 case files) and
   `check_drug_interactions.screen_for` make criteria unreachable for schema-conformant agents.
   `perfect_agent.py` does not catch this because it replays ground truth. Request one of:
   - strip annotation keys before matching;
   - a test that rejects non-schema criterion keys.
3. **RP01 label change.** `accepted[0]` is now "Anti-NMDA receptor encephalitis following
   COVID-19 (CSF-positive, serum-negative)". Rerun `apply_diagnosis_synonyms.py`; the synonym
   guard already passes.
4. **Case fallbacks for catch-all tools.** A case fallback for `order_advanced_imaging` or
   `order_specialized_test` is served for every modality or test type. Request a validator rule
   against a specific `modality`/`test_type` in such a fallback. Also add a note to the tool
   contract that library normals for alternative studies can contradict the pathway.
5. **Literature `query` matching** is by string equality. Request a test that flags `query` in
   `required_arguments`.
6. **Criteria pack `NMDAR-ENC.md`.** Corrections:
   - "Probable = clinical features + abnormal CSF or MRI suggestive" is wrong. Use Graus 2016:
     four groups, or three with a teratoma, plus an abnormal EEG or CSF pleocytosis/OCB. MRI is
     not a probable criterion.
   - Extreme delta brush "30-50%" should be 30% (7 of 23, Schmitt 2012).
   - Section 7 "5-10% of HSV cases" is wrong. Armangue 2018 found autoimmune encephalitis in 27%
     of HSV encephalitis patients, 64% of them with NMDAR antibodies (RP03).
   - DDI and literature are not "Required".
   - The tumour line should follow plan C11: women 12-44 pelvic ultrasound, men under 45 scrotal
     ultrasound, contrast CAP CT at 45 or older.
   - Align the pack with the July 2026 tool review.
7. **Label wording (M05).** `accepted[0]` contains an em dash ("... encephalitis - tumour-negative
   (idiopathic), male patient"). The label is not wrong, so it was not edited (ruling 3). Reword
   it centrally if label style matters.
8. **`perfect_agent.py` cosmetic.** It prints "<- ?" for initial outputs that contain null fields
   (it compares against `model_dump(exclude_none=True)`). The check itself is unaffected (M01).
9. **RP02 `metadata.case_body_concerns[0]`** proposes routing the case to a checkpoint-inhibitor
   pack. That is a routing decision for the condition owner. The case policy now encodes
   nivolumab withdrawal and the interactions the concern said were missing.
10. **Difficulty field (FYI, dataset-wide).** All S and RS cases are `moderate` with
    `expected_agent_confidence` 0.80-0.85, the generator's "straightforward" value. Not edited.

## Open questions for Andrea

- **RP01 label (decided by the lead, flagged for your veto).** RP01 is now anti-NMDAR
  encephalitis after COVID-19 with CSF anti-GluN1 1:4 and a negative serum.
  - The source case (PMC9799706) is a seronegative post-COVID autoimmune encephalitis. Inside the
    NMDAR condition, the appended synonyms rewarded "anti-NMDAR encephalitis" for a case with
    negative antibodies, so the scoring key contradicted itself.
  - Revert path: restore the seronegative label and CSF, and ask CENTRAL for
    `except_cases: [NMDAR-ENC-RP01]` on the `G04.81+nmdar` synonyms. The condition would then hold
    29 anti-NMDAR cases.
  - Only you know whether a seronegative mimic was intended for this condition.

Nothing else needs your input.
