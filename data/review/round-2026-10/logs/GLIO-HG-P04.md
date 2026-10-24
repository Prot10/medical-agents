# GLIO-HG-P04
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| ab9b72cb-94da-42c4-bcf2-df36b2e78190 | FIXED | No-seizure class (plan C5): the levetiracetam prophylaxis must is deleted and replaced by the canonical prohibition `prohibited_recommendations[4]` ("Do not start prophylactic antiseizure medication ... AIOM recommends against prophylaxis ..."). Levetiracetam removed from the drug-interaction follow-up (`proposed`, interaction, warning, lacosamide alternative) and from `action-9-check-drug-interactions` label and expected evidence. The EEG waste entry stays with the canonical rationale. |
| 16cb2bae-a4c1-408a-b7e1-015a21d1df63 | FIXED | "Excludes abscess" and "decisively" removed everywhere: must 1 now says the rim diffusion, rim rCBV 3.1 and absent amino acid peaks "support a high-grade neoplasm over abscess, but tissue with microbiology decides"; the old must 2 that duplicated it is merged; `key_clinical_evidence[1]` says perfusion "supports and targets the biopsy but does not exclude abscess"; the dental red herring no longer says "decisively"; the perfusion report impression no longer states the abscess rCBV; criterion texts for perfusion and spectroscopy reworded; `metadata.diagnostic_challenge_notes` "excludes" changed to "favours". The Law et al. attribution for abscess rCBV went with the deleted literature output (plan C1); `[Law_2003]` remains only on the perfusion criterion as the glioma-perfusion source. |
| 33019b2d-13f6-4d2e-a28c-8cd359884b11 | FIXED | `red_herrings[0].correct_interpretation`: the "steroid-mediated cytokine release" clause is deleted; the fever is now "non-specific and can accompany a necrotic high-grade tumour", with normal WBC and procalcitonin, negative blood cultures and a negative aspirate. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness` | A non-contrast CT "revealed a ring-enhancing lesion" (plan C8; class of P01 e25c4336); the charted ED impression repeated it. | FIXED: "a hypodense lesion ... with surrounding edema and 5 mm leftward midline shift"; ED impression "right temporoparietal lesion with edema: brain abscess vs. neoplasm, abscess more likely given dental source". |
| A | major | `action-3-search-medical-literature`, `initial_tool_outputs.literature_search` | Required literature step in the stop rule; the initial output quoted Law for abscess rCBV and served the discriminators to any query (ruling 5). | FIXED: criterion, stop-rule id and initial output deleted (initial `literature_search` null). |
| B | major | `initial_tool_outputs.tissue_diagnosis` | Tissue in the initial work-up; cultures listed as molecular findings; template meta-text; histology line carrying the integrated diagnosis (plan C2). | FIXED: two follow-ups, `request_stereotactic_aspiration_biopsy` and `request_resection` (gross total resection line), with frozen section, aspirate Gram stain, bacterial and fungal culture as `findings` rows only; integrated diagnosis "Glioblastoma, IDH-wildtype, CNS WHO grade 4"; impression per C2. |
| A | major | `action-11-obtain-tissue-diagnosis` | Assays without ATRX, with 1p/19q; stereotactic biopsy only (plan C3, C4). | FIXED: group B, `stereotactic_biopsy` then `resection`, each with `IDH1_IHC`, `ATRX_IHC`, `MGMT_methylation` (age 55, so IDH sequencing is not mandatory per EANO, but the report keeps it); ATRX IHC "Retained" added to the report; label and rationale per group B. |
| A | major | `action-10-order-microbiology` | Plan says to check it is the aspirate culture: it is the blood culture (the microbiology vocabulary has no brain-aspirate specimen). It required `before_antimicrobials`, Gram stain and susceptibility, which a correct blood-culture order need not name. | FIXED: kept required (febrile patient, plan keeps it required) and relabelled as blood cultures; required arguments reduced to `{specimen: blood_culture}`; report shows two sets with no growth at 5 days, drawn before any antimicrobial. The aspirate culture lives in the tissue criterion, whose label now names Gram stain and culture. See Open questions. |
| B | minor | `initial_tool_outputs.labs` | `type_and_screen` required but absent from the report; interpretive summary ("suboptimally controlled diabetes"). | FIXED: Blood_Bank row; factual summary and interpretation; labs expected evidence from the case values without the culture clause. Anion gap 138 - (101 + 24) = 13; MCHC 33.2. |
| D | major | MRI, perfusion, MRS reports | Capitals and teaching contrasts with abscess in the DWI field and impression; perfusion impression "inconsistent with pyogenic abscess ..."; MRS "argues against pyogenic abscess". | FIXED: within-modality findings; numbered MRI impression with one hedged differential line; perfusion and MRS findings without differential statements; quantitative fields filled. |
| C | major | `assessment.required_recommendations` | Interchangeable biopsy wording; Stupp template; dexamethasone template. | FIXED: group B surgery must; canonical dexamethasone must; glucose must specific to metformin and glipizide (insulin, taper); entity-specific treatment must with KPS 80 and MGMT unmethylated. |
| C | minor | `assessment.prohibited_recommendations` | Antibiotic prohibition framed as "premature treatment delays diagnosis of a fatal tumor"; dashes. | FIXED: "Do not start empirical antibiotics ... before the stereotactic aspirate is taken while he remains stable"; aspiration-without-histology prohibition reworded. |
| B | minor | DDI follow-up | Proposed levetiracetam; "HbA1c 7.8%" correct. | FIXED: dexamethasone against his five medicines, including glipizide hypoglycaemia during the taper and the amlodipine CYP3A4 effect; NKDA stated; guard passes. |
| A | minor | criteria | No performance status (C7). | FIXED: recommended `action-performance-status`, follow-up KPS 80, ECOG 1. |
| C | minor | `ground_truth.differential` | Abscess "high" and metastasis "moderate" at assessment time; radiation necrosis entry irrelevant (no irradiation). | FIXED: abscess low, metastasis, lymphoma, demyelination very low, with for and against; radiation necrosis removed. |
| C | minor | `key_clinical_evidence` | Overstated imaging ("excludes abscess", capitals). | FIXED: hedged and ending on tissue. |
| A | minor | citations, constraints, stop rule, avoided actions | Duplicate keys, `WHO_CNS5`; one template soft constraint; template waste rationales. | FIXED: hard MRI and labs to tissue; stop rule MRI, labs, blood cultures, tissue; canonical waste and LP rationales. |
| E | minor | `fallback_tool_outputs.drug_interactions.general.proposed`, `metadata.difficulty_rationale` | Engineering text; "5 required tools ... consults". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

A 55-year-old teacher with diabetes, a right temporoparietal ring-enhancing mass, a recent dental crown with peri-apical inflammation and a temperature of 37.9, and no seizures. The ED CT is now non-contrast (hypodense lesion, edema, 5 mm shift). Pathway: contrast MRI (thick nodular rim, rim restriction, no central restriction), perfusion (rim rCBV 3.1) and spectroscopy (no amino acid peaks), optional body CT, blood cultures (two sets, no growth, required), labs (CRP and ESR mildly raised, procalcitonin normal, glucose 148, HbA1c 7.8), performance status (KPS 80), then stereotactic aspiration and biopsy with frozen section, Gram stain and culture, or resection: glioblastoma, IDH-wildtype, CNS WHO grade 4, ATRX retained, MGMT unmethylated. Imaging is presented as favouring tumour, never as excluding abscess. The literature step and the prophylactic levetiracetam are gone (prophylaxis is now prohibited). Musts: aspiration then maximal safe resection, dexamethasone with insulin-ready glucose management, Stupp chemoradiation after the diagnosis; antibiotics are withheld until the aspirate while he is stable.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Criteria-pack allow-list: `[AIOM_brain]` (plan 5.1).
- Synonyms: accepted[0] reads "WHO grade 4 (right temporal-parietal lobe)" (plan 5.3); "astrocytoma grade 4" is wrong for IDH-wildtype glioblastoma (plan 5.2).
- Vocabulary: `order_microbiology` has no specimen for a brain abscess aspirate or tissue culture; today the aspirate culture can only be reported inside the tissue report. Consider a `tissue_or_aspirate` specimen if aspirate microbiology should be scorable on its own.

## Open questions for Andrea (judgment calls you could not settle)

- The plan assumed the required microbiology criterion was the aspirate culture; it is the blood culture. I kept it required (he is febrile with a plausible odontogenic source, and blood cultures before antibiotics are standard), which differs from P01 and P03, where blood cultures are recommended in afebrile or less febrile patients. The lead may want the three cases aligned.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the notes (ab9b72cb, 16cb2bae, 33019b2d) and the whole final case.
- Notes: all three are in the table and fixed. No prophylaxis must remains, the prohibition is present, and levetiracetam is absent from the DDI output and its criterion. "Excludes" and "decisively" appear nowhere, and there is no literature output. The steroid clause is gone from the fever red herring.
- Cross-field checks: the non-contrast CT in the HPI; the 37.9 C temperature in vitals and exam; NKDA; the DDI output against the five medicines; anion gap 13; MCHC 33.2; blood cultures drawn 2 weeks after the amoxicillin course; laterality (right inferior parietal lesion, left inferior quadrantanopia, left hemiparesis); procedure-matched tissue follow-ups.
- Found and fixed:
  - The perfusion criterion rationale still said a hyperperfused rim "supports a high-grade neoplasm over abscess" under `[Law_2003]`. This is the residue of note 16cb2bae: Law is not a source on abscess perfusion. The rationale now cites Law for glioma perfusion only: "A markedly hyperperfused rim supports a high-grade neoplasm and points the biopsy to the most vascular nodular rim; it does not exclude abscess, and the diagnosis remains tissue-based."
  - The MRI impression ended "Tissue diagnosis recommended." Deleted (C9).
- Reviewed and agreed: the worker kept the blood-culture criterion required (febrile, dental source) against the plan's assumption. This is defensible, since blood cultures before antibiotics are standard in suspected brain abscess. It remains flagged for the lead's alignment with P01 and P03.
- Minor, not changed: HbA1c 7.8 % is the same value as in P03. It is a plausible value, cited in five fields here, so I judged the edit churn.
- After the fixes: `perfect_agent.py` passes, `case_io.py check` reports no failure naming the case, and `test_case_guards` passes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `fallback_tool_outputs.literature_search` set to null and its entry removed from `metadata.fallback_tool_kinds` (plan C1, uniform with the other 26 cases).
- `fallback_tool_outputs.eeg`: the normal "no focal slowing" study replaced by focal polymorphic slowing over the lesion (continuous delta at T4, T6, P4), no epileptiform discharges, in the RS06 format; a normal EEG contradicts a hemispheric mass with oedema (same class as M04, RS05, RS06).
  `metadata.fallback_tool_kinds.eeg` updated to match.
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- accepted[0]: 'Glioblastoma, IDH-wildtype, WHO grade 4 (right temporal-parietal lobe)' -> 'Glioblastoma, IDH-wildtype, CNS WHO grade 4 (right temporal-parietal lobe)' (summary CENTRAL 3: WHO CNS5 writes "CNS WHO grade"; ruling 3 label correction)
- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- action-10-order-microbiology: required -> recommended, out of the stop rule (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- must removed: 'Obtain MRI brain with gadolinium (tumor protocol with DWI) before any invasive procedure.' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- must removed: 'Obtain pre-operative labs (CBC, BMP, coagulation, type and screen) before the neurosurgical procedure.' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- antibiotic-timing text: ESCMID 2024 qualifier (within about 24 hours) added (Q10: the withholding rule is conditional on neurosurgery within about 24 hours, ESCMID 2024)
- AIOM question numbers removed from the text (edition 2026 numbering unverified) (Q1: AIOM cited as the 2026 update; Quesito numbering not verifiable)
- fallback specialized_test (generic 'Study within normal limits.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['astrocytoma grade 4']; added ['glioblastoma idh wildtype'] (entity, grade and H3 scoping; summary CENTRAL 2).

## Central vocabulary wired (24 Oct 2026)

Terms added by commit e19131d6 (batch-2 review vocabulary), wired as the plan and this log intended. The earlier CENTRAL vocabulary request in this log is resolved by them.

- New required criterion `action-aspirate-microbiology` (`order_microbiology` `{"specimen": "brain_aspirate"}`), after the tissue criterion, with a soft constraint tissue before it (the aspirate comes from the procedure) and added to the stop rule. Reason: the abscess is a live differential of this ring-enhancing mass until the aspirate is examined; Gram stain and culture of the aspirate are its microbiological test (ESCMID 2024, `[ESCMID_BA_2024]`, aspiration with microbiology strong). Blood cultures stay recommended (decision Q6).
- New follow-up `request_brain_aspirate_gram_stain_culture` (specimen `brain_aspirate`, after the tissue follow-ups): no organisms; no growth on aerobic or anaerobic culture at 5 days; collected before empirical antimicrobials (last amoxicillin 2 weeks earlier, as in the blood-culture report). The Gram stain and culture rows were removed from both tissue reports (the tissue tool returns histology and molecular assays; the frozen section stays), and the tissue expected evidence no longer cites them; the tissue label now says the aspirate goes to microbiology.
- This closes the own finding on `action-10-order-microbiology`: that criterion stays the recommended blood culture; the aspirate culture the plan asked for is now its own required criterion. Fungal culture rows dropped (immunocompetent host). `metadata.difficulty_rationale` corrected (it still listed blood cultures as required and performance status as recommended).

Checks after the change: `perfect_agent.py GLIO-HG-P04 -v` ok, `case_io.py check` (schema and synonym guard OK, no failure names the case), `test_case_guards.py -k "GLIO-HG- or ALZ-EARLY-"` 120 passed.

## Discriminators and vocabulary (24 Oct 2026)

Discriminator fixes. The MockServer now routes stored reports by their discriminating field: a vocabulary value answers only its own study, an empty or prose value answers every variant of the tool (PATTERNS.md section 5).

- `fallback_tool_outputs.echo.echo_type` set to `TTE` (was missing): the report is a resting transthoracic study, and untyped it also answered TEE, bubble-study and exercise-echo orders.

Checks: `perfect_agent.py` ok; `case_io.py check` clean for this case.
