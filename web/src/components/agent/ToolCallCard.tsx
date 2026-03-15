import { useState } from "react"
import {
  ChevronRight, ChevronDown, CheckCircle2, XCircle, Loader2,
  Brain, Activity, Heart, FlaskConical, Droplets, BookOpen, Pill,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { ToolResultRenderer } from "@/components/results/ToolResultRenderer"

const TOOL_META: Record<string, { icon: React.ElementType; label: string; accent: string; bgClass: string; color: string }> = {
  analyze_brain_mri: { icon: Brain, label: "Brain MRI", accent: "text-violet-500 dark:text-violet-400", bgClass: "bg-violet-500/15", color: "#8b5cf6" },
  analyze_eeg: { icon: Activity, label: "EEG Analysis", accent: "text-blue-500 dark:text-blue-400", bgClass: "bg-blue-500/15", color: "#3b82f6" },
  analyze_ecg: { icon: Heart, label: "ECG Analysis", accent: "text-rose-500 dark:text-rose-400", bgClass: "bg-rose-500/15", color: "#f43f5e" },
  interpret_labs: { icon: FlaskConical, label: "Lab Results", accent: "text-emerald-500 dark:text-emerald-400", bgClass: "bg-emerald-500/15", color: "#10b981" },
  analyze_csf: { icon: Droplets, label: "CSF Analysis", accent: "text-cyan-500 dark:text-cyan-400", bgClass: "bg-cyan-500/15", color: "#06b6d4" },
  search_medical_literature: { icon: BookOpen, label: "Literature Search", accent: "text-amber-500 dark:text-amber-400", bgClass: "bg-amber-500/15", color: "#f59e0b" },
  check_drug_interactions: { icon: Pill, label: "Drug Interactions", accent: "text-orange-500 dark:text-orange-400", bgClass: "bg-orange-500/15", color: "#f97316" },
}

interface ToolCallCardProps {
  toolName: string
  arguments: Record<string, unknown>
  result?: Record<string, unknown>
  success?: boolean
  pending?: boolean
  turnNumber?: number
}

export function ToolCallCard({ toolName, arguments: args, result, success, pending }: ToolCallCardProps) {
  const [expanded, setExpanded] = useState(false)
  const meta = TOOL_META[toolName] ?? {
    icon: FlaskConical, label: toolName, accent: "text-muted-foreground", bgClass: "bg-muted", color: "#888",
  }
  const Icon = meta.icon

  return (
    <div className={cn(
      "rounded-xl border overflow-hidden transition-all duration-200",
      pending && "border-tool-call/30 glow-pulse",
      !pending && success && "border-border",
      !pending && success === false && "border-red-500/30",
    )}>
      {/* Header */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-3 px-3 py-2.5 hover:bg-accent/30 transition-colors group"
      >
        {/* Expand chevron */}
        <span className="text-muted-foreground/40 group-hover:text-muted-foreground transition-colors">
          {expanded
            ? <ChevronDown className="h-4 w-4" />
            : <ChevronRight className="h-4 w-4" />}
        </span>

        {/* Tool icon badge */}
        <div className={cn("h-8 w-8 rounded-lg flex items-center justify-center shrink-0", meta.bgClass)}>
          <Icon className={cn("h-4 w-4", meta.accent)} />
        </div>

        {/* Tool name */}
        <div className="flex-1 text-left min-w-0">
          <span className="text-base font-semibold">{meta.label}</span>
          {/* Collapsed arg preview */}
          {!expanded && Object.keys(args).length > 0 && (
            <div className="text-sm text-muted-foreground/60 truncate mt-0.5 font-mono">
              {Object.entries(args).map(([k, v]) => `${k}: ${typeof v === "string" ? v : JSON.stringify(v)}`).join(", ")}
            </div>
          )}
        </div>

        {/* Status */}
        <span className="shrink-0">
          {pending ? (
            <span className="flex items-center gap-1.5 text-sm font-medium text-tool-call px-2 py-0.5 rounded-full bg-tool-call/10">
              <Loader2 className="h-3 w-3 animate-spin" />
              Running
            </span>
          ) : success ? (
            <span className="flex items-center gap-1 text-sm font-medium text-emerald-500 px-2 py-0.5 rounded-full bg-emerald-500/10">
              <CheckCircle2 className="h-3.5 w-3.5" />
              Done
            </span>
          ) : (
            <span className="flex items-center gap-1 text-sm font-medium text-red-500 px-2 py-0.5 rounded-full bg-red-500/10">
              <XCircle className="h-3.5 w-3.5" />
              Failed
            </span>
          )}
        </span>
      </button>

      {/* Expanded content */}
      {expanded && (
        <div className="border-t border-border/40 animate-fade-in">
          {/* Arguments */}
          {Object.keys(args).length > 0 && (
            <div className="px-4 py-3 bg-muted/20 border-b border-border/30">
              <div className="text-xs uppercase tracking-widest font-semibold text-muted-foreground/50 mb-2">Arguments</div>
              <div className="space-y-1">
                {Object.entries(args).map(([key, val]) => (
                  <div key={key} className="flex gap-2 text-base">
                    <span className="font-mono text-primary/70 shrink-0">{key}:</span>
                    <span className="text-muted-foreground break-all">{typeof val === "string" ? val : JSON.stringify(val)}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Result */}
          {result && (
            <div className="px-4 py-3">
              <div className="text-xs uppercase tracking-widest font-semibold text-muted-foreground/50 mb-2">Result</div>
              <ToolResultRenderer toolName={toolName} result={result} />
            </div>
          )}
        </div>
      )}
    </div>
  )
}
