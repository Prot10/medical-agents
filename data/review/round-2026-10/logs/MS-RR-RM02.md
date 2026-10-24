# MS-RR-RM02
Reviewer status: R1 not reviewed, R2 not reviewed (no MS-RR notes file in this round) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. All changes below are own findings and the condition plan (plans/MS-RR.md). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C | major | `patient.neurological_exam.cranial_nerves`, `.additional`, `patient.history_present_illness` | Left-eye acuity 20/60 with reduced colour saturation and left-eye floaters: monocular optic-nerve findings that a retrochiasmal lesion cannot cause, with no RAPD and no optic neuritis in the case (plan RM02). | FIXED: acuity 20/20 and full colour vision in both eyes; floaters deleted from HPI and exam; hemianopia macula-sparing; normal discs, no papilloedema stated (LP safety). |
| E | minor | `patient.history_present_illness` | Closing sentence steering toward "a possible autoimmune etiology". | FIXED: replaced by the fact "Her mother has systemic lupus erythematosus." |
| B | major | `fallback_tool_outputs.ct` | CT fallback "No acute intracranial abnormality" with a calcified granuloma, while the HPI reports an outside CT with a right parieto-occipital hypodensity and oedema. | FIXED: CT fallback shows the hypodensity with oedema, mild mass effect, no shift; `metadata.fallback_tool_kinds.ct` abnormal. |
| B | minor | `fallback_tool_outputs.advanced_imaging` | FDG-PET fallback "No abnormality identified" in a patient with a 4.2 cm lesion. | FIXED: mild marginal uptake below cortex, central hypometabolism, no intensely hypermetabolic focus. |
| D | major | `initial_tool_outputs.mri` | Finding type "Large demyelinating-appearing lesion"; DWI "likely reflecting active demyelination"; observation "raising the possibility of prior subclinical demyelinating events"; impression with a four-item differential and "no restricted diffusion" contradicting the rim restriction. | FIXED: neutral finding type, factual DWI and SWI, interpretive observations removed, impression with findings and a hedged imaging read. |
| B | minor | `initial_tool_outputs.mri.findings[3]` | Left frontal juxtacortical lesion; the earlier attack (right face and arm numbness) had no anatomical substrate. | FIXED: lesion placed in the left parietal juxtacortical white matter beneath the postcentral gyrus (same region for DIS). |
| A | major | `initial_tool_outputs.csf` | Myelin basic protein; no kFLC; flow cytometry "findings inconsistent with CNS lymphoma" (interpretation); recital interpretation with the junk "(N/A PMN/N/A lymph)" and em dashes. | FIXED: MBP removed; kFLC index 31.7 (reference < 6.1); flow cytometry reported as polyclonal without monoclonal B cells; pattern interpretation. |
| D | major | `initial_tool_outputs.labs` | "Mimic exclusion" panel with AQP4 and HIV carrying "excludes this reversible mimic"; MOG in a separate panel. | FIXED: "Demyelinating antibodies" panel (AQP4-IgG cell-based, MOG-IgG live cell-based) and a "Serology" panel (HIV), significance null; hedged antibody comment in the interpretation. |
| C | minor | `initial_tool_outputs.labs.panels.Inflammatory and Autoimmune Markers` | ANA 1:80 red herring and a pearl saying lupus-specific antibodies decide, but none were in the case; vitamin D 18 repeated across the batch. | FIXED: anti-dsDNA negative, ENA screen negative, C3 118 added; vitamin D 14 ng/mL. |
| A | major | `followup_outputs` MRS | Spectroscopy served by `analyze_brain_mri` (`request_mri_spectroscopy`), impression "See findings above", interpretive observations (plan G5). | FIXED: `order_advanced_imaging` MR_spectroscopy follow-up with quantitative data (NAA/Cr 1.3, Cho/Cr 1.4, Cho/NAA 1.1, Glx raised, small lactate and lipid) and a within-spectroscopy impression that does not exclude lymphoma. |
| A | major | `followup_outputs` repeat MRI | 3-month repeat MRI (a future scan, plan F). | FIXED: deleted. |
| B | minor | `followup_outputs[0]` spine | Impression "lateral cord" without level or side; "typical of demyelinating disease" interpretation; no measurements. | FIXED: right lateral column C5-C6, 9 mm, less than one third of the cross-section, non-enhancing; measurements; impression with level. |
| C | major | `followup_outputs` drug check | "Corticosteroids may reduce contraceptive efficacy" (false, F11); dexamethasone/PLEX/IVIG alternatives; DVT prophylaxis in an ambulant patient; 5-day fixed course. | FIXED: ibuprofen GI risk kept with acetaminophen or PPI; COC no interaction; sulfonamide allergy no cross-reactivity; steroid-before-biopsy warning; proposed 1 g for 3-5 days; alternatives empty. |
| C | major | `followup_outputs` literature | Wrong title for Lucchinetti 2008; Hardy 2016 attributed to JNNP with an invented title; an unverifiable Kiriyama 2011 study. | FIXED: Lucchinetti 2008 Brain (correct title), Hardy et al. 2016 Lancet Neurol, Montalban 2025; general summary; optional and last. |
| A | major | `ground_truth.action_criteria` | Template criteria; literature and drug required with non-schema keys; AQP4/MOG folded into a 11-panel labs criterion. | FIXED per plan 3.2: brain MRI, spine MRI, labs, AQP4/MOG required; CSF recommended; MRS, drug and literature optional, literature last. |
| A | minor | `ground_truth.stop_rule`, `sequence_constraints` | Literature and drug required; max 0; 2017 citation. | FIXED: required criteria only, max 3; canonical soft MRI-before-CSF. |
| C | major | `ground_truth.assessment.required_recommendations` | DIS/DIT recitals, AQP4/MOG test as a must, generic biopsy/IVMP/DMT/JCV/lifestyle lines. | FIXED: formulation (3 of 5 regions, DIT, CSF, earlier attack) once lymphoma is unlikely; IVMP after negative cytology/flow and MRS, ibuprofen stopped, PLEX if refractory; repeat MRI with biopsy for atypical evolution; driving advice for the hemianopia; DMT by activity with pregnancy discussion; pre-DMT screening; vitamin D replacement. |
| C | major | `ground_truth.assessment.prohibited_recommendations` | JCV (no result in case), fingolimod (no cardiac reason) and myelopathy (no myelopathic signs) items; em dashes. | FIXED: deleted; added steroids-before-cytology/tissue, CNS lupus on ANA alone and stroke prohibitions; resection item rewritten (F10). |
| C | major | `ground_truth.differential` | Lymphoma and glioma "high", NMOSD and MOGAD "moderate" against the case's own results. | FIXED: lymphoma, glioma, NMOSD, MOGAD, ADEM, CNS lupus low; stroke and abscess very low; features from the case. |
| C | minor | `ground_truth.key_clinical_evidence` | Template and engineering lines, "black holes contribute evidence of DIT" (wrong, F5), "biopsy a last resort". | FIXED: rebuilt from the case. |
| B | minor | `ground_truth.red_herrings` | Vitamin D value; em dash. | FIXED: ANA with SLE mother, vitamin D 14, outside CT read as ischaemia. |
| C | minor | `ground_truth.avoided_actions` | Template rationales and citations. | FIXED: case-tied rationales (CT already done before admission); `[Wattjes_2021]` for CT and PET. |
| E | minor | `metadata` | Pearls with ">90% specificity" and DMT advice; condition name with an em dash; difficulty text naming the removed CT stroke read as misdirection only. | FIXED: pearls rewritten; condition name; difficulty and revision fields. |
| A | minor | `fallback_tool_outputs.echo.echo_type` | Missing discriminator value. | FIXED: "TTE". |

## Changes, in one paragraph a physician can read before re-reviewing

A 29-year-old woman with five days of left homonymous hemianopia and a new headache, two weeks of right face and arm numbness 15 months ago, a mother with SLE, ibuprofen for migraine and an oral contraceptive. The eyes now have normal acuity and colour vision, as a retrochiasmal lesion requires. The MRI shows a 4.2 cm right parieto-occipital tumefactive lesion with open-ring enhancement and no shift, two periventricular lesions and a left parietal juxtacortical lesion; the spine shows a right lateral C5-C6 lesion: DIS 3 of 5 with DIT and positive CSF (three bands, kFLC 31.7). CSF cytology and flow cytometry are negative, AQP4/MOG negative, ANA 1:80 with negative dsDNA and ENA, and an optional MR spectroscopy favours demyelination. Required: brain MRI, spine MRI, mimic labs, AQP4/MOG; CSF recommended; MRS, drug check and literature optional; the future repeat MRI is gone. Musts: formulation once lymphoma is unlikely, IVMP only after cytology and flow with ibuprofen stopped, repeat MRI with biopsy for atypical evolution, no driving until fields are tested, DMT with pregnancy discussion, screening, vitamin D. The CT fallback now matches the outside CT.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[McDonald_2024]`, `[Wattjes_2021]`, `[NICE_NG220]` (plan 5.1); synonyms (plan 5.2).
- `test_guidance_claims`: RM02 now has `action-aqp4-mog-cba` (plan 5.3).

## Open questions for Andrea (judgment calls you could not settle)

- The plan names no CT change for RM02, but the CT fallback contradicted the HPI's outside CT, so it now shows the lesion; the CT avoided action stays because a CT was already done before admission. Please confirm.
- I added a driving must (left homonymous hemianopia in a woman who drives). If you consider it outside the scope of the assessment, it can be dropped without affecting the rest.
