import { useEffect, useRef } from "react"
import { Zap, Loader2, GitFork } from "lucide-react"
import { useAgentStore } from "@/stores/agentStore"
import { useAppStore } from "@/stores/appStore"
import { ThinkingBlock } from "./ThinkingBlock"
import { ToolCallCard } from "./ToolCallCard"
import { ReflectionBlock } from "./ReflectionBlock"
import { AssessmentPanel } from "./AssessmentPanel"
import { StreamingContent } from "./StreamingContent"

// ─── Centered connector between blocks ────────────────────────────────────────

function Connector() {
  return (
    <div className="flex justify-center">
      <div className="w-0.5 h-4 bg-border/40" />
    </div>
  )
}

// ─── Main component ───────────────────────────────────────────────────────────

export function AgentTimeline() {
  const { selectedCaseId } = useAppStore()
  const { events, status, errorMessage, streamingContent, streamingThinkContent, streamingTurnNumber } = useAgentStore()
  const scrollRef = useRef<HTMLDivElement>(null)

  const isStreaming = !!(streamingContent || streamingThinkContent)

  useEffect(() => {
    if (status === "running" && scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [events.length, status, streamingContent, streamingThinkContent])

  const groupedItems = groupItems(buildRenderItems(events))
  const hasContent = groupedItems.length > 0 || isStreaming || (status === "running" && !isStreaming)

  return (
    <div className="flex flex-col h-full noise-bg relative bg-card">
      {/* Timeline header */}
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border bg-card/80 backdrop-blur-sm z-10 shrink-0">
        <div className="h-6 w-6 rounded-lg bg-primary/10 flex items-center justify-center">
          <Zap className="h-3.5 w-3.5 text-primary" />
        </div>
        <span className="text-base font-semibold">Agent Timeline</span>
        {status === "running" && (
          <div className="flex items-center gap-1.5 ml-2">
            <Loader2 className="h-3.5 w-3.5 animate-spin text-primary" />
            <span className="text-sm text-primary">Running...</span>
          </div>
        )}
      </div>

      {/* Timeline content */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto relative z-[1]">
        {events.length === 0 && status === "idle" && !isStreaming && (
          <div className="flex flex-col items-center justify-center h-full text-muted-foreground/30">
            <div className="h-16 w-16 rounded-2xl bg-primary/5 flex items-center justify-center mb-4">
              <Zap className="h-8 w-8 text-primary/20" />
            </div>
            <p className="text-base font-medium">
              {selectedCaseId ? "Ready to run" : "Select a case"}
            </p>
            <p className="text-sm text-muted-foreground/40 mt-1">
              {selectedCaseId ? "Click Run Agent to start" : "Choose a case from the sidebar"}
            </p>
          </div>
        )}

        {hasContent && (
          <div className="p-4">
            {groupedItems.map((item, i) => {
              const showConnector = i > 0

              switch (item.type) {
                case "thinking": {
                  const shouldCollapse = i < groupedItems.length - 1 || status === "complete"
                  return (
                    <div key={i}>
                      {showConnector && <Connector />}
                      <div className="space-y-2 animate-fade-in">
                        {item.content && (
                          <StreamingContent
                            content={item.content}
                            turnNumber={item.turnNumber}
                            collapsed={shouldCollapse}
                          />
                        )}
                        {item.thinkContent && (
                          <ThinkingBlock content={item.thinkContent} turnNumber={item.turnNumber} />
                        )}
                      </div>
                    </div>
                  )
                }
                case "tool_pair":
                  return (
                    <div key={i}>
                      {showConnector && <Connector />}
                      <div className="animate-slide-up">
                        <ToolCallCard
                          toolName={item.toolName}
                          arguments={item.arguments}
                          result={item.result}
                          success={item.success}
                          turnNumber={item.turnNumber}
                        />
                      </div>
                    </div>
                  )
                case "tool_call_pending":
                  return (
                    <div key={i}>
                      {showConnector && <Connector />}
                      <ToolCallCard
                        toolName={item.toolName}
                        arguments={item.arguments}
                        pending
                        turnNumber={item.turnNumber}
                      />
                    </div>
                  )
                case "tool_group":
                  return (
                    <div key={i}>
                      {showConnector && <Connector />}
                      <div className="rounded-xl border border-tool-call/20 bg-tool-call/[0.03] p-3 space-y-2">
                        <div className="flex items-center gap-1.5 text-xs text-tool-call/60 px-1">
                          <GitFork className="h-3 w-3 rotate-180" />
                          <span>{item.tools.length} tools called in parallel</span>
                        </div>
                        {item.tools.map((tool, j) => (
                          <div key={j} className="animate-slide-up">
                            <ToolCallCard
                              toolName={tool.toolName}
                              arguments={tool.arguments}
                              result={"result" in tool ? tool.result : undefined}
                              success={"success" in tool ? tool.success : undefined}
                              pending={tool.type === "tool_call_pending"}
                              turnNumber={tool.turnNumber}
                            />
                          </div>
                        ))}
                      </div>
                    </div>
                  )
                case "reflection":
                  return (
                    <div key={i}>
                      {showConnector && <Connector />}
                      <ReflectionBlock />
                      {/* No extra connector after — next item adds its own */}
                    </div>
                  )
                case "assessment":
                  return (
                    <div key={i}>
                      {showConnector && <Connector />}
                      <div className="animate-slide-up">
                        <AssessmentPanel content={item.content} />
                      </div>
                    </div>
                  )
                default:
                  return null
              }
            })}

            {/* Live streaming blocks */}
            {isStreaming && (
              <div>
                {groupedItems.length > 0 && <Connector />}
                <div className="space-y-2 animate-fade-in">
                  {streamingContent && (
                    <StreamingContent
                      content={streamingContent}
                      turnNumber={streamingTurnNumber}
                      streaming
                    />
                  )}
                  {streamingThinkContent && (
                    <ThinkingBlock
                      content={streamingThinkContent}
                      turnNumber={streamingTurnNumber}
                      streaming
                    />
                  )}
                </div>
              </div>
            )}

            {/* Thinking spinner */}
            {status === "running" && !isStreaming && (
              <div>
                {(groupedItems.length > 0 || isStreaming) && <Connector />}
                <div className="flex items-center justify-center gap-2 py-3">
                  <div className="relative h-2.5 w-2.5">
                    <div className="absolute inset-0 rounded-full bg-primary animate-ping opacity-30" />
                    <div className="relative h-2.5 w-2.5 rounded-full bg-primary" />
                  </div>
                  <span className="text-sm text-muted-foreground/60">Agent is thinking...</span>
                </div>
              </div>
            )}
          </div>
        )}

        {errorMessage && (
          <div className="m-4 p-4 rounded-xl border border-red-500/30 bg-red-500/5 text-base text-red-500">
            {errorMessage}
          </div>
        )}
      </div>
    </div>
  )
}

// ─── Data processing ──────────────────────────────────────────────────────────

type ToolPairItem = { type: "tool_pair"; toolName: string; arguments: Record<string, unknown>; result: Record<string, unknown>; success: boolean; turnNumber: number }
type ToolPendingItem = { type: "tool_call_pending"; toolName: string; arguments: Record<string, unknown>; turnNumber: number }

type RenderItem =
  | { type: "thinking"; content: string; thinkContent: string; turnNumber: number }
  | ToolPairItem
  | ToolPendingItem
  | { type: "tool_group"; tools: (ToolPairItem | ToolPendingItem)[]; turnNumber: number }
  | { type: "reflection" }
  | { type: "assessment"; content: string }

function buildRenderItems(events: import("@/api/types").AgentEvent[]): RenderItem[] {
  const items: RenderItem[] = []

  for (let i = 0; i < events.length; i++) {
    const ev = events[i]

    if (ev.type === "thinking") {
      items.push({
        type: "thinking",
        content: ev.content ?? "",
        thinkContent: ev.think_content ?? "",
        turnNumber: ev.turn_number ?? 0,
      })
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

/** Group consecutive tool items into tool_group when there are 2+. */
function groupItems(items: RenderItem[]): RenderItem[] {
  const result: RenderItem[] = []
  let toolBuffer: (ToolPairItem | ToolPendingItem)[] = []

  function flushTools() {
    if (toolBuffer.length === 0) return
    if (toolBuffer.length === 1) {
      result.push(toolBuffer[0])
    } else {
      result.push({ type: "tool_group", tools: [...toolBuffer], turnNumber: toolBuffer[0].turnNumber })
    }
    toolBuffer = []
  }

  for (const item of items) {
    if (item.type === "tool_pair" || item.type === "tool_call_pending") {
      toolBuffer.push(item)
    } else {
      flushTools()
      result.push(item)
    }
  }
  flushTools()

  return result
}
