import { useState } from "react"
import { ChevronDown, ChevronRight, AlertCircle } from "lucide-react"
import { cn } from "@/lib/utils"

interface LabTest {
  test: string
  value: number | string
  unit: string
  reference_range: string
  is_abnormal: boolean
  clinical_significance?: string
}

export function LabResultsTable({ data }: { data: Record<string, unknown> }) {
  const panels = (data.panels ?? {}) as Record<string, LabTest[]>
  const interpretation = data.interpretation as string | undefined
  const [openPanels, setOpenPanels] = useState<Record<string, boolean>>(() => {
    const initial: Record<string, boolean> = {}
    for (const [name, tests] of Object.entries(panels)) {
      if (Array.isArray(tests) && tests.some((t) => t.is_abnormal)) {
        initial[name] = true
      }
    }
    return initial
  })

  const toggle = (name: string) =>
    setOpenPanels((s) => ({ ...s, [name]: !s[name] }))

  return (
    <div className="space-y-2">
      {Object.entries(panels).map(([panelName, tests]) => {
        if (!Array.isArray(tests)) return null
        const isOpen = openPanels[panelName]
        const abnormalCount = tests.filter((t) => t.is_abnormal).length

        return (
          <div key={panelName} className="rounded-lg border border-border/60 overflow-hidden">
            <button
              onClick={() => toggle(panelName)}
              className="w-full flex items-center gap-2 px-3 py-2 text-base hover:bg-accent/50 transition-colors"
            >
              {isOpen
                ? <ChevronDown className="h-3.5 w-3.5 text-muted-foreground" />
                : <ChevronRight className="h-3.5 w-3.5 text-muted-foreground" />}
              <span className="font-medium">{panelName}</span>
              {abnormalCount > 0 && (
                <span className="flex items-center gap-1 text-sm px-2 py-0.5 rounded-full bg-red-500/10 text-red-500 font-medium">
                  <AlertCircle className="h-3 w-3" />
                  {abnormalCount}
                </span>
              )}
              <span className="text-sm text-muted-foreground ml-auto">
                {tests.length} tests
              </span>
            </button>

            {isOpen && (
              <table className="w-full text-base">
                <thead>
                  <tr className="bg-muted/50 text-muted-foreground">
                    <th className="text-left px-3 py-1.5 font-medium text-sm">Test</th>
                    <th className="text-right px-3 py-1.5 font-medium text-sm">Value</th>
                    <th className="text-left px-3 py-1.5 font-medium text-sm">Reference</th>
                  </tr>
                </thead>
                <tbody>
                  {tests.map((t, i) => (
                    <tr
                      key={i}
                      className={cn(
                        "border-t border-border/30",
                        t.is_abnormal && "bg-red-500/[0.04] border-l-2 border-l-red-500",
                      )}
                    >
                      <td className="px-3 py-1.5">
                        <span className={cn(t.is_abnormal && "font-semibold text-red-500 dark:text-red-400")}>
                          {t.test}
                        </span>
                      </td>
                      <td className={cn(
                        "text-right px-3 py-1.5 font-mono",
                        t.is_abnormal ? "font-bold text-red-500 dark:text-red-400" : "text-muted-foreground",
                      )}>
                        {t.value} <span className="text-muted-foreground/60 text-sm">{t.unit}</span>
                      </td>
                      <td className="px-3 py-1.5 text-muted-foreground text-sm">
                        {t.reference_range}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )
      })}

      {interpretation && (
        <div className="text-base text-muted-foreground leading-relaxed px-1 pt-1">
          {interpretation}
        </div>
      )}
    </div>
  )
}
