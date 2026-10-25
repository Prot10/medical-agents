# Brief: library normal reports that contradict a case (25 Oct 2026)

When a case stores no answer for an order, the MockServer's last tier is the benchmark library
(`agent-platform/config/tools/fallback_library.yaml`): the same normal report in every case. A
probe ordered all 332 advertised terms (every tool's discriminator value, every lab panel, every
CSF test) in every case; on average 263 of them reach the library. Most are harmless: a normal
result the case is consistent with (a normal HD gene test in an ALS case). Some contradict the
case: a normal amyloid PET in Alzheimer disease, normal RNS in myasthenia gravis, a normal HbA1c
in a patient on insulin, a normal ammonia in overt hepatic encephalopathy, a normal routine MRI
in a case whose only stored imaging is CT of an infarct. Your job is to find those and make the
case answer them correctly, deciding for dataset quality (decide, apply, record why).

## Input
Your group table (path in the prompt), per condition:
- `cases`: each case's primary label, past medical history and medications (truncated);
- `library_answered`: each term the library answers, with either the number of cases (when it is
  every case of the condition) or the list of cases.
Read the library's normal report for a term in `fallback_library.yaml` (or by calling
`MockServer(case).get_output(tool, params)` from a scratch script) before judging it. Open a case
when the table does not settle it.

## What counts as a contradiction
A library normal contradicts the case when a clinician reading the case would expect that test,
at that point, to be abnormal (or to show a stored finding), because of:
1. the diagnosis itself (the test is a standard confirmatory or characteristic test of the
   condition: amyloid/tau PET and FDG-PET in Alzheimer disease, DaTscan and MIBG in PD, RNS and
   single-fibre EMG in MG, VEP/OCT in MS with optic neuritis history, nerve conduction in GBS,
   CT perfusion in an acute LVO stroke, neuropsychology in dementia or HE);
2. the history and medications (diabetes on treatment -> HbA1c/glucose; CKD -> creatinine,
   eGFR; cirrhosis -> LFTs, albumin, INR, platelets, ammonia; warfarin -> INR; HIV -> HIV
   serology, CD4; known anaemia -> CBC; a prior stroke -> MRI shows an old infarct; atrial
   fibrillation -> ECG/Holter shows AF);
3. findings already stored in the case (a stored CT infarct means an MRI cannot be normal; a
   stored abnormal echo means a TEE cannot be entirely normal).
A normal report is fine when the case is consistent with it (mimic cases included: a normal
DaTscan is right in drug-induced parkinsonism; check each case, not only the condition).

## Fix
For every contradiction, store a case-specific report that is what that test would show in this
patient, written per `dataset-generation/TOOL_REPORT_STYLE_GUIDE.md` (no cross-modality
synthesis, no diagnosis it cannot establish, no management) and consistent with every other
datum of the case. Follow the serving rules in the skill
`/Users/andrea/.claude/skills/neurobench-case-serving/SKILL.md` and `docs/benchmark/tool-contract.md`
(where to store a variant so only that order gets it: the discriminator field, a case fallback
slot, or a follow-up). Leaks: the report must not repeat any criterion's `expected_evidence`
beyond what that test legitimately shows (guards in `agent-platform/tests/test_case_guards.py`).
Never change tiers, criteria, diagnosis or other outputs, and never make a stored criterion's
answer change (run the perfect agent).

## Map
Write `data/review/round-2026-10/plans/LIBRARY-group<N>-map.yaml` listing what the library must
never answer, for the guard test:

```yaml
COND:                      # condition prefix, e.g. ALZ-EARLY
  all_cases:               # terms that must be case-specific in every case of the condition
    - {tool: order_advanced_imaging, params: {modality: amyloid_PET}}
  cases:                   # case-specific terms (history- or finding-driven)
    ALZ-EARLY-M03: [{tool: interpret_labs, params: {panels: [HbA1c]}}]
  except: [ALZ-EARLY-P04]  # cases exempt from all_cases (mimics), with the reason in decisions
```

## Procedure
- Edit through `data/review/round-2026-10/bin/case_io.py` only; touch only your conditions' cases
  (three other agents edit the others now). Scratch scripts in your scratchpad subfolder, run with
  `uv run python -I`; never name a script after a stdlib module.
- After each case: `uv run python data/review/round-2026-10/bin/perfect_agent.py CASE` and the
  guards `uv run pytest agent-platform/tests/test_case_guards.py -q -k CASE`.
- Verify the map with a script: every listed (case, term) is now answered without the library.
- Append "## Library contradictions (25 Oct 2026)" to each changed case log; write
  `data/review/round-2026-10/plans/LIBRARY-group<N>-decisions.md` (per condition: terms judged
  contradictory and why; per case: reports added; doubts for the physicians).
- Do not commit. Report under 200 words: contradictions found per condition, reports added,
  terms left to the library on purpose, doubts.
