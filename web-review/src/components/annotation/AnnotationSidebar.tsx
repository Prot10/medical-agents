import { ArrowRight, MessageSquarePlus, Pencil, Send, ShieldCheck, Trash2 } from "lucide-react"
import { useMemo, useState } from "react"

import type {
  CaseIndexEntry,
  CaseReviewSummary,
  ReviewStatus,
  Severity,
} from "@/api/types"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/Button"
import { SeverityPill } from "@/components/ui/SeverityPill"
import { useAnnotationContext } from "./AnnotationContext"
import { StatusSwitcher } from "./StatusSwitcher"

interface AnnotationSidebarProps {
  status: ReviewStatus
  onSetStatus: (s: ReviewStatus) => Promise<void>
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

  function severityCount(severity: Severity): number {
    return annotations.filter((a) => a.severity === severity).length
  }

  return (
    <aside className="space-y-4">
      <section className="bg-card border border-border rounded-2xl p-4">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-xs uppercase tracking-wider text-muted-foreground font-semibold">
            Status
          </h3>
        </div>
        <StatusSwitcher
          status={status}
          onChange={onSetStatus}
          disabled={statusPending}
        />
        <div className="mt-3 flex flex-wrap items-center gap-2">
          <Button
            size="sm"
            className="flex-1 min-w-0"
            onClick={() => onSetStatus("approved")}
            disabled={statusPending || status === "approved"}
          >
            <ShieldCheck className="w-4 h-4" />
            Approve case
          </Button>
          {nextPending && (
            <Button
              size="sm"
              variant="secondary"
              onClick={() => onNavigate(nextPending)}
            >
              Next pending
              <ArrowRight className="w-4 h-4" />
            </Button>
          )}
        </div>
      </section>

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
            const count = severityCount(sev)
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
              <li
                key={annotation.id}
                className="border border-border rounded-lg p-3 text-xs space-y-1.5 bg-background/40"
              >
                <div className="flex items-center justify-between gap-2 flex-wrap">
                  <button
                    type="button"
                    onClick={() => {
                      const el = document.querySelector(
                        `[data-annotatable-path="${cssEscape(annotation.field_path)}"]`,
                      )
                      if (el instanceof HTMLElement) {
                        el.scrollIntoView({ behavior: "smooth", block: "center" })
                        el.classList.add("attention-pulse")
                        window.setTimeout(
                          () => el.classList.remove("attention-pulse"),
                          800,
                        )
                      }
                    }}
                    className="font-mono text-[10px] tracking-wider text-muted-foreground hover:text-foreground"
                  >
                    {annotation.field_path}
                  </button>
                  <div className="flex items-center gap-1">
                    <SeverityPill severity={annotation.severity} />
                    <button
                      type="button"
                      onClick={() => {
                        const el = document.querySelector(
                          `[data-annotatable-path="${cssEscape(annotation.field_path)}"]`,
                        )
                        if (el instanceof HTMLElement) {
                          ctx.setOpenPopover({
                            fieldPath: annotation.field_path,
                            anchor: el,
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
                <p className="text-foreground/90 leading-relaxed whitespace-pre-wrap">
                  {annotation.comment}
                </p>
              </li>
            ))}
          </ul>
        )}
      </section>
    </aside>
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
