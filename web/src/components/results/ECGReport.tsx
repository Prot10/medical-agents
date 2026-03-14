import { cn } from "@/lib/utils"

export function ECGReport({ data }: { data: Record<string, unknown> }) {
  const rhythm = data.rhythm as string | undefined
  const rate = data.rate as number | string | undefined
  const axis = data.axis as string | undefined
  const intervals = data.intervals as Record<string, string | number> | undefined
  const findings = data.findings as Array<{ finding: string; severity?: string; location?: string }> | string[] | undefined
  const interpretation = data.interpretation as string | undefined
  const clinicalCorrelation = data.clinical_correlation as string | undefined

  return (
    <div className="space-y-2">
      {/* Top-line metrics */}
      <div className="flex gap-3">
        {rhythm && (
          <MetricBadge label="Rhythm" value={rhythm} />
        )}
        {rate && (
          <MetricBadge label="Rate" value={`${rate} bpm`} />
        )}
        {axis && (
          <MetricBadge label="Axis" value={axis} />
        )}
      </div>

      {/* Intervals */}
      {intervals && Object.keys(intervals).length > 0 && (
        <div className="grid grid-cols-3 gap-1">
          {Object.entries(intervals).map(([name, val]) => (
            <div key={name} className="text-[10px]">
              <span className="font-mono font-medium text-foreground/70">{name}:</span>{" "}
              <span className="text-muted-foreground">{val}</span>
            </div>
          ))}
        </div>
      )}

      {/* Findings */}
      {findings && (findings as unknown[]).length > 0 && (
        <div>
          <div className="text-[10px] font-semibold text-muted-foreground mb-0.5">Findings</div>
          <ul className="space-y-0.5">
            {(findings as unknown[]).map((f, i) => {
              const text = typeof f === "string" ? f : (f as Record<string, string>).finding
              const severity = typeof f === "object" ? (f as Record<string, string>).severity : undefined
              return (
                <li key={i} className="flex items-start gap-1.5 text-[11px]">
                  <span className={cn(
                    "mt-1.5 h-1.5 w-1.5 rounded-full shrink-0",
                    severity === "critical" ? "bg-red-500" :
                    severity === "significant" ? "bg-amber-500" : "bg-muted-foreground/40",
                  )} />
                  <span className="text-muted-foreground">{text}</span>
                </li>
              )
            })}
          </ul>
        </div>
      )}

      {interpretation && (
        <div className="text-[11px] leading-relaxed">
          <span className="font-semibold text-foreground/80">Interpretation: </span>
          <span className="text-muted-foreground">{interpretation}</span>
        </div>
      )}

      {clinicalCorrelation && (
        <div className="text-[10px] text-muted-foreground/80 italic border-l-2 border-border pl-2">
          {clinicalCorrelation}
        </div>
      )}
    </div>
  )
}

function MetricBadge({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-md bg-muted/60 px-2 py-1">
      <div className="text-[9px] uppercase tracking-wider text-muted-foreground">{label}</div>
      <div className="text-[11px] font-medium">{value}</div>
    </div>
  )
}
