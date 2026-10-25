# MG-RM13
Reviewer status: none (condition not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none | - | No reviewer notes for this case (`notes/MG.md` does not exist). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness` | HPI said a PET-CT "showed no cancer recurrence", contradicting the PET follow-up that shows a new avid node; em dash in the text. | FIXED: PET mention removed; the last surveillance CT (3 months ago, post-radiation change only) and last month's brain MRI (no metastases) kept as history; parentheses instead of the dash. |
| D | major | `patient.neurological_exam.additional` | NIF -65 in the exam (scored respiratory value, class K); template line "Erectile dysfunction not applicable" in a woman. | FIXED: both removed; neutral line on dry mouth and no orthostatic symptoms. |
| C | minor | `patient.neurological_exam.motor`, `.reflexes` | Motor line called the weakness "fatigable" and repeated the reflexes; reflex line did not describe post-exercise facilitation. | FIXED: hip flexors 3+/5, deltoids 4-/5, brief improvement after effort; reflexes trace/absent, patellar 1+ after 10 s contraction. |
| A | minor | `patient.physical_exam` | No weight or height. | FIXED: 63.5 kg, 162 cm. |
| B | major | `initial_tool_outputs.labs` | Qualitative CBC/BMP stubs, a TSH stub (class G), anti-Hu row (paraneoplastic panel, plan: LEMS keeps only VGCC and SOX1), mixed laboratory ranges, interpretive essay. | FIXED: CBC and BMP with values (calcium, magnesium), TSH 2.2 and free T4 1.3 on levothyroxine, VGCC 0.48 nmol/L, SOX1 positive, AChR and MuSK negative with one laboratory's ranges; Hu removed; report-voice interpretation. |
| B | major | `initial_tool_outputs.specialized_test` | RNS framed as 50 Hz with a ">100%" threshold (plan fact 8: 10 s exercise, 60% cut-off); essay text; sural neuropathy attributed to a cause. | FIXED: technique row; low CMAPs in four nerves, 3 Hz decrement ADM 16% and deltoid 12%, post-exercise increments 139-157% (ADM 2.1 to 5.4 mV, deltoid 0.9 to 2.2 mV); reduced sural SNAPs described without attribution; numbered impression. |
| C | major | `initial_tool_outputs.body_imaging` | CT text argued about CT sensitivity and gave management recommendations; no finding that makes the PET step needed. | FIXED: region "chest, mediastinum"; stable post-radiation fibrosis and a new 1.2 x 0.9 cm right paratracheal node (station 4R), indeterminate; recommendation limited to FDG-PET. Fallback head-CT impression set to the plan's canonical text. |
| B | major | `followup_outputs[request_pet_ct]` | Modality not the vocabulary value; impression not stated as a report. | FIXED: modality FDG_PET, trigger `request_fdg_pet`; 4R node SUVmax 6.8, treated site 2.2, no distant disease; "suspicious for malignant lymphadenopathy, tissue sampling recommended". |
| A | major | `followup_outputs` (biopsy under `interpret_labs`) | Node histology served as a lab result (class H, wrong tool). | FIXED: `obtain_tissue_diagnosis` follow-up, procedure `lymph_node_biopsy`, EBUS-TBNA of station 4R; small cell carcinoma, TTF-1, synaptophysin and chromogranin A positive, Ki-67 about 90%. New recommended criterion `action-node-biopsy`. |
| C | minor | `followup_outputs[request_autonomic_evaluation]` | Test type not in the vocabulary; essays without values. | FIXED: `autonomic_testing`; QSART, HRDB, Valsalva ratio and tilt with values; numbered impression. Criterion set to optional. |
| C | minor | `followup_outputs[request_emg_single_fiber]` | No pair counts. | FIXED: EDC stimulated SFEMG, MCD 78 us at 2 Hz with 8/20 blocking, falling at 10 Hz. Criterion kept optional. |
| C | minor | `followup_outputs[request_respiratory_function]` | Respiratory follow-up in a patient with no dyspnoea or bulbar respiratory signs; no criterion used it. | FIXED: deleted. |
| C | major | `initial_tool_outputs.drug_interactions`, `action-7` | Drug check did not address ondansetron, which is QT-prolonging and contraindicated with amifampridine (EU SmPC); no dosing or seizure warning. | FIXED: one initial output keyed `amifampridine`: ondansetron contraindication, seizure threshold, ECG at start and after titration, EU dosing, NMJ drug list; lisinopril and levothyroxine no interaction. Criterion required, argument `{drug: amifampridine}`. |
| C | major | `initial_tool_outputs.ecg`, `fallback_tool_outputs.ecg` | No ECG in the pathway although amifampridine needs a baseline ECG; fallback ECG answered from the library. | FIXED: initial ECG (sinus 78, QTc 441 ms) with a new required criterion `action-ecg-before-amifampridine`; fallback ECG set to null and removed from `metadata.fallback_tool_kinds`. |
| D | major | `initial_tool_outputs.literature_search`, `action-6` | Literature output repeated expected evidence (leak guard failed); exact-query argument made the criterion unreachable; required tier. | FIXED: plan's canonical LEMS text as the one initial output; criterion optional, `{}` arguments, last. Leak guard passes. |
| C | major | `action_criteria`, `sequence_constraints`, `stop_rule` | Labs criterion did not name SOX1; CT accepted only one study; template tiers and constraints; stop rule included literature. | FIXED: order labs `[anti_VGCC_PQ, anti_SOX1]`, RNS, SFEMG (optional), autonomic (optional), CT (chest CT, CAP CT or mediastinal CT with contrast), PET (required), biopsy, ECG, drug check, literature; soft CT -> PET, CT -> biopsy, ECG -> drug check; stop rule labs, RNS, CT, PET, ECG, drug check with 2 extra actions. |
| C | major | `assessment.required_recommendations`, `.prohibited_recommendations` | Musts were tests and generic MG text; telithromycin in the prohibitions; no oncology step. | FIXED: urgent thoracic oncology referral, stop ondansetron then titrate amifampridine after the ECG, pyridostigmine add-on and IVIG if disabling, drug list and anaesthetic warning for EBUS, early palliative care. Prohibitions: not MG, no amifampridine with QT-prolonging drugs or epilepsy, canonical drug prohibition, CT alone does not exclude recurrence. |
| C | minor | `ground_truth.differential`, `key_clinical_evidence`, `red_herrings` | MG not very_low after the results; carboplatin neuropathy missing; template evidence bullets. | FIXED: MG very_low; carboplatin neuropathy alone added (very_low); other mimics very_low with case reasons; five case bullets; CT red herring reworded. |
| C | minor | `avoided_actions[*]` | Same citation on every waste item. | FIXED: case rationales, citations emptied. |

## Changes, in one paragraph a physician can read before re-reviewing

A 68-year-old woman, 6 months after chemoradiation for limited-stage SCLC, has proximal leg weakness, reflexes that facilitate after effort, dry mouth and mild ocular-bulbar symptoms. The pathway now reads: VGCC and SOX1 antibodies (required; VGCC 0.48 nmol/L, SOX1 positive, AChR and MuSK negative, thyroid normal on levothyroxine), RNS with a post-exercise study (required; low CMAPs, 12-16% decrement, 139-157% facilitation), SFEMG and autonomic testing (optional), contrast chest CT (required; only a new indeterminate 0.9 cm short-axis paratracheal node), FDG-PET (required; node SUVmax 6.8, no distant disease), EBUS sampling of station 4R (recommended; small cell carcinoma), baseline ECG (required; QTc 441 ms), the amifampridine check (required; ondansetron is a contraindication) and literature (optional). The biopsy is now a tissue result, the respiratory follow-up is gone. Musts: urgent oncology referral, stop ondansetron and titrate amifampridine with ECG monitoring, pyridostigmine or IVIG as add-ons, drug list including for the EBUS anaesthetic, early palliative care.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys in text only: Titulaer 2011, EFNS 2011 (Titulaer Eur J Neurol 2011), Oh 2005 (plan CENTRAL 1).

## Open questions for Andrea (judgment calls you could not settle)

- None that need Andrea's information. Decisions recorded: (1) FDG-PET is `required`, not `recommended` as the plan's table says: the CT is deliberately equivocal and plan 3.5 and EFNS 2011 make PET the next step when CT does not show the tumour, so a work-up that stops at the CT misses the recurrence. (2) The DELTA-P score was not used in the text because the SCLC is already known. (3) A baseline ECG is a new required criterion because the EU SmPC asks for it at initiation and the patient takes ondansetron.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log and the whole final case. No reviewer notes exist for MG. Checked each own-finding row against the file: the HPI no longer says a PET showed no recurrence; NIF and the "erectile dysfunction" template line are gone; reflex facilitation described; labs with values and one laboratory's ranges, Hu removed; RNS with the 10 s exercise protocol (increments recomputed: ADM 2.1 to 5.4 mV = 157%, APB 1.8 to 4.3 mV = 139%, deltoid 0.9 to 2.2 mV = 144%); CT with an indeterminate subcentimetre 4R node; FDG_PET and autonomic_testing discriminators; biopsy as `obtain_tissue_diagnosis`; amifampridine output matches the EU SmPC (15 mg/day in three doses, 5 mg steps every 4-5 days, maximum 60 mg/day and 20 mg per dose; QT-prolonging drugs, epilepsy, congenital long QT contraindicated); ECG QTc 441 ms; musts and prohibitions consistent with ondansetron being stopped first. The CT's FDG-PET suggestion and the PET's tissue-sampling suggestion are further diagnostic steps, which the style guide allows.

Found and fixed:
- B minor, `patient.clinical_history.past_medical_history[0]`: "diagnosed 8 months ago" with 4 cycles of carboplatin/etoposide plus thoracic radiation completed 6 months ago leaves about 2 months for a course that takes about 3 months from the first cycle. Changed to "diagnosed 10 months ago".
- C minor, `ground_truth.action_criteria[action-1-interpret-labs]`: required panels were `[anti_VGCC_PQ, anti_SOX1]`. SOX1 is valuable to predict an associated SCLC, but here the SCLC is already known and histology will be obtained, so SOX1 changes nothing; an agent ordering VGCC alone should not miss a required criterion. Required panels now `[anti_VGCC_PQ]` (subset matching still accepts an order that adds SOX1); label and rationale updated; the SOX1 result stays in the report and the expected evidence. This departs from the plan's LEMS tier table for this case only; P02 (new tumour) is not affected.
- N minor, `action-1-interpret-labs.citations`, `action-2-order-specialized-test.citations`: `[Gilhus_2016]` (an MG review) was cited for LEMS serology and post-exercise facilitation. Emptied; the rationales already cite Titulaer 2011 and Oh 2005 in text (plan 1.1: cite by author until CENTRAL adds the keys).
- C minor, `followup_outputs[request_emg_single_fiber]`: the stimulated SFEMG used the voluntary-activation EDC reference (<34 us). Now "<25 us (stimulated)".

Accepted as logged: FDG-PET required (CT deliberately equivocal), node biopsy recommended, ECG required before amifampridine. `perfect_agent.py MG-RM13 -v` passes, `case_io.py check` reports no failure naming the case, case guards pass.

## Condition audit (MG auditor, 24 Oct 2026)

- required_recommendations[1] and initial_tool_outputs.drug_interactions.amifampridine.warnings[1]: ECG 'after titration' replaced by 'at initiation and yearly thereafter' (EU SmPC 4.4), as in P02. FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- LEMS synonyms: "paraneoplastic lambert eaton myasthenic syndrome" and "LEMS with small cell lung cancer" added (G73.1 entry; summary CENTRAL 3). Codes unchanged (G73.1, G70.80). LEMS stays in the MG condition as its classic mimic (plans/MG-decisions.md, Q1).
- Result: accepted = ['lambert eaton myasthenic syndrome', 'lambert-eaton myasthenic syndrome', 'LEMS', 'lambert eaton syndrome', 'paraneoplastic lambert eaton myasthenic syndrome', 'LEMS with small cell lung cancer']; icd_codes = ['G73.1', 'G70.80']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.

## Weight and height (25 Oct 2026)

- `patient.demographics`: weight 58.1 -> 63.5 kg, height 155 -> 162 cm, BMI 24.2 -> 24.2 (the prompt shows height, weight and BMI).
- Why: rule 1: patient.physical_exam.general states weight 63.5 kg, height 162 cm.
- The FVC mL/kg figures and the weight-based IVIg amounts in the text were checked against this weight: all within rounding, no text change.

Checks: `perfect_agent.py` ok; BMI = weight / height^2 to one decimal.
