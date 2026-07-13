import { useEffect, useState } from "react"
import { Zap, Clock } from "lucide-react"
import type { RunStatus } from "@/stores/agentStore"

export function TokenCounter({ tokens, time, status, startedAt }: {
  tokens: number; time: number; status: RunStatus; startedAt: number | null
}) {
  const [now, setNow] = useState(() => Date.now())

  // Tick the live timer while a run is in flight
  useEffect(() => {
    if (status !== "running" || startedAt == null) return
    setNow(Date.now())
    const id = window.setInterval(() => setNow(Date.now()), 100)
    return () => window.clearInterval(id)
  }, [status, startedAt])

  const elapsed =
    status === "running" && startedAt != null ? (now - startedAt) / 1000 : time

  return (
    <div className="flex items-center gap-3 text-sm font-mono text-muted-foreground">
      <div className="flex items-center gap-1.5 px-2 py-1 rounded-lg bg-muted/50">
        <Zap className="h-3 w-3" />
        {tokens > 0 ? `${(tokens / 1000).toFixed(1)}k` : "—"}
      </div>
      <div className="flex items-center gap-1.5 px-2 py-1 rounded-lg bg-muted/50">
        <Clock className="h-3 w-3" />
        {elapsed > 0 ? `${elapsed.toFixed(1)}s` : status === "running" ? "…" : "—"}
      </div>
    </div>
  )
}
