# FND: close-out decisions (24 October 2026)

Close-out of FND under `CLOSEOUT_BRIEF.md` and Andrea's ruling for batch 5 (`CENTRAL_PENDING.md`,
"Rulings for the batch-5 close-out", FND item). Inputs: `plans/FND.md`, `plans/FND-summary.md`
(open questions 1-9, CENTRAL 1-9). Every entry gives the decision, the reason and what changed. Per
case details are in the "Close-out (24 Oct 2026)" section of each `logs/FND-*.md`.

Sources checked on 24 Oct 2026:
- AAN 2025 functional seizures guideline (Tolchin et al., Neurology 2026;106(1):e214466), read in
  the Practical Neurology summary: obtain a detailed description of the events, with video if
  available; evaluate for co-occurring epilepsy; taper antiseizure drugs and benzodiazepines when
  there is no other indication.
- ILAE 2013 minimum requirements (LaFrance et al., Epilepsia 2013): levels of certainty possible,
  probable, clinically established (witnessed by a clinician, including on home video), documented
  (video-EEG). A diagnosis without video-EEG is valid at a lower level.
- NICE CG109 recommendation 1.1.2.2 (read on a mirror, nice.org.uk returned 403): a 12-lead ECG in
  everyone with transient loss of consciousness; NICE NG217 (suspected seizures) agrees.

## Andrea's ruling, as applied

1. **Video-EEG optional** in the 22 cases where it was required. Removed from
   `required_before_assessment`. Each rationale now ends "Without the recording, the positive signs
   and the semiology of witnessed events support the diagnosis at a lower ILAE level of certainty
   (LaFrance 2013)". Necessity wording ("only test that", "required in this case") rewritten.
2. **Red-flag tests to recommended**, out of the stop rule: P08 labs (glucose) and brain MRI, RM01
   sodium and osmolality, M09 brain MRI on natalizumab.
3. **Examination stays required** in all 30.
4. **Drug check stays required** where it is a management act, in 7 cases: M02, RP01, RP03, RS02,
   S03 (taper of an antiseizure drug started for the events), RM03 (desmopressin with water loading
   and hyponatremia), RS01 (regular metoclopramide confounding the movements, QT with low
   magnesium). Listed for the physicians below.
5. **Impressions.** No stored report still says video-EEG "is required in this case". The same
   claim was removed from M-DX and COMM musts, red-herring interpretations, `difficulty_rationale`,
   `difficulty_description`, `estimated_complexity` (RP01), notes (M06, S05) and `revision_reason`.
6. **Constraints naming demoted tests.** Dropped: video-EEG before drug check (M02, RP01, RP03,
   RS02, S03) and sodium before video-EEG (RM01). Kept, because they order two acts that are still
   taken in the right order: examination before MRI (11 cases), examination before spine MRI (S07),
   labs before MRI (P08).
7. **Pack and guidance claims** updated to the new tiers (below).

Resulting tiers: required = examination (30) plus drug check (7). Brain MRI recommended 12,
optional 9; labs recommended 8, optional 4; spine MRI recommended 1 (S07); video-EEG optional 22;
ECG optional 10; neuropsychology and literature optional 30; EMG/NCS and SSEP waste 30.

## Open questions of the summary

**Q1. S03 drug check.** Kept required: the HPI records an empirical levetiracetam start, so the
taper is a management act (AAN 2025). Its video-EEG constraint was dropped with the ruling. The M-ASM
taper must in the five taper cases now reads "once the events are securely diagnosed as functional
(ideally with a habitual event documented on video-EEG) and there is no evidence of epilepsy".

**Q2. Optional imaging beyond the plan.** Kept (spine MRI in M09, brain MRI in RS03 and S09, CTA
and ECG in P08, ECG in RM01, repeat spine MRI waste in P01, DaTscan waste in P07). Each has a case
reason; optional items cost the agent nothing. P01's stored repeat-MRI report is kept: it matches
the documented prior study.

**Q3. MRI arguments `{}` and `{contrast: true}`.** Kept. They work around the missing `contrast`
default (CENTRAL below); harmonise after that code fix.

**Q4. ECG as waste in the event cases.** Changed. The ECG avoided action was replaced by an optional
`action-ecg` criterion ([NICE_CG109], [NICE_NG217], expected "Sinus rhythm with normal conduction
and QT interval") in the 8 cases with apparent unresponsiveness: M01, M02, M04, S01, S05, S06,
S09, S11. ECG stays waste in M05, M06, M09, P07, S02, S03, S04, S07, S10 (motor-only presentations,
or events with preserved awareness or a known cause).

**Q5. RS01 prolactin.** Changed. The post-event prolactin goes from 12 to 64 ng/mL (H), with the
note "Metoclopramide raises prolactin, so a post-event level cannot be interpreted on this drug"
and the abnormal-values summary updated. A normal level on 30 mg/day was the implausible part;
the raised level is a red herring that the agent must explain by the drug.

**Q6. Template data.** Kept: the fibromyalgia family history (13 cases), identical RM02/RM03
vitals and identical normal fallbacks. All are plausible and changing them would invent data.

**Q7. Shared source patients** (RP02 with RS01, RP03 with RS02). Kept; all four are in the train
split, so there is no leak into the test split.

**Q8. M-DX in the pure-seizure cases.** Changed to rest on the signs and the event semiology: "the
semiology of the habitual events, confirmed on video-EEG where recorded" (regex in most cases,
written by hand in M04, M06, RP01, RP03, RS02, RS04). The diagnosis is accepted at the clinically
established level without the recording.

**Q9. Drug check required in 7 cases.** Kept under the ruling, listed below.

Differential `key_features` that cite the video-EEG are kept: the differential is unscored and
describes the whole case (ROUND_POLICY 7).

## Labels, codes and synonyms

Labels (codes unchanged, exclusion clauses removed from positive diagnoses):
- M05: "Functional neurological disorder with right-sided functional weakness and sensory loss, in
  quiescent systemic lupus erythematosus".
- P08: "Functional neurological disorder with functional left arm weakness and hemisensory loss, in
  type 1 diabetes and celiac disease".
- M09: "Functional neurological disorder with functional right leg weakness, coexisting with stable
  relapsing-remitting multiple sclerosis".

No recodes. RP03 and RS02 are mixed (weakness plus seizures), so F44.7 is right.

Synonyms (`diagnosis_synonyms.yaml`), applied with `--prune --conditions
functional_neurological_disorder`, `--check` clean over the 600 cases:
- `F44` is generic: functional neurological disorder, functional neurological symptom disorder,
  conversion disorder, FND; code F44.9. Kept in all 30 cases.
- `F44+seizures` (all FND except the 8 motor-only cases M05, M09, P07, P08, RM02, RP02, S07, S10):
  PNES, psychogenic non-epileptic and nonepileptic seizures, functional seizures, dissociative
  seizures, nonepileptic seizures; code F44.5. "non-epileptic seizures" is deliberately left out:
  its tokens are all contained in "focal non-motor epileptic seizures".
- `F44+motor` (all FND except M04, M06, RP01, RM02): functional weakness, functional limb weakness,
  functional motor disorder; codes F44.4, F44.6, F44.7. RM02 no longer accepts "functional
  weakness".
- `F44+movement` (11 cases with functional movements): functional movement disorder, functional
  tremor.
- `F44+diplopia` (RM02): functional diplopia, functional convergence spasm, functional eye
  movement disorder; codes F44.4, F44.6.
- The global `F44.5` entry gets `except_cases: [FND-M04, FND-M06, FND-RP01]` so it does not
  duplicate the scoped entry.

## Pack, generator, guidance and guards

- `criteria_packs/FND.md` rewritten: codes and phenotype scoping, the work-up hierarchy with the
  counts above, waste, prohibitions, soft constraints, R series described as record-derived, red
  herrings, musts. The allow-list covers every key the cases cite; Stone_2018 and Carson_2012 are
  marked superseded; the free-text sources (McGuigan 2016, Spasovski 2014, NICE CG32, the SmPCs,
  EMA 2013 metoclopramide) are listed.
- `conditions.yaml` FND block: interim comment replaced; prolactin "NOT elevated" and "all
  screening labs normal" removed; video-EEG results no longer in the straightforward presentation;
  EMG/NCS and psychiatric evaluation removed from follow-ups, spine MRI under `order_body_imaging`,
  neuropsychology under `order_specialized_test`, video-EEG described as optional.
- `build_condition_tool_guidance.py` FND response rewritten; YAML regenerated (only the FND line
  changed). `test_guidance_claims.py` FND claims rewritten to the tiers above; all FND claims pass.
- `test_case_guards.py`: FND added to `DISCRIMINATOR_CONDITIONS` (outputs were already clean).

Checks: `perfect_agent.py` 30/30; `test_case_guards -k FND-` 90 passed; full suite passes except
the guidance-claims test, whose failures are FEPI-TEMP, MS-RR and PD claims (their close-outs).

## For the physicians

- Drug check required in M02, RM03, RP01, RP03, RS01, RS02, S03 (management acts, item 4).
- M04 (absence mimic), M06 (known epilepsy) and the taper cases: with video-EEG optional, an agent
  can diagnose and taper without documenting a habitual event. The taper must is conditioned on a
  secure diagnosis; the physicians should confirm that the clinically established level is enough
  here, or ask for video-EEG to be recommended in these cases.
- S05 (eyes open during events): semiology alone is weaker; same question.
- P08: brain MRI and glucose are now only recommended in an acute hemiparesis, per the ruling.
  Confirm the stroke pathway is acceptable at that tier.

## Still for Andrea

Nothing blocking.

## CENTRAL (vocabulary, code, shared tests; not edited here)

1. **EEG routing:** EEG reports have no `eeg_type`, so a `routine` order receives the stored
   multi-day video-EEG with its events. Add the discriminator or serve a routine interictal normal
   report. More urgent now that video-EEG is optional.
2. **`analyze_brain_mri` `contrast` default `False`** (as in `order_ct_scan`, `order_body_imaging`),
   and a `contrast_used` field on `MRIReport` (M01, RP03). Then harmonise P07, P08, RM02, M09.
3. **Banned strings:** FND row in `test_case_guards.py` for "Stone_2018", "Interim composition
   decision", "No further investigation is required to make the diagnosis", "negative result is
   itself a harm", "agent not specified on this case's pathway", "is a prescribing decision, not an
   output of this check", "NNT 5.7"; dataset-wide "ROUND_POLICY ruling", "(round ruling", "criteria
   pack".
4. **Library** (`fallback_library.yaml`): add `convergence_spasm_with_miosis` and a finger-abduction
   finding to the `functional_neuro_signs` normal; the spine-MRI normal ("no intramedullary T2
   lesion") is wrong for an MS patient; the DaTscan normal is wrong for PD.
5. **UI:** show criteria in list order with tiers; mark optional criteria as optional.
6. **Scorer negation:** label tokens match a negated answer ("not functional seizures" matches
   "functional seizures").
7. **Global `F44.5` entry** still gives "non-epileptic seizures" plus F44.4 and F44.7 to the SE and
   FEPI-TEMP F44.5 mimic cases. The tokens of "non-epileptic seizures" match epileptic answers
   containing "non" (e.g. "focal non-motor epileptic seizures"). For their close-outs.
8. **`CENTRAL_PENDING.md`:** mark the FND items done (orchestrator).
