# MG-S05
Reviewer status: none (MG not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none: no reviewer notes for this case | - | - |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | minor | `patient.neurological_exam.cranial_nerves`, `physical_exam.neurological`, ice pack follow-up | Exam gave levator excursion while the ice pack test reads MRD1 (pre-test MRD1 0 mm); the two measures were not reconciled. | FIXED: exam MRD1 right 0.5 mm, left 4 mm; ice pack MRD1 0.5 to 3.5 mm (3.0 mm), technique wording standardised ("at room temperature" removed). |
| B | major | `initial_tool_outputs.labs` | Two laboratories (AChR binding < 0.4 and blocking < 25% against MuSK <= 0.02); MuSK in an AChR-positive patient; CBC and BMP "All indices within normal limits" (plan fact 2, H9, G). | FIXED: one laboratory (AChR binding <= 0.02 nmol/L, blocking <= 15%); MuSK removed; CBC and BMP analytes with values; values kept (2.9 nmol/L, 34%, TSH 1.7, free T4 1.1, CK 112). |
| A | major | `ground_truth.action_criteria[action-3-order-specialized-test]`, `followup_outputs` | RNS required alone and normal (as is typical of ocular MG) with no SFEMG available; expected evidence was a teaching sentence (plan 3.5 ocular pathway). | FIXED: one required neurophysiology criterion with alternatives RNS and SFEMG; SFEMG follow-up added (right frontalis, mean MCD 58 microseconds, jitter 9/20, blocking 3/20); expected evidence states both results. |
| D | major | `followup_outputs[search_ocular_mg_management]`, `[check_mg_drug_interactions]` | Literature with telithromycin as current, "CT chest recommended in all", and a drug check for a patient with no medicines whose `proposed` is a slug (plan B, C). | FIXED: both deleted with their criteria (plan: no medicines, literature deleted in S cases); library answers any search or check. |
| A | major | `ground_truth.action_criteria` | Labs required `[anti_AChR, anti_MuSK, TSH]`; literature and drug check required; labels equal to rationales; `[Wolfe_2016]` everywhere. | FIXED: labs `[anti_AChR, TSH]`; criteria labs, ice pack (recommended), neurophysiology, mediastinal CT (alternatives mediastinum_MRI and chest_CT, served by library normal reports consistent with this normal CT); case-specific text; citations to Jacob/Evoli in text. |
| B | minor | `ground_truth.sequence_constraints`, `stop_rule` | Constraint `labs -> ice pack` with an SFEMG reason; literature and drug check required before assessment; `max_additional_actions: 0`. | FIXED: constraint deleted (SFEMG is an alternative inside the required neurophysiology criterion, so a labs-before-SFEMG constraint would also bind RNS); stop rule labs, neurophysiology, CT; `max_additional_actions: 1`. |
| C | major | `ground_truth.assessment.required_recommendations` | All musts were diagnostic steps (confirm AChR, ice pack, CT, document normal RNS) apart from counselling; no treatment (plan D). | FIXED: pyridostigmine titration; low-dose prednisone if not controlled (Sanders 2016), with the generalization note hedged as observational; generalization counselling with surveillance and red-flag symptoms; occlusion for diplopia; drug list. No thymectomy must (ocular, no thymoma). |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | Telithromycin and separate template drug prohibitions. | FIXED: canonical steroid and drug prohibitions; the normal-RNS prohibition kept and reworded. |
| C | major | `ground_truth.differential` | "Generalized MG (risk of generalization)" listed as a differential diagnosis; thyroid eye disease left moderate after normal TFTs and no proptosis; microvascular third nerve palsy said the presentation is "bilateral" (it is a right ptosis with right adduction deficit, the pattern that does mimic a partial third nerve palsy) (ruling 7). | FIXED: generalization entry removed (it is a prognosis; kept in key evidence and musts); TED low; third nerve palsy key features rewritten from the case data. |
| C | minor | `ground_truth.key_clinical_evidence[0,3,5]` | RNS sensitivity figure, "CT chest required in ALL", telithromycin. | FIXED: SFEMG as the sensitive test when RNS is normal; canonical mediastinal sentence; current drug list. |
| E | minor | `ground_truth.avoided_actions[*]` | `[Wolfe_2016]` citations. | FIXED: emptied, case rationales with Jacob 2025 in text. |
| D | minor | `fallback_tool_outputs.ct.impression` | "does not address the question" (plan F). | FIXED: plain normal head CT. |
| E | minor | `metadata` | Difficulty rationale counted literature and drug check. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 39-year-old man with ocular AChR-positive MG (class I). The work-up is AChR antibody with thyroid function (one laboratory; binding 2.9 nmol/L, blocking 34%; MuSK no longer reported; normal TSH and free T4), the ice pack test (right MRD1 0.5 to 3.5 mm, now matching the exam, which gives MRD1 instead of levator excursion), neurophysiology as one required step that RNS or SFEMG satisfies (RNS normal as is typical in ocular MG; a new SFEMG report shows increased jitter in the frontalis), and contrast mediastinal CT (normal). Literature and the drug check (he takes no medicines) are no longer criteria. Musts are now treatment and follow-up: pyridostigmine titration, low-dose prednisone if symptoms persist, counselling on the risk of generalization with surveillance and red flags, occlusion for diplopia, drug counselling; no thymectomy. "Generalized MG" is no longer listed as a differential diagnosis, thyroid eye disease is low, and the third nerve palsy entry reflects the right ptosis with right adduction deficit.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 1: `[Jacob_2025]`, `[Evoli_2019]` in text only.
- Plan CENTRAL 3: synonyms accept "generalized myasthenia gravis" for this ocular case, so the ocular/generalized distinction is not scored. `icd_codes[0]` is already G70.00 here.

## Open questions for Andrea (judgment calls you could not settle)

- None.

## Verification

Adversarial check, 24 Oct 2026. Read the log, the full diff and the final case. Confirmed: MRD1 consistent across exam, physical exam, ice pack report and expected evidence; right adduction deficit with left-gaze diplopia consistent and correctly used in the third nerve palsy entry; one laboratory; neurophysiology criterion with RNS and SFEMG alternatives both served; constraint removal reasoned (it would bind RNS); musts are management only and fit ocular MG (no thymectomy); generalization removed from the differential; leak guard passes; `icd_codes[0]` already G70.00.

Found and fixed:
- D minor: `fallback_tool_outputs.advanced_imaging.modality` was the prose "MRA head and neck" (PATTERNS 5). Set to the vocabulary value `MR_angiography`, with findings in report voice (normal circle of Willis, no aneurysm including the posterior communicating origins, normal cervical arteries), since a third nerve palsy mimic is in the differential and an MRA order is plausible.
- C minor: no thyroid antibodies (July 2026 guidance: in all patients; thyroid eye disease is the main mimic here). Added anti-TPO 9 IU/mL (normal) to the thyroid panel, interpretation and expected evidence; required arguments unchanged.
- E minor: em dash in the rewritten `neurological_exam.cranial_nerves` sentence replaced by a comma.

perfect_agent passes; case_io check clean for this case.

## Condition audit (MG auditor, 24 Oct 2026)

- fallback_tool_outputs.echo.echo_type set to TTE. FIXED.
  Why: the discriminator guard (PATTERNS.md section 5) requires an exact vocabulary value on every case fallback; an empty echo_type answered every echo variant. The RS11-RS16 verifiers fixed this only in their own cases.
- initial_tool_outputs.body_imaging.region 'mediastinum' -> 'chest, anterior mediastinum' so the chest_CT alternative gets the case's own CT chest report (as S01-S04). FIXED.
  Why: perfect_agent warned that chest_CT fell back to a library normal report for this case.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- Synonyms (G70 entries rescoped): "generalized/generalised myasthenia gravis" removed (this is ocular MG, MGFA class I); "ocular myasthenia" and "ocular MG" added; bare "MG" retired.
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'ocular myasthenia gravis', 'ocular myasthenia', 'ocular MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.
