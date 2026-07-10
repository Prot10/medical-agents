export const meta = {
  name: 'repair-gold-trajectories',
  description: 'Give each rejected trajectory one repair round with its exact validator issues',
  whenToUse: 'After --assemble reports rejections; feeds validator complaints back to the teacher',
  phases: [
    { title: 'Repair', detail: 'one subagent per rejected trajectory', model: 'sonnet' },
  ],
}

// args: { promptsDir, rawDir, targets: [{stem, issues: [...]}, ...] }
//   or: { promptsDir, rawDir, rejectedDir, stems: [...] }  <- agent reads its own issues
const input = typeof args === 'string' ? JSON.parse(args) : args
const { promptsDir, rawDir, rejectedDir } = input

let targets = input.targets
if (!targets && Array.isArray(input.stems)) {
  targets = input.stems.map((stem) => ({ stem, issues: null }))
}

if (!Array.isArray(targets) || targets.length === 0) {
  throw new Error(`workflow needs args.targets or args.stems; got: ${JSON.stringify(input).slice(0, 200)}`)
}

log(`Repairing ${targets.length} rejected trajectories`)

phase('Repair')

const results = await pipeline(
  targets,
  (t) =>
    agent(
      [
        `A clinical ReAct trajectory you previously wrote failed automated validation.`,
        `Rewrite it so it passes, changing as little as possible.`,
        ``,
        `1. Read the original instructions: ${promptsDir}/${t.stem}.txt`,
        `2. Read your previous attempt:    ${rawDir}/${t.stem}.txt`,
        ...(t.issues
          ? [``, `The validator rejected it for these reasons — every one must be fixed:`,
             ...t.issues.map((i) => `  - ${i}`)]
          : [`3. Read the validator's complaint: ${rejectedDir}/${t.stem}.json`,
             `   Its "issues" array lists every problem you must fix. If it instead has`,
             `   "reason": "unparseable", the trace has an unbalanced tag — find and fix it.`]),
        ``,
        `Reminders that cover the common failures:`,
        `  * Each tool may be called AT MOST ONCE. If two workup steps use the same tool,`,
        `    merge them into a single call whose clinical_context covers both, and write the`,
        `    reasoning as one observation.`,
        `  * Use only the argument names in the "Callable tools" section of the instructions.`,
        `  * Every <think>, <tool_call> and <tool_response> needs its matching closing tag.`,
        `    A <tool_call> closes with </tool_call>, never </tool_response>.`,
        `  * Never reveal that you were shown the answer. These exact phrases are banned anywhere`,
        `    in the trace: "as expected", "as required", "ground truth", "red herring", "distractor",`,
        `    "optimal action", "the correct answer", "expected finding", "this case is designed",`,
        `    "per the case", "the case states". Write findings as discoveries, not confirmations.`,
        ``,
        `Preserve the clinical reasoning and the final diagnosis. Keep the same structure.`,
        ``,
        `Overwrite ${rawDir}/${t.stem}.txt with the corrected trace using the Write tool —`,
        `the file must contain ONLY the trace, starting with "<think>".`,
        ``,
        `Then reply with exactly: OK ${t.stem}`,
      ].join('\n'),
      { label: `repair:${t.stem}`, phase: 'Repair', model: 'sonnet', effort: 'low' },
    )
      .then((r) => ({ stem: t.stem, ok: typeof r === 'string' && r.includes(`OK ${t.stem}`) }))
      .catch(() => ({ stem: t.stem, ok: false })),
)

const done = results.filter(Boolean)
const failed = done.filter((r) => !r.ok).map((r) => r.stem)

log(`Repaired ${done.length - failed.length}/${targets.length}; ${failed.length} failed`)

return { requested: targets.length, succeeded: done.length - failed.length, failed }
