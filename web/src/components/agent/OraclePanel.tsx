import { useState, useRef, useCallback, useEffect } from "react"
import {
  Scale, Loader2, CheckCircle2, XCircle, ShieldCheck,
  Target, Crosshair, Brain, AlertTriangle, Sparkles,
  Wrench, ShieldAlert, HelpCircle, Gauge, X,
} from "lucide-react"
import { streamEvaluation } from "@/api/client"
import { useAgentStore } from "@/stores/agentStore"
import { useAppStore } from "@/stores/appStore"
import { cn } from "@/lib/utils"

interface Metrics {
  diagnostic_accuracy_top1: boolean
  diagnostic_accuracy_top3: boolean
  action_precision: number
  action_recall: number
  critical_actions_hit: number
  contraindicated_actions_taken: number
  efficiency_score: number
  safety_score: number
}

interface JudgeScores {
  diagnostic_accuracy: number
  evidence_identification: number
  evidence_integration: number
  differential_reasoning: number
  tool_efficiency: number
  clinical_safety: number
  red_herring_handling: number | null
  uncertainty_calibration: number
  composite_score: number
  strengths: string[]
  weaknesses: string[]
  critical_errors: string[]
  justification: string
}

type EvalStatus = "idle" | "running" | "complete" | "error"

const SCORE_DIMENSIONS: Array<{ key: keyof JudgeScores; label: string; icon: React.ElementType }> = [
  { key: "diagnostic_accuracy", label: "Diagnostic Accuracy", icon: Target },
  { key: "evidence_identification", label: "Evidence ID", icon: Crosshair },
  { key: "evidence_integration", label: "Evidence Integration", icon: Brain },
  { key: "differential_reasoning", label: "Differential Dx", icon: HelpCircle },
  { key: "tool_efficiency", label: "Tool Efficiency", icon: Wrench },
  { key: "clinical_safety", label: "Clinical Safety", icon: ShieldCheck },
  { key: "red_herring_handling", label: "Red Herring Handling", icon: AlertTriangle },
  { key: "uncertainty_calibration", label: "Uncertainty Calibration", icon: Gauge },
]

function ScoreBar({ label, value, icon: Icon }: { label: string; value: number | null; icon: React.ElementType }) {
  if (value === null) return null
  const pct = (value / 5) * 100
  const color = pct >= 80 ? "bg-emerald-500" : pct >= 50 ? "bg-amber-500" : "bg-red-500"
  const textColor = pct >= 80 ? "text-emerald-500" : pct >= 50 ? "text-amber-500" : "text-red-500"
  return (
    <div className="flex items-center gap-2">
      <Icon className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
      <span className="text-sm w-32 shrink-0 truncate">{label}</span>
      <div className="flex-1 h-2 rounded-full bg-muted overflow-hidden">
        <div className={cn("h-full rounded-full transition-all duration-700", color)} style={{ width: `${pct}%` }} />
      </div>
      <span className={cn("text-sm font-mono font-bold w-6 text-right", textColor)}>{value}</span>
    </div>
  )
}

function MetricBadge({ label, value, good }: { label: string; value: string; good: boolean }) {
  return (
    <div className={cn(
      "flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border text-sm font-medium",
      good ? "border-emerald-500/20 bg-emerald-500/5 text-emerald-600 dark:text-emerald-400" : "border-red-500/20 bg-red-500/5 text-red-500",
    )}>
      {good ? <CheckCircle2 className="h-3.5 w-3.5" /> : <XCircle className="h-3.5 w-3.5" />}
      <span>{label}: {value}</span>
    </div>
  )
}

export function OraclePanel() {
  const [status, setStatus] = useState<EvalStatus>("idle")
  const [metrics, setMetrics] = useState<Metrics | null>(null)
  const [judgeScores, setJudgeScores] = useState<JudgeScores | null>(null)
  const [judgeStream, setJudgeStream] = useState("")
  const [errorMsg, setErrorMsg] = useState("")
  const abortRef = useRef<AbortController | null>(null)
  const scrollRef = useRef<HTMLDivElement>(null)

  const agentStatus = useAgentStore((s) => s.status)
  const agentEvents = useAgentStore((s) => s.events)
  const selectedCaseId = useAppStore((s) => s.selectedCaseId)
  const selectedEvaluatorModel = useAppStore((s) => s.selectedEvaluatorModel)
  const oracleTrigger = useAppStore((s) => s.oracleTrigger)

  const canEvaluate = agentStatus === "complete" && !!selectedCaseId && !!selectedEvaluatorModel

  // Run evaluation whenever the trigger increments (from Header button)
  const lastTriggerRef = useRef(0)
  useEffect(() => {
    if (oracleTrigger > lastTriggerRef.current && canEvaluate) {
      lastTriggerRef.current = oracleTrigger
      runEvaluation()
    }
  }, [oracleTrigger, canEvaluate])

  useEffect(() => {
    if (scrollRef.current && status === "running") {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [judgeStream, status])

  const runEvaluation = useCallback(async () => {
    if (!selectedCaseId || !selectedEvaluatorModel) return

    abortRef.current?.abort()
    const controller = new AbortController()
    abortRef.current = controller

    setStatus("running")
    setMetrics(null)
    setJudgeScores(null)
    setJudgeStream("")
    setErrorMsg("")

    const runComplete = agentEvents.find((e) => e.type === "run_complete")
    const finalResponse = runComplete?.final_response ?? ""
    const toolsCalled = runComplete?.tools_called ?? agentEvents.filter((e) => e.type === "tool_call").map((e) => e.tool_name!)

    try {
      await streamEvaluation(
        selectedCaseId,
        selectedEvaluatorModel,
        agentEvents,
        finalResponse,
        toolsCalled,
        (event) => {
          const e = event as Record<string, unknown>
          if (e.type === "metrics") {
            setMetrics(e as unknown as Metrics)
          } else if (e.type === "judge_delta") {
            setJudgeStream((prev) => prev + (e.delta as string))
          } else if (e.type === "judge_complete") {
            setJudgeScores({
              ...(e as unknown as JudgeScores),
              strengths: (e as Record<string, unknown>).strengths as string[] ?? [],
              weaknesses: (e as Record<string, unknown>).weaknesses as string[] ?? [],
              critical_errors: (e as Record<string, unknown>).critical_errors as string[] ?? [],
              justification: ((e as Record<string, unknown>).justification as string) ?? "",
            })
            setStatus("complete")
          } else if (e.type === "eval_error") {
            setErrorMsg(e.message as string)
            setStatus("error")
          }
        },
        (err) => {
          setErrorMsg(err.message)
          setStatus("error")
        },
        controller.signal,
      )
      setStatus((prev) => prev === "running" ? "complete" : prev)
    } catch (err) {
      if ((err as Error).name !== "AbortError") {
        setErrorMsg((err as Error).message)
        setStatus("error")
      }
    }
  }, [selectedCaseId, selectedEvaluatorModel, agentEvents])

  return (
    <div className="flex flex-col h-full bg-card">
      {/* Header */}
      <div className="flex items-center gap-2 px-4 py-2.5 border-t border-border bg-card/80 backdrop-blur-sm shrink-0">
        <div className="h-6 w-6 rounded-lg bg-amber-500/10 flex items-center justify-center">
          <Scale className="h-3.5 w-3.5 text-amber-500" />
        </div>
        <span className="text-base font-semibold">Oracle Evaluation</span>
        {status === "running" && (
          <div className="flex items-center gap-1.5 text-sm text-amber-500">
            <Loader2 className="h-3 w-3 animate-spin" />
            Evaluating...
          </div>
        )}
        <div className="flex-1" />
        <button
          onClick={() => useAppStore.getState().setOracleOpen(false)}
          className="p-1 rounded-md hover:bg-accent transition-colors text-muted-foreground hover:text-foreground"
          title="Close evaluation panel"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* Content */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
        {status === "idle" && !canEvaluate && (
          <div className="flex flex-col items-center justify-center h-full text-muted-foreground/30">
            <Scale className="h-10 w-10 mb-3" />
            <p className="text-base font-medium">
              {!selectedEvaluatorModel ? "Select an evaluator model in sidebar" : "Run agent first"}
            </p>
          </div>
        )}

        {/* Rule-based metrics */}
        {metrics && (
          <div className="animate-slide-up space-y-3">
            <div className="flex items-center gap-1.5 text-sm uppercase tracking-wider font-semibold text-muted-foreground">
              <Target className="h-3.5 w-3.5" />
              Rule-Based Metrics
            </div>
            <div className="flex flex-wrap gap-2">
              <MetricBadge label="Dx Top-1" value={metrics.diagnostic_accuracy_top1 ? "Hit" : "Miss"} good={metrics.diagnostic_accuracy_top1} />
              <MetricBadge label="Dx Top-3" value={metrics.diagnostic_accuracy_top3 ? "Hit" : "Miss"} good={metrics.diagnostic_accuracy_top3} />
              <MetricBadge label="Safety" value={`${Math.round(metrics.safety_score * 100)}%`} good={metrics.safety_score >= 0.7} />
              <MetricBadge label="Efficiency" value={`${Math.round(metrics.efficiency_score * 100)}%`} good={metrics.efficiency_score >= 0.5} />
            </div>
            <div className="grid grid-cols-2 gap-x-4 gap-y-1.5 text-sm">
              <div><span className="text-muted-foreground">Action Precision:</span> <span className="font-mono font-bold">{Math.round(metrics.action_precision * 100)}%</span></div>
              <div><span className="text-muted-foreground">Action Recall:</span> <span className="font-mono font-bold">{Math.round(metrics.action_recall * 100)}%</span></div>
              <div><span className="text-muted-foreground">Critical Actions:</span> <span className="font-mono font-bold">{Math.round(metrics.critical_actions_hit * 100)}%</span></div>
              <div>
                <span className="text-muted-foreground">Contraindicated:</span>{" "}
                <span className={cn("font-mono font-bold", metrics.contraindicated_actions_taken > 0 ? "text-red-500" : "text-emerald-500")}>
                  {metrics.contraindicated_actions_taken}
                </span>
              </div>
            </div>
          </div>
        )}

        {/* LLM Judge — streaming indicator while running */}
        {status === "running" && judgeStream && !judgeScores && (
          <div className="animate-slide-up space-y-2">
            <div className="flex items-center gap-1.5 text-sm uppercase tracking-wider font-semibold text-muted-foreground">
              <Sparkles className="h-3.5 w-3.5" />
              Oracle Assessment
              <Loader2 className="h-3 w-3 animate-spin text-amber-500 ml-1" />
            </div>
            <div className="rounded-xl border border-amber-500/20 bg-amber-500/5 p-3 text-sm font-mono text-foreground/70 max-h-32 overflow-y-auto whitespace-pre-wrap break-all">
              {judgeStream}
            </div>
          </div>
        )}

        {/* Completed judge scores */}
        {judgeScores && (
          <div className="animate-slide-up space-y-4">
            {/* Composite score header */}
            <div className="flex items-center justify-between p-3 rounded-xl border border-border bg-muted/20">
              <div className="flex items-center gap-2">
                <Sparkles className="h-4 w-4 text-amber-500" />
                <span className="text-base font-semibold">Oracle Score</span>
              </div>
              <span className={cn(
                "text-2xl font-bold tabular-nums",
                judgeScores.composite_score >= 0.7 ? "text-emerald-500" :
                judgeScores.composite_score >= 0.4 ? "text-amber-500" : "text-red-500",
              )}>
                {(judgeScores.composite_score * 100).toFixed(0)}%
              </span>
            </div>

            {/* Score bars */}
            <div className="space-y-2">
              {SCORE_DIMENSIONS.map(({ key, label, icon }) => {
                const val = judgeScores[key]
                if (val === null || val === undefined) return null
                return <ScoreBar key={key} label={label} value={val as number} icon={icon} />
              })}
            </div>

            {/* Strengths & Weaknesses */}
            {(judgeScores.strengths?.length ?? 0) > 0 && (
              <div>
                <div className="text-sm font-semibold text-emerald-500 mb-1">Strengths</div>
                <ul className="text-sm text-muted-foreground space-y-0.5">
                  {judgeScores.strengths.map((s, i) => (
                    <li key={i} className="flex items-start gap-1.5">
                      <CheckCircle2 className="h-3 w-3 text-emerald-500 mt-0.5 shrink-0" />
                      {s}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {(judgeScores.weaknesses?.length ?? 0) > 0 && (
              <div>
                <div className="text-sm font-semibold text-amber-500 mb-1">Weaknesses</div>
                <ul className="text-sm text-muted-foreground space-y-0.5">
                  {judgeScores.weaknesses.map((w, i) => (
                    <li key={i} className="flex items-start gap-1.5">
                      <AlertTriangle className="h-3 w-3 text-amber-500 mt-0.5 shrink-0" />
                      {w}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {(judgeScores.critical_errors?.length ?? 0) > 0 && (
              <div>
                <div className="text-sm font-semibold text-red-500 mb-1">Critical Errors</div>
                <ul className="text-sm space-y-0.5">
                  {judgeScores.critical_errors.map((e, i) => (
                    <li key={i} className="flex items-start gap-1.5 text-red-500">
                      <ShieldAlert className="h-3 w-3 mt-0.5 shrink-0" />
                      {e}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Justification */}
            {judgeScores.justification && (
              <div className="text-base text-muted-foreground leading-relaxed border-l-2 border-amber-500/30 pl-3">
                {judgeScores.justification}
              </div>
            )}
          </div>
        )}

        {errorMsg && (
          <div className="p-3 rounded-xl border border-red-500/30 bg-red-500/5 text-base text-red-500">
            {errorMsg}
          </div>
        )}
      </div>
    </div>
  )
}
