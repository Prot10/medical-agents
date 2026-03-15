import { MessageSquare } from "lucide-react"
import { Streamdown } from "streamdown"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { cn } from "@/lib/utils"

export function StreamingContent({
  content,
  turnNumber,
  streaming = false,
}: {
  content: string
  turnNumber: number
  streaming?: boolean
}) {
  if (!content.trim()) return null

  return (
    <div className={cn(
      "relative rounded-xl border overflow-hidden",
      streaming ? "border-primary/30" : "border-primary/15",
      "bg-gradient-to-br from-primary/[0.04] to-transparent",
    )}>
      <div className="absolute left-0 top-0 bottom-0 w-[3px] bg-gradient-to-b from-primary/60 to-primary/10 rounded-l" />

      <div className="flex items-center gap-2 px-4 py-2">
        <MessageSquare className="h-3.5 w-3.5 text-primary/60" />
        <span className="text-sm font-semibold tracking-wide text-primary/60 uppercase">
          Agent Reasoning
        </span>
        {streaming && (
          <span className="relative flex h-2 w-2 ml-1">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary/60 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-primary/80" />
          </span>
        )}
        <span className="text-sm text-muted-foreground/50 ml-auto font-mono bg-muted/50 px-1.5 py-0.5 rounded">t{turnNumber}</span>
      </div>
      <div className="px-4 pb-3 text-base leading-relaxed prose text-foreground/85">
        {streaming ? (
          <Streamdown>{content}</Streamdown>
        ) : (
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
        )}
      </div>
    </div>
  )
}
