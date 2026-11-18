# FEPI-TEMP-P03

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-4-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general; removed metadata.fallback_tool_kinds.literature_search. Any literature query is now answered by the neutral library text.

## Reviewer notes
| note id | ruling | what changed (field paths) |
|---|---|---|
| 944c307b-fa13-4eea-a39c-90ceb614bc6a | FIXED | The literature criterion was removed. Class LIT, commit 393c547e: no literature output (initial, follow-up, fallback) or literature criterion is left in the case; any literature query now gets the neutral library text. The stale metadata line describing a literature step was deleted as well. |
| 1328f06b-b6af-4382-be72-eb93c653bf39 | FIXED | The initial literature output was removed (now null). Class LIT, commit 393c547e: no literature output (initial, follow-up, fallback) or literature criterion is left in the case; any literature query now gets the neutral library text. (`initial_tool_outputs.literature_search`) |
| 982692f3-a754-4537-a504-91b05dc61629 | FIXED | Stereotactic and open biopsy of the right hippocampus are now avoided actions of severity harm (avoid-harm-stereotactic-biopsy, avoid-harm-open-biopsy, [ILAE_PNES_2013]): the known, unchanged hippocampal sclerosis needs no histology and the video-EEG shows the new events are functional seizures. A resection order is also labelled harm (avoid-harm-resection, [Kwan_2010]): the epilepsy has been controlled for 3 years and the new events are functional. The stored biopsy reports stay so an order still gets a coherent result. (`ground_truth.avoided_actions[5]`) |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| E | minor | metadata.case_body_concerns | Two generation-time lines were stale and false: the literature-step line (plan residue) and the drug-interaction line ("case body lacks an output", but an alprazolam interaction report is stored). Deleted; the ECG line left as is. | FIXED |
| B | minor | fallback_tool_outputs.eeg.background.posterior_dominant_rhythm | The 48-hour ambulatory EEG fallback said the alpha rhythm was "reactive throughout 5-day monitoring" (copied from the 5-day video-EEG). Now "9.5 Hz alpha rhythm, symmetric, well-organized and reactive". | FIXED |
| E | minor | fallback_tool_outputs.specialized_test.impression | "Mild Weakness" capitalised mid-phrase; now "Mild weakness". | FIXED |

## Changes
The literature step is gone (class LIT). Stereotactic and open biopsy of the right hippocampus, and resection, are now avoided actions of severity harm: the hippocampal sclerosis is known and unchanged, the new events are functional seizures on video-EEG, and the epilepsy has been controlled for 3 years, so there is no indication for tissue or surgery. Two stale generation notes in metadata.case_body_concerns were deleted; the ambulatory EEG fallback no longer mentions "5-day monitoring" and a capital letter in the neuropsychology fallback impression was corrected. Diagnosis, criteria, musts and stop rule are unchanged; perfect-agent check passes.

## Verification
perfect_agent.py FEPI-TEMP-P03 -v: ok (each criterion served its own stored report; probes of every lab order this case touched done). test_case_guards -k for the six worker cases: 54 passed. case_io check: schema OK, synonym guard OK; only failures are test_guidance_claims (FEPI ECG/video/labs/CT counts), maintained centrally (plan CENTRAL 5). No MRI edited (mri_probe not needed).
Pass 1: 1 errors found
- (E, minor) metadata.case_body_concerns: the remaining generation line "useless_tools entry for `analyze_ecg` dropped: tool output is provided up-front in initial_tool_outputs ..." is false (no tool output is given upfront; this case stores no ECG at all) and is process text shown to physicians, like the lines the worker already deleted. Deleted.
Re-run after the fixes: perfect_agent.py -v ok (each criterion served its own stored report); test_case_guards -k for the six cases: 54 passed.
Pass 2: 0 errors found
- Checked: three notes ruled (LIT x2, BIOPSY); biopsy side (right hippocampus) matches the HS; resection harm consistent with controlled epilepsy and functional events; no literature residue; stop rule ids exist; perfect_agent -v ok. No change.
Pass 3: 0 errors found
- Checked: every note id ruled (rulings file matches the notes); rulings correct against the plan and decisions; served answers probed for every lab criterion and the new panels (no capture of other orders); no literature residue; plain MRI free of gadolinium text where split; laterality, timeline, allergies and medications consistent; avoided actions do not match any required or recommended call; stop-rule and sequence ids exist; DDI outputs carry real content and agree with the patient. No change.
Re-run: perfect_agent.py -v ok for the six cases; test_case_guards -k for the six cases: 54 passed.
Pass 4: 0 errors found
- Checked: every note id ruled (rulings file and annotation count match the notes) and each ruling correct against the plan, decisions and governing guideline; diff against 06b74446 read in full with the final case; served answers probed for each criterion whose source perfect_agent prints as "?" (MRI, labs, CT, hCG) and no capture of other orders; mri_probe clean; no literature residue; no em dash in new text; laterality, timeline, allergies, medications, musts vs prohibitions vs avoided actions, differential vs final evidence consistent; stop-rule ids are required criteria and sequence ids exist; DDI outputs carry real content. No change.
Re-run: perfect_agent.py -v ok for the six cases; test_case_guards -k for the six cases: 54 passed.
Pass 5: 0 errors found
- Checked: every note id of the notes file has a ruling (rulings file and log table match); each ruling against the plan, decisions D1-D36 and the governing guideline; diff against 06b74446 read with the final case (patient, ground truth, stored reports); served answers probed for each criterion perfect_agent prints as "?" (MRI, CT, labs incl. hCG, osmolality/urine sodium, AED levels, prolactin) with no capture of other orders; mri_probe clean where split; automatism side ipsilateral to the focus with contralateral version/dystonia kept; musts vs prohibitions vs avoided actions (no avoided action matches a criterion); stop-rule ids are required criteria and sequence ids exist; DDI outputs carry real content, agree with allergies and medications and do not repeat other modalities' results; no literature residue; no em dash in new text. No change.
Re-run: perfect_agent.py -v ok for the six cases; test_case_guards -k for the six cases: 54 passed.
