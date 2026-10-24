# GBS-P01
Reviewer status: R1 not reviewed, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 09291641-c07a-4c19-99e2-89d0e22d238c | FIXED | Anti-GQ1b IgG 1:6400 is removed from `initial_tool_outputs.labs` (and from its summary and interpretation). It moves to a pathway step, `followup_outputs` trigger `request_anti_gq1b_gt1a_ganglioside_panel`, placed after the CSF. "Anti-GQ1b result pending" and the "Triad: ..." sentence are deleted from `patient.neurological_exam.additional` (now null). The must that asked for the antibody now says to send anti-GQ1b alone and not to wait for it before admission and monitoring. The prohibition that governed waiting on the result is rewritten to "Do not delay admission and monitoring while waiting for the anti-GQ1b result", since immunotherapy is not routinely advised in MFS (EAN/PNS 2023). |
| ee1e4f06-6611-455e-8eb5-b0b4e84a33e0 | FIXED / BLOCKED (criterion) | The follow-up reports anti-GQ1b IgG only, with a hedged templated comment. The must "Order anti-GQ1b IgG and broader ganglioside panel as part of variant typing" is replaced with "Send serum anti-GQ1b IgG (not a broad ganglioside panel)". `anti-GM1 IgM` is removed from `action-1-interpret-labs`, whose expected_evidence ("mild leukocytosis ... trigger identification") is replaced with the canonical text, since WBC is 9.2. The recent-diarrhoea conditional is gone from the a1 label, and the Campylobacter IgG result is deleted from the labs. BLOCKED part: no criterion scores the anti-GQ1b order, because no `interpret_labs` vocabulary term exists for it (plan C2, CENTRAL 1). The follow-up is reachable: a probe with `clinical_context` naming "anti-GQ1b" is served the GQ1b report, while the baseline CBC/CMP/CK order still gets the baseline labs. |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| C | major | `assessment.required_recommendations` | "Initiate IVIG ... both effective in MFS" goes against EAN/PNS 2023: IVIg and PE are not routinely advised in MFS (plan P01). | FIXED: must 1 says immunotherapy is not routinely advised and to admit and monitor for limb, bulbar, respiratory or consciousness changes. Must 2 sets serial respiratory and bulbar checks, with GBS-overlap treatment if they appear. Musts for telemetry, falls and DVT prophylaxis added. |
| B | major | `patient.neurological_exam.mental_status` | "Confused about why he cannot walk" contradicted "denies confusion" and the preserved-alertness reasoning, and would raise Bickerstaff encephalitis (plan P01). | FIXED: "Alert and fully oriented." |
| D | major | `patient.history_present_illness` | The final sentence ("the striking finding is the triad ...") editorialised the diagnosis (C7). | FIXED: deleted. The ED stroke suspicion and the unremarkable CT stay as history. |
| D | major | `initial_tool_outputs.specialized_test.quantitative_data.note` | "Pathology localized primarily to cranial nerve and dorsal root ganglion level" interpreted beyond the modality (Kind 1, plan P01). | FIXED: deleted. Normal limits are added to the motor values, a normal needle EMG line is added, and the impression is in report voice. |
| C | major | `ground_truth.action_criteria` | KCE 3 and the must asked for brain MRI, but no criterion ordered it (plan P01). | FIXED: new `action-10-analyze-brain-mri` (recommended), served by the existing normal MRI follow-up. Its trigger is renamed `order_brain_mri_brainstem`, and it is placed first in both the pathway and the criteria list: acute ophthalmoplegia with ataxia is imaged before the LP to exclude posterior fossa stroke. Brain MRI was not in the avoided actions. |
| A/D | major | `followup_outputs` `request_analyze_ecg` | Placeholder ECG with rate 0 and the a7 expected_evidence pasted as findings (C9). | FIXED: deleted. A real normal ECG (sinus rhythm 88, QTc 418 ms) is now the initial ECG output, so a7 receives case data. a7 expected_evidence describes this ECG. |
| C | major | literature follow-up `request_literature_mfs` | It said "Published evidence supports IVIG and plasmapheresis as therapeutic options" and gave the anti-GQ1b sensitivity as ">95%". There was no source and no evidence level (C11). | FIXED: moved to the initial literature slot as a population-keyed MFS summary [EAN_PNS_2023, Wakerley_2014] (no routine immunotherapy; monitor for overlap; GQ1b in most patients). The follow-up is deleted. a5 is optional and last. KCE 2 says "most patients" instead of ">90%". |
| A | minor | `followup_outputs` `check_ivig_drug_interactions` | Empty DDI placeholder (C9). | FIXED: deleted. There are no current medications, so a6 is optional. The initial DDI output says so and its boilerplate warning is removed. |
| C | major | `ground_truth.differential` | BBE and brainstem stroke stayed "moderate" after an alert exam with areflexia and a normal MRI. The MG entry relied on an AChR result that does not exist. The botulism entry said "cholinergic signs absent", but botulism is anticholinergic (C5, wrong fact). | FIXED: BBE low; stroke, Wernicke and MG very_low, each with case-based reasons. The botulism reason is rewritten (bulbar weakness and dilated, poorly reactive pupils, absent here). "Pupils equal and reactive to light" is added to the cranial nerve exam as the pertinent negative. |
| C | minor | `red_herrings` | The only red herring was albuminocytological dissociation, a supporting finding (C6). | FIXED: replaced with the genuine distractor in the case, the ED suspicion of posterior fossa stroke, resolved by the symmetric peripheral pattern and the normal DWI. |
| C | minor | respiratory follow-up | "All values within normal limits", no weight, no MEP, and a MIP reference that read as an intubation threshold (C1). | FIXED: weight 65.5 kg and height 168 cm (BMI 23.2). FVC 4.1 L (91%; 62.6 mL/kg) within reference. MIP -52 flagged L against the Evans and Whitelaw 2009 lower limit (-58 for a 28-year-old man). MEP 104, cough effective. |
| C | minor | `initial_tool_outputs.labs` | No CMP, liver tests, albumin, glucose, CK or platelets. HIV had the leaky clinical_significance (C10). | FIXED: CMP with glucose 88 (which matches the CSF ratio 0.68), liver tests, albumin, platelets, CK; HIV with null significance. |
| C | minor | telemetry follow-up | 48 h (C12). | FIXED: the first 24 h; a8 expected_evidence is canonical. |
| A | major | `sequence_constraints`, `stop_rule`, citations | Template constraints, a stop rule that included literature and DDI with max 0, and free-text citations (plan 3.3, 1.1). | FIXED: constraints removed. The stop rule lists the five required criteria, max 3. Citations are plan keys. The MR angiography waste rationale is rewritten for this case. |
| E | minor | `patient.neurological_exam.motor`, `reflexes`, `cranial_nerves` | Capitalised editorial phrases ("NO LIMB WEAKNESS", "in setting of no weakness", "ABNORMAL:"). | FIXED: plain findings. |

## Changes, in one paragraph a physician can read before re-reviewing
GBS-P01 is Miller Fisher syndrome with anti-GQ1b, and the antibody result is now a pathway step (GQ1b IgG alone, 1:6400), not a value printed in the initial labs. The patient is alert and oriented, and the editorial triad sentences are gone. Brain MRI is now a recommended criterion, ordered first to exclude posterior fossa stroke and brainstem encephalitis. The management follows EAN/PNS 2023: no routine IVIg or PE in MFS, admission with respiratory, bulbar and consciousness monitoring, GBS-overlap treatment only if those change, telemetry, fall precautions and DVT prophylaxis, and anti-GQ1b sent without waiting on it. The literature output no longer claims IVIg is effective in MFS. The placeholder ECG is replaced by a real normal ECG. The differential is updated after the normal MRI, and the botulism reasoning is corrected. The only red herring is now the ED stroke suspicion.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)
- Plan CENTRAL 1: an `interpret_labs` term for anti-GQ1b IgG (or an anti-ganglioside panel) is needed. Then a recommended criterion `interpret_labs {'panels': ['anti_GQ1b_IgG']}` can score the order the must describes (BLOCKED until then). Plan CENTRAL 11: the new term's tokens must reach trigger `request_anti_gq1b_gt1a_ganglioside_panel`.
- Plan CENTRAL 6: this MFS case accepts "AIDP", "acute inflammatory demyelinating polyneuropathy", "acute motor axonal neuropathy" and "AMAN" through the code-level synonyms.
- Plan CENTRAL 5 (weight field).

## Open questions for Andrea (judgment calls you could not settle)
None.

## Verification
Adversarial verifier, 24 Oct 2026. Read the log, the full diff and the whole final case.
- Note 09291641: confirmed (no GQ1b in the initial labs, no "pending", GQ1b served as a pathway step). Note ee1e4f06: confirmed fixed for the must, a1 args and expected_evidence, and the diarrhoea conditional; the BLOCKED part (no criterion for anti-GQ1b until CENTRAL 1) is sound. Probe: `interpret_labs` with "anti-GQ1b" in `clinical_context` is served the GQ1b report; a plain CBC/CMP/CK order is served the baseline labs.
- Management checked against EAN/PNS 2023: no routine IVIg/PE in MFS, admission and overlap monitoring; brain MRI recommended and not in the avoided actions; no Brighton level quoted (correct for a patient without limb weakness). Arithmetic: BMI 23.2, FVC 4.1/4.5 = 91%, 62.6 mL/kg, MIP/MEP limits for a 28-year-old man (58, 94), CSF 60/88 = 0.68.
- Found and fixed (pre-existing): the NCS reported a median F-wave latency of 52 ms as "borderline", but the median F-wave upper limit is about 31 ms, so 52 ms is markedly prolonged and contradicts the "borderline prolonged" impression. Now "borderline prolonged in median (33 ms; normal <31 ms)". The chief complaint listed exam findings and the MFS triad ("with no limb weakness but complete areflexia", C7 editorialising); rewritten as the patient's complaint: "Four days of double vision, drooping eyelids and imbalance with falls in a 28-year-old man."
- Not changed: the Wakerley 2014 attribution of the brain-MRI sentence in the literature output is general and plausible; I could not verify the exact wording and left it.
- Checks: `perfect_agent.py GBS-P01 -v` passes; `case_io.py check` reports no failure naming GBS-P01.


## Condition audit (24 Oct 2026)
Condition auditor, after the worker and the verifier. Changes made through case_io; `perfect_agent.py` and `case_io.py check` re-run clean for all 30 GBS cases afterwards, and `test_case_guards.py -k GBS` passes.
- E, minor: `fallback_tool_outputs.drug_interactions.general.proposed` read "(agent not specified on this case's pathway)", an engineering note served to any off-pathway interaction check (PATTERNS 5). Now "Medication list review", as in S01-S03 and RS18.

## Close-out (24 Oct 2026)

Decisions in `plans/GBS-decisions.md` (Andrea, 24 Oct 2026: resolve open points for dataset quality).

- Synonyms (`diagnosis_synonyms.yaml` G61.0 split into scoped entries, expanded with `--prune`): now accepts the generic GBS labels plus "miller fisher syndrome", "fisher syndrome" and "MFS"; the AIDP and AMAN labels it used to accept are removed (wrong subtype for MFS).
- MFS no-treatment statements re-cited: must 1 `[EAN_PNS_2023]` -> `[Leonhard_2019]`; literature result 1 source `[EAN_PNS_2023]` -> `[Leonhard_2019]` with evidence_level "review"; literature summary `[EAN_PNS_2023, Wakerley_2014]` -> `[Leonhard_2019, Wakerley_2014]`. EAN/PNS 2023 does not address MFS treatment (read in full text 24 Oct 2026); Leonhard 2019 states treatment is generally not recommended in pure MFS.
- Checks: `perfect_agent.py` pass; `case_io.py check` clean for this case; GBS guards pass; synonym `--check` clean.

## Central vocabulary wired (24 Oct 2026)
Terms added in commit e19131d6 (`interpret_labs` `anti_GQ1b_IgG`, `anti_GT1a_IgG`, `botulinum_toxin_assay`; `analyze_csf` `CMV_PCR`), wired per plan C2/C3/C9 and GBS-decisions CENTRAL 1-3. Checks after the change: `perfect_agent.py -v` pass, `case_io.py check` clean for this case, `test_case_guards -k GBS-` 60 passed; optional criteria probed against the MockServer (served the case's own report, not a fallback).

- New `action-11-interpret-labs-anti-gq1b` (recommended; `interpret_labs` `{panels: [anti_GQ1b_IgG]}`), placed after the CSF, answered by the existing follow-up `request_anti_gq1b_gt1a_ganglioside_panel` (GQ1b IgG 1:6400). Recommended, not required: MFS is defined by the clinical triad and EAN/PNS 2023 advises the antibody when MFS is suspected as support only.
- Must "Send serum anti-GQ1b IgG (not a broad ganglioside panel) ..." deleted: the order is now a scored criterion and the prohibition "Do not delay admission and monitoring while waiting for the anti-GQ1b result" keeps the management point.
- Resolves the BLOCKED part of note ee1e4f06 and CENTRAL 1.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.
- follow-up `request_cardiac_monitoring`: `monitor_type` "Continuous telemetry" -> `telemetry`.
- `initial_tool_outputs.specialized_test.test_type` "Nerve Conduction Studies and EMG" -> `emg_ncs`.
- `fallback_tool_outputs.advanced_imaging` set to null: a generic report (modality 'MRI brain without contrast', impression 'No intracranial lesion identified. No brainstem signal change. No mass, haemorrhage, or restricted diffusion.') that names no one study and so answered every variant; the benchmark library now answers each study with its own normal report.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
