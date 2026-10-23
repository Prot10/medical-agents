# October 2026 review round: the policy every agent follows

Andrea asked for every reviewer note to be resolved and for all 600 cases to be read and corrected
case by case, slowly and properly, with no shortcuts. This file is the shared contract. Read it
whole before touching a case. `PATTERNS.md` next to it is the catalogue of error classes the two
physician reviewers found; apply it to every case, reviewed or not.

Andrea, 24 Oct 2026: open questions are to be resolved "nel modo migliore per la qualità del
dataset". Decide every judgment call yourself, with current guidelines and verified sources, apply
it, and record the decision and its reason. Leave a question for Andrea only when the decision
needs information only Andrea has, and say exactly what is missing.

## What you are working on

- Cases: `data/neurobench/cases/{CASE_ID}.json`, schema v2
  (`packages/neuroagent-schemas/src/neuroagent_schemas/`: `case.py`, `patient.py`,
  `tool_outputs.py`, `evaluation.py`). 20 conditions x 30 cases.
- Reviewer notes: `data/review/round-2026-10/notes/{COND}.md` (and `.json`), with a stable id per
  note. Nine conditions have notes (ALS, ALZ-EARLY, BACT-MEN, GBS, GLIO-HG, HEP-ENC, ISCH-STR, SAH,
  SE); the other eleven were never reviewed.
- Your condition's plan: `data/review/round-2026-10/plans/{COND}.md` (written by the condition lead;
  workers follow it).
- References: `dataset-generation/criteria_packs/{COND}.md` (diagnostic criteria, work-up tiers,
  citation allow-list), `dataset-generation/TOOL_REPORT_STYLE_GUIDE.md` (report realism and answer
  leakage: the authority on what a report may say), `dataset-generation/POLICY_AUTHORING_GUIDE.md`,
  `dataset-generation/TOOL_PARAMETER_VOCABULARY.md`, `docs/benchmark/tool-contract.md`,
  `agent-platform/config/review/condition_tool_guidance.yaml` (the July 2026 tool review: the
  reviewers' tool-level comments for your condition and the answers given), and
  `dataset-generation/config/conditions.yaml` (the generation panel for your condition).

## How the harness uses a case (know this before you move anything)

- The agent sees only `patient` (demographics, chief complaint, HPI, history, medications,
  allergies, family/social history, neurological exam, physical exam, vitals). Nothing else is
  given upfront. `metadata` and `ground_truth` are never shown to the agent.
- `initial_tool_outputs.<tool>` is NOT given upfront: it is the result returned the first time the
  agent orders that tool. `followup_outputs[]` are returned for a later or more specific order,
  matched by the discriminating parameter (`modality`, `test_type`, `study`, `specimen`,
  `procedure`, `assessment_type`, ...) first, then by tokens of `trigger_action` against the call's
  arguments. `fallback_tool_outputs` answers an off-pathway order with a normal report; the
  benchmark library (`agent-platform/config/tools/fallback_library.yaml`) answers anything else.
- The review app shows `initial_tool_outputs` as "Initial workup" and `followup_outputs` in list
  order as "Diagnostic pathway, Step N". Reviewers read that list order as the clinical sequence,
  so it must BE the clinical sequence (see "Pathway order" below). The UI is being fixed centrally
  to show both in criterion order; do not rely on that.
- Scoring (`agent-platform/src/neuroagent/evaluation/policy_reward.py`): diagnosis (token match
  against `ground_truth.diagnosis.accepted`, or ICD code), required/recommended coverage of
  `action_criteria` (a call matches a criterion when its arguments include the criterion's
  `required_arguments`), tool accuracy, safety (`avoided_actions` of severity harm/contraindicated
  cap the score), waste, `sequence_constraints` (hard ones cap at 0.5), stop rule. The assessment
  recommendations are reported for physician review but carry no weight in the scalar.
- Tool vocabulary is closed (`agent-platform/config/tools/costs.yaml`). New terms added for this
  round, usable now: `order_advanced_imaging` modality `functional_MRI`, `DTI_tractography`;
  `obtain_tissue_diagnosis` molecular assays `CD20_IHC`, `EBER_ISH`, `SOX10_IHC`,
  `Melan_A_HMB45_IHC`; `perform_clinical_assessment` assessment_type `performance_status`;
  `order_body_imaging` study `lower_extremity_venous_duplex`; `order_specialized_test`
  `genetic_panel:hereditary_paraganglioma`. Anything else you need goes in your log under CENTRAL.

## Authority and rulings

1. **A reviewer note is a clinical ruling by a physician. Apply it.** Where it offers options
   ("either remove X or add Y"), choose the clinically better one and say which in the log. Where a
   note is factually wrong (cite the guideline and the exact reason), or no longer applies because
   the case already changed, do not apply it: log it DECLINED or ALREADY-FIXED with the evidence.
   Never silently skip a note. Notes refer to fields by the index the reviewer saw; find the target
   by content, since indexes may have moved.
2. **One note is a class, not an instance.** When a note names an error, look for the same error
   in every other case of your batch and fix it there too (and tell the lead if it spans the
   condition). The August per-condition rewrite copied defects across all 30 cases of a condition.
3. **Never change** `case_id` or `condition`. Do not change the labelled diagnosis
   (`ground_truth.diagnosis.accepted[0]`) or `icd_codes[0]` unless a reviewer rules the label
   wrong or it is not a real entity (e.g. a WHO name that does not exist); then correct the label
   within the same condition, log it, and list it under CENTRAL. Never hand-edit the synonym labels
   appended after `accepted[0]`: they come from `agent-platform/config/policies/diagnosis_synonyms.yaml`;
   a wrong synonym goes under CENTRAL. If the data cannot support the labelled diagnosis, fix the
   data (that is what the reviewers ask for); if even that is impossible, log BLOCKED.
4. **Treatment is never a tool call.** There is no treatment tool and no consult tool by design.
   Management (drugs, doses, procedures, referrals, specialist input, admission, monitoring
   frequency) lives in `ground_truth.assessment.required_recommendations` (the "musts") and
   `prohibited_recommendations` ("contraindicated"). A must should be specific, correct per the
   governing guideline, consistent with the patient's allergies, weight, renal function,
   pregnancy, interactions, and phrased so a physician can check it. Remove any action criterion
   that fakes a consult or a treatment through a diagnostic tool (e.g. `interpret_labs` labelled
   "hepatology consult") and turn it into a must. A tool output must not report the effect of
   management the agent has not been able to recommend yet (no "48 h after rifaximin restarted"
   panel, no ammonia drawn "to monitor response"), unless the HPI states that treatment already
   happened before the encounter.
5. **Literature search is not a clinical step.** Reviewer 1 ruled that a literature search must not
   appear as a clinical action in the patient's pathway, and Reviewer 2 found literature outputs
   that echo the scoring key or misstate guidelines. So: `search_medical_literature` criteria are
   `optional` at most (or removed); their stored outputs give general, correctly cited evidence,
   never the case's expected text, never patient-specific conclusions; their follow-ups go last in
   the pathway order. Nothing required or recommended depends on them.
6. **Drug-interaction checks** (`check_drug_interactions`) are `required` only when the case
   contains a concrete interaction, allergy or contraindication that changes management (the
   patient's own medication list against the drug the case needs, a documented allergy, renal or
   hepatic dosing); otherwise `recommended` or `optional`. The stored output must contain that
   real content (not an empty block whose summary repeats the expected text) and must agree with
   the allergies and medications in `patient`. In the pathway order it comes after the diagnosis
   is established, unless the interaction itself is diagnostic.
7. **The differential is the assessment-time view.** Each entry's likelihood reflects the whole
   case, including the results the pathway returns, and `key_features` says what supports or
   excludes it. An alternative the work-up excludes is `low` (or removed), not left `moderate` or
   `high`. A mimic the case raises (in a report, the history or a red herring) is in the
   differential or explicitly excluded.
8. **Guidelines.** Use the current guideline named in the criteria pack or by the reviewer (e.g.
   AHA/ASA 2026 for acute ischaemic stroke, WHO 2025 and NICE NG240 for bacterial meningitis,
   EANO / AIOM for glioma). Where two govern and diverge, say which governs this case and why in
   the rationale. A citation must exist and say what it is cited for; never invent thresholds.

## Pathway order, sequence and stopping

- Reorder `followup_outputs` so that list order is the order a good clinician would obtain those
  results: the diagnostic core first (the studies that establish or exclude the diagnosis and its
  mimics), then staging and confirmatory studies, then pre-treatment safety checks, then
  monitoring; literature searches last. Reordering is safe for the harness (matching is by
  parameters and triggers, not position) but re-run the perfect-agent check.
- Order `ground_truth.action_criteria` the same way: the review app numbers them as "Optimal
  actions 1..N" and reviewers read that list as the work-up sequence. Keep each `criterion_id`
  unchanged when you move a criterion (ids are referenced by sequence constraints and the stop
  rule); a new criterion gets a new descriptive id.
- Add `sequence_constraints` where the order matters clinically (imaging before LP when an LP
  could herniate, EMG before genetic testing in suspected ALS, non-contrast CT before CTA-guided
  decisions, ...). `hard` only when the reverse order is unsafe; `soft` otherwise. Both ids must
  exist.
- Stop rule: `required_before_assessment` lists the required criteria that must be done before the
  diagnosis can responsibly be submitted; `max_additional_actions` is a reasonable allowance.

## Answer leakage and realism (TOOL_REPORT_STYLE_GUIDE.md is the authority)

- The patient block must not contain results of studies the agent is supposed to order (timeline
  leaks: "MRI showed...", "CSF protein 62" in the HPI when that MRI or LP is a criterion), nor name
  the diagnosis or its decisive test result. Prior results from before the encounter are legitimate
  history only if the case does not also score ordering them.
- A tool report states what its modality shows. Kind 1 leakage (cross-modality synthesis,
  differential essays, management prescriptions, the integrated diagnosis from a non-confirmatory
  modality) must go. Kind 2 (a modality naming what it legitimately establishes) stays.
- Every report is internally consistent (impression vs findings; structured fields vs narrative;
  organism fields vs findings; `is_abnormal` vs reference range; units; laterality) and consistent
  with every other field of the case (age, sex, weight, side, timeline, allergies, medications).
- No template carry-over: sex-specific tests in the wrong sex, another pathogen's boilerplate,
  identical numbers across cases, sections that belong to another condition.

## How to edit

- Use the helper, never hand-write JSON with a text editor:
  ```python
  import sys; sys.path.insert(0, "/Users/andrea/Documents/medical-agents/data/review/round-2026-10/bin")
  from case_io import load, save
  case = load("GLIO-HG-RS01"); ...; save(case)   # validates the schema, canonical format, atomic
  ```
  Run Python with `uv run python` from `/Users/andrea/Documents/medical-agents`.
- After editing a case, run both checks and fix anything that names your cases:
  ```bash
  uv run python data/review/round-2026-10/bin/perfect_agent.py CASE_ID -v
  uv run python data/review/round-2026-10/bin/case_io.py check CASE_ID [CASE_ID ...]
  ```
  `perfect_agent.py` must pass: every required and recommended criterion is answered by the case's
  own pathway data, in an order that satisfies the sequence constraints, with no avoided action
  matching it, and a perfect trace scores 1.0. Use `-v` to confirm that each criterion receives the
  report that carries its expected evidence. `case_io.py check` runs the schema, the synonym guard
  and the whole test suite and prints only failures that name your cases or condition.
  `test_guidance_claims` is maintained centrally after the round: ignore it.
  `git diff -- data/neurobench/cases/CASE_ID.json` shows your change.
- Touch only the case files assigned to you and your own log. Never edit `costs.yaml`,
  `fallback_library.yaml`, `diagnosis_synonyms.yaml`, `conditions.yaml`, tests or code: request it
  under CENTRAL in your log.
- If you remove a tool the generation panel marks required, add
  `metadata.panel_required_exemptions[tool] = "<clinical reason>"`; if you add it back, remove the
  exemption.
- Do not add review notes to `metadata`; everything goes in the log.
- Fix errors; do not churn. Correct prose stays as it is. This matters most in cases a reviewer
  approved (SAH, SE and a few GBS, HEP-ENC, ISCH-STR cases): every change there sends the case
  back to re-review, so change an approved case only for a real error, and log why.
- English throughout, keeping the case's spelling convention. No em dashes in new text.

## The case log (one per case)

Write `data/review/round-2026-10/logs/{CASE_ID}.md`:

```
# {CASE_ID}
Reviewer status: R1 ..., R2 ... (from the notes file) | Approved before this round: yes/no

## Reviewer notes
| note id | ruling | what changed (field paths) |
| ... | FIXED / ALREADY-FIXED / DECLINED / BLOCKED | ... |

## Own findings
| dim (A schema, B consistency, C clinical, D leakage, E language) | severity (blocker/major/minor) | field path | finding | action (FIXED/FLAGGED) |

## Changes, in one paragraph a physician can read before re-reviewing

## CENTRAL (requests outside this file: vocabulary, synonyms, library, tests, UI)

## Open questions for Andrea (judgment calls you could not settle)
```

Every note id in the notes file for the case appears in the table. Every change you made appears
in either table. Be exact: a re-reviewer will use this log to check your work.
