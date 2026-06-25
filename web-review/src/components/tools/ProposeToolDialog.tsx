import * as Dialog from "@radix-ui/react-dialog"
import { AnimatePresence, motion } from "framer-motion"
import { Loader2, X } from "lucide-react"
import { useEffect, useState } from "react"

import type { ConditionToolMapping, ProposedTool } from "@/api/types"
import { Button } from "@/components/ui/Button"
import { useCreateProposal, useUpdateProposal } from "@/hooks/useToolReview"
import { cn } from "@/lib/utils"

export function ProposeToolDialog({
  version,
  conditions,
  open,
  onOpenChange,
  editing,
}: {
  version: string
  conditions: ConditionToolMapping[]
  open: boolean
  onOpenChange: (open: boolean) => void
  /** When set, the dialog edits an existing proposal instead of creating one. */
  editing?: ProposedTool | null
}) {
  const createMut = useCreateProposal(version)
  const updateMut = useUpdateProposal(version)

  const [name, setName] = useState("")
  const [description, setDescription] = useState("")
  const [rationale, setRationale] = useState("")
  const [modality, setModality] = useState("")
  const [targets, setTargets] = useState<string[]>([])
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!open) return
    setName(editing?.name ?? "")
    setDescription(editing?.description ?? "")
    setRationale(editing?.rationale ?? "")
    setModality(editing?.modality ?? "")
    setTargets(editing?.target_conditions ?? [])
    setError(null)
  }, [open, editing])

  function toggleTarget(key: string) {
    setTargets((prev) =>
      prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key],
    )
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!name.trim() || !description.trim()) {
      setError("Name and description are required.")
      return
    }
    setSubmitting(true)
    setError(null)
    try {
      if (editing) {
        await updateMut.mutateAsync({
          proposalId: editing.id,
          name: name.trim(),
          description: description.trim(),
          rationale: rationale.trim(),
          modality: modality.trim() || null,
          target_conditions: targets,
        })
      } else {
        await createMut.mutateAsync({
          id: crypto.randomUUID(),
          name: name.trim(),
          description: description.trim(),
          rationale: rationale.trim(),
          modality: modality.trim() || null,
          target_conditions: targets,
        })
      }
      onOpenChange(false)
    } catch (exc) {
      setError(exc instanceof Error ? exc.message : "Could not save the proposal.")
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <AnimatePresence>
        {open && (
          <Dialog.Portal forceMount>
            <Dialog.Overlay asChild>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm"
              />
            </Dialog.Overlay>
            <Dialog.Content asChild>
              <motion.div
                initial={{ opacity: 0, y: 12, scale: 0.98 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 8, scale: 0.98 }}
                transition={{ type: "spring", stiffness: 360, damping: 30 }}
                className="fixed left-1/2 top-1/2 z-50 w-[min(560px,calc(100vw-1.5rem))] max-h-[calc(100vh-2rem)] -translate-x-1/2 -translate-y-1/2 overflow-y-auto rounded-2xl border border-border bg-card p-6 shadow-2xl"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <Dialog.Title className="text-lg font-semibold">
                      {editing ? "Edit proposed tool" : "Propose a new tool"}
                    </Dialog.Title>
                    <Dialog.Description className="text-sm text-muted-foreground mt-0.5">
                      Suggest a diagnostic capability the agent is missing.
                    </Dialog.Description>
                  </div>
                  <Dialog.Close asChild>
                    <button
                      type="button"
                      className="text-muted-foreground hover:text-foreground"
                      aria-label="Close"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </Dialog.Close>
                </div>

                <form onSubmit={handleSubmit} className="mt-5 space-y-4">
                  <Field label="Tool name" required>
                    <input
                      autoFocus
                      value={name}
                      onChange={(e) => setName(e.target.value)}
                      maxLength={120}
                      placeholder="e.g. Order genetic counseling"
                      className="w-full h-9 px-3 bg-background border border-input rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                    />
                  </Field>

                  <Field label="What it does" required>
                    <textarea
                      value={description}
                      onChange={(e) => setDescription(e.target.value)}
                      maxLength={4000}
                      rows={3}
                      placeholder="Describe the test/action and the output it returns."
                      className="w-full bg-background border border-input rounded-md text-sm p-3 leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-ring"
                    />
                  </Field>

                  <Field label="Why it's needed">
                    <textarea
                      value={rationale}
                      onChange={(e) => setRationale(e.target.value)}
                      maxLength={4000}
                      rows={2}
                      placeholder="What gap in the current tool list does it fill?"
                      className="w-full bg-background border border-input rounded-md text-sm p-3 leading-relaxed resize-none focus:outline-none focus:ring-2 focus:ring-ring"
                    />
                  </Field>

                  <Field label="Modality / category (optional)">
                    <input
                      value={modality}
                      onChange={(e) => setModality(e.target.value)}
                      maxLength={120}
                      placeholder="e.g. genetics, neurophysiology, imaging"
                      className="w-full h-9 px-3 bg-background border border-input rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
                    />
                  </Field>

                  <Field label="Relevant conditions">
                    <div className="flex flex-wrap gap-1.5">
                      {conditions.map((c) => {
                        const active = targets.includes(c.condition)
                        return (
                          <button
                            key={c.condition}
                            type="button"
                            onClick={() => toggleTarget(c.condition)}
                            className={cn(
                              "px-2.5 py-1 rounded-full text-xs border transition-colors",
                              active
                                ? "bg-primary/15 text-primary border-primary/50"
                                : "bg-secondary/40 text-muted-foreground border-transparent hover:bg-secondary/70",
                            )}
                          >
                            {c.label}
                          </button>
                        )
                      })}
                    </div>
                  </Field>

                  {error && <div className="text-xs text-rose-500">{error}</div>}

                  <div className="flex items-center justify-end gap-2 pt-2">
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => onOpenChange(false)}
                      disabled={submitting}
                    >
                      Cancel
                    </Button>
                    <Button type="submit" size="sm" disabled={submitting}>
                      {submitting ? (
                        <Loader2 className="w-3.5 h-3.5 animate-spin" />
                      ) : editing ? (
                        "Save changes"
                      ) : (
                        "Submit proposal"
                      )}
                    </Button>
                  </div>
                </form>
              </motion.div>
            </Dialog.Content>
          </Dialog.Portal>
        )}
      </AnimatePresence>
    </Dialog.Root>
  )
}

function Field({
  label,
  required,
  children,
}: {
  label: string
  required?: boolean
  children: React.ReactNode
}) {
  return (
    <label className="block space-y-1.5">
      <span className="text-xs font-medium text-muted-foreground">
        {label}
        {required && <span className="text-rose-500"> *</span>}
      </span>
      {children}
    </label>
  )
}
