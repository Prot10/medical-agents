# GLIO-HG-P03
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 1163206c-0adb-40d7-9516-f047f3b88e88 | FIXED | Both `ground_truth.red_herrings` rewritten from the printed findings: the abscess one now says imaging cannot settle it (diffusion equivocal, abscess not excluded), lists what favours tumour (thick shaggy nodular ring, rim rCBV 3.8, no amino acid peaks, afebrile, normal WBC and procalcitonin) and lets the negative blood cultures, the negative aspirate and the histology decide; the demyelination one no longer claims "closed ring" as diagnostic and ends on histology. The MRI report itself was aligned: DWI "Equivocal: patchy restricted diffusion along parts of the enhancing rim", ring "thick, irregular, shaggy". |
| 76e5c5d3-9a6c-4015-954d-26f6d069c587 | FIXED | `ground_truth.differential`: the two abscess entries merged into "Brain abscess (odontogenic)" (low, with for and against features), the two demyelination entries into "Tumefactive demyelination" (very low); metastasis and PCNSL very low at the assessment-time view. |
| dde4d001-7207-4a6a-a426-07c4a79315e8 | FIXED | `patient.clinical_history.social_history.occupation` "High school history teacher" (matches the HPI lecture episode). Sodium 148 normalised to 141 (`initial_tool_outputs.labs.panels.BMP`), flag cleared, anion gap 141 - (105 + 26) = 10; summary and interpretation recomputed; the labs expected evidence names the actual relevant abnormality (glucose 171, HbA1c 7.8 before dexamethasone). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.clinical_history.allergies`, HPI, `past_medical_history[2]`, red herring | Penicillin allergy (rash) listed, yet the dental abscess was treated with amoxicillin-clavulanate. | FIXED: the dental course is clindamycin "because of his penicillin allergy" in the HPI, the history and the red herring. |
| D | major | HPI | ED CT "showed a ring-enhancing lesion" with no contrast stated (plan C8 class). | FIXED: "A non-contrast CT head ... showed a right frontotemporal hypodense lesion with surrounding edema and 4 mm leftward midline shift." |
| B | major | `initial_tool_outputs.tissue_diagnosis` | Tissue served in the initial work-up; template WHO meta-text; site "contrast-enhancing rim" only (plan C2). | FIXED: two follow-ups, `request_stereotactic_aspiration_biopsy` (procedure `stereotactic_biopsy`) and `request_resection` (procedure `resection`, subtotal about 90%, insular residual), identical integrated diagnosis "Glioblastoma, IDH-wildtype, CNS WHO grade 4" and molecular results; frozen section, aspirate Gram stain and culture rows (group B); impression "Integrated diagnosis: ... MGMT promoter unmethylated." Initial set to null. |
| A | major | `action-10-obtain-tissue-diagnosis` | Assay list (MGMT, 1p/19q, TERT, EGFR, +7/-10) without IDH or ATRX; stereotactic biopsy only; label template (plan C3, C4). | FIXED: group B alternatives `stereotactic_biopsy` then `resection`, each with `IDH1_IHC`, `IDH1_IDH2_sequencing` (age 48), `ATRX_IHC`, `MGMT_methylation`; report rows and `molecular_findings` for each (IDH1 R132H negative, IDH1/IDH2 wildtype, ATRX retained, MGMT unmethylated) plus TERT C228T, EGFR amplified, +7/-10, 1p/19q not codeleted. Label and rationale per plan group B. |
| A | major | `action-3-search-medical-literature` | Literature as a clinical step with expected text on the Stupp protocol (ruling 5; baseline perfect-agent failure). | FIXED: deleted. |
| B | major | `followup_outputs` (`request_functional_mri`) | Language and motor fMRI tagged `perfusion_MRI`, impression mentions DTI absent from findings; no resection-first indication in group B. | FIXED: deleted (plan C6, P03 in the delete list). |
| B | major | `followup_outputs` (`request_blood_cultures`, `request_demyelination_workup`) | Blood cultures filed as `interpret_labs`; a "demyelination work-up" lab panel containing visual evoked potentials. | FIXED: blood cultures are an `order_microbiology` blood_culture follow-up (two sets, collected before antimicrobials, no growth) with a recommended criterion `action-blood-cultures`; the demyelination panel deleted (plan C14; the biopsy decides). |
| D | minor | MRI impression and `additional_observations` | Impression cited the dental abscess (cross-modality); DWI text had a teaching contrast with abscess; capitals. | FIXED: numbered imaging-only impression with one hedged differential line; size changed from the 4.2 x 3.8 x 3.5 cm shared with P02 to 4.4 x 3.9 x 3.6 cm (template carry-over). |
| D | minor | perfusion, MRS follow-ups | Differential statements inside the perfusion pattern ("atypical for abscess or demyelinating disease"); MRS impression named a perilesional choline rise the findings do not contain. | FIXED: within-modality findings and numbered impressions; MRS impression matches its findings (perilesional myoinositol); quantitative fields filled. |
| D | minor | `initial_tool_outputs.eeg.impression` | Clinical essay ("may reflect elevated intracranial pressure ... imaging correlation is essential"). | FIXED: ACNS-style list (electrographic seizure right frontotemporal F8-T4 with its evolution, focal delta, generalized theta, right attenuation). |
| B | minor | labs | PT 13.0 s with INR 0.9; type and screen row with engineering text. | FIXED: PT 11.6 s; Blood_Bank row with null significance. |
| C | major | `assessment.required_recommendations` | Template treat must, Stupp template, interchangeable biopsy or resection must, no aspirin or antibiotic-timing guidance. | FIXED: group B surgery must; canonical dexamethasone must; canonical treat must for the documented focal seizures (home episode, exam episode); glucose must kept and made specific; aspirin hold before surgery; withhold empirical antibiotics until aspiration while stable, compatible with the penicillin allergy; entity-specific treatment must with KPS 80 and unmethylated MGMT. |
| C | minor | `assessment.prohibited_recommendations` | LP prohibition with a dash; no enzyme-inducer prohibition in a treat-class case. | FIXED: reworded; enzyme-inducer prohibition added (plan C5 keeps it in the treat class). |
| A | minor | criteria | No performance status (C7); DDI criterion with template evidence and no stored output. | FIXED: `action-performance-status` recommended with a follow-up (KPS 80, ECOG 1); DDI optional, last, with a follow-up checking dexamethasone and levetiracetam against his four medicines and the penicillin allergy; guard passes. |
| C | minor | `key_clinical_evidence` | Overstated imaging, template off-pathway imaging pearl, dashes. | FIXED: rewritten to the case. |
| A | minor | citations, constraints, stop rule | Duplicate keys, `WHO_CNS5`, Stupp on MRI; one template soft constraint. | FIXED: plan 1.1 keys; hard MRI to tissue and labs to tissue; stop rule MRI, labs, tissue. |
| E | minor | `fallback_tool_outputs.drug_interactions.general.proposed`, metadata | "this case's pathway"; stale literature concerns. | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 48-year-old teacher with focal seizures, morning headache and language and attention deficits, a molar abscess six weeks ago (treated with clindamycin, since he is penicillin-allergic) and remote optic neuritis. The ED CT is now a non-contrast study showing a hypodense lesion with edema. Pathway: contrast MRI (thick shaggy nodular ring, central necrosis, equivocal rim diffusion, 4 mm shift, two small non-enhancing white matter lesions), perfusion (rim rCBV 3.8), spectroscopy (Cho/NAA 8.0, no amino acid peaks), optional body CT, blood cultures (negative), pre-operative labs (glucose 171, HbA1c 7.8, otherwise normal), performance status (KPS 80, ECOG 1), then stereotactic aspiration and biopsy with frozen section, Gram stain and culture (or resection), giving glioblastoma, IDH-wildtype, CNS WHO grade 4 with IDH wildtype on IHC and sequencing, ATRX retained, MGMT unmethylated, TERT, EGFR and +7/-10. The fMRI step, the VEP lab panel and the literature step are gone. Musts: aspiration then maximal safe resection, dexamethasone with glucose control, levetiracetam as treatment of the documented seizures, hold aspirin, withhold empirical antibiotics until aspiration while stable, and Stupp chemoradiation after the diagnosis.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Criteria-pack allow-list: `[AIOM_brain]` (plan 5.1). The antibiotic-timing must cites no key; if one is wanted, ESCMID brain abscess guideline (Bodilsen J et al. Clin Microbiol Infect 2024;30:66-89) would need adding to the allow-list.
- Synonyms: accepted[0] still reads "WHO grade 4" (plan 5.3 normalisation to "CNS WHO grade 4"); "astrocytoma grade 4" is wrong for an IDH-wildtype glioblastoma (plan 5.2).

## Open questions for Andrea (judgment calls you could not settle)

- None that need your information. The antibiotic-timing must reflects ESCMID 2024 (postpone antibiotics until aspiration in a stable patient when surgery is prompt); drop it if you prefer the musts to stay strictly within the glioma guidelines.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the notes (1163206c, 76e5c5d3, dde4d001) and the whole final case.
- Notes: all three are in the table and fixed. Both red herrings now follow the printed MRI: diffusion equivocal, shaggy ring, histology decides. The differential has one abscess entry and one demyelination entry. There is one occupation (history teacher) in the HPI and the social history. Na is 141 and the anion gap is 10.
- Cross-field checks: the penicillin allergy against clindamycin in the HPI, the history and the red herring; the treat-class must against the two documented focal seizures and the electrographic seizure on EEG; the enzyme-inducer prohibition; the DDI output against his four medicines; procedure-matched tissue follow-ups with identical molecular results; the KPS 80 used by the Stupp must.
- Found and fixed:
  - Hb 15.1 with Hct 41.2 gave an MCHC of 36.7 g/dL, above the 32 to 36 range (plan C10 arithmetic). Hct is now 44.6 % (MCHC 33.9); the labs summary and interpretation still hold.
  - The MRI impression ended "Tissue diagnosis recommended." Deleted (C9).
  - The perfusion rationale claimed that the abscess wall "is usually not hyperperfused" under `[Law_2003]`, which is a glioma grading study and not a source on abscess perfusion. This is the class the reviewer raised in P04 (16cb2bae). The rationale now reads: "Rim hyperperfusion supports a high-grade neoplasm and targets the biopsy to the most perfused rim; it does not exclude abscess, and tissue decides."
- Noted, not changed: word-finding pauses and paraphasias in a right-handed man with a right-hemisphere lesion predate this round. They are mild and could be attentional, and the case does not build on them.
- After the fixes: `perfect_agent.py` passes, `case_io.py check` reports no failure naming the case, and `test_case_guards` passes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `fallback_tool_outputs.literature_search` set to null and its entry removed from `metadata.fallback_tool_kinds` (plan C1, uniform with the other 26 cases).
- Language signs in a right-hemisphere tumour with left-dominant language and no fMRI: mental status now "Speech is fluent, with slowed responses. Naming 15/15 ... without paraphasias."; HPI "has been slower to follow conversations"; key evidence "new cognitive deficits"; performance-status output "headache, poor concentration and seizures" (same class the S01 to S04 verifiers fixed).
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- must removed: 'Obtain MRI brain with and without gadolinium contrast (tumor protocol) before any invasive procedure.' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- must removed: 'Obtain pre-operative labs (CBC, BMP, coagulation, type and screen) before the neurosurgical procedure.' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- antibiotic-timing text: ESCMID 2024 qualifier (within about 24 hours) added (Q10: the withholding rule is conditional on neurosurgery within about 24 hours, ESCMID 2024)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic 'Study within normal limits.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Central vocabulary wired (24 Oct 2026)

Terms added by commit e19131d6 (batch-2 review vocabulary), wired as the plan and this log intended. The earlier CENTRAL vocabulary request in this log is resolved by them.

- New required criterion `action-aspirate-microbiology` (`order_microbiology` `{"specimen": "brain_aspirate"}`), after the tissue criterion, with a soft constraint tissue before it (the aspirate comes from the procedure) and added to the stop rule. Reason: the abscess is a live differential of this ring-enhancing mass until the aspirate is examined; Gram stain and culture of the aspirate are its microbiological test (ESCMID 2024, `[ESCMID_BA_2024]`, aspiration with microbiology strong). Blood cultures stay recommended (decision Q6).
- New follow-up `request_brain_aspirate_gram_stain_culture` (specimen `brain_aspirate`, after the tissue follow-ups): no organisms, necrotic debris without neutrophil sheets; no growth on aerobic or anaerobic culture at 5 days; collected before empirical antimicrobials (none in the preceding 4 weeks). The Gram stain and culture rows were removed from both tissue reports (the tissue tool returns histology and molecular assays; the frozen section stays), and the tissue expected evidence no longer cites them; the tissue label now says the aspirate goes to microbiology.
- `metadata.difficulty_rationale` updated to the 5 required criteria.

Checks after the change: `perfect_agent.py GLIO-HG-P03 -v` ok, `case_io.py check` (schema and synonym guard OK, no failure names the case), `test_case_guards.py -k "GLIO-HG- or ALZ-EARLY-"` 120 passed.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.

## MockServer routing (24 Oct 2026)

The MockServer now routes `analyze_eeg` by `eeg_type` (an order without it is a routine EEG; video-EEG and ICU continuous EEG are one study), serves an `interpret_labs` order only the stored panels that answer the assays it names, and treats `analyze_brain_mri.contrast` as false when omitted.

- `initial_tool_outputs.eeg`: `eeg_type` set to `routine`, read from the report's structure: hyperventilation or photic stimulation in a waking or drowsy record, with no sign of prolonged monitoring.

Checks: `perfect_agent.py --all` 600/600; full test suite 3503 passed; synonym guard 0 changes.
