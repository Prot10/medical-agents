# FTD-P06

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-10-search-medical-literature (optional); removed initial literature_search outputs: bvFTD with vascular comorbidity and AD biomarker exclusion; difficulty_rationale: literature mention dropped. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| c7e69332-678a-4770-9654-4c38d8e656f5 | FIXED (class LIT, commit 393c547e) | initial_tool_outputs.literature_search: FIXED by class LIT, commit 393c547e: the literature criterion and the stored literature output were removed; re-checked 16 Nov, the case has no search_medical_literature criterion, follow-up, initial or fallback output (initial_tool_outputs.literature_search and fallback_tool_outputs.literature_search are null). A literature query now gets the neutral library text. |
| 68b33e69-b2ac-473a-8e30-8b1fe479781b | FIXED | initial_tool_outputs.labs.panels.Chemistry: The four rows now carry a clinical significance: fasting glucose 156 and HbA1c 8.2% above the treatment target and relevant to vascular risk management; total cholesterol 221 raised and LDL 142 above target, supporting statin therapy (lipid follow-up, followup_outputs[5]). Must 2 already sets an individualised HbA1c target, blood pressure below 130/80 and a statin. CENTRAL display remark: the review app prints a null significance as 'none' (CENTRAL.md item 1). |
| d3084ce1-9828-4ef8-84b4-2745a47ff0a9 | FIXED (class LIT, commit 393c547e) | (target removed): FIXED by class LIT, commit 393c547e: the literature criterion and the stored literature output were removed; re-checked 16 Nov, the case has no search_medical_literature criterion, follow-up, initial or fallback output (initial_tool_outputs.literature_search and fallback_tool_outputs.literature_search are null). A literature query now gets the neutral library text. The criterion action-10-search-medical-literature no longer exists. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| B | major | followup_outputs[9] (order_performance_status) | Class C6: templated "no longer able to work or manage finances and household decisions without supervision" and "prompting needed", not documented in this history | FIXED: rewritten from the HPI; Karnofsky 70, ECOG 1 kept (financial management impaired by the repeated purchases) |
| C | minor | ground_truth.avoided_actions[avoid-waste-5-order-ct-scan].rationale, citations | Class C22: "CT lacks the resolution and lobar specificity" is wrong (Rascovsky 2011 accepts CT atrophy as imaging support) | FIXED: canonical C22 text (MRI available and preferred; a CT added to it duplicates imaging), citations [NICE_NG97], [SNLG_ISS_2024]; severity stays waste |
| C | minor | ground_truth.avoided_actions[avoid-waste-7-order-advanced-imaging].rationale, citations | Class C23: the rationale said FDG-PET "(or amyloid PET)" characterises the lobar pattern; amyloid PET answers the Alzheimer question | FIXED: canonical C23 text, citations [NICE_NG97], [Frisoni_2024] |
| B | minor | metadata.difficulty_rationale | Listed the optional items without the optional counselled genetics criterion (action-genetic-panel-optional) (found in verification pass 5) | FIXED: "..., and counselled genetic testing" |

## Changes
The literature steps were already removed (class LIT) and re-checked. The raised fasting glucose 156, HbA1c 8.2%, total cholesterol 221 and LDL 142 now carry a clinical significance (above target, relevant to vascular risk management, supporting a statin) instead of a blank that the review app shows as 'none'; must 2 already requires an individualised HbA1c target, blood pressure below 130/80 and a statin. The performance-status report was rewritten from the history (Karnofsky 70, ECOG 1), and the CT and perfusion MRI waste rationales were corrected. Checks: perfect_agent.py passes; test_case_guards and case_io check clean for this case.

## Verification
Pass 1: 0 errors found
- Checked: note rulings (LIT re-verified, C8 rows on glucose, HbA1c, total cholesterol and LDL with must 2 covering glycaemic target, blood pressure and statin), performance status against the history (finances impaired by the purchases is documented), CT and perfusion MRI rationales, no leakage, no em dashes; perfect_agent.py and test_case_guards pass. No change.
Pass 2: 0 errors found
- Checked: all 3 notes ruled (LIT re-verified; C8 rows on glucose, HbA1c, total cholesterol and LDL, with must 2 covering the HbA1c target, blood pressure and a statin; no other abnormal row left null); performance status matches the history (retirement, purchases, normal gait and no falls documented); CT and perfusion MRI rationales; no leakage; no em dashes; perfect_agent.py and test_case_guards pass. No change.
Pass 3: 0 errors found
- Checked: all 3 notes ruled and right; glucose, HbA1c, total cholesterol and LDL rows carry factual significance and must 2 covers the HbA1c target, blood pressure (138/86 against below 130/80) and a statin; no other abnormal row left null; performance status matches the history; no leakage; perfect_agent.py -v and test_case_guards pass. No change.
Pass 4: 0 errors found
- Checked again in full: all 3 notes ruled and right; glucose, HbA1c, total cholesterol and LDL significance agree with must 2 (HbA1c 8.2% above the 7-8% target, a statin); TSH normal on levothyroxine; metformin with eGFR 62 needs no change; FAS 18 identical in the battery and speech report; performance status matches the history; perfect_agent.py -v and test_case_guards pass. No change.
Pass 5: 1 errors found
- metadata.difficulty_rationale omitted the optional counselled genetics criterion (action-genetic-panel-optional) from its list of optional items; added. The rest checked clean: all 3 notes ruled and right; glucose, HbA1c, total cholesterol and LDL significance agree with must 2 (HbA1c target about 7-8%, BP below 130/80 against 138/86, statin indicated in diabetes at 63, never taken one); no abnormal row left null; performance status matches the history; no leakage, no new em dash; perfect_agent.py -v, test_case_guards and case_io check pass. Rulings unchanged.
Pass 6: 0 errors found
- Checked: every note ruled and the rulings right (field paths and follow-up indexes current); diff against 06b74446 re-read with the final case; no abnormal row left with a null significance; no new em dash; no literature remnant; no answer leakage in the patient block; perfect_agent.py -v and test_case_guards pass. No change.
Pass 7: 0 errors found
- Checked: all 3 note ids ruled and right. Glucose, HbA1c (initial labs) and total cholesterol, LDL (lipid follow-up, followup_outputs[5]) carry factual significance, consistent with the abnormal-values summary and with must 2 (HbA1c target about 7-8%, BP below 130/80 against 138/86, statin); eGFR 62 matches creatinine 1.0 at 63; CSF glucose ratio 94/156 computed correctly; performance status matches the history (no change in gait, no falls documented); genetics negative so must 0 without a definite clause is right; difficulty_rationale lists every optional criterion. No leakage, no new em dash. Served-output probe, perfect_agent.py -v, test_case_guards -k and case_io.py check pass. No change.
