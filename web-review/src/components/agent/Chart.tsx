import { useEffect, useRef } from "react"

import type { CaseState, JsonValue, TimelineEntry } from "@/api/agentTypes"
import { formatClock, humanize, parsePresentation } from "@/lib/agentText"
import { ObservationView } from "./ObservationView"

/** The patient's chart: the instructions and the presentation the agent receives, then every
 * order placed so far with its reason and its result. */
export function Chart({ state }: { state: CaseState }) {
  const timeline = state.timeline ?? []
  const lastRef = useRef<HTMLLIElement>(null)
  const count = timeline.length

  // A new result scrolls into view; the first render of a resumed case does too.
  useEffect(() => {
    if (count > 0) lastRef.current?.scrollIntoView({ behavior: "smooth", block: "start" })
  }, [count])

  return (
    <div className="space-y-5">
      <section aria-label="Instructions" className="rounded-xl bg-secondary/60 border border-border/60 px-4 sm:px-5 py-3.5">
        <h2 className="text-xs font-semibold text-muted-foreground">Your instructions, the same the agent is given</h2>
        <p className="mt-1.5 text-sm leading-relaxed text-secondary-foreground whitespace-pre-line">
          {(state.instructions ?? "").replace(/\n/g, " ")}
        </p>
      </section>

      <section aria-label="Presentation" className="bg-card border border-border rounded-xl px-4 sm:px-6 py-5 shadow-sm">
        <h2 className="text-lg font-semibold tracking-tight">Presentation</h2>
        <Presentation text={state.presentation ?? ""} />
      </section>

      {count > 0 && (
        <section aria-label="Orders and results">
          <h2 className="text-sm font-semibold text-muted-foreground mb-3 px-1">Orders and results</h2>
          <ol className="relative space-y-4">
            {timeline.map((entry, i) => (
              <Order key={entry.turn} entry={entry} innerRef={i === count - 1 ? lastRef : undefined} />
            ))}
          </ol>
        </section>
      )}
    </div>
  )
}

function Presentation({ text }: { text: string }) {
  const blocks = parsePresentation(text)
  return (
    <dl className="mt-4 divide-y divide-border/60">
      {blocks.map((block, i) => (
        <div key={i} className="py-3 first:pt-0 last:pb-0 grid gap-x-5 gap-y-1 sm:grid-cols-[10.5rem_1fr]">
          <dt className="text-[13px] font-medium text-muted-foreground sm:pt-0.5">{block.label}</dt>
          <dd className="min-w-0">
            {block.text && (
              <p className="prose-serif text-[15.5px] text-foreground whitespace-pre-line max-w-[72ch]">{block.text}</p>
            )}
            {block.items.length > 0 && (
              <dl className="grid gap-x-4 gap-y-1.5 sm:grid-cols-[8.5rem_1fr]">
                {block.items.map((item, j) => (
                  <div key={j} className="contents">
                    <dt className="text-[13px] text-muted-foreground sm:pt-1">{item.label}</dt>
                    <dd className="prose-serif text-[15px] max-w-[66ch]">{item.text}</dd>
                  </div>
                ))}
              </dl>
            )}
          </dd>
        </div>
      ))}
    </dl>
  )
}

function argumentText(value: JsonValue): string {
  if (Array.isArray(value)) return value.map((item) => argumentText(item)).join(", ")
  if (value !== null && typeof value === "object") return JSON.stringify(value)
  if (typeof value === "boolean") return value ? "yes" : "no"
  return String(value)
}

function Order({ entry, innerRef }: { entry: TimelineEntry; innerRef?: React.Ref<HTMLLIElement> }) {
  const args = Object.entries(entry.arguments)
  return (
    <li ref={innerRef} className="scroll-mt-20 grid grid-cols-[2rem_1fr] gap-x-3" data-testid="order">
      <div className="flex flex-col items-center">
        <span className="w-8 h-8 rounded-full bg-primary text-primary-foreground text-sm font-semibold flex items-center justify-center tabular-nums">
          {entry.turn}
        </span>
        <span className="flex-1 w-px bg-border mt-1" />
      </div>
      <div className="bg-card border border-border rounded-xl shadow-sm overflow-hidden min-w-0">
        <div className="px-4 sm:px-5 pt-3.5 pb-3">
          <div className="flex items-baseline justify-between gap-3">
            <h3 className="font-semibold tracking-tight">
              {humanize(entry.tool_name)}
              <span className="ml-2 font-mono text-xs font-normal text-muted-foreground">{entry.tool_name}</span>
            </h3>
            <time className="text-xs text-muted-foreground tabular-nums flex-shrink-0">{formatClock(entry.sent_at)}</time>
          </div>
          {args.length > 0 && (
            <dl className="mt-2 text-sm grid gap-x-3 gap-y-0.5 sm:grid-cols-[minmax(6rem,10rem)_1fr]">
              {args.map(([key, value]) => (
                <div key={key} className="contents">
                  <dt className="text-muted-foreground">{humanize(key)}</dt>
                  <dd className="min-w-0 break-words">{argumentText(value)}</dd>
                </div>
              ))}
            </dl>
          )}
          <p className="mt-2.5 text-sm border-l-2 border-primary/40 pl-3 text-secondary-foreground">
            <span className="text-muted-foreground">Your reason: </span>
            {entry.rationale}
          </p>
        </div>
        <div className="border-t border-border bg-secondary/30 px-4 sm:px-5 py-3.5">
          <div className="text-xs font-semibold text-muted-foreground mb-2">Result</div>
          {entry.observation ? (
            <ObservationView observation={entry.observation} />
          ) : (
            <span className="text-sm text-muted-foreground">No result recorded.</span>
          )}
        </div>
      </div>
    </li>
  )
}
