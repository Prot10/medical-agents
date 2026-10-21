import { Play, Square, Download, Scale, DollarSign } from "lucide-react"
import { useAppStore } from "@/stores/appStore"
import { useAgentStore } from "@/stores/agentStore"
import { useAgentRun } from "@/hooks/useAgentRun"
import { cn } from "@/lib/utils"
import { TokenCounter } from "@/components/agent/TokenCounter"

const SECTION_LABELS: Record<string, string> = {
  cases: "Patient Cases",
  dataset: "Dataset Analytics",
  episodes: "Episode Replay",
  rules: "Hospital Rules",
  architecture: "Architecture",
  profiles: "Experiment Profiles",
}

export function Header() {
  const { selectedCaseId, selectedProfileId, activeSection, scoreOpen, setScoreOpen } = useAppStore()
  const status = useAgentStore((s) => s.status)
  const events = useAgentStore((s) => s.events)
  const reward = useAgentStore((s) => s.reward)
  const episodeId = useAgentStore((s) => s.episodeId)
  const totalTokens = useAgentStore((s) => s.totalTokens)
  const totalCost = useAgentStore((s) => s.totalCost)
  const elapsedTime = useAgentStore((s) => s.elapsedTime)
  const startedAt = useAgentStore((s) => s.startedAt)
  const { run, stop } = useAgentRun()

  const finished = status === "complete" || status === "failed"

  const handleRun = () => {
    if (!selectedCaseId) return
    run(selectedCaseId, selectedProfileId)
  }

  const handleExport = () => {
    const blob = new Blob([JSON.stringify({ schema_version: "1.0", events }, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `${episodeId ?? `episode_${selectedCaseId}_${Date.now()}`}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <header className="flex items-center gap-3 px-4 py-2 border-b border-border bg-card/80 backdrop-blur-sm shrink-0">
      {/* Breadcrumb */}
      <div className="flex items-center gap-2 text-base min-w-0">
        <span className="font-medium text-foreground">{SECTION_LABELS[activeSection]}</span>
        {selectedCaseId && (
          <>
            <span className="text-muted-foreground/40">/</span>
            <span className="font-mono text-primary font-medium truncate">{selectedCaseId}</span>
          </>
        )}
      </div>

      <div className="flex-1" />

      {/* Metrics */}
      {events.length > 0 && (
        <>
          {totalCost > 0 && (
            <div className="flex items-center gap-1 px-2 py-1 rounded-lg bg-muted/50 text-sm font-mono text-muted-foreground" title="Simulated work-up cost">
              <DollarSign className="h-3 w-3" />
              {totalCost.toLocaleString(undefined, { maximumFractionDigits: 0 })}
            </div>
          )}
          <TokenCounter tokens={totalTokens} time={elapsedTime} status={status} startedAt={startedAt} />
        </>
      )}

      {/* Export button */}
      {finished && (
        <button
          onClick={handleExport}
          className="p-1.5 rounded-lg hover:bg-accent transition-colors text-muted-foreground hover:text-foreground"
          title="Export episode JSON"
        >
          <Download className="h-4 w-4" />
        </button>
      )}

      {/* Reward panel toggle */}
      <button
        onClick={() => setScoreOpen(!scoreOpen)}
        disabled={!reward && !scoreOpen}
        className={cn(
          "flex items-center gap-2 px-4 py-1.5 text-base font-medium rounded-lg transition-all",
          reward
            ? "bg-amber-500 text-white hover:bg-amber-500/90 shadow-sm shadow-amber-500/20"
            : "bg-muted text-muted-foreground cursor-not-allowed opacity-50",
        )}
      >
        <Scale className="h-3.5 w-3.5" />
        {reward ? `Reward ${reward.reward.scalar.toFixed(2)}` : "Reward"}
      </button>

      {/* Run controls */}
      {status === "running" ? (
        <button
          onClick={stop}
          className="flex items-center gap-2 px-4 py-1.5 text-sm font-medium bg-red-500/10 text-red-500 border border-red-500/20 rounded-lg hover:bg-red-500/15 transition-colors"
        >
          <Square className="h-3.5 w-3.5 fill-current" />
          Stop
        </button>
      ) : (
        <button
          onClick={handleRun}
          disabled={!selectedCaseId}
          className={cn(
            "flex items-center gap-2 px-4 py-1.5 text-base font-medium rounded-lg transition-all",
            selectedCaseId
              ? "bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm shadow-primary/20"
              : "bg-muted text-muted-foreground cursor-not-allowed",
          )}
        >
          <Play className="h-3.5 w-3.5 fill-current" />
          Run Agent
        </button>
      )}
    </header>
  )
}
