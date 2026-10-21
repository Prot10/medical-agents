import { Shield, CheckCircle2 } from "lucide-react"
import { cn } from "@/lib/utils"
import type { SubmitAssessment } from "@/api/types"

const URGENCY_STYLES: Record<SubmitAssessment["urgency"], string> = {
  emergent: "bg-red-500/10 text-red-500 border-red-500/20",
  urgent: "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/20",
  routine: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border-emerald-500/20",
}

function percent(value: number | null): string {
  return value == null ? "—" : `${Math.round(value * 100)}%`
}

export function AssessmentPanel({ assessment }: { assessment: SubmitAssessment }) {
  return (
    <div className="relative rounded-xl border-2 border-assessment/30 overflow-hidden success-pulse">
      {/* Gradient header */}
      <div className="flex items-center gap-2.5 px-4 py-3 bg-gradient-to-r from-assessment/15 via-assessment/10 to-transparent border-b border-assessment/15">
        <div className="h-8 w-8 rounded-lg bg-assessment/15 flex items-center justify-center">
          <Shield className="h-4.5 w-4.5 text-assessment" />
        </div>
        <span className="text-base font-bold tracking-tight text-assessment">Final Assessment</span>
        <CheckCircle2 className="h-4.5 w-4.5 text-assessment/60 ml-auto" />
      </div>

      <div className="px-5 py-4 space-y-4 text-base">
        {/* Primary diagnosis */}
        <div>
          <div className="text-xs uppercase tracking-widest font-semibold text-muted-foreground/60 mb-1">Primary diagnosis</div>
          <div className="flex items-baseline gap-2 flex-wrap">
            <span className="text-lg font-bold">{assessment.primary_diagnosis}</span>
            {assessment.icd10_code && (
              <span className="font-mono text-sm px-1.5 py-0.5 rounded bg-muted text-muted-foreground">{assessment.icd10_code}</span>
            )}
          </div>
          <div className="flex items-center gap-2 mt-2 text-sm">
            <span className={cn("px-2 py-0.5 rounded-full border font-medium capitalize", URGENCY_STYLES[assessment.urgency])}>
              {assessment.urgency}
            </span>
            <span className="text-muted-foreground">Confidence {percent(assessment.confidence)}</span>
          </div>
        </div>

        {/* Differential */}
        {assessment.differential.length > 0 && (
          <div>
            <div className="text-xs uppercase tracking-widest font-semibold text-muted-foreground/60 mb-1.5">Differential</div>
            <ul className="space-y-1">
              {assessment.differential.map((d, i) => (
                <li key={i} className="flex items-center gap-2">
                  <span className="flex-1">{d.diagnosis}</span>
                  <span className="text-sm font-mono text-muted-foreground">{percent(d.confidence)}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Recommendations */}
        {assessment.recommendations.length > 0 && (
          <div>
            <div className="text-xs uppercase tracking-widest font-semibold text-muted-foreground/60 mb-1.5">Recommendations</div>
            <ul className="list-disc ml-5 space-y-1 text-foreground/90">
              {assessment.recommendations.map((r, i) => (
                <li key={i}>{r}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}
