import * as Popover from "@radix-ui/react-popover"
import { AnimatePresence, motion } from "framer-motion"
import { Loader2, Send, Trash2 } from "lucide-react"
import { useEffect, useMemo, useState } from "react"

import type { Severity } from "@/api/types"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/Button"
import { useAnnotationContext } from "./AnnotationContext"

const SEVERITY_LABEL: Record<Severity, string> = {
  note: "Note",
  issue: "Issue",
  error: "Error",
}

const SEVERITY_STYLE: Record<Severity, string> = {
  note: "bg-sky-500/10 text-sky-700 dark:text-sky-300 border-sky-500/60",
  issue: "bg-amber-500/10 text-amber-700 dark:text-amber-300 border-amber-500/60",
  error: "bg-rose-500/10 text-rose-700 dark:text-rose-300 border-rose-500/60",
}

export function AnnotationPopover() {
  const ctx = useAnnotationContext()
  const open = ctx.openPopover

  const existing = useMemo(() => {
    if (!open?.annotationId) return null
    return (
      ctx.review?.field_annotations.find((a) => a.id === open.annotationId) ??
      null
    )
  }, [ctx.review, open?.annotationId])

  const [severity, setSeverity] = useState<Severity>("note")
  const [comment, setComment] = useState("")
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [confirmingDiscard, setConfirmingDiscard] = useState(false)

  useEffect(() => {
    if (existing) {
      setSeverity(existing.severity)
      setComment(existing.comment)
    } else {
      setSeverity("note")
      setComment("")
    }
    setError(null)
    setConfirmingDiscard(false)
  }, [open?.fieldPath, open?.annotationId, existing])

  const isDirty =
    comment.trim() !== (existing?.comment ?? "").trim() ||
    (existing != null && severity !== existing.severity)

  function handleClose() {
    if (submitting) return
    if (isDirty) {
      setConfirmingDiscard(true)
      return
    }
    ctx.setOpenPopover(null)
  }

  function discardAndClose() {
    setConfirmingDiscard(false)
    ctx.setOpenPopover(null)
  }

  async function handleSubmit(e?: React.FormEvent) {
    if (e) e.preventDefault()
    if (!open) return
    const trimmed = comment.trim()
    if (!trimmed) {
      setError("Add a comment before saving.")
      return
    }
    setSubmitting(true)
    setError(null)
    try {
      if (existing) {
        await ctx.updateAnnotation(existing.id, {
          comment: trimmed,
          severity,
        })
      } else {
        await ctx.createAnnotation({
          fieldPath: open.fieldPath,
          fieldSnippet: open.fieldSnippet,
          comment: trimmed,
          severity,
        })
      }
      ctx.setOpenPopover(null)
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : "Could not save annotation.")
    } finally {
      setSubmitting(false)
    }
  }

  async function handleDelete() {
    if (!existing) return
    setSubmitting(true)
    try {
      await ctx.deleteAnnotation(existing.id)
      ctx.setOpenPopover(null)
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : "Could not delete annotation.")
    } finally {
      setSubmitting(false)
    }
  }

  function handleKeyDown(event: React.KeyboardEvent) {
    if ((event.metaKey || event.ctrlKey) && event.key === "Enter") {
      event.preventDefault()
      handleSubmit()
    }
  }

  return (
    <Popover.Root
      open={!!open}
      onOpenChange={(value) => {
        if (!value) handleClose()
      }}
    >
      <Popover.Anchor virtualRef={open ? { current: open.anchor } : undefined} />
      <AnimatePresence>
        {open && (
          <Popover.Portal forceMount>
            <Popover.Content
              align="start"
              sideOffset={8}
              collisionPadding={12}
              onOpenAutoFocus={(e) => e.preventDefault()}
              className="z-50 w-[min(360px,calc(100vw-1.5rem))] outline-none"
              asChild
            >
              <motion.div
                initial={{ opacity: 0, y: 6, scale: 0.98 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 4, scale: 0.97 }}
                transition={{ type: "spring", stiffness: 380, damping: 30 }}
                className="bg-popover border border-border rounded-xl shadow-xl p-4"
              >
                <FieldPathBreadcrumb path={open.fieldPath} />

                <div className="mt-3 flex items-center gap-1">
                  {(["note", "issue", "error"] as const).map((sev) => {
                    const active = severity === sev
                    return (
                      <button
                        key={sev}
                        type="button"
                        onClick={() => setSeverity(sev)}
                        className={cn(
                          "flex-1 px-2.5 py-1.5 text-xs font-medium rounded-md border transition-colors",
                          active
                            ? SEVERITY_STYLE[sev]
                            : "bg-secondary/40 text-muted-foreground border-transparent hover:bg-secondary/70",
                        )}
                      >
                        {SEVERITY_LABEL[sev]}
                      </button>
                    )
                  })}
                </div>

                <form onSubmit={handleSubmit} className="mt-3">
                  <textarea
                    autoFocus
                    value={comment}
                    onChange={(e) => setComment(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Describe the issue or note…"
                    rows={5}
                    className="w-full bg-background border border-input rounded-md text-sm p-3 leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-ring"
                  />
                  {error && (
                    <div className="text-xs text-rose-500 mt-2">{error}</div>
                  )}

                  {confirmingDiscard ? (
                    <div className="mt-3 rounded-md border border-amber-500/40 bg-amber-500/10 p-2.5 flex items-center justify-between gap-2">
                      <span className="text-xs text-amber-700 dark:text-amber-300">
                        Discard your unsaved note?
                      </span>
                      <div className="flex items-center gap-2">
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={() => setConfirmingDiscard(false)}
                        >
                          Keep editing
                        </Button>
                        <Button
                          type="button"
                          variant="destructive"
                          size="sm"
                          onClick={discardAndClose}
                        >
                          Discard
                        </Button>
                      </div>
                    </div>
                  ) : (
                    <div className="flex items-center justify-between gap-2 mt-3">
                      {existing ? (
                        <button
                          type="button"
                          onClick={handleDelete}
                          disabled={submitting}
                          className="inline-flex items-center gap-1 text-xs text-rose-500 hover:text-rose-600 disabled:opacity-50"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                          Delete
                        </button>
                      ) : (
                        <span className="text-[11px] text-muted-foreground">
                          ⌘↵ to save · Esc to dismiss
                        </span>
                      )}
                      <div className="flex items-center gap-2 ml-auto">
                        <Button
                          type="button"
                          variant="ghost"
                          size="sm"
                          onClick={handleClose}
                          disabled={submitting}
                        >
                          Cancel
                        </Button>
                        <Button
                          type="submit"
                          size="sm"
                          disabled={submitting || comment.trim().length === 0}
                        >
                          {submitting ? (
                            <>
                              <Loader2 className="w-3.5 h-3.5 animate-spin" />
                              Saving…
                            </>
                          ) : (
                            <>
                              <Send className="w-3.5 h-3.5" />
                              {existing ? "Save" : "Add"}
                            </>
                          )}
                        </Button>
                      </div>
                    </div>
                  )}
                </form>
              </motion.div>
            </Popover.Content>
          </Popover.Portal>
        )}
      </AnimatePresence>
    </Popover.Root>
  )
}

function FieldPathBreadcrumb({ path }: { path: string }) {
  const parts = path.split(/\.|(?=\[)/g).map((p) => p.replace(/\[(\d+)\]/, "[$1]"))
  return (
    <div className="flex items-center gap-1.5 flex-wrap font-mono text-[11px] text-muted-foreground tracking-wider uppercase">
      {parts.map((part, i) => (
        <span key={`${part}-${i}`} className="flex items-center gap-1.5">
          {i > 0 && <span className="opacity-50">›</span>}
          <span className={i === parts.length - 1 ? "text-foreground" : ""}>
            {part.replace(/_/g, " ")}
          </span>
        </span>
      ))}
    </div>
  )
}
