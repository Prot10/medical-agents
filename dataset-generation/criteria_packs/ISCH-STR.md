# Criteria pack: Ischemic stroke

**ICD-10:** I63.x (by mechanism and territory)
**Condition enum:** `NeurologicalCondition.ISCHEMIC_STROKE`
**Case ID prefix:** `ISCH-STR`

---

## 1. Diagnostic criteria

AHA/ASA 2019 guidelines for early management. Clinical syndrome of acute
focal neurologic deficit + neuroimaging evidence of acute ischemia (acute
ischemic stroke = symptoms >24h OR <24h with imaging confirmation; TIA =
symptoms resolved AND imaging negative for acute infarct). NIHSS used for
severity and treatment decisions. Time of last known well (LKW) is critical
for treatment-window decisions: IV thrombolysis up to 4.5h (selected patients
up to 9h with imaging mismatch), mechanical thrombectomy for LVO up to 24h
(DAWN, DEFUSE-3 criteria). TOAST classification by mechanism:
large-artery atherosclerosis, cardioembolism, small-vessel occlusion,
stroke of other determined etiology, undetermined (cryptogenic).

## 2. Standard workup hierarchy

**Required (acute phase):**
- `order_ct_scan` (non-contrast CT head) — exclude hemorrhage prior to tPA; FIRST imaging in any stroke alert [AHA_ASA_2019]
- `order_ct_scan` (`angiography: true`) — CTA head/neck for LVO detection if presenting <24h and considering thrombectomy [AHA_ASA_2019]
- `interpret_labs` (CBC, BMP, glucose, coagulation INR/PTT, troponin) — exclude hypoglycemia mimic; rule out coagulopathy before tPA; assess cardiac comorbidity [AHA_ASA_2019]
- `analyze_ecg` (12-lead) — AFib or other rhythm cause [AHA_ASA_2019]
- `search_medical_literature` — confirm tPA criteria, thrombectomy criteria
- `check_drug_interactions` — tPA contraindications (recent anticoagulation, bleeding, surgery), bridging anticoagulation

**Required (post-acute mechanism workup):**
- `analyze_brain_mri` (with DWI) — confirms infarct, identifies multiple territories suggesting embolic source; not first-line in acute setting unless equivocal CT [AHA_ASA_2019]
- `order_echocardiogram` (`echo_type: TTE`) — cardiac source of embolism; TEE if cryptogenic and TTE non-diagnostic [AHA_ASA_2019]
- `order_cardiac_monitoring` (`monitor_type: holter_24h`, then 30-day event monitor if cryptogenic) — detect paroxysmal AF [Sanna_2014]
- `order_advanced_imaging` (`modality: carotid_duplex`) — carotid stenosis if anterior circulation stroke; alternative to CTA neck [AHA_ASA_2014]

**Recommended:**
- `order_advanced_imaging` (`modality: MR_angiography`) — alternative when CTA contraindicated (contrast allergy, renal disease)
- `order_advanced_imaging` (`modality: transcranial_doppler`) — for vasospasm, microemboli detection, sickle cell stroke risk
- `interpret_labs` (HbA1c, lipid panel, hypercoagulability if young/cryptogenic — antiphospholipid, factor V Leiden, prothrombin gene, protein C/S) — secondary prevention + cryptogenic workup

## 3. Tools that are typically USELESS

- `analyze_eeg` — not part of stroke workup unless post-stroke seizure
- `analyze_csf` — no role unless SAH or vasculitis on differential
- `order_specialized_test` (most) — not part of routine acute workup; only neuropsych in chronic phase

## 4. Tools that are HARMFUL / contraindicated

- `order_ct_scan` with contrast (CTA) — care needed in renal failure (use MRA instead) or contrast allergy
- IV tPA in active bleeding, recent surgery, recent stroke <3mo, severe HTN, recent anticoagulation (not formally a "tool" but a treatment decision)

## 5. Sequence constraints

- `order_ct_scan` (non-contrast) → IV tPA (`hard`): CT to exclude hemorrhage MUST precede thrombolytic [AHA_ASA_2019]
- `order_ct_scan` (`angiography: true`) → mechanical thrombectomy (`hard`): LVO must be documented before intervention
- Lab results → IV tPA (`soft`): coagulation results helpful but tPA not delayed for INR if no history of anticoagulation
- For LP candidates: `analyze_brain_mri` → `analyze_csf` (`hard`) if focal deficit

## 6. Subtype variations

- **M (mild):** minor stroke (NIHSS <5), small vessel; standard acute workup, modified secondary prevention workup
- **S (standard):** moderate stroke, anterior circulation, identifiable mechanism; standard acute + secondary workup
- **P (progressive / severe):** large vessel occlusion, NIHSS ≥6, candidate for thrombectomy; emergent CTA + thrombectomy pathway; comprehensive secondary workup post-acute
- **R (reverse / mimic):** stroke mimics — hypoglycemia, complicated migraine, post-ictal Todd's paralysis, conversion/FND, MS relapse, brain tumor with stroke-like onset; workup adds repeat imaging (perfusion or MRI), targeted labs, EEG if seizure suspected

## 7. Common red-herring categories

- **Normal initial CT** — early ischemic changes may be subtle; does NOT exclude stroke in symptomatic patient
- **Resolved symptoms** — TIA still requires same workup; high short-term recurrence risk (ABCD2)
- **Hypertension** — common in acute stroke (autoregulation); avoid lowering BP aggressively before tPA unless >185/110
- **Atrial fibrillation history** — does NOT prove AF is the cause; lacunar infarct may be unrelated
- **Migraine with aura** — can mimic; new-onset aura in elderly must have stroke workup

## 8. Allowed citations

- `[AHA_ASA_2019]` — Powers WJ et al. Guidelines for the early management of patients with acute ischemic stroke: 2019 update. Stroke 2019;50:e344-e418
- `[AHA_ASA_2014]` — Kernan WN et al. Guidelines for the prevention of stroke in patients with stroke and TIA. Stroke 2014;45:2160-2236
- `[DAWN_2018]` — Nogueira RG et al. Thrombectomy 6-24 hours after stroke with a mismatch between deficit and infarct. NEJM 2018;378:11-21
- `[DEFUSE3_2018]` — Albers GW et al. Thrombectomy for stroke at 6 to 16 hours with selection by perfusion imaging. NEJM 2018;378:708-718
- `[Sanna_2014]` — Sanna T et al. Cryptogenic stroke and underlying atrial fibrillation. NEJM 2014;370:2478-2486
- `[Adams_1993_TOAST]` — Adams HP et al. Classification of subtype of acute ischemic stroke: TOAST. Stroke 1993;24:35-41
