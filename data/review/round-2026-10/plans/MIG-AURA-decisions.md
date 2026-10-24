# MIG-AURA: close-out decisions (24 Oct 2026)

Andrea ruled on 24 Oct 2026: "per i punti aperti, risolvili nel modo migliore per la qualità del
dataset". MIG-AURA has no physician notes; the July 2026 tool review (Reviewer 1) and the round plan
govern. Every item below is decided and applied; per-case detail is under "Close-out (24 Oct 2026)"
in each case log (all 30 changed).

Sources checked on 24 Oct 2026: ICHD-3 (Cephalalgia 2018;38:1-211); Evans RW et al., Neuroimaging
for migraine: AHS systematic review and evidence-based guideline, Headache 2020;60:318-336;
Silberstein SD et al., Neurology 2000;55:754-762 (treatment parameter; the US Headache Consortium
imaging guideline was published separately); UKMEC 2025 (CoSRH, BMJ Sex Reprod Health
2026;52:1-138; tables read for migraine, stroke and breastfeeding); Sacco S et al., EHF CGRP
guideline 2022 update, J Headache Pain 2022;23:67 (full text read: CGRP antibodies "included as a
first line treatment option"); Sacco S et al., EHF/ESC contraception consensus, J Headache Pain
2017;18:108; VASCERN, Do's and Don'ts: CADASIL (April 2023, full text read); Mancuso M et al., Eur J
Neurol 2020;27:909-927 (abstract only); Eigenbrodt AK et al., Nat Rev Neurol 2021;17:501-514;
Evans RW et al., Headache 2010;50:1089-1099; MHRA Drug Safety Update June 2024; Voskoboinik A et
al., NEJM 2020;382:20-28; Thompson BG et al., Stroke 2015;46:2368-2400; Parikh S et al., Genet Med
2017;19(12); Van Gelder IC et al., ESC AF 2024; WHO MEC 6th edition (November 2025, existence only).

## 1. Diagnosis synonyms and labels

| item | decision | change |
| --- | --- | --- |
| "migraine aura" in the G43 group (CENTRAL 1) | Removed and retired: its tokens are a subset of "migraine without aura", so a wrong answer scored. | `diagnosis_synonyms.yaml`: G43 category entry replaced by G43.109 entries; `RETIRED` + "migraine aura" |
| Hemiplegic cases M03, P09, RM11, RS11 (G43.409) received the generic G43 labels and codes (scan) | Removed. Hemiplegic migraine is the subtype these cases score (triptan avoidance, genetics referral), and "migraine with typical aura" names a different ICHD-3 entity (typical aura excludes motor aura). No G43 category entry remains. | hemiplegic labels and G43.4, G43.419 only |
| M04 brainstem aura (CENTRAL 1, scan) | Generic and typical-aura labels removed (1.2.2 is not typical aura and changes the triptan decision); "migraine with brainstem aura", "basilar migraine", "basilar type migraine" added. Residual: G43.109 is the primary code (ICD-10-CM has no brainstem-aura code), so a code-only generic answer still scores (scorer CENTRAL, below). | `G43.109+brainstem` |
| M05 acephalgic (CENTRAL 1) | Added "typical aura without headache", "acephalgic migraine". Declined "migraine aura without headache": "migraine without aura, tension-type headache" contains its tokens. | `G43.109+acephalgic` |
| M01, M07 relabelled 1.5.2 (CENTRAL 1, labels) | Confirmed: each HPI describes a single attack, and ICHD-3 1.2 needs two. "Probable migraine with aura" added (scoped); "migraine with aura" and "migraine with typical aura" stay credited, since a probable diagnosis named without the qualifier is the same entity and its management does not change. | `G43.109+probable` |
| P03 code (plan Q2, CENTRAL 1) | `icd_codes[0]` I63.9 -> G43.609: ICD-10-CM codes migrainous infarction under G43.6 ("persistent migraine aura with cerebral infarction") with I63 as the additional code, so I63.9 first was wrong (ruling 3). Stroke labels and I63 codes are no longer granted: a cryptogenic, cardioembolic or lacunar stroke answer is exactly the error the case tests. New entry credits migrainous infarction labels and G43.6, G43.601, G43.611, G43.619. This settles the CENTRAL_PENDING prune item (P03 loses "stroke" and the mechanism labels, as intended). | case + `G43.609` entry |
| P07 (CENTRAL 1, CENTRAL_PENDING prune item) | Mechanism labels only. Plain "stroke", "lacunar stroke", "lacunar infarct" go, as the plan asked; so do the generic ischaemic-stroke labels and I63.9 (they would credit "migrainous infarction (ischaemic stroke)", the wrong answer the label names), "embolic stroke" (would credit paradoxical embolism through the case's small PFO), "PCA territory infarct" (would credit a migrainous PCA infarct) and I63.432 (left PCA; the infarct is right). Added "cardioembolic infarct/infarction", "atrial fibrillation stroke/infarct". | `I63` category `except_cases: [MIG-AURA-P07]`; `I63.4` scoped to P07; `RETIRED` + "PCA territory infarct" |
| P08 "mitochondrial encephalomyopathy" (scan) | Kept: a broader but correct class name; no other mitochondrial syndrome's usual name contains its tokens. | none |
| Familial vs sporadic hemiplegic migraine (scan) | Cannot be separated by labels ("familial hemiplegic migraine" contains "hemiplegic migraine"). Listed under the existing scorer item (per-case rejected tokens). | CENTRAL |
| M02 label (CENTRAL 2) | Applied: "small PFO, no closure indicated" had no data (no echo, and none indicated). Now "Migraine with combined visual and sensory aura (ICHD-3 1.2.1); combined OCP contraindicated (WHO Category 4)". | M02 `accepted[0]` |
| RM11 label (auditor decision) | Applied: ten fields record two aura-triggered seizures. Now "Sporadic hemiplegic migraine (ICHD-3 1.2.3) with migraine aura-triggered seizures (migralepsy, ICHD-3 1.4.4) and reversible MRI changes; structural and metabolic mimics excluded". | RM11 `accepted[0]` |

Applied with `apply_diagnosis_synonyms.py --prune --conditions migraine_with_aura` (28 cases
changed); `--check --conditions migraine_with_aura` clean.

## 2. Criteria pack

`dataset-generation/criteria_packs/MIG-AURA.md` rewritten from the plan: literature and drug check
no longer required; work-up tiers, MRA/MRV as separate studies, waste list, treatment statements,
soft sequence constraints and stop rule as applied; full verified allow-list.

- **[AAN_2000] superseded (own finding).** It was cited 112 times, mostly for imaging and waste,
  but Silberstein 2000 covers acute and preventive treatment, not neuroimaging (ruling 8: a citation
  must say what it is cited for). Replaced in all 29 citing cases: imaging criteria and CT/MRA waste
  -> [AHS_neuroimaging_2020] (Evans 2020, grade A no-imaging recommendation); CSF, EEG, echo,
  monitoring and OCT waste -> [ICHD_3] (the diagnosis is clinical); M08 sertraline-triptan check ->
  [AHS_triptan_SSRI_2010]; two optional drug checks (M07, P01) left without a citation.
- **UKMEC 2025 supersedes UKMEC 2016 (own finding).** Categories used in the cases are unchanged
  (CHC 4 in migraine with aura; POC and LNG-IUD 2; Cu-IUD 1; after stroke POP and implant 2 to start,
  3 to continue; CHC 4 under 6 weeks breastfeeding). "UKMEC 2016 (amended 2019)" text updated in
  M01, M02, M04, M06, P03, RM11, S07. WHO MEC 5th edition mentions kept as named text (6th edition
  November 2025 not checked; UKMEC governs).
- **Sacco key (CENTRAL 4).** `[Sacco_2022]` is the EHF CGRP 2022 update and is used correctly for
  CGRP antibodies; the 2017 contraception consensus is a separate key `[Sacco_2017]`.
- **EHF_EAN_2021.** The plan described Eigenbrodt 2021 as a cardiovascular statement; it is the
  EHF/EAN "ten steps" consensus. Pack entry describes it correctly (no case cites it).
- Other requested keys added with verified references; sources workers named in text listed.

## 3. Generator block (`conditions.yaml`, migraine_with_aura)

- MRI key findings: "Normal vascular anatomy on MRA" removed (vessel text in a brain MRI report,
  class K); "No DWI restriction (excludes stroke)" -> "DWI excludes infarction, not TIA"; "DWI
  restriction ... (migrainous infarction vs TIA)" rewritten (an infarct is never a TIA; migrainous
  infarction needs an aura over 60 min); "Cerebellar T2 lesion: CADASIL pattern" corrected to anterior
  temporal pole and external capsule; MELAS stroke-like lesion added.
- Labs: the default panel ("coagulation normal rules out thrombophilia", ANA/aPL in every case,
  lipids "in complex migraine") replaced by targeted panels (ESR/CRP over 50, aPL only in an infarct
  work-up, lactate/CK only for MELAS).
- TIA differential: "DWI restriction" removed (TIA has no infarct; the distinction is clinical).
- Difficulty variants: results and answers removed from presentations ("ICHD-3 criteria met", "MRI
  normal", "DWI negative"); the moderate variant now has a previous episode (a first episode would be
  1.5.2).
- Follow-ups: thrombophilia -> antiphospholipid only; mtDNA moved to `order_specialized_test`
  (urine or buccal heteroplasmy, after MRI); MRA follow-up added as its own study. Header comment
  records the round's rules (literature optional, `{"drug"}` checks, counselling as musts).

## 4. Review-app guidance

`test_guidance_claims.py` failed four MIG-AURA claims. Updated responses in
`build_condition_tool_guidance.py` (MRI: absent 11, optional 2, recommended 11, required 6; MRA in 8,
MRV in 1; ECG recommended only in P08; labs targeted in 5, P08 mtDNA the one required laboratory
order; echo text de-duplicated and composition decision stated; EEG accepts routine), regenerated
with `--write` (only the five migraine entries changed), claim table updated and extended (MRA,
MRV, labs recommended, ECG). `test_guidance_claims.py` and `test_condition_tool_guidance.py` pass.

## 5. Open questions (summary section) and auditor flags

1. **Composition (P06 CADASIL, P07 cardioembolic stroke, P08 MELAS).** Keep them in MIG-AURA as
   mimic cases with their own labels and codes. Reason: the dataset builds mimics this way in most
   conditions (ALS-P02 precedent), the pack lists CADASIL and MELAS as migraine-with-aura mimics, and
   each case tests the condition's central skill (not calling migraine with aura when the work-up
   shows another cause). Guidance text updated to say so.
2. **Authored data supporting labels** (P09 sister's 3 mm aneurysm, P03 5-hour aura, P08 prolonged
   stroke-like episode, P05 5-minute build-up). Accepted: these are synthetic cases, each detail is
   clinically plausible, consistent across the case and is what the label requires (AHA 2015 familial
   definition; ICHD-3 1.4.3 over 60 min; MELAS stroke-like episode; P05's build-up is elicited by the
   structured history, consistent with the HPI's stereotyped 15-25 min attacks). Nothing for Andrea.
3. **Policy choices:**
   - P02 stop apixaban (CHA2DS2-VA 0): keep. ESC 2024 does not indicate anticoagulation at 0; the
     must already routes the decision through cardiology; alcohol reduction per Voskoboinik 2020.
   - RM11 EEG routine or video: keep (either answers the post-ictal question; video preferred).
     CSF neutral: keep (no fever or meningism; pleocytosis can occur in hemiplegic migraine, so an LP
     is neither required nor waste). ECG avoided action removed: keep (a first seizure makes an ECG
     defensible).
   - P08 triptan avoidance in MELAS: keep as a prohibition stated as expert opinion (vasoconstriction
     in a stroke-like-episode disorder; prohibitions carry no scalar weight). Lactate 2.8 mmol/L kept:
     raised (range 0.5-2.2), consistent with MELAS, and the spectroscopy lactate doublet carries the
     diagnosis.
   - P06 triptans in CADASIL: the EAN 2020 attribution could not be verified; VASCERN 2023 (read)
     says no evidence contraindicates triptans but they should not be first line (second or third
     choice only). The P06 prohibition stays because his MRI shows an old lacunar infarct (cerebral
     infarction is a label contraindication) and now says so; drug output, literature result and
     rationale restated to VASCERN; P04's CADASIL sentence likewise.
   - S cases without an MRI waste avoided action: keep (plan default). An unindicated MRI already
     costs the stopping score (`max_additional_actions` 0), and the July ruling makes MRI optional for
     red flags rather than an error; pack section 3 records it.
   - M08 SSRI with triptan: allowed with counselling (AHS 2010); label already says so.
4. **CGRP statement (own finding, S07, S10, S09).** The musts said the EHF 2022 guideline supports
   CGRP antibodies "after two failed oral preventives": that was the 2019 EHF guideline; the 2022
   update makes them a first-line option. Rewritten; the NICE threshold (at least 3 failed
   preventives, at least 4 migraine days) is attributed to NICE TA659/TA682/TA764, not to
   [Sacco_2022].
5. **Pre-existing em dashes** (auditor): left (ROUND_POLICY forbids them only in new text).
6. **RM11 label vs data** (auditor): applied (section 1).

## Files changed

- Cases: all 30 MIG-AURA cases (synonyms, citations); substantive text in M01, M02, M04, M06, P03,
  P04, P06, RM11, S01, S03, S07, S09, S10; codes/labels in M02, P03, RM11. Logs appended.
- `agent-platform/config/policies/diagnosis_synonyms.yaml` (G43 entries, G43.609, I63 except, I63.4,
  RETIRED).
- `dataset-generation/criteria_packs/MIG-AURA.md`; `dataset-generation/config/conditions.yaml`
  (migraine_with_aura block).
- `agent-platform/scripts/review/build_condition_tool_guidance.py`,
  `agent-platform/config/review/condition_tool_guidance.yaml`, `agent-platform/tests/test_guidance_claims.py`
  (migraine parts).
- `CENTRAL_PENDING.md`: MIG-AURA prune item and leak-guard count settled.

## Checks

`perfect_agent.py` 30/30; `case_io.py check` on all 30: schema and synonym guard OK, no test failure
names a MIG-AURA case; `test_case_guards.py -k MIG-AURA-` 60 passed;
`apply_diagnosis_synonyms.py --check --conditions migraine_with_aura` clean; guidance tests pass.

## Still for Andrea or the physicians

Nothing blocks. Scoring changes a physician may want to see: P03 now rejects plain stroke answers
(G43.609), P07 rejects generic "ischaemic stroke" and "embolic stroke", hemiplegic and brainstem cases
reject a generic "migraine with aura" label. The whole condition was never physician-reviewed.

## CENTRAL (not done here)

- Vocabulary: `order_specialized_test` `genetic_panel:hemiplegic_migraine` (CACNA1A, ATP1A2, SCN1A,
  PRRT2; next-generation panel), for M03, RM11, RS11 and P09; until it exists the test stays a
  referral must.
- MockServer: `order_cardiac_monitoring` has no duration discriminator (P07 needed a separate
  short-recording follow-up so a 24-hour Holter does not return the loop-recorder AF); a
  monitor_type-aware match is wanted.
- Scorer: code-only matching credits a generic answer in M04 (G43.109 is the brainstem-aura code too);
  per-case rejected tokens would also stop "familial hemiplegic migraine" scoring in the sporadic
  cases and "migrainous infarction (ischaemic stroke)" in P07 (existing items in CENTRAL_PENDING).
