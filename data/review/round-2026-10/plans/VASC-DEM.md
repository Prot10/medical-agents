# VASC-DEM: condition plan for the October 2026 review round

Lead plan for the 30 VASC-DEM cases (M01..M10, P01..P09, S01..S11). Workers follow it case by case so
that every case reaches the same decision for the same defect. Read `ROUND_POLICY.md` and
`PATTERNS.md` first; this plan does not repeat them.

No reviewer has annotated this condition: there is no notes file and no note id to cite. Every class
below was found by the lead survey of all 30 cases (scripts plus a full read of M01, M05, P03, P08,
S05 and S11). Ruling 2 still applies: each class is fixed in every case where it occurs, not only in
the cases listed as examples.

Baseline measured on 24 October 2026 before any edit (git clean for all 30 cases, no VASC-DEM logs):

- `perfect_agent.py`: 30/30 pass. This is a false pass: the perfect agent copies each criterion's own
  arguments, including the non-schema `sequences` key of class C1.
- `test_case_guards` leak test: fails in all 30 cases, because the literature initial output repeats
  the literature criterion's `expected_evidence` (class C2).

How to use this plan:

1. Apply every class of section 2 to your case, in the order listed, using the canonical text
   verbatim where one is given (fill the `<...>` slots from the case).
2. Apply the per-case decisions of section 4.
3. Rebuild `action_criteria`, `followup_outputs`, `sequence_constraints` and `stop_rule` as section 3
   says.
4. Run both checks (section 3.6) and write the log.

Conventions for all new text: English, the case's spelling (British in this condition: ischaemic,
haemorrhage, anaemia, oedema, characterised), no em dashes or en dashes (replace an existing one only
in a sentence you rewrite anyway), units as the case already uses them (mg/dL, mmol/L for HbA1c only
if the case does). Never change `case_id`, `condition`, `diagnosis.accepted[0]` or `icd_codes[0]`;
never hand-edit diagnosis synonyms (central). Where a class asks you to add a result, choose a
plausible value that agrees with age, sex, renal function, medicines and the other reports of the
case, and that differs from the other cases.

---

## 1. Governing guidelines and canonical facts

### 1.1 Which guideline governs what

| question | governing source | citation key |
| --- | --- | --- |
| Diagnosis and severity of vascular cognitive disorder (mild vs major) | Sachdev P et al., Alzheimer Dis Assoc Disord 2014;28:206-218 (VASCOG) | `[VASCOG_2014]` |
| Vascular dementia research criteria, subtypes | Roman GC et al., Neurology 1993;43:250-260 | `[NINDS_AIREN_1993]` |
| Work-up of vascular cognitive impairment | Gorelick PB et al., Stroke 2011;42:2672-2713 | `[AHA_ASA_2011_VCI]` |
| MRI terminology for small-vessel disease | Duering M et al., Lancet Neurol 2023;22:602-618 (STRIVE-2) | `[STRIVE_2]` |
| Cerebral amyloid angiopathy diagnosis | Charidimou A et al., Lancet Neurol 2022;21:714-725 (Boston v2.0) | `[Boston_v2]` |
| MCI: biomarkers not routine, management | Petersen RC et al., Neurology 2018;90:126-135 | `[AAN_MCI_2018]` |
| Secondary prevention after ischaemic stroke or TIA (BP, LDL, AF, LV thrombus, carotid, monitoring) | Kleindorfer DO et al., Stroke 2021;52:e364-e467 | `[AHA_ASA_2021_secondary]` |
| Covert small-vessel disease: no antiplatelet, BP control | Wardlaw JM et al., Eur Stroke J 2021;6:CXI-CLXII (ESO SVD) | `[ESO_2021_SVD]` |
| Major/mild neurocognitive disorder definitions | APA DSM-5-TR 2022 | `[DSM5]` |
| ICH secondary prevention, CAA, LAAO after ICH | Greenberg SM et al., Stroke 2022;53:e282-e361 | `[AHA_ASA_2022_ICH]` (new key, CENTRAL) |
| AF anticoagulation in older adults, falls, CHA2DS2-VA, post-ablation | Van Gelder IC et al., Eur Heart J 2024;45:3314-3414 | `[ESC_AF_2024]` (new key, CENTRAL) |
| Glycaemic targets in older adults with cognitive impairment | ADA Standards of Care 2025, section 13 Older Adults, Diabetes Care 2025;48(Suppl 1) | `[ADA_2025_older_adults]` (new key, CENTRAL) |
| Dementia assessment in primary/secondary care (blood panel scope) | NICE NG97, 2018 | `[NICE_NG97]` (new key, CENTRAL) |
| CADASIL variant position and severity | Rutten JW et al., Genet Med 2019;21:676-682 | `[Rutten_2019]` (new key, CENTRAL) |

Use only bracketed keys in `guideline_citations`. A new key is used in the must or rationale it
supports; the central pass allow-lists it in the criteria pack.

### 1.2 Canonical facts (use these, do not restate them differently)

Severity

- Mild vascular cognitive disorder (VCI without dementia, F06.7): decline in one or more domains with
  preserved independence in instrumental activities, possibly needing compensatory strategies.
  Major vascular cognitive disorder (vascular dementia, F01.x): decline sufficient to interfere with
  independence (VASCOG 2014, DSM-5-TR). The severity is the assessment's conclusion: no tool report
  states it.

Blood pressure

- After ischaemic stroke or TIA: target below 130/80 mmHg for most patients, reached gradually, with
  orthostatic blood pressure checked at each change in an older or frail patient (AHA 2021).
- After intracerebral haemorrhage (hypertensive or CAA): target below 130/80 mmHg (AHA 2022 ICH).
- Covert small-vessel disease without clinical stroke: treat hypertension to the same target; no
  antiplatelet for covert SVD alone (ESO 2021 SVD).
- Border-zone (haemodynamic) infarcts or a severe stenosis not yet revascularised (M06, M10, S08):
  individualise the target, lower gradually, avoid systolic below about 120 mmHg and orthostatic
  hypotension; for a severe carotid stenosis lower more cautiously until the stenosis is treated.

Lipids

- Ischaemic stroke or TIA with atherosclerotic disease: LDL below 70 mg/dL (AHA 2021, from TST).
  Do not use 55 mg/dL as the target in this condition (M10 labs cite it: remove).
- Small-vessel or other non-atherosclerotic ischaemic stroke: high-intensity statin (AHA 2021);
  state "statin to secondary-prevention intensity", not a 55 target.
- After ICH: no statin restriction is required by the guideline; do not start a new statin solely
  for ICH, continue an indicated one (AHA 2022 ICH). Do not write a prohibition on statins in CAA.

Glycaemia

- Older adult with cognitive impairment: individualised HbA1c target, about below 8.0%; avoid
  hypoglycaemia; prefer agents with low hypoglycaemia risk; deprescribe sulfonylureas or insulin
  where hypoglycaemia occurs (ADA 2025 Older Adults). Healthy older adult with intact function:
  below 7.0-7.5%.

Atrial fibrillation and cardioembolism

- AF with prior stroke or TIA: oral anticoagulation, a DOAC in preference to warfarin (except
  mechanical valve or moderate-severe mitral stenosis); stop aspirin when started unless a separate
  indication exists (recent stent, ACS) (AHA 2021).
- Apixaban dose: 5 mg twice daily; 2.5 mg twice daily only when two of age 80 or more, weight 60 kg or
  less, creatinine 1.5 mg/dL or more apply. Edoxaban 60 mg daily; 30 mg when CrCl 15-50 mL/min,
  weight 60 kg or less, or a strong P-gp inhibitor. Use Cockcroft-Gault CrCl, not eGFR, for DOAC
  dosing.
- Falls, older age, cognitive impairment and a few deep microbleeds are not by themselves reasons to
  withhold anticoagulation (ESC AF 2024). Anticoagulation after AF ablation or flutter ablation is
  decided on stroke risk (CHA2DS2-VA), not on rhythm (ESC AF 2024).
- LV thrombus after MI with stroke: warfarin, INR 2-3, for at least 3 months (AHA 2021, 2a); a DOAC
  is a reasonable alternative of uncertain benefit (2b). Refer to cardiology/heart failure for EF
  below 40%.
- Cryptogenic or embolic-pattern stroke: prolonged rhythm monitoring (about 30 days) is reasonable
  (AHA 2021, 2a); TTE is reasonable for an embolic pattern (2a).

Carotid

- Symptomatic stenosis 70-99% within 6 months: CEA (or CAS), ideally within 2 weeks of the event.
- Symptomatic 50-69%: CEA depending on patient factors (age, sex, comorbidity), surgical risk below 6%;
  refer to the vascular team without delay. Never write that 50-69% is "below the threshold".
- Benefit of revascularisation falls with time and is small beyond 6 months: after 6 months a
  stenosis is managed as asymptomatic (best medical therapy; revascularisation only selectively).

CAA (Boston v2.0)

- Probable CAA: age 50 or more, two or more strictly lobar haemorrhagic lesions (ICH, microbleeds,
  cortical superficial siderosis foci, cSAH), or one lobar lesion plus one white matter feature
  (severe centrum semiovale PVS, multispot WMH), and no deep haemorrhagic lesion or other cause.
- Management: stop an antiplatelet that has no indication; avoid anticoagulation where possible; for
  AF consider left atrial appendage occlusion (AHA 2022 ICH, 2b); BP below 130/80; warn about
  transient focal neurological episodes (TFNE) and not to treat them as TIA with antiplatelets.
- CSF in CAA: Abeta40 and Abeta42 are both reduced; an LP is not harmful in chronic CAA without acute
  haemorrhage. It is not needed for the diagnosis, so it is waste, not harm.

Biomarkers

- MCI: amyloid biomarkers are not routinely recommended (AAN 2018); they are optional.
- Dementia with a mixed question (amnestic or posterior cortical syndrome beyond the vascular burden):
  one amyloid biomarker, CSF (Abeta42/40 with p-tau181) or amyloid PET, is the step that changes the
  diagnosis from vascular to mixed.

CADASIL

- NOTCH3 cysteine-altering variants in EGFr domains 1-6 carry the classic, more severe phenotype
  (Rutten 2019). Canonical P05 variant: `NOTCH3 c.544C>T p.(Arg182Cys)`, exon 4, EGFr 4,
  heterozygous, pathogenic. Genetic counselling and cascade testing of at-risk relatives are offered.
- Avoid triptans and ergots for migraine with aura in CADASIL (vasoconstriction).

Labs (reference ranges; use these where the case gives a different range)

- Haemoglobin: men 13.5-17.5 g/dL, women 12.0-16.0 g/dL. Haematocrit: men 41-53%, women 36-46%; keep
  Hct about 3 x Hb (Hb 11.8 → Hct about 35-36%).
- eGFR reference ">=60 mL/min/1.73m2"; a value of 60 is normal, below 60 is flagged.
- HDL: men ">40 mg/dL", women ">50 mg/dL".
- INR belongs in a Coagulation panel, not in the CMP.

---

## 2. Error classes in this condition

Each class: what was found, the cases, the fix. "All" means all 30 cases.

### C1. MRI criterion that no real call can match (blocker)

Found: 29 cases (all except P08, which has no MRI criterion). The MRI criterion has
`required_arguments` `{"contrast": false, "protocol": "dementia" | "stroke", "sequences": "FLAIR, T1,
T2, DWI, SWI"}`. `analyze_brain_mri` has no `sequences` parameter and no `protocol` default, and
`pattern_matches` requires every key, so a model's real call never matches: a required action scored
as missing for every model.

Fix: set the MRI criterion's alternatives to exactly one: `analyze_brain_mri` with
`required_arguments` `{}`. Do not add `protocol` or `contrast`. Keep the criterion id. The MRI initial
output may keep its own `protocol` field and sequence list as report content. Where the report says
"non-contrast" or names SWI, that is fine.

### C2. Literature search: criterion leaks into its own output (rulings 5 and leakage)

Found: all. A `recommended` (or optional) literature criterion whose `expected_evidence` is copied in
`initial_tool_outputs.literature_search`: "VASCOG 2014 criteria and the 2021 AHA/ASA secondary
prevention targets confirmed". This is the leak that fails `test_case_guards` in all 30.

Fix (ruling 5, as in ALZ-EARLY): delete the literature criterion. Set
`initial_tool_outputs.literature_search` to null and delete `fallback_tool_outputs.literature_search`
if present, so the library answers generically. Remove any sequence constraint, follow-up or must
that refers to it. Nothing depends on a literature search.

### C3. Drug-interaction checks (ruling 6)

Found: every case has an optional `check_drug_interactions {}` criterion with the same generic
`expected_evidence`, and `fallback_tool_outputs.drug_interactions` with the same generic "No
prohibitive interaction" text in all 30, which is false where interactions exist.

Fix, in every case: delete `fallback_tool_outputs.drug_interactions`. Then, per case (section 4
names the group):

- Group R (required stays out; tier `recommended`): the case has a concrete interaction that changes
  management. Criterion `action-<n>-check-drug-interactions`, one alternative per drug name
  (string arguments match by folded equality), e.g. `{"drug": "apixaban"}`, `{"drug":
  "rivaroxaban"}`, `{"drug": "edoxaban"}`, `{"drug": "dabigatran"}`, `{"drug": "warfarin"}`. The
  initial `drug_interactions` output is case-specific and keyed by the drug(s): name the pair, the
  mechanism and the management consequence in neutral pharmacology voice (no diagnosis).
  - M03: warfarin with aspirin (bleeding; stop aspirin when warfarin is started unless a separate
    indication), warfarin with alendronate (none of note). Alternatives: warfarin first, then the
    four DOACs.
  - M10, S06, S07, P08: DOAC with aspirin (major bleeding about doubled; stop aspirin), plus the
    case's other relevant medicine (M10: none beyond aspirin; check amlodipine is not an issue).
    Alternatives: apixaban, rivaroxaban, edoxaban, dabigatran, warfarin.
  - M07, M08: cholinesterase inhibitor with a rate-control drug (M07: bisoprolol or the case's
    beta-blocker; M08: diltiazem): additive bradycardia and syncope risk; check heart rate and ECG
    before and after starting. M08 also: edoxaban with diltiazem (no dose change; diltiazem is not a
    strong P-gp inhibitor) and edoxaban dose against CrCl (age 81, creatinine 1.28: compute
    Cockcroft-Gault from the case weight; if no weight, add one to vitals). Alternatives: donepezil,
    rivastigmine, galantamine.
- Group O (tier `optional`, `{}`, with case-specific content): M05 (gliclazide: hypoglycaemia risk
  with cognitive impairment), P05 (sumatriptan contraindicated in CADASIL; sertraline with triptan,
  serotonin toxicity), P09 (zolpidem: falls and confusion), S05 (apixaban with tiotropium: none;
  apixaban dose check), P04 (apixaban: bleeding risk in CAA; any antiplatelet).
- Group D (delete the criterion and set `initial_tool_outputs.drug_interactions` to null): M01, M02,
  M04, M06, M09, P01, P02, P03, P06, P07, S01, S02, S03, S04, S08, S09, S10, S11.

### C4. The neurological exam gives the cognitive screen result

Found: all. `neurological_exam.mental_status` states the MoCA total and item scores, which is the
result of the required screening action.

Fix: replace `mental_status` with a bedside observation in this shape (adapt to the case's syndrome:
apathy, slowing, aphasia, neglect, abulia, pseudobulbar affect):

> "Alert and cooperative; oriented to person and place, year correct, date incorrect. Slow to
> initiate answers; conversation coherent. Formal cognitive screening reported separately."

Keep legitimate referral history: P07's GP MoCA 26/30 in the HPI is the red herring and stays; P02's
earlier headache MRI showing white matter change stays without a Fazekas grade. Any other HPI
mention of a prior score stays only if it is earlier history and differs from the screen result.

### C5. Tool reports that state the diagnosis, the mechanism verdict or the management (Kind 1 leakage)

Found: nearly every report in all 30 cases (cognitive screen, neuropsych, MRI, CT, carotid duplex,
MRA, ECG, echo, monitoring, CSF, PET, gait, labs). Examples, all to strip:

- "sufficient to account for the syndrome", "matches a patient who is functionally independent",
  "the threshold for dementia is not met", "excludes Alzheimer disease", "converts management",
  "renal function adequate for anticoagulation", "supports the reduced apixaban dose", "management is
  determined by MRI", "consistent with the cardioembolic source documented on the ECG", "excluding
  reversible causes";
- differential essays (gait reports arguing against NPH or parkinsonism; MRI paragraphs arguing
  against CAA or AD);
- management text ("Serial reassessment is the appropriate management", MRA "secondary prevention is
  medical", duplex "below the 70% threshold at which revascularisation is offered").

Fix: rewrite in modality-only voice (TOOL_REPORT_STYLE_GUIDE):

- Cognitive screen: total, domain sub-scores, the education correction if applied. No severity label,
  no "vascular pattern".
- Neuropsych: domain scores and a confidence-qualified profile, e.g. "Profile: predominant slowing of
  processing speed and executive function with relatively preserved recognition memory." It may not
  name the disease or the dementia threshold.
- MRI: STRIVE-2 descriptors with grades (Fazekas, lacune count and sites, microbleed count and
  distribution, cSS, PVS, atrophy, MTA score, infarcts with territory). A Kind 2 statement is allowed
  where it is a radiological criterion, e.g. "Findings fulfil Boston criteria v2.0 for probable
  cerebral amyloid angiopathy." Not allowed: the dementia diagnosis, sufficiency for the syndrome,
  the mechanism of cognitive decline, management.
- Carotid duplex/MRA: velocities, NASCET-equivalent percentage, plaque description. No threshold
  statements.
- ECG, monitoring, echo: findings and measurements (rhythm, AF burden, EF, thrombus, LA size). No
  "source of the strokes".
- CSF: values with reference ranges and the laboratory's standard flag, e.g. "Abeta42/40 ratio low;
  p-tau181 raised." No "consistent with AD".
- Amyloid PET: binary read, "Positive" or "Negative", with the visual read description. P03's "consistent
  with CAA" goes.
- Gait: time, cadence, step length, TUG, turns, Romberg and the observation; no diagnostic argument.
- Labs: C6.

### C6. Lab template carry-over

Found: all. Female ranges for Hb (12.0-16.0) and Hct (36-46) in the 18 men; identical normal values
across cases (WBC 6.8 in 30, Hct 41.6 in 29, Plt 238 in 28, MCV 88 in 29, Na 139, K 4.2, Albumin 4.1,
Folate 11.8 in 30, ALT 22 in 28); Hct inconsistent with anaemia (S03 Hb 11.8; M06 "mild anaemia");
eGFR 60 against a ">60" range flagged normal (M07, P08); HDL ">40" for women; INR inside the CMP with
`clinical_significance` text (P03, P04); interpretive `clinical_significance` text (M02, P05, P06, S04,
M02 thiamine); interpretive `interpretation` fields (M03, M08, M10, P04, P08, S05, S11 and others:
"above target", "supports the reduced apixaban dose", "excluding reversible causes").

Fix:

1. Ranges per 1.2: male Hb 13.5-17.5 g/dL and Hct 41-53%; female HDL ">50"; eGFR ">=60".
2. Hct about 3 x Hb in every case; S03 and M06 Hct consistent with their Hb (about 35-37%).
3. Vary the normal values per case within the normal range (WBC, Plt, MCV, Na, K, albumin, folate,
   ALT): do not reuse 6.8 / 238 / 88 / 139 / 4.2 / 4.1 / 11.8 / 22 unchanged.
4. INR, if reported, moves to a `Coagulation` panel (PT, INR, aPTT) with its own range.
5. `clinical_significance` null everywhere; `interpretation` becomes a pattern-level recital of
   flagged values only, e.g. "Flagged: LDL 96 mg/dL (high), HbA1c 7.9% (high), eGFR 58 (low). Other
   results within reference ranges." No targets, no "excluding", no dosing advice.
6. Flags (`is_abnormal`) follow the range: values outside are flagged, values inside are not.

### C7. Fallback outputs that reveal the order was off-pathway

Found: all. `fallback_tool_outputs.advanced_imaging` ("study performed and reported as
non-contributory", empty modality), `fallback_tool_outputs.labs` ("additional panels ... do not
contribute"), CT fallback "better characterised on the MRI already obtained".

Fix:

- Delete the `advanced_imaging` and `labs` fallbacks; the library answers with normal reports.
- CT fallback (all except P08, where CT is the initial study): rewrite as a normal-for-case
  non-contrast CT that describes what CT would show in this patient (periventricular hypodensity,
  old infarcts, atrophy) without any time or comparison reference ("already obtained", "as on MRI").
- EEG, echo and Holter fallbacks: keep only if consistent with the case (no finding that contradicts
  another report, no diagnostic sentence); otherwise delete. Where an echo or monitoring criterion is
  added by C10, the case needs a matching initial output (not a fallback).
- C9 mixed cases need case-authored outputs for both biomarker routes.

### C8. Differential not updated to the assessment-time view (ruling 7)

Found: alternatives the work-up excludes are rated moderate in M01, M02, M03, M04, M05 (both "alone"
entries), M06, M07, M08, M09 (both), M10 (both), P01 (both), P02 (both), P03 (both), P04 (both), P05
(both), P06 (CADASIL, cocaine), P07, P09 (both), S02, S03, S10, S11.

Fix: every alternative that the case's reports exclude is `low`. Specifics:

- Mixed cases: "Vascular dementia alone" and "Alzheimer disease alone" both low.
- P06: delete the entry "Hypertensive SVD" (very_high), which is the diagnosis itself.
- P02: rephrase "posterior cortical atrophy" to "Posterior cortical atrophy (Alzheimer disease)
  without significant vascular contribution", low.
- P08: Alzheimer disease to low; CAA stays moderate (the only entry the CT cannot exclude; keep its
  rationale "cannot be excluded on CT").
- M01: "Vascular dementia (major vascular cognitive disorder)" to low (independence preserved).
- Keep an alternative moderate only when the case genuinely leaves it open at assessment time, and
  say so in its key features.

### C9. Biomarker route in mixed and CAA cases

- M05, M07, P01 (mixed, LP acceptable): one criterion `action-<n>-amyloid-biomarker`, tier as in
  section 4, with two alternatives: `analyze_csf {"special_tests": ["Abeta42", "Abeta42_40_ratio",
  "phospho_tau"]}` and `order_advanced_imaging {"modality": "amyloid_PET"}`. Both answered by
  consistent case data: keep the CSF output; add a follow-up `order_advanced_imaging` amyloid_PET
  output read "Positive" (cortical tracer uptake in at least two regions; tracer as the case's
  centre would use, e.g. florbetaben). Keep the criterion id of the existing CSF criterion.
- M08, P02 (amyloid PET only: LP declined; M08 also on edoxaban): keep the amyloid PET criterion.
  Add avoided `analyze_csf {}`, severity `harm`, rationale "<patient> has declined lumbar puncture
  <M08: and takes edoxaban, which would need interrupting>; amyloid PET answers the same question."
  Add a case-authored CSF follow-up consistent with the PET (positive pattern) so the library does
  not return a contradicting normal CSF if a model orders it anyway.
- M01 (mild VCI): CSF criterion to `optional` (AAN 2018: biomarkers not routine in MCI). Rewrite the
  must "Resolve the Alzheimer question with a biomarker" to: "Do not attribute the decline to
  Alzheimer disease on current evidence; repeat cognitive assessment in 12 months, and consider an
  amyloid biomarker if the profile becomes amnestic or progression outpaces the vascular burden
  [AAN_MCI_2018]."
- P03, P04 (CAA): avoided `analyze_csf` from `harm` to `waste`. Rationale: "Boston v2.0 diagnosis
  rests on MRI; CSF would not change management." Rewrite the prohibition "CSF cannot separate
  vascular from parenchymal amyloid" (partly wrong: Abeta40 is reduced in CAA) to: "Do not perform
  lumbar puncture to establish the diagnosis; it rests on MRI (Boston v2.0) [Boston_v2]." P03's
  optional amyloid PET stays optional; its report reads "Positive" without "consistent with CAA".

### C10. Embolic and ischaemic work-up in strategic and focal infarcts

AHA 2021: ECG for every ischaemic stroke; carotid imaging for anterior circulation; TTE reasonable
(2a); prolonged monitoring reasonable when cryptogenic (2a).

- M04 (cortical angular gyrus infarct): new ECG criterion `recommended` with a normal sinus rhythm
  initial output; MRA criterion becomes `action-<n>-cervical-vessel-imaging` with alternatives
  `order_advanced_imaging {"modality": "MR_angiography"}` and `{"modality": "carotid_duplex"}`, both
  answered (add a duplex output agreeing with the MRA); TTE `optional` with a normal output;
  monitoring `optional` `{}` with a 14-30 day monitor output showing no AF. Remove the echo and
  monitoring waste entries.
- P09, S09 (thalamic strategic infarcts, posterior circulation): new ECG `recommended`; TTE
  `optional`; monitoring `optional`; matching normal outputs; remove the echo and monitoring waste
  entries.
- P09 MRA: the artery of Percheron is usually not visible on MRA. Rewrite the MRA report: "No
  stenosis of the basilar artery, basilar tip or P1 segments. Thalamoperforating arteries are below
  the resolution of MRA." Rewrite the must that relies on MRA visualising the Percheron artery to:
  "Treat as a small perforator infarct: antiplatelet, statin and BP control to target
  [AHA_ASA_2021_secondary]."
- S10, M05 (lacunes worked up at admission): keep as they are.
- M09 (deep ICH): delete the carotid criterion and its initial output; add avoided
  `order_advanced_imaging {"modality": "carotid_duplex"}`, `waste`, rationale "Hypertensive thalamic
  haemorrhage: carotid imaging does not inform ICH prevention." ECG stays recommended.
- S08: delete the duplicated waste entries (keep one each); delete the echo waste altogether (TTE
  is 2a after ischaemic stroke); keep one monitoring waste with the rationale "A severe ipsilateral
  stenosis explains the infarct pattern; prolonged monitoring does not change management."

### C11. P08 pacemaker interrogation coded as an implantable loop recorder

Found: P08's monitoring criterion `{"monitor_type": "implantable_loop_recorder"}`; the patient has a
pacemaker; the report is a device interrogation.

Fix: criterion `order_cardiac_monitoring {}`; the report's `monitor_type` field becomes descriptive
text "pacemaker interrogation, stored device diagnostics"; rephrase the prohibition to "Do not
implant a loop recorder or fit an external monitor before interrogating the pacemaker." CENTRAL:
add a `device_interrogation` term. Also C16 (P08 sequence) and section 4.

### C12. S11: wrong carotid threshold

Found: S11 duplex "below the 70% threshold at which revascularisation is offered". Wrong for a
symptomatic 50-69% stenosis within 6 months (man, NIHSS 3, 10 weeks after the stroke).

Fix: strip the sentence from the report (C5). Add the must: "Refer the symptomatic <percent> right
ICA stenosis to the vascular team without delay for a decision on carotid endarterectomy
[AHA_ASA_2021_secondary]." Add a prohibition: "Do not dismiss a symptomatic 50-69% stenosis as below
the threshold for revascularisation."

### C13. Criterion metadata

Found: all 228 criteria. Every `rationale` equals the `label`; every criterion cites the unbracketed
key next to the bracketed one ("VASCOG_2014" and "[VASCOG_2014]").

Fix: one-sentence case-specific rationale ("Subcortical syndrome with falls: timed gait quantifies
the gait apraxia that VASCOG lists as a supporting feature."); keep only bracketed keys, and only the
ones that support that action (1.1).

### C14. Gait criterion tiers

- Required (subcortical syndrome with gait involvement): S01, S02, S03, S04, S05, M02, P07.
- M01: `recommended` (no gait complaint, normal test).
- Add a `recommended` `perform_clinical_assessment {"assessment_type": "gait_and_balance_timed"}`
  with an authored output in P01, P05, P06 (gait involvement in the case narrative or exam).
- No gait criterion in the other cases.

### C15. Labs in young small-vessel disease

P05, P06: new `recommended` criterion `action-<n>-interpret-labs-young-svd`, `{"panels":
["homocysteine", "ESR", "CRP", "antiphospholipid"]}`, answered by the initial labs (add the panels to
the initial labs output; normal values, P06 homocysteine may be mildly raised if the narrative
supports it). Check the panel names fold in `tools/vocabulary.py`; if one does not, use the
vocabulary spelling.

### C16. Ordering, sequence and stop rule

Order (criteria and follow-ups): cognitive screen; gait; neuropsych; labs (with the young-SVD panel);
MRI (or CT in P08); mechanism studies (ECG, carotid duplex or MRA, TTE, monitoring); biomarkers (CSF /
amyloid PET / FDG); NOTCH3; drug check. Keep existing ids; new criteria take the next free number.

Soft constraints (no hard ones):

- screen before MRI (existing; keep);
- MRI before CSF where a CSF alternative exists (M01, M05, M07, P01);
- ECG before monitoring (S07, P08 and every case with a monitoring criterion: M04, P09, S09);
- MRI before NOTCH3 (P05, P06);
- carotid duplex before MRA (S08);
- P08: screen before CT, ECG before monitoring.

Delete constraints that refer to deleted criteria. Stop rule: the required criteria,
`max_additional_actions: 1` (currently 0 everywhere; 1 as in ALZ-EARLY and ISCH-STR).

### C17. M01 severity leak

M01's clinical summary, MRI, CSF and neuropsych reports name "mild VCI, not dementia". Strip all such
statements (C5). The functional history in the HPI (independent IADLs with strategies) stays: it is
what the agent must weigh. Differential per C8.

### C18. Avoided-action rationales

CT waste rationale (every case except P08): "MRI is available and not contraindicated; CT cannot show
microbleeds, siderosis or small lacunes." Every avoided rationale names this patient's reason (no
"already obtained", no generic text). The DaTscan, MIBG, EEG and paraneoplastic waste entries stay,
each with a one-line case reason (e.g. "No parkinsonism, fluctuations or hallucinations").

### C19. Musts and prohibitions: specific, with canonical facts

Rewrite the generic musts with the case's numbers and the facts of 1.2:

- BP: "Lower blood pressure gradually to below 130/80 mmHg, checking orthostatic BP at each change
  [AHA_ASA_2021_secondary]." After ICH: same target with `[AHA_ASA_2022_ICH]`. M06, M10, S08:
  individualised target per 1.2.
- LDL: "Intensify lipid lowering to LDL below 70 mg/dL (current <value>) [AHA_ASA_2021_secondary]"
  in atherosclerotic cases; high-intensity statin otherwise.
- HbA1c: "Individualise the HbA1c target to about below 8.0% and avoid hypoglycaemia
  [ADA_2025_older_adults]" (M03, M05, M10, S11 and others with diabetes).
- AF: "Start a DOAC (e.g. apixaban 5 mg twice daily, adjusted only by its criteria) and stop aspirin
  [AHA_ASA_2021_secondary]." P04: check the apixaban dose against its criteria (age 81 counts once;
  creatinine 1.02 does not; reduced dose only if weight is 60 kg or less: add the weight to vitals).
- M03: "Anticoagulate with warfarin, INR 2-3, for at least 3 months for the LV apical thrombus, and
  refer to heart failure for EF 38% [AHA_ASA_2021_secondary]."
- Covert SVD without stroke (S01-S04, M02, P07 where no clinical stroke): prohibition "Do not start
  an antiplatelet for covert small-vessel disease alone [ESO_2021_SVD]."; drop any must to start
  aspirin there.
- S05: must "Continue anticoagulation on CHA2DS2-VA; sinus rhythm after flutter ablation, falls and
  few deep microbleeds are not reasons to stop [ESC_AF_2024]."
- CAA (P03, P04): stop aspirin without indication; avoid anticoagulation; P04 refer for LAAO
  consideration [AHA_ASA_2022_ICH]; warn about TFNE.
- Cognitive management musts (cholinesterase inhibitor in VaD is off-label with modest benefit;
  memantine likewise): keep only where the case already has one, reworded as "may be considered";
  in mixed cases a cholinesterase inhibitor is reasonable for the AD component.

### C20. CADASIL variant and P06 metadata

- P05: replace the variant with `NOTCH3 c.544C>T p.(Arg182Cys)`, exon 4, EGFr 4, heterozygous,
  pathogenic (cite `[Rutten_2019]` in the genetics must). The genetic report may say "Genetic
  counselling is recommended" (laboratory standard).
- P06: `metadata.vascular_mechanism` "svd" (not "cadasil"). NOTCH3 stays required (age 54, family
  history); its report is a VUS (non-cysteine) interpretation; the must says a VUS does not make the
  diagnosis and that the hypertension history explains the disease.

### C21. Labs criterion panel

Keep `["CBC", "CMP", "TSH", "B12", "folate", "RPR", "HIV", "HbA1c", "lipid_panel"]` in every case
(pack, and consistency with the other conditions). NICE NG97 does not advise routine syphilis or HIV
testing; they stay because the pack lists them and US practice (AAN) supports them in a dementia
work-up. Do not add or drop panels except C15.

---

## 3. Target pathway and tiers

### 3.1 `action_criteria` order and tiers

| # | criterion | tool and `required_arguments` | tier |
| --- | --- | --- | --- |
| 1 | cognitive screen | `perform_clinical_assessment {"assessment_type": "cognitive_screen"}` | required |
| 2 | gait (C14 cases) | `perform_clinical_assessment {"assessment_type": "gait_and_balance_timed"}` | required / recommended per C14 |
| 3 | neuropsych | `order_specialized_test {"test_type": "neuropsych_battery"}` | as section 4 (required where the case already requires it) |
| 4 | labs | `interpret_labs {"panels": [9 panels]}` | required |
| 5 | young-SVD labs (P05, P06) | `interpret_labs {"panels": ["homocysteine", "ESR", "CRP", "antiphospholipid"]}` | recommended |
| 6 | MRI | `analyze_brain_mri {}` | required (P08: CT `order_ct_scan {}` required) |
| 7 | ECG | `analyze_ecg {}` | per section 4 |
| 8 | carotid duplex / MRA | `order_advanced_imaging {"modality": ...}` | per section 4 |
| 9 | TTE | `order_echocardiogram {}` | per section 4 |
| 10 | monitoring | `order_cardiac_monitoring {}` or the case's `monitor_type` (S07 event_monitor_30d) | per section 4 |
| 11 | amyloid biomarker | C9 | per section 4 |
| 12 | FDG PET | `order_advanced_imaging {"modality": "FDG_PET"}` | optional (M07, M08), recommended (P02) |
| 13 | NOTCH3 | `order_specialized_test {"test_type": "genetic_panel:CADASIL"}` | required (P05, P06) |
| 14 | drug check | C3 | per C3 |

No literature criterion (C2).

### 3.2 Follow-ups and initial outputs

`followup_outputs` in the same order as 3.1. Every criterion's alternative must be served by a case
output (initial or follow-up), never by the library. Initial outputs that no criterion asks for and
that are not referenced by an avoided action may stay only if consistent (C7).

### 3.3 `avoided_actions`

Keep EEG, DaTscan, MIBG, paraneoplastic/autoimmune labs, CT waste (C18). Remove echo and monitoring
waste where C10 adds them; S08 per C10; M09 adds carotid waste; M08, P02 add CSF harm; P03, P04 CSF
waste. P08 MRI harm (pacemaker, MR-unsafe) stays.

### 3.4 Sequence constraints (all soft)

As C16.

### 3.5 Stop rule

`required_criteria` = the required criteria ids; `max_additional_actions: 1`.

### 3.6 Check after editing

- `uv run python data/review/round-2026-10/bin/perfect_agent.py <id> -v` (see the script's `--help`
  for its exact arguments) passes, and in the `-v` output every required and recommended action is
  served by a case output, not by the library or a fallback. It serves only the first alternative of
  each criterion: for the C9 and C10 two-alternative criteria, check by reading the case that the
  second alternative also has a case output.
- `uv run pytest agent-platform/tests/test_case_guards.py -q -k <id>` passes (leak test included).
- `grep -c "sequences" <case>` returns 0 inside `required_arguments`.

---

## 4. Per-case index

All classes apply to every case (C1, C2, C4, C5, C6, C7, C13, C16, C18 everywhere). Below: the
per-case decisions. No case has reviewer notes.

### VASC-DEM-M01 (woman, 69, mild VCI, moderate SVD)
- C3 group D. C9: CSF to optional, rewrite the biomarker must. C14: gait to recommended.
- C17: strip the "mild VCI, not dementia" statements from summary, MRI, CSF, neuropsych.
- C8: "Vascular dementia (major)" to low. Echo and monitoring waste stay (no stroke).
- Soft MRI before CSF. Prohibition: no antiplatelet for covert SVD (C19).

### VASC-DEM-M02 (man, 66, subcortical VaD from untreated hypertension)
- C3 group D. Gait required (C14). Strip the three-component gait report's diagnostic argument (C5).
- C6: thiamine `clinical_significance` to null. C8 per survey. C19: BP and no-antiplatelet prohibition
  if no clinical stroke.

### VASC-DEM-M03 (woman, 77, multi-infarct, LV apical aneurysm with thrombus)
- C3 group R: warfarin first (warfarin + aspirin), then DOACs; content per C3.
- C19: warfarin INR 2-3 for at least 3 months, stop aspirin, heart failure referral (EF 38%); LDL
  below 70 (106); HbA1c individualised (7.4%).
- The contrast allergy prohibition stays. Echo and carotid required stay. C8.

### VASC-DEM-M04 (woman, 64, strategic left angular gyrus infarct)
- C3 group D. C10: ECG recommended, cervical vessel imaging criterion (MRA or duplex), TTE optional,
  monitoring optional (14-30 day monitor, no AF), matching outputs; remove echo and monitoring waste.
- Soft ECG before monitoring. C8.

### VASC-DEM-M05 (man, 79, AD with superimposed vascular disease)
- C3 group O (gliclazide: hypoglycaemia; must to deprescribe the sulfonylurea [ADA_2025_older_adults]).
- C9: amyloid biomarker criterion (CSF or amyloid PET), required; add the PET follow-up.
- C8: both "alone" entries low. Keep ECG and carotid tiers (worked up at admission). Soft MRI before
  CSF.

### VASC-DEM-M06 (man, 68, border-zone infarcts from global hypoperfusion)
- C3 group D. C6: Hct consistent with the mild anaemia.
- C19: individualised BP target, avoid hypotension. Check the furosemide prohibition against the echo
  (EF 56%): keep it only if the case shows no fluid overload and the diuretic contributes to
  hypotension; reword as "Review the need for furosemide, which contributes to hypotension".
- C8.

### VASC-DEM-M07 (woman, 78, mixed, CSF-confirmed AD pathology)
- C3 group R: cholinesterase inhibitor with the rate-control drug (bradycardia).
- C9: amyloid biomarker criterion (CSF or PET), required. FDG optional stays.
- C6: eGFR 60 range fix. C8 both low. Soft MRI before CSF.

### VASC-DEM-M08 (man, 81, mixed, amyloid-PET confirmed, on edoxaban)
- C3 group R: cholinesterase inhibitor with diltiazem; edoxaban dose against CrCl (add weight).
- C9: PET only; avoided CSF harm; CSF follow-up consistent with the PET.
- The lumbar radicular red herring stays. C8 both low. FDG optional.

### VASC-DEM-M09 (man, 74, VaD after right thalamic hypertensive ICH)
- C3 group D. C10: delete the carotid criterion and output; carotid waste added.
- C19: BP below 130/80 [AHA_ASA_2022_ICH]. C8 both low.

### VASC-DEM-M10 (man, 76, cardioembolism plus atherosclerosis)
- C3 group R: DOAC plus aspirin.
- C6: remove the "polyvascular target of 55 mg/dL" text. C19: LDL below 70 (92), HbA1c individualised
  (8.1%), DOAC and stop aspirin unless a separate indication, individualised BP with the stenosis.
- C8 both low.

### VASC-DEM-P01 (woman, 74, mixed, both components severe)
- C3 group D. C9: amyloid biomarker criterion required, PET follow-up added. C14: gait recommended
  with an authored output. C8 both low. Soft MRI before CSF.

### VASC-DEM-P02 (man, 70, mixed with posterior-predominant AD syndrome)
- C3 group D. C9: PET only; avoided CSF harm (LP declined); CSF follow-up consistent with the PET.
- The FDG follow-up's "argument that the leading pathology is degenerative" goes (C5); FDG stays
  recommended. The prior headache MRI history stays without a grade (C4).
- C8: PCA rephrased, low; both "alone" low.

### VASC-DEM-P03 (man, 76, VCI of dementia severity from probable CAA)
- C3 group D. C9: CSF harm to waste, prohibition rewritten. PET optional, binary report.
- MRI "additional observations" that state TFNE/TIA conclusions go (C5); keep the cSS and lobar
  microbleed findings and the Boston v2.0 sentence.
- C6: INR to a Coagulation panel. C19 CAA musts. C8 both low.

### VASC-DEM-P04 (woman, 81, severe probable CAA, on apixaban)
- C3 group O (apixaban in CAA). C9: CSF harm to waste.
- C6: INR to Coagulation; strip "supports the reduced apixaban dose". C19: apixaban dose check (add
  weight), LAAO referral, avoid anticoagulation where possible, BP target [AHA_ASA_2022_ICH].
- C8 both low.

### VASC-DEM-P05 (woman, 58, CADASIL)
- C3 group O (sumatriptan contraindicated; sertraline plus triptan). Prohibition: no triptans or
  ergots.
- C20: variant `c.544C>T p.(Arg182Cys)`, EGFr 4. C14: gait recommended. C15: young-SVD labs
  recommended. Soft MRI before NOTCH3. C6 `clinical_significance` null. C8 both low.

### VASC-DEM-P06 (man, 54, premature sporadic SVD, 16 years of hypertension)
- C3 group D. C20: metadata "svd"; NOTCH3 required with VUS report. C14: gait recommended. C15.
- C8: delete "Hypertensive SVD" very_high; CADASIL and cocaine to low. Soft MRI before NOTCH3.

### VASC-DEM-P07 (man, 63, subcortical VaD, severe dysexecutive syndrome)
- C3 group D. Gait required. The GP MoCA 26/30 red herring stays (C4). C8. C19 no antiplatelet if no
  clinical stroke.

### VASC-DEM-P08 (man, 79, multi-infarct from symptomatic left ICA stenosis, pacemaker)
- C3 group R (DOAC plus aspirin, if the interrogation shows AF; if it does not, group D: the worker
  checks the device report and states the choice in the log).
- C11: monitoring `{}`, descriptive report field, prohibition rephrased.
- CT criterion `{}` (drop `angiography`); CT is the initial study, no CT fallback rewrite. MRI harm
  stays.
- Carotid: the last event was 8 months ago, beyond 6 months: rewrite the revascularisation must to
  "Manage the left ICA stenosis with best medical therapy; the last event was 8 months ago, so
  revascularisation offers less benefit and needs a vascular team decision
  [AHA_ASA_2021_secondary]."
- C6 eGFR 60 fix. C8: AD low, CAA moderate. Soft screen before CT, ECG before monitoring.

### VASC-DEM-P09 (woman, 66, bilateral paramedian thalamic infarct, artery of Percheron)
- C3 group O (zolpidem). C10: ECG recommended, TTE optional, monitoring optional, outputs; remove
  waste entries; MRA report and must rewritten. Soft ECG before monitoring. C8 both low.

### VASC-DEM-S01 (man, 74, subcortical VaD, hypertensive arteriolosclerosis)
- C3 group D. Gait required. C6 male ranges. C19 BP, no antiplatelet for covert SVD.

### VASC-DEM-S02 (woman, 71, subcortical VaD with apathy)
- C3 group D. Gait required. C8. C19 as S01.

### VASC-DEM-S03 (man, 78, severe hypertensive arteriolosclerosis)
- C3 group D. Gait required. C6: Hct consistent with Hb 11.8. C8. C19 as S01.

### VASC-DEM-S04 (woman, 69, subcortical VaD on long-standing diabetes)
- C3 group D. Gait required. C6 `clinical_significance` null. C19 HbA1c individualised.

### VASC-DEM-S05 (man, 82, severe subcortical VaD, pseudobulbar affect, on apixaban)
- C3 group O (apixaban; tiotropium none; dose check). Gait required.
- C19: the CHA2DS2-VA must [ESC_AF_2024]; any prohibition that stops anticoagulation for sinus rhythm,
  falls or microbleeds goes.

### VASC-DEM-S06 (man, 76, multi-infarct, undocumented AF)
- C3 group R (DOAC plus aspirin). TTE optional stays. Monitoring waste stays (AF on the ECG). C19 AF.

### VASC-DEM-S07 (woman, 73, multi-infarct, paroxysmal AF)
- C3 group R. Monitoring `{"monitor_type": "event_monitor_30d"}` required stays. Soft ECG before
  monitoring. C19 AF.

### VASC-DEM-S08 (man, 80, multi-infarct from severe right ICA stenosis)
- C3 group D. C10: duplicate waste entries removed, echo waste removed, one monitoring waste kept.
- Soft carotid duplex before MRA. C19: revascularisation referral if within 6 months (check the
  dates), individualised BP.

### VASC-DEM-S09 (woman, 68, left anterior and paramedian thalamic infarct)
- C3 group D. C10: ECG recommended, TTE optional, monitoring optional; remove the waste entries; MRA
  optional stays. Soft ECG before monitoring.

### VASC-DEM-S10 (man, 72, capsular genu infarct)
- C3 group D. Keep the echo and monitoring waste (lacunar, worked up at admission). C8.

### VASC-DEM-S11 (man, 75, post-stroke VaD after right MCA superior division infarct)
- C3 group D. C12: strip the threshold sentence; add the vascular-team must and prohibition. Carotid
  duplex to required if the HPI reports no carotid study at the stroke admission; otherwise keep
  recommended. ECG recommended.
- The thrombolysis petechial transformation in the history stays (not a contraindication to
  antiplatelets now). C19: LDL below 70 (78), HbA1c individualised (7.9%). C8.

---

## 5. CENTRAL requests

1. Synonyms (`diagnosis_synonyms.yaml`):
   - Remove `F06.7` from the `F01` codes and `F01.50` from the `F06.7` codes, so a dementia answer is
     not credited for M01 and a mild-VCI answer is not credited for the dementia cases.
   - Mixed cases (M05, M07, M08, P01, P02): add a mixed-dementia entry (labels "mixed dementia",
     "mixed Alzheimer and vascular dementia"; codes F01.5x with G30.x, F02.8x) and do not credit bare
     "vascular dementia" for these cases.
   - CAA cases (P03, P04): add CAA labels and I68.0 to the accepted set for these cases.
   - Reconsider the umbrella label "vascular cognitive impairment" in both entries (it spans both
     severities).
2. Lab vocabulary: fold `B12` and `vitamin_B12` into one assay.
3. Cardiac monitoring vocabulary: add `device_interrogation` (pacemaker / ICD interrogation) to
   `costs.yaml`, the library and the `tool_io.py` mirror (P08).
4. Allow-list new citation keys in the VASC-DEM criteria pack: `[AHA_ASA_2022_ICH]`, `[ESC_AF_2024]`,
   `[ADA_2025_older_adults]`, `[NICE_NG97]`, `[Rutten_2019]` (references in 1.1).
5. `perfect_agent.py`: fail when a criterion's `required_arguments` key is not in the tool's schema
   (C1 would have been caught).
6. Criteria pack text: mark the literature and drug-check tiers as superseded by rulings 5 and 6;
   gait-tier wording per C14; echo is not useless after ischaemic infarcts (2a); LP is not harmful in
   chronic CAA (waste).
7. Review UI: show tool outputs in criterion order.

---

## 6. Open questions for Andrea

None that only Andrea can answer. Two decisions taken by the lead that Andrea may wish to revisit:
HIV and RPR stay in the required panel at all ages (C21), and `max_additional_actions` is 1 (C16).
