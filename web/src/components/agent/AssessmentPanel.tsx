import { Shield } from "lucide-react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

export function AssessmentPanel({ content }: { content: string }) {
  return (
    <div className="relative rounded-lg border-2 border-assessment/25 overflow-hidden">
      {/* Gradient header bar */}
      <div className="flex items-center gap-2 px-3 py-2 bg-gradient-to-r from-assessment/15 to-assessment/5 border-b border-assessment/15">
        <Shield className="h-4 w-4 text-assessment" />
        <span className="text-xs font-semibold tracking-tight text-assessment">Final Assessment</span>
      </div>

      {/* Content */}
      <div className="px-4 py-3 text-[12px] leading-[1.65] prose">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{content}</ReactMarkdown>
      </div>
    </div>
  )
}
