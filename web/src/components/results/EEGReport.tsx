interface EEGFinding {
  type: string
  location: string
  frequency?: string
  morphology?: string
  state?: string
  clinical_correlation?: string
}

export function EEGReport({ data }: { data: Record<string, unknown> }) {
  const classification = data.classification as string | undefined
  const background = data.background as string | Record<string, unknown> | undefined
  const findings = (data.findings ?? []) as EEGFinding[]
  const impression = data.impression as string | undefined
  const confidence = data.confidence as number | string | undefined

  return (
    <div className="space-y-2">
      {classification && (
        <div className="flex items-center gap-2">
          <span className="text-[10px] font-semibold uppercase tracking-wider text-blue-500 dark:text-blue-400">
            {classification}
          </span>
          {confidence && (
            <span className="text-[10px] text-muted-foreground ml-auto">
              Conf: {typeof confidence === "number" ? `${(confidence * 100).toFixed(0)}%` : confidence}
            </span>
          )}
        </div>
      )}

      {background && (
        <div className="text-[11px]">
          <span className="font-medium text-foreground/80">Background: </span>
          <span className="text-muted-foreground">
            {typeof background === "string" ? background : JSON.stringify(background)}
          </span>
        </div>
      )}

      {findings.length > 0 && (
        <div className="space-y-1.5">
          {findings.map((f, i) => (
            <div key={i} className="rounded-md border border-border/50 p-2">
              <div className="flex items-center gap-2 text-[10px]">
                <span className="font-semibold text-blue-500 dark:text-blue-400">{f.type}</span>
                <span className="text-muted-foreground">{f.location}</span>
              </div>
              <div className="flex gap-3 mt-1 text-[10px] text-muted-foreground">
                {f.frequency && <span>Freq: {f.frequency}</span>}
                {f.morphology && <span>Morph: {f.morphology}</span>}
                {f.state && <span>State: {f.state}</span>}
              </div>
              {f.clinical_correlation && (
                <div className="text-[10px] text-muted-foreground/70 mt-1 italic">
                  {f.clinical_correlation}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {impression && (
        <div className="text-[11px] leading-relaxed">
          <span className="font-semibold text-foreground/80">Impression: </span>
          <span className="text-muted-foreground">{impression}</span>
        </div>
      )}
    </div>
  )
}
