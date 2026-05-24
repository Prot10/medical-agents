import { BrainCircuit, Moon, Sun } from "lucide-react"

import type { ReviewerProfile } from "@/api/types"
import { useDatasets } from "@/hooks/useReview"
import { useReviewStore } from "@/stores/reviewStore"
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

  const datasetInfo = datasets.data?.find((d) => d.version === datasetVersion)

  return (
    <header className="sticky top-0 z-30 bg-background/85 backdrop-blur border-b border-border">
      <div className="px-6 py-3 flex items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-primary/10 text-primary flex items-center justify-center">
            <BrainCircuit className="w-5 h-5" />
          </div>
          <div>
            <div className="text-[11px] uppercase tracking-wider text-muted-foreground leading-tight">
              NeuroBench Review
            </div>
            <div className="text-sm font-semibold leading-tight">
              Expert Review
            </div>
          </div>
        </div>

        <div className="flex-1 flex items-center justify-center">
          <TabBar
            tabs={[
              { id: "overview", label: "Overview" },
              {
                id: "cases",
                label: "Cases",
                count: datasetInfo?.case_count,
              },
              { id: "methodology", label: "Methodology" },
              {
                id: "admin",
                label: "Admin",
                hidden: profile.role !== "admin",
              },
            ]}
            active={activeTab}
            onChange={setActiveTab}
          />
        </div>

        <div className="flex items-center gap-2">
          <select
            value={datasetVersion}
            onChange={(e) => setDatasetVersion(e.target.value)}
            className="h-8 bg-secondary text-foreground text-xs rounded-md border border-border px-2 focus:outline-none focus:ring-2 focus:ring-ring"
          >
            {datasets.data?.map((d) => (
              <option key={d.version} value={d.version}>
                {d.case_count} cases
              </option>
            ))}
          </select>
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
    </header>
  )
}
