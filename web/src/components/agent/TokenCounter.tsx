import { Zap, Clock } from "lucide-react"
import type { RunStatus } from "@/stores/agentStore"

export function TokenCounter({ tokens, time, status }: {
  tokens: number; time: number; status: RunStatus
}) {
  return (
    <div className="flex items-center gap-3 text-sm font-mono text-muted-foreground">
      <div className="flex items-center gap-1.5 px-2 py-1 rounded-lg bg-muted/50">
        <Zap className="h-3 w-3" />
        {tokens > 0 ? `${(tokens / 1000).toFixed(1)}k` : "\u2014"}
      </div>
      <div className="flex items-center gap-1.5 px-2 py-1 rounded-lg bg-muted/50">
        <Clock className="h-3 w-3" />
        {time > 0 ? `${time.toFixed(1)}s` : status === "running" ? "\u2026" : "\u2014"}
      </div>
    </div>
  )
}
