# MIG-AURA-P07

## Class changes
- LIT (literature search is not a clinical step; R1 ruling, ROUND_POLICY ruling 5 extended, Nov 2026 class 1): removed criterion action-1-search-medical-literature (optional); removed 1 literature follow-up(s). Any literature query is now answered by the neutral library text.

## Reviewer notes
Reviewer status: R1 in_progress (NB-KSC3-TWUA-QDTM) | Approved before this round: no

| note id | ruling | what changed (field paths) |
|---|---|---|
| 895b9b5c-0615-4187-846f-4bfe878abc30 | FIXED | Class LIT, commit 393c547e: the literature criterion and follow-up were removed; checked that the case contains no search_medical_literature criterion, follow-up or stored output. |
| a219ebf2-56f3-4001-8ab4-b169cd3310a4 | FIXED | Label now 'Ischaemic stroke in the right PCA territory, probably cardioembolic from paroxysmal AF found on an implantable loop recorder, occurring during a migraine episode; not migrainous infarction (an alternative cause is present); switch aspirin to DOAC'. The diagnosis must, the PFO prohibition, the migrainous-infarction differential, key evidence [0], red herring [0] and metadata.condition_name say 'probable mechanism', not proof. The DOAC must is unchanged (AF with stroke, CHA2DS2-VA 2). Field: ground_truth.diagnosis.accepted[0]. |

## Own findings
| dim | severity | field path | finding | action |
|---|---|---|---|---|
| B | minor | ground_truth.assessment.prohibited_recommendations[3] | 'atrial fibrillation explains the stroke' stated the mechanism as proven (class of note a219ebf2). | FIXED: 'unlikely to be causal when paroxysmal AF provides a probable mechanism' |
| B | minor | metadata.condition_name | 'Cardioembolic ... misdiagnosed as migrainous infarction' restated certainty. | FIXED: 'Probably cardioembolic ... initially labelled migrainous infarction' |

## Changes
The label and the diagnosis must now say the infarct is probably cardioembolic from the paroxysmal AF found on the loop recorder: migrainous infarction is not diagnosed because AF provides a probable alternative mechanism (ICHD-3 1.4.3 D), but a single 43-minute episode does not prove causation. The PFO prohibition, the migrainous-infarction differential, key evidence and red herring were reworded the same way. The DOAC must and the work-up are unchanged. The literature step had already been removed (class LIT).

## Verification
Pass 1: 0 errors found
Checked: both notes ruled; no remaining text states AF as the proven cause (label, REQ0, PRO3, differential, key evidence, red herrings); DOAC must unchanged; label scores with the matcher; perfect_agent and test_case_guards pass.
Cosmetic (not counted): metadata.difficulty_rationale 'as cardioembolic AF-related stroke' became 'as a probably cardioembolic AF-related stroke', in line with note a219ebf2.
Pass 2: 0 errors found
Checked: every note ruled and applied as the plan states; no literature output; no contradiction found between labels, musts, prohibitions, differential, key evidence and reports; perfect_agent passes; test_case_guards -k passes.
Pass 3: 0 errors found
Checked: both notes ruled; label, REQ0, PRO3, differential[0], key evidence[0], red herrings and metadata say probable mechanism; DOAC must and CHA2DS2-VA 2 unchanged and correct; HPI does not leak the loop recorder result; no literature output; perfect_agent passes; case_io check and test_case_guards -k pass.
Pass 4: 0 errors found
Checked: every note ruled and applied as the plan states; no literature output; labels, musts, prohibitions, differential, key evidence, red herrings and reports agree; no answer leakage in the patient block; perfect_agent passes; case_io check (no failure names the case) and test_case_guards -k pass.
