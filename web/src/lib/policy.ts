import type { EpisodeEvent, Profile, ToolAction, ToolCallPattern } from "@/api/types"

// Mirrors ToolCallPattern.matches in neuroagent_schemas/evaluation.py so the ground-truth view
// marks exactly the criteria the reward credits.

function fold(value: unknown): unknown {
  if (typeof value === "string") return value.trim().toLowerCase().replace(/_/g, " ").split(/\s+/).filter(Boolean).join(" ")
  if (Array.isArray(value)) return value.map(fold)
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, fold(v)]))
  }
  return value
}

function containsRequired(actual: unknown, required: unknown): boolean {
  const a = fold(actual)
  const r = fold(required)
  if (Array.isArray(r)) {
    return Array.isArray(a) && r.every((item) => a.some((candidate) => containsRequired(candidate, item)))
  }
  if (r && typeof r === "object") {
    if (!a || typeof a !== "object" || Array.isArray(a)) return false
    const obj = a as Record<string, unknown>
    return Object.entries(r).every(([key, value]) => key in obj && containsRequired(obj[key], value))
  }
  return a === r
}

export function patternMatches(pattern: ToolCallPattern, action: ToolAction): boolean {
  return action.tool_name === pattern.tool_name && containsRequired(action.arguments, pattern.required_arguments)
}

export function anyPatternMatches(patterns: ToolCallPattern[], actions: ToolAction[]): boolean {
  return actions.some((action) => patterns.some((pattern) => patternMatches(pattern, action)))
}

export function toolActions(events: EpisodeEvent[]): ToolAction[] {
  return events.flatMap((event) =>
    event.type === "action.proposed" && event.action.type === "tool" ? [event.action] : [],
  )
}

export function describePattern(pattern: ToolCallPattern): string {
  const args = Object.entries(pattern.required_arguments)
  if (args.length === 0) return pattern.tool_name
  return `${pattern.tool_name}(${args.map(([k, v]) => `${k}=${typeof v === "string" ? v : JSON.stringify(v)}`).join(", ")})`
}

// Profiles compose one model plugin and one loop plugin.

export function profileModelKey(profile: Profile | undefined): string | undefined {
  return profile?.plugins.find((p) => p.id.startsWith("model."))?.id.slice("model.".length)
}

export function profileLoop(profile: Profile | undefined): string | undefined {
  return profile?.plugins.find((p) => p.id.startsWith("loop."))?.id.slice("loop.".length)
}

export const LOOP_LABELS: Record<string, string> = {
  policy: "Policy",
  direct: "Direct (full information)",
  react: "ReAct ablation",
}
