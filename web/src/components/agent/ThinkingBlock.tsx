import { Sparkles } from "lucide-react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

export function ThinkingBlock({ content, turnNumber }: { content: string; turnNumber: number }) {
  if (!content.trim()) return null

  return (
    <div className="relative rounded-lg border border-thinking/15 bg-gradient-to-br from-thinking/[0.04] to-transparent overflow-hidden">
      {/* Decorative left accent */}
      <div className="absolute left-0 top-0 bottom-0 w-[2px] bg-gradient-to-b from-thinking/60 to-thinking/10" />

      <div className="flex items-center gap-1.5 px-3 py-1.5">
        <Sparkles className="h-3 w-3 text-thinking/70" />
        <span className="text-[10px] font-medium tracking-wide text-thinking/70 uppercase">Reasoning</span>
        <span className="text-[9px] text-muted-foreground/50 ml-auto font-mono">t{turnNumber}</span>
      </div>
      <div className="px-3 pb-2.5 text-[11.5px] leading-[1.6] prose text-foreground/75">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      </div>
    </div>
  )
}
