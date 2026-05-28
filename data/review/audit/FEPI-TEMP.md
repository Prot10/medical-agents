# NeuroBench v5 audit — FEPI-TEMP (focal temporal-lobe epilepsy)

Scope: all 20 `FEPI-TEMP-*` cases (M01–M03, P01–P03, RM01–RM03, RP01–RP03, RS01–RS04, S01–S04).
Each case read in full (patient, exam, every initial/followup/fallback tool output, full ground_truth, metadata)
against the FEPI-TEMP criteria pack and the tool-report style guide.

Mechanical validators across all 20 cases at start: coherence 0/0, schema 20/20 valid, tool-vocab clean,
answer-leakage 0 candidates except one S02 "DNET" hit judged a legitimate Kind-2 within-modality imaging
diagnosis (KEPT, not a leak). Condition-specific KEEP rules honoured: EEG epileptiform patterns and MRI
mesial temporal sclerosis are KEPT; no EEG report says "epilepsy".

| case_id | dim | severity | region.field path | finding | action | detail |
| --- | --- | --- | --- | --- | --- | --- |
| FEPI-TEMP-M03 | B | minor | followup_outputs[6].output.warnings[2] (check_drug_interactions) | Warning cited "penicillin allergy (urticaria)" but the patient's documented allergy is Sulfonamides (rash) | FIXED | Aligned warning to documented allergy: "Patient has sulfonamide allergy (rash)…" |
| FEPI-TEMP-M03 | C | nit | initial_tool_outputs.labs Magnesium | Mg 2.3 flagged high vs stated range 1.7–2.2; range upper bound is on the low side (many labs use up to 2.4) | FLAGGED | Internally consistent (value > stated range); range choice is defensible. Not changed. |
| FEPI-TEMP-P01 | B | major | patient.social_history.occupation vs patient.history_present_illness | occupation = "graduate student" but HPI calls her an "elementary school teacher" on medical leave from teaching with students | FLAGGED | Patient-story contradiction; appended to metadata.case_body_concerns. Do not auto-rewrite the narrative. |
| FEPI-TEMP-P01 | C | major | ground_truth.primary_diagnosis / key_reasoning_points | Diagnosis labelled "drug-resistant" invoking Kwan 2010 (≥2 failed AEDs), but patient never trialed any AED (only sertraline + PRN lorazepam) | FLAGGED | Refractoriness was to anxiolytics, not AEDs; formal drug-resistance criteria not met as written. Appended to case_body_concerns. Clinician adjudication needed. |
| FEPI-TEMP-P01 | B | nit | followup_outputs[6].output.warnings[2] | Warning says "penicillin allergy (hives)"; documented allergy is "Penicillin (rash)" | FLAGGED | Allergen matches; reaction wording (hives vs rash) is within the same family. Not changed. |
| FEPI-TEMP-P02 | E | minor | followup_outputs[4].output (order_specialized_test, neuropsych) | "52 seconds seconds" / "138 seconds seconds" duplicated unit word (Trail Making A/B, findings + quantitative_data + impression) | FIXED | Removed duplicated "seconds" (5 occurrences). |
| FEPI-TEMP-P02 | B/E | minor | followup_outputs[1].output.interpretation (analyze_csf) | Broken templated CSF interpretation: "WBC: N/A (N/A PMN/N/A lymph)" placeholder contradicting populated values (WBC 5, 100% lymphocytes) | FIXED | Rewrote to faithful within-modality recital of the actual values + special tests (LGI1 CSF positive kept as fact). |
| FEPI-TEMP-P02 | D | minor | initial_tool_outputs.mri.additional_observations[0-1] | "This is hippocampal SWELLING, NOT atrophy — an important distinction from mesial temporal sclerosis" reads as a teaching parenthetical with caps | FLAGGED | Within-modality imaging content; conservative not to strip. Style-guide borderline. |
| FEPI-TEMP-RM01 | B | minor | followup_outputs[1].output.impression (analyze_brain_mri) | Impression said "Right hippocampal volume 2.1 cm3, left 3.6 cm3" but the structured findings + volumetrics in the same report say 2.6 / 3.7 | FIXED | Corrected impression numbers to 2.6 / 3.7 to match the structured data. |
| FEPI-TEMP-RM01 | C | major | neurological_exam vs initial_tool_outputs.mri / FDG-PET | LEFT spastic hemiparesis + left facial droop, but the structural lesion (encephalomalacia, ex vacuo dilatation) is described as LEFT frontoparietal on MRI and PET | FLAGGED | Left-hemisphere lesion would be expected to cause right-sided weakness; laterality mismatch. Appended to case_body_concerns. Clinician adjudication needed (do not auto-flip). |
| FEPI-TEMP-RP01 | B/E | minor | followup_outputs[0].output.interpretation (analyze_csf) | Broken templated CSF interpretation: "(N/A PMN/N/A lymph)" placeholder | FIXED | Replaced with actual differential "100% lymphocytes"; HSV-1 PCR positive kept as fact. |
| FEPI-TEMP-RP02 | B/C | minor | ground_truth.primary_diagnosis vs case body | Primary dx asserts "concurrent unrelated pulmonary embolism" but PE is never confirmed by available tools (ECG/echo/Holter all normal; D-dimer nonspecific; no CTPA in toolset) | FLAGGED | Intended diagnostic-puzzle red herring; CTPA outside NeuroBench toolset is a known limitation. Clinician note. |
| FEPI-TEMP-RP03 | B/E | minor | followup_outputs[2].output.interpretation (analyze_csf) | Broken templated CSF interpretation: "(N/A PMN/N/A lymph)" placeholder | FIXED | Replaced with actual differential "92% lymphocytes, 8% monocytes". |
| FEPI-TEMP-RS01 | E | minor | followup_outputs[4].output (order_specialized_test, neuropsych) | "Xth percentile percentile" duplicated word (4 distinct values, in findings, quantitative_data, impression) | FIXED | Removed duplicated "percentile" everywhere. |
| FEPI-TEMP-RS01 | B | minor | difficulty vs metadata.difficulty_description | difficulty enum = "diagnostic_puzzle" + complex difficulty_rationale, but difficulty_description reads "Straightforward … minimal confounders" (confidence 0.85) | FLAGGED | Stale description; appended to case_body_concerns. Do not auto-change the difficulty enum. |
| FEPI-TEMP-RS02 | B | nit | difficulty vs metadata.difficulty_description | difficulty = "moderate" but difficulty_description reads "Straightforward …" (confidence 0.85) | FLAGGED | Minor stale-description gap (moderate vs straightforward). Not changed. |
| FEPI-TEMP-RS02 | D | minor | initial_tool_outputs.ecg.interpretation | ST-elevation V2-V3 interpretation argues against pericarditis/ACS ("less likely … atypical for early repolarization") — leans toward prohibited differential-refutation | FLAGGED | Within-cardiology morphologic read, no integrated dx named; intended cardiac red herring. Conservative not to strip. |
| FEPI-TEMP-RS04 | E | minor | followup_outputs[6].output.alternatives (check_drug_interactions) | Lacosamide listed twice as an alternative (near-duplicate entries) | FIXED | Removed the redundant duplicate lacosamide line. |
| FEPI-TEMP-RS04 | B | minor | difficulty vs metadata.difficulty_description | difficulty = "diagnostic_puzzle" but difficulty_description reads "Straightforward … Minimal confounders" (confidence 0.88) | FLAGGED | Stale description; appended to case_body_concerns. (Drug-resistance IS genuine here — triple AED at therapeutic levels.) |
| FEPI-TEMP-S03 | B | minor | patient.social_history.occupation vs patient.history_present_illness | occupation = "insurance adjuster" but HPI calls him an "elementary school teacher" | FLAGGED | Patient-story contradiction; appended to case_body_concerns. Do not auto-rewrite. |
| FEPI-TEMP-S02 | D | info | followup_outputs[1].output.impression (analyze_brain_mri) | Detector flagged "DNET" naming | KEPT | Legitimate within-modality worded imaging differential ("DNET … ganglioglioma; tissue diagnosis recommended"). Not a leak (Kind-2). |
| FEPI-TEMP (S02,S03,RM03,M01-M03,RS,P,etc.) | B/E | minor | followup_outputs[*].output (order_specialized_test neuropsych) impression + findings[].abnormal | Dataset-wide neuropsych auto-flag artifact: low T-scores and above-average IQ/index scores are marked abnormal with an "(H)" suffix (e.g. FSIQ 114/121, VCI 122/126 flagged abnormal:"yes"; BVMT-R T-score 36 marked "(H)"). "(H)" reads as "High" but is used as a generic abnormal marker, and above-average intelligence is not a deficit. Inconsistent across cases (S04 FSIQ 114 = not abnormal; S02/S03 FSIQ 114/121 = abnormal). | FLAGGED | Pervasive cross-case generator artifact; S01 shows the correct style ("(L)" + material-specific read). Not fixed per-case to avoid intra-condition inconsistency; flagged for dataset maintainers. |
| FEPI-TEMP (all 14 non-mimic G40 cases) | C | minor | ground_truth.icd_code | All non-mimic cases use G40.219 (= localization-related symptomatic epilepsy, **intractable**, without status). Appropriate for the genuinely drug-resistant cases (P01-framing aside, RS04, RP cases), but questionable for newly diagnosed / AED-naive / well-controlled M and S cases that are NOT intractable (G40.209 would be the non-intractable code). | FLAGGED | Criteria pack writes G40.2x9 generically; dataset-wide coding-granularity convention. Changing ICD touches ground_truth semantics — clinician adjudication needed, not auto-fixed. |

## Tally

- Cases audited: 20 / 20 (every field of every case read).
- Findings: 0 blocker, 4 major (P01 occupation contradiction, P01 drug-resistance mislabel, RM01 laterality mismatch; counting the dataset-wide ICD-granularity item as major-adjacent it is recorded as minor), the remainder minor/nit/info.
  - By severity: blocker 0; major 3; minor 14; nit 3; info/KEPT 1.
- Fixed inline: 7 mechanical edits across 9 files —
  - M03: allergen mismatch corrected.
  - P02: 5× "seconds seconds" typo; broken CSF interpretation rewritten.
  - RM01: MRI impression hippocampal-volume numbers corrected to match structured data.
  - RP01: broken CSF interpretation placeholder corrected.
  - RP03: broken CSF interpretation placeholder corrected.
  - RS01: 4× "percentile percentile" typo; difficulty-mismatch flag appended.
  - RS04: duplicate lacosamide alternative removed; difficulty-mismatch flag appended.
  - S03: occupation-contradiction flag appended.
  - P01: occupation + drug-resistance flags appended.
  - RM01: laterality-mismatch flag appended.
- Flagged (not fixed): occupation contradictions (P01, S03), drug-resistance mislabel (P01), laterality mismatch (RM01), difficulty-label mismatches (RS01, RS02, RS04), unconfirmed-PE framing (RP02), pervasive neuropsych "(H)"/over-flagging artifact, dataset-wide G40.219-intractable coding convention, plus minor realism nits (P02 MRI teaching parenthetical, RS02 ECG differential-refutation wording).

## Top clinical-correctness flags for human adjudication

1. **FEPI-TEMP-P01 "drug-resistant" label** — the patient has never received an AED; calling the epilepsy drug-resistant and invoking Kwan 2010 is clinically unsupported as written. (Also: occupation field "graduate student" contradicts the HPI's "elementary school teacher".)
2. **FEPI-TEMP-RM01 laterality mismatch** — left-sided hemiparesis/facial droop with a left-hemisphere encephalomalacia (consistent on MRI + FDG-PET). The expected mapping is contralateral; either the deficit side or the lesion side needs reconciliation.
3. **Dataset-wide ICD coding** — G40.219 (intractable) is used for every non-mimic case including newly diagnosed, AED-naive, and well-controlled patients who are not intractable; consider G40.209 for the non-refractory M/S/RS-standard cases.
4. **Neuropsych abnormal-flagging artifact** — low T-scores and above-average IQ/index scores are both marked "abnormal (H)"; the convention is internally inconsistent across FEPI-TEMP cases and could mislead a model or reviewer (above-average IQ is not a deficit).
5. **Difficulty-label drift** — RS01 and RS04 are tagged `diagnostic_puzzle` but their metadata difficulty_descriptions still read "straightforward"; RS02 has a smaller moderate-vs-straightforward gap.

Self-verification: every fixed case re-validated — coherence stayed 0 and schema valid for all 9 edited files; answer-leakage re-run on the three CSF-edited files returned 0 candidates (no new leaks introduced). Only the 9 FEPI-TEMP files I edited changed; trailing newline (`}\n}\n`) and literal-unicode convention preserved. The S02 "DNET" detector hit is intentional Kind-2 within-modality naming and was left as-is.
