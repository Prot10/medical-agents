import {
  Scale, X, Target, ListChecks, ListPlus, Wrench, ShieldCheck, Trash2, ArrowDownUp, Hand,
  ClipboardList, DollarSign, Zap, AlertTriangle, Loader2,
} from "lucide-react"
import { useAgentStore } from "@/stores/agentStore"
import { useAppStore } from "@/stores/appStore"
import { cn } from "@/lib/utils"
import type { RewardBreakdown } from "@/api/types"

const COMPONENTS: Array<{ key: keyof RewardBreakdown; label: string; icon: React.ElementType }> = [
  { key: "diagnosis", label: "Diagnosis", icon: Target },
  { key: "required_action_coverage", label: "Required actions", icon: ListChecks },
  { key: "recommended_action_coverage", label: "Recommended actions", icon: ListPlus },
  { key: "tool_accuracy", label: "Tool accuracy", icon: Wrench },
  { key: "safety", label: "Safety", icon: ShieldCheck },
  { key: "waste_avoidance", label: "Waste avoidance", icon: Trash2 },
  { key: "sequence", label: "Sequence", icon: ArrowDownUp },
  { key: "stopping", label: "Stopping", icon: Hand },
  { key: "assessment", label: "Assessment", icon: ClipboardList },
  { key: "cost_efficiency", label: "Cost efficiency", icon: DollarSign },
  { key: "token_efficiency", label: "Token efficiency", icon: Zap },
  { key: "icd_code", label: "ICD code (weight 0)", icon: ClipboardList },
]

function tone(value: number) {
  if (value >= 0.8) return { bar: "bg-emerald-500", text: "text-emerald-500" }
  if (value >= 0.5) return { bar: "bg-amber-500", text: "text-amber-500" }
  return { bar: "bg-red-500", text: "text-red-500" }
}

function ScoreBar({ label, value, icon: Icon }: { label: string; value: number; icon: React.ElementType }) {
  const { bar, text } = tone(value)
  return (
    <div className="flex items-center gap-2">
      <Icon className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
      <span className="text-sm w-40 shrink-0 truncate">{label}</span>
      <div className="flex-1 h-2 rounded-full bg-muted overflow-hidden">
        <div className={cn("h-full rounded-full transition-all duration-700", bar)} style={{ width: `${value * 100}%` }} />
      </div>
      <span className={cn("text-sm font-mono font-bold w-10 text-right", text)}>{value.toFixed(2)}</span>
    </div>
  )
}

export function ScorePanel() {
  const reward = useAgentStore((s) => s.reward)
  const status = useAgentStore((s) => s.status)
  const events = useAgentStore((s) => s.events)
  const setScoreOpen = useAppStore((s) => s.setScoreOpen)

  return (
    <div className="flex flex-col h-full bg-card">
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border shrink-0">
        <div className="h-6 w-6 rounded-lg bg-amber-500/10 flex items-center justify-center">
          <Scale className="h-3.5 w-3.5 text-amber-500" />
        </div>
        <span className="text-base font-semibold">Policy Reward</span>
        <button
          onClick={() => setScoreOpen(false)}
          className="ml-auto p-1 rounded-md text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
          title="Close"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        {!reward && status === "running" && (
          <div className="flex items-center justify-center gap-2 py-8 text-sm text-muted-foreground">
            <Loader2 className="h-4 w-4 animate-spin" />
            Scored when the episode ends
          </div>
        )}
        {!reward && status !== "running" && (
          <div className="py-8 text-center text-sm text-muted-foreground">
            {events.length === 0 ? "Run a case or open a saved episode to see its reward." : "No reward for this episode."}
          </div>
        )}

        {reward && (
          <div className="space-y-5">
            {reward.policy_review_status !== "approved" && (
              <div className="flex items-start gap-2 p-3 rounded-lg border border-amber-500/30 bg-amber-500/5 text-sm">
                <AlertTriangle className="h-4 w-4 text-amber-500 mt-0.5 shrink-0" />
                <span>
                  The case policy is <strong>{reward.policy_review_status.replace("_", " ")}</strong>. This is an engineering
                  score against an unreviewed policy and is not reportable.
                </span>
              </div>
            )}

            <div className="flex items-end gap-4">
              <div>
                <div className="text-xs uppercase tracking-widest font-semibold text-muted-foreground/60">Scalar reward</div>
                <div className={cn("text-4xl font-bold font-mono", tone(reward.reward.scalar).text)}>
                  {reward.reward.scalar.toFixed(3)}
                </div>
              </div>
              <div className="text-sm text-muted-foreground pb-1">
                {reward.reward.invalid_actions} invalid action{reward.reward.invalid_actions === 1 ? "" : "s"}
              </div>
            </div>

            {reward.reward.caps_applied.length > 0 && (
              <div>
                <div className="text-xs uppercase tracking-widest font-semibold text-muted-foreground/60 mb-1.5">Caps applied</div>
                <div className="flex flex-wrap gap-1.5">
                  {reward.reward.caps_applied.map((cap) => (
                    <span key={cap} className="text-xs font-mono px-2 py-0.5 rounded-full bg-red-500/10 text-red-500">{cap}</span>
                  ))}
                </div>
              </div>
            )}

            <div className="space-y-2">
              {COMPONENTS.map(({ key, label, icon }) => (
                <ScoreBar key={key} label={label} value={reward.reward[key] as number} icon={icon} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
