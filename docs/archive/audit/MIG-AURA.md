# MIG-AURA — NeuroBench v5 audit

~30 cases audited (M01–M08, P01–P09, RM11, RS11, S01–S11, plus shared CONFIG/PACK-level items) — 108 findings total (0 blocker / 25 major / 54 minor / 29 nit); 27 fixed mechanically, 81 flagged for author/clinical judgment; validators pass (schema OK, coherence 0 on all edited cases).

## Terminology / taxonomy

| case_id | dim | severity | field path | finding | action | recommendation |
|---|---|---|---|---|---|---|
| MIG-AURA-P08 | terminology | major | ground_truth.icd_code | MELAS coded E88.49 ("other mitochondrial") instead of dedicated E88.41 | FIXED | Use E88.41 |
| MIG-AURA-M03 | terminology | major | ground_truth.icd_code | Hemiplegic migraine coded G43.109 (migraine w/ aura) instead of hemiplegic-migraine family G43.4- | FIXED | G43.409 |
| MIG-AURA-P09 | terminology | major | ground_truth.icd_code | Hemiplegic migraine coded G43.109 instead of G43.4- | FIXED | G43.409 |
| MIG-AURA-RM11 | terminology | major | ground_truth.icd_code | Sporadic hemiplegic migraine coded G43.109 instead of G43.4- | FIXED | G43.409 |
| MIG-AURA-RS11 | terminology | major | ground_truth.icd_code | Sporadic hemiplegic migraine coded G43.109 instead of G43.4- | FIXED | G43.409 |
| MIG-AURA-M05 | terminology | major | ground_truth.primary_diagnosis / key_reasoning_points | "Typical aura without headache" tagged ICHD-3 1.2.1.1 (= with headache); correct is 1.2.1.2 | FIXED | 1.2.1.2 |
| MIG-AURA-P03 | terminology | major | ground_truth.primary_diagnosis / key_reasoning_points / optimal_actions | "Migrainous infarction" tagged ICHD-3 1.4.1 (status migrainosus); correct is 1.4.3 | FIXED | 1.4.3 |
| CONFIG | terminology | major | conditions.yaml migraine_with_aura.name | Display name "Migraine with typical aura" is narrower than the actual case set (hemiplegic, brainstem, infarction, mimic subtypes) | FLAGGED | Rename to "Migraine with aura" to match enum/pack/case set (shared file — orchestrator edit) |
| MIG-AURA-P03 | terminology | minor | ground_truth.icd_code | Migrainous infarction coded I63.9 (unspecified infarct) instead of dedicated G43.6- | FLAGGED | Consider G43.609, optionally paired with I63.- |
| MIG-AURA-M06 | terminology | minor | ground_truth.primary_diagnosis | "Migraine with prolonged aura (>60min)" tagged ICHD-3 1.2.1 (typical aura requires 5-60min) | FLAGGED | Drop 1.2.1 tag or reconcile duration; clinician to decide |
| MIG-AURA-M01, MIG-AURA-M07 | terminology | nit | ground_truth.primary_diagnosis | "First-episode migraine with aura (ICHD-3 1.2.1)" — 1.2.1 requires ≥2 attacks | FLAGGED | Consider "probable migraine with aura (1.5.2)" framing for first-ever presentations |

## Audit findings

| case_id | dim | severity | field path | finding | action | recommendation |
|---|---|---|---|---|---|---|
| MIG-AURA-M03 | B internal-consistency | major | patient.pmh[2] vs ground_truth / labs | Elevated LDL 148 drives critical_action + red herring but PMH says "no hyperlipidaemia" and no lab output shows it | FLAGGED | Add lipid panel LabValue + fix PMH, or strip the LDL thread |
| MIG-AURA-M02 | B internal-consistency | major | patient.hpi | HPI says "no family history of stroke" then states father had stroke at 45; contradicted by family_history + 2 red_herrings + difficulty_description | FLAGGED | Remove/reword HPI clause; correct difficulty_description to "positive" |
| MIG-AURA-M03 | terminology | nit | ground_truth.primary_diagnosis / icd_code | "Sporadic hemiplegic migraine" cites parent code 1.2.3, not granular 1.2.3.2 | FLAGGED | Consider tightening to 1.2.3.2 |
| MIG-AURA-M01 | B internal-consistency | nit | ecg.rate vs ecg.findings[0] | Structured rate 72 vs narrative "70 bpm" | FLAGGED | Reconcile narrative to structured rate |
| MIG-AURA-M02 | B internal-consistency | nit | ecg.rate vs ecg.findings[0] | Structured rate 72 vs narrative "66 bpm" | FLAGGED | Reconcile free-text to structured rate |
| MIG-AURA-M01 | B internal-consistency | nit | eeg.background.overall vs eeg.impression | Background says normal PDR, impression calls EEG abnormal for posterior slowing not reflected in background text | FLAGGED | Optionally add slowing note to background.overall |
| MIG-AURA-M05 | C/B | major | followup_outputs[0].output.results[0].abstract | Literature abstract labels "typical aura without headache" as ICHD-3 1.2.2 (brainstem aura); contradicts case's own 1.2.1.2 | FIXED | Corrected 1.2.2 → 1.2.1.2 |
| MIG-AURA-M05 | B/C | major | ground_truth.red_herrings / critical_actions | LDL 132 and FSH/oestradiol referenced in gold text but no lab tool output contains them; labs say "within normal limits" | FLAGGED | Add lipid/hormone panel values or strip references |
| MIG-AURA-M04 | C clinical-correctness | major | ground_truth.differential[3].icd_code | Vertebrobasilar dissection coded I77.71 (carotid); dataset-wide convention across 5 cases | FLAGGED | Systematic fix: I77.71 → I77.74 or I67.0 for vertebral/basilar |
| MIG-AURA-M04 | B internal-consistency | minor | mri.impression vs mri.findings | Impression names WMH lesions; structured findings array empty | FLAGGED | Add finding object or drop clause |
| MIG-AURA-M05 | B internal-consistency | minor | mri.impression vs mri.findings | Same pattern — WMH named in impression, findings array empty | FLAGGED | Populate findings[] or trim impression |
| MIG-AURA-M06 | B internal-consistency | minor | mri.impression vs mri.findings[0] | Impression says "single" WMH, finding says "bilateral" | FLAGGED | Make impression/finding agree |
| MIG-AURA-M06 | B internal-consistency | minor | metadata.case_body_concerns / useless_tools | Metadata claims EEG dropped for no output, but EEG output exists and is correctly absent from useless_tools | FLAGGED | Remove stale line |
| MIG-AURA-M05 | B internal-consistency | minor | ground_truth.differential[0].key_features | TIA differential cites "5-year" aura history vs documented 20-year history elsewhere | FLAGGED | Change 5-year → 20-year |
| MIG-AURA-M05 | C clinical-correctness | minor | ground_truth.optimal_actions[1].category | check_drug_interactions tiered "recommended" vs "required" in pack/sibling cases | FLAGGED | Align tier or document rationale |
| MIG-AURA-M05 | E language/D realism | minor | followup_outputs[2].output.test_type | Ophthalmology exam mislabeled test_type="Electrophysiology" | FLAGGED | Rename to ophthalmology_examination/visual_field_perimetry |
| MIG-AURA-M04 | B internal-consistency | minor | ecg.rate vs findings[0] | Structured rate 72 vs narrative "74 bpm" (pattern across M04/M05/M06) | FLAGGED | Reconcile structured rate with per-case narrative |
| MIG-AURA-M04 | C/B | minor | followup_outputs[1] abstract vs contraindicated_actions | Literature says triptans "cautioned, not absolutely contraindicated" in MBA; ground truth says contraindicated | FLAGGED | Harmonize wording or note as deliberate tension |
| MIG-AURA-M05 | E language | nit | patient.hpi | Frequency stated as "twice monthly" then "2-3 per month" | FLAGGED | Harmonize frequency wording |
| MIG-AURA-M04 | D realism-leakage | nit | followup_outputs[5]/M06 followup_outputs[4] summary | Leakage detector flags condition-name mentions in population-keyed preventive-therapy text; judged benign | FLAGGED | No action — intentional/permitted |
| MIG-AURA-M07 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs report "sinus bradycardia 50 bpm" + HR 52 | FIXED | Set rate to 50 |
| MIG-AURA-M07 | clinical-correctness | minor | ground_truth.differential[0].icd_code | PRES coded G93.49 instead of dedicated I67.83 | FIXED | Use I67.83 |
| MIG-AURA-M07 | clinical-correctness | major | ground_truth.primary_diagnosis | "ICHD-3 1.2.1" applied to confusional aura, which is not a typical-aura symptom per ICHD-3; literature followup also mischaracterizes ICHD-3 as recognizing confusional aura | FLAGGED | Clinical review to re-label aura type or reword |
| MIG-AURA-M07 | clinical-correctness | minor | ground_truth.optimal_actions | Tool tiers (check_drug_interactions, analyze_brain_mri) diverge from pack and from sibling cases M08/P01 | FLAGGED | Reconcile tiering across batch |
| MIG-AURA-M07 | B internal-consistency | nit | metadata.case_body_concerns | Claims ECG/EEG/labs/monitoring/echo dropped, but all are populated in the case | FLAGGED | Regenerate stale metadata |
| MIG-AURA-M08 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs report "74 bpm" (both findings and interpretation) | FIXED | Set rate to 74 |
| MIG-AURA-M08 | D realism-leakage | nit | followup_outputs[1].output.summary | Leakage detector flags generic "migraine" mention in population-keyed summary | FLAGGED | No change — benign per style guide |
| MIG-AURA-M08 | D realism-leakage | nit | ecg.findings | Notes "QTc within normal range on sertraline" — legitimate cardiology QT concern, not cross-modality leak | FLAGGED | Acceptable as-is |
| MIG-AURA-P01 | B internal-consistency | major | patient.history_present_illness | HPI says "no hypertension" but PMH documents borderline HTN and red_herring design relies on vascular risk factors; vitals also support HTN | FLAGGED | Reconcile HPI vs PMH/red_herring/vitals |
| MIG-AURA-P01 | B internal-consistency | minor | ground_truth.red_herrings[1].intended_effect | Cites "prediabetes" with no supporting HbA1c data anywhere | FLAGGED | Remove reference or add supporting lab value |
| MIG-AURA-P01 | clinical-correctness | minor | ground_truth.optimal_actions[3] | Step expects ESR/CRP GCA-exclusion result, but labs output is an empty panel | FLAGGED | Populate labs panel with actual ESR/CRP/lipid/HbA1c values |
| MIG-AURA-P02 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs narrative "74 bpm" (x2) | FIXED | Set rate to 74 |
| MIG-AURA-P03 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs narrative "68 bpm" | FIXED | Set rate to 68 |
| MIG-AURA-P04 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs narrative "70 bpm" | FIXED | Set rate to 70 |
| MIG-AURA-P03 | C clinical-correctness | major | ground_truth.primary_diagnosis / patient.history_present_illness | "Migrainous infarction (1.4.3)" requires aura >60min; HPI documents a 20-minute fully-reversible aura, contradicting the case's own critical_actions criterion | FLAGGED | Revise HPI to prolong aura, or reconsider diagnosis |
| MIG-AURA-P03 | terminology | minor | ground_truth.icd_code | I63.9 used instead of dedicated G43.6- for migrainous infarction | FLAGGED | Consider G43.609 if diagnosis label retained |
| MIG-AURA-P03 | terminology | nit | ground_truth.differential[2].icd_code | "Cervical/vertebral artery dissection" coded I77.71 (carotid) instead of I77.74 (vertebral) | FLAGGED | Consider I77.74 |
| MIG-AURA-P02 | E language | nit | ecg.findings[0] | "Bilateral LA abnormality" is self-contradictory (LA = single chamber, left atrium) | FLAGGED | Reword to "left atrial" or "biatrial abnormality" |
| MIG-AURA-P02 | clinical-correctness | minor | ground_truth.critical_actions / HPI | CHA2DS2-VASc = 0 but patient started on apixaban; anticoagulation not guideline-indicated at score 0 | FLAGGED | Confirm intended teaching point (overtreatment) |
| MIG-AURA-P02 | B internal-consistency | nit | metadata.case_body_concerns | Claims EEG/labs/echo dropped for no output, but all are populated | FLAGGED | Regenerate/ignore stale note |
| MIG-AURA-P04 | A schema | nit | ground_truth.differential[1].icd_code | "Migraine without aura" differential has null icd_code while siblings are coded | FLAGGED | Optionally populate G43.009 |
| MIG-AURA-P05 | D realism-leakage | major | initial_tool_outputs.drug_interactions.warfarin.contraindications/warnings | Drug-check text announces the final diagnosis ("migraine with aphasic aura") and management once "migraine diagnosis is established" | FLAGGED | Reword to category-level guidance without naming diagnosis |
| MIG-AURA-P05 | B internal-consistency | minor | optimal_actions[3].tool_parameters vs followup_outputs[0] vs HPI | Requested 14-day ambulatory monitor vs delivered 48h Holter; also 24h/48h Holter references conflict | FLAGGED | Reconcile requested vs delivered monitoring duration |
| MIG-AURA-P05 | terminology | minor | metadata.case_body_concerns | Claims EEG/labs dropped for no output, but both are populated | FLAGGED | Regenerate stale note |
| MIG-AURA-P06 | D realism-leakage | minor | eeg.background.overall | Background attributes slowing to "small vessel disease pattern" — etiologic label outside EEG's modality | FIXED | Stripped " — small vessel disease pattern" |
| MIG-AURA-P06 | B internal-consistency | minor | ecg.rate vs findings/interpretation | Structured rate 72 vs narrative "68 bpm"; direction ambiguous vs sibling P05/P07 convention | FLAGGED | Align the two values (direction TBD) |
| MIG-AURA-P06 | terminology | nit | case_id | Mimic case (CADASIL) carries "P" tag rather than "R" (reverse/mimic) per pack §6 | FLAGGED | Awareness only; not renaming |
| MIG-AURA-P07 | D realism | minor | labs / followup_outputs[3] | Gold narrative relies on aCL/lipids/HbA1c results absent from any tool output (labs report "within normal limits", empty panels) | FLAGGED | Add supporting lab values or remove red herring |
| MIG-AURA-P07 | B internal-consistency | nit | followup_outputs[0].output.duration_hours vs optimal_actions[3] | Requested 365-day ILR vs delivered 720h (30-day) output | FLAGGED | Harmonize requested vs reported duration |
| MIG-AURA-P08 | B internal-consistency | minor | patient.demographics.bmi | Structured BMI 18.7 vs HPI "18.8" stated twice | FIXED | Aligned to 18.8 |
| MIG-AURA-P08 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs report/interpretation "68 bpm" | FIXED | Set rate to 68 |
| MIG-AURA-P09 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs report "sinus bradycardia 60 bpm" + vitals HR 62 | FIXED | Set rate to 60 |
| MIG-AURA-P08 | B internal-consistency | major | ecg.findings[0] | ECG text states two different PR intervals (156ms then 148ms) and mislabels normal PR as "short" (short PR is <120ms) | FLAGGED | Pick one PR value; correct short-PR distractor logic |
| MIG-AURA-P08 | B internal-consistency | minor | ground_truth.optimal_actions[3].expected_finding | Expects "characteristic MELAS pattern" MRI lesions; actual initial MRI is entirely normal | FLAGGED | Reconcile expected_finding with normal interictal MRI |
| MIG-AURA-P08 | B internal-consistency | minor | ground_truth.optimal_actions[5] | Recommends MRS expecting lactate peak; no MRS output exists, fallback is a normal MRA | FLAGGED | Add MRS output showing lactate peak or downgrade expectation |
| MIG-AURA-P08 | terminology | nit | case_id | MELAS (true diagnosis) is pack §6 "R" (mimic) type but case carries "P" prefix | FLAGGED | Leave case_id; awareness only |
| MIG-AURA-P09 | C clinical-correctness | major | followup_outputs[0].output.findings[0].description | PHASES score 4 coupled with "3.0% 5-year risk" is internally inconsistent; recomputed score from case facts is actually 3 (~0.7%) | FLAGGED | Recompute PHASES = 3, ~0.7%; revise treatment-risk comparison line |
| MIG-AURA-P09 | B internal-consistency | major | ground_truth.optimal_actions[3].tool_name | Required action names consult_medical_specialist but the delivering followup is keyed to order_specialized_test; no matching output for the named tool | FLAGGED | Make tool_name consistent with the delivering followup |
| MIG-AURA-P09 | B internal-consistency | minor | initial_tool_outputs.eeg | Classified "abnormal" with "posterior slowing" impression but PDR is 9-10Hz (normal, not slow) | FLAGGED | Reclassify as normal or specify genuinely slow PDR |
| MIG-AURA-P09 | C clinical-correctness | minor | ground_truth.icd_code | G43.409 (not intractable) vs two further episodes on propranolol — borderline intractability call | FLAGGED | Clinical reviewer to decide G43.409 vs G43.419 |
| MIG-AURA-P09 | D realism-leakage | nit | followup_outputs[2].output.summary | Leakage detector flags "hemiplegic migraine" in population-keyed literature text; judged benign | FLAGGED | Keep; optionally neutralize heading wording |
| MIG-AURA-P09 | A schema | nit | metadata.case_body_concerns | Claims EEG/labs dropped for no output; both are populated | FLAGGED | Regenerate stale note |
| MIG-AURA-RM11 | D realism-leakage | major | patient.clinical_history.medications[1].indication | Medication indication states "WHO Category 4 — must be stopped," pre-answering a gold critical_action | FLAGGED | Reduce indication to factual "Contraception" |
| MIG-AURA-RM11 | C clinical-correctness | minor | ground_truth.icd_code | G43.409 (not intractable) vs two failed preventives + ongoing frequent attacks — borderline intractability | FLAGGED | Clinical reviewer to decide G43.409 vs G43.419 |
| MIG-AURA-RM11 | D realism-leakage | minor | followup_outputs[1].output.recommended_actions[0] | MRA report includes management conclusion "No vascular intervention required" | FLAGGED | Drop or reduce to diagnostic statement |
| MIG-AURA-RM11 | B internal-consistency | nit | initial_tool_outputs.csf.cell_count | Empty cell_count object; differential relies on CSF excluding encephalitis but no WBC/RBC reported | FLAGGED | Add normal WBC 0-5/uL |
| MIG-AURA-RS11 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs narrative "68 bpm" | FIXED | Set rate to 68 |
| MIG-AURA-RS11 | B internal-consistency | major | patient.hpi / physical_exam / neurological_exam | HPI claims "headache-free and fully neurologically intact" but exam documents residual headache and a residual deficit; laterality also mismatched (right-sided episodes, left-sided residual finding) | FLAGGED | Reconcile HPI framing with exam findings and laterality |
| MIG-AURA-RS11 | terminology | minor | ground_truth.primary_diagnosis | "Sporadic hemiplegic migraine (1.2.3)" uses parent code instead of granular 1.2.3.2 | FLAGGED | Consider tightening to 1.2.3.2 |
| MIG-AURA-RS11 | C clinical-correctness | minor | followup_outputs[4].output.summary vs optimal_actions[1]/contraindicated_actions | Drug-interaction text softens triptans to "cautioned" contradicting case's contraindicated framing and FDA labeling | FLAGGED | Harmonize drug-interaction prose with contraindicated stance |
| MIG-AURA-S02 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs narrative "66 bpm" | FIXED | Set rate to 66 |
| MIG-AURA-S02 | terminology | nit | ground_truth.primary_diagnosis | "Menstrually-related (1.2.1)" — ICHD-3 menstrual subtype formally applies only to migraine without aura | FLAGGED | No change required; descriptive use acceptable |
| MIG-AURA-S01 | C clinical-correctness | nit | followup_outputs[3].output.summary | Literature states OCP is "WHO category 3-4" in migraine with aura; correct is Category 4 | FLAGGED | Optionally tighten to Category 4 |
| MIG-AURA-S04 | B internal-consistency | minor | metadata.difficulty_description | Labeled "Straightforward:" while enum/rationale both say "moderate" | FIXED | Relabeled to "Moderate:" |
| MIG-AURA-S05 | B internal-consistency | minor | metadata.difficulty_description | Labeled "Straightforward:" while enum/rationale both say "moderate" | FIXED | Relabeled to "Moderate:" |
| MIG-AURA-S05 | E language | minor | followup_outputs[1].output.summary | Literature followup returns empty query/results/summary, unlike siblings | FLAGGED | Populate with SNOOP/new-onset-aura summary or drop followup |
| MIG-AURA-S03 | C clinical-correctness | minor | followup_outputs[3].output.summary | Claims caffeine enhances sumatriptan absorption "(used in Cafergot preparation)" — Cafergot contains ergotamine, not a triptan | FLAGGED | Remove/replace Cafergot reference |
| MIG-AURA-S04 | D realism-leakage | minor | ecg.findings[0]/interpretation | ECG attributes LVH to "(Stage 1 HTN)" — cross-modality reference that should be stripped | FLAGGED | Drop HTN attribution, keep "LVH by voltage criteria" |
| MIG-AURA-S03 | B internal-consistency | nit | ecg.rate vs findings text | Structured rate 72 vs narrative "70 bpm" (pattern across S03/S04/S05) | FLAGGED | Reconcile structured rate with per-case narrative |
| MIG-AURA-S04 | C clinical-correctness | nit | ground_truth.differential[2].icd_code | PRES coded G93.49 instead of dedicated I67.83 | FLAGGED | Consider I67.83 |
| MIG-AURA-S03 | C clinical-correctness | nit | initial_tool_outputs.ecg / useless_tools / optimal_actions | ECG present but unaccounted for in optimal_actions/useless_tools/red_herrings | FLAGGED | Justify baseline ECG in optimal_actions or classify |
| MIG-AURA-S06 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs narrative "70 bpm" | FIXED | Set rate to 70 |
| MIG-AURA-S07 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs narrative "68 bpm" | FIXED | Set rate to 68 |
| MIG-AURA-S08 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs narrative "66 bpm" | FIXED | Set rate to 66 |
| MIG-AURA-S07 | B internal-consistency | major | ground_truth.key_reasoning_points[0] | Stroke-risk magnitude "6-9x" vs drug-interaction output "4-6 fold" for combined OCP + migraine with aura | FLAGGED | Reconcile to a single cited range |
| MIG-AURA-S07 | B internal-consistency | minor | ground_truth.useless_tools | Echo has a followup output (bubble study) but is absent from useless_tools; metadata falsely claims it was dropped for no output | FLAGGED | Add echo to useless_tools or correct metadata |
| MIG-AURA-S06 | B internal-consistency | nit | metadata.case_body_concerns[0] | Claims MRI/ECG/labs dropped for no output; all three populated | FLAGGED | Regenerate/correct note |
| MIG-AURA-S06 | C clinical-correctness | minor | ground_truth.differential[2].icd_code | "Postpartum PRES" coded G93.49 instead of dedicated I67.83 | FLAGGED | Consider I67.83 |
| MIG-AURA-S08 | C clinical-correctness | nit | ground_truth.differential[2].icd_code | "Cluster headache" coded G44.001 (intractable) with nothing establishing intractability | FLAGGED | Consider G44.009 |
| MIG-AURA-S10 | C clinical-correctness | major | HPI / social_history / primary_diagnosis / key_reasoning_points / metadata | MIDAS "18/27 (Grade IV)" is wrong on two counts: score 18 = Grade III (11-20), and MIDAS has no "/27" denominator; used pervasively across 6 fields | FLAGGED | Raise score to ≥21 to match Grade IV framing, or relabel Grade III and drop "/27" |
| MIG-AURA-S09 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs narrative "70 bpm" | FIXED | Set rate to 70 |
| MIG-AURA-S11 | B internal-consistency | minor | ecg.rate | Structured rate 72 vs narrative "76 bpm" | FIXED | Set rate to 76 |
| MIG-AURA-S11 | clinical-coding | major | ground_truth.differential[0].icd_code | MOH differential coded G44.41 (intractable) but case documents only borderline overuse expected to respond to withdrawal | FLAGGED | Recommend G44.41 → G44.40 |
| MIG-AURA-S11 | B internal-consistency | minor | ground_truth.differential[0].key_features | Claims co-codamol alone meets ≥10-day MOH threshold; documented use is 6-8 days/month (threshold only met combined with rizatriptan) | FLAGGED | Reconcile wording and "high" likelihood with documented use |
| MIG-AURA-S11 | E language | nit | patient.clinical_history.medications[2].indication | Indication field editorializes "OVERUSE" in all caps | FLAGGED | Consider removing the annotation |
| MIG-AURA-S09, MIG-AURA-S10, MIG-AURA-S11 | B internal-consistency | minor | metadata.case_body_concerns[0] | Claims analyze_brain_mri dropped for no output; MRI is populated in all three cases | FLAGGED | Correct or drop from "dropped" list |
| PACK | terminology | nit | criteria_packs/MIG-AURA.md §8 [Charles_2017] | Citation key year (2017) mismatches actual publication year (2018) | FLAGGED | Shared pack file — off-limits to case-agent edits |

**Tally:** 30 cases audited · 108 findings (0 blocker / 25 major / 54 minor / 29 nit) · 27 fixed / 81 flagged · validators pass (schema OK, coherence 0 on all edited cases).
