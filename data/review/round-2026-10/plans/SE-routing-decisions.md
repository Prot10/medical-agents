# SE: EEG and labs after the MockServer routing change (25 October 2026)

Commit 317e46db routes `analyze_eeg` by `eeg_type` (an omitted `eeg_type` is `routine`) and serves an
`interpret_labs` order only the stored panels that answer the assays it names (`tools/lab_matching.py`).
Two consequences for the 30 SE cases, decided here per Andrea's 24 Oct 2026 rule (best for dataset quality).
Every case log has a "## EEG and labs after routing (25 Oct 2026)" section.

## 1. Routine EEG

Problem: every SE case stores its EEG as a `continuous_icu` recording (P02: `video`). A routine order
received the library's normal routine EEG, which a 20 to 40 minute recording during ongoing status, or
in its immediate aftermath, would not show.

Decision: each case stores a routine EEG in `fallback_tool_outputs.eeg` with `eeg_type` `routine`. Why the
fallback tier: the initial slot holds the index cEEG, which must keep answering the cEEG order; a follow-up
would appear in the review app as a pathway step and imply a scored action; a routine EEG is an off-pathway
order, which is what the case fallback answers (the ALS cases already store routine EEG fallbacks). The
routed fallback answers only a routine order (exact term), so `continuous_icu` and `video` orders still get
the stored recording, and the P01 benzodiazepine-trial and P03 sedation-wean follow-ups still answer the
repeat cEEG order. No criterion, no tier change, no change to the reward-relevant policy.

Content rule: the report is what a routine EEG placed when the cEEG was started would record, so it is the
stored cEEG cut to 30 minutes: same patterns, laterality and treatment state (prehospital benzodiazepines,
P03 propofol, P08 levetiracetam load), seizure counts scaled to 30 minutes from the stored rates, events
described by the technologist (no video), activation procedures not performed in an obtunded patient. The
impression calls electrographic status epilepticus only where the 30 minutes meet ACNS 2021 on their own
(10 continuous minutes, or at least 12 minutes of seizures, 20 percent of any hour); S02, S07, S09, S11, S12, P05 and P06 report
the seizures without the label, and P05 says the recording cannot measure an hour's burden. Report style per
TOOL_REPORT_STYLE_GUIDE (no diagnosis names, no management, empty `recommended_actions`).

| case | routine EEG at that point |
|---|---|
| SE-M01 | continuous left temporal evolving rhythmic delta with sharp waves for the whole 30 minutes (electrographic SE), diffuse slowing |
| SE-M02 | five right temporal-parietal seizures of 2-4 minutes in 30 minutes (about half the record, electrographic SE), right temporal LPDs between them |
| SE-M03 | left temporal evolving rhythmic delta over most of the record (electrographic SE), left temporal LPDs in the gaps, posterior slowing |
| SE-M04 | continuous left temporal-parietal evolving discharge (electrographic SE), intermittent triphasic GPDs, left hemisphere attenuation |
| SE-M05 | recurrent right temporal seizures with intervals under 2 minutes (electrographic SE), extreme delta brush, dyskinesias without EEG correlate |
| SE-M06 | continuous right temporal evolving sharp waves for 30 minutes with automatisms (focal electrographic SE), right hemisphere attenuation |
| SE-M07 | continuous generalized 2.5-3.5 Hz spike-and-wave and polyspike-and-wave (+F) with myoclonus, reactive slow background |
| SE-M08 | recurrent left temporal-parietal seizures over more than half the record (focal NCSE), LPDs, left hemisphere slowing |
| SE-M09 | recurrent right temporal-parietal seizures over most of the record (focal NCSE), LPDs, right hemisphere suppression with diffuse slowing |
| SE-P01 | quasi-continuous right temporal-occipital LPDs+F without definite evolution (ictal-interictal continuum), no benzodiazepine trial |
| SE-P02 | NORMAL: reactive 9-10 Hz posterior rhythm persisting through one 7-minute technologist-observed event, no epileptiform discharges |
| SE-P03 | burst-suppression with near-identical left-predominant epileptiform bursts, right arm and face myoclonus with bursts, no reactivity, on propofol |
| SE-P04 | left hemispheric LPDs+F without evolution, left delta, three right arm episodes without EEG correlate, no seizures |
| SE-P05 | five bifrontal-onset seizures in 30 minutes (about 7 minutes), fasciculation artifact without correlate, low-voltage background |
| SE-P06 | continuous generalized triphasic periodic sharp wave complexes with seven superimposed left temporal seizures of 15-30 s |
| SE-P07 | triphasic GPDs attenuating with stimulation and intermittent left temporal 3-4 Hz runs without evolution, no unequivocal seizure |
| SE-P08 | continuous generalized 2-3 Hz spike-and-wave and polyspike-and-wave without interictal background (electrographic SE) during the levetiracetam load |
| SE-RS11 | 8 minutes of post-ictal suppression, then reactive diffuse slowing with five interictal generalized polyspike-wave bursts, no seizures |
| SE-S01 | continuous generalized spike-and-wave evolving to polyspike-and-wave during convulsions (electroclinical SE), artifact-obscured |
| SE-S02 | six right temporal-onset seizures with bilateral spread in 30 minutes, LRDA+S between them, after IM midazolam |
| SE-S03 | continuous right-hemisphere-predominant evolving discharges with bilateral spread during convulsions (electrographic SE), right delta |
| SE-S04 | continuous generalized 2-4 Hz polyspike-and-wave decelerating from 3 to 2 Hz during convulsions (electrographic SE) |
| SE-S05 | continuous generalized 2-3 Hz spike-and-wave during convulsions (electrographic SE), excess beta after IM midazolam |
| SE-S06 | continuous generalized 2-4 Hz spike-and-wave during convulsions (electrographic SE), excess beta, heavy artifact |
| SE-S07 | two right frontal-onset seizures evolving to generalized 3 Hz spike-and-wave in 30 minutes without return to background, right frontal LPDs and delta |
| SE-S08 | diffuse posterior-predominant 2-3 Hz delta, reactive, no epileptiform discharges or seizures in 30 minutes |
| SE-S09 | one left temporal seizure with bilateral spread 10 minutes in, then left temporal LPDs, left temporal delta |
| SE-S10 | continuous generalized spike-and-wave (+F) for the first 20 minutes (electrographic SE), then diffuse slowing without seizures |
| SE-S11 | two generalized seizures in 30 minutes without return to background, triphasic GPDs between them, myoclonus not time-locked |
| SE-S12 | about 24 brief left temporal 8-10 Hz runs with attenuation, each with right face and arm dystonic posturing; left temporal slowing |

Own finding fixed in passing: SE-M08 cEEG `limitations` said "Left scalp laceration"; the HPI and exam put it
over the right temporal scalp (now "Right temporal scalp laceration").

Guard: `test_case_guards.py` section 5, `test_continuous_eeg_case_answers_a_routine_order`: a case that stores a
`continuous_icu` EEG must also store a routine EEG (initial, follow-up or fallback). It passes on all 600
cases (only SE stores `continuous_icu` without a routine recording before this change; NMDAR-ENC stores a
routine index). Video-only cases (FND, FEPI-TEMP) are not covered: there a normal or interictal routine
recording is plausible and is their condition's decision.

## 2. Lab criteria whose evidence cites results their order no longer returns

Rule applied (from the brief): if the result is the criterion's point, or a must, the key evidence or the
differential relies on it as coming from this order, the order must return it: extend the order when the
assay belongs in the same emergency draw, else move the row to the panel the order already returns. If it
is incidental (post-ictal lactate and CK, inflammatory markers in a metabolic screen, cardiac markers after an
arrest, HbA1c in known diabetes, second-tier lupus serology), trim it from `expected_evidence`; the stored
value stays and answers its own order. A must that only says "recheck CK" or "no antibiotics without a
source" does not rely on the baseline value.

| case | criterion | unserved result cited | decision | scoring change |
|---|---|---|---|---|
| SE-M01 | action-2-interpret-labs | venous lactate 2.6 (panel Lactate) | TRIM: post-ictal marker, incidental | no |
| SE-M02 | action-2-interpret-labs | lactate 3.8, CK 480 (Other), CRP 4.2 (Inflammatory Markers) | TRIM: post-convulsive markers and a normal-range CRP, incidental (the differential and red herrings explain them, no must uses them) | no |
| SE-M03 | action-2-interpret-labs | dsDNA 42, C3 62, C4 8, ESR 68 (Rheumatology Panel) | TRIM: lupus serology is a second-tier test answered by its own order (anti_dsDNA, complement); the flare is in the history and the nephritis is shown by the served urinalysis and protein:creatinine ratio, which stay | no |
| SE-M04 | action-2-interpret-labs | lactate 3.6, CK 580 (Other), procalcitonin 0.18 (Inflammatory Markers) | TRIM: incidental post-convulsive markers and a negative infection marker; the served urinalysis stays | no |
| SE-M04 | action-6-interpret-labs | none (the probe's sodium 123 is a core-labs value the evidence does not cite) | NO CHANGE | no |
| SE-M05 | action-2-interpret-labs | CRP 28.4, ESR 72, procalcitonin 0.8 (Infectious and Inflammatory), lactate 2.4 (Other) | TRIM: inflammatory markers are not the point of the metabolic and toxic screen; fever alone justifies the cultures criterion; the values stay available to a CRP or procalcitonin order | no |
| SE-M06 | action-2-interpret-labs | CRP 42.6, ESR 86, procalcitonin 0.6 (Inflammatory Markers) | TRIM: as M05; the cultures criterion rests on fever and leukocytosis | no |
| SE-M07 | action-2-interpret-labs | troponin I 0.24, BNP 486 (Cardiac), lactate 2.6 (Lactate) | TRIM: post-arrest cardiac markers and a post-ictal lactate, incidental (red herring only, no must) | no |
| SE-M08 | action-2-interpret-labs | lactate 2.4 (Lactate), INR 1.0 (Coagulation, not ordered) | TRIM: incidental | no |
| SE-P01 | action-3-interpret-labs | thiamine 42 (Thiamine) | EXTEND with thiamine_B1: the key clinical evidence, differential and a prohibition rely on the level (treatment doses, not 100 mg daily), and EFNS 2010 draws thiamine before giving it in a heavy drinker with encephalopathy | yes |
| SE-P03 | action-2-interpret-labs | troponin I 12.8, BNP 2840 (Cardiac markers), lactate 2.6 (Arterial blood gas and lactate) | TRIM: post-arrest markers, incidental to the seizure work-up | no |
| SE-P04 | action-2-interpret-labs | HbA1c 8.4 (Admission bloods) | TRIM: known diabetes, incidental | no |
| SE-P05 | action-2-interpret-labs | CK 8640 (Muscle and Cardiac Enzymes) | EXTEND with CK: a must treats the rhabdomyolysis with acute kidney injury on this value; CK belongs in the emergency draw after prolonged convulsions and fasciculations | yes |
| SE-P06 | action-2-interpret-labs | venous lactate 3.4, CK 412 (Post-ictal markers) | TRIM: post-ictal markers, incidental | no |
| SE-P08 | action-2-interpret-labs | osmolal gap 4 with measured osmolality 296 (Serum Osmolality), CK 1840 (Muscle Enzymes) | EXTEND with serum_osmolality: the rationale, differential and red herring use the normal osmolal gap to exclude a toxic alcohol in a high anion gap acidosis of unknown cause, part of the same emergency toxicology draw. TRIM CK 1840: the rhabdomyolysis must is a repeat-and-monitor instruction that stands without the baseline value | yes |
| SE-RS11 | action-2-interpret-labs | venous lactate 8.2, CK 1840, troponin I 0.06 (Post-ictal markers); alcohol and drug screen (Toxicology, not ordered) | EXTEND with CK: a must treats rhabdomyolysis on CK 1840; the CK order returns the whole stored Post-ictal markers panel, so lactate and troponin stay in the evidence. TRIM the toxicology clause: the criterion does not require a toxicology screen (rationale: reasonable, not required) | yes |
| SE-S01 | action-2-interpret-labs | lactate 8.4, CK 468 (Other), CRP and procalcitonin (Inflammatory markers) | MOVE lactate into the served Arterial blood gas panel (blood gas analysers report it; the library ABG lists it), because a prohibition cites it; TRIM CK 468 (the must only rechecks CK) and CRP and procalcitonin (incidental; the no-antibiotics must stands on the absent source) | no |
| SE-S02 | action-2-interpret-labs | lactate 6.2, CK 312 (Other), CRP and procalcitonin (Inflammatory markers) | TRIM: incidental; served bicarbonate 19 kept; no served blood gas panel to hold the lactate | no |
| SE-S03 | action-2-interpret-labs | lactate 7.8 (Other), CRP 96, procalcitonin 1.8 (Inflammatory markers), serum osmolality 262 (Osmolality) | MOVE lactate into the served Arterial blood gas panel (a must cites it for holding metformin); TRIM CRP and procalcitonin (the served pyuria and nitrite carry the urinary source) and serum osmolality (the served sodium and urine studies carry the hyponatremia) | no |
| SE-S04 | action-2-interpret-labs | lactate 8.8, CK 410 (Other), dsDNA 142, C3 48, C4 6 (SLE markers), procalcitonin (Inflammatory markers) | MOVE lactate into the served Arterial blood gas panel (consistent with S01 and S03); TRIM the lupus serology (second-tier, answered by anti_dsDNA or complement; the flare is in the history) and procalcitonin | no |
| SE-S05 | action-2-interpret-labs | thiamine 22, lactate 9.2 (Other), phosphate 1.6 (Phosphate) | EXTEND with thiamine_B1 and phosphate: thiamine deficiency is part of the labelled diagnosis and a must replaces phosphate 1.6; both belong in the admission draw of a malnourished heavy drinker. The thiamine order also returns the lactate stored beside it | yes |
| SE-S06 | action-2-interpret-labs | CK 8640, lactate 11.4, uric acid (Other), serum osmolality 270 (Osmolality), phosphate 5.2 (Phosphate) | EXTEND with CK: a must and the criterion's own rationale use CK 8640 for the rhabdomyolysis; the CK order also returns the lactate stored with it. TRIM serum osmolality and phosphate (incidental; the sodium and the served urine studies carry the hyponatremia) | yes |
| SE-S07 | action-2-interpret-labs | lactate 5.8, pH 7.28 (Blood Gas and Muscle Enzymes) | TRIM: post-convulsive; served bicarbonate 19 kept in its place | no |
| SE-S09 | action-2-interpret-labs | lactate 6.4, pH 7.26 (Blood Gas and Muscle Enzymes) | TRIM: post-convulsive; served bicarbonate 17 kept in its place | no |
| SE-S10 | action-2-interpret-labs | pH 7.14, lactate 10.8, CK 3120 (Blood Gas and Muscle Enzymes) | EXTEND with CK: a must treats rhabdomyolysis with acute kidney injury on CK 3120; the CK order returns the whole stored panel, so pH and lactate stay in the evidence | yes |
| SE-S11 | action-2-interpret-labs | pH 7.15 (Blood Gas) | TRIM: the served bicarbonate 12 shows the acidosis that decides dialysis | no |
| SE-M09 | core labs | none | no change | no |
| SE-P02 | core labs | none | no change | no |
| SE-P07 | core labs | none | no change | no |
| SE-S08 | core labs | none | no change | no |
| SE-S12 | core labs | none | no change | no |

Required-arguments changes (scoring changes: an agent must now name the added assay for the required core-labs
criterion):
- SE-P01 `action-3-interpret-labs`: + `thiamine_B1`.
- SE-P05 `action-2-interpret-labs`: + `CK`.
- SE-P08 `action-2-interpret-labs`: + `serum_osmolality`.
- SE-RS11 `action-2-interpret-labs`: + `CK`.
- SE-S05 `action-2-interpret-labs`: + `thiamine_B1`, `phosphate`.
- SE-S06 `action-2-interpret-labs`: + `CK`.
- SE-S10 `action-2-interpret-labs`: + `CK`.
Labels name the added assay; rationales gained one sentence where they did not already justify it (P08 and S06
did). Data moves without a scoring change: SE-S01, S03, S04 `Lactate` moved from panel `Other` into the served
`Arterial blood gas` panel (the library ABG lists lactate as a component). Evidence trims in M01, M02, M03,
M04, M05, M06, M07, M08, P03, P04, P06, P08, RS11, S01, S02, S03, S04, S06, S07, S09, S11.

Verification: for every SE lab criterion and alternative, the order was served in a fresh environment and every
number in `expected_evidence` was found in what came back (remaining hits are units, `HIV-1`, a time and a
historical titer). `perfect_agent.py` 30/30, `case_io.py check` on the 30 cases: schema and synonym guard OK, no
failure names an SE case; `pytest agent-platform/tests -k SE-` 180 passed (with `test_grpo_rollout.py` ignored,
see CENTRAL 7).

## CENTRAL

1. Matcher, interpretation prose: `_filter_lab_payload` keeps a sentence that names any kept test, so the
   one-sentence "Abnormal values: ..." interpretations still read out the dropped panels' values (M02 CRP,
   lactate, CK; M03 dsDNA, C3, C4, ESR; M05 and M06 CRP, ESR, procalcitonin; M07 and P03 troponin and BNP; S01
   CRP and procalcitonin; S07 and S09 lactate and CK). Filtering by clause (comma or semicolon list items) would
   close it; the alternative is rewriting those interpretations one sentence per panel.
2. Matcher, panel granularity: an order is answered panel by panel, so the CK added in RS11 also returns the
   troponin, urine myoglobin and procalcitonin stored in the same `Post-ictal markers` panel, the CK in S10 the
   blood gas, the thiamine in S05 the lactate. Acceptable for these cases; exact serving needs row-level filtering
   or split panels.
3. Matcher: a stored blood-gas panel answers a `CMP` order through its `HCO3` row (S01, S03, S04, S05, S06, P05,
   P08), and stored urine osmolality and urine sodium answer it through "sodium" (S03, S06). The SE evidence now
   relies on both (pH, lactate after the move, urine studies). If stored-side matching becomes name-only for
   ABG and urine panels, those criteria need `ABG` and urine assays in the order.
4. Matcher bug: `_panel_names` compares 5-letter prefixes, so `complement` ("compl") matches the panel
   "Complete Blood Count": an `anti_dsDNA` + `complement` order in SE-M03 also returns the CBC.
5. MockServer: `sleep_deprived` and `ambulatory` EEG orders in SE still get the library normal, since a fallback
   names one `eeg_type`. Proposal: let a routine fallback also answer `sleep_deprived` when the case stores no
   sleep-deprived recording (the same 20 to 40 minute study); ambulatory EEG in status is not a realistic order.
6. Review app: the routine EEG lives in `fallback_tool_outputs`; show case fallbacks to reviewers (they are
   patient data an agent can receive).
7. Test environment: `agent-platform/tests/test_grpo_rollout.py` fails collection without torch (the
   `training` extra), so `pytest agent-platform/tests -k SE-` errors unless that file is ignored or the extra
   is installed.
