import * as Popover from "@radix-ui/react-popover"
import { AnimatePresence, motion } from "framer-motion"
import { Loader2, Send, Trash2 } from "lucide-react"
import { useEffect, useMemo, useState } from "react"

import type { Severity, ToolReview } from "@/api/types"
import { Button } from "@/components/ui/Button"
import {
  useCreateToolAnnotation,
  useDeleteToolAnnotation,
  useUpdateToolAnnotation,
} from "@/hooks/useToolReview"
import { cn } from "@/lib/utils"

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

export interface ToolAnnotationTarget {
  fieldPath: string
  label: string
  anchor: HTMLElement
}

/**
 * Comment/flag popover for a tool-review target (a tool, a condition's tool
 * coverage, etc.). One annotation per field_path: editing replaces it.
 */
export function ToolAnnotationPopover({
  version,
  review,
  target,
  onClose,
}: {
  version: string
  review: ToolReview | undefined
  target: ToolAnnotationTarget | null
  onClose: () => void
}) {
  const createMut = useCreateToolAnnotation(version)
  const updateMut = useUpdateToolAnnotation(version)
  const deleteMut = useDeleteToolAnnotation(version)

  const existing = useMemo(() => {
    if (!target || !review) return null
    return (
      review.field_annotations.find((a) => a.field_path === target.fieldPath) ??
      null
    )
  }, [review, target])

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
  }, [target?.fieldPath, existing])

  const isDirty =
    comment.trim() !== (existing?.comment ?? "").trim() ||
    (existing != null && severity !== existing.severity)

  function handleClose() {
    if (submitting) return
    if (isDirty) {
      setConfirmingDiscard(true)
      return
    }
    onClose()
  }

  function discardAndClose() {
    setConfirmingDiscard(false)
    onClose()
  }

  async function handleSubmit(e?: React.FormEvent) {
    if (e) e.preventDefault()
    if (!target) return
    const trimmed = comment.trim()
    if (!trimmed) {
      setError("Add a comment before saving.")
      return
    }
    setSubmitting(true)
    setError(null)
    try {
      if (existing) {
        await updateMut.mutateAsync({
          annotationId: existing.id,
          comment: trimmed,
          severity,
        })
      } else {
        await createMut.mutateAsync({
          id: crypto.randomUUID(),
          field_path: target.fieldPath,
          field_snippet: target.label,
          comment: trimmed,
          severity,
        })
      }
      onClose()
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : "Could not save.")
    } finally {
      setSubmitting(false)
    }
  }

  async function handleDelete() {
    if (!existing) return
    setSubmitting(true)
    try {
      await deleteMut.mutateAsync(existing.id)
      onClose()
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : "Could not delete.")
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
      open={!!target}
      onOpenChange={(value) => {
        if (!value) handleClose()
      }}
    >
      <Popover.Anchor
        virtualRef={target ? { current: target.anchor } : undefined}
      />
      <AnimatePresence>
        {target && (
          <Popover.Portal forceMount>
            <Popover.Content
              align="end"
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
                <div className="text-[11px] font-medium uppercase tracking-wider text-muted-foreground">
                  {target.label}
                </div>

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
                    placeholder="Is this tool right for this condition? Note a gap or issue…"
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
