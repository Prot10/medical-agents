# Task 06, check C4: independent field-by-field re-read (protocol for reader subagents)

No record content in this file. The reader did not build the cases.

## Input
One file per case, `$W/tmp/reread6/<case_id>.md`:
- PART 1: the case as built: the presentation exactly as the agent sees it, every tool output
  (initial outputs and follow-ups with their triggers), the policy (action criteria), the diagnosis
  labels, the hidden metadata; PART 1b: served-origin metadata (`origin`, `source`, `exam`, `t_h`).
- PART 2: the source: triage, ED medication times, the discharge note, the radiology reports in
  the window (and every served report), machine ECG reads. Times are hours from ED arrival.
Lab values are rechecked by script (not your task), but check that lab panels are not served
after a treatment of that analyte (rule 23 below).

## What to check, field by field
Presentation (demographics, chief complaint, HPI, past history, medications, allergies, family and
social history, vitals, neurological exam, physical exam):
1. Every served sentence or item is in the note (verbatim apart from whitespace, de-identification
   blanks removed, an allowed rewrite of the chief complaint from the HPI symptoms).
2. Nothing in it is: the result of any study; the ED or outside-hospital work-up or treatment and its
   response; the hospital course; a statement of the final diagnosis of this episode. Allowed:
   patient/family/witness/EMS accounts, EMS treatment, past history including known disease of the
   same condition, devices and state in the admission exam.
3. Omissions: an intact, allowed item of the admission exam or history that is not served (count it).
4. Field placement: content in the wrong field (e.g. exam text in family history).

Tool outputs:
5. Each report: the served findings and impression come from the right source report (exam name and
   time in PART 1b), are verbatim apart from the allowed removals, and contain no content of another
   study (CTA content in a plain CT answer, spine content in a brain MRI, perfusion in a CTA, ...).
6. Allowed removals: recommendations, result communication, references to later studies, treatment
   and procedures of the stay, clinical diagnoses the study alone cannot establish (pattern words
   stay), de-identification blanks that hide a value or a negation. Anything else removed is an
   over-removal (omission); anything of these classes left is a leak.
7. Timing: an extra study (ECG, imaging, serial labs, microbiology) after admission + 48 h is an
   error, except the first policy specimen of microbiology. Follow-ups are in time order.
8. Note-extracted outputs (EEG, echo, telemetry text, EMG, clinical assessment, tissue diagnosis):
   the content is stated in the note; EEG type and the order of EEGs are right; eeg_source matches.
9. ECG: rate and machine statements match the first machine read in the window (follow-ups later).
10. Rule 23: no glucose after insulin/dextrose, blood gas after ventilation, coagulation after
    therapeutic anticoagulation or reversal, haemoglobin/platelets after transfusion, drug levels after
    a load. Use the ED medication times.

Ground truth and metadata:
11. Diagnosis: accepted labels name this patient's condition; no rejected label names what the record
    says the patient has. ICD code matches the condition.
12. Policy: every required criterion has a served result; arguments (contrast, panels, specimen) match
    what was served.
13. Metadata: dx_support (clinical_only when no study confirms), known_condition_in_history, eeg_source.

## Error classes (one per finding)
`value_mismatch`, `not_in_source`, `wrong_source_report`, `other_study_content`, `leak_presentation`,
`leak_tool_output`, `timing`, `omission`, `over_removal`, `field_placement`, `deid`, `broken_text`,
`note_extraction`, `ecg`, `lab_after_treatment`, `label`, `policy`, `metadata`, `other`.
Severity: `error` (wrong or leaking content served, or a required item wrong) or `minor` (cosmetic,
a small omission, a source inconsistency carried over faithfully). A source typo carried verbatim is
not an error (note it as `source_issue` in notes, not as a finding).

## Output (one JSON file per reader, one Write call)
```
{"<case_id>": {"fields_checked": <int>, "findings": [{"field": "...", "class": "...", "severity": "error|minor",
  "detail": "short description of the problem class, with the minimal words needed to locate it"}],
  "notes": "..."}, ...}
```

## Round 2 (re-read of the fixed cases)
Files: `$W/tmp/reread6c/<case_id>.md`, same PART 1 / 1c / 2, plus PART 3: the errors the first reader
found in this case. Do the full field-by-field check again (all classes above), and in addition give
for every PART-3 error a verdict: `fixed`, `not_fixed`, or `not_applicable` (the first finding was
wrong), with one short reason. Rules settled since round 1 (not errors):
- a first study that is not a policy step of the case and falls after admission + 48 h is not served;
  a policy (required or recommended) study after that point is served (task-04 rule, a known limitation);
- diagnosis labels are expanded from the repository synonyms file for the case's code (decision 40) and
  may not be edited here: a wrong label is still recorded as `label`, severity error, but mark it
  `not_fixed` with reason "synonyms file";
- a strength grid row shortened by de-identification serves only the cells before its first blank,
  marked "(remaining cells not attributable)".
Output: `{"<case_id>": {"fields_checked": n, "findings": [...], "part3": [{"class": "...", "field": "...", "verdict": "...", "reason": "..."}], "notes": "..."}}`

## Round 3 and later (task 07)
Files: `$W/tmp/reread7_rN/<case_id>.md` (same parts as round 1; PART 1c holds every follow-up, the hidden flags,
the diagnosis labels and the policy-study hours). A full field-by-field check of every field (all classes above).
Settled rules (apply them; a finding that only restates one of these is not an error):
- decision 42: SAH with negative angiography or a non-aneurysmal cause is coded I60.8 and accepts only the non-aneurysmal
  labels; an aneurysmal case keeps its I60.x code. A rejected label never shares all its words with an accepted one.
- decision 43: labels come from the repository synonyms file plus the task-07 overlay; a label the record contradicts is
  still an error (class `label`).
- decision 44: the first result of the stay answers a policy step even after admission + 48 h; its hours from ED arrival are in
  `policy_study_hours`. A CSF is served only from a lumbar puncture (`source`); drain samples are not served.
  A non-policy first study after admission + 48 h is not served.
- decision 45: a grid row shortened by de-identification serves only the cells before its first blank, marked
  "(remaining cells not attributable)"; cells after the first blank are not recovered by column position (not an error).
- decision 46: the EEG `limitations` states the ED medications given before an inpatient EEG; inpatient infusions only when
  timed before the recording.
- decision 47: repeat lab values are withheld only for analytes a treatment changes (insulin/dextrose: glucose, potassium;
  red cells: haemoglobin, haematocrit; platelets; plasma/vitamin K: INR, PT, PTT); repeat blood gases and drug levels are never served.
- decision 48: rejected labels from the templates (one third when half gives none; SE also its mimics).
Severity: `error` = served content that is wrong, leaking, misattributed, from the wrong time, or a required item wrong or
missing. `minor` = cosmetic/formatting, an omission of a non-core intact item, a faithful source inconsistency, or a settled
rule above; every minor finding carries a one-line reason why it is minor.
- decision 23 (first values): insulin/dextrose withholds the first glucose only; potassium is withheld only for repeat values (decision 47).
  A first value of an analyte not listed in decision 23 (calcium, potassium after KCl, albumin) is served (settled, not an error).
- repeat lab values: the whole blood-gas sample (lactate included) is withheld from the repeats.
- SAH: aneurysmal knowledge-tool criteria come from the condition's templates (decision 28) even for an I60.8 case (settled).
- grids (decision 45, conservative): a row shorter than its header with no blank of its own is not attributable (the missing cell may be
  anywhere) and is not served; position is trusted only when every row of the grid fits the header (settled, not an error).
- vitals: the ED triage / vitalsign record; when it holds fewer than 3 values, the admission exam's vitals line of the note (blanked values empty).
- CSF: results the note states for the same first LP (appearance, opening pressure with its unit, named special tests) are served as
  note-extracted fields; results of a prior admission's LP, a repeat LP, a drain, pending results or values with a blank are not (settled).
- social history: served from the note's Social History section when intact; sentences holding a blank are left out (decision 16/27).
- decision 46 (as applied): the EEG statement lists the drugs of the ED medication record (pyxis) given before the recording; ED drugs
  that only the note mentions are not listed (the HPI often cannot be dated to this ED visit). Not an error when the note names more.
- brain + orbit MRI: `analyze_brain_mri` has an `orbits` protocol, so the orbit section of a combined brain/orbit report is part of the
  brain MRI answer (findings and impression); the MRA section of the same report answers the angiography order only.
- labs come from hosp/labevents only (first value per item in the window); a value the note quotes that is not in the table (e.g. a
  point-of-care or outside value) is not served, so the first served value may be a later draw than the note's (settled, not an error).
- brain imaging after a definitive procedure of the stay (coiling, embolization, thrombectomy, stenting, craniotomy) that is not a
  policy step is not served (initial or follow-up); a policy study keeps the first-result rule (decision 44).
- medications: the note's pre-admission list (parsed, or a verbatim reader extraction where the parse broke); held or stopped items and
  header lines are left out.
