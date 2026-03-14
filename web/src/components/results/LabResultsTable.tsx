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
    // Auto-open panels that have abnormal values
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
    <div className="space-y-1.5">
      {Object.entries(panels).map(([panelName, tests]) => {
        if (!Array.isArray(tests)) return null
        const isOpen = openPanels[panelName]
        const abnormalCount = tests.filter((t) => t.is_abnormal).length

        return (
          <div key={panelName} className="rounded-md border border-border/60 overflow-hidden">
            <button
              onClick={() => toggle(panelName)}
              className="w-full flex items-center gap-2 px-2.5 py-1.5 text-xs hover:bg-accent/50 transition-colors"
            >
              {isOpen
                ? <ChevronDown className="h-3 w-3 text-muted-foreground" />
                : <ChevronRight className="h-3 w-3 text-muted-foreground" />}
              <span className="font-medium">{panelName}</span>
              {abnormalCount > 0 && (
                <span className="flex items-center gap-0.5 text-[9px] px-1.5 py-0.5 rounded-full bg-red-500/10 text-red-500">
                  <AlertCircle className="h-2.5 w-2.5" />
                  {abnormalCount}
                </span>
              )}
              <span className="text-[10px] text-muted-foreground ml-auto">
                {tests.length} tests
              </span>
            </button>

            {isOpen && (
              <table className="w-full text-[11px]">
                <thead>
                  <tr className="bg-muted/50 text-muted-foreground">
                    <th className="text-left px-2.5 py-1 font-medium">Test</th>
                    <th className="text-right px-2.5 py-1 font-medium">Value</th>
                    <th className="text-left px-2.5 py-1 font-medium">Ref</th>
                  </tr>
                </thead>
                <tbody>
                  {tests.map((t, i) => (
                    <tr
                      key={i}
                      className={cn(
                        "border-t border-border/30",
                        t.is_abnormal && "bg-red-500/[0.04]",
                      )}
                    >
                      <td className="px-2.5 py-1">
                        <span className={cn(t.is_abnormal && "font-medium text-red-500 dark:text-red-400")}>
                          {t.test}
                        </span>
                      </td>
                      <td className={cn(
                        "text-right px-2.5 py-1 font-mono",
                        t.is_abnormal ? "font-semibold text-red-500 dark:text-red-400" : "text-muted-foreground",
                      )}>
                        {t.value} {t.unit}
                      </td>
                      <td className="px-2.5 py-1 text-muted-foreground">
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
        <div className="text-[11px] text-muted-foreground leading-relaxed px-1 pt-1">
          {interpretation}
        </div>
      )}
    </div>
  )
}
