# NeuroBench v5 audit — MIG-AURA (migraine with aura)

Auditor: neurobench-case-audit skill. Scope: all 29 `MIG-AURA-*` cases.
Mechanical validators run on every case: coherence = 0 for all 29; schema valid for all 29;
tool-vocab clean for all 29; leakage detector candidates judged per-case (all residual hits are
population-keyed `search_medical_literature` summaries or category-level `check_drug_interactions`
content — intentional/allowed, plus within-modality imaging differentials and confirmatory genetics).

Clinical note: migraine is an ICHD-3 clinical diagnosis; imaging/EEG are normal or incidental and
must NOT say "consistent with migraine." Verified: no tool report announces the migraine diagnosis.
Several cases are deliberate mimics (CADASIL, MELAS, cardioembolic stroke, migrainous infarction) —
flagged, not altered; their workups do distinguish the mimic.

| case_id | dim | severity | region.field | finding | action | detail |
|---|---|---|---|---|---|---|
| MIG-AURA-M01 | B | major | initial_tool_outputs.eeg.classification | `classification:"normal"` contradicts own impression "This is an ABNORMAL EEG due to: ... posterior slowing" (which is a documented GT red herring) and the parallel P-case convention (slowing ⇒ abnormal) | FIXED | set classification → "abnormal" to match impression text + P-case convention; impression/background prose untouched; coherence 0, schema OK |
| MIG-AURA-M02 | B | major | initial_tool_outputs.eeg.classification | Same `normal`/"ABNORMAL EEG" contradiction (impression names mild posterior slowing) | FIXED | set classification → "abnormal"; coherence 0, schema OK |
| MIG-AURA-M03 | B | major | initial_tool_outputs.eeg.classification | Same `normal`/"ABNORMAL EEG" contradiction (mild left posterior slowing) | FIXED | set classification → "abnormal"; coherence 0, schema OK |
| MIG-AURA-M03 | B | minor | ground_truth.red_herrings + followup drug review | Narrative/red-herring cite a specific "Elevated LDL 148" but `interpret_labs` is empty ("All values within normal limits", no panel) — referenced lab value absent from any structured output | FLAGGED | judgment; do not fabricate a lab panel |
| MIG-AURA-M03/M04/P03/RS11 | C | minor | ground_truth (triptan stance) vs case literature | Gold `critical_actions`/`expected_finding` say triptans/ergotamines "CONTRAINDICATED" in hemiplegic/brainstem migraine & migrainous infarction, but the case's own literature/drug-review followups say "cautioned (not absolutely contraindicated)" | FLAGGED | clinical-nuance tension; reasonable clinicians differ (absolute vs relative); do not edit |
| MIG-AURA-M05 | C | major | ground_truth.primary_diagnosis / followup literature | ICHD-3 code for "typical aura without headache" is given as 1.2.1.1 in the gold but the acephalic-migraine literature says "ICHD-3 code 1.2.2" (= brainstem aura); both differ from the correct 1.2.1.2 and from each other | FLAGGED | clinical-correctness; changing the diagnosis code is a judgment call — adjudicate |
| MIG-AURA-M05 | B | minor | ground_truth.red_herrings | Red herrings cite "Borderline LDL / LDL 132 / Elevated FSH and low oestradiol" but no lab output contains these values (`interpret_labs` empty) | FLAGGED | narrative references labs not present; do not fabricate |
| MIG-AURA-M06/M07/M08/P0x/S0x | B | minor | patient.vitals vs top-level vitals | Dataset-wide: `patient.vitals` is a generic default block (often 120/80, hr72, temp37.0) while top-level `vitals` carries the case-specific values matching HPI/exam (e.g. M03 134/84, M07 hr52 athlete, P06 136/82). Two divergent vitals per case | FLAGGED (systemic) | structural/harness question, not MIG-AURA-specific; rewriting vitals risks regression & touches clinical story |
| MIG-AURA-M07 | B | minor | initial_tool_outputs.ecg.rate vs findings/interpretation | Structured `rate:72` contradicts the report text "Sinus bradycardia 50 bpm (athlete)" / interpretation "bradycardia"; top-level vitals hr=52 | FLAGGED | `rate` is leave-untouched objective data per style guide; default-72 artefact |
| MIG-AURA-P01 | B | minor | patient.hpi vs patient.pmh | HPI states "no hypertension" but PMH lists "Mild hypertension — borderline (130-138/82)" and red_herring text references HTN | FLAGGED | internal story contradiction; do not rewrite clinical story |
| MIG-AURA-P01 | E | nit | ground_truth.red_herrings | Red-herring text references "prediabetes" not present elsewhere in the case | FLAGGED | minor narrative drift |
| MIG-AURA-P02 | D | minor | followup_outputs[4].output (alcohol literature) | Literature summary phrasing "GGT/ALT elevation consistent with alcohol-related hepatic stress" reads as patient-specific (no GGT/ALT in labs); should stay population-keyed | FLAGGED | borderline Kind-1 (case-specific assertion in a literature tool) |
| MIG-AURA-P04 | D | minor | initial_tool_outputs.mri.impression | MRI gives worded imaging differential "borderline CADASIL pattern... migraine-related WMH also possible; NOTCH3 testing required" | NOTED (intentional) | permitted Kind-2 imaging differential + further-diagnostic recommendation; not Kind-1 leakage |
| MIG-AURA-P04/P05/P08/P09/RS11/S0x | E | minor | followup literature/drug outputs | Inconsistent literature-output schema across dataset: some use `results:[{source,finding,evidence_level}]`, others `results:[{title,authors,year,summary}]`, others a top-level `report` key with no `query`/`results` | FLAGGED | format/quality inconsistency; schema validates; restructuring risks regression |
| MIG-AURA-P05 | B | minor | patient.hpi vs followups | HPI says "a normal 24-hour Holter"; subsequent cardiac-monitoring followup is "48-hour Holter" (and red_herring says 48h) | FLAGGED | minor numeric inconsistency |
| MIG-AURA-P05 | B | minor | initial_tool_outputs.labs / drug review | Supratherapeutic INR 3.8 (clinically central) appears only in narrative + drug review; absent from any structured lab | FLAGGED | consistent with stripped-labs convention but central value missing from labs |
| MIG-AURA-P06 | B/C | major | case_id/condition vs ground_truth.primary_diagnosis | MIMIC: `condition=migraine_with_aura` but gold = CADASIL (NOTCH3 R182C), icd I67.850 — gold answer is NOT migraine | FLAGGED (intentional mimic) | per criteria-pack §6; workup distinguishes via NOTCH3 + MRI pattern; verify, do not "fix" |
| MIG-AURA-P06 | D | minor | initial_tool_outputs.eeg.background.overall | EEG background notes "small vessel disease pattern" — etiologic attribution EEG cannot establish | FLAGGED | minor cross-modality creep; impression itself stays non-specific |
| MIG-AURA-P07 | B/C | major | case_id/condition vs ground_truth.primary_diagnosis | MIMIC: gold = cardioembolic right-PCA ischaemic stroke (paroxysmal AF on ILR), icd I63.4 — NOT migraine | FLAGGED (intentional mimic) | workup distinguishes via ILR PAF + infarct-size criteria; verify, do not "fix" |
| MIG-AURA-P08 | B/C | major | case_id/condition vs ground_truth.primary_diagnosis | MIMIC: gold = MELAS (m.3243A>G), icd E88.49 — NOT migraine | FLAGGED (intentional mimic) | workup distinguishes via mtDNA + lactate + hearing loss/short stature; verify, do not "fix" |
| MIG-AURA-P08 | E | nit | followup_outputs[0].labs (mitochondrial) | Pyruvate 0.14 (ref 0.03-0.10) labelled "borderline elevated" though frankly above range; L/P ratio exactly 20 vs ref "<20" called borderline | FLAGGED | soft descriptor; values otherwise internally consistent |
| MIG-AURA-P09 | B | minor | ground_truth.optimal_actions[3] vs followup | optimal_action step 4 uses `tool_name:"consult_medical_specialist"` but the matching followup delivers the neurovascular referral via `order_specialized_test` | FLAGGED | tool-reference mismatch (coherence validator tolerates); do not alter fallback routing |
| MIG-AURA-RM11 | B | minor | duplicate patient.vitals/neurological_exam vs top-level | Real-seed (PMC3420796) structure: two vitals blocks (numeric vs string) and two neurological_exam blocks; top-level `neurological_exam.sensory` is empty "" | FLAGGED | duplication artefact; not load-bearing |
| MIG-AURA-RM11 | B | minor | initial_tool_outputs.csf.cell_count | CSF `cell_count:{}` empty though interpretation lists OP/protein/glucose; no WBC/RBC reported | FLAGGED | real-seed gap; do not fabricate counts |
| MIG-AURA-RM11 | E | nit | red_herrings | Top-level red_herrings use `misleading_diagnosis` key (v2 format) vs `why_misleading` used by all other MIG-AURA cases | FLAGGED | format variant; schema valid |
| MIG-AURA-RS11 | B | minor | exam laterality | Episodic deficits are right-sided (left hemisphere) but residual exam sign is "left frontal" decreased pain sensation (opposite side); physical_exam says "left parietal headache" vs HPI "left occipital" | FLAGGED | minor lateralization/terminology drift (possibly source-derived) |
| MIG-AURA-S02 | D | minor | followup_outputs[5] (MIDAS) | `request_migraine_diary` delivered via `search_medical_literature` but content is a patient-specific MIDAS score computation, not population-keyed literature | FLAGGED | borderline Kind-1 (case-specific assessment in a literature tool); summary field stays generic |
| MIG-AURA-S05 | E | nit | difficulty vs metadata | `difficulty:"moderate"` but metadata.difficulty_description begins "Straightforward" | FLAGGED | minor metadata inconsistency |
| MIG-AURA-S07 | B | nit | OCP stroke-risk figure | followup drug review says combined-OCP risk "4-6 fold" but key_reasoning_points says "6-9x" (M01 also uses "6-9 fold") | FLAGGED | internal numeric inconsistency; both within literature range |
| MIG-AURA-S08 | E | nit | red_herrings | Red herring calls the aura "monocular visual symptoms" though HPI describes binocular cortical field aura (its own correct_interpretation clarifies it is cortical) | FLAGGED | minor terminology |
| MIG-AURA-S11 | D | minor | followup_outputs[0] (MOH) | `check_codeine_medication_overuse` via `search_medical_literature` contains patient-specific MOH risk verdict ("CURRENT PATIENT... AT RISK") | FLAGGED | borderline Kind-1; summary field stays population-keyed |
| MIG-AURA-S06/S11 | C | nit | interpret_labs.clinical_significance | A couple of routine lab values carry a `clinical_significance` string ("Within normal range") where the style guide prefers null for routine panels | NOTED | harmless; values/flags all correct |

## Tally

- Cases audited: 29 (M01-M08, P01-P09, RM11, RS11, S01-S11) — every field of every case read.
- Mechanical validators (all 29): coherence = 0; schema valid; tool-vocab clean.
- Findings by severity: major 7 (3 fixed EEG-classification; 1 ICHD-code mismatch flagged; 3 mimic case_id/gold flags); minor 17; nit 6; plus 2 NOTED (intentional, no action).
- Fixed: 3 (MIG-AURA-M01, -M02, -M03 — EEG `classification` "normal"→"abnormal" only).
- Flagged (not fixed): all remaining findings above.

## Top clinical-correctness flags for human adjudication

1. MIG-AURA-M05: ICHD-3 code for "typical aura without headache" is internally inconsistent — gold says 1.2.1.1, case literature says 1.2.2; correct is 1.2.1.2. Diagnosis-code change needed but is a judgment call (do not silently change the diagnosis).
2. MIG-AURA-P06 / P07 / P08: three intentional mimics (CADASIL, cardioembolic AF stroke, MELAS) carry `condition=migraine_with_aura` but non-migraine gold diagnoses/ICD codes. Confirm this prefixing is acceptable for the benchmark; workups correctly distinguish each mimic.
3. Triptan stance (M03/M04/P03/RS11): gold actions state absolute contraindication while the cases' own literature says relative ("cautioned"); decide which the benchmark should reward.
4. M03/M05: red-herring narratives reference specific abnormal labs (LDL 148, LDL 132, FSH/oestradiol) that do not exist in any structured lab output — decide whether to add the panels or soften the narrative.

## Self-verification

- Re-ran coherence (0) and schema (pass) on all three fixed cases.
- `git diff` confirms the only MIG-AURA files changed are M01/M02/M03, and the only line changed in each is the EEG `classification` value.
- Trailing newline and literal-unicode convention preserved in all three.
- Residual leakage-detector hits are intentional (population-keyed literature, category-level drug interactions, within-modality imaging differentials, confirmatory genetics) — not chased to zero.
