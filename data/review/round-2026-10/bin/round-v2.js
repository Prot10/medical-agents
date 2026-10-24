export const meta = {
  name: 'neurobench-review-round',
  description: 'Fix every reviewer note and audit all 30 cases of each condition (lead plan, workers, adversarial verifiers, condition audit) ',
  phases: [
    { title: 'Plan', detail: 'one lead per condition surveys the 30 cases and the notes, writes the plan' },
    { title: 'Fix', detail: 'one worker per 6 cases reads every field, applies notes, plan and patterns' },
    { title: 'Verify', detail: 'one adversarial verifier per batch re-reads the diff and the final cases' },
    { title: 'Audit', detail: 'one auditor per condition checks consistency across the 30 cases' },
  ],
}

const ROOT = '/Users/andrea/Documents/medical-agents'
const R = ROOT + '/data/review/round-2026-10'
const COMMON = `You are part of a careful, slow, case-by-case correction of the NeuroBench dataset (repository ${ROOT}). Andrea (the PhD student who owns it) asked for every physician reviewer note to be resolved and every case to be read and corrected properly, explicitly preferring slow and correct over fast with residual errors. No shortcuts: read the actual files, reason clinically, verify your claims against the files.
First read, in full: ${R}/ROUND_POLICY.md (the contract: rulings, invariants, how to edit, how to check, log format) and ${R}/PATTERNS.md (the error classes the reviewers found). Follow ROUND_POLICY exactly. Work only through the shell and file tools yourself; do not spawn subagents. Run Python with \`uv run python\` from ${ROOT}.`

function leadPrompt(c) {
  return `${COMMON}

You are the LEAD for condition ${c.cond}. Its 30 cases: ${c.cases.join(', ')}.
You do not edit cases. You write the plan the workers will follow: ${R}/plans/${c.cond}.md.

Steps:
1. Read the references for ${c.cond}: dataset-generation/criteria_packs/${c.cond}.md, dataset-generation/TOOL_REPORT_STYLE_GUIDE.md, dataset-generation/POLICY_AUTHORING_GUIDE.md, dataset-generation/TOOL_PARAMETER_VOCABULARY.md, docs/benchmark/tool-contract.md, the ${c.cond} entries of agent-platform/config/review/condition_tool_guidance.yaml (find the condition's key by grepping), the ${c.cond} panel in dataset-generation/config/conditions.yaml, and the reviewer notes ${R}/notes/${c.cond}.md if that file exists (if it does not, this condition was never reviewed: your survey is the only safety net).
2. Survey all 30 cases with scripts: for each case extract the action criteria (id, tool, arguments, importance), followup order (tool, trigger), initial outputs present, musts, prohibitions, avoided actions, sequence constraints, stop rule, differential, red herrings, diagnosis label. Measure text shared verbatim across cases (the August rewrite copied text across all 30), and check every PATTERNS.md class at condition level (grep / small scripts). Run \`uv run python data/review/round-2026-10/bin/perfect_agent.py <the 30 ids>\`.
3. Read at least four cases in full, every field (pick different variants: M, P, S and the R-series if present), to understand the condition's template and its errors first-hand.
4. Decide, with the reviewer notes as clinical rulings and the current guidelines: the governing guideline(s) and canonical clinical facts for this condition (criteria, thresholds, doses, timing windows, with citations you are sure exist); the target diagnostic pathway order and the tier (required / recommended / optional) of each recurring criterion, with the variant-specific exceptions; the canonical replacement text for every defect shared across cases; which sequence constraints belong in every case.
5. If ${R}/plans/${c.cond}.md already exists from an interrupted run, complete it rather than starting over. Keep the plan concise and decision-focused (aim under 60 KB): workers read it several times. Write ${R}/plans/${c.cond}.md with sections: (1) Governing guidelines and canonical facts; (2) Error classes in this condition: for each, the description, the note ids and cases it covers, the decided fix, canonical text where shared; (3) Target pathway and tiers; (4) Per-case index: for every one of the 30 cases, the note ids and the survey findings a worker must address (one bullet list per case); (5) CENTRAL requests (vocabulary, synonyms, library, UI); (6) Open questions for Andrea. Be concrete and specific: workers apply this to 6 cases each and must reach the same decisions for the same defect.
Before finishing, re-read your plan against the notes file: every note id must be covered by a class or by the per-case index.`
}

function workerPrompt(c, batch) {
  return `${COMMON}

You are a WORKER for condition ${c.cond}. Your cases (and only these): ${batch.join(', ')}.
Read the condition plan ${R}/plans/${c.cond}.md (written by the condition lead; follow its decisions so that all 30 cases end up consistent) and, if it exists, the reviewer notes file ${R}/notes/${c.cond}.md (and .json, which has the exact note ids). Read the references the plan cites as needed (criteria pack dataset-generation/criteria_packs/${c.cond}.md, TOOL_REPORT_STYLE_GUIDE.md).

Skip any of your cases whose log ${R}/logs/CASE.md already exists and contains a "## Changes" section: it was finished in an earlier run. A case whose file is modified (git diff) but has no complete log was interrupted mid-edit: read its current state and finish it.
Then, ONE CASE AT A TIME, for each remaining case:
1. Read the whole case JSON, every field and every sentence: patient, exam, every initial and followup output, fallback outputs, the whole ground_truth, metadata. Do not work from extracts alone.
2. Read every reviewer note for the case and the plan's per-case index entry.
3. Audit the case yourself on the five dimensions (schema, internal consistency, clinical correctness against the criteria pack and current guidelines, answer leakage per the style guide, language) and against every class in PATTERNS.md. Reason clinically about whether the presentation, the results and the policy hold together for a neurologist.
4. Edit through case_io (load/save), applying the reviewer notes, the plan, and your own findings. Keep related fields consistent when you change one (a value changed in a report must change wherever the case repeats it: HPI, other reports, criteria expected_evidence, musts, red herrings, key_clinical_evidence).
5. Run \`uv run python data/review/round-2026-10/bin/perfect_agent.py CASE -v\` and \`uv run python data/review/round-2026-10/bin/case_io.py check CASE\`; fix whatever names the case. Confirm with -v that each criterion receives the report holding its expected evidence.
6. Write the case log ${R}/logs/CASE.md in the ROUND_POLICY format. Every note id of the case appears in the table.
Only then move to the next case. If the plan is wrong for one of your cases, do what is clinically right, and explain it in the log under Open questions.`
}

function verifierPrompt(c, batch) {
  return `${COMMON}

You are an ADVERSARIAL VERIFIER for condition ${c.cond}, cases ${batch.join(', ')}. A worker has just corrected these cases and written logs in ${R}/logs/. Assume the worker made mistakes and find them. Read the plan ${R}/plans/${c.cond}.md and the notes file ${R}/notes/${c.cond}.md (if present).
Be economical with reading but not with judgment. Skip a case whose log already has a "## Verification" section. For each other case:
1. Read the log and \`git diff -- data/neurobench/cases/CASE.json\`. Read the whole final case only where the diff or the log suggests risk (large rewrites, numbers changed, labels changed, notes DECLINED or BLOCKED, approved cases); otherwise check the cross-field consistency with targeted greps/scripts over the case JSON.
2. Check every claim in the log against the file: each note marked FIXED is really fixed everywhere it applies; each DECLINED / BLOCKED has a sound clinical reason (if not, fix it); no note id is missing from the table.
3. Hunt for errors the edit introduced or left: values changed in one place but not where the case repeats them, sequence or tier changes that contradict the plan, broken laterality / timeline / allergy consistency, new answer leakage, wrong guideline facts, musts that contradict prohibitions or avoided actions, PATTERNS.md classes still present, the differential not matching the final evidence, prose churn in a case that was approved.
4. Fix what is wrong yourself through case_io, re-run \`perfect_agent.py CASE -v\` and \`case_io.py check CASE\` (both must be clean for the case), and append a "## Verification" section to the case log: what you checked, what you found, what you changed.
Be strict: a re-reviewing physician will trust these cases.`
}

function auditPrompt(c) {
  return `${COMMON}

You are the CONDITION AUDITOR for ${c.cond}. All 30 cases (${c.cases.join(', ')}) have been corrected by workers and checked by verifiers. Read the plan ${R}/plans/${c.cond}.md, every case log ${R}/logs/${c.cond}-*.md, and the notes file if present.
1. With scripts over the 30 case files, check that the plan's decisions were applied uniformly: canonical texts, tiers, pathway order, sequence constraints, guideline facts; that no shared defect from the plan or PATTERNS.md survives in any case; that every note id in the notes file appears in exactly one case log with a ruling.
2. Run \`uv run python data/review/round-2026-10/bin/perfect_agent.py <all 30 ids>\` and \`uv run python data/review/round-2026-10/bin/case_io.py check <all 30 ids>\`; both must be clean for the condition.
3. Read in full any case whose log looks thin, inconsistent with the others, or where the verifier changed a lot, and fix stragglers through case_io (append to that case's log what you changed and why).
4. Write ${R}/plans/${c.cond}-summary.md: the error classes found in this condition and how each was fixed, counts (notes FIXED / ALREADY-FIXED / DECLINED / BLOCKED; own findings fixed / flagged; cases changed; approved cases changed), every DECLINED and BLOCKED note with its reason, consolidated CENTRAL requests, consolidated open questions for Andrea.`
}

const BATCH_SCHEMA = {
  type: 'object',
  properties: {
    cases: { type: 'array', items: { type: 'object', properties: {
      case_id: { type: 'string' }, notes_total: { type: 'number' }, notes_fixed: { type: 'number' },
      notes_declined_or_blocked: { type: 'number' }, own_findings_fixed: { type: 'number' },
      perfect_agent_pass: { type: 'boolean' }, open_questions: { type: 'string' } },
      required: ['case_id', 'perfect_agent_pass'] } },
    central_requests: { type: 'string' },
  },
  required: ['cases'],
}
const SUMMARY_SCHEMA = {
  type: 'object',
  properties: { summary: { type: 'string' }, central_requests: { type: 'string' }, open_questions: { type: 'string' } },
  required: ['summary'],
}

function chunks(list, n) { const out = []; for (let i = 0; i < list.length; i += n) out.push(list.slice(i, i + n)); return out }

const results = await pipeline(
  args,
  c => c.planDone ? { summary: 'plan already written' } : agent(leadPrompt(c), { label: `lead:${c.cond}`, phase: 'Plan', schema: SUMMARY_SCHEMA }),
  (plan, c) => pipeline(
    chunks(c.cases, 6),
    batch => agent(workerPrompt(c, batch), { label: `fix:${batch[0]}..${batch[batch.length - 1]}`, phase: 'Fix', schema: BATCH_SCHEMA }),
    (fixed, batch) => agent(verifierPrompt(c, batch), { label: `verify:${batch[0]}..${batch[batch.length - 1]}`, phase: 'Verify', schema: BATCH_SCHEMA }),
  ).then(batches => ({ plan, batches })),
  (work, c) => agent(auditPrompt(c), { label: `audit:${c.cond}`, phase: 'Audit', schema: SUMMARY_SCHEMA })
    .then(audit => ({ cond: c.cond, plan: work.plan, batches: work.batches, audit })),
)
return results
