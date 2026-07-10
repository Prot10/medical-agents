# SE — NeuroBench v5 audit

30 SE cases audited (M01-M09, P01-P08, RS11, S01-S12). 118 findings (0 blocker / 25 major / 57 minor / 36 nit); 25 fixed inline, 93 flagged for reviewer judgment. Validators (schema, coherence, vocab) pass on all fixed cases.

## Terminology / taxonomy

| case_id | dim | severity | field path | finding | action | recommendation |
|---|---|---|---|---|---|---|
| SE-S02 | terminology | major | ground_truth.icd_code | Focal (right temporal/hippocampal sclerosis) SE coded G41.1 (absence SE), contradicting the documented focal seizure type | FIXED | G41.1 → G41.2 (focal SE) |
| SE-S07 | terminology | major | ground_truth.icd_code | Focal (right frontal, GBM) SE coded G41.1 (absence SE) | FIXED | G41.1 → G41.2 (focal SE) |
| SE-S09 | terminology | major | ground_truth.icd_code | Focal (left temporal) SE from carbamazepine toxicity coded G41.1 (absence SE) | FIXED | G41.1 → G41.2 (focal SE) |
| SE-S12 | terminology | major | ground_truth.icd_code | Faciobrachial dystonic seizure (anti-LGI1) SE coded G41.1 (absence SE); FBDS are focal, not absence | FIXED | G41.1 → G41.2 (or G41.8 if reviewer prefers "other") |
| SE-P03 | terminology | major | ground_truth.icd_code | Post-anoxic myoclonic SE coded G41.1 (absence SE); myoclonic SE is neither absence nor grand mal | FIXED | G41.1 → G41.8 (other SE) |
| CONFIG | terminology | nit | conditions.yaml status_epilepticus.icd_code | Canonical icd_code is G41.9 (unspecified) while every case uses a specific subtype code; acceptable as placeholder default, no cross-file contradiction found | FLAGGED | No change required; optionally document G41.9 as placeholder |

## Audit

| case_id | dim | severity | field path | finding | action | recommendation |
|---|---|---|---|---|---|---|
| SE-M01 | E | nit | initial_tool_outputs.labs.abnormal_values_summary[0] | Hu antibody titer rendered "1: 1000" instead of "1:1000" | FIXED | Normalized to "1:1000" |
| SE-M02 | B | major | initial_tool_outputs.labs.panels['AED Levels'][0] vs differential/red_herrings/optimal_actions/critical_actions | Levetiracetam 24 mcg/mL (ref 12-46, is_abnormal=false, therapeutic) contradicted by 5 ground-truth fields calling it "subtherapeutic" | FLAGGED | Set admission level <12 mcg/mL with is_abnormal=true (mirror SE-M03), or drop "subtherapeutic" framing from GT fields |
| SE-M01 | B | minor | ground_truth.optimal_actions[6] | Step 7 prose/expected_finding describe body CT (chest/abd/pelvis) but tool_parameters.modality is FDG_PET | FLAGGED | Reword action to FDG-PET staging, or accept FDG_PET as closest vocab token |
| SE-M01 | E | minor | followup_outputs[4].output.interpretation (analyze_csf) | Template artifact "(N/A PMN/N/A lymph)" in CSF interpretation | FLAGGED | Drop fragment or state "differential not reported" |
| SE-M03 | B | minor | ground_truth.useless_tools[4] | Rationale describes DaTscan/dopamine transporter imaging but tool_parameters.test_type='polysomnography' | FLAGGED | Rewrite rationale to justify polysomnography's uselessness in acute SE |
| SE-M03 | D | minor | followup_outputs[0].output.findings[1] (analyze_brain_mri) | MRI finding imports EEG conclusion "corresponding to NCSE focus" — borderline cross-modality | FLAGGED | Soften to within-imaging phrasing, drop NCSE attribution |
| SE-M06 | B | major | ground_truth.sequence_constraints[1] | before/after inverted relative to own stated reason (labs should precede drug-check per reason, but coded reversed) | FIXED | Swapped to before='interpret_labs', after='check_drug_interactions' |
| SE-M04 | B | major | initial_tool_outputs.eeg.background.symmetry | Right-hemisphere slowing attributed to chronic stroke, but patient's stroke is LEFT MCA; EEG's own impression attributes right-hemisphere GPDs to metabolic cause | FLAGGED | Correct laterality: left-sided chronic slowing, right-sided metabolic GPDs |
| SE-M05 | C | major | ground_truth.optimal_actions[6].tool_parameters.modality | Pelvic imaging for ovarian teratoma coded modality=MR_angiography (vascular study); no pelvic/body-MRI vocab key exists | FLAGGED | Record vocab_gap / extend closed vocab; don't silently keep MR_angiography |
| SE-M05 | D | minor | followup_outputs[0].output.findings[1].type | MRI finding type "Basal ganglia FLAIR signal — anti-NMDAR involvement" ascribes serologic diagnosis to imaging | FLAGGED | Soften to imaging-level statement |
| SE-M05 | E | minor | ground_truth.contraindicated_actions | Haloperidol avoidance duplicated (items 1 & 4), restated again in critical_actions | FLAGGED | Merge into one entry |
| SE-M04 | B | minor | ground_truth.optimal_actions[4] / critical_actions[2] | GT inconsistent on replacement AED: text says levetiracetam, trajectory switches to lacosamide; apixaban-induction claim unaddressed by followup | FLAGGED | Reconcile to one AED and align expected_finding with SIADH-focused followup |
| SE-M04 | B | minor | initial_tool_outputs.labs.abnormal_values_summary | Omits BUN 28 (H) and Glucose 142 (H), both is_abnormal=true and listed in interpretation | FLAGGED | Add both values or confirm intentional curation |
| SE-M04 | D | minor | initial_tool_outputs.labs.interpretation / reference_range | "SIADH" named inside routine-lab interpretation/reference text | FLAGGED | Reduce to pattern-level description without naming SIADH |
| SE-M06 | E | nit | metadata.difficulty_rationale | Says "8 required + 1 optional" but actual is 7 required/1 recommended/1 optional | FLAGGED | Correct count in prose |
| SE-M04 | E | nit | metadata.difficulty_rationale | Says "7 required + 1 optional" but actual is 5 required/2 recommended/1 optional | FLAGGED | Correct count in prose |
| SE-M09 | B | minor | initial_tool_outputs.eeg.findings[0].frequency | Ictal frequency stated 1.5-2.0 Hz vs impression + gold expected_finding both 1.8-2.5 Hz | FIXED | Set finding frequency to 1.8-2.5 Hz |
| SE-M09 | E | nit | fallback_tool_outputs.specialized_test.impression | Trailing semicolon "No abnormality identified;" | FIXED | Terminate with period |
| SE-M07 | E | minor | followup_outputs[3].output.impression | SSEP impression run-on, missing sentence break | FIXED | Insert period after "evaluated" |
| SE-M07 | C | minor | ground_truth.differential[0].icd_code | Myoclonic SE (post-anoxic) coded G41.1 (absence); should be G41.8 | FLAGGED | Change to G41.8 |
| SE-M09 | B | major | patient.neurological_exam | Left facial droop/arm drift (right-hemisphere signs) vs right hyperreflexia + right Babinski (left-hemisphere signs); possible unintended flip or Kernohan phenomenon | FLAGGED | Adjudicate laterality vs. document Kernohan explicitly |
| SE-M09 | D | minor | followup_outputs[2].output.findings[0].clinical_correlation | EEG cross-references surgical/AED management ("NCSE resolved post-SDH evacuation and AED treatment") | FLAGGED | Reduce to electrographic note only |
| SE-M09 | E | nit | followup_outputs[5].output.summary | "CHADS2-VASc" conflates two distinct scores | FLAGGED | Rename to CHA2DS2-VASc |
| SE-M08 | C | minor | ground_truth.optimal_actions[2].action | "Non-contrast head CT" characterizing ring-enhancement, but initial CT has contrast_used=true | FLAGGED | Reconcile contrast labeling vs enhancement claim |
| SE-M08 | B | minor | ground_truth.useless_tools[4].rationale | polysomnography parameter paired with DaTscan rationale | FLAGGED | Rewrite rationale for polysomnography |
| SE-M09 | B | minor | ground_truth.useless_tools[4].rationale | Same polysomnography/DaTscan mismatch | FLAGGED | Rewrite rationale for polysomnography |
| SE-P01 | B | minor | initial_tool_outputs.labs.abnormal_values_summary | "AST:ALT ratio >2:1" arithmetically false (124/82 = 1.5:1) | FIXED | Corrected to "~1.5:1" |
| SE-P01 | terminology | nit | metadata.difficulty_rationale | "11 required + 1 recommended" vs actual 9 required/3 recommended | FIXED | Corrected to "9 required + 3 recommended" |
| SE-P01 | E | nit | fallback_tool_outputs.specialized_test.impression | Trailing semicolon | FIXED | Changed to period |
| SE-P01 | D | minor | initial_tool_outputs.eeg.impression | "Benzodiazepine diagnostic trial" names drug class inside EEG report; borderline (Salzburg IIC maneuver) | FLAGGED | Soften to "diagnostic pharmacologic trial" or accept as legitimate |
| SE-P01 | C | minor | patient.clinical_history.past_medical_history | "NASH" labeled in patient with 6-8 drinks/day x20yr; NASH excludes significant alcohol use; HPI separately says "hepatic steatosis" | FLAGGED | Reconcile to alcohol-related steatohepatitis |
| SE-P01 | B | nit | patient.vitals.temp | HPI states 37.2°C, vitals object lists 37.4 | FLAGGED | Align values (clinically immaterial) |
| SE-P01 | B | minor | ground_truth.useless_tools[2] | polysomnography parameter vs DaTscan rationale (copy-paste) | FLAGGED | Rewrite rationale or change parameter |
| SE-P01 | B | nit | followup_outputs[5].output.search_medical_literature | anti-Hu/SCLC association stated as ">80%" in key_finding vs "75-80%" in summary | FLAGGED | Pick one figure (~80-85%) |
| SE-P02 | B | minor | initial_tool_outputs.labs.panels.AED Levels[0] | Lamotrigine 14.2 exceeds stated reference top of 3-14 yet is_abnormal=false | FLAGGED | Widen range to 3-15 to keep narrative consistent |
| SE-P02 | terminology | nit | metadata.difficulty_rationale | "7 required + 2 optional/recommended" vs actual 6 required/1 recommended/1 optional | FIXED | Corrected to "6 required + 2 optional/recommended" |
| SE-P02 | E | nit | fallback_tool_outputs.specialized_test.impression | Trailing semicolon | FIXED | Changed to period |
| SE-P02 | B | minor | ground_truth.useless_tools[4] | polysomnography parameter vs DaTscan rationale | FLAGGED | Align rationale or parameter |
| SE-P03 | C | minor | ground_truth.differential[1].key_features | "Hypothermia-induced burst-suppression" cited at 33°C but patient's TTM is 36°C | FLAGGED | Downgrade likelihood or correct temperature in mechanism note |
| SE-P03 | C | minor | patient.history_present_illness | "Sometimes malignant Lance-Adams syndrome" — LAS is classically the benign chronic form, not malignant | FLAGGED | Reword HPI musing |
| SE-P03 | D | minor | followup_outputs[0].output.eeg | Structured finding type "post_anoxic_MSE" and "drug-induced contribution excluded" import etiology/refutation claims EEG cannot establish | FLAGGED | Rename to electrographic pattern label; soften "excluded" |
| SE-P03 | E | nit | followup_outputs[2].output.specialized_test.impression | SSEP impression has dangling fragment after standard close, duplicating earlier facts | FLAGGED | Delete trailing fragment |
| SE-P03 | B | nit | fallback_tool_outputs.ecg | Drug-interaction note claims amiodarone prolongs PR to 240ms; fallback ECG shows normal PR 148/QTc 425 | FLAGGED | Reflect amiodarone effect in fallback ECG for coherence |
| SE-P06 | C | major | ground_truth.primary_diagnosis.icd_code + differential[0].icd_code | Sporadic CJD coded A81.01 (= Variant CJD); sporadic CJD is A81.09 | FIXED | Changed A81.01 → A81.09 in both fields |
| SE-P06 | terminology | minor | patient narrative (HPI/PMH/exam) | "Paris-Edinburgh criteria" for CJD does not exist; real frameworks are WHO 1998 / MRI-CJD Consortium (Zerr 2009) / CDC | FLAGGED | Replace with a real criteria set (patient narrative off-limits to mechanical edit) |
| SE-P06 | D | major | initial_tool_outputs.labs vs fallback_tool_outputs.csf vs optimal_actions[4] | CJD-confirmatory CSF markers (14-3-3, RT-QuIC, tau) embedded in interpret_labs, but the CSF tool an agent would order returns a generic normal fallback that contradicts them | FLAGGED | Relocate CSF assays into a real/populated CSF tool output |
| SE-P06 | C | nit | ground_truth.differential[2].icd_code | "Other prion disease (familial, variant)" uses A81.09; variant proper is A81.01, row bundles both | FLAGGED | Judgment call given bundled row; awareness only |
| SE-P05 | C | minor | patient.neurological_exam.cranial_nerves / HPI / key_reasoning_points[0] | Pupils 7mm bilateral mydriasis in OP poisoning; classic muscarinic sign is miosis, and case's own DUMBELS mnemonic lists miosis | FLAGGED | Defensible via nicotinic predominance; flag for clinician realism review |
| SE-P05 | D | nit | followup_outputs[3].output.results[0].key_finding + summary | Literature search names "organophosphate poisoning"; judged Kind-2 (agent-issued query, diagnosis independently confirmed) | FLAGGED | No change; documented judgment |
| SE-P04 | C | minor | ground_truth.optimal_actions[7],[9] | Echocardiogram/carotid duplex marked "recommended" though pack lists them as typically useless in SE; defensible given true stroke etiology | FLAGGED | Reconcile tier vs criteria pack |
| SE-P04 | B | nit | initial_tool_outputs.labs.panels.Coagulation[0] | PT/INR value "1.2 / mildly elevated post-tPA" mixes prose into numeric field; conflicts with is_abnormal=false | FLAGGED | Use clean numeric value; move qualitative note elsewhere |
| SE-P04 | B | nit | fallback_tool_outputs.csf.glucose_ratio | Generic CSF template glucose_ratio 0.6 implies serum glucose ~103, but case's actual serum glucose is 192 | FLAGGED | Low priority; template awareness only |
| SE-P07 | E | nit | fallback_tool_outputs.specialized_test.impression | Trailing semicolon "No additional abnormality identified;" | FIXED | Terminate with period |
| SE-P08 | E | nit | fallback_tool_outputs.specialized_test.impression | Trailing semicolon | FIXED | Terminate with period |
| SE-RS11 | E | nit | fallback_tool_outputs.specialized_test.impression | Trailing semicolon | FIXED | Terminate with period |
| SE-P07 | B | minor | ground_truth.useless_tools[4] | polysomnography parameter vs DaTscan rationale (systemic across SE cases) | FLAGGED | Orchestrator: batch-fix rationale template |
| SE-P08 | B | minor | ground_truth.useless_tools[4] | Same polysomnography/DaTscan mismatch | FLAGGED | Same batch-level fix |
| SE-RS11 | B | minor | ground_truth.useless_tools[4] | Same polysomnography/DaTscan mismatch | FLAGGED | Same batch-level fix |
| SE-P07 | C | minor | case_id / primary_diagnosis | Subtype letter "P" used but diagnosis is HE mimicking NCSE, which pack §6 assigns to "R" subtype | FLAGGED | Curator confirm intended subtype grouping |
| SE-RS11 | D | nit | initial_tool_outputs.labs.panels['Post-ictal Markers'] / followup_outputs[3] | Troponin 0.04 with ref "<0.04" flagged is_abnormal=false, sits exactly on boundary | FLAGGED | Set is_abnormal=true at boundary, or adjust reference string |
| SE-RS11 | C | minor | patient PMH/HPI | JME "diagnosed at age 26" atypically late for juvenile-onset epilepsy (classic 12-18) | FLAGGED | Clinician judgment on acceptability |
| SE-P07 | D | nit | followup_outputs[4].output.results[0].key_finding | Literature result mentions "hepatic encephalopathy"; judged Kind-2 (population-level evidence, not case verdict) | FLAGGED | No action; retain |
| SE-P08 | B | nit | initial_tool_outputs.labs.panels['Toxicology'] vs followup_outputs[5] | Isoniazid therapeutic range inconsistent across two panels (<5 vs 3-8) | FLAGGED | Harmonize the two reference strings |
| SE-S02 | B | major | differential[1]/optimal_actions[1]/red_herrings[0]/critical_actions[0] vs labs.panels.AED_Levels[0] | Lamotrigine 8.2 mcg/mL (ref 3-15, is_abnormal=false, mid-therapeutic) repeatedly labeled "subtherapeutic" across 4 GT fields | FLAGGED | Lower level to genuinely subtherapeutic value, or reword reasoning |
| SE-S02 | B | minor | initial_tool_outputs.labs.abnormal_values_summary[0] | Lists lamotrigine 8.2 and levetiracetam 42 as abnormal though both in-range and is_abnormal=false | FLAGGED | Move to neutral "notable values" note or drop |
| SE-S03 | C | minor | primary_diagnosis / key_reasoning_points[1] | Na 129 called "severe hyponatremia"; by 2014 guideline grading, 129 is moderate (125-129) | FLAGGED | Consider "symptomatic" or "moderate" hyponatremia |
| SE-S03 | C | minor | fallback_tool_outputs.ecg.findings[0]/interpretation | PR 194ms called "borderline first-degree AV block"; threshold is >200ms, 194 is normal | FLAGGED | Reword to "upper-normal PR" or raise value >200ms |
| SE-S03 | C | minor | initial_tool_outputs.eeg / optimal_actions[0].expected_finding | Left-predominant ictal activity with right delta slowing in patient with only a right MCA infarct substrate; post-stroke foci are typically ipsilateral | FLAGGED | Clinician confirm intended lateralization |
| SE-S01 | B | minor | ground_truth.useless_tools[4] | polysomnography parameter vs DaTscan rationale (boilerplate, recurs in S02/S03) | FLAGGED | Fix boilerplate globally |
| SE-S02 | B | minor | ground_truth.useless_tools[4] | Same polysomnography/DaTscan mismatch | FLAGGED | Global boilerplate fix |
| SE-S03 | B | minor | ground_truth.useless_tools[4] | Same polysomnography/DaTscan mismatch | FLAGGED | Global boilerplate fix |
| SE-S01 | E | nit | followup_outputs[4].trigger_action | Named "request_sah_guidelines" for an unrelated SE/JME/rhabdo literature query | FLAGGED | Rename to "request_se_treatment_guidelines" |
| SE-S01 | A | nit | metadata.difficulty_rationale | States "8 required tools" but actual is 5 required/3 recommended | FLAGGED | Update wording |
| SE-S06 | D | major | initial_tool_outputs.ct.findings[0].description / additional_observations[0] | CT report cites serum sodium value ("cerebral edema consistent with severe hyponatremia (Na 124)") — cross-modality synthesis | FIXED | Stripped lab attribution, kept imaging finding |
| SE-S05 | D | major | initial_tool_outputs.ct.additional_observations[1] | CT report cites thiamine lab ("Wernicke risk given low thiamine") — cross-modality synthesis | FIXED | Dropped lab-driven Wernicke attribution |
| SE-S05 | E | nit | fallback_tool_outputs.specialized_test.impression | Dangling semicolon, "only minor incidental finding" | FIXED | Punctuated as complete sentence |
| SE-S04 | B | minor | ground_truth.useless_tools[4] | polysomnography parameter vs DaTscan rationale, recurs identically in S05/S06 | FLAGGED | Orchestrator: align rationale dataset-wide |
| SE-S06 | D | minor | followup_outputs[0].output (check_drug_interactions).warnings | Recites patient-specific labs/vitals and announces diagnosis ("MDMA causes SIADH... dilutional hyponatremia (Na 124)") | FLAGGED | Reduce to interaction-level guidance without reciting labs/naming SIADH |
| SE-S06 | D | minor | initial_tool_outputs.eeg.findings[1].morphology | "Fast activity consistent with sympathomimetic toxidrome" — EEG naming a clinical toxidrome | FLAGGED | Reduce morphology to electrographic description only |
| SE-S05 | D | nit | initial_tool_outputs.ct.findings[2].description | "possible Wernicke" imaging read; borderline given CT insensitivity for Wernicke | FLAGGED | Clinician decide whether to soften |
| SE-S04 | B | nit | metadata.difficulty_rationale | "8 required + 1 recommended" vs actual 6 required/3 recommended | FLAGGED | Correct split |
| SE-S05 | B | nit | metadata.difficulty_rationale | "8 required tools" vs actual 6 required/2 recommended | FLAGGED | Correct split |
| SE-S06 | D | nit | followup_outputs[5].output (analyze_csf).opening_pressure | Inline causal attribution "mildly elevated from cerebral edema" — soft cross-modality note | FLAGGED | Trim to "22 cmH2O (mildly elevated)" |
| SE-S08 | C | major | differential[0].icd_code | Eclampsia coded O15.1 (complicating labor) but patient is 28wk antepartum, not in labor | FIXED | Changed O15.1 → O15.03 (third-trimester antepartum) |
| SE-S07 | B | major | chief_complaint / history_present_illness | States focal seizure in RIGHT arm, but right frontal focus + left-sided exam findings (Todd's, gaze) imply it should be LEFT arm | FLAGGED | Change "right arm" to "left arm" in CC/HPI |
| SE-S07 | C | major | ground_truth.harmful_tools | Empty despite LP being explicitly contraindicated (mass + midline shift); CSF followup output still provided | FLAGGED | Consider adding analyze_csf/LP to harmful_tools |
| SE-S07 | B | minor | initial_tool_outputs.ct.contrast_used vs optimal_actions[2] | CT has contrast_used=true with ring enhancement, but step labeled "Non-contrast head CT" per pack convention | FLAGGED | Reconcile contrast labeling |
| SE-S08 | C | major | ground_truth.harmful_tools | Empty despite LP contraindicated by HELLP coagulopathy (platelets 88); CSF followup still provided | FLAGGED | Consider adding analyze_csf/LP to harmful_tools |
| SE-S08 | D | minor | initial_tool_outputs.ct.findings[0].description / additional_observations | Non-contrast CT attributes pattern to "PRES from eclampsia" — etiologic inference beyond modality scope; impression itself clean | FLAGGED | Trim "-from eclampsia" from finding/additional_observations |
| SE-S08 | C | minor | differential[1].icd_code | PRES coded I67.4 (hypertensive encephalopathy); dedicated I67.83 exists | FLAGGED | Consider I67.83 |
| SE-S09 | B | minor | metadata.difficulty_rationale | "7 required tools" vs actual 5 required/2 recommended | FLAGGED | Correct to "7 tools (5 required + 2 recommended)" |
| SE-S09 | B | minor | patient.neurological_exam.cranial_nerves | Ictal gaze deviation "Left" is ipsilateral to left temporal focus and opposite right-sided clonic activity; contraversive gaze expected rightward | FLAGGED | Verify intended direction (likely "Right gaze deviation") |
| SE-S07 | E | minor | ground_truth.useless_tools[4].rationale | polysomnography parameter vs DaTscan rationale (systemic, recurs S08/S09) | FLAGGED | Systemic fix: align rationale to polysomnography |
| SE-S09 | D | nit | initial_tool_outputs.eeg.impression | Leak detector flagged "status epilepticus" in EEG impression; judged Kind-2 legitimate within-modality (electrographic SE) | FLAGGED | No action; intentional Kind-2 |
| SE-S07 | E | nit | fallback_tool_outputs.specialized_test.impression | Trailing semicolon, systemic across S07/S08/S09 | FLAGGED | Systemic cleanup |
| SE-S11 | B | major | HPI / chief_complaint / neurological_exam.additional | Dialysis-missed timeline self-contradictory: "yesterday" (CC/HPI) vs "4 days ago (Monday→Wednesday)" (HPI) vs "2 days" (exam) | FLAGGED | Pick one intended gap and align all three fields |
| SE-S11 | B | major | fallback_tool_outputs.ecg vs optimal_actions[3].expected_finding | Expected finding calls for peaked T waves/widened QRS (hyperkalemia pattern, K 6.8) but fallback ECG is entirely normal (QRS 86ms) | FLAGGED | Replace fallback ECG with hyperkalemia pattern |
| SE-S11 | D | major | initial_tool_outputs.ct.findings / additional_observations | Non-contrast CT names "uremic encephalopathy and hyponatremia Na 128" and "hypertensive leukoencephalopathy" — cross-modality synthesis citing labs; impression itself clean | FLAGGED | Strip lab references/etiologic diagnosis from findings/additional_observations |
| SE-S11 | terminology | minor | patient.neurological_exam.cranial_nerves | "Periorbital asterixis" is a nonstandard descriptor; asterixis is classically a wrist/limb sign | FLAGGED | Reword to limb-based asterixis or remove "periorbital" |
| SE-S10 | D | minor | followup_outputs[0].output.findings | ECG findings name "TCA + MDMA combined" — cross-modality synthesis with tox screen; borderline since interpretation field is clean and TCA already confirmed | FLAGGED | Optionally soften to "sodium-channel-blocker toxicity pattern" |
| SE-S10 | B | major | ground_truth.useless_tools[4] | polysomnography parameter vs DaTscan rationale (identical to S11/S12) | FLAGGED | Rewrite rationale or switch tool/parameters |
| SE-S11 | B | major | ground_truth.useless_tools[4] | Same polysomnography/DaTscan mismatch | FLAGGED | Align rationale with parameter |
| SE-S12 | B | major | ground_truth.useless_tools[4] | Same polysomnography/DaTscan mismatch | FLAGGED | Align rationale with parameter |
| SE-S10 | E | minor | ground_truth.contraindicated_actions | Near-duplicate phenytoin/antiarrhythmic contraindications listed twice each | FLAGGED | De-duplicate to one entry each |
| SE-S12 | E | minor | ground_truth.contraindicated_actions | Near-duplicate prednisone-taper contraindications | FLAGGED | Collapse to single statement |
| SE-S12 | C | minor | optimal_actions[5].citation | Immunotherapy-escalation step cited to [ESETT_2019] (an AED trial), unrelated to prednisone/IVIG/mycophenolate | FLAGGED | Use [Brophy_2012] or a more apt citation |
| SE-S10 | E | nit | fallback_tool_outputs.specialized_test.impression | Trailing semicolon | FIXED | Changed to period |
| SE-S12 | E | nit | fallback_tool_outputs.specialized_test.impression | Trailing semicolon | FIXED | Changed to period |
| SE-S12 | E | nit | abnormal_values_summary (labs / followup_outputs[3]) | LGI1/CSF antibody titers rendered "1: 64"/"1: 4" (stray space) vs canonical "1:64"/"1:4" | FLAGGED | Remove stray space (systemic formatter behavior) |
| SE-S10 | C | minor | differential[1].icd_code | MDMA coded T43.625A (other psychostimulant, adverse effect) rather than dedicated T43.64x (ecstasy) | FLAGGED | Consider T43.641A; verify poisoning-intent digit |

## Tally

- Cases audited: 30 (SE-M01–M09, P01–P08, RS11, S01–S12)
- Findings by severity: 0 blocker / 25 major / 57 minor / 36 nit (118 total)
- Fixed: 25 · Flagged: 93
- Validators: schema, coherence, and vocab all pass on fixed cases (validators_ok = true)
