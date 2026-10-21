import { useEffect, useMemo, useRef } from "react"
import { Zap, Loader2, AlertTriangle, RotateCcw, Play } from "lucide-react"
import { useAgentStore } from "@/stores/agentStore"
import { useAppStore } from "@/stores/appStore"
import { ThinkingBlock } from "./ThinkingBlock"
import { ToolCallCard } from "./ToolCallCard"
import { AssessmentPanel } from "./AssessmentPanel"
import type { EpisodeEvent, ObservationReceived, SubmitAssessment, ToolAction } from "@/api/types"

const REACT_NAMESPACE = "react.rationale"

const FAILURE_LABELS: Record<string, string> = {
  invalid_action: "Invalid-action budget spent",
  budget_exhausted: "Cost budget exhausted",
  model_error: "Model error",
  environment_error: "Environment error",
}

// ─── Centered connector between blocks ────────────────────────────────────────

function Connector() {
  return (
    <div className="flex justify-center">
      <div className="w-0.5 h-4 bg-border/40" />
    </div>
  )
}

// ─── Main component ───────────────────────────────────────────────────────────

export function AgentTimeline() {
  const selectedCaseId = useAppStore((s) => s.selectedCaseId)
  const events = useAgentStore((s) => s.events)
  const status = useAgentStore((s) => s.status)
  const errorMessage = useAgentStore((s) => s.errorMessage)
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (status === "running" && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [events.length, status])

  const items = useMemo(() => buildRenderItems(events), [events])
  const awaitingModel = status === "running" && !items.some((item) => item.type === "tool" && item.pending)

  return (
    <div className="flex flex-col h-full noise-bg relative bg-card">
      {/* Timeline header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border bg-card/80 backdrop-blur-sm z-10 shrink-0">
        <div className="h-6 w-6 rounded-lg bg-primary/10 flex items-center justify-center">
          <Zap className="h-3.5 w-3.5 text-primary" />
        </div>
        <span className="text-base font-semibold">Episode Timeline</span>
        {status === "running" && (
          <div className="flex items-center gap-1.5 ml-2">
            <Loader2 className="h-3.5 w-3.5 animate-spin text-primary" />
            <span className="text-sm text-primary">Running...</span>
          </div>
        )}
        {status === "cancelled" && <span className="text-sm text-muted-foreground ml-2">Stopped</span>}
      </div>

      {/* Timeline content */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto relative z-[1]">
        {events.length === 0 && status !== "running" && !errorMessage && (
          <div className="flex flex-col items-center justify-center h-full text-muted-foreground/30">
            <div className="h-16 w-16 rounded-2xl bg-primary/5 flex items-center justify-center mb-4">
              <Zap className="h-8 w-8 text-primary/20" />
            </div>
            <p className="text-base font-medium">
              {selectedCaseId ? "Ready to run" : "Select a case"}
            </p>
            <p className="text-sm text-muted-foreground/40 mt-1">
              {selectedCaseId ? "Click Run Agent to start" : "Choose a case from the sidebar"}
            </p>
          </div>
        )}

        {(items.length > 0 || status === "running") && (
          <div className="p-4">
            {items.map((item, i) => (
              <div key={item.key}>
                {i > 0 && <Connector />}
                <TimelineItem item={item} />
              </div>
            ))}

            {/* Waiting for the model's next action */}
            {awaitingModel && (
              <div>
                {items.length > 0 && <Connector />}
                <div className="flex items-center justify-center gap-2 py-3">
                  <div className="relative h-2.5 w-2.5">
                    <div className="absolute inset-0 rounded-full bg-primary animate-ping opacity-30" />
                    <div className="relative h-2.5 w-2.5 rounded-full bg-primary" />
                  </div>
                  <span className="text-sm text-muted-foreground/60">Waiting for the next action...</span>
                </div>
              </div>
            )}
          </div>
        )}

        {errorMessage && (
          <div className="m-4 p-4 rounded-xl border border-red-500/30 bg-red-500/5 text-base text-red-500">
            {errorMessage}
          </div>
        )}
      </div>
    </div>
  )
}

function TimelineItem({ item }: { item: RenderItem }) {
  switch (item.type) {
    case "started":
      return (
        <div className="flex items-center justify-center gap-2 text-sm text-muted-foreground animate-fade-in">
          <Play className="h-3.5 w-3.5" />
          <span className="font-mono">{item.profileId}</span>
          <span className="text-muted-foreground/40">·</span>
          <span className="font-mono truncate">{item.modelId}</span>
        </div>
      )
    case "rationale":
      return (
        <div className="animate-fade-in">
          <ThinkingBlock content={item.content} turnNumber={item.turn} label="Rationale" />
        </div>
      )
    case "tool":
      return (
        <div className="animate-slide-up">
          <ToolCallCard
            toolName={item.action.tool_name}
            arguments={item.action.arguments}
            observation={item.observation}
            pending={item.pending}
            turnNumber={item.turn}
          />
        </div>
      )
    case "rejected":
      return (
        <div className="flex items-start gap-2 rounded-xl border border-amber-500/30 bg-amber-500/5 px-3 py-2 text-sm animate-fade-in">
          <RotateCcw className="h-4 w-4 text-amber-500 mt-0.5 shrink-0" />
          <div className="min-w-0">
            <div className="font-medium text-amber-600 dark:text-amber-400">
              Invalid output {item.retryAllowed ? "· retried with a correction" : "· no retries left"}
            </div>
            <div className="text-muted-foreground break-words font-mono text-xs mt-0.5">{item.reason}</div>
          </div>
          <span className="ml-auto text-xs text-muted-foreground/50 font-mono bg-muted/50 px-1.5 py-0.5 rounded shrink-0">t{item.turn}</span>
        </div>
      )
    case "assessment":
      return (
        <div className="animate-slide-up">
          <AssessmentPanel assessment={item.assessment} />
        </div>
      )
    case "failed":
      return (
        <div className="flex items-start gap-2 rounded-xl border border-red-500/30 bg-red-500/5 px-4 py-3 animate-fade-in">
          <AlertTriangle className="h-4.5 w-4.5 text-red-500 mt-0.5 shrink-0" />
          <div className="min-w-0">
            <div className="text-base font-semibold text-red-500">Run failed · {FAILURE_LABELS[item.reason] ?? item.reason}</div>
            {item.message && <div className="text-sm text-muted-foreground break-words mt-0.5">{item.message}</div>}
          </div>
        </div>
      )
  }
}

// ─── Data processing ──────────────────────────────────────────────────────────

type RenderItem =
  | { type: "started"; key: string; profileId: string; modelId: string }
  | { type: "rationale"; key: string; content: string; turn: number }
  | { type: "tool"; key: string; action: ToolAction; observation?: ObservationReceived; pending: boolean; turn: number }
  | { type: "rejected"; key: string; reason: string; retryAllowed: boolean; turn: number }
  | { type: "assessment"; key: string; assessment: SubmitAssessment }
  | { type: "failed"; key: string; reason: string; message: string }

/**
 * One typed action per turn: a tool call is answered by the observation of the same turn;
 * observations at turn 0 belong to the direct baseline, which hands every result over upfront.
 */
function buildRenderItems(events: EpisodeEvent[]): RenderItem[] {
  const items: RenderItem[] = []
  const finished = events.some((e) => e.type === "run.completed" || e.type === "run.failed")

  for (const ev of events) {
    switch (ev.type) {
      case "run.started":
        items.push({ type: "started", key: ev.event_id, profileId: ev.profile_id, modelId: ev.model_id })
        break
      case "plugin.event":
        if (ev.namespace === REACT_NAMESPACE) {
          items.push({ type: "rationale", key: ev.event_id, content: String(ev.payload.value ?? ""), turn: ev.turn })
        }
        break
      case "action.proposed":
        if (ev.action.type === "tool") {
          const observation = events.find(
            (o): o is ObservationReceived => o.type === "observation.received" && o.turn === ev.turn,
          )
          items.push({
            type: "tool",
            key: ev.event_id,
            action: ev.action,
            observation,
            pending: !observation && !finished,
            turn: ev.turn,
          })
        }
        break
      case "observation.received":
        if (ev.turn === 0) {
          items.push({
            type: "tool",
            key: ev.event_id,
            action: { type: "tool", tool_name: ev.tool_name, arguments: {} },
            observation: ev,
            pending: false,
            turn: 0,
          })
        }
        break
      case "action.rejected":
        items.push({ type: "rejected", key: ev.event_id, reason: ev.reason, retryAllowed: ev.retry_allowed, turn: ev.turn })
        break
      case "assessment.submitted":
        items.push({ type: "assessment", key: ev.event_id, assessment: ev.assessment })
        break
      case "run.failed":
        items.push({ type: "failed", key: ev.event_id, reason: ev.reason, message: ev.message })
        break
    }
  }

  return items
}
