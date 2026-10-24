# NPH: close-out decisions (24 Oct 2026)

Andrea ruled on 24 Oct 2026: "per i punti aperti, risolvili nel modo migliore per la qualità del
dataset". NPH has no physician notes; the July 2026 tool review (Reviewer 1) and the round plan
govern. Every item below is decided and, where a change was needed, applied. Per-case detail is under
"Close-out (24 Oct 2026)" in each case log (all 30 changed, through the synonyms at least).

Sources checked on 24 Oct 2026:
- Kopp SL et al., ASRA evidence-based guidelines, fifth edition, Reg Anesth Pain Med 2025, online 29
  Jan 2025, doi 10.1136/rapm-2024-105766, PMID 39880411. Read through the Guideline Central summary
  table (https://www.guidelinecentral.com/guideline/4293939/). High-dose apixaban and rivaroxaban:
  at least 72 h before a neuraxial puncture, or check a level; first dose at least 24 h after.
  Aspirin and NSAIDs: no interruption (IC). The full text was not read.
- Douketis JD et al., ACCP perioperative antithrombotic guideline, Chest 2022;162(5):e207-e243, doi
  10.1016/j.chest.2022.07.025: suggests against heparin bridging during DOAC interruption.
- Nakajima M et al., Japanese iNPH guideline, third edition, Neurol Med Chir (Tokyo)
  2021;61(2):63-97, PMC7905302. Most of the full text was read; the last third was not.
  - Tap protocol: 30 to 50 mL, reassessment at 2 to 4 h and at about 24 h.
  - Probable iNPH needs a CSF pressure of 200 mmH2O or less.
  - DESH has a high PPV; callosal angle cut-off 90 degrees; programmable valve grade 1B.
  - Amyloid positivity does not exclude shunting.
  - **No numeric tap-test cut-off was found in the guideline.**
- Searches on the tap-test TUG threshold. The proposed criteria are 5 to 10% TUG or gait-speed
  change, or a 5-second absolute change (Kameda and Kajimoto, Front Neurol 2022, doi
  10.3389/fneur.2022.846429; Ishikawa et al., Fluids Barriers CNS 2016;13:20). No guideline fixes a
  single figure.
- The other pack references were confirmed from my own knowledge, not looked up again: Relkin 2005,
  Marmarou 2005, Halperin 2015, Tisell 2011, Massey 2013, Williams and Malm 2016, and the CPIC
  tamoxifen guideline (Goetz 2018).

## 1. Diagnosis synonyms and labels

| item | decision | change |
| --- | --- | --- |
| G91.2 (iNPH, 26 cases) granted G91.0 (scan) | Removed. In ICD-10-CM, G91.0 (communicating hydrocephalus) is the code for secondary NPH, a different entity from iNPH. G91.9 (unspecified) is kept. | `G91.2` codes `[G91.9]` |
| G91.0 (secondary NPH: M06, M08, M09, P05) granted G91.2 and the bare labels "normal pressure hydrocephalus" and "NPH" (scan) | Removed. G91.2 is the idiopathic code. With token matching, the bare labels credited the answer "idiopathic normal pressure hydrocephalus", which is the error these cases test: an antecedent excludes iNPH (Relkin 2005), and the differential lists iNPH as low. Kept: "secondary normal pressure hydrocephalus", "secondary NPH", "communicating hydrocephalus", G91.9. Added, scoped per case, labels naming the antecedent ("subdural NPH", "post-meningitic NPH", "meningitis NPH", "traumatic NPH", "TBI NPH", "SAH NPH", "haemorrhagic NPH", "subarachnoid NPH" and their "normal pressure hydrocephalus" long forms), so natural answers such as "NPH after subdural haematoma" still score. I did not add "post-traumatic hydrocephalus" or "post-meningitic hydrocephalus" without "NPH", because they would credit "hydrocephalus ex vacuo" or an obstructive answer. | `G91.0` entry plus `G91.0+subdural`, `+meningitic`, `+traumatic`, `+sah` |
| R1: G91.3 for M09 | Applied: G91.3 (post-traumatic hydrocephalus, unspecified) is accepted, scoped to M09. | `G91.0+traumatic` codes |
| R6: verbose labels P06, P07 | Applied (ruling 3: the labels were not entities; they carried reasoning and an em dash). Both labels are now "Idiopathic normal pressure hydrocephalus (iNPH)", with ICD code G91.2 unchanged. The exclusions are still stated where they belong: P06's differential and the cytology criterion; P07's PSP prohibition and the Massey 2013 key evidence. | P06, P07 `accepted[0]` |
| Copathology labels (M05, P01-P04) | Kept. "iNPH" without naming the copathology is incomplete but not wrong: the copathology is already diagnosed in the history. An answer naming only the copathology (for example "Parkinson's disease progression") contains no NPH token and does not score. | none |
| Residual | Generic labels in iNPH cases still credit a "secondary NPH" answer, and a negated "not NPH" answer still scores. Both belong to the existing scorer item (per-case rejected tokens, negation). | CENTRAL C6 |

Applied with `apply_diagnosis_synonyms.py --prune --conditions nph` (30 cases changed). `--check
--conditions nph` is clean. Spot-checked with `DiagnosisCriterion.matches`:
- M08 rejects "Idiopathic normal pressure hydrocephalus".
- M08 accepts "Normal pressure hydrocephalus following pneumococcal meningitis".
- M09 accepts G91.3 and "Post-traumatic normal pressure hydrocephalus".
- M01 no longer accepts G91.0.

## 2. Criteria pack (`dataset-generation/criteria_packs/NPH.md`)

I rewrote the pack from the plan and the summary:
- Diagnostic criteria F1 to F10.
- Work-up tiers as applied, with the literature and drug-check steps removed.
- Waste list, the two sequence constraints and the stop rule.
- Musts and fallbacks.
- Per-case ICD codes.
- A full allow-list, which covers every key cited in the 30 cases.

R2 corrections:
- `[Relkin_2005]` now gives S4-S16.
- `[Marmarou_2005]` now has its real title and S17-S28.
- The tap test is attributed to Marmarou 2005 and Nakajima 2021, and the pressure criterion to
  Relkin 2005 (70 to 245 mmH2O; the old pack said "<25 cmH2O" and cited Tisell).
- The "sensitivity ~50-80%" figure is replaced by 26 to 61% (PPV 73 to 100%), and by 50 to 100% for
  drainage.
- The old required tools (neuropsychological battery, literature) and the old tiers are superseded.

New keys:
- `[Nakajima_2021]`, `[Halperin_2015]`, `[Massey_2013]` (R2).
- `[ASRA_2025]` and `[ACCP_2022]` (see Q3).
- `[CPIC_tamoxifen_2018]` (CENTRAL 9).

Changed keys:
- `[ASRA_2018]` is marked superseded; no case cites it now.
- `[Tisell_2011]` is restricted to white matter change and shunt outcome (S09, S11). The plan's
  table entry "Tisell 2011: tap-test predictors" was wrong (auditor A3).

**Own finding: the 10% TUG attribution.** 19 cases cited `[Nakajima_2021]` for "a commonly used
10% TUG criterion". The guideline sets no numeric cut-off (see the sources above), and ruling 8
says a citation must say what it is cited for. The sentence now says the 10% figure is a commonly
used threshold that no guideline fixes. The Nakajima key stays where the sentence states the tap
protocol. Only `key_clinical_evidence` changed: no agent-visible text and no scoring changed.

## 3. Generator block (`conditions.yaml`, normal_pressure_hydrocephalus)

- Header comment: records the round's rules. There is no literature or drug-check step. The
  patient block carries no imaging or gait numbers and no referral diagnosis. Reports carry no
  verdict. The baseline report never contains post-tap values.
- MRI:
  - "Callosal angle <90 degrees (diagnostic)" is now "supportive, not diagnostic".
  - "Evans index borderline (0.3-0.32)" is now 0.31 to 0.33, with "0.30 exactly does not meet the
    criterion".
  - Added: temporal horns with MTA, DESH with both components, Fazekas grade, aqueduct and fourth
    ventricle, and the secondary-NPH and copathology puzzles.
- Labs: the "rules out ..." interpretations are removed ("glucose normal rules out diabetic
  contribution" was wrong reasoning). The panel is now targeted, with values only.
- CSF:
  - Opening pressure "5-18 cmH2O" was wrong: 5 to 18 is mmHg. It now reads 7 to 24.5 cmH2O (70 to
    245 mmH2O), or 20 cmH2O or less in the Japanese guideline.
  - "Protein normal or mildly elevated" is now normal content.
  - The tap-test lines now give figures with no verdict.
  - "False negative ~40%" is replaced by the sensitivity of 26 to 61%.
  - "Opening pressure borderline elevated (18-22)" now reads "upper end of normal" (it is within
    Relkin's limit).
  - "Mild pleocytosis" is deleted: it contradicts the normal content the diagnosis requires.
- Clinical assessment: "TUG >20 s, improves >10% after tap" put the post-tap result in the baseline
  report (plan C6). The block now separates the baseline report from the post-tap reassessment.
- Difficulty variants: the presentations no longer give the Evans index, the callosal angle or the
  tap result. The puzzle variant is now the P09 pattern (cognitive-first decline with an AD label).
- Follow-ups: `request_continuous_lumbar_drainage` is replaced by `repeat_csf_analysis` (plan C16:
  the word "lumbar" captured the index tap), with Marmarou's drainage of about 10 mL/h and 300 to
  500 mL over 72 h. Added `request_moca_cognitive_screen` and `request_post_reassessment` (plan C6).

## 4. Review-app guidance

`test_guidance_claims.py` failed two NPH claims: labs "optional all 30" (the cases have 26) and "no
specialized tests" (P09 has one). I updated four NPH responses in
`build_condition_tool_guidance.py`:
- Labs: 26 optional, 4 recommended (M04, S08, M07, M08), none required.
- Specialized test: the battery is waste in 29 cases and optional only in P09.
- Gait: required as the baseline. The post-tap reassessment is recommended in all 30 and becomes
  required with the timing discriminator. The 10% figure is described as a threshold, not a
  guideline cut-off. The old text said "P08 remains negative"; it is replaced by P08's negative tap
  followed by positive drainage.
- Advanced imaging: waste in all 30, with five authored reports in M05, P01, P02 and P04 so that
  the library never contradicts the case.

The responses that were already true (MRI, CSF) are unchanged. I regenerated the YAML with
`--write`; only the four NPH entries changed on my account. The claim table now covers labs as
(26, 4, 0), specialized tests (P09 optional only), and the post-tap reassessment recommended in
all 30. All NPH claims pass. The test still fails, but only on FTD and MG claims, which those
agents' close-outs are handling.

## 5. Open questions (summary section)

1. **Copathology referral (P01, P04, P09, M05, P02): unconditional or conditional on goals of
   care?** Keep the referral with counselling as the must.
   - A referral starts the shared surgical decision; it is not a commitment to operate.
   - Nakajima 2021: comorbidity lowers the expected benefit but does not exclude shunting, and
     amyloid positivity does not exclude the need for a shunt.
   - A "conditional" must cannot be checked better than a referral with counselling. Where goals
     of care are the real question (P04, bvFTD), the goals-of-care must already exists.
   - No change.
2. **Should the post-tap reassessment become required once R4 lands?** Yes. Reviewer 1 asked for
   gait "before and after the tap". When the timing discriminator exists:
   - the criterion takes `timing: post_intervention` and becomes required;
   - a soft constraint is added: CSF tap before the post-tap reassessment;
   - its id is added to the stop rule.
   Until then it stays recommended, because the scorer would credit it from the baseline call
   alone. Recorded in the pack (section 2) and in the guidance response; CENTRAL C2.
3. **DOAC hold: ASRA 72 h, or the 48 h some services use?** Keep 72 h, and update to ASRA 2025.
   - The fifth edition (2025) keeps at least 72 h for therapeutic apixaban and rivaroxaban before a
     neuraxial puncture, or a residual-level check if the interval is shorter.
   - The 48-hour PAUSE-style holds are perioperative protocols that were not powered for neuraxial
     procedures. A tap test uses a large-volume puncture, and P08-type drainage uses a catheter.
   - Change: the restart. The 2025 edition puts the first therapeutic dose at least 24 h after
     needle placement; the cases said 6 h (ASRA 2018).
   - No heparin bridging is now cited to ACCP 2022.
   - Applied to the musts, key evidence and prohibitions of M03, M06 and S10. The aspirin musts of
     M10, P05 and S06 move to `[ASRA_2025]` with an unchanged statement.
4. **P09 biomarker platform: name one?** No.
   - The report gives each assay's own reference limit, and the interpretation depends only on
     that limit (P09 normal, P01 A+T+).
   - Naming a commercial platform would need its exact cut-offs, which I could not verify. A wrong
     cut-off would be worse than an unnamed but internally consistent laboratory.
   - No change.
5. **Template gait numbers in six cases (M02, M10, P05, P09, S01, S02)?** Accept.
   - The values are plausible and consistent within each case.
   - Changing them means recomputing the figures in the baseline, tap, reassessment, key evidence
     and expected evidence of six cases, which risks new inconsistencies for a cosmetic gain.
   - A pattern across cases does not leak an answer. ROUND_POLICY's template rule targets
     carry-over that contradicts the case, which this is not.
   - No change.

The plan's own questions (section 6) were settled in the round and are confirmed here:
- Q4: P06 cytology stays required, as a targeted test of the alternative the case raises.
- Q5: the P07 exam has no supranuclear palsy, so the label stands (see "For the physicians").
- Q6: M09 lists ex vacuo atrophy, low.
- Q7: neuropathy red herrings were deleted where the exam has no signs.

## 6. Auditor flags and summary CENTRAL items handled here

- **Em dashes in unedited patient text** (M01-M06, P03, P04, P06): left, because ROUND_POLICY bans
  them only in new text. The two in `accepted[0]` (P06, P07) are gone with R6.
- **Citation-key style:** every NPH key is now in the pack, so `[Nakajima_2021]` is valid.
  "(Marmarou 2005)" in words became `[Marmarou_2005]` in M07-M10 and P01.
- **HIV and RPR kept in some cases, removed in others:** accept. RPR is a targeted reversible-cause
  test, and the variation is clinically defensible.
- **M05 "minimal response to today's levodopa dose":** accept, as the summary did.
- **CENTRAL 9 (CPIC key):** applied in P06. The key is on the optional criterion and in the
  duloxetine must.
- **Leak and discriminator counts in `CENTRAL_PENDING.md`:** stale. The NPH leak guard is now 0
  (60 passed). The discriminator count is 30 of 30 cases, each failing on the deliberate post-tap
  value. I did not edit that file: the orchestrator owns it.

## 7. Discriminators (PATTERNS section 5)

Every routed output and fallback in the 30 cases carries a vocabulary term, except one per case:
the post-tap follow-up's `assessment_type` "gait_and_balance_timed (post-tap reassessment)".

This value is prose by design:
- `MockServer._match_by_discriminator` serves the first follow-up whose `assessment_type` equals the
  called term.
- With the bare term, the required baseline call (`gait_and_balance_timed`) would receive the
  post-tap result before the tap, in all 30 cases.
- No data-only fix exists: the tool's `timing` parameter is free text and not routed.

**NPH is therefore not added to `DISCRIMINATOR_CONDITIONS`.** I wrote a narrow guard exemption and
then reverted it, because it changes shared test logic beyond the one-line addition the brief
allows. The exemption accepted a perform_clinical_assessment follow-up whose value is
"<term> (post-... reassessment)" when the stored baseline carries `<term>`. The orchestrator can
choose between C2 and that exemption.

## CENTRAL (not done here: vocabulary, code and shared tests)

- **C1 (R3), `analyze_csf.source` term `lumbar_drain`:** extended lumbar drainage through an
  indwelling catheter.
  - Needs the costs.yaml enum value with a price (CPT 62272 is therapeutic spinal puncture by
    catheter; verify), a fallback_library entry (normal drainage report) and the `tool_io.py`
    mirror.
  - Case NPH-P08 would then set `source: lumbar_drain` on its drainage follow-up, give the drainage
    criterion `required_arguments {"source": "lumbar_drain"}`, and add a soft constraint: tap before
    drainage.
- **C2 (R4), timing discriminator for `perform_clinical_assessment`:** make `timing` an enum
  (`baseline`, `post_intervention`) and route on it in `MockServer._DISCRIMINATOR` and
  `_answers_the_question`, or give the scorer a discriminator.
  - Cases: all 30 NPH post-tap follow-ups move to `assessment_type: gait_and_balance_timed` plus
    `timing: post_intervention`. Each criterion gains `timing`, becomes required (Q2) and gets the
    soft constraint.
  - Then add NPH to `DISCRIMINATOR_CONDITIONS`. Until then the alternative is the guard exemption
    in section 7.
- **C3 (R5), MockServer `is_repeat_call`:** count only earlier calls answered by the same
  discriminator value, so a plain-trigger follow-up cannot jump ahead after a different
  `assessment_type` was called.
- **C4 (R7), library normals:** a condition-keyed tier, or "not performed" markers, for MoCA, the
  neuropsychological battery, DaTscan and amyloid reports. Today they contradict copathology cases
  that do not store their own output.
- **C5 (R8), `perfect_agent.py`:** a realistic-context mode (varied order; contexts with "baseline",
  "before tap", "lumbar", "lp"), and `-v` should serialise with `exclude_none`.
- **C6, scorer:** per-case rejected tokens and negation (existing items). For NPH, so that iNPH
  cases can reject "secondary NPH" and secondary cases can accept a bare "NPH" without crediting
  "idiopathic NPH".

## Files changed

- Cases: all 30 NPH cases.
  - Synonyms, applied by script: all 30.
  - `accepted[0]`: P06, P07.
  - Musts, prohibitions and key evidence: M03, M06, M10, P05, P06, S06, S10.
  - `key_clinical_evidence` citation wording: 24 cases.
  - Logs appended for all 30.
- `agent-platform/config/policies/diagnosis_synonyms.yaml`: the G91 block.
- `dataset-generation/criteria_packs/NPH.md`: rewritten.
- `dataset-generation/config/conditions.yaml`: the normal_pressure_hydrocephalus block.
- Guidance files, NPH parts only: `agent-platform/scripts/review/build_condition_tool_guidance.py`,
  `agent-platform/config/review/condition_tool_guidance.yaml` and
  `agent-platform/tests/test_guidance_claims.py`.

## Checks

- `perfect_agent.py`: 30/30 pass.
- `case_io.py check` on all 30: schema and synonym guard OK, and no test failure names an NPH case.
- `test_case_guards.py -k NPH-`: 60 passed.
- `apply_diagnosis_synonyms.py --check --conditions nph`: clean.
- NPH guidance claims: pass.

## Still for Andrea or the physicians

Nothing needs information that only Andrea has. For the re-review (NPH has never been physician-
reviewed; schedule it):
- **Scoring change:** the four secondary cases no longer accept a bare "NPH" or the G91.2 code, and
  the iNPH cases no longer accept G91.0.
- **ASRA 2025 restart:** therapeutic DOACs restart 24 h after the tap (was 6 h). I read the change
  in the guideline summary, not the full text; confirm it from the full text.
- **P07:** MDS-PSP 2017 counts slow vertical saccades (O2) as a core feature. The case keeps "PSP
  not supported" because the slowing is mild, upward only, with full range and normal downward
  saccades; the MRI ratio is 0.55 and the tap response is 32%. If a reviewer reads the finding as
  O2, the case becomes iNPH with possible PSP copathology, which is a label change.
