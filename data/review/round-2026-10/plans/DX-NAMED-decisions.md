# Patient text that names the case's own diagnosis (3 Nov 2026)

Request: Andrea, 3 Nov 2026, relayed by the session "Statistiche diversità casi" (analysis in
`docs/paper/case-diversity.md` section 9: 115 of 600 cases name an accepted label).

## Recount
Text checked: what the model sees at turn 0, `harness/context.py::format_patient_info` (chief
complaint, HPI, past history, medications with their indication, family and social history,
examination, vitals). Tool outputs are not visible at turn 0. Every accepted label of the case,
acronyms included (case-sensitive), possessive and plural forms folded.

- 173 cases named an accepted label, not 115. The first count kept only labels of 6 or more
  characters, so it missed the acronyms ("No ALS family history" in 23 ALS cases; FTD, MG, HE,
  SE, FND, PD, MS), and did not read the medication indications (e.g. "Lactulose (HE prophylaxis)").
- Fields: family history 117, HPI 54, medications 34, past history 28, examination 12, chief
  complaint 5.
- After the fix: 84 cases still name a label, all in the classes kept on purpose below.

## Fixed (113 cases, 125 edits)
1. Negated family history naming the condition's own disease (98 cases): ALS 23, MS-RR 23, PD 19,
   MIG-AURA 13, FTD 9, FND 3, MG 3, ALZ-EARLY, FEPI-TEMP, NMDAR-ENC, SAH, SE 1 each. The disease
   name is removed from the list ("No family history of multiple sclerosis or other demyelinating
   diseases" -> "No family history of demyelinating diseases"); an item that named only the
   disease is dropped, and an emptied family history reads "Non-contributory". Mimic cases too
   (PD-P01, PD-RP03, MG-P03): the name pointed at the condition in every case of it.
   Hemiplegic migraine: sporadic HM (ICHD-3 1.2.3) needs the absence of affected relatives, so in
   all 13 MIG-AURA items the negation stays, as "migraine with motor weakness".
2. Negated personal history naming the diagnosis: HEP-ENC M01, M09, M10, P07, P08 ("no prior
   episodes of hepatic encephalopathy" -> "no prior similar episodes" / "overt encephalopathy"),
   SYNC-CARD-RS05 (sustained VT -> sustained arrhythmia), MS-RR-P05 ("no prior MS diagnosis").
3. The patient's worry naming the true diagnosis: ALS-S07 (chief complaint and HPI), ALS-S08,
   ALS-P01, SAH-P07 -> "a serious neurological disease" / "something serious".
4. A referral listing the true diagnosis as one option: FND-RP02, FND-RS01 ("schizophrenia /
   psychosis versus conversion disorder" -> the wrong anchor alone), MIG-AURA-M03 ("possible TIA
   or hemiplegic migraine" -> "possible TIA").
5. Positive history without clinical weight that only pointed at the answer: FND-S03 (aunt with
   conversion disorder -> anxiety disorder), GLIO-HG-P03 (uncle with glioblastoma -> brain tumour
   of unknown type, as the HPI already said).
6. Past history stating the lateralisation that is the case's question: FEPI-TEMP-RP04 ("Left
   temporal lobe epilepsy diagnosed at 41" -> "Focal epilepsy", as the HPI says).
The legacy `patient.hpi` copy (not shown to the agent) got the same HPI edits.

## Kept on purpose (listed for the physicians)
- Known disease, the question being the complication or the cause: recurrent HE with secondary
  prophylaxis (HEP-ENC, SE-P07), known MG in crisis (MG-M04, RM14, RM15), known PD (PD-RM01,
  RM05, RP04), known focal epilepsy for presurgical work-up (FEPI-TEMP-P04, RP04, RS03, RS04),
  established migraine with aura for management (MIG-AURA-S10, S11, P04), known hemiplegic
  migraine with an incidental aneurysm (MIG-AURA-P09), known PNES (SE-P02), recurrent
  meningitis (BACT-MEN-RP04, RS02, RP03).
- Status epilepticus observed on arrival ("arrives in active status epilepticus", exam "SE >20
  minutes"): the state is seen, not inferred; the cause is the question.
- Positive family history with a clinical role: PD (RS01, RS02, RS05, S01, RM03, RM05), MS (P05,
  S03, S04, S06), ALS-S10 and ALS-P09 (C9orf72), FTD-M06 and S05 (GRN, familial), ALZ-EARLY
  (M02, M05, S02-S04), ISCH-STR (RS01, S05; RP05 CADASIL), MIG-AURA (S02, S06; P06 CADASIL, P08
  MELAS), SYNC-CARD (RP04, RS03 conduction disease), SAH-S07 (ruptured aneurysm).
  Doubt: MG-M02 (aunt with MG prompted the referral) is a strong pointer with little clinical
  weight; left for the physicians.
- Designed wrong anchors that name the condition but not the answer: PD-P02 (DLB referred as
  PD), PD-P03, GLIO-HG-P02 (PCNSL referred as GBM), MG-P04 ("excluding MG").
- Risk-factor negatives that do not name the diagnosis: "No family history of aneurysm" (SAH),
  "of epilepsy" (FEPI-TEMP), "of stroke" (ISCH-STR), sick contacts with meningitis (BACT-MEN).

Checks: perfect agent 600/600, `apply_diagnosis_synonyms.py --check` 0, pytest 6529 passed.
