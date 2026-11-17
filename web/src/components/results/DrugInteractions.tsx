import { cn } from "@/lib/utils"
import { AlertTriangle, Shield } from "lucide-react"
import { Badge } from "@/components/ui/Badge"

interface Interaction {
  drug: string
  severity: string
  description: string
  mechanism?: string
}

export function DrugInteractions({ data }: { data: Record<string, unknown> }) {
  const proposed = data.proposed as string | undefined
  const interactions = (data.interactions ?? []) as Interaction[]
  const contraindications = (data.contraindications ?? []) as string[]
  const alternatives = (data.alternatives ?? []) as Array<{ drug: string; rationale?: string }> | string[]

  const severityColors: Record<string, string> = {
    major: "bg-red-500/10 text-red-500 border-red-500/30",
    moderate: "bg-amber-500/10 text-amber-600 dark:text-amber-400 border-amber-500/30",
    minor: "bg-blue-500/10 text-blue-500 border-blue-500/30",
  }

  return (
    <div className="space-y-3">
      {proposed && (
        <div className="text-base">
          <span className="font-medium">Proposed: </span>
          <span className="font-mono text-orange-500 dark:text-orange-400">{proposed}</span>
        </div>
      )}

      {interactions.length > 0 && (
        <div className="space-y-2">
          {interactions.map((ix, i) => (
            <div
              key={i}
              className={cn(
                "rounded-lg border p-3 text-base",
                severityColors[ix.severity?.toLowerCase()] ?? "border-border",
              )}
            >
              <div className="flex items-center gap-2">
                <AlertTriangle className="h-3.5 w-3.5 shrink-0" />
                <span className="font-semibold">{ix.drug}</span>
                <Badge variant={ix.severity?.toLowerCase() === "major" ? "destructive" : "warning"} className="ml-auto text-xs">
                  {ix.severity}
                </Badge>
              </div>
              <p className="text-base mt-1.5 opacity-80">{ix.description}</p>
            </div>
          ))}
        </div>
      )}

      {contraindications.length > 0 && (
        <div>
          <div className="text-sm font-semibold text-red-500 mb-1.5">Contraindications</div>
          <ul className="space-y-1">
            {contraindications.map((c, i) => (
              <li key={i} className="flex items-start gap-2 text-base text-red-400">
                <span className="mt-1.5 h-2 w-2 rounded-full bg-red-500 shrink-0" />
                {c}
              </li>
            ))}
          </ul>
        </div>
      )}

      {alternatives.length > 0 && (
        <div>
          <div className="flex items-center gap-1.5 text-sm font-semibold text-emerald-600 dark:text-emerald-400 mb-1.5">
            <Shield className="h-3.5 w-3.5" />
            Alternatives
          </div>
          <div className="flex flex-wrap gap-1.5">
            {alternatives.map((a, i) => {
              const name = typeof a === "string" ? a : a.drug
              return (
                <Badge key={i} variant="success">{name}</Badge>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
