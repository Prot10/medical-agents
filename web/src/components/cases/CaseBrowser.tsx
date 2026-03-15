import { useMemo, useState } from "react"
import { Search, Brain, Heart, Zap, Activity, FlaskConical, Pill, AlertCircle, Microscope, Stethoscope, HeartPulse } from "lucide-react"
import { DifficultyStars } from "@/components/ui/DifficultyStars"
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

const CONDITION_ICONS: Record<string, React.ElementType> = {
  alzheimers_early: Brain,
  bacterial_meningitis: AlertCircle,
  focal_epilepsy_temporal: Zap,
  functional_neurological: Activity,
  glioblastoma: Microscope,
  ischemic_stroke: Heart,
  multiple_sclerosis_rr: Stethoscope,
  nmdar_encephalitis: FlaskConical,
  parkinsons: Pill,
  cardiac_syncope: HeartPulse,
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
      <div className="p-4 text-base text-muted-foreground">Loading cases...</div>
    )
  }

  return (
    <div className="flex flex-col h-full">
      {/* Search */}
      <div className="p-3 border-b border-sidebar-border">
        <div className="relative">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search cases..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-8 pr-3 py-2 text-base bg-sidebar-accent border border-sidebar-border rounded-lg focus:outline-none focus:ring-1 focus:ring-ring placeholder:text-muted-foreground/50"
          />
        </div>

        {/* Difficulty filter chips */}
        <div className="flex gap-1.5 mt-2">
          {["straightforward", "moderate", "diagnostic_puzzle"].map((d) => (
            <button
              key={d}
              onClick={() => setFilterDifficulty(filterDifficulty === d ? null : d)}
              className={cn(
                "px-2 py-1 rounded-lg border transition-all",
                filterDifficulty === d
                  ? "border-primary/30 bg-primary/5"
                  : "border-sidebar-border hover:bg-sidebar-accent",
              )}
            >
              <DifficultyStars difficulty={d} />
            </button>
          ))}
          <span className="text-sm text-muted-foreground ml-auto leading-7 tabular-nums">
            {Object.values(grouped).flat().length}
          </span>
        </div>
      </div>

      {/* Case list */}
      <div className="flex-1 overflow-y-auto">
        {Object.entries(grouped).map(([condition, condCases]) => {
          const CondIcon = CONDITION_ICONS[condition] ?? Brain
          return (
            <div key={condition}>
              <div className="sticky top-0 flex items-center gap-2 px-3 py-1.5 text-sm font-semibold uppercase tracking-wider text-muted-foreground bg-sidebar/95 backdrop-blur-sm border-b border-sidebar-border">
                <CondIcon className="h-3.5 w-3.5" />
                {CONDITION_LABELS[condition] ?? condition}
              </div>
              {condCases.map((c) => (
                <button
                  key={c.case_id}
                  onClick={() => handleSelect(c.case_id)}
                  className={cn(
                    "w-full text-left px-3 py-2.5 border-b border-sidebar-border/50 transition-all hover:bg-sidebar-accent",
                    selectedCaseId === c.case_id && "bg-primary/10 border-l-[3px] border-l-primary",
                  )}
                >
                  <div className="flex items-center gap-2">
                    <span className="text-base font-mono font-medium">{c.case_id}</span>
                    <DifficultyStars difficulty={c.difficulty} />
                  </div>
                  <div className="text-base text-muted-foreground mt-1 line-clamp-1">
                    {c.age}{c.sex === "male" ? "M" : "F"} — {c.chief_complaint}
                  </div>
                </button>
              ))}
            </div>
          )
        })}
      </div>
    </div>
  )
}
