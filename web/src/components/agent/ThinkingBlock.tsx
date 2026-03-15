import { useState } from "react"
import { Sparkles, ChevronRight } from "lucide-react"
import { Streamdown } from "streamdown"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { cn } from "@/lib/utils"

export function ThinkingBlock({
  content,
  turnNumber,
  streaming = false,
}: {
  content: string
  turnNumber: number
  streaming?: boolean
}) {
  const [expanded, setExpanded] = useState(streaming)

  if (!content.trim()) return null

  return (
    <div className={cn(
      "relative rounded-xl border overflow-hidden transition-all",
      streaming ? "border-thinking/30 shimmer-border" : "border-thinking/15",
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
          Internal Reasoning
        </span>
        {streaming && (
          <span className="relative flex h-2 w-2 ml-1">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-thinking/60 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-thinking/80" />
          </span>
        )}
        <span className="text-sm text-muted-foreground/50 ml-auto font-mono bg-muted/50 px-1.5 py-0.5 rounded">t{turnNumber}</span>
      </button>

      {expanded && (
        <div className="px-4 pb-3 text-base leading-relaxed prose text-foreground/60">
          {streaming ? (
            <Streamdown>{content}</Streamdown>
          ) : (
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
          )}
        </div>
      )}
    </div>
  )
}
