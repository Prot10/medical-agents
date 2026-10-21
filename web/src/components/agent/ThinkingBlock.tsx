import { useState } from "react"
import { Sparkles, ChevronRight } from "lucide-react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { cn } from "@/lib/utils"

/** Collapsible block for the model's visible rationale (the ReAct ablation records one per turn). */
export function ThinkingBlock({
  content,
  turnNumber,
  label = "Reasoning",
}: {
  content: string
  turnNumber: number
  label?: string
}) {
  const [expanded, setExpanded] = useState(true)

  if (!content.trim()) return null

  return (
    <div className={cn(
      "relative rounded-xl border overflow-hidden transition-all border-thinking/15",
      "bg-gradient-to-br from-thinking/[0.05] to-transparent",
    )}>
      {/* Left accent */}
      <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-thinking/50 to-thinking/10 rounded-l" />

      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-2 px-4 py-2 hover:bg-thinking/[0.04] transition-colors"
      >
        <ChevronRight className={cn(
          "h-3.5 w-3.5 text-thinking/50 transition-transform duration-200",
          expanded && "rotate-90",
        )} />
        <Sparkles className="h-3.5 w-3.5 text-thinking/60" />
        <span className="text-sm font-semibold tracking-wide text-thinking/60 uppercase">
          {label}
        </span>
        <span className="text-sm text-muted-foreground/50 ml-auto font-mono bg-muted/50 px-1.5 py-0.5 rounded">t{turnNumber}</span>
      </button>

      {expanded && (
        <div className="px-4 pb-3 text-base leading-relaxed prose text-foreground/60">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
        </div>
      )}
    </div>
  )
}
