# BACT-MEN-RP02
Reviewer status: R1 none, R2 needs_changes | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| 10d64799-c48c-4aaa-984c-1519f29d9f52 | FIXED | CRITICAL ACTIONS: the "vancomycin + ceftriaxone" must is replaced by meropenem 2 g IV every 8 hours with vancomycin 15-20 mg/kg, ceftriaxone withheld for the documented hypersensitivity (`assessment.required_recommendations[0]`); a prohibition "Do not give ceftriaxone or cefotaxime" added; the drug check (`followup_outputs[3]`) proposes the same regimen and is now required. ORDERING: pathway reordered rather than the constraint dropped: blood cultures, CT (`followup_outputs[1]`), then the index LP (`followup_outputs[2]`, `request_lumbar_puncture`, moved out of `initial_tool_outputs.csf`); repeat LP deleted; HARD constraint CT before CSF kept. JUSTIFICATION: every IDSA 2004 criterion removed; CT label, must, prohibition, pearl and constraint reason now name "mild bilateral papilledema on fundoscopy" (WHO 2025 Annex A.4), and the reason says NICE NG240 does not cover her (recent neurosurgery). STEP 3: `collected_before_antimicrobials` false; impression "Collected while on meropenem 1 g IV every 8 hours and vancomycin 1 g IV every 12 hours (perioperative course)." BREAKTHROUGH: meropenem medication entry now reads "... prophylactic dosing, below the meningeal dose (sub-meningeal CSF exposure)"; the drug check and a pearl state that prophylactic doses do not reach meningeal concentrations. |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| A | major | `ground_truth.action_criteria[1].alternatives[0].required_arguments` | `before_antimicrobials: true` required while she is on IV meropenem and vancomycin, so a truthful order (`false`) would miss the criterion. | FIXED: argument removed (specimen and tests kept). Class issue (see Open questions). |
| C | major | `assessment.required_recommendations[1]`, `key_clinical_evidence[3]` | Template dexamethasone must "before or with the first antibiotic dose" in a patient on parenteral meropenem and vancomycin for days. | FIXED (departs from plan C5): must states adjunctive dexamethasone is not required because the WHO window (with the first dose) has passed and no trial supports starting it after days of parenteral therapy; if given, 4 days maximum. Template Gram-stain dexamethasone prohibition deleted. |
| B | major | `followup_outputs` (`request_repeat_lp`, `request_repeat_inflammatory_markers`, `request_pcr_panel`, `request_audiometry`, literature), `action-6-search-medical-literature` | Post-treatment repeat LP and 48-hour inflammatory markers (treatment response), duplicate PCR under `interpret_labs`, pre-treatment audiometry as `baep`, literature step with IDSA 2004 and ESCMID. | FIXED (C1, C8, C9): all deleted; hearing must added. |
| B | major | `patient.neurological_exam.mental_status` | "Alert but somnolent ... uncertain of date. GCS 14 (E3 V5 M6)": disorientation to date is V4 and E3 is not alert. | FIXED: "Somnolent, opens eyes to voice; ... GCS 13 (E3 V4 M6)". No effect on the imaging decision (GCS not below 10). |
| B | major | CSF report `opening_pressure` | Opening pressure 22 cmH2O "upper limit of normal" beside papilledema, the limb the reviewer ruled applies. | FIXED: 27 cmH2O (elevated). |
| B | minor | `patient.history_present_illness` | Timeline: blood patch "three days ago", fever 18 hours later, rash 3 hours later, then "over the subsequent 12 hours" (about 33 hours in all). | FIXED: "Over the subsequent 2 days". |
| D | minor | `patient.history_present_illness` | Last sentence listed the differential ("meningitis versus drug fever versus epidural abscess"). | FIXED (C12): deleted. |
| B | minor | `patient.clinical_history.past_medical_history[3]` | "Lumbar CSF drain placed and removed 5 days ago" against the HPI (placed intraoperatively 10 days ago). | FIXED: "placed intraoperatively 10 days ago and removed 5 days ago". |
| B | minor | `initial_tool_outputs.labs` | Eosinophils filed in the hepatic panel; differential summed to 102%; action-1 orders coagulation and HIV but neither was reported; no bilirubin; interpretive summary ("stress hyperglycemia", "intermediate zone"). | FIXED: eosinophils moved to CBC, neutrophils 74% and monocytes 2% (total 100%), PT 12.6 s, INR 1.0, aPTT 30 s, HIV non-reactive, bilirubin 0.5 mg/dL; summary as values with direction. |
| B | minor | CSF report (`RBC`, `glucose`, `glucose_ratio`, `CSF_lactate`, `CSF_culture`, PCR, `interpretation`) | RBC 120 "likely traumatic tap or related to recent procedures"; glucose 48 "low-normal"; ratio "reference >0.6"; lactate "<2.1"; culture "preliminary no growth at 24 hours" at the time of the LP. | FIXED (C7): canonical strings; culture "Pending (final report at 48 hours)"; PCR "no other panel target detected"; pattern-only interpretation. |
| B | minor | `followup_outputs[1].output` (CT) | "No contraindication to lumbar puncture"; findings with empty descriptions. | FIXED (C3): described findings and a findings-only numbered impression. |
| B | minor | `followup_outputs[0].output` (blood cultures) | No susceptibilities, although the must narrows by them; one set only. | FIXED (C6): two sets with intervals; penicillin 0.06 (susceptible, meningitis breakpoint), ceftriaxone 0.5 or less, meropenem 0.12, vancomycin 0.5. |
| B | minor | `followup_outputs[3]` (drug check) | Dexamethasone 0.15 mg/kg; chloramphenicol and linezolid alternatives; nothing on the new rash on current drugs. | FIXED (C9): meningeal regimen; ceftriaxone contraindication; prophylactic vs meningeal doses; new-rash warning; diphenhydramine sedation. Tier required (plan 4.0) with case-specific expected evidence, cited `[IDSA_2017_HCVM]`. |
| C | minor | `assessment.required_recommendations` | Two overlapping CSF-leak musts; "broaden coverage" must duplicated the regimen; generic oral-antibiotics prohibition irrelevant to an inpatient on IV therapy. | FIXED: one neurosurgery and leak-repair must; narrowing must on the MICs; pneumococcal conjugate vaccination must (CSF leak is an indication); drug-fever prohibition added; oral prohibition deleted. |
| C | minor | `ground_truth.differential` | Boilerplate (viral meningitis and HSV moderate, TB, cryptococcal, SAH) ignoring the entities the case raises. | FIXED (C10): drug fever, postoperative chemical meningitis, healthcare-associated staphylococcal or Gram-negative meningitis, spinal epidural abscess after the blood patch, viral meningitis, all low with the excluding result. |
| B | minor | `ground_truth.red_herrings` | "Sinus mucosal thickening on MRI" (no MRI; the sinuses were obliterated); Gram-stain red herring pointed at the initial CSF. | FIXED (C11): sinus red herring deleted; Gram-stain one points at the LP report; drug-fever red herring rewritten with the rash and eosinophilia. |
| A | minor | `action_criteria[*].citations`, `avoided_actions[*].citations` | Free-text duplicates, `[IDSA_2004]`, `[De_Gans_2002]`. | FIXED. |
| B | minor | `metadata.difficulty_rationale` | "5 required tools; 3 red herrings". | FIXED. |

## Changes, in one paragraph a physician can read before re-reviewing

The pathway is labs (coagulation, HIV and a corrected differential added), two sets of blood cultures, a required non-contrast CT before LP because of mild bilateral papilledema (WHO 2025 Annex A.4; NICE does not cover her after neurosurgery), the index LP, and a required drug check. The post-treatment repeat LP, repeat inflammatory markers, duplicate PCR, audiometry and literature step are gone. The CSF keeps the partially treated picture (85 cells, mixed, ratio 0.41, lactate 3.8, Gram stain negative, S. pneumoniae DNA on PCR), now with an opening pressure of 27 cmH2O that fits the papilledema. Blood cultures are flagged as taken on meropenem and vancomycin and give S. pneumoniae at 36 hours with susceptibilities. The record now says why the breakthrough happened: meropenem 1 g every 8 hours is a prophylactic, sub-meningeal dose. Musts: meropenem 2 g every 8 hours plus vancomycin with ceftriaxone withheld (IDSA 2017); dexamethasone not required because she has been on parenteral antibiotics for days; blood cultures; CT before LP; full CSF panel; narrowing on susceptibilities; droplet precautions; neurosurgical assessment and repair of the leak; pneumococcal conjugate vaccination; audiology. GCS corrected to 13 (E3 V4 M6), the HPI timeline made consistent, and the differential now covers drug fever, chemical meningitis, healthcare-associated organisms and epidural abscess, all excluded by the results.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Citation keys `[WHO_Meningitis_2025]` and `[IDSA_2017_HCVM]` for the criteria pack allow-list.
- Diagnosis synonyms: `accepted` carries "community acquired bacterial meningitis" for a meningitis after neurosurgery and lumbar drainage (plan section 5.5 raises the same for M05, RS04).

## Open questions for Andrea (judgment calls you could not settle)

- Dexamethasone: the plan's canonical must (start with the first antibiotic dose, 4 days for pneumococcus) does not fit a patient on parenteral meropenem and vancomycin for days; I wrote that it is not required. A reviewer should confirm.
- `before_antimicrobials: true` removed from action-2's required arguments (she is on antibiotics); the same question applies to every pretreated BACT-MEN case and needs a condition-wide decision.
- Opening pressure raised from 22 to 27 cmH2O so that the papilledema the reviewer ruled on is supported by the CSF. Alternatively drop the papilledema and keep CT as B (post-neurosurgical indication, IDSA 2017 recommends neuroimaging) without the HARD constraint.
- The pneumococcal vaccination must is new (not asked by the reviewer); delete if you want the musts limited to the acute episode.

## Verification

Adversarial verifier, 23 October 2026. Read the log, the diff and the whole patient, follow-ups and ground truth.
Checked: every part of note 10d64799 (meropenem 2 g every 8 hours plus vancomycin with ceftriaxone withheld,
and a matching prohibition; pathway reordered with the HARD constraint kept and satisfied; papilloedema as the
only limb, IDSA criteria gone; blood cultures `false` with the reviewer's line; the medication entry states
prophylactic, sub-meningeal dosing). Ceftriaxone appears nowhere as a recommendation; the drug check
(required, with concrete content) proposes the same regimen as the must. Cross-field: paired glucose 118,
ratio 48/118 = 0.41; anion gap 11; CBC differential 100% with eosinophils 6% matching the drug-fever red
herring; GCS 13 (E3 V4 M6) matches "somnolent, opens eyes to voice, uncertain of date"; opening pressure 27
fits the papilloedema; timeline (drain out 5 days ago, patch 3 days ago, fever 18 hours later, 2 days of
deterioration) consistent across chief complaint, HPI and history; meropenem MIC 0.12 susceptible by CLSI
(0.25 or less). The dexamethasone departure from plan C5 is clinically reasoned and flagged; kept.
Found and fixed: `key_clinical_evidence` said meningitis "after neurosurgery or skull base trauma" is treated
with vancomycin plus meropenem or cefepime (IDSA 2017). That regimen is the post-neurosurgical one; for a basilar
skull fracture without neurosurgery the pneumococcal-oriented regimen (a third-generation cephalosporin,
with vancomycin where resistance warrants it) applies, so the sentence overgeneralised. Now "Meningitis after neurosurgery, as here 10 days after
dural repair, is treated with vancomycin plus meropenem or cefepime (IDSA 2017)".
Left as logged: the condition-wide `before_antimicrobials` decision and the "community acquired" synonym.
`perfect_agent.py -v` and `case_io.py check` clean after the edit.

## Condition audit (23 October 2026)
- Condition-wide decision on the open `before_antimicrobials` question raised in this log: the argument is required only where the blood culture report flag `collected_before_antimicrobials` is true, and absent where it is false. This case already follows the rule (argument absent, flag false); no change to the case for it.

## Central (synonyms)

Synonym table scoped (October 2026, `diagnosis_synonyms.yaml`, applied with `apply_diagnosis_synonyms.py --prune --conditions ...`); `accepted[0]` unchanged.
"community acquired bacterial meningitis" removed: post-traumatic CSF-leak meningitis after an epidural blood patch (`except_cases` on `G00+community`).
- labels removed: "community acquired bacterial meningitis"
- `case_io.py validate` OK; `perfect_agent.py` passes.

## Open questions resolved (24 Oct 2026)

Andrea's ruling of 24 Oct 2026 (resolve open points for dataset quality); decisions and sources in `plans/BACT-MEN-decisions.md`.

- 'WHO 2025 Annex A.4' renamed 'WHO 2025 section A.4' (6 strings): the cranial imaging recommendations are section A.4 of chapter 3 of the guideline, not an annex
- Hearing must cites WHO 2025 (strong recommendation: formal audiological screening before discharge, or within four weeks of discharge), which covers every adult with acute meningitis, instead of NICE NG240, which excludes immunocompromised and neurosurgical patients

Re-run: `perfect_agent.py` ok; `case_io.py check` clean for the case; BACT-MEN case guards pass; synonym `--check` clean.
