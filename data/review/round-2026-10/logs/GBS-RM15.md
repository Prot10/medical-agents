# GBS-RM15
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| e89ffe81-0d83-4cdc-a95b-78daf43baa89 | FIXED (route: positive antibody, per plan) | Of the reviewer's options I took "make at least one ganglioside antibody positive": the ganglioside follow-up (renamed `request_anti_gq1b_gt1a_ganglioside_panel`) now reports anti-GQ1b IgG positive 1:320 (GT1a negative, GM1 row dropped), which places acute bilateral ptosis with areflexia in the anti-GQ1b antibody syndrome, an incomplete form of Miller Fisher syndrome listed by Wakerley 2014. `diagnosis.accepted[0]` "Anti-GQ1b antibody syndrome (acute bilateral ptosis with areflexia), Guillain-Barré syndrome spectrum" (G61.0 kept). Myasthenia gravis lowered from high to low with the case's reasons; AChR/MuSK/LRP4 moved out of the routine labs into a new recommended criterion `action-10-interpret-labs-anti-achr-musk-lrp4` with its own follow-up; RNS and single-fibre EMG stay in the NCS report; edrophonium follow-up deleted (unsafe, superseded). Brain MRI moved from `order_advanced_imaging` to `initial_tool_outputs.mri` with recommended `action-11-analyze-brain-mri` (midbrain lesion); brain MRI removed from waste. The ganglioside step's own criterion is BLOCKED on the vocabulary (plan CENTRAL 1); the follow-up is probed reachable when the order names GQ1b or ganglioside. |
| e62f0ba4-b211-41b2-a224-f289d6b4436a | FIXED | "Initiate IVIG / plasma exchange if GBS variant confirmed" deleted. Must 1: admit for monitoring without IVIg or PE while deficits stay restricted (EAN/PNS: not routinely advised in MFS-spectrum disease); must 2 defines when to treat (limb weakness, bulbar or respiratory involvement) and what to monitor; pearl 4 restates it. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| D | major | `patient.history_present_illness` | Exam findings and reasoning in the HPI ("eye movements are fully intact", "The initial concern was myasthenia gravis ... global areflexia is present on exam"), em dashes. | FIXED: history only. |
| B | minor | `patient.neurological_exam.additional`, `cranial_nerves`, `reflexes` | Spirometry and repeated history in `additional`; capitals "FULL", "NO"; em dashes. | FIXED: `additional` removed (fatigability on upgaze moved to cranial nerves); text normalised. |
| C | major | `ground_truth.assessment` | Musts were diagnostic orders (ganglioside panel, ice pack, AChR, RNS, MRI) and a conditional immunotherapy; MG prohibition generic. | FIXED: four management musts (monitor without immunotherapy, overlap monitoring with treatment trigger, telemetry, prognosis and support); prohibitions: canonical steroid text, no pyridostigmine/MG treatment with the reasons. |
| C | major | `initial_tool_outputs.labs` | Serology (Campylobacter, EBV), HIV with the leaky sentence; MG antibodies served with routine labs; no CMP or CK. | FIXED: serology and HIV removed; MG antibodies in their own follow-up (AChR interpretive comment hedged); CMP, CK and platelets added (normal). |
| A | major | `followup_outputs` | Brain MRI under `order_advanced_imaging`; edrophonium "specialized test"; empty literature and DDI placeholders (C9). | FIXED: MRI moved to `analyze_brain_mri`; others deleted; optional `action-12-order-specialized-test-ice-pack` with a negative ice pack follow-up added for the bedside MG test the old must asked for. |
| C | minor | `followup_outputs[4]` (respiratory) | "All values within normal limits" though MIP -48 cmH2O is below reference for a woman; no weight, no MEP. | FIXED: weight 63 kg, height 168 cm (BMI 22.4); FVC 3.4 L (94%, 54 mL/kg), MIP -48 L, MEP 84; a4 canonical. |
| C | minor | `followup_outputs[5]` (telemetry) | 48-hour report. | FIXED: first 24 h; a8 canonical. |
| C | major | `ground_truth.differential` | MG high, MFS moderate, LEMS/CPEO low despite the work-up; MG "preserved reflexes and fatigability favour MG" read as if present. | FIXED: MG low; "Progression to complete MFS or GBS overlap" low; botulism (exposure history in HPI) added very_low; LEMS, CPEO, midbrain stroke very_low with case reasons. |
| D | minor | `initial_tool_outputs.specialized_test` | Impression concluded "demyelinating polyradiculoneuropathy with proximal involvement" from mild median and sural changes; pattern field interpretive. | FIXED: "Mild demyelinating features with absent late responses; no evidence of a neuromuscular junction disorder"; `test_type` "emg_ncs". |
| D | major | `initial_tool_outputs.literature_search` | Scoring-key echo. | FIXED: population-keyed MFS treatment summary [EAN_PNS_2023]; a5 optional, last. |
| C | minor | `ground_truth.action_criteria`, constraints, stop rule | Template. | FIXED: canonical; order a2, a3, a10, a11, a12, a1, a4, a8, a7, a6 (optional, no medicines), a5; constraints deleted; stop rule five required, `max_additional_actions` 3. |
| E | minor | `key_clinical_evidence`, `red_herrings[0]`, metadata | Em dashes; pearl 3 claimed a panel "positive in many"; RH location a path. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The case keeps its presentation (7 days of bilateral ptosis, full eye movements, normal strength, global areflexia, CSF protein 62 with 3 cells, mild demyelinating NCS with absent F-waves and H-reflexes, normal RNS and SFEMG) and now has a positive anti-GQ1b IgG (1:320), so it is a recognised incomplete form of Miller Fisher syndrome: "Anti-GQ1b antibody syndrome (acute bilateral ptosis with areflexia), Guillain-Barré syndrome spectrum". Myasthenia is excluded by a recommended antibody step (AChR, MuSK, LRP4 negative), the neurophysiology and an optional ice pack test; a midbrain lesion by a recommended normal brain MRI. The musts no longer mandate immunotherapy: she is admitted and monitored without IVIg or PE, which are given only if limb, bulbar or respiratory involvement develops, with telemetry and serial respiratory checks; pyridostigmine and corticosteroids are prohibited. Weight is 63 kg; FVC 94% and MEP are normal, MIP -48 is flagged low. Edrophonium, the placeholder look-ups and the template serology are gone.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Plan CENTRAL 1: ganglioside term in `interpret_labs` so the anti-GQ1b step can be a recommended criterion (BLOCKED part of e89ffe81).
- `ground_truth.diagnosis.accepted[0]` changed (plan open question 1, route chosen: positive antibody, same code G61.0). Plan CENTRAL 6 applies: "miller fisher syndrome" in the synonyms fits this case.

## Open questions for Andrea (judgment calls you could not settle)

- Plan open question 1 decided as the plan proposes: the case is kept in GBS as an anti-GQ1b acute ptosis presentation rather than relabelled ocular myasthenia, because the areflexia and CSF dissociation already argue for the GBS spectrum and the reviewer listed a positive antibody as an acceptable fix.

## Verification (adversarial verifier, 24 Oct 2026)

Checked: route chosen (positive anti-GQ1b, acute ptosis as an incomplete MFS form, Wakerley 2014) matches plan section 4 and the reviewer's options; the label, KCE, RH and differential all reflect it; MG lowered to low with RNS, SFEMG, ice pack and negative AChR/MuSK/LRP4, each served by its own step (probed); midbrain MRI moved to `analyze_brain_mri` and removed from waste; edrophonium gone; must 1/2 follow EAN/PNS for MFS-spectrum disease and define when to treat (note e62f0ba4); no IVIg must left. FVC 3.4/3.6 L = 94%, 54 mL/kg; MIP -48 flagged L for a woman, others not flagged. Pyridostigmine prohibition is consistent with the evidence.
Found and fixed: the new weight and height (63 kg, 168 cm) give BMI 22.3, not the stored 22.4. Changed `patient.demographics.bmi` to 22.3 (weight and every mL/kg value unchanged).
Checks re-run after the verifier's edits: `perfect_agent.py -v` ok (each criterion served by its intended report; labs, brain MRI and ganglioside probes confirmed by a direct MockServer probe where relevant) and `case_io.py check` clean for this case (the remaining failures name GBS-RP16 and GBS-RS16 only).


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- B, minor: `action-7-analyze-ecg` expected_evidence was the condition template ("Sinus tachycardia or bradycardia; conduction or repolarisation abnormalities reflecting autonomic involvement") and the rationale repeated the label, while the ECG shows normal sinus rhythm 84 bpm with QTc 418 ms. Rewritten to what the ECG shows, with the rationale used in RP12, RP14-RP16 (the RP12 verifier had flagged this template in this case).
- E, minor: `fallback_tool_outputs.drug_interactions.general.proposed` read "(agent not specified on this case's pathway)", an engineering note served to any off-pathway interaction check (PATTERNS 5). Now "Medication list review", as in S01-S03 and RS18.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels plus "anti gq1b syndrome" and "incomplete miller fisher syndrome" (Wakerley 2014: acute ptosis is an incomplete MFS form); AIDP, AMAN and plain Miller Fisher labels removed.
- MFS-spectrum no-treatment statements re-cited from `[EAN_PNS_2023]` to `[Leonhard_2019]` (must 1 now `[Leonhard_2019, Wakerley_2014]`, KCE 4, literature result 1 with evidence_level "review", literature summary). Reason as in P01.
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Central vocabulary wired (24 Oct 2026)
Terms added in commit e19131d6 (`interpret_labs` `anti_GQ1b_IgG`, `anti_GT1a_IgG`, `botulinum_toxin_assay`; `analyze_csf` `CMV_PCR`), wired per plan C2/C3/C9 and GBS-decisions CENTRAL 1-3. Checks after the change: `perfect_agent.py -v` pass, `case_io.py check` clean for this case, `test_case_guards -k GBS-` 60 passed; optional criteria probed against the MockServer (served the case's own report, not a fallback).

- New `action-13-interpret-labs-anti-gq1b` (REQUIRED; `{panels: [anti_GQ1b_IgG]}`), after the CSF, answered by `request_anti_gq1b_gt1a_ganglioside_panel` (GQ1b IgG 1:320, GT1a negative); added to `stop_rule.required_before_assessment`. Required because acute bilateral ptosis with areflexia is an incomplete MFS form only with the antibody (Wakerley 2014): the label 'anti-GQ1b antibody syndrome' cannot be reached responsibly without it, and it is the result that separates the case from ocular myasthenia.
- Resolves the BLOCKED part of note e89ffe81 and CENTRAL 1. Musts unchanged (none asked for the test).
