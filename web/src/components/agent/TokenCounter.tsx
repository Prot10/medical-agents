import { Zap, Clock } from "lucide-react"
import type { RunStatus } from "@/stores/agentStore"

export function TokenCounter({ tokens, time, status }: {
  tokens: number; time: number; status: RunStatus
}) {
  return (
    <div className="flex items-center gap-3 text-[10px] font-mono text-muted-foreground/70">
      <div className="flex items-center gap-1">
        <Zap className="h-2.5 w-2.5" />
        {tokens > 0 ? `${(tokens / 1000).toFixed(1)}k` : "\u2014"}
      </div>
      <div className="flex items-center gap-1">
        <Clock className="h-2.5 w-2.5" />
        {time > 0 ? `${time.toFixed(1)}s` : status === "running" ? "\u2026" : "\u2014"}
      </div>
    </div>
  )
}
