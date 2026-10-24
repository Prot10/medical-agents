# FEPI-TEMP: condition plan for the October 2026 review round

Lead plan for the 30 `focal_epilepsy_temporal` cases: M01..M05, P01..P05, RM01..RM04,
RP01..RP05, RS01..RS05, S01..S06. Read `ROUND_POLICY.md`, `PATTERNS.md`,
`TOOL_REPORT_STYLE_GUIDE.md`, `TOOL_PARAMETER_VOCABULARY.md` and `docs/benchmark/tool-contract.md`
first; this plan does not repeat them.

There are no reviewer notes for FEPI-TEMP (`notes/FEPI-TEMP.md` does not exist): the condition was
never reviewed by a physician in a notes round. The physician input is the July 2026 tool guidance
for `focal_epilepsy_temporal` in `agent-platform/config/review/condition_tool_guidance.yaml`
(Reviewer 1, summarised in 1.3) plus ROUND_POLICY. Every finding below comes from the lead's
survey, so the survey is the only safety net: workers read every field of their case, not only the
items listed here. Each log has a "Reviewer notes" section that says "No reviewer notes for this
case".

Baseline (24 October 2026, before any edit): `perfect_agent.py` passes 30/30. The leak guard fails
3 cases: P02 and P03 (initial literature and drug blocks are empty `{}` or repeat the expected
evidence) and RP05 (follow-up `search_temporal_encephalocele_epilepsy` repeats it). 26 cases carry
the same `MRI -> drug check` soft constraint with a reason about "low-grade tumor -> CYP-neutral".
Every stop rule has `max_additional_actions: 0` and lists the literature and drug-check criteria as
required. 29 MRI criteria require `{contrast: true, protocol: epilepsy}`. 22 cases report a
prolactin row (26 mention prolactin somewhere). 14 cases store an FDG-PET follow-up that no
criterion orders (P05 holds one as a case fallback). Discriminator defects (the guard
`test_routed_outputs_name_their_study` does not cover FEPI-TEMP yet): untyped echo fallback in 28
cases, `specialized_test` fallback `not_specified` in P03, P05, RP01, `advanced_imaging` fallback
`MRI` in P03, RP02 body-imaging follow-up without `study` (class Q). Every case must pass
`discriminator_defects` (in `agent-platform/tests/test_case_guards.py`) before its log is closed.

Red herrings: every `ground_truth.red_herrings[].field_path` exists today. After any rewrite or
reorder (followup indices move: RP04 points at `followup_outputs[3]`; M01, RP05, S06, RS05 point
into the MRI or labs you may rewrite), re-check that each path still holds its `data_point`, and
update the path or the data point.

Use: apply the classes of section 2 that name your case (canonical text verbatim, `<...>` slots
filled), then the case decisions of section 4; rebuild criteria, follow-up order, constraints and
stop rule per section 3; run
`uv run python data/review/round-2026-10/bin/perfect_agent.py CASE -v`,
`uv run python data/review/round-2026-10/bin/case_io.py check CASE` and
`uv run pytest agent-platform/tests/test_case_guards.py -q -k CASE`; write `logs/{CASE_ID}.md`.
Edit only through `case_io` load/save.

New text: English, American spelling as the cases already use (generalized, tumor, anemia), no em
or en dashes. New values must fit age, sex, weight and medicines, and must not copy another case's
numbers (several cases share identical PET asymmetry indices, hippocampal volumes and lesion sizes;
do not add more).

---

## 1. Governing guidelines and canonical facts

### 1.1 Sources and keys

Keys marked * are not in the pack allow-list yet (CENTRAL request 2).

| key | source (what it governs) |
| --- | --- |
| `[ILAE_def_2014]`* | Fisher RS et al., Epilepsia 2014;55:475-482 (definition of epilepsy) |
| `[ILAE_2017]` | Fisher RS et al., Epilepsia 2017;58:522-530; Scheffer IE et al., Epilepsia 2017;58:512-521 (classification) |
| `[NICE_NG217_2025]`* | NICE NG217, Epilepsies in children, young people and adults (2022) (first seizure, ECG, labs, EEG, imaging, first-line ASM) |
| `[AAN_2007]`, `[AAN_2015]`* | Krumholz A et al., Neurology 2007;69:1996-2007 and 2015;84:1705-1713 (first unprovoked seizure in adults) |
| `[ILAE_MRI_2019]`* | Bernasconi A et al., Epilepsia 2019;60:1054-1068 (HARNESS-MRI epilepsy protocol) |
| `[IFCN_ILAE_EEG_2023]`* | Peltola ME et al., Epilepsia 2023;64:602-618; Tatum WO et al., Clin Neurophysiol 2018;129:1056-1082 (EEG staging) |
| `[SANAD2_2021]`* | Marson A et al., Lancet 2021;397:1363-1374 (lamotrigine vs levetiracetam vs zonisamide) |
| `[ILAE_drug_2017]` | the pack key; its text must become Glauser T et al., Epilepsia 2013;54:551-563 (CENTRAL request 1) |
| `[Kwan_2010]` | Kwan P et al., Epilepsia 2010;51:1069-1077 (drug resistance) |
| `[Engel_2003]`, `[Wiebe_2001]`*, `[ERSET_2012]`* | Engel J et al., Neurology 2003;60:538-547; Wiebe S et al., NEJM 2001;345:311-318; Engel J et al., JAMA 2012;307:922-930 (surgery) |
| `[Willmann_2007]` | Willmann O et al., Seizure 2007;16:509-520 (FDG-PET in presurgical TLE) |
| `[AAN_prolactin_2005]`* | Chen DK, So YT, Fisher RS, Neurology 2005;65:668-675 |
| `[Lateralization_2005]`* | Loddenkemper T, Kotagal P, Epilepsy Behav 2005;7:1-17 |
| `[ILAE_HS_2013]`*, `[ILAE_FCD_2011]`* | Blumcke I et al., Epilepsia 2013;54:1315-1329; Blumcke I et al., Epilepsia 2011;52:158-174 |
| `[ILAE_PNES_2013]`* | LaFrance WC et al., Epilepsia 2013;54:2005-2018; Goldstein LH et al., Lancet Psychiatry 2020;7:491-505 (CODES) |
| `[AAN_SUDEP_2017]`* | Harden C et al., Neurology 2017;88:1674-1680 |
| `[CPIC_2018]`* | Phillips EJ et al., Clin Pharmacol Ther 2018;103:574-581 (HLA and carbamazepine, oxcarbazepine) |
| `[EURAP_2018]`*, `[AAN_WWE_2009]`* | Tomson T et al., Lancet Neurol 2018;17:530-538; Harden CL et al., Neurology 2009;73:142-149 (pregnancy, levels, breastfeeding) |
| `[MHRA_VPA_2024]`*, `[MHRA_TPM_2024]`* | MHRA Drug Safety Update: valproate (January 2024), topiramate (June 2024) |
| `[Sabers_2003]`* | Sabers A et al., Neurology 2003;61:570-571 (oral contraceptives lower lamotrigine) |
| `[ACOG_imaging_2017]`*, `[Ray_2016]`* | ACOG Committee Opinion 723, Obstet Gynecol 2017;130:e210-e216; Ray JG et al., JAMA 2016;316:952-961 |
| `[ACOG_HTN_2020]`* | ACOG Practice Bulletin 222, Obstet Gynecol 2020;135:e237-e260 (eclampsia) |
| `[Graus_2016]`*, `[Irani_2011]`* | Graus F et al., Lancet Neurol 2016;15:391-404; Irani SR et al., Ann Neurol 2011;69:892-900 (P02) |
| `[IDSA_enc_2008]`*, `[ABN_enc_2012]`* | Tunkel AR et al., Clin Infect Dis 2008;47:303-327; Solomon T et al., J Infect 2012;64:347-373 (RP01) |
| `[ACNS_2021]`*, `[Salzburg_2015]`*, `[ILAE_ASS_2010]`* | Hirsch LJ et al., J Clin Neurophysiol 2021;38:1-29; Leitinger M et al., Epilepsy Behav 2015;49:158-163; Beghi E et al., Epilepsia 2010;51:671-675 (RP01) |
| `[ESC_syncope_2018]`* | Brignole M et al., Eur Heart J 2018;39:1883-1948 (P05) |
| `[IDSA_NCC_2018]`*, `[Garcia_2014]`* | White AC Jr et al., Clin Infect Dis 2018;66:e49-e75; Garcia HH, Nash TE, Del Brutto OH, Lancet Neurol 2014;13:1202-1215 (RS02) |
| `[TSC_2021]`*, `[EXIST3_2016]`* | Northrup H et al., Pediatr Neurol 2021;123:50-66; French JA et al., Lancet 2016;388:2153-2163 (RM02) |
| `[ESC_PE_2019]`*, `[EHRA_DOAC_2021]`* | Konstantinides SV et al., Eur Heart J 2020;41:543-603; Steffel J et al., Europace 2021;23:1612-1676 (RP02) |
| `[ASCO_irAE_2018]`* | Brahmer JR et al., J Clin Oncol 2018;36:1714-1768 (RP03) |
| `[Cavernoma_2017]`* | Akers A et al., Neurosurgery 2017;80:665-680 (M05) |
| `[Blumcke_2017]`* | Blumcke I et al., NEJM 2017;377:1648-1656 (epilepsy-associated tumors) |
| `[Encephalocele_2015]`* | Saavalainen T et al., Neurology 2015;85:1467-1474 (RP05) |

Citation rule: one bracketed key per criterion and avoided action, never the same key twice with
and without brackets. If `case_io.py check` refuses a starred key, cite the nearest pack key and
list the wanted key in the log's CENTRAL table. Literature outputs cite only these sources, as
`Author et al., Journal Year;Vol:pages | Title`; every other source is deleted (class O).

### 1.2 Canonical clinical facts (use these; do not restate them differently)

1. Epilepsy: two unprovoked seizures more than 24 h apart, or one with a recurrence risk of at least
   60% [ILAE_def_2014]. Stereotyped focal aware or impaired-awareness seizures before a first
   convulsion are prior seizures: the 2-seizure criterion is met, the single-seizure rule is not
   needed.
2. Acute symptomatic seizures or status epilepticus during an acute encephalitis are not epilepsy
   [ILAE_ASS_2010].
3. MRI with a dedicated epilepsy protocol (3D T1 and 3D FLAIR about 1 mm, coronal T2 perpendicular to
   the hippocampus; 3T when available) is the imaging of choice; CT only if MRI is unavailable or
   contraindicated, or in an emergency (head injury, persistent deficit, no return to baseline,
   anticoagulation, shunt, cancer) [ILAE_MRI_2019]. Gadolinium is not routine; it is added when a
   tumor, vascular malformation, infection or inflammation is suspected.
4. HS on MRI: hippocampal atrophy, T2/FLAIR hyperintensity, loss of internal architecture, often
   temporal horn enlargement. "Borderline volume, below HS threshold" is not HS.
5. EEG: routine awake EEG with drowsiness or sleep first; if non-diagnostic, sleep-deprived, then
   ambulatory or video for event capture. Video-EEG for uncertain diagnosis (PNES, syncope),
   presurgical evaluation or quantification; continuous ICU EEG only for suspected NCSE or
   unexplained encephalopathy [IFCN_ILAE_EEG_2023]. One routine EEG shows interictal discharges in
   roughly 30 to 50% of adults with epilepsy; a normal EEG does not exclude epilepsy.
6. First-line ASM for focal epilepsy: lamotrigine or levetiracetam [NICE_NG217_2025]; lamotrigine
   was superior in SANAD II [SANAD2_2021]; carbamazepine, oxcarbazepine, zonisamide, lacosamide are
   further options. Glauser 2013 Level A for adults with focal seizures: carbamazepine,
   levetiracetam, phenytoin, zonisamide; lamotrigine and gabapentin are Level A only in the elderly.
   Never write "lamotrigine Level A" or "oxcarbazepine Level A" for an adult under 60.
7. Valproate is not first-line for focal epilepsy; MHRA 2024: not started under 55 unless two
   specialists document that nothing else works or is tolerated, and in women of childbearing
   potential only within a pregnancy prevention programme. Topiramate (MHRA 2024): pregnancy
   prevention programme; avoid in pregnancy for epilepsy unless no alternative.
8. Ethinylestradiol roughly halves lamotrigine levels (levels rise in the pill-free week)
   [Sabers_2003]. Carbamazepine, oxcarbazepine, phenytoin, phenobarbital and topiramate above
   200 mg/day reduce hormonal contraceptive efficacy; levetiracetam, lacosamide and lamotrigine do
   not.
9. Carbamazepine, phenytoin and phenobarbital lower DOAC and warfarin exposure [EHRA_DOAC_2021],
   many chemotherapy agents, dexamethasone, atorvastatin and simvastatin, sertraline and
   lamotrigine; valproate roughly doubles lamotrigine (halve its titration) and raises
   phenobarbital.
10. HLA-B*15:02 before starting carbamazepine or oxcarbazepine (and phenytoin) in patients of East,
    Southeast or South Asian ancestry who never took them [CPIC_2018]; long-term users without
    reaction need no test. No HLA term exists: must or prohibition only.
11. Prolactin drawn 10 to 20 minutes after a suspected tonic-clonic or focal impaired-awareness
    seizure helps against PNES; it does not separate seizure from syncope, and a level drawn hours
    later or after an aura has no value [AAN_prolactin_2005].
12. Lateralization [Lateralization_2005]: unilateral manual automatisms are usually ipsilateral;
    dystonic limb posturing, late forced head version and Todd paresis are contralateral; postictal
    aphasia means the language-dominant hemisphere; oral automatisms and tongue-bite side do not
    lateralize. In a left-handed patient write "probably language-dominant" unless dominance was
    tested.
13. "Dual pathology" is HS plus a separate lesion outside the hippocampus (tumor, malformation, FCD
    type II, scar). HS with an associated temporal cortical abnormality is FCD type IIIa, a
    histological diagnosis; on MRI write "temporopolar gray-white blurring associated with HS,
    possibly FCD type IIIa" [ILAE_FCD_2011].
14. Driving: no driving until the locally applicable seizure-free interval is met; pilots and
    occupational drivers have stricter rules (FAA medical certification for a US pilot).
15. SUDEP: counsel every patient, especially with ongoing tonic-clonic seizures; seizure control
    lowers the risk [AAN_SUDEP_2017].
16. A seizure after 20 weeks of pregnancy or postpartum is eclampsia until proven otherwise: blood
    pressure, urine protein/creatinine, platelets, creatinine, liver enzymes; magnesium sulfate
    treats eclampsia [ACOG_HTN_2020]. Gadolinium only if it changes outcome [ACOG_imaging_2017];
    exposure is linked to stillbirth or neonatal death and inflammatory skin disease [Ray_2016].
    No FDG-PET in pregnancy. Lamotrigine and levetiracetam clearance rise in pregnancy: monitor
    levels, raise the dose, reduce it after delivery [AAN_WWE_2009].
17. Calcified neurocysticercosis: no antiparasitic drug, ASM only [IDSA_NCC_2018]; no albendazole in
    pregnancy.
18. HSV encephalitis: IV acyclovir 10 mg/kg every 8 h adjusted to renal function, on suspicion
    [IDSA_enc_2008]. CSF: lymphocytic pleocytosis, raised protein, often red cells; acellular early
    or when immunosuppressed.
19. LGI1 encephalitis [Graus_2016, Irani_2011]: faciobrachial dystonic seizures (FBDS), memory
    decline, hyponatremia; antibodies more often in serum than CSF (send both); CSF often normal;
    FBDS often lack an EEG correlate and respond to immunotherapy more than to ASMs; tumors under
    10% (thymoma): chest CT.
20. PNES with epilepsy: habitual events captured on video-EEG without ictal correlate
    [ILAE_PNES_2013]; continue the effective ASM; CBT-based therapy; no benzodiazepine escalation.

### 1.3 July 2026 physician guidance (Reviewer 1, condition_tool_guidance.yaml)

- MRI: required, dedicated epilepsy protocol; CT only if MRI unavailable or contraindicated
  (NICE NG217, ILAE Neuroimaging Task Force 2019, ACR).
- EEG: required; routine awake first, then sleep-deprived, then ambulatory or video for event capture
  or PNES; continuous ICU only for NCSE (NICE NG217, IFCN/ILAE 2023).
- ECG: requested tier `optional`; a 12-lead ECG is appropriate at a first suspected seizure or
  TLOC to find a cardiac mimic. The July reply made it `required` in 21 cases, against the
  requested tier.
- Labs: requested tier `optional`, used when clinically indicated (hypoglycemia, electrolytes,
  infection, toxins, drugs, pregnancy, metabolic causes).
- Cardiac monitoring and echocardiography: remove.
- The team's July reply claimed prolactin had been removed from the template. It was not (22 cases
  still report it); class M does it now.

---

## 2. Error classes in this condition

Classes apply to the cases listed. "All" means all 30 unless section 4 says otherwise.

### A. Literature required and in the stop rule (27 cases; leak in P02, P03, RP05)

Literature criteria are `required` in 27 cases and appear in every stop rule. Ruling 5: literature
is `optional` at most, last in the criteria list and last in `followup_outputs`, never in a
sequence constraint or the stop rule. Rewrite each literature output as a general, correctly cited
summary (sources only from 1.1) that answers its query without repeating any criterion's
`expected_evidence`, the diagnosis label, or case-specific findings. Empty `{}` initial literature
and drug blocks (P02, P03) are deleted, not filled. RP05's encephalocele summary repeats the MRI
criterion's evidence: rewrite it per the rule. Literature `expected_evidence`:
`General evidence on <topic of the query>; not required for the diagnosis.`

### B. Drug check required by template (27 cases)

`check_drug_interactions` is required in 27 cases with the template evidence "Identify
pharmacokinetic interactions (CYP induction by carbamazepine/phenytoin) and CNS adverse-effect
overlap" in 17. Ruling 6 tiers (decided per case in section 4):

- required: the patient takes a drug with a documented interaction that changes the ASM choice or
  dose (fact 8 or 9): combined hormonal contraception (P04, RM02, S02, S04), anticoagulation (RP02),
  an inducer or inhibitor combination already in use (RP04, RS04).
- recommended: a comedication matters only if an inducer or a specific agent is chosen (statin,
  SSRI, chemotherapy or ICI with steroids, acyclovir with renal drugs, phenytoin switch): P02, P05,
  RM03, RM04, RP01, RP03, RS03.
- optional: no relevant comedication (all other cases).

The output answers the case's real comedication list (no invented creatinine or levels the case
does not report; no claim that lamotrigine has no interaction with an oral contraceptive) and keeps
the warnings factual. The `expected_evidence` names the case's actual interaction or, when
optional, says
`No interaction between <proposed ASM> and <current medicines> that changes management.`
The check comes after the MRI and EEG in the criteria order.

### C. Shared MRI -> drug check soft constraint (26 cases)

Keep it only where the drug check stays required or recommended; delete it where the drug check is
optional. Canonical reason:
`Know the structural cause before finalizing the ASM and its interactions (a tumor or planned oncologic therapy favors non-inducing ASMs).`
Never a constraint involving literature. Hard constraints only in 3.3.

### D. Stop rule (all)

`max_additional_actions: 0` everywhere and literature and drug check listed. Rebuild per 3.4.

### E. MRI arguments and gadolinium (29 criteria)

The MRI criterion requires `{contrast: true, protocol: epilepsy}` before the lesion is known.
Decision: `required_arguments: {protocol: epilepsy}` in all cases except RP01 and RP03
(`{contrast: true}`, known cancer, encephalitis or metastasis; no protocol argument), P02 (no
arguments: any MRI answers the encephalitis question) and RS02 (`{protocol: epilepsy, contrast:
false}` plus the harm avoided action in K/section 4). Report wording:

- HS, MRI-negative and FCD cases: no gadolinium in the report. Delete "Normal gadolinium
  enhancement pattern", "No pathological enhancement following gadolinium" and similar lines
  (RS03, RS04, RS05, S04 and the rest).
- Tumor, cavernoma, malformation cases: `Post-contrast T1 sequences were added by the reviewing radiologist because a lesion was seen.`
- Musts that order "MRI with contrast" or "gadolinium-enhanced MRI" (RM04, S02, S03) are deleted
  (class L).

### F. Stored MRI is not the ordered epilepsy-protocol study (M01, M02, M03, RM01, RM02, RM03, RP04, RP05, RS01, RS02)

The initial MRI is an equivocal 1.5T or standard study that "recommends epilepsy protocol" while
the label rests on definite findings (HS, dual pathology, encephalocele). Fix the data, not the
label: rewrite `initial_tool_outputs.mri` as the dedicated epilepsy-protocol MRI the criterion
orders, showing the labelled lesion with the definite findings of fact 4. A prior standard study
stays only in the history ("an outside 1.5T standard MRI two years ago was read as normal"). Move
every red herring that pointed at the old MRI text to the history path, and delete
`recommended_actions` asking for another MRI. Specific content per case in section 4.

### G. Engineering lines in key_clinical_evidence (all)

Delete "Tier per the July 2026 clinical review: ..." and "July 2026 review applied end to end: ..."
from every `key_clinical_evidence`.

### H. Citations and rationales (all)

Every criterion lists the same key twice (`[AAN_2007]`, `AAN_2007`) and in about 29 cases the
rationale repeats the label; template `expected_evidence` lines are shared by 5 to 23 cases (MRI
"Hippocampal sclerosis, low-grade tumor ...", EEG "Interictal focal temporal discharges may
support ...", labs "Answer the specific provocation ...", ECG "Identify or exclude
pre-excitation ...", video "Concordant electroclinical event ...", neuropsychology "Memory and
language lateralization ...", sleep-deprived "Sleep may activate ..."). Fix: one bracketed key per criterion from 1.1 matched to its content
(MRI `[ILAE_MRI_2019]`, EEG `[IFCN_ILAE_EEG_2023]`, ECG and labs `[NICE_NG217_2025]`, PET
`[Willmann_2007]`, neuropsychology `[Engel_2003]`, ASM and interactions per fact 6 to 9), and a
one-sentence case-specific rationale that says why this patient needs the action. The EEG
`expected_evidence` names the case's actual finding (side, electrodes, wave form), not "Interictal
focal temporal discharges may support the clinical diagnosis". The labs `expected_evidence` names
the targeted question, not "Answer the specific provocation or treatment question".

### I. Template avoided actions (25 cases)

CSF, TTE and Holter as waste are correct where no indication exists (rationale case-specific,
never the shared sentence). CT as waste is wrong where CT is indicated (fact 3): delete it in RM01
(VP shunt), RM03 (head injury, GCS 8, depressed fracture), RP01 and RP03 (cancer, encephalopathy),
RS02 (pregnancy, head CT is acceptable) and P04 (CT is the claustrophobia alternative). P04's ECG
avoided action is deleted (cheap, indicated before lacosamide). Add `FDG_PET` waste per class J.
Echo fallbacks lack `echo_type`: add `"echo_type": "TTE"` to every `fallback_tool_outputs.echo`
(all cases).

### J. FDG-PET follow-ups that no criterion orders (M01, M02, M03, RM01, RM02, RM03, RP01, RP02, RS02, RS03, S01, S02, S03, S04)

These cases store an FDG-PET (often as the first follow-up) for a first diagnosis with a concordant
MRI and EEG or for an acute illness. RP03 joins the class although PET is a criterion there:
delete its PET criterion and follow-up too (the contrast MRI already characterizes the growing
metastasis; brain FDG-PET has high cortical background and changes nothing before radiosurgery or
resection), with the waste rationale
`Contrast MRI already characterizes the enlarging metastasis; brain FDG-PET does not change management here.`
Decision: delete the follow-up. If
`fallback_tool_outputs.advanced_imaging` is empty and the report is consistent with the rewritten
case, move it there with `"modality": "FDG_PET"`; otherwise drop it (RM01's PET describes a "left
frontoparietal known lesion" that does not exist: drop). Add the avoided action
`order_advanced_imaging {modality: FDG_PET}` severity `waste` with rationale
`FDG-PET adds nothing to a first diagnosis with concordant MRI and EEG; it belongs to presurgical evaluation of drug-resistant epilepsy.`
In RS02 the severity is `harmful` (pregnancy, fact 16). Cases where PET is a criterion keep it with
the tier in section 4.

### K. EEG report template carry-over (M01, M02, M03, RM01, RM03, RM04, RP02, RP03, RS02, RS03, RS05, S01..S06)

- Routine EEG limitations that recommend further monitoring ("Prolonged video-EEG monitoring is
  recommended", "would provide greater yield", "recommended if clinical evaluation warrants", "may
  be considered") (M02, RM03, RM04, RS02, RS03, RS05, S01..S06): replace with the recording's own
  limits, for example
  `Routine <n>-minute recording with drowsiness; no habitual event captured.`
- Sleep-deprived EEG limitations copied from video or ambulatory studies ("Only one habitual event
  captured", "48-hour", "96 hours", "Three-day monitoring") in M01, M02, M03, RM01, RP02: rewrite
  for a sleep-deprived study. RM01 claims a subclinical seizure in the limitations while the
  impression says none: remove it.
- M03 and RP02 ambulatory: "48-hour 48-hour" duplication, "96 hours" vs 48 hours; M03 finding
  "evolving ... bilateral" contradicts "remaining lateralized". Make duration and findings agree.
- The sleep-deprived impression "Abnormal sleep-deprived EEG with right anterior temporal
  epileptiform discharges activated in sleep; no seizure captured." is identical in M01, M02 and
  RM01, and "Normal sleep-deprived EEG ... A normal study does not exclude epilepsy." in M03 and
  RP02: write each impression from that study's own findings (electrodes, frequency, state); no
  teaching sentences. RP03's routine impression ends "Note: A single routine EEG has limited
  sensitivity (~29-55%) ...": delete the note.
- Capitalised teaching text in reports ("This is an ABNORMAL EEG due to: 1. ...") is acceptable
  report style; capitalised teaching lines in P03's video report ("NO ictal correlate - THIS IS
  PNES") are not: write them as a neurophysiologist would.

### L. Musts and prohibitions template (all)

Musts are case management, never work-up steps already scored by criteria. Delete process musts:
"Pursue prolonged video-EEG", "Obtain/Repeat 3T MRI epilepsy protocol", "Obtain routine EEG",
"Order FDG-PET", "Order neuropsychological battery", "Check topiramate level", "Order CT skull
base", "Obtain contrasted MRI" (M01, M02, M03, M05, P01, P03, P04, P05, RM01, RM02, RM03, RM04,
RP02, RP03, RP04, RP05, RS01, RS02, RS03, RS04, RS05, S01, S02, S03, S04, S05, S06). A must
that is really a diagnostic insight stays only if it is case management ("Do not treat as panic
disorder" is fine as a prohibition). Delete generic prohibitions unrelated to the case (M01
bupropion; S03 HLA in an African American patient; S05 "single normal routine EEG" when the EEG is
abnormal). Canonical texts (fill slots):

- First-line ASM: `Start <lamotrigine or levetiracetam> as first-line monotherapy for focal epilepsy, chosen for <case reason: contraception, mood history, pregnancy plans, interactions>.`
- Valproate prohibition (patients under 55): `Do not start valproate: it is not first-line for focal epilepsy and, under the 2024 MHRA rules, is not started under 55 unless two specialists document that no alternative works.`
- Women of childbearing potential: `Discuss contraception and pregnancy plans before choosing the ASM; start folic acid.`
- HLA (fact 10): every East, Southeast or South Asian patient who is starting or switching an ASM
  and has never taken carbamazepine or oxcarbazepine gets `Test HLA-B*15:02 before any carbamazepine or oxcarbazepine.`
  That is M02, M04, M05, P04, RS05, S04, S06 (not RM03: the switch is to levetiracetam or
  lamotrigine; not RS01, RS04: no carbamazepine start or long-term tolerated use). No HLA line in
  any other case (delete S03's).
- Driving: `Advise no driving until the locally applicable seizure-free interval is met and explain the duty to inform the licensing authority.`
- SUDEP (all cases with focal to bilateral tonic-clonic seizures or drug resistance): `Counsel on SUDEP risk and how seizure control reduces it.`
- Drug resistance (only P04, RP04, RS01, RS04 and RM03 if section 4 says so): `Refer to a comprehensive epilepsy center for presurgical evaluation: two appropriately chosen and tolerated ASM schedules have failed (ILAE 2010).`
- Lesional epilepsy amenable to surgery (S02, S03, S06, M04, M05, RM04, RP05): `Refer for epilepsy surgery evaluation of the <lesion>.` (no "drug-resistant" unless two ASMs failed).

### M. Prolactin (22 cases)

Prolactin rows are reported hours after the event (S01 at 6 h, M04 at 45 min, M05 at 2 h, RS05
about 7 h) or after a focal aware aura (RP05, 25 min), in pregnancy (RS02), and are used by KCE,
differentials and musts to argue for a seizure or against syncope. Decision (fact 11): delete the
prolactin row and every mention (impression, abnormal summary, KCE, differential, must, red
herring) in all cases except P05, where the level was drawn 22 minutes after a witnessed convulsion;
P05 keeps it as evidence against PNES only (see section 4). RP04's KCE, must and prohibition about
a "normal prolactin drawn 3 hours post-event" refer to a test the case does not contain: delete.

### N. Lateralization errors (M04, S06, RP05, RM01)

Fix the claims, not the HPI (fact 12): M04 KCE says right-hand automatisms are "contralateral to
the dominant lesion"; S06 must and KCE say right-sided automatisms and right tongue bite "confirm
left temporal onset"; RP05 KCE and differential call right-hand automatisms "contralateral". Write
that localization rests on EEG and MRI concordance, and on postictal language difficulty where
present. RM01: chronic left hemiparesis implies a right hemisphere injury and the focus is right
temporal, but the postictal deficit is a new RIGHT arm weakness: change the Todd paresis to the
left arm (worsening of the baseline left hemiparesis) in HPI, exam and every mention.

### O. Fabricated or misattributed sources in literature outputs (most)

Examples: "Glauser 2017 Epilepsia 58:1235-1268" (does not exist; used in M04, RS05, S05, S06 and
the pack), Knake Epilepsia 2005 (M01), Bernasconi N Brain 2019 (M04), Carne Brain 2004 with wrong
title and pages (P04), Tomson Lancet Neurol 2019 (RS02, S04, RS04), Wilson CID 2009 (RS02), Garcia
Lancet Neurol 2014 with a wrong title (RS02), Pennell Neurology 2008 with a wrong title (RS03),
Meador Epilepsia 2014 (RS03), Chassoux Neurology 2012 (S03), Englot Epilepsia 2012;53:1588 (S02,
S06), Zupanc Epilepsia 2006 (S04), Engel 2003 with a wrong title (RS05). Blank author fields
(`" | Title"`) in M01, M05, P05, RM01, RM02, RM03, RM04, RP01, RP02, RP04, RP05, RS01; journal and
year without authors in RP03. Evidence-level claims contradicting fact 6: "Level A evidence for
lamotrigine" (RM01, 24 years), "Level A-B evidence" for levetiracetam, lamotrigine, oxcarbazepine
and lacosamide (RP05), "lamotrigine and levetiracetam Level A", "oxcarbazepine (Level A)" (RS05).
Fix: sources only from 1.1; delete any other; state levels exactly as fact 6.

### P. Differential not updated to the assessment-time view (most)

Ruling 7: excluded mimics are `low` or `very_low`. Examples: P04 PNES `high` after video-EEG ictal
onset; M04 "MRI-negative" `high` after FCD found; P05 syncope `high` and PNES `moderate` after
video-EEG; P01, M02, M03 PNES `moderate`; RP01 tumor recurrence and radiation necrosis `high` after
MRI and HSV PCR; RP02 convulsive syncope from PE `high` after ambulatory EEG; RP03 ICI
encephalitis `high` after CSF; RP05 "MRI-negative TLE" `very_high`; RS02 eclampsia `high` after
normal BP and labs; RS04 coexisting PNES `moderate` after 11 captured seizures; RS01 isolated
mesial TLE `moderate` with a hamartoma on MRI. Each entry's text says which finding excluded it.

### Q. Discriminators and fallbacks

- RP02 body-imaging follow-up has `modality: "CT angiography"`: replace with `"study": "chest_CTA"`.
- P03 `fallback_tool_outputs.advanced_imaging` has `modality: "MRI"`: delete the fallback.
- P03, P05, RP01 `fallback_tool_outputs.specialized_test` has `test_type: "not_specified"`: delete.
- Echo fallbacks without `echo_type`: class I.

### R. Duplicate patients and inconsistent social history

Names repeat across cases: Delgado (M01, P01, both elementary school teachers), Chen (M02, M05),
Kapoor (M03 Caucasian, S03 African American, S06 South Asian), Sharma (M04, RS05), Ramirez (RM04,
RS02, RS03). Keep the name in M01, M02, S06 (Kapoor fits only her recorded ethnicity), M04, RM04;
rename P01, M05, M03, S03, RS05, RS02, RS03 with a name that fits the recorded
ethnicity and that no other case in the dataset uses (`grep -l` the cases before choosing).
Occupation contradictions between HPI and `social_history.occupation`: P01 (teacher vs graduate
student), S02 (teacher vs restaurant manager), S03 (teacher vs insurance adjuster), S04 (restaurant
worker vs manager). Make them agree, keeping the HPI's occupation.

### S. Claims about outputs the case does not contain (M01, M04, M05, RM02, RS01, RP04, RS02, P04)

KCE, differential or musts cite tests that are not served: M01 KCE (3T, FDG-PET, neuropsychology),
M04 PNES differential (video-EEG, prolactin), M05 KCE (prolactin at 2 h; no prolactin row), RM02
KCE (neuropsychology), RS01 KCE (neuropsychology), RP04 KCE and DDI output (lamotrigine 3.2 and
carbamazepine 9.8 levels; no labs output), RS02 must (urine protein, LFT; no labs ordered), P04
must (elevated prolactin). Either add the output where section 4 says so or delete the claim.

### T. ECG

ECG is `required` in 21 cases with the template evidence about pre-excitation and Brugada. Tier
(Reviewer 1's July ruling, 1.3): `optional` wherever the case stores an ECG, so ordering it at a
first presentation is credited and never waste; `required` only in P05 (seizure versus syncope is
the case question); `recommended` in RP02 (part of the PE assessment). Evidence names the actual
ECG result.
Rate words must match the stored `rate` (tachycardia only at 100/min or more): RM03 rate 98
("Sinus tachycardia, rate 98 bpm", "mild sinus tachycardia"), RP02 rate 96 ("borderline sinus
tachycardia"), RP03 rate 86 ("Sinus tachycardia borderline (86 bpm)"), RS02 rate 94 ("slight sinus
tachycardia appropriate for third trimester"): write `Normal sinus rhythm, <rate>/min` (RS02 may add
"upper normal for the third trimester"). Triage `vitals.hr` may differ by a few beats; keep it.

### U. Hippocampal volumetric arithmetic (S01, RS03, RS04, RS05, S04)

The finding's "reduced by approximately N%" disagrees with the stored volumes (numbers in section
4). The `asymmetry_index` values use (L - R)/(L + R) and are correct; keep that definition. Fix:
percentage = `1 - smaller/larger`, or change the smaller volume and recompute the index. RS04, RS05
and S04 share 1.9 cm3: give each its own value. Class F rewrites keep volumes, index and
percentage consistent.

### V. Patient-block contradictions and labels (S01, P02)

- S01 `neurological_exam.additional` says "No tongue bite observed" and then a lateral tongue bite:
  keep one (a right lateral tongue bite, which does not lateralize, fact 12).
- P02 `neurological_exam.motor` and `.additional` name the sign ("faciobrachial dystonic seizures
  (FBDS)"): describe the episodes (brief right arm extension with right facial contraction), do
  not name them; recognizing FBDS is what the case scores. P02 MMSE 22/30 lists lost points that
  sum to 10 ("missing 2 points"): make the itemized losses sum to 8.

---

## 3. Target pathway and tiers

### 3.1 Pathway order (followup_outputs and action_criteria)

Emergency or first presentation (S cases, RS05, RM03, RS02, RP01, RP02): labs and ECG, CT when
indicated, MRI, routine EEG, prolonged EEG (sleep-deprived, ambulatory, video, continuous ICU),
CSF when indicated, other specific tests (body imaging), drug check, literature.

Elective, inpatient or presurgical (M cases, P cases, RM01, RM02, RM04, RP03, RP04, RP05, RS01,
RS03, RS04): MRI, EEG (routine then prolonged or video), labs, ECG, CT or CSF when indicated,
FDG-PET, neuropsychology, drug check, literature.

`followup_outputs` follow the same order; literature always last.

### 3.2 Criteria rules

- MRI `{protocol: epilepsy}` required (exceptions in class E); the first EEG (`eeg_type` of the
  stored first study) required. One EEG required unless a later study is the one that establishes
  the diagnosis (section 4 says which).
- Sleep-deprived or ambulatory EEG `recommended` when the routine EEG is non-diagnostic or
  equivocal; delete the criterion (and its follow-up) when the routine EEG is diagnostic and
  concordant and nothing else needs it.
- Video-EEG `required` only in presurgical evaluation (P04, RP04, RS01, RS04), a PNES question (P01,
  P03) or seizure-versus-syncope (P05); otherwise `recommended` or absent.
- Labs (Reviewer 1: optional unless clinically indicated): `required` where a provoked cause or
  a management-critical value is the case question (P02 serum antibodies and sodium, RM03 trauma
  and phenytoin, RS02 eclampsia); `recommended` where the case holds a specific indication (an
  ASM level in breakthrough seizures: RM02, RP02, RP03, RP04, RS03; renal function for acyclovir:
  RP01; hypoglycemia in a metformin-treated patient: RS05); `optional` otherwise, including first
  presentations without a provoking clue.
- CSF: `required` P02, RP01; `recommended` RP03; elsewhere waste.
- FDG-PET: `required` P04; `optional` in other presurgical or lesional cases where it is a
  criterion (P01, P02, M04, RP04, RP05, RS01, RS04); waste or harm elsewhere (class J, RP03
  included).
- Neuropsychology `neuropsych_battery`: `recommended` in presurgical drug-resistant cases (P04,
  RP04, RS04); `optional` in M05, RP05.
- Drug check per class B; literature `optional` per class A; ECG per class T.
- `expected_evidence` is what the stored output shows, specific to the case.

### 3.3 Sequence constraints

- Hard: `MRI -> CSF` in P02, RP01, RP03 (exclude mass effect before LP), reason
  `Exclude mass effect on imaging before lumbar puncture.` P02's existing MRI -> CSF constraint is
  `soft`: make it hard (P02's second constraint is MRI -> drug check: class C).
- Soft: `MRI -> drug check` per class C only; RM03 `CT -> MRI` soft
  (`Head CT first after a fall with head injury and depressed consciousness.`).
- No constraint with literature, with an optional criterion, or that orders two EEG types.

### 3.4 Stop rule

`required_before_assessment` lists only the required criteria; `max_additional_actions: 1` for S
cases, 2 for all others.

---

## 4. Per-case index

Every log: "Reviewer notes: No reviewer notes for this case." Classes A, B, C, D, G, H, I, L, O and
the echo fallback of Q apply to every case and are not repeated. "PET: delete" means class J
(delete the follow-up, FDG_PET waste). "Prolactin: delete" means class M. "EEG limits" means
class K. Tier lines list every criterion the case keeps; max = `max_additional_actions`.

### M cases

- **FEPI-TEMP-M01** (41 F, right MTS, sertraline)
  - F: dedicated MRI with definite right HS; outside 1.5T in the history; red herrings citing the
    "initial 1.5T" move to the history path.
  - EEG limits (sleep-deprived "one habitual event", "48-hour"). PET: delete. Prolactin: delete.
  - S: KCE about 3T, PET, neuropsychology deleted. O: Knake 2005 and the rest replaced.
  - L: delete video-EEG and 3T musts and the bupropion prohibition; first-line ASM; keep "reassess
    the anxiety diagnosis"; driving; SUDEP.
  - Tiers: MRI, routine EEG required; sleep-deprived recommended; labs, ECG, drug check (sertraline,
    ibuprofen), literature optional; max 2.
- **FEPI-TEMP-M02** (41 F, right MTS, olfactory aura, sertraline, sumatriptan)
  - F: dedicated MRI, definite right HS. EEG limits (routine; sleep-deprived "48-hour").
  - PET: delete. Prolactin: delete (27 ng/mL). P: PNES to `low`. KCE "video-EEG gold standard" out.
  - L: delete video-EEG and 3T musts; first-line ASM; driving and classroom safety; HLA (East
    Asian); CT-in-lieu prohibition kept.
  - Tiers: as M01; drug check optional; max 2.
- **FEPI-TEMP-M03** (35 M Caucasian, right MTS "subtle", sertraline, metformin)
  - R: rename ("Kapoor" does not fit the recorded ethnicity; S06 keeps it).
  - F: dedicated MRI with mild but definite right HS (not "borderline").
  - EEG limits: ambulatory "48-hour 48-hour", "96 hours", "evolving bilateral" vs "remaining
    lateralized"; sleep-deprived limits. PET: delete. Prolactin: delete. P: PNES to `low`.
  - L: delete video-EEG and 3T musts; first-line ASM; driving.
  - Tiers: MRI, routine EEG required; sleep-deprived and ambulatory recommended (the ambulatory
    captures the events); labs, ECG, drug check optional; max 2.
- **FEPI-TEMP-M04** (26 M left-handed, left temporal FCD)
  - N: KCE "right-hand automatisms contralateral to the dominant lesion" rewritten (fact 12). The
    posterior superior temporal FCD is "left temporal, concordant with the left temporal EEG
    focus", not "concordant with F7/T3".
  - P: "MRI-negative TLE" (`high`) and left MTS (`moderate`, hippocampi symmetric and normal) to
    `low`. S: PNES differential cites video-EEG and prolactin not served.
  - Prolactin: delete (45 min). O: Bernasconi N 2019, Glauser 2017 replaced.
  - L: delete the two "teaching point" musts and the "do not accept a normal standard MRI" must;
    keep lesional surgical referral, first-line ASM, driving, SUDEP; add HLA (South Asian).
  - Tiers: MRI, EEG required; PET, ECG, labs, drug check optional; max 2.
- **FEPI-TEMP-M05** (38 F left-handed, right temporal cavernoma, cetirizine)
  - R: rename (duplicate Chen). S: KCE "prolactin at 2 h" deleted (no prolactin row).
  - Sources: use `[Cavernoma_2017]`; drop unverified Josephson 2013 and Zabramski 1994.
  - L: delete the GRE/SWI "order MRI" must (the MRI report must show the SWI hemosiderin rim);
    the acute-hemorrhage and thrombolysis "do not" musts move to prohibitions; keep surgical
    referral, ASM, driving; add HLA (East Asian).
  - Tiers: MRI required; first EEG required, second EEG recommended; neuropsychology, ECG, drug
    check optional; max 2.

### P cases

- **FEPI-TEMP-P01** (29 F, misdiagnosed panic disorder, sertraline, lorazepam, never on an ASM)
  - Label: "drug-resistant" is wrong (the refractoriness is to panic treatment); fixing the data
    would destroy the pitfall. CENTRAL request 4; workers do not edit the label.
  - MRI reported normal while the label says "suspected FCD on 3T": rewrite as a 3T epilepsy-protocol
    MRI with subtle right anterior temporal gray-white blurring and FLAIR signal suspicious for FCD
    (keep the two nonspecific white matter foci).
  - R: rename (duplicate Delgado); occupation teacher everywhere.
  - Penicillin "rash" vs drug output "hives": align; delete the claim on rash risk in women under 30.
  - Neuropsych impression in lab voice: rewrite as a neuropsychologist's summary.
  - L: delete drug-resistance, video and presurgical musts; musts: first-line ASM (lamotrigine,
    sertraline compatible), lorazepam taper once seizures are treated, revisit the panic diagnosis
    with psychiatry, driving. P: PNES and panic to `low`.
  - Tiers: MRI, routine EEG, video-EEG (event capture for panic versus seizure) required; PET,
    neuropsychology, ECG (normal Holter), drug check optional; max 2.
- **FEPI-TEMP-P02** (31 M, LGI1 encephalitis, label kept; levetiracetam, carbamazepine,
  lacosamide)
  - A: leak; delete the initial literature and drug blocks (their `general` entries only repeat
    the criteria's expected evidence).
  - Labs: raise the existing labs criterion to required with panels `autoimmune_encephalitis` and
    `sodium`; stored labs add serum LGI1 IgG positive by cell-based assay (keep sodium 126 mEq/L,
    carbamazepine 8.2) and the interpretation names carbamazepine as a contributor to the
    hyponatremia.
  - V: describe the episodes in the exam without naming FBDS; MMSE losses sum to 8.
  - Tumor screening: add a recommended `order_body_imaging {study: chest_CT}` criterion after the
    CSF, with a stored follow-up (no thymoma or mediastinal mass); delete the "chest/abdomen/pelvis
    CT, testicular ultrasound" must (the criterion scores it). P: presumed drug-resistant TLE and
    NMDAR encephalitis to `low`; "Paraneoplastic limbic encephalitis (CASPR2 / GAD65)" becomes
    "Other antibody-mediated limbic encephalitis (CASPR2, GAD65, onconeural)" `low`; HSV entry ICD
    `B00.4`.
  - CSF says "LGI1 detected in CSF" while the evidence says serum: CSF normal or mildly raised
    protein, LGI1 negative or weak (fact 19); evidence matches.
  - MRI: drop teaching capitals ("SWELLING, NOT atrophy"); report voice.
  - Musts: immunotherapy (kept), review carbamazepine with hyponatremia; "do not escalate ASMs
    alone" kept. EEG evidence: the stored video-EEG's actual events (6 brief events with a subtle
    bilateral temporal onset); FBDS often lack an EEG correlate.
  - Tiers: MRI (no arguments), CSF (hard MRI -> CSF), labs, video-EEG required; chest CT, drug
    check recommended; ECG, PET, literature optional; max 2.
- **FEPI-TEMP-P03** (38 F, PNES with controlled right MTLE, lamotrigine, alprazolam)
  - A: leak; delete empty initial blocks. K: teaching capitals in the video report rewritten.
  - Q: delete `advanced_imaging` (modality "MRI") and `specialized_test` ("not_specified")
    fallbacks.
  - P: breakthrough epileptic seizures to `low`.
  - Musts kept: lamotrigine unchanged, CBT-based therapy, alprazolam taper with addiction medicine,
    explain the diagnosis. Delete the "admit for video-EEG" must. Driving follows the epileptic
    seizure status.
  - Tiers: MRI, video-EEG required; drug check, literature optional; FDG_PET waste kept; max 2.
- **FEPI-TEMP-P04** (30 F South Asian, drug-resistant right TLE, MRI-negative, lamotrigine,
  metformin, oral contraceptive, sulfonamide allergy)
  - No MRI criterion: add `metadata.panel_required_exemptions` for MRI (prior 1.5T epilepsy-protocol
    MRI normal; could not tolerate 3T; declined general anesthesia) and make the history say so.
  - CT impression "This remains MRI-negative focal epilepsy" is a leak: CT findings only.
  - P: PNES to `low`. S: delete the "elevated prolactin" must and all prolactin mentions.
  - O: Carne RP et al., Brain 2004;127:2276-2285, "MRI-negative PET-positive temporal lobe
    epilepsy: a distinct surgically remediable syndrome" (allowed in this case).
  - Drug check required: ethinylestradiol lowers lamotrigine (fact 8); zonisamide is a sulfonamide.
    Musts: presurgical referral, contraception, SUDEP, HLA-B*15:02 before carbamazepine or
    oxcarbazepine.
  - I: delete CT and ECG avoided actions.
  - Tiers: video-EEG, FDG-PET, drug check required; neuropsychology recommended; CT, literature
    optional; max 2.
- **FEPI-TEMP-P05** (55 M, right MTS with remote cortical injury, cardiology syncope work-up,
  lisinopril, atorvastatin)
  - M: prolactin at 22 min kept; the must and KCE saying it favors seizure over syncope are wrong
    (fact 11): "argues against PNES; does not separate seizure from syncope".
  - Q: delete the `specialized_test` fallback. O: blank authors replaced.
  - P: syncope to `low`, PNES to `very_low`.
  - Musts: pacemaker and antiarrhythmic prohibitions kept; ASM without inducers (atorvastatin,
    fact 9); driving; SUDEP; delete the video-EEG must.
  - Tiers: MRI, routine EEG, video-EEG, ECG required; drug check recommended; labs, literature
    optional; FDG_PET waste kept; max 2.

### RM cases

- **FEPI-TEMP-RM01** (24 M, right MTS after neonatal meningitis, VP shunt, chronic left
  hemiparesis, baclofen)
  - F: dedicated MRI with definite right HS plus meningitis sequelae (right hemispheric gliosis,
    catheter, stable ventricles), the label's dual pathology.
  - N: Todd paresis to the left arm. EEG "breach rhythm ... prior craniotomy": "over the right
    parietal shunt burr-hole site". EEG limits: remove the subclinical seizure.
  - PET: delete and drop (describes a nonexistent left lesion). Prolactin: delete; delete other
    stray abnormal rows (TSH, CK, lactate) unless used.
  - CT: add a recommended `order_ct_scan` with a stored CT (catheter in place, stable ventricles)
    replacing the "confirm shunt functioning" must; delete CT waste. Shunt LP prohibition kept;
    carbamazepine-hyponatremia prohibition deleted.
  - Tiers: MRI, routine EEG required; sleep-deprived, CT recommended; labs, drug check optional;
    max 2.
- **FEPI-TEMP-RM02** (29 F, TSC, valproate, clobazam, oral contraceptive)
  - F: dedicated MRI with the left mesial temporal tuber and definite left HS.
  - HPI sentence on an ECG abnormality "prompting additional cardiac workup" has no ECG: delete it.
  - PET: delete. Prolactin: delete. S: KCE about neuropsychology deleted.
  - Drug check required: valproate in a woman of childbearing potential (fact 7), lamotrigine with
    valproate and with ethinylestradiol (facts 8, 9) for the planned switch; no "Category X".
  - Musts: switch away from valproate within a pregnancy prevention programme, adherence, TSC
    surveillance [TSC_2021], everolimus only if refractory [EXIST3_2016]; delete video and 3T musts.
  - Tiers: MRI, routine EEG, drug check required; labs recommended (valproate 38 with missed
    doses); literature optional; no ECG criterion (the case stores no ECG); max 2.
- **FEPI-TEMP-RM03** (27 M South Asian, ECCL, phenytoin non-adherence, prolonged GTC, fall with
  head injury, GCS 8)
  - CT: add a required `order_ct_scan` first (minimally depressed right parietal fracture, no
    hemorrhage, scalp lipoma, intracranial lipomas and calcifications); soft CT -> MRI; delete CT
    waste; must: neurosurgical review of the fracture.
  - F: dedicated MRI with definite right HS (not "equivocal").
  - Labs required (phenytoin total and free, glucose, CK, lactate, electrolytes); prolactin: delete.
    T: ECG rate 98: "Normal sinus rhythm, 98/min". PET: delete. Delete the video-EEG must.
  - Musts: reload or switch the ASM with a reliable supply (social work for refills), treat
    recurrence as status epilepticus, SUDEP.
  - Tiers: CT, MRI, routine EEG, labs required; drug check recommended; ECG, literature optional;
    max 2.
- **FEPI-TEMP-RM04** (34 M left-handed, left superior temporal gyrus ganglioglioma, sertraline)
  - PMH "sertraline now tapered off" vs 50 mg in the list: "tapered from 100 to 50 mg six weeks ago".
  - Prolactin: delete, with the migraine differential's "elevated prolactin".
  - L: delete the gadolinium MRI must and the presurgical video must; keep neurosurgery referral for
    resection and tissue diagnosis.
  - Drug check recommended (inducers lower sertraline, fact 9; levetiracetam mood effects are an
    adverse effect, not an interaction).
  - Tiers: MRI, routine EEG required; drug check recommended; ECG, labs (iron deficiency is the red
    herring), literature optional; max 2.

### RP cases

- **FEPI-TEMP-RP01** (59 M, HSV-1 encephalitis with NCSE after skull-base cancer treatment,
  dexamethasone, metformin, amlodipine)
  - Label: not epilepsy (fact 2); CENTRAL request 3; workers do not edit the label.
  - CSF WBC 3, protein 38 vs evidence "pleocytosis": rewrite to a lymphocytic pleocytosis with raised
    protein and some red cells, HSV-1 PCR positive (fact 18).
  - Drug output: amlodipine does not prolong PR; "dexamethasone may reduce seizure threshold":
    delete both.
  - Continuous ICU EEG: ACNS terms (lateralized periodic discharges, right temporal electrographic
    seizures) and a limitations line.
  - PET: delete. Prolactin: delete. Q: delete the `specialized_test` fallback.
  - P: tumor recurrence and radiation necrosis to `low` after MRI and PCR.
  - Tiers: MRI `{contrast: true}`, CSF (hard MRI -> CSF), continuous ICU EEG required; labs (renal
    function for acyclovir, glucose), drug check recommended; literature optional; delete CT waste;
    max 2.
- **FEPI-TEMP-RP02** (31 M pilot, MRI-negative left mesial TLE, concurrent PE, levetiracetam)
  - Q: body imaging `study: chest_CTA`.
  - The brain MRI's "4 mm lingular nodule on scout images" is implausible: delete it from the MRI
    and from the hypercoagulability literature output.
  - EEG limits (sleep-deprived "Three-day monitoring"; ambulatory "48-hour 48-hour"). PET: delete.
    Prolactin: delete.
  - Drug check required (inducers lower DOAC and warfarin, fact 9; levetiracetam 8.2 low).
  - P: convulsive syncope from PE and cardiogenic syncope to `low`.
  - Musts: anticoagulation for PE, FAA certification and no flying or driving (kept); delete the
    video and 3T must.
  - Tiers: MRI, routine EEG, ambulatory EEG (captures the events that make the diagnosis), chest
    CTA, drug check required; sleep-deprived, labs (D-dimer, level), ECG recommended; two
    literature criteria optional and last; max 2.
- **FEPI-TEMP-RP03** (30 F, metastatic melanoma on ipilimumab and nivolumab, enlarging left temporal
  metastasis, levetiracetam non-adherence, dexamethasone, escitalopram)
  - The brain MRI reports vertebral metastases (T4, T7, T11, L2, L4): remove them from the brain
    MRI. The exam has a right-sided L2 to L4 pattern (right hip flexion 4+/5, ankle dorsiflexion
    5-/5, right patellar 1+): put the spine in the history ("staging spine MRI two weeks ago:
    vertebral metastases including L2 and L4 with right L3-L4 foraminal tumor, no cord compression
    or epidural disease"), and make the exam fit a right lumbar radiculopathy (tone normal, right
    plantar flexor).
  - CSF (now WBC 8, protein 73) `recommended` (mild mass effect, no shift): rewrite to normal cells
    (WBC 0 to 4), normal or mildly raised protein, cytology, flow and antibodies negative; evidence
    matches.
  - P: ICI neurotoxicity (`high`) and leptomeningeal disease (`moderate`) to `low`.
  - PET: delete criterion, follow-up and PET must (class J); FDG_PET waste.
  - T: ECG "Sinus tachycardia borderline (86 bpm)" deleted.
  - Prolactin: delete. Labs recommended (levetiracetam level 8.2, TSH 6.8 for ICI thyroiditis).
  - Musts: levetiracetam adherence or lacosamide add-on, oncology for radiosurgery or resection and
    ICI decisions, driving.
  - Tiers: MRI `{contrast: true}`, routine EEG required; CSF (hard MRI -> CSF), labs, drug check
    recommended; ECG, literature optional; delete CT waste; max 2.
- **FEPI-TEMP-RP04** (47 M, drug-resistant left TLE, HS with temporopolar abnormality,
  lamotrigine, carbamazepine)
  - Label wording "dual pathology ... FCD Type IIIa" (fact 13): CENTRAL request 5.
  - F: 3T dedicated MRI with left HS and left temporopolar gray-white blurring "possibly FCD type
    IIIa"; delete "3T recommended".
  - S: the drug output quotes lamotrigine 3.2 and carbamazepine 9.8 levels no output reports: add an
    initial labs output (AED levels, sodium) and a `recommended` labs criterion; the drug output
    explains induction without the numbers. KCE "right temporal delta on initial inpatient EEG":
    reword to the outpatient EEG and the video-EEG.
  - Prolactin: delete the KCE, must and prohibition. O: blank sources replaced (keep Kwan 2010).
  - P: HS single pathology to `moderate`; bitemporal to `low`.
  - Musts: presurgical referral, resection including the temporopolar region (prohibition kept,
    reworded), SUDEP, driving; delete 3T, video, PET, neuropsychology musts.
  - Tiers: MRI, video-EEG, drug check required; neuropsychology, labs recommended; PET, literature
    optional; max 2.
- **FEPI-TEMP-RP05** (41 F, left temporal encephalocele, never treated, obesity, empty sella)
  - F: dedicated MRI with thin coronal sequences showing the left anteroinferior temporal
    encephalocele and normal hippocampi; the 1.5T studies in the history. Red herrings: [0]
    ("routine 1.5T MRI reported as no acute abnormality") moves to `patient.history_present_illness`;
    [1] (empty sella) keeps pointing at the MRI finding that reports the partial empty sella.
  - A: leak in the encephalocele literature follow-up.
  - Not drug-resistant: delete the KCE on "two appropriate AED trials" and "drug-resistant course"
    in the referral must.
  - N: right-hand automatisms are not "contralateral"; postictal expressive language difficulty is
    the lateralizing sign. Prolactin: delete (25 min after an aura).
  - "Blurred disc margins": the fundoscopy reports them (mildly blurred, no spontaneous venous
    pulsations, no frank papilledema): keep the IIH red herring, its differential and the
    prohibition; KCE says only that these features are associated with temporal encephaloceles.
  - P: MRI-negative TLE, HS to `low`; PNES to `very_low`.
  - Tiers: MRI, routine EEG required; video-EEG, CT skull base recommended; ECG, PET,
    neuropsychology, labs, drug check (ibuprofen), literature optional; max 2.

### RS cases

- **FEPI-TEMP-RS01** (22 M East Asian, hypothalamic hamartoma with gelastic seizures and left HS,
  valproate, clonazepam, levetiracetam)
  - F: the MRI calls the 1.3 x 1.6 cm sessile tuber cinereum lesion a "Hypothalamic mass", never
    names it, and the impression omits it ("Post-gamma knife treatment changes" plus "subtle" HS):
    dedicated MRI with thin hypothalamic sections whose findings and impression state the residual
    sessile lesion consistent with hypothalamic hamartoma (MRI establishes it: Kind 2) and definite
    left HS (fact 4).
  - Drug output: valproate does not raise clonazepam by CYP3A4 inhibition; delete the mechanism.
  - S: KCE neuropsychology deleted. P: isolated mesial TLE to `low`.
  - L: delete MRI, video, PET musts; keep surgical referral (hamartoma treatment), endocrine
    follow-up; SUDEP.
  - Tiers: MRI, video-EEG required; PET, drug check, literature optional; max 2.
- **FEPI-TEMP-RS02** (31 F, 33 weeks pregnant, right MTS with calcified neurocysticercosis, missed
  levetiracetam)
  - R: rename (duplicate Ramirez); PMH "initially attributed to vasovagal syncope, then diagnosed as
    epilepsy".
  - F and E: non-contrast 1.5T epilepsy-protocol MRI with definite right HS and calcified granulomas
    on SWI, no cyst or scolex on 3D T2; criterion `{protocol: epilepsy, contrast: false}`; avoided
    action MRI `{contrast: true}` `harmful` [ACOG_imaging_2017].
  - Labs required (fact 16): normal urine protein/creatinine, platelets, creatinine, AST/ALT,
    sodium, glucose, levetiracetam 5.8 low; panels `urinalysis`, `CBC`, `LFT`, `CMP`, `AED_levels`.
  - T: ECG rate 94: "Normal sinus rhythm, 94/min". EEG limits (keep "hyperventilation omitted in
    pregnancy").
  - PET: delete; FDG_PET avoided action `harmful`. I: delete CT waste.
  - P: eclampsia, active neurocysticercosis to `low`; metabolic to `very_low`.
  - O: Tomson 2019 and Wilson 2009 deleted; Garcia 2014 with its real title.
  - Musts: obstetric and fetal assessment (kept), levetiracetam restart and level-guided dose
    increase, reduction after delivery, no antiparasitic drug (albendazole prohibition kept), social
    work and medication access, newborn safety; delete the MRI must.
  - Tiers: MRI, routine EEG, labs required; ECG, drug check, literature optional; max 2.
- **FEPI-TEMP-RS03** (31 F, right MTS on topiramate 17 years, 6 weeks postpartum, breastfeeding)
  - R: rename (duplicate Ramirez). E: delete the gadolinium line. EEG limits. PET: delete.
    U: 2.0 vs 3.3 cm3 is 39%, not "approximately 30%".
    Prolactin: delete (4 h).
  - Topiramate 3.2 low at 6 weeks postpartum on an unchanged dose: clearance normalizes after
    delivery, so the labs and KCE point to missed doses, not to postpartum clearance.
  - O: Meador 2014, Pennell 2008, Harden Epilepsia 2009 replaced by `[AAN_WWE_2009]`, `[EURAP_2018]`.
  - Musts: topiramate pregnancy prevention programme and contraception, consider switching to
    lamotrigine or levetiracetam, breastfeeding with infant monitoring, infant safety (no bathing
    alone, change on the floor), sleep protection; delete the 3T and "check level" musts and the
    "no second ASM without the level" prohibition.
  - Tiers: MRI, routine EEG required; labs (topiramate level, bicarbonate), drug check recommended;
    literature optional; max 2.
- **FEPI-TEMP-RS04** (29 F Japanese, drug-resistant right MTS on valproate, phenobarbital,
  carbamazepine)
  - U: 1.9 vs 3.2 cm3 is 41%, not "approximately 30%"; volumes shared with RS05 and S04.
  - E: delete gadolinium lines. "Three convulsive episodes per week" (once weekly is convulsive):
    "three seizures per week".
  - Neuropsych in lab voice: rewrite (nonverbal memory deficit, right temporal dysfunction).
  - PET text is identical to RS03's: write a distinct report or drop it with the optional criterion.
  - P: coexisting PNES to `low`; "topiramate-induced slowing" becomes phenobarbital sedation.
  - Prohibition on "dominant-hemisphere lobectomy": right HS is non-dominant here; reword to "do not
    plan resection without memory and language lateralization (neuropsychology, fMRI or Wada where
    uncertain)".
  - Drug check required (fact 9 triple interactions, fact 7); long-term carbamazepine: no HLA test.
  - Musts: presurgical referral, valproate pregnancy prevention programme, rationalize polytherapy,
    SUDEP; delete video, 3T, PET, neuropsychology musts.
  - Tiers: MRI, video-EEG, drug check required; neuropsychology recommended; PET, labs, literature
    optional; max 2.
- **FEPI-TEMP-RS05** (52 M South Asian, left MTS, first convulsion after a year of auras, metformin,
  amlodipine)
  - R: rename (duplicate Sharma). E: delete the gadolinium line. U: 1.9 vs 3.2 cm3 is 41%, not
    "approximately 28%".
  - KCE "ILAE 2017 criteria after a single convulsion": recurrent focal seizures meet fact 1
    `[ILAE_def_2014]`; delete the overstated amlodipine KCE.
  - O: "Glauser updated 2017" and the wrong Engel 2003 title; "lamotrigine Level A, oxcarbazepine
    Level A" wrong (fact 6). Prolactin: delete. Red herring `labs.panels.BMP[6]`: verify it is
    glucose.
  - Musts: first-line ASM, driving, SUDEP, HLA-B*15:02 before carbamazepine or oxcarbazepine;
    delete 3T and "confirm concordant" musts; oxcarbazepine prohibition becomes sodium monitoring.
  - Tiers: MRI, routine EEG required; labs (glucose: hypoglycemia on metformin is the provoked-seizure
    question) recommended; ECG, drug check, literature optional; max 2.

### S cases

- **FEPI-TEMP-S01** (34 M, left MTS, first convulsion, omeprazole)
  - Prolactin: delete (6 h). EEG limits. PET: delete. E: delete "No enhancement after gadolinium".
  - KCE "ILAE criteria ... after a single seizure require >=60% ...": the HPI has three or four
    stereotyped deja vu and epigastric auras in six months, so the two-seizure criterion is met
    (fact 1); KCE "First-line ... (ILAE 2017 guideline)": rewrite per fact 6.
  - U: 2.1 vs 3.4 cm3 is a 38% reduction, not "approximately 25%". V: tongue-bite contradiction.
  - Label identical to RS05's: keep, but MRI values and KCE differ from RS05's.
  - L: delete routine EEG and 3T musts; first-line ASM, driving, SUDEP, valproate prohibition.
  - Tiers: MRI, routine EEG required; labs, ECG, drug check, literature optional; max 1.
- **FEPI-TEMP-S02** (27 F left-handed, right mesial temporal DNET, oral contraceptive)
  - R: occupation teacher. Prolactin: delete. EEG limits. PET: delete. E: post-contrast line in the
    report; delete the "MRI with contrast" must.
  - MRI identical to S03's (18 x 14 x 12 mm): change S02's size and description.
  - O: sources replaced by `[Blumcke_2017]`. P: ganglioglioma to `moderate`.
  - Tiers: MRI, routine EEG, drug check (ethinylestradiol and lamotrigine, fact 8) required; labs,
    ECG, literature optional; max 1.
- **FEPI-TEMP-S03** (42 M left-handed, right mesial temporal DNET, vitamin D)
  - R: rename ("Kapoor" in an African American patient; S06 keeps it); occupation teacher. Allergy "Contrast dye": "iodinated CT contrast
    (mild urticaria)".
  - Prolactin: delete. EEG limits. PET: delete. L: delete the contrast MRI must and the HLA
    prohibition. P: ganglioglioma to `moderate`.
  - Tiers: MRI, routine EEG required; labs, ECG, drug check, literature optional; max 1.
- **FEPI-TEMP-S04** (19 F East Asian left-handed, right MTS, sertraline, oral contraceptive)
  - R: restaurant worker in both fields. Prolactin: delete. EEG limits. PET: delete. E: delete the
    gadolinium line. U: 1.9 vs 3.3 cm3 is 42%, not "approximately 30%".
  - Drug output "lamotrigine does not interact with oral contraceptives" is wrong (fact 8).
  - O: Zupanc 2006 and Tomson 2019 replaced; Wiebe 2001 kept.
  - Musts: first-line ASM with the contraceptive interaction, HLA-B*15:02 before carbamazepine or
    oxcarbazepine, kitchen safety, driving, SUDEP; delete 3T and EEG musts.
  - Tiers: MRI, routine EEG, drug check required; labs, ECG, literature optional; max 1.
- **FEPI-TEMP-S05** (33 M, left MTS, right-hand dystonia, postictal dysphasia, loratadine)
  - KCE and must "ILAE 2017 diagnosis after a single seizure": recurrent focal seizures (fact 1).
    KCE on "negative first recording" and the matching prohibition: delete (EEG abnormal).
    Lateralizing claims are correct: keep.
  - Prolactin: delete. EEG limits. O: Glauser 2017 replaced; literature text per fact 1.
  - Tiers: MRI, routine EEG required; labs, ECG, drug check, literature optional;
    FDG_PET waste; max 1.
- **FEPI-TEMP-S06** (24 F South Asian, left inferior temporal DNET, no hormonal contraception)
  - R: keep the name (Kapoor fits her recorded South Asian ethnicity; M03 and S03 are renamed).
    N: KCE and must on right-sided automatisms and tongue bite "confirming" left onset rewritten
    (fact 12).
  - Red herring path `initial_tool_outputs.mri.findings[0].size` exists ("14 x 11 x 10 mm"); keep it
    unless you change the size, then keep path and data point in step.
  - Prolactin: delete. EEG limits. O: Blumcke 2021, Glauser 2017, Englot 2012 replaced. P:
    ganglioglioma to `moderate`.
  - Musts: non-inducing first-line ASM (future contraception), lesional surgical referral, lab
    safety, driving, HLA-B*15:02 before carbamazepine or oxcarbazepine; delete the MRI must.
  - Tiers: MRI, routine EEG required; labs, ECG, drug check, literature optional;
    FDG_PET waste; max 1.

---

## 5. CENTRAL requests (outside the case files)

1. Criteria pack `criteria_packs/FEPI-TEMP.md`: the `[ILAE_drug_2017]` entry cites "Glauser 2017
   Epilepsia 58:1235-1268", which does not exist; correct it to Glauser T et al., Epilepsia
   2013;54:551-563 (keep the key name to avoid churn, or rename to `ILAE_drug_2013` across the 30
   cases in one pass). The pack's workup hierarchy generates this round's defects and must follow
   section 3: literature and drug check are not "Required" (rulings 5, 6); prolactin is not a
   routine lab (fact 11); CT is indicated in the emergencies of fact 3, not "inferior" in every
   case; the section 5 example "tumor -> consider carbamazepine" is wrong (fact 9: non-inducing
   ASMs with oncologic therapy); section 7 "Elevated prolactin supports recent convulsion" needs the
   timing caveat; video-EEG and PET tiers per 3.2.
2. Pack allow-list: add the keys marked (CENTRAL) in 1.1, starting with `NICE_NG217_2025` (already
   used in every case), `ILAE_MRI_2019`, `IFCN_ILAE_EEG_2023`, `SANAD2_2021`, `ILAE_def_2014`,
   `AAN_prolactin_2005`, `Lateralization_2005`, `ILAE_HS_2013`, `ILAE_FCD_2011`, `ILAE_PNES_2013`,
   `AAN_SUDEP_2017`, `CPIC_2018`, `Graus_2016`, `ILAE_ASS_2010`, `ACOG_imaging_2017`, `Ray_2016`.
3. Label RP01: acute symptomatic NCSE in HSV-1 encephalitis is not epilepsy (Beghi 2010). Decision:
   accepted[0] becomes "Nonconvulsive focal status epilepticus of temporal origin due to HSV-1
   encephalitis in a post-radiotherapy patient (acute symptomatic, not epilepsy)", icd_codes[0]
   `B00.4` with `G41.8` second; synonyms "HSV encephalitis", "herpes simplex encephalitis",
   "nonconvulsive status epilepticus", "acute symptomatic seizures". The case stays in
   `focal_epilepsy_temporal` as a mimic (like P02 and P03); the epilepsy synonyms are removed from
   this case.
4. Label P01: "drug-resistant" is wrong (no ASM ever given). Decision: accepted[0] becomes "Focal
   epilepsy of right temporal lobe origin with suspected focal cortical dysplasia on 3T
   epilepsy-protocol MRI, misdiagnosed as refractory panic disorder", icd_codes[0] `G40.209` (not
   intractable) instead of `G40.219`.
5. Label RP04: replace "dual pathology (left mesial temporal sclerosis and adjacent left temporal
   focal cortical dysplasia, FCD Type IIIa)" with "left hippocampal sclerosis with associated left
   temporopolar cortical abnormality (suspected FCD type IIIa)" (Blumcke 2011); ICD unchanged.
6. Synonyms (`diagnosis_synonyms.yaml`): every FEPI case inherits "mesial temporal lobe epilepsy"
   and "mesial temporal sclerosis epilepsy", including lateral neocortical (RM04), neocortical DNET
   (S06), encephalocele (RP05) and FCD (M04, P01) cases, where they are wrong; and the shared code
   list contains `G40.009`/`G40.019` (idiopathic localization-related), which do not fit structural
   epilepsy. Make the MTLE synonyms per case or per sub-entity, and drop the idiopathic codes from
   the structural TLE list.
7. `conditions.yaml` FEPI-TEMP `common_followups`: neuropsychological testing is listed under
   `interpret_labs` and FDG-PET under `analyze_brain_mri`; move them to `order_specialized_test`
   (`neuropsych_battery`) and `order_advanced_imaging` (`FDG_PET`), and limit FDG-PET to
   presurgical drug-resistant cases. Remove the seeded repeat "3T MRI with epilepsy protocol"
   follow-up (it produced class F and the 3T musts): the first MRI is the dedicated study.
8. `test_guidance_claims.py` / the July reply: the claim that prolactin was removed from the
   template was false; after this round it becomes true (only P05 keeps a timed level). Update the
   claim text and the test if it encodes the old wording.
9. Dataset-wide duplicate patient names: run a name check across all conditions (FEPI alone had 5
   duplicate surnames, two with the same occupation and name).
10. Vocabulary: no HLA genotype term exists; not needed as a criterion (fact 10 keeps it a must).
    No action unless another condition needs it.

## 6. Open questions for Andrea

None. All judgment calls are decided above per Andrea's 24 October 2026 ruling; the three label
corrections (RP01, P01, RP04) are decided and handed to CENTRAL because workers do not edit labels.
