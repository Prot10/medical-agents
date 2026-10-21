import { useMemo } from "react"
import { BarChart3, Users, Activity, Brain } from "lucide-react"
import { useCases } from "@/hooks/useCases"
import { Card, CardTitle } from "@/components/ui/Card"
import { QueryError } from "@/components/ui/QueryError"
import { ConditionChart } from "./charts/ConditionChart"
import { DifficultyDonut } from "./charts/DifficultyDonut"
import { AgeHistogram } from "./charts/AgeHistogram"
import { CaseHeatmap } from "./charts/CaseHeatmap"
import { conditionLabel } from "@/lib/conditions"
import type { CaseIndexEntry } from "@/api/types"

function StatCard({ icon: Icon, label, value, sub }: {
  icon: React.ElementType; label: string; value: string | number; sub?: string
}) {
  return (
    <Card className="flex items-center gap-3">
      <div className="h-10 w-10 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
        <Icon className="h-5 w-5 text-primary" />
      </div>
      <div>
        <div className="text-2xl font-bold tracking-tight">{value}</div>
        <div className="text-sm text-muted-foreground">{label}</div>
      </div>
      {sub && <div className="ml-auto text-sm text-muted-foreground">{sub}</div>}
    </Card>
  )
}

export function DatasetDashboard() {
  const { data: cases, isLoading, isError, error, refetch } = useCases()

  const stats = useMemo(() => {
    if (!cases) return null
    return computeStats(cases)
  }, [cases])

  if (isError) {
    return <QueryError message="Could not load dataset." error={error} onRetry={() => refetch()} centered />
  }

  if (isLoading || !stats) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        <div className="text-center">
          <BarChart3 className="h-12 w-12 mx-auto mb-3 opacity-30" />
          <p className="text-base">Loading dataset...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="h-full overflow-y-auto">
      <div className="p-6 space-y-6 max-w-5xl mx-auto">
        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div>
            <h2 className="text-xl font-bold tracking-tight">
              NeuroBench Dataset
            </h2>
            <p className="text-base text-muted-foreground mt-1">
              {`${stats.total} neurological cases across ${stats.conditionCount} conditions and 3 difficulty levels`}
            </p>
          </div>
        </div>

        {/* Stat cards */}
        <div className="grid grid-cols-4 gap-4">
          <StatCard icon={Brain} label="Total Cases" value={stats.total} />
          <StatCard icon={Users} label="Avg Age" value={stats.avgAge} sub={`${stats.maleCount}M / ${stats.femaleCount}F`} />
          <StatCard icon={Activity} label="Conditions" value={stats.conditionCount} />
          <StatCard icon={BarChart3} label="Most Common" value={stats.topConditionLabel} />
        </div>

        {/* Charts row 1 */}
        <div className="grid grid-cols-2 gap-4">
          <Card>
            <CardTitle className="mb-4">Condition Distribution</CardTitle>
            <ConditionChart data={stats.conditionData} />
          </Card>
          <Card>
            <CardTitle className="mb-4">Difficulty Breakdown</CardTitle>
            <DifficultyDonut data={stats.difficultyData} />
          </Card>
        </div>

        {/* Charts row 2 */}
        <div className="grid grid-cols-2 gap-4">
          <Card>
            <CardTitle className="mb-4">Age Distribution</CardTitle>
            <AgeHistogram data={stats.ageData} />
          </Card>
          <Card>
            <CardTitle className="mb-4">Case Matrix</CardTitle>
            <CaseHeatmap data={stats.heatmapData} />
          </Card>
        </div>
      </div>
    </div>
  )
}


function computeStats(cases: CaseIndexEntry[]) {
  const conditions: Record<string, number> = {}
  const diffCounts = { straightforward: 0, moderate: 0, diagnostic_puzzle: 0 }
  const ageBins: Record<string, number> = {}
  let totalAge = 0
  let maleCount = 0
  let femaleCount = 0

  // Heatmap: condition x difficulty
  const heatmap: Record<string, Record<string, number>> = {}

  for (const c of cases) {
    conditions[c.condition] = (conditions[c.condition] || 0) + 1
    if (c.difficulty in diffCounts) diffCounts[c.difficulty as keyof typeof diffCounts]++
    totalAge += c.age
    if (c.sex === "male") maleCount++
    else femaleCount++

    // Age histogram bins (5-year)
    const binStart = Math.floor(c.age / 10) * 10
    const binLabel = `${binStart}-${binStart + 9}`
    ageBins[binLabel] = (ageBins[binLabel] || 0) + 1

    // Heatmap
    if (!heatmap[c.condition]) heatmap[c.condition] = {}
    heatmap[c.condition][c.difficulty] = (heatmap[c.condition][c.difficulty] || 0) + 1
  }

  const topCondition = Object.entries(conditions).sort(([, a], [, b]) => b - a)[0]

  return {
    total: cases.length,
    avgAge: Math.round(totalAge / cases.length),
    maleCount,
    femaleCount,
    conditionCount: Object.keys(conditions).length,
    topConditionLabel: conditionLabel(topCondition[0]),
    conditionData: Object.entries(conditions)
      .map(([name, count]) => ({ name: conditionLabel(name), count, key: name }))
      .sort((a, b) => b.count - a.count),
    difficultyData: [
      { name: "Straightforward", value: diffCounts.straightforward, key: "straightforward" },
      { name: "Moderate", value: diffCounts.moderate, key: "moderate" },
      { name: "Diagnostic Puzzle", value: diffCounts.diagnostic_puzzle, key: "diagnostic_puzzle" },
    ],
    ageData: Object.entries(ageBins)
      .map(([range, count]) => ({ range, count }))
      .sort((a, b) => parseInt(a.range) - parseInt(b.range)),
    heatmapData: Object.entries(heatmap).map(([condition, diffs]) => ({
      condition: conditionLabel(condition),
      straightforward: diffs.straightforward || 0,
      moderate: diffs.moderate || 0,
      diagnostic_puzzle: diffs.diagnostic_puzzle || 0,
    })),
  }
}
