import { motion } from "framer-motion"
import { ArrowLeft, ArrowRight, BrainCircuit, CheckCircle2, Loader2 } from "lucide-react"
import { useMemo } from "react"

import type { ReviewStatus, ReviewerProfile } from "@/api/types"
import { useCases, useMyReviews } from "@/hooks/useReview"
import { isDecided } from "@/hooks/useSetProgress"
import { conditionColor, conditionLabel } from "@/lib/conditions"
import { cn } from "@/lib/utils"
import { useReviewStore } from "@/stores/reviewStore"
import { GateBackground } from "./CodeEntryGate"

interface ConditionRow {
  condition: string
  total: number
  done: number
  started: number
}

/** First step of the full review: pick the condition to work on. */
export function ConditionPicker({ profile }: { profile: ReviewerProfile }) {
  const chooseWorkspace = useReviewStore((s) => s.chooseWorkspace)
  const chooseCondition = useReviewStore((s) => s.chooseCondition)
  const cases = useCases("neurobench")
  const reviews = useMyReviews("neurobench")

  const rows = useMemo<ConditionRow[]>(() => {
    const status = new Map<string, ReviewStatus>()
    for (const r of reviews.data ?? []) status.set(r.case_id, r.status)
    const byCondition = new Map<string, ConditionRow>()
    for (const c of cases.data ?? []) {
      const row = byCondition.get(c.condition) ?? { condition: c.condition, total: 0, done: 0, started: 0 }
      const s = status.get(c.case_id) ?? "pending"
      row.total += 1
      if (isDecided(s)) row.done += 1
      else if (s === "in_progress") row.started += 1
      byCondition.set(c.condition, row)
    }
    return [...byCondition.values()].sort((a, b) =>
      conditionLabel(a.condition).localeCompare(conditionLabel(b.condition)),
    )
  }, [cases.data, reviews.data])

  return (
    <div className="relative min-h-screen overflow-hidden bg-background px-4 sm:px-6 py-8 sm:py-12">
      <GateBackground />

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: "easeOut" }}
        className="relative z-10 w-full max-w-5xl mx-auto"
      >
        <div className="flex items-center justify-between gap-3 mb-8">
          <button
            type="button"
            onClick={() => chooseWorkspace(null)}
            className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground"
          >
            <ArrowLeft className="w-4 h-4" />
            Back
          </button>
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <span className="w-7 h-7 rounded-lg bg-primary/10 text-primary flex items-center justify-center">
              <BrainCircuit className="w-4 h-4" />
            </span>
            <span className="hidden sm:inline">Full review · {profile.name}</span>
          </div>
        </div>

        <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight">
          Which condition would you like to review?
        </h1>
        <p className="text-muted-foreground mt-2 mb-8 text-sm sm:text-base max-w-2xl">
          You will see only the cases of that condition, with your progress at the top. You can
          change condition at any time.
        </p>

        {cases.isLoading ? (
          <div className="flex items-center justify-center py-20 text-muted-foreground">
            <Loader2 className="w-5 h-5 animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
            {rows.map((row) => (
              <ConditionCard key={row.condition} row={row} onOpen={() => chooseCondition(row.condition)} />
            ))}
          </div>
        )}
      </motion.div>
    </div>
  )
}

function ConditionCard({ row, onOpen }: { row: ConditionRow; onOpen: () => void }) {
  const pct = row.total ? Math.round((row.done / row.total) * 100) : 0
  const finished = row.total > 0 && row.done === row.total
  const color = conditionColor(row.condition)
  return (
    <button
      type="button"
      onClick={onOpen}
      className={cn(
        "group text-left bg-card border rounded-xl p-4 flex flex-col gap-3 transition-all duration-200",
        "hover:-translate-y-0.5 hover:shadow-lg hover:border-primary/40",
        "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background",
        finished ? "border-emerald-500/40" : "border-border",
      )}
    >
      <div className="flex items-start justify-between gap-2">
        <span className="flex items-center gap-2 min-w-0">
          <span className="w-2.5 h-2.5 rounded-full flex-shrink-0" style={{ background: color }} />
          <span className="text-sm font-semibold leading-tight">{conditionLabel(row.condition)}</span>
        </span>
        {finished ? (
          <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0" />
        ) : (
          <ArrowRight className="w-4 h-4 text-muted-foreground opacity-0 -translate-x-1 group-hover:opacity-100 group-hover:translate-x-0 transition-all flex-shrink-0" />
        )}
      </div>
      <div>
        <div className="flex items-center justify-between text-[11px] text-muted-foreground mb-1.5 tabular-nums">
          <span>
            {row.done} of {row.total} reviewed
            {row.started > 0 && ` · ${row.started} started`}
          </span>
          <span>{pct}%</span>
        </div>
        <div className="h-1.5 rounded-full bg-muted overflow-hidden">
          <div
            className={cn("h-full rounded-full", finished ? "bg-emerald-500" : "bg-primary")}
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>
    </button>
  )
}
