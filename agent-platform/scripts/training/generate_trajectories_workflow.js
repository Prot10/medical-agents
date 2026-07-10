export const meta = {
  name: 'generate-gold-trajectories',
  description: 'Fan out one Sonnet subagent per NeuroBench case to author a gold ReAct trajectory',
  whenToUse: 'After prepare-prompts has written prompts/*.txt and manifest.json',
  phases: [
    { title: 'Generate', detail: 'one subagent per trajectory, isolated context', model: 'sonnet' },
  ],
}

// args: { promptsDir, rawDir, stems: [...] }
//   or: { promptsDir, rawDir, caseIds: [...], styles: [...], skipStems: [...] }
// The second form keeps the payload small for a 1000-trajectory run.
// Depending on how the caller passes it, args may arrive already parsed or as JSON text.
const input = typeof args === 'string' ? JSON.parse(args) : args
const { promptsDir, rawDir, caseIds, styles, skipStems } = input

let stems = input.stems
if (!stems && Array.isArray(caseIds) && Array.isArray(styles)) {
  const skip = new Set(skipStems || [])
  stems = caseIds.flatMap((c) => styles.map((s) => `${c}_${s}`)).filter((s) => !skip.has(s))
}

if (!Array.isArray(stems) || stems.length === 0) {
  throw new Error(`workflow needs args.stems or args.caseIds+styles; got: ${JSON.stringify(input).slice(0, 200)}`)
}

log(`Generating ${stems.length} trajectories -> ${rawDir}`)

phase('Generate')

// One subagent per trajectory. Each reads ONLY its own case prompt and writes its own
// file, so no case's reasoning can contaminate another's context.
const results = await pipeline(
  stems,
  (stem) =>
    agent(
      [
        `Read the file ${promptsDir}/${stem}.txt with the Read tool.`,
        `It contains a complete, self-contained instruction set for authoring one clinical ReAct trajectory.`,
        `Follow it exactly.`,
        ``,
        `Then write the resulting trace — and nothing else, no preamble, no code fences, no commentary —`,
        `to ${rawDir}/${stem}.txt using the Write tool.`,
        ``,
        `The file must begin with "<think>" and end with the "### Red Flags / Alerts" section.`,
        `Do not use any tool other than Read and Write. Do not search the web or read other files.`,
        ``,
        `When done, reply with exactly: OK ${stem}`,
      ].join('\n'),
      { label: stem, phase: 'Generate', model: 'sonnet', effort: 'low' },
    ).then((r) => ({ stem, ok: typeof r === 'string' && r.includes(`OK ${stem}`) }))
      .catch(() => ({ stem, ok: false })),
)

const done = results.filter(Boolean)
const failed = done.filter((r) => !r.ok).map((r) => r.stem)

log(`Generated ${done.length - failed.length}/${stems.length}; ${failed.length} failed`)

return {
  requested: stems.length,
  succeeded: done.length - failed.length,
  failed,
}
