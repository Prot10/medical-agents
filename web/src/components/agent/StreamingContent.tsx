import { useState, useEffect } from "react"
import { MessageSquare, ChevronRight, ChevronDown } from "lucide-react"
import { Streamdown } from "streamdown"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { cn } from "@/lib/utils"

export function StreamingContent({
  content,
  turnNumber,
  streaming = false,
  collapsed = false,
}: {
  content: string
  turnNumber: number
  streaming?: boolean
  collapsed?: boolean
}) {
  const [expanded, setExpanded] = useState(!collapsed)

  // Sync with collapsed prop — when parent signals collapse, close it
  useEffect(() => {
    if (collapsed) setExpanded(false)
  }, [collapsed])

  if (!content.trim()) return null

  return (
    <div className={cn(
      "rounded-xl border overflow-hidden transition-all duration-200",
      streaming ? "border-primary/30" : "border-border",
    )}>
      {/* Header — matches ToolCallCard layout */}
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

        {/* Icon badge */}
        <div className="h-8 w-8 rounded-lg flex items-center justify-center shrink-0 bg-primary/15">
          <MessageSquare className="h-4 w-4 text-primary" />
        </div>

        {/* Label + collapsed preview */}
        <div className="flex-1 text-left min-w-0">
          <span className="text-base font-semibold">Agent Reasoning</span>
          {!expanded && content && (
            <div className="text-sm text-muted-foreground/60 truncate mt-0.5">
              {content.slice(0, 100)}{content.length > 100 ? "..." : ""}
            </div>
          )}
        </div>

        {/* Status badge */}
        <span className="shrink-0">
          {streaming ? (
            <span className="flex items-center gap-1.5 text-sm font-medium text-primary px-2 py-0.5 rounded-full bg-primary/10">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary" />
              </span>
              Streaming
            </span>
          ) : (
            <span className="flex items-center gap-1 text-sm font-medium text-muted-foreground/50 px-2 py-0.5 rounded-full bg-muted/50 font-mono">
              t{turnNumber}
            </span>
          )}
        </span>
      </button>

      {/* Expanded content */}
      {expanded && (
        <div className="border-t border-border/40 animate-fade-in">
          <div className="px-4 py-3 text-base leading-relaxed prose text-foreground/85">
            {streaming ? (
              <Streamdown>{content}</Streamdown>
            ) : (
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
