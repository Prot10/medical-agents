import { ChevronDown, ChevronRight, Eye, Loader2, MessageSquareText } from "lucide-react"
import { useMemo, useState } from "react"

import type { CaseDiff, Severity } from "@/api/types"
import { useAdminCaseDiff } from "@/hooks/useReview"
import { cn } from "@/lib/utils"
import { SeverityPill } from "@/components/ui/SeverityPill"
import { StatusPill } from "@/components/ui/StatusPill"

/**
 * Admin-only, read-only view of every clinical review on the case currently
 * open in the Cases workspace.  This deliberately uses the protected admin
 * endpoint rather than exposing another reviewer's file through the normal
 * reviewer API.
 */
export function ReviewerAnnotationsPanel({
  version,
  caseId,
}: {
  version: string
  caseId: string
}) {
  const [open, setOpen] = useState(true)
  const [severity, setSeverity] = useState<Severity | "all">("all")
  const { data, isLoading, error } = useAdminCaseDiff(version, caseId)

  const annotationCount = useMemo(
    () => data?.field_rows.reduce((total, row) => total + Object.keys(row.by_reviewer).length, 0) ?? 0,
    [data],
  )

  return (
    <section className="bg-card border border-primary/25 rounded-2xl overflow-hidden">
      <button
        type="button"
        onClick={() => setOpen((value) => !value)}
        className="w-full px-4 py-3 flex items-center justify-between gap-3 text-left hover:bg-secondary/30 transition-colors"
        aria-expanded={open}
      >
        <span className="flex items-center gap-2 min-w-0">
          <Eye className="w-4 h-4 text-primary shrink-0" />
          <span>
            <span className="block text-xs uppercase tracking-wider text-muted-foreground font-semibold">
              Reviewer annotations
            </span>
            <span className="block text-[11px] text-muted-foreground mt-0.5">
              Admin-only · all reviewers on this case
            </span>
          </span>
        </span>
        <span className="flex items-center gap-2 text-xs text-muted-foreground">
          {data && <span className="tabular-nums">{annotationCount}</span>}
          {open ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        </span>
      </button>

      {open && (
        <div className="border-t border-border p-4 space-y-4">
          {isLoading && (
            <div className="flex justify-center py-6 text-muted-foreground">
              <Loader2 className="w-4 h-4 animate-spin" />
            </div>
          )}
          {error && (
            <p className="text-xs text-rose-500 leading-relaxed">
              Could not load reviewer annotations for this case.
            </p>
          )}
          {data && <ReviewerAnnotationContents diff={data} severity={severity} onSeverity={setSeverity} />}
        </div>
      )}
    </section>
  )
}

function ReviewerAnnotationContents({
  diff,
  severity,
  onSeverity,
}: {
  diff: CaseDiff
  severity: Severity | "all"
  onSeverity: (value: Severity | "all") => void
}) {
  const rows = diff.field_rows.filter((row) =>
    Object.values(row.by_reviewer).some((annotation) =>
      severity === "all" || annotation.severity === severity,
    ),
  )
  const notes = diff.reviewers.flatMap((reviewer) => reviewer.case_comments)

  return (
    <>
      <div className="grid grid-cols-1 gap-2">
        {diff.reviewers.map((reviewer) => (
          <div key={reviewer.code} className="rounded-lg bg-secondary/35 px-3 py-2 flex items-center justify-between gap-2">
            <div className="min-w-0">
              <div className="text-xs font-medium truncate">{reviewer.name}</div>
              <div className="font-mono text-[10px] text-muted-foreground">{reviewer.code}</div>
            </div>
            <div className="text-right shrink-0">
              <StatusPill status={reviewer.status} />
              <div className="text-[10px] text-muted-foreground mt-1 tabular-nums">
                {reviewer.annotation_count} fields · {reviewer.comment_count} notes
              </div>
            </div>
          </div>
        ))}
      </div>

      {notes.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center gap-1.5 text-xs font-semibold">
            <MessageSquareText className="w-3.5 h-3.5 text-muted-foreground" />
            Case-wide notes
          </div>
          {diff.reviewers.flatMap((reviewer) => reviewer.case_comments.map((comment) => ({ reviewer, comment }))).map(({ reviewer, comment }) => (
            <article key={comment.id} className="border-l-2 border-primary/35 pl-2.5 py-1 text-xs">
              <div className="flex items-center gap-1.5 flex-wrap">
                <span className="font-medium">{reviewer.name}</span>
                <SeverityPill severity={comment.severity} />
              </div>
              <p className="mt-1 text-foreground/90 leading-relaxed whitespace-pre-wrap">{comment.comment}</p>
            </article>
          ))}
        </div>
      )}

      <div>
        <div className="flex items-center justify-between gap-2 mb-2">
          <span className="text-xs font-semibold">Field annotations</span>
          <div className="flex gap-1" aria-label="Filter reviewer annotations by severity">
            {(["all", "note", "issue", "error"] as const).map((value) => (
              <button
                key={value}
                type="button"
                onClick={() => onSeverity(value)}
                className={cn(
                  "px-1.5 py-0.5 rounded text-[10px] uppercase tracking-wide transition-colors",
                  severity === value ? "bg-primary text-primary-foreground" : "bg-secondary/70 text-muted-foreground hover:text-foreground",
                )}
              >
                {value}
              </button>
            ))}
          </div>
        </div>

        {rows.length === 0 ? (
          <p className="text-xs text-muted-foreground py-3 text-center">
            No reviewer annotations match this filter.
          </p>
        ) : (
          <div className="space-y-2">
            {rows.map((row) => (
              <article key={row.field_path} className="rounded-lg border border-border bg-background/40 p-2.5 space-y-2">
                <button
                  type="button"
                  onClick={() => focusField(row.field_path)}
                  className="block max-w-full font-mono text-[10px] tracking-wider text-muted-foreground hover:text-primary text-left break-all"
                  title="Jump to this field in the case"
                >
                  {row.field_path}
                </button>
                {diff.reviewers.map((reviewer) => {
                  const annotation = row.by_reviewer[reviewer.code]
                  if (!annotation || (severity !== "all" && annotation.severity !== severity)) return null
                  return (
                    <div key={annotation.id} className="text-xs">
                      <div className="flex items-center gap-1.5 flex-wrap">
                        <span className="font-medium">{reviewer.name}</span>
                        <SeverityPill severity={annotation.severity} />
                      </div>
                      <p className="mt-1 text-foreground/90 leading-relaxed whitespace-pre-wrap">{annotation.comment}</p>
                    </div>
                  )
                })}
              </article>
            ))}
          </div>
        )}
      </div>
    </>
  )
}

function focusField(fieldPath: string) {
  const escaped = typeof CSS !== "undefined" && CSS.escape
    ? CSS.escape(fieldPath)
    : fieldPath.replace(/[^a-zA-Z0-9_-]/g, (char) => `\\${char}`)
  const element = document.querySelector(`[data-annotatable-path="${escaped}"]`)
  if (!(element instanceof HTMLElement)) return
  element.scrollIntoView({ behavior: "smooth", block: "center" })
  element.classList.add("attention-pulse")
  window.setTimeout(() => element.classList.remove("attention-pulse"), 800)
}
