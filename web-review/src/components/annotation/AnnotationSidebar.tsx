import { ArrowRight, CheckCircle2, MessageSquarePlus, Pencil, RotateCcw, Send, Trash2, Unlink } from "lucide-react"
import { useEffect, useMemo, useState } from "react"

import type {
  CaseIndexEntry,
  CaseReviewSummary,
  DimensionDecision,
  FieldAnnotation,
  PolicyReviewVerdict,
  ReviewStatus,
  Severity,
} from "@/api/types"
import { cn } from "@/lib/utils"
import { fieldExists } from "@/lib/fieldPath"
import { Button } from "@/components/ui/Button"
import { SeverityPill } from "@/components/ui/SeverityPill"
import { useAnnotationContext } from "./AnnotationContext"

interface AnnotationSidebarProps {
  /** The case on screen; annotations whose field_path it no longer contains are flagged. */
  caseData: unknown
  status: ReviewStatus
  onSetStatus: (s: ReviewStatus, verdict?: PolicyReviewVerdict) => Promise<void>
  statusPending: boolean
  cases: CaseIndexEntry[]
  reviews: CaseReviewSummary[]
  currentCaseId: string
  onNavigate: (caseId: string) => void
  onCreateComment: (vars: {
    id: string
    comment: string
    severity: Severity
  }) => Promise<void>
  onDeleteComment: (commentId: string) => Promise<void>
}

const SEVERITIES: Severity[] = ["note", "issue", "error"]

function generateId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) return crypto.randomUUID()
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`
}

export function AnnotationSidebar({
  caseData,
  status,
  onSetStatus,
  statusPending,
  cases,
  reviews,
  currentCaseId,
  onNavigate,
  onCreateComment,
  onDeleteComment,
}: AnnotationSidebarProps) {
  const ctx = useAnnotationContext()
  const [filter, setFilter] = useState<Severity | "all">("all")

  const annotations = ctx.review?.field_annotations ?? []
  const comments = ctx.review?.case_comments ?? []

  const filtered = useMemo(() => {
    if (filter === "all") return annotations
    return annotations.filter((a) => a.severity === filter)
  }, [annotations, filter])

  const nextPending = useMemo(() => {
    const reviewByCase = new Map<string, CaseReviewSummary>()
    for (const r of reviews) reviewByCase.set(r.case_id, r)
    const currentIdx = cases.findIndex((c) => c.case_id === currentCaseId)
    if (currentIdx === -1) return null
    for (let i = currentIdx + 1; i < cases.length; i += 1) {
      const review = reviewByCase.get(cases[i].case_id)
      if (!review || review.status === "pending") return cases[i].case_id
    }
    for (let i = 0; i < currentIdx; i += 1) {
      const review = reviewByCase.get(cases[i].case_id)
      if (!review || review.status === "pending") return cases[i].case_id
    }
    return null
  }, [cases, currentCaseId, reviews])

  const severityCounts = useMemo(() => {
    const counts: Record<Severity, number> = { note: 0, issue: 0, error: 0 }
    for (const a of annotations) counts[a.severity] += 1
    return counts
  }, [annotations])

  return (
    <aside className="space-y-4">
      <PolicyReviewPanel
        status={status}
        existing={ctx.review?.policy_verdict ?? null}
        pending={statusPending}
        unresolvedErrors={annotations.filter((a) => a.severity === "error" && !a.resolved).length}
        onSubmit={onSetStatus}
      />
      {nextPending && (
        <Button
          size="sm"
          variant="secondary"
          className="w-full"
          onClick={() => onNavigate(nextPending)}
        >
          Next pending
          <ArrowRight className="w-4 h-4" />
        </Button>
      )}

      <CaseThread
        comments={comments}
        onCreate={async (input) => {
          await onCreateComment({ id: generateId(), ...input })
        }}
        onDelete={onDeleteComment}
      />

      <section className="bg-card border border-border rounded-2xl p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-xs uppercase tracking-wider text-muted-foreground font-semibold">
            Field annotations
            <span className="ml-2 text-foreground/80 tabular-nums">
              {annotations.length}
            </span>
          </h3>
        </div>
        <div className="flex flex-wrap gap-1 mb-3">
          <FilterChip
            label={`All ${annotations.length}`}
            active={filter === "all"}
            onClick={() => setFilter("all")}
          />
          {SEVERITIES.map((sev) => {
            const count = severityCounts[sev]
            if (count === 0) return null
            return (
              <FilterChip
                key={sev}
                label={`${sev} ${count}`}
                active={filter === sev}
                onClick={() => setFilter(sev)}
              />
            )
          })}
        </div>
        {filtered.length === 0 ? (
          <p className="text-xs text-muted-foreground py-6 text-center">
            No annotations yet. Hover a field on the left and click the comment
            icon to annotate.
          </p>
        ) : (
          <ul className="space-y-2">
            {filtered.map((annotation) => (
              <AnnotationListItem
                key={annotation.id}
                annotation={annotation}
                fieldMissing={!fieldExists(caseData, annotation.field_path)}
              />
            ))}
          </ul>
        )}
      </section>
    </aside>
  )
}


/**
 * One field annotation. The edit popover anchors to the field when it is on screen and to
 * this row otherwise, so an annotation on a field the case no longer has (written against an
 * earlier schema) can still be read, edited, resolved or deleted.
 */
function AnnotationListItem({
  annotation,
  fieldMissing,
}: {
  annotation: FieldAnnotation
  fieldMissing: boolean
}) {
  const ctx = useAnnotationContext()
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fieldElement = () => {
    const el = document.querySelector(
      `[data-annotatable-path="${cssEscape(annotation.field_path)}"]`,
    )
    return el instanceof HTMLElement ? el : null
  }

  const toggleResolved = async () => {
    setSaving(true)
    setError(null)
    try {
      await ctx.updateAnnotation(annotation.id, { resolved: !annotation.resolved })
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : "Could not update the annotation.")
    } finally {
      setSaving(false)
    }
  }

  return (
    <li
      className={cn(
        "border border-border rounded-lg p-3 text-xs space-y-1.5 bg-background/40",
        annotation.resolved && "opacity-60",
      )}
    >
      <div className="flex items-center justify-between gap-2 flex-wrap">
        <button
          type="button"
          onClick={() => {
            const el = fieldElement()
            if (el) {
              el.scrollIntoView({ behavior: "smooth", block: "center" })
              el.classList.add("attention-pulse")
              window.setTimeout(() => el.classList.remove("attention-pulse"), 800)
            }
          }}
          className={cn(
            "font-mono text-[10px] tracking-wider text-muted-foreground hover:text-foreground text-left break-all",
            fieldMissing && "line-through decoration-muted-foreground/50",
          )}
        >
          {annotation.field_path}
        </button>
        <div className="flex items-center gap-1">
          <SeverityPill severity={annotation.severity} />
          <button
            type="button"
            onClick={(event) => {
              const anchor = fieldElement() ?? event.currentTarget.closest("li")
              if (anchor instanceof HTMLElement) {
                ctx.setOpenPopover({
                  fieldPath: annotation.field_path,
                  anchor,
                  annotationId: annotation.id,
                })
              }
            }}
            className="w-6 h-6 rounded hover:bg-secondary/60 text-muted-foreground flex items-center justify-center"
            title="Edit annotation"
          >
            <Pencil className="w-3 h-3" />
          </button>
        </div>
      </div>
      {fieldMissing && (
        <div className="flex items-start gap-1.5 rounded-md border border-amber-500/30 bg-amber-500/5 px-2 py-1.5 text-[11px] text-amber-700 dark:text-amber-300">
          <Unlink className="w-3 h-3 mt-0.5 shrink-0" />
          <span>
            This field is no longer in the case (it was written against an earlier version of
            the case).
            {annotation.field_snippet && (
              <>
                {" "}It read: <span className="italic">“{annotation.field_snippet}”</span>
              </>
            )}
          </span>
        </div>
      )}
      <p className="text-foreground/90 leading-relaxed whitespace-pre-wrap">
        {annotation.comment}
      </p>
      <div className="flex items-center justify-between gap-2 pt-0.5">
        {annotation.resolved ? (
          <span className="inline-flex items-center gap-1 text-[11px] text-emerald-600 dark:text-emerald-400">
            <CheckCircle2 className="w-3 h-3" />
            Resolved
          </span>
        ) : (
          <span />
        )}
        <button
          type="button"
          onClick={toggleResolved}
          disabled={saving}
          className="inline-flex items-center gap-1 text-[11px] font-medium text-muted-foreground hover:text-foreground disabled:opacity-50"
        >
          {annotation.resolved ? (
            <>
              <RotateCcw className="w-3 h-3" />
              Reopen
            </>
          ) : (
            <>
              <CheckCircle2 className="w-3 h-3" />
              Mark resolved
            </>
          )}
        </button>
      </div>
      {error && <p className="text-[11px] text-rose-500">{error}</p>}
    </li>
  )
}

type DimensionKey =
  | "scenario_plausibility"
  | "diagnosis"
  | "actions"
  | "avoided_actions"
  | "sequencing"
  | "stopping"
  | "assessment"

const POLICY_DIMENSIONS: Array<[DimensionKey, string]> = [
  ["scenario_plausibility", "Scenario plausibility"],
  ["diagnosis", "Diagnosis standard"],
  ["actions", "Required / equivalent actions"],
  ["avoided_actions", "Waste and harmful-test labels"],
  ["sequencing", "Ordering constraints"],
  ["stopping", "Stop rule"],
  ["assessment", "Final recommendations"],
]

const DEFAULT_DECISIONS: Record<DimensionKey, DimensionDecision> = {
  scenario_plausibility: "approve",
  diagnosis: "approve",
  actions: "approve",
  avoided_actions: "approve",
  sequencing: "approve",
  stopping: "approve",
  assessment: "approve",
}

function PolicyReviewPanel({
  status,
  existing,
  pending,
  unresolvedErrors,
  onSubmit,
}: {
  status: ReviewStatus
  existing: PolicyReviewVerdict | null
  pending: boolean
  unresolvedErrors: number
  onSubmit: (status: ReviewStatus, verdict?: PolicyReviewVerdict) => Promise<void>
}) {
  const [decisions, setDecisions] =
    useState<Record<DimensionKey, DimensionDecision>>(DEFAULT_DECISIONS)
  const [comment, setComment] = useState("")
  // A case judged before the per-dimension verdict existed has a terminal status but no
  // verdict; start from that status (all "Revise" for needs_changes) so the earlier judgment
  // is not shown as an approval.
  const legacyTerminal = existing === null && (status === "approved" || status === "needs_changes")
  useEffect(() => {
    const next = { ...DEFAULT_DECISIONS }
    if (existing) {
      for (const [key] of POLICY_DIMENSIONS) next[key] = existing[key]
    } else if (status === "needs_changes") {
      for (const [key] of POLICY_DIMENSIONS) next[key] = "needs_revision"
    }
    setDecisions(next)
    setComment(existing?.comment ?? "")
  }, [existing, status])

  const allApproved = Object.values(decisions).every((value) => value === "approve")
  const submit = async () => {
    const verdict: PolicyReviewVerdict = { ...decisions, comment }
    await onSubmit(allApproved ? "approved" : "needs_changes", verdict)
  }

  return (
    <section className="bg-card border border-border rounded-2xl p-4">
      <h3 className="text-xs uppercase tracking-wider text-muted-foreground font-semibold">
        Physician policy review
      </h3>
      <p className="text-xs text-muted-foreground mt-1 mb-3">
        Judge each scoring dimension independently. Two concordant physician approvals are
        required; disagreement triggers a third review.
      </p>
      {legacyTerminal && (
        <p className="mb-3 rounded-md border border-amber-500/30 bg-amber-500/5 px-2 py-1.5 text-[11px] text-amber-700 dark:text-amber-300">
          You marked this case “{status === "approved" ? "approved" : "needs changes"}” before
          the per-dimension review existed. The dimensions start from that judgment: check each
          one and submit to record it.
        </p>
      )}
      <div className="space-y-2">
        {POLICY_DIMENSIONS.map(([key, label]) => (
          <div key={key} className="flex items-center justify-between gap-2 text-xs">
            <span>{label}</span>
            <div className="flex rounded-md border border-border overflow-hidden">
              {(["approve", "needs_revision"] as DimensionDecision[]).map((decision) => (
                <button
                  key={decision}
                  type="button"
                  onClick={() => setDecisions((value) => ({ ...value, [key]: decision }))}
                  className={cn(
                    "px-2 py-1",
                    decisions[key] === decision
                      ? decision === "approve"
                        ? "bg-emerald-500/15 text-emerald-700 dark:text-emerald-300"
                        : "bg-amber-500/15 text-amber-700 dark:text-amber-300"
                      : "text-muted-foreground hover:bg-secondary",
                  )}
                >
                  {decision === "approve" ? "Approve" : "Revise"}
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>
      <textarea
        value={comment}
        onChange={(event) => setComment(event.target.value)}
        placeholder="Required context for revisions; optional for approval"
        rows={2}
        className="mt-3 w-full bg-background border border-input rounded-md text-xs p-2 resize-none"
      />
      {unresolvedErrors > 0 && allApproved && (
        <p className="mt-2 text-xs text-rose-600">
          Resolve {unresolvedErrors} error annotation(s) before approval.
        </p>
      )}
      <div className="mt-3 grid grid-cols-2 gap-2">
        <Button
          size="sm"
          variant="secondary"
          onClick={() => onSubmit("in_progress")}
          disabled={pending || status === "in_progress"}
        >
          Save in progress
        </Button>
        <Button
          size="sm"
          onClick={submit}
          disabled={pending || (allApproved && unresolvedErrors > 0)}
        >
          {allApproved ? "Submit approval" : "Request revision"}
        </Button>
      </div>
    </section>
  )
}

function cssEscape(value: string): string {
  if (typeof CSS !== "undefined" && CSS.escape) return CSS.escape(value)
  return value.replace(/[^a-zA-Z0-9_-]/g, (c) => `\\${c}`)
}

function FilterChip({
  label,
  active,
  onClick,
}: {
  label: string
  active: boolean
  onClick: () => void
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "px-2 py-0.5 rounded-full text-[11px] font-medium uppercase tracking-wider transition-colors",
        active
          ? "bg-primary text-primary-foreground"
          : "bg-secondary/50 text-muted-foreground hover:bg-secondary",
      )}
    >
      {label}
    </button>
  )
}

function CaseThread({
  comments,
  onCreate,
  onDelete,
}: {
  comments: NonNullable<ReturnType<typeof useAnnotationContext>["review"]>["case_comments"]
  onCreate: (input: { comment: string; severity: Severity }) => Promise<void>
  onDelete: (commentId: string) => Promise<void>
}) {
  const [comment, setComment] = useState("")
  const [severity, setSeverity] = useState<Severity>("note")
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    const trimmed = comment.trim()
    if (!trimmed) return
    setSubmitting(true)
    try {
      await onCreate({ comment: trimmed, severity })
      setComment("")
      setSeverity("note")
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <section className="bg-card border border-border rounded-2xl p-4">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-xs uppercase tracking-wider text-muted-foreground font-semibold">
          Case-wide notes
          <span className="ml-2 text-foreground/80 tabular-nums">
            {comments.length}
          </span>
        </h3>
      </div>
      {comments.length > 0 && (
        <ul className="space-y-2 mb-3">
          {comments.map((c) => (
            <li
              key={c.id}
              className="border-l-2 border-primary/40 pl-3 py-1 text-sm relative group/comment"
            >
              <div className="flex items-center justify-between gap-2">
                <SeverityPill severity={c.severity} />
                <button
                  type="button"
                  onClick={() => onDelete(c.id)}
                  className="opacity-0 group-hover/comment:opacity-100 text-muted-foreground hover:text-rose-500 transition-opacity"
                  title="Delete"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
              <p className="text-foreground/95 mt-1 leading-relaxed whitespace-pre-wrap">
                {c.comment}
              </p>
            </li>
          ))}
        </ul>
      )}
      <form onSubmit={handleSubmit} className="space-y-2">
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Add a case-wide note…"
          rows={2}
          className="w-full bg-background border border-input rounded-md text-sm p-2 leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-ring"
        />
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-1">
            {SEVERITIES.map((sev) => (
              <button
                key={sev}
                type="button"
                onClick={() => setSeverity(sev)}
                className={cn(
                  "text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded border transition-colors",
                  severity === sev
                    ? sev === "note"
                      ? "bg-sky-500/15 text-sky-700 dark:text-sky-300 border-sky-500/60"
                      : sev === "issue"
                        ? "bg-amber-500/15 text-amber-700 dark:text-amber-300 border-amber-500/60"
                        : "bg-rose-500/15 text-rose-700 dark:text-rose-300 border-rose-500/60"
                    : "bg-secondary/40 text-muted-foreground border-transparent hover:bg-secondary/70",
                )}
              >
                {sev}
              </button>
            ))}
          </div>
          <Button
            type="submit"
            size="sm"
            disabled={submitting || comment.trim().length === 0}
          >
            {submitting ? (
              <Send className="w-3.5 h-3.5 animate-pulse" />
            ) : (
              <>
                <MessageSquarePlus className="w-3.5 h-3.5" />
                Add note
              </>
            )}
          </Button>
        </div>
      </form>
    </section>
  )
}
