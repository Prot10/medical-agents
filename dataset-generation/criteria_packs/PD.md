# Criteria pack: Parkinson's disease

**ICD-10-CM:** G20.A1 (Parkinson's disease without dyskinesia, without mention of fluctuations;
also PD NOS), G20.A2 (without dyskinesia, with fluctuations), G20.B1 (with dyskinesia, without
mention of fluctuations), G20.B2 (with dyskinesia, with fluctuations). G20.C is "Parkinsonism,
unspecified" and is not a PD code. Mimic cases kept in this condition: MSA G90.3, DLB G31.83, PSP
G23.1 (section 7).
**Condition enum:** `NeurologicalCondition.PARKINSONS` (`parkinsons`)
**Case ID prefix:** `PD`

Updated 24 Oct 2026 to the October 2026 review round (`data/review/round-2026-10/plans/PD.md`,
`PD-summary.md`) and its close-out (`plans/PD-decisions.md`). Every statement below is taken from
the plan's canonical facts F1 to F9 and its section 3, and every count is measured on the 30 cases
after the round.

---

## 1. Diagnostic criteria (MDS 2015, [Postuma_2015])

1.1 **Entry criterion:** parkinsonism, i.e. bradykinesia with rest tremor or rigidity, or both.

1.2 **Clinically established PD:** no absolute exclusion, at least two supportive criteria, no red
flag.

1.3 **Clinically probable PD:** no absolute exclusion; red flags only if counterbalanced by
supportive criteria (one red flag needs one supportive criterion, two need two); never more than
two red flags. With no red flag, probable PD needs no supportive criterion.

1.4 **Supportive criteria (only these four):**
- a clear and dramatic beneficial response to dopaminergic therapy;
- levodopa-induced dyskinesia;
- rest tremor of a limb on examination;
- olfactory loss on a validated test for age and sex (UPSIT, Sniffin' Sticks), or cardiac
  sympathetic denervation on MIBG scintigraphy.

Not supportive: RBD (a prodromal marker, [Berg_2015]), constipation, self-reported or bedside
smell loss, a family history, an SWI nigrosome sign, an abnormal DaTscan.

1.5 **Red flags used in this condition:** rapid gait progression needing a wheelchair within 5
years; recurrent falls (more than one a year) because of impaired balance within 3 years of onset;
severe autonomic failure within 5 years (orthostatic fall within 3 minutes of at least 30 mmHg
systolic or 15 mmHg diastolic, or severe urinary incontinence or retention); inspiratory stridor;
bilateral symmetric parkinsonism; disproportionate anterocollis; early bulbar dysfunction; no
progression over 5 years; unexplained pyramidal signs.

1.6 **Absolute exclusions used here:** cerebellar abnormalities; downward vertical supranuclear
gaze palsy; probable bvFTD or PPA within 5 years; parkinsonism restricted to the legs for more than
3 years; dopamine-blocker exposure in a dose and time course consistent with drug-induced
parkinsonism; no response to high-dose levodopa (at least 600 mg/day) despite at least moderate
severity; normal presynaptic dopaminergic imaging; a documented alternative condition.

1.7 **Consequence for first visits.** A patient who has never taken levodopa has at most one
supportive criterion (rest tremor) unless the case contains a validated smell test or an MIBG, so
the label is **clinically probable PD**, never "established". "Clinically established" is used only
in PD-M04 (rest tremor and UPSIT microsmia), PD-RM05 (documented response and rest tremor) and
PD-RP04 (dramatic response, dyskinesia, rest tremor).

1.8 **Current D2-blocker exposure (PD-M01, M02, M03).** While metoclopramide is taken the exposure is
an absolute exclusion, so the MDS criteria cannot yet be met. The label "PD unmasked by
metoclopramide" rests on the abnormal DaTscan (pure drug-induced parkinsonism has normal
presynaptic imaging, [Marshall_2009]) and on non-motor features a D2 blocker does not cause (RBD,
hyposmia, only where the history reports them); it is confirmed when the parkinsonism persists
after withdrawal.

1.9 **Drug-induced parkinsonism and DaTscan.** Metoclopramide and prochlorperazine are central D2
antagonists; valproate and lithium cause parkinsonism by other mechanisms. In pure drug-induced
parkinsonism the DaTscan is normal and the signs resolve over weeks to months after withdrawal. DaT
ligands are not displaced by D2 antagonists. DaTscan does not separate PD from MSA, PSP or DLB.

## 2. Work-up hierarchy (Reviewer 1, July 2026; plan section 3)

Tiers as applied in the 30 cases. The diagnosis of PD is clinical; tests exclude mimics or answer
a case-specific question.

**Required**
- `analyze_brain_mri {}` in 29 cases (S06: `order_ct_scan {}`, severe claustrophobia, with its
  panel exemption). MRI is normal in PD; it excludes vascular lesions, NPH, mass and the midbrain,
  pontine and putaminal signs of PSP and MSA [Postuma_2015]. A standard parkinsonism MRI is
  non-contrast; no criterion fixes `contrast` or `protocol`. An SWI nigrosome finding is cited
  [Schwarz_2014] only where the report gives it. Evans index above 0.30 is abnormal.
- `order_advanced_imaging {"modality": "DaTscan"}` only where the label rests on it: M01, M02, M03
  (PD unmasked by metoclopramide) and RM02 (PD despite valproate).
- `interpret_labs` only in P04 (Wilson screen in young-onset parkinsonism: ceruloplasmin, serum
  and 24-hour urinary copper, with slit-lamp examination for Kayser-Fleischer rings
  [EASL_ERN_Wilson_2025]).
- `check_drug_interactions {}` only where a dopamine-blocking drug is on the list or the referral
  asks for the review: M01, M02, M03 (metoclopramide), RM05 (prochlorperazine), RP04 (pre-DBS:
  iron with levodopa, rasagiline before surgery).
- `order_specialized_test {"test_type": "neuropsych_battery"}` only in RP04 (pre-DBS candidacy).

**Recommended**
- DaTscan in RP05 (vascular versus degenerative parkinsonism with Fazekas 2 white matter disease).
- Labs: RM02 (valproate level, ammonia), RM05 (TSH, free T4 on levothyroxine), RS01 (lithium
  level).
- Medication review in P01, RP01, RP02, RP03 (drugs that worsen neurogenic orthostatic
  hypotension), P02 (rivastigmine with midodrine and syncope), RM02 (valproate), RS01 (lithium with
  lisinopril).
- `order_advanced_imaging {"modality": "MIBG_scan"}` in RP02 (reduced uptake is the second
  supportive criterion that makes probable PD).
- `order_specialized_test {"test_type": "polysomnography"}` in M05 (violent dream enactment with
  obstructive sleep apnoea as an RBD mimic).
- `analyze_ecg {}` and `order_cardiac_monitoring {"monitor_type": "holter_24h"}` in RP01 only
  (syncope with known WPW: a 12-lead ECG in every syncope, [ESC_2018]); a departure from Reviewer
  1's removal of the ECG, shown to the reviewer.

**Optional**
- DaTscan in M04, RM03 (prior essential tremor; the clinical picture is clear, so NICE NG71 gives
  no indication), P02, P04, RM05, RS01, S05, S06.
- Labs in M04, RS05 (TSH), RP04 (iron studies), RS03, RS04 (B12, copper after bariatric surgery).
- Polysomnography in 14 cases where dream enactment is reported and not PSG-confirmed (M01, M02,
  M04, P02, P04, RM02, RM03, RM04, RP02, RP03, RP04, RP05, RS01, S03).
- Neuropsychological battery in 10 cases where cognition is clinically relevant (P02, P03, RM02,
  RM04, RM05, RP01, RP02, RP03, RS03, RS04). Where the exam MoCA is below 28 the case stores a
  battery consistent with it, with or without a criterion.
- `order_specialized_test {"test_type": "genetic_panel:PD"}` in P04 (onset at 42) and RM05
  (first-degree relative), after counselling.
- MIBG in P01, P02, RP01, RP03; FDG-PET in P02; echocardiogram in RP01.
- `perform_clinical_assessment {"assessment_type": "orthostatic_blood_pressure"}` in M01, RM04 and
  RP04 (orthostatic light-headedness with no lying and standing figures in the exam).
- Medication review in the other 18 cases.

**Never a criterion:** literature search (deleted in all 30, ruling 5), EEG, CSF, EMG/NCS,
repetitive nerve stimulation, biopsies, evoked potentials, formal autonomic testing, tilt-table
testing (Reviewer 1). Specialist referral, levodopa start and other management are musts, not
tool calls (ruling 4).

**Facts the musts use**
- Levodopa start: carbidopa-levodopa 25/100 mg, half a tablet three times daily with food,
  increasing over 2 to 4 weeks to one tablet three times daily (300 mg/day), reviewed after 2 to 3
  months [NICE_NG71]. Immediate-release tablets are 10/100, 25/100 and 25/250; there is no 25/200
  immediate-release tablet. Daily levodopa is milligrams per dose times doses.
- Dopamine agonists: warn about impulse control disorders and excessive daytime sleepiness and ask
  at every visit [NICE_NG71].
- Iron salts chelate levodopa: at least 2 hours apart.
- MAO-B inhibitors (rasagiline label): meperidine, tramadol, methadone, dextromethorphan, St John's
  wort, cyclobenzaprine and other MAO inhibitors are contraindicated; sympathomimetic amines are
  avoided. With an SSRI serotonin syndrome is rare; fluoxetine and fluvoxamine are best avoided
  with rasagiline (at least 5 weeks after stopping fluoxetine). "Sertraline plus levodopa causes
  serotonin syndrome" is false.
- If an antipsychotic is needed, quetiapine or clozapine; never haloperidol, metoclopramide,
  prochlorperazine or another central D2 blocker.

## 3. Tools that are waste in this condition (`avoided_actions`, severity `waste`)

- DaTscan in the 17 cases with a clear clinical diagnosis (M05, P01, P03, RM01, RM04, RP01, RP02,
  RP03, RP04, RS02 to RS05, S01 to S04): "DaT SPECT is indicated when tremor cannot be clinically
  separated from parkinsonism; here the clinical diagnosis is clear" [NICE_NG71]; in P01, P03,
  RP01, RP02 and RP03 "a DaTscan does not separate PD from MSA or PSP" [Marshall_2009]. Every case
  still stores an abnormal DaTscan (the library default is normal, an absolute exclusion).
- `order_specialized_test` autonomic testing and tilt table: all 30 (bedside orthostatic
  measurement suffices, or already documents the neurogenic orthostatic hypotension in P01, RP01,
  RP02, RP03).
- CSF all 30; echocardiogram 29 (not RP01); cardiac monitoring 27 (not RP01, RP02, RP03); EEG 28
  (not P02 and P03: in the DLB case posterior slowing is a supportive biomarker); ECG 18; amyloid PET 6 (M04, M05, RM04, RP04, RP05, S06); FDG-PET 3
  (M04, RM04, RP04).

## 4. Harmful or contraindicated

No avoided action is `harm` or `contraindicated`. Prohibited recommendations (all cases): do not
prescribe metoclopramide, prochlorperazine, haloperidol or other centrally acting D2-blocking
antiemetics or antipsychotics. P02 adds the severe neuroleptic sensitivity of DLB [DLB_2017].
M01 to M03: do not start levodopa while metoclopramide remains in the regimen.

## 5. Sequence constraints

Only one, `soft`, in the 13 cases with a DaTscan criterion: brain MRI (or CT) before DaTscan,
"Exclude structural and vascular causes on MRI before interpreting a DaTscan" [Postuma_2015]. No
other constraint (the old "labs before drug check" constraints were removed). Stop rule:
`required_before_assessment` is the required set; `max_additional_actions` 2.

## 6. Report rules

- DaTscan reports are binary statements of the finding with binding ratios, no disease name, no
  "rather than", no "confirms". PD and DLB: asymmetric posterior putaminal reduction contralateral
  to the clinically worse side, relative caudate sparing. MSA and PSP: bilateral, relatively
  symmetric reduction in putamen and caudate.
- MIBG: "Reduced (or normal) cardiac MIBG uptake (early H/M, delayed H/M, washout)"; reduced in PD
  and DLB, usually normal in MSA and PSP. No "Lewy-body" wording.
- PSG impression: REM sleep without atonia percentage, video behaviours, AHI, PLMI; no diagnosis
  name. Neuropsychological impression: impaired and preserved domains, profile, mood scale. Flags
  follow the reference range in the right direction (no "Abnormal values" builder).
- MoCA losses are itemised within the item maxima (trail-making 1, cube 1, clock 3, naming 3,
  attention 6 with serial subtraction 3, repetition 2, fluency 1, abstraction 2, delayed recall 5,
  orientation 6).
- A CSF fallback glucose is in proportion to the serum glucose the case stores.
- Orthostatic figures: every orthostatic complaint has measured lying and standing pressures,
  either in the exam or in a stored `orthostatic_blood_pressure` report.

## 7. Mimic cases kept in this condition (ruling 3: case_id and condition never change)

| case | label | primary code | scored against |
| --- | --- | --- | --- |
| PD-P01 | MSA, parkinsonian type (clinically probable) | G90.3 (also accepted G23.2) | [Wenning_2022] |
| PD-RP03 | MSA, mixed parkinsonian and cerebellar features (clinically established) | G90.3 (also accepted G23.2, G23.3) | [Wenning_2022] |
| PD-P02 | DLB (probable) | G31.83 | [DLB_2017] |
| PD-P03 | PSP, Richardson syndrome (probable) | G23.1 | [Hoglinger_2017] |

Their accepted labels and codes name their own disease; no PD label or G20 code is accepted in
them, and no MSA, DLB or PSP label or code is accepted in the 26 PD cases
(`diagnosis_synonyms.yaml`, 24 Oct 2026). MSA code: ICD-10-CM FY2026 codes MSA to G90.3; WHO
ICD-10 (2016 update onward) and ICD-10-GM use G23.2 (MSA-P) and G23.3 (MSA-C); in ICD-10-CM G23.2
is striatonigral degeneration and G23.3 does not exist.

- **MSA (MDS 2022).** Autonomic dysfunction = orthostatic fall of at least 20/10 mmHg within 3
  minutes, urinary urge incontinence, or a post-void residual of at least 100 mL. Clinically
  established MSA: autonomic dysfunction, poorly levodopa-responsive parkinsonism or a cerebellar
  syndrome, at least two supportive features and at least one MRI marker. Clinically probable MSA:
  at least two of autonomic dysfunction, parkinsonism and a cerebellar syndrome, plus one
  supportive feature. Poor levodopa response: by history, or less than 30% improvement on
  MDS-UPDRS III, on up to 1000 mg/day for at least 1 month; no trial means it cannot be stated
  (P01). MRI markers: putaminal atrophy with signal decrease on iron-sensitive sequences, middle
  cerebellar peduncle or pontine atrophy, hot cross bun sign. MIBG and olfaction usually
  preserved. Stridor is a supportive feature and needs urgent laryngoscopy.
- **DLB (McKeith 2017).** Dementia is essential. Core: fluctuating cognition, recurrent visual
  hallucinations, RBD, parkinsonism. Indicative biomarkers: reduced DaT uptake, low MIBG uptake,
  PSG-confirmed REM sleep without atonia. Supportive biomarkers: preserved medial temporal lobes,
  occipital hypometabolism with the cingulate island sign, posterior slow-wave EEG. Probable DLB:
  two core features, or one core feature with an indicative biomarker. Dementia before or within
  a year of parkinsonism separates DLB from PD dementia.
- **PSP (MDS 2017).** Probable PSP-RS: O1 (vertical supranuclear gaze palsy) or O2 (slow vertical
  saccades) with P1 (repeated unprovoked falls within 3 years) or P2 (tendency to fall on the pull
  test within 3 years). Midbrain atrophy is supportive, not required.

## 8. Subtype variations

- **S (standard):** first visit, asymmetric parkinsonism with rest tremor, clinically probable PD;
  MRI required, everything else optional or waste.
- **M (moderate):** a confounder: dopamine-blocker exposure (M01 to M03, DaTscan required),
  prior essential tremor (M04, RM03), dream enactment with OSA (M05).
- **P (puzzle):** the PD mimics of section 7 and young-onset PD with a Wilson screen (P04).
- **RS, RM, RP (real-case seeded):** PD with lithium, a VP shunt, bariatric surgery or topiramate
  (RS); undertreated or fluctuating PD, valproate, prochlorperazine, misattributed shoulder pain
  (RM); orthostatic syncope blamed on WPW (RP01), early autonomic failure resolved by MIBG (RP02),
  MSA (RP03), pre-DBS assessment (RP04), vascular risk (RP05).

A PD-labelled case must meet clinically probable PD in its data: asymmetric onset with a rest tremor
on examination, a normal-for-age MRI, at most the red flags its supportive criteria counterbalance
(RP01 and RP02 were fixed this way). Atypical MRI markers and a "poor levodopa response" belong
only in an MSA or PSP case, the latter only after a documented trial.

## 9. Common red herrings

- Symmetric onset, early falls or orthostatic symptoms: red flags to be counted, not a diagnosis.
- Antiemetic exposure (metoclopramide, prochlorperazine): DaTscan separates unmasked PD from pure
  drug-induced parkinsonism.
- A prior essential-tremor label or a family history of tremor (ET can coexist with PD).
- Self-reported smell loss (not a supportive criterion) and post-viral anosmia.
- Musculoskeletal attributions of rigidity (adhesive capsulitis, cervical spondylosis).
- A red herring must be a datum in the patient block; no copied red herrings.

## 10. Allowed citations

Every key cited in the 30 cases is listed (checked 24 Oct 2026).

- `[Postuma_2015]` Postuma RB, Berg D, Stern M, et al. MDS clinical diagnostic criteria for
  Parkinson's disease. Mov Disord 2015;30(12):1591-1601. doi:10.1002/mds.26424
- `[Berg_2015]` Berg D, Postuma RB, Adler CH, et al. MDS research criteria for prodromal
  Parkinson's disease. Mov Disord 2015;30(12):1600-1611. doi:10.1002/mds.26431
- `[Marshall_2009]` Marshall VL, Reininger CB, Marquardt M, et al. Parkinson's disease is
  overdiagnosed clinically at baseline in diagnostically uncertain cases: a 3-year European
  multicenter study with repeat [123I]FP-CIT SPECT. Mov Disord 2009;24(4):500-508.
  doi:10.1002/mds.22108
- `[Schwarz_2014]` Schwarz ST, Afzal M, Morgan PS, et al. The 'swallow tail' appearance of the
  healthy nigrosome: a new accurate test of Parkinson's disease: a case-control and retrospective
  cross-sectional MRI study at 3T. PLoS One 2014;9(4):e93814. doi:10.1371/journal.pone.0093814
- `[Tolosa_2021]` Tolosa E, Garrido A, Scholz SW, Poewe W. Challenges in the diagnosis of
  Parkinson's disease. Lancet Neurol 2021;20(5):385-397. doi:10.1016/S1474-4422(21)00030-2
- `[NICE_NG71]` National Institute for Health and Care Excellence. Parkinson's disease in adults.
  NICE guideline NG71, July 2017.
- `[Wenning_2022]` Wenning GK, Stankovic I, Vignatelli L, et al. The Movement Disorder Society
  criteria for the diagnosis of multiple system atrophy. Mov Disord 2022;37(6):1131-1148.
  doi:10.1002/mds.29005
- `[DLB_2017]` McKeith IG, Boeve BF, Dickson DW, et al. Diagnosis and management of dementia with
  Lewy bodies: fourth consensus report of the DLB Consortium. Neurology 2017;89(1):88-100.
  doi:10.1212/WNL.0000000000004058
- `[Hoglinger_2017]` Höglinger GU, Respondek G, Stamelou M, et al. Clinical diagnosis of
  progressive supranuclear palsy: the Movement Disorder Society criteria. Mov Disord
  2017;32(6):853-864. doi:10.1002/mds.26987
- `[Litvan_2012]` Litvan I, Goldman JG, Tröster AI, et al. Diagnostic criteria for mild cognitive
  impairment in Parkinson's disease: Movement Disorder Society Task Force guidelines. Mov Disord
  2012;27(3):349-356. doi:10.1002/mds.24893
- `[ESC_2018]` Brignole M, Moya A, de Lange FJ, et al. 2018 ESC Guidelines for the diagnosis and
  management of syncope. Eur Heart J 2018;39(21):1883-1948. doi:10.1093/eurheartj/ehy037
- `[EASL_ERN_Wilson_2025]` European Association for the Study of the Liver, European Reference
  Network on Hepatological Diseases (Socha P, et al.). EASL-ERN Clinical Practice Guidelines on
  Wilson's disease. J Hepatol 2025;82(4):690-728. doi:10.1016/j.jhep.2024.11.007

Superseded or retired (never cite):
- `[EASL_Wilson_2012]` EASL Clinical Practice Guidelines: Wilson's disease. J Hepatol
  2012;56(3):671-685. Superseded by `[EASL_ERN_Wilson_2025]` (PD-P04 recited 24 Oct 2026).
- `[Gilman_2008]` Gilman S, et al. Second consensus statement on the diagnosis of multiple system
  atrophy. Neurology 2008;71:670-676. Superseded by `[Wenning_2022]`.
- `[McKeith_2017_DLB]` alias of `[DLB_2017]`; no PD case uses it.
- `[Postuma_2019]` removed: cited by no case and its listed locator could not be verified.
