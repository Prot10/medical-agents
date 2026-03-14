import { CheckCircle, XCircle, AlertTriangle } from "lucide-react"
import { useAgentStore } from "@/stores/agentStore"
import { cn } from "@/lib/utils"
import type { GroundTruth } from "@/api/types"

export function GroundTruthPanel({ groundTruth }: { groundTruth: GroundTruth }) {
  const events = useAgentStore((s) => s.events)
  const toolsCalled = events
    .filter((e) => e.type === "tool_call")
    .map((e) => e.tool_name!)

  return (
    <div className="mt-3 border border-border rounded-lg p-3 space-y-3 bg-secondary/30">
      {/* Primary Diagnosis */}
      <div>
        <Label>Primary Diagnosis</Label>
        <p className="text-sm font-semibold">{groundTruth.primary_diagnosis}</p>
        <p className="text-[10px] text-muted-foreground">ICD: {groundTruth.icd_code}</p>
      </div>

      {/* Differential */}
      {groundTruth.differential_diagnoses.length > 0 && (
        <div>
          <Label>Differential Diagnoses</Label>
          <div className="space-y-1">
            {groundTruth.differential_diagnoses.map((d, i) => (
              <div key={i} className="text-xs">
                <span className="font-medium">{d.diagnosis}</span>
                <span className="text-muted-foreground"> ({d.likelihood})</span>
                <span className="text-muted-foreground"> — {d.key_distinguishing}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Optimal Actions Compliance */}
      {groundTruth.optimal_actions.length > 0 && (
        <div>
          <Label>Action Compliance</Label>
          <div className="space-y-0.5">
            {groundTruth.optimal_actions.map((a, i) => {
              const done = toolsCalled.some((t) =>
                a.action.toLowerCase().includes(t.toLowerCase()) ||
                t.toLowerCase().includes(a.action.toLowerCase().split(" ")[0])
              )
              return (
                <div key={i} className="flex items-start gap-1.5 text-xs">
                  {done ? (
                    <CheckCircle className="h-3.5 w-3.5 text-green-500 mt-0.5 shrink-0" />
                  ) : (
                    <XCircle className="h-3.5 w-3.5 text-zinc-400 mt-0.5 shrink-0" />
                  )}
                  <span className={cn(!done && "text-muted-foreground")}>
                    {a.action}
                    <span className={cn(
                      "ml-1 text-[9px] px-1 py-0.5 rounded",
                      a.category === "required" && "bg-blue-500/10 text-blue-500",
                      a.category === "acceptable" && "bg-zinc-500/10 text-zinc-400",
                    )}>
                      {a.category}
                    </span>
                  </span>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Critical Actions */}
      {groundTruth.critical_actions.length > 0 && (
        <div>
          <Label>Critical Actions</Label>
          <div className="space-y-0.5">
            {groundTruth.critical_actions.map((a, i) => (
              <div key={i} className="flex items-start gap-1.5 text-xs">
                <AlertTriangle className="h-3.5 w-3.5 text-yellow-500 mt-0.5 shrink-0" />
                <span>{a}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key Reasoning Points */}
      {groundTruth.key_reasoning_points.length > 0 && (
        <div>
          <Label>Key Reasoning Points</Label>
          <ul className="text-xs text-muted-foreground list-disc ml-4 space-y-0.5">
            {groundTruth.key_reasoning_points.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

function Label({ children }: { children: React.ReactNode }) {
  return (
    <div className="text-[10px] uppercase tracking-wider font-semibold text-muted-foreground mb-1">
      {children}
    </div>
  )
}
