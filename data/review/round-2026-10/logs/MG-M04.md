# MG-M04
Reviewer status: R1 not reviewed, R2 not reviewed (no notes file for MG) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. The physician input is the July 2026 tool guidance for myasthenia_gravis, applied through the condition plan (crisis pathway, plan 3.5). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `ground_truth.action_criteria` (`action-4-order-specialized-test`) | RNS required "to confirm NMJ worsening" in known AChR-positive MG in impending crisis (plan 3.5: not indicated, delays treatment). | FIXED: criterion deleted; RNS and SFEMG added as waste avoided actions (`avoid-waste-7-rns`, `avoid-waste-8-sfemg`). The stored RNS report is kept as data (recommended actions removed, impression numbered) so an RNS order is not answered by a contradictory normal library report. |
| C | major | `ground_truth.action_criteria` (`action-5-order-body-imaging`) | Mediastinal CT required "repeat indicated with acute exacerbation"; the history documents negative thymic CT 6 and 3 years ago and the precipitant is explained. | FIXED (plan 3.5 rule, worker choice logged): optional, with chest_CT alternative; report kept, region "mediastinum chest". |
| A | major | `action-1-interpret-labs` | Labs required AChR, TSH and urinalysis "with culture" as one order; AChR repeat not needed in known MG. | FIXED: required alternatives `["CBC","CMP"]` or `["CBC","BMP"]`; magnesium and phosphate added to the stored panel (normal); panel keys renamed "CBC (complete blood count)" and "CMP (comprehensive metabolic panel)" so the set-valued order guard sees the ordered assays. AChR rows stay in the report but are not scored. |
| B | major | `initial_tool_outputs.labs.panels["Urinalysis"]` (urine culture row), new `initial_tool_outputs.microbiology` | Plan H8: urine culture inside labs ("Pending, E. coli growth at 24h"). | FIXED: row removed; `order_microbiology` urine report: E. coli >100,000 CFU/mL collected on day 4 of ciprofloxacin (`collected_before_antimicrobials` false), ciprofloxacin and amoxicillin resistant, nitrofurantoin, fosfomycin, TMP-SMX, cefalexin susceptible; new recommended criterion `action-urine-culture`. |
| B | major | `followup_outputs` (`request_drug_interactions_ciprofloxacin_mg`) | Wrong fact "ciprofloxacin inhibits xanthine oxidase, increasing azathioprine levels"; telithromycin listed; pivmecillinam (a penicillin) offered to a penicillin-allergic patient; `proposed` a narrative. | FIXED: moved to `initial_tool_outputs.drug_interactions["ciprofloxacin"]`; checker voice: fluoroquinolone boxed warning, metoprolol caution, ciprofloxacin dysglycemia with metformin, TMP-SMX with azathioprine myelosuppression; contraindications include the penicillin allergy; alternatives nitrofurantoin, fosfomycin, TMP-SMX. |
| D | major | `followup_outputs` (`request_literature_search_mg_drug_exacerbation`) | Unverifiable sources ("Neurology 2020 / FDA", "J Neurol 2019 systematic review"), "NIF >-30" threshold, patient-specific antibiotic advice. | FIXED: deleted; one initial literature output with the FDA 2011 boxed warning, Sanders 2016 and Lawn 2001, general wording. Criterion optional, last. |
| D | major | `patient.neurological_exam.additional`, `patient.history_present_illness` | Bedside NIF -32 in the exam (the scored result) and baseline NIF -52 in the HPI (class K). | FIXED: both numbers removed; the baseline now appears only as a same-modality comparison inside the respiratory report; weak cough added. |
| B | major | `followup_outputs` (`request_respiratory_function`) | "FVC 1.6 L ... below 20 mL/kg threshold" without a weight (1.6 L is 24 mL/kg at her weight); management wording. | FIXED: `physical_exam.general` "Weight 66 kg, height 158 cm" (BMI 26.4); FVC 1.60 L (56%, 24 mL/kg), MIP -32 (previous -52), MEP 38, single-breath count 15, ABG; impression in report voice. |
| B | minor | `patient.clinical_history.past_medical_history` | "Type 2 diabetes mellitus (diet-controlled)" while she takes metformin. | FIXED: "(on metformin)". Em dashes in medication indications replaced by commas. |
| C | major | `ground_truth.assessment.required_recommendations` | IVIG/PLEX only "as rescue if worsening continues" although MEP 38 and MIP -32 with bulbar weakness meet impending-crisis criteria; "Serial AChR antibody levels" must; tool names in musts ("via check_drug_interactions"). | FIXED: seven musts: stop ciprofloxacin; nitrofurantoin or fosfomycin per susceptibility (non-penicillin); ICU or HDU with 4-6-hourly FVC/MIP/MEP and intubation thresholds; IVIG 2 g/kg or PLEX now; no further pyridostigmine escalation (hold if intubated), continue azathioprine and prednisone with any increase under monitoring; nil by mouth for thin liquids until swallow assessment; replace metoprolol. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | Telithromycin; "Do NOT delay respiratory assessment" (a process line); no penicillin prohibition. | FIXED: no fluoroquinolone; no aminoglycoside, macrolide or IV magnesium; no penicillin (rash); no attribution to the UTI alone; reduced-dose NMB with monitoring if intubated. |
| C | minor | `ground_truth.differential` | Sepsis-driven worsening and spontaneous progression left moderate after the work-up; cholinergic crisis not considered although she self-escalated pyridostigmine. | FIXED: both low with reasons; new "Cholinergic crisis" low (300 mg/day, no muscarinic signs); crisis entry and LEMS key features reworded. |
| E | major | `ground_truth.key_clinical_evidence`, `red_herrings` | Engineering text ("must immediately trigger check_drug_interactions, this is the load-bearing tool call"; "check_drug_interactions confirms"). | FIXED: six clinical lines; red-herring texts rewritten without tool names. |
| C | major | `ground_truth.sequence_constraints`, `stop_rule` | `respiratory -> drug check` constraint; stop rule with RNS, CT and literature; max 0. | FIXED (plan): `respiratory -> mediastinal CT` soft; stop rule respiratory, drug check, labs; max 2. |
| D | minor | `fallback_tool_outputs.ct` | Class F wording. | FIXED: plain normal head CT. |
| C | minor | `ground_truth.avoided_actions[*]` | `[Wolfe_2016]` cited for waste. | FIXED: case rationales, Jacob 2025 in text, citations empty. |

## Changes, in one paragraph a physician can read before re-reviewing

A 60-year-old woman with known AChR-positive generalized MG (on pyridostigmine, prednisone 10 mg, azathioprine, metoprolol, metformin; penicillin allergy) whose weakness, ptosis, dysarthria and dysphagia worsened 24-36 hours after ciprofloxacin for cystitis. The pathway is now the crisis pathway: respiratory function first (FVC 56%, 24 mL/kg; MIP -32 from -52; MEP 38 cmH2O), the ciprofloxacin drug check (boxed warning, metoprolol caution, safe non-penicillin alternatives), blood count and metabolic panel with electrolytes (mild leukocytosis, CRP 28, normal procalcitonin, normal K, Mg, phosphate), and a urine culture (ciprofloxacin-resistant E. coli, nitrofurantoin and fosfomycin susceptible). RNS and SFEMG are waste; mediastinal CT is optional because thymic imaging was negative twice. Musts: stop ciprofloxacin, nitrofurantoin or fosfomycin, ICU or HDU with intubation thresholds, IVIG or PLEX now, no further pyridostigmine escalation, continue immunosuppression, nil by mouth for thin liquids until assessed, replace metoprolol. Cholinergic crisis is added as a low-likelihood alternative; sepsis and spontaneous progression are low.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- `icd_codes[0]` G70.01 fits this exacerbation (plan CENTRAL 2); synonyms could add "myasthenic exacerbation" / "fluoroquinolone-induced exacerbation of myasthenia gravis" (plan CENTRAL 3).
- Guidance claims: mediastinal CT is optional in this case (plan CENTRAL 5).
- Criteria pack keys `[Jacob_2025]`, `[Lawn_2001]` (named in text only).
- An SFEMG order is answered by the library's normal SFEMG, which a severe AChR-positive exacerbation would not produce; it is a waste avoided action here, so no case output was authored for it.

## Open questions for Andrea (judgment calls you could not settle)

None. The mediastinal CT tier (plan 3.5 leaves M04 to the worker) was set optional because the history documents two negative thymic CTs and the deterioration has an explained precipitant.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the plan (M04 entry, crisis pathway 3.5), the diff and the whole final case. No notes file exists for MG. Every FIXED finding is in the file: RNS criterion deleted and RNS/SFEMG added as waste (the stored RNS report kept as data, consistent with known AChR+ MG); respiratory required first (1.60 L / 66 kg = 24 mL/kg, BMI 66/1.58^2 = 26.4, MIP -32 from -52 shown only as a same-modality comparison, so the HPI no longer leaks it); ciprofloxacin drug check required in checker voice (boxed warning, metoprolol caution, the xanthine-oxidase/azathioprine error and telithromycin gone, penicillin allergy listed); labs required as CBC with CMP or BMP, with magnesium and phosphate; urine culture moved to `order_microbiology` (ciprofloxacin-resistant E. coli, collected on day 4 of ciprofloxacin, `collected_before_antimicrobials` false, consistent); mediastinal CT optional with the reason (negative thymic CT 6 and 3 years ago, explained precipitant); constraint respiratory -> mediastinal CT soft; stop rule respiratory, drug check, labs. Musts: nitrofurantoin or fosfomycin match the susceptibilities and the penicillin allergy, creatinine 0.9 allows nitrofurantoin; ICU thresholds per fact 15; IVIG or PLEX now (MEP 38, MIP -32 with bulbar weakness). Cholinergic crisis low is consistent with the HPI (self-increase to five doses after the weakness began, no muscarinic signs, pupils 3 mm, HR 84). The old PMH "diet-controlled" diabetes contradiction with metformin is fixed.

Found: nothing requiring a change. The plan's mediastinal CT tier choice is the worker's and is sound.

Checks: `perfect_agent.py MG-M04 -v` passes, `case_io.py check` clean for the case, case guards pass.

## Close-out (24 Oct 2026)

- `icd_codes[0]` G70.01 kept (exacerbation or crisis). G70.00 ("without exacerbation") is no longer accepted; crisis and exacerbation labels added (myasthenic crisis, myasthenic exacerbation, impending myasthenic crisis, MG crisis, MG exacerbation): the case is an impending or established crisis and its differential rates crisis high.
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'myasthenic crisis', 'myasthenic exacerbation', 'impending myasthenic crisis', 'MG crisis', 'MG exacerbation', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.01', 'G70.0']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Matcher fix (25 Oct 2026)

The lab matcher now keeps a urine or CSF row out of a blood order: a urinalysis, urine sodium or urine osmolality row answers only an order that names the urine assay, so a CBC or CMP order no longer returns the urine results. The lab criterion therefore names the urine assays its expected evidence cites.

- `ground_truth.action_criteria[action-1-interpret-labs]`: new first alternative `{panels: ['CBC', 'CMP', 'urinalysis']}` (adds `urinalysis`); the previous orders stay as alternatives, so every call that matched before still matches. The expected evidence reads pyuria with positive nitrite (the label already names the urinalysis), which the first order received only through two matcher defects fixed on 25 Oct 2026: a urine row answered a blood-count or metabolic order (`Urine WBC` as WBC, `Urine sodium` as sodium, a urine creatinine ratio as creatinine), and the unit `mg/dL` read as magnesium. Scoring: cost reference only (the policy's reference order is fuller); coverage unchanged.

## Engineering text (25 Oct 2026)

Review-process wording (references to the round's rulings, the round policy file, the criteria packs, and tier markers such as "(optional)" in criterion labels and rationales) is shown to physicians in the review app, so it was rewritten in clinical language. The tier stays in the criterion's `importance` field; scoring is unchanged. `test_case_guards.py::test_no_review_process_text` now fails on any of it.

- criterion `action-6-search-medical-literature` label: "Literature on fluoroquinolones and MG exacerbation (optional)" -> "Literature on fluoroquinolones and MG exacerbation"
