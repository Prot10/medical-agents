# FEPI-TEMP-RS04
Reviewer status: no reviewer notes for FEPI-TEMP (R1 and R2 never reviewed this condition in a notes round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input applied: the July 2026 tool guidance for focal_epilepsy_temporal via plans/FEPI-TEMP.md. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.mri` (classes E, U) | "Reduced by approximately 30%" with 1.9 vs 3.2 cm3 (41%); right volume 1.9 cm3 shared with RS05 (and formerly S04); gadolinium lines in an HS case; threshold teaching in volumetrics; no technique line. | FIXED: right hippocampus 1.7 cm3 (47% smaller, index 0.31 as (L - R)/(L + R)); 3T epilepsy-protocol technique line, no gadolinium; temporal horn enlargement and preserved temporopolar gray-white differentiation; numbered impression. |
| B | major | `patient.chief_complaint`, `.history_present_illness` | "Three convulsive episodes per week" while the HPI says once weekly is convulsive; "admitted to the epilepsy monitoring unit" and "brought to the emergency department" read as two encounters. | FIXED: "about three seizures per week" in both; HPI opens "admitted from the emergency department to the inpatient epilepsy monitoring unit". |
| B | minor | `patient.neurological_exam.motor` | Increased tone in the right arm, unexplained by right temporal sclerosis (a deficit no lesion explains). | FIXED: "Bulk and tone normal." |
| B | minor | `followup_outputs` video-EEG | "Frequent" discharges at 15 per hour (ACNS: occasional); "eleven seizures over 5 days (consistent with approximately 3 per day)" is 2.2 per day. | FIXED: rates stated without the qualifier; "about 2 per day during medication reduction"; numbered ABNORMAL impression. |
| D | minor | `followup_outputs` FDG-PET | Text identical to RS02 and RS03 (same 0.76 index); no tracer line. | FIXED: distinct report (right mesial and anterior temporal hypometabolism, maximal in hippocampus and temporal pole, asymmetry 14%, no extratemporal or left temporal change); tracer "18F-FDG, interictal". |
| D | minor | `followup_outputs` neuropsychology | Impression in lab voice ("Abnormal values: ..."). | FIXED: neuropsychologist's summary (average IQ, impaired nonverbal learning and recall, preserved verbal memory, right temporal pattern; language lateralization not assessed). |
| C | major | `followup_outputs` drug check | HLA-B*1502 warning in a Japanese woman (that allele is rare in Japanese, and long-term use without reaction needs no test, fact 10); "contraindicated" wording for valproate; no contraception interaction; "levetiracetam not teratogenic". | FIXED: full triple-regimen interactions, inducers and contraception (IUD or depot unaffected), iron; valproate within a pregnancy prevention programme (MHRA 2024); HLA line corrected; alternatives levetiracetam, lacosamide, lamotrigine with valproate and inducer effects. |
| D | major | `followup_outputs` literature (classes A, O) | Tomson Lancet Neurol 2019 does not exist as cited; de Tisi 2011 not on the allow-list; wrong titles; Kwan title wrong. | FIXED: Kwan 2010, Wiebe 2001, Engel 2012 (ERSET) with real titles and figures, Tomson 2018 (EURAP); general summary; last in the pathway. |
| B | minor | `fallback_tool_outputs.ct` | Fallback CT reported a right frontal calcified granuloma that the MRI does not show. | FIXED: normal CT; `metadata.fallback_tool_kinds.ct` normal. |
| A | major | `ground_truth.action_criteria` (classes A, B, D, E, H, S) | MRI `{contrast: true, protocol: epilepsy}`; literature required; drug check with template evidence; PET recommended with template text; neuropsychology optional; KCE and HPI cite therapeutic levels with no labs output. | FIXED: order MRI, video-EEG, labs, PET, neuropsychology, drug check, literature. MRI `{protocol: epilepsy}` required [ILAE_MRI_2019]; video-EEG required [IFCN_ILAE_EEG_2023]; new `action-9-interpret-labs` optional `{panels: [AED_levels]}` with a new initial labs output (levels in range, sodium 134, mild microcytic anemia on iron, GGT 74) [NICE_NG217_2025]; PET optional [Willmann_2007]; neuropsychology recommended [Engel_2003]; drug check required [MHRA_VPA_2024]; literature optional [Kwan_2010]; follow-ups reordered the same way. |
| A | minor | `ground_truth.sequence_constraints`, `.stop_rule` (classes C, D) | Template constraint reason; stop rule with literature, max 0. | FIXED: MRI -> drug check soft with the canonical reason; stop rule MRI, video-EEG, drug check, max 2. |
| C | major | `ground_truth.assessment` (class L) | Musts were work-up steps (video-EEG, 3T MRI, PET, neuropsychology); "dominant-hemisphere lobectomy" prohibition for a right (non-dominant in a right-hander) resection; generic LP prohibition; no valproate pregnancy programme, polytherapy plan or SUDEP. | FIXED: musts: presurgical referral (canonical), surgical and neuromodulation options, valproate pregnancy prevention programme with inducer-proof contraception and a planned switch, polytherapy rationalization, SUDEP. Prohibitions: escalation only, resection without memory and language lateralization, abrupt phenobarbital withdrawal. |
| C | major | `ground_truth.differential` (class P) | Coexisting PNES `moderate` after eleven captured electrographic seizures; "topiramate-induced slowing" (no topiramate); no bitemporal epilepsy entry. | FIXED: bitemporal epilepsy, PNES, frontal lobe epilepsy, chronic autoimmune limbic encephalitis `low`; generalized epilepsy and phenobarbital sedation (T42.3X5A) `very_low`; each names the excluding finding. |
| D | minor | `ground_truth.key_clinical_evidence` (class G) | Engineering lines; "60-70% seizure freedom", Wada and 3T claims not in the case. | FIXED: five case-specific statements. |
| C | minor | `ground_truth.avoided_actions` (class I) | Template rationales. | FIXED: case-specific rationales; CT waste kept (back to baseline, nonfocal exam, MRI available). |
| A | minor | `fallback_tool_outputs.echo` (class I) | No `echo_type`. | FIXED: `TTE`. |
| B | minor | `metadata.case_body_concerns`, `.difficulty_description`, `.difficulty_rationale` | AUDIT-FLAG on a stale "Straightforward ... minimal confounders" description. | FIXED: description and rationale rewritten; resolved AUDIT-FLAG removed. |

## Changes, in one paragraph a physician can read before re-reviewing

Ms. Tanaka, 29, Japanese, right-handed, has drug-resistant right mesial temporal epilepsy (epigastric and deja vu aura, oral and right manual automatisms, about three seizures a week, one weekly convulsive) on valproate 1400 mg, phenobarbital 140 mg and carbamazepine 1200 mg. The required epilepsy-protocol MRI now shows right hippocampal sclerosis with consistent volumetrics (1.7 versus 3.2 cm3) and no gadolinium; the required 5-day video-EEG captures eleven habitual seizures, all right anterior temporal in onset. Neuropsychology (recommended) shows a right temporal nonverbal memory deficit; FDG-PET (optional) has its own report; a new optional labs output confirms therapeutic levels. The required drug review lists the real triple interactions, the inducers' effect on contraception and the valproate pregnancy rules, and no longer suggests an HLA test. Management: presurgical referral, surgical and neuromodulation options, a valproate pregnancy prevention programme with an IUD and a planned switch, slow phenobarbital taper, SUDEP counselling; no resection without memory and language lateralization. PNES is now low after all captured events were epileptic; bitemporal epilepsy is in the differential and excluded.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys not yet in the pack allow-list: `[ILAE_MRI_2019]`, `[IFCN_ILAE_EEG_2023]`, `[NICE_NG217_2025]`, `[MHRA_VPA_2024]` (plan request 2).
- Synonyms (plan request 6): the inherited idiopathic codes G40.009/G40.019 do not fit structural drug-resistant epilepsy.

## Open questions for Andrea (judgment calls you could not settle)

- Decided: a labs output and an optional labs criterion were added (the plan lists labs as optional but the case had no labs output, while the HPI and the old KCE cite therapeutic levels). The levels are in range, in keeping with the HPI; sodium 134 and GGT 74 are typical of carbamazepine and the inducers, and the microcytic anemia matches the iron deficiency in the history.
- Decided: the plan's prohibition wording was kept, and the must on rationalizing polytherapy names levetiracetam or lacosamide as replacements for valproate because both have few pharmacokinetic interactions (inducers lower lacosamide only modestly) and neither carries valproate's malformation and neurodevelopmental risk (levetiracetam has the strongest pregnancy registry data).

## Verification

Adversarial verifier, 24 Oct 2026. Checked the log against the case file and `git diff master`. Tiers (MRI, video-EEG, drug check required; neuropsychology recommended; labs, PET, literature optional), the MRI -> drug check soft constraint (canonical reason) and the stop rule (MRI, video-EEG, drug check; `max_additional_actions: 2`, as plan 3.4 sets) match the plan. Volumetrics (1.7 vs 3.2 cm3: 47%, index 0.31; volume now unique), 11 seizures in 5 days (about 2 per day), the three-seizures-a-week wording in the chief complaint and HPI, the new labs (levels in range consistent with the HPI, sodium 134 and GGT 74 flagged, microcytic anemia on iron), the drug-interaction facts (valproate raises phenobarbital and carbamazepine epoxide, inducers lower valproate and contraception, an IUD or depot is unaffected, no HLA test after long-term carbamazepine) and the neuropsychology (nonverbal deficit, right temporal) hold. Guards pass.

Found and fixed:
- `ground_truth.assessment.required_recommendations` (polytherapy must): "replace valproate with a non-teratogenic ASM such as levetiracetam or lacosamide" overstated the evidence (no ASM is proven non-teratogenic; lacosamide pregnancy data are limited). Reworded to an ASM of lower teratogenic risk, with levetiracetam as the best-supported choice and lacosamide as an option with limited pregnancy data.

## Condition audit

Condition auditor, 24 Oct 2026. Checked uniformity of the plan's decisions across the 30 cases and the FND and MS-RR audit classes (engineering text, any-query outputs, second-tier labs, copied numbers, sharp-wave durations, differential codes). After the changes below, `perfect_agent.py` and `case_io.py check` are clean for all 30 cases and `test_case_guards.py -k FEPI-TEMP` passes.

- `initial_tool_outputs.literature_search.general`: neutral focal-epilepsy block added (definition, classification, MRI protocol, first-line ASM, drug resistance), so a literature query that names no case-specific topic no longer receives a stored follow-up.
- `action-4-search-medical-literature.label`: "Optional" prefix removed.
