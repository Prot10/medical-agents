# ISCH-STR: condition summary of the October 2026 review round

Condition auditor, 23 October 2026. Sources: the plan (`plans/ISCH-STR.md`), the 30 case logs
(`logs/ISCH-STR-*.md`, each with a worker table, a verifier section and, for nine cases, a
"Condition audit" section), the notes (`notes/ISCH-STR.json`, 97 notes, all from Reviewer 2) and
scripted checks over the 30 case files.

## Final state

- `perfect_agent.py` on all 30 ids: 30/30 pass. `case_io.py check` on all 30 ids: schema OK for
  every case, synonym guard OK; the suite has 2 failures elsewhere, none naming an ISCH-STR case or
  the condition.
- Every one of the 97 note ids appears in exactly one log (its own case), in exactly one table row,
  with a ruling.
- Scripted uniformity checks over the 30 files (all clean after the audit fixes below):
  - Template strings: no `[AHA_ASA_2019]`, `[AHA_ASA_2014]`, free-text "AHA/ASA acute ischemic
    stroke guideline 2026", "140/90", NCCT management text, "clinically implicated territory",
    "Tier per the July 2026...", "Off-pathway modality", `vocab_gap` text, "Exclusion studies"
    panels, `holter_72h`, HPI eligibility verdicts ("outside/within the standard window"), "on the
    cusp", the template telemetry and secondary-prevention musts, or echo "Abnormal values (H)"
    impressions.
  - Order: criteria start NCCT, labs, ECG, CTA in 29 cases (RP02: NCCT, labs, ECG, MRI with MRA).
    The CTA is the first follow-up (RP02: MRA). Literature is optional, at most one criterion, and
    always last.
  - Constraints: only soft ones. NCCT before CTA, CTA before echo and before monitoring everywhere,
    plus CTA before CTP where CTP exists. RP02 uses the MRI in place of the CTA.
  - Stop rule: `required_before_assessment` equals the set of required criteria in all 30, and
    `max_additional_actions` is 1.
  - Tiers match plan 3.1: echo, monitoring, CTP, drug check (C7 list) and aetiology labs (only P05,
    RP02, RP03, RP04 required, RS04, RP05). The logged departures are listed under Open questions.
  - Every CTA has `contrast_used` true, and its impression opens with the principal finding.
  - Every monitor report states that it was recorded on the stroke unit after admission, and its
    type matches its duration.
  - Every case has one LKW must and one explicit decision must ("IV thrombolysis: ...
    Thrombectomy: ..."); RM02 and RM03 have no infarct and so no reperfusion must.
  - The C5 "COR 3 No Benefit" text appears only in cases with no reperfusion.
  - BP-lowering musts appear in every case that gives IVT with BP at or above 185/110 (M05, RS05,
    S01 to S05).
  - Troponin musts in RS01, RS05, S01 to S04; rate-control musts in RS01, RS03, S01 to S04.
  - Anion gap is 9 to 15 and Hct about 3 x Hb in all 30. Hb and Hct reference ranges match sex and
    pregnancy.
  - NIHSS totals agree across all fields within each case.
  - `metadata.case_body_concerns` and `vocab_gap` are empty everywhere. RP05 keeps a
    `citation_gap` that lists its new citation keys.

## Error classes and how each was fixed

| class | defect | notes | fix |
| --- | --- | --- | --- |
| C1 pathway order | Echo, Holter, thrombophilia panel, literature and drug check ran before the CTA in all 30. | 6feeb306, eae4a343, 132ec224, 6ecd20c2, f7f3b32d | Criteria and follow-ups reordered: core diagnosis first, aetiology next, literature last. Soft constraints replace the template hard NCCT-to-drug-check constraint. |
| C2 monitoring timing and type | 24 to 48 h Holters (P05 also a 30-day monitor) were reported before the CTA; `monitor_type` contradicted `duration_hours` (8 cases at 48 h, 2 at 72 h). | f7f3b32d, 6ecd20c2, 132ec224 | Every report is recorded on the stroke unit after admission, with a type that matches its duration and criterion alternatives `holter_24h`/`holter_48h`/`telemetry`. P05 and RP03 outpatient monitors became a must. Canonical stroke-unit telemetry must. |
| C3 extended window on one limb | Wake-up cases closed IVT on DWI-FLAIR only; M03 used the 1.8 TIMELESS ratio. | 06456aa6, b798000b, 5e0dbec2, 6d879e51 | Both limbs addressed in every wake-up or unknown-onset case. New CTP (recommended) failing EXTEND in M01, M02 and P05; M03 restated on EXTEND (ratio 1.4, mismatch 8 mL); P04 CTP required for EVT. |
| C4 reperfusion decision | Template LKW, door-to-needle and pre-IVT BP musts pasted regardless of eligibility; no decision stated. | a407727c, db9768a7, 0bc84371, c0233fc3, 3f611291, 55e9c9c7, 19d1e303, 4660dbc9, 19ff066b, 16f5be33, d703ff12, 7eec1867, 4e5a5ed6, cd879e2d, 10f6a890, 7d003b88 | One case-specific LKW must and one decision must per case. IVT musts only where IVT is given, BP lowering where needed, and EVT musts with §4.7/§4.7.3 criteria. RS02 vascular discussion must per §4.12. |
| C5 "below 140/90" prohibition | Not a guideline figure (27 cases). | df9be70d, db9768a7 | AHA/ASA 2026 §4.3 COR 3 No Benefit text where there is no reperfusion; removed where there is. |
| C6 template secondary prevention | "Antiplatelet or anticoagulation and high-intensity statin per mechanism" in 20 cases. | 027c14a1, 7d003b88, 60a69345, dc0e0aee, ec9af643, f9e644a8 | Mechanism-specific musts: DOAC with CHA2DS2-VASc, HAS-BLED and ELAN timing; carotid revascularization 2 days to 2 weeks; dissection 3 months; moyamoya; IE (no antithrombotic); PFO (AAN 2020, RoPE); APS (warfarin); pregnancy (LMWH or aspirin, no statin or warfarin). |
| C7 drug-interaction checks | Required in all 30 as an alteplase checklist ignoring the patient's drugs. | ec825b6a, ec9af643, 4660dbc9, ffd8459c, 7d4454af, 4332d93d, 7d003b88 | Required only where a concrete issue exists (17 cases: M01, M02, M05, P01, P02, P03, RM01 to RM04, RP02, RP04, RP05, RS03, RS04, S03, S04), recommended elsewhere. Outputs list the actual medicines and allergies, and are placed before the decision they inform. |
| C8 literature as a step | Recommended literature criteria; orphan outputs; an unverifiable statement (RS04). | (survey) | Optional, last, one general-evidence output per case. RS04 uses ESO 2022. P02 and P03 moved out of the initial work-up and P02 to P04 got matchable arguments (audit, below). |
| C9 aetiological panels | Orphan thrombophilia follow-ups (19), contradictory "Exclusion studies" panels (9), duplicate lipid/HbA1c steps, Factor V Leiden negative and positive. | ba9bdca8, 7fc996b4, 7c967ef5 | Scaffolding panels removed. Aetiology criteria kept only in P05, RP02, RP03, RP04, RS04, RP05. A single FVL entry in P05. VITT excluded in RP03 with reasons. |
| C10 leakage and timeline in the patient block | Eligibility verdicts and ordered-study results in HPIs; LKW clocks; unsupported antecedents. | 06456aa6, b798000b, cd879e2d, d3d1bb91, 9685cde6, 9e53616c, eea99434, bc4354fa, 212fe881 | Verdicts removed with times kept. RS04 has one clock (LKW 18 h). Prior silent infarcts are moved into the PMH. RM02 HPI no longer names dissection (verifier). |
| C11 report defects | CTA impressions omitted the occlusion; CTA `contrast_used` false (16); NCCT management text; echo "Abnormal values (H)"; MRI impressions omitted or invented findings; RP05 PP1. | ef70fcc1, ec46ecc7, d923cc86, 3fea7d10, c7026407, 50ffe53e, eea99434, fdfaae93, 0fd09831 | All fixed per plan; canonical NCCT impression with ASPECTS; real echo impressions. |
| C12 imaging timing | FLAIR "3-4 hours" at under 3 hours (7 cases); intramural haematoma age. | fdfaae93, c9b7c467, 667da1af, 17db3372 | FLAIR wording matches LKW in all 30. RM03 haematoma acute; RM04 subacute, explained by 3 days of neck pain. |
| C13 NIHSS/GCS miscounts | Totals not derivable from the exam; invented items (hand, gait). | a46588b0, d1ad43a9, b36e42fb, 7695631d, ceadf1cd, bcb508a7, 0f2a9dec, a220ccd8, de5e529f, f6628b06, 9802d420, 8b01e6c6 | Every NIHSS recounted and itemised. Exams made scorable where needed. Totals agree across fields. See open question 1 on item 3. |
| C14 abnormal results without action | Impossible anion gaps (6 cases), Hct not 3 x Hb, untreated troponin, rapid AF, thiamine, apraclonidine. | 9c627e7e, 55291633, 3c9586d9, 22f804cf, 97a9f686, 73bf8a81 | Values corrected. Troponin, rate-control and thiamine musts added. Verifiers also fixed MCV/RBC arithmetic (S01, S02), a glucose interpretation (P03) and a female Hb range (RS04). |
| C15 neuroanatomy and laterality | Wrong-side signs, gaze deviation, HINTS, neglect side, UMN face, deficits no lesion explains. | f9ddb5ea, b36e42fb, c97b3f6e, 20b2416f, 5f9d3088, 3451a4bc, 8b0515f8, 64a4f269, 1fe2a211, 68d979b1, 4a90422f, 4d4b454f | S01 body flipped to the left-hemisphere lesion. RS03 fetal PCA with capsular extension. RP02 M2 occlusion and the dissection 2 cm beyond the bulb. Verifiers extended S03 and S04 lesions to explain the hemianopia. |
| C16 contrast allergy and CKD vs CTA | CKD and mild contrast reaction musts or prohibitions against a required CTA. | 799ea64c, 0a65085d | Canonical "proceed with CTA" must; CKD prohibitions removed. |
| C17 engineering leakage and stale metadata | "document in metadata.vocab_gap" inside a must; tier and off-pathway lines; stale concerns. | 2e2ccbff | Removed; P05 venous duplex added; concerns resolved and emptied. |
| Case-specific | RM02 label; P03 TEE and prophylaxis; P02 family screening and silent infarction; RM03 sweating pearl and cluster headache discriminators; RM04 V4 extension; RP02 MRA instead of CTA; RP03 MRV; P05 DVT; RP05 migraine. | ffd8459c, b331962d, 0c5ef38d, daf0605e, bc4354fa, 1a96c82d, 02d120ad, d0aedb17, 15ecae28, 00e99485, 2e2ccbff, 58f1cd4c | As in plan section 4. RM02 relabelled to I77.71 (ICA dissection without infarct). |
| Found by verifiers (class) | HAS-BLED "prior stroke" in AF cases without a previous stroke (S01 to S05); RM01 IVT despite a 2-week-old infarct; P05 must leaving no interim antithrombotic; RS02 BP must contradicting the C5 prohibition. | none | Fixed in each case (30 verifier changes in 20 cases). |
| Found by the audit (class) | Template numbers identical across cases (PATTERNS 4): M01 to M03 shared ECG intervals and rate, echo LAVI/septum/EF, Holter average, M03 copied M01's AF episode clock and PAC count; S02 to S04 shared the Holter average/range and a unitless LAVI "42". | none (M02 and M03 workers had FLAGGED it) | M02, M03 ECG/echo/Holter values made distinct; S03, S04 Holter average/range and LAVI distinct; units added to unitless LAVI in RM03, S01, S03, S04 (approved S02 and S05 left: impression carries the unit). |
| Found by the audit (class) | Literature in `initial_tool_outputs` (P02, P03), shown as "Initial workup"; literature criteria with exact-query `required_arguments` that no agent query can equal (P02, P03, P04). | none | P02 and P03 outputs are now the last follow-up (served for any query, checked); arguments set to {} as in the other 27 cases. |

## Counts

- Reviewer notes (97, R2 only, 29 cases; S06 never reviewed):
  - FIXED: 97. One of them, RM03 `02d120ad`, is FIXED for its rewrite while its alternative
    option is DECLINED (see below).
  - ALREADY-FIXED: 0. DECLINED (whole note): 0. BLOCKED: 0.
- Own findings:
  - Workers: 530 logged; 524 FIXED and 6 FLAGGED. The auditor has since fixed 2 of the 6 (the M02
    and M03 template values), so 4 stay flagged: M04 shared PAC/EF values, M05 Friedewald LDL,
    S06 synonyms (CENTRAL), and the S06 NCCT observation.
  - Verifiers: 30 further changes in 20 cases.
  - Auditor: 13 changes in 9 cases (M02, M03, S03, S04, P02, P03, P04, RM03, S01), each logged
    under "Condition audit" in that case's log.
- Cases changed: 30 of 30.
- Approved cases changed: 4 of 4 (RS01, RS05, S02, S05; R2 approvals per the notes file), each
  for logged real errors. The audit changed no approved case. (PATTERNS.md says 5 ISCH-STR
  approvals; the notes file shows 4 approved, with P04 and RM01 in progress.)

## DECLINED and BLOCKED notes

- RM03 `02d120ad-eac1-4b0e-8618-5b6eeec89880`: the rewrite of the prohibition and of the cluster
  headache entry is FIXED. The note's option to raise cluster headache in the differential is
  DECLINED. Reason: the differential is the assessment-time view (ROUND_POLICY ruling 7), and CTA
  and MRI show the dissection, so cluster headache stays low. Its discriminators are written into
  the prohibition and the differential.
- No note is BLOCKED.

## CENTRAL requests (consolidated)

1. **Criteria pack** `dataset-generation/criteria_packs/ISCH-STR.md`:
   - Add these keys to the allow-list: `[AHA_ASA_Stroke_2026]`, `[AHA_ASA_2021_secondary]`,
     `[ESO_women_2022]`, `[ESC_endocarditis_2023]`, `[AHA_IE_prophylaxis_2021]`, `[AAN_PFO_2020]`,
     `[Kattah_HINTS_2009]`, plus `[EAN_monogenic_SVD_2020]` and `[Sumatriptan_SmPC]` (RP05).
   - Proposed new keys: `[Chabriat_2009]` and `[OSullivan_2001]` (RP05), `[EULAR_APS_2019]` (RP04)
     and an ISTH 2020 TTP key (RP02).
   - Mark `[AHA_ASA_2019]` and `[AHA_ASA_2014]` superseded.
   - Align the literature and drug-check tiers with rulings 5 and 6, and replace the BP pitfall
     with the plan 1.2 rules.
2. **Synonyms** (`diagnosis_synonyms.yaml`; nothing was hand-edited):
   - The I63 category appends "lacunar stroke/infarct", "cardioembolic stroke" and "embolic
     stroke" to every ISCH case, crediting wrong mechanisms. Reported in M04, P01, P05, RM04,
     RP01, RP02, RP03, RP04, RP05, RS01, RS03, RS04, RS05, S01, S02 and S06.
   - The I63.81 lacune (S06) accepts "embolic", "cardioembolic" and "CADASIL".
   - The I63.011 entry appends "lateral medullary syndrome/Wallenberg" to RM04, which has no
     medullary infarct.
   - The I63.232 entry grants "moyamoya disease" (RM01 and other I63.232 cases).
   - The I77.71 entry appends I63.231 (an infarct, and on the wrong side) to RM02 and RM03.
   - RM02 was relabelled to I77.71 and needs its list regenerated (the worker did this for the
     case only; a central `--prune` run should confirm).
   - RP02 `accepted[0]` changed from "ostium" to "cervical" ICA dissection; regenerate its
     synonyms for a dissection.
3. **Labels and codes left untouched (owner decision):**
   - RS02 `icd_codes[0]` I97.811 is "intraoperative infarction", but this stroke occurred 6 weeks
     after surgery.
   - P05 `accepted[0]` names Valsalva, which the history does not record.
   - Several `accepted[0]` values contain em dashes (M01 to M05, S06).
4. **Schema and simulator:**
   - `EchoReport` has no `echo_type` field, so the value written into echo outputs (plan C11) is
     dropped. The MockServer echo discriminator never fires, and echo follow-ups route by trigger
     tokens only. In consequence a plain TTE order receives the bubble study (P05, RP03), a TTE
     order receives the TEE (RS02), and a TEE order receives the TTE (P02). Add
     `echo_type: str = ""` to `EchoReport` and to the `tool_io.py` mirror.
   - `tool_parameters` on follow-ups is not a schema field either. It is read by nothing, so its
     absence in some follow-ups (P02, P03 and P04 monitors, drug checks, literature) has no
     effect. Either add it to the schema or strip it.
   - With no CTA follow-up, an `order_ct_scan` angiography order is answered with the
     non-contrast CT (RP02).
   - `event_monitor_30d` and `telemetry` orders are answered with the stored Holter (RP03, RP04).
   - `perfect_agent.py` copies only the first alternative (e.g. the TEE alternatives of P05 and
     RP03 are never exercised), and its source labeller prints `<- ?` for initial outputs.
5. **Fallback library:**
   - Confirm normal reports for `MR_venography`, `CT_perfusion` and
     `lower_extremity_venous_duplex`.
   - The `MR_angiography` normal text assumes a contrast-enhanced neck MRA; pregnancy cases need a
     protocol-neutral (TOF) text.
6. **Review UI:**
   - Show the initial work-up (NCCT, labs, ECG) as numbered steps in criterion order (M02 note
     eae4a343).
7. **Generator:** R2 asked for a generator fix (d923cc86) of these template defects:
   - CTA impressions omit the occlusion and CTA `contrast_used` is false.
   - The NCCT template writes management text.
   - Echo impressions print "Abnormal values (H)" and flag a low-normal LVEF.
   - The Holter type ignores the duration.
   - Echo, ECG and Holter numbers are copied across sibling cases (found again by this audit).
   - Female reference ranges are applied to men (S03).
8. **Schema:** `Demographics` has no weight. Alteplase, tenecteplase and DOAC dosing cannot be
   stated exactly in any case (S04).
9. **`condition_tool_guidance.yaml`:** no change. Note the departures from the July answers: P04
   CTP required; RP02 MRI required; MRI recommended in M04, P01, RM02, RM03, RM04 and RP05.

## Open questions for Andrea (consolidated)

1. **NIHSS item 3 convention: one rule for the condition.** The official instruction scores
   visual extinction 1 on item 3 and carries it to item 11. R2 (S05 note 9802d420) counts it under
   item 11 only.
   - M01, M02, M03 and RP04 follow the official rule (totals 9, 9, 9, 6). S01 and S05 follow R2
     (22, 13).
   - Under R2's rule M01 to M03 become 8 and RP04 becomes 5. Under the official rule S01 becomes
     23 and S05 becomes 14.
   - No reperfusion decision changes either way. Choose one rule and the totals can be aligned.
2. **"Disabling" judgments decide IVT in low-NIHSS cases:** M04 (4), P01 (2), RP05 (4) and S06 (5)
   give IVT. RM04 withholds it for the intradural extension, which is stronger than the guideline's
   "uncertain benefit". RM01 was changed by the verifier from "give" to "do not give" because of a
   subacute pallidal infarct 2 weeks earlier ("may be harmful" within 3 months). The 2026 class of
   that recommendation needs confirming against the guideline text.
3. **IVT contraindications argued from the reviewer's reasoning:**
   - RS02: a dissected CCA 7 cm from a six-week-old arch graft; the guideline names only aortic
     arch dissection (plan open question 2).
   - RP04: an isolated aPTT of 46 s without an anticoagulant leads to "give IVT"; AHA/ASA lists an
     aPTT above 40 s, framed around heparin exposure.
   - P02: no IVT in moyamoya.
   - RS03: the fresh oesophageal anastomosis closes the perfusion limb.
4. **Mechanism and antithrombotic choices:**
   - M02 anticoagulates for a single 45-second AF episode.
   - M03 manages the ipsilateral 55-60% stenosis medically as cardioembolic.
   - M05 uses short DAPT before carotid revascularization.
   - RS02 anticoagulates rather than giving DAPT.
   - RP04 gives aspirin until APS is confirmed at 12 weeks.
   - RS04 gives low-dose aspirin rather than therapeutic LMWH in pregnancy.
   - RP03 and the other PFO cases get no statin despite LDL above 100.
   - The ELAN size category is a borderline call in M01, M03, RS03, S02 and S04. The M03 verifier
     changed it to "major".
5. **Plan departures by workers (kept):**
   - MRI is recommended rather than optional in M04, P01, RM02, RM03, RM04 and RP05.
   - RM03 echo and monitoring are optional.
   - P05 venous duplex is required rather than recommended.
   - P05 and RP03 do not accept a plain TTE for the echo criterion, while RP04 does.
6. **Stored data changed beyond a recount:**
   - M01 stenosis to "approximately 65%"; S01 left ICA stenosis 50 to 35%.
   - M02 CKD restaged to 3b.
   - P01 diplopia replaced by oscillopsia, and sodium normalised.
   - RP02 ADAMTS13 inhibitor added.
   - RP03 MRI made territorial and NCCT ASPECTS 7.
   - RS04 Foville pattern with a lesion crossing the midline.
   - S02 hemianopia changed to a quadrantanopia (approved case).
   - The audit's distinct ECG, echo and Holter numbers in M02, M03, S03 and S04.
7. **From the plan, still open:**
   - RS04 reference Miller et al. Stroke 2026 is unverified; ESO 2022 is used instead.
   - RM02 and RM03 now contain no infarct (two of 30 cases).
   - CTP results in M01, M02 and P05 were written to fail EXTEND.
   - `max_additional_actions` is 1 in all 30.
   - RP02 moved from M1 to M2, which removes thrombectomy.
8. **Unresolved data points flagged by workers:**
   - P03 TEE without abscess (consistent with the normal PR).
   - RP01 normal NCCT at 15 hours beside FLAIR-positive cerebellar infarcts, and a lateral
     medullary infarct outside the basilar territory.
   - RS05 large DWI lesion at 38 minutes.
   - S04 creatinine 1.3 at 78 without a CKD diagnosis.
   - S06 was never physician-reviewed and needs a first review.
