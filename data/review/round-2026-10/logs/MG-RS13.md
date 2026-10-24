# MG-RS13
Reviewer status: not reviewed (no MG notes file) | Approved before this round: no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| --- | --- | --- |
| (none) | n/a | No reviewer notes for this case. Physician input applied: July 2026 tool guidance via plan MG.md (generalized AChR+ pathway, section 3.5). |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |
| --- | --- | --- | --- | --- |
| B | major | `patient.history_present_illness` | Timeline impossible: onset "Eight weeks prior to the current admission" but "Now, 8 months after the initial presentation" (PMH: Brown syndrome diagnosed 8 months ago). | FIXED: "Eight months prior to the current admission". |
| D | major | `patient.history_present_illness`, `patient.neurological_exam.cranial_nerves`, `patient.physical_exam.neurological` | The ice pack result (4 mm bilaterally) was in the patient block while the ice pack test is a scored criterion (result already "done"). | FIXED: result removed from HPI and exam; ice pack follow-up now holds it (MRD1 right 0.5 to 4.5, left 1.0 to 5.0 mm after 5 minutes). SLURP and Cogan signs stay as exam. |
| B | major | `ground_truth.red_herrings[2]`, `patient.history_present_illness` | Red herring "ANA 1:160" contradicted the HPI ("serological testing for SLE ... negative") and no report held it. | FIXED: HPI states the prior rheumatology work-up (ANA 1:160, negative anti-dsDNA, anti-ENA, RF, anti-CCP, normal C3/C4, no CTD); red herring field path set. |
| A | minor | `patient` top-level duplicates; medication indications and PMH | Extra keys (class K); em dashes in "Presumed Brown syndrome — under review" and PMH. | FIXED: ethnicity to demographics, duplicates removed; dashes replaced by parentheses or commas. |
| B | minor | `patient.physical_exam.general`, `.abdomen` | No weight/height for mL/kg; "(prednisolone effect)" interpretation in the exam. | FIXED: "Weight 72 kg, height 168 cm" (BMI 25.5 as stored); "mild cushingoid features", "mild central adiposity". |
| A | major | `followup_outputs[request_achr_musk_lrp4_antibodies]`, `initial_tool_outputs.labs` | Serology behind a TSH stub (H6, G); blocking in nmol/L; MuSK <0.4. | FIXED: initial labs AChR binding 4.8 nmol/L (kept), blocking 31%, MuSK <0.01 (Mayo-style), TSH 1.6, free T4 1.3, anti-TPO 186 IU/mL (consistent with Hashimoto hypothyroidism), TRAb negative (thyroid eye disease in the differential, fact 3); follow-up deleted. |
| C | major | `followup_outputs[request_pyridostigmine_trial]`, criterion `action-6-check-drug-interactions` | Drug output with a "trial" trigger, "hydroxychloroquine has been used off-label in some NMJ disorder protocols" (wrong, fact 23), generic required criterion. | FIXED: follow-up deleted (J); one `initial_tool_outputs.drug_interactions` in checker voice: hydroxychloroquine a drug of caution in MG, no pyridostigmine interactions, methotrexate teratogenicity; criterion recommended (pyridostigmine or hydroxychloroquine). |
| D | major | `followup_outputs[search_brown_syndrome_vs_mg]`, `[request_mgtx_thymectomy]`, criterion `action-5-search-medical-literature` | Two literature follow-ups, one with a patient-specific conclusion ("should trigger NMJ evaluation"); required literature step. | FIXED: both deleted; canonical initial literature output; criterion optional, last. |
| B | minor | `followup_outputs` RNS, SFEMG, respiratory, ice pack | RNS and SFEMG without structured values; respiratory and ice pack stubs repeating the expected text (I). | FIXED: RNS with CMAPs, temperature, brief-exercise (no facilitation), decrements 18/14/11% kept; SFEMG 64 microseconds, 24% blocking kept with pairs; respiratory FVC 3.08 L (88%, 43 mL/kg), MIP -64, MEP 82; ice pack as above. |
| D | minor | `initial_tool_outputs.body_imaging`, `.ecg`, `fallback_tool_outputs.ct` | Indication "New MG diagnosis"; ECG note about hydroxychloroquine and template PR/QRS/rate 72 against HR 78; fallback "does not address the question". | FIXED: "Evaluation for thymoma", region chest/mediastinum; ECG rate 78, PR 150, QRS 86, QTc 418 without drug commentary; canonical head CT text. |
| C | major | `ground_truth.assessment` | Musts were tests; no plan for the prednisolone taper, hydroxychloroquine or methotrexate started for a withdrawn diagnosis; no thymectomy must at 47. | FIXED: musts: revised diagnosis, pyridostigmine, keep prednisolone at 25 mg rather than tapering off (bone, glucose), stop hydroxychloroquine, azathioprine after TPMT replacing methotrexate (contraception while on it), thymectomy per MGTX, ophthalmology co-management. Prohibitions: canonical steroid, canonical drug, no strabismus/tendon surgery, no abrupt prednisolone stop. |
| C | minor | `ground_truth.differential` | Key features not tied to results; hydroxychloroquine as a possible contributor missing. | FIXED: each entry states the excluding result; MS very_low; drug-induced worsening (HCQ) added low. |
| E | minor | criteria, `key_clinical_evidence`, `avoided_actions`, `red_herrings`, `sequence_constraints`, `stop_rule`, `metadata` | Template criteria with labels equal to rationales, Wolfe 2016 everywhere, template pearls, labs -> RNS constraint with SFEMG reason, stop rule with literature and drug check (max 0), "1 red herrings". | FIXED: criteria per plan 3.2 (labs, RNS, CT required; ice pack, respiratory, drug review recommended; SFEMG and literature optional); case-specific evidence; red herring paths; constraint removed; stop rule labs, RNS, CT, max 2; difficulty text updated. |

## Changes, in one paragraph a physician can read before re-reviewing

AChR-positive generalized MG in a 47-year-old woman labelled acquired Brown syndrome for 8 months (the HPI timeline is now consistent). The ice pack result was moved out of the exam into its own report, and the prior rheumatology serology (ANA 1:160 otherwise negative) is stated in the HPI so the ANA red herring rests on data. Required: AChR serology with thyroid function (AChR 4.8 nmol/L, MuSK negative, TSH normal on levothyroxine, anti-TPO positive, TRAb negative), RNS (11-18% decrement), mediastinal CT with contrast (no thymoma). Recommended: ice pack, respiratory function (normal), and a medication review whose output flags hydroxychloroquine as a drug of caution in MG. SFEMG and literature are optional; the "pyridostigmine trial" drug output and both literature follow-ups were deleted. Musts: revise the diagnosis, start pyridostigmine, hold prednisolone at 25 mg instead of tapering off, stop hydroxychloroquine, move from methotrexate to azathioprine after TPMT, thymectomy per MGTX, and ophthalmology co-management; no strabismus surgery.

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

- Text citations `[Jacob_2025]`, `[Evoli_2019]`, `[Lawn_2001]`, `[Narayanaswami_2021]` (plan CENTRAL 1).
- `icd_codes[0]` G70.01 for a stable new diagnosis (plan CENTRAL 2).

## Open questions for Andrea (judgment calls you could not settle)

- Departures from plan MG.md, decided on clinical grounds: (1) the drug check is recommended, not optional, because she is taking hydroxychloroquine, a drug of caution in MG prescribed for the withdrawn diagnosis (the plan makes the same call for MG-M02); (2) no orbit MRI criterion was added: two orbital MRIs during the last 8 months are in the history and the stored MRI is a third normal study, so a further MRI adds nothing.

## Verification

Verifier, 24 Oct 2026 (adversarial pass; no reviewer notes exist for MG, so the table check is the "no reviewer notes" row).

Checked: timeline (onset 8 months before admission, consistent with PMH and the later paragraph); ice pack result no longer in the patient block; ANA red herring now rests on the HPI; anti-TPO positive fits treated hypothyroidism and the maternal Hashimoto history; hydroxychloroquine drug output agrees with the medication list; musts (keep prednisolone 25 mg, stop HCQ, azathioprine after TPMT replacing methotrexate, thymectomy at 47) do not contradict the prohibitions (no abrupt stop, no strabismus surgery); the worker's two departures from the plan (drug check recommended; no orbit MRI criterion) are clinically sound and logged.

- Found (all six RS11-RS16, missed by the worker, PATTERNS 5 discriminators): `fallback_tool_outputs.echo` had no `echo_type` and `fallback_tool_outputs.advanced_imaging` carried a prose modality, so a normal report answered every echo and every advanced-imaging variant. Changed: echo fallback `echo_type: TTE` (its content is a normal TTE); advanced-imaging fallback set to null and `metadata.fallback_tool_kinds.advanced_imaging` removed, so the library answers per modality (probed: MR_angiography and TEE orders get their own library reports).
- No other error found.

Checks re-run after the edits: `perfect_agent.py -v` passes (only the known mediastinum_MRI alternative served by the library normal), `case_io.py check` clean for the case, `test_case_guards.py -k` passes, and the 24 Oct discriminator guard (run by hand; MG is not yet in `DISCRIMINATOR_CONDITIONS`) reports no defect.
