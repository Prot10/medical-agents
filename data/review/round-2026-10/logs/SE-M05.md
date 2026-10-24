# SE-M05
Reviewer status: R1 none, R2 none (no notes; counted among the R2 approvals per the plan) | Approved before this round: yes (treated as approved per plans/SE.md; every fix below is a section-2 class or a real error)

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | | No reviewer notes on this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `initial_tool_outputs.labs.panels["Exclusion studies"]`, `["Mimic exclusion"]` | Template blocks (lactate, ABG, oligoclonal bands, paraneoplastic panel, beta-hCG) in the first-line serum labs; oligoclonal bands are a CSF test (C1). | FIXED: both deleted; lactate 2.4 (H) in its own row, hepatic panel and chloride added, beta-hCG <2 kept in a pregnancy panel (C2); oligoclonal bands reported in the CSF only (4 CSF-specific bands). |
| D | major | `patient.history_present_illness` | "Comprehensive urine drug screen is negative" leaked a result; EMS temperature 38.9 against 39.1 in the vitals and exam (C7). | FIXED: drug-screen sentence removed (the result is in the labs); temperature 39.1. |
| C | major | criterion action-11 microbiology | Blood cultures required before antimicrobials with template text (C3). | FIXED: recommended, label cites fever 39.1 C, tachycardia and procalcitonin 0.8, argument `specimen: blood_culture` only; report "no growth to date". |
| C | major | criterion action-5 CSF | Required `oligoclonal_bands` instead of the diagnostic CSF NMDAR antibody (C15). | FIXED: `special_tests` HSV_PCR and NMDAR_antibodies; CSF report states NMDAR IgG 1:32 and the full viral PCR panel. |
| C | major | criterion action-6 antibody panel | Asked for `paraneoplastic_panel`, which shares no token with its follow-up trigger, so the first-line labs answered it. | FIXED: alternatives `autoimmune_encephalitis_panel` and `NMDAR_IgG_cell_based`; trigger `request_autoimmune_encephalitis_nmdar_panel`; serum NMDAR IgG 1:320 by cell-based assay, CASPR2 added; required. |
| C | major | criterion action-7 body imaging; `followup_outputs` `request_pelvic_imaging_ovarian_teratoma` | Single CT alternative; an orphan advanced-imaging pelvic MRI reported a 6.8 x 5.2 cm lesion while the CT measured 4.6 x 3.9 cm (C5, C15). | FIXED: orphan deleted; alternatives pelvis_abdomen_MRI, pelvis_abdomen_ultrasound, pelvis_abdomen_CT, each with its own consistent report (about 4.6 x 3.9 cm). Management text ("removal is part of definitive treatment") removed from the CT impression. |
| C | major | `initial_tool_outputs.drug_interactions`, `fallback_tool_outputs.drug_interactions` | Initial "general" drug output repeated criterion text (leak guard failure); fallback generic (C9). | FIXED: both deleted; T-DDI follow-up (fosphenytoin with the combined pill, ibuprofen with acyclovir, IVIG with estrogen, valproate teratogenicity as contraindication); criterion optional. |
| C | minor | literature follow-up, criterion action-9 | Literature carried management conclusions and sat in the stop rule (C8). | FIXED: optional, last, T-LIT content with [Graus_2016], [Tunkel_2008], [Titulaer_2013], [ESETT_2019]; trigger `request_autoimmune_encephalitis_literature`. |
| C | minor | `followup_outputs` cEEG follow-up | Post-treatment EEG follow-up (C4). | FIXED: deleted; the `continuous_icu` order receives the initial EEG. |
| B | minor | `initial_tool_outputs.eeg` | Not in ACNS terms; dyskinesias reported as ictal. | FIXED: right temporal electrographic seizures, extreme delta brush, diffuse slowing; dyskinesias without EEG correlate; numbered impression. |
| D | minor | MRI follow-up `signal_characteristics`, finding types | "anti-NMDAR involvement", "limbic encephalitis" in data fields. | FIXED: signal descriptions only; impression keeps the imaging differential. Expected evidence no longer says "May be normal in 50%" for an abnormal MRI. |
| C | major | `required_recommendations`, `prohibited_recommendations` | Lorazepam without maximum; no acyclovir stop condition; immunotherapy without doses; several overlapping neuroleptic prohibitions. | FIXED: T-MUST-BZD; acyclovir 10 mg/kg every 8 hours renally adjusted, stopped once HSV PCR is negative [Tunkel_2008]; T-MUST-2L levetiracetam avoiding valproate (reproductive age); T-MUST-cEEG; methylprednisolone 1 g x 5 days with IVIG 0.4 g/kg/day x 5 days or PLEX [Titulaer_2013; Graus_2016]; teratoma removal with gynecology. One haloperidol prohibition kept (C15). |
| C | major | `ground_truth.differential` | HSV encephalitis "high" with negative PCR (C14). | FIXED: HSV low, bacterial meningitis, other autoimmune, paraneoplastic, psychiatric and toxic causes very_low, each citing the result that lowers it. |
| B | major | `sequence_constraints` | Hard labs before drug check ("beta-hCG before contrast") (C13). | FIXED: deleted; CT before CSF hard kept. |
| E | minor | criteria labels/rationales; labs and EEG arguments | Inflammatory markers and ABG/lactate as required lab arguments; EEG without `eeg_type`. | FIXED: T-LABS with tox_screen and beta-hCG extras, T-CT, T-EEG (continuous_icu or video). |
| A | minor | `fallback_tool_outputs.specialized_test`; `red_herrings[0].field_path` | Non-vocabulary specialized fallback (C10); red herring pointed at the whole labs. | FIXED: fallback deleted, `fallback_tool_kinds` updated; path is the procalcitonin row. |
| B | minor | order; `stop_rule` | Not the diagnostic order; allowance 0 (C12). | FIXED: labs, blood cultures, CT, EEG, MRI, CSF, antibody panel, pelvic imaging, drug check, literature; stop rule = 7 required, allowance 1. |
| E | minor | whole file | British "tumour" and em dashes. | FIXED: "tumor", em dashes replaced. |

## Changes, in one paragraph a physician can read before re-reviewing
A 34-year-old woman with a 5-day psychiatric prodrome, fever 39.1 C, orofacial dyskinesias and a seizure without return to baseline. The HPI no longer gives the drug-screen result. First-line labs show leukocytosis and raised CRP, ESR, procalcitonin and lactate, with negative toxicology and beta-hCG. The EEG shows right temporal electrographic SE with extreme delta brush; the dyskinesias have no EEG correlate. MRI shows bilateral mesial temporal FLAIR change. CSF is lymphocytic with oligoclonal bands, negative viral PCRs and NMDAR IgG 1:32; serum NMDAR IgG is 1:320. Pelvic MRI, ultrasound or CT each show a 4.6 cm right ovarian mature teratoma. Blood cultures are recommended and negative. Musts: lorazepam, acyclovir until PCR is negative, levetiracetam (not valproate), cEEG, first-line immunotherapy with doses, teratoma removal; neuroleptics are prohibited. The HSV differential is now low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: allow-list `[ACNS_2021]`, `[Tunkel_2008]`, `[Graus_2016]`, `[Titulaer_2013]` for SE; this case cites them.
- `perfect_agent.py` warns that the `pelvis_abdomen_ultrasound` alternative is "answered by a fallback", but a direct served-output probe returns the case's ultrasound follow-up (`from_fallback` false); the warning likely comes from the simulator's sequential consumption of the body-imaging follow-ups. Worth a look in the tool.

## Open questions for Andrea (judgment calls you could not settle)
None. Decided: the drug check stays optional (plan C9) because no interaction changes the ASM choice once levetiracetam is chosen; the blood cultures are recommended rather than required since the CSF and procalcitonin carry the infection question.

## Verification
`perfect_agent.py SE-M05 -v`: pass (one warning on the ultrasound alternative, see CENTRAL); labs, blood cultures and CT from initial outputs, EEG initial for `continuous_icu`, MRI, CSF, antibody panel and pelvic MRI from follow-ups; served-output probe confirms MRI, ultrasound and CT each get their own report. `pytest -k "SE-M05 or red_herring"` (case guards incl. leak guard, red-herring paths): pass. `case_io.py check SE-M05`: schema and synonym guard OK; no failure names SE-M05.

## Verification (adversarial verifier, 24 Oct 2026)
Checked: whole final case read. Exclusion and Mimic blocks gone; oligoclonal bands only in the CSF; beta-hCG kept with a value; blood cultures recommended with case text and no `before_antimicrobials`; CSF criterion asks for HSV_PCR and NMDAR_antibodies and the CSF report carries NMDAR IgG 1:32; serum panel required and answered by its own follow-up (1:320); pelvic MRI, ultrasound and CT give consistent sizes (4.5 to 4.6 cm); one neuroleptic prohibition; HSV low with negative PCRs; HPI no longer states the drug-screen result and the temperature is 39.1 throughout; stop rule equals the 7 required criteria.
Found and fixed:
- B minor `patient.neurological_exam.mental_status`: "GCS 9 (E3V2M4)" contradicts its own descriptors (markedly agitated and combative in restraints, so eyes open spontaneously, E4; disorganized speech, not incomprehensible sounds, V3; combative without following commands, localizing, M5). FIXED: "GCS 12 (E4V3M5)".
Tried and reverted: moving the pelvic CT out of `initial_tool_outputs.body_imaging` into a follow-up (plan 3.2) made the CT alternative fall to the library normal report whenever the order's context names another modality, because the trigger matcher picks a sibling body-imaging follow-up and the modality guard then rejects it with no other case payload left. The initial CT is kept so that every CT order receives the case's CT.
CENTRAL: same matcher defect for the ultrasound alternative, already flagged by the worker. Reproduced: `order_body_imaging {"study": "pelvis_abdomen_ultrasound", "clinical_context": "...pelvic MRI, pelvic ultrasound or CT"}` returns the library "no adnexal mass" report, because `match_followup` ties the MRI and ultrasound triggers and declaration order picks MRI, which `_answers_the_question` then rejects. Fix proposal for `mock_server.get_output`: filter follow-up candidates by `_answers_the_question` before choosing (or give `order_body_imaging` a working discriminator: its outputs carry `modality` and `region`, not `study`, so `_match_by_discriminator` never fires for it). Not fixable in the case without breaking the symmetric MRI order.
Checks re-run after my edits: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards -k` pass.

## Close-out (24 Oct 2026)
Decisions in `plans/SE-decisions.md`.
- synonyms: the G41 category no longer grants the type codes G41.0, G41.2 and G41.8 (a type code is granted only by the case's own code, so an answer coded with the wrong SE type no longer scores by code); `apply_diagnosis_synonyms.py --prune --conditions status_epilepticus` removed G41.0 and G41.8 from `ground_truth.diagnosis.icd_codes`. Labels unchanged.
- Checks: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, SE case guards pass, `apply_diagnosis_synonyms.py --check --conditions status_epilepticus` clean.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `continuous_icu`, decided by reading the report.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## EEG and labs after routing (25 Oct 2026)

Commit 317e46db routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG) and serves an `interpret_labs` order only the stored panels it names. Decisions for the condition in `plans/SE-routing-decisions.md`.

- EEG: a routine order received the library's normal routine EEG, which contradicts the case. Added `fallback_tool_outputs.eeg` with `eeg_type` `routine` (the stored continuous_icu recording cut to a 30-minute portable recording without video, technologist notes for the clinical events, activation not performed): recurrent right temporal seizures with intervals under 2 minutes (electrographic SE), extreme delta brush, dyskinesias without EEG correlate. No criterion, tiers and the reward-relevant policy unchanged; the clinically correct test stays the continuous EEG of `action-1-analyze-eeg`. A `continuous_icu` or `video` order still receives `initial_tool_outputs.eeg`.
- Labs `action-2-interpret-labs`: unserved result cited in `expected_evidence`: CRP 28.4, ESR 72, procalcitonin 0.8 (Infectious and Inflammatory), lactate 2.4 (Other). TRIM: inflammatory markers are not the point of the metabolic and toxic screen; fever alone justifies the cultures criterion; the values stay available to a CRP or procalcitonin order. Scoring change: no.
  - action-2-interpret-labs expected_evidence: 'WBC 13.2, CRP 28.4, ESR 72, procalcitonin 0.8, lactate 2.4; electrolytes, renal and hepatic function normal; toxicology screen negative; beta-hCG negative' -> 'WBC 13.2; electrolytes, renal and hepatic function normal; toxicology screen negative; beta-hCG negative'
- Checks: `perfect_agent.py -v` pass; `case_io.py check` schema and synonym guard OK, no test failure names the case; probe: routine (omitted and explicit) order -> the new case fallback, `continuous_icu` and `video` -> the stored index recording; every number in each lab criterion's evidence is in what its order returns.
