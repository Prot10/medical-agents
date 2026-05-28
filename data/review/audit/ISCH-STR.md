# NeuroBench v5 audit — ISCH-STR (ischemic stroke)

Scope: all 20 `ISCH-STR-*` cases (M01–M03, P01–P03, RM01–RM03, RP01–RP03,
RS01–RS04, S01–S04). Method: full field-by-field read of every case against the
ISCH-STR criteria pack (AHA/ASA 2019; DAWN/DEFUSE-3; CADISS; Sanna 2014) and the
tool-report style guide; mechanical validators run on every case. Conservative fix
policy — only unambiguous mechanical errors fixed; everything requiring clinical
judgment flagged.

Per audit instruction, the following are KEPT (not stripped) as legitimate
within-modality conclusions: imaging infarct/territory naming + CTA/MRA occlusion and
dissection characterization; ECG atrial fibrillation; echo PFO/vegetation; literature
results stating population-level alteplase/thrombectomy evidence. Time-critical
sequence constraints (door-to-CT, tPA window, hard `order_ct_scan`→
`check_drug_interactions` tPA gate) verified clinically sound in every case.

Mechanical baseline (all 20 cases): coherence validator 0 issues, schema valid,
tool-vocab pass. Leakage detector: only ISCH-STR-S01 `search_medical_literature.summary`
flagged ("acute ischemic stroke" phrase) — population-keyed alteplase/thrombectomy
evidence, allowed by the style guide (Kind-2), NOT a case-specific verdict. No Kind-1
literature leaks found.

## Findings

| case_id | dim | severity | region.field path | finding | action | detail |
|---|---|---|---|---|---|---|
| ISCH-STR-S01 | B/C | blocker | patient.neurological_exam (motor/sensory/cranial_nerves/additional) + history_present_illness vs initial_tool_outputs.mri + ground_truth | LATERALIZATION CONTRADICTION: imaging + GT = LEFT MCA infarct (left M1/ICA-T occlusion); global aphasia fits left/dominant hemisphere — BUT all motor/sensory/gaze/face/HPI findings are LEFT-body (left hemiplegia, left facial droop, right gaze preference, left hemineglect, left extinction, tongue deviates left) = RIGHT-hemisphere pattern, the OPPOSITE of a left MCA stroke (should be right-sided deficits) | FLAGGED | added to metadata.case_body_concerns. Not auto-edited: touches the clinical story across HPI + multiple exam fields; fixing requires deciding lesion side vs body side. Most significant clinical flag in the set |
| ISCH-STR-M01 | B | minor | followup_outputs[2].output.duration_hours | `duration_hours: 1` contradicts its own narrative ("Twenty-four hour Holter monitoring", "847 in 24 hours", episodes spanning a 24h day) | FIXED | changed 1 → 24 (mirrors the 24h impression/events; consistent with the holter_24h monitor_type) |
| ISCH-STR-M03 | B | minor | followup_outputs[2].output.duration_hours | `duration_hours: 5` contradicts narrative ("approximately 20.5 hours of the 24-hour recording", "847 in 24 hours", "Twenty-four hour Holter monitoring") | FIXED | changed 5 → 24 |
| ISCH-STR-M03 | B | minor | patient.demographics.bmi vs clinical_history.past_medical_history | PMH lists "Obesity (BMI 31.2)" but demographics.bmi = 29.8 (overweight, not obese); 31.2 is a copy artifact (identical to M01) | FLAGGED | added to case_body_concerns. Not fixed: changing the number to 29.8 would leave the "Obesity" label clinically wrong (29.8 < 30); reconciling label + value is a judgment call |
| ISCH-STR-M01 | C | minor | followup_outputs[6].output.contraindications[0] | apixaban dose-reduction text says "This patient meets only one criterion (creatinine 1.52)" but the case's BMP creatinine is 1.4 mg/dL; 1.4 < 1.5 means the patient meets ZERO criteria, so even the conclusion's "one criterion" framing is off | FLAGGED | drug-interaction reasoning + internal numeric mismatch (1.52 vs 1.4); GT/output semantics, do-not-fix. Final dosing conclusion (standard 5 mg BID) is clinically fine |
| ISCH-STR-RM01 | E | minor | followup_outputs[6].output.interactions[1] | typo "rivarfaxaban" | FIXED | corrected to "rivaroxaban" |
| ISCH-STR-RP01 | B/C | major | ground_truth.differential[1].key_features | "Alcohol intoxication" key_features states "serum ethanol below threshold", but the case's ethanol is 2.3 per mille (clearly ABOVE the <0.5 threshold; narrative repeatedly says significant intoxication). Should read: patient was intoxicated, but persistent/worsening focal deficits + basilar occlusion exclude pure intoxication | FLAGGED | added to case_body_concerns. GT semantics — not auto-edited |
| ISCH-STR-S03 | C | major | patient.neurological_exam.cranial_nerves | "Conjugate right gaze deviation" in a LEFT MCA stroke with right hemiparesis — cortical gaze deviation is toward the lesion (should be LEFT/away from weak side). Wrong direction | FLAGGED | added to case_body_concerns. Rest of exam correctly right-sided; only gaze direction wrong. Compare S02 (correct: "Left gaze preference") |
| ISCH-STR-S04 | C | major | patient.neurological_exam.cranial_nerves + history_present_illness | "Conjugate right gaze deviation" (exam) and "right gaze preference" (HPI/EMS) in a LEFT MCA stroke with right hemiparesis — should be LEFT gaze. Wrong direction in both fields | FLAGGED | added to case_body_concerns. Rest correctly right-sided |
| ISCH-STR-S03 | E | nit | history_present_illness | "The daughter reports that he spoke to his mother on the phone at 09:00" — patient (age 55) speaking to his mother is implausible; likely a template slip (daughter spoke to the patient) | FLAGGED | added to case_body_concerns; minor narrative artifact |
| ISCH-STR-S01, S03 | A/info | info | metadata.case_body_concerns[0] | pre-existing concern claims `check_drug_interactions` (step 6) has no pre-generated output, but both cases DO have a check_drug_interactions followup_outputs entry — concern is now STALE | NOTED | left in place (removing is a metadata-semantics judgment); reviewer can clear |
| ISCH-STR-P01, P03 | A/info | info | metadata.case_body_concerns | stale concerns: P01 (check_drug_interactions) and P03 (check_drug_interactions, order_cardiac_monitoring, order_advanced_imaging step 11) all now HAVE followup outputs | NOTED | left in place |
| ISCH-STR-RM01, RM02 | A/info | info | metadata.case_body_concerns[0] | stale concern: order_cardiac_monitoring (step 9) now HAS a holter followup in both | NOTED | left in place |
| ISCH-STR-P02 | A/C | minor | metadata.case_body_concerns + followup_outputs | 3 listed concerns; 2 (check_drug_interactions, order_cardiac_monitoring) now stale (outputs exist), but `search_medical_literature` (required step 5) genuinely has NO followup output — agent receives only the generic literature fallback | FLAGGED | the lit-search gap is real and valid; reviewer should add a moyamoya-keyed literature followup |
| ISCH-STR-P03 | C | minor | ground_truth.optimal_actions step 8 vs followup_outputs echo | gold wants `echo_type: TEE` (TTE misses ~30% of vegetations in IE) but the provided echo followup reports as a TTE that already shows the 1.8 cm vegetation | FLAGGED | the vegetation is provided regardless; mild action/output modality mismatch |
| ISCH-STR-P03 | B | minor | followup_outputs[3].output (analyze_brain_mri) vs followup_outputs[7].output (order_advanced_imaging MRA) | two mycotic-aneurysm descriptions differ: brain-MRI says RIGHT MCA M2 fusiform 4 mm; MRA says LEFT MCA M3/M4 saccular 3 mm — different side/morphology/size | FLAGGED | could be two separate aneurysms in a multi-territory septic shower (plausible) or an inconsistency between two outputs meant to be the same lesion. Reviewer to confirm intent |
| ISCH-STR-P02 | B/C | minor | initial_tool_outputs.mri.impression | MRI impression states only "Multiple bilateral chronic watershed infarcts…" and omits the ACUTE left frontal opercular DWI lesion (finding #1) and the bilateral ICA/MCA flow attenuation present in its own findings | FLAGGED | within-modality impression completeness; may be deliberately understated to avoid leaking moyamoya — do-not-rewrite (voice/judgment) |
| ISCH-STR-RS01, S01, S03, S04, RS04 | D/B | minor | followup_outputs (order_ct_scan CTA).output.impression | recurring pattern in the cardioembolic/LVO + basilar cases: CTA `findings` include a "Large vessel occlusion" (M1 / ICA-T / basilar) but the CTA `impression` omits the LVO entirely, mentioning only incidental carotid atherosclerosis | FLAGGED | information is recoverable (LVO is in the structured findings AND named in the MRI impression), so not answer-loss; but a real CTA impression would lead with the LVO/thrombectomy target. Systematic realism quality issue; do-not-rewrite (within-modality voice) |
| ISCH-STR-RM01, RM03, RP02 | B | minor | followup_outputs (CTA / carotid_duplex).output.impression | within-modality impression omits the primary positive finding present in its own findings array: RM01 CTA impression skips the headline left ICA dissection; RM03 CTA impression skips left ICA dissection; RP02 carotid-duplex impression says "Normal left carotid… no atherosclerotic disease bilaterally" while findings show markedly elevated right ICA velocities (dissection) | FLAGGED | same impression-completeness pattern; do-not-rewrite |
| ISCH-STR-P01, RM02 | B | minor | followup_outputs (carotid_duplex / order_advanced_imaging).output | findings note an abnormal vertebral/vessel signal but the impression understates it (P01: left vertebral "dampened waveform" in findings, impression only states "Normal right vertebral"; RM02 minor) | FLAGGED | within-modality completeness; do-not-rewrite |
| ISCH-STR-RP01 | B | minor | followup_outputs (order_advanced_imaging, modality=carotid_duplex) | a TCD/vertebrobasilar study (basilar TCD high-PI, vertebral PSVs) is reported under `modality: carotid_duplex`; gold step 10 expects `transcranial_doppler`. Impression also omits the basilar high-PI finding | FLAGGED | modality-label vs content mismatch; do-not-fix (vocab is free-text-ish here, but reviewer may relabel) |
| ISCH-STR-RP03 | B | minor | ground_truth.optimal_actions step 9 vs followup_outputs cardiac_monitoring | gold step 9 specifies `monitor_type: event_monitor_30d` (cryptogenic) but the provided followup is a 48h `holter_24h` | FLAGGED | output is normal either way; action/output monitor-type mismatch |
| ISCH-STR-RP02 | C/E | minor | initial_tool_outputs.ecg.interpretation | ECG rate 86 + rhythm "Normal sinus rhythm" but interpretation closes "Mild sinus tachycardia may reflect…pregnancy" — 86 bpm is not tachycardia and contradicts the NSR call | FLAGGED | within-modality wording inconsistency; do-not-rewrite (interpretive text/borderline meaning) |
| ISCH-STR-RS02 | C | minor | ground_truth.critical_actions + contraindicated_actions vs HPI | tPA framing leans on "recent major surgery (within 14 days)" contraindication, but the aortic arch replacement was 6 weeks ago (outside the 14-day window). The drug-check output correctly notes "6 weeks…beyond the high-risk window but warrants caution" | FLAGGED | clinical-judgment nuance: at 6 weeks the strict 14-day tPA bar has passed; the dissection/aortic involvement may still argue against tPA. Reviewer to reconcile the recency framing |
| ISCH-STR-RM03 | B/info | info | ground_truth.primary_diagnosis + icd_code | by-design "reverse" case: final dx is "Left ICA dissection presenting with painful Horner syndrome — high stroke risk WITHOUT completed cerebral infarct" (icd I77.71, NOT I63.x); MRI explicitly shows no acute DWI | NOTED | coherent and intentional (a stroke-mimic/precursor under the ISCH-STR condition); reviewer should be aware an ISCH-STR case has a non-I63 final diagnosis |
| ISCH-STR-RS02 | B/info | info | ground_truth.icd_code | iatrogenic post-surgical dissection-stroke coded I97.811 (intraoperative/postprocedural cerebrovascular complication) rather than I63.x | NOTED | clinically defensible for the iatrogenic etiology; flagged for coding-consistency awareness |
| ISCH-STR (all 20) | A/B | info | followup_outputs[].output.monitor_type | every case uses `monitor_type: "holter_24h"` even when duration is 48h/72h or the report describes telemetry/30d monitoring; the enum lacks longer-duration keys | NOTED | consistent generator artifact; internally the impressions match the stated duration; not auto-edited |

## Cross-cutting positives (verified, no action)

- Hard tPA gate `order_ct_scan (non-contrast) → check_drug_interactions` present and
  correct in all 20 cases; LVO cases additionally gate thrombectomy on CTA. Door-to-CT
  primacy and "no tPA before CT excludes hemorrhage" in every critical/contraindicated
  action set.
- Wake-up / late-window logic sound: M01–M03 use DWI-FLAIR mismatch (WAKE-UP/EXTEND)
  correctly; FLAIR-positive ⇒ outside window. RP01 (basilar) and P-series correctly
  invoke DAWN/DEFUSE-3 / ATTENTION / BAOCHE thrombectomy windows.
- Sex-specific and pregnancy-adjusted lab reference ranges used appropriately (female
  Hgb 12.0–16.0 and HDL >50 in RM01/RM02/RS01; pregnancy ranges in RP02 — Hgb 11–14,
  Cr 0.5–0.9, fibrinogen/D-dimer/Protein S notes).
- Contrast caution for CKD (M01/M02/M03) and gadolinium-avoidance in pregnancy (RP02)
  correctly encoded in contraindicated_actions.
- KEPT within-modality conclusions verified appropriate: ECG atrial fibrillation;
  MRI/MRA/CTA dissection + infarct + LVO; echo PFO/ASA and IE vegetation (P03); CSF
  fallback normal; literature population-keyed (CADISS, CLOSE/RESPECT, WAKE-UP, VITT,
  ATTENTION/BAOCHE). No Kind-1 cross-modality synthesis or management prescription found
  in any tool report (drug-interaction outputs give legitimate category-level management
  only — e.g. sumatriptan-in-dissection contraindication RM03, moyamoya hemorrhage risk
  P02, IE tPA contraindication P03).
- S02 confirmed as the correctly-lateralized left-MCA template (left gaze preference,
  right deficits, right field cut, tongue right) — the standard against which S01/S03/S04
  gaze/lateralization flags were judged.
- Differentials verified likelihood-descending and enum-valid; off-pathway
  amyloid_PET/DaTscan/FDG_PET key_reasoning_points present and correct in every case.

## Tally

- Cases audited: 20 (all ISCH-STR-*), every field of every case read.
- Findings by severity: 1 blocker, 4 major, 16 minor, 1 nit, 7 info/noted.
  (Several rows group multiple cases; ~30 distinct case-level observations.)
- Fixed: 3 (M01 duration_hours, M03 duration_hours, RM01 rivaroxaban typo).
- Flagged (not fixed): the remainder — including 5 case_body_concerns appended
  (M03 BMI, RP01 ethanol-below-threshold, S01 lateralization, S03 gaze+HPI, S04 gaze).
- Self-verify: coherence validator 0 and schema valid on all 7 edited files; JSON
  well-formed; trailing newline + escaped-unicode convention preserved; only
  ISCH-STR-* files modified.

### Top clinical-correctness flags for human adjudication

1. **ISCH-STR-S01 — lateralization is internally incoherent**: left-MCA imaging + global
   aphasia vs entirely left-body (right-hemisphere) deficits. A left MCA stroke cannot
   produce left-body hemiplegia. Must be reconciled (likely flip body-side findings to
   right; flipping lesion side breaks the aphasia).
2. **ISCH-STR-S03 & S04 — wrong-direction gaze**: "right gaze deviation/preference" in
   left-MCA strokes with right hemiparesis; cortical gaze should deviate left (toward the
   lesion). Likely a simple left/right swap to correct.
3. **ISCH-STR-RP01 — factually wrong differential reasoning**: "serum ethanol below
   threshold" contradicts the case's 2.3-per-mille intoxication; the intended point is
   intoxication present but excluded by focal deficits + basilar occlusion.
4. **ISCH-STR-RS02 — tPA recency framing vs 6-week interval**: gold actions invoke the
   14-day surgical contraindication though surgery was 6 weeks prior; reconcile.
5. **ISCH-STR-P03 — two divergent mycotic-aneurysm descriptions** (R-M2-fusiform vs
   L-M3/M4-saccular): confirm whether two aneurysms or one inconsistency; and TEE-vs-TTE
   action/output mismatch.
6. **ISCH-STR-M03 BMI** (obesity label vs 29.8) and **M01 apixaban "creatinine 1.52" vs
   lab 1.4**: numeric self-contradictions in narrative/output text.
