import { UserCheck } from "lucide-react"

interface Props {
  data: Record<string, unknown>
}

export function SpecialistResult({ data }: Props) {
  const opinion = (data.specialist_opinion as string) ?? ""
  const model = (data.model as string) ?? "specialist"

  // Split opinion into sections based on ### headers
  const sections = opinion.split(/(?=###\s)/).filter(Boolean)

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-purple-500 dark:text-purple-400 text-xs font-medium">
        <UserCheck className="h-3.5 w-3.5" />
        <span>Specialist consultation ({model})</span>
      </div>

      {sections.length > 0 ? (
        <div className="space-y-2">
          {sections.map((section, i) => {
            const lines = section.trim().split("\n")
            const header = lines[0]?.replace(/^###\s*/, "").trim()
            const body = lines.slice(1).join("\n").trim()

            return (
              <div key={i} className="border-l-2 border-purple-500/30 pl-3">
                {header && (
                  <div className="text-xs font-semibold text-purple-600 dark:text-purple-400 mb-1">
                    {header}
                  </div>
                )}
                {body && (
                  <div className="text-sm text-foreground/80 whitespace-pre-wrap leading-relaxed">
                    {body}
                  </div>
                )}
              </div>
            )
          })}
        </div>
      ) : (
        <div className="text-sm text-foreground/80 whitespace-pre-wrap border-l-2 border-purple-500/30 pl-3">
          {opinion || "No specialist opinion available."}
        </div>
      )}
    </div>
  )
}
