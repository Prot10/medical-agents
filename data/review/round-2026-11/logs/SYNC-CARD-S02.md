# SYNC-CARD-S02

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-6-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: split followup_outputs[6] (brain MRI, trigger request_brain_mri, off-pathway: no MRI criterion, stop rule or sequence constraint names it) into a non-contrast study (contrast_used false, same slot and trigger) and the gadolinium study (contrast_used true, text unchanged, trigger request_brain_mri_with_contrast, followup[7] right after it). Plain copy: removed the observation 'No enhancing lesions on post-gadolinium sequences'; nothing else referred to gadolinium. No criterion changed: in syncope brain imaging, and gadolinium in particular, is not indicated without focal signs (ESC 2018; decision 2). Probe: plain order gets the plain copy (gad_text=n), contrast order the gadolinium study, in either order; perfect_agent -v passes.
- MRI-CONTRAST verified: checked the git diff against 393c547e (gadolinium copy byte-identical to the original apart from contrast_used true; no other field or follow-up changed), plain copy free of gadolinium keys, findings, observations and impression clauses and still consistent with its findings, contrast_used true/false per the decision with no stored gadolinium study left null, no MRI criterion (gadolinium not indicated in syncope, criterion-free off-pathway study), pathway order (plain and gadolinium studies adjacent, after the core cardiac work-up), case fallback MRI absent; mri_probe: plain and contrast orders served by the case in either sequence, never the library; perfect_agent -v and case_io check pass. No error found, nothing changed.

## Reviewer notes
Reviewer status: R2 approved | Approved before this round (R2, work/approved.txt): changed only for condition class defects (plan SYNC-CARD.md C3 AVOIDED-DECOY, D3), which are additive avoided-action labels.

| note id | ruling | what changed (field paths) |
|---|---|---|
| NB-87M:SYNC-CARD-S02:policy_verdict | NO-ACTION | Approval with no comment. Class C3 labels added (see Own findings). |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | `ground_truth.avoided_actions[8]` | Served exercise echo had no label while the exercise test is harm in symptomatic severe aortic stenosis: new `avoid-harm-exercise-echo`, harm, ESC/EACTS 2025 `[ESC_EACTS_2025_VHD]` (D4). | FIXED |
| C | minor | `ground_truth.avoided_actions[6]`, `[7]`, `[9]`, `[10]` | Served off-pathway reports without a label (class C3): `avoid-waste-electrophysiology-study` [ESC_2018], `avoid-waste-bubble-study`, `avoid-waste-emg-ncs` (known mild length-dependent diabetic neuropathy; fallback NCS), `avoid-waste-tee` (fallback). | FIXED |
| E | minor | `fallback_tool_outputs.specialized_test` (NCS) | Identical NCS numbers to RS03, RS05 and S01 (template carry-over in a decoy); kept per D3. Reported to the lead. | FLAGGED |
| A | minor | `metadata.last_revised`, `metadata.revision_reason` | Updated to 2026-11-17. | FIXED |

Checks: new entries match only their own calls and no criterion; each call is answered by the case's own report or case fallback; perfect_agent passes; test_case_guards pass; case_io check: no failure names the case. Driving must R7 left as is (plan C5 NO-ACTION).

## Changes
Approved case; Reviewer 2 asked for nothing. The only change is additive: the exercise echocardiogram is now labelled harm, like the exercise test, because exercise testing is contraindicated in symptomatic severe aortic stenosis (ESC/EACTS 2025), and the electrophysiology study, bubble study, nerve conduction studies and TEE, which the case answers when ordered but which play no part here, are labelled waste, as in the rest of the condition. No clinical text, criterion, sequence or stop rule changed.

## Verification
Pass 1: 0 errors found
Cosmetic (not counted): `avoid-waste-emg-ncs` rationale said "Known ... neuropathy", but no prior diagnosis is recorded; the neuropathy is an examination finding. Reworded to "... peripheral neuropathy on examination". The NCS decoy report had numbers identical to the other SYNC-CARD cases (template carry-over, flagged by the worker). The per-nerve values are now adjusted to this patient (age, height, severity on examination), with the same impression.
Pass 2: 0 errors found
- Checked the pass-1 changes: `avoid-waste-emg-ncs` rationale matches the exam (vibration mildly reduced at the great toes and medial malleoli, Achilles 1+) and history (type 2 diabetes). Fallback emg_ncs values (74 y, 171 cm) are plausible and slightly worse than the younger cases (sural 3 uV, tibial F 58 ms), motor studies within normal limits for age, quantitative_data equals the findings, impression unchanged. No change. perfect_agent -v ok, test_case_guards ok.
Pass 3: 0 errors found
- Nothing was changed after the last 0-error pass (no condition-audit or orchestrator entry). Checks only: perfect_agent -v ok, test_case_guards ok.
Pass 4: 0 errors found
- Nothing changed after the last 0-error pass. Checks only: perfect_agent -v ok, test_case_guards ok.
Pass 5: 0 errors found
- Nothing was changed after the last 0-error pass (pass 4; no condition-audit or orchestrator entry after it). Checks only: perfect_agent -v ok, test_case_guards -k ok. No change.
