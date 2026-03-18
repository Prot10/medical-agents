import { useMemo, useState } from "react"
import { History, Clock, Zap, Wrench, Play, SkipForward, Search, Trash2 } from "lucide-react"
import { useQueryClient } from "@tanstack/react-query"
import { DifficultyStars } from "@/components/ui/DifficultyStars"
import { useTraces, useReplay } from "@/hooks/useReplay"
import { useAppStore } from "@/stores/appStore"
import { api } from "@/api/client"
import { cn } from "@/lib/utils"

const HOSPITAL_LABELS: Record<string, string> = {
  us_mayo: "Mayo",
  uk_nhs: "NHS",
  de_charite: "Charité",
  jp_todai: "Todai",
  br_hcfmusp: "HCFMUSP",
}

export function TraceBrowser() {
  const { data: traces, isLoading } = useTraces()
  const { replay, replayInstant } = useReplay()
  const { selectCase, setOracleOpen } = useAppStore()
  const queryClient = useQueryClient()

  const [search, setSearch] = useState("")
  const [filterDifficulty, setFilterDifficulty] = useState<string | null>(null)
  const [filterModel, setFilterModel] = useState<string | null>(null)
  const [filterHospital, setFilterHospital] = useState<string | null>(null)

  // Derive unique models and hospitals from traces for filter chips
  const { uniqueModels, uniqueHospitals } = useMemo(() => {
    if (!traces) return { uniqueModels: [], uniqueHospitals: [] }
    const models = [...new Set(traces.map((t) => t.model_short).filter(Boolean))]
    const hospitals = [...new Set(traces.map((t) => t.hospital).filter(Boolean))]
    return { uniqueModels: models, uniqueHospitals: hospitals }
  }, [traces])

  const filtered = useMemo(() => {
    if (!traces) return []
    return traces.filter((t) => {
      const matchSearch =
        !search || t.case_id.toLowerCase().includes(search.toLowerCase())
      const matchDifficulty = !filterDifficulty || t.difficulty === filterDifficulty
      const matchModel = !filterModel || t.model_short === filterModel
      const matchHospital = !filterHospital || t.hospital === filterHospital
      return matchSearch && matchDifficulty && matchModel && matchHospital
    })
  }, [traces, search, filterDifficulty, filterModel, filterHospital])

  const handleReplay = (traceId: string, caseId: string) => {
    selectCase(caseId)
    setOracleOpen(false)
    replay(traceId)
  }

  const handleInstant = (traceId: string, caseId: string) => {
    selectCase(caseId)
    setOracleOpen(false)
    replayInstant(traceId)
  }

  const handleDelete = async (traceId: string) => {
    if (!window.confirm(`Delete trace ${traceId}?`)) return
    try {
      await api.deleteTrace(traceId)
      queryClient.invalidateQueries({ queryKey: ["traces"] })
    } catch {
      // silently ignore — the list will stay as-is
    }
  }

  if (isLoading) {
    return <div className="p-4 text-base text-muted-foreground">Loading traces...</div>
  }

  if (!traces || traces.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
        <History className="h-8 w-8 mb-2 opacity-30" />
        <p className="text-base">No saved traces</p>
        <p className="text-sm text-muted-foreground/60 mt-1">Run an agent to create traces</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full">
      {/* Search + filters */}
      <div className="p-3 border-b border-sidebar-border space-y-2">
        <div className="relative">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search traces..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-8 pr-3 py-2 text-base bg-sidebar-accent border border-sidebar-border rounded-lg focus:outline-none focus:ring-1 focus:ring-ring placeholder:text-muted-foreground/50"
          />
        </div>

        {/* Difficulty filter chips */}
        <div className="flex gap-1.5">
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
            {filtered.length}
          </span>
        </div>

        {/* Model filter chips */}
        {uniqueModels.length > 1 && (
          <div className="flex flex-wrap gap-1.5">
            {uniqueModels.map((m) => (
              <button
                key={m}
                onClick={() => setFilterModel(filterModel === m ? null : m)}
                className={cn(
                  "text-xs px-2 py-0.5 rounded-full border transition-all",
                  filterModel === m
                    ? "border-blue-500/30 bg-blue-500/10 text-blue-500"
                    : "border-sidebar-border text-muted-foreground hover:bg-sidebar-accent",
                )}
              >
                {m}
              </button>
            ))}
          </div>
        )}

        {/* Hospital filter chips */}
        {uniqueHospitals.length > 1 && (
          <div className="flex flex-wrap gap-1.5">
            {uniqueHospitals.map((h) => (
              <button
                key={h}
                onClick={() => setFilterHospital(filterHospital === h ? null : h)}
                className={cn(
                  "text-xs px-2 py-0.5 rounded-full border transition-all",
                  filterHospital === h
                    ? "border-violet-500/30 bg-violet-500/10 text-violet-500"
                    : "border-sidebar-border text-muted-foreground hover:bg-sidebar-accent",
                )}
              >
                {HOSPITAL_LABELS[h] ?? h}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Trace list */}
      <div className="flex-1 overflow-y-auto divide-y divide-border">
        {filtered.map((t) => (
          <div
            key={t.trace_id}
            className="px-3 py-2.5 hover:bg-sidebar-accent transition-colors relative group"
          >
            {/* Delete button */}
            <button
              onClick={() => handleDelete(t.trace_id)}
              className="absolute top-2 right-2 p-1 rounded-md opacity-0 group-hover:opacity-100 text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-all"
              title="Delete trace"
            >
              <Trash2 className="h-3.5 w-3.5" />
            </button>

            {/* Case ID + badges */}
            <div className="flex items-center gap-2 flex-wrap pr-6">
              <span className="font-mono text-base font-medium text-foreground">
                {t.case_id}
              </span>
              {t.difficulty && <DifficultyStars difficulty={t.difficulty} />}
              {t.hospital && (
                <span className="text-xs px-1.5 py-0.5 rounded-full bg-violet-500/10 text-violet-500">
                  {HOSPITAL_LABELS[t.hospital] ?? t.hospital}
                </span>
              )}
              {t.model_short && (
                <span className="text-xs px-1.5 py-0.5 rounded-full bg-blue-500/10 text-blue-500">
                  {t.model_short}
                </span>
              )}
            </div>

            {/* Stats */}
            <div className="flex items-center gap-3 mt-1 text-sm text-muted-foreground">
              <span className="flex items-center gap-1">
                <Wrench className="h-3 w-3" />
                {t.total_tool_calls}
              </span>
              <span className="flex items-center gap-1">
                <Zap className="h-3 w-3" />
                {(t.total_tokens / 1000).toFixed(1)}k
              </span>
              <span className="flex items-center gap-1">
                <Clock className="h-3 w-3" />
                {t.elapsed_time_seconds.toFixed(1)}s
              </span>
              {t.total_cost_usd != null && t.total_cost_usd > 0 && (
                <span className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400">
                  ${t.total_cost_usd.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                </span>
              )}
            </div>

            {/* Actions */}
            <div className="flex gap-1.5 mt-2">
              <button
                onClick={() => handleReplay(t.trace_id, t.case_id)}
                className="flex items-center gap-1 text-xs font-medium px-2 py-1 rounded-md bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
              >
                <Play className="h-3 w-3" />
                Replay
              </button>
              <button
                onClick={() => handleInstant(t.trace_id, t.case_id)}
                className="flex items-center gap-1 text-xs font-medium px-2 py-1 rounded-md bg-muted text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
              >
                <SkipForward className="h-3 w-3" />
                Skip to End
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
