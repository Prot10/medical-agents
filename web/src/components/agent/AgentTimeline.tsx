import { useEffect, useRef, useState } from "react"
import { Play, Square, Download, Loader2, Zap, History } from "lucide-react"
import { useAgentStore } from "@/stores/agentStore"
import { useAppStore } from "@/stores/appStore"
import { useAgentRun } from "@/hooks/useAgentRun"
import { useTraces, useReplay } from "@/hooks/useReplay"
import { cn } from "@/lib/utils"
import { ThinkingBlock } from "./ThinkingBlock"
import { ToolCallCard } from "./ToolCallCard"
import { ReflectionBlock } from "./ReflectionBlock"
import { AssessmentPanel } from "./AssessmentPanel"
import { TokenCounter } from "./TokenCounter"

export function AgentTimeline() {
  const { selectedCaseId, selectedHospital, selectedModel } = useAppStore()
  const { events, status, errorMessage, totalTokens, elapsedTime } = useAgentStore()
  const { run, stop } = useAgentRun()
  const { data: traces } = useTraces()
  const { replay } = useReplay()
  const [showReplayMenu, setShowReplayMenu] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (status === "running" && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [events.length, status])

  const handleRun = () => {
    if (!selectedCaseId) return
    run(selectedCaseId, selectedHospital, selectedModel)
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

  const renderedItems = buildRenderItems(events)

  return (
    <div className="flex flex-col h-full noise-bg relative">
      {/* Controls bar */}
      <div className="flex items-center gap-2 px-3 py-2.5 border-b border-border bg-card/80 backdrop-blur-sm z-10">
        {status === "running" ? (
          <button
            onClick={stop}
            className="flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-medium bg-red-500/10 text-red-500 border border-red-500/20 rounded-md hover:bg-red-500/15 transition-colors"
          >
            <Square className="h-3 w-3 fill-current" />
            Stop
          </button>
        ) : (
          <button
            onClick={handleRun}
            disabled={!selectedCaseId}
            className={cn(
              "flex items-center gap-1.5 px-3 py-1.5 text-[11px] font-medium rounded-md transition-all",
              selectedCaseId
                ? "bg-primary text-primary-foreground hover:bg-primary/90 shadow-sm shadow-primary/20"
                : "bg-muted text-muted-foreground cursor-not-allowed",
            )}
          >
            <Play className="h-3 w-3 fill-current" />
            Run Agent
          </button>
        )}

        {/* Replay dropdown */}
        {status !== "running" && traces && traces.length > 0 && (
          <div className="relative">
            <button
              onClick={() => setShowReplayMenu(!showReplayMenu)}
              className="flex items-center gap-1 px-2 py-1.5 text-[11px] text-muted-foreground hover:text-foreground rounded-md hover:bg-accent transition-colors"
              title="Replay a saved trace"
            >
              <History className="h-3 w-3" />
              Replay
            </button>
            {showReplayMenu && (
              <div className="absolute top-full left-0 mt-1 w-56 bg-popover border border-border rounded-lg shadow-lg z-20 max-h-48 overflow-y-auto">
                {traces.map((t) => (
                  <button
                    key={t.trace_id}
                    onClick={() => {
                      replay(t.trace_id)
                      setShowReplayMenu(false)
                    }}
                    className="w-full text-left px-3 py-2 text-[11px] hover:bg-accent transition-colors border-b border-border/30 last:border-0"
                  >
                    <div className="font-mono font-medium">{t.case_id}</div>
                    <div className="text-[9px] text-muted-foreground mt-0.5">
                      {t.total_tool_calls} calls · {(t.total_tokens / 1000).toFixed(1)}k tokens · {t.elapsed_time_seconds.toFixed(1)}s
                    </div>
                  </button>
                ))}
              </div>
            )}
          </div>
        )}

        {status === "running" && (
          <div className="flex items-center gap-1.5 text-[10px] text-primary/60">
            <Loader2 className="h-3 w-3 animate-spin" />
          </div>
        )}

        <div className="flex-1" />

        {events.length > 0 && (
          <TokenCounter tokens={totalTokens} time={elapsedTime} status={status} />
        )}

        {status === "complete" && (
          <button
            onClick={handleExport}
            className="p-1.5 rounded-md hover:bg-accent transition-colors text-muted-foreground hover:text-foreground"
            title="Export trace JSON"
          >
            <Download className="h-3.5 w-3.5" />
          </button>
        )}
      </div>

      {/* Timeline content */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto relative z-[1]">
        {events.length === 0 && status === "idle" && (
          <div className="flex flex-col items-center justify-center h-full text-muted-foreground/30">
            <Zap className="h-10 w-10 mb-3" />
            <p className="text-xs tracking-wide">
              {selectedCaseId ? "Ready to run" : "Select a case"}
            </p>
          </div>
        )}

        {renderedItems.length > 0 && (
          <div className="p-3 space-y-2">
            {renderedItems.map((item, i) => {
              switch (item.type) {
                case "thinking":
                  return <ThinkingBlock key={i} content={item.content} turnNumber={item.turnNumber} />
                case "tool_pair":
                  return (
                    <ToolCallCard
                      key={i}
                      toolName={item.toolName}
                      arguments={item.arguments}
                      result={item.result}
                      success={item.success}
                      turnNumber={item.turnNumber}
                    />
                  )
                case "tool_call_pending":
                  return (
                    <ToolCallCard
                      key={i}
                      toolName={item.toolName}
                      arguments={item.arguments}
                      pending
                      turnNumber={item.turnNumber}
                    />
                  )
                case "reflection":
                  return <ReflectionBlock key={i} />
                case "assessment":
                  return <AssessmentPanel key={i} content={item.content} />
                default:
                  return null
              }
            })}

            {status === "running" && (
              <div className="flex items-center gap-2.5 py-3 pl-1">
                <div className="relative h-2.5 w-2.5">
                  <div className="absolute inset-0 rounded-full bg-primary animate-ping opacity-30" />
                  <div className="relative h-2.5 w-2.5 rounded-full bg-primary" />
                </div>
                <span className="text-[11px] text-muted-foreground/60">Agent is thinking...</span>
              </div>
            )}
          </div>
        )}

        {errorMessage && (
          <div className="m-3 p-3 rounded-lg border border-red-500/30 bg-red-500/5 text-[11px] text-red-500">
            {errorMessage}
          </div>
        )}
      </div>
    </div>
  )
}

// Build renderable items from raw events
type RenderItem =
  | { type: "thinking"; content: string; turnNumber: number }
  | { type: "tool_pair"; toolName: string; arguments: Record<string, unknown>; result: Record<string, unknown>; success: boolean; turnNumber: number }
  | { type: "tool_call_pending"; toolName: string; arguments: Record<string, unknown>; turnNumber: number }
  | { type: "reflection" }
  | { type: "assessment"; content: string }

function buildRenderItems(events: import("@/api/types").AgentEvent[]): RenderItem[] {
  const items: RenderItem[] = []

  for (let i = 0; i < events.length; i++) {
    const ev = events[i]

    if (ev.type === "thinking" && ev.content) {
      items.push({ type: "thinking", content: ev.content, turnNumber: ev.turn_number ?? 0 })
    } else if (ev.type === "tool_call") {
      const resultEvent = events.slice(i + 1).find(
        (e) => e.type === "tool_result" && e.tool_name === ev.tool_name
      )
      if (resultEvent) {
        items.push({
          type: "tool_pair",
          toolName: ev.tool_name!,
          arguments: ev.arguments ?? {},
          result: resultEvent.output ?? {},
          success: resultEvent.success ?? true,
          turnNumber: ev.turn_number ?? 0,
        })
      } else {
        items.push({
          type: "tool_call_pending",
          toolName: ev.tool_name!,
          arguments: ev.arguments ?? {},
          turnNumber: ev.turn_number ?? 0,
        })
      }
    } else if (ev.type === "reflection") {
      items.push({ type: "reflection" })
    } else if (ev.type === "assessment") {
      items.push({ type: "assessment", content: ev.content ?? "" })
    }
  }

  return items
}
