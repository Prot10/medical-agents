import * as Dialog from "@radix-ui/react-dialog"
import { AnimatePresence, motion } from "framer-motion"
import { X } from "lucide-react"

import { SeverityPill } from "@/components/ui/SeverityPill"
import { StatusPill } from "@/components/ui/StatusPill"
import type { ReviewStatus, Severity } from "@/api/types"

const SEVERITY_HELP: Array<{ severity: Severity; meaning: string }> = [
  {
    severity: "note",
    meaning:
      "A remark or suggestion — not necessarily wrong, but worth recording (style, phrasing, a question).",
  },
  {
    severity: "issue",
    meaning:
      "Something likely incorrect or inconsistent that should be reviewed and probably changed.",
  },
  {
    severity: "error",
    meaning:
      "A clear factual or clinical error that must be fixed before the case is usable.",
  },
]

const STATUS_HELP: Array<{ status: ReviewStatus; meaning: string }> = [
  { status: "pending", meaning: "Not yet opened or reviewed." },
  {
    status: "in_progress",
    meaning: "You've started — set automatically once you add your first note.",
  },
  {
    status: "needs_changes",
    meaning: "You found problems the case authors must address.",
  },
  {
    status: "approved",
    meaning: "Clinically sound and ready as-is, in your judgment.",
  },
]

export function GuidelinesDialog({
  open,
  onOpenChange,
}: {
  open: boolean
  onOpenChange: (open: boolean) => void
}) {
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
                className="fixed left-1/2 top-1/2 z-50 w-[min(640px,calc(100vw-1.5rem))] max-h-[calc(100vh-2rem)] -translate-x-1/2 -translate-y-1/2 overflow-y-auto rounded-2xl border border-border bg-card p-6 shadow-2xl"
              >
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <Dialog.Title className="text-lg font-semibold">
                      How to review
                    </Dialog.Title>
                    <Dialog.Description className="text-sm text-muted-foreground mt-0.5">
                      A quick guide to annotating NeuroBench cases.
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

                <div className="mt-5 space-y-6 text-sm leading-relaxed">
                  <section className="space-y-2">
                    <h3 className="font-semibold">What we're asking</h3>
                    <p className="text-muted-foreground">
                      Read each case as if it were a real patient handed to you.
                      Flag anything that is clinically inaccurate, internally
                      inconsistent, unrealistic, or that gives away the diagnosis
                      in a way a real report wouldn't. Your annotations are private
                      to your reviewer code; we compare reviewers afterwards.
                    </p>
                  </section>

                  <section className="space-y-2">
                    <h3 className="font-semibold">How to annotate</h3>
                    <ul className="list-disc pl-5 space-y-1 text-muted-foreground">
                      <li>
                        Hover any field and click the{" "}
                        <span className="font-medium text-foreground">Comment</span>{" "}
                        pill to attach a note to that exact field.
                      </li>
                      <li>
                        Pick a severity, write your comment, and press{" "}
                        <kbd className="px-1.5 py-0.5 rounded bg-secondary text-[11px] font-mono">
                          ⌘↵
                        </kbd>{" "}
                        (or Ctrl+Enter) to save.
                      </li>
                      <li>
                        Use{" "}
                        <span className="font-medium text-foreground">
                          case-wide notes
                        </span>{" "}
                        in the sidebar for comments about the whole case.
                      </li>
                      <li>
                        When you're done with a case, set its status to{" "}
                        <span className="font-medium text-foreground">
                          Approved
                        </span>{" "}
                        or{" "}
                        <span className="font-medium text-foreground">
                          Needs changes
                        </span>
                        .
                      </li>
                    </ul>
                  </section>

                  <section className="space-y-3">
                    <h3 className="font-semibold">Severity levels</h3>
                    <div className="space-y-2">
                      {SEVERITY_HELP.map(({ severity, meaning }) => (
                        <div key={severity} className="flex items-start gap-3">
                          <SeverityPill severity={severity} className="mt-0.5" />
                          <span className="text-muted-foreground">{meaning}</span>
                        </div>
                      ))}
                    </div>
                  </section>

                  <section className="space-y-3">
                    <h3 className="font-semibold">Case status</h3>
                    <div className="space-y-2">
                      {STATUS_HELP.map(({ status, meaning }) => (
                        <div key={status} className="flex items-start gap-3">
                          <StatusPill status={status} />
                          <span className="text-muted-foreground">{meaning}</span>
                        </div>
                      ))}
                    </div>
                  </section>

                  <section className="space-y-2">
                    <h3 className="font-semibold">Tool Review (first step)</h3>
                    <p className="text-muted-foreground">
                      Before diving into cases, the{" "}
                      <span className="font-medium text-foreground">Tool Review</span>{" "}
                      tab asks you to validate the diagnostic tools available to
                      the agent, grouped by condition — flag gaps and propose any
                      missing tools. Mark it reviewed when done; you can return
                      anytime from the menu.
                    </p>
                  </section>
                </div>
              </motion.div>
            </Dialog.Content>
          </Dialog.Portal>
        )}
      </AnimatePresence>
    </Dialog.Root>
  )
}
