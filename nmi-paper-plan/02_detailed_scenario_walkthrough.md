# NeuroAgent: Detailed Clinical Scenario Walkthroughs

This document demonstrates exactly what the NeuroAgent system does, step by step, on realistic clinical cases. It is intended for supervisors and clinical collaborators to understand the system's behavior, evaluate its clinical reasoning, and assess its potential value.

---

## Scenario 1: New-Onset Seizure with Structural Lesion (Straightforward Case)

### Patient Presentation

A 32-year-old right-handed man is brought to the Emergency Department by ambulance after a witnessed generalized tonic-clonic seizure at work. His colleague describes that the patient suddenly stopped talking mid-sentence, his eyes deviated to the left, his left arm began jerking rhythmically, and within seconds the jerking became bilateral and he fell to the ground. The episode lasted approximately 90 seconds. Post-ictally, the patient was confused for 20 minutes and complained of a severe headache. He has no prior seizure history. He reports occasional "strange feelings" over the past 3 months — episodes where familiar environments suddenly feel unreal, lasting 30-60 seconds, which he attributed to stress.

No significant past medical history. Takes no regular medications. No allergies. Mother has epilepsy (diagnosed age 25). Works as an accountant. Social drinker, no recreational drugs. Sleeps 6-7 hours per night.

---

### Step-by-Step Agent Behavior

#### TURN 1 — Initial Assessment and Planning

**Agent receives**: Chief complaint and history above.

**Agent THINKS** (chain-of-thought, visible to the doctor):
```
REASONING:
This is a first generalized tonic-clonic seizure in a 32-year-old male. Several
features are clinically significant:

1. The seizure had a FOCAL ONSET — the eyes deviated to the left and the left
   arm began jerking before secondary generalization. Left-sided onset suggests a
   RIGHT HEMISPHERE epileptogenic focus.

2. The 3-month history of "strange feelings" where familiar environments feel
   unreal is highly suggestive of DÉJÀ VU or DEREALIZATION episodes, which are
   classic temporal lobe auras. These were likely FOCAL AWARE SEIZURES that went
   unrecognized.

3. Family history is positive (mother with epilepsy) — this increases seizure
   risk but also raises the question of genetic vs. structural etiology.

4. The combination of focal seizures with a structural semiology at age 32
   MANDATES brain imaging to rule out a structural lesion.

INITIAL DIFFERENTIAL (before any investigations):
1. Focal epilepsy secondary to structural lesion (tumor, cavernoma, cortical
   dysplasia) — HIGH SUSPICION given focal onset and age
2. Focal epilepsy, genetic/unknown etiology — possible given family history
3. Provoked seizure (sleep deprivation, alcohol) — less likely given the
   preceding aura history

PLAN: I need to follow the hospital's First Seizure Protocol.
Required investigations:
- EEG (mandatory, within 24h)
- Brain MRI with epilepsy protocol (mandatory, within 7d)
- Blood panel (CBC, BMP, glucose, prolactin, hepatic/renal function)
- Detailed clinical history review

I will start with the blood work and EEG, then MRI.
```

**Agent ACTS — Tool Call #1**: `interpret_labs`
```json
{
  "tool": "interpret_labs",
  "parameters": {
    "results": {
      "CBC": "WBC 8.2, Hb 14.5, Plt 245 — all normal",
      "BMP": "Na 140, K 4.1, Cl 102, CO2 24, BUN 15, Cr 0.9, Glucose 95 — all normal",
      "Prolactin": "42 ng/mL (drawn 45 min post-seizure; ref <20)",
      "LFTs": "AST 22, ALT 28, ALP 65 — all normal",
      "TSH": "2.1 — normal",
      "Alcohol_level": "0 mg/dL",
      "Tox_screen": "negative"
    },
    "clinical_context": "First seizure, 45 minutes post-ictal"
  }
}
```

**Mock Tool Returns**:
```json
{
  "interpretation": "All routine labs within normal limits. Prolactin is mildly elevated at 42 ng/mL, which is consistent with a recent generalized tonic-clonic seizure (typically peaks 15-60 min post-ictally and supports an epileptic rather than non-epileptic event). No metabolic cause for seizure identified. Toxicology negative — no substance-provoked etiology.",
  "abnormal_values": [
    {"test": "prolactin", "value": 42, "unit": "ng/mL", "reference": "<20", "clinical_significance": "Expected post-ictal elevation; supports genuine epileptic seizure"}
  ],
  "normal_values_of_note": [
    {"test": "glucose", "note": "Normal — hypoglycemia excluded"},
    {"test": "sodium", "note": "Normal — hyponatremia excluded"},
    {"test": "alcohol", "note": "Zero — alcohol-related seizure excluded"}
  ]
}
```

**Agent REFLECTS**:
```
Lab results exclude metabolic and toxic causes. The elevated prolactin supports
a genuine epileptic seizure (as opposed to a psychogenic non-epileptic event).
No contraindication to standard antiepileptic medications identified in liver/
renal function. Proceeding to EEG.
```

---

#### TURN 2 — EEG Analysis

**Agent ACTS — Tool Call #2**: `analyze_eeg`
```json
{
  "tool": "analyze_eeg",
  "parameters": {
    "eeg_file_path": "patient_032_eeg.edf",
    "patient_age": 32,
    "clinical_context": "First GTC seizure with focal onset (left arm jerking, eye deviation left). 3-month history of derealization episodes. EEG obtained 18 hours post-seizure.",
    "montage": "bipolar_longitudinal",
    "focus_areas": ["epileptiform_discharges", "focal_slowing", "background_asymmetry"]
  }
}
```

**Mock Tool Returns**:
```json
{
  "classification": "abnormal",
  "background": {
    "posterior_dominant_rhythm": "9.5 Hz alpha, symmetric, reactive to eye opening",
    "sleep_features": "Normal vertex waves and sleep spindles observed during stage 2 sleep",
    "overall": "Well-organized background for age"
  },
  "findings": [
    {
      "type": "sharp_wave",
      "location": "F8/T4, maximum phase reversal at T4 (RIGHT ANTERIOR TEMPORAL)",
      "frequency": "Intermittent, 4-5 discharges per 30-minute recording",
      "morphology": "Biphasic sharp waves, amplitude 90-130 μV, duration 70-120ms, followed by a slow wave",
      "state": "More frequent during drowsiness and stage 1 sleep",
      "clinical_correlation": "Consistent with a right anterior temporal epileptogenic focus"
    },
    {
      "type": "intermittent_regional_slowing",
      "location": "Right temporal region (T4/T6)",
      "frequency": "Theta range (4-6 Hz), intermittent",
      "significance": "May indicate underlying structural abnormality in the right temporal region"
    }
  ],
  "artifacts": [
    {"type": "muscle_artifact", "location": "bilateral temporal", "note": "Intermittent, does not obscure epileptiform discharges"},
    {"type": "electrode_artifact", "location": "O2", "note": "Brief, non-significant"}
  ],
  "activating_procedures": {
    "hyperventilation": "Accentuated right temporal slowing. No generalized spike-wave.",
    "photic_stimulation": "Normal photic driving response. No photoparoxysmal response."
  },
  "confidence": 0.91,
  "impression": "Abnormal EEG. Right anterior temporal sharp waves (F8/T4, max T4) and intermittent right temporal slowing. These findings indicate a right temporal epileptogenic focus. The intermittent regional slowing raises the possibility of an underlying structural lesion.",
  "limitations": "30-minute routine recording, interictal only. No seizures captured. If pre-surgical evaluation is considered, prolonged video-EEG monitoring is recommended.",
  "recommended_actions": ["Brain MRI with epilepsy protocol to evaluate for structural lesion in right temporal region"]
}
```

**Agent REFLECTS**:
```
CRITICAL FINDINGS:
The EEG confirms a RIGHT TEMPORAL epileptogenic focus — this is CONCORDANT with
the clinical semiology (left arm jerking = right hemisphere origin, derealization
= temporal lobe aura).

The INTERMITTENT REGIONAL SLOWING is important — in a 32-year-old, right temporal
slowing on a routine EEG raises suspicion for an underlying structural lesion.
This is NOT expected in purely genetic epilepsy.

Updated differential:
1. Structural focal epilepsy — right temporal lesion (ELEVATED SUSPICION)
   → Now the most likely diagnosis. The slowing plus epileptiform discharges
     in a young adult strongly suggests a lesion.
2. Focal epilepsy, unknown etiology — if MRI is normal

NEXT STEP: Brain MRI is now URGENT, not just routine. The combination of focal
seizure + focal EEG abnormality + regional slowing strongly predicts a structural
finding. I will request MRI with epilepsy protocol.
```

---

#### TURN 3 — Brain MRI Analysis

**Agent ACTS — Tool Call #3**: `analyze_brain_mri`
```json
{
  "tool": "analyze_brain_mri",
  "parameters": {
    "mri_path": "patient_032_mri/",
    "sequences_available": ["T1", "T1_contrast", "T2", "FLAIR", "DWI", "SWI"],
    "patient_age": 32,
    "clinical_question": "Evaluate for structural lesion in RIGHT TEMPORAL region. Patient has focal epilepsy with right temporal EEG focus and regional slowing.",
    "compare_with_prior": false
  }
}
```

**Mock Tool Returns**:
```json
{
  "findings": [
    {
      "type": "mass_lesion",
      "location": "Right mesial temporal lobe, centered on the amygdala and extending into the anterior hippocampus",
      "size": "2.3 × 1.8 × 2.0 cm",
      "signal_characteristics": {
        "T1": "Isointense to slightly hypointense relative to gray matter",
        "T2": "Hyperintense, relatively homogeneous",
        "FLAIR": "Hyperintense with partial suppression — suggests some cystic/fluid component",
        "DWI": "No restricted diffusion (ADC not reduced) — argues against high-grade malignancy or acute infarct",
        "T1_contrast": "No enhancement after gadolinium administration",
        "SWI": "No susceptibility artifact (no calcification, no hemorrhage)"
      },
      "mass_effect": "Minimal. Slight expansion of the right temporal lobe. No midline shift. No hydrocephalus.",
      "edema": "Minimal perilesional edema on FLAIR",
      "borders": "Relatively well-defined margins. No irregular enhancement."
    }
  ],
  "volumetrics": {
    "right_hippocampus": "Mildly expanded due to lesion involvement — not atrophic",
    "left_hippocampus": "Normal volume for age",
    "asymmetry_note": "Right > left hippocampal volume (abnormal; due to lesion, not hypertrophy)"
  },
  "additional_observations": [
    "No other intracranial lesions identified",
    "No leptomeningeal enhancement",
    "Remaining brain parenchyma appears normal",
    "Ventricles normal in size and configuration"
  ],
  "impression": "Well-circumscribed, non-enhancing, T2/FLAIR hyperintense lesion in the right mesial temporal lobe (amygdala/anterior hippocampus), measuring 2.3 cm. The imaging characteristics — non-enhancing, no restricted diffusion, well-defined margins, minimal mass effect — are most consistent with a low-grade neoplasm. The differential includes dysembryoplastic neuroepithelial tumor (DNET), ganglioglioma, or low-grade astrocytoma (WHO Grade 2).",
  "differential_by_imaging": [
    {"diagnosis": "DNET (dysembryoplastic neuroepithelial tumor)", "likelihood": "high", "supporting": "Young adult, temporal location, cortical-based, non-enhancing, well-circumscribed, associated with epilepsy"},
    {"diagnosis": "Ganglioglioma", "likelihood": "moderate", "supporting": "Temporal lobe location, young patient, associated with long-standing epilepsy, but typically shows some enhancement"},
    {"diagnosis": "Low-grade diffuse astrocytoma (WHO Grade 2)", "likelihood": "lower", "supporting": "T2/FLAIR hyperintensity, but usually less well-circumscribed and involves more white matter"}
  ],
  "confidence": 0.88,
  "recommended_actions": [
    "Neurosurgical consultation for lesion management",
    "Consider MR spectroscopy for metabolic characterization",
    "Consider advanced imaging (perfusion MRI) if surgical planning needed",
    "Follow-up MRI in 3-6 months if conservative management chosen"
  ]
}
```

**Agent REFLECTS**:
```
SYNTHESIS — All modalities now converge:

CLINICAL: Focal seizures (déjà vu auras × 3 months → GTC with left arm onset)
EEG:      Right anterior temporal sharp waves + regional slowing
MRI:      2.3 cm right mesial temporal mass (amygdala/anterior hippocampus)

The CONCORDANCE is striking — the seizure semiology (temporal aura + left
motor involvement), EEG focus (right temporal), and MRI lesion (right mesial
temporal) all point to the same location. This is a textbook case of
LESIONAL FOCAL EPILEPSY.

The imaging characteristics strongly suggest a LOW-GRADE NEOPLASM, most
likely DNET or ganglioglioma. Key reasoning:
- Non-enhancing → not high-grade
- Well-circumscribed → developmental tumor (DNET/ganglioglioma) > diffuse astrocytoma
- Mesial temporal, cortically based → classic DNET location
- Young adult with epilepsy → DNET is the most common cause of drug-resistant
  temporal lobe epilepsy in this age group

This is NOT an emergency (no mass effect, no enhancement suggesting transformation)
but DOES require neurosurgical evaluation.

FINAL DIFFERENTIAL:
1. DNET with secondary focal epilepsy (HIGH confidence: 0.85)
2. Ganglioglioma with secondary focal epilepsy (MODERATE: 0.60)
3. Low-grade astrocytoma WHO Grade 2 (LOWER: 0.30)

Before making final recommendations, let me check drug interactions and
search the literature for current management guidelines.
```

---

#### TURN 4 — Literature Search and Drug Check

**Agent ACTS — Tool Call #4**: `search_medical_literature`
```json
{
  "tool": "search_medical_literature",
  "parameters": {
    "query": "DNET ganglioglioma temporal lobe epilepsy surgical outcome drug-resistant seizure management guidelines 2023 2024",
    "sources": ["pubmed", "aan_guidelines"],
    "max_results": 5
  }
}
```

**Agent ACTS — Tool Call #5** (parallel): `check_drug_interactions`
```json
{
  "tool": "check_drug_interactions",
  "parameters": {
    "proposed_medication": "levetiracetam",
    "dose": "500mg BID",
    "current_medications": [],
    "patient_conditions": ["focal_epilepsy", "right_temporal_mass"],
    "patient_age": 32,
    "hepatic_function": "normal",
    "renal_function": "normal"
  }
}
```

**Mock Literature Returns**:
```json
{
  "key_findings": [
    {
      "source": "ILAE Surgical Treatment Guidelines (2024 update)",
      "finding": "For drug-resistant focal epilepsy with a concordant MRI lesion, surgical resection is recommended (Level A evidence). Seizure freedom rates after temporal lobectomy/lesionectomy for DNET: 80-90%. For ganglioglioma: 75-85%."
    },
    {
      "source": "European Epilepsy Guidelines (2023)",
      "finding": "In patients with a first seizure and a lesion on MRI, the risk of seizure recurrence is >60% within 2 years. Initiation of antiepileptic medication is recommended. Levetiracetam or lamotrigine are first-line for focal epilepsy."
    },
    {
      "source": "Neurosurgical management of low-grade epilepsy-associated tumors — systematic review (2024)",
      "finding": "Early surgical intervention for DNETs and gangliogliomas is associated with better seizure outcomes compared to prolonged medical management. Gross total resection achieves seizure freedom in 85-92% of DNET cases."
    }
  ],
  "evidence_level": "Level A (strong recommendation for surgical evaluation in concordant lesional epilepsy)"
}
```

**Mock Drug Check Returns**:
```json
{
  "proposed": "Levetiracetam 500mg BID",
  "interactions": "None — patient on no other medications",
  "contraindications": "None identified",
  "warnings": [
    "Monitor for behavioral side effects (irritability, mood changes) — reported in ~10-15% of patients",
    "Dose adjustment needed if renal function declines (not currently applicable)"
  ],
  "formulary_status": "Available — first-line per hospital formulary for focal epilepsy",
  "alternative_if_intolerant": "Lamotrigine (requires slow titration over 6-8 weeks)"
}
```

---

#### TURN 5 — Final Synthesis and Report

**Agent ACTS — Tool Call #6**: `check_hospital_rules`
```json
{
  "tool": "check_hospital_rules",
  "parameters": {
    "pathway": "first_seizure_protocol",
    "completed_steps": ["labs", "eeg", "brain_mri"],
    "findings": "focal_epilepsy_with_lesion"
  }
}
```

**Mock Rules Returns**:
```json
{
  "protocol_status": "All mandatory steps completed",
  "required_next_steps": [
    {"action": "neurology_consultation", "timing": "within 48h", "status": "IN PROGRESS (this agent session)"},
    {"action": "neurosurgical_referral", "timing": "within 2 weeks", "required_because": "concordant MRI lesion with epilepsy"},
    {"action": "initiate_aed", "timing": "before discharge", "recommendation": "levetiracetam 500mg BID per formulary"}
  ],
  "documentation_required": ["diagnostic_summary", "referral_letter_neurosurgery"]
}
```

**Agent GENERATES — Final Diagnostic Summary**:
```
══════════════════════════════════════════════════════════════
                    DIAGNOSTIC SUMMARY
══════════════════════════════════════════════════════════════

PATIENT: 32-year-old right-handed male
PRESENTATION: First generalized tonic-clonic seizure with focal
              onset (left arm clonic activity, eye deviation left)
              3-month history of derealization episodes (likely
              focal aware seizures)

─── INVESTIGATION RESULTS ───────────────────────────────────

BLOOD WORK: All within normal limits. Prolactin 42 ng/mL (post-
ictal elevation consistent with epileptic seizure). No metabolic
or toxic etiology identified.

EEG: ABNORMAL — Right anterior temporal sharp waves (F8/T4, max
phase reversal T4) and intermittent right temporal theta slowing.
Findings indicate a right temporal epileptogenic focus. Regional
slowing raises suspicion for underlying structural abnormality.

BRAIN MRI: Well-circumscribed, non-enhancing, T2/FLAIR hyper-
intense lesion in the right mesial temporal lobe (amygdala/
anterior hippocampus), 2.3 × 1.8 × 2.0 cm. No restricted
diffusion, no hemorrhage, minimal mass effect.

─── CLINICAL CORRELATION ────────────────────────────────────

All three modalities show CONCORDANCE pointing to the right
mesial temporal lobe:
  • Clinical:  Left motor onset → right hemisphere
               Derealization aura → temporal lobe
  • EEG:      Right anterior temporal epileptiform focus
  • MRI:      Right mesial temporal lesion

─── DIAGNOSIS ───────────────────────────────────────────────

FOCAL EPILEPSY secondary to a right mesial temporal mass, most
likely a low-grade neuroepithelial tumor (DNET > ganglioglioma
> low-grade astrocytoma).

Diagnostic confidence: HIGH (0.92)

─── RECOMMENDATIONS ─────────────────────────────────────────

1. INITIATE ANTIEPILEPTIC MEDICATION
   → Levetiracetam 500mg BID (per hospital formulary, first-line
     for focal epilepsy). No drug interactions. Monitor for
     behavioral side effects.

2. NEUROSURGICAL REFERRAL (within 2 weeks)
   → For evaluation of surgical resection. Current evidence
     supports early surgery for epilepsy-associated low-grade
     tumors (seizure freedom rate 85-92% for DNET with gross
     total resection).

3. FURTHER INVESTIGATIONS (to discuss with neurosurgery):
   → MR spectroscopy for metabolic characterization
   → Video-EEG monitoring if pre-surgical evaluation pursued
   → Consider advanced MRI (perfusion) for surgical planning

4. PATIENT COUNSELING
   → Driving restriction per local regulations (typically 6-12
     months seizure-free, varies by jurisdiction)
   → Seizure precautions (avoid heights, swimming alone, etc.)
   → Return to ED if seizure recurrence

5. FOLLOW-UP
   → Neurology outpatient in 4-6 weeks
   → Repeat MRI in 3 months if surgery not immediately pursued

─── EVIDENCE BASE ───────────────────────────────────────────

• ILAE Surgical Guidelines (2024): Level A recommendation for
  surgical evaluation in concordant lesional focal epilepsy
• Seizure recurrence risk with lesion on MRI: >60% within 2 years
• European Epilepsy Guidelines (2023): Levetiracetam first-line
  for focal epilepsy

══════════════════════════════════════════════════════════════
```

**Agent updates PATIENT MEMORY**:
```json
{
  "patient_id": "032",
  "encounter_date": "2026-XX-XX",
  "encounter_type": "emergency",
  "diagnoses_added": [
    {"code": "G40.109", "description": "Focal epilepsy, right temporal, not intractable"},
    {"code": "D33.0", "description": "Right mesial temporal neoplasm, suspected benign (DNET)"}
  ],
  "medications_started": ["levetiracetam 500mg BID"],
  "pending_referrals": ["neurosurgery"],
  "pending_investigations": ["MR spectroscopy", "video-EEG (if pre-surgical)"],
  "follow_up": "neurology outpatient 4-6 weeks",
  "key_findings_for_future_encounters": "Right temporal epileptogenic focus concordant with 2.3cm right mesial temporal mass. If patient returns with seizure recurrence, consider medication dose increase and expedite surgical evaluation."
}
```

---

### Summary of Agent Actions on This Case

| Turn | Agent Action | Tool Called | Key Outcome |
|------|-------------|-------------|-------------|
| 1 | Reviews history, identifies focal onset, plans workup | `interpret_labs` | Excludes metabolic/toxic causes |
| 2 | Requests EEG, interprets focal findings | `analyze_eeg` | Right temporal epileptogenic focus with slowing |
| 3 | Requests MRI targeting right temporal region | `analyze_brain_mri` | 2.3cm mesial temporal mass (likely DNET) |
| 4 | Searches literature + checks drug interactions | `search_literature` + `check_drug_interactions` | Evidence for surgical referral; levetiracetam safe |
| 5 | Checks protocol compliance, generates report | `check_hospital_rules` | All mandatory steps completed; generates summary |

**Total tool calls**: 6
**Correct diagnosis**: Yes (focal epilepsy secondary to right temporal mass, likely DNET)
**Critical actions taken**: EEG ✓, MRI ✓, AED initiated ✓, neurosurgical referral ✓
**Protocol adherence**: Full compliance with First Seizure Protocol
**Dangerous actions avoided**: Did not dismiss the derealization episodes; did not attribute to anxiety

---

## Scenario 2: Returning Patient — 4-Month Follow-Up (Tests Longitudinal Memory)

### Context

The same patient returns to the neurology outpatient clinic 4 months later. He has been on levetiracetam 500mg BID. He saw the neurosurgeon, who recommended monitoring for now given the benign imaging features and only one provoked seizure to date.

**New Complaint**: He reports 2 more episodes of derealization over the past month (despite medication), and his wife noticed that during one episode he was "staring and smacking his lips" for about 30 seconds — he has no memory of this.

---

### Agent Behavior (Memory-Enabled)

#### TURN 1 — Memory Retrieval

**Agent retrieves from patient memory**:
```
PREVIOUS ENCOUNTER (4 months ago):
- First GTC with focal onset (left arm, eyes left)
- 3-month history of derealization episodes prior to GTC
- EEG: Right anterior temporal sharp waves + regional slowing
- MRI: 2.3cm right mesial temporal mass (likely DNET)
- Started levetiracetam 500mg BID
- Referred to neurosurgery — recommended monitoring
- Pending: follow-up MRI in 3 months
```

**Agent THINKS**:
```
REASONING (using memory):
This patient has a KNOWN right mesial temporal lesion (likely DNET) and was
started on levetiracetam 500mg BID 4 months ago. He is now reporting:

1. BREAKTHROUGH FOCAL AWARE SEIZURES — the derealization episodes have
   continued despite medication (2 in the past month)
2. NEW: FOCAL IMPAIRED AWARENESS SEIZURE — the episode with lip smacking
   and staring (oral automatisms + impaired awareness) is a clear FOCAL
   SEIZURE WITH IMPAIRED AWARENESS, a progression from the focal aware
   seizures he had before

This represents SEIZURE PROGRESSION despite first-line AED therapy.
This changes the clinical picture significantly:

- The epilepsy is now DRUG-RESISTANT to first-line therapy (seizures persisting
  despite adequate trial of one AED)
- Per ILAE definition, drug resistance is established after failure of 2
  appropriately chosen AEDs. Technically, one more trial is needed, BUT...
- Given the concordant structural lesion, the surgical option becomes more
  compelling

ALSO: The follow-up MRI was due 1 month ago. Has it been done?

PLAN:
1. Verify: was the 3-month follow-up MRI completed? If not, ORDER IT NOW
2. Consider: increase levetiracetam dose (can go to 1500mg BID max) OR
   add second AED (lamotrigine)
3. Re-refer to neurosurgery with updated seizure information — the case
   for surgical resection is now STRONGER
4. Consider: prolonged video-EEG to characterize the new seizure type
```

**Agent ASKS the doctor**: "The follow-up MRI was scheduled 3 months after the initial presentation — has this been completed? I don't have the results in the patient's record."

**Doctor responds**: "No, the patient missed that appointment. We need to reschedule it."

**Agent ACTS — Tool Call #1**: `analyze_eeg` (new EEG obtained today)

**Mock Tool Returns**: Similar right temporal sharp waves, now more frequent (8-10 per 30 minutes vs. 4-5 previously), with a brief run of right temporal rhythmic theta activity during drowsiness.

**Agent REFLECTS**:
```
The EEG shows INCREASED epileptiform activity compared to 4 months ago
(8-10 vs 4-5 discharges). This, combined with the clinical seizure
progression, suggests the epilepsy is becoming more active despite medication.

The new finding of brief rhythmic theta activity is concerning — this may
represent subclinical seizure activity.

UPDATED ASSESSMENT: This patient has DRUG-RESISTANT FOCAL EPILEPSY secondary
to a right temporal mass. The trajectory is worsening.

RECOMMENDATION: Strongly advocate for:
1. Urgent repeat MRI (to assess lesion stability — must rule out growth)
2. Medication adjustment: increase levetiracetam to 750mg BID
3. Expedited neurosurgical re-evaluation with emphasis on progression
4. Video-EEG monitoring for pre-surgical evaluation
```

**Agent generates updated report with explicit reference to the prior encounter and trend data.**

---

### What This Scenario Demonstrates

- **Memory matters**: The agent knew this was a returning patient, recalled the lesion, the EEG findings, the medication, and the pending follow-up MRI
- **Trend detection**: The agent compared EEG findings across encounters (more discharges now)
- **Clinical progression reasoning**: The agent recognized that continuing seizures on medication = drug resistance = stronger surgical indication
- **Safety catch**: The agent identified the missed follow-up MRI and flagged it

**Without memory**, the agent would have treated this as a new patient, potentially re-ordering all baseline investigations from scratch and missing the critical temporal trend.

---

## Scenario 3: Diagnostic Puzzle — Autoimmune Encephalitis (Challenging Case)

### Patient Presentation

A 24-year-old woman is brought in by her family. Over the past 2 weeks, she developed progressively worsening confusion, bizarre behavior (talking to people who aren't there, undressing in public), and a new-onset seizure yesterday. The family reports that 3 weeks ago she had a flu-like illness with fever and headache that seemed to resolve, but then the psychiatric symptoms started.

Previously healthy. No medications. No drug use. No travel history. No family history of neurological or psychiatric disease.

---

### Agent Behavior (Abbreviated)

**TURN 1** — Agent reviews history and identifies this as a DIAGNOSTIC PUZZLE:
```
REASONING:
This is a subacute onset of encephalopathy (confusion + behavioral change +
seizure) in a young woman following a viral prodrome. This is a RED FLAG
pattern.

CRITICAL: This is NOT primarily psychiatric. The combination of:
- Subacute cognitive decline (days to weeks)
- New psychiatric symptoms (hallucinations, disinhibition)
- Seizures
- Preceding viral illness
... is CLASSIC for AUTOIMMUNE ENCEPHALITIS until proven otherwise.

The most important diagnosis to consider is ANTI-NMDAR ENCEPHALITIS —
this is the most common autoimmune encephalitis in young women and can
present exactly like this.

However, I must also consider:
1. Viral encephalitis (HSV — this is an emergency to rule out)
2. Autoimmune encephalitis (anti-NMDA receptor, LGI1, CASPR2)
3. CNS vasculitis
4. Neoplastic (limbic involvement from occult tumor)

HSV encephalitis is a MEDICAL EMERGENCY requiring immediate treatment.
I cannot wait for results before raising this concern.

⚠️ URGENT RECOMMENDATION TO DOCTOR: Consider empiric IV acyclovir NOW
while awaiting HSV PCR results. HSV encephalitis is fatal if untreated
and the clinical presentation overlaps. This should not wait for
diagnostic confirmation.
```

**Agent flags the urgency, then systematically requests**:
- Labs (including autoimmune panel, HSV PCR)
- Brain MRI (looking for temporal lobe signal change in HSV, or more diffuse changes in autoimmune)
- EEG (looking for extreme delta brush in anti-NMDAR, or periodic lateralized discharges in HSV)
- CSF analysis (cell count, protein, glucose, HSV PCR, autoimmune antibody panel)

**Key reasoning moments**:

After MRI returns showing **bilateral medial temporal FLAIR hyperintensity without restricted diffusion**: the agent notes this could be either HSV or autoimmune encephalitis and flags that the pattern is more symmetric than typical HSV.

After EEG returns showing **generalized rhythmic delta activity with superimposed beta ("extreme delta brush" pattern)**: the agent recognizes this as highly specific for **anti-NMDAR encephalitis** and raises its confidence significantly.

After CSF returns with **lymphocytic pleocytosis (WBC 35, 95% lymphocytes), mildly elevated protein, normal glucose, HSV PCR negative**: the agent excludes HSV (PCR negative is highly sensitive) and the profile matches autoimmune encephalitis.

**Agent requests an additional test** (this is the key decision): `order_test: anti-NMDA_receptor_antibodies_serum_and_csf`

The agent also recommends: `order_test: pelvic_ultrasound` — because anti-NMDAR encephalitis in young women is frequently associated with ovarian teratoma, and identifying this is critical for treatment.

**Final diagnosis**: Anti-NMDA receptor encephalitis, pending antibody confirmation. Recommend first-line immunotherapy (IV methylprednisolone + IVIG or plasmapheresis) and pelvic imaging.

---

### What This Scenario Demonstrates

- **Differential diagnosis under uncertainty**: The agent kept multiple diagnoses alive simultaneously and used each test result to narrow them
- **Urgency recognition**: Flagged HSV as a medical emergency requiring immediate empiric treatment
- **Pattern recognition across modalities**: The "extreme delta brush" on EEG, combined with the clinical picture and CSF profile, pointed to anti-NMDAR
- **Proactive test ordering**: The agent requested the specific antibody panel AND the pelvic ultrasound — a step that even some neurologists miss early on
- **Sequential reasoning**: The agent didn't request everything at once; it interpreted each result and adjusted its next request accordingly

---

## Scenario 4: Agent Correctly Identifies a Non-Neurological Cause

### Brief Description

A 55-year-old man is referred to neurology for "seizure-like episodes" — brief episodes of feeling faint, blurred vision, and one episode of loss of consciousness. His wife says he "shook a little" during the LOC episode.

The agent:
1. Obtains an EEG → **normal**
2. Notes that the episodes are triggered by standing up, preceded by lightheadedness (not typical seizure aura)
3. Requests an ECG → reveals **intermittent second-degree heart block (Mobitz Type II)**
4. Concludes this is **cardiac syncope, not epilepsy**
5. Recommends urgent cardiology referral rather than starting antiepileptic medication
6. Does NOT start any AED — correctly avoiding unnecessary treatment

**What this shows**: The agent can use negative results (normal EEG) as evidence, recognize non-neurological diagnoses within its scope, and make appropriate cross-specialty referrals.

---

## Key Points for Supervisors and Clinical Collaborators

### What the agent does well:
1. **Integrates multi-modal evidence** — doesn't look at EEG, MRI, labs in isolation but synthesizes them
2. **Reasons sequentially** — orders tests strategically based on prior results, not all at once
3. **Recognizes urgency** — flags emergencies (HSV encephalitis) before completing the full workup
4. **Uses memory** — recalls prior encounters, detects trends, flags missed follow-ups
5. **Follows protocols** — adheres to institutional pathways, documents required steps
6. **Shows its reasoning** — every decision is explained, making it auditable

### What the agent does NOT do:
1. Does not replace the doctor — it suggests, the doctor decides
2. Does not directly interpret raw images or signals — it calls specialized tools and interprets their outputs
3. Does not have access to real patient data in this evaluation — all cases and tool outputs are simulated
4. Does not claim certainty — it always provides confidence levels and differential diagnoses, not single answers

### Why mock tool outputs are valid for evaluation:
The question we're testing is: "Given that an EEG model tells you X and an MRI model tells you Y, can the agent put the pieces together correctly?" This is like testing a medical student with case studies — the student doesn't run the MRI machine, but they need to interpret the radiology report. We're testing clinical reasoning, not image processing.
