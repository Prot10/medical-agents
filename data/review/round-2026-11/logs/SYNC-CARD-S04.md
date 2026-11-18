# SYNC-CARD-S04

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-6-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: split followup_outputs[4] (brain MRI, trigger request_brain_mri, off-pathway: no MRI criterion, stop rule or sequence constraint names it) into a non-contrast study (contrast_used false, same slot and trigger) and the gadolinium study (contrast_used true, text unchanged, trigger request_brain_mri_with_contrast, followup[5] right after it). Plain copy: removed the observation 'No enhancing lesions post-gadolinium'; nothing else referred to gadolinium. No criterion changed: in syncope brain imaging, and gadolinium in particular, is not indicated without focal signs (ESC 2018; decision 2). Probe: plain order gets the plain copy (gad_text=n), contrast order the gadolinium study, in either order; perfect_agent -v passes.
- MRI-CONTRAST verified: checked the git diff against 393c547e (gadolinium copy byte-identical to the original apart from contrast_used true; no other field or follow-up changed), plain copy free of gadolinium keys, findings, observations and impression clauses and still consistent with its findings, contrast_used true/false per the decision with no stored gadolinium study left null, no MRI criterion (gadolinium not indicated in syncope, criterion-free off-pathway study), pathway order (plain and gadolinium studies adjacent, after the core cardiac work-up), case fallback MRI absent; mri_probe: plain and contrast orders served by the case in either sequence, never the library; perfect_agent -v and case_io check pass. No error found, nothing changed.

## Reviewer notes
Reviewer status: R2 approved (NB-87MF-FBTV-TPWE) | Approved before this round: yes

| note id | ruling | what changed (field paths) |
|---|---|---|
| NB-87M:SYNC-CARD-S04:policy_verdict | NO-ACTION | Approval, no comment. Class C3 additive labels applied (see Own findings). |

## Own findings
Approved case: changed only for the class defect C3 (a served test that is useless or unsafe for this patient with no label), additive entries only.

| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.avoided_actions[5] | Stored exercise echo (followup[10]) unlabelled in symptomatic severe aortic stenosis, while the exercise test is harm. | FIXED: avoid-harm-exercise-echo, ESC/EACTS 2025 |
| C | minor | ground_truth.avoided_actions[6..9] | Served EPS (followup[8]), bubble study (followup[9]), TEE (fallback echo), EMG/NCS (followup[11]) unlabelled. | FIXED: waste entries, plan C3 canonical rationales (EMG names the known diabetic neuropathy) |
| C | - | ground_truth.assessment.required_recommendations[6] | Driving "1 week after pacemaker implantation (ESC 2018)": correct package, NO-ACTION per plan C5/D8. | none |
| B | minor | (serving) | Coronary angiography/CTA, chest imaging and gait orders are answered by library normals (a normal coronary angiogram in an 82-year-old diabetic is plausible, not contradicted by the case). | FLAGGED, no change |
| A | minor | metadata | last_revised and revision_reason updated. | FIXED |

## Changes
Approved case, changed only by adding safety labels for tests the case answers but that do not belong in this patient's work-up; no clinical text, criterion, must, stop rule or diagnosis changed. Ordering exercise stress echocardiography is now scored as harmful (symptomatic severe aortic stenosis, ESC/EACTS 2025, like the existing exercise-test label). Electrophysiology study, bubble study, TEE and nerve conduction studies are labelled low-yield (waste). perfect_agent passes; test_case_guards clean.

## Verification
Pass 1: 0 errors found
- Checked: the approval note is NO-ACTION and the only changes are the plan's class C3 additive avoided entries (plus LIT and MRI-CONTRAST class changes); each new entry matches exactly one call pattern and no criterion, each served report it labels exists at the logged index, rationale facts agree with the case, citations are allow-list keys. No clinical text changed; no em dashes; perfect_agent -v, mri_probe and test_case_guards -k pass.
- Cosmetic (not counted): none.
