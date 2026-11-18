import { useIsMutating } from "@tanstack/react-query"
import { motion } from "framer-motion"
import {
  ArrowRight,
  BrainCircuit,
  CheckCircle2,
  ClipboardCheck,
  HelpCircle,
  LayoutGrid,
  Loader2,
  Moon,
  Sun,
} from "lucide-react"
import { useState } from "react"

import type { CaseIndexEntry, ReviewSet, ReviewerProfile } from "@/api/types"
import { useCases } from "@/hooks/useReview"
import { useSetProgress, type SetProgress } from "@/hooks/useSetProgress"
import { conditionColor, conditionLabel } from "@/lib/conditions"
import { cn } from "@/lib/utils"
import { useReviewStore } from "@/stores/reviewStore"
import { CaseDetail } from "@/components/cases/CaseDetail"
import { GuidelinesDialog } from "@/components/layout/GuidelinesDialog"
import { SaveIndicator } from "@/components/layout/Header"
import { ReviewerChip } from "@/components/layout/ReviewerChip"
import { CaseProgressStrip } from "@/components/review/CaseProgressStrip"
import { Button } from "@/components/ui/Button"
import { StatusPill } from "@/components/ui/StatusPill"

/**
 * The re-check of a review set: the same case view as the full review, one case at a time,
 * with a progress bar over the whole set on top.
 */
export function RecheckWorkspace({
  profile,
  reviewSet,
}: {
  profile: ReviewerProfile
  reviewSet: ReviewSet
}) {
  const selectedCaseId = useReviewStore((s) => s.selectedCaseId)
  const setSelectedCaseId = useReviewStore((s) => s.setSelectedCaseId)
  const cases = useCases(reviewSet.id)
  const progress = useSetProgress(reviewSet.id, reviewSet.case_ids)

  const caseById = new Map<string, CaseIndexEntry>()
  for (const c of cases.data ?? []) caseById.set(c.case_id, c)

  const open = (caseId: string | null) => {
    setSelectedCaseId(caseId)
    window.scrollTo({ top: 0 })
  }

  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground">
      <div className="sticky top-0 z-30 bg-background/90 backdrop-blur border-b border-border">
        <RecheckHeader profile={profile} title={reviewSet.name} />
        <CaseProgressStrip
          caseIds={reviewSet.case_ids}
          statusOf={progress.statusOf}
          currentCaseId={selectedCaseId}
          onOpen={open}
          describe={(id) => {
            const entry = caseById.get(id)
            return `${entry ? conditionLabel(entry.condition) : id} (${id})`
          }}
          heading={(index) => {
            const entry = index >= 0 ? caseById.get(reviewSet.case_ids[index]) : undefined
            return entry ? (
              <div className="text-sm leading-tight truncate">
                <span className="font-semibold tabular-nums">
                  Case {index + 1} of {reviewSet.case_count}
                </span>
                <span className="text-muted-foreground"> · {conditionLabel(entry.condition)}</span>
              </div>
            ) : (
              <div className="text-sm font-semibold leading-tight">
                {progress.total > 0 && progress.done === progress.total
                  ? "All cases reviewed"
                  : "Your progress"}
              </div>
            )
          }}
        />
      </div>

      <main className="flex-1 min-h-0 px-4 sm:px-6 py-4 sm:py-6 max-w-7xl mx-auto w-full">
        {cases.isLoading ? (
          <div className="flex items-center justify-center py-32 text-muted-foreground">
            <Loader2 className="w-5 h-5 animate-spin" />
          </div>
        ) : selectedCaseId ? (
          <CaseDetail
            key={selectedCaseId}
            caseId={selectedCaseId}
            backLabel="All re-check cases"
          />
        ) : (
          <RecheckIntro
            reviewSet={reviewSet}
            caseById={caseById}
            progress={progress}
            onOpen={open}
          />
        )}
      </main>
    </div>
  )
}

// ---------------------------------------------------------------------------
// Header

function RecheckHeader({ profile, title }: { profile: ReviewerProfile; title: string }) {
  const darkMode = useReviewStore((s) => s.darkMode)
  const setDarkMode = useReviewStore((s) => s.setDarkMode)
  const chooseWorkspace = useReviewStore((s) => s.chooseWorkspace)
  const isMutating = useIsMutating() > 0
  const [guidelinesOpen, setGuidelinesOpen] = useState(false)

  return (
    <div className="px-4 sm:px-6 py-2.5 sm:py-3 flex items-center justify-between gap-2 sm:gap-4">
      <div className="flex items-center gap-2 sm:gap-3 min-w-0">
        <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-lg bg-primary/10 text-primary flex items-center justify-center flex-shrink-0">
          <BrainCircuit className="w-4 h-4 sm:w-5 sm:h-5" />
        </div>
        <div className="min-w-0">
          <div className="text-[10px] sm:text-[11px] uppercase tracking-wider text-muted-foreground leading-tight">
            NeuroBench Review
          </div>
          <div className="text-sm font-semibold leading-tight truncate">{title}</div>
        </div>
      </div>

      <div className="flex items-center gap-1 sm:gap-2 flex-shrink-0">
        <SaveIndicator saving={isMutating} />
        <Button
          variant="ghost"
          size="sm"
          onClick={() => chooseWorkspace({ kind: "full" })}
          title="Leave the re-check and open the full review"
          className="text-muted-foreground hover:text-foreground"
        >
          <LayoutGrid className="w-4 h-4" />
          <span className="hidden md:inline">Full review</span>
        </Button>
        <button
          type="button"
          onClick={() => setGuidelinesOpen(true)}
          aria-label="How to review"
          className="w-8 h-8 rounded-md flex items-center justify-center hover:bg-secondary/70 transition-colors text-muted-foreground"
        >
          <HelpCircle className="w-4 h-4" />
        </button>
        <button
          type="button"
          onClick={() => setDarkMode(!darkMode)}
          aria-label={darkMode ? "Switch to light theme" : "Switch to dark theme"}
          className="w-8 h-8 rounded-md flex items-center justify-center hover:bg-secondary/70 transition-colors text-muted-foreground"
        >
          {darkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
        </button>
        <ReviewerChip profile={profile} />
      </div>
      <GuidelinesDialog open={guidelinesOpen} onOpenChange={setGuidelinesOpen} />
    </div>
  )
}

// ---------------------------------------------------------------------------
// Landing: what to do, and the list of cases

function RecheckIntro({
  reviewSet,
  caseById,
  progress,
  onOpen,
}: {
  reviewSet: ReviewSet
  caseById: Map<string, CaseIndexEntry>
  progress: SetProgress
  onOpen: (caseId: string | null) => void
}) {
  const chooseWorkspace = useReviewStore((s) => s.chooseWorkspace)
  const finished = progress.total > 0 && progress.done === progress.total
  const started = progress.done > 0 || progress.started > 0

  return (
    <div className="space-y-6">
      <motion.section
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className={cn(
          "bg-card border rounded-2xl p-6 sm:p-8",
          finished ? "border-emerald-500/40" : "border-border",
        )}
      >
        {finished ? (
          <div className="flex flex-col sm:flex-row sm:items-center gap-5">
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center flex-shrink-0">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <div className="flex-1">
              <h1 className="text-xl font-semibold tracking-tight">
                All {progress.total} cases re-checked. Thank you!
              </h1>
              <p className="text-sm text-muted-foreground mt-1">
                Your answers are saved. You can still open any case below to change them.
              </p>
            </div>
            <Button variant="secondary" onClick={() => chooseWorkspace({ kind: "full" })}>
              <LayoutGrid className="w-4 h-4" />
              Go to the full review
            </Button>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-6 lg:gap-10 items-center">
            <div>
              <div className="inline-flex items-center gap-2 text-xs font-medium text-primary bg-primary/10 border border-primary/20 rounded-full px-2.5 py-1 mb-4">
                <ClipboardCheck className="w-3.5 h-3.5" />
                {reviewSet.case_count} cases · one per condition
              </div>
              <h1 className="text-xl sm:text-2xl font-semibold tracking-tight">
                Are these cases right now?
              </h1>
              <p className="text-sm text-muted-foreground mt-2 max-w-2xl leading-relaxed">
                {reviewSet.description}
              </p>
              <ol className="mt-5 grid grid-cols-1 sm:grid-cols-3 gap-3">
                {[
                  ["Read the case", "Same view as before: patient, tests, pathway and policy."],
                  ["Mark what is still wrong", "Click any field to leave a note, as you did before."],
                  ["Give your verdict", "Approve if it is correct now, or ask for changes."],
                ].map(([title, text], i) => (
                  <li key={title} className="flex gap-3 rounded-xl bg-secondary/50 border border-border p-3">
                    <span className="w-6 h-6 rounded-full bg-primary text-primary-foreground text-xs font-semibold flex items-center justify-center flex-shrink-0">
                      {i + 1}
                    </span>
                    <span>
                      <span className="block text-sm font-medium leading-tight">{title}</span>
                      <span className="block text-xs text-muted-foreground mt-1 leading-snug">{text}</span>
                    </span>
                  </li>
                ))}
              </ol>
            </div>
            <div className="flex flex-col items-stretch gap-2 lg:w-64">
              <Button size="lg" onClick={() => onOpen(progress.nextCaseId)}>
                {started ? `Continue with case ${progress.nextNumber}` : "Start with case 1"}
                <ArrowRight className="w-4 h-4" />
              </Button>
              <p className="text-xs text-muted-foreground text-center">
                Your work is saved as you go. You can stop and come back at any time.
              </p>
            </div>
          </div>
        )}
      </motion.section>

      <section>
        <h2 className="text-xs uppercase tracking-wider text-muted-foreground font-semibold mb-3">
          The {reviewSet.case_count} cases
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
          {reviewSet.case_ids.map((id, i) => {
            const entry = caseById.get(id)
            const status = progress.statusOf(id)
            const isNext = id === progress.nextCaseId
            return (
              <button
                key={id}
                type="button"
                onClick={() => onOpen(id)}
                className={cn(
                  "text-left bg-card border rounded-xl p-3.5 transition-all hover:-translate-y-0.5 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
                  isNext ? "border-primary/50 ring-1 ring-primary/20" : "border-border",
                )}
              >
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="text-[11px] font-semibold text-muted-foreground tabular-nums">
                    {i + 1} / {reviewSet.case_count}
                  </span>
                  <StatusPill status={status} className="text-[10px] px-2 py-0.5" />
                </div>
                <div className="flex items-center gap-2">
                  <span
                    className="w-2 h-2 rounded-full flex-shrink-0"
                    style={{ background: entry ? conditionColor(entry.condition) : undefined }}
                  />
                  <span className="text-sm font-medium leading-tight truncate">
                    {entry ? conditionLabel(entry.condition) : id}
                  </span>
                </div>
                <div className="font-mono text-[11px] text-muted-foreground mt-1">{id}</div>
              </button>
            )
          })}
        </div>
      </section>
    </div>
  )
}
