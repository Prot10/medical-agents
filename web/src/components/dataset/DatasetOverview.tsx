import { useMemo } from "react"
import { useCases } from "@/hooks/useCases"
import { useAppStore } from "@/stores/appStore"
import { DifficultyStars } from "@/components/ui/DifficultyStars"
import { cn } from "@/lib/utils"

const CONDITION_LABELS: Record<string, string> = {
  alzheimers_early: "Alzheimer's",
  bacterial_meningitis: "Meningitis",
  focal_epilepsy_temporal: "Epilepsy",
  functional_neurological: "FND",
  glioblastoma: "Glioblastoma",
  ischemic_stroke: "Stroke",
  multiple_sclerosis_rr: "MS",
  nmdar_encephalitis: "NMDAR Enc.",
  parkinsons: "Parkinson's",
  cardiac_syncope: "Syncope",
}

const CONDITION_COLORS: Record<string, string> = {
  alzheimers_early: "bg-purple-500",
  bacterial_meningitis: "bg-red-500",
  focal_epilepsy_temporal: "bg-blue-500",
  functional_neurological: "bg-gray-500",
  glioblastoma: "bg-rose-500",
  ischemic_stroke: "bg-orange-500",
  multiple_sclerosis_rr: "bg-cyan-500",
  nmdar_encephalitis: "bg-emerald-500",
  parkinsons: "bg-amber-500",
  cardiac_syncope: "bg-indigo-500",
}

export function DatasetOverview() {
  const { data: cases } = useCases()
  const { datasetFilters, setDatasetFilters } = useAppStore()

  const stats = useMemo(() => {
    if (!cases) return null

    const conditions: Record<string, number> = {}
    const difficulties = { straightforward: 0, moderate: 0, diagnostic_puzzle: 0 }
    let totalAge = 0

    for (const c of cases) {
      conditions[c.condition] = (conditions[c.condition] || 0) + 1
      if (c.difficulty in difficulties) {
        difficulties[c.difficulty as keyof typeof difficulties]++
      }
      totalAge += c.age
    }

    const maxCondCount = Math.max(...Object.values(conditions))

    return {
      total: cases.length,
      conditions,
      difficulties,
      avgAge: Math.round(totalAge / cases.length),
      maxCondCount,
    }
  }, [cases])

  if (!stats) return <div className="p-4 text-base text-muted-foreground">Loading...</div>

  const toggleDifficulty = (d: string) => {
    const current = datasetFilters.difficulties
    setDatasetFilters({
      difficulties: current.includes(d) ? current.filter((x) => x !== d) : [...current, d],
    })
  }

  const toggleCondition = (c: string) => {
    const current = datasetFilters.conditions
    setDatasetFilters({
      conditions: current.includes(c) ? current.filter((x) => x !== c) : [...current, c],
    })
  }

  return (
    <div className="p-3 space-y-4">
      {/* Summary */}
      <div className="flex items-baseline gap-2">
        <span className="text-2xl font-bold text-foreground">{stats.total}</span>
        <span className="text-base text-muted-foreground">cases</span>
        <span className="text-sm text-muted-foreground ml-auto">avg age {stats.avgAge}</span>
      </div>

      {/* Difficulty breakdown */}
      <div>
        <div className="text-xs uppercase tracking-wider font-semibold text-muted-foreground mb-1.5">Difficulty</div>
        <div className="flex gap-1.5">
          {[
            { key: "straightforward", count: stats.difficulties.straightforward },
            { key: "moderate", count: stats.difficulties.moderate },
            { key: "diagnostic_puzzle", count: stats.difficulties.diagnostic_puzzle },
          ].map((d) => (
            <button
              key={d.key}
              onClick={() => toggleDifficulty(d.key)}
              className={cn(
                "flex-1 flex flex-col items-center gap-1 py-1.5 rounded-lg border transition-all",
                datasetFilters.difficulties.includes(d.key)
                  ? "border-primary bg-primary/10"
                  : "border-border hover:border-primary/30",
              )}
            >
              <span className="text-base font-bold">{d.count}</span>
              <DifficultyStars difficulty={d.key} />
            </button>
          ))}
        </div>
      </div>

      {/* Condition distribution */}
      <div>
        <div className="text-xs uppercase tracking-wider font-semibold text-muted-foreground mb-1.5">Conditions</div>
        <div className="space-y-1">
          {Object.entries(stats.conditions)
            .sort(([, a], [, b]) => b - a)
            .map(([condition, count]) => {
              const isActive = datasetFilters.conditions.includes(condition)
              return (
                <button
                  key={condition}
                  onClick={() => toggleCondition(condition)}
                  className={cn(
                    "w-full flex items-center gap-2 py-1 px-1 rounded-md transition-all text-left",
                    isActive ? "bg-primary/10" : "hover:bg-sidebar-accent",
                  )}
                >
                  <div className={cn("h-2 w-2 rounded-full shrink-0", CONDITION_COLORS[condition] ?? "bg-gray-500")} />
                  <span className="text-sm truncate flex-1">{CONDITION_LABELS[condition] ?? condition}</span>
                  <div className="flex items-center gap-1.5">
                    <div className="w-16 h-1.5 rounded-full bg-border overflow-hidden">
                      <div
                        className={cn("h-full rounded-full transition-all", CONDITION_COLORS[condition] ?? "bg-gray-500")}
                        style={{ width: `${(count / stats.maxCondCount) * 100}%` }}
                      />
                    </div>
                    <span className="text-xs text-muted-foreground w-4 text-right font-mono">{count}</span>
                  </div>
                </button>
              )
            })}
        </div>
      </div>
    </div>
  )
}
