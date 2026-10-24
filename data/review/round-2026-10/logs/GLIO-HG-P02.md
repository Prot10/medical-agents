# GLIO-HG-P02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 5481518a-4352-4899-bae9-7a49bcba599b | FIXED | Chose "remove the step": the `analyze_csf` follow-up (`request_csf`, positive cytology, monoclonal B cells, CSF EBV DNA 45,000) is deleted; the diagnosis now comes from the stereotactic biopsy. `avoid-harm-1-analyze-csf` stays harm with the canonical rationale "Lumbar puncture is contraindicated with 6 mm midline shift and bilateral papilledema: the pressure gradient risks herniation [Hasbun_2001]."; the LP prohibition is reworded without a dash. `key_clinical_evidence[3]` now says CSF cytology and flow wait until the mass effect has resolved, and the staging must says the same. |
| 5dae46fc-6da9-4e5b-941a-bf0ad76a3693 | FIXED | Chose "withhold steroids": the dexamethasone loading-dose must and the "defer corticosteroids" must are replaced by one must, `required_recommendations[2]`: "Withhold corticosteroids until the stereotactic biopsy is obtained, because they can render lymphoma non-diagnostic; give dexamethasone first only if herniation is impending [EANO_PCNSL_2015]." GCS 14 with 6 mm shift is not impending herniation. |
| 20ea01fe-64cb-4c7b-a5ae-8f2a7f837048 | FIXED | `action-9-obtain-tissue-diagnosis.alternatives[0].required_arguments.molecular_assays` is now `["CD20_IHC", "EBER_ISH"]` (procedure `stereotactic_biopsy` only, plan group C). The tissue report (now `followup_outputs[4]`, `request_stereotactic_biopsy`) has one `findings` row and one `molecular_findings` entry for CD20 IHC and EBER ISH, plus CD79a, CD10 (negative), BCL6, MUM1 (non-germinal centre by Hans), Ki-67, GFAP and IDH1 R132H rows. Flow cytometry on tissue is not added (no data in the case; the plan allowed it as optional). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| B | major | `initial_tool_outputs.tissue_diagnosis` | Biopsy result served in the initial work-up (plan C2); site "targeted on the contrast-enhancing rim" for a homogeneously enhancing mass; template WHO meta-text in the impression. | FIXED: moved to a `obtain_tissue_diagnosis` follow-up, initial set to null; site "enhancing component (stereotactic target)"; integrated diagnosis in pathology voice "Diffuse large B-cell lymphoma, EBV-positive, non-germinal centre B-cell phenotype, involving the brain"; impression "Integrated diagnosis: ...". Histology row added. |
| A | major | `action-3-search-medical-literature` | Literature as a clinical step (ruling 5, plan C1); its expected evidence had no stored output, which made the baseline perfect-agent check fail. | FIXED: criterion deleted (it was not in any constraint or the stop rule). No literature output existed. |
| A | major | `assessment.required_recommendations[3]` | Must demanded HIV testing, CD4 and viral load, but no criterion ordered them; the results were bundled into the routine labs. | FIXED: new required criterion `action-hiv-testing` (`interpret_labs {panels: [HIV]}`), in the stop rule, soft constraint before the biopsy; HIV, CD4, viral load, toxoplasma and EBV serology moved from `initial_tool_outputs.labs` to a follow-up `request_hiv_cd4_viral_load_toxoplasma_serology`, with an HIV-1/2 differentiation row confirming the 4th-generation screen. `-v` confirms the criterion receives it. |
| B | major | `followup_outputs` (`request_perfusion` under `analyze_brain_mri`, `request_perfusion_mri`) | Two perfusion outputs: the real one (rCBV 2.4, homogeneous) under the wrong tool, and a template one ("rCBV typically > 1.75") under the criterion's tool. | FIXED: one `order_advanced_imaging` perfusion_MRI report with the real values and a within-imaging impression; the duplicate deleted. Expected evidence rewritten from it. |
| D | major | `followup_outputs` (`request_pet_ct`) | FDG PET-CT filed under `interpret_labs` with interpretive values ("HIV-related, not lymphomatous"). | FIXED: deleted (plan C14). Its body findings (axillary nodes, spleen 14 cm) are carried into the CT chest/abdomen/pelvis, which previously reported no lymphadenopathy despite palpable cervical and axillary nodes. |
| B | major | `initial_tool_outputs.body_imaging` | CT reported "no adenopathy" and normal spleen against the exam, and its impression did cross-modality synthesis ("supports a primary CNS process"). | FIXED: bilateral axillary nodes up to 1.3 cm with fatty hila, spleen 14 cm without focal lesion; impression imaging-only. |
| C | minor | `action-8-order-body-imaging` | Optional, framed as metastasis exclusion. In suspected lymphoma with generalized lymphadenopathy, body imaging distinguishes primary from secondary CNS lymphoma and is standard staging. | FIXED: recommended, relabelled, expected evidence from the CT (deviation from plan 3.1, see Open questions). |
| D | major | `initial_tool_outputs.mri` | Teaching text in a report ("important distinction from GBM", "GBM typically ...", capitals). | FIXED: findings in radiology voice; numbered impression; "No additional intracranial lesion" added as a pertinent negative (the deleted PET reported no other CNS lesion). The imaging differential stays hedged and does not name the answer outright. |
| D | minor | MRS follow-up | "argues against IDH-mutant glioma" parenthetical; impression "Tissue diagnosis is required" with no findings. | FIXED: numbered impression of the measured metabolites. |
| B | minor | `initial_tool_outputs.eeg.impression` | Impression omitted the right frontal delta in the findings. | FIXED: ACNS-style impression listing both abnormalities. |
| E | major | `initial_tool_outputs.labs.panels["Baseline workup"]` | Engineering text ("which is what this case's diagnosis rests on") and no actual coagulation values although a biopsy is required (plan C10). | FIXED: Coagulation panel PT 12.6 s, INR 1.0, aPTT 32 s, fibrinogen 410 (H, consistent with the inflammatory state); Blood_Bank row "Group A, RhD positive; antibody screen negative"; `clinical_significance` null; summary and interpretation recomputed. Hb/Hct 11.2/33.8 gives MCHC 33.1. |
| E | minor | `fallback_tool_outputs.drug_interactions.general.proposed` | "(agent not specified on this case's pathway)" served to the agent. | FIXED: "Agents as entered". |
| C | major | `assessment.required_recommendations` | Stupp/temozolomide must for a lymphoma; no opportunistic-infection prophylaxis at CD4 82 with Toxoplasma IgG positive; no lymphoma staging. | FIXED: plan's haematology/neuro-oncology and antiretroviral must; TMP-SMX prophylaxis must with atovaquone around methotrexate (TMP-SMX increases methotrexate toxicity); staging must (slit-lamp, body CT or PET-CT, bone marrow biopsy, CSF once mass effect resolved). Surgery must rewritten for group C. |
| C | minor | `assessment.prohibited_recommendations` | No seizure, no prophylaxis prohibition (plan C5); resection prohibition with a dash. | FIXED: canonical no-prophylaxis prohibition; resection prohibition reworded. |
| A | minor | `action_criteria`, follow-ups | No performance status (plan C7). | FIXED: `action-performance-status` recommended (age 56) and a follow-up: KPS 60, ECOG 2 from the exam (unsteady but independent gait, needs prompting and occasional help because of confusion). |
| C | minor | `ground_truth.differential` | Toxoplasmosis listed twice; GBM and toxoplasmosis "moderate" after a diagnostic biopsy; systemic lymphoma, which the lymphadenopathy raises, absent. | FIXED: duplicates merged, assessment-time likelihoods with for/against features; "Secondary CNS involvement by systemic lymphoma" added at low. |
| C | minor | `red_herrings` | Toxoplasma IgG positive in AIDS is the strongest distractor and was not addressed. | FIXED: second red herring; first one completed with its `field_path`. |
| A | minor | citations | Duplicate unbracketed keys, `WHO_CNS5`, `[Stupp_2005]` on the MRI criterion. | FIXED per plan 1.1. |
| B | minor | `action-2-interpret-labs` | Template expected evidence and "craniotomy". | FIXED: the case's own values, "before stereotactic biopsy". |
| A | minor | `sequence_constraints`, `stop_rule` | Single soft template constraint. | FIXED: hard MRI to tissue, hard labs to tissue, soft HIV to tissue; stop rule MRI, labs, HIV, tissue. |
| C | minor | DDI | No interaction check although methotrexate, TMP-SMX and antiretroviral therapy will start together. | FIXED: optional `action-check-drug-interactions` (last) with a follow-up listing methotrexate with TMP-SMX, PPIs and tenofovir, and the booster warning; its text does not repeat the expected evidence (guard passes). |
| B | minor | `metadata.case_body_concerns`, `difficulty_rationale` | Duplicated stale literature concerns; "4 required tools". | FIXED: stale entries removed; rationale updated. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway is now: contrast MRI (homogeneous enhancement without necrosis, diffuse restricted diffusion, subependymal and callosal spread, single lesion, 6 mm shift), perfusion (rCBV 2.4, homogeneous) and spectroscopy (high choline, lipid-lactate, no 2HG), body CT (small axillary nodes with fatty hila, spleen 14 cm, no extracranial mass), routine pre-operative labs with real coagulation values, HIV testing (HIV-1, viral load 156,000, CD4 82, Toxoplasma IgG positive and IgM negative, blood EBV DNA 12,400), performance status (KPS 60, ECOG 2), stereotactic biopsy (EBV-positive DLBCL, CD20 and EBER positive, non-GCB, GFAP and IDH1 negative) and an optional interaction check. The lumbar puncture that delivered the answer, the PET-CT filed as a lab, the duplicate perfusion and the literature step are gone. Steroids are withheld until biopsy (dexamethasone only for impending herniation); resection, LP and antiseizure prophylaxis are prohibited. Musts add TMP-SMX prophylaxis with atovaquone around methotrexate, lymphoma staging, and haematology/neuro-oncology referral for methotrexate-based induction with antiretroviral therapy.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Criteria-pack allow-list: `[EANO_PCNSL_2015]` (Hoang-Xuan K et al. Lancet Oncol 2015;16:e322-e332), as plan section 5.1.
- Synonyms: the accepted list carries no "HIV-associated" or "AIDS-related" variant ("AIDS-related primary CNS lymphoma", "HIV-associated CNS lymphoma", "EBV-positive diffuse large B-cell lymphoma of the CNS"); consider adding them to `diagnosis_synonyms.yaml` for C83.39.
- Vocabulary: `flow_cytometry` exists only for `analyze_csf`, not as a tissue assay; not needed for this case.

## Open questions for Andrea (judgment calls you could not settle)

- Plan open question 6 (label): decided to keep accepted[0] unchanged. It names a real clinical entity, no reviewer ruled it wrong, and ruling 3 forbids changing it otherwise. Note for the record that WHO-HAEM5 reserves "primary large B-cell lymphoma of immune-privileged sites" for immunocompetent patients and files this as an immunodeficiency-associated EBV-positive DLBCL; the tissue report uses that pathology wording.
- Deviation from plan 3.1: CT chest/abdomen/pelvis is recommended here, not optional, because lymphoma staging requires body imaging and the patient has generalized lymphadenopathy. HIV testing is a new required criterion because the accepted label names newly diagnosed HIV/AIDS and a must demanded it.

## Verification

Adversarial verifier, 24 Oct 2026. Read the log, the notes (5481518a, 5dae46fc, 20ea01fe) and the whole final case.
- Notes: all three are in the table and are fixed in every place they apply. No CSF follow-up remains and LP stays harm in both the avoided action and the prohibition. There is one steroid must (withhold until biopsy) and no loading-dose must; the HPI records no steroid given. The tissue criterion requires `CD20_IHC` and `EBER_ISH`, and the biopsy report has a row and a molecular entry for each.
- Cross-field checks, all consistent: MCHC 33.1, anion gap 12, PT/INR, the CD4/toxoplasma IgG prophylaxis must against the DDI output, NKDA, no medicines. Laterality is consistent (right frontal lesion, left arm signs). The perfusion, MRS, CT and HIV panel values match their expected evidence. The differential matches the final evidence, and the red herrings match the printed findings.
- Found and fixed: (1) The MRI impression still ended "Tissue diagnosis recommended.", a management line in a report (plan C9). Deleted. (2) The perfusion criterion label was the glioma template "target highest-grade region for biopsy", which is wrong for a lymphoma. It now reads "to assess the vascularity of the mass and guide the biopsy target".
- Left as is: the hedged MRI differential naming "a hypercellular lymphoid or round-cell neoplasm" (kind 2: the pattern is what MRI legitimately shows). The deviations from the plan that the worker logged (CT CAP recommended, HIV testing required) are clinically sound.
- After the fixes: `perfect_agent.py` passes, `case_io.py check` reports no failure naming the case, and `test_case_guards` passes.

## Condition audit (24 Oct 2026)

Condition auditor, cross-case uniformity pass. Changed:
- `fallback_tool_outputs.literature_search` set to null and its entry removed from `metadata.fallback_tool_kinds` (plan C1, uniform with the other 26 cases).
- `ground_truth.red_herrings[1].field_path` was empty: now `followup_outputs[2].output.panels.HIV_and_opportunistic_infection_serology[5]`.
- `patient.history_present_illness`: "a CT head revealed an enhancing brain lesion" now "a CT head revealed a right frontal mass with surrounding edema" (non-contrast CT cannot show enhancement; C8 class).
Re-ran perfect-agent (30/30 pass), `case_io.py check` (no failure names the case) and the case guards (60 passed).

## Close-out (24 Oct 2026)

Decisions in `plans/GLIO-HG-decisions.md` (Andrea, 24 Oct 2026: open points resolved for dataset quality).

- action-performance-status: recommended -> required (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- stop rule: + action-performance-status (Q3: KPS selects the treatment branch in every case, EANO 2021; Reviewer 2 RP04 0289beef applied as a class)
- must removed: 'Obtain MRI brain with and without gadolinium contrast (tumor protocol) before any invasive procedure.' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- must removed: 'Obtain pre-operative labs (CBC, BMP, coagulation, type and screen) before the stereotactic biopsy.' (Q9: diagnostic step restating a required criterion; musts are management, ruling 4)
- fallback specialized_test (generic 'Study within normal limits.', test_type '') -> null; the library answers by test_type (auditor flag, S01 class: a case fallback is served for any order of the tool, whatever the test type)
- Synonyms re-expanded from `diagnosis_synonyms.yaml` (`--prune --conditions brain_tumor_glioma`): removed ['cns lymphoma']; added ['primary cns diffuse large b cell lymphoma', 'hiv associated cns lymphoma', 'aids related cns lymphoma', 'ebv positive diffuse large b cell lymphoma cns'] (entity, grade and H3 scoping; summary CENTRAL 2).
