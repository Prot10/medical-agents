import { cn } from "@/lib/utils"
import type { ReviewStatus } from "@/api/types"

const STATUS_LABEL: Record<ReviewStatus, string> = {
  pending: "Pending",
  in_progress: "In progress",
  needs_changes: "Needs changes",
  approved: "Approved",
}

const STATUS_STYLE: Record<ReviewStatus, string> = {
  pending:
    "bg-slate-500/10 text-slate-600 dark:text-slate-300 border-slate-400/30",
  in_progress:
    "bg-sky-500/10 text-sky-600 dark:text-sky-400 border-sky-500/30",
  needs_changes:
    "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/30",
  approved:
    "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/30",
}

export function StatusPill({
  status,
  className,
}: {
  status: ReviewStatus
  className?: string
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium border tabular-nums",
        STATUS_STYLE[status],
        className,
      )}
    >
      <span
        className={cn(
          "w-1.5 h-1.5 rounded-full",
          status === "pending" && "bg-slate-400",
          status === "in_progress" && "bg-sky-500",
          status === "needs_changes" && "bg-amber-500",
          status === "approved" && "bg-emerald-500",
        )}
      />
      {STATUS_LABEL[status]}
    </span>
  )
}

export function statusBorderColor(status: ReviewStatus): string {
  return {
    pending: "border-l-slate-400",
    in_progress: "border-l-sky-500",
    needs_changes: "border-l-amber-500",
    approved: "border-l-emerald-500",
  }[status]
}
