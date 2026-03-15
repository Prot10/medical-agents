import { Badge } from "@/components/ui/Badge"

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
    <div className="space-y-3">
      {classification && (
        <div className="flex items-center gap-2">
          <Badge variant={classification === "normal" ? "success" : "warning"} className="uppercase text-xs font-bold">
            {classification}
          </Badge>
          {confidence && (
            <span className="text-sm text-muted-foreground ml-auto">
              Confidence: {typeof confidence === "number" ? `${(confidence * 100).toFixed(0)}%` : confidence}
            </span>
          )}
        </div>
      )}

      {background && (
        <div className="text-base">
          <span className="font-medium text-foreground/80">Background: </span>
          <span className="text-muted-foreground">
            {typeof background === "string" ? background : JSON.stringify(background)}
          </span>
        </div>
      )}

      {findings.length > 0 && (
        <div className="space-y-2">
          {findings.map((f, i) => (
            <div key={i} className="rounded-lg border border-border/50 p-3">
              <div className="flex items-center gap-2 text-base">
                <Badge variant="info" className="text-xs">{f.type}</Badge>
                <span className="text-muted-foreground">{f.location}</span>
              </div>
              <div className="flex gap-4 mt-1.5 text-sm text-muted-foreground">
                {f.frequency && <span>Freq: <span className="font-mono">{f.frequency}</span></span>}
                {f.morphology && <span>Morph: {f.morphology}</span>}
                {f.state && <span>State: {f.state}</span>}
              </div>
              {f.clinical_correlation && (
                <div className="text-sm text-muted-foreground/70 mt-1.5 italic">
                  {f.clinical_correlation}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {impression && (
        <div className="text-base leading-relaxed">
          <span className="font-semibold text-foreground/80">Impression: </span>
          <span className="text-muted-foreground">{impression}</span>
        </div>
      )}
    </div>
  )
}
