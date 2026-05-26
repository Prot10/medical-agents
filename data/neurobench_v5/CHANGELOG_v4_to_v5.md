# NeuroBench v4 → v5 changelog

**Cases in both versions:** 200
**Cases new in v5:** 316
**Cases removed in v5:** 0

## Aggregate changes (v4 → v5)

- primary_diagnosis changed: 140
- icd_code changed: 89
- difficulty changed: 45

### Difficulty transitions
- diagnostic_puzzle → diagnostic_puzzle: 58
- straightforward → straightforward: 49
- moderate → moderate: 48
- straightforward → moderate: 24
- moderate → diagnostic_puzzle: 10
- straightforward → diagnostic_puzzle: 7
- moderate → straightforward: 2
- diagnostic_puzzle → moderate: 2

### Per-case tool workup
- avg required tools v4: 3.82
- avg required tools v5: 5.16
- avg recommended tools v5: 1.39
- avg optional tools v5: 0.61
- avg useless_tools v5: 3.75
- avg harmful_tools v5: 0.12
- avg sequence_constraints v5: 1.53
- avg cited actions v5: 8.57 / 8.78

### Tool additions / removals (top 15 each)

**Most-added tools (in v5 but not in v4 for the matching case):**
- search_medical_literature: 137 cases
- check_drug_interactions: 91 cases
- order_advanced_imaging: 66 cases
- consult_medical_specialist: 60 cases
- order_ct_scan: 44 cases
- order_specialized_test: 29 cases
- order_cardiac_monitoring: 27 cases
- analyze_csf: 20 cases
- analyze_eeg: 10 cases
- analyze_brain_mri: 5 cases
- order_echocardiogram: 5 cases
- interpret_labs: 1 cases
- analyze_ecg: 1 cases

**Most-removed tools (in v4 but not in v5 for the matching case):**
- analyze_eeg: 43 cases
- analyze_ecg: 11 cases
- order_specialized_test: 10 cases
- interpret_eeg: 10 cases
- search_medical_literature: 7 cases
- order_advanced_imaging: 7 cases
- order_echocardiogram: 5 cases
- analyze_csf: 5 cases
- check_drug_interactions: 2 cases
- read_eeg: 1 cases
- analyze_brain_mri: 1 cases

### Authoring flags (v5)
- cases with case_body_concerns: 45
- total case_body_concerns entries: 71
- cases with citation_gap: 4
- cases with vocab_gap: 0

## Per-case detail

| case_id | dx changed | difficulty | required v4→v5 | useless | harmful | seq | cited |
|---|---|---|---|---|---|---|---|
| ALZ-EARLY-M01 | ✓ | moderate | 4 → 5 | 4 | 0 | 1 | 10/10 |
| ALZ-EARLY-M02 | ✓ | moderate | 5 → 5 | 4 | 0 | 1 | 10/10 |
| ALZ-EARLY-M03 | ✓ | moderate | 4 → 5 | 4 | 0 | 1 | 10/10 |
| ALZ-EARLY-P01 | ✓ | diagnostic_puzzle | 4 → 5 | 4 | 0 | 1 | 10/10 |
| ALZ-EARLY-P02 | ✓ | diagnostic_puzzle | 3 → 5 | 5 | 0 | 0 | 11/11 |
| ALZ-EARLY-P03 | ✓ | diagnostic_puzzle | 4 → 5 | 4 | 0 | 0 | 11/11 |
| ALZ-EARLY-RM01 | ✓ | moderate | 4 → 5 | 4 | 0 | 1 | 11/11 |
| ALZ-EARLY-RM02 | ✓ | moderate | 4 → 5 | 3 | 0 | 1 | 10/10 |
| ALZ-EARLY-RM03 | ✓ | moderate | 4 → 5 | 3 | 0 | 1 | 11/11 |
| ALZ-EARLY-RP01 | ✓ | diagnostic_puzzle | 4 → 5 | 4 | 0 | 1 | 11/11 |
| ALZ-EARLY-RP02 | ✓ | diagnostic_puzzle | 4 → 5 | 3 | 0 | 1 | 11/11 |
| ALZ-EARLY-RP03 | ✓ | diagnostic_puzzle | 4 → 5 | 3 | 0 | 1 | 10/10 |
| ALZ-EARLY-RS01 | ✓ | straightforward | 3 → 3 | 3 | 0 | 1 | 10/10 |
| ALZ-EARLY-RS02 | ✓ | straightforward | 4 → 3 | 4 | 0 | 1 | 10/10 |
| ALZ-EARLY-RS03 | ✓ | straightforward | 4 → 3 | 4 | 0 | 1 | 10/10 |
| ALZ-EARLY-RS04 | ✓ | straightforward | 4 → 3 | 4 | 0 | 1 | 10/10 |
| ALZ-EARLY-S01 | ✓ | straightforward | 4 → 3 | 4 | 0 | 1 | 10/10 |
| ALZ-EARLY-S02 | ✓ | straightforward | 4 → 3 | 4 | 0 | 1 | 10/10 |
| ALZ-EARLY-S03 | ✓ | straightforward | 4 → 3 | 4 | 0 | 1 | 10/10 |
| ALZ-EARLY-S04 | ✓ | straightforward | 4 → 3 | 4 | 0 | 1 | 10/10 |
| BACT-MEN-M01 |  | moderate → diagnostic_puzzle | 4 → 5 | 5 | 0 | 2 | 6/6 |
| BACT-MEN-M02 | ✓ | moderate → diagnostic_puzzle | 4 → 5 | 5 | 0 | 2 | 6/6 |
| BACT-MEN-M03 | ✓ | moderate → diagnostic_puzzle | 4 → 5 | 5 | 0 | 2 | 6/6 |
| BACT-MEN-P01 |  | diagnostic_puzzle | 3 → 5 | 5 | 0 | 2 | 6/6 |
| BACT-MEN-P02 | ✓ | diagnostic_puzzle | 3 → 4 | 4 | 1 | 2 | 5/5 |
| BACT-MEN-P03 | ✓ | diagnostic_puzzle | 2 → 4 | 4 | 1 | 2 | 5/5 |
| BACT-MEN-RM01 | ✓ | moderate | 3 → 5 | 4 | 0 | 2 | 6/6 |
| BACT-MEN-RM02 | ✓ | moderate → diagnostic_puzzle | 5 → 5 | 4 | 0 | 2 | 6/6 |
| BACT-MEN-RM03 | ✓ | moderate | 4 → 5 | 5 | 0 | 2 | 6/6 |
| BACT-MEN-RP01 | ✓ | diagnostic_puzzle | 3 → 5 | 4 | 0 | 2 | 6/6 |
| BACT-MEN-RP02 | ✓ | diagnostic_puzzle | 4 → 5 | 4 | 0 | 2 | 6/6 |
| BACT-MEN-RP03 | ✓ | diagnostic_puzzle | 3 → 5 | 4 | 0 | 2 | 6/6 |
| BACT-MEN-RS01 |  | straightforward → diagnostic_puzzle | 4 → 5 | 4 | 0 | 2 | 6/6 |
| BACT-MEN-RS02 | ✓ | straightforward → moderate | 4 → 5 | 5 | 0 | 2 | 6/6 |
| BACT-MEN-RS03 |  | straightforward → moderate | 3 → 5 | 4 | 0 | 2 | 6/6 |
| BACT-MEN-RS04 | ✓ | straightforward → moderate | 3 → 5 | 4 | 0 | 2 | 6/6 |
| BACT-MEN-S01 | ✓ | straightforward → moderate | 4 → 5 | 5 | 0 | 2 | 6/6 |
| BACT-MEN-S02 | ✓ | straightforward → moderate | 4 → 5 | 4 | 0 | 2 | 6/6 |
| BACT-MEN-S03 | ✓ | straightforward → moderate | 4 → 5 | 5 | 0 | 2 | 6/6 |
| BACT-MEN-S04 | ✓ | straightforward → moderate | 4 → 5 | 5 | 0 | 2 | 6/6 |
| FEPI-TEMP-M01 | ✓ | moderate | 4 → 5 | 4 | 0 | 1 | 8/9 |
| FEPI-TEMP-M02 | ✓ | moderate | 4 → 5 | 5 | 0 | 1 | 7/8 |
| FEPI-TEMP-M03 | ✓ | moderate | 4 → 5 | 4 | 0 | 1 | 8/9 |
| FEPI-TEMP-P01 | ✓ | diagnostic_puzzle | 4 → 5 | 4 | 0 | 1 | 8/9 |
| FEPI-TEMP-P02 | ✓ | diagnostic_puzzle | 3 → 4 | 2 | 0 | 2 | 8/9 |
| FEPI-TEMP-P03 | ✓ | diagnostic_puzzle | 3 → 3 | 5 | 0 | 1 | 6/7 |
| FEPI-TEMP-RM01 | ✓ | moderate | 3 → 5 | 4 | 0 | 1 | 7/8 |
| FEPI-TEMP-RM02 | ✓ | moderate | 3 → 5 | 3 | 0 | 1 | 8/9 |
| FEPI-TEMP-RM03 | ✓ | moderate | 3 → 5 | 4 | 0 | 1 | 7/8 |
| FEPI-TEMP-RP01 | ✓ | diagnostic_puzzle | 4 → 6 | 3 | 0 | 1 | 7/8 |
| FEPI-TEMP-RP02 | ✓ | diagnostic_puzzle | 4 → 6 | 2 | 0 | 1 | 11/12 |
| FEPI-TEMP-RP03 | ✓ | diagnostic_puzzle | 3 → 6 | 3 | 0 | 2 | 9/10 |
| FEPI-TEMP-RS01 | ✓ | straightforward → diagnostic_puzzle | 3 → 5 | 4 | 0 | 1 | 8/9 |
| FEPI-TEMP-RS02 | ✓ | straightforward → moderate | 4 → 5 | 4 | 0 | 1 | 6/7 |
| FEPI-TEMP-RS03 | ✓ | straightforward | 4 → 5 | 4 | 0 | 1 | 6/7 |
| FEPI-TEMP-RS04 | ✓ | straightforward → diagnostic_puzzle | 4 → 5 | 4 | 0 | 1 | 8/9 |
| FEPI-TEMP-S01 | ✓ | straightforward | 4 → 5 | 4 | 0 | 1 | 6/7 |
| FEPI-TEMP-S02 | ✓ | straightforward | 4 → 5 | 4 | 0 | 1 | 6/7 |
| FEPI-TEMP-S03 | ✓ | straightforward | 4 → 5 | 4 | 0 | 1 | 6/7 |
| FEPI-TEMP-S04 | ✓ | straightforward | 4 → 5 | 4 | 0 | 1 | 6/7 |
| FND-M01 |  | moderate | 4 → 3 | 6 | 0 | 0 | 7/8 |
| FND-M02 |  | moderate | 3 → 3 | 6 | 0 | 0 | 7/8 |
| FND-M03 |  | moderate | 3 → 3 | 5 | 0 | 0 | 7/8 |
| FND-P01 |  | diagnostic_puzzle | 4 → 3 | 5 | 0 | 0 | 7/8 |
| FND-P02 |  | diagnostic_puzzle | 3 → 2 | 5 | 0 | 0 | 7/8 |
| FND-P03 |  | diagnostic_puzzle | 2 → 2 | 6 | 0 | 0 | 6/7 |
| FND-RM01 |  | moderate | 3 → 3 | 6 | 0 | 0 | 7/8 |
| FND-RM02 |  | moderate | 3 → 3 | 5 | 0 | 0 | 6/7 |
| FND-RM03 |  | moderate | 3 → 3 | 5 | 0 | 0 | 7/8 |
| FND-RP01 |  | diagnostic_puzzle | 4 → 3 | 5 | 0 | 0 | 7/8 |
| FND-RP02 |  | diagnostic_puzzle | 5 → 3 | 4 | 0 | 0 | 6/7 |
| FND-RP03 |  | diagnostic_puzzle | 3 → 3 | 4 | 0 | 0 | 7/8 |
| FND-RS01 |  | straightforward | 3 → 3 | 5 | 0 | 0 | 7/8 |
| FND-RS02 |  | straightforward | 4 → 3 | 4 | 0 | 0 | 7/8 |
| FND-RS03 |  | straightforward | 3 → 3 | 3 | 0 | 0 | 7/8 |
| FND-RS04 |  | straightforward | 3 → 3 | 5 | 0 | 0 | 7/8 |
| FND-S01 |  | straightforward | 3 → 3 | 6 | 0 | 0 | 7/8 |
| FND-S02 |  | straightforward | 3 → 3 | 6 | 0 | 0 | 7/8 |
| FND-S03 |  | straightforward | 3 → 3 | 6 | 0 | 0 | 7/8 |
| FND-S04 |  | straightforward | 3 → 3 | 6 | 0 | 0 | 7/8 |
| GLIO-HG-M01 | ✓ | moderate | 4 → 4 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-M02 |  | moderate | 4 → 4 | 2 | 1 | 2 | 8/8 |
| GLIO-HG-M03 | ✓ | moderate | 5 → 4 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-P01 |  | diagnostic_puzzle | 4 → 3 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-P02 | ✓ | diagnostic_puzzle | 4 → 3 | 2 | 1 | 2 | 8/8 |
| GLIO-HG-P03 |  | diagnostic_puzzle | 2 → 3 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-RM01 | ✓ | moderate → straightforward | 4 → 4 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-RM02 | ✓ | moderate → diagnostic_puzzle | 5 → 4 | 2 | 1 | 2 | 8/8 |
| GLIO-HG-RM03 | ✓ | moderate → straightforward | 3 → 4 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-RP01 |  | diagnostic_puzzle → moderate | 4 → 4 | 2 | 1 | 2 | 8/8 |
| GLIO-HG-RP02 | ✓ | diagnostic_puzzle → moderate | 4 → 4 | 2 | 1 | 2 | 8/8 |
| GLIO-HG-RP03 | ✓ | diagnostic_puzzle | 4 → 4 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-RS01 | ✓ | straightforward → diagnostic_puzzle | 3 → 4 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-RS02 | ✓ | straightforward | 3 → 4 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-RS03 | ✓ | straightforward | 3 → 4 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-RS04 | ✓ | straightforward → moderate | 4 → 4 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-S01 | ✓ | straightforward | 3 → 4 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-S02 | ✓ | straightforward | 3 → 4 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-S03 | ✓ | straightforward | 4 → 4 | 2 | 1 | 2 | 9/9 |
| GLIO-HG-S04 | ✓ | straightforward | 4 → 3 | 2 | 1 | 2 | 9/9 |
| ISCH-STR-M01 | ✓ | moderate → diagnostic_puzzle | 6 → 9 | 3 | 0 | 3 | 13/13 |
| ISCH-STR-M02 | ✓ | moderate | 6 → 9 | 3 | 0 | 2 | 12/12 |
| ISCH-STR-M03 | ✓ | moderate | 6 → 9 | 3 | 0 | 2 | 12/12 |
| ISCH-STR-P01 | ✓ | diagnostic_puzzle | 5 → 9 | 3 | 0 | 2 | 14/14 |
| ISCH-STR-P02 |  | diagnostic_puzzle | 4 → 9 | 3 | 0 | 2 | 14/14 |
| ISCH-STR-P03 | ✓ | diagnostic_puzzle | 5 → 9 | 2 | 1 | 3 | 13/13 |
| ISCH-STR-RM01 | ✓ | moderate | 6 → 9 | 2 | 0 | 2 | 14/14 |
| ISCH-STR-RM02 | ✓ | moderate → diagnostic_puzzle | 4 → 9 | 3 | 0 | 2 | 13/13 |
| ISCH-STR-RM03 | ✓ | moderate | 5 → 9 | 3 | 0 | 2 | 13/13 |
| ISCH-STR-RP01 | ✓ | diagnostic_puzzle | 5 → 8 | 3 | 0 | 3 | 13/13 |
| ISCH-STR-RP02 | ✓ | diagnostic_puzzle | 4 → 9 | 3 | 0 | 2 | 14/14 |
| ISCH-STR-RP03 | ✓ | diagnostic_puzzle | 5 → 9 | 3 | 0 | 2 | 13/13 |
| ISCH-STR-RS01 | ✓ | straightforward → moderate | 4 → 9 | 3 | 0 | 2 | 12/12 |
| ISCH-STR-RS02 | ✓ | straightforward → diagnostic_puzzle | 4 → 9 | 3 | 0 | 2 | 13/13 |
| ISCH-STR-RS03 | ✓ | straightforward → diagnostic_puzzle | 5 → 9 | 3 | 0 | 2 | 12/12 |
| ISCH-STR-RS04 |  | straightforward → diagnostic_puzzle | 4 → 9 | 3 | 0 | 2 | 14/14 |
| ISCH-STR-S01 | ✓ | straightforward | 4 → 9 | 3 | 0 | 2 | 12/12 |
| ISCH-STR-S02 | ✓ | straightforward → moderate | 4 → 9 | 3 | 0 | 2 | 12/12 |
| ISCH-STR-S03 | ✓ | straightforward → moderate | 4 → 9 | 3 | 0 | 2 | 12/12 |
| ISCH-STR-S04 | ✓ | straightforward → moderate | 4 → 9 | 3 | 0 | 2 | 12/12 |
| MS-RR-M01 | ✓ | moderate | 3 → 5 | 5 | 0 | 1 | 8/8 |
| MS-RR-M02 | ✓ | moderate | 3 → 5 | 5 | 0 | 1 | 8/8 |
| MS-RR-M03 | ✓ | moderate | 2 → 5 | 5 | 0 | 1 | 8/8 |
| MS-RR-P01 | ✓ | diagnostic_puzzle | 4 → 5 | 5 | 0 | 1 | 8/8 |
| MS-RR-P02 | ✓ | diagnostic_puzzle | 3 → 4 | 5 | 0 | 1 | 8/8 |
| MS-RR-P03 | ✓ | diagnostic_puzzle | 2 → 4 | 5 | 0 | 1 | 8/8 |
| MS-RR-RM01 | ✓ | moderate → diagnostic_puzzle | 5 → 5 | 3 | 0 | 1 | 8/8 |
| MS-RR-RM02 | ✓ | moderate → diagnostic_puzzle | 3 → 5 | 5 | 0 | 1 | 8/8 |
| MS-RR-RM03 | ✓ | moderate | 3 → 5 | 5 | 0 | 1 | 8/8 |
| MS-RR-RP01 | ✓ | diagnostic_puzzle | 4 → 5 | 4 | 0 | 1 | 8/8 |
| MS-RR-RP02 | ✓ | diagnostic_puzzle | 5 → 4 | 5 | 0 | 1 | 8/8 |
| MS-RR-RP03 | ✓ | diagnostic_puzzle | 5 → 5 | 4 | 0 | 1 | 8/8 |
| MS-RR-RS01 | ✓ | straightforward | 4 → 5 | 5 | 0 | 1 | 8/8 |
| MS-RR-RS02 | ✓ | straightforward | 4 → 5 | 5 | 0 | 1 | 8/8 |
| MS-RR-RS03 | ✓ | straightforward | 4 → 5 | 5 | 0 | 1 | 8/8 |
| MS-RR-RS04 | ✓ | straightforward | 4 → 5 | 5 | 0 | 1 | 8/8 |
| MS-RR-S01 | ✓ | straightforward | 3 → 5 | 5 | 0 | 1 | 8/8 |
| MS-RR-S02 | ✓ | straightforward | 3 → 5 | 5 | 0 | 1 | 8/8 |
| MS-RR-S03 | ✓ | straightforward | 3 → 4 | 5 | 0 | 1 | 8/8 |
| MS-RR-S04 | ✓ | straightforward | 2 → 5 | 5 | 0 | 1 | 8/8 |
| NMDAR-ENC-M01 |  | moderate | 4 → 5 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-M02 |  | moderate | 4 → 7 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-M03 |  | moderate | 4 → 5 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-P01 |  | diagnostic_puzzle | 4 → 5 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-P02 |  | diagnostic_puzzle | 4 → 5 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-P03 |  | diagnostic_puzzle | 3 → 5 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-RM01 |  | moderate | 5 → 7 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-RM02 |  | moderate | 5 → 7 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-RM03 |  | moderate | 4 → 7 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-RP01 |  | diagnostic_puzzle | 5 → 7 | 2 | 0 | 2 | 9/9 |
| NMDAR-ENC-RP02 |  | diagnostic_puzzle | 4 → 7 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-RP03 |  | diagnostic_puzzle | 4 → 7 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-RS01 |  | straightforward → moderate | 5 → 7 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-RS02 |  | straightforward → moderate | 4 → 7 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-RS03 |  | straightforward → moderate | 4 → 7 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-RS04 |  | straightforward → moderate | 4 → 7 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-S01 |  | straightforward → moderate | 4 → 5 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-S02 |  | straightforward → moderate | 4 → 5 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-S03 |  | straightforward → moderate | 4 → 5 | 4 | 0 | 2 | 9/9 |
| NMDAR-ENC-S04 |  | straightforward → moderate | 4 → 5 | 4 | 0 | 2 | 9/9 |
| PD-M01 | ✓ | moderate | 3 → 5 | 5 | 0 | 2 | 8/8 |
| PD-M02 | ✓ | moderate | 3 → 5 | 5 | 0 | 2 | 8/8 |
| PD-M03 | ✓ | moderate | 4 → 5 | 5 | 0 | 2 | 8/8 |
| PD-P01 |  | diagnostic_puzzle | 4 → 4 | 5 | 0 | 2 | 9/9 |
| PD-P02 | ✓ | diagnostic_puzzle | 3 → 4 | 4 | 0 | 1 | 9/9 |
| PD-P03 | ✓ | diagnostic_puzzle | 2 → 3 | 4 | 0 | 1 | 7/7 |
| PD-RM01 | ✓ | moderate | 2 → 4 | 5 | 0 | 2 | 8/8 |
| PD-RM02 | ✓ | moderate | 4 → 5 | 5 | 0 | 2 | 7/7 |
| PD-RM03 | ✓ | moderate | 3 → 5 | 5 | 0 | 2 | 7/7 |
| PD-RP01 |  | diagnostic_puzzle | 4 → 5 | 3 | 0 | 2 | 10/10 |
| PD-RP02 |  | diagnostic_puzzle | 4 → 6 | 4 | 0 | 2 | 9/9 |
| PD-RP03 | ✓ | diagnostic_puzzle | 4 → 5 | 4 | 0 | 2 | 9/9 |
| PD-RS01 | ✓ | straightforward | 2 → 4 | 5 | 0 | 2 | 7/7 |
| PD-RS02 |  | straightforward → moderate | 3 → 4 | 5 | 0 | 2 | 7/7 |
| PD-RS03 | ✓ | straightforward → moderate | 3 → 4 | 5 | 0 | 2 | 7/7 |
| PD-RS04 | ✓ | straightforward → moderate | 2 → 4 | 5 | 0 | 2 | 7/7 |
| PD-S01 |  | straightforward | 3 → 4 | 5 | 0 | 2 | 7/7 |
| PD-S02 | ✓ | straightforward | 3 → 4 | 5 | 0 | 2 | 7/7 |
| PD-S03 | ✓ | straightforward | 3 → 4 | 5 | 0 | 2 | 7/7 |
| PD-S04 |  | straightforward | 3 → 4 | 5 | 0 | 2 | 7/7 |
| SYNC-CARD-M01 | ✓ | moderate | 5 → 5 | 2 | 0 | 3 | 10/10 |
| SYNC-CARD-M02 | ✓ | moderate | 4 → 5 | 2 | 0 | 2 | 9/9 |
| SYNC-CARD-M03 | ✓ | moderate | 5 → 5 | 1 | 0 | 2 | 10/10 |
| SYNC-CARD-P01 | ✓ | diagnostic_puzzle | 6 → 9 | 3 | 0 | 3 | 10/10 |
| SYNC-CARD-P02 | ✓ | diagnostic_puzzle | 6 → 8 | 2 | 0 | 3 | 10/10 |
| SYNC-CARD-P03 | ✓ | diagnostic_puzzle | 4 → 4 | 3 | 0 | 2 | 9/9 |
| SYNC-CARD-RM01 | ✓ | moderate → diagnostic_puzzle | 5 → 8 | 1 | 0 | 2 | 10/10 |
| SYNC-CARD-RM02 | ✓ | moderate | 5 → 7 | 3 | 0 | 2 | 9/9 |
| SYNC-CARD-RM03 | ✓ | moderate | 5 → 7 | 2 | 0 | 2 | 10/10 |
| SYNC-CARD-RP01 | ✓ | diagnostic_puzzle | 6 → 8 | 3 | 0 | 2 | 9/9 |
| SYNC-CARD-RP02 | ✓ | diagnostic_puzzle | 4 → 8 | 3 | 0 | 2 | 9/9 |
| SYNC-CARD-RP03 | ✓ | diagnostic_puzzle | 6 → 8 | 3 | 0 | 2 | 10/10 |
| SYNC-CARD-RS01 |  | straightforward | 4 → 7 | 3 | 0 | 2 | 9/9 |
| SYNC-CARD-RS02 |  | straightforward | 4 → 7 | 2 | 0 | 2 | 8/8 |
| SYNC-CARD-RS03 |  | straightforward | 4 → 7 | 2 | 0 | 2 | 8/8 |
| SYNC-CARD-RS04 | ✓ | straightforward | 4 → 7 | 3 | 0 | 2 | 9/9 |
| SYNC-CARD-S01 |  | straightforward | 4 → 5 | 1 | 0 | 2 | 8/8 |
| SYNC-CARD-S02 | ✓ | straightforward | 4 → 5 | 1 | 1 | 3 | 8/8 |
| SYNC-CARD-S03 | ✓ | straightforward | 4 → 5 | 1 | 0 | 3 | 8/8 |
| SYNC-CARD-S04 | ✓ | straightforward | 4 → 5 | 1 | 0 | 2 | 8/8 |
