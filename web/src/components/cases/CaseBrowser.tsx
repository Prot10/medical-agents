import { useMemo, useState } from "react"
import { Search } from "lucide-react"
import { useCases } from "@/hooks/useCases"
import { useAppStore } from "@/stores/appStore"
import { useAgentStore } from "@/stores/agentStore"
import { cn } from "@/lib/utils"
import type { CaseIndexEntry } from "@/api/types"

const CONDITION_LABELS: Record<string, string> = {
  alzheimers_early: "Alzheimer's (Early)",
  bacterial_meningitis: "Bacterial Meningitis",
  focal_epilepsy_temporal: "Focal Epilepsy",
  functional_neurological: "FND",
  glioblastoma: "Glioblastoma",
  ischemic_stroke: "Ischemic Stroke",
  multiple_sclerosis_rr: "MS (Relapsing)",
  nmdar_encephalitis: "NMDAR Encephalitis",
  parkinsons: "Parkinson's",
  cardiac_syncope: "Cardiac Syncope",
}

const DIFFICULTY_COLORS: Record<string, string> = {
  straightforward: "bg-green-500/20 text-green-600 dark:text-green-400",
  moderate: "bg-yellow-500/20 text-yellow-600 dark:text-yellow-400",
  diagnostic_puzzle: "bg-red-500/20 text-red-600 dark:text-red-400",
}

const DIFFICULTY_SHORT: Record<string, string> = {
  straightforward: "S",
  moderate: "M",
  diagnostic_puzzle: "P",
}

export function CaseBrowser() {
  const { data: cases, isLoading } = useCases()
  const { selectedCaseId, selectCase } = useAppStore()
  const resetAgent = useAgentStore((s) => s.reset)
  const [search, setSearch] = useState("")
  const [filterDifficulty, setFilterDifficulty] = useState<string | null>(null)

  const grouped = useMemo(() => {
    if (!cases) return {}
    const filtered = cases.filter((c) => {
      const matchSearch =
        !search ||
        c.case_id.toLowerCase().includes(search.toLowerCase()) ||
        c.chief_complaint.toLowerCase().includes(search.toLowerCase())
      const matchDifficulty = !filterDifficulty || c.difficulty === filterDifficulty
      return matchSearch && matchDifficulty
    })

    const groups: Record<string, CaseIndexEntry[]> = {}
    for (const c of filtered) {
      const key = c.condition
      if (!groups[key]) groups[key] = []
      groups[key].push(c)
    }
    return groups
  }, [cases, search, filterDifficulty])

  const handleSelect = (caseId: string) => {
    selectCase(caseId)
    resetAgent()
  }

  if (isLoading) {
    return (
      <div className="p-4 text-sm text-muted-foreground">Loading cases...</div>
    )
  }

  return (
    <div className="flex flex-col h-full">
      {/* Search */}
      <div className="p-2 border-b border-border">
        <div className="relative">
          <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search cases..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-7 pr-2 py-1.5 text-xs bg-secondary border border-border rounded-md focus:outline-none focus:ring-1 focus:ring-ring"
          />
        </div>

        {/* Difficulty filter chips */}
        <div className="flex gap-1 mt-1.5">
          {["straightforward", "moderate", "diagnostic_puzzle"].map((d) => (
            <button
              key={d}
              onClick={() => setFilterDifficulty(filterDifficulty === d ? null : d)}
              className={cn(
                "text-[10px] px-1.5 py-0.5 rounded-full border border-border transition-colors",
                filterDifficulty === d
                  ? DIFFICULTY_COLORS[d]
                  : "text-muted-foreground hover:bg-accent",
              )}
            >
              {DIFFICULTY_SHORT[d]}
            </button>
          ))}
          <span className="text-[10px] text-muted-foreground ml-auto leading-5">
            {Object.values(grouped).flat().length} cases
          </span>
        </div>
      </div>

      {/* Case list */}
      <div className="flex-1 overflow-y-auto">
        {Object.entries(grouped).map(([condition, condCases]) => (
          <div key={condition}>
            <div className="sticky top-0 px-2 py-1 text-[10px] font-semibold uppercase tracking-wider text-muted-foreground bg-card/95 backdrop-blur-sm border-b border-border">
              {CONDITION_LABELS[condition] ?? condition}
            </div>
            {condCases.map((c) => (
              <button
                key={c.case_id}
                onClick={() => handleSelect(c.case_id)}
                className={cn(
                  "w-full text-left px-2 py-1.5 border-b border-border/50 transition-colors hover:bg-accent",
                  selectedCaseId === c.case_id && "bg-primary/10 border-l-2 border-l-primary",
                )}
              >
                <div className="flex items-center gap-1.5">
                  <span className="text-xs font-mono font-medium">{c.case_id}</span>
                  <span
                    className={cn(
                      "text-[9px] px-1 rounded-full",
                      DIFFICULTY_COLORS[c.difficulty],
                    )}
                  >
                    {DIFFICULTY_SHORT[c.difficulty]}
                  </span>
                </div>
                <div className="text-[11px] text-muted-foreground mt-0.5 line-clamp-1">
                  {c.age}{c.sex === "male" ? "M" : "F"} — {c.chief_complaint}
                </div>
              </button>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}
