# Criteria pack: Normal Pressure Hydrocephalus

**ICD-10-CM, per case:** G91.2 ((idiopathic) normal pressure hydrocephalus) for iNPH, copathology
cases included; G91.0 (communicating hydrocephalus, which ICD-10-CM uses for secondary NPH) for the
secondary cases (NPH-M06 after subdural haematoma, M08 after meningitis, M09 after head injury, P05
after aneurysmal SAH); G91.3 (post-traumatic hydrocephalus, unspecified) is also accepted in M09.
G91.2 and G91.0 never grant each other, and the secondary cases do not accept a bare "NPH" label:
with token matching it would credit "idiopathic NPH", which an antecedent excludes
(`diagnosis_synonyms.yaml`, 24 Oct 2026).
**Condition enum:** `NeurologicalCondition.NPH`
**Case ID prefix:** `NPH`

Updated 24 Oct 2026 to the October 2026 review round (`data/review/round-2026-10/plans/NPH.md`,
`NPH-summary.md`) and its close-out (`plans/NPH-decisions.md`). No physician has annotated the
cases; the July 2026 tool review (Reviewer 1) is the only physician input: MRI required with the
NPH markers; the tap test required with opening pressure and objective pre/post gait; generic CSF
assays, advanced imaging and the neuropsychological battery removed; labs optional and targeted.

---

## 1. Diagnostic criteria

**Clinical (probable iNPH)** [Relkin_2005]: insidious onset after age 40; duration of at least 3 to
6 months; no antecedent event (head trauma, haemorrhage, meningitis, other known cause of secondary
hydrocephalus); progression; a gait or balance disturbance plus at least one of cognitive
impairment or urinary symptoms. The full triad is not required: its absence never excludes iNPH and
its presence never establishes it.

**Imaging** [Relkin_2005] [Nakajima_2021]:
- Required: ventricular enlargement not entirely attributable to atrophy (Evans index greater than
  0.3; 0.30 exactly does not meet it), no macroscopic obstruction to CSF flow.
- At least one supportive feature: temporal horns enlarged out of proportion to hippocampal atrophy;
  an acute callosal angle (below 90 degrees, coronal plane through the posterior commissure);
  periventricular signal change not attributable to small-vessel disease; an aqueductal or
  fourth-ventricle flow void.
- DESH has two components: tight high-convexity and medial parietal sulci, and enlarged Sylvian
  fissures. It has a high positive and low negative predictive value.

**Pressure and CSF content:** opening pressure 70 to 245 mmH2O (about 7 to 24.5 cmH2O)
[Relkin_2005]; 200 mmH2O or less for probable iNPH in the Japanese guideline [Nakajima_2021]. Cell
count, protein and glucose normal.

**Categories** [Nakajima_2021]: possible iNPH (age 60 or over, compatible syndrome, Evans index
above 0.3, no antecedent); probable (possible plus normal-pressure, normal-content CSF and either
DESH with gait disturbance, or improvement after a tap or drainage test); definite (improvement
after shunting).

**Secondary NPH:** communicating hydrocephalus with an identified antecedent (SAH, meningitis, head
injury, intracranial surgery or subdural haematoma) is secondary NPH, not iNPH; it is treated by
the same shunt route.

**Copathology:** iNPH coexists with Alzheimer's disease, Parkinson's disease, PSP and bvFTD more
often than chance predicts. A coexisting disease lowers the expected benefit (mainly gait improves)
but does not exclude shunting; amyloid positivity does not by itself exclude the need for a shunt
[Nakajima_2021].

**PSP sign (P07):** a midsagittal midbrain-to-pons diameter ratio below 0.52 is specific for PSP
[Massey_2013]; 0.55 is not.

## 2. Standard workup hierarchy

Order of `action_criteria` and `followup_outputs` (the review app reads it as the work-up
sequence): brain MRI; labs; baseline timed gait; cognitive screen; spine MRI where a spinal mimic
exists; CSF tap test; post-tap reassessment; extended lumbar drainage (P08); CSF AD biomarkers and
neuropsychological battery (P09). **No literature criterion, initial output, follow-up or fallback
(ruling 5), and no drug-interaction step except P06's optional tamoxifen check** (ruling 6).

**Required in every case:**
- `analyze_brain_mri {}`: technique line (no contrast needed; P06 may use contrast), Evans index,
  callosal angle, temporal horns with an MTA score, DESH (both components, present or absent),
  periventricular signal with the Fazekas grade, aqueduct and fourth ventricle, no obstruction,
  case-specific lesions (old infarct, burr holes, coil artefact, TBI residue, SWI nigral finding,
  midbrain and pons measures). The impression is descriptive ("Communicating ventriculomegaly
  (Evans index x) with ... and no obstructing lesion"): never iNPH, a shunt or a disease name
  [Relkin_2005] [Nakajima_2021]
- `perform_clinical_assessment {"assessment_type": "gait_and_balance_timed"}`, the baseline: TUG,
  10-m walk time and steps, turn steps, qualitative gait features; `criteria_met` and
  `pre_post_comparison` null; no post-tap value [Nakajima_2021]
- `analyze_csf {}`, the tap test: 30 to 50 mL removed, the same timed measures at 2 to 4 hours and
  24 hours [Nakajima_2021]; the report gives opening pressure, content and the tap figures with %
  change, never "positive", "responsive", "supports shunting" or "refer". Sensitivity 26% to 61%,
  PPV 73% to 100% [Marmarou_2005]: **a single negative tap does not exclude shunt-responsive iNPH**.
  An improvement of 10% or more in TUG is a commonly used positive threshold in tap-test studies;
  no guideline sets a single cut-off, so the cases do not cite one for it. P06: the required CSF
  criterion carries the cytology alternatives (`["cytology"]`, `["cytology", "flow_cytometry"]`)

**Recommended:**
- Post-tap reassessment, `perform_clinical_assessment {"assessment_type": "gait_and_balance_timed"}`,
  served by a follow-up with trigger `request_post_reassessment` and the prose `assessment_type`
  "gait_and_balance_timed (post-tap reassessment)" (never "tap" in the trigger). Its pattern equals
  the baseline criterion, so the scorer cannot tell them apart; it becomes **required**, with a soft
  CSF-before-reassessment constraint, when the timing discriminator lands (decision Q2, CENTRAL)
- Labs where a case-specific mimic or safety question exists: M04 and S08 (thyroid), M07 (B12 and
  MMA on metformin), M08 (`{"panels": ["CBC", "coagulation"]}`, platelets 88 and INR 1.4, within
  the usual LP thresholds of platelets 50 x10^9/L or more and INR 1.5 or less)
- Spine MRI, `order_body_imaging {"study": "spine_MRI"}`: M04 (prior C5-C6 discectomy), P03 (CSM
  after fusion)
- P08 extended lumbar drainage, `analyze_csf {}` (trigger `repeat_csf_analysis`, about 10 mL/hour,
  300 to 500 mL over 72 hours; sensitivity 50% to 100%, PPV 80% to 100% [Marmarou_2005])
- P01 CSF AD biomarkers (`["Abeta42_40_ratio", "phospho_tau"]` or `["Abeta42", "phospho_tau"]`),
  follow-up repeating the full tap report

**Optional:** labs elsewhere (`interpret_labs {}`, targeted, `clinical_significance` null);
cognitive screen (`cognitive_screen`, case-authored MoCA with subscores so the library normal is
never served); lumbar spine MRI in M07 and M10; P09 AD biomarkers (normal) and neuropsychological
battery (subcortical-frontal profile, recognition preserved); P06 tamoxifen and duloxetine check
[CPIC_tamoxifen_2018].

**Management lives in the musts** (ruling 4): referral to neurosurgery for CSF shunting with a
programmable valve on the case's tap or drainage response, MRI and normal-pressure CSF
[Nakajima_2021] (the AAN grades shunting "possibly effective" for gait [Halperin_2015]);
copathology counselling (gait benefit expected more than cognition or parkinsonism; the coexisting
disease keeps its own treatment); falls prevention where falls are documented; comorbidity
actions. Anticoagulants: hold therapeutic apixaban or rivaroxaban at least 72 hours before the
tap (or document a residual drug level), restart no sooner than 24 hours after, no heparin bridging,
weighed against the CHA2DS2-VASc risk [ASRA_2025] [ACCP_2022]; continue low-dose aspirin and
NSAIDs [ASRA_2025]. Levodopa unchanged and the pre/post gait in the same medication state.

**Fallbacks:** CT shows the patient's own ventricles (Evans index about the MRI value) and lesions,
with no comparison wording; ECG and Holter consistent with the history (sinus rhythm in paroxysmal
AF); echo `echo_type` "TTE" and Holter `monitor_type` "holter_24h"; no literature, drug,
advanced-imaging or specialized-test fallback.

## 3. Tools that are typically USELESS (avoided as waste)

- `analyze_eeg`, `analyze_ecg`, `order_echocardiogram`, `order_cardiac_monitoring`: no role in the
  iNPH decision (each rationale case-specific)
- `order_ct_scan`: MRI is available in all 30 cases
- `order_advanced_imaging` (any modality): the iNPH decision rests on MRI and the tap test. Where a
  library normal would contradict the case (DaTscan in M05 and P02, amyloid PET in P01, FDG-PET in
  P01 and P04) a consistent case output is authored, still under the waste entry
- `order_specialized_test {"test_type": "neuropsych_battery"}`: the bedside screen and timed gait
  measures are enough (not in P09, where it is optional)
- Generic CSF assays Reviewer 1 removed: 14-3-3, RT-QuIC, oligoclonal bands, meningitis panel,
  HSV PCR (not P01, P06 or P09 for their own assays)

## 4. Tools that are HARMFUL / contraindicated

- `analyze_csf` before brain imaging (hard sequence constraint): a mass or obstructive hydrocephalus
  must be excluded before CSF is removed
- The lumbar tap while a therapeutic DOAC is active (a prohibition, not a tool criterion)

## 5. Sequence constraints and stop rule

Exactly two per case:
- MRI before CSF (`hard`): "Brain imaging must exclude a mass or obstructive hydrocephalus before CSF
  is removed [Relkin_2005]"
- baseline gait before CSF (`soft`): "The baseline gait must be measured before the tap, or the
  post-tap change cannot be interpreted [Nakajima_2021]"

No constraint names the post-tap or the P08 drainage criterion (their patterns equal the baseline
and the tap). Stop rule: `required_before_assessment` = MRI, baseline gait, CSF;
`max_additional_actions` 1.

## 6. Subtypes and difficulty

- **S (standard):** gait-predominant syndrome, supportive MRI, clear tap response
- **M (moderate):** missing DESH, mixed urinary causes (BPH), comorbid mimics (lumbar stenosis, CSM,
  B12 deficiency, hypothyroidism), anticoagulation, secondary NPH (M06, M08, M09)
- **P (puzzle):** copathology (AD P01, PD M05/P02, CSM P03, bvFTD P04, a prior PSP label P07),
  secondary NPH after SAH (P05), a cancer survivor with leptomeningeal disease to exclude (P06), a
  negative tap with a positive extended drainage (P08), cognitive-predominant iNPH with a prior AD
  label (P09)

## 7. Common red-herring categories

- **Ventriculomegaly alone**: atrophy ex vacuo, congenital or secondary causes; the diagnosis needs
  the clinical syndrome and supportive imaging (canonical prohibition in all 30)
- **A single negative tap**: does not exclude shunt response (P08)
- **Concurrent neurodegenerative disease**: does not preclude shunt benefit for gait
- **White matter change**: Fazekas-graded small-vessel disease is separated from transependymal
  signal; VCI is `moderate` only with Fazekas 2 or more or lacunes
- **Neuropathy from diabetes**: kept only where the exam documents distal sensory loss or reduced
  ankle reflexes

## 8. Allowed citations

- `[Relkin_2005]`: Relkin N, Marmarou A, Klinge P, Bergsneider M, Black PM. Diagnosing idiopathic
  normal-pressure hydrocephalus. Neurosurgery 2005;57(3 Suppl):S4-S16 (corrected 24 Oct 2026; the
  pack had S2-S4)
- `[Marmarou_2005]`: Marmarou A, Bergsneider M, Klinge P, Relkin N, Black PM. The value of
  supplemental prognostic tests for the preoperative assessment of idiopathic normal-pressure
  hydrocephalus. Neurosurgery 2005;57(3 Suppl):S17-S28 (corrected 24 Oct 2026; the pack had another
  title and S1-S52). Tap test, extended drainage and their sensitivity and PPV
- `[Nakajima_2021]`: Nakajima M, Yamada S, Miyajima M, et al. Guidelines for management of
  idiopathic normal pressure hydrocephalus (third edition): endorsed by the Japanese Society of
  Normal Pressure Hydrocephalus. Neurol Med Chir (Tokyo) 2021;61(2):63-97. doi:10.2176/nmc.st.2020-0292.
  Categories, DESH, callosal angle, CSF pressure 200 mmH2O or less, tap protocol (30 to 50 mL,
  reassessment at 2 to 4 and 24 hours), programmable valve (grade 1B), comorbidity. It sets no
  numeric tap-test cut-off
- `[Halperin_2015]`: Halperin JJ, Kurlan R, Schwalb JM, Cusimano MD, Gronseth G, Gloss D. Practice
  guideline: idiopathic normal pressure hydrocephalus: response to shunting and predictors of
  response. Neurology 2015;85(23):2063-2071
- `[Tisell_2011]`: Tisell M, Tullberg M, Hellström P, Edsbagge M, Högfeldt M, Wikkelsø C. Shunt
  surgery in patients with hydrocephalus and white matter changes. J Neurosurg 2011;114(5):1432-1438.
  Cited only for white matter change and shunt outcome (S09, S11), never for tap-test predictors
- `[Williams_2016]`: Williams MA, Malm J. Diagnosis and treatment of idiopathic normal pressure
  hydrocephalus. Continuum (Minneap Minn) 2016;22(2 Dementia):579-599
- `[Hakim_1965]`: Hakim S, Adams RD. The special clinical problem of symptomatic hydrocephalus with
  normal cerebrospinal fluid pressure. J Neurol Sci 1965;2(4):307-327 (historical; not cited in the
  cases)
- `[Massey_2013]`: Massey LA, Jäger HR, Paviour DC, et al. The midbrain to pons ratio: a simple and
  specific MRI sign of progressive supranuclear palsy. Neurology 2013;80(20):1856-1861 (P07)
- `[ASRA_2025]`: Kopp SL, Vandermeulen E, McBane RD, Perlas A, Leffert L, Horlocker T. Regional
  anesthesia in the patient receiving antithrombotic or thrombolytic therapy: American Society of
  Regional Anesthesia and Pain Medicine evidence-based guidelines (fifth edition). Reg Anesth Pain
  Med 2025, published online 29 January 2025. doi:10.1136/rapm-2024-105766 (PMID 39880411).
  Therapeutic apixaban and rivaroxaban: stop at least 72 hours before a neuraxial puncture (or check
  a level), first dose at least 24 hours after; aspirin and NSAIDs need no interruption
- `[ASRA_2018]`: **superseded** by `[ASRA_2025]` (Horlocker TT et al., fourth edition, Reg Anesth
  Pain Med 2018;43(3):263-309; it gave a 6-hour restart). No case cites it since 24 Oct 2026
- `[ACCP_2022]`: Douketis JD, Spyropoulos AC, Murad MH, et al. Perioperative management of
  antithrombotic therapy: an American College of Chest Physicians clinical practice guideline.
  Chest 2022;162(5):e207-e243. doi:10.1016/j.chest.2022.07.025. Suggests against heparin bridging
  during DOAC interruption
- `[CPIC_tamoxifen_2018]`: Goetz MP, Sangkuhl K, Guchelaar HJ, et al. Clinical Pharmacogenetics
  Implementation Consortium (CPIC) guideline for CYP2D6 and tamoxifen therapy. Clin Pharmacol Ther
  2018;103(5):770-777 (P06: avoid moderate or strong CYP2D6 inhibitors such as duloxetine with
  tamoxifen)
