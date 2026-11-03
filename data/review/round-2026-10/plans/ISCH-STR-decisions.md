# ISCH-STR: decisions on the open questions (24 October 2026)

Andrea's ruling of 24 Oct 2026: every open question is decided and applied for the dataset's
clinical quality. Sources: `ISCH-STR-summary.md` (open questions 1 to 8, auditor flags, CENTRAL),
the extra items of the brief, and the coordinator's echo_type request. Each case change is logged
under "Open questions resolved (24 Oct 2026)" in `logs/ISCH-STR-{case}.md`.

References verified on 24 Oct 2026 (web): AHA/ASA 2026 early management, Prabhakaran S et al.,
Stroke 2026, doi 10.1161/STR.0000000000000513; Miller EC et al., AHA scientific statement on
maternal stroke, Stroke 2026, doi 10.1161/STR.0000000000000514; Tektonidou MG et al., EULAR APS
2019, Ann Rheum Dis 2019;78:1296-1304; Zheng XL et al., ISTH TTP diagnosis guideline, J Thromb
Haemost 2020;18:2486-2495 (treatment companion 2496-2502). The 2026 guideline full text is
paywalled (HTTP 403); where a decision rests on a recommendation class I could not read in the
2026 text, the entry says so.

## Step 1: leaks (all 60 ISCH-STR guards pass)

| case | leak | fix |
| --- | --- | --- |
| M04 | literature output repeated "antiplatelet or anticoagulant therapy for at least 3 months" from its own criterion | criterion `action-6` evidence reworded to a general-evidence description; the output (a correct guideline summary) kept |
| P01 | same, criterion `action-7` | same fix |
| RP05 | CADASIL literature summary repeated the MRI criterion evidence | summary reworded in literature voice |

## Echo type (coordinator request)

Stored echo outputs carried `echo_type` only in `tool_parameters`. Added the value (TTE, TEE,
bubble_study, as each report and its parameters describe) to the stored output in 24 cases (RP03:
bubble_study and TEE; RS02: TEE; the rest TTE). Removed the strict xfail for RP03 and RS02 in
`agent-platform/tests/test_echo_type_routing.py`; 13/13 pass.

## Open questions

**OQ1 NIHSS item 3.** Decision: the official NINDS rule for the whole condition: visual extinction
scores 1 on item 3 and is carried to item 11. Reason: the item 3 instruction says so explicitly; R2
note 9802d420 (S05) is declined on this point. Changed: S01 22 to 23, S05 13 to 14 (exam, key
evidence, musts). M01 to M03 and RP04 already follow it. No reperfusion decision changes.

**OQ2 "Disabling" in low-NIHSS cases.** Decision: IVT stays where a disabling deficit is stated and
justified (P01 gait, RP05 dominant hand and dysarthria, S06 grip and gait); M04 now states why (dysphagia
to saliva, right-arm dysmetria, unsafe gait). RM04 withholding kept, reworded: intracranial dissection
has uncertain benefit in the guideline, so withholding is a defensible choice, not a contraindication.
RM01 kept "do not give": IVT within 3 months of an ischaemic stroke may be harmful (AHA/ASA 2019
COR 3 Harm; class in the 2026 table not read, see "Needs Andrea"), and the deficit is NIHSS 2 and improving.

**OQ3a RS02.** Decision: IVT is given. R2 asked to withhold it until aortic extension was excluded;
the case's own CTA shows the graft, anastomoses and native aorta intact and the entry 7 cm beyond
the graft. With that excluded, no contraindication remains: extracranial cervical dissection is not
one, surgery was 42 days ago (outside 14 days), the deficit is disabling at about 3 hours, BP 162/88.
Musts, prohibitions, key evidence and drug check aligned (antithrombotic after 24-hour imaging, BP
below 180/105 after IVT without further lowering).
**OQ3b RP04.** Kept: give IVT despite the isolated aPTT of 46 s (R2 ruling: no anticoagulant, no
bleeding history, INR and platelets normal; a lupus anticoagulant prolongs the aPTT in vitro). Note:
the 2019 table listed aPTT above 40 s as a reason not to give IVT; the 2026 wording could not be read.
**OQ3c P02.** Kept: no IVT in moyamoya (safety not established, fragile collaterals; R2 ruling).
**OQ3d RS03.** Kept: no IVT. LKW over 10 hours and FLAIR-positive close both time limbs; the recent
resection of a GI malignancy with a 21-day anastomosis adds high bleeding risk.

**OQ4 Mechanism and antithrombotic choices.**
- a. M02: anticoagulation kept; the must now says a 45-second episode meets the 30-second AF
  definition and post-stroke anticoagulation does not depend on burden (AHA/ASA 2021).
- b. M03: changed. The ipsilateral symptomatic 55-60% stenosis is a competing mechanism and is
  referred for vascular surgical review within 2 weeks (CEA for 50-69% decided on patient factors,
  perioperative risk below 6%, AHA/ASA 2021), as M01 already does with PAF.
- c. M05: kept short-term DAPT while awaiting revascularization: the must leaves the regimen to the
  vascular surgeon, and DAPT is needed if stenting is chosen; the omeprazole switch stays conditional on clopidogrel.
- d. RS02: anticoagulation kept (events recurred on aspirin; CADISS and TREAT-CAD show no clear
  difference), now started after 24-hour post-IVT imaging.
- e. RP04: interim aspirin until persistence at 12 weeks, then warfarin INR 2 to 3, no DOAC: kept,
  now cited to `[EULAR_APS_2019]`.
- f. RS04: low-dose aspirin kept. Pregnancy-associated hypercoagulability is not a thrombophilia that
  requires anticoagulation; LMWH if a cardioembolic, venous or thrombophilic indication appears
  (ESO 2022).
- g. Statins: changed. AHA/ASA 2021 (COR 1, SPARCL) gives atorvastatin 80 mg after non-cardioembolic
  ischaemic stroke with LDL above 100 mg/dL and no known CHD, whatever the mechanism. Must added in
  RP03 (112), P05 (108), RM01 (108, with non-oestrogen contraception), P01 (117), RM04 (118). Not in
  RM03 (no infarct: primary prevention, as written), not in pregnancy (RP02, RS04).
- h. ELAN size: classify by the number of named cortical MCA branches. A single branch or a deep
  branch is moderate (within 48 h): M01 (central-artery territory, 2.8 cm), M02 (deep, 2.1 cm). Two or
  more cortical branches, or cortical plus deep, is major (day 6 to 7): M03, S02, S04, RS03, S01, S03,
  S05, RS01. All current musts already match; no change.

**OQ5 Plan departures.** All kept. MRI is recommended where CT is insensitive or MRI is the diagnostic
study (posterior fossa M04, P01, RM04; dissection without infarct RM02, RM03; CADASIL RP05). RM03
echo and monitoring are optional because there is no infarct. P05 duplex is required because DVT changes
treatment. P05 and RP03 need the bubble or TEE study because a plain TTE misses the PFO; RP04
accepts a TTE (Libman-Sacks valve disease).

**OQ6 Stored data changed beyond a recount.** Accepted as made. Each change removed an
inconsistency the logs document, and none changes a label.

**OQ7 From the plan.**
- a. RS04 Miller et al.: verified. Key `[AHA_maternal_stroke_2026]` added to the pack and cited
  beside ESO 2022 in RS04 (CTA criterion, thrombectomy must) and RP02 (MRI criterion).
- b. RM02, RM03 without infarct: kept. The pack's R variant includes dissection without infarct;
  cervical dissection is managed on the stroke pathway, and the cases test not over-calling an infarct.
- c. CTP failing EXTEND in M01, M02, P05: kept. The results fit each infarct (a deep 2.1 cm
  subcortical infarct has no mismatch). Changing the story would add risk without fixing an error.
- d. `max_additional_actions` 1: kept (one overlapping vascular study is reasonable).
- e. RP02 M2: kept (it fits the small infarct and NIHSS 2).

**OQ8 Unresolved data points.**
- a. P03: no change. The TEE shows no abscess, the PR is normal, and telemetry watches for a new block; consistent.
- b. RP01: the left lateral medullary infarct is removed (the medulla is vertebral/PICA territory and
  both vertebrals are patent). PC-ASPECTS 6 is unchanged (the medulla is not scored). The negative
  posterior-fossa NCCT is plausible (CT is insensitive there) and now states that the cerebellum is
  limited by beam hardening.
- c. RS05: a 5.4 x 3.9 cm confluent DWI core with T2 change at 38 minutes contradicted ASPECTS 9.
  Made patchy (largest focus 2.6 x 1.8 cm), T2 negative. Approved case; real inconsistency.
- d. S04 creatinine 1.3: no change (one value is not CKD; no apixaban dose-reduction criterion is met).
- e. S06 has never been physician-reviewed: needs a first physician review (see below).

## Auditor flags (FLAGGED rows)

- M04 template values: EF 60% to 63%, PACs 11 to 8 (now distinct from siblings).
- M05 Friedewald: triglycerides 196 to 211 mg/dL so 218 - 38 - 211/5 = 138 matches the reported LDL.
- S06 synonyms: already resolved centrally (I63.81 now grants only lacunar labels); `--check` clean.
- S06 NCCT naming the capsule and corona radiata with no hypodensity: kept. A radiologist answers the
  clinical question, and it states only what CT shows.

## Extra items

- X1. 'Reference to confirm' entries in the pack: `[EULAR_APS_2019]` and `[ISTH_TTP_2020]`
  completed with verified references and cited in RP04 and RP02. `[AHA_maternal_stroke_2026]` added.
  No unverified entry remains.
- X2. RS02 I97.811 (intraoperative infarction) is wrong for a stroke 6 weeks after surgery. Now
  I63.232, as the other carotid dissection cases. In `diagnosis_synonyms.yaml`: RS02 added to
  `I63.232+dissection`; the `I97.811` entry removed; "perioperative stroke" and "postprocedural
  stroke" added to RETIRED; pruned and checked for ischemic_stroke (the label "iatrogenic stroke"
  stays as case-specific). `accepted[0]` unchanged.
- X3. `conditions.yaml` ISCH block: the default `request_hypercoagulability_panel` follow-up is
  removed and replaced by a comment: write a panel only when the case indicates it and only with its
  criterion. The Holter description now says inpatient telemetry or a 24-48 h Holter after vessel
  imaging, with the type matching the duration.

## Needs Andrea

- S06 needs a first physician review (never reviewed).
- The 2026 AHA/ASA thrombolysis contraindication table could not be read (paywall). Please confirm
  two classes, which the decisions above take from the 2019 wording: prior ischaemic stroke within 3
  months (RM01), and aPTT above 40 s without an anticoagulant (RP04).
- RS02's reversal to "give IVT" contradicts R2's written decision, on the condition R2 set. Tell R2
  at re-review.

## CENTRAL

None new. No new vocabulary or code is needed.
