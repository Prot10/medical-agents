import { CircleAlert } from "lucide-react"

import type { JsonValue, Observation } from "@/api/agentTypes"
import { humanize } from "@/lib/agentText"
import { cn } from "@/lib/utils"

/** The result of an order, laid out for reading. Every key and value of the agent's
 * observation is shown; nothing is added or left out. */
export function ObservationView({ observation }: { observation: Observation }) {
  if (!observation.success) {
    return (
      <div className="flex gap-2.5 rounded-lg border border-amber-500/40 bg-amber-500/10 px-3.5 py-3 text-sm text-amber-900 dark:text-amber-200">
        <CircleAlert className="w-4 h-4 mt-0.5 flex-shrink-0" />
        <div>
          <div className="font-medium">No result</div>
          <div className="mt-0.5 leading-relaxed">{observation.error_message ?? "The order failed."}</div>
          {observation.output && <Value value={observation.output} depth={0} />}
        </div>
      </div>
    )
  }
  return (
    <div className="text-sm">
      <Value value={observation.output} depth={0} />
      {observation.error_message && (
        <p className="mt-2 text-amber-800 dark:text-amber-200">{observation.error_message}</p>
      )}
    </div>
  )
}

function isScalar(value: JsonValue): value is string | number | boolean | null {
  return value === null || typeof value !== "object"
}

function Scalar({ value }: { value: string | number | boolean | null }) {
  if (value === null) return <span className="text-muted-foreground">not reported</span>
  if (typeof value === "boolean") return <span>{value ? "Yes" : "No"}</span>
  return <span className="whitespace-pre-wrap break-words">{String(value)}</span>
}

function Value({ value, depth }: { value: JsonValue; depth: number }) {
  if (isScalar(value)) return <Scalar value={value} />
  if (Array.isArray(value)) {
    if (value.length === 0) return <span className="text-muted-foreground">none</span>
    if (value.every(isScalar)) {
      return (
        <ul className="list-disc pl-5 space-y-0.5 marker:text-muted-foreground">
          {value.map((item, i) => (
            <li key={i}>
              <Scalar value={item} />
            </li>
          ))}
        </ul>
      )
    }
    return (
      <div className="space-y-2">
        {value.map((item, i) => (
          <div key={i} className="rounded-md border border-border/70 bg-background/60 px-3 py-2">
            <Value value={item} depth={depth + 1} />
          </div>
        ))}
      </div>
    )
  }
  const entries = Object.entries(value)
  if (entries.length === 0) return <span className="text-muted-foreground">none</span>
  return (
    <dl className={cn("grid gap-x-4 gap-y-1.5", depth === 0 ? "sm:grid-cols-[minmax(7rem,11rem)_1fr]" : "sm:grid-cols-[minmax(6rem,9rem)_1fr]")}>
      {entries.map(([key, item]) => (
        <div key={key} className="contents">
          <dt className="text-muted-foreground sm:pt-px">{humanize(key)}</dt>
          <dd className="min-w-0 mb-1 sm:mb-0">
            <Value value={item} depth={depth + 1} />
          </dd>
        </div>
      ))}
    </dl>
  )
}
