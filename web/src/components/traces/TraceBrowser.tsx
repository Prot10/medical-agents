import { History, Clock, Zap, Wrench, Play, SkipForward } from "lucide-react"
import { useTraces, useReplay } from "@/hooks/useReplay"
import { useAppStore } from "@/stores/appStore"

export function TraceBrowser() {
  const { data: traces, isLoading } = useTraces()
  const { replay, replayInstant } = useReplay()
  const { selectCase, setOracleOpen } = useAppStore()

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
    <div className="divide-y divide-border">
      {traces.map((t) => (
        <div
          key={t.trace_id}
          className="px-3 py-2.5 hover:bg-sidebar-accent transition-colors"
        >
          <div className="font-mono text-base font-medium text-foreground">
            {t.case_id}
          </div>
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
          </div>
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
  )
}
