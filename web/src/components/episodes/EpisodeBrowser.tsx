import { useMemo, useState } from "react"
import { History, Zap, Wrench, Play, SkipForward, Search, Trash2, Clock } from "lucide-react"
import { useQueryClient } from "@tanstack/react-query"
import { DifficultyStars } from "@/components/ui/DifficultyStars"
import { QueryError } from "@/components/ui/QueryError"
import { useEpisodes, useReplay } from "@/hooks/useReplay"
import { useAppStore } from "@/stores/appStore"
import { api } from "@/api/client"
import { cn } from "@/lib/utils"

/** The trailing nanosecond timestamp of an episode id, zero-padded so strings sort by time. */
function savedAt(episodeId: string): string {
  return (episodeId.split("_").pop() ?? "").padStart(20, "0")
}

export function EpisodeBrowser() {
  const { data: episodes, isLoading, isError, error, refetch } = useEpisodes()
  const { replay, replayInstant } = useReplay()
  const selectCase = useAppStore((s) => s.selectCase)
  const queryClient = useQueryClient()

  const [search, setSearch] = useState("")
  const [filterDifficulty, setFilterDifficulty] = useState<string | null>(null)
  const [filterProfile, setFilterProfile] = useState<string | null>(null)

  const uniqueProfiles = useMemo(
    () => [...new Set((episodes ?? []).map((e) => e.profile_id))].sort(),
    [episodes],
  )

  // Newest first: episode ids end with the save time in nanoseconds
  const filtered = useMemo(() => {
    if (!episodes) return []
    return episodes
      .filter((e) => {
        const matchSearch = !search || e.case_id.toLowerCase().includes(search.toLowerCase())
        const matchDifficulty = !filterDifficulty || e.difficulty === filterDifficulty
        const matchProfile = !filterProfile || e.profile_id === filterProfile
        return matchSearch && matchDifficulty && matchProfile
      })
      .sort((a, b) => savedAt(b.episode_id).localeCompare(savedAt(a.episode_id)))
  }, [episodes, search, filterDifficulty, filterProfile])

  const handleReplay = (episodeId: string, caseId: string) => {
    selectCase(caseId)
    replay(episodeId)
  }

  const handleInstant = (episodeId: string, caseId: string) => {
    selectCase(caseId)
    replayInstant(episodeId)
  }

  const handleDelete = async (episodeId: string) => {
    if (!window.confirm(`Delete episode ${episodeId}?`)) return
    try {
      await api.deleteEpisode(episodeId)
      queryClient.invalidateQueries({ queryKey: ["episodes"] })
    } catch {
      // silently ignore — the list will stay as-is
    }
  }

  if (isLoading) {
    return <div className="p-4 text-base text-muted-foreground">Loading episodes...</div>
  }

  if (isError) {
    return <QueryError message="Could not load episodes." error={error} onRetry={() => refetch()} />
  }

  if (!episodes || episodes.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-muted-foreground">
        <History className="h-8 w-8 mb-2 opacity-30" />
        <p className="text-base">No saved episodes</p>
        <p className="text-sm text-muted-foreground/60 mt-1">Every run is saved as an episode</p>
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
            placeholder="Search episodes..."
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

        {/* Profile filter chips */}
        {uniqueProfiles.length > 1 && (
          <div className="flex flex-wrap gap-1.5">
            {uniqueProfiles.map((p) => (
              <button
                key={p}
                onClick={() => setFilterProfile(filterProfile === p ? null : p)}
                className={cn(
                  "text-xs px-2 py-0.5 rounded-full border transition-all font-mono",
                  filterProfile === p
                    ? "border-blue-500/30 bg-blue-500/10 text-blue-500"
                    : "border-sidebar-border text-muted-foreground hover:bg-sidebar-accent",
                )}
              >
                {p}
              </button>
            ))}
          </div>
        )}
      </div>

      {/* Episode list */}
      <div className="flex-1 overflow-y-auto divide-y divide-border">
        {filtered.map((e) => (
          <div
            key={e.episode_id}
            className="px-3 py-2.5 hover:bg-sidebar-accent transition-colors relative group"
          >
            {/* Delete button */}
            <button
              onClick={() => handleDelete(e.episode_id)}
              className="absolute top-2 right-2 p-1 rounded-md opacity-0 group-hover:opacity-100 text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-all"
              title="Delete episode"
            >
              <Trash2 className="h-3.5 w-3.5" />
            </button>

            {/* Case ID + badges */}
            <div className="flex items-center gap-2 flex-wrap pr-6">
              <span className="font-mono text-base font-medium text-foreground">{e.case_id}</span>
              {e.difficulty && <DifficultyStars difficulty={e.difficulty} />}
              {e.status !== "run.completed" && (
                <span className="text-xs px-1.5 py-0.5 rounded-full bg-red-500/10 text-red-500">
                  {e.status === "run.failed" ? "failed" : "incomplete"}
                </span>
              )}
            </div>
            <div className="text-xs font-mono text-blue-500 mt-0.5 truncate">{e.profile_id}</div>

            {/* Stats */}
            <div className="flex items-center gap-3 mt-1 text-sm text-muted-foreground">
              <span className="flex items-center gap-1" title="Tool calls">
                <Wrench className="h-3 w-3" />
                {e.tool_call_count}
              </span>
              <span className="flex items-center gap-1" title="Tokens">
                <Zap className="h-3 w-3" />
                {(e.total_tokens / 1000).toFixed(1)}k
              </span>
              <span className="flex items-center gap-1" title="Model latency">
                <Clock className="h-3 w-3" />
                {e.model_latency_seconds.toFixed(1)}s
              </span>
              {e.total_cost_usd > 0 && (
                <span className="flex items-center gap-1 text-emerald-600 dark:text-emerald-400">
                  ${e.total_cost_usd.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                </span>
              )}
            </div>

            {/* Actions */}
            <div className="flex gap-1.5 mt-2">
              <button
                onClick={() => handleReplay(e.episode_id, e.case_id)}
                className="flex items-center gap-1 text-xs font-medium px-2 py-1 rounded-md bg-primary/10 text-primary hover:bg-primary/20 transition-colors"
              >
                <Play className="h-3 w-3" />
                Replay
              </button>
              <button
                onClick={() => handleInstant(e.episode_id, e.case_id)}
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
