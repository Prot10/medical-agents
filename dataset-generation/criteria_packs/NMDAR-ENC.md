# Criteria pack: Anti-NMDAR encephalitis

**ICD-10:** G04.81 (other encephalitis and encephalomyelitis; used for autoimmune encephalitis)
**Condition enum:** `NeurologicalCondition.AUTOIMMUNE_ENCEPHALITIS_NMDAR`
**Case ID prefix:** `NMDAR-ENC`

Revised 24 Oct 2026 (October 2026 review round close-out) from `data/review/round-2026-10/plans/NMDAR-ENC.md`
sections 1 to 3 and the July 2026 tool review (`condition_tool_guidance.yaml`, key
`autoimmune_encephalitis_nmdar`, Reviewer 2). No physician has reviewed the cases of this condition;
the facts below were checked against the cited sources.

**Which source governs.** Graus 2016 governs diagnosis. Acute treatment follows Titulaer 2013 and
Abboud 2021: no randomised trial exists, so musts say "observational evidence and expert consensus",
never "guideline-mandated". Aciclovir follows Venkatesan 2013 and Solomon 2012. Checkpoint-inhibitor
cases add ASCO 2021. Older patients' tumour search follows Titulaer_late_2013 and Graus 2021.

---

## 1. Diagnostic criteria (Graus 2016)

Six major groups: (1) abnormal behaviour (psychiatric) or cognitive dysfunction; (2) speech
dysfunction (pressured speech, verbal reduction, mutism); (3) seizures; (4) movement disorder,
dyskinesias, rigidity or abnormal postures; (5) decreased level of consciousness; (6) autonomic
dysfunction or central hypoventilation.

- **Probable anti-NMDAR encephalitis:** rapid onset (under 3 months) of at least four of the six
  groups, or three groups with a systemic teratoma, PLUS at least one laboratory finding: an abnormal
  EEG (focal or diffuse slow or disorganised activity, epileptic activity, or extreme delta brush) or
  CSF pleocytosis or oligoclonal bands; with reasonable exclusion of other disorders. MRI is NOT one
  of the probable criteria.
- **Definite anti-NMDAR encephalitis:** one or more of the six groups plus IgG anti-GluN1 antibodies,
  after reasonable exclusion of other disorders. Antibody testing should include CSF; a serum-only
  result needs confirmatory tests. Onset duration is not part of the definite criteria.
- **CSF versus serum:** all 250 patients of Gresa-Arribas 2014 had CSF antibodies, and about 14% were
  serum-negative (serum sensitivity 85.6%). Serum can also be falsely positive at low titre. The CSF
  cell-based assay is decisive; serum is read with the CSF, never alone.
- **MRI:** abnormal in about a third (Titulaer 2013), usually T2/FLAIR signal in medial temporal or
  cortical/subcortical regions, without restricted diffusion or haemorrhage. A normal MRI does not
  exclude the diagnosis; the MRI's role is to exclude alternatives (HSV encephalitis, structural
  lesions, demyelination).
- **EEG:** abnormal in most (diffuse or focal slowing, epileptiform activity, seizures). Extreme delta
  brush in 7 of 23 adults (30%) in Schmitt 2012: supportive, not pathognomonic; its absence excludes
  nothing. Never write "highly specific", "30-50%" or "pathognomonic".
- **CSF routine:** lymphocytic pleocytosis, mildly raised protein and/or OCB in most; a normal CSF does
  not exclude the disease. Glucose is normal: a CSF/serum glucose ratio below about 0.5 is not a
  feature and points to another process.
- **Tumours:** 38% of 577 patients had a tumour, nearly all ovarian teratomas, peaking in women of
  reproductive age (Titulaer 2013); rare in men and children under 12. At 45 or older, 7 of 31
  patients (23%) had a tumour, one a teratoma and six carcinomas (breast, lung, thymic, ovarian), and
  45% were men (Titulaer_late_2013). Post-HSV anti-NMDAR encephalitis is not tumour-associated
  (Armangue 2018).
- **Prodrome:** a viral-like prodrome precedes the illness in about 70% (Dalmau 2011).
- **Antibody titres:** end-point dilutions of one doubling series per specimen (serum usually from
  1:10, CSF from 1:2 or undiluted). A value outside any series (e.g. "1:56") is an error.

## 2. Standard workup hierarchy (minimal `required_arguments`)

Criteria in this order (the review app reads list order as the work-up sequence):

**Required (all five are the stop rule; `max_additional_actions: 2`):**
1. `interpret_labs`: A `panels: [CBC, CMP, TSH, anti_TPO, HIV, NMDAR_IgG_cell_based]`, B the same with
   `thyroid` instead of `TSH`. Women 12-50 add `beta-hCG` (not a postmenopausal woman). Patients 45 or
   older add `paraneoplastic_panel` and `autoimmune_encephalitis_panel`. MRI showing demyelination or
   optic neuritis adds `MOG_IgG_cell_based` and `AQP4_IgG_cell_based`. The report carries the serum
   anti-GluN1 result in one panel `Serum anti-GluN1 IgG (cell-based assay)` and never a CSF result
   [Graus_2016] [Gresa-Arribas_2014]
2. `analyze_brain_mri` `{contrast: true}` (no `protocol`): excludes HSV encephalitis, structural
   lesions and overlapping demyelination before LP; normal in about two thirds [Titulaer_2013]
3. `analyze_csf`: A `special_tests: [HSV_PCR, NMDAR_antibodies, oligoclonal_bands]`, B
   `[HSV_PCR, NMDAR_antibodies, IgG_index]` (cells, protein and glucose come with every CSF order; no
   `basic` key). A CJD mimic adds `RT_QuIC` to both. The CSF report carries the final titre in one
   `NMDAR_antibodies` key, never "pending" [Graus_2016] [Gresa-Arribas_2014] [Venkatesan_2013]
4. `analyze_eeg` `{eeg_type: routine}`, `{eeg_type: video}` or `{eeg_type: continuous_icu}` (a first
   cEEG satisfies the baseline) [Schmitt_2012]
5. `order_body_imaging` tumour screen, by demography (July 2026 review: required, tailored, never
   blanket CAP CT): women 12-44 `{study: pelvis_abdomen_ultrasound}`; men under 45
   `{study: testicular_ultrasound}`; anyone 45 or older `{study: chest_abdomen_pelvis_CT, contrast: true}`
   [Dalmau_2011] [Titulaer_late_2013]

**Recommended:**
- `analyze_eeg` `{eeg_type: continuous_icu}` (cEEG escalation) when consciousness fluctuates or
  seizures, behavioural arrests or rhythmic activity are present; every case stores a cEEG follow-up
  consistent with its routine EEG, so the library never answers it with a normal report [Herman_2015]
- Case-specific diagnostic extras: pelvic MRI `{study: pelvis_abdomen_MRI}` for an equivocal adnexal
  lesion; germ-cell tumour markers (AFP, beta-hCG, LDH) and staging CAP CT for a testicular mass
  [EAU_Testicular_2024]; SIADH work-up `{panels: [serum_osmolality, urine_osmolality]}` when sodium is
  below 130 mmol/L [Spasovski_2014]
- `check_drug_interactions` `{}` where an antipsychotic, SSRI or thiazide (hyponatraemia), or prior
  valproate is on board

**Required only with a concrete interaction (ruling 6):** `check_drug_interactions` `{}` (e.g.
lamotrigine with valproate as the seizure option; CKD with aciclovir and levetiracetam; checkpoint
inhibitor). Otherwise optional.

**Optional:** `search_medical_literature` `{}` (never required or recommended; its output is general,
correctly cited evidence and its follow-up goes last).

Management is never a tool call: specialist input (neurology with psychiatry; gynaecology, urology or
oncology for a found tumour), first-line immunotherapy, aciclovir, antiseizure therapy and level of
care are musts (see section 9).

## 3. Tools that are typically USELESS (waste)

- `order_echocardiogram`, `order_specialized_test` EMG/NCS (unless flaccid weakness or areflexia),
  `order_advanced_imaging` amyloid PET and DaTscan.
- `order_advanced_imaging` FDG-PET: not a case criterion (July 2026 review removed it); no case
  stores a catch-all advanced-imaging or specialised-test fallback.
- `order_microbiology` blood cultures: removed in the July 2026 review; not indicated without sepsis.
- `analyze_ecg` and `order_cardiac_monitoring`: no criterion; every case stores an initial ECG at the
  vitals heart rate and telemetry matching the examination; cardiac monitoring is part of the level-of-
  care must.

## 4. Tools that are HARMFUL / contraindicated

- LP without prior imaging in a patient with seizures or altered consciousness: covered by the
  prohibition P4 and the soft sequence constraint, not by a harm avoided action.
- Haloperidol and other high-potency D2 antagonists: a prohibition (P1), not a tool [Lejuste_2016].

## 5. Sequence constraints

- `analyze_brain_mri` before `analyze_csf` (`soft`) in every case: imaging before LP in a patient with
  seizures or altered consciousness; a CT head is an acceptable alternative, so it is soft. No hard
  constraint (even a case with a known extra-axial lesion had a CT head in the ED).
- Immunotherapy is not delayed for the antibody result once infection is reasonably excluded: a must
  and the prohibition P2, not a sequence constraint.

## 6. Subtype variations

- **M (mild):** partial syndrome, mostly psychiatric and cognitive, ward care.
- **S (standard):** classic multistage syndrome (prodrome, psychiatric, seizures/dyskinesias,
  dysautonomia).
- **P (progressive / severe):** dysautonomia, central hypoventilation, catatonia or coma; ICU by the
  level-of-care rule; consider early escalation.
- **R (reverse / atypical):** atypical host or trigger (post-HSV, post-COVID, checkpoint inhibitor,
  age 45 or older, MOG/AQP4 overlap, optic neuritis). Mimics each case raises go in its differential:
  HSV encephalitis or relapse, other neuronal-surface antibody encephalitis (LGI1, CASPR2, GABA-B,
  AMPA), SREAT/Hashimoto encephalopathy, ADEM/MOGAD/NMOSD, CJD (RT-QuIC), leptomeningeal disease,
  checkpoint-inhibitor encephalitis, primary psychiatric disorder or bipolar relapse, NMS and drug-
  induced hyponatraemia, valproate encephalopathy, NPSLE, Wernicke encephalopathy.

## 7. Common red-herring categories

- **Psychiatric presentation**: P3, "do not attribute the presentation to a primary psychiatric
  disorder while seizures, dyskinesias, autonomic instability, an abnormal EEG or CSF inflammation
  remain unexplained" (no "young" wording: older patients exist).
- **Negative serum antibodies**: do not exclude; about 14% are serum-negative (Gresa-Arribas 2014).
- **Normal initial MRI**: about two thirds.
- **Hyponatraemia**: occurs, but is far more typical of anti-LGI1 encephalitis; graded mild 130-134,
  moderate 125-129, profound below 125 mmol/L (Spasovski 2014); needs its own work-up.
- **Viral-like prodrome**: about 70% (Dalmau 2011); does not establish viral encephalitis, which CSF
  PCR addresses.
- **Improvement with an antipsychotic**: does not exclude the disease.
- **Post-HSV relapse of symptoms**: autoimmune encephalitis developed in 14 of 51 patients (27%) after
  HSV encephalitis, 9 of them (64%) with NMDAR antibodies, 7 to 61 days after HSV encephalitis
  (Armangue 2018); a negative CSF HSV PCR excludes HSV relapse. (The earlier "5-10% of HSV cases" was
  wrong.)
- **Raised CK**: from seizures and dyskinesias; NMS needs antipsychotic exposure, rigidity,
  hyperthermia and markedly raised CK.

## 8. Allowed citations

All verified 24 Oct 2026.

- `[Graus_2016]`: Graus F, Titulaer MJ, Balu R, et al. A clinical approach to diagnosis of autoimmune encephalitis. Lancet Neurol 2016;15(4):391-404
- `[Titulaer_2013]`: Titulaer MJ, McCracken L, Gabilondo I, et al. Treatment and prognostic factors for long-term outcome in patients with anti-NMDA receptor encephalitis: an observational cohort study. Lancet Neurol 2013;12(2):157-165
- `[Titulaer_late_2013]`: Titulaer MJ, McCracken L, Gabilondo I, et al. Late-onset anti-NMDA receptor encephalitis. Neurology 2013;81(12):1058-1063 (patients 45 or older: tumours 23%, mostly carcinomas)
- `[Dalmau_2011]`: Dalmau J, Lancaster E, Martinez-Hernandez E, Rosenfeld MR, Balice-Gordon R. Clinical experience and laboratory investigations in patients with anti-NMDAR encephalitis. Lancet Neurol 2011;10(1):63-74
- `[Dalmau_2018]`: Dalmau J, Graus F. Antibody-mediated encephalitis. N Engl J Med 2018;378(9):840-851
- `[Dalmau_2019]`: Dalmau J, Armangué T, Planagumà J, et al. An update on anti-NMDA receptor encephalitis for neurologists and psychiatrists: mechanisms and models. Lancet Neurol 2019;18(11):1045-1057
- `[Gresa-Arribas_2014]`: Gresa-Arribas N, Titulaer MJ, Torrents A, et al. Antibody titres at diagnosis and during follow-up of anti-NMDA receptor encephalitis: a retrospective study. Lancet Neurol 2014;13(2):167-177
- `[Schmitt_2012]`: Schmitt SE, Pargeon K, Frechette ES, Hirsch LJ, Dalmau J, Friedman D. Extreme delta brush: a unique EEG pattern in adults with anti-NMDA receptor encephalitis. Neurology 2012;79(11):1094-1100
- `[Abboud_2021]`: Abboud H, Probasco JC, Irani S, et al. Autoimmune encephalitis: proposed best practice recommendations for diagnosis and acute management. J Neurol Neurosurg Psychiatry 2021;92(7):757-768
- `[Lejuste_2016]`: Lejuste F, Thomas L, Picard G, et al. Neuroleptic intolerance in patients with anti-NMDAR encephalitis. Neurol Neuroimmunol Neuroinflamm 2016;3(5):e280
- `[Armangue_2018]`: Armangue T, Spatola M, Vlagea A, et al. Frequency, symptoms, risk factors, and outcomes of autoimmune encephalitis after herpes simplex encephalitis: a prospective observational study and retrospective analysis. Lancet Neurol 2018;17(9):760-772
- `[Venkatesan_2013]`: Venkatesan A, Tunkel AR, Bloch KC, et al. Case definitions, diagnostic algorithms, and priorities in encephalitis: consensus statement of the International Encephalitis Consortium. Clin Infect Dis 2013;57(8):1114-1128
- `[Solomon_2012]`: Solomon T, Michael BD, Smith PE, et al. Management of suspected viral encephalitis in adults: Association of British Neurologists and British Infection Association national guidelines. J Infect 2012;64(4):347-373
- `[Herman_2015]`: Herman ST, Abend NS, Bleck TP, et al. Consensus statement on continuous EEG in critically ill adults and children, part I: indications. J Clin Neurophysiol 2015;32(2):87-95
- `[Spasovski_2014]`: Spasovski G, Vanholder R, Allolio B, et al. Clinical practice guideline on diagnosis and treatment of hyponatraemia. Eur J Endocrinol 2014;170(3):G1-G47
- `[ASCO_irAE_2021]`: Schneider BJ, Naidoo J, Santomasso BD, et al. Management of immune-related adverse events in patients treated with immune checkpoint inhibitor therapy: ASCO guideline update. J Clin Oncol 2021;39(36):4073-4126 (RP02)
- `[Graus_2021]`: Graus F, Vogrig A, Muñiz-Castrillo S, et al. Updated diagnostic criteria for paraneoplastic neurologic syndromes. Neurol Neuroimmunol Neuroinflamm 2021;8(4):e1014
- `[EAU_Testicular_2024]`: EAU Guidelines on Testicular Cancer, 2024 edition. Arnhem: EAU Guidelines Office; 2024 (limited update of the 2023 text, summarised in Patrikidou A et al., Eur Urol 2023;84(3):289-301). Cited only in P02 for pre-orchiectomy tumour markers (AFP, beta-hCG, LDH) and contrast CT staging, which later editions keep
- `[Lancaster_2016]`: Lancaster E. The diagnosis and treatment of autoimmune encephalitis. J Clin Neurol 2016;12(1):1-13

## 9. Canonical musts and prohibitions (plan section C9)

Musts (keep those that apply, with case cautions): M1 IV aciclovir 10 mg/kg every 8 h, renally
adjusted (12-hourly at CrCl 25-50, 24-hourly at 10-25 mL/min), stopped once CSF HSV PCR is negative and
the antibody diagnosis is established, PCR repeated on a second sample if the first LP was within 72 h
of onset and HSV remains plausible (post-HSV: restart until relapse is excluded); M2 first-line
immunotherapy without waiting for the antibody result once infection is reasonably excluded (IV
methylprednisolone 1 g daily for 5 days with IVIG 0.4 g/kg/day for 5 days or plasma exchange 5 to 7
exchanges); M3 tumour (teratoma removal, ovary-sparing where feasible, as part of first-line
treatment; surveillance after a negative screen; orchiectomy for a testicular mass); M4 seizures
(levetiracetam, renally adjusted, or lacosamide; avoid valproate in a woman able to become pregnant;
with lamotrigine, avoid valproate or halve the lamotrigine dose); M5 cEEG where the criterion exists;
M6 level of care (ICU for GCS 12 or less, central hypoventilation, HR above 130 or labile BP with
diaphoresis, status epilepticus, catatonia with refusal of food and fluids; otherwise neurology ward
with seizure precautions and cardiac monitoring); M7 escalation to rituximab (after hepatitis B
screening) and/or cyclophosphamide if no meaningful improvement 10 to 14 days after first-line
therapy, discussing fertility; M8 benzodiazepines first for agitation and catatonia, stopping any
antipsychotic; M9 hyponatraemia below 130 as SIADH after review of thiazide or SSRI, correcting by no
more than 10 mmol/L in 24 h; M10 neurology-led care with psychiatry and the tumour's specialty.

Prohibitions in every case: P1 no haloperidol or other high-potency D2 antagonists; P2 do not delay
immunotherapy for the antibody result; P3 do not attribute the presentation to a primary psychiatric
disorder while organic features are unexplained; P4 no LP without imaging in a patient with seizures
or altered consciousness; P5 a negative serum antibody does not exclude the disease.
