# FND: condition plan for the October 2026 review round

Lead plan for the 30 `functional_neurological_disorder` cases: M01..M06, M09, P01, P07, P08,
RM01..RM03, RP01..RP03, RS01..RS04, S01..S07, S09..S11. Read `ROUND_POLICY.md`, `PATTERNS.md`,
`dataset-generation/TOOL_REPORT_STYLE_GUIDE.md`, `docs/benchmark/tool-contract.md` and
`dataset-generation/criteria_packs/FND.md` first; this plan does not repeat them.

No reviewer notes exist for FND (`notes/FND.md` and `notes/FND.json` are absent). The physician
input is the July 2026 guidance for `functional_neurological_disorder` in
`agent-platform/config/review/condition_tool_guidance.yaml` (1.3). All findings come from the
lead's survey. Each log's "Reviewer notes" section says "No reviewer notes for this case".

**Baseline (24 Oct 2026, before any edit).**
- `perfect_agent.py` passes 30/30.
- The leak guard fails M09, P08, S05, S06 and S10: the initial literature summary is the
  `expected_evidence` "Confirms multidisciplinary CBT + physiotherapy is the evidence-based
  treatment for FND".
- No case has a sequence constraint.
- Every stop rule is `[action-3-perform-clinical-assessment]` with `max_additional_actions: 0`.
- Every instrumental criterion is `optional`.

The pack (section 2, rewritten 2026-08-06) already requires video-EEG where the phenotype is
paroxysmal, and recommends MRI, labs and the drug check on named questions. The cases were never
brought into line with it. This plan implements the pack's tiers, with the case corrections of
sections 3 and 4.

**Use.**
1. Apply the classes of section 2 that name your case (canonical text verbatim, `<...>` filled),
   then the decisions of section 4.
2. Rebuild criteria, follow-up order, constraints and stop rule per section 3.
3. Run `uv run python data/review/round-2026-10/bin/perfect_agent.py CASE -v`,
   `uv run python data/review/round-2026-10/bin/case_io.py check CASE` and
   `uv run pytest agent-platform/tests/test_case_guards.py -q -k CASE`.
4. Write `logs/{CASE_ID}.md`.

Edit only through `case_io` load/save.

New text is in English with the cases' American spelling (hyponatremia, anemia, behavior), with no
em or en dashes. New values fit the patient's age, sex, weight and medicines, and differ from the
shared template values.

---

## 1. Governing guidelines and canonical facts

### 1.1 Which source governs what

All sources were checked and exist. Keys marked (C) are new; they may be used now (no test checks
keys), and section 5 asks for them in the pack.

| question | source | key |
| --- | --- | --- |
| Positive diagnosis, signs, model of care | Espay AJ et al. JAMA Neurol 2018;75:1132-1141; DSM-5 criterion B | `[Espay_2018]`, `[DSM5_FND]` |
| Assessment as treatment, iatrogenic harm | Stone J. Pract Neurol 2016;16:7-17 | `[Stone_2016]` (C) |
| Validity of motor and sensory signs | Daum C, Hubschmid M, Aybek S. JNNP 2014;85:180-190 | `[Daum_2014]` (C) |
| Hoover sign: sensitivity 63%, specificity 100% in suspected stroke | McWhirter L et al. J Psychosom Res 2011;71:384-386 | `[McWhirter_2011]` (C) |
| Levels of certainty for functional seizures | LaFrance WC Jr et al. (ILAE) Epilepsia 2013;54:2005-2018 | `[ILAE_PNES_2013]` |
| Evaluation and management of functional seizures | Tolchin B, Goldstein LH, Reuber M et al. AAN guideline, Neurology 2026;106(1):e214466 (online 10 Dec 2025; endorsed by AES and FNDS) | `[AAN_Functional_Seizures_2025]` (existing; never cite it for "positive FND signs") |
| Semiology of functional vs epileptic seizures | Avbersek A, Sisodiya SM. JNNP 2010;81:719-725 | `[Avbersek_2010]` (C) |
| Post-event prolactin | Chen DK, So YT, Fisher RS. Neurology 2005;65:668-675 | `[Chen_2005]` (C) |
| Dual diagnosis with epilepsy | Kutlubaev MA et al. Epilepsy Behav 2018;89:70-78 | `[Kutlubaev_2018]` (C) |
| Antiseizure drug withdrawal | Oto M et al. JNNP 2005;76:1682-1685; AAN 2025 | `[Oto_2005]` (C) |
| Physiotherapy | Nielsen G et al. JNNP 2015;86:1113-1119 (consensus); Physio4FMD, Nielsen G et al. Lancet Neurol 2024;23:675-686 | `[Nielsen_2015]`, `[Nielsen_2024]` (C) |
| CBT for dissociative seizures | CODES, Goldstein LH et al. Lancet Psychiatry 2020;7:491-505 | `[Goldstein_2020]` (C) |
| Misdiagnosis, delay, prognosis | Stone J et al. BMJ 2005;331:989; Reuber M et al. Neurology 2002;58:493-495; Gelauff J et al. JNNP 2014;85:220-226 | `[Stone_2005]`, `[Reuber_2002]`, `[Gelauff_2014]` (C) |
| Reviews (literature outputs only) | Aybek S, Perez DL. BMJ 2022;376:o64; Hallett M et al. Lancet Neurol 2022;21:537-550 | none |

Two pack keys need correcting:
- `[Stone_2018]` does not exist (Pract Neurol 2018;18:267-278 is not this paper). Replace it with
  `[Espay_2018]`, or with `[Stone_2016]` for claims about the assessment as treatment or iatrogenic
  harm.
- `[Carson_2012]` is misnamed: the text is Carson and Lehn, Handb Clin Neurol 2016;139:47-60
  (epidemiology). Use it for epidemiology only.

A citation without a key is written "Author, Journal Year;vol:pages".

### 1.2 Canonical clinical facts (use these; do not restate them differently)

1. **FND is a rule-in diagnosis.** It rests on positive features incompatible with recognised
   disease (DSM-5 criterion B). A stressor is neither required nor sufficient. Normal tests do not
   make the diagnosis; abnormal tests do not exclude it.
2. **Validated rule-in signs (Daum 2014).**
   - The signs: Hoover sign, hip abductor sign, collapsing (give-way) weakness, drift without
     pronation, dragging monoplegic gait, tremor entrainment, distractibility or variability,
     finger abduction sign, co-contraction, convergence spasm with miosis.
   - Count only these in `scores.positive_rule_in_signs_documented`.
   - Hoover tests hip extension and never applies to an arm or hand; for hand weakness use the
     finger abduction sign or collapsing weakness.
   - "Upward drift" occurs with parietal and cerebellar lesions and is not a functional sign.
3. **Signs of low specificity are supportive and never counted:** midline splitting, splitting of
   vibration, non-dermatomal sensory loss, la belle indifference, normal function when unobserved,
   and "tubular" fields not formally tested at two distances.
4. **Functional seizure semiology (Avbersek 2010).** Supporting features: eyes closed and
   resisting opening, asynchronous or waxing-waning movements, side-to-side head movement, pelvic
   thrusting, ictal crying, long duration, preserved recall, rapid recovery without confusion. No
   single feature is diagnostic.
5. **ILAE 2013 levels.**
   - Documented: a habitual event recorded on video-EEG without ictal change, interpreted by an
     experienced clinician, with a typical history.
   - Clinically established: the event is seen or reviewed on video, with a routine EEG.
   - A routine interictal EEG records no events.
6. **Post-event prolactin (Chen 2005).** A raised level 10-20 min after a generalized tonic-clonic
   or focal impaired-awareness seizure supports an epileptic seizure; a normal level excludes
   nothing. Lab `clinical_significance` must not claim more.
7. **AAN 2025 (Tolchin) guideline:**
   - detailed history with witness accounts and videos;
   - video-EEG may confirm;
   - evaluate co-occurring epilepsy and psychiatric disorders;
   - taper antiseizure drugs with no other indication;
   - no benzodiazepines without epilepsy or another indication;
   - psychological therapy is possibly effective;
   - clear, empathetic delivery of the diagnosis, involving the family.
8. **Dual diagnosis.** About 22% of patients with functional seizures also have epilepsy
   (Kutlubaev 2018). After a normal video-EEG with captured habitual events, "epileptic seizures"
   is `low` for those events, not excluded. In M06 the epilepsy is established.
9. **Withdrawal.** Supervised withdrawal of antiseizure drugs started for functional events is safe
   (Oto 2005). Long-term benzodiazepines are tapered over weeks; abrupt stopping can provoke
   seizures.
10. **The trials, stated exactly.** Neither trial reports an NNT; never write "NNT 5.7" or
    "moderate effect sizes for seizure reduction".
    - CODES: CBT plus standardised care did not reduce dissociative-seizure frequency at 12 months
      against standardised care alone; several secondary outcomes favoured CBT.
    - Physio4FMD: specialist physiotherapy was not superior to community neurological physiotherapy
      on SF-36 physical function at 12 months; several secondary outcomes favoured it.
11. **Misdiagnosis and delay.** About 4% of patients diagnosed with conversion symptoms since 1970
    later received another diagnosis (Stone 2005). The mean delay to a functional-seizure diagnosis
    is about 7 years (Reuber 2002).
12. **Iatrogenic harm.** Repeated negative investigation and unneeded treatment are the main
    iatrogenic harms (Stone 2016; Espay 2018).
13. **Imaging.**
    - Non-contrast brain MRI with DWI answers the stroke-mimic and demyelination questions.
    - Gadolinium only when enhancement is the question: MS on a disease-modifying drug, PML, tumor,
      inflammation.
    - Spine MRI is `order_body_imaging` `spine_MRI` and MRA is `order_advanced_imaging`; neither is
      bundled into `analyze_brain_mri`.
14. **Glucose first.** In an acute focal deficit on insulin, the fingerstick glucose comes before
    imaging.
15. **Thiamine before glucose** in malnutrition with vomiting, with refeeding monitoring of
    phosphate, potassium and magnesium.
16. **Interactions present in these cases:**
    - Benzodiazepine PRN: rescue use reinforces the epileptic model and sedates; taper it.
    - SSRI or SNRI with a triptan, cyclobenzaprine or duloxetine: serotonergic.
    - SSRI or SNRI with an NSAID: GI bleeding.
    - Sertraline with desmopressin in polydipsia with hyponatremia: severe hyponatremia risk; stop
      desmopressin.
    - Metoclopramide: a dopamine antagonist. Dystonia, akathisia and parkinsonism mimic or confound
      movements, and it prolongs QT with hypomagnesemia; stop it.
    - Ondansetron with low K and Mg: QT prolongation.
    - Risperidone: small dose-related lowering of the seizure threshold.
    - Carbamazepine with phenytoin: mutual induction. Sertraline raises phenytoin; carbamazepine
      causes hyponatremia; taper one drug at a time.
    - Levetiracetam: irritability, low mood and anxiety.

### 1.3 July 2026 physician guidance

Reviewer 1: "DISCUTERE SE TENERE PATOLOGIA, SE VOGLIAMO CONTROLLARE SE L'AGENTE AI FA OVERTESTING"
(discuss whether to keep the condition, if we want to check whether the AI agent over-tests). The
recorded response keeps FND to measure overuse, and adds DLB regardless.

This plan honours that response:
- The only universal required act is the examination.
- Every waste avoided action stays.
- Required instrumental work is limited to the pack's paroxysmal video-EEG and to named red flags:
  P08 glucose and imaging, RM01 sodium, M09 MRI on natalizumab.

The response's "every instrumental action is optional" and its counts "MRI in 20, labs in 12" are
stale (CENTRAL 4).

---

## 2. Error classes in this condition

No note ids exist. Where a case differs, section 4 is authoritative.

### A. Template criteria and tiers (all 30)

**Problem.**
- The criteria are stamped from one template: literature `recommended`, drug check `recommended`
  `{}`, exam `required`, and MRI, video-EEG and labs `optional`.
- Labels equal rationales. The MRI label reads "Consider MRI only for the explicit first focal
  deficit...".
- 84 citations read "positive FND signs; AAN functional seizures guideline 2025".

**Fix.**
- Rebuild per section 3.
- The label is a short imperative. The rationale says why for this patient, with its source; the
  two differ.
- Citations name the source of the claim; drop the "FND criteria pack - ..." strings.
- `expected_evidence` states the case's own result, worded differently from every stored output.

### B. Literature outputs: scoring key and fabrication (all; leak guard fails M09, P08, S05, S06, S10)

**Problem.**
- The initial summary is the `expected_evidence`.
- Follow-ups invent results: CODES "reduces seizure frequency"; M02 "NNT 5.7 in JAMA Psychiatry".
- They misattribute titles:
  - "Espay ... BMJ 2018" is Aybek and Perez, BMJ 2022.
  - "Espay ... Lancet Neurol 2018;17:84-98, new subtypes and shared mechanisms" is Hallett et al.,
    Lancet Neurol 2022.
- They reuse PMIDs 26276867 and 30503873.
- M04, M05, M06, P07 and S09 are empty stubs.
- Six disguise clinical acts (ruling 4): `palliative_care_referral_husband` (P07),
  `rheumatology_consultation_sle` (M05), `review_prior_negative_workup` (S11),
  `family_meeting_fnd_education` (S07), `va_fnd_ptsd_documentation` (S09),
  `patient_education_fnd_pnes` (M04).

**Fix.**
- Delete every literature follow-up; clinical content becomes a must (a family meeting becomes
  M-COMM).
- Keep one `initial_tool_outputs.literature_search`, keyed by the criterion query, with this
  canonical content. Motor-only cases may drop the LaFrance and Goldstein rows.

```
query: "functional neurological disorder diagnosis treatment"
results:
- {source: "Espay AJ et al. JAMA Neurol 2018;75:1132-1141", evidence_level: "narrative review",
   finding: "Diagnosis of functional neurological disorder rests on positive clinical features such as the Hoover sign, tremor entrainment and functional seizure semiology, not on the exclusion of other disease; treatment combines explanation, physiotherapy and psychological therapy."}
- {source: "Daum C et al. J Neurol Neurosurg Psychiatry 2014;85:180-190", evidence_level: "systematic review",
   finding: "Motor signs such as the Hoover sign, hip abductor sign, drift without pronation and dragging gait have high specificity; sensory signs such as midline splitting have low specificity."}
- {source: "LaFrance WC Jr et al. Epilepsia 2013;54:2005-2018", evidence_level: "ILAE consensus",
   finding: "Defines levels of certainty for psychogenic nonepileptic seizures; the documented level requires a typical event recorded on video-EEG without ictal EEG change."}
- {source: "Tolchin B et al. Neurology 2026;106:e214466", evidence_level: "AAN evidence-based guideline",
   finding: "For functional seizures: assess for co-occurring epilepsy and psychiatric disorders, taper antiseizure medication without another indication, avoid benzodiazepines, and offer psychological therapy, which is possibly effective."}
- {source: "Goldstein LH et al. Lancet Psychiatry 2020;7:491-505", evidence_level: "randomised controlled trial",
   finding: "CBT added to standardised medical care did not reduce dissociative seizure frequency at 12 months; several secondary outcomes favoured CBT."}
- {source: "Nielsen G et al. Lancet Neurol 2024;23:675-686", evidence_level: "randomised controlled trial",
   finding: "Specialist physiotherapy for functional motor disorder was not superior to community neurological physiotherapy on physical function at 12 months; several secondary outcomes favoured it."}
- {source: "Stone J et al. BMJ 2005;331:989", evidence_level: "systematic review",
   finding: "About 4% of patients diagnosed with conversion symptoms since 1970 later received another diagnosis."}
summary: "Guideline and trial evidence supports a positive clinical diagnosis of functional neurological disorder, video-EEG confirmation of functional seizures, tapering of unneeded antiseizure drugs and benzodiazepines, and physiotherapy and psychological treatment whose trial effects on primary outcomes were modest."
```

The summary must not equal any `expected_evidence` (any-query rule). Null the literature fallback.

### C. Drug-check outputs empty or a plan (all)

**Problem.**
- Initial outputs only list the medicines, with the leak warning "...is a prescribing decision,
  not an output of this check".
- Follow-ups are plans: "Sertraline 150 mg (dose increase)" (S01, S02, S04), naltrexone (S09),
  CGM education (P08), natalizumab options (M09), "Consider adding SSRI" (M06), sertraline for
  RS01 and RP02, who do not take it.
- Cross-modality text: RS04 cites a QTc of 418 ms with no ECG; RM03 cites urine osmolality.
- Real interactions are missed (fact 16): benzodiazepine PRN (M01, M02, M09, S03, S04, RS04,
  RP01); triptan with SSRI or SNRI (M03, M04, P01, RM02, RS03, S06); M02 cyclobenzaprine; RM03
  desmopressin; RS01 metoclopramide; RP02 ondansetron; RP01 carbamazepine with phenytoin.

**Fix.** One `initial_tool_outputs.drug_interactions` in `DrugInteractionResult` fields:
- `proposed`: the medicines, verbatim from `patient.clinical_history.medications`.
- `interactions`: each fact-16 pair that applies, with its mechanism.
- `contraindications`: a relevant allergy (RP01 sulfonamide: no sulfonamide anticonvulsant).
- `warnings`: drug cautions.
- `summary`: one sentence in report voice.

No dose, start, increase or other modality. Without a relevant interaction, the output says "No
clinically significant interactions among the current medicines". Delete plan follow-ups after
moving their real content; null the drug fallback.

### D. Shared musts and prohibitions (all 30)

**Problem.**
- Five musts appear in all cases, two of them long-form duplicates.
- "Order a comprehensive neuropsychological battery ... (criteria-pack 'recommended' tier)": the
  pack says optional.
- "Obtain video-EEG..." (22 cases) is a test, not a recommendation.
- "Document the event semiology... not by a limb sign" (M04, M06, RP01).
- "Do NOT make the diagnosis by exclusion..." (27).
- Prohibitions cite "per Stone 2018", and forbid long-term antiseizure drugs ("start or
  continue"), which contradicts M06.

**Fix.** Replace both lists with the canonical set below plus the section 4 items. Delete the
neuropsychology, duplicate, video-EEG and semiology musts.

**Musts.**
- **M-DX**: "Make a positive diagnosis of functional neurological disorder (`<functional seizures |
  functional limb weakness | functional tremor | functional diplopia with convergence spasm |
  mixed>`) based on `<the case's rule-in signs and, for events, the recorded video-EEG events>`,
  and not by exclusion of other disease."
- **M-COMM**: "Explain the diagnosis to the patient, and with consent to the family, as a common
  and genuine disorder of nervous system functioning that can improve, show the positive signs,
  and give written information."
- **M-PHYSIO** (motor phenotype): "Refer for physiotherapy with expertise in functional motor
  disorder (motor retraining, Nielsen 2015 consensus)."
- **M-PSY** (functional seizures, or a psychiatric comorbidity that is a target): "Refer for
  psychological therapy by a clinician experienced in FND (CBT-informed) and treat the comorbid
  `<anxiety | depression | PTSD>`."
- **M-ASM** (M02, RP01, RP03, RS02): "Taper and stop `<drugs>` under neurological supervision,
  one drug at a time, since the events are functional and there is no evidence of epilepsy."
  Diazepam after long-term use is tapered "slowly over weeks".
- **M-EPI** (M06 only): "Continue levetiracetam at the current dose for the established right
  temporal lobe epilepsy, and do not escalate antiseizure treatment for the new functional
  events."
- **M-RESCUE** (paroxysmal): "Give the patient, family and ward a written plan for typical events:
  keep safe, do not restrain, wait for the event to end, and do not give emergency benzodiazepines
  or intubate for a typical functional seizure." M06 adds "rescue medication only for an event
  with the semiology of his known epileptic seizures".
- **M-COMORB**: case-specific (section 4).

**Prohibitions.** No citation inside the text.
- **P1**: "Order further investigations once the positive diagnosis is established, without a new
  specific clinical question (repeat MRI, CT, lumbar puncture, EMG or nerve conduction studies,
  evoked potentials, PET)."
- **P2**: "Tell the patient the symptoms are imagined, feigned, 'all in your head', or that nothing
  is wrong."
- **P3**: "Perform invasive testing without a specific indication (lumbar puncture, nerve or muscle
  biopsy, catheter angiography)."
- **P5** (paroxysmal): "Start or escalate antiseizure medication for the functional seizures."
  M-ASM cases add "or stop it abruptly". M06: "Add or escalate antiseizure medication for the new
  functional events."
- **P6** (paroxysmal): "Give benzodiazepines or intubate for a typical functional seizure" (M06:
  "event").
- **P7** (all except M09): "Give gadolinium contrast without a specific indication."

### E. Key evidence, red herrings, metadata (all 30)

**Problem.**
- The key_clinical_evidence (KCE) has 7 shared items, and an 8th in 22 cases. They include the
  leak "Interim composition decision, August 2026: FND remains only to keep the frozen
  dataset...", "Brain MRI and basic laboratory testing are OPTIONAL here...", and "Stone 2018"
  claims.
- Red herrings cite absent data:
  - "Family history of epilepsy" in M01 (the FH says none), P01, RM02, RP02, RS01, RS02, RS03, RS04
    and S03.
  - "Family history of MS" in RM03 and S02.
- `difficulty_rationale` and `revision_reason` are templates.

**Fix.**
- KCE: 3-6 case-specific items (signs found; event semiology; video-EEG result; the answer to the
  case's specific question; context as supportive, fact 1).
- Delete the leak, OPTIONAL and Stone items, and every red herring whose data are absent. Keep real
  ones (M04 aunt and febrile convulsions; RS03 outside label; M06 known epilepsy).
- Rewrite `difficulty_rationale` for the case; no review notes in metadata.

### F. Differential template (all 30)

**Problem.** Template rows:
- "normal brain MRI ... effectively excludes" a structural lesion, also where no MRI is in the
  pathway.
- Autoimmune encephalitis "(when obtained) negative antibody panel".
- Malingering `very_low` (21 cases), resting on a symptom-validity test never done.
- MS `low`.
- Epileptic seizures `moderate` (19) or `high` (M06, RM01, RP01), not lowered after the video-EEG.
- Neuropathy "(when obtained) normal EMG/NCS", although EMG is avoided.

**Fix (rule 7).**
- `key_features` cite this case's history, exam and the results of required or recommended
  criteria. Never "(when obtained)"; never an avoided or optional test.
- Epileptic seizures `low` after a normal video-EEG, key feature: "Habitual events recorded on
  video-EEG without ictal change; co-occurring epilepsy remains possible in about one in five
  patients with functional seizures."
- Delete autoimmune encephalitis (no case raises it).
- Malingering or factitious disorder: only where an external incentive is stated (M06, S09, M09),
  as `low`: "Feigning is conscious and cannot be separated from FND by examination signs;
  `<incentive>` is noted, but `<case evidence>` argues against it." Delete it elsewhere.
- MS, stroke, structural lesion: only where the presentation raises them, `low`, citing the
  clinical incompatibility (and the MRI where it is required or recommended).
- Neuropathy: only RS02, RP03, RP02 and RS01, citing reflexes and the sensory pattern.
- Add the case mimics of section 4.

### G. Fallbacks (all 30)

**Problem.**
- `specialized_test` (29): `test_type: ''` or neuropsych. 20 say "...the negative result is
  itself a harm" (a leak), 9 say "Study within normal limits", S07 says "Minor non-specific
  finding".
- `advanced_imaging` (29): modality `MRI_brain_functional` or `''`.
- `drug_interactions` (11): "(agent not specified on this case's pathway)".
- `literature_search` (5): a no-evidence report.
- `echo` (5): "benign incidental finding" without naming it.

**Fix.**
- Null the specialized_test, advanced_imaging, drug_interactions and literature_search fallbacks;
  the library answers by study.
- For echo, name the finding (for example "trace physiological tricuspid regurgitation") or null
  it.
- Keep the normal ct, csf, ecg, echo and cardiac_monitoring fallbacks (P08's CT moves, section 4).
- Remove the nulled keys from `metadata.fallback_tool_kinds`.

### H. Clinical assessment output (all 30)

**Problem.**
- 26 impressions end "...No further investigation is required to make the diagnosis; whatever
  imaging or laboratory testing is performed is for a separate, specific question" (a key leak).
- M04, M06 and RP01 say "...which is why video-EEG is required in this case rather than optional".
- `criteria_met` holds meta keys: `diagnosis_made_by_exclusion_only`,
  `psychological_stressor_required_for_diagnosis`, `positive_clinical_sign_present`,
  `symptoms_inconsistent_with_organic_disease`.
- Findings are fragments ("However, Hoover sign POSITIVE: ..."), and weak signs are counted.
- Wrong signs:
  - RP02 "Sternocleidomastoid weakness ipsilateral to the hemiparesis", with no hemiparesis.
  - P08 "upward drift".
  - S11 "Hoover sign bilaterally" for hand weakness.
  - RP01 "drug-refractory course".

**Fix.** Canonical shape:

```
assessment_type: functional_neuro_signs
scores: {positive_rule_in_signs_documented: "<n, fact 2>", internal_inconsistency: "present",
         distribution_consistent_with_a_single_lesion: "no"}
criteria_met: library keys, true/false for this patient: hoover_sign_positive, hip_abductor_sign_positive,
  give_way_weakness, drift_without_pronation, tremor_entrainment_positive, distractibility_of_deficit,
  inconsistency_between_examination_and_function; paroxysmal cases add functional_seizure_semiology_observed
  (true only if the examiner saw an event); RM02 adds convergence_spasm_with_miosis
findings: one clean sentence per sign examined, e.g.
  {sign: "Hoover sign", result: "Right hip extension weak on direct testing, full strength during contralateral hip flexion against resistance."}
  {sign: "Supportive features (low specificity)", result: "<...>; not counted as rule-in signs."}
  {sign: "Observed event", result: "<semiology, fact 4>"}   # only if seen
impression: "<Positive signs of functional weakness | tremor>: <list>. The pattern is inconsistent with a structural lesion."
  paroxysmal, add: "The event semiology (<features>) is typical of functional seizures; the examination does not by itself exclude epileptic seizures."
  no limb sign and no event seen: "No motor or sensory functional sign; neurological examination otherwise normal."
recommended_actions: []
pre_post_comparison: null
```

`patient.neurological_exam` must agree, and leaks there go: P08 "Capillary glucose was checked",
RM03 "serum sodium ... 131", the duplicated sentence in S11, and the RP01 commentary.

### I. MRI reports

**Problem.**
- Gadolinium is reported although the criterion is `contrast: false`: M01, M02, M03, P01, RM02,
  RS04, S01, S02, S03, S04, S05, S06 and S10. M05 says "no abnormal enhancement".
- P01 has a contrast allergy, yet has contrast brain plus cervical and lumbar spine.
- S03, S04 and RP03 bundle MRA. S07 bundles cervical and thoracic spine.

**Fix.**
- A non-contrast brain report (T1, T2, FLAIR, DWI/ADC, SWI), `contrast_used: false`, with no
  enhancement statements.
- MRA is removed. The spine goes to `body_imaging` `study: spine_MRI` (S07) or is deleted (P01).
- M09 is the exception (contrast required).

### J. EEG reports (22 cases)

**Problem.**
- M01 and RM03 impressions omit the captured events; M01 lacks a final period.
- M03 stores the prior routine EEG with no events, although admitted for video-EEG.
- M04 and S09 are written in capitals ("NO EEG CHANGE").
- RP01 has "bitemporal theta ... likely related to medications".
- Several impressions do not open with "This is a NORMAL EEG".

**Fix.** Canonical impression: "This is a NORMAL video-EEG. `<n>` habitual events were recorded
(`<brief semiology>`) without ictal EEG change before, during or after the events; the posterior
dominant rhythm persisted during the events. No interictal epileptiform discharges. No
electrographic seizures."
- M06 keeps "This is an ABNORMAL video-EEG due to right temporal interictal sharp-and-slow-wave
  discharges..." with the event recorded without ictal change.
- Findings carry the event times and durations; `clinical_correlation` is "".
- Never write "PNES", "functional" or "psychogenic" in an EEG report.

### K. Labs

**Problem.**
- M01: unexplained Na 149; Hct 44.8 against MCV x RBC 42.2, and Hct/Hb 3.37.
- M03: Hct 42.3 against 37.7.
- Templates in `clinical_significance` ("Ordered as part of the baseline workup; no
  abnormality...") in M05, M06, M09, RP03 and S09.
- Management text in RP02 and RS01 ("replace empirically", "there are no Wernicke features").
- Prolactin rows overclaim (fact 6).
- M06 TSH and B12 read "Within reference range" with no unit.

**Fix.**
- M01 Na within range (for example 140), removed from `abnormal_values_summary`.
- CBC consistent: Hct = MCV x RBC / 10, MCHC 32-36.
- `clinical_significance` null or a one-line analytic note.
- Qualitative rows get values and units; `interpretation` lists the abnormal values only.
- M02 and M03 Na 132 on an SSRI is plausible: keep it and name it in the drug output.

### L. Avoided actions (all)

**Problem.** ECG (19), echo (28), monitoring (29), CT (30), CSF (23), FDG_PET (29), emg_ncs (30)
and ssep (30) are all `waste`, cited `[Stone_2018]`.

**Fix.**
- Keep them as waste; replace the citation with `[Espay_2018]` or `[Stone_2016]`; each rationale
  is specific to the patient.
- Remove the P08 CT (section 4).
- Add a repeat-study waste where a prior normal study exists: P01 brain MRI; RP02 and RS01 spine
  MRI (`order_body_imaging` `{study: spine_MRI}`).
- Stored outputs of avoided actions stay null; the normal fallbacks answer them.

---

## 3. Target pathway and tiers

### 3.1 Pathway order (followup_outputs and action_criteria)

1. `perform_clinical_assessment` `functional_neuro_signs` (P08: after the fingerstick glucose).
2. Required or recommended red-flag tests: `interpret_labs`; `analyze_brain_mri` (or
   `order_ct_scan` in P08); `order_body_imaging` `spine_MRI` (S07).
3. `analyze_eeg` `video` (paroxysmal).
4. `check_drug_interactions`.
5. `order_specialized_test` `neuropsych_battery` (optional; no stored output).
6. `search_medical_literature`, last.

### 3.2 Criteria rules and tiers

**Exam** (`action-3-perform-clinical-assessment`): required in all 30, first in the list (except
P08). Keep the id.

**Video-EEG** (`analyze_eeg {"eeg_type": "video"}`, existing ids action-4 or action-5): required
in the 22 paroxysmal cases.
- Cases: M01, M02, M03, M04, M06, P01, RM01, RM03, RP01, RP03, RS01, RS02, RS03, RS04, S01, S02,
  S03, S04, S05, S06, S09, S11.
- Basis: pack section 2; ILAE 2013 documented level; AAN 2025 on co-occurring epilepsy and taper.
- `expected_evidence`: "Habitual events recorded on video with no EEG change and a normal
  interictal record".
- No routine-EEG alternative.

**Brain MRI.**
- Required:
  - M09: `contrast: true`, `protocol: ms`.
  - P08: action-4, labelled "emergency brain imaging", with alternatives
    `analyze_brain_mri {contrast: false, protocol: stroke}` and `order_ct_scan {contrast: false}`.
    Confirm with perfect_agent that the moved CT report serves the CT alternative.
- Recommended (`contrast: false`):
  - stroke mimics: M05, S05, S06, S10, RS04;
  - M03: post-event right arm deficit with word-finding difficulty; MRI ordered, not done;
  - P07: new deficit on Parkinson's disease;
  - RM02: functional diplopia;
  - RP03 and RS02: late-onset events with EGPA, CNS vasculitis question.
- Optional: M01, M02, S01, S02, S03, S04, and the S07 brain.
- Deleted: P01 (normal outpatient brain and spine MRI), with a repeat-MRI waste added.
- None: M04, M06, RM01, RM03, RP01, RP02, RS01, RS03, S09, S11 (leave as is).

**Spine MRI** (S07): new recommended `action-spine-mri`, `order_body_imaging {study: spine_MRI}`.

**Labs.** Panel names checked in costs.yaml: `glucose`, `sodium`, `serum_osmolality`,
`urine_osmolality`, `magnesium`, `phosphate`, `thiamine_B1`, `CMP`, `CBC`, `antiphospholipid`,
`complement C3/C4`, `anti_dsDNA`, `ESR`, `CRP`.
- Required:
  - P08: action-5, `["glucose"]`.
  - RM01: new `action-sodium-osmolality`, `["sodium", "serum_osmolality"]`, with a stored panel.
- Recommended:
  - RM03: sodium and serum and urine osmolality.
  - RP02 and RS01: magnesium, phosphate, thiamine_B1, CMP.
  - S09: magnesium, thiamine_B1, CMP.
  - M05: antiphospholipid, complement C3/C4, anti_dsDNA.
  - RP03: CBC, ESR, CRP.
- Optional: M01, M02, M03, M09.
- Deleted: M06 (`AED_levels` already in the HPI).

**Drug check** (`action-2-check-drug-interactions`, `{}`):

| tier | cases |
| --- | --- |
| required | M02 (levetiracetam started for the events, lorazepam), RP01 (carbamazepine, phenytoin, diazepam, sertraline), RP03 (levetiracetam, diazepam), RS02 (levetiracetam), RM03 (desmopressin, sertraline, polydipsia), RS01 (metoclopramide) |
| recommended | M01, M09, S03, S04, RS04 (benzodiazepine PRN); M06 (levetiracetam); RM01 (risperidone); P01 (serotonergic cluster, pregabalin); RP02 (ondansetron with low K and Mg) |
| optional | M03, M04, M05, P07, P08, RM02, RS03, S01, S02, S05, S06, S09, S10, S11 |
| delete | S07 (no medicines) |

**Neuropsychology**: new optional `action-neuropsych-battery`,
`order_specialized_test {test_type: neuropsych_battery}`, in all 30, with no stored output.

**Literature**: optional in all 30, last.

**Ids**: keep existing ids; new criteria take the ids above.

### 3.3 Sequence constraints (all soft)

- Exam -> MRI (or spine MRI), where the MRI is required or recommended, except P08. Reason: "The
  examination comes first: its positive signs decide whether imaging has a specific question to
  answer (Espay 2018)."
- Video-EEG -> drug check in M02, RP01, RP03 and RS02. Reason: "The decision to taper antiseizure
  drugs rests on the recorded events (AAN 2025; Oto 2005)."
- P08: `action-5-interpret-labs -> action-4-analyze-brain-mri`. Reason: "A fingerstick glucose
  comes before imaging in an acute deficit on insulin."
- RM01: `action-sodium-osmolality -> <video-EEG>`. Reason: "Exclude a hyponatremic cause in a
  patient with polydipsia and a prior hyponatremic seizure before prolonged monitoring."
- Never a constraint on literature, neuropsychology or an optional criterion.

### 3.4 Stop rule

- `required_before_assessment`: every required criterion of the case.
- `max_additional_actions`: keep 0. Recommended and optional criteria are justified and do not
  count; overuse is the construct (1.3).

### 3.5 Variant pathways

- **Motor or sensory only** (M05, M09, P07, P08, RM02, RP02, S07, S10): the exam plus the case's
  red-flag test.
- **Paroxysmal** (the other 22): the exam, then the required video-EEG, plus any red-flag test.
- **Taper** (M02, RP01, RP03, RS02): the drug check is required, plus the taper constraint, M-ASM,
  and P5 "abruptly".
- **Established epilepsy** (M06): M-EPI and the M06 variants of P5, P6 and M-RESCUE.
- **R series**: the pack calls R an "organic mimic", but every R case is labelled FND. Treat them
  as FND with record-derived complexity (CENTRAL 1); never relabel.

---

## 4. Per-case index

Every log: "Reviewer notes: No reviewer notes for this case." Classes A-H and L apply to all cases.
The classes I, J and K are named where they apply. "Pr" lists the prohibitions.

### M cases

- **FND-M01** (35 F; functional seizures with limb weakness; 48 h video-EEG)
  - Video-EEG required; J: name the 3 events in the impression.
  - I: non-contrast; the MRI stays optional.
  - K: Na 149 to normal; fix the CBC. Labs optional.
  - Drug check recommended: lorazepam PRN; escitalopram with ibuprofen.
  - E: delete the FH epilepsy red herring.
  - Musts: DX, COMM, PHYSIO, PSY (anxiety), RESCUE. Pr: P1-P3, P5, P6, P7.
- **FND-M02** (42 F; functional seizures and right-hand tremor; CT head normal; 72 h video-EEG)
  - Add levetiracetam 500 mg twice daily to `medications` (the HPI says it was started).
  - Drug check required: levetiracetam taper; lorazepam PRN; sertraline with cyclobenzaprine and
    with ibuprofen; Na 132.
  - Video-EEG required, with the constraint video-EEG -> drug check; J: rewrite the opening.
  - MRI optional (I); labs optional.
  - Signs: tremor entrainment and distractibility count; tuning-fork splitting is supportive.
  - Delete `search_literature_pnes` (NNT 5.7).
  - Musts: DX, COMM, PSY, PHYSIO, ASM, RESCUE. Pr: P1-P3, P5 (abruptly), P6, P7.
- **FND-M03** (29 M; functional seizures with right-sided weakness after events; head CT and a
  routine EEG normal; outpatient MRI not done)
  - J: replace the stored EEG with an inpatient video-EEG recording 2-3 habitual events without
    ictal change; the routine EEG stays as history.
  - MRI recommended (I); constraint exam -> MRI. Differential: add "Postictal (Todd) paresis" `low`.
  - Hoover is equivocal: report it so, and count the other validated signs (at least one must
    remain).
  - K: Hct; keep Na 132. Drug check optional (escitalopram with sumatriptan).
  - Musts: DX, COMM, PHYSIO, PSY, RESCUE. Pr: P1-P3, P5, P6, P7.
- **FND-M04** (35 F; functional seizures mimicking absence: eyelid flutter, some triggered by light;
  febrile convulsions at 3; maternal aunt with epilepsy)
  - Video-EEG required, with hyperventilation and photic stimulation in `activating_procedures`;
    J: no capitals.
  - Differential: add "Absence epilepsy or eyelid myoclonia" `low` (no generalized spike-wave, and
    normal responses to hyperventilation and photic stimulation). Keep the family-history red
    herring.
  - H: use the no-sign impression, unless the exam text describes an event.
  - No MRI criterion. Drug check optional.
  - Delete `patient_education_fnd_pnes` (it becomes COMM).
  - Musts: DX, COMM, PSY, RESCUE. Pr: P1-P3, P5, P6, P7.
- **FND-M05** (29 F; SLE on hydroxychloroquine; sudden right hemiparesis and sensory loss for 48 h;
  walks normally when unobserved)
  - MRI recommended, non-contrast with DWI (I: remove the enhancement sentence); exam -> MRI.
  - Labs recommended (antiphospholipid, complement C3/C4, anti_dsDNA), and the stored panel must
    contain them; K templates.
  - Differential: add "Neuropsychiatric SLE or antiphospholipid-related stroke" `low`; stroke
    `low`. "Normal when unobserved" is supportive.
  - Delete `rheumatology_consultation_sle`. Fold any real content of
    `hydroxychloroquine_interaction_check` into the initial output (QT, minor), then delete it.
    Drug check optional.
  - Musts: DX, COMM, PHYSIO, plus "Inform the rheumatologist; continue hydroxychloroquine". Pr:
    P1-P3, P7.
- **FND-M06** (42 M truck driver; established right TLE with MTS, seizure-free on levetiracetam for
  4 years; new arched-back events with closed eyes lasting 2-5 min; licence suspended; disability
  claim)
  - Video-EEG required; J: keep the abnormal interictal discharges and the event without ictal
    change.
  - Patient block: delete the editorial clause "(which is treatable and would support his
    disability claim) rather than to a functional cause"; keep the facts neutrally.
  - Delete the labs criterion (`AED_levels`, CMP); K: give TSH and B12 values.
  - Drug check recommended (levetiracetam mood effects). Delete `levetiracetam_mood_effects` and
    `mixed_epilepsy_pnes_literature`.
  - Differential: "Recurrence of known right TLE" `low`; malingering `low`, with the claim named.
  - H: event-based impression.
  - Musts: DX (coexisting with epilepsy), EPI, COMM, PSY, RESCUE (M06), and COMORB "Advise on
    commercial driving under the applicable regulations given the established epilepsy and the new
    events, and document it". Pr: P1-P3, P5 and P6 (M06), P7.
- **FND-M09** (47 F; RRMS on natalizumab for 4 years, JCV index 2.8; 10 days of right leg
  weakness that "feels different")
  - MRI required, `contrast: true`, `protocol: ms`. The stored report already shows stable lesions,
    no enhancement and no PML; state the gadolinium. Delete P7.
  - Patient block: delete the commentary "Natalizumab is the MS disease-modifying therapy with the
    highest PML risk"; keep the JCV index as a dated prior result.
  - Labs optional; K templates. The JCV row is history: remove it or mark it as a prior value.
  - Drug check optional; delete `natalizumab_pml_risk_management`.
  - Differential: MS relapse `low` (no new or enhancing lesion; Hoover), PML `low`, malingering
    `low` (medical leave).
  - Musts: DX, COMM, PHYSIO, plus "Continue natalizumab with routine PML surveillance by the MS
    team; no relapse treatment with steroids is indicated". Pr: P1-P3, plus "Treat as an MS relapse
    with high-dose steroids".

### P cases

- **FND-P01** (40 F; fibromyalgia; normal outpatient brain and spine MRI, NCS and bloods; contrast
  reaction; shaking events and tremor)
  - Delete MRI action-4. Add `avoid-waste-repeat-brain-mri` (`analyze_brain_mri`, `{}`): "A normal
    brain and spine MRI was obtained as an outpatient; repeating it answers no new question (Stone
    2016)."
  - I: the stored MRI becomes a non-contrast brain report matching the prior.
  - Video-EEG required (2 events; J).
  - Drug check recommended: duloxetine, cyclobenzaprine and sumatriptan (serotonergic);
    pregabalin with cyclobenzaprine (sedation); duloxetine with ibuprofen (bleeding).
  - Hoover equivocal: as M03. E: delete the FH red herring and the literature follow-up.
  - Musts: DX, COMM, PHYSIO, PSY, RESCUE. Pr: P1 (naming the repeat MRI and NCS), P2, P3, P5, P6,
    P7.
- **FND-P07** (61 F; PD on levodopa, pramipexole 1 mg three times daily and venlafaxine; 4 weeks of
  new left 8-10 Hz entraining, distractible action tremor and left arm weakness)
  - MRI recommended; exam -> MRI.
  - Differential: add "Progression of Parkinson's disease to the left side" `low` (different
    frequency, entrains) and "Right hemisphere stroke" `low`.
  - Delete `levodopa_adjustment_pramipexole` and `palliative_care_referral_husband`; caregiver
    support goes into COMM. Drug check optional.
  - Musts: DX (coexisting with PD), COMM, PHYSIO, plus "Continue the dopaminergic regimen
    unchanged". Pr: P1-P3, P7, plus "Increase dopaminergic medication for the functional tremor".
- **FND-P08** (24 F; T1DM on a pump; sudden left arm weakness 3 h after a bolus; HR 108)
  - Glucose required (action-5 `["glucose"]`); rename the row "Capillary glucose (on arrival)",
    keeping the value 92.
  - Imaging required (3.2); move `fallback_tool_outputs.ct` to `initial_tool_outputs.ct`; delete
    the CT avoided action. Constraint: glucose -> imaging.
  - H: drift without pronation, not "upward drift"; remove "Capillary glucose was checked" from the
    exam.
  - Delete `insulin_pump_cgm_education`; drug check optional. B: leak guard.
  - Differential: "Hypoglycemia with focal deficit" `low` (glucose 92), "Acute ischemic stroke"
    `low` (normal imaging plus positive signs).
  - Musts: DX, COMM, PHYSIO. Pr: P1-P3, P7.

### RM cases

- **FND-RM01** (38 M; paranoid schizophrenia on risperidone and benztropine; haloperidol dystonia;
  polydipsia up to 6 L/day; hyponatremic seizure 18 months ago; recurrent shaking events)
  - New required `action-sodium-osmolality`; write `initial_tool_outputs.labs` with a mild
    hyponatremia that does not explain the events (for example Na 134 mEq/L, osmolality 278
    mOsm/kg) plus normal glucose and calcium. Constraint: sodium -> video-EEG.
  - Video-EEG required. Drug check recommended: move the real content of
    `check_risperidone_seizure_threshold` into the initial output, then delete it.
  - Differential: add "Hyponatremia-provoked seizures" `low`; lower "Epileptic seizures" from
    `high` to `low`.
  - Patient block: delete the editorial "Importantly,".
  - Musts: DX, COMM (with the psychiatric team), PSY, RESCUE, plus "Continue risperidone; monitor
    fluid intake". Pr: P1-P3, P5, P6, P7, plus "Give haloperidol".
- **FND-RM02** (29 F; acute horizontal diplopia with convergence spasm; childhood bilateral medial
  rectus recession; 10-12 h/day of screens)
  - MRI recommended (I); exam -> MRI.
  - H: convergence spasm with miosis is the rule-in sign; midline vibration splitting is supportive.
  - Differential: add "Acute acquired comitant esotropia or decompensated strabismus" `low` (miosis
    with the esotropia; full abduction on ductions) and "Sixth nerve palsy" `low`.
  - E: delete the FH red herring. Drug check optional; delete both follow-ups.
  - Musts: DX (functional diplopia), COMM, plus "Orthoptic assessment and convergence-relaxation
    exercises" (no PHYSIO). Pr: P1-P3, P7, plus "Strabismus surgery for convergence spasm".
- **FND-RM03** (32 F; polydipsia with chronic hyponatremia; sertraline, desmopressin PRN,
  ondansetron; ED Na 129; events)
  - Drug check required: desmopressin with polydipsia and sertraline (severe hyponatremia).
  - Labs recommended; keep the values.
  - Video-EEG required; J: name the events.
  - H and patient block: remove "serum sodium ... 131" and its interpretation from the exam.
  - E: delete the FH MS red herring. Delete both follow-ups after moving their real content.
  - Musts: DX, COMM, PSY, RESCUE, plus "Stop desmopressin" and "Fluid restriction with serial sodium;
    review sertraline as a cause of SIADH with her psychiatrist". Pr: P1-P3, P5, P6, P7, plus
    "Continue desmopressin".

### RP cases

- **FND-RP01** (48 F; 26 years of carbamazepine, phenytoin and diazepam for "posttraumatic
  epilepsy"; 5-day video-EEG with taper; sulfonamide allergy)
  - Video-EEG required (5 events). J: remove the attribution "likely related to medications".
  - Drug check required (fact 16 pairs, diazepam dependence, the allergy); video-EEG -> drug check.
  - H: remove "drug-refractory course" and the commentary with scare-quoted 'seizures'; use the
    event-based impression.
  - Differential: "Epileptic seizures (posttraumatic epilepsy)" from `high` to `low` (fact 8).
  - Musts: DX, COMM, PSY, RESCUE, and ASM "Taper and stop carbamazepine and phenytoin one at a
    time, then diazepam slowly over weeks, under neurological supervision". Pr: P1-P3, P5
    (abruptly), P6, P7.
- **FND-RP02** (19 F, East African; BMI 14.8; protracted vomiting; primary amenorrhea; bereavement;
  prior head CT and spine MRI normal; leg weakness)
  - Labs recommended; K: remove the management text.
  - H: remove the SCM sign.
  - Drug check recommended: ondansetron with K 3.3 and Mg 1.5 (QT). Delete the sertraline
    follow-up.
  - Add a repeat spine MRI waste.
  - Differential: add "Eating disorder (anorexia nervosa)" as a comorbidity to assess, and "Thiamine
    deficiency (Wernicke, dry beriberi)" `low` (examination, thiamine level); note the refeeding
    risk. E: delete the FH red herring.
  - Musts: DX, COMM (interpreter and family as appropriate), PHYSIO, PSY, plus "Thiamine before
    glucose-containing fluids, with refeeding monitoring of phosphate, potassium and magnesium" and
    "Eating disorder assessment". Pr: P1 (naming the repeat CT and spine MRI), P2, P3, P7, plus
    "Give glucose-containing fluids before thiamine".
- **FND-RP03** (62 M; EGPA on prednisolone; diabetes with neuropathy; levetiracetam and diazepam
  started for events with an ear-pulsation prodrome; 7 events recorded)
  - Video-EEG required.
  - MRI recommended; I: remove the MRA (no MRA criterion); exam -> MRI.
  - Labs recommended (CBC, ESR, CRP); K templates.
  - Drug check required: the taper, and prednisolone with metformin (hyperglycemia). Delete
    `check_medication_interactions_ssri` (no SSRI). Video-EEG -> drug check.
  - Differential: add "CNS vasculitis (EGPA)" `low` (normal MRI; events without ictal change).
  - Musts: DX, COMM, PSY (illness anxiety about vasculitis), RESCUE, ASM (levetiracetam, then
    diazepam), plus "Continue EGPA treatment with rheumatology". Pr: P1-P3, P5 (abruptly), P6, P7.

### RS cases

- **FND-RS01** (19 F; the RP02 source patient; metoclopramide 10 mg three times daily, omeprazole;
  shaking events; prior CT and spine MRI normal)
  - Video-EEG required. Drug check required: metoclopramide (dystonia or akathisia; QT with Mg
    1.6). Delete the sertraline follow-up.
  - Labs and K as RP02. Add a repeat spine MRI waste. E: delete the FH red herring.
  - Differential: as RP02, plus "Metoclopramide-induced movement disorder" `low`.
  - Musts: as RP02, plus RESCUE and "Stop metoclopramide". Pr: as RP02, plus P5, P6 and "Continue
    metoclopramide".
- **FND-RS02** (64 M; the RP03 source patient; levetiracetam and gabapentin; diabetic neuropathy;
  EGPA with no steroid on the list)
  - Video-EEG required. MRI recommended (I); exam -> MRI.
  - Drug check required: levetiracetam taper, with gabapentin kept for the neuropathy. Delete
    `check_levetiracetam_interactions`; video-EEG -> drug check.
  - If the HPI names current EGPA treatment, add it to `medications`; otherwise log it.
  - Differential and musts as RP03 (ASM: levetiracetam only). E: delete the FH red herring.
- **FND-RS03** (26 F; an outside label of "psychogenic seizures" that she doubts; prior syncope
  with an unrevealing cardiac workup)
  - Video-EEG required (J). Drug check optional. Cardiac tests stay unscored.
  - E: delete the FH red herring; keep the outside label as a red herring ("a prior diagnosis is
    re-examined on positive evidence").
  - Musts: DX, COMM (address her doubt with the recorded events and the signs), PSY, PHYSIO,
    RESCUE. Pr: P1-P3, P5, P6, P7.
- **FND-RS04** (40 F; 5 days of right leg weakness and shaking after an argument; lorazepam and IV
  dexamethasone at the outside hospital; clonazepam PRN)
  - Video-EEG required. MRI recommended (I; stroke or demyelination had been considered); exam ->
    MRI.
  - Drug check recommended: clonazepam; escitalopram with naproxen. C: remove the QTc sentence;
    delete the follow-up.
  - Differential: stroke and MS `low`. E: delete the FH red herring.
  - Musts: DX, COMM, PHYSIO, PSY, RESCUE, plus "Stop dexamethasone" if it is still listed. Pr:
    P1-P3, P5, P6, P7.

### S cases

- **FND-S01, S02, S03, S04** (young adults; weeks of leg weakness and shaking events; outside CT
  head normal; inpatient video-EEG)
  - Video-EEG required (events: S01 1, S02 1, S03 3, S04 2); J: open with "This is a NORMAL
    video-EEG".
  - MRI optional (I); S03 and S04 also drop the MRA.
  - Drug check: recommended in S03 and S04 (lorazepam PRN); optional in S01 and S02 (sertraline
    with ibuprofen; S02 hydroxyzine adds sedation and QT). Delete the "Sertraline 150 mg"
    follow-ups (S01, S02, S04).
  - H: S03 "Tubular visual fields" is supportive; S04 counts only the validated signs among its 9.
  - E: delete the FH epilepsy red herring (S03) and the FH MS red herring (S02).
  - S04: PTSD after witnessing a fatal accident, named in PSY.
  - Musts: DX, COMM, PHYSIO, PSY, RESCUE. Pr: P1 (naming the repeat CT), P2, P3, P5, P6, P7.
- **FND-S05** (28 F; two events of arm shaking with eyes open and rolled back; 3 days of right leg
  weakness; similar weakness 2 years ago)
  - Video-EEG required (1 event; open eyes are atypical, so the record carries the events).
  - MRI recommended (I); exam -> MRI. B: leak guard. Drug check optional.
  - Musts and Pr: as S01.
- **FND-S06** (34 F; migraine; acute left arm and leg weakness with left hand tremor over 24 h;
  staring with eyelid flutter recorded; fluoxetine and sumatriptan)
  - Video-EEG required. MRI recommended (I); exam -> MRI. B: leak guard.
  - Differential: add "Hemiplegic migraine or prolonged aura" `low` (no headache phase; positive
    signs; normal MRI).
  - Drug check optional.
  - Musts: DX, COMM, PHYSIO, PSY (trauma-informed, given the abuse history), RESCUE. Pr: P1-P3,
    P5, P6, P7.
- **FND-S07** (22 F; 24 h of acute paraplegia; normal reflexes and sensation; bilateral Hoover;
  walks to the bathroom; no medicines)
  - New recommended `action-spine-mri`. Move the cervical and thoracic part of the stored MRI to
    `initial_tool_outputs.body_imaging` with `study: spine_MRI` (normal cord, no compression). The
    brain MRI stays brain-only and its criterion becomes optional. Exam -> spine MRI.
  - Delete the drug-check criterion and its output. G: null the "Minor non-specific finding"
    fallback.
  - Differential: add "Spinal cord compression" and "Transverse myelitis" `low` (normal spine MRI,
    no sensory level, normal bladder) and "Guillain-Barre syndrome" `low` (preserved reflexes).
  - Delete `family_meeting_fnd_education` (COMM includes the family).
  - Musts: DX, COMM, PHYSIO, PSY. Pr: P1-P3, P7.
- **FND-S09** (31 M veteran; PTSD on sertraline and prazosin; blast mild TBI in 2019; 2-4 beers
  daily; VA claim denied; unresponsive episodes)
  - Video-EEG required (J: no capitals).
  - Labs recommended; K templates.
  - Differential: add "Alcohol withdrawal seizures" `low` and "Post-traumatic epilepsy" `low`;
    malingering `low` with the claim named.
  - Drug check optional. Delete `alcohol_counseling_referral` and `va_fnd_ptsd_documentation`.
  - Musts: DX, COMM, PSY (trauma-focused therapy for PTSD), RESCUE, plus "Assess alcohol use and
    offer a brief intervention". Pr: P1-P3, P5, P6, P7.
- **FND-S10** (26 F; sudden left hemiparesis for 2 days after a call from her dissertation
  committee; HR 104; anorexia in remission)
  - MRI recommended (I); exam -> MRI. B: leak guard. Drug check optional.
  - Differential: stroke `low`.
  - Musts: DX, COMM, PHYSIO, PSY (social anxiety). Pr: P1-P3, P7.
- **FND-S11** (45 F; many prior presentations with normal investigations; 3 weeks of bilateral hand
  weakness; three unresponsive episodes)
  - Video-EEG required (1 episode).
  - H: replace "Hoover sign bilaterally" with the finger abduction sign or collapsing weakness;
    remove the duplicated sentence in `additional`.
  - Drug check optional (venlafaxine with naproxen). Delete `review_prior_negative_workup`.
  - Differential: MS `low`, citing the clinical incompatibility (no MRI criterion).
  - Musts: DX, COMM (address her concern about MS), PHYSIO, PSY, RESCUE. Pr: P1 (naming the repeat
    investigations), P2, P3, P5, P6, P7.

---

## 5. CENTRAL requests (outside the case files)

1. **Pack** `criteria_packs/FND.md`:
   - Remove `[Stone_2018]`.
   - Rename `[Carson_2012]` to `[Carson_Lehn_2016]`.
   - Add the (C) keys of 1.1, with `[AAN_Functional_Seizures_2025]` = Tolchin, Neurology
     2026;106:e214466.
   - Rewrite section 6 "R (reverse / mimic)": every R case is labelled FND.
   - Literature and drug check stop being recommended by default (ROUND_POLICY 5, 6).
   - Update the counts: MRI required in 2 and recommended in 10, plus the S07 spine; labs required
     in 2 and recommended in 6.
2. **Synonyms** (`diagnosis_synonyms.yaml`, the F44 group, lines 179-185):
   - Every FND case accepts the PNES labels and F44.5, so the motor-only cases (M05, M09, P07, P08,
     RM02, RP02, S07, S10) accept "psychogenic non-epileptic seizures", and RM02 (diplopia) accepts
     "functional weakness".
   - Scope the seizure labels and F44.5 to the paroxysmal cases, the motor labels and F44.4 to the
     motor cases, and F44.6 to sensory. Keep the generic FND labels for all.
3. **EEG routing**: EEG reports carry no `eeg_type`, so a `routine` order receives the stored
   video-EEG with its events. Request either a rule that serves a routine interictal normal report
   in that case, or an `eeg_type` discriminator.
4. **Guidance claims** (`condition_tool_guidance.yaml`, `test_guidance_claims.py`): replace "every
   instrumental action is optional", "MRI in 20, labs in 12" with the post-round tiers:
   - video-EEG required in 22;
   - MRI required in M09 and P08, recommended in 10;
   - spine MRI recommended in S07;
   - labs required in P08 and RM01.
5. **`conditions.yaml`** `functional_neurological_disorder`:
   - `common_followups` put EMG and neuropsychology under `interpret_labs` and spine MRI under
     `analyze_brain_mri`. Use `order_specialized_test` (`emg_ncs`, `neuropsych_battery`) and
     `order_body_imaging` `spine_MRI`.
   - Add video `analyze_eeg` for the paroxysmal phenotype.
6. **Banned strings** (`test_case_guards.py`): add an FND row for:
   - "Stone_2018" and "per Stone 2018";
   - "Interim composition decision";
   - "No further investigation is required to make the diagnosis";
   - "negative result is itself a harm";
   - "agent not specified on this case's pathway";
   - "is a prescribing decision, not an output of this check";
   - "NNT 5.7".
7. **Library** (`fallback_library.yaml`):
   - If the specialized-test sentence "does not contribute ... itself a harm" exists at library
     level, neutralise it.
   - Add `convergence_spasm_with_miosis` and a finger-abduction finding to the
     `functional_neuro_signs` normal report.
8. **UI** (review app): show the criteria in list order with their tiers. Mark the optional
   neuropsychology criterion as optional, not as a step.

---

## 6. Open questions for Andrea

**Resolved by the lead** (Andrea, 24 Oct 2026: resolve for dataset quality). Each can be reverted.

1. **Video-EEG required in the 22 paroxysmal cases.** This implements the pack (2026-08-06); it is
   not a new policy. To revert: set the EEG criteria to `optional`, remove them from the stop rule,
   and drop the video-EEG -> drug-check constraints.
2. **MRI and labs beyond the pack's examples.** MRI: M03, RS04, RP03, RS02 and S06. Labs: RM01,
   RM03, S09, M05 and RP03. Each has a named question in section 4.
3. **Duplicate source patients** (RP02 with RS01, RP03 with RS02). All four are in the train split,
   so there is no train/test contamination. Keep all four, and invent no divergent data.
4. **Optional neuropsychology criterion in all 30** (pack Optional). The 1104 EUR battery becomes
   justified but uncredited, rather than a stopping penalty.

**Still open (only Andrea can answer)**

5. **Composition.** Reviewer 1 asked whether FND should stay; the recorded answer keeps it for the
   overuse measurement, with DLB added. Confirm FND stays in the frozen dataset for the paper. If
   DLB is to replace FND rather than join it, this round's FND work is moot.
