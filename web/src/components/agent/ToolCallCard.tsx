import { useState } from "react"
import {
  ChevronRight, ChevronDown, CheckCircle2, XCircle, Loader2,
  Brain, Activity, Heart, FlaskConical, Droplets, BookOpen, Pill,
} from "lucide-react"
import { cn } from "@/lib/utils"
import { ToolResultRenderer } from "@/components/results/ToolResultRenderer"

const TOOL_META: Record<string, { icon: React.ElementType; label: string; accent: string; bg: string }> = {
  analyze_brain_mri: { icon: Brain, label: "Brain MRI", accent: "text-violet-500 dark:text-violet-400", bg: "bg-violet-500" },
  analyze_eeg: { icon: Activity, label: "EEG", accent: "text-blue-500 dark:text-blue-400", bg: "bg-blue-500" },
  analyze_ecg: { icon: Heart, label: "ECG", accent: "text-rose-500 dark:text-rose-400", bg: "bg-rose-500" },
  interpret_labs: { icon: FlaskConical, label: "Labs", accent: "text-emerald-500 dark:text-emerald-400", bg: "bg-emerald-500" },
  analyze_csf: { icon: Droplets, label: "CSF", accent: "text-cyan-500 dark:text-cyan-400", bg: "bg-cyan-500" },
  search_medical_literature: { icon: BookOpen, label: "Literature Search", accent: "text-amber-500 dark:text-amber-400", bg: "bg-amber-500" },
  check_drug_interactions: { icon: Pill, label: "Drug Interactions", accent: "text-orange-500 dark:text-orange-400", bg: "bg-orange-500" },
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
    icon: FlaskConical, label: toolName, accent: "text-muted-foreground", bg: "bg-muted-foreground",
  }
  const Icon = meta.icon

  const argSummary = Object.entries(args)
    .map(([k, v]) => `${k}=${typeof v === "string" ? v : JSON.stringify(v)}`)
    .join(", ")

  return (
    <div className={cn(
      "rounded-lg border overflow-hidden transition-all duration-150",
      pending && "border-tool-call/20 glow-pulse",
      !pending && success && "border-border/60",
      !pending && !success && "border-red-500/30",
    )}>
      {/* Header — click to expand */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-2 px-2.5 py-2 hover:bg-accent/40 transition-colors group"
      >
        {/* Expand chevron */}
        <span className="text-muted-foreground/50 group-hover:text-muted-foreground transition-colors">
          {expanded
            ? <ChevronDown className="h-3 w-3" />
            : <ChevronRight className="h-3 w-3" />}
        </span>

        {/* Tool icon with color dot */}
        <span className="relative">
          <Icon className={cn("h-3.5 w-3.5", meta.accent)} />
        </span>

        {/* Tool name */}
        <span className="text-[11px] font-mono font-medium tracking-tight">{meta.label}</span>

        {/* Collapsed args preview */}
        {!expanded && argSummary && (
          <span className="text-[10px] text-muted-foreground/50 truncate max-w-[180px] font-mono">
            ({argSummary})
          </span>
        )}

        {/* Status icon */}
        <span className="ml-auto shrink-0">
          {pending ? (
            <Loader2 className="h-3.5 w-3.5 text-tool-call animate-spin" />
          ) : success ? (
            <CheckCircle2 className="h-3.5 w-3.5 text-tool-result/70" />
          ) : (
            <XCircle className="h-3.5 w-3.5 text-red-500" />
          )}
        </span>
      </button>

      {/* Expanded content */}
      {expanded && (
        <div className="border-t border-border/40">
          {/* Arguments section */}
          {Object.keys(args).length > 0 && (
            <div className="px-3 py-2 bg-muted/20 border-b border-border/30">
              <div className="text-[9px] uppercase tracking-widest font-semibold text-muted-foreground/50 mb-1">Args</div>
              <pre className="text-[10px] font-mono text-muted-foreground/80 whitespace-pre-wrap break-words leading-relaxed">
                {JSON.stringify(args, null, 2)}
              </pre>
            </div>
          )}

          {/* Result section */}
          {result && (
            <div className="px-3 py-2.5">
              <div className="text-[9px] uppercase tracking-widest font-semibold text-muted-foreground/50 mb-1.5">Result</div>
              <ToolResultRenderer toolName={toolName} result={result} />
            </div>
          )}
        </div>
      )}
    </div>
  )
}
