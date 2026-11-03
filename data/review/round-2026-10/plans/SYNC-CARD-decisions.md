# SYNC-CARD: close-out decisions (24 Oct 2026)

Andrea, 24 Oct 2026: resolve every open point "nel modo migliore per la qualità del dataset". SYNC-CARD
has no physician notes (never annotated); the July 2026 tool review (Reviewer 2), the round plan and
the condition summary govern. Every item below is decided and applied. Per-case detail is under
"## Close-out (24 Oct 2026)" in each case log (all 30 changed).

Sources checked on 24 Oct 2026:
- ICD-10-CM tabular (findacode.com group pages): I47 = I47.0, I47.1 (I47.10 SVT unspecified, I47.11
  inappropriate sinus tachycardia, I47.19 other SVT), I47.2 (I47.20 VT unspecified, I47.21 torsades de
  pointes, I47.29 other VT), I47.9; I47.21 carries "code also long QT syndrome (I45.81)" and "use
  additional code for adverse effect"; T36.3X5A adverse effect of macrolides; T45.0X5A adverse effect
  of antiallergic and antiemetic drugs; T43.22- selective serotonin reuptake inhibitors (T43.21- is
  SNRIs), so T43.225A is the SSRI adverse-effect code.
- 2025 ESC/EACTS Guidelines for the management of valvular heart disease (Praz F, Borger MA et al.,
  Eur Heart J 2025;46:4635-4736, doi:10.1093/eurheartj/ehaf194; EACTS announcement and the PMC review
  PMC12871073): update of 2021; TAVI age threshold in tricuspid AS moves from 75 to 70 years
  (transfemoral access, Heart Team, lifetime management).
- ESC Congress 2026 (28-31 Aug) published heart failure, cardiac rehabilitation and CVD-CKD guidelines
  and the 5th UDMI: none supersedes the syncope (2018), pacing (2021), VA/SCD (2022),
  cardiomyopathy (2023), SVT (2019), PE (2019) or AF (2024) guidelines the cases use.
- Locati ET et al., External prolonged electrocardiogram monitoring in unexplained syncope and
  palpitations: results of the SYNARR-Flash study, Europace 2016;18:1265-1272 (PMC4974630).
- Su YT, Kuo CW, Lee JC. Central sleep apnea as an initial presentation of small cell lung carcinoma
  with anti-Hu antibody-related paraneoplastic neurologic syndrome. Respirol Case Rep
  2024;12(12):e70079 (PMC11623976, the RM01 seed; full text read).

## 1. Diagnosis synonyms and labels (summary C1, plus a scan of all 30 cases)

Rule applied: a label is granted only if no mimic in the case's own differential contains its tokens
(the scorer matches when every token of a label occurs in the answer), and only if it names the
case's mechanism, grade or substrate. Scan script: every accepted label against every differential
entry; after the change the only hits are the case's own diagnosis (RM02 "recurrent ARF with
carditis", high) and RS06 "thyrotoxicosis precipitating atrial flutter" (very low; the arrhythmia
is still the diagnosis, so crediting it is correct).

| item | decision | change |
| --- | --- | --- |
| Generic "cardiac syncope", "arrhythmic syncope", "bradyarrhythmia", "tachyarrhythmia", "conduction disease syncope" (C1) | Removed and retired: 29 of 30 cases accepted "cardiac syncope"; "bradyarrhythmia" also sat inside "ACS with bradyarrhythmia" (S01-S04 mimics). | all entries; `RETIRED` |
| R55 in I44 (C1) | Removed: syncope unspecified credits any answer. | I44 codes |
| I44 grades (C1, scan) | Split. I44.1 (M01, M02, RM03, M03): Mobitz II and high-grade labels, I44.30. I44.2: complete heart block labels, I44.30. M03 keeps the CHB labels and I44.2 scoped (telemetry captures transient CHB). Bare "second degree av block" retired (credits Mobitz I). I44.39 (other AV block) and I45.9 (unspecified conduction disorder) dropped. RP04 loses Mobitz II (its ILR shows neither). | `I44.1`, `I44.1+chb`, `I44.2` |
| I47 split (C1) | SVT/AVNRT (I47.1, M05: I47.10, I47.19) and VT do not grant each other; I47.9 dropped. VT labels only in RS05 (I47.20, I47.29), where VT is the diagnosis. P01 must name ARVC (I42.8 added), RP03 CPVT: their mimics (idiopathic RVOT VT, ischaemic VT, polymorphic VT of other causes) contain the VT tokens. | `I47.1`, `I47.2+vt/+arvc/+cpvt` |
| M04 code (C1, summary Q3, plan Q2) | Applied: `icd_codes[0]` T46.2X5A -> I45.81, with I47.21, T36.3X5A, T45.0X5A, T43.225A (verified above). CENTRAL owns the synonyms file and this close-out is that step. Drug-induced and acquired LQT labels only; bare "torsades de pointes" retired (tokens in "congenital LQTS with torsades", M04's first mimic). T46.2X5A entry deleted (no case uses it). | case M04; `I45.81+drug` |
| P04 congenital LQTS (scan) | Congenital, inherited, hereditary, LQT1, KCNQ1 labels; bare "long qt syndrome" and "LQTS" retired ("acquired long QT syndrome" is in P04's differential). NMDAR-ENC and ALS-P08 precedent. | `I45.81+congenital` |
| RP05 (C1) | "complete heart block" removed so the sarcoid cause must be named; "cardiac sarcoid", "sarcoid heart disease" added; "sarcoid myocarditis" retired (tokens in "non-sarcoid myocarditis", a mimic). | `D86.85` |
| RM02 (C1) | Generic CHB and Mobitz labels not granted here (chloroquine toxicity and familial conduction disease are its mimics; temporary pacing plus benzathine penicillin needs the rheumatic cause); rheumatic carditis / rheumatic heart block labels and I01.8, I01.9 added. accepted[0] unchanged (it names the rheumatic cause). | `I44.2` except, `I44.2+rheumatic` |
| RM01 (C1) | Scores the paraneoplastic cause: anti-Hu / paraneoplastic brainstem encephalitis labels. "central sleep apnoea/apnea", "sleep apnea syncope", "nocturnal asystole", "sleep related bradyarrhythmia" retired (heart-failure CSA, OSA and sinus node disease are in its differential); G47.31 (idiopathic CSA) and G47.37 dropped. | `G13.1` |
| RP02 (scan) | "cardiac tumour/tumor" retired ("malignant primary cardiac tumour" is a mimic); RVOT myxoma labels added. | `D15.1` |
| P03 (scan) | Bare "brugada" retired (credits "Brugada phenocopy"); "brugada syndrome" kept. | `I49.8` |
| RM04 (scan) | I26.9 (PE without acute cor pulmonale) dropped: the case has RV strain. | `I26.09` |
| P02 (scan) | Generic HCM labels kept: HCM is the disease; the obstruction is scored by the required exercise echo. "obstructive hypertrophic cardiomyopathy" added. | `I42.1` |
| RS06, S06, RS04, S05, RP01 | Generic labels removed only; RS06 gains "typical atrial flutter", "atrial flutter with 1:1 conduction" and I48.92. | entries |

Applied with `apply_diagnosis_synonyms.py --prune --conditions syncope_cardiac` (30 cases changed);
`--check --conditions syncope_cardiac` and the global `--check` clean. Residual: a primary code still
credits any answer that submits it (P01 and RP03 I47.2, RM02 I44.2, P04/M04 I45.81): the existing
code-alone scorer item in CENTRAL_PENDING. Recoding P01 to I42.8 or RM02 to I01.8 was considered and
not done: neither is a wrong code, and the scorer fix covers all of them.

## 2. Criteria pack (`dataset-generation/criteria_packs/SYNC-CARD.md`)

Rewritten from the plan's canonical facts and the applied tiers: diagnostic definitions, workup
hierarchy and pathway order, targeted labs and drug-check tiers, waste and harm rules (EEG, MRI,
CSF, tilt, exercise, NG232 head CT, D-dimer), treatment statements per mechanism, sequence
constraints (no labs-before-monitoring rule; hard TTE before exercise) and stop rule, subtype tier
table, pitfalls, scoring note, full verified allow-list.

- **C4 citation keys:** added `[ESC_2021_Pacing]`, `[ACC_AHA_HRS_2018_Bradycardia]`,
  `[ESC_2022_VA_SCD]`, `[ESC_2023_Cardiomyopathy]`, `[ESC_2019_SVT]`, `[ESC_2019_PE]`,
  `[ESC_EACTS_2025_VHD]`, `[ESC_2024_AF]`, `[ARVC_TFC_2010]`, `[HRS_2014_Sarcoid]`,
  `[ATS_2020_Sarcoid]`, `[OMahony_2014]`, `[Drew_2010]`, `[Gewitz_2015]`, `[Graus_2021]`,
  `[NICE_NG232]`, `[Fletcher_2013]`, `[REVERT_2015]`, `[Postema_2009]`. Then every criterion, avoided
  action and sequence constraint whose rationale names a guideline cites that guideline's key (ruling
  8): 130 citation arrays changed, including the 40 that were empty (NG232 head-CT rows, RP05 sarcoid
  criteria, RM04 PE rows, exercise-harm rows) and the head-CT rows that cited ESC 2018 for an NG232
  statement. Rows that name no guideline (CSF waste) keep empty citations. All 19 keys used in the 30
  cases (`[NICE_NG232]` in all 30) are in the allow-list; `[OMahony_2014]` and `[REVERT_2015]` are
  allowed but not yet cited.
- **C5 `[Locati_2014]`:** superseded by `[Locati_2016]` (SYNARR-Flash, Europace 2016); M05 re-cited.
- **ESC/EACTS 2025 supersedes 2021 (own finding):** the TAVI threshold changed (75 -> 70 years in
  tricuspid AS). Text "ESC/EACTS 2021" renamed in M03, P01, P02, P04, RP01, RP03, RS04, S02, S04,
  S05; the three valve literature results (S02, S04, S05) cite Praz 2025 with the 70-year threshold;
  S02 (74, trileaflet) must now says TAVI is favoured if transfemoral access is feasible. Statements
  that did not change (Class I intervention in symptomatic severe AS, exercise testing contraindicated
  in symptomatic severe AS, severe AS thresholds) kept. Evidence levels written as "Class I" only
  (levels not read in the full text).
- **RM04 `metadata.citation_gap`:** cleared; its request ([ESC_PE_2019]) is met by `[ESC_2019_PE]`.

## 3. Generator block (`conditions.yaml`, syncope_cardiac)

- `common_followups`: every follow-up was filed under the wrong tool (echo and tilt under
  `interpret_labs`, Holter and exercise under `analyze_ecg`, cardiac MRI under `analyze_brain_mri`:
  summary class F). Now echo -> `order_echocardiogram` TTE, monitoring -> `order_cardiac_monitoring`
  by risk tier with the same recording as fallback, exercise -> `order_specialized_test` only after
  TTE, cardiac MRI -> `order_advanced_imaging` cardiac_MRI. The tilt follow-up is removed (it seeded
  the isoproterenol tilt reports and the tilt-as-work-up defect; tilt is waste or harm here).
- Labs key findings: the all-difficulties CBC/BMP/troponin/Mg battery (seeded class C, pinned panels
  everywhere) replaced by the targeted rules.
- Difficulty variants: "ECG shows complete heart block" and "ECG shows bifascicular block" removed
  from the presentations (a scored result in the patient block, class N); "Normal initial ECG"
  removed from the puzzle presentation likewise.
- Differentials: orthostatic hypotension "reproducible on tilt table" -> active-stand criterion
  (ESC 2018); epileptic seizure no longer "epileptiform EEG" (interictal EEG is usually normal);
  PNES -> psychogenic pseudosyncope.
- Header comment: the "3 cases legitimately skip EEG" line was wrong (EEG is waste in 28) and the
  "required in 11 cases" count is now 10; the round's rules recorded.

## 4. Review-app guidance

`test_guidance_claims.py` failed two SYNC-CARD claims (labs required 11 / recommended 19 -> 10 / 20;
cardiac MRI in 18 -> 21). Responses rewritten in `build_condition_tool_guidance.py` (advanced imaging:
CMR 4 required, 8 recommended, 9 optional, FDG-PET in the sarcoid case; labs: 10 / 20, the assays each
required panel names, TSH and BNP each named in one case, no labs-before-monitoring rule; the
unverifiable "6108 to 4686 EUR" spend figure removed), regenerated with `--write` (only the two
syncope entries changed), claim table updated and extended (TSH 1, BNP 1, CMR 4/8/9, FDG-PET 1, EEG
optional 2). All SYNC-CARD claims pass; the remaining failures are FTD, MG and NPH claims (their
close-outs are running).

## 5. Open questions (summary) and auditor flags

**Q1. RM01 placement.** Decision: keep RM01 in SYNC-CARD as the condition's neurological mimic.
Reason: the benchmark has no paraneoplastic condition to move it to (NMDAR-ENC is antibody-specific),
the pack lists non-cardiac causes of transient loss of consciousness as the R-variant mimics, and the
case tests the condition's central skill: not stopping at a cardiac answer (pacing) when sleep-only
asystole follows central apnoea. Precedent: BACT-MEN Q1, MIG-AURA composition, ALS-P02. Now that its
labels require the anti-Hu cause, nothing is misattributed. No change beyond section 1.

**Q2. RM01 source fidelity.** Decision: the seed is a scenario, not a record the benchmark must
reproduce (NMDAR-ENC precedent; dataset-generation/README: "the real case provides the clinical
scenario"). The source (read in full) differs from the case in: brain MRI normal in the source
(case: dorsal medullary T2/FLAIR lesion); 22 min CPR and intubation (case: brief bag-mask
ventilation); CSF without pleocytosis, protein 59 mg/dL (case: lymphocytic pleocytosis and
oligoclonal bands); 72 years (case: 71); excisional biopsy proved small-cell carcinoma (case: tissue
diagnosis is a must). Each case value is plausible for anti-Hu brainstem encephalitis and internally
consistent, and the diagnosis stays derivable; the shorter arrest removes an anoxic confounder. Kept.
CC-BY 4.0 requires indicating changes: listed under CENTRAL for the dataset card.

**Q3. M04 primary code.** Applied (section 1).

**Auditor flags (summary "3 flagged"):**
- Library exercise report age ("peak 158 bpm, 93%"), and the tier-2 rule that serves the first
  unserved follow-up: code and library, CENTRAL (unchanged requests C3). Case data already
  neutralise both (per-case "not performed" or own reports; neutral initial literature and drug
  blocks).
- Plan head-CT row vs NICE NG232: decided for NG232. Head CT is recommended where NG232 criteria are
  met (M03, RS02, RS03, S01, S03, S04: age 65 or over with loss of consciousness and a head strike, or
  anticoagulation) and waste otherwise; the pack states the rule.

**Worker "please confirm" items (logs):**
- RP04 short monitoring recommended (not optional): confirmed. A typical event occurred during sleep
  (syncope while supine is an ESC 2018 high-risk feature calling for in-hospital monitoring); the
  ILR stays the required, diagnostic study.
- RP05 calcium without ACE, CMR added as recommended, chest imaging recommended: confirmed (serum ACE
  has poor sensitivity and specificity, ATS 2020; LGE extent informs the ICD decision, HRS 2014;
  chest imaging precedes EBUS).
- M02 BMP required (sodium 128 on a thiazide), M05 telemetry as high-risk (palpitation immediately
  before syncope), RM04 catheter-directed rescue rather than fibrinolysis 18 days after arthroplasty,
  RS02/RS03 troponin pinned: confirmed, each guideline-concordant.
- RM02 infranodal block in rheumatic carditis and RM03 CRT-P vs CRT-D: already resolved by the
  verifiers; confirmed.

**Own finding, RS02:** the bridge must offered isoprenaline in a patient with coronary artery disease
and LVEF 42%. ACC/AHA/HRS 2018 (Kusumoto 2019) reserves beta-agonists for symptomatic AV block with a
low likelihood of coronary ischaemia; the must now names temporary transvenous pacing as the bridge
and says to avoid isoprenaline.

## 6. Discriminators (PATTERNS 5, summary C9)

`SYNC-CARD` added to `DISCRIMINATOR_CONDITIONS` in `agent-platform/tests/test_case_guards.py`;
`test_routed_outputs_name_their_study` passes for all 30 (the CENTRAL_PENDING entries for P03, P04,
RP04 prose monitor types were already fixed by the round: every stored monitoring report carries an
exact `monitor_type`).

## Files changed

- Cases: all 30 SYNC-CARD (synonyms; citations; text as above in M03, M04, M05, P01, P02, P04, RM04,
  RP01, RP03, RS02, RS04, S02, S04, S05). Logs appended (Close-out section).
- `agent-platform/config/policies/diagnosis_synonyms.yaml` (SYNC-CARD block, RETIRED).
- `dataset-generation/criteria_packs/SYNC-CARD.md`; `dataset-generation/config/conditions.yaml`
  (syncope_cardiac block).
- `agent-platform/scripts/review/build_condition_tool_guidance.py`,
  `agent-platform/config/review/condition_tool_guidance.yaml`, `agent-platform/tests/test_guidance_claims.py`
  (syncope parts); `agent-platform/tests/test_case_guards.py` (`DISCRIMINATOR_CONDITIONS`).

## Checks

`perfect_agent.py` 30/30; `case_io.py check` on all 30: schema OK, synonym guard OK, no failure names a
SYNC-CARD case; `test_case_guards.py -k SYNC-CARD-` 90 passed; `apply_diagnosis_synonyms.py --check
--conditions syncope_cardiac` clean; SYNC-CARD guidance claims pass.

## Still for Andrea or the physicians

- Nothing needs information only Andrea has.
- SYNC-CARD has never been physician-reviewed and all 30 cases changed: schedule it for the next
  review round, pointing the reviewers at the scoring changes in section 1 (no generic "cardiac
  syncope"; P01, RP03, RM01, RM02, RP05, P04 must name the substrate or cause; M04 recoded I45.81).

## CENTRAL (not done here: vocabulary, code, tests, library)

1. **Vocabulary** (costs.yaml with library reports and the `tool_io.py` mirror), unchanged from
   summary C2; until then these stay musts:
   - `order_specialized_test` `electrophysiology_study` (HV interval, inducibility, accessory-pathway
     refractory period): RS04 (WPW risk stratification and ablation), M01/M02/RM03 context
     (bifascicular block), P01.
   - `order_specialized_test` `sodium_channel_blocker_challenge` (ajmaline/flecainide): none required
     now (P03 has a spontaneous type 1 pattern); for future Brugada cases with a non-diagnostic ECG.
   - `order_specialized_test` `genetic_panel:inherited_arrhythmia` (KCNQ1, KCNH2, SCN5A, RYR2, CASQ2)
     and `genetic_panel:cardiomyopathy` (PKP2, DSP, DSG2, LMNA, MYH7, MYBPC3): P03, P04, RP03 (no
     genetic result or test is stored in these cases), P01, RP01, RS01, RP04, RM02.
   - `perform_clinical_assessment` `orthostatic_blood_pressure` (active stand, 3 min): every case's
     initial evaluation (ESC 2018 Class I), S04 (indapamide, telmisartan).
   - `order_advanced_imaging` whole-body `FDG_PET_CT` for a tumour search (the existing `FDG_PET` is
     cerebral): RM01.
   - `order_specialized_test` or `order_advanced_imaging` `coronary_angiography` already exists; no
     request.
2. **Library** (summary C3): a "no study stored for this order" answer instead of normal tilt (HR 68),
   monitoring, exercise, TEE and mediastinum MRI reports; an age-neutral exercise report (93% of
   predicted at 158 bpm is wrong for most ages); a guard or code fix for the tier-2 rule (first unserved
   follow-up answers any call to a tool without an initial output).
3. **Test BANNED rows for SYNC-CARD** (summary C6; the cases are already clean, so the rows pass):
   "Do not call `", "cited via", "citation_gap" (in clinical text), "Not retrieved on this pathway",
   "on this case's pathway", "on this pathway", "CHA2DS2-VASc", and `monitor_type` "Continuous
   telemetry" (the discriminator guard now also catches the last). C7: fail a tilt report containing
   "isoproterenol" or "isoprenaline" in a case whose history lists ischaemic heart disease, AS or HCM
   (no case fails it now).
4. **Scorer:** code-alone matching (existing CENTRAL_PENDING item) leaves P01/RP03 (I47.2), RM02
   (I44.2), M04/P04 (I45.81) creditable by code; negation matching ("non-obstructive HCM" contains
   "obstructive hypertrophic cardiomyopathy") is the existing negation item.
5. **Review UI** (summary C8): show the stop-rule criteria and sequence constraints next to the action
   criteria.
6. **Dataset card:** CC-BY 4.0 seeded cases are adapted, not reproduced (RM01 departs from PMC11623976
   in MRI, CPR, CSF and age); the card should say that changes were made.
