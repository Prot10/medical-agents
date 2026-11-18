# FTD: decisions of the November 2026 round (lead, 16 Nov 2026)

Base: commit 71517e55 (after class LIT 393c547e and MRI-CONTRAST 71517e55). 108 notes, all from R1
(NB-KSC3-TWUA-QDTM), 30 cases. No FTD case is approved (`work/approved.txt` lists none). The
measurements behind every class are in `plans/FTD.md` section 2. Scratch scripts are in
`/home/aprotani/review-round-2026-11/work/scratch/ftd-lead/`.

Scorer facts I checked before deciding (they decide several rulings):
- `policy_reward.py` lines 138-147: once the required set is done, only actions that match no
  criterion count as extra. Recommended and optional criteria (FDG-PET, genetics, P08 respiratory
  tests) are never penalised by `max_additional_actions: 0`. Every note that says the stop rule
  "terminates the pathway" before such a test rests on a wrong premise. The clinical point
  behind it is still acted on where the case needs it.
- `DiagnosisCriterion.matches` (`dxmatch_ftd.py`) already accepts in every bvFTD case: "bvFTD with
  definite FTLD pathology", "definite bvFTD", "possible bvFTD", "C9orf72-associated bvFTD",
  "GRN-associated bvFTD", "genetically confirmed familial bvFTD", "C9orf72-related FTD with
  parkinsonism". Through per-case `rejected` labels it vetoes: M05 "probable bvFTD with a possible
  contribution from lithium toxicity", M07 "probable bvFTD; possible Wernicke encephalopathy", M08
  "probable bvFTD with possible HAND contribution", and M10 "rtvFTD" and "right-sided semantic
  dementia". These per-case `rejected` lists are case data: `apply_diagnosis_synonyms.py` keeps
  labels that no yaml entry grants, so the case worker edits them.

## 1. LIT, literature search (48 notes, 30 cases)
Notes: every note whose comment is "no", "No", "NO", "nol" or "?" on a literature item (list in
FTD.md section 3). Decision: FIXED by class LIT, commit 393c547e. Checked on 16 Nov:
`survey_ftd.py` finds no `search_medical_literature` string, no literature criterion, follow-up,
initial or fallback output in any of the 30 cases. Workers re-check after editing and add nothing
back. The M05 "?" note (7e90367d) gets the same ruling, since the same item is the target. Reason:
ROUND_POLICY ruling 5 and the addendum.

## 2. DX-CERTAINTY (a): definite bvFTD when the optional panel is pathogenic
Notes: d1c4e3b7 (M02), 116ebe03 (P01), 8aa821c6 (P02), c0117e9b (P03), f3545383 (P04), f8fc0c33
(P05), 9ee3d9d6 (P07), 5040499f (S03), b94d7e75 (S05), b4a2044c (S07), 8b9672cf (S10).
Decision. `accepted[0]` stays "probable". R1 says to retain probable before genetic testing, and
October decision Q1 holds the same view: the label states what the required data support. The
scorer already accepts the higher-certainty and gene-specific answers, so nothing is needed in the
synonyms. The open defect is the musts, which allow only "(possible or probable)". Must 0 becomes
the canonical text C2 (FTD.md) in every case whose authored panel is pathogenic: M02, P03, P04,
P05, P07, P08, S03, S05, S07, S10. P01 and P02 already have it, so 116ebe03 and 8aa821c6 are
ALREADY-FIXED (must 0 says "definite if a pathogenic variant is found"). The S03, S05, S07 and S10
requests to "expand accepted diagnoses" are already met by the scorer, verified per label. The
ruling there is FIXED, for the must part. Citation: Rascovsky 2011 (definite bvFTD = clinical
criteria plus a known pathogenic mutation).

## 3. DX-CERTAINTY (b): possible bvFTD with a normal or equivocal MRI
Notes: ccb82f4f (P01), 7d0e7312 (P02), aa063460 (P05), 57e3f6ed (P07).
Decision. FDG-PET stays recommended in these four cases. October Q2 is confirmed: R1 asks that
possible bvFTD be accepted and that certainty be updated after PET, not that PET be made optional.
The scorer accepts "possible bvFTD". P01 and P02 must 0 already distinguish possible (normal MRI)
from probable (supportive PET) and definite, so both notes are ALREADY-FIXED. P05 and P07 get the
same must 0 (canonical C3). The stop-rule part of all four notes rests on a wrong premise (see the
scorer facts above): ruled ALREADY-FIXED, with that line quoted in the log. Citation: Rascovsky 2011
(probable needs imaging support); NICE NG97 1.2 (FDG-PET or perfusion SPECT when the subtype is
uncertain).

## 4. DX-CERTAINTY (g): mild FDG hypometabolism is non-specific
Notes: ad58e131 (P02), 4a526dcb (P05). Class: the FDG-PET and perfusion SPECT reports of the four
normal or equivocal MRI cases (P01, P02, P05, P07), whose impressions read "consistent with
frontotemporal lobar degeneration" with no qualifier.
Decision: FIXED. Keep the findings. End the impression with the hedged sentence of canonical C4.
The style guide allows one hedged alternative and "clinical correlation". Keep the recommended
tier. Citation: Ducharme S et al., Brain 2020;143:1632-1650: "abnormal non-specific regional
hypometabolism should not be over-interpreted in the case of a psychiatric differential
diagnosis"; when it is the only abnormal imaging, reconsider a psychiatric origin.

## 5. ALS gene panel served without motor neuron disease
Notes: 3fce79a8 (S03), cd3a3e1d (S05), 73ab2e96 (S10). Measured: an ALS panel follow-up is stored in
M02, P01, P04, P05, P07, P08, S03, S05 and S10. None is a criterion except in P08.
Decision: FIXED. Make it conditional rather than delete it.
- In P01, P04, P05, P07, S03, S05 and S10 (no MND signs, no relative with ALS), add the avoided
  action `order_specialized_test {test_type: genetic_panel:ALS}`, severity waste. Rationale: "No
  sign of motor neuron disease and the FTD panel already tests C9orf72; an ALS panel adds nothing
  to this work-up, and motor neuron disease is followed clinically."
- Keep the stored ALS report and move it to the end of `followup_outputs`. Deleting it would hand
  the order to the library's normal C9orf72 report, which contradicts the case. October item 9 and
  CENTRAL 4 are therefore not undone.
- M02 (brother died of ALS): add `genetic_panel:ALS` as a second alternative of the optional
  genetics criterion. A relative with ALS makes either panel a reasonable counselled first test.
  P08 already has it.
- The S05 request to "permit counselled genetic testing after diagnosis" is ALREADY-FIXED: the
  panel is optional and never extra.
Citation: Strong 2017 (ALS-FTSD needs clinical and EMG evidence; a genotype alone does not make
MND).

## 6. Templated performance-status report (class NEW:templated-performance-status)
Notes: 909dee2f (M06), 6fd2b279 (M10), baf51bf8 (P03), 15046dcf (P07). Measured: the same two
finding lines and "Karnofsky 70, ECOG 1" appear in 26 of 30 FTD cases. The exceptions are P08,
S09, S11 and S12.
Decision: FIXED in all 26. Rewrite each `order_performance_status` follow-up from that case's own
HPI and examination (canonical C6): what the history documents (work, finances, household,
self-care, supervision) and no capacity the history does not establish. Re-grade the scores to
match; where Karnofsky 70 does not fit, use 80 for intact self-care and work loss only. The same
kind of template exists in ALZ-EARLY (24 cases, "no longer able to manage finances, medications
or complex household tasks without help"); the ALZ lead is told.

## 7. Rascovsky features over-scored (class NEW:rascovsky-feature-overscored)
Notes: 5a6ec98f (M04), c9480a7a (P07), 43930018 (M06), 4612da84 (M09).
Rule (Rascovsky 2011). Feature E (hyperorality or dietary change) is present only when the history
documents a change from premorbid eating: altered food preference or food fads described as new,
sweet craving, binge eating, increased alcohol or cigarettes, or oral exploration. One behaviour
counts in one domain only, so a fixed meal routine that is part of the stereotypy is not also
counted as E. Feature F (executive-predominant profile) is a neuropsychological feature: at the
bedside it is "present" only when a screen was completed and shows executive failure with
relatively spared memory and visuospatial items. A feature is counted only on a persistent
behaviour, not a single equivocal act.
Applied:
- M04, P07 (notes), and M01 and M03 (same defect, measured): E is absent unless the HPI documents
  a new change. The worker reads the HPI; in M01, M03, M04 and P07 the only evidence is the fixed
  meal or snack routine. Recount 6 to 5 and correct `criteria_met`, scores, impression, expected
  evidence and must 0 lists. This reverses the October M01 "hyperorality true" change; R1's ruling
  and Rascovsky's own wording (one behaviour, new change) govern. P05 ("diet has narrowed to three
  specific foods"): keep E only if the HPI describes the narrowing as new since onset, otherwise
  apply the same rule. P08 keeps E (new preference for sweets).
- M09: the MoCA was not completed, so F is "not established at the bedside; to be confirmed by the
  battery". Count 5 of 6. The battery result already confirms it, so the diagnosis is unchanged.
- M06: disinhibition rests on one act (photographs given away) and empathy on "does not visibly
  grieve". Mark A "not established (a single impulsive act)" and C "not established at the
  bedside (blunted grief can reflect coping; social-cognition testing is the better measure)".
  Count 3 of 6: apathy (withdrawal from friends of 30 years), rigid routine, executive profile.
  That still meets possible bvFTD, probable with the MRI and functional decline, and definite with
  the known GRN variant, so the label's level is unchanged. Align must 1, differential 1, key
  evidence 2 and red herring 1, which cite "impulsive acts". The scenario note (SCENARIO class) is
  satisfied by this conservative scoring: the case now teaches that genetic status must not inflate
  the feature count. The HPI is not rewritten.

## 8. Abnormal lab rows with null clinical significance (REPORT-CONTRADICTION a)
Notes: 071a5363 (M03), 808af2e1 (M05), 94b68fbc (M07), 68b33e69 (P06). Measured: 38 abnormal FTD
rows have a null `clinical_significance` (listed in FTD.md section 2).
Decision: FIXED, with a CENTRAL display remark (CENTRAL.md item 1: null renders as "none").
- Fill `clinical_significance` with one short factual sentence that does not name the diagnosis,
  for every abnormal row that needs management or explains a finding: M03 and P06 glucose and
  HbA1c; P06 LDL and total cholesterol; M05 lithium; M07 ALT, AST, GGT, MCV and CDT; P01 ammonia;
  S01, S05 and S09 CDT; S01, S05 and S11 glucose and HbA1c; M01 HbA1c 6.1 (prediabetic range);
  P08 CK; M04 anti-TPO and anti-thyroglobulin (known Hashimoto thyroiditis); P03 CCP and RF (known
  rheumatoid arthritis); M06, P02 and S07 low progranulin (consistent with GRN haploinsufficiency).
- Check that each case has the must it needs. M03 must 2 already covers glycaemia and blood
  pressure. P06 must 2 already covers HbA1c, blood pressure and a statin. M07 gets the liver must
  (decision 14). M05 gets decision 9. S01 and S05 glucose: fold glycaemic review into the
  vascular or safety must only if the case has no such must; S05 HbA1c 7.4 on metformin needs a
  line.

## 9. M05 lithium (808af2e1)
Decision: FIXED.
- Lithium row significance: "Above the maintenance range; chronic lithium neurotoxicity can impair
  cognition even without tremor or ataxia."
- Must 1 becomes C9a. The level is corrected and lithium toxicity is not categorically excluded:
  it may contribute, but it does not explain a 16-month euthymic frontal syndrome with frontal
  atrophy. Must 2 adds: "reassess cognition and behaviour once the level is back in range."
- Remove "lithium toxicity" and "lithium neurotoxicity" from `rejected`, so that a qualified
  answer ("probable bvFTD; lithium neurotoxicity may contribute") scores. A bvFTD token is still
  required.
- Differential 1 key features: say "may contribute; does not explain the whole syndrome".
Citation: R1; NICE NG97 (reversible contributors); the October pack, section 1 (lithium is a
reversible mimic).

## 10. M05 stop rule (0367115d)
Decision: ALREADY-FIXED, plus CENTRAL display. The two lab criteria are distinct
(`action-4-interpret-labs` panels CBC...CRP, `action-lithium-level` panels [lithium_level]). Both
are in `required_before_assessment`, and the scorer matches each on its own `required_arguments`.
The review app shows only the tool name (CENTRAL.md item 3).

## 11. ECG with a patient-specific safety indication
Notes: baa96bf5 (M05), bf5a7b2b (P03). Measured across 600 cases: P03 is the only case whose ECG
is labelled waste while the patient takes 2 or more QT-prolonging drugs. M05 has coronary disease
and a lithium level above range.
Decision: FIXED.
- P03 (escitalopram 20 mg with hydroxychloroquine 400 mg): delete the ECG waste avoided action and
  add a `recommended` criterion `action-ecg-qtc` (`analyze_ecg`, no arguments), citation
  `[Escitalopram_SmPC]`. Move the ECG report from `fallback_tool_outputs.ecg` to
  `initial_tool_outputs.ecg`. Keep its values if they are plausible (QTc reported), place it after
  the diagnostic core, and add a must (canonical C11).
- M05: delete the ECG waste avoided action and add an `optional` criterion `action-ecg-safety`,
  with the ECG moved to the initial outputs in the same way. The ECG is not needed for the
  diagnosis, but it is justified for safety.
- ECG stays waste in the other 28 cases.
Citation: MHRA Drug Safety Update, Dec 2011 (updated Dec 2014), citalopram and escitalopram;
escitalopram SmPC section 4.3: contraindicated with medicines known to prolong the QT interval.

## 12. Drug-interaction reports that omit or overstate a warning
Notes: 2cce5786 (M04), 84873d7e (M05), 5869578c (P03).
Decision: FIXED with canonical C12.
- M04: replace "limit triptan use" with individual risk assessment and symptom counselling
  (Evans RW et al., AHS position paper, Headache 2010;50:1089-1099: the evidence does not support
  limiting triptans with SSRIs).
- M05: add the antidepressant-induced switch to mania or a mixed state in bipolar I, with
  psychiatry co-management and monitoring; lithium lowers but does not remove the risk (Yatham LN
  et al., CANMAT/ISBD 2018 bipolar guidelines, Bipolar Disord 2018;20:97-170).
- P03: escitalopram with hydroxychloroquine is a contraindicated QT combination (escitalopram
  SmPC 4.3; MHRA 2011/2014). It needs explicit medication review with the prescribers, an
  alternative where possible, and ECG with potassium and magnesium.
- No other FTD drug report needed the same fix. Measured: no other triptan; no other bipolar
  patient with an SSRI check, because P01's bipolar II has no SSRI check.

## 13. M06 "early corticobasal syndrome features" (f1f67b4e)
Decision: FIXED, as a label wording change (CENTRAL list).
- `accepted[0]` becomes "Behavioral variant frontotemporal dementia (bvFTD), definite (known
  pathogenic GRN variant), with possible early corticobasal-spectrum signs (mild right-hand
  apraxia and graphesthesia)". The ICD code is unchanged and the scoring is unchanged (generic
  labels).
- Must 2 becomes C13. Key evidence 3 is aligned.
- Mild ideomotor apraxia with agraphesthesia but no rigidity, akinesia, dystonia or myoclonus
  meets neither probable nor possible CBS (Armstrong MJ et al., Neurology 2013;80:496-503: possible
  CBS needs at least 1 motor and 1 cortical feature; probable CBS needs an asymmetric presentation
  with 2 of each).
- CBS is not added to `rejected` (an over-call is not vetoed, and no criterion rewards it).

## 14. M07 alcohol, family history and thiamine
Notes: eb9986c4, 51130a17, ce2fbd1b, 94b68fbc.
Decision: FIXED.
- Label (51130a17, eb9986c4): `accepted[0]` becomes "Behavioral variant frontotemporal dementia
  (bvFTD), probable (provisional until reassessment after abstinence and sleep apnoea treatment),
  with concurrent alcohol use disorder and alcohol-related cerebellar degeneration; family history
  suggestive but unconfirmed". "Sporadic" goes, because a mother with dementia from her late 50s
  and an uncle institutionalised in midlife do not support it. Code and scoring are unchanged.
  This is a label change (CENTRAL list).
- Must 0: the certainty clause becomes "probable, held provisionally: alcohol and untreated sleep
  apnoea can contribute to frontal deficits and atrophy; reassess after sustained abstinence and
  CPAP".
- Remove "wernicke" from `rejected`: the case's own must says two Caine criteria are met, so
  "possible Wernicke encephalopathy" is a correct qualifier. Keep "korsakoff" (normal mammillary
  bodies, preserved recognition memory) and "mania".
- Differential 1 stays moderate. Its wording becomes "may contribute; abstinence decides".
- Thiamine (ce2fbd1b), must 2, becomes canonical C14a: parenteral high-dose thiamine before or
  together with carbohydrate wherever feasible, never delaying glucose for hypoglycaemia.
  Citation: EFNS 2010 (Galvin R et al., Eur J Neurol 2010;17:1408-1418: 200 mg three times daily,
  preferably IV, before any carbohydrate) read with R1's hypoglycaemia caveat. The same "before
  any glucose" wording is in 21 cases of other conditions (FND, HEP-ENC, ISCH-STR, NMDAR-ENC, SAH,
  SE): flagged to their leads and in CENTRAL.
- Labs (94b68fbc): fill significance (decision 8) and add must C14b, alcohol-related liver injury
  assessment (NICE NG50: transient elastography for people who drink harmful amounts).

## 15. M08 HAND and CSF HIV RNA
Notes: 962d3cd1, bb11618e.
Decision: FIXED.
- Label: `accepted[0]` becomes "Behavioral variant frontotemporal dementia (bvFTD), probable, in a
  person with well-controlled HIV (CSF viral escape and opportunistic infection excluded;
  HIV-associated neurocognitive disorder unlikely)" (label change, CENTRAL list).
- Must 1: rewrite to C15. Differential 1: "unlikely; cannot be categorically excluded".
- Remove "HAND" and "HIV-associated neurocognitive disorder" from `rejected`. Keep "HIV-associated
  dementia", PML, cryptococcal and toxoplasmosis, which the MRI, CSF and CD4 count exclude.
- CSF tier (bb11618e): `action-8-analyze-csf` goes from required to recommended and leaves
  `required_before_assessment`. Keep the MRI-before-CSF soft constraint.
- This revises October Q4. EACS (12.0/13.0, neurocognitive impairment algorithm) puts CSF in the
  work-up of people "without obvious confounding conditions". Here the phenotype is a cortical
  frontal syndrome with frontal atrophy, which is itself a competing explanation, so the guideline
  does not clearly require LP. LP is still good practice, since CSF escape is treatable and is
  found in about 9% of symptomatic people (NAMACO/Neuro-HIV, JAIDS 2023). Recommended credits it;
  it no longer fails an agent that justifies omitting it.

## 16. M09 emergency CT and toxicology
Notes: 2dacb58f, 44fdd4b7.
Decision: FIXED. This revises October Q6 for M09; S06 is unchanged.
- CT (`action-4-order-ct-scan`) goes from required to optional (acceptable, never extra). Remove it
  from the stop rule and delete the CT-before-MRI soft constraint.
- Reason: the HPI excludes trauma, headache, focal signs, fever, seizures and sudden change, and
  the patient is alert and oriented. NICE NG97 1.2.10 asks for structural imaging, preferably MRI,
  without an emergency CT, and nothing in the case calls for a scan in the ED. MRI stays required.
- Toxicology (`action-tox-screen-blood-alcohol`) goes from required to recommended. The ED team
  raises intoxication, and the stolen item was cognac, so the test is good practice but not a
  scoring requirement.
- Must 1, key evidence 3 and differential 2: "negative" no longer "excludes". Use C16: the
  undetectable blood alcohol, the absence of a toxidrome and the 18-month course make
  intoxication very unlikely, and a urine immunoassay does not detect every substance.
- The worker probes which assay serves blood alcohol. `BAL` is bronchoalveolar lavage, and
  `lab_matching` maps "blood alcohol" to `ethanol`. If no orderable term returns the stored blood
  alcohol, that is a CENTRAL vocabulary request.

## 17. M10 right temporal variant and SSRI
Notes: d645ace0, 0102f4ac.
Decision: FIXED.
- Label: `accepted[0]` becomes "Right temporal variant frontotemporal dementia (rtvFTD), meeting
  probable behavioral variant FTD (bvFTD) criteria" (label change, CENTRAL list). Code G31.09 is
  unchanged. R1 rules the bvFTD-only classification incomplete; Ulugut Erkoyun 2020 defines rtvFTD
  (person-specific semantic loss with right anterior temporal atrophy).
- Remove "semantic dementia" from `rejected` and keep "svPPA" and "semantic variant primary
  progressive aphasia" (R1: classic svPPA is less appropriate).
- CENTRAL synonyms entry `G31.09+rtv` (cases [FTD-M10]): rtvFTD, right temporal variant FTD,
  right temporal variant frontotemporal dementia, right semantic dementia, right temporal
  semantic dementia.
- SSRI (0102f4ac): red herring 2 `correct_interpretation` becomes C17. Prohibition 1 becomes "Do
  not escalate antidepressant therapy for presumed depression in place of the dementia work-up"
  ("continue" goes). Must 4 already reviews the SSRI against the compulsive behaviour.

## 18. P01 valproate must (4a0fdd2d)
Decision: FIXED.
- Must 2 becomes C18, a qualified interpretation with no abrupt withdrawal. Ammonia gets its
  significance line (decision 8).
- Prohibition 4 becomes "Do not stop or switch valproate abruptly on account of a mildly raised
  ammonia alone".
- Keep "hyperammonaemic encephalopathy" in `rejected`: he has no encephalopathy (alert, insidious
  course), and the label does not veto a qualified "valproate neurotoxicity may contribute"
  answer (tokens checked).

## 19. P04 parkinsonism and DaTscan
Notes: de76c48a, 4473d085.
Decision: FIXED.
- Label: `accepted[0]` becomes "Behavioral variant frontotemporal dementia (bvFTD), probable, with
  levodopa-responsive parkinsonism (co-existing Parkinson's disease or FTD-associated
  parkinsonism)" (label change, CENTRAL list).
- Add a differential entry "C9orf72- or FTLD-associated parkinsonism (one process)" with
  likelihood moderate. Key features: asymmetric levodopa-responsive parkinsonism is reported with
  C9orf72; coincidental PD remains possible.
- Add a must 1 sentence: name both interpretations and that only genetics or follow-up separates
  them.
- Rewrite `metadata.notes` and the red herrings, which assert co-existing PD.
- DaTscan: delete the optional criterion `action-8-order-advanced-imaging` and add a waste avoided
  action `{modality: DaTscan}`. Rationale: the parkinsonism is clinically established and
  levodopa-responsive; DaT-SPECT is for tremor that cannot be separated from essential tremor
  (NICE NG71 1.2.6), and it cannot distinguish PD from C9orf72 parkinsonism. Keep the stored
  report at the end of the follow-ups.
- CENTRAL: the guidance text "P04 has one explicit optional DaTscan exception" and the pack
  section 2 line.

## 20. P08 respiratory stop rule (edc62f71)
Decision: ALREADY-FIXED. Respiratory function is a recommended criterion
(`action-4-order-specialized-test`, respiratory_function) and is never counted as extra. Must 4
already arranges FVC (upright and supine), SNIP and MIP with NIV referral (NICE NG42, AAN 2009).

## 21. Alcohol musts and contribution (S01 353235b4, S09 ade5774b; class)
Measured: current heavy or escalating drinking in M07, S01 (6-8 beers nightly), S05 (beer
throughout the day), S06 (4-6 beers daily), S09 (6 glasses of wine daily) and S10 (8-10 beers
daily). The musts say "limit access, involve his wife, support abstinence" (S01, S05), "supervised
reduction with her husband controlling access" (S09) or nothing (S06). S10 already has "medically
supervised reduction with withdrawal precautions".
Decision: FIXED.
- The alcohol must in S01, S05, S06 and S09 becomes canonical C21. Add to it where it exists, and
  add it to S06, whose must 1 only argues the drinking away. S10 is aligned to the same wording
  (minor). In M07 must 2 carries the addiction-services part.
- Differential: alcohol-related brain damage is "low as the sole cause; a contribution is not
  excluded".
- `rejected`: remove "alcohol-related brain damage" and "alcohol-related dementia" in S01, S05, S06,
  S09 and S10, so that a qualified answer scores. Keep "korsakoff" and "wernicke", which these
  cases do not support.
Citation: NICE CG115 (AUDIT; SADQ; assisted withdrawal usually needed at SADQ 15 or more, with a
benzodiazepine regimen); NICE CG100 1.2.1 (oral thiamine for harmful or dependent drinkers at
nutritional risk, parenteral when Wernicke is suspected). Escalating alcohol use is itself
Rascovsky feature E, which is why these cases attribute the drinking to bvFTD; that stays.

## 22. Head CT rationale (S01 5d57a74c, S02 143588da; class 27 cases)
Measured: 27 cases carry "CT lacks the resolution and lobar specificity". That is wrong, because
Rascovsky 2011 accepts CT atrophy as imaging support.
Decision: FIXED.
- Keep severity waste in the 27 cases where an MRI is available and required. CT is not
  "universally low-yield": it is redundant here.
- Replace the rationale with canonical C22. No CT criterion is added: MRI is available in every one
  of these cases.
- S06 keeps CT required (MRI declined). M09 follows decision 16.
Citation: NICE NG97; SNLG/ISS 2024 (CT when MRI is unavailable or contraindicated).

## 23. Perfusion MRI rationale naming amyloid PET (S07 832dd141; class 9 cases)
Measured: P03, P04, P05, P06, P07, S07, S08, S09 and S10 say "FDG-PET (or amyloid PET) have
characterised the lobar pattern".
Decision: FIXED. Replace with canonical C23 in all 9 cases. Citation: Frisoni 2024 (FDG-PET is the
neurodegeneration and pattern marker; amyloid PET answers the AD question).

## 24. S06 violence risk (80e972af)
Decision: FIXED. Must 2 is split. The firearm and violence-risk must (C24) is added and the safety
must keeps driving, finances and LPA. Citation: Betz ME et al., Ann Intern Med 2018;169:47-49
(firearm access assessment and restriction in dementia).

## 25. S11 earlier MRI asymmetry (8d60dcbe)
Decision: FIXED. Red herring 2 `correct_interpretation` and must 2 attribute the outside scan
tentatively (C25). The images are unavailable, so the earlier asymmetry "may have been early
atrophy". The current findings argue against encephalitis sequelae.

## 26. S12 DWI prohibition (acb7ab4d)
Decision: FIXED. Prohibition 0 becomes C26. The differential stroke entry stays low and cites the
same reasons, with no DWI prerequisite.

## 27. October decisions re-examined
- Revised: Q4 (M08 CSF required → recommended, decision 15); Q6 for M09 (CT required → optional,
  decision 16); the M01 hyperorality setting (decision 7); the "CT lacks resolution" rationale
  (decision 22); the P04 DaTscan optional exception (decision 19).
- Kept: Q1 (labels stay probable before genetics; decision 2); Q2 (FDG recommended in P01, P02,
  P05, P07; decision 3); ALS reports authored and served (decision 5); S06 CT required and MRI
  waste; Q5 PPA keys.

No NEEDS-ANDREA items: every point was decidable from the notes and the guidelines above.
