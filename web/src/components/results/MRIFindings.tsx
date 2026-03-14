import { cn } from "@/lib/utils"

interface Finding {
  type: string
  location: string
  size?: string
  signal_characteristics?: Record<string, string>
  mass_effect?: string
  borders?: string
}

export function MRIFindings({ data }: { data: Record<string, unknown> }) {
  const findings = (data.findings ?? []) as Finding[]
  const impression = data.impression as string | undefined
  const differential = data.differential_by_imaging as Array<{ diagnosis: string; likelihood: string }> | undefined
  const confidence = data.confidence as number | string | undefined

  return (
    <div className="space-y-2">
      {findings.map((f, i) => (
        <div key={i} className="rounded-md border border-border/50 p-2.5">
          <div className="flex items-start gap-2 mb-1.5">
            <span className="text-[10px] font-semibold uppercase tracking-wider text-purple-500 dark:text-purple-400">
              {f.type}
            </span>
            <span className="text-[10px] text-muted-foreground">{f.location}</span>
            {f.size && (
              <span className="text-[10px] text-muted-foreground ml-auto font-mono">{f.size}</span>
            )}
          </div>

          {f.signal_characteristics && (
            <div className="grid grid-cols-2 gap-x-3 gap-y-0.5 mt-1">
              {Object.entries(f.signal_characteristics).map(([seq, signal]) => (
                <div key={seq} className="text-[10px]">
                  <span className="font-mono font-medium text-foreground/70">{seq}:</span>{" "}
                  <span className="text-muted-foreground">{signal}</span>
                </div>
              ))}
            </div>
          )}

          {f.mass_effect && (
            <div className="text-[10px] text-muted-foreground mt-1">
              Mass effect: {f.mass_effect}
            </div>
          )}
        </div>
      ))}

      {impression && (
        <div className="text-[11px] leading-relaxed">
          <span className="font-semibold text-foreground/80">Impression: </span>
          <span className="text-muted-foreground">{impression}</span>
        </div>
      )}

      {differential && differential.length > 0 && (
        <div>
          <div className="text-[10px] font-semibold text-muted-foreground mb-0.5">Imaging Differential</div>
          <div className="flex flex-wrap gap-1">
            {differential.map((d, i) => (
              <span
                key={i}
                className={cn(
                  "text-[10px] px-1.5 py-0.5 rounded-full border",
                  d.likelihood === "high"
                    ? "border-purple-500/30 bg-purple-500/10 text-purple-600 dark:text-purple-400"
                    : "border-border text-muted-foreground",
                )}
              >
                {d.diagnosis}
              </span>
            ))}
          </div>
        </div>
      )}

      {confidence && (
        <div className="text-[10px] text-muted-foreground">
          Confidence: {typeof confidence === "number" ? `${(confidence * 100).toFixed(0)}%` : confidence}
        </div>
      )}
    </div>
  )
}
