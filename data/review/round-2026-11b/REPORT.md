# Round 2026-11b: the last physician notes of 21-22 November 2026

Follow-up to round 2026-11, same rules (`round-2026-10/ROUND_POLICY.md`). Input: the 94 items in
`~/review-round-2026-11b/input/new_notes.jsonl` (VPS snapshot 2026-11-25T10:39Z): 40 from the
re-check set `recheck-2026-11` (R2 on ten cases, R1 on three, plus approvals) and 54 from R1's full
review of ISCH-STR (`neurobench` set, version 88bd8dc0, targets found by content).
Base: master 332e52d9, cases hash `58c1d905...c122`. Branch `fix/review-round-2026-11b`.

## Counts

| Status | Items | |
|---|---|---|
| FIXED | 68 | R1 54, R2 14 |
| NO-ACTION | 17 | 7 R1 all-dimension approvals with no comment; 10 R2 verdicts that summarise their own notes |
| CENTRAL | 6 | stop-rule display (MG-S03, SAH-M01, SYNC-CARD-M02), "first order" MRI label (ALS-P05, MS-RR-RS05), duplicated tool names in the stop box (ALS-P05) |
| NEEDS-ANDREA | 2 | ISCH-STR-RM02, ISCH-STR-RM03 condition assignment |
| DECLINED | 1 | ISCH-STR-P01 6fc4ce59: P01 already gives clopidogrel alone (aspirin allergy); the note repeats M05 word for word |

76 case files changed (ISCH-STR 30, SAH 23, NMDAR-ENC 11, GLIO-HG 5, BACT-MEN, GBS, HEP-ENC,
MIG-AURA, MS-RR, SE and SYNC-CARD 1 each) plus `diagnosis_synonyms.yaml`. Every ruling is in
`ledger.jsonl` (built by `bin/compile_ledger.py` from `rulings/`, November schema, `round: "2026-11b"`).
`round-2026-11/bin/new_notes_since.py` now reads every follow-up ledger; on the snapshot it
reports 0 unruled items for both `neurobench` and `recheck-2026-11`.

## Classes and the cases each touched

Re-check (block A):

- **SAH BP must (R2 37cb9bf7, ESO 2026).** "Lower blood pressure now ... [Connolly_2012]" replaced
  by R2's text (analgesia and nimodipine first; if SBP stays above 160-180, gradual lowering to
  about 160 by infusion, MAP fall at most 10% in 2 h) in **23** SAH cases; S08 (cocaine) keeps its own.
- **NMDAR continuous EEG (R2 a0365786).** cEEG made required and put in the stop rule in **11**
  cases whose differential or key evidence cites a finding only the cEEG returns (P01, M03, M04,
  M05, P05, P06, P07, P08, RM02, RP02, RP03). The other 18 keep it recommended (the must is
  conditional and nothing in their ground truth depends on it).
- **GLIO-HG IDH wording (R2 8b4554c6).** R2's EANO 2021 sentence in **5** cases over 55 with an
  IHC-only tissue criterion (S05, S01, S02, S06, RP01). Their pathology reports still carry an
  "IDH1/2 sequencing" row as a reflex result; not changed (see open items).
- **Clinical reorder of drug checks** (ruling 1, second half): BACT-MEN-M03 (after blood cultures),
  GLIO-HG-S05 (before dexamethasone), HEP-ENC-P05 (before the drugs).
- Single-case fixes: GBS-RM12 FVC 52% predicted; SE-M07 GCS 10 (E3V3M4) and relabel; HEP-ENC-P05
  E51.2; SYNC-CARD-M02 I45.2; BACT-MEN-M03 10-14 days (WHO 2025, ESCMID 2016); MIG-AURA-P06 MRI
  required and triptan wording; MS-RR-RS05 McDonald 2024 wording (no other MS-RR case had it).

ISCH-STR (block B, all 30 cases checked):

- **STOP-SCOPE (ruling 3):** 22 cases. Drug checks, TTE, rhythm monitoring moved to recommended
  and out of the stop rule. Kept required, outside the stop rule, where the diagnosis names what the
  test establishes: M01/M02/M03 monitoring (paroxysmal AF found on monitoring, ECG in sinus), P03
  cultures/TTE/TEE, P05 venous duplex and bubble echo, RP03 bubble echo, RP04 antiphospholipid
  panel, RP05 NOTCH3. NCCT, CTA, admission bloods and ECG stay required in the stop rule (the
  benchmark has no clock between actions; "do not delay IVT" is in the IVT must, class NOWAIT).
  Exceptions on R1's or R2's own words: RM02 NCCT and RM03 ECG/troponin left the stop rule; RP02
  first imaging is CT or MRI and its TTP screen is required in the stop rule (R2).
- **WAKE-UP (ruling 4):** M01, M02, M03, P05. The perfusion criterion became "CT perfusion or MRI
  DWI-FLAIR" (either), required and in the stop rule. P04 already had CTP required.
- **NIHSS-ITEM3 (ruling 5, October open question 1 closed):** M01, M02, M03 (9→8), RP04 (6→5),
  S01 (23→22), S05 (14→13). The dataset grep found extinction elsewhere only in two ALZ-EARLY exams
  without an NIHSS. No reperfusion decision changed by the recount.
- **SWALLOW (ruling 6):** must added in 24 cases (aspiration precautions in the 10 with dysarthria,
  and P04); M04 (airway and secretions, R1 77aaa422), RP01, RP03, RS03 already had one; RM02/RM03
  not added (no neurological deficit).
- **LDL (ruling 7):** target removed in 5 non-atherosclerotic cases (P01, P05, RM01, RM04, RP03).
- **NOWAIT (R1 M04 e8e19d93, RP05, RS01):** 14 cases (P02 included) that give IVT state it starts without
  waiting for CTA, ECG, troponin or labs other than glucose unless coagulopathy or anticoagulant
  exposure is suspected.
- **IVT decisions (ruling 8; October open questions 2-3 closed by R1):** P02 moyamoya: give after
  individualised assessment, prohibition removed; RM01 prior infarct: individualised, prohibition
  removed; RM04 intradural V4: individualised, withholding defensible; RP04 aPTT 46 s: do not give
  (and the BP, aspirin and post-IVT musts, report and key evidence aligned); RM02 apixaban:
  individualised, normal INR does not exclude activity. RS02 (arch graft) and RS03 were not raised
  by R1 and are unchanged.
- Single-case: M03 FLAIR wording, M05 SAPT default, P02 RNF213, P03 empirical antibiotics, P04
  perfusion volumes (CT and MR follow-ups), RP01 07:00 imaging, RP02 CTA alternative (new CTA
  follow-up), plasma exchange and hydrochlorothiazide, RP03 PFO wording and aspirin timing, RS01
  CHA2DS2-VASc 6.

## NEEDS-ANDREA: ISCH-STR-RM02 and RM03 (dissection without infarct)

R1 (b4fff16d, 235983da) says both are isolated cervical ICA dissections without infarct or TIA
filed under ischaemic stroke, and asks to reassign or replace them. Not changed (ruling 9). Options:

1. **Keep with a note** (condition ISCH-STR, a "cerebrovascular, no infarct" variant). Cheapest;
   the label already says "without completed infarct", but per-condition accuracy then mixes two
   entities and R1 may block approval.
2. **Exclude from the splits** (mark them out in `split_manifest.json`, like the 2 already
   excluded). Keeps the files for a later dissection condition; ISCH-STR drops to 28 scored cases.
3. **Rewrite as TIA or minor stroke** (a small DWI lesion or a transient deficit), so the label
   becomes "ischaemic stroke/TIA secondary to ICA dissection". Fits the condition, but it is a new
   case content that needs a new physician review of both cases.

**Recommendation: option 2 now**, option 3 later if the dataset needs 30 ISCH-STR cases. Excluding
keeps the condition clean without inventing data the physicians have not seen, and costs one
manifest change and a split re-count. Their other notes were applied "as retained" (RM02 NCCT out
of the stop rule, RM03 ECG and troponin out, apixaban wording), which is harmless under any option.

## CENTRAL

1. **Review app (Mac session):** stop-rule box wording ("further unjustified actions allowed: N";
   recommended and optional criteria never count, `policy_reward.py`), criterion labels instead of
   tool names in that box (ALS-P05 "interpret_labs / interpret_labs", R1's CT-vs-CTA requests in
   M02, M05, P01, P02), and the "First order of this tool" MRI label (ALS-P05, MS-RR-RS05:
   `perfect_agent.py -v` shows the contrast order served by `request_contrast_mri`).
2. **`test_guidance_claims.py` fails** (maintained centrally per `case_io.py`): the review-app
   guidance counts are now nmdar cEEG recommended 18 (was 29); stroke MRI optional/recommended/
   required 23/6/5 (was 23/6/1), CT perfusion recommended/required 0/5 (was 4/1); mig MRI
   recommended 7 (was 8) and MIG-AURA-P06 joins the required exceptions. Update
   `condition_tool_guidance.yaml` counts.
3. **SE-M07 label change** (reviewer ruled the label wrong): accepted[0] is now "Post-anoxic
   myoclonic status epilepticus (ILAE 2015 A.2) ..."; new scoped synonym entry
   `G41.8+postanoxic_myoclonic`, NCSE labels no longer granted to SE-M07 (applied with `--prune`).
   New code-only entries `K72.90+wernicke` (E51.2) and `I44.1+bifascicular` (I45.2).
4. **Criteria packs:** add `[ESO_2026]` (ESO SAH guideline) to the SAH pack allow-list; add the
   AHA/ASA 2026 rulings closed here (moyamoya, prior infarct, intradural dissection, aPTT > 40 s,
   DOAC within 48 h, NIHSS item 3) to the ISCH-STR pack.
5. **Policy-verdict ids collide across review sets** (`<code[:6]>:<case>:policy_verdict` is the
   same in `neurobench` and `recheck-2026-11`): `new_notes_since.py` now keeps every ruled digest
   per id; anything joining ledgers by `note_id` must also key on the round.
6. **Environment:** the worktree venv has no `torch`, so `test_grpo_rollout.py` cannot be
   collected (6587 passed, 1 failed as above, 1 collection error).

## Open items (not ruled by any note)

- ISCH-STR-P05: the diagnosis names heterozygous factor V Leiden, but the thrombophilia criterion
  is recommended; by ruling 3's logic it should be required (outside the stop rule).
- Pre-existing perfect-agent warnings (not introduced here): ISCH-STR-RP04 echo alternative
  `bubble_study` and SYNC-CARD-RM03 `coronary_CTA` are answered by a fallback.
- GLIO-HG S01, S05, RP01: the tissue reports carry an "IDH1/2 sequencing" row that no criterion
  orders (a result the agent did not ask for).
- RP04: the published seed case was thrombolysed; the case now withholds IVT (aPTT 46 s) as R1
  rules. The metadata keeps the seed history.

## Checks

- `perfect_agent.py --all`: 600/600 pass (two pre-existing warnings above).
- `apply_diagnosis_synonyms.py --check`: 0 of 600 would change.
- Full pytest: 6587 passed, 2 skipped; 1 failure (`test_guidance_claims`, CENTRAL 2), 1 collection
  error (no torch, CENTRAL 6).
- Final cases hash: `334fad07fd522f9bf655789b7ffc9b83bb427dd477c4d2cfb6321e039968e7f2`.
