import { motion } from "framer-motion"
import {
  ArrowRight,
  BrainCircuit,
  CheckCircle2,
  ClipboardCheck,
  LayoutGrid,
  Loader2,
} from "lucide-react"
import { useEffect } from "react"

import type { ReviewSet, ReviewerProfile } from "@/api/types"
import { useMyProgress, useReviewSets } from "@/hooks/useReview"
import { useSetProgress } from "@/hooks/useSetProgress"
import { cn } from "@/lib/utils"
import { useReviewStore } from "@/stores/reviewStore"
import { GateBackground } from "./CodeEntryGate"

/** The screen right after the reviewer code: re-check a review set, or open the full review. */
export function WorkspaceChooser({ profile }: { profile: ReviewerProfile }) {
  const chooseWorkspace = useReviewStore((s) => s.chooseWorkspace)
  const signOut = useReviewStore((s) => s.signOut)
  const sets = useReviewSets()
  // A guided code opens its assigned sets only: no full review to fall back on.
  const guided = (profile.review_sets ?? []).length > 0

  // No review set on the server: there is nothing to choose.
  useEffect(() => {
    if (!guided && sets.data && sets.data.length === 0) chooseWorkspace({ kind: "full" })
  }, [guided, sets.data, chooseWorkspace])

  const firstName = profile.name.split(" ")[0] || profile.name

  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden bg-background px-4 sm:px-6 py-10">
      <GateBackground />

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: "easeOut" }}
        className="relative z-10 w-full max-w-3xl"
      >
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
            <BrainCircuit className="w-5 h-5" />
          </div>
          <div>
            <div className="text-xs uppercase tracking-wider text-muted-foreground">
              NeuroBench
            </div>
            <div className="text-sm font-semibold tracking-tight">Expert Review</div>
          </div>
        </div>

        <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight">
          Welcome back, {firstName}.
        </h1>
        <p className="text-muted-foreground mt-2 mb-8 text-sm sm:text-base">
          Where would you like to work today? You can switch at any time from your
          name at the top right.
        </p>

        {sets.isLoading ? (
          <div className="flex items-center justify-center py-20 text-muted-foreground">
            <Loader2 className="w-5 h-5 animate-spin" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {(sets.data ?? []).map((set, i) => (
              <SetCard
                key={set.id}
                set={set}
                featured={i === 0}
                onOpen={() => chooseWorkspace({ kind: "set", setId: set.id })}
              />
            ))}
            {!guided && <FullReviewCard onOpen={() => chooseWorkspace({ kind: "full" })} />}
          </div>
        )}

        <p className="text-center text-xs text-muted-foreground mt-8">
          Signed in as {profile.name}.{" "}
          <button
            type="button"
            onClick={signOut}
            className="underline underline-offset-2 hover:text-foreground"
          >
            Not you?
          </button>
        </p>
      </motion.div>
    </div>
  )
}

function SetCard({
  set,
  featured,
  onOpen,
}: {
  set: ReviewSet
  featured: boolean
  onOpen: () => void
}) {
  const progress = useSetProgress(set.id, set.case_ids)
  const finished = progress.total > 0 && progress.done === progress.total
  const second = set.kind === "second_review"
  const cta = finished
    ? "See your answers"
    : progress.done > 0 || progress.started > 0
      ? `Continue · case ${progress.nextNumber} of ${progress.total}`
      : second
        ? "Start the review"
        : "Start the re-check"

  return (
    <ChoiceCard
      onOpen={onOpen}
      featured={featured}
      icon={finished ? <CheckCircle2 className="w-5 h-5" /> : <ClipboardCheck className="w-5 h-5" />}
      badge={finished ? "Done" : "New · start here"}
      title={set.name}
      meta={second ? `${set.case_count} cases` : `${set.case_count} cases · one per condition`}
      body={
        second
          ? set.description
          : "We corrected these cases after your notes. Review each one as before and tell us whether it is now right."
      }
      progressLabel={`${progress.done} of ${progress.total} reviewed`}
      progressValue={progress.total ? progress.done / progress.total : 0}
      cta={cta}
      primary
    />
  )
}

function FullReviewCard({ onOpen }: { onOpen: () => void }) {
  const progress = useMyProgress("neurobench")
  const total = progress.data?.total_cases ?? 0
  const touched = progress.data?.touched_cases ?? 0
  return (
    <ChoiceCard
      onOpen={onOpen}
      icon={<LayoutGrid className="w-5 h-5" />}
      title="Full review"
      meta={total ? `${total} cases · all conditions` : "All cases"}
      body="The complete dataset, as before: overview, every case, tool review and methodology."
      progressLabel={total ? `${touched} of ${total} opened` : ""}
      progressValue={total ? touched / total : 0}
      cta="Open the full review"
    />
  )
}

function ChoiceCard({
  onOpen,
  icon,
  badge,
  title,
  meta,
  body,
  progressLabel,
  progressValue,
  cta,
  featured = false,
  primary = false,
}: {
  onOpen: () => void
  icon: React.ReactNode
  badge?: string
  title: string
  meta: string
  body: string
  progressLabel: string
  progressValue: number
  cta: string
  featured?: boolean
  primary?: boolean
}) {
  return (
    <button
      type="button"
      onClick={onOpen}
      className={cn(
        "group relative text-left bg-card border rounded-2xl p-6 flex flex-col transition-all duration-200",
        "hover:-translate-y-0.5 hover:shadow-xl focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background",
        featured
          ? "border-primary/40 shadow-lg shadow-primary/10 ring-1 ring-primary/20"
          : "border-border shadow-sm",
      )}
    >
      <div className="flex items-start justify-between gap-3 mb-5">
        <div
          className={cn(
            "w-11 h-11 rounded-xl flex items-center justify-center",
            primary ? "bg-primary/10 text-primary" : "bg-secondary text-muted-foreground",
          )}
        >
          {icon}
        </div>
        {badge && (
          <span className="text-[11px] font-medium px-2.5 py-1 rounded-full bg-primary/10 text-primary border border-primary/20">
            {badge}
          </span>
        )}
      </div>

      <h2 className="text-lg font-semibold tracking-tight">{title}</h2>
      <div className="text-xs text-muted-foreground mt-1 tabular-nums">{meta}</div>
      <p className="text-sm text-muted-foreground leading-relaxed mt-3 flex-1">{body}</p>

      <div className="mt-6 h-5">
        {progressLabel && (
          <>
            <div className="flex items-center justify-between text-[11px] text-muted-foreground mb-1.5 tabular-nums">
              <span>{progressLabel}</span>
              <span>{Math.round(progressValue * 100)}%</span>
            </div>
            <div className="h-1.5 rounded-full bg-muted overflow-hidden">
              <div
                className={cn("h-full rounded-full", primary ? "bg-primary" : "bg-muted-foreground/40")}
                style={{ width: `${Math.round(progressValue * 100)}%` }}
              />
            </div>
          </>
        )}
      </div>

      <span
        className={cn(
          "mt-6 inline-flex items-center justify-center gap-2 h-11 rounded-md text-sm font-medium transition-all",
          primary
            ? "bg-primary text-primary-foreground shadow-sm group-hover:brightness-110"
            : "bg-secondary text-secondary-foreground border border-border group-hover:bg-secondary/70",
        )}
      >
        {cta}
        <ArrowRight className="w-4 h-4 transition-transform group-hover:translate-x-0.5" />
      </span>
    </button>
  )
}
