# FTD round plan (November 2026)

Lead plan for FTD-M01..M10, P01..P08, S01..S12, written 16 Nov 2026. The decisions and their
reasons are in `plans/FTD-decisions.md` (D1..D27 below refer to its entries). There are 108 notes,
all from R1. **No FTD case is approved** (`work/approved.txt`).

Cases read in full: M05, M06, M09, P04. Read in part: M08 (HPI, criteria, differential, CSF and
drug outputs), P01, S06, S11, M10, M07.

The class sweeps were scripted over all 30 cases, and over the 600 where cheap. The scripts are in
`/home/aprotani/review-round-2026-11/work/scratch/ftd-lead/`:

| script | what it measures |
|---|---|
| `survey_ftd.py` | criteria, stop rules, sequence, avoided actions, musts |
| `classes_ftd.py` | genetics, MRI, FDG |
| `classes2_ftd.py` | performance status, Rascovsky findings |
| `classes3_ftd.py` | meds, ECG, CT, perfusion-MRI rationales |
| `classes4_ftd.py` | null significance, drug reports, thiamine, alcohol musts |
| `cross600.py` | the same checks across all 600 cases |
| `dxmatch_ftd.py` | scorer acceptance of candidate answers |

Workers:
- Edit only through `case_io`.
- After each case, run `perfect_agent.py CASE -v`, `case_io.py check CASE` and, after any MRI edit,
  `mri_probe.py`.
- Keep `criterion_id`s.
- English in the case's own spelling; no em dashes in new text; no review-process text in `metadata`.
- After any `rejected` edit, test the answers listed below with `DiagnosisCriterion.matches`.

## 1. Governing guidelines and canonical facts

| Key | Source | Governs |
|---|---|---|
| `[Rascovsky_2011]` | Brain 2011;134:2456-2477 | bvFTD features and certainty. Possible = 3 of 6 features. Probable = possible + functional decline + imaging (MRI/CT atrophy or PET/SPECT). Definite = histopathology or a known pathogenic mutation. Feature E includes increased alcohol. |
| `[Gorno_Tempini_2011]` | Neurology 2011;76:1006-1014 | svPPA, nfvPPA (S11, S12) |
| `[NICE_NG97]` | NICE NG97 (2018) | Reversible-cause bloods; structural imaging (MRI preferred, CT if MRI unavailable or contraindicated); FDG-PET or perfusion SPECT when the subtype is uncertain; no ChEI or memantine in FTD |
| `[SNLG_ISS_2024]` | ISS/SNLG dementia guideline 2024 | as NICE NG97 (R1's source) |
| `[Ducharme_2020]` | Brain 2020;143:1632-1650 | bvFTD versus psychiatric disorders. Non-specific FDG hypometabolism must not be over-interpreted; when it is the only abnormal imaging, reconsider a psychiatric origin. |
| `[Frisoni_2024]` | Lancet Neurol 2024;23:302-312 | FDG = neurodegeneration pattern; amyloid PET / CSF = AD question |
| `[Ulugut_2020]` | Brain 2020;143:2831-2843 | Right temporal variant FTD (M10) |
| `[Strong_2017]`, `[Gold_Coast_2020]`, `[EAN_ALS_2024]`, `[NICE_NG42]`, `[AAN_2009]` | as in the pack | FTD-MND (P08) |
| `[EACS_2025]` | EACS Guidelines 13.0 | HIV neurocognitive work-up: MRI and CSF in people "without obvious confounding conditions" (M08) |
| `[Armstrong_2013]` NEW | Armstrong MJ et al. Neurology 2013;80:496-503 | CBS criteria: possible = at least 1 motor (limb rigidity or akinesia, dystonia, myoclonus) plus at least 1 cortical feature; probable = asymmetric, 2 plus 2 (M06) |
| `[Escitalopram_SmPC]` NEW | Escitalopram SmPC section 4.3; MHRA Drug Safety Update Dec 2011/Dec 2014 | Escitalopram contraindicated with other QT-prolonging drugs; max 20 mg (10 mg at 65 or older) (P03) |
| `[AHS_Evans_2010]` NEW | Evans RW et al. Headache 2010;50:1089-1099 | Evidence does not support limiting triptans with SSRIs (M04) |
| `[CANMAT_ISBD_2018]` NEW | Yatham LN et al. Bipolar Disord 2018;20:97-170 | Antidepressants in bipolar I: switch risk, only adjunctive to a mood stabiliser, with monitoring (M05) |
| `[EFNS_Wernicke_2010]` NEW | Galvin R et al. Eur J Neurol 2010;17:1408-1418 | Thiamine 200 mg three times daily, preferably IV, before carbohydrate; Caine criteria (M07) |
| `[NICE_CG115]` NEW | NICE CG115 (2011) | AUDIT, SADQ; assisted withdrawal at SADQ 15 or more; benzodiazepine regimen |
| `[NICE_CG100]` NEW | NICE CG100 (2010) 1.2.1 | Oral thiamine for harmful or dependent drinkers at nutritional risk; parenteral when Wernicke is suspected |
| `[NICE_NG50]` NEW | NICE NG50 (2016) | Transient elastography for people who drink harmful amounts (M07) |
| `[NICE_NG71]` NEW | NICE NG71 (2017) 1.2.6 | DaT-SPECT for tremor not clinically separable from essential tremor (P04) |
| `[Betz_2018]` NEW | Betz ME et al. Ann Intern Med 2018;169:47-49 | Firearm access assessment and restriction in dementia (S06) |

Scorer facts (D-preamble):
- Recommended and optional criteria are never "extra" for the stop rule.
- The bvFTD cases already accept "definite bvFTD", "bvFTD with definite FTLD pathology",
  "possible bvFTD", "C9orf72-/GRN-associated bvFTD" and "genetically confirmed familial bvFTD".

Pathogenic authored panels:
- C9orf72: M02, P01, P04, P05, P07, P08, S03, S05, S10.
- GRN: P02, S07; M06 is a known carrier.
- MAPT: P03.

Stored ALS panels: M02, P01, P04, P05, P07, P08, S03, S05, S10.

MRI normal or equivocal: P01, P02, P05, P07.

## 2. Classes

Each class gives: description, notes, cases measured, fix, and the canonical text.

### C1 LIT (D1)
- **Notes:** 48 literature "no" / "?" notes (every case).
- **Measured:** 0 of 30 cases has any literature remnant.
- **Fix:** FIXED by class LIT, commit 393c547e. Workers re-verify and never add anything back.

### C2 Definite certainty in musts (D2)
- **Notes:** d1c4e3b7, c0117e9b, f3545383, 9ee3d9d6, 5040499f, b94d7e75, b4a2044c, 8b9672cf, f8fc0c33.
  116ebe03 and 8aa821c6 are ALREADY-FIXED.
- **Cases to edit:** M02, P03, P04, P05, P07, P08, S03, S05, S07, S10. Must 0 says "(possible or
  probable)" while the panel is pathogenic.
- **Labels:** unchanged.

Canonical must 0 (bvFTD):

> "Apply the Rascovsky 2011 criteria: state which features are present, the functional decline,
> and the level of certainty: possible or probable on the clinical and imaging findings, and
> definite (bvFTD with definite FTLD pathology) if the counselled gene panel shows a pathogenic
> variant."

- Keep any case-specific clause already in must 0 (for example M04 "Base it on her husband's
  account...").
- P08: append "; definite if a pathogenic variant is found" to its certainty clause.

### C3 Possible bvFTD with a normal or equivocal MRI (D3)
- **Notes:** ccb82f4f (P01) and 7d0e7312 (P02) are ALREADY-FIXED; aa063460 (P05) and 57e3f6ed (P07)
  are FIXED.
- **Measured:** P01 and P02 must 0 already have the three-level clause; P05 and P07 do not.
- **Fix:** FDG-PET stays recommended in all four.

P05 and P07 must 0:

> "Apply the Rascovsky 2011 criteria: state which features are present, the functional decline,
> and the level of certainty: possible on the clinical features with a {normal / borderline} MRI;
> probable once functional imaging shows frontal or anterior temporal hypometabolism; definite if
> a pathogenic variant is found."

This text supersedes C2 in P05 and P07.

### C4 FDG/SPECT over-call with normal or equivocal MRI (D4)
- **Notes:** ad58e131 (P02), 4a526dcb (P05).
- **Measured:** the FDG and SPECT reports of P01, P02, P05 and P07 all end with "consistent with
  frontotemporal lobar degeneration / early frontotemporal ... profile" and no qualifier.
- **Fix:** keep the findings; replace the closing sentence of each impression with:

> "The pattern is compatible with frontotemporal lobar degeneration; mild frontal hypometabolism
> is not specific and can occur in primary psychiatric disorders. Clinical correlation
> recommended."

For SPECT, use "hypoperfusion".

### C5 ALS panel without MND (D5)
- **Notes:** 3fce79a8 (S03), cd3a3e1d (S05), 73ab2e96 (S10).
- **Measured:** ALS reports are stored in 9 cases; none is a criterion except in P08.
- **Fix:**
  - P01, P04, P05, P07, S03, S05, S10: add the avoided action below and move the ALS follow-up to
    the end of `followup_outputs` (keep the report).
  - M02: add `{test_type: genetic_panel:ALS}` as an alternative of the optional genetics criterion
    `action-4-order-specialized-test` (brother died of ALS).
  - P08: unchanged.

Avoided action:

```json
{"criterion_id": "avoid-waste-als-gene-panel", "severity": "waste", "citations": ["[Strong_2017]"],
 "alternatives": [{"tool_name": "order_specialized_test", "required_arguments": {"test_type": "genetic_panel:ALS"}}],
 "rationale": "No sign of motor neuron disease and the FTD panel already tests C9orf72; an ALS panel adds nothing to this work-up, and motor neuron disease is followed clinically."}
```

### C6 Templated performance status (D6)
- **Notes:** 909dee2f (M06), 6fd2b279 (M10), baf51bf8 (P03), 15046dcf (P07).
- **Measured:** identical lines in 26 cases (all except P08, S09, S11, S12).
- **Fix:** rewrite the `order_performance_status` follow-up of all 26 from the case's HPI:
  - "activity": the documented occupational, social and instrumental limits;
  - "self-care": what is documented (independent, prompted, supervised);
  - what the history says about finances, driving and living alone, as documented, or "not
    formally assessed".
- **Scores:** Karnofsky 80 / ECOG 1 when self-care is intact and only work or complex activities
  are lost; 70 / 1 when instrumental activities need supervision; lower only when documented.
- **Impression:** one line matching the scores.
- Examples of what is documented:
  - M06: retired before onset, manages her own finances with subtle errors, errors in her
    daughter's medication schedule, basic ADLs intact.
  - M10: dependent on relatives in social situations because she cannot recognise familiar people;
    otherwise autonomous.
  - P03: resigned from chaplaincy work, lives alone, finances not documented as impaired.
  - P07: work failure, reduced social engagement, prompting for hygiene.
- **Elsewhere:** also in ALZ-EARLY (24 cases); told to that lead.

### C7 Rascovsky feature scoring (D7)
- **Notes:** 5a6ec98f (M04), c9480a7a (P07), 43930018 (M06), 4612da84 (M09).
- **Measured cases:**

| Case | Finding | Action |
|---|---|---|
| M01 | macaroni-and-cheese routine | E counted on a fixed meal routine; check the HPI, likely 6 to 5 |
| M03 | chips and dip at the same time | as M01 |
| M04 | same lunch | as M01 |
| P07 | same meals | as M01 |
| P05 | diet narrowed to three foods | keep only if the HPI says it is new |
| M09 | F present with the MoCA not completed | 6 to 5 |
| M06 | A from one act, C from absent visible grief | 5 to 3 |

- Already conservative (no change): M10, P01, P02, M07, M08.
- **Rule:** E only for a documented change from premorbid eating (a new food fad or preference,
  sweet craving, binge eating, more alcohol or cigarettes, oral exploration). One behaviour counts
  in one domain. F at the bedside only with a completed screen. A feature needs a persistent
  pattern, not one act.
- **Fields to align:** `criteria_met`, scores ("Rascovsky features present"), impression count and
  list, criterion `expected_evidence`, must 0 lists, key evidence.
- **Text for a feature not counted:**
  - E: "Absent: the fixed {meal} is part of the routine counted above; no change in appetite, food
    preference, sweet craving or alcohol use reported."
  - M09 F: "Not established at the bedside: clock planning and trails B are failed, but the MoCA
    could not be completed; the neuropsychological battery decides."
  - M06 A: "Not established: a single impulsive act (photographs given away); no persistent
    pattern of disinhibition described."
  - M06 C: "Not established at the bedside: blunted response to her daughter's decline, which may
    also reflect coping; social-cognition testing is the better measure."
- **M06 knock-on:** M06 must 1, differential 1, key evidence 2 and red herring 1 drop "impulsive
  acts" and keep "rigid routines, withdrawal, errors she denies, executive deficits, asymmetric
  atrophy and right-hand cortical signs".

### C8 Abnormal rows with null significance (D8)
- **Notes:** 071a5363 (M03), 808af2e1 (M05), 94b68fbc (M07), 68b33e69 (P06).
- **Measured (38 rows):**

| Case | Rows |
|---|---|
| M01 | glucose 104, HbA1c 6.1 |
| M03 | glucose 156, HbA1c 7.8 |
| M04 | anti-TPO 320, anti-Tg 144 |
| M05 | glucose 138, HbA1c 7.1, lithium 1.28 |
| M06 | progranulin 42 |
| M07 | ALT 62, AST 88, GGT 148, MCV 101, CDT 3.4 |
| P01 | ammonia 38 (twice) |
| P02 | fasting glucose 102, progranulin 38 |
| P03 | CCP 112, RF 64 |
| P06 | glucose 156, HbA1c 8.2, TC 221, LDL 142 |
| P08 | CK 318 |
| S01 | glucose 112, CDT 2.6, HbA1c 6.9 |
| S05 | glucose 128, CDT 3.1, HbA1c 7.4 |
| S07 | progranulin 41 |
| S09 | CDT 2.4 |
| S11 | glucose 118 and HbA1c 6.8 (twice) |

- **Fix:** one factual sentence per row, not naming the diagnosis. Examples:
  - glycaemia: "Above the diabetes treatment target; relevant to vascular risk management."
  - CDT: "Consistent with sustained heavy alcohol intake."
  - LFT, GGT and MCV: "Pattern consistent with alcohol-related liver injury; needs follow-up."
  - progranulin: "Low, consistent with GRN haploinsufficiency."
  - CK: "Mildly raised; seen with denervation."
  - known autoimmunity: "Consistent with the known {Hashimoto thyroiditis / rheumatoid arthritis}."
  - ammonia: see C18.
- Check that a must covers each managed abnormality (M07 liver C14b; S05 HbA1c; M05 C9a).
- Ruling FIXED, with the CENTRAL display remark.

### C9 Lithium (M05) (D9)
- **Notes:** 808af2e1.

C9a, must 1:

> "Explain why lithium toxicity or a bipolar relapse does not account for the whole syndrome
> while lithium neurotoxicity may still contribute: the level of 1.28 mmol/L is above range with
> an eGFR of 64, and chronic neurotoxicity can impair cognition without tremor or ataxia, but his
> son describes a euthymic, qualitatively new syndrome of apathy, stereotyped repetition and
> impulsivity over 16 months with frontal atrophy."

- Must 2: append "and reassess cognition and behaviour once the level is back in range."
- `rejected`: remove "lithium toxicity" and "lithium neurotoxicity".
- Check that "probable bvFTD; lithium neurotoxicity may contribute" matches.

### C11 ECG for a safety indication (D11)
- **Notes:** baa96bf5 (M05), bf5a7b2b (P03).
- **Measured across 600:** P03 is the only ECG-waste case with 2 QT drugs.
- **Fix, both cases:** delete `avoid-waste-2-analyze-ecg`; move `fallback_tool_outputs.ecg` to
  `initial_tool_outputs.ecg` (set the fallback to null and update `fallback_tool_kinds`); place
  the criterion after the diagnostic core.
- **P03:** add `action-ecg-qtc`, recommended, `analyze_ecg {}`.
  - Label: "ECG for QTc on escitalopram with hydroxychloroquine".
  - Rationale: "Two QT-prolonging drugs, a contraindicated combination for escitalopram; the QTc
    decides the medication review."
  - Citations `[Escitalopram_SmPC]`; expected evidence is the stored QTc.
  - Add the must: "Review the escitalopram and hydroxychloroquine combination with her
    psychiatrist and rheumatologist: escitalopram is contraindicated with other QT-prolonging
    drugs, so consider an alternative antidepressant, and check the QTc, potassium and magnesium."
- **M05:** add `action-ecg-safety`, optional.
  - Label: "ECG for cardiac safety on lithium with coronary disease".
  - Rationale: "Coronary disease and a lithium level above range; not needed for the dementia
    diagnosis."

### C12 Drug-check reports (D12)
- **Notes:** 2cce5786 (M04), 84873d7e (M05), 5869578c (P03).
- **M04** interaction line: "Sertraline + sumatriptan: serotonin syndrome is rare with this
  combination and the evidence does not support limiting triptan use; counsel on symptoms
  (agitation, tremor, myoclonus, hyperthermia) and assess individually."
- **M05** warning: "Bipolar I disorder: an antidepressant can trigger a switch to mania or a mixed
  state; use only alongside the mood stabiliser, with his psychiatrist, and monitor for manic or
  mixed symptoms; lithium lowers but does not remove the risk."
- **P03**, in the initial `drug_interactions` (the proposed agent is escitalopram):
  - interaction: "Escitalopram + hydroxychloroquine: additive QT prolongation; escitalopram is
    contraindicated with QT-prolonging drugs; review the combination with the prescribers,
    consider an alternative, and monitor QTc and electrolytes."
  - Keep the methotrexate and folic acid lines: no clinically significant interaction.

### C13 M06 corticobasal wording (D13)
- **Notes:** f1f67b4e.
- New `accepted[0]`: "Behavioral variant frontotemporal dementia (bvFTD), definite (known
  pathogenic GRN variant), with possible early corticobasal-spectrum signs (mild right-hand
  apraxia and graphesthesia)".
- Must 2:

> "Describe the mild right-hand ideomotor apraxia and impaired graphesthesia as possible early
> corticobasal-spectrum signs that do not meet corticobasal syndrome criteria (no rigidity,
> akinesia, dystonia or myoclonus), and plan follow-up of motor, language and praxis function."

- Cite `[Armstrong_2013]`.

### C14 M07 (D14)
- **Notes:** eb9986c4, 51130a17, ce2fbd1b, 94b68fbc.
- New `accepted[0]`: "Behavioral variant frontotemporal dementia (bvFTD), probable (provisional
  until reassessment after abstinence and sleep apnoea treatment), with concurrent alcohol use
  disorder and alcohol-related cerebellar degeneration; family history suggestive but
  unconfirmed".
- Must 0 certainty clause: "(probable, held provisionally: heavy alcohol use and untreated sleep
  apnoea can also cause frontal deficits and atrophy, so reassess after sustained abstinence and
  CPAP)".
- `rejected`: remove "wernicke".
- Any genetics rationale or text saying "sporadic" gets "family history suggestive but
  unconfirmed".

C14a, must 2:

> "Give parenteral high-dose thiamine (EFNS 2010: 200 mg three times daily, preferably IV), before
> or together with any glucose-containing fluid wherever feasible and never delaying glucose for
> hypoglycaemia, because cerebellar signs with cognitive impairment in a heavy drinker meet two
> Caine criteria for Wernicke encephalopathy; then continue oral thiamine, and refer to addiction
> services for assessment of dependence and medically assisted withdrawal."

C14b, new must:

> "Assess the raised transaminases, GGT and macrocytosis as alcohol-related liver injury: repeat
> liver tests after abstinence and refer for liver fibrosis assessment (NICE NG50)."

### C15 M08 (D15)
- **Notes:** 962d3cd1, bb11618e.
- New `accepted[0]`: "Behavioral variant frontotemporal dementia (bvFTD), probable, in a person
  with well-controlled HIV (CSF viral escape and opportunistic infection excluded; HIV-associated
  neurocognitive disorder unlikely)".
- Must 1:

> "Explain why HIV-associated neurocognitive disorder is unlikely to explain the syndrome, without
> excluding a contribution: suppressed plasma HIV RNA, CD4 680, normal white matter and a cortical
> frontal rather than subcortical profile; CSF HIV RNA, if obtained, excludes CSF viral escape;
> explain why treatment-resistant depression does not account for a change unlike her earlier
> episodes."

- `action-8-analyze-csf`: importance recommended; remove it from `required_before_assessment`.
- Rationale: "Recommended: CSF HIV RNA detects CSF viral escape, a treatable cause, although the
  frontal phenotype with atrophy already gives a competing explanation."
- `rejected`: remove "HAND" and "HIV-associated neurocognitive disorder".
- Differential 1 likelihood stays low, with "cannot be categorically excluded".
- Update `difficulty_rationale`.

### C16 M09 (D16)
- **Notes:** 2dacb58f, 44fdd4b7, 4612da84 (C7).
- `action-4-order-ct-scan`: optional. Rationale: "Acceptable if MRI cannot be obtained promptly; no
  trauma, focal sign or acute change calls for an emergency CT."
- Remove the CT criterion from the stop rule; delete the CT-before-MRI constraint.
- `action-tox-screen-blood-alcohol`: recommended, out of the stop rule. Rationale: "The ED team
  raises intoxication; a negative screen with undetectable alcohol makes it very unlikely but an
  immunoassay does not detect every substance."
- Must 1: "...an insidious 18-month course without mood elevation or reduced need for sleep, no
  toxidrome and undetectable blood alcohol (a urine immunoassay does not cover every substance),
  normal metabolic tests, and full alertness and orientation."
- The same wording goes in key evidence 3 and differential 2. Fix the KCE "exclude" wording too.
- Move the CT initial output's use to optional: keep the report.
- Probe the served blood alcohol (`BAL` = bronchoalveolar lavage; "blood alcohol" maps to
  `ethanol`). If no term serves it, raise a CENTRAL request.

### C17 M10 (D17)
- **Notes:** d645ace0, 0102f4ac.
- New `accepted[0]`: "Right temporal variant frontotemporal dementia (rtvFTD), meeting probable
  behavioral variant FTD (bvFTD) criteria".
- `rejected`: remove "semantic dementia"; keep "svPPA" and "semantic variant primary progressive
  aphasia".
- Synonyms are CENTRAL.
- Red herring 2 `correct_interpretation`:

> "Apathy in FTD is not depression: there is no dysphoria, hopelessness or neurovegetative change,
> and the lack of response to sertraline argues against depression as the explanation. An SSRI may
> still be continued for compulsive or repetitive behaviour in FTD if it helps, judged on that
> effect."

- Prohibition 1: "Do not escalate antidepressant therapy for presumed depression in place of the
  dementia work-up: treating FTD apathy as depression delays diagnosis."
- Cite `[Ulugut_2020]` on the clinical-assessment or MRI criterion if it is not already present.

### C18 P01 valproate (D18)
- **Notes:** 4a0fdd2d.
- Must 2:

> "Interpret the valproate level and ammonia: a therapeutic trough and a mildly raised ammonia
> with normal liver tests make valproate encephalopathy an unlikely explanation for an 18-month
> progressive syndrome but do not exclude a contribution; continue valproate (no abrupt
> withdrawal), review it with his psychiatrist, and recheck ammonia and review the drug if the
> ammonia stays raised or drowsiness, fluctuating confusion or asterixis appear."

- Prohibition 4: insert "abruptly".
- Ammonia significance: "Mildly raised; common on valproate and not by itself evidence of
  encephalopathy; recheck if it persists."

### C19 P04 (D19)
- **Notes:** de76c48a, 4473d085.
- New `accepted[0]`: "Behavioral variant frontotemporal dementia (bvFTD), probable, with
  levodopa-responsive parkinsonism (co-existing Parkinson's disease or FTD-associated
  parkinsonism)".
- New differential entry, likelihood moderate:
  - Name: "C9orf72- or FTLD-associated parkinsonism (one process)".
  - Key features: "For: early-onset behavioural syndrome with parkinsonism; C9orf72 expansions can
    cause asymmetric, sometimes levodopa-responsive parkinsonism. Against: typical asymmetric rest
    tremor with a good levodopa response. Only genetics or follow-up separates it from
    coincidental PD."
- Must 1: append "and that the parkinsonism may be co-existing Parkinson's disease or part of one
  FTD-associated process (for example C9orf72), which genetics or follow-up decides."
- Delete criterion `action-8-order-advanced-imaging` (DaTscan); add an avoided waste action
  `{modality: DaTscan}`.
  - Citations `[NICE_NG71]`.
  - Rationale: "The parkinsonism is clinically established and levodopa-responsive; DaT-SPECT is
    for tremor that cannot be separated from essential tremor, and it cannot distinguish Parkinson's
    disease from C9orf72-associated parkinsonism."
- Check that no other avoided action already matches DaTscan; replace the wildcard if one does.
- Move the DaTscan follow-up last.
- Reword red herring 1, `metadata.notes` and `difficulty_rationale` ("co-existing PD" →
  "parkinsonism, PD or FTD-associated").

### C21 Alcohol (D21)
- **Notes:** 353235b4 (S01), ade5774b (S09).
- **Cases:** S01, S05, S06, S09; S10 aligned; M07 via C14a.

Canonical must:

> "Assess the escalating drinking ({amount}) as both a possible bvFTD behaviour and a contributor
> that is not excluded: screen for dependence (AUDIT, and SADQ if dependent) and previous
> withdrawal symptoms; if dependent, arrange medically assisted withdrawal with alcohol services
> rather than abrupt unsupervised abstinence, with {spouse} controlling access as support, not as
> withdrawal management; give oral thiamine, parenteral if Wernicke encephalopathy is suspected or
> nutrition is poor (NICE CG115, CG100)."

- Where must 1 combines "explain why ARBD does not account" with management, keep the "explain"
  clause softened to "does not account for the whole progressive syndrome" and replace the
  management clause with the text above.
- S06: add it as a new must.
- Differential "Alcohol-related brain damage" key features end: "low as the sole cause; a
  contribution is not excluded".
- `rejected`: S01, S05, S06, S09 and S10 drop "alcohol-related brain damage" and "alcohol-related
  dementia"; keep "korsakoff" and "wernicke".
- S01 prohibition 4 ("not to alcohol alone") stays.

### C22 Head CT rationale (D22)
- **Notes:** 5d57a74c (S01), 143588da (S02).
- **Cases:** 27 (all except S06, M09, S12).
- **Rationale text:**

> "MRI is available and is the preferred structural study; non-contrast CT is the alternative only
> when MRI is unavailable or contraindicated, so a CT added to the MRI duplicates imaging without
> new information."

- Citations `["[NICE_NG97]", "[SNLG_ISS_2024]"]`. Severity stays waste.
- PPA (S11): "...structural study for the PPA work-up...".

### C23 Perfusion MRI rationale (D23)
- **Notes:** 832dd141 (S07).
- **Cases:** P03, P04, P05, P06, P07, S07, S08, S09, S10.
- **Text:**

> "Perfusion MRI is not part of the FTD work-up; FDG-PET, or perfusion SPECT where FDG-PET is
> unavailable, is the functional study when one is needed. Amyloid PET answers a different
> question (Alzheimer pathology)."

- Citations `["[NICE_NG97]", "[Frisoni_2024]"]`.

### C24 S06 violence risk (D24)
- **Notes:** 80e972af.
- New must:

> "Assess the risk of violence now: intent toward the neighbour or others, threats to his wife,
> access to other weapons or ammunition (including firearms stored elsewhere), and his wife's
> safety; agree a written safety plan with her, keep firearms and ammunition out of the home
> permanently, and arrange urgent psychiatric or emergency assessment if the risk is imminent."

- Must 2 keeps driving, finances and LPA. Cite `[Betz_2018]` in the log.

### C25 S11 (D25)
- **Notes:** 8d60dcbe.
- Red herring 2 `correct_interpretation`:

> "The outside images are not available, so the earlier 'asymmetry' can only tentatively be read
> as early atrophy; the current MRI shows focal anterior temporal atrophy without the signal
> change, encephalomalacia or haemosiderin that HSV encephalitis leaves, and the course is
> progressive, which argues against old encephalitis."

- Must 2: insert "(the earlier outside scan cannot be reinterpreted without its images)".

### C26 S12 (D26)
- **Notes:** acb7ab4d.
- Prohibition 0:

> "Do not attribute the progressive speech deficit to the prior TIA: the deficit has progressed
> continuously for 18 months, the MRI shows no chronic strategic infarct or encephalomalacia, and
> the atrophy is left posterior fronto-insular; a negative DWI this late cannot date or exclude an
> old event."

- Differential stroke key features: the same reasons, with no "DWI-negative" prerequisite.

## 3. Per-case index (all 30; none approved)

Rulings: FIXED, DECLINED, ALREADY-FIXED, CENTRAL, NEEDS-ANDREA, NO-ACTION. "LIT" = FIXED by class
LIT, commit 393c547e, re-verified with no remnant. The class findings without a note are listed per
case (C6, C22, C23, C7, C8, C21).

**FTD-M01**
- 57885156-d2c5-48af-bd6d-8551f3ccdab5: LIT.
- aaa59470-91a6-4f2d-9581-a7648262814f: LIT.
- Class: C7 (E fixed routine, likely 6 to 5), C8 (glucose, HbA1c), C6, C22.

**FTD-M02**
- bf932975-92ef-46fd-972d-1701a2710b52: LIT.
- 0f5fe9ee-1af0-4593-8ecf-28636c5fae3a: LIT.
- d1c4e3b7-4505-4019-b5a5-67eeceb7dc72: FIXED (C2 must 0; label kept probable, scorer already
  accepts definite).
- Class: C5 (ALS panel as an alternative of the optional genetics), C6, C22.

**FTD-M03**
- df91dd17-b668-4b69-82b2-5649c3b9d9ef: LIT.
- 071a5363-6a29-4cc0-a006-4f90fab0db45: FIXED (C8 significance on glucose and HbA1c; must 2
  already covers glycaemia; CENTRAL display remark).
- Class: C7 (E chips routine), C6, C22.

**FTD-M04**
- 59bdbd63-c806-42af-b4f8-b53bbaa50048: LIT.
- 5a6ec98f-44a1-4d4d-a235-b9bcbb360b6d: FIXED (C7: E absent, 5 of 6).
- 2cce5786-8870-4ab7-b45a-02ff45335c8d: FIXED (C12 triptan line).
- Class: C8 (thyroid antibodies), C6, C22.

**FTD-M05**
- 7e90367d-5b6f-4f9b-b65f-7f0fa51db0a1: LIT.
- 808af2e1-0e60-4399-bc40-04f110431f87: FIXED (C8 + C9a, must 2, `rejected`, differential 1).
- 0367115d-cea0-44c5-9a25-7d9399e705b6: ALREADY-FIXED (distinct criteria `action-4-interpret-labs`
  and `action-lithium-level` both in the stop rule) + CENTRAL (display item 3).
- 84873d7e-c171-41a7-aa16-6b9b0fc097ce: FIXED (C12 mania warning).
- baa96bf5-04ef-4199-8c52-29066289908d: FIXED (C11 optional ECG, waste removed).
- Class: C8 glucose and HbA1c, C6, C22.

**FTD-M06**
- ae720673-1e2a-484d-9b13-4d4bd5f1143f: LIT.
- 904bfc61-d772-47f6-a2a0-298e8c965650: LIT.
- 909dee2f-432d-48e0-bc4f-f9ad34ae72e8: FIXED (C6).
- 43930018-474c-4e62-bd87-563c1fcabe70: FIXED (C7: 3 of 6, knock-on fields).
- f1f67b4e-3390-42a2-b110-b36aba2becee: FIXED (C13 label wording + must 2; label change on the
  CENTRAL list).
- Class: C8 progranulin, C22.

**FTD-M07**
- 05a17bc0-0f4a-4cd4-aa39-0be6d4c0e248: LIT.
- 6881b5e1-f3f3-4970-ad50-1267bdcce94b: LIT.
- eb9986c4-3be6-4c56-a106-880238aead53: FIXED (C14 label "provisional", must 0; must 1 already
  reassesses after abstinence and CPAP).
- ce2fbd1b-808c-4b84-af43-6ca52a4aab17: FIXED (C14a).
- 51130a17-3728-4c08-a50a-6d6ecbfd706f: FIXED (C14 label without "sporadic").
- 94b68fbc-31b5-423d-b7c4-18e7c726dfd3: FIXED (C8 + C14b).
- Class: `rejected` minus "wernicke", C6, C22.

**FTD-M08**
- 1fc26759-2172-4ef4-bce3-0d8d9f522b2d: LIT.
- 14aceff2-5025-40be-87b3-b932b9c9d713: LIT.
- 962d3cd1-79ac-4712-bfdf-6bbed5cc5631: FIXED (C15 label, must 1, differential, `rejected`).
- bb11618e-1818-49f3-a64c-52f57b8f010f: FIXED (C15: CSF recommended, out of the stop rule; revises
  October Q4).
- Class: C6, C22.

**FTD-M09**
- bd4783ce-dd44-4692-9ca2-46241116977d: LIT.
- c7064ff7-1c6e-4530-a95b-6fa6d87012b2: LIT.
- 2dacb58f-af61-4be9-a3cb-70e5f895310e: FIXED (C16: CT optional, constraint deleted; revises
  October Q6).
- 44fdd4b7-9f74-415a-a3af-ca052ffb6722: FIXED (C16: toxicology recommended, wording).
- 4612da84-c533-4630-8c17-c0de24c57f45: FIXED (C7: F not established, 5 of 6).
- Class: C6 (no CT avoided action here).

**FTD-M10**
- dd2e4516-1c6f-4364-9bee-646f83c3f0b8: LIT.
- 95ff54e9-018c-444d-98ac-b1f1dcc92f59: LIT.
- d645ace0-75e8-4aac-bdf6-1ba07bf1233b: FIXED (C17 label rtvFTD, `rejected`) + CENTRAL (synonyms
  `G31.09+rtv`).
- 6fd2b279-a559-40bc-8588-0c0616bef39e: FIXED (C6).
- 0102f4ac-2d96-4489-83f1-a06c95d9f277: FIXED (C17 red herring, prohibition 1).
- Class: C22.

**FTD-P01**
- 7adab368-1503-41a2-8099-f5b682aed407: LIT.
- 72ba9e03-44f5-43bd-87b4-bb2b14066b45: LIT.
- ccb82f4f-6f6f-4cbc-92bf-425a9a94332f: ALREADY-FIXED (must 0 distinguishes possible, probable
  and definite; FDG recommended and never extra; the scorer accepts "possible bvFTD").
- 116ebe03-ccd7-4290-90e9-a4f92c98a142: ALREADY-FIXED (must 0 "definite if a pathogenic variant
  is found"; the scorer accepts it).
- 4a0fdd2d-0768-4eec-a789-31e6e7abab87: FIXED (C18).
- Class: C4 (FDG and SPECT hedge), C5 (ALS waste), C8 ammonia, C6, C22.

**FTD-P02**
- ea2be647-17af-4e44-9142-0d9f3882c2d6: LIT.
- 7d0e7312-f577-4246-8bd5-06a1b1b3442e: ALREADY-FIXED (must 0 three levels; scorer accepts
  possible).
- 8aa821c6-6175-4aa3-80ae-efc6841c7856: ALREADY-FIXED (must 0 includes definite).
- ad58e131-fd9b-4567-b5b9-e227f5bcc09f: FIXED (C4).
- Class: C8 glucose and progranulin, C6, C22.

**FTD-P03**
- 9f20a979-cfb4-40a2-bae3-9f050bfa92c4: LIT.
- c0117e9b-b425-4120-a5e1-8497013c12ca: FIXED (C2).
- 5869578c-7684-45bd-89a8-8006a5417211: FIXED (C12).
- bf5a7b2b-4d4c-44da-bba6-652f7fc9e878: FIXED (C11 recommended ECG + must).
- baf51bf8-fdff-428d-80eb-99eb19ba9537: FIXED (C6).
- Class: C8 CCP and RF, C22, C23.

**FTD-P04**
- 6b4008ab-9404-420d-84dc-f973608f2c1c: LIT.
- ef5ae893-13ac-46c4-a7ca-83bcd8b0f215: LIT.
- de76c48a-eab4-4c94-b5c2-d5f0ce72deb7: FIXED (C19 label, differential, must 1, notes).
- f3545383-0590-42b1-b240-25aabe6cf2fc: FIXED (C2).
- 4473d085-6d28-4d8a-ad07-be159ad81b42: FIXED (C19: DaTscan becomes waste, criterion deleted) +
  CENTRAL (guidance text).
- Class: C5 ALS waste, C6, C22, C23.

**FTD-P05**
- 72709aa7-7e53-4d70-b76d-382a0bbf49c6: LIT.
- 8cc17559-ba08-4c6a-b697-cc8715202340: LIT.
- aa063460-0318-452e-9f80-711e4e34253e: FIXED (C3 must 0; stop-rule premise answered:
  recommended is never extra).
- f8fc0c33-9e19-48e3-b761-ecafeff79fd3: FIXED (C3 must 0 includes definite).
- 4a526dcb-8540-4f2c-b52f-f59428ccdc0c: FIXED (C4).
- Class: C5, C7 (check E "narrowed to three foods"), C6, C22, C23.

**FTD-P06**
- c7e69332-678a-4770-9654-4c38d8e656f5: LIT.
- d3084ce1-9828-4ef8-84b4-2745a47ff0a9: LIT.
- 68b33e69-b2ac-473a-8e30-8b1fe479781b: FIXED (C8 significance on glucose, HbA1c, TC and LDL;
  must 2 already covers glycaemia, blood pressure and a statin; CENTRAL display remark).
- Class: C6, C22, C23.

**FTD-P07**
- 5a92cdbd-d716-4d1a-9c89-1db595061d4c: LIT.
- 57e3f6ed-6f00-48e3-ab3c-6427e4e2a900: FIXED (C3 must 0; stop-rule premise answered).
- 9ee3d9d6-e6c1-41ec-bf79-68b9e36ae68b: FIXED (C3 includes definite).
- c9480a7a-cdd6-4325-aed6-5fe7fce7a071: FIXED (C7: E absent, 5 of 6).
- 15046dcf-fefd-49e2-b5e6-c3d663db384e: FIXED (C6).
- Class: C4, C5, C22, C23.

**FTD-P08**
- aac2146c-4845-48ad-a9da-bd32568f097d: LIT.
- 275af18e-6e17-4d80-a333-bc9a80fbf7ce: LIT.
- edc62f71-208f-4d0b-93b5-4df2dba060ec: ALREADY-FIXED (respiratory is recommended, never extra;
  must 4 arranges FVC, SNIP and MIP per NICE NG42).
- Class: C2 (definite clause in must 0), C8 CK, C22.

**FTD-S01**
- 6d607adc-b414-470e-b9c8-263716dcc9fb: LIT.
- 7627a8b2-e89f-4195-b8aa-d8bdee9b422c: LIT.
- 353235b4-36ee-40d4-9cb4-4c79cccc4c9e: FIXED (C21 must, differential, `rejected`).
- 5d57a74c-0c3f-4a90-b8d8-8dae3c593a82: FIXED (C22; severity stays waste because the MRI is
  available and done).
- Class: C8 glucose, CDT and HbA1c, C6.

**FTD-S02**
- fd0f5051-9bf6-4b80-b5b8-25471a78e190: LIT.
- 15a028bb-f225-4a50-89a8-0eabfe87c90d: LIT.
- 143588da-037c-49be-b768-292c2a380556: FIXED (C22).
- Class: C6.

**FTD-S03**
- f3e6b607-4816-4580-b404-6d1352b9aecc: LIT.
- 5040499f-2859-4884-a94d-78cee332ecf4: FIXED (C2 must 0; the requested labels are already
  accepted by the scorer).
- 3fce79a8-e237-4509-b5ae-6c72adfe2672: FIXED (C5 ALS waste, report kept last; must 5 MND review
  already present).
- Class: C6, C22.

**FTD-S04**
- 061b9d9a-065b-44c4-bbb7-e6b24b723203: LIT.
- Class: C6, C22.

**FTD-S05**
- 47fa4a86-43da-47ff-bc75-0b7dacd05532: LIT.
- b94d7e75-2b50-4d67-bec0-95b70af88769: FIXED (C2; labels already accepted).
- cd3a3e1d-9eb6-4302-aced-6379d2fcec64: FIXED (C5); its stop-rule part is ALREADY-FIXED (genetics
  optional, never extra).
- Class: C21 alcohol must and `rejected`, C8 glucose, CDT and HbA1c, C6, C22.

**FTD-S06**
- 823fcd1f-1ede-4c53-bee8-0df71ac9fdd8: LIT.
- 27c241e4-5957-4a0a-b4b4-468632e6c35a: LIT.
- 80e972af-17a0-4a16-ab97-e1539d79b349: FIXED (C24).
- Class: C21 (new alcohol must, `rejected`), C6. CT stays required; MRI stays waste.

**FTD-S07**
- 13d4d753-1991-41ab-b1aa-fbc4ea0faa72: LIT.
- b4a2044c-cde2-43fc-8323-4a8b508d0fbd: FIXED (C2; labels already accepted).
- 832dd141-7083-4495-9fdf-adecca85e126: FIXED (C23).
- Class: C8 progranulin, C6, C22.

**FTD-S08**
- 5d03e1fe-41ab-4c90-84f9-0fa309c063c1: LIT.
- Class: C6, C22, C23.

**FTD-S09**
- bc253a6c-a31a-4b29-90e5-49cbcfe506fb: LIT.
- 4662ca9b-9b7b-4368-89f3-2f242930114f: LIT.
- ade5774b-702d-4331-97db-5e7429b6b592: FIXED (C21).
- Class: C8 CDT, C22, C23. Performance status is not templated.

**FTD-S10**
- 096c241c-d473-4e09-9ef0-d28c55a69767: LIT.
- 8b9672cf-96d9-40a8-87f2-48cbf6316777: FIXED (C2; labels already accepted).
- 73ab2e96-9949-4594-9e8f-2c948fc751e0: FIXED (C5).
- Class: C21 (align wording, `rejected`), C6, C22, C23.

**FTD-S11**
- 6689c73e-c114-4532-9117-189a607c7172: LIT.
- 1a346239-42c2-40df-b0b1-e814d7a6b58a: LIT.
- 8d60dcbe-b2cd-4cb8-821c-ae6125d2e42d: FIXED (C25).
- Class: C8 glucose and HbA1c, C22 (PPA wording).

**FTD-S12**
- bf1184cb-bea4-4d38-ad1d-adda1c1ebdda: LIT.
- 501bfd6b-a880-4a2d-bd9e-232001014756: LIT.
- acb7ab4d-c35d-4268-ace3-e40b66f30f1b: FIXED (C26).
- Class: none further.

Totals:

| Ruling | Notes |
|---|---|
| LIT | 48 |
| FIXED | 54 |
| ALREADY-FIXED | 6 (ccb82f4f, 116ebe03, 7d0e7312, 8aa821c6, edc62f71, 0367115d) |
| CENTRAL with fix | d645ace0, 4473d085, 0367115d |
| DECLINED | 0 |
| NEEDS-ANDREA | 0 |

## 4. CENTRAL requests

1. **Synonyms** (`diagnosis_synonyms.yaml`). New entry `G31.09+rtv`, `cases: [FTD-M10]`, labels:
   rtvFTD, right temporal variant FTD, right temporal variant frontotemporal dementia, right
   semantic dementia, right temporal semantic dementia. Test with `matches` that M10 accepts them
   and that S11 does not.
2. **Label changes** (`accepted[0]`, rule 3; scoring unchanged, all G31.09): M06 (C13), M07 (C14),
   M08 (C15), M10 (C17), P04 (C19). Re-run `apply_diagnosis_synonyms.py --check --conditions ftd`.
3. **Criteria pack** `dataset-generation/criteria_packs/FTD.md`:
   - Section 2, M08: CSF recommended. M09: CT optional and toxicology recommended. P04: DaTscan
     becomes waste, so drop the exception. P03: ECG recommended; M05: ECG optional. ALS panel
     waste rule (C5). CT rationale (C22). Dietary-feature rule (C7).
   - Section 1: certainty wording (definite once a pathogenic variant is found, accepted in
     answers).
   - Section 8: add `[Armstrong_2013]`, `[Escitalopram_SmPC]`, `[AHS_Evans_2010]`,
     `[CANMAT_ISBD_2018]`, `[EFNS_Wernicke_2010]`, `[NICE_CG115]`, `[NICE_CG100]`, `[NICE_NG50]`,
     `[NICE_NG71]`, `[Betz_2018]`.
4. **Guidance** (`condition_tool_guidance.yaml` via `build_condition_tool_guidance.py`, FTD).
   Remove "P04 has one explicit optional DaTscan exception". The CT response becomes "M09 optional
   CT". Note the M08 CSF tier and the ECG exceptions. `test_guidance_claims` FTD rows are central.
5. **Review app display**: CENTRAL.md items 1 (null shown as "none": notes 071a5363, 808af2e1,
   94b68fbc, 68b33e69) and 3 (stop rule shows the tool name only: 0367115d).
6. **Vocabulary, conditional**: if the M09 probe shows that no orderable term returns the stored
   blood alcohol (`BAL` is bronchoalveolar lavage), add a priced `ethanol` / blood alcohol term in
   `costs.yaml` with its `tool_io.py` mirror.
7. **Cross-condition flags for other leads**:
   - "thiamine before any glucose" wording in 21 non-FTD cases (FND-RP02, FND-RS01, HEP-ENC-M01,
     M02, M04, M09, P02, P05, P06, S01, S02, S03, S04, S10, ISCH-STR-RP01, NMDAR-ENC-RS02, SAH-P04,
     SAH-RS12, SAH-S06, SE-P01, SE-S05): add "never delaying glucose for hypoglycaemia".
   - ALZ-EARLY templated performance status (24 cases).
8. **Guard suggestion**: per-case `rejected` labels must not name a comorbid contributor that the
   case's own musts or differential keep open (M05, M07, M08, S01 class).

## 5. Open questions

None for Andrea. Two worker-level checks are delegated with a rule:
- M01, M03 and P05: is the eating change described as new in the HPI? Apply the C7 rule.
- P03: keep the stored ECG values if plausible.

<!-- PLAN COMPLETE -->
