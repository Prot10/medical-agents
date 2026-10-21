import { CheckCircle, XCircle, AlertTriangle, Target, ListChecks, Brain, ShieldAlert, ArrowDownUp, Hand, ClipboardList, Eye, Fish } from "lucide-react"
import { useAgentStore } from "@/stores/agentStore"
import { cn } from "@/lib/utils"
import { anyPatternMatches, describePattern, toolActions } from "@/lib/policy"
import { Badge } from "@/components/ui/Badge"
import { Card } from "@/components/ui/Card"
import { SectionLabel } from "@/components/ui/SectionLabel"
import type { GroundTruth, ActionImportance, AvoidanceSeverity } from "@/api/types"

const IMPORTANCE_BADGE: Record<ActionImportance, "info" | "outline" | "default"> = {
  required: "info",
  recommended: "outline",
  optional: "default",
}

const SEVERITY_BADGE: Record<AvoidanceSeverity, "warning" | "destructive"> = {
  waste: "warning",
  harm: "destructive",
  contraindicated: "destructive",
}

const REVIEW_BADGE = {
  approved: "success",
  needs_revision: "warning",
  draft: "warning",
} as const

/**
 * The case's clinical policy. When an episode is on screen, each criterion is checked against
 * its tool actions with the same pattern matching the reward uses.
 */
export function GroundTruthPanel({ groundTruth }: { groundTruth: GroundTruth }) {
  const events = useAgentStore((s) => s.events)
  const actions = toolActions(events)
  const hasEpisode = events.length > 0
  const labels = Object.fromEntries(groundTruth.action_criteria.map((c) => [c.criterion_id, c.label]))

  return (
    <div className="space-y-5">
      {/* Review status */}
      <div className="flex items-center gap-2 text-sm">
        <span className="text-muted-foreground">Policy review</span>
        <Badge variant={REVIEW_BADGE[groundTruth.review_status]}>{groundTruth.review_status.replace("_", " ")}</Badge>
      </div>

      {/* Primary Diagnosis */}
      <Card accent="success">
        <SectionLabel icon={Target}>Accepted diagnosis</SectionLabel>
        <p className="text-base font-bold">{groundTruth.diagnosis.accepted[0]}</p>
        {groundTruth.diagnosis.accepted.length > 1 && (
          <p className="text-sm text-muted-foreground mt-1">
            Also accepted: {groundTruth.diagnosis.accepted.slice(1).join(" · ")}
          </p>
        )}
        {groundTruth.diagnosis.icd_codes.length > 0 && (
          <div className="flex flex-wrap gap-1.5 mt-2">
            {groundTruth.diagnosis.icd_codes.map((code) => (
              <Badge key={code} variant="info">ICD {code}</Badge>
            ))}
          </div>
        )}
      </Card>

      {/* Differential */}
      {groundTruth.differential.length > 0 && (
        <div>
          <SectionLabel icon={Brain}>Differential Diagnoses</SectionLabel>
          <div className="space-y-2">
            {groundTruth.differential.map((d, i) => (
              <div key={i} className="flex items-start gap-2 text-base">
                <Badge variant={d.likelihood.includes("high") ? "warning" : "outline"} className="shrink-0 mt-0.5">
                  {d.likelihood.replace("_", " ")}
                </Badge>
                <div>
                  <span className="font-medium">{d.diagnosis}</span>
                  {d.key_features && <span className="text-muted-foreground"> — {d.key_features}</span>}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action criteria */}
      {groundTruth.action_criteria.length > 0 && (
        <div>
          <SectionLabel icon={ListChecks}>Action criteria</SectionLabel>
          <div className="space-y-2">
            {groundTruth.action_criteria.map((c) => {
              const done = anyPatternMatches(c.alternatives, actions)
              return (
                <div key={c.criterion_id} className="flex items-start gap-2 text-base">
                  {!hasEpisode ? (
                    <span className="h-4 w-4 mt-0.5 shrink-0 rounded-full border border-border" />
                  ) : done ? (
                    <CheckCircle className="h-4 w-4 text-emerald-500 mt-0.5 shrink-0" />
                  ) : (
                    <XCircle className="h-4 w-4 text-muted-foreground/40 mt-0.5 shrink-0" />
                  )}
                  <div className="min-w-0 flex-1">
                    <div className={cn(hasEpisode && !done && "text-muted-foreground")}>{c.label}</div>
                    <div className="text-xs font-mono text-muted-foreground/70 break-words">
                      {c.alternatives.map(describePattern).join("  |  ")}
                    </div>
                    {c.rationale && <div className="text-sm text-muted-foreground mt-0.5">{c.rationale}</div>}
                  </div>
                  <Badge variant={IMPORTANCE_BADGE[c.importance]} className="ml-auto shrink-0">{c.importance}</Badge>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Avoided actions */}
      {groundTruth.avoided_actions.length > 0 && (
        <div>
          <SectionLabel icon={ShieldAlert}>Avoided actions</SectionLabel>
          <div className="space-y-2">
            {groundTruth.avoided_actions.map((c) => {
              const taken = hasEpisode && anyPatternMatches(c.alternatives, actions)
              return (
                <div key={c.criterion_id} className="flex items-start gap-2 text-base">
                  <AlertTriangle className={cn("h-4 w-4 mt-0.5 shrink-0", taken ? "text-red-500" : "text-amber-500/60")} />
                  <div className="min-w-0 flex-1">
                    <div className="text-xs font-mono text-muted-foreground/80 break-words">
                      {c.alternatives.map(describePattern).join("  |  ")}
                    </div>
                    <div className={cn("text-sm", taken ? "text-red-500" : "text-muted-foreground")}>
                      {taken && <strong>Taken · </strong>}
                      {c.rationale}
                    </div>
                  </div>
                  <Badge variant={SEVERITY_BADGE[c.severity]} className="ml-auto shrink-0">{c.severity}</Badge>
                </div>
              )
            })}
          </div>
        </div>
      )}

      {/* Sequence and stopping */}
      {(groundTruth.sequence_constraints.length > 0 || groundTruth.stop_rule.required_before_assessment.length > 0) && (
        <div className="space-y-3">
          {groundTruth.sequence_constraints.length > 0 && (
            <div>
              <SectionLabel icon={ArrowDownUp}>Sequence</SectionLabel>
              <ul className="space-y-1.5 text-base">
                {groundTruth.sequence_constraints.map((s, i) => (
                  <li key={i}>
                    <span className="font-medium">{labels[s.before_criterion_id] ?? s.before_criterion_id}</span>
                    <span className="text-muted-foreground"> before </span>
                    <span className="font-medium">{labels[s.after_criterion_id] ?? s.after_criterion_id}</span>
                    <span className="text-sm text-muted-foreground"> — {s.reason}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          {groundTruth.stop_rule.required_before_assessment.length > 0 && (
            <div>
              <SectionLabel icon={Hand}>Stop rule</SectionLabel>
              <p className="text-base text-muted-foreground">
                Assess only after: {groundTruth.stop_rule.required_before_assessment.map((id) => labels[id] ?? id).join(", ")}
                {groundTruth.stop_rule.max_additional_actions > 0 &&
                  `; at most ${groundTruth.stop_rule.max_additional_actions} further action${groundTruth.stop_rule.max_additional_actions === 1 ? "" : "s"}`}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Assessment requirements */}
      {(groundTruth.assessment.required_recommendations.length > 0 || groundTruth.assessment.prohibited_recommendations.length > 0) && (
        <div>
          <SectionLabel icon={ClipboardList}>Assessment requirements</SectionLabel>
          <ul className="text-base space-y-1">
            {groundTruth.assessment.required_recommendations.map((r, i) => (
              <li key={`r${i}`} className="flex gap-2"><CheckCircle className="h-4 w-4 text-emerald-500 mt-0.5 shrink-0" />{r}</li>
            ))}
            {groundTruth.assessment.prohibited_recommendations.map((r, i) => (
              <li key={`p${i}`} className="flex gap-2"><XCircle className="h-4 w-4 text-red-500 mt-0.5 shrink-0" />{r}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Key clinical evidence */}
      {groundTruth.key_clinical_evidence.length > 0 && (
        <div>
          <SectionLabel icon={Eye}>Key clinical evidence</SectionLabel>
          <ul className="text-base text-muted-foreground list-disc ml-5 space-y-1">
            {groundTruth.key_clinical_evidence.map((p, i) => (
              <li key={i}>{p}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Red herrings */}
      {groundTruth.red_herrings.length > 0 && (
        <div>
          <SectionLabel icon={Fish}>Red herrings</SectionLabel>
          <div className="space-y-2">
            {groundTruth.red_herrings.map((h, i) => (
              <div key={i} className="text-base">
                <div className="font-medium">{h.data_point}</div>
                <div className="text-sm text-muted-foreground">{h.correct_interpretation}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
