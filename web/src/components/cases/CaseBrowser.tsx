import { useMemo, useState } from "react"
import { Search, Brain, Heart, Zap, Activity, FlaskConical, Pill, AlertCircle, Microscope, Stethoscope, HeartPulse, Gauge, Wind, Hand, Droplets } from "lucide-react"
import { DifficultyStars } from "@/components/ui/DifficultyStars"
import { QueryError } from "@/components/ui/QueryError"
import { useCases } from "@/hooks/useCases"
import { useAppStore } from "@/stores/appStore"
import { useAgentStore } from "@/stores/agentStore"
import { cn } from "@/lib/utils"
import { conditionLabel } from "@/lib/conditions"
import type { CaseIndexEntry } from "@/api/types"


const CONDITION_ICONS: Record<string, React.ElementType> = {
  als: Hand,
  alzheimers_early: Brain,
  autoimmune_encephalitis_nmdar: FlaskConical,
  bacterial_meningitis: AlertCircle,
  brain_tumor_glioma: Microscope,
  focal_epilepsy_temporal: Zap,
  ftd: Brain,
  functional_neurological_disorder: Activity,
  guillain_barre: Hand,
  hepatic_encephalopathy: Droplets,
  ischemic_stroke: Heart,
  migraine_with_aura: Zap,
  multiple_sclerosis: Stethoscope,
  myasthenia_gravis: Activity,
  nph: Gauge,
  parkinsons: Pill,
  status_epilepticus: Zap,
  subarachnoid_hemorrhage: AlertCircle,
  syncope_cardiac: HeartPulse,
  vascular_dementia: Wind,
}


export function CaseBrowser() {
  const { data: cases, isLoading, isError, error, refetch } = useCases()
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

  if (isError) {
    return <QueryError message="Could not load cases." error={error} onRetry={() => refetch()} />
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
                {conditionLabel(condition)}
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
