# NeuroBench v5 audit — BACT-MEN (Bacterial meningitis)

Scope: all 20 `BACT-MEN-*` cases. Every field of every case read against the BACT-MEN
criteria pack, the tool-report style guide, the parameter vocabulary, and the
`NeuroBenchCase` schema. CSF is the diagnostic/confirmatory test for this condition;
Gram-stain organism, culture, cell counts, antigen/PCR results were verified for
clinical coherence and KEPT (Kind-2 confirmatory results).

Mechanical validators (all 20 cases, before and after fixes): coherence = 0 issues,
schema = valid, answer-leakage detector = 0 candidates, tool-vocab = no BACT-MEN issues.

Naming note: in this condition the `R` prefix denotes v2 **real-case-seeded** cases
(metadata.generation_method = real_case_seed), not "reverse/mimic". The
non-bacterial mimics live under the M/S/**P** prefixes here (P02 TBM, P03 cryptococcal).

| case_id | dim | severity | region.field path | finding | action | detail |
|---|---|---|---|---|---|---|
| BACT-MEN-M01 | E | nit | followup_outputs[audiometry].* + impression | `"35 dB HL dB HL"` etc. duplicated unit suffix in values, quantitative_data, and impression recital | FIXED | Collapsed `dB HL dB HL`→`dB HL` (13 substrings) |
| BACT-MEN-M01 | B | major | followup_outputs[check_drug_interactions].warnings | Warns of "childhood penicillin rash" / "tolerates amoxicillin"; patient.allergies = "No known drug allergies" — fabricated allergy contradicting record | FLAGGED | Noted in metadata.case_body_concerns |
| BACT-MEN-M01 | B | minor | initial.csf vs followup[repeat_lp] | Repeat-LP "improved from" baselines (OP 32, WBC 380, protein 165, glucose 34) don't match initial values (31/392/153.2/30.7) | FLAGGED | Authoring artifact; not auto-edited |
| BACT-MEN-M01 | B | minor | initial.csf.glucose / labs.BMP.Glucose | CSF cites "serum glucose 142" but BMP glucose is 137; glucose_ratio 0.24 vs 30.7/142≈0.22 | FLAGGED | Within authoring tolerance; not edited |
| BACT-MEN-M01 | C/E | nit | followup_outputs[audiometry].test_type | `test_type: "baep"` but content is pure-tone audiometry (BAEP measures wave latencies) | FLAGGED | "audiometry" not in closed vocab; `baep` is the allowed container — not edited |
| BACT-MEN-M02 | E | nit | followup_outputs[audiometry].* | Duplicated `dB HL dB HL` / `% %` | FIXED | 5 substrings collapsed |
| BACT-MEN-M02 | B | major | followup_outputs[check_drug_interactions].contraindications | "Documented penicillin allergy (childhood rash)"; patient.allergies = "Contrast dye" only — fabricated allergy | FLAGGED | Noted in metadata.case_body_concerns |
| BACT-MEN-M02 | B | minor | initial.csf vs followup[repeat_lp]; csf serum glucose 188 vs BMP 194 | Repeat-LP baselines mismatch; paired serum glucose differs from BMP | FLAGGED | Not auto-edited |
| BACT-MEN-M02 | C/E | nit | followup_outputs[audiometry].test_type | `baep` mislabel (audiometry content) | FLAGGED | Systematic; not edited |
| BACT-MEN-M03 | E | nit | followup_outputs[audiometry].* | Duplicated `dB HL dB HL` / `88% %` | FIXED | 15 substrings collapsed |
| BACT-MEN-M03 | B | major | followup_outputs[ceftriaxone interactions].warnings | "Patient reports penicillin allergy (childhood rash)"; patient.allergies = "Tetracycline" only — fabricated allergy | FLAGGED | Appended to metadata.case_body_concerns |
| BACT-MEN-M03 | B | minor | initial.csf vs followup[repeat_lp] | Repeat-LP "from" baselines don't match initial values | FLAGGED | Not auto-edited |
| BACT-MEN-M03 | C/E | nit | followup_outputs[audiometry].test_type | `baep` mislabel | FLAGGED | Not edited |
| BACT-MEN-P01 | B | major | patient.history_present_illness vs social_history.occupation | HPI: "high school mathematics teacher"; social_history.occupation = "paralegal", education = "Bachelor's in education" — occupation contradiction | FLAGGED | Appended to metadata.case_body_concerns |
| BACT-MEN-P01 | E | nit | followup_outputs[audiometry].* | Duplicated `dB HL dB HL` / `% %` | FIXED | 13 substrings collapsed |
| BACT-MEN-P01 | B | minor | ground_truth.red_herrings[sinus].field_path | Red-herring cites mri.additional_observations; sinus thickening actually lives in mri.findings (a "Mucosal thickening" finding) | FLAGGED | Path imprecision; data present; not edited |
| BACT-MEN-P01 | C/E | nit | followup_outputs[audiometry].test_type | `baep` mislabel | FLAGGED | Not edited |
| BACT-MEN-P02 | B | major | case_id prefix / condition enum vs ground_truth.primary_diagnosis | P-prefix + condition `bacterial_meningitis` but gold dx = Tuberculous meningitis (A17.0); per pack §6 TBM is a mimic subtype | FLAGGED | Noted; intentional mimic, prefix/enum convention needs human adjudication |
| BACT-MEN-P02 | B | major | ground_truth.harmful_tools[analyze_csf] vs initial.csf | LP flagged harmful (ICP/hydrocephalus) yet initial CSF is the populated, confirmatory test (AFB+, GeneXpert+) | FLAGGED | Internal tension; not auto-edited |
| BACT-MEN-P02 | C | minor | ground_truth.contraindicated_actions | Retains pyogenic-meningitis dexamethasone boilerplate that doesn't fit a TBM case (template bleed) | FLAGGED | Not edited |
| BACT-MEN-P02 | B | minor | followup_outputs[request_chest_ct].tool_name | Chest-CT findings returned under tool_name `analyze_brain_mri` (tool/content mismatch) | FLAGGED | Not edited |
| BACT-MEN-P02 | D | minor | followup_outputs[ophtho].abnormal_values_summary | "Bilateral choroidal tubercles — pathognomonic for disseminated tuberculosis" — borderline disease-naming verdict in a labs panel | FLAGGED | Choroidal tubercles are a legitimate ophthalmologic finding; left as-is |
| BACT-MEN-P03 | B | major | case_id prefix / condition enum vs ground_truth.primary_diagnosis | P-prefix + condition `bacterial_meningitis` but gold dx = Cryptococcal meningoencephalitis (B45.1); pack §6 mimic subtype | FLAGGED | Noted; intentional mimic, needs human adjudication |
| BACT-MEN-P03 | B | major | ground_truth.harmful_tools[analyze_csf] vs critical_actions | LP flagged harmful, yet critical_actions mandates serial therapeutic LPs and a therapeutic-LP followup exists; direct contradiction | FLAGGED | Noted in metadata.case_body_concerns |
| BACT-MEN-P03 | C | minor | ground_truth.contraindicated_actions | Pyogenic/dexamethasone boilerplate contradicts cryptococcal case (steroids noted harmful) | FLAGGED | Template bleed; not edited |
| BACT-MEN-P03 | B | minor | followup_outputs[request_chest_ct].tool_name | Chest-CT under `analyze_brain_mri` | FLAGGED | Not edited |
| BACT-MEN-P03 | B | minor | chief_complaint vs history_present_illness | "over 3 weeks" vs "4-week history" headache duration | FLAGGED | Not edited |
| BACT-MEN-RM01 | E | nit | followup_outputs[audiometry].* | Duplicated `dB HL dB HL` | FIXED | 10 substrings collapsed |
| BACT-MEN-RM01 | C | minor | ground_truth.critical/contraindicated_actions | Dexamethasone boilerplate says "in confirmed pneumococcal meningitis"; organism is Hib (G00.0) | FLAGGED | Action still appropriate; not edited |
| BACT-MEN-RM01 | C/E | nit | followup_outputs[audiometry].test_type | `baep` mislabel | FLAGGED | Not edited |
| BACT-MEN-RM02 | E | nit | followup_outputs[audiometry].* | Duplicated `dB HL dB HL` / `% %` | FIXED | 18 substrings collapsed |
| BACT-MEN-RM02 | C/E | nit | followup_outputs[audiometry].test_type | `baep` mislabel | FLAGGED | Not edited |
| BACT-MEN-RM03 | E | nit | followup_outputs[audiometry].* | Duplicated `dB HL dB HL` | FIXED | 12 substrings collapsed |
| BACT-MEN-RM03 | C/E | nit | followup_outputs[audiometry].test_type | `baep` mislabel | FLAGGED | Not edited |
| BACT-MEN-RP01 | E | nit | followup_outputs[audiometry].* | Duplicated `dB HL dB HL` / `% %` | FIXED | 10 substrings collapsed |
| BACT-MEN-RP01 | C/E | nit | followup_outputs[audiometry].test_type | `baep` mislabel | FLAGGED | Not edited |
| BACT-MEN-RP02 | C | nit | patient.allergies = Ceftriaxone | Verified deliberate, clinically load-bearing allergy (forces meropenem/vancomycin); not a fabrication | OK | No action |
| BACT-MEN-RP03 | C | major | initial.csf vs ground_truth.primary_diagnosis | Gold dx = pneumococcal meningitis, but initial CSF is pauci-cellular (WBC 3), glucose ratio 0.55 (above the <0.4 bacterial threshold the case itself cites), Gram/culture negative; diagnosis rests entirely on follow-up PCR/blood culture. CD4 359 is not AIDS-range yet "advanced HIV" is invoked | FLAGGED | Confirmed coherent by design (followup confirms S. pneumoniae); CD4/wording + bland initial CSF noted in metadata.case_body_concerns |
| BACT-MEN-RS01 | C | — | initial.csf | Florid GBS meningitis (WBC 1310, 94% PMN, ratio 0.10, protein 248); G00.2 correct | OK | Coherent; KEPT |
| BACT-MEN-RS02 | E | nit | followup_outputs[shunt tap].interpretation | `"8 cells/uL cells/uL"`, `"52 mg/dL mg/dL"` duplicated units in interpretation recital | FIXED | 2 substrings collapsed |
| BACT-MEN-RS03 | E | nit | initial.csf.protein | Protein given dual-unit `"3120 mg/L (312 mg/dL)"` (conversion correct) vs dataset mg/dL convention | FLAGGED | Conversion correct; not edited |
| BACT-MEN-RS04 | B | minor | initial.csf.cell_count key + interpretation | cell_count key is `total_WBC` (2,840) not `WBC`; auto-generated interpretation renders "WBC: N/A" and omits the count | FLAGGED | Cosmetic render artifact, data intact; noted in metadata.case_body_concerns |
| BACT-MEN-RS04 | C | — | ground_truth | Healthcare-associated Proteus mirabilis meningitis (gram-neg rods), G00.8 appropriate | OK | Coherent; KEPT |
| BACT-MEN-S01 | C/E | — | full case | Otogenic/sinugenic pneumococcal meningitis; florid CSF (WBC 3414, ratio 0.06); Cephalosporins allergy load-bearing | OK | Coherent; KEPT |
| BACT-MEN-S02 | C | — | full case | Pneumococcal meningitis, female + wife, pronouns consistent; florid CSF | OK | Coherent; KEPT |
| BACT-MEN-S03 | C | — | full case | Pneumococcal meningitis; florid CSF (ratio 0.07) | OK | Coherent; KEPT |
| BACT-MEN-S04 | C | — | full case | Pneumococcal meningitis with ventriculitis; grossly purulent CSF, lancet diplococci, ratio 0.07 | OK | Coherent; KEPT |

## Cross-cutting observations

- **Systematic `baep` mislabel (18/20 cases):** every post-meningitis hearing-screen
  followup uses `order_specialized_test` with `test_type: "baep"` while the body is
  pure-tone audiometry / speech discrimination / tympanometry. "audiometry" is not in
  the closed `test_type` vocabulary; `baep` is the nearest allowed container and the
  vocab validator passes. Not auto-edited (changing it would break vocab validation).
  Recommend the dataset team add an `audiometry` test_type to the vocabulary.
- **Fabricated penicillin allergy in M01/M02/M03 drug-interaction reports:** all three
  reference a "childhood penicillin rash"/"tolerates amoxicillin" that contradicts each
  patient's actual allergy field. Likely a shared boilerplate snippet. FLAGGED, not
  rewritten (clinical-reasoning text).
- **Repeat-LP "improved from X" baselines (M01/M02/M03):** the followup LP narratives
  cite prior values that differ slightly from the initial CSF. Authoring artifact; the
  trend direction is correct. FLAGGED, not edited.
- **P02/P03 mimic design:** both are non-bacterial mimics (TBM, cryptococcal) under a
  P (progressive bacterial) prefix with `condition: bacterial_meningitis`. The
  harmful_tools `analyze_csf` flag coexists with populated/confirmatory CSF and, in
  P03, with a required therapeutic-LP critical action — an internal contradiction that
  needs human adjudication.

## Tally

- **Cases audited:** 20 (all `BACT-MEN-*`), every field read.
- **Findings by severity:** major 8 (M01 allergy, M02 allergy, M03 allergy, P01
  occupation, P02 prefix/enum, P02 harmful-CSF, P03 harmful-CSF-vs-critical-action,
  P03 prefix/enum) — note RP03 logged as 1 major clinical flag; minor ~11; nit ~13.
- **Fixed (inline, mechanical):** 9 cases edited for duplicated-unit collapse
  (`dB HL dB HL`→`dB HL`, `% %`→`%`, `cells/uL cells/uL`→`cells/uL`,
  `mg/dL mg/dL`→`mg/dL`): M01, M02, M03, P01, RM01, RM02, RM03, RP01, RS02.
- **Flagged (not fixed):** all judgment/clinical items above; case-body contradictions
  also appended to each case's `metadata.case_body_concerns` (M01, M02, M03, P01, P02,
  P03, RP03, RS04).
- **Never changed:** no diagnosis, no patient story, no ground_truth meaning, no Kind-2
  within-modality / confirmatory CSF results stripped.
- **Self-verify:** coherence = 0 and schema valid on every edited file; leakage detector
  = 0 candidates; vocab clean; unicode (literal) and trailing newline preserved; only
  `BACT-MEN-*` files touched (13 modified).

## Top clinical flags for human adjudication

1. **RP03** — initial CSF (WBC 3, glucose ratio 0.55, neg Gram/culture) is too bland to
   support "pneumococcal meningitis" on its own; diagnosis depends entirely on follow-up
   PCR/blood culture, and CD4 359 contradicts the "advanced HIV" rationale. Confirm the
   case is acceptable as a puzzle or revise the initial CSF / CD4.
2. **P02 & P03** — `analyze_csf` in `harmful_tools` conflicts with the populated
   confirmatory CSF and (P03) the required serial therapeutic LPs. Decide whether LP is
   harmful-then-cleared or simply required, and reconcile.
3. **P02 & P03 prefix/enum** — non-bacterial mimics (TBM, cryptococcal) carrying a
   bacterial P-prefix and `condition: bacterial_meningitis`. Confirm this is intended.
4. **M01/M02/M03 fabricated penicillin allergy** in drug-interaction reports — rewrite to
   match each patient's actual allergy field.
5. **P01 occupation contradiction** (teacher vs paralegal) — pick the intended occupation.
