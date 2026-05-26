# Criteria pack: Migraine with aura

**ICD-10:** G43.1x
**Condition enum:** `NeurologicalCondition.MIGRAINE_WITH_AURA`
**Case ID prefix:** `MIG-AURA`

---

## 1. Diagnostic criteria

ICHD-3 (International Classification of Headache Disorders, 3rd edition):
**1.2 Migraine with aura** — At least 2 attacks meeting B-D: (B) one or
more fully reversible aura symptoms (visual, sensory, speech/language, motor,
brainstem, retinal); (C) at least 3 of: ≥1 aura symptom spreads gradually
over ≥5 min, ≥2 aura symptoms in succession, each individual aura symptom
lasts 5-60 min, ≥1 unilateral, ≥1 positive symptom (e.g., scintillating
scotoma, paresthesias), aura accompanied/followed within 60 min by headache;
(D) not better accounted for by another ICHD-3 diagnosis, and TIA excluded.
Diagnosis is **clinical** — no diagnostic test confirms migraine.

## 2. Standard workup hierarchy

**Required:**
- `search_medical_literature` — confirm ICHD-3 criteria, exclude SNOOP/CHATS red flags
- `check_drug_interactions` — triptans, ergotamines (cardiovascular contraindications), CGRP antagonists, prophylactic medications (beta-blockers, topiramate, valproate, amitriptyline)

**Recommended (when red flags or atypical features present, otherwise OMIT imaging):**
- `analyze_brain_mri` — ONLY for SNOOP (Systemic symptoms, Neurologic deficits, sudden Onset, Onset after age 50, Pattern change); routine imaging in typical migraine is NOT indicated [AAN_2000]
- `interpret_labs` (CBC, ESR/CRP for temporal arteritis in age >50) — only when red flags
- `analyze_eeg` — only when seizure on differential; otherwise NOT indicated

**Optional:**
- `consult_medical_specialist` — neurology/headache subspecialist for refractory or atypical cases

## 3. Tools that are typically USELESS

- `analyze_brain_mri` — in typical migraine with aura matching ICHD-3, MRI is OFTEN unnecessary and over-ordered; reserve for atypical features
- `order_ct_scan` — even less indicated than MRI; MRI superior when imaging needed
- `analyze_csf` — only if SAH on differential
- `analyze_ecg` — only as baseline for triptan contraindications
- `order_echocardiogram` — controversial; bubble study sometimes done for migraine with aura + suspected PFO + cryptogenic stroke, but routine echo NOT indicated
- `order_cardiac_monitoring` — not indicated
- `order_advanced_imaging` (any) — none indicated
- `order_specialized_test` (most) — none indicated

## 4. Tools that are HARMFUL / contraindicated

(none diagnostic; treatment harms from ergotamines/triptans in vascular disease and triptans within 24h of each other)

## 5. Sequence constraints

(none)

## 6. Subtype variations

- **M (mild):** typical aura (visual scintillating scotoma) followed by headache; minimal workup
- **S (standard):** classic migraine with aura, occasional; minimal workup, abortive + lifestyle counseling
- **P (progressive / refractory):** chronic migraine (≥15 days/month), medication-overuse headache, status migrainosus; same workup + comprehensive medication review + consider neurology referral
- **R (reverse / mimic):** TIA (especially in age >50 with vascular risk factors, no associated headache, sudden onset), focal seizure with aura, AVM/cavernoma, MELAS, CADASIL, retinal artery occlusion, posterior reversible encephalopathy syndrome (PRES); workup adds MRI/MRA, vascular workup, ECG/echo for cardiac source, genetic testing for CADASIL/MELAS in family history cases

## 7. Common red-herring categories

- **First-ever migraine aura in older adult** — must exclude TIA/stroke; even classical "march" of visual symptoms isn't proof
- **Aura without headache** — possible (acephalgic migraine) but exclude TIA, especially in older adults
- **Family history of stroke** — does NOT rule in migraine; conversely CADASIL has migraine + later stroke
- **MRI white matter spots in migraineurs** — common (non-specific), increased prevalence; does not change management unless inflammatory/demyelinating features
- **PFO** — controversial association with migraine; routine bubble study not recommended

## 8. Allowed citations

- `[ICHD_3]` — Headache Classification Committee of the International Headache Society. The International Classification of Headache Disorders, 3rd edition. Cephalalgia 2018;38:1-211
- `[AAN_2000]` — Silberstein SD; AAN. Practice parameter: evidence-based guidelines for migraine headache. Neurology 2000;55:754-762
- `[Charles_2017]` — Charles A. The pathophysiology of migraine: implications for clinical management. Lancet Neurol 2018;17:174-182
- `[Holland_2012]` — Holland S, Silberstein SD et al. Evidence-based guideline update: NSAIDs and other complementary treatments for episodic migraine prevention in adults. Neurology 2012;78:1346-1353
- `[Sacco_2022]` — Sacco S et al. European Headache Federation guideline on the use of monoclonal antibodies targeting the calcitonin gene related peptide pathway for migraine prevention. J Headache Pain 2022;23:67
