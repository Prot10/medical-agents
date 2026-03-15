import { CheckCircle, XCircle, AlertTriangle, Target, ListChecks, Brain, ShieldAlert } from "lucide-react"
import { useAgentStore } from "@/stores/agentStore"
import { cn } from "@/lib/utils"
import { Badge } from "@/components/ui/Badge"
import { Card } from "@/components/ui/Card"
import { SectionLabel } from "@/components/ui/SectionLabel"
import type { GroundTruth } from "@/api/types"

export function GroundTruthPanel({ groundTruth }: { groundTruth: GroundTruth }) {
  const events = useAgentStore((s) => s.events)
  const toolsCalled = events
    .filter((e) => e.type === "tool_call")
    .map((e) => e.tool_name!)

  return (
    <div className="space-y-5">
      {/* Primary Diagnosis */}
      <Card accent="success">
        <SectionLabel icon={Target}>Primary Diagnosis</SectionLabel>
        <p className="text-base font-bold">{groundTruth.primary_diagnosis}</p>
        <Badge variant="info" className="mt-1">ICD: {groundTruth.icd_code}</Badge>
      </Card>

      {/* Differential */}
      {groundTruth.differential?.length > 0 && (
        <div>
          <SectionLabel icon={Brain}>Differential Diagnoses</SectionLabel>
          <div className="space-y-2">
            {groundTruth.differential.map((d, i) => (
              <div key={i} className="flex items-start gap-2 text-base">
                <Badge variant={d.likelihood.toLowerCase().includes("high") ? "warning" : "outline"} className="shrink-0 mt-0.5">
                  {d.likelihood}
                </Badge>
                <div>
                  <span className="font-medium">{d.diagnosis}</span>
                  <span className="text-muted-foreground"> — {d.key_distinguishing}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action Compliance */}
      {groundTruth.optimal_actions?.length > 0 && (
        <div>
          <SectionLabel icon={ListChecks}>Action Compliance</SectionLabel>
          <div className="space-y-1.5">
            {groundTruth.optimal_actions.map((a, i) => {
              const done = toolsCalled.some((t) =>
                a.action.toLowerCase().includes(t.toLowerCase()) ||
                t.toLowerCase().includes(a.action.toLowerCase().split(" ")[0])
              )
              return (
                <div key={i} className="flex items-start gap-2 text-base">
                  {done ? (
                    <CheckCircle className="h-4 w-4 text-emerald-500 mt-0.5 shrink-0" />
                  ) : (
                    <XCircle className="h-4 w-4 text-muted-foreground/40 mt-0.5 shrink-0" />
                  )}
                  <span className={cn(!done && "text-muted-foreground")}>
                    {a.action}
                  </span>
                  <Badge
                    variant={a.category === "required" ? "info" : "outline"}
                    className="ml-auto shrink-0"
                  >
                    {a.category}
                  </Badge>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Critical Actions */}
      {groundTruth.critical_actions?.length > 0 && (
        <div>
          <SectionLabel icon={ShieldAlert}>Critical Actions</SectionLabel>
          <div className="space-y-1.5">
            {groundTruth.critical_actions.map((a, i) => (
              <div key={i} className="flex items-start gap-2 text-base">
                <AlertTriangle className="h-4 w-4 text-amber-500 mt-0.5 shrink-0" />
                <span>{a}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key Reasoning Points */}
      {groundTruth.key_reasoning_points?.length > 0 && (
        <div>
          <SectionLabel icon={Brain}>Key Reasoning Points</SectionLabel>
          <ul className="text-base text-muted-foreground list-disc ml-5 space-y-1">
            {groundTruth.key_reasoning_points.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
