import { Play, Square, Download, Scale } from "lucide-react"
import { useAppStore } from "@/stores/appStore"
import { useAgentStore } from "@/stores/agentStore"
import { useAgentRun } from "@/hooks/useAgentRun"
import { cn } from "@/lib/utils"
import { TokenCounter } from "@/components/agent/TokenCounter"

const SECTION_LABELS: Record<string, string> = {
  cases: "Patient Cases",
  dataset: "Dataset Analytics",
  traces: "Trace Replay",
  settings: "Settings",
}

export function Header() {
  const { selectedCaseId, selectedHospital, selectedModel, selectedEvaluatorModel, activeSection, triggerOracle } = useAppStore()
  const status = useAgentStore((s) => s.status)
  const events = useAgentStore((s) => s.events)
  const totalTokens = useAgentStore((s) => s.totalTokens)
  const elapsedTime = useAgentStore((s) => s.elapsedTime)
  const { run, stop } = useAgentRun()

  const canEvaluate = status === "complete" && !!selectedCaseId && !!selectedEvaluatorModel

  const handleRun = () => {
    if (!selectedCaseId) return
    run(selectedCaseId, selectedHospital, selectedModel)
  }

  const handleEvaluate = () => {
    triggerOracle()
  }

  const handleExport = () => {
    const blob = new Blob([JSON.stringify(events, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `trace_${selectedCaseId}_${Date.now()}.json`
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
        <TokenCounter tokens={totalTokens} time={elapsedTime} status={status} />
      )}

      {/* Export button */}
      {status === "complete" && (
        <button
          onClick={handleExport}
          className="p-1.5 rounded-lg hover:bg-accent transition-colors text-muted-foreground hover:text-foreground"
          title="Export trace JSON"
        >
          <Download className="h-4 w-4" />
        </button>
      )}

      {/* Evaluate button */}
      <button
        onClick={handleEvaluate}
        disabled={!canEvaluate}
        className={cn(
          "flex items-center gap-2 px-4 py-1.5 text-base font-medium rounded-lg transition-all",
          canEvaluate
            ? "bg-amber-500 text-white hover:bg-amber-500/90 shadow-sm shadow-amber-500/20"
            : "bg-muted text-muted-foreground cursor-not-allowed opacity-50",
        )}
      >
        <Scale className="h-3.5 w-3.5" />
        Evaluate
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
