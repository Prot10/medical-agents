# Library contradictions, group 3: decisions (25 Oct 2026)

Conditions BACT-MEN, GBS, MG, NPH, SYNC-CARD (150 cases). Map: `LIBRARY-group3-map.yaml`
(1519 (case, order) pairs; a script using the guard's own `contradicted_orders` / `library_answers`
confirms none is answered by the library now). All 150 cases changed; about 1410 case-specific
reports added; 36 contradicting case fallbacks replaced. 150/150 pass the perfect-agent check,
1230 case guards pass, and a before/after snapshot of every criterion alternative is identical in
every case (no criterion answer changed). Initial outputs, follow-ups already stored, criteria
and diagnoses were not touched.

## Group-wide decisions

- **Performance status in every case.** The library's Karnofsky 100 / ECOG 0 means "normal; no
  complaints; no evidence of disease", and it adds "working". That contradicts every patient who
  comes in with symptoms. Each case now has its own KPS and ECOG, based on the history, exam,
  care setting and social history.
- **Examination-type assessments are judged against the documented exam.** The library describes
  a healthy adult who can walk: normal timed gait, a levodopa challenge with normal gait and arm
  swing, MoCA 28, normal speech, a normal orthostatic set, a Bruce protocol at 10.4 METs. Where the
  exam rules that out, the case now has its own report. When the patient cannot do the test
  (drowsy, intubated, cannot stand, the test would be unsafe), the report says what the examiner
  could and could not do.
- **Condition-wide terms** (all cases, `except` lists the variants where the normal report is
  right):
  - BACT-MEN: performance status, timed gait, levodopa challenge, ICHD-3 headache history (these
    patients have an acute febrile headache with red flags) and brain MRI. The brain MRI is
    written without and with gadolinium, consistent with the stored CT, the organism and the
    complications.
  - GBS: performance status, timed gait, levodopa challenge, spine MRI and MR neurography. The
    library reads the nerve roots and cauda equina as not enhancing; enhancement is present in
    most AIDP and AMAN patients. Exempt variants: P01, RM12, RM15, RS11, RS15.
  - MG: performance status and EMG/NCS. The library's EMG/NCS impression rules out a
    neuromuscular junction disorder, which conduction studies without repetitive stimulation
    cannot do, and which is false in every case here.
  - NPH: performance status, levodopa challenge, neuropsychological battery (frontal-subcortical
    profile), exercise stress test and exercise echo (both impossible with these gait disorders).
  - SYNC-CARD: performance status, exercise stress test, tilt table and exercise echo. These now
    carry the patient's own rates, or "not performed" where the test would be unsafe: HCM, severe
    AS, an obstructing mass, febrile Brugada, torsades.
- **Per-case terms** follow the three rules of the brief: the diagnosis (NMJ tests in MG, the
  organism's microbiology in meningitis, the EEG in encephalopathy), the history and medications
  (HbA1c in treated diabetes, smear after splenectomy, immunoglobulins in hypogammaglobulinaemia,
  tox screen on benzodiazepines, coronary studies in known CAD, device interrogation with a
  device), and stored findings (a TEE, bubble study or exercise echo after an abnormal TTE,
  mediastinal MRI and whole-body PET when the CT shows a thymoma, an ECG rate that matches the
  vitals).
- **Case fallbacks replaced (an extension of the brief).** The case's own off-pathway fallback
  sometimes made the same error one tier up. Examples: a "normal awake and drowsy EEG" in an
  obtunded patient, a normal-rate ECG with HR 120, "no hydrocephalus" on CT in TB or cryptococcal
  meningitis. Leaving them would also have contradicted the new reports. They were replaced in
  place, with the same discriminator. Counts: 22 BACT-MEN, 9 GBS, 4 MG, 1 NPH. Every replacement
  is listed per case below and in the case logs. No pathway output was changed.
- **Left to the library on purpose:** what each case is consistent with (listed per condition
  under (c)). Also the library AED, valproate and lithium levels: they are wrong in every patient
  not on the drug, which is a central library defect (below), and no group-3 patient takes these
  drugs with a wrong level shown.

## Central issues (library or MockServer, beyond the per-case fix)

1. `AED_levels`, `valproate_level` and `lithium_level` report therapeutic levels in every patient.
   The library should report "not detected" unless the case stores a level.
2. `performance_status` says KPS 100 and "working". Examination-type library reports
   (gait, levodopa challenge, exercise test, exercise echo, orthostatic BP) describe a healthy,
   walking adult. The same contradiction is likely in PD, ataxia, myelopathy and stroke cases of
   the other groups.
3. `device_interrogation` describes an implanted device in patients who have none.
4. The `chest_CTA` library template has modality "CT". A case report built from it does not
   route as a CTA, and a stored chest CT answers a CTA order. The reports in this pass set "CTA"
   by hand. Related: a stored chest-abdomen-pelvis CT answers chest_CT and pelvis_abdomen_CT
   orders. That is consistent, but only partial, so GBS added separate reports.
5. Library values ignore stored data:
   - serum osmolality 288 with stored sodium 119-130;
   - a normal ABG with low stored bicarbonate, or with a gas already written in a stored
     respiratory-function report;
   - normal-brain resection and open-biopsy reports, and a cervical node biopsy, whatever the
     site.
6. The lab matcher answers GBS-M02's `antiphospholipid` order with stored anti-TPO and
   anti-thyroglobulin panels (shared "anti" stem). An ABG "pH" clause leaks into a urinalysis
   order (GBS-RS13).
7. Once an MRI or EEG follow-up exists, a plain-order fallback never reaches a plain order
   (GBS).
8. `whole_body_FDG_PET` and `FDG_PET` are separate terms. The pelvis MRI library report reads as
   a female pelvis. The library spine MRI never shows leptomeningeal enhancement.
9. Stored blood cultures in BACT-MEN-RP05 and RS02 say "susceptibilities as listed" but have no
   table. This is pathway data, so it was left unchanged.
10. Brain DTI, FDG-PET and perfusion SPECT in iNPH need a condition-wide decision. Only the
    cases with a stored focal lesion were changed (NPH).


## BACT-MEN

All 30 cases are acute meningitis presentations (26 bacterial, 1 tuberculous P02, 1 cryptococcal P03, 2 healthcare-associated M05/RS04), so the map has no exception. 30 cases changed, 439 reports added, 22 case fallbacks replaced. The map lists 5 all-cases orders and 334 case-specific orders; a script confirmed that none of the 484 (case, order) pairs is still answered by the library. Every case passes the perfect-agent check and the 9 case guards. No criterion answer changed: the snapshot before and after was identical in all 30 cases.

### (a) Terms judged contradictory and why

Condition-wide (every case):
- `performance_status` (30): the library returns Karnofsky 100 / ECOG 0, working, with no evidence of disease. Each case now has its own score: KPS 10-20 / ECOG 4 for obtunded or septic patients, KPS 30 / ECOG 3-4 for alert but toxic patients, KPS 40-50 / ECOG 2-3 for ambulant ones (P01, P03, RP01, RP03, RS01).
- `gait_and_balance_timed` (30): the library gives TUG 9.1 s and 1.28 m/s. Most patients could not or would not stand, so the report says "not performed" with the reason the stored exam gives. Ambulant patients (P01, P03, RP03, RS01, S05) got timed values that match their documented gait.
- `levodopa_challenge` (30): the library describes a normal gait, normal postural reflexes and a normal neck. It is now "not performed / not assessable", with the patient's own motor findings: nuchal rigidity, essential tremor (RS03), torticollis (RS01), hemiparesis (RS02).
- `structured_headache_history_ichd3` (30): the library elicits no red flags. Each case lists its own red flags without naming the diagnosis. The report says "no headache reported" where the patient denies headache (RS01), and "history not obtainable" where the patient is obtunded (RS04).
- `analyze_brain_mri` (17, where no MRI is stored): a gadolinium MRI is never normal here. Each report has leptomeningeal enhancement, agrees with the stored CT, includes the sinus or mastoid disease, post-surgical change, extradural collection, oedema or small vessel change the case records, and leaves contrast_used null. 13 cases store their own MRI.

Per case:
- EEG (`continuous_icu`/`video`, `ambulatory`, `sleep_deprived`, `routine`): an encephalopathic patient has a slowed background. The grade (mild, moderate) follows the stored routine EEG or the GCS. RP03 also has right frontal slowing over its stored lesion.
- `cognitive_screen` and `neuropsych_battery` (27 each): impaired or not testable whenever the stored exam records confusion or inattention. The library gives MoCA 28/30 and an average battery.
- `orthostatic_blood_pressure` (28): the library gives supine HR 68 and 3 minutes of standing. The reports now use the stored vitals, with standing "not performed" where the patient cannot stand. RS01 (near-syncope on standing) shows orthostatic hypotension.
- `whole_blood_pcr` (19): positive wherever the organism is a panel target (S. pneumoniae) and blood cultures grew it. The collection timing is copied from the stored culture.
- `analyze_ecg` (6 added, 9 case fallbacks replaced): sinus tachycardia at the presenting rate; the library and several case fallbacks say "normal ECG" at 72.
- `speech_language_evaluation` (12): dysarthria where the exam records it; not testable at GCS 9; limited testing in lethargic patients who do not follow commands.
- Labs:
  - ABG (10) where stored bicarbonate is 19 or lower, or the patient is hypoxic.
  - `serum_osmolality` (8) where stored sodium gives a calculated osmolality below 272. The library's 288 cannot coexist with sodium 119-130.
  - Peripheral smear (10): Howell-Jolly bodies in asplenia; cytopenias; thrombocytopenia with schistocytes in DIC.
  - Immunoglobulins in hypogammaglobulinaemia and IgA deficiency; SPEP/IFE/IgA in IgA MGUS (RS03).
  - HbA1c in treated diabetes; RF and anti-CCP in rheumatoid arthritis (M04, RS05); urine opiates on hydrocodone (RS01); niacin in pellagra (RS04); IGRA (P02).
- Hearing: `audiometry` and `baep` where hearing loss is stated (RM04, RP05, RS05, S03, S04).
- Eyes: OCT and perimetry for papilloedema (P03, RP02).
- Advanced brain imaging (perfusion MRI, MRS, FDG/amino-acid PET, SPECT, DTI, CT perfusion, fMRI) where the stored imaging shows a parenchymal lesion: M05 (resection cavity), RP03 (right frontal lesion), RS02 (encephalomalacia).
- Body imaging where findings are recorded:
  - bronchiectasis and splenomegaly (RP01);
  - VP shunt tubing (RS02);
  - effusions and ascites (RS04);
  - cervical spondylosis (RS01 spine CT);
  - the submandibular node (RP03 whole-body PET).
- Microbiology: Candida throat swab (P03); Klebsiella in the ear discharge (RP05); ascitic fluid "not obtained" (RS04).
- Cardiac: TEE, bubble and exercise echo from the abnormal TTE (M04); a coronary stent, and an exercise test that could not be done (RS03).
- Respiratory function "not performed" in patients who cannot cooperate (P05, S04); RM02 cerebral angiography and MRA; RM03 spine MRI; M05 resection pathology.

### (b) Per case: reports added and case fallbacks replaced

- **BACT-MEN-M01** (17 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (drowsy, unable to stand); timed tests not performed; levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: diffuse leptomeningeal enhancement and sulcal FLAIR hyperintensity; maxillary sinus mucosal thickening; no complication; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not completed (drowsy, inattentive); disoriented to place and time; neuropsych_battery: not completed (reduced arousal, inattention); speech_language_evaluation: dysarthria; language content appropriate; testing limited by drowsiness; whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 107/67, HR 106; standing not performed; peripheral smear: Howell-Jolly bodies, neutrophilia with toxic granulation; quantitative_Ig: IgG 410 mg/dL (low); IgG_subclasses: IgG1, IgG2, IgG3 low; ABG: metabolic acidosis with partial respiratory compensation; serum_osmolality: serum osmolality 266 mOsm/kg (low); case fallback replaced `fallback_tool_outputs.eeg` (analyze_eeg {eeg_type: routine}): routine EEG now shows continuous generalised theta-delta slowing (was a normal awake and drowsy EEG); case fallback replaced `fallback_tool_outputs.ecg` (analyze_ecg): sinus tachycardia at 106 bpm, otherwise normal (was a normal ECG).
- **BACT-MEN-M02** (13 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not performed (headache, photophobia, confusion); brief supported standing steady; levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: diffuse leptomeningeal enhancement and sulcal FLAIR hyperintensity; no complication; continuous_icu: mild generalised theta slowing; no epileptiform discharges or seizures; ambulatory: mild generalised theta slowing; no epileptiform discharges or seizures; cognitive_screen: MoCA 17/30 with inattention and temporal disorientation; neuropsych_battery: not completed (inattention, acute confusion); whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 102/70, HR 119; standing not performed; peripheral smear: Howell-Jolly bodies, toxic granulation; serum_osmolality: serum osmolality 268 mOsm/kg (low); case fallback replaced `fallback_tool_outputs.eeg` (analyze_eeg {eeg_type: routine}): routine EEG now shows mild generalised theta slowing; no epileptiform discharges or seizures (was a normal awake and drowsy EEG); case fallback replaced `fallback_tool_outputs.ecg` (analyze_ecg): sinus tachycardia at 119 bpm, otherwise normal (was a normal ECG).
- **BACT-MEN-M03** (15 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (drowsy, clinically unstable); timed tests not performed; levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: diffuse leptomeningeal enhancement and sulcal FLAIR hyperintensity; maxillary sinus mucosal thickening; no complication; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not completed (drowsy, inattentive); disoriented to time; neuropsych_battery: not completed (reduced arousal, inattention); whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 132/79, HR 114; standing not performed; peripheral smear: Howell-Jolly bodies, toxic granulation; HbA1c: HbA1c 7.3%; ABG: metabolic acidosis with partial respiratory compensation; serum_osmolality: serum osmolality 260 mOsm/kg (low); case fallback replaced `fallback_tool_outputs.eeg` (analyze_eeg {eeg_type: routine}): routine EEG now shows continuous generalised theta-delta slowing; no epileptiform discharges or seizures (was a normal awake and drowsy EEG); case fallback replaced `fallback_tool_outputs.ecg` (analyze_ecg): sinus tachycardia at 114 bpm, otherwise normal (was a normal ECG).
- **BACT-MEN-M04** (15 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (cannot sit unaided); limb ataxia left > right; levodopa_challenge: no parkinsonian signs; action tremor and limb ataxia; challenge not performed; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not completed (lethargic); impaired recall, disoriented to time; neuropsych_battery: not completed (reduced arousal, inattention); speech_language_evaluation: mild dysarthria; no aphasia; orthostatic_blood_pressure: supine BP 148/82, HR 96; standing not performed; TEE: mild LA enlargement, mitral annular calcification and aortic sclerosis; no vegetation; bubble_study: no shunt; mild LA enlargement, mitral annular calcification and aortic sclerosis; exercise_echo: stress not performed (cannot exercise); resting study as the stored TTE; RF: rheumatoid factor 52 IU/mL (elevated); anti_CCP: anti-CCP 110 U/mL (elevated); case fallback replaced `fallback_tool_outputs.eeg` (analyze_eeg {eeg_type: routine}): routine EEG now shows continuous generalised theta-delta slowing; no epileptiform discharges or seizures (was a normal awake and drowsy EEG).
- **BACT-MEN-M05** (18 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (bed-bound, EVD, lethargic); levodopa_challenge: no parkinsonian signs; left hemiparesis; challenge not performed; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; continuous_icu: generalised slowing with right centroparietal focal delta and breach rhythm; no epileptiform discharges; ambulatory: generalised slowing with right centroparietal focal delta and breach rhythm; no epileptiform discharges; cognitive_screen: not completed (lethargic); disoriented to time; neuropsych_battery: not completed (reduced arousal, inattention); orthostatic_blood_pressure: supine BP 138/82, HR 102; standing not performed; resection: glioblastoma, IDH-wildtype, CNS WHO grade 4 (the resection specimen); amino_acid_PET: resection cavity with mild marginal uptake; no other focal uptake; perfusion_MRI: resection cavity without marginal hyperperfusion; ependymal hyperperfusion; MR_spectroscopy: abnormal spectra at the resection margin; FDG_PET: resection cavity; otherwise symmetric uptake; DTI_tractography: resection cavity with tract displacement; functional_MRI: resection cavity; motor activation preserved; left language dominance; CT_perfusion: cavity non-perfused; no territorial deficit; perfusion_SPECT: perfusion defect at the resection cavity; case fallback replaced `fallback_tool_outputs.eeg` (analyze_eeg {eeg_type: routine}): routine EEG now shows generalised slowing with right centroparietal focal delta and breach rhythm (was a mildly disorganised background with an 8-9 Hz posterior rhythm).
- **BACT-MEN-P01** (10 reports): performance_status: Karnofsky 50, ECOG 2; gait_and_balance_timed: mildly slowed gait speed, balance preserved; levodopa_challenge: no parkinsonian signs; neck stiffness noted; challenge not administered; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: thin leptomeningeal enhancement over both convexities; no complication; cognitive_screen: MoCA 25/30 with attention errors; neuropsych_battery: mildly reduced attention and processing speed; whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: no orthostatic hypotension; resting HR 92; serum_osmolality: serum osmolality 270 mOsm/kg (low).
- **BACT-MEN-P02** (13 reports): performance_status: Karnofsky 30, ECOG 4; gait_and_balance_timed: not testable (confused, unsteady); levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; routine: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; sleep_deprived: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: MoCA 16/30 with inattention, poor recall and temporal disorientation; neuropsych_battery: not completed (acute confusion, inattention); orthostatic_blood_pressure: supine BP 128/78, HR 88; standing not performed; IGRA: IGRA positive; serum_osmolality: serum osmolality 263 mOsm/kg (low); case fallback replaced `fallback_tool_outputs.ct` (order_ct_scan): a CT with mild communicating hydrocephalus and basal cistern hyperattenuation (was a normal CT without hydrocephalus).
- **BACT-MEN-P03** (14 reports): performance_status: Karnofsky 50, ECOG 2; gait_and_balance_timed: slowed gait speed and mildly reduced balance; levodopa_challenge: no parkinsonian signs; slow cautious gait; challenge not administered; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; routine: mild generalised theta slowing; no epileptiform discharges or seizures; sleep_deprived: mild generalised theta slowing; no epileptiform discharges or seizures; continuous_icu: mild generalised theta slowing; no epileptiform discharges or seizures; ambulatory: mild generalised theta slowing; no epileptiform discharges or seizures; cognitive_screen: MoCA 20/30 with inattention, poor recall and temporal disorientation; neuropsych_battery: multidomain impairment (processing speed, attention, executive, retrieval); optical_coherence_tomography: bilateral RNFL thickening with optic disc swelling; visual_field_perimetry: bilateral blind-spot enlargement; throat_swab: heavy growth of Candida albicans; peripheral smear: normocytic anaemia and leucopenia; case fallback replaced `fallback_tool_outputs.ct` (order_ct_scan): a CT with mild communicating hydrocephalus (was a normal CT without hydrocephalus).
- **BACT-MEN-P04** (8 reports): performance_status: Karnofsky 30, ECOG 3; gait_and_balance_timed: not performed (headache, photophobia); a few assisted steps with normal base; levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: leptomeningeal enhancement; right maxillary and ethmoid sinus disease; no complication; cognitive_screen: MoCA 24/30 with mild inattention and reduced recall; neuropsych_battery: mildly reduced attention, processing speed and recall; orthostatic_blood_pressure: supine BP 122/78, HR 108; standing not performed.
- **BACT-MEN-P05** (15 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (GCS 11, unable to walk safely); levodopa_challenge: no parkinsonian signs; right pyramidal signs; challenge not performed; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: leptomeningeal enhancement greater on the left; subtle left frontotemporal cortical signal change; sinus disease; continuous_icu: generalised delta slowing with left frontotemporal focal slowing; no epileptiform discharges or seizures; ambulatory: generalised delta slowing with left frontotemporal focal slowing; no epileptiform discharges or seizures; cognitive_screen: not completed (encephalopathy, paraphasic speech); neuropsych_battery: not completed (encephalopathy); speech_language_evaluation: paraphasic speech with impaired naming, repetition and comprehension; whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 148/86, HR 118; standing not performed; ABG: metabolic acidosis with hypoxaemia (pO2 61); respiratory_function: not performed (unable to cooperate); serum_osmolality: serum osmolality 270 mOsm/kg (low); case fallback replaced `fallback_tool_outputs.eeg` (analyze_eeg {eeg_type: routine}): repeat routine EEG now shows generalised delta slowing with left frontotemporal focal slowing (was a normal awake and drowsy EEG).
- **BACT-MEN-RM01** (14 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (bed-bound, GCS 11); levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: diffuse leptomeningeal enhancement, mild diffuse swelling, maxillary sinus thickening; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not completed (GCS 11); neuropsych_battery: not completed (reduced consciousness); whole_blood_pcr: Haemophilus influenzae DNA detected; orthostatic_blood_pressure: supine BP 92/58, HR 118; standing not performed; peripheral smear: Howell-Jolly bodies, left shift with toxic granulation; HbA1c: HbA1c 7.8%; analyze_ecg: sinus tachycardia at 118 bpm, otherwise normal.
- **BACT-MEN-RM02** (14 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (GCS 10, unable to stand); levodopa_challenge: no parkinsonian signs; bilateral pyramidal signs; challenge not performed; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not completed (GCS 10); neuropsych_battery: not completed (reduced consciousness); speech_language_evaluation: severe dysarthria; language not testable; whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 142/82, HR 96; standing not performed; cerebral_angiography: hypoplastic arterial segments; no vasculitic change; MR_angiography: hypoplastic arterial segments; no stenosis; ABG: metabolic acidosis with partial respiratory compensation.
- **BACT-MEN-RM03** (16 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (drowsy, cannot stand); prior shuffling small-step gait noted; levodopa_challenge: no rest tremor; increased tone; challenge not performed; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: communicating hydrocephalus, leptomeningeal and ependymal enhancement with ventricular debris, small vessel change; routine: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; sleep_deprived: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: K-MMSE about 15/30; MoCA not completed; neuropsych_battery: not completed (reduced arousal, inattention); whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 148/82, HR 102; standing not performed; peripheral smear: Howell-Jolly bodies, toxic granulation; HbA1c: HbA1c 7.8%; spine_MRI: L4-L5 disc herniation; cord normal.
- **BACT-MEN-RM04** (13 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: broad-based ataxic gait, Romberg positive, tandem impossible; timed tests not completed; levodopa_challenge: no parkinsonian signs; ataxic gait; challenge not administered; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: leptomeningeal enhancement and bilateral labyrinthine enhancement; clear mastoids; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not completed (drowsy, severe hearing loss); neuropsych_battery: not completed (drowsy, severe hearing loss); audiometry: bilateral severe-profound sensorineural hearing loss; baep: absent waves bilaterally; orthostatic_blood_pressure: supine BP 138/84, HR 108; standing not performed; HbA1c: HbA1c 7.4%; case fallback replaced `fallback_tool_outputs.eeg` (analyze_eeg {eeg_type: routine}): routine EEG now shows continuous generalised theta-delta slowing; no epileptiform discharges or seizures (was a normal awake EEG).
- **BACT-MEN-RP01** (18 reports): performance_status: Karnofsky 40, ECOG 3; gait_and_balance_timed: not performed (headache, unsteadiness on standing); levodopa_challenge: no parkinsonian signs; neck stiffness noted; challenge not administered; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: thin leptomeningeal enhancement; paranasal sinus disease; no complication; cognitive_screen: MoCA 24/30 with mild inattention and reduced recall; neuropsych_battery: mildly reduced attention, processing speed and recall; whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: no orthostatic hypotension; resting HR 92; IgA: IgA 12 mg/dL (low); IgG_subclasses: all IgG subclasses low; chest_CT: bilateral basal bronchiectasis with mucus plugging; chest_CTA: no embolism; bilateral basal bronchiectasis; chest_xray: basal bronchial wall thickening; chest_abdomen_pelvis_CT: bronchiectasis and mild splenomegaly; pelvis_abdomen_CT: mild splenomegaly; pelvis_abdomen_ultrasound: mild splenomegaly; pelvis_abdomen_MRI: mild splenomegaly.
- **BACT-MEN-RP02** (14 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not performed (somnolent, refuses to walk); levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: post-surgical frontal changes, 4 mm bifrontal extradural collection, diffuse leptomeningeal enhancement; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not completed (somnolent, inattentive); uncertain of date; neuropsych_battery: not completed (somnolence, inattention); whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 108/62, HR 112; standing not performed; analyze_ecg: sinus tachycardia at 112 bpm, otherwise normal; optical_coherence_tomography: mild bilateral RNFL thickening with optic disc swelling; visual_field_perimetry: mild bilateral blind-spot enlargement, reduced reliability; case fallback replaced `fallback_tool_outputs.eeg` (analyze_eeg {eeg_type: routine}): routine EEG now shows continuous generalised theta-delta slowing; no epileptiform discharges or seizures (was a normal awake and drowsy EEG).
- **BACT-MEN-RP03** (20 reports): performance_status: Karnofsky 50, ECOG 3; gait_and_balance_timed: timed gait and balance normal; testing limited by inattention; levodopa_challenge: no parkinsonian signs; neck stiffness noted; challenge not administered; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; routine: mild generalised theta slowing; no epileptiform discharges or seizures; sleep_deprived: mild generalised theta slowing; no epileptiform discharges or seizures; continuous_icu: mild generalised theta slowing; no epileptiform discharges or seizures; ambulatory: mild generalised theta slowing; no epileptiform discharges or seizures; cognitive_screen: MoCA 19/30 with inattention, dysexecutive features and disinhibition; neuropsych_battery: frontal-subcortical pattern with inattention and disinhibition; whole_blood_pcr: Streptococcus pneumoniae DNA detected; peripheral smear: mild normocytic anaemia, leucopenia with lymphopenia; MR_spectroscopy: abnormal spectra in the right frontal lesion; perfusion_MRI: hypoperfused right frontal lesion; FDG_PET: hypometabolic right frontal lesion; amino_acid_PET: no uptake in the right frontal lesion; perfusion_SPECT: right frontal hypoperfusion; DTI_tractography: reduced FA in the right frontal lesion; major tracts intact; CT_perfusion: mildly reduced perfusion in the right frontal hypodensity; no territorial deficit; whole_body_FDG_PET: FDG-avid right submandibular node and buccal ulcer.
- **BACT-MEN-RP04** (13 reports): performance_status: Karnofsky 30, ECOG 4; gait_and_balance_timed: not performed (refuses to stand: headache, photophobia); levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; routine: mild generalised theta slowing; no epileptiform discharges or seizures; sleep_deprived: mild generalised theta slowing; no epileptiform discharges or seizures; continuous_icu: mild generalised theta slowing; no epileptiform discharges or seizures; ambulatory: mild generalised theta slowing; no epileptiform discharges or seizures; cognitive_screen: MoCA 18/30 with inattention and temporal disorientation; neuropsych_battery: not completed (inattention, acute confusion); whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 122/74, HR 108; standing not performed; serum_osmolality: serum osmolality 267 mOsm/kg (low).
- **BACT-MEN-RP05** (15 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (drowsy, unable to stand); levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: subacute progressive headache with red flags; criteria for a primary headache disorder not met; sleep_deprived: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not completed (drowsy, inattentive); oriented to name only; neuropsych_battery: not completed (reduced arousal, inattention); speech_language_evaluation: dysarthria; language testing limited by drowsiness; audiometry: bilateral conductive hearing loss, worse on the left; baep: prolonged wave I bilaterally (left worse), normal interpeak latencies; wound_swab: Klebsiella pneumoniae from the left ear discharge; ABG: metabolic acidosis with partial respiratory compensation; orthostatic_blood_pressure: supine BP 138/90, HR 128; standing not performed.
- **BACT-MEN-RS01** (9 reports): performance_status: Karnofsky 50, ECOG 2; gait_and_balance_timed: mildly slowed antalgic gait; lightheaded on rising; levodopa_challenge: no parkinsonian signs; fixed left torticollis; challenge not administered; structured_headache_history_ichd3: no headache; persistent neck pain and stiffness with systemic red flags; analyze_brain_mri: basal and posterior fossa leptomeningeal enhancement; no complication; analyze_ecg: sinus tachycardia at 120 bpm, otherwise normal; orthostatic_blood_pressure: orthostatic hypotension with symptoms; resting HR 120; spine_CT: C4-C6 degenerative disc disease; no fracture or bone destruction; tox_screen: urine opiates positive (prescribed hydrocodone).
- **BACT-MEN-RS02** (23 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (GCS 9, unable to stand); levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; sleep_deprived: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not testable (GCS 9); neuropsych_battery: not testable (reduced consciousness); speech_language_evaluation: not testable (GCS 9); whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 142/88, HR 112; standing not performed; perfusion_MRI: non-perfused encephalomalacia; sulcal hyperperfusion; MR_spectroscopy: reduced metabolites in the encephalomalacia; FDG_PET: right frontoparietal hypometabolism; amino_acid_PET: photopenic encephalomalacia; no increased uptake; perfusion_SPECT: right frontoparietal perfusion defect; DTI_tractography: thinned right corticospinal tract at the encephalomalacia; functional_MRI: altered right motor activation; left language dominance; CT_perfusion: no territorial deficit; encephalomalacia non-perfused; chest_xray: clear lungs; continuous shunt tubing; pelvis_abdomen_CT: distal shunt catheter in place; no pseudocyst or collection; chest_abdomen_pelvis_CT: shunt in place without complication; otherwise normal; case fallback replaced `fallback_tool_outputs.ecg` (analyze_ecg): sinus tachycardia at 112 bpm, otherwise normal (was a normal ECG).
- **BACT-MEN-RS03** (20 reports): performance_status: Karnofsky 30, ECOG 4; gait_and_balance_timed: not performed (acute illness, debility); levodopa_challenge: action tremor (essential tremor), no parkinsonian signs; challenge not performed; structured_headache_history_ichd3: new headache after age 50 with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: diffuse leptomeningeal enhancement; chronic small vessel change; no complication; routine: mild generalised theta slowing; no epileptiform discharges or seizures; sleep_deprived: mild generalised theta slowing; no epileptiform discharges or seizures; continuous_icu: mild generalised theta slowing; no epileptiform discharges or seizures; ambulatory: mild generalised theta slowing; no epileptiform discharges or seizures; cognitive_screen: MoCA 20/30 with inattention and temporal disorientation; neuropsych_battery: not completed (acute illness, inattention); whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 148/82, HR 108; standing not performed; analyze_ecg: sinus tachycardia at 108 bpm, otherwise normal; SPEP: monoclonal band 0.6 g/dL (beta region); IFE: IgA kappa monoclonal protein; quantitative_Ig: IgA 640 mg/dL (raised); emg_ncs: mild length-dependent axonal sensory neuropathy; no myopathy; exercise_stress_test: not performed (acute illness, cannot exercise); coronary_angiography: patent stent; non-obstructive disease.
- **BACT-MEN-RS04** (22 reports): performance_status: Karnofsky 10, ECOG 4; gait_and_balance_timed: not testable (GCS 9, non-ambulatory); levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: history not obtainable (obtunded); red flags present; sleep_deprived: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not testable (GCS 9); neuropsych_battery: not testable (reduced consciousness); speech_language_evaluation: not testable (GCS 9); orthostatic_blood_pressure: supine BP 92/58, HR 118; standing not performed; analyze_ecg: sinus tachycardia at 118 bpm, otherwise normal; ABG: metabolic acidosis with partial respiratory compensation; mild hypoxaemia; serum_osmolality: serum osmolality 252 mOsm/kg (low); niacin_B3: niacin 0.4 ug/mL (low); peripheral smear: normocytic anaemia, neutrophilia with toxic granulation; chest_xray: small bilateral effusions; chest_CT: small bilateral effusions; no consolidation; pelvis_abdomen_CT: minimal ascites; no collection or obstruction; chest_abdomen_pelvis_CT: small effusions and ascites; no collection; pelvis_abdomen_ultrasound: minimal ascites; no hydronephrosis; ascitic_fluid: not obtained (no accessible fluid); case fallback replaced `fallback_tool_outputs.eeg` (analyze_eeg {eeg_type: routine}): routine EEG now shows continuous generalised theta-delta slowing; no epileptiform discharges or seizures (was a normal awake and drowsy EEG).
- **BACT-MEN-RS05** (16 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (lethargic, unable to stand); levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: diffuse leptomeningeal enhancement; age-related small vessel change; no complication; sleep_deprived: mild generalised theta slowing; no epileptiform discharges or seizures; continuous_icu: mild generalised theta slowing; no epileptiform discharges or seizures; ambulatory: mild generalised theta slowing; no epileptiform discharges or seizures; cognitive_screen: not completed (lethargic, inattentive); oriented to name only; neuropsych_battery: not completed (reduced arousal, inattention); speech_language_evaluation: slow soft speech; testing limited by lethargy; audiometry: bilateral high-frequency sensorineural loss (presbycusis); baep: low-amplitude delayed wave I; normal interpeak latencies; RF: rheumatoid factor 64 IU/mL (elevated); anti_CCP: anti-CCP 140 U/mL (elevated); orthostatic_blood_pressure: supine BP 128/74, HR 108; standing not performed.
- **BACT-MEN-S01** (14 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (lethargic, unable to stand); levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: diffuse leptomeningeal enhancement, mild oedema, maxillary and ethmoid sinusitis; sleep_deprived: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not completed (lethargic, inattentive); oriented to self only; neuropsych_battery: not completed (reduced arousal, inattention); speech_language_evaluation: dysarthria; language content intact; testing limited by lethargy; whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 135/90, HR 117; standing not performed; ABG: metabolic acidosis with partial respiratory compensation; case fallback replaced `fallback_tool_outputs.eeg` (analyze_eeg {eeg_type: routine}): routine EEG now shows continuous generalised theta-delta slowing; no epileptiform discharges or seizures (was a normal awake and drowsy EEG); case fallback replaced `fallback_tool_outputs.ecg` (analyze_ecg): sinus tachycardia at 117 bpm, otherwise normal (was a normal ECG).
- **BACT-MEN-S02** (15 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (GCS 11, bed-bound); levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: diffuse leptomeningeal enhancement; maxillary and ethmoid sinusitis; no complication; sleep_deprived: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not testable (GCS 11); neuropsych_battery: not testable (reduced consciousness); speech_language_evaluation: dysarthria; incoherent output; testing limited by obtundation; whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 90/54, HR 116; standing not performed; analyze_ecg: sinus tachycardia at 116 bpm, otherwise normal; ABG: lactic metabolic acidosis with partial respiratory compensation; case fallback replaced `fallback_tool_outputs.eeg` (analyze_eeg {eeg_type: routine}): routine EEG now shows continuous generalised theta-delta slowing; no epileptiform discharges or seizures (was a normal awake and drowsy EEG).
- **BACT-MEN-S03** (14 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (lethargic, unable to walk); levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; sleep_deprived: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not completed (lethargic, inattentive); oriented to self only; neuropsych_battery: not completed (reduced arousal, inattention); speech_language_evaluation: slow confused speech, no dysphasia; testing limited; audiometry: mild right conductive hearing loss; baep: prolonged right wave I; normal interpeak latencies; whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 133/74, HR 125; standing not performed; case fallback replaced `fallback_tool_outputs.eeg` (analyze_eeg {eeg_type: routine}): routine EEG now shows continuous generalised theta-delta slowing; no epileptiform discharges or seizures (was a normal awake and drowsy EEG); case fallback replaced `fallback_tool_outputs.ecg` (analyze_ecg): sinus tachycardia at 125 bpm, otherwise normal (was a normal ECG).
- **BACT-MEN-S04** (17 reports): performance_status: Karnofsky 20, ECOG 4; gait_and_balance_timed: not testable (somnolent, unable to stand); levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; sleep_deprived: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; continuous_icu: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; ambulatory: continuous generalised theta-delta slowing; no epileptiform discharges or seizures; cognitive_screen: not completed (somnolent, inattentive); oriented to person only; neuropsych_battery: not completed (reduced arousal, inattention); speech_language_evaluation: dysarthria; testing limited by somnolence; audiometry: profound right loss (cochlear implant); left near normal; baep: absent right waves; normal left; whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 85/53, HR 116; standing not performed; ABG: lactic metabolic acidosis with partial respiratory compensation; peripheral smear: toxic granulation, thrombocytopenia, occasional schistocytes; respiratory_function: not performed (unable to cooperate); case fallback replaced `fallback_tool_outputs.eeg` (analyze_eeg {eeg_type: routine}): routine EEG now shows continuous generalised theta-delta slowing; no epileptiform discharges or seizures (was a normal awake and drowsy EEG); case fallback replaced `fallback_tool_outputs.ecg` (analyze_ecg): sinus tachycardia at 116 bpm, otherwise normal (was a normal ECG).
- **BACT-MEN-S05** (7 reports): performance_status: Karnofsky 30, ECOG 3; gait_and_balance_timed: slowed antalgic gait, no ataxia; levodopa_challenge: no parkinsonian signs; neck stiffness noted; challenge not administered; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; orthostatic_blood_pressure: supine BP 102/62, HR 124; standing not performed; ABG: lactic metabolic acidosis with partial respiratory compensation; peripheral smear: toxic granulation, thrombocytopenia, occasional schistocytes.
- **BACT-MEN-S06** (7 reports): performance_status: Karnofsky 30, ECOG 4; gait_and_balance_timed: not performed (headache, dizziness); brief standing steady; levodopa_challenge: no parkinsonian signs; challenge not performed; gait and postural reflexes not assessable; structured_headache_history_ichd3: new acute headache with red flags; criteria for a primary headache disorder not met; analyze_brain_mri: diffuse leptomeningeal enhancement; partial left mastoid opacification; no complication; whole_blood_pcr: Streptococcus pneumoniae DNA detected; orthostatic_blood_pressure: supine BP 148/92, HR 112; standing not performed.

### (c) Terms left to the library on purpose

- EEG in alert, oriented, mildly inattentive patients (P01, P04, RP01, RS01, S05, S06): a normal waking background is plausible.
- Cognitive screen and battery where the stored exam records intact orientation and attention (RS01, S05, S06).
- `whole_blood_pcr` where the organism is not a panel target (Listeria M04/RS05, S. aureus M05, M. tuberculosis P02, Cryptococcus P03, S. suis RM04, Klebsiella RP05, GBS RS01, Proteus RS04), or the culture is negative (P04), or the case stores its own (S05).
- Holter fallbacks, and TEE, bubble and exercise echo, wherever the stored TTE is normal.
- Library head CT in cases without a stored CT (normal is plausible).
- `urine_sodium` and `urine_osmolality`: the library's 85 mmol/L and 550 mOsm/kg already fit the hyponatraemia these cases show.
- Orthostatic BP in P03 and RP03 (vitals close to the library's, no orthostatic symptoms).
- ECG in non-tachycardic patients and where the case stores one.
- ABG where bicarbonate is 20 or more and the patient is not hypoxic (RS01, S03 and others).
- Speech where only word-finding pauses, slowed or tangential speech without dysarthria are recorded.
- Peripheral smear for a left shift alone, outside asplenia, cytopenia or DIC.
- D-dimer and coagulation: a coagulation panel is stored in all 30 cases, and a raised D-dimer in the 18 cases with sepsis or DIC. Elsewhere the library's normal D-dimer is left, since there is no DIC.
- Other terms:
  - AED, valproate and lithium levels: no patient here takes valproate or lithium; M05's levetiracetam level of 25 is plausible.
  - Stereotactic and open biopsy in M05.
  - Beta2-microglobulin, toxoplasma IgG, RPR and cryptococcal antigen where they agree with the stored data.
  - beta2-transferrin in RP02 (leak repaired).
  - Lymph node biopsy in RP03 (a reactive node is plausible).
  - Carotid and venous duplex.
  - Temporal artery ultrasound and biopsy in RS03.
  - Complement and throat swab in S05.
  - Chest imaging in P02, P05 and in patients without pulmonary signs.
  - Sputum, the PFTs in RP01, anti-TPO in P02, BAEP in M04.

### (d) Doubts for the physicians

- P02: a positive IGRA in tuberculous meningitis (could be indeterminate).
- M04 and RS05: RA seropositivity is assumed (RF and anti-CCP positive). The cases state only "rheumatoid arthritis".
- RS03: the MGUS light chain was chosen as kappa; the case says only "IgA monoclonal gammopathy". The reports also include an LAD-unspecified patent stent and a mild axonal sensory neuropathy on NCS.
- RM02: the vessels named in the angiography and MRA reports.
- Spine MRI: the library reports no leptomeningeal or cauda equina enhancement in any meningitis case without a stored spine MRI. Should this become condition-wide?
- BAEP in M04's brainstem lesion; CXR in tuberculous meningitis (P02) and in hypoxic COPD (P05).
- RP03: the advanced imaging pattern describes the right frontal lesion as non-enhancing, hypoperfused and without amino-acid uptake. It was chosen to fit the stored MRI and to stay non-diagnostic; please confirm.
- RP03 lymph node biopsy (left reactive) with a 3-week buccal ulcer and a 2 cm firm node.
- RS02: SSEP left normal despite the right frontoparietal encephalomalacia and left spastic hemiparesis.
- RP05: the left ear swab grows Klebsiella. This is inferred from the source; the case records only mucopurulent discharge.
- RS01: orthostatic hypotension values (26 mmHg fall) are chosen to fit the near-syncope; tamsulosin and cyclobenzaprine are possible contributors.
- S04 and S05: occasional schistocytes on the smear in DIC are assumed.

### (e) Central issues for the lead

- `chest_CTA` template modality is "CT", so a stored chest CT report answers a chest CTA order. My reports set modality "CTA" (RP01). The template should say CTA.
- Library defaults that assume a healthy ambulant adult, contradicted in almost every acute case:
  - performance status reports "working";
  - levodopa challenge and exercise tests describe a normal gait and 10.4 METs;
  - serum osmolality is 288 even when stored sodium is 119-130;
  - the ABG is normal even when stored bicarbonate is low.
  A library tier that reads the stored sodium, bicarbonate and vitals would remove most of these per-case reports.
- AED, valproate and lithium library levels are "therapeutic" in every patient, including those not on the drug.
- The spine MRI library reports no leptomeningeal enhancement (see doubts).
- Case data defect, not changed (stored follow-up): RP05 and RS02 blood cultures say "susceptibilities as listed" but carry no susceptibility table.

## GBS

30 cases, all changed; 336 case-specific reports added; 9 case fallbacks replaced. Every case:
criteria answers unchanged, perfect agent pass (30/30), case guards pass (240), every term in
`GBS-map.yaml` answered without the library. Only `fallback_tool_outputs` and appended follow-ups
changed; initial outputs, existing follow-ups, criteria and diagnoses untouched. Logs appended
under "## Library contradictions (25 Oct 2026)".

### (a) Terms judged contradictory and why

Condition-wide (`all_cases`, except P01, RM12, RM15, RS11, RS15):
- `performance_status` (all 30 including exceptions): the library gives Karnofsky 100 / ECOG 0 and a
  working patient. Every GBS patient here is admitted, most cannot walk; values set from the case
  (Karnofsky 20-80, ECOG 1-4).
- `gait_and_balance_timed`: a normal timed gait in patients who cannot walk or need support. Reports
  give "not performed (cannot stand)" or measured impaired gait (Berg, Romberg) from the examination.
- `levodopa_challenge`: the library describes a normal motor exam, gait and postural reflexes. Report:
  no tremor or rigidity, items limited by flaccid weakness, not validly scorable; ventilated
  patients: challenge not performed.
- `spine_MRI` (AIDP, AMAN, AMSAN, PCB): smooth cauda equina / ventral root enhancement is the typical
  finding; library reads roots as normal. Already stored (not library) in RM14, RM16, RP11, RP13,
  RP16, RS12, RS13, RS18; added in the other 19 non-exempt cases (cervical roots in RS15, PCB).
- `peripheral_nerve_MRI`: extends the spine MRI rationale (rule 1 and 3: root enhancement, as on the
  spine MRI of the case). Lumbosacral by default; cervical plus lumbosacral in RM16, RS18;
  cervical in RM12 and RS15 (PCB).

Per case (rules 1-3 of the policy; data in each log line):
- `orthostatic_blood_pressure` (25 cases): the library has 3 minutes of symptom-free standing in
  patients who cannot stand. Reports: standing not performed, supine and sitting (or head-up in bed
  for ventilated) values from the vitals and telemetry; RM11 stands with support (no OH, tachycardia).
- `nerve_biopsy` (22): AIDP with abnormal sural response on the stored NCS gets inflammatory
  demyelination (diabetic microangiopathy added in M03, RM13, RS16, RS17, S04; prominent secondary
  axonal degeneration in S03; mild non-inflammatory large-fibre loss in P01, MFS).
- `autonomic_testing` + `tilt_table` (17 each): dysautonomia on stored telemetry (BP lability,
  tachycardia, bradycardia episodes, urinary retention). Ambulatory lability pattern; symptomatic OH
  in M02, RM14, RP15; ventilated (RS16-18): limited study, tilt not performed.
- `speech_language_evaluation` (17): facial or bulbar weakness on examination (flaccid dysarthria,
  hypernasality, labial type in bifacial cases); ventilated: not assessable, comprehension intact.
- `cognitive_screen` / `neuropsych_battery` (5 each): RM13 hepatic encephalopathy (MoCA 22/30), RS13
  vascular dementia with acute confusion (not completed), RS16-18 intubated (not administrable).
- `ssep` (5: RM16, RP13, RS16, RS18, S01): absent SNAPs plus marked large-fibre sensory loss.
- `ABG` (7: M01, M02, RS13, RS17, S01, S03, S04): stored gases (rule 3) or SpO2 93% on room air.
- EEG: RM13, RS13, RS17 continuous_icu, ambulatory, video (encephalopathy, confusion, stored slow EEG);
  RP14 routine (empty slot filled; mild residual slowing after hyponatraemic encephalopathy).
- Comorbidity imaging and labs (rule 2): RM13 cirrhosis (abdomen x4, chest CT, HbA1c, quantitative Ig);
  RM14 postpartum (abdomen x4, chest CT, prolactin); M02 Hashimoto (anti_TPO, anti_thyroglobulin);
  M03 and S04 diabetic neuropathy (skin_biopsy_iencf); RP11 metastatic uterine cancer (chest x4,
  abdomen x3, FDG PET); RP13 colectomy and cholecystectomy (abdomen x4, chest CT, spine_CT cervical
  stenosis); RP14 COPD (chest x4, abdominal CT); RP15 lung transplant (chest x4, mediastinum CT,
  abdominal CT); RP16 leukaemia induction (peripheral smear); RM16 and RS12 spine_CT (spondylosis;
  L1-L5 laminectomy and fusion); RS13 crush rhabdomyolysis (urinalysis: blood 2+, 1 RBC/hpf); RS15
  aspiration pneumonia (chest x4, abdominal CT); RS16 STEMI with PCI and AF (TEE, bubble, exercise
  echo and stress test "not performed", coronary angiography, coronary CTA, cardiac MRI, EP study,
  HbA1c, chest x4, abdominal CT); RS17 pneumonia and diabetes (chest x4, abdominal CT, HbA1c); S04 BPH
  (abdomen x4, chest CT).
- Own `chest_CT` (RM13, RM14, RP13, S04) and `pelvis_abdomen_CT` (RP14, RP15, RS15, RS16, RS17)
  reports were added because those orders otherwise received the chest-abdomen-pelvis follow-up
  (a chest CT describing the uterus or prostate, an abdominal CT describing the lung transplant).

### (b) Per case: reports added; case fallbacks replaced

| Case | Reports | Fallbacks replaced |
|---|---|---|
| M01 | 11 | |
| M02 | 13 | |
| M03 | 11 | |
| P01 (MFS) | 5 | |
| P02 | 9 | |
| P03 | 6 | |
| RM11 | 8 | |
| RM12 (PCB) | 5 | |
| RM13 | 19 | brain MRI (pallidal T1 hyperintensity), EEG (mild diffuse slowing) |
| RM14 | 14 | |
| RM15 (anti-GQ1b ptosis) | 1 | |
| RM16 | 11 | |
| RP11 | 17 | |
| RP12 | 9 | |
| RP13 | 13 | brain MRI (chronic small vessel change, as stored) |
| RP14 | 13 | brain MRI (nonspecific T2 foci, no osmotic demyelination, as in history) |
| RP15 | 15 | |
| RP16 | 6 | |
| RS11 (bifacial) | 2 | |
| RS12 | 6 | |
| RS13 | 15 | EEG (moderate diffuse slowing, posterior delta) |
| RS14 | 6 | |
| RS15 (PCB) | 10 | head CT and brain MRI (chronic left PCA infarct) |
| RS16 | 27 | |
| RS17 | 22 | EEG (mild generalized slowing, as stored), brain MRI (mild small vessel change, as stored) |
| RS18 | 12 | |
| S01 | 12 | |
| S02 | 10 | |
| S03 | 11 | |
| S04 | 17 | |

The exact terms per case are in `GBS-map.yaml`; the content and reason of each report is in the
case log.

### (c) Terms left to the library on purpose

- Exceptions to `all_cases`: P01 (Miller Fisher: normal spine and nerve MRI acceptable), RM12 and
  RS15 (pharyngeal-cervical-brachial: normal gait), RM15 (anti-GQ1b ptosis only: normal gait and limbs,
  normal spine acceptable), RS11 (bifacial weakness with paraesthesias: normal gait and limbs).
- `nerve_biopsy` normal where the sural response is spared or the variant is axonal-motor: RM12, RM15,
  RS11, RS12, RS13, RS14, RS15, RP16.
- `orthostatic_blood_pressure` in ambulant patients without orthostatic symptoms: P03, RM12, RM15,
  RS11, RS15. Speech in P02 (voice normal on examination).
- Normal is the right answer for GBS: `peripheral_nerve_ultrasound` (evidence mixed), RNS, SFEMG, ice
  pack test, anti-ganglioside antibodies in AIDP, structured headache history, functional signs (P03
  included), visual fields with ptosis (RM15, P01).
- ABG in ventilated patients (RS16, RS18) and in S02 (SpO2 95%); RP14 urine osmolality and sodium
  (consistent with SIADH); beta-hCG in RM14 (22 days postpartum); ANA in PBC (RM13); lipid panel
  RS16; iron studies RM14; urinalysis on lenvatinib (RP11); RS11 brain MRI fallback (non-contrast,
  not contradictory); EEG fallbacks of RS16 and RS18 (alert patients, normal acceptable); other EEG
  types in RP14 (encephalopathy resolved).
- `device_interrogation`, `AED_levels`, valproate and lithium levels: library defects listed in (e),
  not fixed per case.

### (d) Doubts for the physicians

- SSEP: added only where large-fibre sensory loss is marked (5 cases); in every AIDP case SSEPs would
  probably be abnormal. Should all AIDP cases carry an abnormal SSEP?
- Spine MRI enhancement in every AIDP/AMAN case: frequent but not universal; some reviewers may prefer a
  normal report in early cases (P03 has subtle enhancement only).
- ABG values invented within the stored SpO2 (RS13 PaO2 66, S04 PaO2 67); S02 left normal at SpO2 95%.
- HbA1c values (RM13 7.1, RS16 7.6, RS17 7.8) chosen from diabetes on metformin and glucose levels.
- RS16 cardiac reports (LAD 90%, occluded posterolateral branch, patent RCA stent from the history;
  LGE pattern, coronary calcium score, EP study in AF) are plausible extrapolations.
- RP11 staging imaging (endometrial mass size, nodal and peritoneal disease, lung nodules) is
  extrapolated from "stage IVB, progressed after first-line chemotherapy".
- S01: stool culture left normal 2 weeks after confirmed Campylobacter (shedding may persist).

### (e) Central issues for the lead

1. `device_interrogation` library report describes a pacemaker or loop recorder in patients without a
   device (AF burden 0%); it should answer "no implanted device".
2. `exercise_stress_test` and `exercise_echo` report ~10 METs on a treadmill in patients who cannot
   walk; fixed only in RS16 (cardiac case). Every non-ambulant case in the benchmark is affected.
3. `performance_status` library reads "working" (known); `AED_levels`, valproate and lithium levels are
   therapeutic in patients not taking them (known).
4. Lab matcher: an `antiphospholipid` order in M02 is answered by the stored anti_TPO and
   anti_thyroglobulin panels (the panel-name matcher accepts the shared "anti" stem) and gets no
   antiphospholipid result. Any case storing an `anti_*` panel is exposed.
5. Lab prose: a urinalysis order in RS13 receives the clause "Arterial blood gas (room air): pH 7.41"
   because both panels have a "pH" row; a lactate order receives the whole ABG sentence.
6. Body imaging: a stored `chest_abdomen_pelvis_CT` follow-up answers `chest_CT` and
   `pelvis_abdomen_CT` orders when those have no report of their own; a `chest_CTA` order is answered
   only by a report whose `modality` is "CTA", while the library template says "CT".
7. Brain MRI and EEG fallbacks are unreachable for a plain order once an MRI or EEG follow-up exists
   (RS11, RS15, RS17, RP13); replaced anyway for consistency.

## MG

All 30 cases are disorders of neuromuscular transmission (28 myasthenia gravis, 2 Lambert-Eaton: MG-P02, MG-RM13), so the map has no exception: the two all-cases terms are justified in the LEMS cases too. 30 cases changed, 199 reports added (map verified: none of the 199 listed (case, term) orders is answered by the library), 4 case fallbacks replaced. Every case passes the perfect-agent check and the 8 case guards; no criterion answer changed.

### (a) Terms judged contradictory and why

- `performance_status` (all 30): the library reports Karnofsky 100 / ECOG 0, working, no evidence of disease. Each case got the patient's own score (KPS 20-90, ECOG 1-4) from the history and examination.
- `emg_ncs` (all 30): the library impression says there is no neuromuscular junction disorder, which routine conductions and needle EMG cannot show (no repetitive stimulation is done) and which is false here. 26 cases got normal conductions and EMG with the statement "Neuromuscular transmission was not assessed by this study (no repetitive stimulation performed)". Four cases got the abnormal conductions that their stored RNS reports already describe: vincristine axonal sensory polyneuropathy (RM11), residual demyelination after the GBS-like illness (RM12), and diffusely low CMAPs with reduced sural SNAPs in LEMS (P02, RM13).
- `emg_single_fiber`, `repetitive_nerve_stimulation`: normal jitter or no decrement where the library answers a true NMJ case (SFEMG: M04, P02, RM14, RM15, RM16; RNS: RM14, RM15).
- `ice_pack_test`: no ptosis at baseline in the library; replaced where ptosis is at rest and the test is not stored (M04, RM14).
- `clustered_AChR_cell_based`: negative in the library; positive in the 10 AChR-binding-positive cases where it is not stored.
- Thymus and mediastinum (`mediastinum_MRI`, `whole_body_FDG_PET`, `chest_xray`): the library reports a normal involuted thymus, no uptake and a normal radiograph. Replaced where the stored CT or MRI shows a thymoma, thymic hyperplasia, residual nodes, a post-thymectomy bed, lung surgery, emphysema, radiation fibrosis or aspiration change. Chest X-ray only for masses of 4 cm or more (RP11 4.4 cm, S01 4.2 cm) or a visible lung or pleural finding.
- Examination-type tests the library answers normal against the documented examination: `gait_and_balance_timed`, `levodopa_challenge` (its normal gait and arm swing), `speech_language_evaluation` (no dysarthria in bulbar MG), `orthostatic_blood_pressure`, `cognitive_screen`, `neuropsych_battery`, `functional_neuro_signs` (crisis and intubated patients; tachycardic Graves disease).
- History-driven terms: anti-thyroglobulin (autoimmune thyroiditis with raised anti-TPO), ANA (SLE; ANA 1:160 recorded in RS13), HbA1c and fasting glucose (diabetes), urine benzodiazepines (clonazepam, midazolam), ABG (the stored respiratory function report gives a gas with different values from the library's), minor salivary gland biopsy (Sjogren), polysomnography (OSA on CPAP), SSEP and neuropsychology (MS), DaTscan, MIBG, olfaction and muscle biopsy (parkinsonism, documented biopsy), spine MRI and CT (cervical spondylosis), coronary CTA and angiography (known CAD), prostate on pelvis MRI (prostate cancer on surveillance).

### (b) Per case: reports added and case fallbacks replaced

- **MG-M01** (9 reports): Karnofsky 70, ECOG 2; emg_ncs normal, transmission not assessed; clustered_AChR_cell_based: clustered AChR antibody (cell-based assay) positive; whole_body_FDG_PET: moderately FDG-avid 3.1 cm anterior mediastinal mass, no nodal, pleural or distant disease; anti_thyroglobulin: anti-thyroglobulin antibody 210 IU/mL (elevated); gait_and_balance_timed: mildly slow TUG 11.8 s and gait speed 1.02 m/s, waddling on repeated walking, balance preserved; levodopa_challenge: no parkinsonian signs and no levodopa response; mild gait and chair-rise points from proximal weakness; speech_language_evaluation: fatigable flaccid dysarthria with hypernasality after 2 minutes of speech; language normal; ABG: pH 7.43, pCO2 40, pO2 88 mmHg on room air, normal.
- **MG-M02** (7 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed; clustered_AChR_cell_based: clustered AChR antibody (cell-based assay) positive; ANA: ANA positive 1:640, homogeneous pattern; minor_salivary_gland_biopsy: focal lymphocytic sialadenitis, focus score 2 per 4 mm2; speech_language_evaluation: fatigable flaccid dysarthria with hypernasality after 2 minutes; language normal; ABG: pH 7.42, pCO2 39, pO2 90 mmHg on room air, normal.
- **MG-M03** (10 reports): Karnofsky 70, ECOG 2; emg_ncs normal, transmission not assessed; clustered_AChR_cell_based: clustered AChR antibody (cell-based assay) positive; whole_body_FDG_PET: FDG-avid 2.2 cm anterior mediastinal nodule, emphysema, no nodal or distant disease; chest_xray: hyperinflation with emphysema, normal mediastinal contour; ABG: pO2 74 mmHg (low) on room air with pH 7.40 and pCO2 44 mmHg; pelvis_abdomen_MRI: organ-confined 8 mm left peripheral zone prostate lesion with benign enlargement, no nodal or bone disease; gait_and_balance_timed: TUG 12.4 s, gait speed 0.98 m/s, waddling on prolonged walking; levodopa_challenge: no parkinsonian signs and no levodopa response; points from gait and chair rise only; speech_language_evaluation: fatigable flaccid dysarthria with hypernasality after 5 minutes; language normal.
- **MG-M04** (10 reports): Karnofsky 50, ECOG 3; emg_ncs normal, transmission not assessed; clustered_AChR_cell_based: clustered AChR antibody (cell-based assay) positive; emg_single_fiber: markedly increased jitter with blocking in EDC and frontalis; ice_pack_test: positive on the right (MRD1 +2.5 mm); HbA1c: HbA1c 7.3% (elevated); gait_and_balance_timed: TUG 21 s, gait speed 0.62 m/s, needs arm push-off to rise; levodopa_challenge: no parkinsonian signs and no levodopa response; points from gait and chair rise only; speech_language_evaluation: moderate fatigable flaccid dysarthria with hypernasality; language normal; ABG: pH 7.41, pCO2 43, pO2 82 mmHg on room air, no hypercapnia.
- **MG-P01** (4 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed; tox_screen: urine benzodiazepines positive, rest negative; speech_language_evaluation: normal at rest, mild fatigable hypernasality after 15 minutes of reading.
- **MG-P02** (8 reports): Karnofsky 60, ECOG 2; emg_ncs diffusely low CMAPs with normal conduction, reduced sural SNAPs, unstable motor units without denervation; emg_single_fiber: markedly increased jitter and blocking improving at higher stimulation rate; whole_body_FDG_PET: FDG-avid left hilar node (SUVmax 8.4), post-surgical staple-line uptake, no distant lesion; chest_xray: post right upper lobectomy changes and emphysema, no mass; gait_and_balance_timed: TUG 16.5 s, gait speed 0.78 m/s, wide-based, Berg 45/56; levodopa_challenge: no parkinsonian signs and no levodopa response; points from gait and chair rise only; speech_language_evaluation: mild fatigable dysarthria after 5 minutes; language normal.
- **MG-P03** (9 reports): Karnofsky 70, ECOG 2; emg_ncs normal, transmission not assessed; mediastinum_MRI: 2.8 cm solid anterior mediastinal mass without signal loss, thymoma most likely; whole_body_FDG_PET: moderately FDG-avid 2.8 cm anterior mediastinal mass; gait_and_balance_timed: mild right spastic-ataxic gait, gait speed 0.95 m/s, impaired tandem; levodopa_challenge: no parkinsonian signs and no levodopa response; spastic right-sided gait unchanged; ssep: prolonged central conduction of the right median and tibial SSEPs; cognitive_screen: MoCA 26/30 with reduced fluency and attention, recall intact; neuropsych_battery: reduced processing speed with preserved memory, language and visuospatial function.
- **MG-P04** (4 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed; polysomnography: moderate obstructive sleep apnoea off CPAP, controlled on CPAP, no hypoventilation; speech_language_evaluation: mild fatigable dysarthria from count 35; language normal.
- **MG-RM11** (8 reports): Karnofsky 60, ECOG 2; emg_ncs length-dependent sensory axonal polyneuropathy with mild distal reinnervation, transmission not assessed; clustered_AChR_cell_based: clustered AChR antibody (cell-based assay) positive; mediastinum_MRI: fatty involuted thymus and 1.3 cm residual paratracheal/subcarinal nodal tissue; whole_body_FDG_PET: residual mediastinal nodal tissue Deauville 3, diffuse reactive marrow uptake; gait_and_balance_timed: broad-based steppage gait, Romberg positive, gait speed 0.94 m/s; levodopa_challenge: no parkinsonian signs and no levodopa response; points from gait and chair rise only; speech_language_evaluation: fatigable hypernasal dysarthria from count 30; language normal.
- **MG-RM12** (8 reports): Karnofsky 70, ECOG 2; emg_ncs mild residual demyelinating features improving since the earlier study, transmission not assessed; clustered_AChR_cell_based: clustered AChR antibody (cell-based assay) positive; mediastinum_MRI: thymic hyperplasia with uniform chemical-shift signal loss; whole_body_FDG_PET: mild diffuse thymic uptake (SUVmax 2.6), hyperplasia pattern; gait_and_balance_timed: mildly wide-based gait, TUG 11.4 s, Berg 52/56; levodopa_challenge: no parkinsonian signs and no levodopa response; points from gait and chair rise only; speech_language_evaluation: fatigable hypernasal dysarthria after 3 minutes; language normal; case fallback replaced `fallback_tool_outputs.csf`: protein 62 mg/dL with 1 cell/uL (albuminocytological dissociation) in place of a normal CSF.
- **MG-RM13** (8 reports): Karnofsky 60, ECOG 2; emg_ncs diffusely low CMAPs with normal conduction, reduced sural SNAPs, unstable motor units without denervation; mediastinum_MRI: 0.9 cm paratracheal node with restricted diffusion and post-radiation fibrosis; whole_body_FDG_PET: FDG-avid paratracheal node (SUVmax 6.8), post-radiation uptake, no distant disease; chest_xray: right paramediastinal post-radiation fibrosis; gait_and_balance_timed: TUG 17.2 s, gait speed 0.77 m/s, mildly wide-based; levodopa_challenge: no parkinsonian signs and no levodopa response; points from gait and chair rise only; speech_language_evaluation: mild fatigable hypernasality after 10 minutes; language normal.
- **MG-RM14** (9 reports): Karnofsky 20, ECOG 4; emg_ncs normal, transmission not assessed; emg_single_fiber: severely increased jitter with frequent blocking in EDC and frontalis; repetitive_nerve_stimulation: decrement 34% nasalis, 29% trapezius, 16% ADM; ice_pack_test: positive bilaterally (MRD1 +2.5 mm); gait_and_balance_timed: not performed, unable to stand safely; levodopa_challenge: not performed, oral challenge unsafe in crisis; speech_language_evaluation: severe flaccid dysarthria, barely intelligible; language normal; orthostatic_blood_pressure: not performed, unable to stand; supine 158/96, HR 118; case fallback replaced `fallback_tool_outputs.cardiac_monitoring`: persistent sinus tachycardia (mean 108, minimum 92, maximum 132 bpm) without arrhythmia, in place of a normal sinus rhythm with minimum 49 bpm.
- **MG-RM15** (14 reports): Karnofsky 20, ECOG 4; emg_ncs normal, transmission not assessed; emg_single_fiber: increased jitter with blocking in orbicularis oculi (stimulated); repetitive_nerve_stimulation: decrement 21% nasalis, 9% trapezius, 4% ADM, train-of-four 1.0; mediastinum_MRI: post-thymectomy mediastinum without residual tissue; right apical collapse; whole_body_FDG_PET: inflammatory uptake in the collapsed right upper lobe segment, empty thymic bed; tox_screen: urine benzodiazepines positive (midazolam given at intubation), rest negative; gait_and_balance_timed: not performed, intubated and sedated; levodopa_challenge: not performed, intubated and sedated; speech_language_evaluation: not assessable (intubated and sedated); orthostatic_blood_pressure: not performed, intubated; supine 124/78, HR 88; cognitive_screen: not testable, sedated; neuropsych_battery: not performed, sedated; functional_neuro_signs: not assessable, sedated; case fallback replaced `fallback_tool_outputs.eeg`: diffuse slowing with excess frontal beta, consistent with sedation, without epileptiform discharges, in place of a normal awake EEG.
- **MG-RM16** (7 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed; clustered_AChR_cell_based: clustered AChR antibody (cell-based assay) positive; whole_body_FDG_PET: mild thymic uptake (hyperplasia pattern) and diffuse thyroid uptake; speech_language_evaluation: fatigable hypernasality after 3 minutes; language normal; orthostatic_blood_pressure: no orthostatic hypotension; resting HR 100 rising to 112; case fallback replaced `fallback_tool_outputs.mri`: bilateral extraocular muscle belly enlargement (inferior and medial recti, right greater than left) with tendon sparing and proptosis, in place of a normal brain MRI; emg_single_fiber: increased jitter with blocking in frontalis, mild in EDC.
- **MG-RP11** (8 reports): Karnofsky 60, ECOG 2; emg_ncs normal, transmission not assessed; clustered_AChR_cell_based: clustered AChR antibody (cell-based assay) positive; mediastinum_MRI: 4.4 cm solid anterior mediastinal mass without invasion, thymoma most likely; whole_body_FDG_PET: moderately FDG-avid 4.4 cm anterior mediastinal mass, no nodal or distant disease; chest_xray: oval anterior mediastinal mass over the right heart border; ABG: pO2 76 mmHg on room air, normal pH and pCO2; speech_language_evaluation: fatigable hypernasality after 2 minutes; language normal.
- **MG-RP12** (13 reports): Karnofsky 50, ECOG 3; emg_ncs normal, transmission not assessed; clustered_AChR_cell_based: clustered AChR antibody (cell-based assay) positive; whole_body_FDG_PET: no recurrence; mild inflammatory bibasal uptake from aspiration; chest_xray: post-lobectomy changes and patchy bilateral lower-zone opacities; gait_and_balance_timed: parkinsonian shuffling gait, Berg 36/56, freezing at the turn; levodopa_challenge: MDS-UPDRS III 32 to 19 (41%), bulbar signs unchanged; speech_language_evaluation: hypophonic and fatigable hypernasal dysarthria; language normal; cognitive_screen: MMSE 26/30; neuropsych_battery: attention-executive and visuospatial mild cognitive impairment; DaTscan: abnormal, asymmetric putaminal loss; MIBG_scan: reduced heart-to-mediastinum ratio (1.3); olfactory_test: severe hyposmia (UPSIT 19/40).
- **MG-RP13** (6 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed; clustered_AChR_cell_based: clustered AChR antibody (cell-based assay) positive; gait_and_balance_timed: normal short tests; reduced endurance (6-minute walk 380 m with a stop); speech_language_evaluation: fatigable hypernasality after 2 minutes; language normal; glucose: fasting glucose 138 mg/dL (elevated).
- **MG-RP14** (3 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed; speech_language_evaluation: fatigable hypernasal dysarthria; language normal.
- **MG-RS11** (2 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed.
- **MG-RS12** (3 reports): Karnofsky 70, ECOG 2; emg_ncs normal, transmission not assessed; speech_language_evaluation: fatigable hypernasal dysarthria after 2 minutes; language normal.
- **MG-RS13** (5 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed; anti_thyroglobulin: anti-thyroglobulin antibody 145 IU/mL (elevated); ANA: ANA positive 1:160, homogeneous pattern; speech_language_evaluation: fatigable hypernasal dysarthria after 3 minutes; language normal.
- **MG-RS14** (9 reports): Karnofsky 40, ECOG 3; emg_ncs normal, transmission not assessed; gait_and_balance_timed: festinating gait with freezing, TUG 24.5 s, Berg 38/56; levodopa_challenge: MDS-UPDRS III 41 to 35 (15%), axial and bulbar signs unchanged; speech_language_evaluation: severe mixed flaccid-hypokinetic dysarthria; language normal; cognitive_screen: MoCA 23/30 with executive deficits, limited by dysarthria; neuropsych_battery: mild dysexecutive profile; DaTscan: abnormal, asymmetric putaminal loss; muscle_biopsy: type I and II fibre atrophy, normal COX and SDH.
- **MG-RS15** (3 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed; speech_language_evaluation: fatigable hypophonia with volume decrement on sustained phonation; language normal.
- **MG-RS16** (10 reports): Karnofsky 60, ECOG 2; emg_ncs normal, transmission not assessed; gait_and_balance_timed: mildly shuffling gait with head drop, TUG 12.6 s; levodopa_challenge: MDS-UPDRS III 18 to 14 (22%), equivocal; head drop unchanged; speech_language_evaluation: mild fatigable dysphonia; language normal; glucose: fasting glucose 136 mg/dL (elevated); spine_MRI: mild cervical spondylosis without cord compression; spine_CT: mild cervical spondylosis without canal stenosis; coronary_CTA: moderate proximal LAD stenosis, calcium score 420, CAD-RADS 3; coronary_angiography: 60% proximal LAD and 30% RCA stenoses.
- **MG-RS17** (3 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed; speech_language_evaluation: fatigable hypernasal dysarthria after 3 minutes; language normal.
- **MG-S01** (5 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed; speech_language_evaluation: fatigable hypernasal dysarthria after 3 minutes; language normal; chest_xray: anterior mediastinal mass on the lateral view; whole_body_FDG_PET: moderately FDG-avid 4.2 cm anterior mediastinal mass.
- **MG-S02** (3 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed; speech_language_evaluation: fatigable hypernasal dysarthria after 3 minutes; language normal.
- **MG-S03** (5 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed; anti_thyroglobulin: anti-thyroglobulin antibody 96 IU/mL (elevated); speech_language_evaluation: fatigable hypernasal dysarthria after 3 minutes; language normal; whole_body_FDG_PET: moderately FDG-avid 3.6 cm anterior mediastinal mass.
- **MG-S04** (4 reports): Karnofsky 80, ECOG 1; emg_ncs normal, transmission not assessed; gait_and_balance_timed: normal short tests; waddling after 200 m on the 6-minute walk; speech_language_evaluation: fatigable hypernasal dysarthria after 3 minutes; language normal.
- **MG-S05** (2 reports): Karnofsky 90, ECOG 1; emg_ncs normal, transmission not assessed.

Case fallbacks replaced (discriminator kept): MG-RM12 `csf` (protein 62 mg/dL with 1 cell, 4 weeks after the illness whose CSF had protein 58); MG-RM14 `cardiac_monitoring` holter_24h (persistent sinus tachycardia, mean 108, minimum 92); MG-RM15 `eeg` routine (diffuse slowing with sedation beta, abnormal); MG-RM16 `mri` (extraocular muscle belly enlargement with tendon sparing and proptosis). In MG-RP11 and MG-S01, the radiograph sentence recommending CT was moved from the impression into `recommended_actions` after the first pass.

### (c) Terms left to the library on purpose

- Ice pack test without ptosis at rest: P02, RM13 (ptosis only after 80 s of upgaze), RM15, RP12, RS14, RS15, RS16. A negative test is what these patients would show.
- Mediastinum MRI and whole-body PET where the thymus is fatty or involuted and the chest is normal (M02, M04, P01, P04, RM14, RP13, RP14, RS11-RS17, S02, S04, S05). Mediastinum MRI where it is already stored (RM16, S01, S03).
- Chest X-ray for anterior mediastinal masses under 4 cm (M01 3.1 cm, M03 2.2 cm, P03 2.8 cm, S03 3.6 cm); a normal radiograph is plausible at that size.
- Clustered AChR in LEMS (P02, RM13) and in AChR-negative cases where the cell-based assay is stored; MuSK negative in AChR-positive cases.
- Respiratory function normal in P02, RM13 and S05 (no breathing symptoms, normal SpO2).
- ABG in cases without a stored gas and without respiratory compromise; RM11 (its stored report says the ABG is in range).
- Gait and levodopa in patients whose casual gait is normal and who waddle only on prolonged walking (S01, S02, S03, RS17, RP11, RP14): the short timed tests are plausibly normal.
- Anti-TPO in unspecified hypothyroidism (RM13, RM14); anti-thyroglobulin in S02 and RM16; RF and anti-SSB in M02; lipid panels on statins.
- NSE in SCLC (P02, RM13); RM11 cervical lymph node biopsy (reactive is plausible) and RM11 abdomen CT; M03 pelvis CT.
- P03 CT head, VEP, BAEP and spine MRI (normal is possible in MS without visual, brainstem or cord relapse).
- RS14 MIBG and olfaction; RS16 DaTscan.
- Normal TTE despite LVH by ECG voltage (RP12, RS11, RS12, RS16); normal muscle biopsy in RP13 (consistent with MG); functional signs normal in P01; RM11 cognitive screen.

### (d) Doubts for the physicians

1. Clustered AChR cell-based assay reported positive in every AChR-binding-positive case: the assay is rarely sent when the binding assay is positive; accept positive as the realistic answer?
2. Anti-TPO in RM13 and RM14 (hypothyroidism of unstated cause) and anti-thyroglobulin in S02 and RM16 left negative: should autoimmune thyroid disease be assumed?
3. NSE in the two SCLC cases (P02, RM13) left normal; it is often raised in SCLC.
4. P03 (MS on natalizumab): VEP, BAEP, spine MRI and CT head left normal; only SSEP was made abnormal from the right hemiparesis. Should a chronic cord lesion be on spine MRI?
5. RS14 (MuSK MG with parkinsonism): MIBG and olfaction left normal, DaTscan made abnormal. RS16: DaTscan left normal although parkinsonian signs are documented. Is the parkinsonism in these two cases degenerative?
6. RM11 cervical lymph node biopsy left reactive in active T-cell lymphoma.
7. Performance status: Karnofsky and ECOG pairs chosen from the narrative (e.g. RS14 KPS 40 / ECOG 3 on NG feeding; S05 KPS 90 / ECOG 1 in ocular MG). Please confirm.
8. RM14 and RM15 (crisis): SFEMG and RNS answered abnormal although they are waste in crisis per the plan; the answer is what the test would show, not an endorsement.
9. RS16 coronary CTA and angiography values (calcium 420, 60% proximal LAD) are written from "CAD managed conservatively" only.
10. M04 ABG: the stored gas has HCO3 27 mmol/L, just above the library range 22-26; the new panel flags it high, while the stored respiratory report calls the gas normal.

### (e) Central issues for the lead

- The library `emg_ncs` impression concludes "no neuromuscular junction disorder" without repetitive stimulation. It should say transmission was not assessed; fixed per case in all 30 MG cases, but it affects every NMJ case in the benchmark.
- The library `performance_status` says KPS 100 / ECOG 0, working, for every patient; every case of every condition needs its own score.
- AED, valproate and lithium levels are reported therapeutic for every patient (not touched here; no MG case takes these drugs).
- The library answers examination tests normal (gait, levodopa challenge, speech, cognitive screen, neuropsychology, functional signs, orthostatic BP) even for intubated, sedated or crisis patients. MG-RM14 and MG-RM15 needed "not testable" reports; a library "not assessable when sedated" rule would cover all ICU cases.
- The library `pelvis_abdomen_MRI` template reads as a female pelvis, with no prostate (seen in MG-M03, a man).
- The library ABG differs numerically from blood gases already written into stored respiratory function reports (MG-M01-M04 fixed). Other conditions with stored gases inside spirometry reports will show the same problem.
- Library `whole_body_FDG_PET` and `FDG_PET` are separate terms. Cases whose stored PET is FDG_PET answer whole_body_FDG_PET from the library unless both are stored (done here for RP11, S01, S03, RM13).

## NPH

All 30 cases changed: 228 case-specific reports stored, 1 case fallback replaced (NPH-M09 EEG), 230 orders in
`NPH-map.yaml` (two chest-abdomen-pelvis CT orders are answered by the abdomen-pelvis or chest CT report
stored in this pass, see (b)). Every case: perfect agent pass, `test_case_guards -k NPH` 240 passed,
`case_io.py check` clean (6529 passed), criterion snapshots unchanged, and the baseline gait, post-tap
reassessment, cognitive screen, CSF, MRI, CBC and TTE orders still receive the same report. A probe of
all 332 terms before (git HEAD) and after shows no other order whose answer changed. No criterion's
answer would have changed. The new clinical assessments leave `timing` empty and route by
`assessment_type`, so the baseline gait and the post-tap reassessment orders are not captured.

### (a) Terms judged contradictory

Condition-wide (`all_cases`, no `except`):
- `performance_status`: the library says Karnofsky 100 / ECOG 0, working. Every patient is a retired,
  symptomatic inpatient with falls and a walking aid or assistance: KPS 50 to 70, ECOG 2 to 3 from
  the HPI and social history.
- `levodopa_challenge`: the library describes a normal motor examination and gait. Each report gives
  the patient's MDS-UPDRS III (14 to 28, mainly gait, freezing and postural items) with a 4% to 8%
  change and gait unchanged. PD copathology (M05, P02): partial response limited to tremor,
  rigidity and limb bradykinesia (M05 16%, which fits the "minimal response" in the exam; P02 32%),
  with gait and freezing unchanged. P07 (iNPH with a prior PSP label): no response.
- `neuropsych_battery`: the library reports normal cognition. 29 reports (P09 already had one):
  frontal-subcortical profile whose severity follows the stored MoCA (mild for 21 to 23, moderate for
  17 to 20); PD copathology with prominent visuospatial involvement (M05, P02); P01 (AD
  copathology, A+T+) amnestic with impaired recognition, matching its stored screen; P04 (bvFTD)
  severe behavioural-dysexecutive. Language matches the exam where word-finding is impaired.
- `exercise_stress_test` and `exercise_echo` (added to the lead's list): the library describes a
  9.5-minute Bruce protocol at 10.4 METs (echo 9.5 METs). Every patient has a magnetic gait with
  falls, most with an aid. Each now shows a submaximal, non-diagnostic modified-Naughton test
  stopped at 2.3 METs for gait unsteadiness, or "not performed" when walking needs assistance or
  TUG is 34 s or more (M05, M09, P01, P03, P04, P07, S06, S09). The resting echo matches each
  case's stored TTE.

Per case (rule 2 history and medications, rule 3 stored findings):
- Prior focal brain lesion fixes related brain studies: M03 (chronic left precentral and corona
  radiata infarct with Wallerian degeneration) DTI, FDG-PET, perfusion SPECT, perfusion MRI, CT
  perfusion, fMRI, plus SSEP (right hemibody sensory loss); M09 (diffuse axonal injury,
  microhaemorrhages, right frontal encephalomalacia) DTI, FDG-PET, perfusion SPECT.
- Copathology evidence: P01 tau PET (CSF A+T+) and perfusion SPECT (stored temporoparietal FDG
  pattern); P04 perfusion SPECT (stored frontal and anterior temporal FDG pattern); M05 and P02
  cardiac MIBG and smell test (PD with an abnormal stored DaTscan).
- Spine and nerve: spine CT where the stored spine MRI or the history is abnormal (M04 C5-C6
  discectomy, M07 lumbar lateral recess stenosis, M10 L4-L5 stenosis, P03 C3-C6 fusion); EMG/NCS
  where the exam or history documents radiculopathy, neuropathy or anterior horn involvement (M04
  right C6, M07 diabetic polyneuropathy, M10 L5 per the history's EMG, P03 C5-C6); M07 skin biopsy
  and tibial SSEP (distal sensory loss, absent ankle reflexes); P03 SSEP (cord signal change,
  posterior column signs).
- Speech: 11 cases whose exam documents dysarthria, hypophonia, word-finding difficulty, anomia,
  perseverative or slowed speech (M02, M03, M04, M05, M06, M10, P01, P04, S02, S08, S11).
- Echo variants: TEE and bubble study wherever the stored TTE is not normal (LA enlargement, aortic
  sclerosis, MAC: M09, M10, P08, P09, S01, S04, S06, S11).
- History: M09 HbA1c (diabetes on metformin; the only diabetic case without a stored HbA1c); M07
  homocysteine (stored raised MMA with low-normal B12); M08 cirrhosis (abdominal ultrasound, CT, MRI,
  the chest-abdomen-pelvis CT, MR spectroscopy with low myo-inositol and choline and raised Glx,
  peripheral smear for platelets 88); BPH or prostate disease (M01, S02, P07 pelvis ultrasound
  showing an enlarged prostate); P05 coiled right PCOM aneurysm (catheter and MR angiography); S06
  CABG for CAD (chest X-ray, chest CT, chest CTA, mediastinum CT and MRI, coronary CTA and
  angiography, cardiac MRI with a small non-transmural inferior scar); S07 OSA on CPAP
  (polysomnography without CPAP: moderate OSA).
- Orthostatic BP where the exam records the pressures (P02, P08, S11): the report now gives the
  patient's own values.

### (b) Per case

- NPH-M01 (6): core 5/5; plus pelvis_abdomen_ultrasound
- NPH-M02 (6): core 5/5; plus speech_language_evaluation
- NPH-M03 (13): core 5/5; plus DTI_tractography, FDG_PET, perfusion_SPECT, perfusion_MRI, CT_perfusion, functional_MRI, ssep, speech_language_evaluation
- NPH-M04 (8): core 5/5; plus speech_language_evaluation, emg_ncs, spine_CT
- NPH-M05 (8): core 5/5 (levodopa: partial limb-sign response); plus MIBG_scan, olfactory_test, speech_language_evaluation
- NPH-M06 (6): core 5/5; plus speech_language_evaluation
- NPH-M07 (10): core 5/5; plus emg_ncs, skin_biopsy_iencf, ssep, homocysteine, spine_CT
- NPH-M08 (11): core 5/5; plus pelvis_abdomen_ultrasound, pelvis_abdomen_CT, pelvis_abdomen_MRI, MR_spectroscopy, peripheral smear; chest_abdomen_pelvis_CT is answered by the stored abdomen-pelvis CT (region routing), so no separate report
- NPH-M09 (11): core 5/5; plus HbA1c, DTI_tractography, FDG_PET, perfusion_SPECT, TEE, bubble_study. **Case fallback replaced:** `fallback_tool_outputs.eeg` was classified normal with a normal background yet its impression described diffuse slowing; it is now consistently an abnormal EEG with mild diffuse slowing (PDR 7.5 to 8 Hz, intermittent theta), which fits severe TBI with DAI
- NPH-M10 (10): core 5/5; plus TEE, bubble_study, speech_language_evaluation, emg_ncs, spine_CT
- NPH-P01 (8): core 5/5; plus tau_PET, perfusion_SPECT, speech_language_evaluation
- NPH-P02 (8): core 5/5 (levodopa: partial limb-sign response); plus MIBG_scan, olfactory_test, orthostatic_blood_pressure
- NPH-P03 (8): core 5/5; plus spine_CT, ssep, emg_ncs
- NPH-P04 (7): core 5/5; plus perfusion_SPECT, speech_language_evaluation
- NPH-P05 (7): core 5/5; plus cerebral_angiography, MR_angiography
- NPH-P06 (5): core 5/5
- NPH-P07 (6): core 5/5; plus pelvis_abdomen_ultrasound
- NPH-P08 (8): core 5/5; plus TEE, bubble_study, orthostatic_blood_pressure
- NPH-P09 (6): core 4/5 (neuropsych battery already stored); plus TEE, bubble_study
- NPH-S01 (7): core 5/5; plus TEE, bubble_study
- NPH-S02 (7): core 5/5; plus pelvis_abdomen_ultrasound, speech_language_evaluation
- NPH-S03 (5), NPH-S05 (5), NPH-S09 (5), NPH-S10 (5): core 5/5
- NPH-S04 (7): core 5/5; plus TEE, bubble_study
- NPH-S06 (16): core 5/5; plus TEE, bubble_study, chest_xray, chest_CT, chest_CTA, mediastinum_CT, mediastinum_MRI, coronary_CTA, coronary_angiography, cardiac_MRI; chest_abdomen_pelvis_CT is answered by the stored chest CT
- NPH-S07 (6): core 5/5; plus polysomnography
- NPH-S08 (6): core 5/5; plus speech_language_evaluation
- NPH-S11 (9): core 5/5; plus TEE, bubble_study, orthostatic_blood_pressure, speech_language_evaluation

Storage: the first report of a tool went into the empty case-fallback slot, the others into
follow-ups whose trigger names the study (`request_<term>`); labs into `fallback_tool_outputs.labs`.

### (c) Left to the library on purpose (consistent with the case)

- DaTscan, MIBG, smell test in the non-PD cases; DaTscan normal in P07, consistent with iNPH and its
  disproved PSP label. Amyloid PET, tau PET and FDG-PET normal in P09: consistent with its stored A-T-
  CSF (an AD mimic). Amyloid PET in P04 (bvFTD) negative.
- Labs: lipid panel on statins (treated); coagulation in M06 and S10 on a DOAC (held before the tap;
  the stored M03 coagulation is normal too); CDT in M08 (abstinent 5 years); hepatitis serologies and
  AFP in M08 (alcohol-related, no lesion); anti-TPO in M04 and S08 (hypothyroidism of unstated
  cause); PTH and phosphate in S09 (CKD stage 2); genetic panels (PD in M05 with a father with PD,
  FTD in P04 with a possibly affected father, early-onset AD): normal is plausible and not decidable.
- Holter, ECG and event monitors in paroxysmal AF (M03, M06, S10): the stored sinus-rhythm reports
  are consistent; a longer monitor gets the stored Holter by tier routing.
- Carotid duplex and MRA in M03 (prior MCA stroke in a patient with AF) and S06 (CAD): plaque
  is likely but not certain; normal kept.
- EEG fallbacks "normal awake and drowsy" in alert patients (kept everywhere except the M09 fix);
  CT and TTE fallbacks match the MRI and history.
- Whole-body FDG-PET and chest CT in P06 (breast cancer in remission 6 years); pelvis ultrasound in
  P06 on tamoxifen; prostate MRI in P07 (Gleason 6 on surveillance).
- Brain DTI, FDG-PET, perfusion SPECT and MRS in the other 28 cases (see (e)).

### (d) Doubts for the physicians

- Exercise testing: is a modified-Naughton treadmill to about 2.3 METs a realistic report for these
  gait disorders, or should every case say "not performed"?
- KPS/ECOG from the history (no formal scoring stored): KPS 50 for M09, P01, P04, S06, S09 and 70 for
  M01, M04, M10, S04, S07, S11; the rest 60.
- Levodopa responses invented within the case's constraints (M05 16%, P02 32%); P02's challenge
  withdraws pramipexole overnight.
- S06 coronary anatomy (native three-vessel disease, patent arterial and venous grafts, small
  inferior subendocardial scar) and M08 imaging (splenomegaly 14 cm, varices on CT) are plausible
  details that the case does not state.
- M10 EMG written as mild chronic bilateral L5 radiculopathy from the history's "mild L4-L5
  radiculopathy" (side not stated). P03 EMG: chronic C5-C6 neurogenic changes with an upper motor
  neuron recruitment pattern in the hands.
- P07 prostate size on finasteride (46 mL) and M01/S02 volumes are assumptions.

### (e) Central issues for the lead

- The library's `device_interrogation` report describes a pacemaker's stored diagnostics in every
  patient; no NPH patient has a device. Same class as AED/lithium levels and "working" in
  performance status.
- The library DTI report says the corticospinal tracts are "not displaced"; in iNPH (Evans 0.31 to
  0.42 in these cases) periventricular tracts are stretched and FA in the corticospinal tract is
  altered. Brain FDG-PET and perfusion SPECT in iNPH often show reduced frontal/periventricular
  metabolism or perfusion (and convexity relative hyperperfusion with DESH). Left to the library
  outside M03 and M09; a condition-wide decision is needed.
- Library treadmill reports (exercise test, exercise echo) assume a normal gait: they contradict
  every gait-disorder condition (NPH, PD, MSA, ataxias, GBS, myelopathy). NPH is fixed per case; the
  other conditions may need the same.
- The library `chest_CTA` report carries modality "CT", so a stored chest CT and a CTA can only be
  told apart when the case report says "CTA". A `chest_abdomen_pelvis_CT` order is answered by any
  stored chest or abdomen-pelvis CT through region overlap (M08, S06): consistent here, but partial.
- The library audiogram (10 to 20 dB HL to 8 kHz) is not age-appropriate for patients of 64 to 80;
  not a contradiction of any stated finding, so not changed.

## SYNC-CARD

30 cases, all changed: 210 case-specific reports added, 0 case fallbacks replaced. No initial output, follow-up, criterion or diagnosis was edited; every case was snapshotted before and after (criteria answers unchanged), passes the perfect-agent check and the 8 case guards, and the map script finds no listed (case, term) still answered by the library. `test_guidance_claims.py` passes (no assay added to any criterion). Logs: `data/review/round-2026-10/logs/SYNC-CARD-*.md`, section "Library contradictions (25 Oct 2026)".

### (a) Terms judged contradictory, and why

Condition-wide (every case, in `all_cases`):
- `perform_clinical_assessment {assessment_type: performance_status}`: the library returns Karnofsky 100, "no complaints", working, in patients with syncope, palpitations, exertional dyspnoea or heart failure, most of them retired. Each case now gets Karnofsky/ECOG from its own history (timing "").
- `order_specialized_test {test_type: exercise_stress_test}`, `{test_type: tilt_table}`, `order_echocardiogram {echo_type: exercise_echo}`: the library answers with a generic patient (resting 118/74 mmHg, HR 68, 9.5-10.4 METs, 90% of predicted HR, normal ECG). In this condition the rhythm is the diagnosis (complete heart block, 2:1 block, flutter with 1:1 conduction, pre-excitation, VT), so a generic normal study at sinus rates contradicts the case. Where the case already stores the exercise test, the exercise echo repeats it (rates, workload, arrhythmia) with the TTE's chambers, valves, EF and wall motion; where the case stores "not performed", the exercise echo is "not performed" too; tilt is a negative passive tilt at the patient's own rates. In cases where exercise or tilt would be harmful (HCM with obstruction, severe or symptomatic AS, obstructing RV mass, febrile Brugada, torsades) the report is "not performed, deferred by the clinical team" or names the contraindication.

Per case (in `cases`), by rule:
- TEE and bubble study (23 cases): rule 3, whenever the stored TTE is abnormal (reduced EF, LVH, regional wall motion, valve disease, dilated atria) the library's normal heart contradicts it; the new reports copy the TTE's chambers, valves, EF and wall motion.
- Coronary CTA and coronary angiography (9 and 8): rule 2, known coronary disease, stents or CABG (patent grafts, native disease, calcium score) against the library's normal coronaries and calcium score 0.
- Cardiac MRI (5 added; the others are stored): rule 3, structural disease on the TTE (ischaemic scar, RV dilatation, AS fibrosis, LVH, dilated atria) against the library's normal MRI.
- Chest X-ray, chest CT, chest CTA: rule 2, sternotomy and graft clips after CABG, cardiomegaly in a dilated LV, lung or mediastinal disease in the history.
- EMG/NCS (9): rule 2, diabetic length-dependent neuropathy on examination (reduced vibration, Achilles 1+).
- Polysomnography (6): rule 2, known obstructive sleep apnoea.
- Labs: HbA1c in diabetes where not stored (3), PTH in CKD 3b (4), serum osmolality with stored hyponatraemia (3), iron studies and smear with microcytosis (2), tox screen with benzodiazepines or opioids on the medication list (2), ABG, lipid panel, beta-hCG, prolactin.
- Audiometry (3), timed gait (4), cognitive screen, speech and language evaluation: findings recorded on the case's examination (presbycusis, cane, antalgic gait, tandem with side-step).
- Body imaging after nephrectomy (RS02: chest-abdomen-pelvis CT, abdomen CT, MRI, ultrasound), tissue diagnosis (RM01 SCLC node biopsy, RP02 myxoma resection), FDG-PET (RM02 cardiac, RP02 and RP05 whole body), mediastinum MRI, microbiology (sputum, throat swab), respiratory function.

### (b) Per case: reports added (fallback slot or follow-up); case fallbacks replaced: none

- M01 (8): performance_status (Karnofsky 80, ECOG 1, exertional limitation and recurrent falls); TEE (LVEF 47% with anterior-apical hypokinesis and concentric LVH, no thrombus or shunt); bubble_study (same LV findings as the TTE, no right-to-left shunt); exercise_echo (exercise-induced 2:1 AV block with presyncope, fixed anterior-apical hypokinesis, submaximal); coronary_CTA (patent LAD stent and mild non-obstructive plaque, calcium score 412); coronary_angiography (patent LAD stent, non-obstructive disease elsewhere, LVEDP 17 mmHg); polysomnography (severe obstructive sleep apnoea, AHI 34/h, nadir SpO2 81%); emg_ncs (mild length-dependent sensorimotor axonal polyneuropathy).
- M02 (7): performance_status (Karnofsky 80, ECOG 1); TEE (low-normal LVEF 53% with mild concentric LVH, no thrombus or shunt); bubble_study (mild LVH with LVEF 53%, no right-to-left shunt); exercise_echo (exercise-induced 2:1 AV block with a 3.8 s pause and presyncope, submaximal); respiratory_function (mild fixed airflow obstruction, FEV1/FVC 0.65, FEV1 82%); emg_ncs (mild length-dependent sensory-predominant axonal polyneuropathy); [serum_osmolality] (serum osmolality 271 mOsm/kg (low)).
- M03 (8): performance_status (Karnofsky 80, ECOG 1); TEE (mild calcific aortic stenosis, concentric LVH, LVEF 52%, no thrombus or shunt); bubble_study (concentric LVH and mild AS as on the TTE, no right-to-left shunt); exercise_echo (chronotropic incompetence, 5.2 METs, Mobitz II in recovery, mild AS); coronary_CTA (non-obstructive plaque, calcium score 486, calcified aortic valve); coronary_angiography (non-obstructive coronary disease, LVEDP 16 mmHg); polysomnography (moderate obstructive sleep apnoea, AHI 27/h); emg_ncs (mild length-dependent sensory-predominant axonal polyneuropathy).
- M04 (5): performance_status (Karnofsky 80, ECOG 1); exercise_echo (not performed, deferred by the clinical team, as the stored exercise test); chest_xray (resolving right lower zone consolidation, normal heart size); chest_CT (right lower lobe consolidation in resolution, no effusion); sputum (normal flora on a specimen collected on day 5 of azithromycin).
- M05 (4): performance_status (Karnofsky 90, ECOG 0); exercise_stress_test (normal test at the patient's own rates (rest 76 bpm, 118/74 mmHg), isolated PACs in recovery); [tox_screen] (benzodiazepines positive, other classes negative); exercise_echo (normal at the patient's own rates (9.8 METs, 76 to 160 bpm)).
- P01 (7): performance_status (Karnofsky 90, ECOG 0); tilt_table (negative passive tilt at the patient's own rates (139/78 mmHg, 84 bpm)); TEE (dilated hypokinetic RV with basal free-wall bulge, normal LV); bubble_study (dilated hypokinetic RV as on the TTE, no right-to-left shunt); exercise_echo (exercise-induced sustained LBBB-morphology VT with collapse; RV dysfunction at rest); polysomnography (mild obstructive sleep apnoea, AHI 11/h); [HbA1c] (HbA1c 6.0% (elevated)).
- P02 (5): performance_status (Karnofsky 80, ECOG 1); tilt_table (not performed, deferred by the clinical team); TEE (asymmetric septal hypertrophy, SAM with posteriorly directed MR, no thrombus); bubble_study (asymmetric septal hypertrophy with SAM, no right-to-left shunt); polysomnography (moderate obstructive sleep apnoea, AHI 22/h).
- P03 (4): performance_status (Karnofsky 80, ECOG 1 during the febrile illness); exercise_stress_test (not performed, deferred by the clinical team); exercise_echo (not performed, deferred by the clinical team); throat_swab (influenza A RNA detected, group A Streptococcus negative).
- P04 (2): performance_status (Karnofsky 90, ECOG 0); exercise_echo (exercise-induced polymorphic VT with presyncope, QT not shortening, normal contractile response).
- RM01 (7): performance_status (Karnofsky 70, ECOG 1); exercise_stress_test (7.1 METs, appropriate heart rate response at the patient's own rates, no arrhythmia); speech_language_evaluation (oropharyngeal dysphagia with delayed swallow initiation, normal speech and language); chest_xray (widened right paratracheal stripe and splayed carina); lymph_node_biopsy (metastatic small cell carcinoma in the subcarinal node (EBUS-TBNA)); cognitive_screen (MoCA 27/30 (delayed recall 3/5, abstraction 1/2)); exercise_echo (reduced capacity (7.1 METs) at the patient's own rates, no ischaemia).
- RM02 (6): performance_status (Karnofsky 70, ECOG 1); TEE (rheumatic-type mitral valve with moderate MR, mild AR, no vegetation, LVEF 45%); bubble_study (LVEF 45% with rheumatic valve changes, no right-to-left shunt); exercise_echo (severe chronotropic incompetence, 2:1 AV block with a pause in recovery, limited contractile reserve); cardiac_FDG_PET (focal basal inferoseptal and inferolateral myocardial uptake, no nodal uptake); chest_xray (mild cardiomegaly with left atrial enlargement).
- RM03 (6): performance_status (Karnofsky 70, ECOG 1); TEE (LVEF 38% with anteroseptal-apical hypokinesis and thinning, no thrombus, aortic atheroma); bubble_study (LVEF 38% with regional hypokinesis, no right-to-left shunt); exercise_echo (2:1 AV block in stage 1 with presyncope, fixed regional hypokinesis); coronary_CTA (occluded mid LAD, moderate RCA stenosis, calcium score 684); coronary_angiography (chronic total occlusion of the mid LAD with collaterals, moderate RCA stenosis).
- RM04 (10): performance_status (Karnofsky 60, ECOG 2); TEE (thrombus in the proximal right pulmonary artery, RV pressure overload, no intracardiac thrombus); bubble_study (RV dilatation and dysfunction as on the TTE, no shunt at rest); exercise_echo (not performed: walker-dependent after knee arthroplasty); cardiac_MRI (dilated RV with RVEF 33% and septal flattening, normal LV); chest_xray (peripheral right basal opacity, small bilateral effusions, prominent pulmonary artery); gait_and_balance_timed (walker-dependent antalgic gait, TUG 34 s, 10 m walk not completed); [ABG] (hypoxaemia with hypocapnia on nasal oxygen, low bicarbonate, lactate 2.8); [HbA1c] (HbA1c 7.1% (elevated)); [tox_screen] (oxycodone positive, other classes negative).
- RP01 (9): performance_status (Karnofsky 80, ECOG 1); electrophysiology_study (inducible sustained monomorphic LBBB-superior-axis VT, normal AV conduction); TEE (mildly dilated RV with subtricuspid hypokinesis, normal LV); bubble_study (mild RV dilatation with regional hypokinesis, no shunt); exercise_echo (exercise-induced LBBB-superior-axis NSVT with dizziness, regional RV hypokinesis); [iron_studies] (iron deficiency pattern, ferritin 9 ng/mL); [peripheral smear] (microcytic hypochromic red cells with pencil cells); [beta-hCG] (beta-hCG 46 mIU/mL, still detectable); [prolactin] (prolactin 118 ng/mL).
- RP02 (10): performance_status (Karnofsky 80, ECOG 1); TEE (pedunculated mobile RVOT mass with severe subpulmonic obstruction, no other mass); bubble_study (RVOT mass with severe obstruction, no shunt); exercise_echo (not performed, deferred by the clinical team); chest_CT (low-attenuation RVOT filling defect with RV wall thickening, small pericardial effusion); chest_CTA (low-attenuation RVOT filling defect with RV wall thickening, small pericardial effusion); coronary_CTA (normal coronaries; RVOT mass reported as a non-coronary finding); cardiac_FDG_PET (mildly FDG-avid RVOT mass, no myocardial uptake); whole_body_FDG_PET (mildly FDG-avid RVOT mass, no extracardiac lesion); resection (cardiac myxoma, completely excised).
- RP03 (6): performance_status (Karnofsky 90, ECOG 0); tilt_table (negative passive tilt at the patient's own rates (108/68 mmHg, 78 bpm)); TEE (mild posterior mitral leaflet prolapse with trivial MR, otherwise normal); bubble_study (mild mitral prolapse, no right-to-left shunt); exercise_echo (workload-dependent ectopy escalating to bidirectional and polymorphic VT with presyncope); [peripheral smear] (microcytic hypochromic red cells with pencil cells).
- RP04 (4): performance_status (Karnofsky 80, ECOG 1); exercise_stress_test (normal at the patient's own rates (rest 62 bpm, PR 192 ms), 1:1 conduction throughout); tilt_table (negative passive tilt at the patient's own rates (122/74 mmHg, 62 bpm)); exercise_echo (normal at the patient's own rates (9.4 METs, 62 to 166 bpm), 1:1 conduction).
- RP05 (6): performance_status (Karnofsky 70, ECOG 1); TEE (basal anteroseptal hypokinesis with increased echogenicity, preserved LVEF); bubble_study (basal anteroseptal regional abnormality, no shunt); exercise_echo (persistent complete AV block, ventricular rate 40-46 bpm, stopped at 3.5 METs); whole_body_FDG_PET (intensely avid bilateral hilar and paratracheal nodes, focal septal uptake); mediastinum_MRI (symmetric bilateral hilar and right paratracheal lymphadenopathy).
- RS01 (5): performance_status (Karnofsky 80, ECOG 1); TEE (mild posterior mitral leaflet prolapse, otherwise normal); bubble_study (mild mitral prolapse, no shunt); exercise_echo (persistent complete AV block, escape 40 to 54 bpm, stopped early); [lipid_panel] (LDL 168 mg/dL, total cholesterol 246 mg/dL).
- RS02 (11): performance_status (Karnofsky 70, ECOG 2); TEE (LVEF 42% with basal inferior hypokinesis, mild AS, no thrombus); bubble_study (LVEF 42% and mild AS as on the TTE, no shunt); exercise_echo (persistent complete AV block, flat BP response, stopped early); coronary_CTA (severe mid RCA and moderate proximal LAD stenoses, calcium score 812); coronary_angiography (two-vessel disease (80% RCA, 60% LAD), LVEDP 21 mmHg); chest_abdomen_pelvis_CT (status post left nephrectomy, no recurrence, mild emphysema); pelvis_abdomen_CT (status post left nephrectomy, no recurrence); pelvis_abdomen_MRI (status post left nephrectomy, no recurrence); pelvis_abdomen_ultrasound (surgically absent left kidney, normal right kidney); [PTH] (intact PTH 96 pg/mL).
- RS03 (10): performance_status (Karnofsky 70, ECOG 1); TEE (LVEF 45% with anteroseptal hypokinesis, mild calcific AS, no thrombus); bubble_study (LVEF 45% and mild AS as on the TTE, no shunt); exercise_echo (persistent complete heart block, symptomatic hypotension at 2 minutes); coronary_CTA (patent LIMA-LAD and SVG-OM grafts, severe native LAD and circumflex disease); coronary_angiography (patent grafts, grafted severe native disease, LVEDP 19 mmHg); chest_xray (sternotomy wires and graft clips, borderline heart size); chest_CT (post-CABG and sternotomy changes, coronary and aortic valve calcification); chest_CTA (no PE, post-CABG and sternotomy changes); emg_ncs (mild length-dependent sensory-predominant axonal polyneuropathy).
- RS04 (3): performance_status (Karnofsky 90, ECOG 0); exercise_echo (pre-excitation persisting to 168 bpm, normal contractile response); tilt_table (negative passive tilt at the patient's own rates (122/78 mmHg, 72 bpm)).
- RS05 (10): performance_status (Karnofsky 70, ECOG 1); TEE (dilated LV with LVEF 32%, inferior hypokinesis, no thrombus); bubble_study (LVEF 32% with inferior hypokinesis as on the TTE, no shunt); exercise_echo (3.8 METs, NSVT in recovery, fixed inferior hypokinesis); cardiac_MRI (dilated LV, LVEF 31%, inferior and inferolateral infarct scar); coronary_CTA (patent RCA stent, non-obstructive left coronary plaque); coronary_angiography (patent RCA stent, no new obstructive disease, LVEDP 22 mmHg); chest_xray (cardiomegaly (CTR 0.56), no pulmonary oedema); tilt_table (negative passive tilt at the patient's own rates (104/62 mmHg, 92 bpm)); emg_ncs (mild length-dependent sensory-predominant axonal polyneuropathy).
- RS06 (7): performance_status (Karnofsky 80, ECOG 1); TEE (atrial flutter, no appendage thrombus, mildly dilated atria, LVEF 55%); bubble_study (dilated atria as on the TTE, no shunt); exercise_echo (1:1 flutter conduction at about 300 bpm in stage 1, stopped); polysomnography (mild obstructive sleep apnoea (AHI 11 /h), flutter with 4:1 conduction); [HbA1c] (HbA1c 6.6%); cardiac_MRI (mild biatrial enlargement, LVEF 54%, no late enhancement).
- S01 (7): performance_status (Karnofsky 70, ECOG 2); TEE (LVEF 45% with mid-anterior hypokinesis, mild LVH, no thrombus); bubble_study (LVEF 45% as on the TTE, no shunt); exercise_echo (stress phase not performed, deferred by the clinical team); coronary_CTA (patent LAD stent, non-obstructive RCA and circumflex plaque); coronary_angiography (patent LAD stent, non-obstructive RCA disease); emg_ncs (mild length-dependent sensory-predominant axonal polyneuropathy).
- S02 (7): performance_status (Karnofsky 70, ECOG 2); TEE (severe calcific AS (AVA about 0.8 cm2), LVEF 40%, no thrombus); bubble_study (severe AS and LVEF 40% as on the TTE, no shunt); exercise_echo (stress phase not performed in symptomatic severe AS with complete heart block); [PTH] (intact PTH 118 pg/mL); [iron_studies] (iron deficiency pattern, ferritin 24 ng/mL); emg_ncs (mild length-dependent sensory-predominant axonal polyneuropathy).
- S03 (14): performance_status (Karnofsky 60, ECOG 2); TEE (LVEF 35% with anterior and apical akinesis, moderate AS and MR, no thrombus); bubble_study (LVEF 35% and moderate AS as on the TTE, no shunt); exercise_echo (stress phase not performed, deferred by the clinical team); coronary_CTA (patent LIMA and two vein grafts, severe native three-vessel disease); coronary_angiography (patent grafts, grafted native three-vessel disease, LVEDP 24 mmHg); chest_xray (cardiomegaly, mild interstitial oedema, small effusions, sternotomy wires); chest_CT (cardiomegaly, mild oedema, small effusions, post-CABG changes); chest_CTA (no PE, cardiomegaly with mild oedema, post-CABG changes); polysomnography (moderate obstructive sleep apnoea (AHI 26 /h) off CPAP, complete AV block on the ECG channel); emg_ncs (moderate length-dependent sensorimotor axonal polyneuropathy); gait_and_balance_timed (slow cane-assisted gait, TUG 19.8 s, Berg 44/56); [PTH] (intact PTH 132 pg/mL); [serum_osmolality] (serum osmolality 276 mOsm/kg (low)).
- S04 (8): performance_status (Karnofsky 70, ECOG 1); TEE (severe calcific AS (AVA about 0.8 cm2), concentric LVH, LVEF 46%); bubble_study (severe AS and LVH as on the TTE, no shunt); exercise_echo (stress phase not performed in symptomatic severe AS with complete heart block); audiometry (bilateral moderate high-frequency sensorineural hearing loss); emg_ncs (mild length-dependent sensory-predominant axonal polyneuropathy); [PTH] (intact PTH 104 pg/mL); [serum_osmolality] (serum osmolality 263 mOsm/kg (low)).
- S05 (7): performance_status (Karnofsky 70, ECOG 1); TEE (severe calcific AS (AVA about 0.7 cm2), concentric LVH, LVEF 62%); bubble_study (severe AS and LVH as on the TTE, no shunt); exercise_echo (stress phase not performed in symptomatic severe AS); cardiac_MRI (severe AS with concentric LVH, patchy septal mid-wall enhancement); audiometry (bilateral mild high-frequency sensorineural hearing loss); gait_and_balance_timed (slow antalgic gait, TUG 15.6 s, tandem not completed).
- S06 (7): performance_status (Karnofsky 80, ECOG 1); TEE (mild LVH, mildly dilated LA, aortic sclerosis, no thrombus); bubble_study (mild LVH and LA dilatation as on the TTE, no shunt); exercise_echo (stress phase not performed, deferred by the clinical team); audiometry (bilateral mild high-frequency sensorineural hearing loss); gait_and_balance_timed (mildly slowed gait, TUG 12.4 s, tandem with one side-step); cardiac_MRI (mild concentric LVH, mildly dilated LA, no late enhancement).

### (c) Terms left to the library on purpose, and why

- TEE, bubble study: left where the stored TTE is normal (M04, M05, P03, P04, RP04, RS04) or where it shows only a mildly dilated LA (RM01); the library's normal heart agrees with them.
- Electrophysiology study, where not stored: M04 (acquired long QT), P02 (HCM, programmed stimulation of low yield), P03 (Brugada), P04, RM01 (the apnoea mechanism stands), RP02, RP03, RM04, S05. A normal EP study is consistent with each case.
- Cardiac MRI where the TTE is normal (M04, M05, P04, RM01).
- Chest X-ray in LVH without dilatation or lung disease (M01, M02, M03, RS02, S01, S02, S04, S05 and others); a normal radiograph is plausible.
- Coronary CTA and angiography in patients with no known coronary disease (S02, S04, S05 included, where pre-valve work-up is realistic); the library normal is plausible.
- Carotid duplex (RM03), B12 (M03), anti-TPO in treated hypothyroidism (M04, M05, RP04, S06), thrombophilia (RM04), blood cultures and throat swab in rheumatic carditis (RM02), urine sodium and osmolality (M02, S04: consistent with thiazide hyponatraemia), lipid panels in statin-treated patients, genetic panels, cardiac FDG-PET in RS01, RS02 and RS05 (no inflammatory picture), chest CT and CTA without stated lung disease.
- Device interrogation in every case without a device, and in RP04 (implantable loop recorder): see (e).
- Tilt fallbacks already stored as "Study within normal limits" or as aborted (P03, P04, RM01, RS06) were kept as they are.

### (d) Doubts for the physicians

- P03 (Brugada): an SCN5A carrier may have a prolonged HV interval; the library EP study (normal) was kept.
- RS01: the classic LMNA picture (conduction disease with family history) may deserve a positive genetic panel; RP04 and RM03 (familial conduction disease) the same question. The library panel was kept.
- RS02 (pembrolizumab): immune checkpoint myocarditis is in the differential; the library cardiac FDG-PET (no inflammation) was kept.
- M03: macrocytosis with a normal library B12.
- S01: patchy RV insertion-point enhancement on the stored MRI with a normal library cardiac FDG-PET; acceptable as non-specific?
- The Karnofsky/ECOG values are set from the history (KPS 60-90); ECOG 1 versus 2 is a judgement call in S03, S04, RS02 and RS05.
- Harm convention: tilt and exercise studies are "not performed" in HCM with obstruction, severe AS, an obstructing RV mass, febrile Brugada and torsades; elsewhere they are answered at the patient's own rates. Please confirm the line.

### (e) Central issues for the lead

- `AED_levels` in the library reports six antiseizure drugs at therapeutic levels in every patient (P04 takes levetiracetam only).
- `performance_status` library says "working" with Karnofsky 100; most syncope patients are retired and symptomatic. Fixed per case here, but it is a library default worth changing.
- `device_interrogation` library presumes a pacemaker or ICD; in a patient without a device it returns a 6-month device history. In RP04 (implantable loop recorder) it is unclear whether this is a leak or a contradiction.
- `obtain_tissue_diagnosis` library: `resection` and `open_biopsy` report normal brain tissue, `lymph_node_biopsy` a cervical node, whatever the site ordered.
- The library `chest_CTA` template carries `modality: CT`; stored CTAs use `CTA`. A case report with `modality: CT` is not routed to a chest_CTA order (fixed here by using `CTA`).
- Exercise, exercise echo and tilt library templates are a generic patient's rates (HR 68, 9.5-10.4 METs); for a rhythm-diagnosis condition they would better answer "not available" when the case has no report.
