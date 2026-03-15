import { Shield, CheckCircle2 } from "lucide-react"
import { Streamdown } from "streamdown"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { cn } from "@/lib/utils"

export function AssessmentPanel({
  content,
  streaming = false,
}: {
  content: string
  streaming?: boolean
}) {
  return (
    <div className={cn(
      "relative rounded-xl border-2 border-assessment/30 overflow-hidden",
      !streaming && "success-pulse",
    )}>
      {/* Gradient header */}
      <div className="flex items-center gap-2.5 px-4 py-3 bg-gradient-to-r from-assessment/15 via-assessment/10 to-transparent border-b border-assessment/15">
        <div className="h-8 w-8 rounded-lg bg-assessment/15 flex items-center justify-center">
          <Shield className="h-4.5 w-4.5 text-assessment" />
        </div>
        <div>
          <span className="text-base font-bold tracking-tight text-assessment">Final Assessment</span>
        </div>
        {streaming ? (
          <span className="relative flex h-2 w-2 ml-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-assessment/60 opacity-75" />
            <span className="relative inline-flex rounded-full h-2 w-2 bg-assessment/80" />
          </span>
        ) : (
          <CheckCircle2 className="h-4.5 w-4.5 text-assessment/60 ml-auto" />
        )}
      </div>

      {/* Content */}
      <div className="px-5 py-4 text-base leading-relaxed prose">
        {streaming ? (
          <Streamdown>{content}</Streamdown>
        ) : (
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
        )}
      </div>
    </div>
  )
}
