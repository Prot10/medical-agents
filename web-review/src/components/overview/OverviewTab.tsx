import { motion } from "framer-motion"
import {
  ArrowRight,
  BookOpenText,
  CheckCircle2,
  ChevronRight,
  Compass,
  Hourglass,
  ListChecks,
  Loader2,
  PlayCircle,
  ShieldAlert,
} from "lucide-react"
import { useMemo } from "react"

import type { ReviewStatus, ReviewerProfile } from "@/api/types"
import { useMyProgress, useMyReviews } from "@/hooks/useReview"
import { useReviewStore } from "@/stores/reviewStore"
import { Button } from "@/components/ui/Button"

const STATUS_COLOR: Record<ReviewStatus, string> = {
  pending: "bg-slate-400",
  in_progress: "bg-sky-500",
  needs_changes: "bg-amber-500",
  approved: "bg-emerald-500",
}

export function OverviewTab({ profile }: { profile: ReviewerProfile }) {
  const version = useReviewStore((s) => s.datasetVersion)
  const setActiveTab = useReviewStore((s) => s.setActiveTab)
  const setSelectedCaseId = useReviewStore((s) => s.setSelectedCaseId)
  const progress = useMyProgress(version)
  const myReviews = useMyReviews(version)

  const stats = progress.data
  const recent = useMemo(() => {
    const list = myReviews.data ?? []
    return list
      .filter((r) => !!r.last_updated_at)
      .sort((a, b) =>
        (b.last_updated_at ?? "") > (a.last_updated_at ?? "") ? 1 : -1,
      )
      .slice(0, 5)
  }, [myReviews.data])

  const isNewReviewer = stats !== undefined && stats.touched_cases === 0

  const milestones = stats
    ? [
        { label: "5 reviewed", target: 5, met: stats.touched_cases >= 5 },
        { label: "50 reviewed", target: 50, met: stats.touched_cases >= 50 },
        { label: "200 reviewed", target: 200, met: stats.touched_cases >= 200 },
        { label: stats.total_cases + " complete", target: stats.total_cases, met: stats.touched_cases >= stats.total_cases },
      ]
    : []

  return (
    <div className="px-6 py-8 max-w-6xl mx-auto w-full space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
      >
        <div className="flex items-baseline justify-between flex-wrap gap-2">
          <div>
            <p className="text-sm text-muted-foreground">
              Hello, {profile.name.split(" ")[0]}.
            </p>
            <h1 className="text-3xl font-semibold tracking-tight">
              Your review of {stats?.dataset_version ?? version}
            </h1>
          </div>
          <span className="text-sm text-muted-foreground">
            {stats ? `${stats.touched_cases} / ${stats.total_cases} cases touched` : null}
          </span>
        </div>
      </motion.div>

      {isNewReviewer && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, delay: 0.05 }}
          className="rounded-2xl border border-primary/20 bg-gradient-to-br from-primary/10 via-primary/5 to-emerald-500/5 p-6 sm:p-8"
        >
          <div className="flex items-start gap-4 flex-wrap">
            <div className="w-12 h-12 rounded-xl bg-primary/15 text-primary flex items-center justify-center">
              <Compass className="w-6 h-6" />
            </div>
            <div className="flex-1 min-w-0">
              <h2 className="text-lg font-semibold tracking-tight">
                Welcome aboard.
              </h2>
              <p className="text-sm text-muted-foreground leading-relaxed max-w-xl mt-1">
                {stats?.total_cases ?? 516} cases across {Object.keys(stats?.by_condition ?? {}).length || 20}{" "}
                neurological conditions are waiting for your review. Take a moment
                to skim the methodology, then start anywhere.
              </p>
              <div className="flex flex-wrap items-center gap-2 mt-4">
                <Button
                  onClick={() => {
                    setActiveTab("cases")
                    setSelectedCaseId(null)
                  }}
                >
                  <PlayCircle className="w-4 h-4" />
                  Start reviewing
                </Button>
                <Button
                  variant="secondary"
                  onClick={() => setActiveTab("methodology")}
                >
                  <BookOpenText className="w-4 h-4" />
                  Read the methodology
                </Button>
              </div>
            </div>
          </div>
        </motion.div>
      )}

      {!isNewReviewer && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.35, delay: 0.05 }}
          className="grid grid-cols-1 md:grid-cols-4 gap-3"
        >
          <StatCard
            label="Approved"
            value={stats?.by_status.approved ?? 0}
            tone="emerald"
            icon={<CheckCircle2 className="w-4 h-4" />}
          />
          <StatCard
            label="Needs changes"
            value={stats?.by_status.needs_changes ?? 0}
            tone="amber"
            icon={<ShieldAlert className="w-4 h-4" />}
          />
          <StatCard
            label="In progress"
            value={stats?.by_status.in_progress ?? 0}
            tone="sky"
            icon={<Loader2 className="w-4 h-4" />}
          />
          <StatCard
            label="Pending"
            value={stats?.by_status.pending ?? 0}
            tone="slate"
            icon={<Hourglass className="w-4 h-4" />}
          />
        </motion.div>
      )}

      {stats && (
        <div className="space-y-3">
          <div className="flex items-center justify-between text-sm">
            <span className="font-medium">Progress</span>
            <span className="text-muted-foreground tabular-nums">
              {Math.round((stats.touched_cases / Math.max(1, stats.total_cases)) * 100)}% touched
            </span>
          </div>
          <ProgressBar stats={stats} />
          <div className="flex items-center gap-3 flex-wrap text-xs text-muted-foreground">
            {milestones.map((m) => (
              <span
                key={m.label}
                className={
                  m.met
                    ? "px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30"
                    : "px-2 py-0.5 rounded-full bg-muted text-muted-foreground border border-border"
                }
              >
                {m.met ? "✓ " : ""}
                {m.label}
              </span>
            ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 rounded-xl border border-border bg-card p-5">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold tracking-tight">
              Recently reviewed
            </h3>
            <button
              type="button"
              onClick={() => setActiveTab("cases")}
              className="text-xs text-primary hover:underline flex items-center gap-1"
            >
              View all
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
          {recent.length === 0 ? (
            <p className="text-sm text-muted-foreground py-8 text-center">
              Nothing here yet — your touched cases will appear in this list.
            </p>
          ) : (
            <ul className="divide-y divide-border -mx-2">
              {recent.map((review) => (
                <li key={review.case_id}>
                  <button
                    type="button"
                    onClick={() => {
                      setSelectedCaseId(review.case_id)
                      setActiveTab("cases")
                    }}
                    className="w-full flex items-center justify-between px-2 py-2.5 rounded-md hover:bg-secondary/40 transition-colors text-left"
                  >
                    <span className="flex items-center gap-3 min-w-0">
                      <span
                        className={`w-2 h-2 rounded-full ${STATUS_COLOR[review.status]}`}
                      />
                      <span className="font-mono text-xs tracking-wider text-foreground/90">
                        {review.case_id}
                      </span>
                      <span className="text-xs text-muted-foreground truncate">
                        {review.annotation_count} annotations
                      </span>
                    </span>
                    <ChevronRight className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="rounded-xl border border-border bg-card p-5">
          <h3 className="text-sm font-semibold tracking-tight mb-4">
            Quick actions
          </h3>
          <div className="space-y-2">
            <Button
              variant="primary"
              className="w-full justify-start"
              onClick={() => {
                setSelectedCaseId(null)
                setActiveTab("cases")
              }}
            >
              <ListChecks className="w-4 h-4" />
              Browse cases
            </Button>
            <Button
              variant="secondary"
              className="w-full justify-start"
              onClick={() => setActiveTab("methodology")}
            >
              <BookOpenText className="w-4 h-4" />
              Methodology
            </Button>
            {profile.role === "admin" && (
              <Button
                variant="secondary"
                className="w-full justify-start"
                onClick={() => setActiveTab("admin")}
              >
                <ShieldAlert className="w-4 h-4" />
                Admin dashboard
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

function StatCard({
  label,
  value,
  tone,
  icon,
}: {
  label: string
  value: number
  tone: "emerald" | "amber" | "sky" | "slate"
  icon: React.ReactNode
}) {
  const tones = {
    emerald: "from-emerald-500/15 to-emerald-500/0 text-emerald-700 dark:text-emerald-300",
    amber: "from-amber-500/15 to-amber-500/0 text-amber-700 dark:text-amber-300",
    sky: "from-sky-500/15 to-sky-500/0 text-sky-700 dark:text-sky-300",
    slate: "from-slate-400/15 to-slate-400/0 text-slate-700 dark:text-slate-300",
  }
  return (
    <div className={`rounded-xl border border-border bg-gradient-to-br p-4 ${tones[tone]}`}>
      <div className="flex items-center gap-2 text-xs uppercase tracking-wider">
        {icon}
        <span>{label}</span>
      </div>
      <div className="text-3xl font-semibold tabular-nums mt-2">{value}</div>
    </div>
  )
}

function ProgressBar({
  stats,
}: {
  stats: { total_cases: number; by_status: Record<ReviewStatus, number> }
}) {
  const total = Math.max(1, stats.total_cases)
  const segments: { key: ReviewStatus; color: string }[] = [
    { key: "approved", color: "bg-emerald-500" },
    { key: "needs_changes", color: "bg-amber-500" },
    { key: "in_progress", color: "bg-sky-500" },
    { key: "pending", color: "bg-slate-300 dark:bg-slate-700" },
  ]
  return (
    <div className="flex h-2.5 rounded-full overflow-hidden bg-muted">
      {segments.map((seg) => {
        const value = stats.by_status[seg.key] ?? 0
        const pct = (value / total) * 100
        if (pct === 0) return null
        return (
          <div
            key={seg.key}
            className={`${seg.color} transition-all`}
            style={{ width: `${pct}%` }}
            title={`${seg.key}: ${value}`}
          />
        )
      })}
    </div>
  )
}
