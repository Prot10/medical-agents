# MS-RR-RS01
Reviewer status: R1 not reviewed, R2 not reviewed (no MS-RR notes file in this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | - | No reviewer notes for this case. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `followup_outputs[request_repeat_mri_3months]` | Brain MRI "3 months later" with a new lesion: future data the agent cannot have at assessment (plan F). | FIXED: follow-up deleted; a repeat brain MRI order now returns the initial study. |
| C | major | `followup_outputs[search_mcdonald_criteria_2017]`, `[search_late_onset_ms]` | Two literature outputs: one presents the 2017 criteria (DIS 2 of 4 regions, OCB substitute for DIT) as current; the other has an empty summary and two references that could not be verified as cited (Polliack "Late-onset CNS demyelinating disease" J Neurol Sci 2006; Tan CT 2020 review). | FIXED: one general follow-up (`search_ms_diagnostic_criteria`, last in the pathway) with the canonical 2024 text (plan O), Montalban 2025 and Wattjes 2021, and the real Polliack, Barak, Achiron paper (Late-onset multiple sclerosis, J Am Geriatr Soc 2001). No patient-specific content, no criterion text. |
| A | major | `ground_truth.action_criteria[action-3]` | Literature search required, with a long `query` argument no agent would type (ruling 5). | FIXED: optional, `required_arguments {}`, empty expected_evidence, last; removed from the stop rule. |
| A | major | `ground_truth.action_criteria[action-4]` | Drug check required with non-schema keys `proposed_class`, `screen_for` (unmatchable). | FIXED: optional, `required_arguments {}`, after the diagnostic core, out of the stop rule (plan A5). |
| A | major | `ground_truth.action_criteria[action-6]` | Labs criterion demanded 9 analytes incl. `calcium`, `glucose` (a CMP order fails it). | FIXED: `{panels: [CBC, vitamin_B12, TSH, HIV]}`, canonical label (plan A7). Stored panel unchanged in content. |
| A | major | `ground_truth.action_criteria[action-5]` | CSF demanded OCB + IgG index + kFLC together; optional although age 61 with vascular risk makes positive CSF part of the decision (F4). | FIXED: two alternatives (OCB or kFLC), `recommended` (plan 3.2), canonical label; soft MRI-before-CSF constraint kept with the canonical reason. |
| C | major | `ground_truth.action_criteria`, `initial_tool_outputs.labs` | No AQP4/MOG criterion or result although onset at 61 is a red flag (plan 3.2: required). The must "Exclude NMOSD and MOGAD with AQP4-IgG and MOG-IgG..." asked for a test the case neither scored nor served (plan B). | FIXED: new `action-aqp4-mog-cba` (required, after labs, three alternatives); `labs.panels.Neuroimmunology` with "AQP4-IgG (cell-based assay)" and "MOG-IgG (live cell-based assay)" negative; the test-as-must deleted. |
| A | minor | `ground_truth.action_criteria[*]` | Label identical to rationale in every criterion; free-text citation strings ("MAGNIMS-CMSC-NAIMS 2024/2025", "Reich 2018 NEJM review", "NICE NG220 (2026)"). | FIXED: canonical labels, one case-specific rationale each, bracketed keys only (`[McDonald_2024]`, `[Wattjes_2021]`, `[Wingerchuk_2015]`, `[Banwell_2023_MOGAD]`, `[NICE_NG220]`). Criteria in pathway order: brain MRI, spine MRI, labs, AQP4/MOG, CSF, drug check, literature. |
| A | minor | `ground_truth.stop_rule` | `max_additional_actions` 0; literature and drug check required before assessment. | FIXED: required criteria only (brain MRI, spine MRI, labs, AQP4/MOG), allowance 2. |
| B | major | `patient.neurological_exam.cranial_nerves` | Right eye fails to adduct and left eye fails to abduct on left gaze, called a "bilateral horizontal gaze palsy": this is a left (ipsilesional) horizontal gaze palsy. | FIXED: "consistent with a left horizontal gaze palsy. Rightward gaze is full." |
| D | minor | `patient.neurological_exam.additional` | Exam text localised the lesion to the left dorsal pons, PPRF and facial nucleus (the reasoning the agent should do, and the MRI result). | FIXED: localisation sentence removed. |
| B | minor | `initial_tool_outputs.mri.findings[2].location` | Lesion placed in the "paramedian pontine reticular formation", which does not explain the ipsilateral LMN facial palsy; a gaze palsy plus facial palsy localises to the abducens nucleus and facial genu (facial colliculus). | FIXED: "Left dorsal pontine tegmentum at the level of the facial colliculus (abducens nucleus and facial nerve genu region)"; same wording in KCE. |
| B | minor | `initial_tool_outputs.mri.findings[1]` | Cerebellar lesions labelled "cortical and juxtacortical white matter" (they are infratentorial) and "multiple" while the volumetrics count 3 infratentorial lesions including the pontine one. | FIXED: "Cerebellar hemispheric white matter, bilateral", "Two small round lesions, 3 mm and 8 mm", enhancement in both. |
| D | minor | `initial_tool_outputs.mri.findings[0].signal_characteristics.T1`, `findings[2].signal_characteristics.ADC`, `.impression` | Interpretive glosses ("indicating chronic demyelination", "excluding acute ischemia"); impression a prose paragraph. | FIXED: glosses trimmed; impression a numbered list of findings with one within-imaging read ("pattern consistent with inflammatory demyelination"). |
| B | minor | `followup_outputs[0].output` (spine) | Lesion description empty; impression an unnumbered run-on. | FIXED: description with length, cross-section, enhancement; numbered impression; "No longitudinally extensive cord signal abnormality" kept as a pertinent negative. |
| C | major | `initial_tool_outputs.csf` | Myelin basic protein reported (obsolete, F6); no kFLC; interpretation a recital with "(N/A PMN/N/A lymph)". | FIXED: MBP deleted; "kappa free light chain index": "31.4 (elevated; reference < 6.1)"; canonical pattern interpretation. |
| D | minor | `initial_tool_outputs.labs.panels["Mimic exclusion"]` | HIV row with `clinical_significance` "Reported negative in this case's own workup; excludes this reversible mimic" (plan E); panel named for its purpose. | FIXED: panel renamed "Serology", significance null, reference "Non-reactive". |
| B | minor | `initial_tool_outputs.labs.panels.Other[3]`, `abnormal_values_summary[3]`, `interpretation`, `red_herrings[0]` | Vitamin D 18 ng/mL copied across seven cases (plan E). | FIXED: 21 ng/mL everywhere it appears (labs, summary, interpretation, red herring, must). |
| C | major | `followup_outputs[check_drug_interactions].output` | Ocrelizumab dose "300 mg IV every 6 months" is wrong (600 mg every 6 months after two 300 mg infusions 2 weeks apart); TB screening stated as required; "aspirin does not affect B-cell depletion efficacy" gloss. | FIXED: correct dosing; HBV screening and live-vaccine timing per F11; each current medicine listed with "no clinically significant interaction". |
| C | major | `ground_truth.assessment.required_recommendations` | Template musts: DIS and DIT as two interpretation musts, AQP4/MOG test as a must, IV-only steroid must, generic DMT and lifestyle musts (Uhthoff, smoking cessation in a never smoker). | FIXED: formulation must with the four DIS regions and the over-50 additional evidence; steroid must (IV inpatient or oral, infection excluded, gastric protection with aspirin, BP and glucose monitoring, PLEX if refractory); corneal protection for incomplete eyelid closure; DMT must weighing activity against infection risk at 61; pre-DMT screening (F11); vitamin D replacement. |
| C | minor | `ground_truth.assessment.prohibited_recommendations` | T10 teriflunomide-in-women prohibition in a man; T8 natalizumab/JCV and T9 fingolimod prohibitions with no case trigger; T13 myelopathy prohibition without myelopathic signs. | FIXED: kept T7, T11, T12; added "Do not attribute the brain lesions to small-vessel disease or a lacunar infarct without explaining the enhancing lesions, the C5-C6 cord lesion and the CSF-restricted oligoclonal bands". |
| C | major | `ground_truth.differential` | NMOSD and MOGAD "high" and neurosarcoidosis "moderate" after a work-up that excludes them; no stroke or small-vessel entry although the case raises both (PCP suspected lacunar stroke; small-vessel change on MRI); no lupus entry despite an ANA row. | FIXED: all entries low with the case's own discriminating results; added pontine lacunar infarct (I63.81), cerebral small-vessel disease (no ICD code), CNS lupus (M32.19); neurosarcoidosis kept because of the facial palsy, with why it is fascicular. |
| E | major | `ground_truth.key_clinical_evidence` | Engineering lines ("July 2026 review...", "Tier per the July 2026 clinical review..."), wrong facts ("three of these regions establishes DIS", F2; "black holes ... contribute evidence of DIT", F5), tumefactive and DMT template lines. | FIXED: six case-observable lines per plan D (syndrome and lesion, DIS 4 of 5, over-50 evidence and DIT, no restricted diffusion, AQP4/MOG negative, vascular distractor). |
| D | minor | `ground_truth.red_herrings` | Only red herring was vitamin D; the case's real distractor (vascular risk, lacunar-stroke referral, small-vessel change) was not recorded. | FIXED: second red herring at `initial_tool_outputs.mri.additional_observations[5]`. |
| C | minor | `ground_truth.avoided_actions[*]` | Generic rationales with em dashes and citations that do not govern (`[Reich_2018]` for echo). | FIXED: one case-tied sentence each; `[Wattjes_2021]` for CT and PET, none for EEG, echo, monitoring. |
| E | minor | `fallback_tool_outputs.echo` | No `echo_type` (an untyped echo fallback answers every echo variant, PATTERNS 5). | FIXED: `echo_type: "TTE"`. |
| E | minor | `metadata.difficulty_rationale`, `.difficulty_description` | Cited "McDonald 2017". | FIXED: 2024 criteria and the over-50 rule; difficulty stays "straightforward". |

## Changes, in one paragraph a physician can read before re-reviewing

A 61-year-old hypertensive man with a one-week left horizontal gaze palsy and left LMN facial palsy (the exam now calls it a left, not bilateral, gaze palsy). The brain MRI places the enhancing lesion at the left facial colliculus, calls the cerebellar lesions infratentorial (two, both enhancing), and has a numbered findings-only impression; the 3-month repeat MRI is gone. The spine MRI reports a short non-enhancing left dorsolateral C5-C6 lesion. The CSF adds a kFLC index of 31.4 (reference < 6.1) and drops myelin basic protein; the labs add negative AQP4-IgG and MOG-IgG by cell-based assay; vitamin D is 21 ng/mL. The work-up reads: brain MRI, spine MRI, mimic labs and AQP4/MOG (all required), CSF (recommended, because over 50 the 2024 criteria want supporting evidence), then optional drug check (ocrelizumab dose corrected) and literature (one general 2024-criteria output). Musts: formulate RRMS with four DIS regions and the over-50 evidence (cord lesion, CSF bands), methylprednisolone with gastric protection and BP/glucose monitoring, corneal protection, DMT weighed against infection risk at 61, pre-DMT screening, vitamin D. The differential now has every mimic low with its excluding result, including lacunar infarct, small-vessel disease and lupus.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` used per plan 1.1 (plan CENTRAL 1: add to the MS-RR criteria pack).
- Diagnosis synonyms (plan CENTRAL 2): G35.B/G35.C and "demyelinating disease" in the accepted list; not hand-edited.

## Open questions for Andrea (judgment calls you could not settle)

None. Decisions taken: CSF recommended, not required: with four regions DIS is met and the cord lesion alone already supplies over-50 supporting evidence, so CSF strengthens but does not gate the diagnosis. The drug-check output stays on ocrelizumab (the DMT question) rather than methylprednisolone; the steroid-aspirin GI point is carried by the steroid must.

## Verification

`perfect_agent.py MS-RR-RS01 -v`: pass; brain MRI <- `initial_tool_outputs.mri`, spine <- `followup[0] request_spine_mri`, labs and AQP4/MOG <- `initial_tool_outputs.labs` (expected warning: both criteria answered by the one stored panel, which holds the CBC/B12/TSH/HIV rows and the two CBA rows), CSF <- `initial_tool_outputs.csf`. `case_io.py check`: schema and synonym guard OK, no failure naming MS-RR-RS01 (condition-wide leak failures name P02, S03 and RS05, the last one mine and fixed in its own pass). `test_case_guards.py -k MS-RR-RS01`: 2 passed.

## Verification (adversarial verifier, 24 Oct 2026)

Checked against the committed worker version (b8be2153): every own-finding row against the case file (field by field read of the whole final case), the plan tier table (section 3.5), the stop rule, the sequence constraint, laterality and lesion-to-exam fit, timeline, allergies against drug outputs, leakage in the brain MRI (no cord text) and the literature/drug outputs (guards pass), PATTERNS classes (template numbers across RS01-RS06, 2017 facts, test-as-must, F2/F5 wrong facts), and the differential against the final results. No reviewer notes exist for MS-RR, so no note id can be missing. Re-run after the changes below: `perfect_agent.py -v` pass, `case_io.py check` schema and synonym guard OK with no failure naming the case, `test_case_guards.py -k` pass.

Found: no error. Gaze palsy plus LMN facial palsy now localise to the facial colliculus lesion; enhancing lesion count (3) matches the DMT must; vitamin D 21 consistent in labs, summary, red herring and must; ocrelizumab dosing and premedication correct; Polliack, Barak, Achiron 2001 J Am Geriatr Soc is a real paper. Changed: nothing.

## Condition audit

Condition auditor, 24 Oct 2026 (uniformity scripts over all 30 MS-RR cases; edits through `case_io`; perfect agent, `case_io check` and the case guards clean afterwards).

- `ground_truth.differential[4].icd_code` D86.85 -> D86.89: D86.85 is sarcoid myocarditis; neurosarcoidosis is D86.89, as in the other 11 MS-RR cases.
- `ground_truth.differential[7].icd_code` G04.81 -> G04.00: G04.81 is other encephalitis; ADEM is G04.00, as in the other 8 MS-RR cases.
- `action-3-search-medical-literature.label` "Literature search (background evidence only)" -> "Literature search on the MS diagnostic criteria at late onset": engineering text replaced by the topic of the stored output.
- `assessment.prohibited_recommendations[2]` chronic-steroid prohibition set to the condition's canonical text (was "Do not use chronic oral corticosteroids as a maintenance treatment for MS [em dash] they are ineffective long-term and carry significant harm").
- `initial_tool_outputs.labs`: the AQP4-IgG and MOG-IgG rows moved to a new `followup_outputs` entry (`interpret_labs`, trigger `request_aqp4_mog_cell_based_assay`, panel `Neuroimmunology`, placed after the imaging follow-ups). Served in the initial labs payload, they answered the mimic-exclusion panel order as well, so an agent learned the result of `action-aqp4-mog-cba` without ordering it (perfect-agent warning "answered with the same stored report"); the MockServer now serves them only to an order that names the assays (checked for all three alternatives and both orders).

## Close-out (24 Oct 2026)

Condition close-out (`plans/MS-RR-decisions.md`). What changed and why:

- Diagnosis synonyms (`diagnosis_synonyms.yaml` G35 entry, re-applied with `apply_diagnosis_synonyms.py --prune --conditions multiple_sclerosis`): removed the label "demyelinating disease" (G37.9 is an Excludes1 of G35.A, and its tokens occur in an NMOSD, MOGAD or ADEM answer, which would have scored as correct) and the codes G35.B and G35.C (primary and secondary progressive MS in FY2026 ICD-10-CM, a different course from this relapsing-remitting case). Accepted now: the label, multiple sclerosis, MS, relapsing(-)remitting multiple sclerosis, RRMS; codes G35.A, G35, G35.D.
- Checks: `perfect_agent.py` pass, `case_io.py check` clean for the case, `test_case_guards.py -k MS-RR-` passes with MS-RR now in `DISCRIMINATOR_CONDITIONS`.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `fallback_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
