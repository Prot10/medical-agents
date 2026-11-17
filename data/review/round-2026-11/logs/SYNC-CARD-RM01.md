# SYNC-CARD-RM01

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-7-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: split followup request_brain_mri: the gadolinium study (contrast_used true, trigger request_brain_mri_with_contrast) is placed first as the core diagnostic study, the plain copy (contrast_used false) follows without T1_post_contrast, "No leptomeningeal enhancement" and the enhancement clauses of the impression (T2/FLAIR medullary lesion and measurements kept). action-3-analyze-brain-mri required_arguments {} -> {contrast: true}: a new brainstem lesion in suspected paraneoplastic rhombencephalitis needs gadolinium to separate inflammation from an infiltrative tumour or leptomeningeal disease (decision 2: encephalitis and tumour mimic; the criterion label already asks for contrast); no plain alternative, since the plain study cannot exclude the mimic. expected_evidence unchanged (the contrast report contains it).
- MRI-CONTRAST verified: plain copy free of gadolinium content (T1_post_contrast, leptomeningeal enhancement, enhancement clauses removed; impression numbering and measurements intact), gadolinium copy unchanged with contrast_used true, criterion contrast true justified (brainstem lesion, tumour mimic) and its expected_evidence ('faint enhancement') is in the contrast report it receives; mri_probe: plain, contrast and both orders in either sequence answered by the case (never the library), case fallback MRI consistent; no other field changed against 393c547e; perfect_agent -v passes. No error found in the case; removed the two duplicate copies of the worker's MRI-CONTRAST log line.

## Reviewer notes
Reviewer status: R2 needs_changes (scenario_plausibility, diagnosis) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| NB-87M:SYNC-CARD-RM01:policy_verdict | FIXED (relabel); move DECLINED | ground_truth.diagnosis.accepted[0]: "Syncope due to nocturnal central sleep apnoea with sleep-dependent asystole, driven by anti-Hu paraneoplastic brainstem encephalitis" -> "Hypoxic transient loss of consciousness from nocturnal central sleep apnoea with secondary sleep-related asystole, due to anti-Hu paraneoplastic brainstem encephalitis". This applies ESC 2018 Table 2: hypoxia, and cardiac arrest without spontaneous recovery, are not syncope. ground_truth.action_criteria[4].rationale (action-3-analyze-brain-mri) now says "indicated in this hypoxic loss of consciousness". No other ground-truth text used "syncope" for these events. The mimic labels stay: differential[7] "Vasovagal / sleep-related reflex syncope", the tilt avoided rationale, and rejected "reflex syncope". The move to another condition is DECLINED (no paraneoplastic condition exists; October Q1, plan D16). icd_codes[0] G13.1 and the synonym labels are unchanged. DiagnosisCriterion.matches was re-tested: the new label, "Hypoxic loss of consciousness from central sleep apnoea due to anti-Hu brainstem encephalitis" and "paraneoplastic central sleep apnoea" score; "obstructive sleep apnoea with bradyarrhythmia" and "sick sinus syndrome" do not. CENTRAL C1c records the label change. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | minor | ground_truth.avoided_actions (new avoid-waste-exercise-stress-test) | A stored exercise test report answered an unlabelled order. The events are sleep-related, not exertional (class C3). | FIXED: waste entry {order_specialized_test, test_type exercise_stress_test}, [Fletcher_2013]. |
| C | minor | ground_truth.avoided_actions (new avoid-waste-exercise-echo) | The case fallback echo is an exercise echo, and an exercise echo order was unlabelled (class C3, D4). | FIXED: waste entry {order_echocardiogram, echo_type exercise_echo}, [Fletcher_2013]. |
| B | minor | followup_outputs order | The optional whole-body FDG-PET (staging) sat after the two drug checks. | FIXED: moved to followup_outputs[8], right after the chest CT studies and before the methylprednisolone and IVIG checks. The exercise test, speech-language evaluation and cognitive screen stay last. |
| C | minor | followup_outputs[12], [13] (speech-language evaluation, cognitive screen) | Served with no criterion. They are left unlabelled by plan D27: the speech-language evaluation serves the dysphagia must R5, and the cognitive screen is harmless context. | FLAGGED (no change, D27). |

## Changes
The primary diagnosis no longer calls these events syncope. Following the reviewer and ESC 2018 (Table 2 excludes hypoxia, and cardiac arrest without spontaneous recovery, from syncope), it now reads "Hypoxic transient loss of consciousness from nocturnal central sleep apnoea with secondary sleep-related asystole, due to anti-Hu paraneoplastic brainstem encephalitis". The brain MRI rationale now describes the events as a hypoxic loss of consciousness. The case stays in the cardiac syncope condition as its neurological mimic, because no paraneoplastic condition exists in the benchmark. The ICD code (G13.1) and the accepted anti-Hu labels are unchanged. Two waste labels were added: the exercise test and the exercise echo, which the case answers with stored results, play no part in sleep-related apnoeic events. In the pathway list the optional FDG-PET now follows the chest CT studies, before the drug checks. No criterion, must, report or differential entry changed otherwise. The perfect-agent check passes.

## Verification
perfect_agent.py -v passes (each criterion receives the stored report carrying its expected evidence); case_io.py check: schema OK, synonym guard OK, no test failure names the case; test_case_guards.py -k <id> passes.

Pass 1: 0 errors found
- Checked: accepted[0] matches plan D16 exactly; no remaining ground-truth text calls these events syncope (only the mimic label, the tilt rationale on reflex syncope and the general ESC Class III statement); move DECLINED with October Q1; exercise test and exercise echo waste per plan C3; PET reorder; perfect_agent -v, test_case_guards -k and case_io check. Nothing changed.

Pass 2: 0 errors found
- Pass 1 found 0 errors and no condition-audit or orchestrator change follows it, so nothing was left unverified. Re-ran perfect_agent.py -v (passes) and test_case_guards.py -k (passes). Nothing changed.
Pass 4: 0 errors found
- No change after the last 0-error pass. perfect_agent.py -v passes; test_case_guards.py -k (64 tests for the 8 SYNC-CARD pass-4 cases) passes. Nothing changed.
