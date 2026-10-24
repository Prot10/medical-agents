# MG-RM11
Reviewer status: none (condition not reviewed in this round; July 2026 tool review only) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| none | - | No reviewer notes for this case (`notes/MG.md` does not exist). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.clinical_history.medications` | Dexamethasone 40 mg days 1-4 listed as an "EPOCH component": EPOCH contains prednisone, not dexamethasone (and the drug check called it partial MG treatment). | FIXED: dexamethasone entry deleted; vincristine neuropathy added to the history (it was referred to throughout). |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.additional` | HPI ended with the oncologist's reasoning that the fatigable pattern pointed to the NMJ; exam held NIF -48 (the scored respiratory result, class K) and a synthesis sentence. | FIXED: neutral referral sentence; prior contrast MRI of brain and spine kept as history (not scored); NIF and synthesis removed; bedside nasal speech after counting kept. |
| B | minor | `patient.neurological_exam.cranial_nerves`, `.motor`, `.reflexes` | Diplopia on leftward gaze with "limited left eye adduction" (adduction is used on rightward gaze); reflexes repeated in the motor line. | FIXED: limited, fatigable left abduction; reflexes only in `reflexes` (ankle jerks absent from the neuropathy); toe extensor weakness for the peroneal CMAP. |
| A | minor | `patient.physical_exam` | No weight or height for mL/kg. | FIXED: 68.6 kg, 172 cm (BMI 23.2). |
| B | major | `initial_tool_outputs.labs` | Anti-titin row (not orderable; plan CENTRAL 7) used as a thymoma pointer; paraneoplastic Hu/Yo/SOX1 panel (no paraneoplastic panel in MG); TSH stub row "Ordered to exclude an alternative cause..." (class G); AChR range of another laboratory; percentages as strings. | FIXED: titin and paraneoplastic rows removed; TSH 1.9 and free T4 1.3; one laboratory's ranges; VGCC kept (LEMS is a real question with cancer and low reflexes); report-voice interpretation. |
| A | blocker | `ground_truth.action_criteria`, `initial_tool_outputs.specialized_test` | No RNS criterion and no RNS report although RNS is the first electrodiagnostic test; SFEMG required with expected evidence describing an RNS decrement. | FIXED: new required `action-repetitive-nerve-stimulation` with an initial RNS report: borderline decrement (nasalis 9%, trapezius 8%), normal CMAPs, no post-exercise facilitation, NCS with a length-dependent axonal sensory neuropathy (vincristine). SFEMG recommended (plan 3.5, RNS borderline). |
| C | major | `followup_outputs[request_emg_single_fiber]` | SFEMG of EDC, a limb muscle inside the territory of the vincristine axonal neuropathy, which itself raises jitter. | FIXED: SFEMG of the left orbicularis oculi (clinically weak, outside a length-dependent neuropathy), mean MCD 54 us, 14/20 pairs with increased jitter, blocking 8/20. |
| D | minor | `initial_tool_outputs.body_imaging` | "Consistent with lymphoma treatment response" (history in a CT report); management recommendations ("follow-up per oncology"). | FIXED: thymus and residual nodes described with comparison to the prior staging CT; no recommended actions; `region` "mediastinum, chest" (chest CT alternative served). |
| C | major | `followup_outputs[request_respiratory_function]` | FVC without % predicted or mL/kg, reference "> 3.0 L predicted"; MIP reference sign inverted. | FIXED: FVC 2.8 L (70%, 40.8 mL/kg), supine 2.6 L, MIP -48, MEP 71 (all flagged L), normal ABG, trend recommended. |
| D | major | `followup_outputs` (vincristine drug check, pre-IVIG labs, literature, MuSK/LRP4/VGCC) | Drug check with wrong facts (pyridostigmine "may worsen vincristine constipation"; dexamethasone "partial MG benefit") and a treatment suggestion; pre-IVIG IgA/IgG panel (class J); patient-specific literature with unverifiable sources ("corticosteroids problematic"); MuSK/LRP4 re-test in an AChR-positive case (H9). | FIXED: all deleted; one initial drug output in checker voice (vincristine no NMJ effect, pyridostigmine increases GI motility, EPOCH drugs no interaction, EPOCH prednisone and infection risk, fluoroquinolone prophylaxis and aminoglycosides to avoid, IVIG renal and thrombotic cautions) and one canonical literature output. Leak guard passes. |
| C | major | new criterion `action-ice-pack-test`; `metadata.actions_withdrawn` | Ice pack withdrawn in August for lack of a report; asymmetric fatigable ptosis is present. | FIXED: recommended criterion and report (left MRD1 0.5 to 3.0 mm); withdrawn entry removed. |
| C | major | `action_criteria` tiers, order, arguments | Template tiers (literature and generic drug check required, `screen_for`, exact query), labs requiring MuSK and LRP4 in an AChR-positive case, labels equal rationales. | FIXED: order respiratory (required, bulbar patient, plan 3.1 and 3.2), ice pack, labs `[anti_AChR, TSH]`, RNS, SFEMG, mediastinal CT (alternative chest CT), drug check (recommended, plan 3.2), literature (optional, last); schema arguments only; case rationales. |
| C | major | `sequence_constraints`, `stop_rule` | `labs -> SFEMG` with resource-stewardship wording; stop rule with literature and drug check, 0 extra actions. | FIXED: soft `labs -> SFEMG` and `RNS -> SFEMG`; stop rule respiratory, labs, RNS, CT; `max_additional_actions: 2`. |
| C | major | `assessment.required_recommendations` | Musts were tests and generic statements. | FIXED: pyridostigmine; IVIG 2 g/kg for bulbar weakness with reduced reserve; monitored bed with twice-daily FVC/MIP/MEP and the 20/30/40 ICU triggers; immunotherapy agreed with haematology (EPOCH prednisone continues, no thymectomy during stage IV lymphoma treatment); MG-safe febrile-neutropenia antibiotics. |
| C | minor | `assessment.prohibited_recommendations` | Template set with telithromycin, "pyridostigmine bridge", SFEMG before a functional label (not the mimic here). | FIXED: canonical drug and steroid prohibitions; mimic prohibition naming vincristine neurotoxicity and chemotherapy fatigue. The febrile-neutropenia antibiotic point moved to a must. |
| C | major | `ground_truth.differential` | Vincristine neuropathy alone and LEMS `moderate` after AChR, VGCC and RNS results; brainstem lymphoma "CSF not supportive" with no CSF in the case. | FIXED: vincristine neuropathy low, LEMS very_low, steroid myopathy low, fatigue very_low, leptomeningeal or brainstem lymphoma very_low (MRI), each with the excluding result. |
| C | minor | `key_clinical_evidence`, `red_herrings` | Template bullets; red herring relied on anti-titin; "dyspnea" not in the case. | FIXED: eight case-specific bullets; titin removed; field paths unchanged and valid. |
| C | minor | `avoided_actions[*]` | `[Wolfe_2016]` on every waste item; generic rationales. | FIXED: case rationales (CSF cytology not needed after a clean contrast MRI; PET and echo belong to the oncology schedule); citations emptied. |
| D | minor | `fallback_tool_outputs.ct` | Class F wording. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 57-year-old man with stage IV PTCL on DA-EPOCH and a vincristine neuropathy presents with fatigable ptosis, diplopia, nasal speech and proximal weakness. The pathway now reads: respiratory function first (required; FVC 2.8 L, 70%, 40.8 mL/kg, MIP -48, MEP 71 cmH2O, normal ABG), ice-pack test (recommended, positive on the left), AChR antibody with thyroid function (required; AChR binding 1.4 nmol/L, blocking and modulating raised, MuSK and VGCC negative), RNS with NCS (required, new report; borderline 8-9% decrement, no facilitation, and a length-dependent axonal sensory neuropathy), SFEMG of orbicularis oculi (recommended; abnormal jitter and blocking), mediastinal CT (required; no thymoma, shrinking residual nodes), a drug check (recommended; MG-unsafe antibiotics in febrile neutropenia, EPOCH prednisone) and literature (optional). Dexamethasone, the anti-titin and paraneoplastic rows and the treatment-style follow-ups are gone. Musts: pyridostigmine, IVIG 2 g/kg, monitored care with respiratory triggers, MG immunotherapy agreed with haematology, MG-safe antibiotics. LEMS and the oncological mimics are very low after the results.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys in text only: Jacob 2025, Narayanaswami 2021, Lawn 2001 (plan CENTRAL 1).
- Plan CENTRAL 7 (anti-titin not orderable) applied here: the titin row was removed.

## Open questions for Andrea (judgment calls you could not settle)

- None that need Andrea's information. Decisions recorded: (1) respiratory function is `required`, not `recommended` as the plan's 3.5 table says, because plan 3.2 makes it required when bulbar symptoms are present and the case reports reduced FVC and MIP, and the IVIG and level-of-care musts depend on it. (2) The SFEMG muscle was changed from EDC to orbicularis oculi because a length-dependent vincristine neuropathy can itself raise jitter in a distal limb muscle, which would make a limb SFEMG non-specific in this patient. (3) The label's "paraneoplastic in context of peripheral T-cell lymphoma" is kept (ROUND_POLICY 3); the case data support an association, not proof.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log and the whole final case. No reviewer notes exist for MG. Checked each own-finding row against the file: dexamethasone removed (EPOCH contains prednisone), NIF and synthesis removed from the exam, diplopia on leftward gaze now with limited left abduction (correct muscle), titin and paraneoplastic rows gone, TSH and free T4 with values, new RNS report with NCS showing the vincristine axonal neuropathy and no facilitation (ADM increment 11%), SFEMG in orbicularis oculi, respiratory values correct (FVC 2.8 L = 40.8 mL/kg at 68.6 kg, 70% of 4.0 L), BMI 23.2 matches, drug output in checker voice, musts specific (IVIG 2 g/kg, 20/30/40 ICU triggers, MG-safe febrile-neutropenia antibiotics, thymectomy deferred during stage IV lymphoma treatment).

Found and fixed:
- C minor, `ground_truth.differential[0]`: the HPI raises "vincristine-induced cranial neuropathy" as a mimic, but the entry covered only the peripheral neuropathy (ruling 7: a mimic the case raises must be in the differential or excluded). Renamed "Vincristine neurotoxicity alone (peripheral and cranial neuropathy)" with key features that say why the cranial form does not fit (fixed rather than fatigable ptosis and ophthalmoparesis, no ice-pack response) and "absent ankle reflexes" as on the exam.
- C minor, `ground_truth.differential[4]`: the HPI also raises opportunistic infection; key features now note he is afebrile (37.1 C) and the contrast MRI shows no lesion to suggest an opportunistic CNS infection.

Accepted as logged: respiratory function required (bulbar with reduced FVC and MIP), SFEMG recommended (RNS borderline), label and G70.01 left for CENTRAL. `perfect_agent.py MG-RM11 -v` passes, `case_io.py check` reports no failure naming the case, case guards pass.

## Condition audit (MG auditor, 24 Oct 2026)

- patient.neurological_exam.cranial_nerves: levator excursion replaced by MRD1 (left 0.5, right 2.5 mm) matching the ice-pack baseline. FIXED.
- `perfect_agent.py` and `case_io.py check` re-run on all 30 MG cases after the changes; the hand-run discriminator guard reports 0 defects in the 30 MG cases.

## Close-out (24 Oct 2026)

- `ground_truth.diagnosis.icd_codes[0]` G70.01 -> G70.00. ICD-10-CM G70.01 is myasthenia gravis with (acute) exacerbation, including crisis; this is a new or stable presentation, not an exacerbation. G70.01 stays accepted as a secondary code (plans/MG-decisions.md, Q2).
- Synonyms (G70 entries rescoped): "ocular myasthenia gravis" removed (this is generalized MG); "generalized MG" and "generalised MG" added; bare "MG" retired (a one-token label matched any text mentioning MG).
- Result: accepted = ['myasthenia gravis', 'autoimmune myasthenia', 'generalized myasthenia gravis', 'generalised myasthenia gravis', 'generalized MG', 'generalised MG']; icd_codes = ['G70.00', 'G70.0', 'G70.01']. Applied with `apply_diagnosis_synonyms.py --prune --conditions myasthenia_gravis`; `--check` clean; perfect-agent and case guards pass.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
