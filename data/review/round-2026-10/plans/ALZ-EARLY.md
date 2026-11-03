# ALZ-EARLY: condition plan for the October 2026 review round

Lead plan for the 30 ALZ-EARLY cases (M01..M05, P01..P04, RM01..RM04, RP01..RP05, RS01..RS06,
S01..S06). Workers follow it case by case so that every case reaches the same decision. Read
`ROUND_POLICY.md` and `PATTERNS.md` first; this plan does not repeat them. All 69 Reviewer 1 notes
(11 cases: M01..M05, P01..P04, RM01, RM02) are listed in section 4 with the class (section 2) that
resolves them. Reviewer 2 has not reviewed this condition (pending on M01 only). The other 19 cases
have no notes, but every class applies to them (ruling 2: a note is a class).

Baseline measured on 24 October 2026 before any edit: no ALZ-EARLY case or log is modified in git.
`perfect_agent.py` copies each criterion's own arguments, so it does not catch the library and
fallback defects of class C2; check them by reading `-v` output (section 3.6).

Section 2 cites notes by the first 8 characters of their id; section 4 gives every full id under its
case.

How to use this plan:

1. Apply every class in section 2 to your case, in the order listed, using the canonical text
   verbatim where a canonical text is given (fill the `<...>` slots from the case).
2. Then apply the per-case decisions of section 4.
3. Rebuild `action_criteria`, `followup_outputs`, `sequence_constraints` and `stop_rule` exactly as
   section 3 says.
4. Run both checks, write the log, cite every note id of the case.

Conventions for all new text: English, the case's spelling (US in this condition), no em dashes or
en dashes (replace an existing em dash only in a sentence you rewrite anyway), units as the case
already uses them. Do not invent numbers the case does not need; where a class asks you to add a
result, choose a plausible value that agrees with age, sex, renal function, medicines and the other
reports of the case, and differs from the other cases.

---

## 1. Governing guidelines and canonical facts

### 1.1 Which guideline governs what

| question | governing source | citation key |
| --- | --- | --- |
| Clinical diagnosis of dementia due to AD, possible/probable | McKhann GM et al., Alzheimers Dement 2011;7:263-269 | `[NIA_AA_2011]` |
| MCI due to AD, functional threshold, biomarker likelihood levels | Albert MS et al., Alzheimers Dement 2011;7:270-279 | `[NIA_AA_MCI_2011]` (new key, CENTRAL) |
| A/T/N biomarker categories | Jack CR Jr et al., Alzheimers Dement 2018;14:535-562 | `[NIA_AA_2018]` |
| Revised biological criteria (Core 1 biomarkers, staging) | Jack CR Jr et al., Alzheimers Dement 2024;20:5143-5169 | `[AA_2024]` (new key, CENTRAL; see Q1) |
| MCI management (no routine cholinesterase inhibitor, exercise, serial assessment) | Petersen RC et al., Neurology 2018;90:126-135 | `[AAN_dementia_2018]` (existing key; it is the AAN MCI guideline) |
| Dementia assessment and drug treatment (AChEI for mild to moderate AD, memantine for moderate or severe) | NICE NG97, Dementia: assessment, management and support (2018) | `[NICE_NG97]` (from the July tool guidance) |
| Amyloid PET appropriate use | Johnson KA et al., Alzheimers Dement 2013;9:e1-e16 | `[Appropriate_Use_Amyloid_PET]` |
| Posterior cortical atrophy | Crutch SJ et al., Alzheimers Dement 2017;13:870-884 | `[PCA_consensus_2017]` (new key, CENTRAL) |
| Primary progressive aphasia, logopenic variant | Gorno-Tempini ML et al., Neurology 2011;76:1006-1014 | `[PPA_2011]` (new key, CENTRAL) |
| Behavioural/dysexecutive variant of AD | Ossenkoppele R et al., Brain 2015;138:2732-2749 | `[bvAD_2015]` (new key, CENTRAL) |
| bvFTD criteria (differential of P03) | Rascovsky K et al., Brain 2011;134:2456-2477 | `[FTDC_2011]` (new key, CENTRAL) |
| Genetic counselling and testing for AD and FTD | Goldman JS et al., Genet Med 2011;13:597-605 | `[ACMG_NSGC_2011]` (new key, CENTRAL) |
| Autosomal-dominant AD natural history | Bateman RJ et al., N Engl J Med 2012;367:795-804 | `[Bateman_2012]` |
| sCJD diagnosis (RP04) | Hermann P et al., Lancet Neurol 2021;20:235-246 | `[CJD_2021]` (new key, CENTRAL) |
| iNPH (RM02) | Relkin N et al., Neurosurgery 2005;57(3 Suppl):S4-S16; Nakajima M et al., Neurol Med Chir 2021;61:63-97 | `[iNPH_2005]`, `[iNPH_Japan_2021]` (new keys, CENTRAL) |
| Cerebral amyloid angiopathy (lobar microbleeds) | Charidimou A et al., Lancet Neurol 2022;21:714-725 (Boston 2.0) | `[Boston_CAA_2022]` (new key, CENTRAL) |
| Small-vessel disease terms | Wardlaw JM et al., Lancet Neurol 2013;12:822-838 (STRIVE) | `[STRIVE_2013]` (new key, CENTRAL) |
| Low-normal B12 and MMA | Devalia V et al., Br J Haematol 2014;166:496-513 (BSH) | `[BSH_B12_2014]` (new key, CENTRAL) |
| Subclinical hypothyroidism | Pearce SH et al., Eur Thyroid J 2013;2:215-228 (ETA); Stott DJ et al., N Engl J Med 2017;376:2534-2544 (TRUST) | `[ETA_SCH_2013]`, `[TRUST_2017]` (new keys, CENTRAL) |
| Potentially inappropriate medicines in older adults | American Geriatrics Society Beers Criteria 2023, J Am Geriatr Soc 2023;71:2052-2081 | `[Beers_2023]` (new key, CENTRAL) |
| Anti-amyloid antibody eligibility (only where the case already discusses it) | van Dyck CH et al., N Engl J Med 2023;388:9-21 (CLARITY AD); Cummings J et al., J Prev Alzheimers Dis 2023;10:362-377 | `[CLARITY_AD_2023]`, `[Lecanemab_AUR_2023]` (new keys, CENTRAL) |

Until the new keys exist centrally, use them anyway in the case (the citation guard reports unknown
keys; the lead files them under CENTRAL). Never cite a "2023 AAN MCI guideline": it does not exist
(the current AAN MCI guideline is Petersen 2018).

### 1.2 Canonical facts (use these, do not restate them differently)

Staging (Albert 2011; McKhann 2011)

- MCI: concern about a change in cognition, impairment in one or more domains beyond age and
  education norms, **preservation of independence in functional abilities** (the patient may be
  less efficient, slower, or use aids and reminders), and no dementia.
- Dementia: the cognitive impairment interferes with the ability to function at work or in usual
  activities. Operational rule for this round: instrumental independence is **lost** when another
  person has taken over, or must supervise, at least one complex activity (finances, medicines,
  driving, cooking safety, work duties) because of cognition, or there are repeated safety
  incidents (car accidents or getting lost, missed medicines with consequences, stove left on,
  scams). It is **preserved** when errors are isolated and the patient's own strategies
  (calendars, pill box, phone reminders) compensate them.
- Mild dementia due to AD with onset under 65 years: G30.0; 65 years or more: G30.1. MCI: G31.84
  (as the criteria pack says). Age at **onset**, not at visit, decides G30.0 versus G30.1.

Biomarkers

- NIA-AA 2018 categories: A = amyloid (CSF Abeta42 or Abeta42/40 ratio, amyloid PET); T =
  phosphorylated tau (CSF p-tau, tau PET); N = neurodegeneration (MRI atrophy, FDG-PET
  hypometabolism, CSF total tau). A+T- is "Alzheimer's pathologic change"; A+T+ is "Alzheimer's
  disease" in the biological sense.
- Albert 2011 likelihood: MCI due to AD with **intermediate** likelihood when only one biomarker
  category is positive or tested; **high** likelihood when both an amyloid and a neuronal injury
  marker are positive.
- AA 2024 (Jack 2024) counts an abnormal Core 1 biomarker (amyloid PET, CSF Abeta42/40, CSF
  p-tau181/Abeta42, CSF t-tau/Abeta42) as sufficient for the biological diagnosis. Whether a case is
  written to 2018 or 2024 is open question Q1; until Andrea answers, write impressions that are
  true under both: name the measured profile ("decreased Abeta42/40 ratio with p-tau within the
  laboratory range") and do not write "A+T+" or "biomarker-confirmed AD" unless both amyloid and
  p-tau are abnormal.
- CSF Abeta42/40 needs Abeta40 to be measured. A report that has no Abeta40 value must not state a
  ratio.
- 14-3-3 protein and RT-QuIC belong to the work-up of rapidly progressive dementia; they are not
  part of a routine AD biomarker panel (only RP04 keeps them).
- CSF opening pressure is the measurement taken at the LP for NPH; the tap test outcome is a
  timed gait and cognitive comparison before and after removal of 30 to 50 mL.
- Amyloid PET and CSF are alternatives for amyloid status; a second test is not needed when one is
  conclusive (Johnson 2013; July 2026 tool guidance).

Imaging

- Contrast is not part of the dementia MRI protocol. When `contrast` is false a report must not say
  "no abnormal enhancement" or "post-gadolinium".
- Lobar (cortical or juxtacortical) microbleeds point to cerebral amyloid angiopathy; deep
  (basal ganglia, thalamus, brainstem) microbleeds point to hypertensive arteriopathy (Boston 2.0).
- Evans index above 0.3 is ventriculomegaly. iNPH imaging supporting signs: disproportionately
  enlarged subarachnoid space hydrocephalus (DESH), acute callosal angle (under 90 degrees). The
  full triad is not required for possible iNPH; a negative tap test does not exclude shunt
  response (Relkin 2005).
- MTA (Scheltens) grade is a visual MRI rating, 0 to 4, per side. On CT the case can state only
  qualitative medial temporal volume loss unless coronal reformats were acquired.

Medicines

- Cholinesterase inhibitors (donepezil, rivastigmine, galantamine) are indicated for mild to
  moderate AD dementia (NICE NG97). They are **not** approved for MCI, and the AAN 2018 guideline
  says clinicians may choose not to offer them in MCI; if offered, the patient must be told the use
  is off-label and not supported by evidence.
- Memantine is for moderate or severe AD (or when AChEIs are not tolerated); not for MCI or mild AD.
- Donepezil is metabolised by CYP2D6 and CYP3A4 (not CYP2C19). Strong CYP2D6 inhibitors
  (fluoxetine, paroxetine, bupropion) can raise its levels.
- Donepezil can cause bradycardia, heart block and QT prolongation; with another QT-prolonging drug
  (citalopram, escitalopram) a baseline ECG is reasonable.
- Amlodipine does not slow the heart rate. Beta-blockers, verapamil, diltiazem and digoxin do.
- Tamsulosin is an alpha-1 blocker; it is not anticholinergic. Oxybutynin, tolterodine,
  solifenacin, diphenhydramine, tricyclics and paroxetine are.
- Proton pump inhibitors do not reduce donepezil absorption. Long-term PPI use is associated with
  low B12 (relevant to the B12 finding, not to donepezil).
- Levetiracetam does not lower the seizure threshold; bupropion and tramadol do.
- Zolpidem and benzodiazepines in older adults with cognitive impairment: avoid (Beers 2023);
  deprescribe with a taper. This is a must, not a drug-interaction check finding.
- Subclinical hypothyroidism (TSH above range, free T4 normal): repeat TSH and free T4 with TPO
  antibodies in 2 to 3 months; levothyroxine is not routine in older adults with TSH under 10 mIU/L
  (ETA 2013, TRUST 2017). It is not a reversible cause of dementia at that level.
- Serum B12 in the low-normal range (about 148 to 221 pmol/L, 200 to 300 pg/mL) is indeterminate:
  measure methylmalonic acid (MMA) and homocysteine; replace B12 when MMA is raised (BSH 2014).

---

## 2. Error classes in this condition

Each class: what is wrong, where (notes and survey), the decided fix, canonical text.

### C1. Cholinesterase-inhibitor drug check in MCI, and wrong interaction content (rulings 4, 6)

Notes: 78693860, dd4d5e93 (M01); 3c5edf5d (M02); 2a2dd64e (M03); b5a52f53, 4ce60934 (M04);
e9050809 (M05); 2e39ab2d, 262248db (RM01); af88df2d (P04).

Found: every case has a `check_drug_interactions` criterion with a donepezil follow-up (except RP04
and RP05), and every MCI case has the key evidence item "Cholinesterase inhibitors are first-line
symptomatic therapy...". The drug-check outputs carry wrong pharmacology: M03 says amlodipine
slows the heart and calls tamsulosin anticholinergic; RM02 says pantoprazole reduces donepezil
absorption; RM04 and S06 route donepezil through CYP2C19 (omeprazole); RM03 pairs zolpidem with
donepezil as a "CNS depressant" interaction and refers to an ECG the case does not contain; RP03
says levetiracetam lowers the seizure threshold; RS02 recommends a baseline ECG while ECG is an
avoided action. The heart rate quoted in the drug-check output differs from the vitals in M01 (74
vs 68), M02 (76 vs 74), S02 (76 vs 72), S03 (76 vs 79), S04 (76 vs 72).

Fix:

1. **MCI-staged cases** (after C4: M01, M02, M03, M04, RM04, S06, and any case that stays MCI):
   delete the `check_drug_interactions` criterion and its follow-up; set
   `initial_tool_outputs.drug_interactions` and `fallback_tool_outputs.drug_interactions` to null.
   Add the prohibition below. Replace the key evidence item on AChEI first-line with the MCI fact
   below.
2. **Dementia-staged cases**: keep the criterion as `optional`, last in the clinical order (before
   literature only), with `required_arguments` `{"drug": "donepezil"}` so a call matches only the
   drug the case needs. Make it `required` only where the case has a concrete interaction:
   P04 and RP02 (escitalopram, QT), RP03 (fluoxetine, CYP2D6; check the list), RM03 if restaged
   (zolpidem is a deprescribing must, the interaction check stays optional unless another
   concrete interaction exists). Rewrite the stored output so every statement is true per 1.2 and
   uses the heart rate, ECG status and medicines of this case. No ECG is quoted unless the case
   contains one.
3. M04 (4ce60934): levothyroxine is not started for TSH 6.8 with normal free T4. Remove it from the
   drug check and the musts; add the subclinical hypothyroidism must below.

Canonical text:

- Prohibition (MCI): "Do not start a cholinesterase inhibitor or memantine as routine treatment for
  mild cognitive impairment; neither is approved for MCI and the guideline does not support routine
  use [AAN_dementia_2018]."
- Must (MCI): "Arrange cognitive and functional reassessment in 6 to 12 months and recommend regular
  exercise (at least twice weekly); explain that no medicine is approved for mild cognitive
  impairment [AAN_dementia_2018]."
- Key evidence (MCI, replaces the AChEI item): "Cholinesterase inhibitors are not approved for mild
  cognitive impairment and are not recommended routinely at this stage; serial assessment and
  vascular risk management are the evidence-based steps [AAN_dementia_2018]."
- Must (dementia): "Offer a trial of a cholinesterase inhibitor (donepezil, rivastigmine or
  galantamine) for mild Alzheimer dementia after checking pulse, conduction history and current
  medicines <case-specific: e.g. 'and a baseline ECG because of escitalopram'> [NICE_NG97]."
- Must (subclinical hypothyroidism, M04 and any case with TSH above range and normal free T4):
  "Repeat TSH and free T4 with TPO antibodies in 2 to 3 months rather than starting levothyroxine;
  a TSH of <value> with normal free T4 does not explain the cognitive decline [ETA_SCH_2013]."

### C2. Biomarker route: one criterion, two alternatives, and the library contradicts the case

Notes: 88980d7d (M01); aec83190 (M03); d758bd87 (M04); 32e77625 (M05); 34769945 (M05).

Found: 22 cases have an `analyze_csf` criterion and 8 cases (P01, P02, P03, RM04, RP01, RP02,
RP03, RP05) an `order_advanced_imaging` `amyloid_PET` criterion, each labelled "... as the single
optional biological-confirmation route". 20 cases carry the must "Consider the single
case-designated optional biomarker route ...", which is engineering language. Reviewer 1 rules:
PET is an alternative to CSF, needed only if uncertainty remains and it would change management.
If an agent orders the other test, it gets the library default, which is **normal** (amyloid PET
"Amyloid-negative", centiloid 8; CSF Abeta42 980, ratio 0.098): a correct alternative returns a
result that contradicts the case. `fallback_tool_outputs.advanced_imaging` is a DaTscan report in
M05, RM04, RP04, RS06, S05 and an MR spectroscopy report in RP05; a fallback answers **every**
modality of its tool, so an amyloid PET or FDG order in those cases returns a DaTscan report.

Fix:

1. Keep the existing criterion id. Give it two alternatives:
   `analyze_csf` `{"special_tests": ["Abeta42", "Abeta42_40_ratio", "phospho_tau", "total_tau"]}`
   and `order_advanced_imaging` `{"modality": "amyloid_PET"}`. Tier `optional` (RP04: CSF stays
   `required` and single-alternative, with 14-3-3 and RT-QuIC, because the question there is CJD).
2. Author the concordant counterpart so both alternatives return the case's biology:
   - CSF-route cases: add a follow-up `order_advanced_imaging` amyloid PET (trigger
     `order_amyloid_pet`, modality `amyloid_PET`). Positive where the CSF shows a decreased
     Abeta42/40 (M01 and M03 included: a decreased ratio is concordant with a positive PET); write
     a visual read and a centiloid value consistent with the CSF; no tau statement (amyloid PET
     does not measure T).
   - PET-route cases: add `initial_tool_outputs.csf` (or a CSF follow-up) with Abeta42, Abeta40,
     ratio, p-tau181 and t-tau concordant with the PET and the MRI; cell count, protein and glucose
     normal; no 14-3-3, RT-QuIC, infectious or autoimmune panels (C6).
3. Set `fallback_tool_outputs.advanced_imaging` to null in M05, RM04, RP04, RP05, RS06, S05. If the
   case needs a DaTscan answer (RP05 has a DaTscan criterion; it already has its own follow-up),
   keep it as a follow-up with modality `DaTscan`.
4. Label and rationale (rationale must differ from the label, C13):
   - label: "Establish amyloid status with CSF biomarkers or amyloid PET when the result would change
     management"
   - rationale: "Either CSF Abeta42/40 with p-tau or amyloid PET establishes amyloid status; one
     conclusive test is enough, and it is needed when the diagnosis remains uncertain after the
     clinical, neuropsychological and MRI assessment or when disease-modifying treatment is being
     considered [NIA_AA_2018] [Appropriate_Use_Amyloid_PET]."
   - `expected_evidence`: describe the result in terms both tests satisfy (e.g. "Amyloid
     positivity: decreased CSF Abeta42/40 ratio with raised p-tau, or a positive amyloid PET").
5. Replace the must "Consider the single case-designated optional biomarker route..." with:
   "Offer amyloid biomarker testing (CSF or amyloid PET) if a biological diagnosis would change
   management, such as eligibility for anti-amyloid treatment or diagnostic uncertainty; one
   conclusive test is sufficient [Appropriate_Use_Amyloid_PET]."
6. Key evidence items and narratives must not cite a biomarker the pathway does not return
   (M05 KCE "amyloid PET positivity", RP04 "Positive amyloid PET"): remove or reword (34769945).

### C3. Template clinical assessment (`initial_tool_outputs.clinical_assessment`)

Notes: 30a27ac9 (M03); 03a603fe, 4ffea6c8 (M04); ccca2140, d7ec34ff (P01); e0c624ba (P02);
d82080e9 (P03).

Found: `amnestic_predominant_profile` is true in all 30, including the PCA, lvPPA and frontal
variants (P01, P02, P03, RP01, RP02, RP03). The impression is one of two templates: dementia
cases say "delayed recall that does not recover with cueing, a storage rather than a retrieval
deficit"; MCI cases say "partial benefit from cueing". Neither is grounded in the case. Every
impression ends with "This assessment is the step that makes the syndrome measurable; imaging and
biomarkers then attribute it." (engineering text) and the MCI ones with "the threshold is
functional, and this assessment is where it is decided". The cueing field is true while the
recorded exam shows no cue benefit in M03, M04, S02, S05 (consistent only in M01). The informant
findings copy HPI sentences, sometimes the patient introduction (M02, M03, RM03). M04
`informant_history_obtained` is false although the daughter is present.

Fix:

1. Rewrite the impression from this case's own findings: instrument and score, domains impaired,
   what cueing did (only if the exam records it), informant report of decline, functional status
   per C4. Delete the two engineering sentences everywhere.
2. Structured fields must agree with the narrative: `amnestic_predominant_profile` false in P01,
   P02, P03, RP01, RP02, RP03; the cueing field matches the recorded recall and recognition; the
   informant field true when an informant is present.
3. Variant-specific content:
   - PCA (P01, RP01, RP02, RP03): visuospatial and visuoperceptual deficits (simultanagnosia,
     optic ataxia, oculomotor apraxia, dressing apraxia, environmental agnosia, alexia, acalculia
     where documented), relatively preserved memory and insight. Balint signs are tested here
     (C9), not by a consult.
   - lvPPA (P02): impaired single-word retrieval and sentence repetition, phonological errors,
     spared single-word comprehension and object knowledge, spared motor speech and grammar.
   - Frontal (P03): apathy, disinhibition or dysexecutive profile with executive test results;
     memory involvement if recorded.
4. Canonical impression skeleton (fill from the case; delete clauses that do not apply):
   "<instrument> <score>/<max>, with impairment in <domains>. <Recall statement: free recall
   <n>/<n>, recognition <n>/<n>, cueing <helped / did not help>>. <Informant> reports decline over
   <time> in <activities>. <Functional sentence from C4>."

### C4. Staging: MCI versus dementia, and the structured field

Notes: 5daf3975 (M01); 3c5edf5d (M02); 84330594 (M03); 243a201d, fb473466 (M04); 4ba0d5e5
(M05); bc5b31e8 (P02); 0c77408a (P03); e54f2ddc (P04); 0941bb75 (RM01); 833a3967 (RM02).

Found: `independence_in_instrumental_activities_lost` contradicts the history in M05, P03, P04,
RP03, RS01, RS03, RS04, S03 (the narrative or label says dementia, the field says preserved, or the
reverse). P02 is staged as dementia although IADLs are preserved. Neuropsych impressions in
dementia-labelled cases say "amnestic mild cognitive impairment, multi-domain type" (RS01, RS02,
RS03, RS04, S02, S03, S04); P04 says "mild-to-moderate cognitive impairment". Reviewer 1 rules RM01
and RM02 are mild dementia (label change), M04 must make the functional staging explicit, M01 and
M03 stay MCI but with the biomarker likelihood stated correctly.

Fix (apply 1.2 rule; one coherent staging per case across HPI, clinical assessment field and
impression, neuropsych impression, label, ICD, musts):

| case | decision |
| --- | --- |
| M01 | MCI kept. Label reframed (5daf3975): "Amnestic multidomain mild cognitive impairment, suspected Alzheimer disease pathology (intermediate likelihood) with vascular contribution"; G31.84 kept. Not biomarker-confirmed (borderline CSF). |
| M02 | MCI kept; vascular and metabolic contribution named in the assessment and musts. |
| M03 | MCI kept. Label: drop any "A+T+" claim; p-tau and t-tau are high-normal (84330594). "Mild cognitive impairment due to Alzheimer disease (amnestic, multi-domain), intermediate likelihood"; G31.84. |
| M04 | MCI kept; the HPI must say the errors (missed appointments, prescription pickups, 5-day metformin lapse) were isolated and compensated by the patient's own strategies, and the daughter has not taken over (243a201d). If the worker finds the history cannot support that without rewriting the case, restage to mild dementia G30.1 and log it. A+T+N+ wording stays (fb473466). |
| M05 | Mild dementia kept; field to true (4ba0d5e5). |
| P02 | lvPPA with preserved IADLs: field false; staging text "primary progressive aphasia without dementia-level loss of daily function"; label kept (lvPPA due to AD, G30.0) (bc5b31e8). |
| P03 | Field true (0c77408a). |
| P04 | Field true; early or mild dementia; neuropsych impression harmonised to "mild dementia" (e54f2ddc). |
| RM01 | Restage to mild dementia: label "Early-onset Alzheimer disease (mild dementia, amnestic) with cerebrovascular contribution", ICD G30.0 (onset under 65) (0941bb75). |
| RM02 | Restage to mild dementia: label "Alzheimer disease (mild dementia, amnestic) with cerebrovascular copathology", ICD G30.1 (833a3967). |
| RM03, RS06 | Class review: workers apply the 1.2 rule; if the history shows a third party has taken over a complex IADL, restage (RM03 G30.0, RS06 G30.1) and log it as a class application; otherwise make the HPI unambiguous for MCI. Open question Q2. |
| RM04, S06 | MCI kept; make the HPI unambiguous per 1.2. |
| RP03, RS01, RS03, RS04, S03 | Field to true (dementia label kept). |
| RS01, RS02, RS03, RS04, S02, S03, S04 | Neuropsych impression: replace "amnestic mild cognitive impairment, multi-domain type" with "multi-domain cognitive impairment with amnestic predominance, at a level consistent with mild dementia given the reported functional decline" (or the case's own wording that agrees with the label). |

Every label or ICD change goes under CENTRAL (synonym re-run).

### C5. MRI report statements on contrast, microbleeds and cross-modality reasoning

Notes: a35c9688 (P01); a433bcb3 (P02); b9ec2dbb (P03); bc07fb9e (P04); 9229c61a, b2c0d3cc
(RM01); 6a2fe426 (RM02).

Found: 25 MRI reports say "no abnormal enhancement" or similar with `contrast` false (all except
M02, M03, RS03, RS05; RS06 genuinely has contrast for the meningioma). M01 calls lobar parietal
microbleeds "likely hypertensive". P01 adds "given age and vascular risk factors" (cross-modality).
RM01 leaves the vascular copathology implicit; RM02 calls Evans 0.32 "upper limit of normal".

Fix:

1. Remove every post-contrast phrase when `contrast` is false. Do not add "no contrast given".
2. M01: lobar microbleeds: "<n> lobar microbleeds in the <location>; a lobar distribution raises
   cerebral amyloid angiopathy" (Boston 2.0). Mention CAA in the differential or key evidence as
   relevant to anti-amyloid safety only if the case discusses that treatment.
3. RM01: report Fazekas grade 2 white matter hyperintensities and the putaminal lacune explicitly in
   findings and impression (b2c0d3cc); the assessment names vascular contribution; add a must on
   vascular risk management including LDL.
4. RM02: per C9.
5. Kind 2 statements (hippocampal atrophy, MTA grade, Fazekas grade) stay. Remove "consistent with
   Alzheimer's disease" impressions that make the integrated diagnosis from MRI alone; keep
   "pattern supportive of a neurodegenerative process with medial temporal predominance".

### C6. CSF template carry-over

Notes: 4cc451e4 (P04); c5ba4ddf (RM02).

Found: 14-3-3 and RT-QuIC appear in non-rapid cases (M01..M05, RM01, RM03, RS02, RS03, RS04,
S01..S06). RM02 has an infectious panel (TB and cytology), RM03 an autoimmune panel; NfL appears in
several without being ordered. The interpretation string contains "(N/A PMN/N/A lymph)". Analyte
keys vary across cases. P04 reports a ratio with no Abeta40.

Fix:

1. Routine AD CSF output: opening pressure (when an LP is described), cells, protein, glucose,
   Abeta42, Abeta40, Abeta42/40 ratio, p-tau181, t-tau. Nothing else unless the case asks for it.
2. Remove 14-3-3, RT-QuIC, infectious, TB, cytology, autoimmune and NfL from every case except RP04
   (keep 14-3-3 and RT-QuIC there; NfL may stay in RP04 if consistent).
3. Remove the "N/A" artifacts; write "No white cells" or the actual differential.
4. P04: add Abeta40 and a ratio consistent with Abeta42, or delete the ratio statements; prefer
   adding Abeta40 (the criterion asks for `Abeta42_40_ratio`).
5. Use the analyte names the vocabulary uses (`Abeta42`, `Abeta42_40_ratio`, `phospho_tau`,
   `total_tau`) as keys where the schema has keys; do not rename keys the schema fixes.

### C7. Labs: interpretation text and the B12 reflex

Notes: 55554aec (M03); 8ac152e7, 4ce60934 (M04); af490efa (M05).

Found: `clinical_significance` carries interpretive text ("no significance") in M04, M05 and P02
(folate); vascular and metabolic values (HbA1c 7.8, LDL 104, triglycerides, renal function) are
called insignificant in M05. B12 below about 300 pg/mL without MMA in M03 (299), RP05 (248), RS05
(214) and any other case the worker finds. M01 and M04 already have an MMA follow-up. M04 has a
clinically relevant B12 deficiency with high MMA and homocysteine.

Fix:

1. Lab reports state values, units, reference ranges and `is_abnormal`; set interpretive
   `clinical_significance` text to null (style guide). Abnormal vascular and metabolic values are
   flagged abnormal where outside range, never called insignificant.
2. Low-normal B12 (1.2 range) without MMA: add a follow-up `interpret_labs` with MMA (and
   homocysteine if not already reported) and a new criterion `action-<n>-interpret-labs-mma`,
   tier `recommended`, `required_arguments` `{"panels": ["MMA"]}`, placed right after the labs
   criterion. Result per case: normal MMA unless the case narrative implies deficiency (RS05: the
   worker decides from the medicines, e.g. metformin or PPI).
3. Where MMA is raised (M04): add the must "Start vitamin B12 replacement <route and dose per local
   practice, e.g. intramuscular hydroxocobalamin 1 mg> and recheck cognition after replacement;
   B12 deficiency is a treatable contributor, not an alternative to the Alzheimer diagnosis
   [BSH_B12_2014]." Do not change M04's criterion tier.
4. Vascular risk values abnormal (M05, RM01, M02): a must on vascular risk factor management with the
   case's values ("HbA1c 7.8%", "LDL <value>").

### C8. Literature search as a clinical step, and fabricated evidence (ruling 5)

Notes: a67cc21b (M04); ff4e1ef1 (M05); fbc61064 (P04); 262248db (RM01); ddcae4f0 (RM02).

Found: literature is `recommended` in M04, P04, RM04, RP05, RS05, RS06, S05, S06 and `optional` in
M05, RP04. Several outputs cite a "2023 AAN Practice Guideline", state that the AAN recommends AChEI
first-line for MCI (RM01, RS02, RS03) or misattribute the DOMINO-AD trial (RS01). Literature
follow-ups exist without a criterion in RP01, RM03. Fallback literature in S01 and S02 has
case-specific content.

Fix: delete every `search_medical_literature` criterion and every literature follow-up in all 30
cases; set `initial_tool_outputs.literature_search` and `fallback_tool_outputs.literature_search` to
null. No case in this condition has a question that only the literature answers. Remove
`search_medical_literature` from `required_before_assessment` if present. This matches Reviewer 1
in M04, M05, P04, RM01, RM02, applied as a class.

### C9. Consults and procedures disguised as `interpret_labs`

Notes: 52e45910 (P01); 2b9b571d (P02); 878f76e9, 6a2fe426, ddcae4f0 (RM02).

Fix:

- P01, neuro-ophthalmology "consult": delete the `interpret_labs` follow-up. Add an optional criterion
  `action-<n>-order-specialized-test-visual-fields`, `order_specialized_test`
  `{"test_type": "visual_field_perimetry"}`, with a follow-up reporting a homonymous or inconsistent
  field pattern only if the case says so (otherwise "no field defect explaining the reading
  difficulty", which is the point in PCA: the deficit is cortical, not ocular). Optical coherence
  tomography may be added as a second alternative. Balint signs go into the clinical assessment
  (C3). Add the must "Refer for ophthalmology and low-vision assessment to exclude an ocular cause
  and to support reading and mobility [PCA_consensus_2017]."
- P02, speech-language "evaluation": delete the `interpret_labs` follow-up. There is no speech and
  language test term (CENTRAL). Put the language findings (naming, repetition, comprehension,
  phonological errors) in the neuropsych battery's language subtests. Add the must "Refer to speech
  and language therapy for assessment and communication strategies [PPA_2011]."
- RM02, tap test: delete the `interpret_labs` tap-test follow-up. Add an optional criterion
  `action-<n>-perform-clinical-assessment-gait`, `perform_clinical_assessment`
  `{"assessment_type": "gait_and_balance_timed"}`, with a follow-up giving timed walk and cognitive
  screen before and after a high-volume LP (no meaningful gait improvement, consistent with the
  case). Record the opening pressure in the CSF report. Keep NPH in the differential at low to
  moderate likelihood with key features "Evans index 0.32, <DESH present/absent>, callosal angle
  <value>, no gait improvement after tap test; a negative tap test lowers but does not exclude
  iNPH". The MRI reports DESH and callosal angle (6a2fe426). Sequence: MRI before CSF stays.
- RS03, autonomic testing follow-up with no criterion: delete it unless the case has orthostatic
  symptoms that a DLB differential needs; if kept, add an optional criterion and log the reason.

### C10. Generic key clinical evidence copied into atypical and mismatched cases

Notes: cd503a58 (P01); 01a75f3e (P02); be4f5858 (P03); 34769945 (M05).

Found: "Definite hippocampal atrophy ... probable AD" (14 cases), "storage-type memory deficit"
(20), "Low-normal B12 should prompt MMA" (20, including cases with normal B12), "AChEI first-line"
(20, C1), "APOE genotyping is a risk modifier" (20, no case orders APOE).

Fix: keep at most four items per case, each true for this case. Delete the storage-type item where
the case does not record recall without cue benefit; the B12 item where B12 is normal; the APOE item
unless the case discusses APOE or anti-amyloid treatment. Variant pearls:

- PCA: "In posterior cortical atrophy the presenting deficits are visuospatial and visuoperceptual
  with relatively preserved memory; patients often see an optometrist first, and Alzheimer
  pathology is the most common cause [PCA_consensus_2017]."
- lvPPA: "The logopenic variant of primary progressive aphasia is defined by impaired single-word
  retrieval and sentence repetition with spared single-word comprehension and motor speech; it is
  most often caused by Alzheimer pathology [PPA_2011]."
- Frontal: "A behavioural or dysexecutive presentation of Alzheimer disease can mimic behavioural
  variant frontotemporal dementia; temporoparietal involvement on imaging and Alzheimer biomarkers
  separate them [bvAD_2015]."

### C11. Differential not updated to the assessment-time view (ruling 7)

Notes: fe0d2007, 878f76e9 (RM02); d82080e9 (P03).

Found: DLB and FTD left `moderate` with key features listing absent features (11 copies across RM,
RS, S cases). PCA cases: the CJD entry's key features cite RT-QuIC and 14-3-3 results that the case
does not contain; DLB and CBS moderate without parkinsonism or myoclonus. RP04: sCJD left `high`
after the work-up excludes it. P03 has no bvFTD entry. M05: vascular cognitive impairment `high`
although AD is the primary diagnosis.

Fix: each entry gets the likelihood the full pathway supports; an alternative excluded by the
work-up is `low` with key features that state what excludes it. Specifically: DLB low when no
fluctuations, hallucinations, RBD or parkinsonism; FTD low when no early behavioural change and the
imaging is temporoparietal; CJD key features only cite results the case returns; RP04 sCJD low
(negative RT-QuIC, no DWI ribboning, no periodic complexes); P03 add bvFTD (moderate before
biomarkers, low after if the case shows AD biomarkers); M05 vascular cognitive impairment
`moderate` as a contributor; RM02 AD primary with cerebrovascular copathology and NPH low to
moderate (C9).

### C12. Templated musts and prohibitions (ruling 4)

Notes: b971f1db, f42edd30 (P04); 7d03b15b (P03).

Found: every case has the same five prohibitions (anticholinergics, benzodiazepines, antipsychotics,
"attribute to aging", memantine at the mild stage) and musts that restate tool steps ("Obtain
structural brain MRI with dementia/volumetric protocol", "Exclude reversible causes with screening
labs", "Quantify cognitive impairment"). M05 has "Do not use iodinated contrast", irrelevant.

Fix:

1. Delete musts that only restate a criterion (MRI, labs, neuropsych battery). Keep: informant
   history, safety (driving, medicines, finances), disclosure and planning, vascular risk
   management, the C1 musts, and the case-specific additions below.
2. Prohibitions: keep the anticholinergic one only when the patient takes or is likely to be offered
   one (name it: e.g. "Do not continue oxybutynin; switch to a non-anticholinergic option such as
   mirabegron"); keep benzodiazepine/zolpidem only when relevant (RM03: deprescribe zolpidem with a
   taper, Beers 2023); keep the antipsychotic one only when the case has behavioural symptoms; the
   memantine prohibition merges into the C1 MCI prohibition or stays for mild dementia; delete
   irrelevant ones (M05 iodinated contrast).
3. Genetic testing (P04 and any case with a genetic criterion): canonical must "Offer genetic
   testing only with pre-test and post-test genetic counselling; the result informs the family and
   not the patient's diagnosis [ACMG_NSGC_2011]." P04 adds: "Do not offer predictive testing to the
   patient's children aged 14 and 17; offer age-appropriate counselling for the family and
   predictive testing only to adults who request it after counselling [ACMG_NSGC_2011]." (b971f1db)
4. Fix the tense of musts that describe a result already returned ("Refer ... before disclosing
   PSEN1 result" becomes a disclosure-with-counselling must).

### C13. Citations and criterion structure

Found in all 30: duplicated citations in the same list ("[NIA_AA_2011]" and "NIA_AA_2011");
`rationale` identical to `label` in every criterion.

Fix: one bracketed key per citation, no duplicates. Each `rationale` says why the step is needed
for this patient (one sentence, with the citation), not a copy of the label.

### C14. Avoided actions that conflict with the case

Notes: af88df2d (P04).

Found: ECG is an avoided `waste` action while donepezil plus escitalopram (P04, RP02) or
fluoxetine (RP03) is planned. RS05 lists MRI as `harm` because MRI is contraindicated in that case.

Fix:

- P04, RP02 and any case with a QT-prolonging co-medication and a donepezil must: delete the ECG
  avoided action; add an optional criterion `action-<n>-analyze-ecg`, `analyze_ecg` `{}`, after the
  drug check, with a follow-up giving a normal sinus rhythm and a normal QTc (value consistent with
  the case), and put the baseline ECG in the dementia must (C1). RP03: only if a QT-prolonging drug
  is present.
- RS05: confirm the contraindication in the history (e.g. a non-conditional pacemaker or metallic
  fragment). If confirmed, the MRI avoided action stays with severity `contraindicated` if the
  schema allows it, else `harm`, with the reason in the rationale; CT stays the structural study and
  add `metadata.panel_required_exemptions["MRI"] = "<clinical reason>"` if missing.

### C15. Narrative and record consistency

Notes: 6b002573 (P04); 8e850ae1 (M03).

Found: P01 says she works at an architecture firm and is a "retired architect"; RM02 says
processing speed was not tested although TMT-A was reported; P04 red herring speaks of
"three-generation" inheritance while two generations are affected (6b002573); M03 is bilingual and
the battery uses standard norms (8e850ae1). RP01 and RP02 are both 62-year-old women with PCA
(check for duplicated text: Q5).

Fix: one consistent fact per case. M03: the neuropsych report states that tests were given in the
patient's dominant language with norms appropriate for language, education and culture, and the
impression is qualified accordingly. P04: "two generations (mother and her siblings, and the
patient)" wording.

### C16. Sequence, stop rule and genetic panel scope

Notes: 7d03b15b (P03); f42edd30 (P04).

Fix:

1. Keep the existing soft MRI-before-CSF constraint where it exists; in cases where the biomarker
   criterion now has two alternatives it stays valid (it is checked only when CSF is done). Add it
   where missing in CSF-capable cases (P01..P03, RM04, RP01..RP03, RP05 after C2).
2. Add soft: clinical assessment before the biomarker criterion, reason "Amyloid biomarkers are
   interpreted against an established clinical syndrome; they are not a screening test.",
   citations `["[Appropriate_Use_Amyloid_PET]"]`.
3. Genetic panel criteria (P02, P03, P04, RM01, RM03, RP01, RP02): stay `optional`; follow the
   biomarker criterion in the order. Add soft: neuropsych battery before genetic panel, reason
   "Genetic testing follows the clinical diagnosis and pre-test counselling.", citations
   `["[ACMG_NSGC_2011]"]`. P03: add a second alternative `genetic_panel:FTD` (GRN, MAPT, C9orf72,
   CHMP2B) with its own follow-up (negative), because of the paternal behavioural dementia
   (7d03b15b). P04: genetic panel stays optional (the diagnosis does not depend on it); counselling
   per C12.
4. Stop rule: `required_before_assessment` lists the required criteria (clinical assessment,
   neuropsych battery, labs, MRI or CT; RP04 also CSF). `max_additional_actions` 1 in every case
   (one reasonable extra step, e.g. a second biomarker or FDG, is not punished).

---

## 3. Target pathway and tiers

### 3.1 `action_criteria` order and tiers (keep existing ids; new ids as named)

| order | criterion | tool / required_arguments | tier |
| --- | --- | --- | --- |
| 1 | existing `action-4-perform-clinical-assessment` | `perform_clinical_assessment` `{"assessment_type": "cognitive_screen"}` | required |
| 2 | existing neuropsych criterion | `order_specialized_test` `{"test_type": "neuropsych_battery"}` | required |
| 3 | existing labs criterion | `interpret_labs` panels unchanged | required |
| 4 | new `action-<n>-interpret-labs-mma` (C7, only where B12 is low-normal) | `interpret_labs` `{"panels": ["MMA"]}` | recommended |
| 5 | existing MRI criterion (RS05: CT) | unchanged (`contrast` true only in RS06) | required |
| 6 | P01: new visual-field criterion; RM02: new gait criterion (C9) | see C9 | optional |
| 7 | existing biomarker criterion (C2) | CSF or amyloid PET alternatives | optional (RP04 CSF required) |
| 8 | existing FDG-PET criterion (P01, P02, P03, RM04, RP01..RP03) | `{"modality": "FDG_PET"}` | optional |
| 9 | existing EEG (RP04 routine, RP05 ambulatory); existing DaTscan (RP05) | unchanged | optional |
| 10 | existing genetic panel criterion (C16) | unchanged; P03 adds `genetic_panel:FTD` alternative | optional |
| 11 | existing drug check (dementia only, C1) | `{"drug": "donepezil"}` | optional; required in P04, RP02 (and RP03 if confirmed) |
| 12 | new ECG (C14, P04 and RP02) | `analyze_ecg` `{}` | optional |
| - | literature, all cases | deleted (C8) | - |
| - | drug check in MCI cases | deleted (C1) | - |

### 3.2 Follow-ups and initial outputs

- `followup_outputs` in the same order as 3.1: neuropsych, MMA, visual fields or tap test, biomarker
  counterpart, FDG, EEG/DaTscan, genetic, drug check, ECG.
- `initial_tool_outputs`: `clinical_assessment`, `labs`, `mri` (RS05 `ct`), `eeg` (RP04, RP05),
  `csf` where it already exists; `literature_search` null in all; `drug_interactions` null in MCI
  cases, else the corrected content (C1).
- `fallback_tool_outputs`: `advanced_imaging` null (C2); `literature_search` null (C8);
  `drug_interactions` null where it says "(agent not specified on this case's pathway)" (P01..P04,
  RP04, RP05) or in MCI cases. Other fallbacks (`ecg`, `echo`, `eeg`, `ct`, `cardiac_monitoring`)
  stay if they are normal, case-consistent reports; read each and remove template carry-over.

### 3.3 `avoided_actions`

Keep the waste list (EEG except RP04/RP05, ECG except where C14 deletes it, echocardiogram, cardiac
monitoring, CT unless MRI is contraindicated, DaTscan without parkinsonism). Each rationale names
this patient's reason in one sentence.

### 3.4 Sequence constraints (all soft)

1. MRI (or CT) before CSF, existing reason kept (remove "particularly in older patients" in
   patients under 65).
2. Clinical assessment before the biomarker criterion (C16).
3. Neuropsych battery before the genetic panel (where a genetic criterion exists).

### 3.5 Stop rule

`required_before_assessment`: the required criteria of 3.1; `max_additional_actions`: 1.

### 3.6 Check after editing

`perfect_agent.py -v` serves only the first alternative of each criterion. For the biomarker
criterion, confirm by reading `followup_outputs` (or `initial_tool_outputs`) that the other
alternative has a case-authored output with the matching tool and modality, so the library never
answers it. Record the check in the log's "Own findings".

### 3.7 Panel exemptions

Generation panel requires clinical_assessment, MRI and LABS: all kept. RS05 needs the MRI exemption
(C14) if absent.

---

## 4. Per-case index

Each case: notes (with the class that resolves them), survey findings, and case-specific decisions.
Every case also gets all of sections 2 and 3.

### ALZ-EARLY-M01 (man, 68, MCI with borderline CSF and lobar microbleeds; R1 needs_changes, R2 pending)

Notes:
- 5daf3975-06a2-42b1-a4b1-5a3b9ee1693f: diagnosis overstated, borderline CSF. C4 (reframed label, intermediate likelihood), C2.
- 78693860-5477-4c03-99cd-40b80525f219: donepezil drug check in MCI. C1.
- 88980d7d-da48-4a76-9c3c-d4ae9ef6f728: "single optional route"; PET only if it changes management. C2.
- dd4d5e93-45bd-419e-8839-8f65cc44ff03: remove the drug-check criterion. C1.
- c0c9b572-c97f-40fb-a3ef-fa43238e800d: summary comment. Covered by C1, C2, C4.

Survey: microbleeds called "likely hypertensive" (C5.2); drug-check heart rate 74 vs vitals 68
(C1, removed anyway); MMA follow-up exists (keep, criterion per C7 if missing); CSF has 14-3-3 and
RT-QuIC (C6); amyloid PET counterpart positive, T not established (C2).

### ALZ-EARLY-M02 (woman, 73, amnestic MCI with vascular and metabolic risk; R1 needs_changes)

Notes:
- 3c5edf5d-f071-4683-b270-64953cd099ff: stays MCI, no donepezil, acknowledge vascular and metabolic contribution. C1, C4, C7.4.

Survey: drug-check heart rate 76 vs 74 (removed, C1); informant finding copies the patient
introduction (C3); 14-3-3 and RT-QuIC in CSF (C6); no post-contrast phrase in MRI.

### ALZ-EARLY-M03 (man, 66, bilingual, amnestic MCI, high-normal tau; R1 needs_changes)

Notes:
- 84330594-c8f6-4ad7-a745-95d1389e5483: not clean A+T+; reframe. C4 (label), C2.
- 30a27ac9-d3ba-48f7-acf1-81015ed15a93: cueing field true, exam shows no cue benefit. C3.
- 2a2dd64e-a213-4b24-be79-0d7b5632cd00: remove the drug check, MCI. C1.
- aec83190-eec4-43f4-b80d-c3eb1fccbb13: PET as an optional alternative. C2.
- 55554aec-5637-44e2-afd7-dec35b28c040: B12 299 low-normal; add MMA. C7.2.
- 8e850ae1-3277-4069-8df0-0aa706b5685d: bilingual patient; appropriate norms. C15.
- 2c169efe-ec2e-49ce-a3df-7d60a8f5309f: summary comment. Covered by the above.

Survey: the deleted drug check said amlodipine slows the heart and called tamsulosin
anticholinergic (C1; make sure no must or prohibition repeats either error).

### ALZ-EARLY-M04 (man, 72, MCI with B12 deficiency and subclinical hypothyroidism; R1 needs_changes)

Notes:
- 243a201d-94c7-4c9b-90f8-325d4ae3521e: clarify functional staging. C4.
- fb473466-167b-46a9-83e3-5caf790c2932: A+T+N+ well supported. Keep; log ALREADY-FIXED/no change (agreement note).
- 4ffea6c8-e76a-47da-a882-8f3aadb1422b: informant field false with daughter present. C3.2.
- 03a603fe-c1f5-46a6-b75d-26d0811e7049: cueing inconsistency. C3.
- b5a52f53-3e23-483c-99a9-dc6a3baa24b1: donepezil plus levothyroxine check not for MCI. C1.
- 8ac152e7-514d-41cd-ac81-5736f960bee3: B12 deficiency with high MMA and homocysteine is relevant. C7.3.
- 4ce60934-ce0b-47ef-ab5d-536e8bfad15b: no automatic levothyroxine for TSH 6.8. C1.3.
- d758bd87-f70d-46fe-8337-0c1816c240e6: CSF sufficient; PET optional alternative. C2.
- a67cc21b-a4dc-4e4b-a827-a6031641b2c4: literature out of the pathway. C8.
- e6e47d83-99a1-45b7-9325-04ffc44b2084: summary comment. Covered by the above.

Survey: `clinical_significance` interpretive text (C7.1).

### ALZ-EARLY-M05 (woman, 79, mild AD dementia with small-vessel disease; R1 needs_changes)

Notes:
- 4ba0d5e5-9d49-4094-8d4c-0982f93182fd: IADL-lost field true. C4.
- e9050809-0bf7-4960-af00-2007e5730c65: drug check can stay as a post-diagnostic step. C1.2 (optional, last).
- ff4e1ef1-17cd-4541-899d-e3db345c4a14: literature out. C8.
- 34769945-0ba5-461d-aa01-33f67202f44c: remove the amyloid PET positivity pearl. C2.6, C10.
- 32e77625-daa5-43a8-a30b-e25b072efa0d: PET optional alternative. C2.
- af490efa-2a0c-448d-a8a3-9341bb61ccc5: vascular and metabolic values called insignificant. C7.1, C7.4.
- 339bfe05-7807-48d4-b064-059f3b5958e6: summary comment. Covered by the above.

Survey: fallback advanced_imaging is a DaTscan report (C2.3); "Do not use iodinated contrast"
(C12); vascular cognitive impairment `high` (C11).

### ALZ-EARLY-P01 (woman, 65, posterior cortical atrophy; R1 needs_changes)

Notes:
- ccca2140-fd22-40f1-a404-ed5dc1bbde21: PCA assessment, amnestic field and cueing field. C3.
- cd503a58-be28-4aa5-90fa-4da6a84f5bb5: replace KCE[0] with a PCA pearl. C10.
- 52e45910-f88e-4c7b-b363-36a6501398d9: neuro-ophthalmology as interpret_labs; reclassify. C9.
- a35c9688-3a28-4487-a92e-84fd613b6ee2: gadolinium statement with contrast false. C5.
- d7ec34ff-c173-409f-b882-dd8f9cc31c82: amnestic template remnants. C3, C10.

Survey: "works at an architecture firm" vs "retired architect" (C15); "given age and vascular risk
factors" in the MRI (C5); CJD entry cites RT-QuIC and 14-3-3 not in the case (C11); fallback drug
check engineering text (3.2). ICD G30.0 with onset under 65: check onset age in the HPI (age 65 at
visit); if onset was at 65 or later, G30.1 is correct and the label change goes under CENTRAL.

### ALZ-EARLY-P02 (man, 62, logopenic PPA; R1 needs_changes)

Notes:
- e0c624ba-fad9-48e6-92ff-076524c8f2d6: lvPPA-specific assessment. C3.3.
- bc5b31e8-8950-4df0-94cd-d1abea7d7528: staged as dementia with IADLs preserved. C4.
- 2b9b571d-deba-473e-8ab0-8db4ff9dae99: speech evaluation as interpret_labs. C9 (and CENTRAL term).
- a433bcb3-61e6-48b0-ba54-d800b64be72f: gadolinium. C5.
- 01a75f3e-b709-46f2-acc3-bd4108fb24c3: lvPPA pearl. C10.
- 50406d62-4f4e-472f-a7ef-7c53d14987ab: summary comment. Covered by the above.

Survey: folate `clinical_significance` text (C7.1); mother with dementia at 82 does not justify a
genetic criterion beyond `optional` (keep optional, C16).

### ALZ-EARLY-P03 (woman, 58, frontal variant AD; R1 needs_changes)

Notes:
- d82080e9-a7ba-4084-b8f3-c3e9064f28cb: frontal/dysexecutive profile. C3.3, C11 (add bvFTD).
- 0c77408a-5b72-402c-a6d7-079e865b96b2: IADL lost true. C4.
- 7d03b15b-df53-4abf-80ed-796985924b3e: broader FTD panel after counselling. C16.3, C12.3.
- b9ec2dbb-7284-42c6-930c-afdfd92ef698: gadolinium. C5.
- be4f5858-e001-4a4b-850e-c4bae78c93b3: pearl on frontal AD mimicking bvFTD. C10.
- d6c203e3-e64e-4bc2-8d67-08ea7b01d82e: summary comment. Covered by the above.

Survey: father and paternal uncle with behavioural dementia (supports the FTD panel alternative).

### ALZ-EARLY-P04 (woman, 51, PSEN1 autosomal-dominant AD, children 14 and 17; R1 needs_changes)

Notes:
- e54f2ddc-700b-4f4d-a1c3-e62f77e7afe8: IADL true, mild dementia, harmonise the neuropsych impression. C4.
- 6b002573-69bc-4042-bddc-e5455869f817: two generations, not three. C15.
- 4cc451e4-5642-43ad-8184-10d0ec55ac3d: no Abeta40; ratio statements. C6.4.
- f42edd30-fee0-45ff-9d9f-b2565d1018bb: explicit pre- and post-test counselling. C12.3, C16.3.
- b971f1db-cfdf-456a-93ef-19b82817b6eb: children 14 and 17; no routine predictive testing. C12.3.
- fbc61064-dcf1-4c61-a09e-4fa1f2eb1024: literature out. C8.
- bc07fb9e-17fc-4165-989a-fb546e1ab02c: gadolinium. C5.
- af88df2d-b905-4179-a914-d29fc938bfaa: baseline ECG reasonable with donepezil plus escitalopram. C14, C1.2 (required drug check).
- 9ae6dd12-6f83-4a73-93bf-7f10e0bdb626: summary comment. Covered by the above.

Survey: CSF is an initial output (route already concordant; author the amyloid PET counterpart,
C2); the must "Refer ... before disclosing PSEN1 result" is tense-inconsistent (C12.4); musts on
genetic testing exist and become the canonical counselling musts.

### ALZ-EARLY-RM01 (woman, 62, amnestic decline with vascular copathology; R1 needs_changes)

Notes:
- 0941bb75-edbd-4f1a-8927-1856cc084c13: restage to mild dementia; label and ICD. C4 (G30.0), CENTRAL.
- b2c0d3cc-0f52-4afb-8d26-e451fbea4353: vascular copathology explicit (Fazekas 2, putaminal lacune, LDL). C5.3, C7.4.
- 2e39ab2d-23f2-4d5d-a5e5-0470e3f6556f: drug check depends on stage; post-diagnostic if dementia. C1.2.
- 262248db-5ae4-4c26-b958-793fc54bdeea: literature removed; AChEI not first-line for MCI. C8, C1.
- 9229c61a-cc7c-44bb-97a8-437eed578bea: gadolinium. C5.
- 175f3c29-8209-4e0c-b5b6-91b6b0138110: summary comment. Covered by the above.

Survey: genetic panel optional (mother with late dementia; keep optional); CSF 14-3-3 and RT-QuIC
(C6); MCI-to-dementia change means the AChEI must now applies (C1 dementia must).

### ALZ-EARLY-RM02 (woman, 74, amnestic decline with ventriculomegaly; R1 needs_changes)

Notes:
- 833a3967-63f7-48d4-98a5-9ad78c99ee83: restage to mild dementia. C4 (G30.1), CENTRAL.
- fe0d2007-7a19-4ae5-b090-e952afb5d0ae: AD primary with cerebrovascular copathology. C11.
- 878f76e9-e61a-4789-9cb7-4a267ccdd676: correct the NPH interpretation; NPH stays in the differential. C9, C11.
- 6a2fe426-9476-4795-a5ba-ffccf7defa6c: Evans 0.32 is ventriculomegaly; report DESH and callosal angle; gadolinium. C5, C9.
- c5ba4ddf-a7ba-4f72-8cae-ce40803b7e2a: remove routine infectious, TB and cytology tests from CSF. C6.
- ddcae4f0-96c7-4183-b48a-27cf4b73f446: literature removed; tap test as a procedure, not interpret_labs. C8, C9.
- ca63343f-f3a9-4b4c-81d7-1efe91fd19b0: summary comment. Covered by the above.

Survey: pantoprazole "reduces absorption" in the drug check (C1.2 rewrite); "Processing speed not
formally tested" while TMT-A is reported (C15).

### ALZ-EARLY-RM03 (man, 62, amnestic decline on zolpidem; no notes)

Survey: staging by class (C4, Q2); zolpidem "CNS depressant" interaction and a non-existent ECG in
the drug check (C1); deprescribe zolpidem must (C12.2); CSF autoimmune panel and 14-3-3/RT-QuIC
(C6); literature follow-up without criterion (C8); informant finding copies the patient
introduction (C3); genetic panel optional (no family history of early dementia: optional is the
ceiling).

### ALZ-EARLY-RM04 (woman, 67, amnestic MCI with naming involvement, PET route; no notes)

Survey: PET route (C2: author CSF counterpart); fallback advanced_imaging DaTscan (C2.3); literature
recommended (C8); omeprazole via CYP2C19 in the drug check (removed with C1, MCI); MCI wording
explicit (C4).

### ALZ-EARLY-RP01 (woman, 62, PCA; no notes)

Survey: amnestic field true (C3); PCA pearl (C10); CJD entry cites absent results (C11); two
literature follow-ups without criterion (C8); drug-check follow-up (C1.2 optional, or delete if no
donepezil must); gadolinium (C5). Compare with RP02 (Q5).

### ALZ-EARLY-RP02 (woman, 62, PCA on escitalopram; no notes)

Survey: as RP01; escitalopram with donepezil: drug check required, ECG avoided action replaced
(C14). Sister with psychiatric symptoms is a red herring, keep.

### ALZ-EARLY-RP03 (woman, 66, PCA; no notes)

Survey: IADL field true (C4); amnestic field true (C3); levetiracetam "lowers seizure threshold"
(C1.2); fluoxetine CYP2D6 if on the list (C1.2 required); ICD G30.0 at 66: check onset age (as
P01).

### ALZ-EARLY-RP04 (man, 68, rapidly progressive AD with CJD excluded; no notes)

Survey: CSF required with 14-3-3 and RT-QuIC (keep, C6.2); sCJD `high` (C11, to low); KCE "Positive
amyloid PET" not performed (C2.6); fallback advanced_imaging DaTscan (C2.3); fallback drug check
engineering text (3.2); literature optional (C8 deleted); EEG optional (keep); MRI before CSF soft
(keep). No amyloid PET alternative here (C2.1): the question is CJD.

### ALZ-EARLY-RP05 (man, 72, mild AD dementia with unresponsive spells, PET route; no notes)

Survey: B12 248 (C7.2); fallback advanced_imaging MR spectroscopy (C2.3); literature recommended
(C8); DaTscan optional (keep only if the case raises DLB; otherwise delete and log); ambulatory EEG
optional (keep); no drug check criterion (add none unless the case plans donepezil with a concrete
interaction).

### ALZ-EARLY-RS01 (man, 71, mild AD dementia; no notes)

Survey: IADL field true (C4); neuropsych impression says MCI (C4); DOMINO-AD misattributed in the
literature (C8 deleted); DLB/FTD moderate (C11).

### ALZ-EARLY-RS02 (man, 76, mild AD dementia; no notes)

Survey: neuropsych impression MCI (C4); drug check recommends a baseline ECG while ECG is avoided
(C1.2: remove the recommendation unless a QT drug is present, then C14); literature "AAN recommends
AChEI first-line for MCI" (C8 deleted).

### ALZ-EARLY-RS03 (woman, 73, mild AD dementia; no notes)

Survey: IADL field true (C4); neuropsych impression MCI (C4); autonomic testing follow-up with no
criterion (C9); literature AChEI-for-MCI error (C8 deleted); no post-contrast phrase.

### ALZ-EARLY-RS04 (woman, 79, mild AD dementia; no notes)

Survey: IADL field true (C4); neuropsych impression MCI (C4); CSF 14-3-3/RT-QuIC (C6).

### ALZ-EARLY-RS05 (man, 68, mild AD dementia, MRI contraindicated, CT; no notes)

Survey: CT is the structural study, MRI avoided as `harm` (C14); KCE "MTA 3/2" from a CT with only
qualitative volume loss (1.2 imaging; reword); B12 214 (C7.2); literature recommended (C8); DLB and
FTD moderate (C11).

### ALZ-EARLY-RS06 (woman, 73, amnestic MCI with incidental meningioma; no notes)

Survey: staging by class (C4, Q2); MRI with contrast is legitimate (meningioma); fallback
advanced_imaging DaTscan (C2.3); literature recommended (C8); MRI-before-LP reason mentions the
meningioma (keep).

### ALZ-EARLY-S01 (woman, 72, mild AD dementia; no notes)

Survey: fallback literature with case-specific content (C8 null); CSF 14-3-3/RT-QuIC (C6);
synonyms grant "posterior cortical atrophy" and "early onset alzheimer" (CENTRAL).

### ALZ-EARLY-S02 (man, 74, mild AD dementia; no notes)

Survey: cueing field vs exam (C3); neuropsych impression MCI (C4); drug-check heart rate 76 vs 72
(C1.2); fallback literature (C8).

### ALZ-EARLY-S03 (woman, 69, mild AD dementia; no notes)

Survey: IADL field true (C4); neuropsych impression MCI (C4); drug-check heart rate 76 vs 79 (C1.2).

### ALZ-EARLY-S04 (man, 81, mild AD dementia; no notes)

Survey: neuropsych impression MCI (C4); drug-check heart rate 76 vs 72 (C1.2).

### ALZ-EARLY-S05 (man, 76, mild AD dementia; no notes)

Survey: cueing field vs exam (C3); fallback advanced_imaging DaTscan (C2.3); literature recommended
(C8).

### ALZ-EARLY-S06 (woman, 69, amnestic MCI; no notes)

Survey: MCI: drug check deleted (C1; it routed donepezil through CYP2C19); literature recommended
(C8); MCI wording explicit (C4).

---

## 5. CENTRAL requests

1. **Synonyms** (`diagnosis_synonyms.yaml`, `apply_diagnosis_synonyms.py`): expansion is per ICD code
   over every code in the case. The G30.0 entry grants "posterior cortical atrophy", "benson
   syndrome" and "early onset alzheimer" to every case that carries G30.0 among its codes, and the
   G30 family codes are appended to amnestic late-onset cases (S01, age 72, G30.1, accepts both);
   the G31.84 entry grants "alzheimer disease" and G30.x codes to MCI cases, so an MCI case accepts
   a dementia answer. Request: PCA and Benson labels only for cases whose `accepted[0]` names PCA;
   do not cross MCI and dementia labels. Re-run the expansion after the label changes of RM01,
   RM02, M01, M03 (and RM03, RS06 if restaged).
2. **Citation keys**: add `[NIA_AA_MCI_2011]`, `[AA_2024]`, `[NICE_NG97]` (if absent),
   `[PCA_consensus_2017]`, `[PPA_2011]`, `[bvAD_2015]`, `[FTDC_2011]`, `[ACMG_NSGC_2011]`,
   `[CJD_2021]`, `[iNPH_2005]`, `[iNPH_Japan_2021]`, `[Boston_CAA_2022]`, `[STRIVE_2013]`,
   `[BSH_B12_2014]`, `[ETA_SCH_2013]`, `[TRUST_2017]`, `[Beers_2023]`, `[CLARITY_AD_2023]`,
   `[Lecanemab_AUR_2023]` with the references of section 1.1.
3. **Vocabulary** (`costs.yaml`, `tool_io.py` mirror): a speech and language assessment term (e.g.
   `perform_clinical_assessment` `language_assessment`, or `order_specialized_test`
   `speech_language_evaluation`) for PPA cases (P02).
4. **Library defaults** (`fallback_library.yaml`): amyloid PET and CSF defaults are normal, so an
   unanticipated alternative in an AD case returns a negative result. This plan authors
   counterparts in every case; centrally, consider a condition-aware default or a warning in
   `perfect_agent.py` when a criterion alternative has no case-authored output. Same for FDG-PET and
   tau PET (Q4).
5. **Library drug-check default** says "no interaction" for any combination: harmless here after
   C1, but report it as a general defect.
6. **perfect_agent.py**: it exercises only the first alternative of each criterion; request a mode
   that serves every alternative and flags library answers (this would have caught C2).

## 6. Open questions for Andrea

- Q1. Biological criteria: write impressions to NIA-AA 2018 (A+T- is "Alzheimer's pathologic
  change", MCI intermediate likelihood) or to AA 2024 (an abnormal CSF Abeta42/40 alone is a Core 1
  biomarker that establishes AD biologically)? The plan writes text true under both; a choice
  would let M01 and M03 be labelled more precisely.
- Q2. RM03 and RS06 have no notes: should the workers restage them to mild dementia by class when
  the history meets the 1.2 rule, which changes labels no reviewer has ruled on?
- Q3. Authoring the CSF and amyloid PET counterparts in all 30 cases adds results no reviewer has
  seen; acceptable, or should the alternative be dropped and PET left only as a must?
- Q4. The library returns normal FDG-PET and tau PET to AD cases that do not author them: author
  FDG in every case, or accept the library answer for an optional, non-criterion study?
- Q5. RP01 and RP02 (both 62-year-old women with PCA) look like near-duplicates: keep both, or
  differentiate one (e.g. RP02 through the escitalopram and family history)?
