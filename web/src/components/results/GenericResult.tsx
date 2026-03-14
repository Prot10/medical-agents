import { useState } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

interface Props {
  data: Record<string, unknown>
}

export function GenericResult({ data }: Props) {
  const [showRaw, setShowRaw] = useState(false)

  // Try to render human-readable fields first
  const impression = extractString(data, "impression", "clinical_correlation", "summary", "interpretation")
  const findings = data.findings as unknown[] | undefined

  return (
    <div className="space-y-1.5">
      {/* Key metrics (if any top-level string/number fields) */}
      {renderKeyMetrics(data)}

      {/* Findings list */}
      {Array.isArray(findings) && findings.length > 0 && (
        <div className="space-y-1">
          {findings.map((f, i) => (
            <div key={i} className="text-xs border border-border/50 rounded p-1.5">
              {typeof f === "string" ? f : renderObject(f as Record<string, unknown>)}
            </div>
          ))}
        </div>
      )}

      {/* Impression */}
      {impression && (
        <div className="text-xs italic text-muted-foreground border-l-2 border-border pl-2">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{impression}</ReactMarkdown>
        </div>
      )}

      {/* Raw toggle */}
      <button
        onClick={() => setShowRaw(!showRaw)}
        className="text-[9px] text-muted-foreground hover:text-foreground transition-colors"
      >
        {showRaw ? "Hide" : "Show"} raw JSON
      </button>
      {showRaw && (
        <pre className="text-[10px] font-mono text-muted-foreground whitespace-pre-wrap break-words max-h-48 overflow-y-auto bg-secondary/50 rounded p-2">
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
    <div className="grid grid-cols-2 gap-x-3 gap-y-0.5 text-[11px]">
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
    <div className="text-[11px] space-y-0.5">
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
