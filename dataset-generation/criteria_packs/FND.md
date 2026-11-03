# Criteria pack: Functional Neurological Disorder (FND)

**ICD-10-CM:** F44.4 (conversion disorder with motor symptom or deficit), F44.5 (with seizures or
convulsions), F44.6 (with sensory symptom or deficit), F44.7 (with mixed symptom presentation), F44.9
(unspecified). Per case, `icd_codes[0]` names the presentation: F44.5 for the three pure
functional-seizure cases (M04, M06, RP01), F44.4 for single-phenotype motor cases, F44.7 for mixed
presentations. Accepted labels and codes are scoped by phenotype in `diagnosis_synonyms.yaml` (24
Oct 2026): functional-seizure labels and F44.5 only in the 22 paroxysmal cases, motor labels and
F44.4/F44.6/F44.7 only where there is a motor deficit, "functional movement disorder" and
"functional tremor" only where a functional tremor is examined, and the diplopia case (RM02) its
own labels.
**Condition enum:** `NeurologicalCondition.FUNCTIONAL_NEUROLOGICAL_DISORDER`
**Case ID prefix:** `FND`

Updated 24 Oct 2026 to the October 2026 review round (`data/review/round-2026-10/plans/FND.md`,
`FND-summary.md`) and its close-out (`plans/FND-decisions.md`), which applied Andrea's ruling of the
same day: FND stays in the dataset (DLB is a deferred future swap) on the terms agreed with the
physicians in August 2026, **the examination of positive functional signs is the only required
diagnostic act, and all instrumental work is optional or, for a named red flag, recommended**.

---

## 1. Diagnostic criteria

DSM-5 functional neurological symptom disorder (conversion disorder) [DSM5_FND]: (A) one or more
symptoms of altered voluntary motor or sensory function; (B) clinical findings provide evidence of
incompatibility between the symptom and recognized neurological or medical conditions; (C) not
better explained by another disorder; (D) clinically significant distress or impairment, or
medical evaluation is warranted. A psychological stressor is neither required nor sufficient.

**FND is a rule-in diagnosis.** It rests on positive features [Espay_2018]. Normal tests do not make
it; abnormal tests do not exclude it, since FND commonly coexists with neurological disease (MS,
Parkinson's disease, epilepsy in these cases).

**Validated rule-in signs** [Daum_2014] (count only these in
`scores.positive_rule_in_signs_documented`): Hoover sign (hip extension; never applied to an arm or
hand), hip abductor sign, collapsing (give-way) weakness, drift without pronation, dragging
monoplegic gait, tremor entrainment, distractibility or variability, finger abduction sign,
co-contraction, convergence spasm with miosis. Hoover sign: sensitivity 63%, specificity 100% in
suspected stroke [McWhirter_2011]. "Upward drift" occurs with parietal and cerebellar lesions and is
not a functional sign.

**Supportive, low specificity, never counted:** midline splitting, splitting of vibration,
non-dermatomal sensory loss, la belle indifference, normal function when unobserved, "tubular"
fields not tested at two distances.

**Functional seizure semiology** [Avbersek_2010]: eyes closed and resisting opening, asynchronous or
waxing-waning movements, side-to-side head movement, pelvic thrusting, ictal crying, long duration,
preserved recall, rapid recovery without confusion. No single feature is diagnostic.

**Levels of certainty for functional seizures** [ILAE_PNES_2013]: possible (history and witness),
probable (event seen by a clinician or on video, with typical semiology), clinically established
(seen by an experienced clinician, with an EEG without ictal activity), documented (a habitual event
recorded on video-EEG without ictal change, with a typical history). The diagnosis can be made and
explained at the probable or clinically established level; video-EEG raises it to documented. A
routine interictal EEG records no events.

**Post-event prolactin** [Chen_2005]: a raised level 10-20 min after a generalized tonic-clonic or
focal impaired-awareness seizure supports an epileptic seizure; a normal level excludes nothing; a
dopamine antagonist (metoclopramide, risperidone) makes the level uninterpretable.

**Dual diagnosis:** about 22% of patients with functional seizures also have epilepsy
[Kutlubaev_2018]. After typical events without ictal change, "epileptic seizures" is `low` for those
events, not excluded.

**Misdiagnosis and delay:** about 4% of patients diagnosed with conversion symptoms later receive
another diagnosis [Stone_2005]; mean delay to a functional-seizure diagnosis about 7 years
[Reuber_2002]; prognosis of functional motor symptoms [Gelauff_2014]; epidemiology
[Carson_Lehn_2016].

## 2. Work-up hierarchy (as applied in the 30 cases, 24 Oct 2026)

> **Clinical tool review, July 2026, and the August 2026 agreement.** The physicians asked whether
> FND should be replaced by dementia with Lewy bodies, or kept with every diagnostic tool optional
> if the project also wants to measure diagnostic overuse. It is kept on those terms: the
> examination of positive functional signs is the only required diagnostic act; all instrumental
> work, video-EEG in paroxysmal cases included, is optional, and a test that answers a named red
> flag is recommended. The October 2026 round briefly required video-EEG in the 22 paroxysmal
> cases and the red-flag tests in three; the close-out reverted that (ruling of 24 Oct 2026).

**Required (30 of 30):**
- `perform_clinical_assessment` (`assessment_type: functional_neuro_signs`): the diagnostic act.
  It documents which sign was positive, not which disease was excluded, and in paroxysmal cases the
  semiology of an event when one is observed [Espay_2018] [Daum_2014] [DSM5_FND].

**Required as a management act (7 of 30):**
- `check_drug_interactions` in M02, RM03, RP01, RP03, RS01, RS02, S03: a drug started for the events
  is to be tapered (levetiracetam, carbamazepine, phenytoin, diazepam), or a drug on the list
  worsens the picture (RM03 desmopressin with polydipsia and sertraline; RS01 metoclopramide). The
  review is not a diagnostic act; it is required because management depends on it (ROUND_POLICY
  ruling 6). The physicians are asked to confirm this at re-review [Oto_2005]
  [AAN_Functional_Seizures_2025]. Recommended in 7 (benzodiazepine as needed, levetiracetam mood
  effects, risperidone, serotonergic clusters, ondansetron with low K and Mg), optional in 15.

**Recommended (a named red flag or alternative question):**
- `analyze_brain_mri`, once, in 12 cases: M09 with gadolinium (new deficit on natalizumab, JC virus
  index 2.8: relapse and PML) [McGuigan 2016]; P08 emergency imaging (MRI with DWI, or non-contrast
  CT as the alternative) in an acute hemiparesis within 3 hours [AHA_ASA_Stroke_2026]; without
  contrast in M03 (post-event deficit with word-finding difficulty), M05 (SLE, stroke mimic), P07 (new
  deficit on Parkinson's disease), RM02 (diplopia before convergence spasm is accepted), RP03 and RS02
  (EGPA, CNS vasculitis question), RS04, S05, S06 and S10 (stroke or demyelination mimic).
- `order_body_imaging` (`study: spine_MRI`) in S07 (acute paraplegia).
- `interpret_labs`, named assays, in 8 cases: P08 glucose first (acute deficit 3 h after an
  insulin bolus); RM01 sodium and osmolality (polydipsia, prior hyponatremic seizure); RM03 sodium
  and serum and urine osmolality; RP02 and RS01 CMP, magnesium, phosphate, thiamine (malnutrition,
  vomiting); S09 CMP, magnesium, thiamine (daily alcohol); M05 antiphospholipid, complement, anti-dsDNA
  (SLE); RP03 CBC, ESR, CRP (EGPA).

**Optional (justified, uncredited):**
- `analyze_eeg` (`eeg_type: video`) in the 22 paroxysmal cases (M01, M02, M03, M04, M06, P01, RM01,
  RM03, RP01, RP03, RS01, RS02, RS03, RS04, S01, S02, S03, S04, S05, S06, S09, S11). A habitual
  event recorded without ictal change reaches the documented level and screens for co-occurring
  epilepsy; without it, the positive signs and the semiology of witnessed events support the
  diagnosis at a lower level [ILAE_PNES_2013] [AAN_Functional_Seizures_2025]. Video-EEG is most
  informative where the semiology is atypical (S05 eyes open), where epilepsy is established (M06),
  where the events mimic absences (M04), and before withdrawing long-standing antiseizure drugs
  (RP01, RP03, RS02, M02, S03); the taper musts say so.
- `analyze_brain_mri` without contrast in 9 (M01, M02, RS03, S01, S02, S03, S04, S07, S09) and spine
  MRI in M09.
- `interpret_labs` in 4 (M01, M02, M03, M09).
- `analyze_ecg` in 10: P08 and RM01 (QT on the medicines), and M01, M02, M04, S01, S05, S06, S09,
  S11, whose events are apparent unresponsiveness, for which NICE advises a 12-lead ECG after
  transient loss of consciousness [NICE_CG109] and after a suspected seizure [NICE_NG217].
- `order_ct_scan` (`angiography: true`) in P08 (acute stroke pathway).
- `order_specialized_test` (`test_type: neuropsych_battery`) in all 30: quantifies the comorbidity
  that treatment targets; it does not make the diagnosis and is the most expensive item.
- `search_medical_literature` in all 30, last, never a clinical step (ROUND_POLICY ruling 5).

**Stop rule:** `required_before_assessment` is the examination, plus the drug check in the seven
cases above; `max_additional_actions` 0. Recommended and optional criteria are justified and do not
count against stopping; overuse is the construct.

## 3. Tools that are typically USELESS (waste avoided actions)

- `order_specialized_test` `emg_ncs` and `ssep` (30): the deficit is not neuromuscular or a
  somatosensory-pathway lesion, and a normal result reinforces the search for an organic cause
  [Stone_2016].
- `order_advanced_imaging` `FDG_PET` (29); `DaTscan` in P07 (Parkinson's disease is established).
- `order_ct_scan` (29, not P08): MRI is the study when imaging has a question.
- `analyze_csf` (23), `order_echocardiogram` (28), `order_cardiac_monitoring` (29).
- `analyze_ecg` (9: M05, M06, M09, P07, S02, S03, S04, S07, S10) where nothing raises a cardiac
  question: no transient loss of consciousness (awareness retained, or no events), no palpitations,
  no QT-relevant drug at a relevant dose.
- Repeat studies after a normal prior study: brain MRI in P01, spine MRI in P01, RP02, RS01.
- Each rationale is specific to the patient and cites `[Espay_2018]` or `[Stone_2016]`. In FND the
  iatrogenic harm is usually the second and third investigation, not the first [Stone_2016].

## 4. Harmful or contraindicated management (prohibitions, not tool calls)

- Telling the patient the symptoms are imagined, feigned or "all in your head".
- Starting or escalating antiseizure medication for functional seizures; stopping a long-term
  antiseizure drug or benzodiazepine abruptly (taper one drug at a time under supervision)
  [Oto_2005] [AAN_Functional_Seizures_2025].
- Emergency benzodiazepines or intubation for a typical functional seizure.
- Invasive testing without a specific indication; gadolinium without a specific indication.
- Case-specific: haloperidol after a dystonic reaction (RM01), continuing desmopressin (RM03) or
  metoclopramide (RS01), glucose before thiamine in malnutrition (RP02, RS01), steroids for a
  presumed MS relapse (M09), raising dopaminergic drugs for a functional tremor (P07), strabismus
  surgery for convergence spasm (RM02).

## 5. Sequence constraints (all soft)

- Examination before MRI (or spine MRI) where the imaging is recommended, except P08: its positive
  signs decide whether imaging has a specific question to answer [Espay_2018].
- P08: fingerstick glucose before emergency imaging in an acute deficit on insulin.
- No constraint names an optional criterion (video-EEG, optional imaging or labs, neuropsychology,
  literature). The October 2026 constraints "video-EEG before the drug check" (M02, RP01, RP03, RS02,
  S03) and "sodium before video-EEG" (RM01) were removed with the ruling.

## 6. Subtype variations

- **Motor or sensory only** (M05, M09, P07, P08, RM02, RP02, S07, S10): the examination, plus the
  case's red-flag test as recommended.
- **Paroxysmal** (the other 22): the examination with the event semiology; video-EEG optional.
- **Taper** (M02, RP01, RP03, RS02, S03): the drug check is required, the taper must (M-ASM) names
  the drugs and conditions the taper on a secure diagnosis, ideally documented on video-EEG, and the
  prohibition adds "or stop it abruptly".
- **Established epilepsy** (M06): continue levetiracetam, do not escalate for the new events,
  rescue medication only for events with his known epileptic semiology.
- **R series** (RM, RP, RS): record-derived cases. Every R case is labelled FND; the "R" marks the
  source, not a reversed diagnosis. Never relabel an R case as a mimic.

## 7. Common red-herring categories

- **Psychiatric history**: neither establishes nor refutes FND; it is a treatment target.
- **Stressor**: supportive context, neither required nor sufficient.
- **Family history of epilepsy or MS**: only where the case's family history contains it.
- **An outside label** (psychogenic seizures, epilepsy): re-examined on positive evidence.
- **An external incentive** (licence, disability claim, medical leave): does not show feigning, and
  examination signs cannot separate feigning from FND (M06, M09, S09 only).
- **Coexisting neurological disease** (MS, PD, epilepsy, EGPA, SLE): FND coexists with it.

## 8. Musts (canonical, per plan section 2.D)

M-DX (positive diagnosis on the case's signs and, for events, their semiology, with video-EEG
confirmation where recorded; not by exclusion), M-COMM (explain the diagnosis, show the positive
signs, written information, family with consent), M-PHYSIO (motor phenotype; [Nielsen_2015]
consensus; trial evidence [Nielsen_2024]), M-PSY (functional seizures or a psychiatric target;
CBT-informed, [Goldstein_2020]), M-ASM (taper cases), M-EPI (M06), M-RESCUE (paroxysmal), plus
case-specific musts. Trial facts, stated exactly: CODES did not reduce dissociative-seizure
frequency at 12 months against standardised care alone, with several secondary outcomes favouring
CBT; Physio4FMD was not superior on SF-36 physical function at 12 months, with several secondary
outcomes favouring specialist physiotherapy. Neither reports an NNT.

## 9. Allowed citations

- `[Espay_2018]`: Espay AJ, Aybek S, Carson A, et al. Current concepts in diagnosis and treatment of
  functional neurological disorders. JAMA Neurol 2018;75(9):1132-1141
- `[Stone_2016]`: Stone J. Functional neurological disorders: the neurological assessment as
  treatment. Pract Neurol 2016;16(1):7-17 (assessment as treatment, iatrogenic harm)
- `[Daum_2014]`: Daum C, Hubschmid M, Aybek S. The value of 'positive' clinical signs for weakness,
  sensory and gait disorders in conversion disorder: a systematic and narrative review. J Neurol
  Neurosurg Psychiatry 2014;85(2):180-190
- `[McWhirter_2011]`: McWhirter L, Stone J, Sandercock P, Whiteley W. Hoover's sign for the
  diagnosis of functional weakness: a prospective unblinded cohort study in patients with suspected
  stroke. J Psychosom Res 2011;71(6):384-386
- `[DSM5_FND]`: American Psychiatric Association. Diagnostic and Statistical Manual of Mental
  Disorders, 5th ed. Functional neurological symptom disorder (conversion disorder). 2013 (criteria
  unchanged in DSM-5-TR, 2022)
- `[ILAE_PNES_2013]`: LaFrance WC Jr, Baker GA, Duncan R, Goldstein LH, Reuber M. Minimum
  requirements for the diagnosis of psychogenic nonepileptic seizures: a staged approach. A report
  from the ILAE Nonepileptic Seizures Task Force. Epilepsia 2013;54(11):2005-2018
- `[AAN_Functional_Seizures_2025]`: Tolchin B, Goldstein LH, Reuber M, et al. Management of
  functional seizures: practice guideline executive summary, report of the AAN Guidelines
  Subcommittee (endorsed by the AES and the FND Society). Neurology 2026;106(1):e214466, doi
  10.1212/WNL.0000000000214466 (online December 2025). Never cited for "positive FND signs"
- `[Avbersek_2010]`: Avbersek A, Sisodiya S. Does the primary literature provide support for
  clinical signs used to distinguish psychogenic nonepileptic seizures from epileptic seizures? J
  Neurol Neurosurg Psychiatry 2010;81(7):719-725
- `[Chen_2005]`: Chen DK, So YT, Fisher RS. Use of serum prolactin in diagnosing epileptic seizures:
  report of the Therapeutics and Technology Assessment Subcommittee of the AAN. Neurology
  2005;65(5):668-675
- `[Kutlubaev_2018]`: Kutlubaev MA, Xu Y, Hackett ML, Stone J. Dual diagnosis of epilepsy and
  psychogenic nonepileptic seizures: systematic review and meta-analysis of frequency, correlates,
  and outcomes. Epilepsy Behav 2018;89:70-78
- `[Oto_2005]`: Oto M, Espie C, Pelosi A, Selkirk M, Duncan R. The safety of antiepileptic drug
  withdrawal in patients with non-epileptic seizures. J Neurol Neurosurg Psychiatry
  2005;76(12):1682-1685
- `[Nielsen_2015]`: Nielsen G, Stone J, Matthews A, et al. Physiotherapy for functional motor
  disorders: a consensus recommendation. J Neurol Neurosurg Psychiatry 2015;86(10):1113-1119
- `[Nielsen_2024]`: Nielsen G, Stone J, Lee TC, et al. Specialist physiotherapy for functional motor
  disorder in England and Scotland (Physio4FMD): a pragmatic, multicentre, phase 3 randomised
  controlled trial. Lancet Neurol 2024;23(7):675-686
- `[Goldstein_2020]`: Goldstein LH, Robinson EJ, Mellers JDC, et al. Cognitive behavioural therapy
  for adults with dissociative seizures (CODES): a pragmatic, multicentre, randomised controlled
  trial. Lancet Psychiatry 2020;7(6):491-505
- `[Stone_2005]`: Stone J, Smyth R, Carson A, et al. Systematic review of misdiagnosis of conversion
  symptoms and "hysteria". BMJ 2005;331(7523):989
- `[Reuber_2002]`: Reuber M, Fernandez G, Bauer J, Helmstaedter C, Elger CE. Diagnostic delay in
  psychogenic nonepileptic seizures. Neurology 2002;58(3):493-495
- `[Gelauff_2014]`: Gelauff J, Stone J, Edwards M, Carson A. The prognosis of functional
  (psychogenic) motor symptoms: a systematic review. J Neurol Neurosurg Psychiatry
  2014;85(2):220-226
- `[Carson_Lehn_2016]`: Carson A, Lehn A. Epidemiology. Handb Clin Neurol 2016;139:47-60
  (epidemiology only)
- `[NICE_CG109]`: NICE clinical guideline CG109. Transient loss of consciousness ('blackouts') in
  over 16s. 2010, recommendation 1.1.2.2: record a 12-lead ECG with automated interpretation in
  everyone with transient loss of consciousness
- `[NICE_NG217]`: NICE guideline NG217. Epilepsies in children, young people and adults. 2022
- `[AHA_ASA_Stroke_2026]`: Prabhakaran S, Gonzalez NR, Zachrison KS, et al. AHA/ASA guideline for
  the early management of patients with acute ischemic stroke. Stroke 2026 (P08: glucose before
  imaging, emergency imaging of an acute deficit)

Free-text sources cited by name in single cases (no key): McGuigan C, Craner M, Guadagno J, et al.
Stratification and monitoring of natalizumab-associated progressive multifocal leukoencephalopathy
risk: recommendations from an expert group. J Neurol Neurosurg Psychiatry 2016;87(2):117-125 (M09);
Spasovski G, Vanholder R, Allolio B, et al. Clinical practice guideline on diagnosis and treatment
of hyponatraemia. Eur J Endocrinol 2014;170(3):G1-G47, and the desmopressin SmPC (RM03); NICE
clinical guideline CG32, Nutrition support for adults (2006, updated 2017), and the ondansetron SmPC
(RP02); the metoclopramide SmPC and the EMA 2013 restriction of metoclopramide to short-term use
(RS01). Literature outputs may also cite Aybek S, Perez DL. BMJ 2022;376:o64 and Hallett M et al.
Lancet Neurol 2022;21:537-550 by name.

**Superseded keys (do not use):**
- `[Stone_2018]`: does not exist as cited (Pract Neurol 2018;18:267-278 is not this paper); use
  `[Espay_2018]`, or `[Stone_2016]` for assessment as treatment and iatrogenic harm.
- `[Carson_2012]`: misnamed; the text is Carson and Lehn 2016, now `[Carson_Lehn_2016]`.
