import { Check, CircleDot, CircleDashed, ShieldAlert, ShieldCheck } from "lucide-react"

import type { ReviewStatus } from "@/api/types"
import { cn } from "@/lib/utils"

const STATUSES: Array<{
  value: ReviewStatus
  label: string
  icon: React.ComponentType<{ className?: string }>
  activeStyle: string
}> = [
  {
    value: "pending",
    label: "Pending",
    icon: CircleDashed,
    activeStyle: "bg-slate-500/15 text-slate-700 dark:text-slate-200 border-slate-400",
  },
  {
    value: "in_progress",
    label: "In progress",
    icon: CircleDot,
    activeStyle: "bg-sky-500/15 text-sky-700 dark:text-sky-300 border-sky-500",
  },
  {
    value: "needs_changes",
    label: "Needs changes",
    icon: ShieldAlert,
    activeStyle:
      "bg-amber-500/15 text-amber-700 dark:text-amber-300 border-amber-500",
  },
  {
    value: "approved",
    label: "Approved",
    icon: ShieldCheck,
    activeStyle:
      "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border-emerald-500",
  },
]

export function StatusSwitcher({
  status,
  onChange,
  disabled,
}: {
  status: ReviewStatus
  onChange: (next: ReviewStatus) => void
  disabled?: boolean
}) {
  return (
    <div className="grid grid-cols-2 gap-1.5">
      {STATUSES.map(({ value, label, icon: Icon, activeStyle }) => {
        const active = status === value
        return (
          <button
            key={value}
            type="button"
            disabled={disabled}
            onClick={() => onChange(value)}
            className={cn(
              "flex items-center gap-2 px-2.5 py-2 rounded-md border text-xs font-medium transition-all text-left",
              active
                ? `${activeStyle} border`
                : "border-transparent bg-secondary/40 text-muted-foreground hover:bg-secondary/70 hover:text-foreground",
              disabled && "opacity-50 cursor-not-allowed",
            )}
          >
            <Icon className="w-3.5 h-3.5 flex-shrink-0" />
            <span className="truncate">{label}</span>
            {active && <Check className="w-3.5 h-3.5 ml-auto flex-shrink-0" />}
          </button>
        )
      })}
    </div>
  )
}
