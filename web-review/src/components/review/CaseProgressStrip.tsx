import { ArrowLeft, ArrowRight } from "lucide-react"

import type { ReviewStatus } from "@/api/types"
import { isDecided } from "@/hooks/useSetProgress"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/Button"

const SEGMENT_COLOR: Record<ReviewStatus, string> = {
  approved: "bg-emerald-500",
  needs_changes: "bg-amber-500",
  in_progress: "bg-sky-400",
  pending: "bg-muted-foreground/20",
}

const STATUS_WORD: Record<ReviewStatus, string> = {
  approved: "approved",
  needs_changes: "needs changes",
  in_progress: "started",
  pending: "not reviewed yet",
}

/**
 * A progress bar over a fixed list of cases: one segment per case, coloured by the reviewer's
 * decision, the open case highlighted, each segment a link to its case, and previous/next
 * buttons while a case is open.
 */
export function CaseProgressStrip({
  caseIds,
  statusOf,
  currentCaseId,
  onOpen,
  heading,
  describe,
}: {
  caseIds: string[]
  statusOf: (caseId: string) => ReviewStatus
  currentCaseId: string | null
  onOpen: (caseId: string) => void
  /** Left-hand title; receives the open case's 0-based position, or -1. */
  heading: (index: number) => React.ReactNode
  /** Short name of a case for the segment tooltips. */
  describe: (caseId: string) => string
}) {
  const index = currentCaseId ? caseIds.indexOf(currentCaseId) : -1
  const total = caseIds.length
  const done = caseIds.filter((id) => isDecided(statusOf(id))).length
  const nextUndecided = caseIds.find((id) => id !== currentCaseId && !isDecided(statusOf(id))) ?? null
  const prev = index > 0 ? caseIds[index - 1] : null
  const next = index >= 0 && index < total - 1 ? caseIds[index + 1] : null
  const currentDecided = index >= 0 && isDecided(statusOf(caseIds[index]))
  const pct = total ? Math.round((done / total) * 100) : 0

  return (
    <div className="pb-3 pt-0.5">
      <div className="max-w-7xl mx-auto w-full px-4 sm:px-6">
        <div className="flex items-end justify-between gap-3 mb-2">
          <div className="min-w-0">{heading(index)}</div>
          <div className="flex items-center gap-1.5 flex-shrink-0">
            <span className="text-xs text-muted-foreground tabular-nums mr-1">
              <span className="font-semibold text-foreground">{done}</span>/{total} reviewed · {pct}%
            </span>
            {index >= 0 && (
              <>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={!prev}
                  onClick={() => prev && onOpen(prev)}
                  aria-label="Previous case"
                  className="px-2 sm:px-3"
                >
                  <ArrowLeft className="w-4 h-4" />
                  <span className="hidden sm:inline">Previous</span>
                </Button>
                <Button
                  variant={currentDecided ? "primary" : "outline"}
                  size="sm"
                  disabled={!next && !nextUndecided}
                  onClick={() => {
                    const target = next ?? nextUndecided
                    if (target) onOpen(target)
                  }}
                  aria-label="Next case"
                  className="px-2 sm:px-3"
                >
                  <span className="hidden sm:inline">Next case</span>
                  <ArrowRight className="w-4 h-4" />
                </Button>
              </>
            )}
          </div>
        </div>

        <div className="flex items-center gap-[3px] sm:gap-1" role="list" aria-label="Cases">
          {caseIds.map((id, i) => {
            const status = statusOf(id)
            const isCurrent = id === currentCaseId
            const label = `${i + 1}. ${describe(id)}: ${STATUS_WORD[status]}`
            return (
              <button
                key={id}
                type="button"
                role="listitem"
                title={label}
                aria-label={label}
                aria-current={isCurrent ? "step" : undefined}
                onClick={() => onOpen(id)}
                className="group flex-1 py-1.5 -my-1.5 focus-visible:outline-none"
              >
                <span
                  className={cn(
                    "block rounded-full transition-all duration-300",
                    isCurrent && status === "pending" ? "bg-primary/35" : SEGMENT_COLOR[status],
                    isCurrent
                      ? "h-2.5 ring-2 ring-primary ring-offset-2 ring-offset-background"
                      : "h-1.5 group-hover:h-2.5 group-focus-visible:ring-2 group-focus-visible:ring-ring",
                  )}
                />
              </button>
            )
          })}
        </div>
      </div>
    </div>
  )
}
