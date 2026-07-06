# Criteria pack: Focal epilepsy, temporal lobe

**ICD-10:** G40.2x9 (localization-related symptomatic focal epilepsy). Default to the *not-intractable* code (G40.209 / G40.20x); use the *intractable* code (G40.219 / G40.21x) ONLY when the case documents failure of ≥2 adequate AED trials (non-adherence and subtherapeutic dosing do not qualify).
**Condition enum:** `NeurologicalCondition.FOCAL_EPILEPSY_TEMPORAL`
**Case ID prefix:** `FEPI-TEMP`

---

## 1. Diagnostic criteria

ILAE 2017 classification: focal-onset seizures (with or without impaired
awareness) localizing to temporal lobe. Mesial TLE presents with epigastric
aura, déjà vu, fear, automatisms (oroalimentary, manual); lateral/neocortical
TLE with auditory or vertiginous aura. ILAE diagnosis of EPILEPSY requires
≥2 unprovoked seizures >24h apart OR 1 unprovoked seizure + ≥60%
recurrence risk over 10 years. Concordant EEG (interictal spikes/sharps
in anterior temporal region) + MRI lesion (hippocampal sclerosis,
DNET, ganglioglioma, cavernoma) supports symptomatic focal epilepsy.

## 2. Standard workup hierarchy

**Required:**
- `analyze_eeg` (routine; if non-diagnostic, ambulatory or video-EEG) — interictal sharps/spikes, focal slowing in anterior temporal region; long-term monitoring needed to capture ictal events [ILAE_2017]
- `analyze_brain_mri` (epilepsy protocol — thin-cut coronal T1, FLAIR, T2, DWI through hippocampi) — identify hippocampal sclerosis, low-grade tumor (DNET, ganglioglioma), cavernoma, FCD; "epilepsy protocol" critical, not standard brain MRI [AAN_2007]
- `interpret_labs` (CBC, CMP, AED levels if on therapy, prolactin if recent seizure) — baseline + exclude metabolic seizure provocation [ILAE_drug_2017]
- `search_medical_literature` — AED selection, ILAE classification
- `check_drug_interactions` — when initiating or changing AEDs (enzyme inducers vs non-inducers, drug-drug interactions)

**Recommended:**
- `analyze_eeg` (`eeg_type: video`) — long-term video-EEG for surgical candidacy or refractory cases; not routine first-line [Engel_2003]
- `order_advanced_imaging` (`modality: FDG_PET`) — hypometabolism ipsilateral to focus when MRI non-localizing, prior to epilepsy surgery [Willmann_2007]

**Optional:**
- `order_specialized_test` (`test_type: neuropsych_battery`) — memory lateralization for surgical planning

## 3. Tools that are typically USELESS

- `analyze_csf` — only if suspicion of encephalitis or first seizure in immunocompromised patient
- `analyze_ecg` — exclude convulsive syncope only if presentation atypical
- `order_echocardiogram` — only when convulsive syncope on differential
- `order_cardiac_monitoring` — same; only if syncope-vs-seizure
- `order_ct_scan` — inferior to MRI for epilepsy workup
- `order_advanced_imaging` (most modalities) — only PET useful when MRI-negative

## 4. Tools that are HARMFUL / contraindicated

(none — epilepsy workup is safe)

## 5. Sequence constraints

- `analyze_brain_mri` → AED selection (`soft`): structural cause changes AED choice (e.g., tumor → consider carbamazepine; hippocampal sclerosis → multiple options) [ILAE_drug_2017]

## 6. Subtype variations

- **M (mild):** infrequent, well-controlled seizures, normal MRI; standard workup
- **S (standard):** typical mesial TLE with hippocampal sclerosis; standard workup
- **P (progressive / refractory):** drug-resistant epilepsy (failure of ≥2 appropriate AEDs at adequate doses); add video-EEG long-term monitoring, FDG-PET, neuropsych battery — surgical evaluation pathway
- **R (reverse / mimic):** psychogenic non-epileptic spells (PNES — diagnosed by video-EEG capturing event without EEG correlate), convulsive syncope (ECG, tilt-table), cardiogenic (Holter, echo), TIA, migraine aura, paroxysmal dyskinesias

## 7. Common red-herring categories

- **Single seizure does not = epilepsy** — diagnosis requires recurrence risk OR ≥2 events
- **Normal MRI** — does not exclude TLE; 20-30% of refractory TLE has normal MRI initially; epilepsy protocol MRI catches additional lesions
- **Normal interictal EEG** — single routine EEG sensitivity ~25-50%; repeat or sleep-deprived improves yield
- **Elevated prolactin** — supports recent convulsion but normal does not exclude
- **Postictal Todd's paralysis** — mimics stroke acutely; resolves over hours

## 8. Allowed citations

- `[ILAE_2017]` — Fisher RS et al. Operational classification of seizure types by the ILAE. Epilepsia 2017;58:522-530
- `[AAN_2007]` — Krumholz A et al. Practice Parameter: Evaluating an apparent unprovoked first seizure in adults. AAN, Neurology 2007;69:1996-2007
- `[ILAE_drug_2017]` — Glauser T et al. ILAE evidence-based guideline: initial monotherapy for epileptic seizures. Epilepsia 2017;58:1235-1268
- `[Engel_2003]` — Engel J et al. Practice parameter: Temporal lobe and localized neocortical resections for epilepsy. AAN, Neurology 2003;60:538-547
- `[Willmann_2007]` — Willmann O et al. The contribution of 18F-FDG PET in preoperative epilepsy surgery evaluation. Seizure 2007;16:509-520
- `[Kwan_2010]` — Kwan P et al. Definition of drug resistant epilepsy. Epilepsia 2010;51:1069-1077
