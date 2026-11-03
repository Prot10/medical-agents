# VASC-DEM: close-out decisions (24 Oct 2026)

Andrea ruled on 24 Oct 2026: "per i punti aperti, risolvili nel modo migliore per la qualità del
dataset". Every item below is decided and, where it needed a change, applied. Per-case detail is in
each case log under "Close-out (24 Oct 2026)" (all 30 logs). VASC-DEM has never been reviewed by a
physician; the round's survey findings and this close-out are its only clinical check so far.

Sources checked on 24 Oct 2026: Knopman DS et al., Practice parameter: diagnosis of dementia,
Neurology 2001;56:1143-1153 (abstract read in the PDF: "Screening for syphilis in patients with
dementia is not justified unless clinical suspicion for neurosyphilis is present"); NICE NG97 as
reported by Pract Neurol commentary (no routine HIV or syphilis test without risk factors or
clinical features); 2026 ACC/AHA/AACVPR/ABC/ACPM/ADA/AGS/APhA/ASPC/NLA/PCNA dyslipidemia guideline,
Circulation 2026;153(17):e1154-e1276 (via the UIC drug-information summary and Guideline Central:
LDL-C goal below 55 mg/dL for clinical ASCVD at very high risk, defined as two or more major ASCVD
events, or one plus two or more high-risk conditions; major events: ACS within 12 months, prior MI,
prior ischaemic stroke, symptomatic PAD; high-risk conditions: age 65 or more, coronary
revascularisation, current smoking, diabetes, heart failure, hypertension, LDL-C 100 mg/dL or more
despite statin plus ezetimibe; below 70 otherwise; CKD below 55); ICD-10-CM FY2023 addenda (F06.70
and F06.71 replace F06.7); WHO ICD-10 F00.2 "Dementia in Alzheimer disease, atypical or mixed type"
(and the WA coding rule that it is used only when "mixed" is documented); ESC Council on
Hypertension position document on hypertensive emergencies (van den Born 2019) for malignant
hypertension. The full text of the 2026 dyslipidemia guideline and the ESH 2023 guideline is
paywalled; the statements used are the ones the summaries agree on.

## 1. Diagnosis synonyms (`diagnosis_synonyms.yaml`, VASC-DEM entries)

Applied with `apply_diagnosis_synonyms.py --prune --conditions vascular_dementia` (29 cases
changed; P05 unchanged). `--check` and `--check --prune` are clean for the condition.

| entry | before | after | reason |
| --- | --- | --- | --- |
| `F01` | 8 labels incl. "vascular cognitive impairment", "subcortical vascular dementia", "multi-infarct dementia", "small vessel disease dementia"; codes incl. F06.7 and I67.3; any condition | `conditions: [vascular_dementia]`, `except_cases` the 5 mixed cases; labels "vascular dementia", "major vascular neurocognitive disorder", "major neurocognitive disorder due to vascular disease", "VaD"; codes F01.50, F01.51, F01.5, F01.9, F01.A0, F01.B0, F01.C0 | F06.7 credited a mild-VCI answer (and its code) in all 29 dementia cases, P07 most exposed; the umbrella label matched both severities; subtype labels named other mechanisms (subcortical for the large-artery S08, multi-infarct for the single strategic S09) |
| `F01+svd` (new) | | M02, P06, P07, S01-S05: subcortical labels (both spellings of ischaemic), "small vessel disease dementia"; F01.2, I67.3 | subcortical small-vessel mechanism only |
| `F01+multi_infarct` (new) | | M03, M10, P08, S06, S07, S08: "multi-infarct dementia" (two spellings); WHO F01.1 | |
| `F01+strategic` (new) | | M04, P09, S09, S10: "strategic infarct dementia" | an answer without the word "vascular" used to fail |
| `F01+post_stroke` (new) | | M09, S11: "post-stroke dementia" | M05 is mixed and excluded |
| `F01+caa` (new) | | P03, P04: "cerebral amyloid angiopathy", "CAA"; I68.0 | summary CENTRAL 1; the generic vascular-dementia labels stay (CAA is the cause of a vascular dementia) |
| `F01+mixed` (new) | | M05, M07, M08, P01, P02: "mixed dementia", "alzheimer vascular dementia", "alzheimers vascular dementia", "alzheimer cerebrovascular disease", "alzheimers cerebrovascular disease"; WHO F00.2 | a vascular-only answer no longer scores. No G30 or F02.8x code: alone they credit an Alzheimer-only answer. "mixed Alzheimer and vascular dementia" was not used as a label because the token "and" would reject "mixed Alzheimer/vascular dementia" |
| `F06.7` | umbrella label; codes F01.50 (dementia), G31.84 (MCI of any cause, including Alzheimer MCI); any condition | `conditions: [vascular_dementia]`; labels mild VCI, mild vascular cognitive disorder, mild vascular neurocognitive disorder (DSM-5 term), mild NCD due to vascular disease, vascular MCI, "vascular cognitive impairment no dementia"; code F06.70 | M01 no longer credits a dementia overcall or an Alzheimer-MCI code |
| `RETIRED` | | + "vascular cognitive impairment" | so `--prune` strips it (no entry grants it any more; no other condition uses it) |

Scan of all 30 against accepted[0]: after the change no accepted label or code names another
entity, mechanism or severity. Kept on purpose: F01.A0/B0/C0 (severity sub-codes of the same entity;
none would be submitted for a mild-VCI answer); I67.850 for P05 (shared with MIG-AURA-P06, correct).

Label/code changes (ruling 3): `icd_codes[0]` unchanged in all 30. `accepted[0]`: the em dash
replaced by a colon or semicolon in the 25 labels that had one (summary CENTRAL 1 and auditor flag;
wording, entity and scoring unchanged). P05's variant string (`c.544C>T p.(Arg182Cys)`) is not
mirrored anywhere else (the old `c.475C>T p.(Arg159Cys)` occurs nowhere in the repository).

Limitations left to the scorer (CENTRAL below): an answer coded F01.50 still scores in a mixed case
(F01.50 is the primary code; code-alone matching); P06 credits "vascular dementia due to CADASIL"
(its own excluded alternative) through the generic tokens; negated answers ("not vascular
dementia") match.

## 2. Criteria pack (`dataset-generation/criteria_packs/VASC-DEM.md`)

Rewritten to the plan's rulings and the decisions here: per-case ICD rule (F01.50, F06.7/F06.70,
I67.850) and severity as the label; STRIVE-2 reporting with the Kind 2 limit; Boston v2.0, CADASIL
canonical variant, mixed disease; work-up order and per-case tiers as they now stand in the 30 cases
(gait C14, ECG after every ischaemic infarct, cervical vessels, TTE never waste after an ischaemic
infarct, monitoring, the two-alternative amyloid criterion, CSF harm when declined or on
anticoagulation, CSF waste not harm in CAA, FDG, NOTCH3, drug checks per ruling 6); MRI criterion
`{}`; no literature step; fallback rules; soft sequence constraints and the stop rule; mechanism
list per case; management facts (BP, lipids per the 2026 guideline, HbA1c, DOAC dosing, LV thrombus,
carotid timing, CAA, CADASIL, cognitive drugs). Allow-list: every key cited in the 30 cases, each
with a full reference, plus the new `[AAN_dementia_2001]`, `[ACC_AHA_dyslipidemia_2026]`,
`[ADA_older_adults_2026]`, `[ESH_2023]`, `[ESC_HTN_emergencies_2019]` and the summary's
`[AHA_ASA_2022_ICH]`, `[ESC_AF_2024]`, `[NICE_NG97]`, `[Rutten_2019]`, `[BSH_B12_2014]`. Superseded:
`[ADA_2025_older_adults]`, the July literature and blanket drug-check tiers. Script check: no key
used in a case is missing from the allow-list.

## 3. Generator block (`conditions.yaml`, `vascular_dementia` only)

- Difficulty presentations: MoCA scores and imaging results removed (the screen and MRI are scored
  steps); the straightforward and moderate presentations now carry the functional history that
  decides severity.
- Key findings rewritten in modality voice: labs without "(excludes ...)" or "vascular driver" text,
  sex-specific ranges, Friedewald and CKD-EPI consistency, RPR/HIV only with risk, no "at target";
  CSF, amyloid PET, FDG, ECG and MRI lines without diagnostic or mechanism verdicts ("mixed AD/
  vascular", "an embolic source", "CADASIL must be excluded"); Boston v2.0 sentence kept as Kind 2;
  CAA CSF pattern (Abeta40 and Abeta42 reduced) added.
- Common follow-ups: none generated a summary defect (no literature, consult or generic drug-check
  follow-up existed); the CSF follow-up now names when LP is harm or waste, the monitoring follow-up
  names pacemaker interrogation. Header comment for the round.

## 4. Review-app tool guidance

`test_guidance_claims.py` has no VASC-DEM claim and `build_condition_tool_guidance.py` no
`vascular_dementia` response: the condition replaced peripheral neuropathy after the July 2026 tool
review, so no reviewer comment exists to answer. Nothing to change; the claim test fails only on
NMDAR-ENC, MIG-AURA and SE rows (other agents).

## 5. Open questions (summary) and auditor flags

1. **Q1: HIV and RPR in the required panel at every age.** Decision: remove them from the required
   arguments in 29 cases; keep them in P06. Reason: the plan's premise ("US practice (AAN)
   supports them") is wrong: AAN 2001 states syphilis screening is not justified without clinical
   suspicion, NICE NG97 does not test routinely, and the ALZ-EARLY and FTD packs already require
   them only with risk. Requiring them failed the required labs criterion for an agent that follows
   either guideline. P06 (onset before 55, years of cocaine use) has the risk that makes them
   indicated. Labels, rationales (M01, M02) and `[AAN_dementia_2001]` updated; the stored outputs
   keep the results, so ordering them is still answered. Perfect agent 30/30.
2. **Q2: `max_additional_actions` 1.** Keep: as ALZ-EARLY and ISCH-STR; one defensible extra order
   (MMA at a borderline B12, a TTE where it is optional) is not penalised, two are. No change.
3. **Q3: no physician review.** Cannot be settled here: the condition must go into the next physician
   review round (Andrea schedules it). Items for that review are listed under "Still for Andrea".
4. **Flag: em dashes in `accepted[0]` (M01, M02, M05, P06, P07, P08; in fact 25 labels).** Applied
   (section 1).
5. **Flag: em dashes in untouched report strings (P03-P07).** Decision: leave. They are pre-round
   prose in correct sentences; the plan's rule replaces an em dash only in a sentence rewritten for a
   reason, and churn would send nothing better to the reviewers.
6. **Flag: P07 B12 322 pg/mL on metformin with reduced toe vibration.** Decision: no change. The
   value is inside the laboratory range and above the condition's MMA trigger (about 250 pg/mL with
   metformin or neuropathy, S04 at 244), diabetic neuropathy explains the vibration loss, and the
   cognitive syndrome is fully explained by the vascular disease. NICE NG239 would call 180-350
   indeterminate; an agent that orders MMA receives the library's normal result and stays within
   `max_additional_actions`.
7. **Own finding: LDL target outdated (summary class "LDL 55 polyvascular target" treated as
   wrong).** The 2026 ACC/AHA multisociety dyslipidemia guideline, which ALZ-EARLY already applies,
   sets LDL below 55 mg/dL for clinical ASCVD at very high risk. All eight atherosclerotic stroke
   cases meet it (M03 MI plus strokes; M10 and S08 stroke plus PAD; M05, P08, S06, S07, S11 stroke
   plus age 65 or more with hypertension, and diabetes in M05 and S11). Their lipid musts now give
   the below-55 goal with ezetimibe as the next step, cited `[ACC_AHA_dyslipidemia_2026]`; P08's
   labs expected evidence and S08's key evidence and teaching point follow. Lacunar and
   cardioembolic stroke cases keep their high-intensity statin musts (correct under both
   guidelines); covert SVD cases are primary prevention. The pack no longer says "do not use 55".
8. **Own finding: P06 malignant hypertension.** 186/108 mmHg with flame haemorrhages, exudates and
   renal involvement is malignant hypertension (a hypertensive emergency); the must now asks for
   same-day hospital assessment and a 20-25% fall in mean arterial pressure over several hours
   (`[ESC_HTN_emergencies_2019]`), then below 130/80 over weeks (`[ESH_2023]`). Resolves the
   summary's `[ESH_2023]` item (it was cited under `[ESO_2021_SVD]`, which does not cover this).
9. **Superseded citation.** `[ADA_2025_older_adults]` -> `[ADA_older_adults_2026]` in every VASC-DEM
   case that cited it (same target), as in ALZ-EARLY.
10. **Summary CENTRAL 9, metadata hygiene (case files, so done here).** `metadata.revision_reason`
    in M01-P08 replaced (stale August text); `metadata.fallback_tool_kinds` set to `case` where the
    fallback describes the patient (CT in 29 cases; AF Holters in M07, M08, M10, P04; P04 AF ECG;
    abnormal echoes in M07, M08, M09, P04, P06, S05). Not read by the harness.
11. **Summary CENTRAL 2 and 3 (allow-list, pack text).** Done (section 2).

## Files changed

- Cases: all 30 VASC-DEM (synonyms in 29; accepted[0] punctuation in 25; labs criterion in 30;
  lipid musts in M03, M05, M10, P08, S06, S07, S08, S11; P06 BP must; ADA key; metadata). Logs: all
  30, "Close-out (24 Oct 2026)".
- `agent-platform/config/policies/diagnosis_synonyms.yaml` (F01, F06.7 and new scoped F01 entries;
  RETIRED), `dataset-generation/criteria_packs/VASC-DEM.md`, `dataset-generation/config/conditions.yaml`
  (vascular_dementia block).

## Checks

`perfect_agent.py` 30/30; `case_io.py check` on all 30: schema and synonym guard OK, no test
failure names a VASC-DEM case; `test_case_guards.py -k VASC-DEM-` 60 passed;
`apply_diagnosis_synonyms.py --check --conditions vascular_dementia` clean (also with `--prune`);
no VASC-DEM guidance claim exists.

## Still for Andrea or the physicians

- Nothing blocks. The condition has had no physician review: it should be in the next round
  (needs Andrea to schedule reviewers). For that review: the S05 reversal to continue apixaban, the
  M10 laterality correction, the M08 edoxaban dose reduction, the RPR/HIV decision, the below-55 LDL
  goals, the P06 malignant-hypertension must, and the scoring changes (M01 no longer accepts
  dementia answers or G31.84; dementia cases no longer accept mild-VCI answers; mixed cases no longer
  accept a vascular-only answer; subtype labels scoped).
- The 2026 dyslipidemia guideline was read through summaries; a physician with the full text should
  confirm that a lacunar or cardioembolic ischaemic stroke counts as a major ASCVD event (it would
  move those cases to the below-55 goal too).

## CENTRAL (not made here; owners elsewhere)

1. **Scorer**: code-alone matching credits a vascular-only answer coded F01.50 in the five mixed
   cases (same root as the GLIO-HG and HEP-ENC items in CENTRAL_PENDING); per-case rejected tokens
   would let P06 reject "CADASIL" and mixed cases reject answers without "alzheimer"; negation
   ("not vascular dementia").
2. **Vocabulary** (`costs.yaml`, library, `tool_io.py` mirror; summary CENTRAL 4): an
   `order_cardiac_monitoring` `monitor_type` term `device_interrogation` (pacemaker or ICD
   interrogation of stored diagnostics; P08, now `{}` with a descriptive `monitor_type`); fold the
   `interpret_labs` analytes `B12` and `vitamin_B12` into one assay.
3. **MockServer** (summary CENTRAL 5): `monitor_type` as a discriminator for
   `order_cardiac_monitoring`, so a Holter order does not receive a stored 30-day monitor or device
   report (M04, P08, P09, S07, S09).
4. **Schema** (summary CENTRAL 6): a `weight_kg` vital (DOAC dosing weights sit in
   `physical_exam.general` in M08, M10, P04, P08, S05, S06, S07).
5. **perfect_agent.py** (summary CENTRAL 7): fail when a `required_arguments` key is not in the tool
   schema; fix the "<- ?" display for stored outputs with null fields.
6. **Library** (summary CENTRAL 8): the `analyze_csf` default returns a normal Abeta42 for any case.
7. **Review UI** (summary CENTRAL 10): show tool outputs in criterion order.
