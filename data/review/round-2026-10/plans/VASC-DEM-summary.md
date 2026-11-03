# VASC-DEM: condition summary of the October 2026 review round

Condition auditor, 24 October 2026. Sources: the plan (`plans/VASC-DEM.md`), the 30 case logs
(`logs/VASC-DEM-*.md`, each with a worker table, a verifier section and, for 18 cases, a
"Condition audit" section), and scripted checks over the 30 case files. VASC-DEM has never been
annotated by a physician: there is no `notes/VASC-DEM.md` or `.json`, so there are no note ids to
rule on, and every change below comes from the lead survey, the workers, the verifiers or this audit.

## Final state

- `perfect_agent.py` on all 30 ids: 30/30 pass, no warnings. `case_io.py check` on all 30 ids:
  schema OK for every case, synonym guard OK; the suite's 47 failures are elsewhere and none names a
  VASC-DEM case or the condition. `test_case_guards -k VASC-DEM`: 60 passed (the leak test failed in
  all 30 at baseline).
- Note ids: none exist. Every log says so in its reviewer-notes table.
- Scripted uniformity checks over the 30 files, all clean after the audit fixes below:
  - C1: every MRI criterion is `analyze_brain_mri {}`; no `sequences` key anywhere in a criterion.
  - C2: no literature criterion, no literature initial output, no literature fallback.
  - C3: no `drug_interactions` fallback. Group R (recommended, one alternative per drug, case-keyed
    outputs): M03, M07, M08, M10, P08, S06, S07. Group O (optional `{}`, case content): M05, P04, P05,
    P09, S05. Group D (no criterion, initial null): the other 18.
  - C4: every `mental_status` is a bedside observation ending "Formal cognitive screening reported
    separately"; no MoCA, MMSE or "/30" in any exam. The P07 GP MoCA 26/30 (red herring) and the P02
    headache-MRI history stay in the HPIs as the plan rules.
  - C5/C17: no report states the severity, the dementia diagnosis, sufficiency for the syndrome or
    management. The audit found two leaks the per-case passes left (below: `criteria_met` severity
    keys in 11 cases, M01 neuropsychology "independent by informant report"). The kept Kind 2
    statements are the Boston v2.0 sentence (P03, P04), hedged "suggestive of an embolic mechanism"
    (M03, S06, S07), the NOTCH3 genetic result (P05, P06), the style-guide FDG wording
    "consistent with an Alzheimer-type metabolic profile" (M07, M08, P02), and neuropsychological
    profile descriptors ("storage-type", "retrieval pattern") in battery reports only.
  - C6: Hb and Hct ranges match sex in all 30; Hct about 3 x Hb in all 30; female HDL ">50", male
    ">40"; every eGFR range ">=60"; no INR in a CMP (P03, P04 have Coagulation panels); every
    `clinical_significance` null; every `is_abnormal` flag agrees with its range; every eGFR within 3
    of the CKD-EPI 2021 value for the stored creatinine, age and sex; every lipid panel satisfies
    TC = LDL + HDL + TG/5 within 3 mg/dL; no labs interpretation mentions a target, dosing or
    "excluding"; the template normals (WBC 6.8, Hct 41.6, Plt 238, MCV 88, Na 139, K 4.2, albumin
    4.1, folate 11.8, ALT 22) occur nowhere.
  - C7: no `advanced_imaging` or `labs` fallback; no "already obtained", "non-contributory" or
    "better characterised on the MRI" text; every CT fallback describes the patient's own CT.
  - C13: no rationale equals its label; only bracketed citation keys.
  - C16: only soft constraints, all ids valid. Screen before MRI everywhere (P08: screen before CT);
    MRI before the CSF/amyloid criterion in M01, M05, M07, P01; ECG before monitoring in M04, P08,
    P09, S07, S09; MRI before NOTCH3 in P05, P06; duplex before MRA in S08; labs before MMA in S04.
    Stop rule: `required_before_assessment` equals the required set in all 30 and
    `max_additional_actions` is 1.
  - C18: no duplicate avoided entries; the canonical CT rationale in the 28 cases that score CT as
    waste (P09 adds its own reason); no avoided rationale reuses the August template text (fixed here
    in M01-M06).
  - Tiers match plan sections 3 and 4 (gait C14, ECG/TTE/monitoring C10, biomarkers C9, NOTCH3,
    young-SVD labs C15). Logged departures are listed under "Decisions beyond the plan".

## Error classes and how each was fixed

| class | defect | cases | fix |
| --- | --- | --- | --- |
| C1 unmatchable MRI criterion (blocker) | `required_arguments` held `sequences`/`protocol`/`contrast`; no real call matched the required MRI. | 29 (all but P08) | `analyze_brain_mri {}`. P08's CT criterion lost its `angiography`/`contrast` arguments too. |
| C2 literature leak | Literature criterion's expected evidence copied into its own output (leak test failure). | 30 | Criterion, initial output and fallback deleted. |
| C3 drug checks | Generic optional check and a false "no prohibitive interaction" fallback in all 30. | 30 | Fallback deleted; groups R, O, D as listed above, with real pairs (warfarin or DOAC with aspirin, AChEI with bisoprolol or diltiazem, edoxaban renal dosing, gliclazide with perindopril, sumatriptan in CADASIL, zolpidem, apixaban in CAA, dextromethorphan-quinidine). |
| C4 screen in the exam | MoCA total and items in `mental_status`. | 30 | Bedside observation, canonical closing sentence. |
| C5/C17 Kind 1 leakage | Reports stated the diagnosis, severity, mechanism, sufficiency, differential essays or management. | 30 | Modality-only rewrites (STRIVE-2 MRI, velocity-only duplex, rhythm-only ECG, binary amyloid PET, measurement-only gait, profile-only neuropsychology). Audit: `criteria_met` severity keys removed in 11 cases. |
| C6 lab carry-over and arithmetic | Female ranges in men, template normals, Hct vs Hb, eGFR vs creatinine, Friedewald, INR in CMP, interpretive text, wrong flags (ALT 46 unflagged, MCV 99 called macrocytic, UACR 148 called macroalbuminuria, Hct 47.8 called erythrocytosis). | 30 | Per plan; creatinine or eGFR made consistent case by case; audit fixed the remaining Friedewald (13 cases) and eGFR (M02) mismatches. |
| C7 off-pathway fallbacks | "non-contributory" fallbacks; CT "already obtained"; Holter and library ECG in sinus rhythm for patients in AF; echo "No cardioembolic source"; identical echo fallback text in S01-S05. | 30 | Fallbacks deleted or rewritten to the patient (AF Holter in M07, M08, M10, P04, S06; case ECGs in M07, M08, P04, P06; echo text varied). |
| C8 stale differential | Excluded alternatives left moderate or high; P06 listed its own diagnosis. | 25 | All excluded alternatives low; P06 self-entry deleted; P08 CAA kept moderate ("cannot be excluded on CT"). |
| C9 biomarker route | CSF-only route; LP harm in chronic CAA; CSF biomarkers recommended in MCI. | M01, M05, M07, M08, P01, P02, P03, P04 | Two-alternative amyloid criterion with authored positive PET (M05, M07, P01); PET only with CSF harm and a concordant CSF follow-up (M08, P02); CSF waste with an authored CAA-pattern CSF (P03, P04); M01 CSF optional. Verifiers corrected tracer thresholds and SUVR-Centiloid pairs (M07, M08, P01, P02). |
| C10 embolic work-up | No ECG after ischaemic infarcts; TTE and monitoring scored as waste after cortical or thalamic infarcts; MRA claimed to show the artery of Percheron; carotid imaging after a deep ICH. | M04, P09, S09, M09, S08 (plus S01, M06, S11 at verification) | Per plan; S01 ECG recommended and echo waste removed (clinical lacunar events); M06 cervical-vessel criterion added (anterior border-zone infarcts); S11 and S10 histories record the admission work-up that justifies their waste entries. |
| C11 P08 device report | Pacemaker interrogation coded as a loop recorder. | P08 | `order_cardiac_monitoring {}`, descriptive `monitor_type`; CENTRAL `device_interrogation`. |
| C12 carotid threshold | "Below the 70% threshold" for a symptomatic 50-69% stenosis. | S11 (P08, S08 checked) | Sentence removed; vascular-team must and prohibition; S11 duplex required. P08 grade corrected to 50-69% from its velocities, managed medically (last event 8 months ago); S08 CEA referral (3 months). |
| C13 criterion metadata | Rationale = label; unbracketed duplicate keys. | 30 (228 criteria) | Case-specific rationales, bracketed keys. |
| C14/C15 gait and young-SVD labs | Tiers wrong or criteria missing. | M01, P01, P05, P06 (and the required group) | Per plan; P05 and P06 young-SVD panel served by the initial labs and by a targeted follow-up. |
| C16 order and stop rule | Neuropsych and mechanism studies out of order; `max_additional_actions` 0. | 30 | Reordered with ids kept; max 1. |
| C18 avoided rationales | "already obtained", generic text. | 30 | Case-specific; audit replaced the surviving template MIBG and autoimmune rationales in M01-M06 (the autoimmune one called every case a "chronic stepwise decline with a hypertensive imaging burden"). |
| C19 musts | Musts restated diagnostic steps; no targets; S05 taught stopping apixaban for sinus rhythm after ablation, falls and deep microbleeds. | 30 | Management musts with the case's numbers and plan 1.2 facts (BP below 130/80 or individualised; LDL below 70 only with atherosclerosis; HbA1c about below 8.0%; DOAC dose criteria with Cockcroft-Gault, weights added in M08, M10, P04, P08, S05, S06, S07; warfarin INR 2-3 for LV thrombus; CAA: stop aspirin, avoid anticoagulation, LAAO). S05 now continues apixaban on CHA2DS2-VA. |
| C20 CADASIL | Non-canonical variant (P05); P06 mechanism "cadasil". | P05, P06 | Canonical `c.544C>T p.(Arg182Cys)`, EGFr 4; P06 VUS report, mechanism "svd". |
| MoCA arithmetic (worker class) | Item losses did not add up to the stated total; fluency item scored on animals instead of letter F; serial sevens scored out of 5; "fully oriented" in a dense amnesia (S09). | about 27 | Item-level findings summing to the unchanged totals (education point applied where the MoCA gives it); M09 kept category fluency because the Mandarin version uses it. |
| Anatomy, laterality and timeline (worker class) | M10 left occipital infarct for a left hemianopia; M04 left-field driving errors from a left angular infarct and a "transient" deficit still present; M03 Wernicke's area infarct without aphasia; M05 pure VPL lacune with motor signs; S06 right precentral infarct with no left signs; S07 calcarine infarct with full fields; P03 siderosis on the wrong side; infarct counts and volumes wrong (S06, S07, S09, S10). | 12 | Corrected in the reports and every field that mentions them (M10: right occipital infarct with a non-fetal PCA documented). |
| Other wrong facts (worker class) | PR 192 ms called first-degree block (M06); valve click with a bioprosthesis (M06); AF burden 4.9% from 5 h over 26 days (S07); left ICA "40-50%" with a PSV in the 50-69% band (S08); LDL 55 polyvascular target (M10, S08); HbA1c 7.8-7.9% called above target in older adults with dementia (M09, P07); B12 296 called normal without MMA (M01); B12 244 on metformin with neuropathy (S04, MMA criterion added). | 10 | Fixed in each case. |
| HPI timeline leaks | HbA1c given in the HPI (M05, S11); exam sentences naming the cause (M02, S01, S04, P09). | 6 | Removed. |

## Changes made by this audit (logged in each case's "Condition audit" section)

- Lab arithmetic: total cholesterol set to LDL + HDL + TG/5 in M03, M05, M06, P03, P08, P09, S02,
  S03, S04, S05 (flags unchanged); where TC is flagged and quoted, HDL (M01) or triglycerides (P07,
  S01) moved instead; M02 eGFR 84 to 92 (creatinine 0.92, man of 66).
- Severity leak: `criteria_met.independence_in_iadl_lost` (and `executive_predominant_profile`,
  `occupational_function_lost`, `onset_before_60`) removed from the cognitive screen in M01-M06 and
  P03-P07, matching the other 19 cases; M01 neuropsychology `functional_status` now gives the FAQ
  score instead of "independent by informant report". The P03 worker's flag is thereby resolved.
- Screen findings: the "retrieval pattern" suffix removed from the memory row of the cognitive screen in
  P03-P06.
- Avoided rationales: template MIBG and autoimmune-panel rationales replaced in M01-M06.

## Counts

- Notes: FIXED 0, ALREADY-FIXED 0, DECLINED 0, BLOCKED 0 (no notes file exists).
- Own findings fixed: about 660 table rows marked FIXED across the 30 logs (workers, verifiers and
  this audit's 36 rows in 18 cases), plus 21 verifier fixes described in prose (M07, M08, M09, P01,
  P02, P03, P05, P07, P08, P09 x2, S01 x3, S02, S04 to S09).
- Own findings flagged: 11 rows, of which 1 is now resolved by the audit (P03 `criteria_met`). The
  10 remaining: em dashes in `accepted[0]` labels (M01, M02, M05, P06, P07, P08: ruling 3, central)
  and in untouched report strings (P03, P04, P05, P06, P07: plan rule, left), and P07's B12
  322 pg/mL (normal; diabetic neuropathy explains the vibration loss, no change).
- Cases changed: 30 of 30. Approved cases changed: 0 (no VASC-DEM case was ever approved).

## DECLINED and BLOCKED notes

None: the condition has no reviewer notes, and no own finding was left BLOCKED.

## Decisions beyond the plan (taken and logged; listed so a re-reviewer can check them)

- S01 and P07: the plan's covert-SVD "no antiplatelet" prohibition was not applied; both have dated
  clinical lacunar events, so single antiplatelet therapy continues (AHA 2021). S01's ECG raised to
  recommended and its echo waste removed by the verifier.
- M07, M08: optional ECG with an authored AF report (the library ECG would show sinus rhythm before a
  cholinesterase inhibitor on a rate-control drug). M08: weight 71 kg added, Cockcroft-Gault 46 mL/min,
  so the must reduces edoxaban to 30 mg; edoxaban added as a fourth drug-check alternative.
- M06: carotid imaging added (recommended) for anterior border-zone infarcts.
- S04: recommended methylmalonic acid criterion (B12 244 pg/mL, 22 years of metformin, neuropathy).
- S11: duplex required (the discharge letter gives no carotid result).
- P02: CSF avoided as harm (refusal after lumbar fusion), as the plan says for M08 and P02.
- P05, P06: young-SVD panel both in the initial labs and as a targeted follow-up.
- P05: `accepted[0]` changed in its variant string only, per plan C20 (entity unchanged).
- This audit: Friedewald consistency enforced condition-wide (half the cases had been fixed by the
  workers, so the class had to be closed in the rest).

## CENTRAL requests (consolidated)

1. Synonyms (`diagnosis_synonyms.yaml`): remove `F06.7` from the F01 codes and `F01.50` from the
   F06.7 codes, so M01 (mild VCI) is not credited a dementia answer and the 29 dementia cases are not
   credited a mild-VCI answer (P07 is the case most exposed). Add a mixed-dementia entry (labels
   "mixed dementia", "mixed Alzheimer and vascular dementia"; F01.5x with G30.x, F02.8x) for M05,
   M07, M08, P01, P02 and stop crediting bare "vascular dementia" there. Add CAA labels and I68.0 for
   P03, P04. Reconsider the umbrella "vascular cognitive impairment" label in both entries, and the
   subtype labels credited across mechanisms ("subcortical vascular dementia" for the large-artery
   S08, "multi-infarct dementia" for the strategic single-infarct S09). Check that the P05 label's new
   variant string is reflected wherever the label is mirrored. Optionally strip the em dashes from
   the `accepted[0]` labels of M01, M02, M05, P06, P07, P08.
2. Criteria pack allow-list: `[AHA_ASA_2022_ICH]`, `[ESC_AF_2024]`, `[ADA_2025_older_adults]`,
   `[NICE_NG97]`, `[Rutten_2019]`, `[BSH_B12_2014]` (S04, already used in ALZ-EARLY); consider
   `[ESH_2023]` (P06 same-day BP handling with grade 3 retinopathy, currently cited under
   `[ESO_2021_SVD]`).
3. Criteria pack text: literature and drug-check tiers superseded by rulings 5 and 6; gait tiers per
   C14; TTE is reasonable (2a) after ischaemic infarcts; LP is waste, not harm, in chronic CAA.
4. Vocabulary: `order_cardiac_monitoring` `device_interrogation` term in `costs.yaml`, the library and
   the `tool_io.py` mirror (P08); fold `B12` and `vitamin_B12` into one assay.
5. MockServer: add `monitor_type` as a discriminator for `order_cardiac_monitoring` (as `echo_type`
   is), so a Holter order does not receive a stored 30-day monitor or device report (M04, P08, P09,
   S07, S09).
6. Schema: a `weight_kg` vital; weights for DOAC dosing currently sit in `physical_exam.general`
   (M08, M10, P04, P08, S05, S06, S07).
7. `perfect_agent.py`: fail when a criterion's `required_arguments` key is not in the tool schema (C1
   passed 30/30 at baseline); fix the "<- ?" display for stored outputs with null fields.
8. Library: the `analyze_csf` default returns a normal Abeta42 for any case; CAA and mixed cases now
   author their own CSF, but other conditions may be exposed.
9. Metadata hygiene (not read by the harness): `metadata.revision_reason` in M01-P08 still describes
   the August literature/interaction audit; `metadata.fallback_tool_kinds` labels case-specific
   fallbacks (AF Holters, patient-specific CT) as "normal".
10. Review UI: show tool outputs in criterion order.

## Open questions for Andrea

None that needs information only Andrea has. Three decisions she may wish to revisit:

1. HIV and RPR stay in the required dementia panel at every age (plan C21: pack and US practice;
   NICE NG97 does not test routinely).
2. `max_additional_actions` is 1, as in ALZ-EARLY and ISCH-STR.
3. VASC-DEM has had no physician review at all; every clinical decision above (including the S05
   reversal to continue anticoagulation, the M10 laterality correction and the M08 edoxaban dose
   reduction) rests on the plan, the workers, the verifiers and this audit. The condition should be
   included in the next physician review round.
