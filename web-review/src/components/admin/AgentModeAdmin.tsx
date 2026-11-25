import { ChevronDown, ChevronRight, Loader2 } from "lucide-react"
import { Fragment, useState } from "react"

import type { AdminAgentSection, AdminEpisode } from "@/api/agentTypes"
import { ReviewApiError } from "@/api/client"
import { ObservationView } from "@/components/agent/ObservationView"
import { useAdminAgentEpisode, useAdminAgentOverview } from "@/hooks/useAgentMode"
import { humanize } from "@/lib/agentText"
import { conditionShort } from "@/lib/conditions"
import { cn, formatDuration } from "@/lib/utils"

const COMPONENTS = [
  "diagnosis",
  "required_action_coverage",
  "recommended_action_coverage",
  "tool_accuracy",
  "safety",
  "waste_avoidance",
  "sequence",
  "stopping",
  "assessment",
  "cost_efficiency",
] as const

/** Admin view of the agent-mode study: who has done what, and each finished episode scored by
 * the benchmark's own reward. */
export function AgentModeAdmin() {
  const overview = useAdminAgentOverview()
  if (overview.isLoading) {
    return (
      <div className="py-16 flex justify-center text-muted-foreground">
        <Loader2 className="w-5 h-5 animate-spin" />
      </div>
    )
  }
  if (overview.isError || !overview.data) {
    const missing = overview.error instanceof ReviewApiError && overview.error.status === 404
    return (
      <p className="text-sm text-muted-foreground py-8">
        {missing ? "The agent-mode study is not configured on this server." : "The agent-mode summary could not be loaded."}
      </p>
    )
  }
  const { sections, scorer_id, limits } = overview.data
  return (
    <div className="space-y-10">
      <p className="text-sm text-muted-foreground max-w-[80ch]">
        Physicians work each case as the agent does, under the limits of <span className="font-mono text-xs">{limits.from}</span>{" "}
        ({limits.max_turns} turns). Finished episodes are scored by <span className="font-mono text-xs">{scorer_id}</span>, the scorer used for
        model episodes.
      </p>
      {sections.map((section) => (
        <SectionBlock key={section.key} section={section} />
      ))}
    </div>
  )
}

function SectionBlock({ section }: { section: AdminAgentSection }) {
  const [open, setOpen] = useState<string | null>(null)
  const draft = section.episodes.some((e) => e.row && !e.row.reportable)
  return (
    <section data-testid={`admin-section-${section.key}`}>
      <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
        <h2 className="text-lg font-semibold tracking-tight">{section.title}</h2>
        <span className="text-sm text-muted-foreground">
          {section.cases} cases, set <span className="font-mono text-xs">{section.set_id}</span>
        </span>
      </div>

      <div className="mt-3 overflow-x-auto bg-card border border-border rounded-xl">
        <table className="w-full text-sm">
          <thead className="text-left text-muted-foreground">
            <tr className="border-b border-border">
              <th className="px-4 py-2.5 font-medium">Physician</th>
              <th className="px-4 py-2.5 font-medium w-[40%]">Progress</th>
              <th className="px-4 py-2.5 font-medium text-right">Done</th>
              <th className="px-4 py-2.5 font-medium text-right">In progress</th>
              <th className="px-4 py-2.5 font-medium text-right">Ended early</th>
            </tr>
          </thead>
          <tbody>
            {section.reviewers.map((person) => (
              <tr key={person.reviewer_id} className="border-b border-border/60 last:border-0">
                <td className="px-4 py-2.5">
                  <span className="font-medium">{person.name}</span>
                  <span className="ml-2 font-mono text-xs text-muted-foreground">{person.reviewer_id}</span>
                  {!person.active && <span className="ml-2 text-xs text-muted-foreground">inactive</span>}
                </td>
                <td className="px-4 py-2.5">
                  <div className="h-1.5 rounded-full bg-muted overflow-hidden">
                    <div
                      className="h-full bg-status-approved"
                      style={{ width: `${person.assigned ? ((person.done + person.failed) / person.assigned) * 100 : 0}%` }}
                    />
                  </div>
                </td>
                <td className="px-4 py-2.5 text-right tabular-nums">
                  {person.done} / {person.assigned}
                </td>
                <td className="px-4 py-2.5 text-right tabular-nums">{person.in_progress}</td>
                <td className="px-4 py-2.5 text-right tabular-nums">{person.failed}</td>
              </tr>
            ))}
            {section.reviewers.length === 0 && (
              <tr>
                <td colSpan={5} className="px-4 py-6 text-muted-foreground">
                  No code opens this section yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="mt-6 flex flex-wrap items-center gap-3">
        <h3 className="font-semibold">Episodes</h3>
        {draft && (
          <span className="text-xs font-medium rounded-md border border-amber-500/50 bg-amber-500/10 text-amber-800 dark:text-amber-200 px-2 py-1">
            Scored against draft policies: engineering only, not reportable
          </span>
        )}
      </div>
      <div className="mt-2 overflow-x-auto bg-card border border-border rounded-xl">
        <table className="w-full text-sm">
          <thead className="text-left text-muted-foreground">
            <tr className="border-b border-border">
              <th className="w-8" />
              <th className="px-3 py-2.5 font-medium">Case</th>
              <th className="px-3 py-2.5 font-medium">Physician</th>
              <th className="px-3 py-2.5 font-medium">Status</th>
              <th className="px-3 py-2.5 font-medium text-right">Orders</th>
              <th className="px-3 py-2.5 font-medium text-right">Invalid</th>
              <th className="px-3 py-2.5 font-medium text-right">Time</th>
              <th className="px-3 py-2.5 font-medium">Diagnosis given</th>
              <th className="px-3 py-2.5 font-medium text-right">Dx</th>
              <th className="px-3 py-2.5 font-medium text-right">Required</th>
              <th className="px-3 py-2.5 font-medium text-right">Reward</th>
            </tr>
          </thead>
          <tbody>
            {section.episodes.map((episode) => {
              const key = `${episode.reviewer_id}/${episode.case_number}`
              const expanded = open === key
              const reward = episode.row?.reward
              return (
                <Fragment key={key}>
                  <tr
                    className={cn("border-b border-border/60 cursor-pointer hover:bg-secondary/40", expanded && "bg-secondary/40")}
                    onClick={() => setOpen(expanded ? null : key)}
                  >
                    <td className="pl-3 text-muted-foreground">
                      {expanded ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                    </td>
                    <td className="px-3 py-2.5 whitespace-nowrap">
                      <span className="tabular-nums text-muted-foreground mr-2">{episode.case_number}</span>
                      <span className="font-mono text-xs">{episode.case_id}</span>
                      <span className="ml-2 text-xs text-muted-foreground">{conditionShort(episode.condition)}</span>
                    </td>
                    <td className="px-3 py-2.5 whitespace-nowrap">{episode.reviewer_name}</td>
                    <td className="px-3 py-2.5 whitespace-nowrap">
                      {episode.status === "completed" ? "Completed" : episode.status === "failed" ? `Ended early (${episode.row?.failure_reason ?? ""})` : "In progress"}
                    </td>
                    <td className="px-3 py-2.5 text-right tabular-nums">{episode.orders}</td>
                    <td className="px-3 py-2.5 text-right tabular-nums">{episode.invalid_attempts}</td>
                    <td className="px-3 py-2.5 text-right tabular-nums whitespace-nowrap">
                      {formatDuration(episode.active_seconds ?? episode.elapsed_seconds)}
                    </td>
                    <td className="px-3 py-2.5 max-w-[16rem] truncate">{episode.row?.primary_diagnosis ?? ""}</td>
                    <td className="px-3 py-2.5 text-right tabular-nums">{reward ? Number(reward.diagnosis).toFixed(0) : ""}</td>
                    <td className="px-3 py-2.5 text-right tabular-nums">{reward ? Number(reward.required_action_coverage).toFixed(2) : ""}</td>
                    <td className="px-3 py-2.5 text-right tabular-nums font-semibold">{reward ? reward.scalar.toFixed(3) : ""}</td>
                  </tr>
                  {expanded && (
                    <tr className="border-b border-border/60">
                      <td colSpan={11} className="px-4 sm:px-6 py-5 bg-background/60">
                        <EpisodeDetail section={section.key} episode={episode} />
                      </td>
                    </tr>
                  )}
                </Fragment>
              )
            })}
            {section.episodes.length === 0 && (
              <tr>
                <td colSpan={11} className="px-4 py-6 text-muted-foreground">
                  No case has been started yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  )
}

function EpisodeDetail({ section, episode }: { section: string; episode: AdminEpisode }) {
  const detail = useAdminAgentEpisode(section, episode.reviewer_id, episode.case_number, true)
  const reward = episode.row?.reward
  if (!detail.data) {
    return <Loader2 className="w-4 h-4 animate-spin text-muted-foreground" />
  }
  const d = detail.data
  return (
    <div className="grid gap-8 lg:grid-cols-[minmax(0,1fr)_20rem]">
      <div className="min-w-0 space-y-4">
        <ol className="space-y-3">
          {d.timeline.map((entry) => (
            <li key={entry.turn} className="border border-border rounded-lg bg-card overflow-hidden">
              <div className="px-4 py-2.5">
                <div className="font-medium">
                  <span className="text-muted-foreground tabular-nums mr-2">{entry.turn}</span>
                  {humanize(entry.tool_name)}
                  <span className="ml-2 font-mono text-xs font-normal text-muted-foreground">{JSON.stringify(entry.arguments)}</span>
                </div>
                <p className="mt-1 text-sm border-l-2 border-primary/40 pl-3">{entry.rationale}</p>
              </div>
              {entry.observation && (
                <details className="border-t border-border bg-secondary/30 px-4 py-2 text-sm">
                  <summary className="cursor-pointer text-muted-foreground">Result{entry.observation.success ? "" : " (no result)"}</summary>
                  <div className="mt-2">
                    <ObservationView observation={entry.observation} />
                  </div>
                </details>
              )}
            </li>
          ))}
          {d.timeline.length === 0 && <li className="text-sm text-muted-foreground">No test ordered.</li>}
        </ol>
        {d.assessment && (
          <div className="border border-border rounded-lg bg-card px-4 py-3 text-sm space-y-1.5">
            <div className="font-semibold text-base">{d.assessment.primary_diagnosis}</div>
            <div className="text-muted-foreground">
              {d.assessment.icd10_code ? `ICD-10 ${d.assessment.icd10_code}, ` : ""}
              confidence {Math.round(d.assessment.confidence * 100)}%, {d.assessment.urgency}
            </div>
            {d.assessment.differential.length > 0 && (
              <div>
                Differential:{" "}
                {d.assessment.differential
                  .map((h) => `${h.diagnosis}${h.confidence != null ? ` (${Math.round(h.confidence * 100)}%)` : ""}`)
                  .join("; ")}
              </div>
            )}
            {d.assessment.recommendations.length > 0 && <div>Recommendations: {d.assessment.recommendations.join("; ")}</div>}
            {d.diagnostic_reasoning && <p className="border-l-2 border-primary/40 pl-3 mt-2">{d.diagnostic_reasoning}</p>}
          </div>
        )}
        {d.failure && <p className="text-sm text-amber-800 dark:text-amber-200">Ended early: {d.failure.reason}. {d.failure.message}</p>}
      </div>
      <div>
        {reward ? (
          <>
            <div className="text-sm text-muted-foreground">
              Policy reward
              {!episode.row?.reportable && <span className="ml-2 text-amber-700 dark:text-amber-300">draft policy, not reportable</span>}
            </div>
            <div className="text-3xl font-semibold tabular-nums tracking-tight">{reward.scalar.toFixed(3)}</div>
            <dl className="mt-3 space-y-1.5 text-sm">
              {COMPONENTS.map((name) => {
                const value = Number(reward[name])
                return (
                  <div key={name} className="grid grid-cols-[1fr_3.5rem_2.5rem] items-center gap-2">
                    <dt className="text-muted-foreground truncate">{humanize(name)}</dt>
                    <div className="h-1.5 rounded-full bg-muted overflow-hidden">
                      <div className="h-full bg-primary" style={{ width: `${value * 100}%` }} />
                    </div>
                    <dd className="text-right tabular-nums">{value.toFixed(2)}</dd>
                  </div>
                )
              })}
            </dl>
            <div className="mt-3 text-sm text-muted-foreground">
              Unjustified actions {String(reward.unjustified_actions)}, invalid {String(reward.invalid_actions)}
              {reward.caps_applied.length > 0 && <>, caps: {reward.caps_applied.join(", ")}</>}
            </div>
            <div className="mt-1 text-sm text-muted-foreground">Cost ${episode.row?.total_cost_usd.toFixed(0)}</div>
          </>
        ) : (
          <p className="text-sm text-muted-foreground">Scored when the case is finished.</p>
        )}
      </div>
    </div>
  )
}
