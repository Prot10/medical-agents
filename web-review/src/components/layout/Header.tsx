import { useIsMutating } from "@tanstack/react-query"
import { BrainCircuit, Check, HelpCircle, Loader2, Moon, Sun } from "lucide-react"
import { useState } from "react"

import type { ReviewerProfile } from "@/api/types"
import { useDatasets, useMyProgress } from "@/hooks/useReview"
import { useToolReview } from "@/hooks/useToolReview"
import { useReviewStore } from "@/stores/reviewStore"
import { GuidelinesDialog } from "./GuidelinesDialog"
import { ReviewerChip } from "./ReviewerChip"
import { TabBar } from "./TabBar"

export function Header({ profile }: { profile: ReviewerProfile }) {
  const activeTab = useReviewStore((s) => s.activeTab)
  const setActiveTab = useReviewStore((s) => s.setActiveTab)
  const darkMode = useReviewStore((s) => s.darkMode)
  const setDarkMode = useReviewStore((s) => s.setDarkMode)
  const datasetVersion = useReviewStore((s) => s.datasetVersion)
  const setDatasetVersion = useReviewStore((s) => s.setDatasetVersion)
  const datasets = useDatasets()
  const toolReview = useToolReview(datasetVersion)
  const progress = useMyProgress(datasetVersion)
  const isMutating = useIsMutating() > 0
  const [guidelinesOpen, setGuidelinesOpen] = useState(false)

  const datasetInfo = datasets.data?.find((d) => d.version === datasetVersion)
  const toolReviewPending =
    !!toolReview.data && toolReview.data.completed_at == null

  const tabItems = [
    { id: "overview" as const, label: "Overview" },
    {
      id: "cases" as const,
      label: "Cases",
      count: datasetInfo?.case_count,
    },
    { id: "tools" as const, label: "Tool Review", dot: toolReviewPending },
    { id: "methodology" as const, label: "Methodology" },
    {
      id: "admin" as const,
      label: "Admin",
      hidden: profile.role !== "admin",
    },
  ]

  return (
    <header className="sticky top-0 z-30 bg-background/85 backdrop-blur border-b border-border">
      <div className="px-4 sm:px-6 py-2.5 sm:py-3 flex items-center justify-between gap-2 sm:gap-4">
        <div className="flex items-center gap-2 sm:gap-3 min-w-0">
          <div className="w-8 h-8 sm:w-9 sm:h-9 rounded-lg bg-primary/10 text-primary flex items-center justify-center flex-shrink-0">
            <BrainCircuit className="w-4 h-4 sm:w-5 sm:h-5" />
          </div>
          <div className="min-w-0">
            <div className="text-[10px] sm:text-[11px] uppercase tracking-wider text-muted-foreground leading-tight">
              NeuroBench Review
            </div>
            <div className="text-sm font-semibold leading-tight truncate">
              Expert Review
            </div>
          </div>
        </div>

        {/* Desktop tab bar (centered between logo and controls) */}
        <div className="flex-1 hidden sm:flex items-center justify-center">
          <TabBar
            tabs={tabItems}
            active={activeTab}
            onChange={setActiveTab}
            layoutId="tab-underline-desktop"
          />
        </div>

        <div className="flex items-center gap-1 sm:gap-2 flex-shrink-0">
          <SaveIndicator saving={isMutating} />
          {progress.data && (
            <span
              className="hidden md:inline-flex items-center gap-1.5 text-[11px] text-muted-foreground tabular-nums"
              title="Cases you've touched"
            >
              {progress.data.touched_cases}/{progress.data.total_cases}
              <span className="w-16 h-1.5 rounded-full bg-muted overflow-hidden">
                <span
                  className="block h-full bg-primary"
                  style={{
                    width: `${Math.round(
                      (progress.data.touched_cases /
                        Math.max(1, progress.data.total_cases)) *
                        100,
                    )}%`,
                  }}
                />
              </span>
            </span>
          )}
          <select
            value={datasetVersion}
            onChange={(e) => setDatasetVersion(e.target.value)}
            aria-label="Select dataset"
            className="hidden sm:block h-8 bg-secondary text-foreground text-xs rounded-md border border-border px-2 focus:outline-none focus:ring-2 focus:ring-ring"
          >
            {datasets.data?.map((d) => (
              <option key={d.version} value={d.version}>
                {d.case_count} cases
              </option>
            ))}
          </select>
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
      </div>

      <GuidelinesDialog open={guidelinesOpen} onOpenChange={setGuidelinesOpen} />

      {/* Mobile tab bar — second row, horizontally scrollable */}
      <div className="sm:hidden border-t border-border overflow-x-auto scrollbar-hide">
        <div className="px-2 py-1 w-max min-w-full flex justify-center">
          <TabBar
            tabs={tabItems}
            active={activeTab}
            onChange={setActiveTab}
            layoutId="tab-underline-mobile"
          />
        </div>
      </div>
    </header>
  )
}

function SaveIndicator({ saving }: { saving: boolean }) {
  return (
    <span
      className="hidden sm:inline-flex items-center gap-1 text-[11px] text-muted-foreground min-w-[4.5rem] justify-end"
      aria-live="polite"
    >
      {saving ? (
        <>
          <Loader2 className="w-3 h-3 animate-spin" />
          Saving…
        </>
      ) : (
        <>
          <Check className="w-3 h-3 text-emerald-500" />
          Saved
        </>
      )}
    </span>
  )
}
