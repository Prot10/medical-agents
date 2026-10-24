# ALZ-EARLY-RM04
Reviewer status: R1 not reviewed, R2 not reviewed (no entry in notes/ALZ-EARLY.md) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer note names this case. Condition classes C1, C2, C3, C4, C5, C8, C10, C11, C12, C13, C16 of plans/ALZ-EARLY.md applied (see below). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | patient.history_present_illness; initial_tool_outputs.clinical_assessment | Functional staging ambiguous ("missed two appointments despite being reminded", "increasing difficulty managing her calendar and correspondence") for a case labelled MCI (C4, rule 1.2). | FIXED: HPI states the two misses were six months ago, she compensates with a wall calendar and phone alerts, still manages calendar, correspondence and bills herself, husband has taken over nothing, no driving accidents or getting lost. Clinical assessment findings and impression rewritten to match. |
| B/E | major | initial_tool_outputs.clinical_assessment.impression, .scores, .findings | Template impression with engineering sentences ("this assessment is where it is decided", "imaging and biomarkers then attribute it"); first finding was a sentence fragment ending in ";" (C3). | FIXED: impression rebuilt from the case (MMSE 25, MoCA 21, domains, no cue benefit, informant, functional sentence); findings completed with language and the full orientation result; score keys renamed (Animal fluency, Functional stage). Structured fields already agreed (cueing false matches "no benefit from category cues"; informant true). |
| B | minor | initial_tool_outputs.labs.panels.Thyroid Function[TSH] | Current TSH 6.2 identical to the pre-referral TSH that led to the dose increase four months earlier. | FIXED: current TSH 5.8 mIU/L (6.2 kept as the pre-referral value in HPI); propagated to interpretation, abnormal summary, criterion expected_evidence, red herring, differential, KCE, musts, prohibition. |
| D | minor | initial_tool_outputs.labs.abnormal_values_summary | Interpretive text ("subclinical to mild overt hypothyroidism", "consistent with iron deficiency", "microcytic anemia pattern"); free T4 1.1 (within range) listed as abnormal "low-normal". | FIXED: factual list only; free T4 shown as within range. |
| B | minor | initial_tool_outputs.mri.additional_observations | "No ... abnormal enhancement post-gadolinium" with contrast false (C5). | FIXED: "No mass lesion". |
| B | minor | followup_outputs[neuropsych].findings (TMT-A, TMT-B) | TMT-A 44 s and TMT-B 98 s marked normal (29th and 26th percentile) while their reference ranges (<42 s, <90 s) made them abnormal. | FIXED: reference ranges <50 s and <120 s for age/education, consistent with the percentiles. |
| C | major | followup_outputs[neuropsych].impression; action-5 expected_evidence | Impression called the profile "amnestic MCI, predominantly amnestic" although naming (BNT 7th percentile) and semantic fluency (14th) are impaired: that is amnestic multi-domain MCI. "Hippocampal-type memory failure" is a cross-modality inference. | FIXED: impression now "amnestic multi-domain mild cognitive impairment (episodic memory with milder naming and semantic fluency involvement)", adds the Rey delayed recall and copy, executive and speed normal. Label conflict sent to CENTRAL (accepted[0] says "single-domain"). |
| A/C | major | followup_outputs (check_drug_interactions); action-11 | Donepezil drug check in an MCI case, routing donepezil through CYP2C19 (omeprazole) (C1). | FIXED: criterion and follow-up deleted; initial and fallback drug_interactions already null; MCI prohibition and MCI must added. |
| A | major | followup_outputs (search_medical_literature); action-10; fallback_tool_outputs.literature_search; metadata.fallback_tool_kinds | Literature search was a `recommended` clinical step whose expected_evidence restated the case (C8, ruling 5). | FIXED: criterion, follow-up and fallback deleted (null); `literature_search` removed from fallback_tool_kinds. |
| A/B | major | ground_truth.action_criteria[action-8]; initial_tool_outputs.csf | Amyloid PET was the "single optional biological-confirmation route"; a CSF order would have returned the library's normal CSF, contradicting the case (C2). | FIXED: action-8 now has two alternatives (CSF Abeta42/ratio/p-tau/t-tau, amyloid PET) with the plan's label and rationale; authored initial_tool_outputs.csf concordant with the positive PET (Abeta42 498, Abeta40 10850, ratio 0.046 low, p-tau181 92 high, t-tau 610 high, acellular, protein 38, glucose 60, opening pressure 14 cmH2O). |
| A | major | fallback_tool_outputs.advanced_imaging | DaTscan report as the fallback for every advanced-imaging modality (C2.3). | FIXED: null. |
| C | minor | action-9 expected_evidence | Said lvPPA has an "asymmetric frontotemporal pattern"; lvPPA hypometabolism is left posterior temporoparietal. | FIXED: Alzheimer-type symmetric pattern contrasted with the frontotemporal pattern of FTD and the left-lateralized temporoparietal pattern of lvPPA; label reworded for MCI ("if the syndrome remains uncertain"). |
| E | minor | all action_criteria rationale and citations | Rationale identical to label; duplicated citations "[X]" and "X" (C13). | FIXED: one bracketed key each; rationale rewritten per patient. action-4 now cites [NIA_AA_MCI_2011]. |
| A | minor | ground_truth.sequence_constraints; stop_rule | No sequence constraints; max_additional_actions 0 (C16). | FIXED: soft MRI before biomarker criterion; soft clinical assessment before biomarker criterion; max_additional_actions 1. |
| C | major | assessment.required_recommendations | Musts restated tool steps (MRI, neuropsych, labs) and the engineering "single case-designated biomarker route" must (C12, C2.5). Thyroid must did not address the absorption problem. Persistent iron-deficiency anaemia (ferritin 9 despite two years of oral iron, 67-year-old woman) had no management. | FIXED: restating musts deleted; canonical biomarker must; MCI must; thyroid must (separate levothyroxine from calcium and iron by 4 h, recheck TSH/free T4 in 6 to 8 weeks); iron-deficiency must (review absorption, GI evaluation); informant, safety and disclosure musts kept and made case-specific. |
| C | minor | assessment.prohibited_recommendations | Generic anticholinergic, benzodiazepine, antipsychotic and memantine prohibitions with no trigger in the case; the TSH prohibition cited "positive amyloid biomarkers" that only an optional step returns (C12). | FIXED: three prohibitions kept: TSH attribution (reworded), PPA anchoring, the canonical MCI cholinesterase-inhibitor/memantine prohibition. |
| C | minor | ground_truth.differential | lvPPA left `moderate` after a work-up that shows an amnestic profile; FTD key features cited "tau biomarkers" the case did not contain; hypothyroidism entry called free T4 "low-normal rather than unequivocally low" (C11). | FIXED: lvPPA `low` with excluding features; FTD and hypothyroidism key features rewritten from case data. Depression and DLB unchanged (correct). |
| D/C | minor | ground_truth.key_clinical_evidence | Six items, including A+T+N+ (no tau measured in the required pathway), APOE (not in the case) and "AChEI first-line" (C10). | FIXED: four items: word-finding pearl, thyroid pearl (with absorption), storage-type pearl, MCI cholinesterase-inhibitor fact. |
| B | minor | ground_truth.red_herrings[0..2] | Interpretations cited an "A+T+N+ CSF biomarker profile" and "biomarker changes" that are not in the required pathway. | FIXED: rewritten to cite MRI and neuropsychology only; [0] data_point updated to the current TSH. |
| C | minor | avoided_actions (EEG, ECG, CT) | Generic rationales. | FIXED: one case-specific sentence each. |
| B | minor | followup_outputs (amyloid PET, FDG-PET).tracer_or_protocol | null. | FIXED: tracer and method filled. |
| - | check | 3.6 check | Probe of every alternative (scratch script): CSF -> initial_tool_outputs.csf, amyloid PET -> followup request_amyloid_pet, FDG -> followup request_fdg_pet; none answered by the library. perfect_agent -v: each required criterion receives the report with its expected evidence. | OK |

## Changes, in one paragraph a physician can read before re-reviewing
The case stays amnestic MCI due to Alzheimer disease in a 67-year-old professor with word-finding complaints. The HPI and clinical assessment now make the staging explicit: two missed appointments six months ago, none since she adopted a calendar and phone alerts, and she still runs her calendar, correspondence and bills herself. The neuropsychology impression now names amnestic multi-domain MCI (memory with milder naming and semantic fluency involvement). The current TSH is 5.8 mIU/L (the 6.2 before referral is kept as history), and the thyroid must now targets absorption (calcium carbonate and ferrous sulfate taken with levothyroxine) with a recheck in 6 to 8 weeks. A new must addresses the persistent iron-deficiency anaemia. The donepezil interaction check and the literature search are gone. Amyloid status can now be established by CSF or amyloid PET as alternatives, with a concordant CSF report authored (low Abeta42/40, high p-tau181 and t-tau). The DaTscan fallback is removed, the post-gadolinium phrase is gone, lvPPA is now low in the differential, and the musts and prohibitions are case-specific. Two soft sequence constraints were added.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Diagnosis label: `accepted[0]` reads "Mild cognitive impairment due to Alzheimer's disease (amnestic, predominantly amnestic single-domain with naming involvement)". The data show memory plus naming and semantic fluency impairment, which is amnestic multi-domain MCI (Albert 2011). Proposed label: "Mild cognitive impairment due to Alzheimer's disease (amnestic multi-domain, with naming involvement)", G31.84 unchanged. Not changed here because no reviewer ruled on it (ROUND_POLICY rule 3).
- Synonyms: the expansion grants this MCI case "alzheimer dementia", "dementia due to alzheimer", "posterior cortical atrophy", "benson syndrome", "early onset alzheimer" and G30.0/G30.1/G30.8/G30.9/F00. Onset was at about 66 years, the stage is MCI and the phenotype is not PCA (plan section 5.1).
- Citation keys: `[NIA_AA_MCI_2011]` (plan); `[ATA_hypothyroidism_2014]` = Jonklaas J et al., Guidelines for the treatment of hypothyroidism, Thyroid 2014;24:1670-1751; `[BSG_IDA_2021]` = Snook J et al., British Society of Gastroenterology guidelines for the management of iron deficiency anaemia in adults, Gut 2021;70:2030-2051.

## Open questions for Andrea (judgment calls you could not settle)
- None needing Andrea. Deviation from the plan recorded: the plan's canonical subclinical-hypothyroidism must (repeat TSH with TPO antibodies, do not start levothyroxine) does not fit this patient, who has known treated hypothyroidism; the must used is the under-replacement version (adherence and absorption, recheck in 6 to 8 weeks), per ATA 2014.

## Verification
Adversarial check, 24 Oct 2026. Read the log, the full diff and the whole final case. No reviewer note names this case; the table correctly says so.
- Checked every own-finding claim against the file: HPI and clinical assessment staging agree (two misses six months ago, compensated, nothing taken over; IADL field false, amnestic true, cueing false, informant true); TSH 5.8 propagated to labs, abnormal summary, criterion evidence, red herring [0] (field path still points to the TSH row), differential, key evidence, musts and prohibition, with 6.2 kept only as the pre-referral value in HPI and PMH; free T4 within range; drug check and literature gone, initial and fallback drug_interactions and literature_search null, fallback advanced_imaging null; TMT ranges agree with the percentiles; no post-contrast phrase with contrast false.
- Biomarker criterion: both alternatives are case-authored (CSF in initial_tool_outputs, amyloid PET follow-up); CSF arithmetic checked (498/10850 = 0.046; glucose 60/89 = 0.67) and concordant with the positive PET; FDG follow-up exists.
- Musts and prohibitions: canonical MCI prohibition and must present, no cholinesterase inhibitor must, levothyroxine timing and iron-deficiency musts are clinically sound (ATA 2014, BSG 2021), avoided ECG rationale consistent with no planned rate-slowing drug. Differential matches the final evidence.
- Label: accepted[0] still says "single-domain" while the neuropsychology impression (correctly) says multi-domain; the worker's CENTRAL request is the right route under ROUND_POLICY rule 3 (no reviewer ruling). Scoring is unaffected.
- Found nothing to change. perfect_agent.py -v and case_io.py check clean.


## Condition audit (24 Oct 2026)
Cross-case consistency pass by the ALZ-EARLY condition auditor, through case_io. Changed:
- lab panel key `Reviewed_cognitive_panel_additions` renamed `Magnesium, Homocysteine, ESR and CRP` (the key exposed a review-round artefact to the agent; contents and order unchanged).
- 'the reviewed cognitive laboratory panel' reworded 'the cognitive laboratory panel' (the labs criterion label), the wording the other six cases already use.
- `Basic Metabolic Panel` completed to `Comprehensive Metabolic Panel` with normal liver tests (total protein 7.1, albumin 4.2, AST 21, ALT 18, ALP 63, bilirubin 0.6): the labs criterion orders a CMP, so the authored report has to carry the hepatic part; no field_path points into the panel.
- MMSE and MoCA item arithmetic: the listed losses summed to 27/30 and 23/30 against the stated 25/30 and 21/30; MMSE now recall 1/3 (2 points), serial sevens two errors starting at 93 (2) and date (1) = 25; MoCA adds serial subtraction 2/3 and orientation (date) = 21 (exam, findings[1], [2], impression, which now says 1/3 on the MMSE and lists attention); expected_evidence and the neuropsychological report carry only totals and needed no change.
After the change: perfect_agent.py and case_io.py check clean on all 30 cases; test_case_guards (ALZ-EARLY) pass.
- Normal values in `Magnesium, Homocysteine, ESR and CRP` varied (Magnesium 2.0 to 1.9, Homocysteine 10.2 to 8.9, ESR 12 to 14, CRP 1.8 to 1.3), all still within the case's reference ranges: the same numbers (magnesium 2.0, homocysteine 10.2, ESR 12, CRP 1.8) had been copied into up to 13 cases, a template artefact raised by the S01 worker; no text cites the changed values.
- Checks re-run after these additions: perfect_agent.py, case_io.py check and test_case_guards clean.

## Close-out (24 Oct 2026)

- Synonyms re-expanded (`apply_diagnosis_synonyms.py --prune --conditions alzheimers_early`): MCI labels only. Removed "alzheimer disease", "alzheimer's disease", "alzheimers disease", "alzheimer dementia", "dementia due to alzheimer", "posterior cortical atrophy", "benson syndrome", "early onset alzheimer" and the codes G30.0, G30.1, G30.8, G30.9, F00, because every "dementia due to Alzheimer disease" answer contains those tokens and would have scored an overcall of this MCI case as correct.
- `ground_truth.diagnosis.accepted[0]`: "... (amnestic, predominantly amnestic single-domain with naming involvement)" -> "Mild cognitive impairment due to Alzheimer's disease (amnestic multi-domain, with naming involvement)"; G31.84 unchanged. The battery shows memory plus naming and semantic fluency impairment, which is amnestic multi-domain MCI (Albert 2011); the old label contradicted the case's own neuropsychology impression (ROUND_POLICY ruling 3, decided under Andrea's 24 Oct 2026 ruling).
- Checks: `perfect_agent.py -v` pass; `case_io.py check` no failure names this case; case guards pass; synonym `--check` clean. Decisions in `plans/ALZ-EARLY-decisions.md`.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, named in the report's own text.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Lab evidence (25 Oct 2026)

Since 24 Oct 2026 an `interpret_labs` order returns only the stored panels it names (`tools/lab_matching.py`). This criterion's `expected_evidence` cited results its own order (the first alternative) no longer returned; a perfect agent following it would not see them.

- `ground_truth.action_criteria[action-6-interpret-labs]`.alternatives: was [CBC, CMP, TSH, B12, folate, homocysteine, magnesium, ESR, CRP]; now [CBC, CMP, TSH, B12, folate, homocysteine, magnesium, ESR, CRP, iron_studies] | [CBC, CMP, TSH, B12, folate, homocysteine, magnesium, ESR, CRP].
- Decision: serve: new first alternative (old order kept as an alternative). A must investigates the iron-deficiency anaemia (ferritin 9); the iron studies were not returned.
- Scoring: coverage unchanged (any call matching the old order still matches); the cost reference of the required work-up now uses the new first order.

Checks: `perfect_agent.py` ok (the order returns every result its evidence cites); `case_io.py check` clean for this case.
