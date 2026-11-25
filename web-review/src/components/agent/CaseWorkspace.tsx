import { CircleCheck, Code2, Info, Loader2, TriangleAlert } from "lucide-react"
import { useState } from "react"

import type { CaseState, JsonValue } from "@/api/agentTypes"
import { ReviewApiError } from "@/api/client"
import type { ReviewerProfile } from "@/api/types"
import { Button } from "@/components/ui/Button"
import { useCaseState, useSendAction } from "@/hooks/useAgentMode"
import { cn } from "@/lib/utils"
import { useAgentStore } from "@/stores/agentStore"
import { AgentHeader } from "./AgentHeader"
import { AssessmentForm } from "./AssessmentForm"
import { Chart } from "./Chart"
import { OrderPad } from "./OrderPad"
import { RawViewDialog } from "./RawViewDialog"
import { useStepTelemetry } from "./useStepTelemetry"

/** One case: the chart on the left, the next action on the right. */
export function CaseWorkspace({
  profile,
  section,
  sectionTitle,
  number,
}: {
  profile: ReviewerProfile
  section: string
  sectionTitle: string
  number: number
}) {
  const openCase = useAgentStore((s) => s.openCase)
  const openSection = useAgentStore((s) => s.openSection)
  const query = useCaseState(section, number)
  const state = query.data
  const crumbs = [
    { label: "Cases", onClick: () => openSection(null) },
    { label: sectionTitle, onClick: () => openCase(null) },
    { label: `Case ${number}` },
  ]

  if (!state) {
    return (
      <div className="min-h-screen flex flex-col bg-background">
        <AgentHeader profile={profile} crumbs={crumbs} />
        <div className="flex-1 flex items-center justify-center text-muted-foreground px-6 text-center">
          {query.isError ? (
            <div>
              <p className="text-foreground font-medium">This case can't be opened.</p>
              <p className="text-sm mt-1">{query.error instanceof ReviewApiError ? query.error.message : "Check your connection."}</p>
              <Button variant="outline" className="mt-4" onClick={() => openCase(null)}>Back to the list</Button>
            </div>
          ) : (
            <Loader2 className="w-5 h-5 animate-spin" />
          )}
        </div>
      </div>
    )
  }
  if (state.status !== "in_progress") {
    return (
      <div className="min-h-screen flex flex-col bg-background">
        <AgentHeader profile={profile} crumbs={crumbs} />
        <CaseDone state={state} />
      </div>
    )
  }
  return <ActiveCase profile={profile} section={section} number={number} state={state} crumbs={crumbs} />
}

function ActiveCase({
  profile,
  section,
  number,
  state,
  crumbs,
}: {
  profile: ReviewerProfile
  section: string
  number: number
  state: CaseState
  crumbs: Array<{ label: string; onClick?: () => void }>
}) {
  const send = useSendAction(section, number)
  const telemetry = useStepTelemetry(state.expected_step)
  const [mode, setMode] = useState<"order" | "assess">("order")
  const [rawOpen, setRawOpen] = useState(false)
  const mustAssess = !!state.require_assessment
  const active = mustAssess ? "assess" : mode
  const tools = (state.tools ?? []).filter((tool) => tool.function.name !== state.submit_name)

  const dispatch = (name: string, args: Record<string, JsonValue>, rationale: string) =>
    send.mutate(
      { expected_step: state.expected_step, name, arguments: args, rationale, telemetry: telemetry.collect() },
      { onSuccess: () => setMode("order") },
    )

  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground">
      <AgentHeader profile={profile} crumbs={crumbs}>
        <button
          type="button"
          onClick={() => {
            telemetry.noteRawView()
            setRawOpen(true)
          }}
          className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-sm text-muted-foreground hover:bg-secondary/70"
        >
          <Code2 className="w-4 h-4" />
          <span className="hidden sm:inline">Raw view</span>
        </button>
      </AgentHeader>

      <div className="flex-1 w-full max-w-[1440px] mx-auto px-4 sm:px-6 py-5 grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(400px,480px)] items-start">
        <main className="min-w-0">
          <Chart state={state} />
        </main>

        <aside
          aria-label="Next step"
          className="bg-card border border-border rounded-xl shadow-sm lg:sticky lg:top-[4.5rem] lg:max-h-[calc(100vh-5.5rem)] flex flex-col min-w-0"
        >
          <div className="px-4 sm:px-5 pt-4 pb-3 border-b border-border">
            <div className="flex items-baseline justify-between gap-3">
              <h2 className="text-base font-semibold tracking-tight">
                Step {state.turn}
                {state.max_turns ? <span className="text-muted-foreground font-normal"> of {state.max_turns}</span> : null}
              </h2>
              <span className="text-xs text-muted-foreground">Saved after every step</span>
            </div>
            {state.notice && (
              <div
                className={cn(
                  "mt-3 flex gap-2.5 rounded-lg border px-3 py-2.5 text-sm",
                  mustAssess && !state.notice.startsWith("The previous")
                    ? "border-primary/40 bg-primary/5"
                    : "border-amber-500/40 bg-amber-500/10 text-amber-900 dark:text-amber-200",
                )}
                role="status"
                data-testid="notice"
              >
                {mustAssess && !state.notice.startsWith("The previous") ? (
                  <Info className="w-4 h-4 mt-0.5 flex-shrink-0 text-primary" />
                ) : (
                  <TriangleAlert className="w-4 h-4 mt-0.5 flex-shrink-0" />
                )}
                <p className="leading-relaxed break-words min-w-0">{state.notice}</p>
              </div>
            )}
            {!mustAssess && (
              <div className="mt-3 grid grid-cols-2 gap-1 p-1 bg-secondary/70 rounded-lg" role="tablist">
                {(
                  [
                    ["order", "Order a test"],
                    ["assess", "Give your assessment"],
                  ] as const
                ).map(([id, label]) => (
                  <button
                    key={id}
                    type="button"
                    role="tab"
                    aria-selected={active === id}
                    onClick={() => setMode(id)}
                    className={cn(
                      "h-9 rounded-md text-sm font-medium transition-colors",
                      active === id ? "bg-card shadow-sm text-foreground" : "text-muted-foreground hover:text-foreground",
                    )}
                  >
                    {label}
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="px-4 sm:px-5 py-4 overflow-y-auto min-h-0">
            {send.isError && (
              <p className="mb-3 rounded-md border border-rose-500/40 bg-rose-500/10 px-3 py-2 text-sm text-rose-700 dark:text-rose-300" role="alert">
                {send.error instanceof ReviewApiError ? send.error.message : "The step was not sent. Check your connection and try again."}
              </p>
            )}
            {active === "order" ? (
              <OrderPad
                key={state.expected_step}
                tools={tools}
                sending={send.isPending}
                onSend={dispatch}
                onToolOpened={telemetry.noteTool}
                onSearch={telemetry.noteSearch}
              />
            ) : (
              <AssessmentForm
                key={state.expected_step}
                sending={send.isPending}
                onSubmit={(assessment, reasoning) => dispatch(state.submit_name ?? "submit_assessment", assessment, reasoning)}
              />
            )}
          </div>
        </aside>
      </div>

      {state.raw && <RawViewDialog raw={state.raw} open={rawOpen} onOpenChange={setRawOpen} />}
    </div>
  )
}

const FAILURES: Record<string, string> = {
  invalid_action: "It ended early because too many actions were not valid.",
  budget_exhausted: "It ended early because the cost ceiling of the encounter was reached.",
}

/** After the assessment: the case is locked and nothing is said about the answer. */
function CaseDone({ state }: { state: CaseState }) {
  const openCase = useAgentStore((s) => s.openCase)
  return (
    <div className="flex-1 flex items-center justify-center px-6 py-12">
      <div className="max-w-md text-center">
        <CircleCheck className="w-11 h-11 mx-auto text-status-approved" strokeWidth={1.5} />
        <h1 className="mt-4 text-2xl font-semibold tracking-tight">Case {state.number} is finished</h1>
        <p className="mt-2 text-muted-foreground leading-relaxed">
          {state.status === "failed"
            ? (FAILURES[state.failure?.reason ?? ""] ?? "It ended early.") + " What you did is saved."
            : "Your work-up and assessment are saved and the case is locked."}{" "}
          To keep the study blind, no answer is shown.
        </p>
        <div className="mt-6 flex flex-col sm:flex-row gap-2 justify-center">
          {state.next != null && (
            <Button size="lg" onClick={() => openCase(state.next)}>
              Start case {state.next}
            </Button>
          )}
          <Button size="lg" variant="outline" onClick={() => openCase(null)}>
            {state.next != null ? "Stop here for now" : "Back to the list"}
          </Button>
        </div>
        {state.next == null && <p className="mt-5 text-sm text-muted-foreground">That was the last case of this section. Thank you.</p>}
      </div>
    </div>
  )
}
