# PD: decisions of the November 2026 round (lead, 16 Nov 2026)

Base: the working tree at commit c443a564 (after class LIT 393c547e and MRI-CONTRAST). 47 notes,
all from R1 (NB-KSC3-TWUA-QDTM), in 30 cases. No PD case is approved (`work/approved.txt` lists
none). The measurements are in `plans/PD.md` section 2. The scripts are in
`/home/aprotani/review-round-2026-11/work/scratch/pd-lead/`: `survey.txt` (criteria, avoided
actions, sequence, stop rules, musts), `classes_pd.py`, `mri_refs.py`, `exams.txt`.

Sources I verified this round (WebSearch, 16 Nov 2026):
- NICE NG71 (2017), section 1.2. Rec 1.2.9: "Do not use structural MRI to diagnose Parkinson's
  disease" [2006, amended 2017]. Rec 1.2.10: structural MRI "may be considered in the differential
  diagnosis of other parkinsonian syndromes". Rec 1.3.1 (first-line treatment): offer levodopa to
  people in the early stages whose motor symptoms affect their quality of life; a choice of
  agonist, levodopa or MAO-B inhibitor only when they do not (rec 1.3.2).
- EMA Article 31 referral on domperidone (EMA/465179/2014) and MHRA Drug Safety Update, May 2014.
  Domperidone is restricted to the relief of nausea and vomiting, at the lowest dose for the
  shortest time (usually no more than 1 week, at most 10 mg three times daily). It is
  contraindicated with impaired cardiac conduction, underlying cardiac disease, severe hepatic
  impairment, QT-prolonging drugs and potent CYP3A4 inhibitors. Risk is higher above 60.
- EASL-ERN Wilson 2025 (Socha P et al., J Hepatol 2025;82:690-728). Wilson disease is considered
  in adults with an otherwise unexplained neurological or neuropsychiatric disorder. The first
  diagnostic step is serum ceruloplasmin with basal 24-hour urinary copper. I could not see an
  age cut-off for adult movement disorders in the parts available to me, so I state none.
- 2019 ESC SVT guidelines (Brugada J et al., Eur Heart J 2020;41:655-720). An EPS is recommended
  to risk-stratify pre-excitation in defined groups. A patient with pre-excitation and syncope is
  symptomatic, not asymptomatic. I state only: "accessory-pathway risk stratification by an
  electrophysiologist (EPS), with ablation decided there".
- Tinazzi M et al., Task force consensus on nosology and cut-off values for axial postural
  abnormalities in parkinsonism. Mov Disord Clin Pract 2022;9:594-603 (MDS task force).
  Pisa syndrome is lateral trunk flexion above 10 degrees. "Lateral trunk flexion" is 5 to 10
  degrees.

Keys used as standard references, not re-verified on the web:
- MDS 2015 PD criteria (Postuma 2015) for the definitions of parkinsonism and rigidity, and the
  red-flag and counterbalancing rules. The severe-autonomic-failure red flag excludes orthostatic
  hypotension "explained by medication or other disease".
- MDS 2017 PSP (Höglinger 2017).
- MDS 2022 MSA (Wenning 2022). Established MSA needs poorly levodopa-responsive parkinsonism OR a
  cerebellar syndrome.
- Follett KA et al., Pallidal versus subthalamic deep-brain stimulation for Parkinson's disease.
  N Engl J Med 2010;362:2077-2091.
- ACG Clinical Guideline: Gastroparesis (Camilleri M et al., Am J Gastroenterol
  2022;117:1197-1220).
- ATA hypothyroidism guideline (Jonklaas J et al., Thyroid 2014;24:1670-1751).

New keys go into the pack through CENTRAL item 2: `[EMA_Domperidone_2014]`,
`[ACG_Gastroparesis_2022]`, `[ESC_SVT_2019]`, `[Tinazzi_2022]`, `[Follett_2010]`, `[ATA_2014]`.

Scorer facts I checked in `policy_reward.py` (they decide D1):
- `_coverage` returns 1.0 when a case has no required criterion.
- With an empty `required_before_assessment`, the stop rule is satisfied at once (completion index
  -1). Every unjustified action then counts as extra, and more than `max_additional_actions` (2)
  lowers `stopping`.
- Optional and recommended criteria are credited in tool accuracy and are never "extra". An agent
  that orders an optional MRI loses nothing. An agent that diagnoses from the examination alone
  scores 1.0.
- `perfect_agent.py` handles an empty work-up: it makes no call and submits.
- `test_no_case_has_a_free_required_set` skips cases with no required criterion by design.
- `test_panel_required_tools_are_present_or_exempted` is satisfied by an optional MRI criterion.

---

## D1. Structural imaging tier in clinically typical PD (class TIER-MRI)
Notes: 9d6d3209 (RS04), 7d906e55 (RS05), f4766ad1 (S01), 9e04baa6 (S02), 0dcbe488 (S03),
5ee462a7 (S04), e29754f8 (S05), 69817fd8 (RM05), and 5dcbd891 (S06, head CT).

**Decision.**
- Applies to clinically typical PD: asymmetric parkinsonism with no red flag, no atypical sign and
  no structural question raised by the history.
- In these cases the MRI (or CT) criterion becomes `optional` and leaves `required_before_assessment`.
- Applied to the 9 noted cases and, as a class (ruling 2), to six unnoted cases that meet the same
  definition: M04, M05, RM03, RM04, RS01, RS03. That is 15 cases.
- Imaging stays `required` in the other 15, each for a written reason (PD.md section 2, C1).

**Reason.** NICE NG71 rec 1.2.9 is "Do not use structural MRI to diagnose Parkinson's disease".
Rec 1.2.10 keeps MRI for the differential of other parkinsonian syndromes. This is what R1 asks.

**Conflict with October.** The October tier (MRI required in 29 cases plus CT in 1) came from R1's
July guidance "Alternatively, CT scan", which we read as a required tier. The same reviewer now
rules explicitly, and the guideline supports the ruling. The October decision is superseded in
the typical cases and kept where an atypical feature or structural question exists.

**Consequence.** 14 cases have no required criterion: S01-S06, RS03, RS04, RS05, M04, M05, RM03,
RM04 and RS01. RM05 keeps its required medication review. In these 14 the correct answer is a
clinical diagnosis with no test. The scorer rewards that, and still penalises waste and more than
two unjustified orders. This is the guideline answer, and it measures restraint, so I apply it.
It is reported to Andrea as a dataset property (PD.md section 5), not as a question.

**Canonical text** (optional MRI criterion):
- label: "Consider brain MRI only if an atypical feature or another structural question arises"
- rationale: "PD is a clinical diagnosis (MDS 2015); structural MRI is not used to diagnose PD and
  is considered only in the differential of other parkinsonian syndromes [NICE_NG71][Postuma_2015]"

S06 CT:
- label: "Consider non-contrast head CT only if structural imaging becomes indicated (MRI declined
  for claustrophobia)"
- same rationale, plus: "CT has a lower sensitivity for atypical-parkinsonism signs".
- The S06 `panel_required_exemptions.analyze_brain_mri` stays.

Evidence lines, differential entries and red herrings in these 15 cases must not rest on the
MRI (it is no longer part of the required pathway; October C15 rule). The MRI key-evidence line
becomes: "Clinically typical PD without red flags or atypical signs: structural imaging is not
needed for the diagnosis [NICE_NG71]; if MRI is obtained it shows <the stored findings>".
Differential `key_features` lead with the clinical features. An MRI clause stays only as "and,
if imaged, <finding>".

## D2. MRI-before-DaTscan soft constraint (class SEQUENCE)
Notes: e29754f8 (S05), 5dcbd891 (S06).

**Decision.** Delete the constraint in 12 of the 13 cases that carry it:
- M01, M02, M03, M04, P02, P04, RM02, RM03, RM05, RS01, S05;
- the CT-before-DaTscan constraint in S06.

Keep it only in RP05, where the referral question is vascular versus degenerative parkinsonism
(Fazekas 2). There the reason reads: "Read the DaTscan against the MRI extent and site of the
small-vessel disease: a basal ganglia vascular lesion can itself reduce striatal binding". It has
no guideline citation, so the `citations` list is empty.

**Reason.** R1 rules a fixed MRI-before-DaTscan order not mandatory. The October reason cited
`[Postuma_2015]`, which does not state this rule. I could not verify that the EANM/SNMMI 2020
procedure standard states it either. An unsourced copied rule goes (addendum).

## D3. Provisional diagnosis while metoclopramide continues (M01, M02, M03)
Notes: ee26c7b1 (M01), e851351e (M02), 811211a3 (M03).

**Decision. The label is changed: CENTRAL synonyms check.** `accepted[0]` in all three becomes:
"Degenerative parkinsonism, probably Parkinson's disease, unmasked by metoclopramide (to be
confirmed after withdrawal)". `icd_codes[0]` G20.A1 stays.

**Canonical diagnostic must** (replaces REQ[0]):
"Diagnose a degenerative presynaptic parkinsonism, most likely Parkinson's disease, unmasked or
worsened by metoclopramide: current D2-blocker exposure is an MDS absolute exclusion while it
continues, and the abnormal DaTscan shows a presynaptic dopaminergic deficit that pure
drug-induced parkinsonism does not cause, but it does not by itself establish PD (MSA, PSP and DLB
also reduce DaT binding)<, and RBD / RBD and hyposmia are not drug effects>; record the diagnosis
as provisional until the clinical reassessment after withdrawal [Postuma_2015][Marshall_2009]"

**REQ[2] (canonical):** "Reassess the parkinsonism clinically after metoclopramide has been
withdrawn (drug-induced signs can take weeks to months to resolve) and confirm Parkinson's disease
by the MDS criteria only then; the abnormal DaTscan will not normalise [Marshall_2009]"

**Add a prohibition:** "Do not record idiopathic Parkinson's disease as a definitive diagnosis
before the reassessment after metoclopramide withdrawal".

Also:
- `key_clinical_evidence` and the DaTscan criterion rationale say "supports a degenerative
  parkinsonism, not specific for PD".
- The DaTscan stays required: it separates pure drug-induced parkinsonism.
- `drug induced parkinsonism` stays in `rejected`: pure DIP is what the abnormal DaTscan excludes.
- The worker tests these answers with `DiagnosisCriterion.matches`:
  - should match: "Parkinson's disease unmasked by metoclopramide", "probable Parkinson's disease";
  - should not match: "drug-induced parkinsonism".

**Stop rule.** The reassessment is a later visit, and no tool or criterion can stand for it. The
stop rule keeps the DaTscan, the medication review and the MRI (MRI stays required here, D1). The
physician's demand that the diagnosis not be closed as definitive is met by the provisional
label, the must and the prohibition. Ruling FIXED, with this explanation in the log.

## D4. Domperidone as a routine gastroparesis substitute (class MUST-WRONG)
Notes: 004770c3 (M01), 102d4199 (M02), d0fa04ff (M03).

**Decision.** Replace REQ[1] in M01-M03 (canonical below, with the case's own clause kept: M02
glucose on glipizide, M03 weight):

"Stop metoclopramide with the gastroenterologist and choose a gastroparesis treatment without
central D2 blockade (dietary measures and glycaemic control first); any prokinetic, domperidone or
erythromycin included, is a specialist choice after review of its licensed indication, cardiac
risk and interactions: domperidone is restricted to short-term nausea and vomiting and is
contraindicated with cardiac conduction disease, QT-prolonging drugs and potent CYP3A4 inhibitors
[EMA_Domperidone_2014][ACG_Gastroparesis_2022]"

**Drug-interaction outputs** of M01-M03: replace "domperidone where available after an ECG for the
QTc" in `alternatives`, `interactions` and `warnings` with the factual EMA restriction. A
drug-check report may give category-level management.

**Class extension, RM05.**
- REQ[1] becomes: "Stop prochlorperazine and treat migraine-associated nausea without central D2
  blockade: ondansetron (not with apomorphine), or domperidone only short term after a review of
  cardiac risk, QT-prolonging drugs and CYP3A4 inhibitors [EMA_Domperidone_2014]".
- The same wording goes into its drug output and the expected_evidence of
  `action-2-check-drug-interactions`.

RP02 PRO[1] (no domperidone with flecainide) is correct under the EMA contraindication and stays.

Across 600: the only cases that pair domperidone with an ECG are these 4.

## D5. MDS definitions of rigidity and bradykinesia in the exam (class SCENARIO)
Notes: 8cd68b0a (M01; anchored on mental_status, the text concerns the motor exam), 92ca20f9
(RM04).

**Rigidity.** MDS 2015: rigidity is velocity-independent resistance to slow passive movement;
isolated cogwheeling without rigidity does not count. With no rest tremor, rigidity is needed for
parkinsonism.
- The class is the PD-labelled cases with no rest tremor on examination and only "cogwheel"
  wording: M01, M02, M03, plus P02 (DLB, where parkinsonism is a core feature).
- Canonical motor sentence: "Velocity-independent rigidity on slow passive movement at both wrists
  (lead-pipe, with superimposed cogwheeling), <side> more than <side>".
- Mirror the edit into `patient.hpi` if that field exists.

**Bradykinesia.** RM04 gets "progressive decrement in amplitude and speed on repetitive finger
tapping, hand opening-closing and pronation-supination on the left, milder on the right". Every
other PD-labelled case already documents decrement (scripted).

## D6. Near-duplicate cases M01, M02, M03 (class NEW:near-duplicate-case)
Notes: 0d250e2e (M02), 36b4026f (M03).

**Measured.**
- All three share the label, the tiers and the work-up.
- HPI token Jaccard is 0.30 to 0.34.
- M01 and M03 share one exam sentence verbatim, the rigidity sentence (it is rewritten under D5).

**Decision.** Keep the three as a graded triad that tests one reasoning step at three evidence
levels, and make the grading explicit while removing the shared surface:
- M01: DaTscan plus RBD, orthostatic light-headedness on tamsulosin;
- M02: DaTscan plus RBD and hyposmia (UPSIT), depression, ET in her brother;
- M03: DaTscan the only marker, age 75, weight loss.

Worker actions:
1. Give M02 and M03 chief complaints that do not repeat M01's. M02 leads with slowness and low
   mood. M03 leads with stiffness and smaller handwriting, all from their own HPI.
2. Remove verbatim shared exam sentences.
3. State each case's distinct axis in `metadata.primary_teaching_point`.

**Reason.** Rewriting one case into another drug scenario would change the label and the whole
pathway, for a severity=note comment. The triad is defensible as three difficulty levels.

Ruling FIXED (de-templated). Replacing M03 by a different dopamine-blocker scenario is listed as
an optional composition choice for Andrea (PD.md section 5).

## D7. Family history contradiction (class REPORT-CONTRADICTION)
Note: 82b35cac (M02).
- M02 `family_history[3]` becomes "No other family history of movement disorders" (brother with
  ET at [2]).
- Class extension, P04: "No known family history of Wilson's disease, dystonia or other movement
  disorders" sits beside a maternal uncle's unexplained tremor. It becomes "No known family history
  of Wilson's disease, dystonia or parkinsonism".
- Across 600 the scripted check finds only M02 with the exact pattern.

## D8. Handedness and micrographia (class SCENARIO)
Note: b468a5e6 (M05).
- M05's HPI has him doing left-hand tasks "including writing", and the exam shows left-hand
  micrographia. He writes with the left hand, so `demographics.handedness` becomes "left" and the
  HPI says "left-handed". That is the clinically consistent option of the two the note offers.
- Class extension, S06: "right-handed", yet she "has stopped using left-handed scissors" and her
  handwriting is smaller with a left-sided PD. Make her left-handed in the same way.
- Every other case was checked (scripted handedness against micrographia side): consistent.

## D9. Nigral swallow-tail sign (class DX-CERTAINTY)
Note: d579cd94 (M04).

**Canonical evidence wording:** "SWI loss of the nigral swallow-tail appearance is consistent with
nigral degeneration but is not specific for PD and is not a diagnostic criterion; the diagnosis is
clinical (MDS 2015) and MRI serves to exclude other causes [Schwarz_2014][Postuma_2015]".

Applies to every evidence line that mentions the sign:
- M04 KCE[3], RM04 KCE[3], RM05 KCE[4]: MRI optional there, so also use the D1 "if obtained" form;
- RP02 KCE[3], RP05 KCE[3]: MRI required.

The criterion `expected_evidence` lines that restate the report stay.

## D10. ECG in presyncope and falls (class AVOIDED-MISSING / TIER)
Note: caaaca18 (P01).

**P01.**
- Delete `avoid-waste-5-analyze-ecg`.
- Add a `recommended` criterion `ecg-baseline` (`analyze_ecg {}`), placed after the MRI. Rationale:
  "Recurrent falls, near-syncope and neurogenic orthostatic hypotension, with midodrine or
  droxidopa planned: a baseline 12-lead ECG screens for a cardiac contribution [ESC_2018]".
- Store the ECG as `initial_tool_outputs.ecg`: sinus rhythm at the case HR, normal intervals.
  Null the case fallback ECG if it would duplicate it.

**Class extension, P02.**
- REQ[1] demands an ECG before the cholinesterase inhibitor, but no criterion orders one and no
  case output stores one (a must cannot demand an unordered study).
- The patient has had two falls with loss of consciousness.
- Add a `recommended` criterion `ecg-before-chei` with a stored ECG (sinus rhythm, normal PR and
  QTc).

**Checked and kept as waste.** M04, M05, P04, RM02, RM03, RM04, RP04 (pre-anaesthetic ECG arranged
with surgery), RP05, RS02, RS04, RS05, S01-S06. None has syncope or presyncope; their
"lightheadedness" mentions are denials or brief orthostatic symptoms. RP01 is handled by D21.

## D11. Levodopa trial as a diagnostic requirement (class MUST-WRONG / UNSOURCED-RULE)
Notes: 4d967b13 (P03), 722c125f (RP03).

MDS 2017 PSP: probable PSP-RS is O1 with P1. MDS 2022 MSA: established MSA can rest on the
cerebellar syndrome. Neither needs levodopa resistance.

**Canonical must (P03 REQ[3], RP03 REQ[4]):** "Levodopa may be titrated further (toward up to
1000 mg/day) for possible symptomatic benefit if tolerated, with lying and standing blood pressure
at each step <RP03: given the severe orthostatic hypotension>, and tapered slowly if there is no
benefit; it is not needed for the diagnosis and must not delay fall prevention and the swallowing
assessment [Hoglinger_2017 / Wenning_2022]".

Other edits:
- P03 REQ[0] drops "levodopa resistance cannot yet be stated" as a missing element. It may say a
  poor response would be supportive.
- RP03 REQ[0] says the criteria are met through the cerebellar route as well.
- P01 REQ[1] (start a levodopa trial in probable MSA-P) is symptomatic treatment, not a
  diagnostic requirement. It is unchanged.

## D12. Wilson screening at 42 (P04)
Note: 56aee7f4.

**Decision.**
- `action-4-interpret-labs` goes from `required` to `optional` and leaves the stop rule, which
  becomes [MRI].
- REQ[1] becomes: "Consider Wilson disease at onset age 42: slit-lamp examination shows no
  Kayser-Fleischer rings; if screened, serum ceruloplasmin with 24-hour urinary copper is the first
  step [EASL_ERN_Wilson_2025]".
- Evidence lines that cite the stored copper results take the "if obtained" form.
- `wilson disease` stays in `rejected`.

**Conflict with October R1a** (kept required under EASL-ERN 2025). EASL-ERN 2025 asks that Wilson
be considered in an otherwise unexplained neurological disorder. This presentation is typical PD
without hepatic, psychiatric, dystonic or ocular features, and the slit-lamp is already normal. The
physician's ruling stands. I chose `optional` (the note's option) over `recommended`: I found no
verified age threshold that would make screening the standard of care here.

**MRI stays required in P04.** Onset before 50 widens the secondary differential (structural,
metabolic, NBIA, Wilson T2 basal-ganglia change), and NICE 1.2.10 allows MRI in the differential
of other parkinsonian syndromes. The physician read P04 and did not ask to change the MRI.

## D13. First-line levodopa when motor symptoms impair work (P04)
Note: 3ed94a70.

**REQ[2] (canonical):** "Start levodopa as first-line treatment, since tremor and slowness impair
his work and quality of life (carbidopa-levodopa 25/100 mg, half a tablet three times daily with
food, increasing over 2 to 4 weeks to one tablet three times daily); a dopamine agonist or an MAO-B
inhibitor are alternatives to discuss according to his preferences and risks, and if an agonist is
used, warn about impulse control disorders and excessive daytime sleepiness and ask about them at
every visit [NICE_NG71]".

KCE[5] is rewritten to the same point. Reason: NICE NG71 rec 1.3.1. No other case says "are all
options" (scripted, 600 cases).

## D14. Bipolar disorder and dopaminergic treatment
Notes: c2e6d577 (RM02, bipolar II), 1d3af06d (RS01, bipolar I).

**Canonical must** (added to the levodopa must or as its own must):
"Coordinate levodopa initiation and titration with psychiatry and monitor at each step for
hypomania, mania, psychosis and impulse-control symptoms; avoid dopamine agonists, or use them only
with particular caution and psychiatric agreement [NICE_NG71]".

RS01 REQ[3] is rewritten to it. No other PD case has bipolar disorder (scripted).

## D15. Propranolol for postural tremor
Note: 32a0532b (RM03). Class extension: M04 REQ[2], same template.

**Canonical must:** "Review propranolol: it treats the longstanding postural tremor, but with a
resting heart rate of <58 RM03 / 62 M04> and levodopa being introduced, reduce or stop it if
bradycardia or orthostatic symptoms appear, tapering rather than stopping abruptly; measure lying
and standing blood pressure and heart rate at each levodopa step".

- Delete "which levodopa does not treat" in both. Levodopa can improve the postural (re-emergent)
  component, and the categorical claim is unsourced.
- M04 keeps "propranolol and amlodipine add to orthostatic falls".
- RM03 PRO[2] (no abrupt stop) stays.
- RP04's "levodopa-unresponsive postural and kinetic tremor" is that patient's documented history
  and stays.

## D16. Frozen shoulder (RM04)
Note: 23ea4603.

The HPI documents restriction of both active and passive range at orthopaedic diagnosis, so
coexisting adhesive capsulitis is plausible.
- **REQ[1] (canonical):** "Explain that the lost arm swing, micrographia and slowness are
  parkinsonian and that the shoulder stiffness is at least partly parkinsonian rigidity, while the
  restriction of active and passive range suggests a coexisting adhesive capsulitis; reassess both
  after dopaminergic treatment is established, continuing shoulder physiotherapy and asking
  orthopaedics to review if the restriction persists".
- Delete PRO[0] (the blanket ban on further shoulder treatment).
- Remove `adhesive capsulitis` and `frozen shoulder` from `rejected`. A true coexisting condition
  must not veto the answer (scorer v2 rule).
- The differential entry reads "coexists possibly; does not explain the parkinsonism" at low.
- The red-herring `correct_interpretation` is aligned.
- Add passive range to the exam if missing: "passive abduction also limited, with a capsular end
  feel".

## D17. DaTscan for prochlorperazine in established PD (RM05)
Note: eac7edfb.

- Delete criterion `action-7-order-advanced-imaging` (and its sequence constraint, D2).
- Add `avoid-waste-datscan` (waste): "In established PD an abnormal DaT scan is expected and
  cannot show whether intermittent D2 blockade aggravates the symptoms; stop prochlorperazine and
  review [Marshall_2009][NICE_NG71]".
- Keep the stored DaTscan follow-up, so an order is answered truthfully.

## D18. Levothyroxine (RM05)
Note: 8de3e101.

**REQ[4] (canonical):** "Review levothyroxine adherence and timing (on an empty stomach, apart from
calcium, iron and omeprazole, which can reduce absorption), recheck TSH and free T4 in 6 to 8
weeks, and increase the dose only if under-replacement persists; this does not delay management of
the wearing-off [ATA_2014]".

## D19. RM01 label and saccadic freezing
Note: d3fc1f93.

**Label change: CENTRAL synonyms check.** `accepted[0]` becomes "Parkinson's disease with motor
worsening and episodic saccadic freezing on low-dose levodopa (possibly dopamine-responsive)".

**REQ[0] (canonical):** "Keep the diagnosis of PD: the saccadic freezing with a full vertical range,
preserved optokinetic responses and a normal midbrain on MRI is not a supranuclear gaze palsy; the
freezing may be dopamine-responsive, so record its relation to levodopa doses and reassess eye
movements after dose optimisation before attributing it to undertreatment".

REQ[1] already reassesses after the increase.

## D20. Posterior-circulation TIA as a safety differential (RM01)
Note: cfc0fa20.

- Add a differential entry "Posterior circulation transient ischaemic attack" (G45.0), low.
  key_features: "Vascular risk (insulin-treated diabetes, hypertension, hyperlipidaemia) and
  episodic oculomotor symptoms with dysarthria raise it; episodes are reproduced on examination
  during saccade testing and are broken by smooth pursuit, without other brainstem signs, and a
  normal MRI does not exclude transient ischaemia".
- Add one must: "If episodes occur outside eye-movement tasks or with other brainstem symptoms,
  assess for posterior-circulation ischaemia (vascular imaging of the vertebrobasilar circulation)".
- No vascular-imaging criterion. The physician asks not to make it mandatory.

## D21. Syncope with known WPW (RP01)
Note: 8352e97d.

**ECG.** `action-ecg-syncope` goes from `recommended` to `required` and joins the stop rule
([MRI, ECG]). Reason: ESC 2018, a 12-lead ECG in every syncope (Class I); a red flag must be
addressed before stopping.

**New criterion.** `recommended` `eps-accessory-pathway`
(`order_specialized_test {"test_type": "electrophysiology_study"}`). Reason: pre-excitation with
syncope is symptomatic and needs invasive risk stratification [ESC_SVT_2019]. Without a stored
report the library would answer normally and contradict the known pathway. Store a follow-up
(trigger `request_electrophysiology_study`, `test_type` set):
- manifest left-lateral accessory pathway, antegrade effective refractory period 310 ms;
- shortest pre-excited RR interval in induced AF 300 ms;
- no inducible AV re-entrant tachycardia with or without isoprenaline;
- impression: "Low-risk antegrade accessory-pathway properties; no inducible AVRT".
- No management in the report.

**REQ[1] (canonical):** "Orthostatic hypotension is the probable mechanism of both syncopes (both on
standing, 32/20 mmHg fall with a heart-rate rise of 6/min), but a Holter that captured only
light-headedness does not exclude an arrhythmia in a man with pre-excitation and syncope: arrange
prompt cardiac electrophysiology review for accessory-pathway risk stratification, with ablation
or further monitoring decided there [ESC_2018][ESC_SVT_2019]".

**Other edits.**
- PRO[2] becomes "Do not consider the syncope evaluation complete after a negative Holter".
- KCE[3] is rewritten: no syncope was captured; the EPS result, if done, gives the risk.
- Differential "cardiac syncope, WPW" key_features are rewritten the same way (low after the
  low-risk EPS).
- Remove `wolff parkinson white` and `WPW` from `rejected`: WPW is a true coexisting condition.
- REQ[0] wording: "one red flag, counterbalanced (one supportive criterion is enough; here rest
  tremor and Sniffin' Sticks)".

## D22. RP02: MIBG not decisive; OH on metoprolol
Notes: d6571979 (anchored on REQ[1]; the text concerns REQ[0], the MIBG criterion and KCE),
f4a8e329.

MDS 2015: one red flag needs one supportive criterion. The severe-autonomic-failure red flag
excludes OH plausibly explained by medication, and metoprolol also blunts the heart-rate response.

**Decision.**
- MIBG criterion from `recommended` to `optional`. Rationale: "may add support; not required and
  not definitive".
- **REQ[0] (canonical):** "Diagnose clinically probable PD (MDS 2015): right-predominant
  bradykinesia with decrement, rigidity and a right-hand rest tremor; the rest tremor is a
  supportive criterion, which is enough to counterbalance one red flag; whether the orthostatic
  hypotension (42/30 mmHg at 3 minutes) is the severe-autonomic-failure red flag cannot be decided
  while metoprolol may explain it and blunts the heart-rate response [Postuma_2015]".
- Add a must: "Review metoprolol, the flecainide and the AF regimen with cardiology, then repeat
  lying and standing blood pressure and heart rate before classifying the orthostatic hypotension
  as neurogenic".
- KCE[1] is rewritten likewise: "...severe; not classed as neurogenic or as a red flag until the
  beta-blocker is reviewed".
- Lines that cite the MIBG take the "if obtained" form.
- REQ[1] (OH treatment) keeps "review metoprolol with his cardiologist".

The label "PD with early prominent autonomic failure" is not the object of a note and stays.

## D23. RP03 amlodipine
Note: 8069f8d7 (anchored on REQ[3]; the text concerns REQ[2]).

REQ[2]'s clause "review tamsulosin and stop daytime amlodipine" becomes: "review the
antihypertensives (amlodipine 10 mg, tamsulosin, propranolol) individually with his cardiologist,
given his coronary disease and supine hypertension (148/90), monitoring supine and standing
pressure at each change". The rest of REQ[2] stays.

## D24. RP04: STN versus GPi
Note: 7ebc619e.

**REQ[2] (canonical):** "The levodopa challenge (MDS-UPDRS III 46 to 16, 65% improvement) supports
DBS candidacy; the multidisciplinary team compares STN and GPi targets: GPi may be preferable with
her multidomain mild cognitive impairment, anxiety and depressive symptoms and troublesome
peak-dose dyskinesia, STN allows a larger medication reduction; the levodopa-unresponsive
postural and kinetic tremor enters the target choice [CAPSIT_PD_1999][Follett_2010]".

- REQ[3]: "does not exclude STN-DBS" becomes "does not exclude DBS".
- PRO[3] stays.

## D25. RP05 DaTscan
Note: 61f2065e.

- DaTscan from `recommended` to `optional`. Rationale: "if diagnostic uncertainty persists; an
  abnormal DaT scan is not specific for PD and does not exclude a vascular contribution".
- REQ[1] drops "and the DaTscan shows an asymmetric presynaptic deficit". The argument rests on
  the clinical picture and the MRI (required).
- The vascular differential says the same.
- The soft MRI-before-DaTscan constraint stays (D2).

## D26. RS01 lithium
Note: 582e1ee0.

**REQ[1] (canonical):** "Keep PD as the leading diagnosis: the asymmetric rest tremor with RBD and
hyposmia is not typical of lithium, but chronic lithium can contribute to tremor and parkinsonism
even at a therapeutic level (0.72 mEq/L); keep lithium under psychiatric care, coordinate any
change with psychiatry without stopping it abruptly, and monitor the level and renal function,
since lisinopril raises lithium levels".

- Remove `lithium induced tremor` from `rejected`: the postural tremor component may be
  lithium-related.
- `lithium induced parkinsonism` stays.
- The differential entry "lithium-associated parkinsonism" becomes "possible contributor" (low).

## D27. RS02 shunt
Notes: 0d17ed0e, 6029713d.

**PRO[1] (canonical):** "Do not arrange shunt revision without evidence of malfunction: normal
ventricles (Evans 0.27) and no headache, nausea or visual symptom make shunt failure an unlikely
cause, although normal ventricular size does not completely exclude shunt dysfunction; compare
with the previous surveillance imaging and ask neurosurgery to review if symptoms or findings
raise concern".

**REQ[1] (canonical):** "Before the MRI, identify the VP shunt valve model, its MR conditional
status and whether it is programmable, and document the current setting; after the MRI, check and
reprogram the setting according to the manufacturer's protocol".

The red-herring interpretation ("shunt failure would enlarge the ventricles") and the
shunt-failure differential are aligned.

Elsewhere: 31 NPH cases and FEPI-TEMP-RM01 mention programmable valves. Told to the NPH lead
through CENTRAL item 6.

## D28. RS03 trunk posture
Note: ec3fb0d3.

- The exam becomes: "Leftward lateral trunk flexion of about 8 degrees when standing, fully
  corrected when supine and on passive correction".
- Replace "Pisa syndrome" with "leftward lateral trunk flexion" in the must, the differential,
  KCE[3] and metadata [Tinazzi_2022].
- Keep the physiotherapy and postural assessment must and the PD label.

## D29. Approval note
Note: 5b975043 (P02, "tutto ok"): NO-ACTION. P02 still receives the class edits D5 (rigidity
wording) and D10 (ECG before the cholinesterase inhibitor), which are real defects.

## D30. Rejected labels that are true in the case (class from SKILL_NOTES scorer v2)
Applied in RP01 (D21), RM04 (D16), RS01 (D26) and two more cases:
- RM02: remove `post encephalitic parkinsonism` and `postencephalitic`. Note 07401754: an
  encephalitis of uncertain cause 18 months ago, 8 months before the motor onset, is not
  excluded.
- M02: remove `essential tremor`. Her years-long bilateral postural tremor is a coexisting ET
  ("coexists" in the differential); M04, RM03 and RP04 already do not reject ET.

The worker re-tests the candidate answers after any `rejected` edit.

## D31. Post-encephalitic parkinsonism (RM02)
Note: 07401754.

Keep PD as the label.
- The differential entry becomes "not excluded until the outside hospital records (cause, imaging,
  CSF, neurological course) are reviewed" (low).
- The MRI rationale's "sequelae of the encephalitic illness" becomes "and looks for sequelae of the
  encephalitic illness".
- Add a must: "Obtain and review the outside hospital records of the febrile encephalitic illness
  before treating post-encephalitic parkinsonism as excluded".
- Remove the rejected labels (D30).

## D32. LIT and MRI-CONTRAST
No PD note raises them. Checked 16 Nov: no PD case stores a literature output or a literature
criterion. Workers add none back and run `mri_probe.py` after any MRI edit.
