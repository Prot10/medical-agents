import {
  ChartColumn,
  Flame,
  GitCompareArrows,
  Loader2,
  Users,
  Wrench,
} from "lucide-react"
import { useMemo, useState } from "react"

import { ReviewApiError } from "@/api/client"
import {
  useAdminAgreement,
  useAdminCaseDiff,
  useAdminHotspots,
  useAdminProgress,
} from "@/hooks/useReview"
import { useAdminToolReview } from "@/hooks/useToolReview"
import { conditionShort } from "@/lib/conditions"
import { cn, formatDuration } from "@/lib/utils"
import { useReviewStore } from "@/stores/reviewStore"
import { SeverityPill } from "@/components/ui/SeverityPill"
import { StatusPill } from "@/components/ui/StatusPill"
import type {
  AdminAgreementRow,
  CaseDiff,
  FieldHotspot,
  ReviewStatus,
} from "@/api/types"

type AdminView = "agreement" | "progress" | "hotspots" | "diff" | "tools"

const VIEWS: Array<{ id: AdminView; label: string; icon: React.ComponentType<{ className?: string }> }> = [
  { id: "agreement", label: "Inter-rater agreement", icon: GitCompareArrows },
  { id: "progress", label: "Reviewer progress", icon: ChartColumn },
  { id: "hotspots", label: "Field hotspots", icon: Flame },
  { id: "diff", label: "Side-by-side diff", icon: Users },
  { id: "tools", label: "Tool proposals", icon: Wrench },
]

export function AdminTab() {
  const [view, setView] = useState<AdminView>("agreement")

  return (
    <div className="px-4 sm:px-6 py-6 sm:py-8 max-w-7xl mx-auto w-full space-y-4">
      <div>
        <p className="text-xs uppercase tracking-widest text-primary font-semibold">
          Researcher view
        </p>
        <h1 className="text-2xl font-semibold tracking-tight">Admin dashboard</h1>
      </div>
      <div className="flex items-center gap-1 border-b border-border overflow-x-auto scrollbar-hide -mx-4 sm:mx-0 px-4 sm:px-0">
        {VIEWS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            type="button"
            onClick={() => setView(id)}
            className={cn(
              "px-3 sm:px-3.5 py-2 text-sm font-medium border-b-2 -mb-px flex items-center gap-1.5 transition-colors whitespace-nowrap flex-shrink-0",
              view === id
                ? "border-primary text-foreground"
                : "border-transparent text-muted-foreground hover:text-foreground",
            )}
          >
            <Icon className="w-3.5 h-3.5" />
            {label}
          </button>
        ))}
      </div>

      <div>
        {view === "agreement" && <AgreementView />}
        {view === "progress" && <ProgressView />}
        {view === "hotspots" && <HotspotsView />}
        {view === "diff" && <DiffView />}
        {view === "tools" && <ToolReviewView />}
      </div>
    </div>
  )
}

// --- Agreement -------------------------------------------------------

function AgreementView() {
  const version = useReviewStore((s) => s.datasetVersion)
  const { data, isLoading, error } = useAdminAgreement(version)
  const [search, setSearch] = useState("")
  const [consensusFilter, setConsensusFilter] = useState<string>("all")

  const filtered = useMemo(() => {
    if (!data) return [] as AdminAgreementRow[]
    return data.rows.filter((r) => {
      if (consensusFilter !== "all" && r.consensus !== consensusFilter) return false
      if (search && !r.case_id.toLowerCase().includes(search.toLowerCase())) return false
      return true
    })
  }, [data, consensusFilter, search])

  if (isLoading) return <CenteredLoader />
  if (error || !data) return <ErrorBox error={error} />

  return (
    <div className="space-y-4">
      <KappaCard kappa={data.kappa} />
      <SummaryStrip
        items={[
          {
            label: "Unanimous",
            value: data.consensus_summary.unanimous ?? 0,
            tone: "emerald",
          },
          {
            label: "Disagree",
            value: data.consensus_summary.disagree ?? 0,
            tone: "rose",
          },
          {
            label: "In review",
            value: data.consensus_summary.in_review ?? 0,
            tone: "sky",
          },
        ]}
      />

      <div className="flex flex-wrap items-center gap-2">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search case ID…"
          className="h-9 px-3 bg-secondary border border-border rounded-md text-sm w-64 focus:outline-none focus:ring-2 focus:ring-ring"
        />
        <select
          value={consensusFilter}
          onChange={(e) => setConsensusFilter(e.target.value)}
          className="h-9 px-2 bg-secondary border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
        >
          <option value="all">All cases</option>
          <option value="unanimous">Unanimous</option>
          <option value="disagree">Disagree</option>
          <option value="in_review">In review</option>
          <option value="agree">Agree</option>
        </select>
        <span className="text-xs text-muted-foreground ml-auto">
          {filtered.length} / {data.rows.length} cases
        </span>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-border bg-card">
        <table className="w-full text-sm">
          <thead className="bg-secondary/40 border-b border-border">
            <tr className="text-left text-xs uppercase tracking-wider text-muted-foreground">
              <th className="px-4 py-2.5 font-semibold">Case</th>
              <th className="px-4 py-2.5 font-semibold">Condition</th>
              {data.reviewer_codes.map((code) => (
                <th key={code} className="px-4 py-2.5 font-semibold">
                  {code}
                </th>
              ))}
              <th className="px-4 py-2.5 font-semibold">Consensus</th>
            </tr>
          </thead>
          <tbody>
            {filtered.slice(0, 200).map((row) => (
              <tr
                key={row.case_id}
                className="border-b border-border/60 hover:bg-secondary/20"
              >
                <td className="px-4 py-2 font-mono text-xs">{row.case_id}</td>
                <td className="px-4 py-2 text-xs text-muted-foreground">
                  {conditionShort(row.condition)}
                </td>
                {data.reviewer_codes.map((code) => (
                  <td key={code} className="px-4 py-2">
                    <StatusPill status={row.statuses[code]} />
                  </td>
                ))}
                <td className="px-4 py-2">
                  <ConsensusBadge consensus={row.consensus} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length > 200 && (
          <div className="px-4 py-2 text-xs text-muted-foreground border-t border-border">
            Showing first 200 of {filtered.length}. Narrow the filter to see the
            rest.
          </div>
        )}
      </div>
    </div>
  )
}

function KappaCard({ kappa }: { kappa: import("@/api/types").AgreementKappa }) {
  const hasValue = kappa.overall != null
  return (
    <div className="rounded-2xl border border-border bg-card p-4">
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div>
          <div className="text-xs uppercase tracking-wider text-muted-foreground">
            Inter-rater reliability
          </div>
          <div className="text-sm text-muted-foreground mt-0.5">
            Mean pairwise Cohen's κ on settled verdicts (approved vs. needs changes)
          </div>
        </div>
        <div className="text-right">
          <div className="text-3xl font-semibold tabular-nums">
            {hasValue ? kappa.overall!.toFixed(2) : "—"}
          </div>
          {kappa.interpretation && (
            <div className="text-xs uppercase tracking-wider text-muted-foreground">
              {kappa.interpretation}
            </div>
          )}
        </div>
      </div>
      {kappa.note && (
        <p className="text-xs text-muted-foreground mt-2">{kappa.note}</p>
      )}
      {kappa.pairs.length > 0 && (
        <div className="flex flex-wrap gap-1.5 mt-3">
          {kappa.pairs.map((p) => (
            <span
              key={`${p.a}-${p.b}`}
              className="text-[11px] tabular-nums px-2 py-0.5 rounded-full bg-secondary/60 text-muted-foreground"
              title={`${p.n} cases both settled`}
            >
              {p.a}↔{p.b}: <span className="font-mono">{p.kappa.toFixed(2)}</span> (n={p.n})
            </span>
          ))}
        </div>
      )}
    </div>
  )
}

function ConsensusBadge({ consensus }: { consensus: AdminAgreementRow["consensus"] }) {
  const style: Record<AdminAgreementRow["consensus"], string> = {
    unanimous:
      "bg-emerald-500/10 text-emerald-700 dark:text-emerald-300 border-emerald-500/40",
    agree:
      "bg-sky-500/10 text-sky-700 dark:text-sky-300 border-sky-500/40",
    in_review:
      "bg-slate-500/10 text-slate-700 dark:text-slate-300 border-slate-500/40",
    disagree:
      "bg-rose-500/10 text-rose-700 dark:text-rose-300 border-rose-500/40",
  }
  return (
    <span
      className={cn(
        "inline-block px-2 py-0.5 rounded-full text-[11px] border uppercase tracking-wider",
        style[consensus],
      )}
    >
      {consensus.replace(/_/g, " ")}
    </span>
  )
}

// --- Progress --------------------------------------------------------

function ProgressView() {
  const version = useReviewStore((s) => s.datasetVersion)
  const { data, isLoading, error } = useAdminProgress(version)
  if (isLoading) return <CenteredLoader />
  if (error || !data) return <ErrorBox error={error} />

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
      {data.map((r) => (
        <div
          key={r.code}
          className="rounded-2xl border border-border bg-card p-5 space-y-3"
        >
          <div className="flex items-baseline justify-between">
            <div>
              <div className="text-base font-semibold">{r.name}</div>
              <div className="font-mono text-[11px] tracking-wider text-muted-foreground">
                {r.code}
              </div>
            </div>
            <div className="text-2xl font-semibold tabular-nums">
              {r.touched_cases} / {r.total_cases}
            </div>
          </div>
          <StackedProgress byStatus={r.by_status} total={r.total_cases} />
          <div className="flex flex-wrap gap-1.5 pt-1">
            {(["approved", "needs_changes", "in_progress", "pending"] as ReviewStatus[]).map(
              (s) => (
                <span
                  key={s}
                  className="text-[11px] tabular-nums px-2 py-0.5 rounded-full bg-secondary/50"
                >
                  <span className="capitalize">{s.replace(/_/g, " ")}</span>{" "}
                  <span className="font-mono">{r.by_status[s] ?? 0}</span>
                </span>
              ),
            )}
          </div>
          <div className="flex flex-wrap gap-1.5 border-t border-border pt-3 text-[11px] text-muted-foreground">
            <span>
              Total time{" "}
              <span className="font-mono text-foreground">
                {formatDuration(r.total_time_spent_seconds)}
              </span>
            </span>
            <span>·</span>
            <span>
              Avg / case{" "}
              <span className="font-mono text-foreground">
                {formatDuration(r.avg_time_spent_seconds)}
              </span>
            </span>
          </div>
        </div>
      ))}
    </div>
  )
}

function StackedProgress({
  byStatus,
  total,
}: {
  byStatus: Record<string, number>
  total: number
}) {
  const segments: Array<{ key: string; color: string }> = [
    { key: "approved", color: "bg-emerald-500" },
    { key: "needs_changes", color: "bg-amber-500" },
    { key: "in_progress", color: "bg-sky-500" },
    { key: "pending", color: "bg-slate-300 dark:bg-slate-700" },
  ]
  return (
    <div className="flex h-2 rounded-full overflow-hidden bg-muted">
      {segments.map((s) => {
        const v = byStatus[s.key] ?? 0
        if (v === 0) return null
        return (
          <div
            key={s.key}
            className={s.color}
            style={{ width: `${(v / Math.max(1, total)) * 100}%` }}
            title={`${s.key}: ${v}`}
          />
        )
      })}
    </div>
  )
}

// --- Hotspots --------------------------------------------------------

function HotspotsView() {
  const version = useReviewStore((s) => s.datasetVersion)
  const { data, isLoading, error } = useAdminHotspots(version)
  const [search, setSearch] = useState("")
  if (isLoading) return <CenteredLoader />
  if (error || !data) return <ErrorBox error={error} />

  const filtered = data.filter((d) =>
    d.field_path.toLowerCase().includes(search.toLowerCase()),
  )

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search field path…"
          className="h-9 px-3 bg-secondary border border-border rounded-md text-sm w-80 focus:outline-none focus:ring-2 focus:ring-ring"
        />
        <span className="text-xs text-muted-foreground ml-auto">
          {filtered.length} flagged fields
        </span>
      </div>
      <div className="overflow-x-auto rounded-2xl border border-border bg-card">
        <table className="w-full text-sm">
          <thead className="bg-secondary/40 border-b border-border">
            <tr className="text-left text-xs uppercase tracking-wider text-muted-foreground">
              <th className="px-4 py-2.5 font-semibold">Field path</th>
              <th className="px-4 py-2.5 font-semibold">Reviewers</th>
              <th className="px-4 py-2.5 font-semibold">Severity</th>
              <th className="px-4 py-2.5 font-semibold">Cases</th>
              <th className="px-4 py-2.5 font-semibold">Latest comment</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((h: FieldHotspot) => (
              <tr key={h.field_path} className="border-b border-border/60">
                <td className="px-4 py-2 font-mono text-xs tracking-wider">
                  {h.field_path}
                </td>
                <td className="px-4 py-2 text-xs">
                  {h.reviewer_codes.join(", ")}
                </td>
                <td className="px-4 py-2">
                  <div className="flex items-center gap-1.5">
                    {(["note", "issue", "error"] as const).map((sev) => {
                      const c = h.by_severity[sev] ?? 0
                      if (c === 0) return null
                      return (
                        <span
                          key={sev}
                          className="text-[11px] tabular-nums inline-flex items-center gap-1"
                        >
                          <SeverityPill severity={sev} />
                          <span className="font-mono">{c}</span>
                        </span>
                      )
                    })}
                  </div>
                </td>
                <td className="px-4 py-2 text-xs font-mono">
                  {h.case_ids.length}
                </td>
                <td className="px-4 py-2 text-xs max-w-md">
                  <span className="line-clamp-2 text-muted-foreground">
                    {h.latest_comment}
                  </span>
                </td>
              </tr>
            ))}
            {filtered.length === 0 && (
              <tr>
                <td colSpan={5} className="text-center py-10 text-sm text-muted-foreground">
                  No flagged fields yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

// --- Side-by-side diff ----------------------------------------------

function DiffView() {
  const version = useReviewStore((s) => s.datasetVersion)
  const [caseId, setCaseId] = useState("")
  const [showAll, setShowAll] = useState(false)
  const { data, isLoading, error } = useAdminCaseDiff(version, caseId || null)

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-center gap-2">
        <input
          type="text"
          value={caseId}
          onChange={(e) => setCaseId(e.target.value.toUpperCase())}
          placeholder="Case ID (e.g. ALS-M01)"
          className="h-9 px-3 bg-secondary border border-border rounded-md text-sm w-64 font-mono tracking-wider focus:outline-none focus:ring-2 focus:ring-ring"
        />
        <label className="text-xs text-muted-foreground flex items-center gap-1">
          <input
            type="checkbox"
            checked={showAll}
            onChange={(e) => setShowAll(e.target.checked)}
          />
          Show fields without disagreement
        </label>
      </div>

      {!caseId && (
        <div className="rounded-2xl border border-dashed border-border bg-card/40 p-10 text-center text-sm text-muted-foreground">
          Enter a case ID to see all reviewers' annotations side by side.
        </div>
      )}
      {caseId && isLoading && <CenteredLoader />}
      {caseId && error && <ErrorBox error={error} />}
      {caseId && data && <DiffTable diff={data} showAll={showAll} />}
    </div>
  )
}

function DiffTable({ diff, showAll }: { diff: CaseDiff; showAll: boolean }) {
  const reviewers = diff.reviewers
  const rows = diff.field_rows.filter((row) => {
    if (showAll) return true
    const reviewerCount = Object.keys(row.by_reviewer).length
    if (reviewerCount === reviewers.length) {
      const severities = Object.values(row.by_reviewer).map((a) => a.severity)
      const allEqual = severities.every((s) => s === severities[0])
      if (allEqual) return false
    }
    return true
  })

  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-border bg-card p-4 flex items-center justify-between gap-3 flex-wrap">
        <div>
          <div className="font-mono text-xs text-muted-foreground tracking-wider">
            {diff.case_id}
          </div>
          <div className="text-base font-semibold mt-0.5 capitalize">
            {diff.consensus}
          </div>
        </div>
        <div className="flex items-center gap-4">
          {reviewers.map((r) => (
            <div key={r.code} className="text-right">
              <div className="text-xs text-muted-foreground">{r.name}</div>
              <StatusPill status={r.status} />
            </div>
          ))}
        </div>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-border bg-card">
        <table className="w-full text-sm">
          <thead className="bg-secondary/40 border-b border-border">
            <tr className="text-left text-xs uppercase tracking-wider text-muted-foreground">
              <th className="px-4 py-2.5 font-semibold w-1/3">Field</th>
              {reviewers.map((r) => (
                <th key={r.code} className="px-4 py-2.5 font-semibold">
                  {r.name}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.field_path} className="border-b border-border/60 align-top">
                <td className="px-4 py-3 font-mono text-xs tracking-wider">
                  {row.field_path}
                </td>
                {reviewers.map((r) => {
                  const annotation = row.by_reviewer[r.code]
                  if (!annotation)
                    return (
                      <td key={r.code} className="px-4 py-3 text-muted-foreground">
                        —
                      </td>
                    )
                  return (
                    <td key={r.code} className="px-4 py-3 space-y-1">
                      <SeverityPill severity={annotation.severity} />
                      <p className="text-xs leading-relaxed text-foreground/90 whitespace-pre-wrap">
                        {annotation.comment}
                      </p>
                    </td>
                  )
                })}
              </tr>
            ))}
            {rows.length === 0 && (
              <tr>
                <td
                  colSpan={reviewers.length + 1}
                  className="text-center py-10 text-sm text-muted-foreground"
                >
                  {showAll
                    ? "No annotations yet on this case."
                    : "Reviewers agree on every annotated field."}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="rounded-2xl border border-border bg-card p-4">
        <h3 className="text-xs uppercase tracking-wider text-muted-foreground font-semibold mb-3">
          Case-wide notes
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {reviewers.map((r) => (
            <div key={r.code} className="space-y-1.5">
              <div className="text-xs font-semibold">{r.name}</div>
              {r.case_comments.length === 0 ? (
                <p className="text-xs text-muted-foreground italic">
                  No case-wide notes.
                </p>
              ) : (
                <ul className="space-y-1.5">
                  {r.case_comments.map((c) => (
                    <li
                      key={c.id}
                      className="border-l-2 border-primary/40 pl-2 py-1 text-xs"
                    >
                      <SeverityPill severity={c.severity} />
                      <p className="mt-1 leading-relaxed whitespace-pre-wrap">
                        {c.comment}
                      </p>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

// --- Tool proposals & coverage ---------------------------------------

function ToolReviewView() {
  const version = useReviewStore((s) => s.datasetVersion)
  const { data, isLoading, error } = useAdminToolReview(version)
  if (isLoading) return <CenteredLoader />
  if (error || !data) return <ErrorBox error={error} />

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-sm font-semibold mb-2">Reviewer completion</h3>
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-2">
          {data.reviewer_status.map((r) => (
            <div
              key={r.reviewer_code}
              className="rounded-xl border border-border bg-card p-3"
            >
              <div className="text-sm font-medium truncate">{r.reviewer_name}</div>
              <div className="font-mono text-[10px] text-muted-foreground tracking-wider">
                {r.reviewer_code}
              </div>
              <div className="mt-2 flex items-center justify-between text-xs">
                <span
                  className={cn(
                    "px-2 py-0.5 rounded-full border text-[11px]",
                    r.completed
                      ? "border-emerald-500/40 bg-emerald-500/10 text-emerald-700 dark:text-emerald-300"
                      : r.started
                        ? "border-sky-500/40 bg-sky-500/10 text-sky-700 dark:text-sky-300"
                        : "border-slate-500/30 bg-slate-500/10 text-slate-600 dark:text-slate-300",
                  )}
                >
                  {r.completed ? "Reviewed" : r.started ? "In progress" : "Not started"}
                </span>
                <span className="text-muted-foreground tabular-nums">
                  {r.proposal_count}p · {r.annotation_count}f
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div>
        <h3 className="text-sm font-semibold mb-2">
          Proposed tools ({data.proposals.length})
        </h3>
        {data.proposals.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-border bg-card/40 p-10 text-center text-sm text-muted-foreground">
            No tools proposed yet.
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
            {data.proposals.map((p) => (
              <div key={p.id} className="rounded-2xl border border-border bg-card p-4">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-sm font-semibold">{p.name}</span>
                  {p.modality && (
                    <span className="text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded border border-border text-muted-foreground">
                      {p.modality}
                    </span>
                  )}
                  <span className="text-[11px] text-muted-foreground ml-auto">
                    {p.reviewer_name}
                  </span>
                </div>
                <p className="text-xs text-foreground/80 mt-1.5 leading-relaxed">
                  {p.description}
                </p>
                {p.rationale && (
                  <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                    <span className="font-medium">Why: </span>
                    {p.rationale}
                  </p>
                )}
                {p.target_conditions.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {p.target_conditions.map((k) => (
                      <span
                        key={k}
                        className="text-[10px] px-1.5 py-0.5 rounded-full bg-secondary/60 text-muted-foreground"
                      >
                        {conditionShort(k)}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      <div>
        <h3 className="text-sm font-semibold mb-2">
          Coverage flags ({data.coverage.length})
        </h3>
        {data.coverage.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-border bg-card/40 p-10 text-center text-sm text-muted-foreground">
            No coverage annotations yet.
          </div>
        ) : (
          <div className="overflow-x-auto rounded-2xl border border-border bg-card">
            <table className="w-full text-sm">
              <thead className="bg-secondary/40 border-b border-border">
                <tr className="text-left text-xs uppercase tracking-wider text-muted-foreground">
                  <th className="px-4 py-2.5 font-semibold">Target</th>
                  <th className="px-4 py-2.5 font-semibold">Reviewers</th>
                  <th className="px-4 py-2.5 font-semibold">Comments</th>
                </tr>
              </thead>
              <tbody>
                {data.coverage.map((row) => (
                  <tr key={row.field_path} className="border-b border-border/60 align-top">
                    <td className="px-4 py-3 font-mono text-xs tracking-wider">
                      {row.field_path}
                    </td>
                    <td className="px-4 py-3 text-xs">{row.reviewers.join(", ")}</td>
                    <td className="px-4 py-3 space-y-1.5">
                      {row.comments.map((c, i) => (
                        <div key={i} className="flex items-start gap-1.5">
                          <SeverityPill severity={c.severity} />
                          <p className="text-xs leading-relaxed text-foreground/90 whitespace-pre-wrap">
                            {c.comment}
                            <span className="text-muted-foreground">
                              {" "}
                              — {c.reviewer_name}
                            </span>
                          </p>
                        </div>
                      ))}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

// --- shared ----------------------------------------------------------

function CenteredLoader() {
  return (
    <div className="flex items-center justify-center py-20 text-muted-foreground">
      <Loader2 className="w-5 h-5 animate-spin" />
    </div>
  )
}

function ErrorBox({ error }: { error?: unknown }) {
  // Only surface ReviewApiError details — generic Error.message can leak
  // internal stack traces in dev builds, so we keep the fallback generic.
  const detail =
    error instanceof ReviewApiError ? error.message : null
  return (
    <div className="text-center py-12 text-rose-500 text-sm">
      <div>Could not load admin data.</div>
      {detail && (
        <div className="mt-1 text-xs text-rose-400/80 font-mono">{detail}</div>
      )}
    </div>
  )
}

function SummaryStrip({
  items,
}: {
  items: Array<{ label: string; value: number; tone: "emerald" | "rose" | "sky" }>
}) {
  return (
    <div className="grid grid-cols-3 gap-3">
      {items.map((item) => (
        <div
          key={item.label}
          className={cn(
            "rounded-xl border p-3",
            item.tone === "emerald" &&
              "border-emerald-500/30 bg-emerald-500/5 text-emerald-700 dark:text-emerald-300",
            item.tone === "rose" &&
              "border-rose-500/30 bg-rose-500/5 text-rose-700 dark:text-rose-300",
            item.tone === "sky" &&
              "border-sky-500/30 bg-sky-500/5 text-sky-700 dark:text-sky-300",
          )}
        >
          <div className="text-xs uppercase tracking-wider opacity-80">{item.label}</div>
          <div className="text-2xl font-semibold tabular-nums mt-1">
            {item.value}
          </div>
        </div>
      ))}
    </div>
  )
}

