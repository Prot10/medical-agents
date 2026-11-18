# SYNC-CARD-S05

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-5-search-medical-literature (optional); removed 1 literature follow-up(s); removed initial literature_search outputs: general. Any literature query is now answered by the neutral library text.
- MRI-CONTRAST: split followup_outputs[4] (brain MRI, trigger request_brain_mri, off-pathway: no MRI criterion, stop rule or sequence constraint names it) into a non-contrast study (contrast_used false, same slot and trigger) and the gadolinium study (contrast_used true, text unchanged, trigger request_brain_mri_with_contrast, followup[5] right after it). Plain copy: observation 'No mass lesion or enhancing abnormality' -> 'No mass lesion', impression 'No acute infarction, hemorrhage, mass, or enhancing lesion.' -> 'No acute infarction, hemorrhage, or mass.'; the case fallback MRI has no gadolinium content and stays null; nothing else referred to gadolinium. No criterion changed: in syncope brain imaging, and gadolinium in particular, is not indicated without focal signs (ESC 2018; decision 2). Probe: plain order gets the plain copy (gad_text=n), contrast order the gadolinium study, in either order; perfect_agent -v passes.
- MRI-CONTRAST verified: checked the git diff against 393c547e (gadolinium copy byte-identical to the original apart from contrast_used true; no other field or follow-up changed), plain copy free of gadolinium keys, findings, observations and impression clauses and still consistent with its findings, contrast_used true/false per the decision with no stored gadolinium study left null, no MRI criterion (gadolinium not indicated in syncope, criterion-free off-pathway study), pathway order (plain and gadolinium studies adjacent, after the core cardiac work-up), case fallback MRI null-flag with no gadolinium content; mri_probe: plain and contrast orders served by the case in either sequence, never the library; perfect_agent -v and case_io check pass. No error found, nothing changed.

## Reviewer notes
Reviewer status: R2 approved (NB-87MF-FBTV-TPWE) | Approved before this round: yes

| note id | ruling | what changed (field paths) |
|---|---|---|
| NB-87M:SYNC-CARD-S05:policy_verdict | NO-ACTION | Approval, no comment. Class C3 additive labels applied (see Own findings). |

## Own findings
Approved case: changed only for the class defect C3, additive entries only.

| dim | severity | field path | finding | action |
|---|---|---|---|---|
| C | major | ground_truth.avoided_actions[6] | Stored exercise echo (followup[9]) unlabelled in symptomatic severe aortic stenosis, while the exercise test is harm. | FIXED: avoid-harm-exercise-echo, ESC/EACTS 2025 |
| C | minor | ground_truth.avoided_actions[7,8] | Served bubble study (followup[8]) and TEE (fallback echo) unlabelled. | FIXED: waste entries, plan C3 canonical rationales |
| B | minor | initial_tool_outputs.ecg | Interpretation mentions T-wave inversion in I, aVL, V5-V6 that the findings list does not (findings give ST depression, strain). Consistent with strain; not changed in an approved case. | FLAGGED |
| A | minor | metadata | last_revised and revision_reason updated. | FIXED |

## Changes
Approved case, changed only by adding safety labels for tests the case answers but that do not belong in this patient's work-up; no clinical text, criterion, must, stop rule or diagnosis changed. Ordering exercise stress echocardiography is now scored as harmful (symptomatic severe aortic stenosis, ESC/EACTS 2025, like the existing exercise-test label). Bubble study and TEE are labelled low-yield (waste). perfect_agent passes; test_case_guards clean.

## Verification
Pass 1: 0 errors found
- Checked: the approval note is NO-ACTION and the only changes are the plan's class C3 additive avoided entries (plus LIT and MRI-CONTRAST class changes); each new entry matches exactly one call pattern and no criterion, each served report it labels exists at the logged index, rationale facts agree with the case, citations are allow-list keys. No clinical text changed; no em dashes; perfect_agent -v, mri_probe and test_case_guards -k pass.
- Cosmetic (not counted): none.
- Condition auditor, 17 Nov 2026, blind leak pass: a check_drug_interactions output (served to any drug query, including a first call before any test) named the diagnosis before any echo ("in severe aortic stenosis", four outputs: contraindication, amlodipine interaction, titration warning). Now conditional on the examination: "if the ejection systolic murmur reflects a fixed left ventricular outflow obstruction", "with a fixed outflow obstruction, stroke volume cannot rise", "Until the murmur and the syncope are explained, introduce or titrate antihypertensives in small steps". Approved case: changed for a real leak only. perfect_agent, test_case_guards -k, case_io check clean.
Pass 4: 1 error found
- Checked the condition-audit change: all four drug outputs (initial, fallback, amlodipine and lisinopril follow-ups) now conditional on the murmur ('fixed left ventricular outflow obstruction'), no longer naming severe aortic stenosis; action-6 expected evidence (vasodilator caution, avoid nitrates and PDE5 inhibitors) still carried.
- B, metadata.revision_reason: read 'No clinical text changed.' followed by 'Drug-interaction outputs reworded...', a self-contradiction introduced by the audit (the same phrase was already removed in RS06). Removed 'No clinical text changed.'.
- Cosmetic (not counted): the exercise echo follow-up (avoided, harm) says 'Not performed in symptomatic severe aortic stenosis'; it also carries the resting valve data, which an echo legitimately establishes (Kind 2), so left as is.
- perfect_agent -v ok, test_case_guards ok.
Pass 5: 0 errors found
- Checked the pass-4 fix to metadata.revision_reason: 'No clinical text changed.' is gone; the text now lists the safety labels and the drug-output rewording, matching the avoided_actions entries and the condition-audit change logged above; no self-contradiction, no other field touched by it. perfect_agent -v ok, test_case_guards -k ok. No change.
