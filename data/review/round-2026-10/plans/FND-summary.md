# FND: condition summary of the October 2026 review round

Condition auditor, 24 October 2026. Sources: the plan (`plans/FND.md`), the 30 case logs
(`logs/FND-*.md`), `CENTRAL_PENDING.md` and scripted checks over the 30 case files (M01 to M06,
M09, P01, P07, P08, RM01 to RM03, RP01 to RP03, RS01 to RS04, S01 to S07, S09 to S11). All 30
cases are `draft`. 24 cases have a worker table and a verifier section. Six have worker-only
verification (RM03, RP01, RP02, RP03, RS01, RS02); the auditor read all six in full. Each of the
30 logs now ends with a "## Condition audit" section listing the audit's edits.

This summary does not apply Andrea's FND ruling of 24 Oct 2026 (video-EEG back to optional, the
red-flag tests to recommended). Following the brief, it does not treat the plan's required tiers
as an inconsistency. The last section lists every place the close-out must change.

## Final state

- `perfect_agent.py` on all 30 ids: 30/30 pass.
- `case_io.py check` on all 30 ids: schema OK and synonym guard OK for every case. The suite has
  1 failure (`test_guidance_claims::test_every_quantified_claim_in_the_guidance_is_true`), which is
  expected until the FND guidance claims are rewritten (CENTRAL 4). No test failure names an FND
  case. 3332 tests pass.
- `test_case_guards.py -k FND`: 60 passed (leak guard, banned strings, hijacked index orders).
- Scripted uniformity checks, clean after the audit fixes:
  - tiers match plan 3.2 and section 4, or a logged and justified deviation (listed under Open
    questions);
  - the stop rule lists exactly the required criteria;
  - sequence constraints are all soft, with the plan's pairs: exam before MRI, video-EEG before
    the drug check in the taper cases, lab before imaging in P08, sodium before EEG in RM01;
  - the literature criterion is optional and last, with one `initial_tool_outputs.literature_search`
    keyed by the criterion query. There are two variants: the canonical 7-row output with the plan
    summary (22 paroxysmal cases), and the motor-only 4-row output (Espay, Daum, Nielsen 2024,
    Stone 2005) with a motor summary (M05, M09, P07, P08, RM02, RP02, S07, S10);
  - every EEG impression is the canonical "This is a NORMAL video-EEG." No EEG report says PNES,
    functional or psychogenic. Event times are not shared across cases. No impression says
    video-EEG "is required in this case" (M04, M06 and RP01 were fixed by their workers);
  - MRI reports are non-contrast everywhere except M09 (the natalizumab and JC virus question);
  - the clinical assessment output has the canonical `functional_neuro_signs` shape, with
    `criteria_met` keys from the library;
  - musts and prohibitions are canonical. P5, P6 and RESCUE appear in exactly the 22 paroxysmal
    cases. P7 (no gadolinium without indication) appears everywhere except M09. "Abruptly"
    (benzodiazepine or ASM withdrawal) appears only in M02, RP01, RP03, RS02 and S03;
  - epileptic seizures are `low` in every differential. There are no autoimmune encephalitis rows.
    Malingering appears only where the case raises it (M06, M09, S09);
  - family-history red herrings match the patient's family history;
  - the drug check's `proposed` lists match the medications;
  - the specialized-test, advanced-imaging (except P07's DaTscan), drug and literature fallbacks
    are nulled, and `metadata.fallback_tool_kinds` matches;
  - no follow-ups remain except P08's CTA;
  - none of these strings is left: `[Stone_2018]`, "Interim composition decision", "No further
    investigation is required", "itself a harm", "is a prescribing decision", NNT, "(round ruling
    5)", "ROUND_POLICY", "criteria pack", "earns no credit", or a tier word inside a label or
    rationale.
- The remaining banned-string hits are not defects:
  - em dashes in patient text written before the round (chief complaints, allergies, PMH); the
    policy bans them in new text only;
  - "the agent" in `metadata.difficulty_rationale` and `difficulty_description`;
  - "pack tiers" in `metadata.revision_reason`.

## Error classes and how each was fixed

The plan's classes A to L were applied by the workers and checked by the verifiers.

- **A. Template criteria and tiers (30).** Rebuilt per plan 3.2:
  - the exam is required in all 30;
  - video-EEG is required in the 22 paroxysmal cases (pre-ruling);
  - MRI and labs only where a named question exists;
  - drug check required in the seven taper cases (M02, RM03, RP01, RP03, RS01, RS02, S03);
  - neuropsychology and literature optional.
  Labels are short imperatives, distinct from the rationales, and the "FND criteria pack - ..."
  citation strings are gone.
- **B. Literature outputs (30).** Follow-ups were deleted, including the six that disguised
  clinical acts (ruling 4); their content became musts. One canonical
  `initial_tool_outputs.literature_search` remains per case, and the fallback is nulled.
  Misattributed titles, reused PMIDs and the invented NNT are gone. The leak guard passes.
- **C. Drug-check outputs (30).** Plans and prescribing decisions were removed. The real
  interactions are now named: benzodiazepine PRN, triptan with SSRI or SNRI, M02 cyclobenzaprine,
  RM03 desmopressin, RP02 ondansetron QT and omeprazole with iron, RS01 metoclopramide.
  Cross-modality values were removed (RS04 QTc, RM03 urine osmolality).
- **D. Shared musts and prohibitions (30).** These are now the canonical M-DX, M-COMM, M-PHYSIO,
  M-PSY, M-ASM, M-EPI and M-RESCUE, and P1 to P3 and P5 to P7, plus case-specific musts. Several
  workers added M-PHYSIO or M-PSY where the plan's own phenotype rule applies (RM01, RM03, RP03,
  RS02, S09, P07, M05).
- **E. Key evidence, red herrings, metadata (30).** Generic red herrings were rewritten from the
  case data (for example, "family history of epilepsy" where the family history says none).
  `[Stone_2018]` was removed.
- **F. Differential template (30).** Each differential now holds the alternatives the
  presentation raises, with case reasons. Template rows were dropped.
- **G. Fallbacks (30).** Stubs were nulled. Holter and CSF impressions name their findings.
- **H. Clinical assessment output (30).** Canonical shape, with signs counted against the library
  `criteria_met`. Upward drift is not counted as a functional sign (P08 now has drift without
  pronation). Midline splitting and normal walking when unobserved are supportive only. The
  no-sign impression is used where the examination shows no limb sign (M04, M06, RP01).
- **I. MRI reports.** Non-contrast except M09. Bundled MRA and spine studies were split off
  (S03, S04, RP03; S07 now has its own spine report).
- **J. EEG reports (22).** Canonical normal video-EEG with the events recorded, and no diagnostic
  label in the report. The RP01 75% diazepam reduction during monitoring was removed (plan
  fact 9).
- **K. Labs.** Values were checked and template "baseline" rows filled. The auditor rechecked the
  arithmetic in the six unverified cases.
- **L. Avoided actions.** Repeat imaging and over-investigation are marked as waste with the case
  reasons. P07 adds a DaTscan waste with a case fallback; P01 adds a repeat spine MRI.

Classes the condition audit found after the workers and verifiers, all fixed through `case_io`:

- **M. Engineering text in criteria (30 cases, 66 fields).**
  - "(round ruling 5)" and "(ROUND_POLICY ruling 5)" in 24 literature rationales;
  - "(criteria pack, optional tier)" in 6 neuropsychology rationales (M09, P01, P07, P08, RM01,
    RM02);
  - "(criteria pack section 2 ...)" in S07 and S09;
  - "earns no credit", "earns no diagnostic credit" and "without credit" in about 14 optional lab
    and MRI rationales (M01, M02, M03, M09, P08, RS03, S01 to S04, S07, S09);
  - "Optional:" opening 6 neuropsychology rationales (RM03, RP01, RP02, RP03, RS01, RS02);
  - "(optional)" ending 14 labels in M01 to M06.
  Credit wording became "does not contribute to the diagnosis", and ruling references became "no
  step of the work-up depends on it". Clinical content is unchanged.
- **N. Literature summary that names rows the output lacks (M05, RP02, S07, S10).** These four
  motor-only cases had dropped the LaFrance and Goldstein rows (RP02, S07 and S10 had also kept
  Tolchin) but kept the paroxysmal summary ("video-EEG confirmation of functional seizures ...
  psychological treatment"). They now carry the motor-only output of M09, P07, P08 and RM02. The
  leak guard passes.
- **O. MRI `protocol: standard` argument (RP03, RS02).** Dropped from the MRI criterion's
  alternative, leaving `{contrast: false}` as in the other FND MRI criteria. The plan does not set
  a protocol, and a correct order that omits the parameter would fail.
- **P. RP01 clinical text.**
  - M-COMM said "show the positive signs" in a case with no limb sign; it now says "show how the
    recorded events support it", as in M04 and M06.
  - The PMH said "Mild obesity (BMI 26.7)"; it now says "Overweight".
- **Q. RM03 sensory contradiction.** The differential and the clinical assessment finding said
  "loss of all sensory modalities" while proprioception is preserved. Both now list light touch,
  pinprick, temperature and vibration.
- **R. Empty neuropsychology `expected_evidence` (S01 to S04, RS03, RS04).** Filled with the
  wording the other batteries use.

## Counts

- Plan classes A to L: applied in all 30 cases by the workers. The worker and verifier findings
  are in the case logs.
- Condition audit: 82 field edits in 30 cases (classes M to R), all fixed, none declined.
  Flagged but not changed: 9 items (Open questions 1 to 9 below).
- Cases changed by the audit: 30 of 30 (class M touched every case).

## CENTRAL requests (consolidated)

1. **Pack** `criteria_packs/FND.md` (plan 5.1):
   - remove `[Stone_2018]` and rename `[Carson_2012]`;
   - add the keys the cases now cite: `[Daum_2014]`, `[Stone_2016]`, `[Oto_2005]`,
     `[Avbersek_2010]`, `[Kutlubaev_2018]`, `[McWhirter_2011]`, `[Chen_2005]`, `[Goldstein_2020]`,
     `[Nielsen_2015]`, `[Nielsen_2024]`, `[Stone_2005]`, `[Reuber_2002]`, `[Gelauff_2014]`, and
     `[AAN_Functional_Seizures_2025]` (Tolchin, Neurology 2026);
   - add the case-specific sources cited as free text: McGuigan 2016 PML guidance (M09), AHA/ASA
     acute stroke guideline as `[AHA_ASA_Stroke_2026]` (P08), Spasovski 2014 hyponatremia
     guideline and the desmopressin SmPC (RM03), NICE CG32 and the ondansetron SmPC (RP02), the
     metoclopramide SmPC and the EMA 2013 restriction (RS01);
   - rewrite section 6 (every R case is labelled FND) and update the counts. These counts change
     again with the ruling; see the last section.
2. **Synonyms** (`diagnosis_synonyms.yaml`, F44 group, plan 5.2):
   - the motor-only cases (M05, M09, P07, P08, RM02, RP02, S07, S10) accept the PNES labels and
     F44.5, and RM02 (diplopia) accepts "functional weakness"; scope the seizure, motor and
     sensory labels per phenotype;
   - two `accepted[0]` labels carry exclusion clauses inside a positive diagnosis: M05
     "(neuropsychiatric SLE excluded)" and P08 "celiac neurological complications excluded". Put
     them through the label review.
3. **EEG routing** (plan 5.3): EEG reports have no `eeg_type`, so a `routine` order in every
   paroxysmal case receives the stored multi-day video-EEG with its recorded events. Add an
   `eeg_type` discriminator, or a rule that serves a routine interictal normal report. This
   matters more once video-EEG is optional: an agent that orders a cheap routine EEG gets the
   video-EEG answer.
4. **Guidance claims** (`condition_tool_guidance.yaml`, `test_guidance_claims.py`, plan 5.4):
   rewrite the FND claims to the post-ruling tiers (see the last section). This is the one
   expected test failure.
5. **`conditions.yaml`** `functional_neurological_disorder` (plan 5.5):
   - move EMG and neuropsychology to `order_specialized_test`, and the spine MRI to
     `order_body_imaging spine_MRI`;
   - add video `analyze_eeg`.
6. **Banned strings** (`test_case_guards.py`, plan 5.6): add an FND row for "Stone_2018",
   "Interim composition decision", "No further investigation is required to make the diagnosis",
   "negative result is itself a harm", "agent not specified on this case's pathway", "is a
   prescribing decision, not an output of this check" and "NNT 5.7". Dataset-wide, add
   "ROUND_POLICY ruling", "(round ruling" and "criteria pack" to the rationale guard. The same
   strings are still in GBS (about 18 cases), MIG-AURA (about 7), and BACT-MEN, GLIO-HG and PD.
7. **Library** (`fallback_library.yaml`, plan 5.7):
   - add `convergence_spasm_with_miosis` and a finger-abduction finding to the
     `functional_neuro_signs` normal report;
   - the library spine MRI normal says "no intramedullary T2 lesion", which is wrong as a default
     for a patient with MS (M09);
   - P07 needed a case fallback because the library DaTscan normal does not fit a patient with
     PD.
8. **Code, high priority:** `analyze_brain_mri` has no schema default for `contrast`, unlike
   `order_ct_scan` and `order_body_imaging` (default `False`). A criterion `{contrast: false}`
   therefore fails a correct MRI order that omits the parameter. This affects 17 FND MRI criteria,
   and also ALZ-EARLY, FTD and ISCH-STR. Default `contrast` to `False`. After that, harmonize P07,
   RM02 and P08, which use `{}` as a workaround. `MRIReport` also has no `contrast_used` field
   (M01, RP03).
9. **UI** (review app, plan 5.8): show the criteria in list order with their tiers, and mark the
   optional neuropsychology criterion as optional.

## Open questions for Andrea

Deviations from the plan, logged and clinically justified, left for the physicians:

1. **S03:** the drug check is required, with a video-EEG before drug-check constraint, because the
   HPI records an empirical levetiracetam start (the plan's M02 decision). This puts S03 in the
   taper group, so the plan's counts change by one.
2. **Optional imaging added beyond the plan:**
   - spine MRI in M09;
   - brain MRI in RS03 and S09;
   - CTA and ECG in P08, both on the acute stroke pathway;
   - ECG in RM01 (risperidone and QT);
   - a repeat spine MRI waste in P01 (whose stored report was kept, against class L's null rule);
   - DaTscan waste in P07.
3. **MRI arguments:** P07 and P08 use `{}` and M09 uses `{contrast: true}`, without `protocol:
   ms`. All three work around CENTRAL 8.
4. **ECG marked as waste in the event cases:** NICE CG109 and NG217 advise a 12-lead ECG after a
   first transient loss of consciousness (S09 verifier). Decide whether to drop the ECG avoided
   action where the events were unrecorded before admission.
5. **RS01:** a normal post-event prolactin (12) on metoclopramide 30 mg/day, which usually raises
   prolactin. Plausible but unusual, and pre-existing.
6. **Template data:**
   - a "Mother with fibromyalgia ..." family history recurs in about 10 cases;
   - RM02 and RM03 have identical vitals;
   - the normal CSF and head-CT fallbacks are identical in 23 cases each.
   All are normal and plausible, but they are templates. Neither the workers nor the auditor
   changed them, since doing so would invent data.
7. **Shared source patients:** RP02 with RS01 (PMC4607000) and RP03 with RS02 (PMC9552981). All
   four are in the train split, so there is no contamination. The plan says to keep them and
   invent no divergent data (plan 6.3).
8. **M-DX in the pure-seizure cases** (M04, M06, RP01, RP03, RS02) rests on "the habitual events
   recorded on video-EEG". With video-EEG optional, should these musts say "where recorded", or
   should the physicians accept a diagnosis at the clinically established level from the
   witnessed semiology alone?
9. **Drug check required in seven cases** (M02, RM03, RP01, RP03, RS01, RS02, S03). It is a
   management act (stopping or tapering a drug started for the events) and may stay required
   under the ruling, but the physicians must see it listed.

Answered: FND stays in the dataset (plan 6.5; ruling of 24 Oct 2026, DLB deferred).

## Places the close-out must change for the FND ruling (not applied here)

1. **Video-EEG criterion to `optional`, and removed from `required_before_assessment`**, in 22
   cases:
   - M01 `action-5-analyze-eeg`, M02 `action-5`, M03 `action-5`, M04 `action-4`, M06 `action-4`;
   - P01 `action-5`;
   - RM01 `action-4`, RM03 `action-4`;
   - RP01 `action-4`, RP03 `action-5`;
   - RS01 `action-4`, RS02 `action-5`, RS03 `action-4`, RS04 `action-5`;
   - S01 `action-5`, S02 `action-5`, S03 `action-5`, S04 `action-5`, S05 `action-5`,
     S06 `action-5`, S09 `action-4`, S11 `action-4`.
2. **Red-flag tests to `recommended`, and removed from the stop rule:**
   - P08 `action-5-interpret-labs` (glucose) and `action-4-analyze-brain-mri`. The soft lab
     before MRI constraint can stay. The CT alternative stays inside the MRI criterion;
   - RM01 `action-sodium-osmolality`. Review the soft sodium before EEG constraint once both are
     non-required;
   - M09 `action-4-analyze-brain-mri`. The soft exam before MRI constraint can stay.
3. **Video-EEG before drug-check soft constraints:** M02, RP01, RP03, RS02 and S03. With an
   optional EEG and a required drug check, decide whether to drop them or keep them. A required
   act constrained to follow an optional one penalizes an agent that skips the optional act.
4. **Drug check required** in M02, RM03, RP01, RP03, RS01, RS02 and S03. It may stay, but list it
   for the physicians.
5. **Impressions saying video-EEG "is required in this case":** none remain (M04, M06 and RP01
   were fixed by their workers; checked by script).
6. **Text that states the requirement:**
   - `metadata.revision_reason`: M01, M02, M03, M04, M06 ("video-EEG required"); S05, S06, S09,
     S11 ("exam and video-EEG required"); M03 ("brain MRI recommended") is fine;
   - `metadata.difficulty_rationale` "The required work-up is the examination and the video-EEG":
     S01, S02, S04, RS03, RS04; S03 adds "and the review of the levetiracetam and lorazepam";
   - RP01 `metadata.estimated_complexity` "requires video-EEG for the diagnosis";
   - M06 `metadata.notes` "Video-EEG essential in known epilepsy patients" (keep it as clinical
     advice or soften it);
   - RP01 exam rationale: "the positive diagnostic act is the video-EEG recording, which the
     examination cannot replace";
   - M03 `red_herrings[3].correct_interpretation`: "the habitual events must be recorded on
     video-EEG";
   - M04 EEG rationale: "absence epilepsy or eyelid myoclonia must be tested";
   - RM01 sodium rationale: "a provoked seizure must be excluded with a sodium";
   - M09 `key_clinical_evidence[3]`: "why imaging is required here";
   - the 22 EEG rationales base the criterion on reaching "the ILAE documented level". As an
     optional criterion's reason this is still true, but no rationale may say the level is needed
     for the diagnosis;
   - M-DX musts that rest on "the habitual events recorded on video-EEG" (all 22 paroxysmal cases;
     see Open question 8);
   - P08 must "fingerstick glucose first, then emergency brain imaging": a management statement
     that may stay.
7. **Plan, pack and tests:**
   - plan 6.1 already gives the revert steps (EEG optional, out of the stop rule, drop the EEG
     before drug-check constraints); add the P08, RM01 and M09 changes;
   - the pack counts (CENTRAL 1);
   - the guidance claims (CENTRAL 4): video-EEG optional in 22; MRI recommended in M09, P08 and
     the 10 others; spine MRI recommended in S07; labs recommended in P08 and RM01; exam required
     in 30; drug check required in 7.
8. **After the edits:** re-run `perfect_agent.py`, `case_io.py check` and `test_case_guards -k FND`
   on the 30 ids. The stop rule must then list only the exam, plus the drug check in the seven
   taper cases.
