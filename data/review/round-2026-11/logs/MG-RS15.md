# MG-RS15

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-5-search-medical-literature (optional); removed initial literature_search outputs: myasthenia gravis. Any literature query is now answered by the neutral library text.
- Synonyms (orchestrator, 17 Nov): G70.01 (with exacerbation) is no longer an accepted code in this stable case (diagnosis_synonyms.yaml G70.00 entry, MG CENTRAL C4); the code is a weight-0 component.

## Reviewer notes
Reviewer status: R2 needs_changes (NB-87MF-FBTV-TPWE) | Approved before this round: no

| note id | ruling | what changed, field paths |
| --- | --- | --- |
| NB-87M:MG-RS15:policy_verdict | FIXED (swallow criterion CENTRAL C1) | RNS: ground_truth.action_criteria[1] (action-2-order-specialized-test) recommended, removed from stop_rule. ECG: new action_criteria[5] action-baseline-ecg; M1 in required_recommendations[1] (constipation clause kept). Thymectomy: required_recommendations[4] 'discuss' at 53 (Jacob 2025; ICG 2020), action_criteria[2] (action-4-order-body-imaging) rationale and citations [Jacob_2025][Narayanaswami_2021], key_clinical_evidence[4]; October Q22 'refer at 53' reversed (plan D6). Contra 1: prohibited_recommendations[0] = P1. Must 3: required_recommendations[2] = S1 (5-10 mg, +5 mg every 3-5 days to 30 mg) with azathioprine after TPMT/NUDT15 if needed; required_recommendations[3] = S5 (DEXA). Must 5 (SLT voice and swallow) kept as required_recommendations[5]. Swallow criterion: CENTRAL C1; speech battery labelled waste (avoided_actions[6]). |

## Own findings
| dim | severity | field path | finding | action |
| --- | --- | --- | --- | --- |
| C clinical | minor | ground_truth.avoided_actions[5] | Stored normal brain MRI answered no criterion and no label (C9, D10) | FIXED: avoid-waste-brain-mri, ABN trigger not met |
| C clinical | minor | ground_truth.avoided_actions[6] | speech_language_evaluation unlabelled (C9, D11) | FIXED: avoid-waste-speech-language-evaluation |
| A schema | minor | ground_truth.sequence_constraints[0..1]; followup_outputs | Old SFEMG reasons (C3); SFEMG before respiratory in the list | FIXED: Q1 reasons [Jacob_2025]; follow-ups RNS, respiratory, SFEMG, speech battery (waste, last) |
| C clinical | minor | ground_truth.action_criteria[3] (action-7-order-specialized-test) | Rationale cited Lawn 2001 (D8). Plan C11 lists RS15 for 'required (choking)', but the HPI says she denied choking, coughing and aspiration; there is no dysphagia, breathlessness or must acting on the values, so D18 keeps it recommended | FIXED rationale (Jacob 2025); tier kept recommended (deviation from plan C11, reason given) |
| C clinical | minor | ground_truth.assessment.prohibited_recommendations[2] | 'before AChR antibody testing and neurophysiology' (C2 consequence) | FIXED: '(and neurophysiology when serology is negative)' |
| C clinical | minor | ground_truth.assessment.required_recommendations[6] | No MG severity recording (D23) | FIXED: G1, MGFA IIb |
| E language | minor | metadata.difficulty_rationale, last_revised, revision_reason | Out of date | FIXED |
| C clinical | minor | ground_truth.diagnosis.icd_codes | G70.01 granted (D21) | CENTRAL C4 |
| E language | minor | metadata.vocab_gap | Engineering note in a field physicians see | FLAGGED (all 30 MG cases; lead) |
| - | - | literature | Class LIT: none left | checked |

## Changes
With AChR binding antibody 1.11 nmol/L the diagnosis is serological, so repetitive nerve stimulation is now recommended rather than required and no longer gates the assessment; the stored ECG (sinus 74/min, normal) is a recommended baseline before pyridostigmine. Respiratory function stays recommended: she has fatigable laryngeal and palatal weakness but denies choking, aspiration or breathlessness and has no dysphagia. The normal brain MRI and the speech and language battery are labelled waste (the ABN trigger for imaging is not met; the battery never assesses swallowing). SFEMG follows the core results, with constraint reasons that say what ABN 2025 says. Management: pyridostigmine after an ECG with the 360 mg/day ceiling (constipation and diarrhea advice kept); if symptoms persist, prednisone from 5-10 mg, raised by 5 mg every 3-5 days to 30 mg, with the warning about days 5-10 (the unsourced 'above 20 mg/day' prohibition became 'do not start at full dose at once'); screening before immunosuppression and steroid monitoring with bone densitometry; thymectomy at 53 is now to be discussed (ABN 2025 at 50-65; ICG 2020 recommends 18-50 and found no benefit at 50 or over), reversing the October 'refer at 53'; the SLT voice and swallowing assessment stays; MGFA IIb with a baseline MG-ADL. A scored swallow assessment needs a new vocabulary term (CENTRAL). Checks: perfect_agent.py -v ok. No MRI edited. Not an approved case. Literature (class LIT): none left.

## Verification
- 17 Nov 2026: perfect_agent.py -v ok; test_case_guards.py -k (MG-RS11..MG-RS16) 48 passed; case_io.py check: schema OK, synonym guard OK, no test failure names these cases.
- Pass 1: 0 errors found. Checked RNS tier and stop rule, ECG (rate 74 matches vitals), T2 thymectomy wording in must, rationale and key evidence, P1 and S1 (no significant bulbar weakness: no dysphagia, choking denied), S5, the respiratory tier kept recommended against plan C11 (the HPI denies choking, coughing and aspiration, so D18 gives recommended; reason accepted), waste labels for the normal brain MRI and the speech battery, C3 reasons and follow-up order, G1 IIb. perfect_agent.py -v ok; test_case_guards -k 48 passed; case_io.py check: no failure names these cases. No change.
- Pass 2: 0 errors found. Pass 1 found 0 errors and nothing was changed after it (no condition-audit or orchestrator entry), so nothing new to verify. perfect_agent.py -v ok (mediastinum_MRI contrast alternative answered by a fallback, the plan C-wide alternative, warning only); test_case_guards -k MG-RS11..MG-RS16 48 passed. No change.
- Pass 3: 0 errors found. Pass 2 found 0 errors and nothing was changed after it (no condition-audit or orchestrator entry), so nothing new to verify. perfect_agent.py -v ok (mediastinum_MRI contrast alternative answered by a fallback where flagged, warning only); test_case_guards.py -k (MG-RS11, RS13..RS16, S03, S04) 56 passed. No change.
