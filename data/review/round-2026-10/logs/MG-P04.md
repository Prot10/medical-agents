# MG-P04
Reviewer status: none (condition not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none | - | No reviewer notes for this case (`notes/MG.md` does not exist). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.neurological_exam.additional`, `.cranial_nerves` | NIF -58 and FVC 3.8 L (84%) in the exam, the scored respiratory result (class K); the ice-pack result in the exam, the scored ice-pack criterion. | FIXED: both removed; exam keeps the bedside picture (counting to 50 with slurring, chewing fatigue, hoarse voice). Prior outside AChR/MuSK negatives kept as history: they are the anchor of the functional label, and the scored labs are the reference-laboratory repeat plus thyroid function (plan K). |
| B | major | `followup_outputs[request_ice_pack_test]`, `patient.neurological_exam.cranial_nerves` | Ice-pack report called 5 mm an MRD1 and "MRD1 >=3 mm normal" while describing it as ptosis, so the numbers read as normal lids; teaching parenthetical on acetylcholinesterase. | FIXED: exam and report in MRD1 (left 2.5 mm at rest, 0.5 mm after upgaze; 0.5 to 3.5 mm after ice; right 3.5 to 4.0 mm); impression in report voice. |
| B | minor | `patient.history_present_illness` | Overnight oximetry cannot give an AHI; em dash. | FIXED: CPAP download with residual AHI below 5; dash removed. |
| A | minor | `patient.physical_exam` | No weight or height for mL/kg. | FIXED: 86.8 kg, 178 cm (BMI 27.4 as in demographics). |
| B | minor | `initial_tool_outputs.labs` | AChR range of one laboratory (<0.4) with MuSK of another (<0.02); CBC and BMP "All normal"; summary listed normal results; MuSK "6% of AChR-seronegative" figure; panel name with an em dash. | FIXED: one laboratory (<=0.02 nmol/L, blocking <=15%, modulating <=20%); CBC and BMP analytes with values; empty abnormal summary; hedged serology comment; panel `Neuromuscular_Junction_Antibody_Panel` (red herring path updated). |
| C | minor | `followup_outputs[LRP4]` | "1-5% of double-seronegative MG" (plan fact 1 forbids a single figure) and a mechanism essay. | FIXED: LRP4 by cell-based assay 1:400 with a clustered AChR CBA (negative) in the same report; hedged comment; trigger renamed `request_lrp4_and_clustered_achr_antibodies`. |
| B | major | `initial_tool_outputs.specialized_test`, `followup_outputs` | SFEMG sat in the initial work-up and RNS in a follow-up, so the review app showed SFEMG before RNS; RNS report mixed a 50 Hz label with a 10 s exercise and carried a sensitivity lecture. | FIXED: RNS is the initial specialized test (technique row, deltoid 8%, trapezius 9%, nasalis 7%, ADM increment 6% after 10 s exercise, normal NCS); SFEMG is a follow-up with jitter percentages and blocking per muscle. Red herring path moved to `initial_tool_outputs.specialized_test.impression`. |
| D | minor | `initial_tool_outputs.body_imaging` | "Consistent with prior smoking history" (clinical history in a CT report); pleural finding located in the mediastinum. | FIXED: modality-only wording; locations corrected; `region` "mediastinum, chest" so the `chest_CT` alternative is answered by this report. |
| C | major | `followup_outputs[request_respiratory_function]` | FVC 84% called "borderline reduced"; male MEP reference ">60"; NIF and MIP reported as two measurements; no mL/kg. | FIXED: FVC 3.8 L (84%, 43.8 mL/kg), supine 3.6 L, MIP -72, MEP 112 (reference >=95), strong cough, called normal. |
| D | major | `followup_outputs[request_drug_interaction_check_mg]`, `[request_literature_lrp4_seronegative_mg]` | Generic MG-drug essay with telithromycin and "dose NMB at 10-20%"; literature with invented journals, "1-5%", "misdiagnosed as FND in up to 30%". | FIXED: both deleted; one initial drug output in checker voice (lisinopril, atorvastatin statin caution, MG class warnings, steroid worsening) and one initial literature output (Sanders 2016 and update, Higuchi 2011, Zisimopoulou 2014). Leak guard passes. |
| A | major | `action_criteria[action-6-search-medical-literature]`, `[action-7-check-drug-interactions]` | Exact literature query and non-schema `screen_for`. | FIXED: `{}`; both optional (ruling 5, plan 3.2: no interaction that changes management). |
| C | major | `ground_truth.action_criteria` order, labels, citations | Labels equal rationales; `[Wolfe_2016]` on every criterion; "gold standard >95%". | FIXED: order ice pack, AChR/MuSK/TSH, RNS, LRP4, SFEMG, mediastinal CT (alternative chest CT), respiratory, drug check, literature; ids kept; case rationales; `[Wolfe_2016]` only on thymic imaging. Tiers per plan: labs, LRP4, RNS, SFEMG, CT required; ice pack and respiratory recommended. |
| C | major | `sequence_constraints`, `stop_rule` | Single `labs -> SFEMG` with a muddled reason; stop rule required literature and drug check with 0 extra actions. | FIXED: soft `labs -> SFEMG`, `RNS -> SFEMG`, `labs -> LRP4`; stop rule the five required criteria, `max_additional_actions: 2`. |
| C | major | `ground_truth.assessment.required_recommendations` | All six musts were tests or documentation. | FIXED: pyridostigmine dosing; low-dose prednisone titration and azathioprine after TPMT if needed; record correction of the functional label; drug list, statin review and red flags. No thymectomy must (not routine in LRP4 MG, plan fact 20). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Template set with telithromycin and "pyridostigmine bridge". | FIXED: case-specific functional prohibition, plan canonical drug and steroid prohibitions, beta-blocker prohibition kept. |
| C | major | `ground_truth.differential` | FND, MuSK MG and AChR MG left `moderate` after the results exclude them; CMS "genetic panel deferred". | FIXED: FND low; MuSK MG, AChR MG, LEMS, CMS, CPEO very_low, each with the excluding result. |
| C | minor | `ground_truth.key_clinical_evidence`, `red_herrings` | Template figures (10-15%, 1-5%, >95%). | FIXED: six case-specific bullets; red herring interpretations rewritten without figures. |
| C | minor | `ground_truth.avoided_actions[*]` | `[Wolfe_2016]` on every waste item. | FIXED: case rationales with Jacob 2025 in text; citations emptied. |
| D | minor | `fallback_tool_outputs.ct`, `.mri`, `.echo` | Head-CT fallback said it "does not address the question" (class F); MRI and echo fallbacks commented on relevance to the case. | FIXED: plain normal wording. |

## Changes, in one paragraph a physician can read before re-reviewing

A 48-year-old man labelled functional after outside AChR and MuSK negatives. The exam no longer shows the ice-pack or spirometry results. The pathway now reads: ice-pack test (recommended; left MRD1 0.5 to 3.5 mm), repeat AChR/MuSK with thyroid function at the reference laboratory (required; all negative, one laboratory's ranges), RNS (required, now the initial study; normal, maximum 9%, no increment), LRP4 with clustered AChR by cell-based assay (required; LRP4 1:400 positive, clustered AChR negative), SFEMG (required; abnormal jitter and blocking in EDC and orbicularis oculi), mediastinal CT with contrast (required; involuted thymus, mild emphysema), respiratory function (recommended; normal, 43.8 mL/kg), then optional drug check and literature. Musts are now management: pyridostigmine, cautious prednisone with azathioprine after TPMT if needed, correcting the functional label, and drug safety. The differential has FND low and the other subtypes and mimics very low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys used in text only: Jacob 2025, Evoli 2019, Narayanaswami 2021, Lawn 2001 (plan CENTRAL 1); Higuchi O et al., Ann Neurol 2011;69:418-422 and Zisimopoulou P et al., J Autoimmun 2014;52:139-145 in the literature output (an LRP4 key would also settle `metadata.citation_gap`).
- Harness: one `interpret_labs` call listing `anti_AChR`, `anti_MuSK`, `anti_LRP4`, `TSH` together is answered by the LRP4 follow-up alone (the AChR/MuSK/thyroid report is not returned). Scoring is unaffected, but the agent sees only part of what it ordered; the resolver could merge the initial report with a set-valued follow-up.

## Open questions for Andrea (judgment calls you could not settle)

- None. Spelling: the case is written in British English, so new text keeps it (haemoglobin, titre, anaesthetist), per ROUND_POLICY.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log and the whole final case. No reviewer notes exist for MG. Checked each own-finding row against the file: NIF, FVC and ice-pack results are out of the exam; ice-pack MRD1 values agree between exam (2.5 mm at rest, 0.5 mm after upgaze) and report; one laboratory's ranges; CBC and BMP with values; RNS is the initial study and normal (maximum 9%), SFEMG abnormal in EDC and orbicularis oculi; LRP4 and clustered AChR CBA in one follow-up; respiratory values correct (FVC 3.8 L = 43.8 mL/kg at 86.8 kg, 84% of 4.5 L; supine fall 5%); BMI 27.4 matches; the literature citations (Higuchi 2011, Zisimopoulou 2014) exist and say what they are cited for; no thymectomy must (not routine in LRP4 MG); differential lowered with the excluding results; fallbacks in plain wording.

Found and fixed:
- C minor, `ground_truth.sequence_constraints`: the two soft constraints that put the repeat AChR/MuSK panel before LRP4 and before SFEMG were removed. Their premise (negative AChR and MuSK antibodies) is already documented in the HPI from the outside laboratory, so an agent that goes straight to the extended cell-based panel or SFEMG is doing the right thing and should not lose sequence credit. This departs from the plan's per-case line ("labs -> SFEMG keep; add labs -> LRP4"); the reason is the documented prior serology. `RNS -> SFEMG` (soft) is kept.

Accepted as logged: the repeat AChR/MuSK with thyroid function stays required (reference-laboratory confirmation including modulating antibodies, and thyroid function never checked), drug check and literature optional. `perfect_agent.py MG-P04 -v` passes, `case_io.py check` reports no failure naming the case, case guards pass.

## Close-out (24 Oct 2026)

- `metadata.citation_gap` emptied: the note was stale (the MG pack now lists [Higuchi_2011] and [Zisimopoulou_2014]) and wrong (it gave Higuchi 2011 as Muscle Nerve, it is Ann Neurol 2011;69:418-422, and Zhang 2012 as Nature Communications, it is Arch Neurol).
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Scoped subtype synonyms added: double seronegative and LRP4 labels.
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG', 'double seronegative myasthenia gravis', 'double seronegative MG', 'LRP4 myasthenia gravis', 'LRP4 antibody positive myasthenia gravis', 'LRP4 MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 88.8 -> 86.8 kg, height 180 -> 178 cm, BMI 27.4 -> 27.4 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 86.8 kg, height 178 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.

## Library contradictions (25 Oct 2026)

- `perform_clinical_assessment {assessment_type: performance_status}`: Karnofsky 80, ECOG 1 (normal activity with effort; some signs and symptoms) (fallback_tool_outputs.clinical_assessment). Why: rule 1: the library reports Karnofsky 100 / ECOG 0 (no evidence of disease, working); rule 3: generalized MG with ocular, bulbar and deltoid fatigability, still working.
- `order_specialized_test {test_type: emg_ncs}`: normal nerve conductions and needle EMG, stating that neuromuscular transmission was not assessed (fallback_tool_outputs.specialized_test). Why: rule 1: the library report concludes there is no neuromuscular junction disorder, which routine conductions and needle EMG without repetitive stimulation cannot assess and which is not true here; the stored RNS study reports normal nerve conductions, which this report keeps.
- `order_specialized_test {test_type: polysomnography}`: moderate obstructive sleep apnoea off CPAP, controlled on CPAP, no hypoventilation (followup_outputs[4] request_polysomnography). Why: rule 2: obstructive sleep apnoea treated with CPAP (residual AHI below 5 on the download); the library reports no sleep-disordered breathing.
- `order_specialized_test {test_type: speech_language_evaluation}`: mild fatigable dysarthria from count 35; language normal (followup_outputs[5] request_speech_language_evaluation). Why: rule 3: the library reports no dysarthria; the examination documents dysarthria on counting to 50 and a hoarse voice.

Checks: perfect agent ok; case guards pass; criteria answers unchanged.
