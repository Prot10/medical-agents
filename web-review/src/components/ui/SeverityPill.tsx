import { cn } from "@/lib/utils"
import type { Severity } from "@/api/types"

const SEVERITY_STYLE: Record<Severity, string> = {
  note: "bg-sky-500/10 text-sky-600 dark:text-sky-400 border-sky-500/30",
  issue: "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/30",
  error: "bg-rose-500/10 text-rose-600 dark:text-rose-400 border-rose-500/30",
}

const SEVERITY_LABEL: Record<Severity, string> = {
  note: "Note",
  issue: "Issue",
  error: "Error",
}

export function SeverityPill({
  severity,
  className,
}: {
  severity: Severity
  className?: string
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center px-2 py-0.5 rounded-md text-[11px] font-medium border uppercase tracking-wide",
        SEVERITY_STYLE[severity],
        className,
      )}
    >
      {SEVERITY_LABEL[severity]}
    </span>
  )
}

