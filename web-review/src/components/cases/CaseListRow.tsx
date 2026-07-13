import { ChevronRight } from "lucide-react"
import { memo } from "react"

import type {
  CaseIndexEntry,
  CaseReviewSummary,
  Severity,
} from "@/api/types"
import { conditionColor, conditionLabel, conditionShort } from "@/lib/conditions"
import { cn } from "@/lib/utils"
import { DifficultyStars } from "@/components/ui/DifficultyStars"
import { statusBorderColor } from "@/components/ui/StatusPill"

const SEVERITY_DOT: Record<Severity, string> = {
  note: "bg-sky-500",
  issue: "bg-amber-500",
  error: "bg-rose-500",
}

// Memoized: the 600-row list re-renders on every filter/search keystroke, but
// individual rows only change when their own props do. All props are stable —
// `onSelect` receives the case_id so callers can pass a stable store setter.
export const CaseListRow = memo(function CaseListRow({
  entry,
  review,
  selected,
  onSelect,
}: {
  entry: CaseIndexEntry
  review: CaseReviewSummary | undefined
  selected: boolean
  onSelect: (caseId: string) => void
}) {
  const status = review?.status ?? "pending"
  return (
    <button
      type="button"
      onClick={() => onSelect(entry.case_id)}
      className={cn(
        "group relative w-full text-left bg-card border border-border rounded-lg pl-4 pr-3 py-3 transition-all",
        "hover:border-primary/40 hover:shadow-sm",
        selected && "ring-2 ring-primary/50 border-primary/40",
      )}
    >
      <span
        className={cn(
          "absolute left-0 top-0 bottom-0 w-1 rounded-l-lg",
          statusBorderColor(status).replace("border-l-", "bg-"),
        )}
        aria-hidden
      />

      {/* Row 1: condition badge · case_id · stars (left), severity counts · chevron (right) */}
      <div className="flex items-center justify-between gap-2">
        <div className="flex items-center gap-2 sm:gap-3 min-w-0 flex-wrap">
          <span
            className="px-2 py-0.5 rounded-md text-[10px] font-bold tracking-wider flex-shrink-0"
            style={{
              background: `${conditionColor(entry.condition)}1a`,
              color: conditionColor(entry.condition),
            }}
            title={conditionLabel(entry.condition)}
          >
            {conditionShort(entry.condition)}
          </span>
          <span className="font-mono text-xs text-foreground/80 tabular-nums tracking-wider">
            {entry.case_id}
          </span>
          <DifficultyStars difficulty={entry.difficulty} />
        </div>
        <div className="flex items-center gap-2 sm:gap-3 flex-shrink-0">
          {review && (
            <span className="flex items-center gap-1 text-xs text-muted-foreground">
              {(["note", "issue", "error"] as const).map((sev) => {
                const count = review.severity_counts?.[sev] ?? 0
                if (count === 0) return null
                return (
                  <span key={sev} className="flex items-center gap-0.5">
                    <span className={cn("w-1.5 h-1.5 rounded-full", SEVERITY_DOT[sev])} />
                    <span className="tabular-nums">{count}</span>
                  </span>
                )
              })}
              {review.annotation_count + review.comment_count > 0 ? (
                <span className="ml-1 tabular-nums">
                  {review.annotation_count + review.comment_count}
                </span>
              ) : null}
            </span>
          )}
          <ChevronRight className="w-4 h-4 text-muted-foreground group-hover:text-foreground transition-colors" />
        </div>
      </div>

      {/* Row 2: chief complaint — wraps on small screens, single-line truncate on wide */}
      <div className="mt-1.5 text-sm text-foreground/90 line-clamp-2 sm:line-clamp-1 sm:truncate">
        {entry.chief_complaint}
      </div>

      {/* Row 3: demographics */}
      <div className="mt-1 text-[11px] text-muted-foreground/80 flex items-center gap-2">
        <span>{entry.age} y · {entry.sex}</span>
        <span>·</span>
        <span className="capitalize">{entry.encounter_type}</span>
      </div>
    </button>
  )
})
