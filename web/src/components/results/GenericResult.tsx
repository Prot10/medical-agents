import { useState } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

interface Props {
  data: Record<string, unknown>
}

export function GenericResult({ data }: Props) {
  const [showRaw, setShowRaw] = useState(false)

  const impression = extractString(data, "impression", "clinical_correlation", "summary", "interpretation")
  const findings = data.findings as unknown[] | undefined

  return (
    <div className="space-y-2">
      {renderKeyMetrics(data)}

      {Array.isArray(findings) && findings.length > 0 && (
        <div className="space-y-1.5">
          {findings.map((f, i) => (
            <div key={i} className="text-base border border-border/50 rounded-lg p-2.5">
              {typeof f === "string" ? f : renderObject(f as Record<string, unknown>)}
            </div>
          ))}
        </div>
      )}

      {impression && (
        <div className="text-base italic text-muted-foreground border-l-2 border-border pl-3">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{impression}</ReactMarkdown>
        </div>
      )}

      <button
        onClick={() => setShowRaw(!showRaw)}
        className="text-sm text-muted-foreground hover:text-foreground transition-colors"
      >
        {showRaw ? "Hide" : "Show"} raw JSON
      </button>
      {showRaw && (
        <pre className="text-sm font-mono text-muted-foreground whitespace-pre-wrap break-words max-h-48 overflow-y-auto bg-secondary/50 rounded-lg p-3">
          {JSON.stringify(data, null, 2)}
        </pre>
      )}
    </div>
  )
}

function extractString(data: Record<string, unknown>, ...keys: string[]): string | null {
  for (const key of keys) {
    if (typeof data[key] === "string") return data[key] as string
  }
  return null
}

function renderKeyMetrics(data: Record<string, unknown>) {
  const metrics = Object.entries(data).filter(
    ([k, v]) => (typeof v === "string" || typeof v === "number") && !["success", "tool_name", "error_message"].includes(k)
  )

  if (metrics.length === 0) return null

  return (
    <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-base">
      {metrics.slice(0, 10).map(([k, v]) => (
        <div key={k}>
          <span className="font-medium capitalize">{k.replace(/_/g, " ")}:</span>{" "}
          <span className="text-muted-foreground">{String(v)}</span>
        </div>
      ))}
    </div>
  )
}

function renderObject(obj: Record<string, unknown>) {
  return (
    <div className="text-base space-y-0.5">
      {Object.entries(obj).map(([k, v]) => (
        <div key={k}>
          <span className="font-medium capitalize">{k.replace(/_/g, " ")}:</span>{" "}
          <span className="text-muted-foreground">
            {typeof v === "object" ? JSON.stringify(v) : String(v)}
          </span>
        </div>
      ))}
    </div>
  )
}
