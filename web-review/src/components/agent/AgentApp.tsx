import { Check, CircleDot, Loader2 } from "lucide-react"

import type { AgentSectionSummary, AgentWorklist } from "@/api/agentTypes"
import type { ReviewerProfile } from "@/api/types"
import { Button } from "@/components/ui/Button"
import { useAgentSections, useAgentWorklist } from "@/hooks/useAgentMode"
import { cn } from "@/lib/utils"
import { useAgentStore } from "@/stores/agentStore"
import { AgentHeader } from "./AgentHeader"
import { CaseWorkspace } from "./CaseWorkspace"

/** The agent-mode study, for a code that opens it: sections, then a section's cases, then a case. */
export function AgentApp({ profile }: { profile: ReviewerProfile }) {
  const section = useAgentStore((s) => s.section)
  const caseNumber = useAgentStore((s) => s.caseNumber)
  const sections = useAgentSections()
  const current = sections.data?.find((s) => s.section === section)

  if (section && current && caseNumber != null) {
    return <CaseWorkspace profile={profile} section={section} sectionTitle={current.title} number={caseNumber} />
  }
  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground">
      {section && current ? <SectionCases profile={profile} summary={current} /> : <SectionChoice profile={profile} sections={sections} />}
    </div>
  )
}

function Progress({ done, total, className }: { done: number; total: number; className?: string }) {
  return (
    <div className={cn("h-1.5 rounded-full bg-muted overflow-hidden", className)} role="progressbar" aria-valuenow={done} aria-valuemin={0} aria-valuemax={total}>
      <div className="h-full bg-status-approved rounded-full transition-[width]" style={{ width: `${total ? (done / total) * 100 : 0}%` }} />
    </div>
  )
}

function SectionChoice({
  profile,
  sections,
}: {
  profile: ReviewerProfile
  sections: ReturnType<typeof useAgentSections>
}) {
  const openSection = useAgentStore((s) => s.openSection)
  return (
    <>
      <AgentHeader profile={profile} crumbs={[{ label: "Cases" }]} />
      <main className="flex-1 w-full max-w-3xl mx-auto px-4 sm:px-6 py-10 sm:py-14">
        <h1 className="text-3xl font-semibold tracking-tight">Work each case as you would at the bedside</h1>
        <p className="mt-3 text-muted-foreground leading-relaxed max-w-[62ch]">
          You get the same presentation, the same tests and the same results as the AI agent we are
          studying. Order what you need, one test at a time, then give your assessment.
        </p>

        {sections.isLoading ? (
          <div className="py-16 flex justify-center text-muted-foreground">
            <Loader2 className="w-5 h-5 animate-spin" />
          </div>
        ) : sections.isError || !sections.data?.length ? (
          <p className="mt-10 rounded-xl border border-border bg-card px-5 py-6 text-muted-foreground">
            No case set is open for your code on this server. Ask the study team if you expected one.
          </p>
        ) : (
          <div className="mt-9 grid gap-4 sm:grid-cols-2">
            {sections.data.map((item) => (
              <SectionCard key={item.section} item={item} onOpen={() => openSection(item.section)} />
            ))}
          </div>
        )}

        <ol className="mt-12 grid gap-x-8 gap-y-5 sm:grid-cols-3 text-sm">
          {[
            ["Read the presentation", "It is all you know at the start. There is nothing hidden elsewhere on the page."],
            ["Order one test at a time", "Say briefly why. The result comes back at once and an order cannot be undone."],
            ["Give your assessment", "At any step, when you have enough. The case is then locked and no answer is shown."],
          ].map(([title, body], i) => (
            <li key={title} className="border-t border-border pt-3">
              <div className="font-semibold">
                <span className="text-primary tabular-nums mr-2">{i + 1}</span>
                {title}
              </div>
              <p className="mt-1 text-muted-foreground leading-relaxed">{body}</p>
            </li>
          ))}
        </ol>
      </main>
    </>
  )
}

function SectionCard({ item, onOpen }: { item: AgentSectionSummary; onOpen: () => void }) {
  const finished = item.total > 0 && item.done === item.total
  return (
    <button
      type="button"
      onClick={onOpen}
      data-testid={`section-${item.section}`}
      className="group text-left bg-card border border-border rounded-2xl p-5 shadow-sm hover:border-primary/60 hover:shadow-md transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
    >
      <h2 className="text-lg font-semibold tracking-tight group-hover:text-primary">{item.title}</h2>
      <p className="mt-1.5 text-sm text-muted-foreground leading-relaxed min-h-[3.75rem]">{item.description}</p>
      <Progress done={item.done} total={item.total} className="mt-4" />
      <div className="mt-2.5 flex items-center justify-between text-sm">
        <span className="text-muted-foreground tabular-nums">
          {item.done} of {item.total} done
        </span>
        <span className="font-medium text-primary">
          {finished ? "All done" : item.done === 0 && item.current === 1 ? "Open" : `Continue with case ${item.current}`}
        </span>
      </div>
    </button>
  )
}

function SectionCases({ profile, summary }: { profile: ReviewerProfile; summary: AgentSectionSummary }) {
  const openSection = useAgentStore((s) => s.openSection)
  const openCase = useAgentStore((s) => s.openCase)
  const worklist = useAgentWorklist(summary.section)
  const data: AgentWorklist | undefined = worklist.data
  const current = data?.cases.find((c) => c.number === data.current)

  return (
    <>
      <AgentHeader profile={profile} crumbs={[{ label: "Cases", onClick: () => openSection(null) }, { label: summary.title }]} />
      <main className="flex-1 w-full max-w-3xl mx-auto px-4 sm:px-6 py-8 sm:py-10">
        <h1 className="text-2xl font-semibold tracking-tight">{summary.title}</h1>
        <p className="mt-1.5 text-muted-foreground leading-relaxed max-w-[62ch]">{summary.description}</p>

        {!data ? (
          <div className="py-16 flex justify-center text-muted-foreground">
            <Loader2 className="w-5 h-5 animate-spin" />
          </div>
        ) : (
          <>
            <div className="mt-6 bg-card border border-border rounded-2xl p-5 shadow-sm flex flex-col sm:flex-row sm:items-center gap-4">
              <div className="flex-1 min-w-0">
                <div className="text-sm text-muted-foreground tabular-nums">
                  {data.done} of {data.total} cases done
                </div>
                <Progress done={data.done} total={data.total} className="mt-2" />
              </div>
              {current ? (
                <Button size="lg" onClick={() => openCase(current.number)} data-testid="open-current">
                  {current.status === "in_progress" ? `Continue case ${current.number}` : `Start case ${current.number}`}
                </Button>
              ) : (
                <span className="text-sm font-medium text-accent-foreground">All cases done. Thank you.</span>
              )}
            </div>

            <ul className="mt-6 border-t border-border" data-testid="case-list">
              {data.cases.map((item) => {
                const isCurrent = item.number === data.current
                return (
                  <li key={item.number} className="flex items-center gap-3 py-3 border-b border-border">
                    <span
                      className={cn(
                        "w-7 h-7 rounded-full flex items-center justify-center flex-shrink-0",
                        item.status === "done" && "bg-status-approved/15 text-status-approved",
                        item.status === "in_progress" && "bg-primary/10 text-primary",
                        item.status === "todo" && "border border-border text-muted-foreground",
                      )}
                    >
                      {item.status === "done" ? <Check className="w-4 h-4" /> : item.status === "in_progress" ? <CircleDot className="w-4 h-4" /> : null}
                    </span>
                    <span className={cn("font-medium tabular-nums", item.status === "todo" && !isCurrent && "text-muted-foreground")}>
                      Case {item.number}
                    </span>
                    <span className="text-sm text-muted-foreground">
                      {item.status === "done"
                        ? "Done"
                        : item.status === "in_progress"
                          ? `In progress, ${item.orders} ${item.orders === 1 ? "order" : "orders"} so far`
                          : isCurrent
                            ? "Next"
                            : "To do"}
                    </span>
                    {isCurrent && (
                      <button type="button" onClick={() => openCase(item.number)} className="ml-auto text-sm font-medium text-primary hover:underline">
                        {item.status === "in_progress" ? "Continue" : "Start"}
                      </button>
                    )}
                  </li>
                )
              })}
            </ul>
            <p className="mt-4 text-sm text-muted-foreground">
              Cases are worked one at a time, in this order. You can stop whenever you like: your place is kept.
            </p>
          </>
        )}
      </main>
    </>
  )
}
