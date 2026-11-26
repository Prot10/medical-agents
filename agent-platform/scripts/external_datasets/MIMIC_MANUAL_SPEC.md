# The reader's manual file for a MIMIC pilot case (tasks 03 and 04)

One JSON file per case, `$W/out/03_manual/<case_id>.json`, written whole (one Write call). It holds
only what needs judgement; everything else is computed by `mimic_case_build3.py`, which checks every
phrase you copy against the source and fails the build when one is not verbatim. No record content
in this document (PhysioNet DUA).

Inputs to read, per case: `$W/out/02_source/<case_id>.json` (all rows, the discharge note in
`discharge[0].text`) and `$W/out/02_draft/<case_id>.json` (note sections, `admission_exam`).

## Rules (workspace CLAUDE.md, "Decisions")
- The presentation must contain no study result, no ED or outside-hospital work-up (tests,
  treatments given in the ED and their response), no hospital course, nothing naming or implying the
  diagnosis. It keeps what the patient, family, witnesses and EMS report, pre-hospital events and
  treatment, past history (prior episodes of the same condition stay; their work-up results go).
- Never serve a de-identification blank that hides a negation ("___ edema", "There is ___ X").
- Exam: the admission exam only, never the discharge exam. Keep state and devices (intubated, on
  oxygen, catheter); cut items naming a treatment chosen for the diagnosis (thrombolysis given,
  antiseizure loading named, a specific drip) and items naming the diagnosis ("due to status").
- Note-extracted reports (EEG, EMG/NCS, echo, telemetry, respiratory function) follow the NeuroBench
  format: findings + impression. Findings and impression are taken from the note (verbatim phrases
  listed in `_verbatim`). The impression keeps only what the study itself shows (electrographic
  status epilepticus, an acute demyelinating polyneuropathy pattern, LV ejection fraction 40 %); it
  drops clinical diagnoses that need other information ("consistent with GBS"), recommendations,
  comparisons with later studies, treatment and course. Serve only the first recording in the work-up
  window; a whole-stay summary that cannot be separated is not served.
- The record must support the coded diagnosis: the discharge diagnosis names the condition, or the
  note documents its defining evidence (SE: a seizure of >= 5 min, repeated seizures without recovery
  in between, or electrographic status on EEG). Record the reason in `dx_support`.


## Task-04 additions (decisions 20-29)
- Transfer (decisions 8, 21): treatment or intubation at an outside facility (another hospital or
  ED, urgent care, clinic, dialysis or infusion unit, nursing or residential facility) before arrival
  makes the admission a transfer: set `"exclude": "inter-hospital transfer after outside work-up (...)"`.
  So does any work-up there (labs, imaging) or a stated transfer from another hospital. EMS treatment
  on the way (benzodiazepines, intubation by EMS) is pre-hospital care and stays in the HPI (the
  NeuroBench templates hold it). An outside evaluation with no treatment and no test is kept; say so
  in `other_edits`. When the giver or the place of a pre-arrival treatment is not stated, exclude.
- FEPI (focal epilepsy): the EEG is the first EEG of the stay (routine, video or continuous); set
  `eeg_type` to what was recorded. Record support: the discharge diagnosis names a focal / partial /
  localization-related epilepsy, or the note documents focal-onset seizures (aura, focal motor or
  impaired-awareness semiology, a focal EEG or lesion). A provoked seizure only (alcohol withdrawal,
  hypoglycaemia), a generalized epilepsy, or status epilepticus as the reason for admission: exclude
  with the class. Known epilepsy in the history stays (decision 25); write in `other_edits` whether
  the epilepsy was known before this admission ("known epilepsy: yes|no").
- Note-extracted impressions (decision 24): no disease or syndrome name the study alone cannot
  establish (multiple sclerosis, GBS / AIDP, vasculitis, NMO, ADEM, Balo: write the pattern, e.g.
  "concentric ring lesion"). Electrographic and electrodiagnostic patterns stay ("focal seizures
  arising from the left temporal region", "demyelinating polyneuropathy").
- Values blanked by de-identification (decision 27) are never written into a note-extracted report
  ("EF ___ %", "protein ___"): leave that value out.


## Task-06 additions (decisions 30-41)
- Files: `$W/out/06_manual/<case_id>.json` (same schema plus the fields below). Build check:
  `~/projects/medical-agents/.venv/bin/python -I mimic_case_build6.py --out $W/out --selection <file> --cases-only <ids>`.
- EEG storage (41): `eeg` is the FIRST EEG of the stay with its true `eeg_type` (routine, continuous_icu,
  video, ambulatory, sleep_deprived). Every later EEG goes in `eeg_followups: [ {...same EEG schema...} ]`
  in time order, each with its own `eeg_type`, `_verbatim` and `_verbatim_source`.
- `eeg_source`: `formal_report` (an EEG report or its impression in the note) or `course_summary` (a
  hospital-course sentence). Prefer the formal report. A course sentence counts only when it states the
  finding the diagnosis rests on (32): SE: electrographic seizures or status, or their absence; FEPI:
  focal discharges or seizures and their side or region. "EEG done" or "unremarkable" alone is not a
  result for SE or FEPI: `exclude: "thin_eeg"`.
- Burst suppression, medication effect and similar wording in an EEG is a pattern and stays (36).
- FEPI (33, 34): explicitly frontal, parietal or occipital focus -> `exclude: "non_temporal_focus"`; a
  prolonged focal seizure or a cluster coded as status -> `exclude: "possible_status"`. Temporal or not
  localised foci stay.
- EMS (31): EMS benzodiazepines, airway management and glucose stay in the presentation. An exam charted
  before an ED intubation is served as charted; the HPI states the intubation only if it happened before
  the ED decision (EMS or before arrival).
- `clinical_assessment` (when the condition's policy requires `perform_clinical_assessment` and the note
  records the result): `{"assessment_type": "performance_status|functional_neuro_signs|cognitive_screen|
  gait_and_balance_timed|orthostatic_blood_pressure", "timing": "", "scores": {...}, "criteria_met": null,
  "findings": [...], "impression": "", "_verbatim": [...], "_verbatim_source": ""}` from the admission
  documentation only (a KPS, a positive Hoover sign, orthostatic vital signs with values).
- `tissue_diagnosis` (GLIO): `{"procedure": "resection|stereotactic_biopsy|open_biopsy", "site": "",
  "specimen_adequate": true, "integrated_diagnosis": "", "histological_diagnosis": "", "who_grade": null,
  "molecular_findings": {...} | null, "diagnosis_suffix": null, "_verbatim": [...], "_verbatim_source": ""}`
  from the pathology report or final pathology stated in the note.
- `echo` for SYNC and ISCH: the first TTE of the stay; EF only as a single recorded number (29).
- New conditions: SYNC (`syncope_cardiac`): record support requires a documented cardiac cause of the
  syncope (arrhythmia, conduction disease, structural heart disease) named in the discharge diagnosis or
  shown by the work-up; vasovagal, orthostatic, situational or unexplained syncope -> `exclude:
  "not_cardiac_syncope"`. Write the cause's ICD-10 code in `dx_support.cause_icd10` (e.g. I44.1), the cause as a short
  generic diagnosis label in `dx_support.cause_label` (e.g. "complete heart block"; never "cardiac syncope"), and the
  cause in generic words in `dx_support.reason`. HEP: hepatic encephalopathy in cirrhosis. GLIO: a
  glioma (not metastasis, not lymphoma) with tissue diagnosis in the stay. FND: functional signs
  documented on the admission exam.

## Schema
```json
{
 "case_id": "MIMIC-XX-NNN",
 "hpi_removals": [{"from": "<first words of the passage, verbatim>", "to": "<last words, verbatim; omit for a one-sentence passage>",
                    "class": "names_dx|ed_course|outside_workup|study_result|prior_workup_result|treatment_response|hospital_course|deid_ambiguous|noise",
                    "why": "<short reason, no patient detail>"}],
 "chief_complaint_rewrite": null | {"text": "<presenting symptoms, words of the kept HPI>", "_verbatim": ["<phrases of the kept HPI used>"],
                                    "decision": 7 | 9},
 "handedness": "right|left|",
 "past_medical_history": null | ["<verbatim items>"],
 "allergies": null | ["..."], "family_history": null | ["..."], "medications": null | [{"drug","dose","frequency","indication"}],
 "social_history": {},
 "neurological_exam": {"mental_status": "", "cranial_nerves": "", "motor": "", "sensory": "", "reflexes": "", "coordination": "", "gait": "", "additional": null},
 "physical_exam": {"general": "", "HEENT": "", "...": ""},
 "exam_cuts": [{"text": "<what was cut>", "class": "treatment_named|diagnosis_named|deid_ambiguous|discharge_exam"}],
 "exam_devices_kept": ["intubated", "foley", "..."],
 "eeg": null | {"eeg_type": "continuous_icu|video|routine", "classification": "normal|abnormal", "background": {"overall": "..."},
                "findings": [{"type": "...", "location": "...", "frequency": "", "morphology": "", "state": "", "clinical_correlation": ""}],
                "artifacts": [], "activating_procedures": {}, "impression": "<electrographic diagnosis>", "limitations": "", "recommended_actions": [],
                "_verbatim": ["..."], "_verbatim_source": "<where in the note, and what was dropped>"},
 "emg": null | {"test_type": "emg_ncs", "findings": [{"nerve": "...", "finding": "..."}], "quantitative_data": null,
                "impression": "<electrodiagnostic pattern>", "recommended_actions": [], "_verbatim": [], "_verbatim_source": ""},
 "respiratory_function": null | {"test_type": "respiratory_function", "findings": [{"test": "NIF|VC|FVC", "result": "..."}],
                                 "quantitative_data": null, "impression": "", "recommended_actions": [], "_verbatim": [], "_verbatim_source": ""},
 "telemetry": null | {"duration_hours": 0, "monitor_type": "telemetry", "rhythm_summary": "...", "heart_rate_range": {}, "events": [],
                      "findings": [], "impression": "", "recommended_actions": [], "_verbatim": [], "_verbatim_source": ""},
 "echo": null | {"echo_type": "TTE", "chambers": {}, "valves": {}, "ejection_fraction": null, "wall_motion": null, "findings": [],
                 "impression": "", "recommended_actions": [], "_verbatim": [], "_verbatim_source": ""},
 "radiology_drop_sentences": [{"study": "any", "sentence": "<verbatim sentence of a radiology report>", "why": "refers to a later study"}],
 "dx_support": {"supported": true|false, "basis": "discharge_diagnosis|defining_evidence|none", "reason": "<class, no quote>"},
 "exclude": null | "<reason class>",
 "other_edits": ["<edits that are not removals>"], "exam_notes": []
}
```
`null` for PMH, allergies, family history or medications means "computed from the note section";
give a list only to correct it. Exam values may join several verbatim fragments with ` | `.
ECG, CT, CTA, MRI, spine MRI, labs, CSF labs, telemetry (rhythm records) and ICU respiratory values
are computed from tables: do not write them. Write `telemetry` or `respiratory_function` only when the
note states a result of the first recording; the table answer is used when it exists.
