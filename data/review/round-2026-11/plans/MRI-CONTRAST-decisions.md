# Class MRI-CONTRAST (November 2026 round): decisions

## The defect
The review app shows `MRIReport.contrast_used` as "contrast used: none" when the field is null.
Reviewers (R1 in MS-RR and FEPI-TEMP, R2 in NMDAR-ENC and GLIO-HG) found that header above
reports describing post-gadolinium series and enhancement. Measured on the base (06b74446):
214 stored brain-MRI reports in 213 cases of 15 conditions carry gadolinium content (enhancement,
positive or negative, a post-contrast sequence, "T1 post", "following gadolinium") and do not
state `contrast_used: true`: 142 initial outputs, 50 follow-ups, 22 case fallbacks. Three
body-imaging MRIs (MG 1, SAH 2) describe enhancement with `contrast: false`.

## How the MockServer routes contrast (why setting the flag alone is wrong)
`analyze_brain_mri.contrast` defaults to false. A stored report that states `contrast_used`
answers only an order with that value; null answers any order
(`MockServer._FLAG_DISCRIMINATOR`, docs/benchmark/tool-contract.md). If a case's only MRI is set
to `true`, every plain order (the default) misses it and falls to the case fallback or the
library's normal MRI: a glioma or MS patient would get "Normal MRI of the brain". Probe on
ALZ-EARLY-RS06 (the October precedent, a plain initial and a contrast follow-up): a plain order
gets the plain study and a contrast order the contrast study, in any order of calls.

## Decision
1. Every stored brain MRI with gadolinium content becomes a pair:
   - the gadolinium study, text unchanged except for internal contradictions, with
     `contrast_used: true`, stored as an `analyze_brain_mri` follow-up with trigger
     `request_contrast_mri` (or a trigger naming the study when the case already has several);
   - a non-contrast study of the same examination, `contrast_used: false`: the same pre-contrast
     sequences and measurements, every post-contrast finding, signal key (`T1_post_contrast`,
     ...), observation and impression clause removed, nothing hinting that enhancement was
     assessed. It takes the original slot (initial output, or the follow-up position for a
     follow-up study).
2. The MRI criterion names the contrast it needs: `contrast: true` where gadolinium is required by
   the governing guideline for the question the criterion answers (MS: MAGNIMS-CMSC-NAIMS 2021
   and McDonald 2024 for dissemination in time; glioma: EANO 2021 / RANO; encephalitis and
   meningitis complications; abscess; a tumour mimic), with the plain study as a second
   alternative only where the plain study alone answers the clinical question. Where
   gadolinium is not indicated (stroke, syncope, NPH, dementia, typical epilepsy protocol) the
   criterion stays plain. `expected_evidence` must be text of the report that the criterion's
   own first alternative receives.
3. A case fallback MRI cannot be split (one slot): its gadolinium sentences are removed and
   `contrast_used` stays null, so it stays true for any order.
4. A stored MRI with no gadolinium content stays null (answers both orders, says nothing about
   enhancement). Setting it to false would send a contrast order to the library normal.
5. Body-imaging MRIs that describe enhancement get `contrast: true` (no routing flag there).
6. Every split is checked with a probe: plain order, contrast order, both orders in either
   sequence; and with perfect_agent.py -v.

## CENTRAL
- `fallback_library.yaml` is consistent (library MRI reports set the flag from the order).
- Consider a guard: a stored brain MRI with gadolinium content states `contrast_used: true`.

## Outcome (16 Nov 2026)
- 216 cases processed by 28 Opus workers, each chunk re-checked by an independent Opus verifier
  (56 agents in two runs); 208 case files changed. Log lines `- MRI-CONTRAST:` and
  `- MRI-CONTRAST verified:` in every case log.
- After: 0 stored gadolinium studies with a null flag. The 10 reports the regex still matches are
  false positives: TOF MRA "flow-related enhancement" (ISCH-STR, 9) and plain epilepsy protocols
  whose technique line says "no gadolinium" (FEPI-TEMP; these stay null, decision 4, so a contrast
  order still gets the patient's own study).
- Probe over all 600 cases: no MRI order in a case that stores an MRI is answered by the library.
  HEP-ENC-S08 and S10 stored a fallback with `contrast_used: false` (no gadolinium content), so a
  contrast order got the library normal: set to null (decision 3).
- Perfect agent 600/600 (16 warnings, as at base); test_case_guards, panel contract, guidance
  claims, MockServer tests pass; synonyms --check 0.
- 40 approved cases changed (MRI pair or fallback only): GBS-RS18, HEP-ENC-P09, HEP-ENC-S10,
  ISCH-STR-RS05, NMDAR-ENC P03 P07 P08 RM02 S01 S02 S03 S04 S06 S09 S10, SAH-M05 RP11 S07,
  SE M01 M02 M04 M05 M06 M08 P01 P06 S01 S02 S05 S06 S07, SYNC-CARD P02 RM04 RS03 RS06 S01 S02
  S04 S05 S06.
