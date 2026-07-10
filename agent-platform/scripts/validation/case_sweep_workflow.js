export const meta = {
  name: 'neurobench-case-contract-sweep',
  description: 'One clinician subagent per condition, driving validate_cases.py to zero issues',
  whenToUse: 'After migrate_cases.py has removed the deterministic issues',
  phases: [{ title: 'Sweep', detail: 'one subagent per condition, scoped to its own cases' }],
}

// args: { repo, specPath, conditions: ["als", ...] }
const input = typeof args === 'string' ? JSON.parse(args) : args
const { repo, specPath, conditions } = input

if (!Array.isArray(conditions) || conditions.length === 0) {
  throw new Error(`workflow needs args.conditions; got ${JSON.stringify(conditions)}`)
}

log(`Sweeping ${conditions.length} conditions`)

phase('Sweep')

const results = await pipeline(
  conditions,
  (condition) =>
    agent(
      [
        `You are the clinical expert for the NeuroBench condition: ${condition}.`,
        ``,
        `1. Read the sweep spec: ${specPath}. Follow it exactly.`,
        `2. Read your work packet: ${repo}/data/review/work_packets/${condition}.json`,
        `   It maps each of your case files to the validator issues you must close.`,
        `3. Read the allowlist and rules in ${repo}/agent-platform/scripts/validation/validate_cases.py`,
        `   (ANNOTATION_KEYS) and the closed vocabulary in ${repo}/agent-platform/config/tools/costs.yaml.`,
        `4. Fix each case in ${repo}/data/neurobench/cases/.`,
        ``,
        `Hard rules:`,
        `  * Edit ONLY the case files named in your packet. No other file, ever.`,
        `  * Never change clinical content: primary_diagnosis, icd_code, differential, patient,`,
        `    tool outputs, rationale/action/expected_finding text. You are fixing how a step names`,
        `    the tool it intends and with which arguments.`,
        `  * Never invent a vocabulary value to silence the validator. If the honest fix needs a`,
        `    term that does not exist, leave the issue open and REPORT it.`,
        `  * Preserve formatting: json.dumps(obj, indent=2, ensure_ascii=False) + "\\n".`,
        ``,
        `Verify before reporting. For every case file you touched, run:`,
        `  cd ${repo} && uv run python agent-platform/scripts/validation/validate_cases.py --case <FILE>`,
        `It must print "1/1 cases clean, 0 issues".`,
        ``,
        `Then reply with exactly this, and nothing else:`,
        `  CONDITION: ${condition}`,
        `  CLEAN: <n>/<total>`,
        `  DECISIONS: <one line per non-mechanical judgment call, especially drugs -> drug vs current_medications>`,
        `  VOCAB_GAPS: <case_id: missing term>  (or "none")`,
      ].join('\n'),
      { label: condition, phase: 'Sweep', model: 'sonnet', effort: 'high' },
    )
      .then((r) => ({ condition, report: typeof r === 'string' ? r : '' }))
      .catch((e) => ({ condition, report: `FAILED: ${e}` })),
)

const done = results.filter(Boolean)
log(`Swept ${done.length}/${conditions.length} conditions`)

return { reports: done }
