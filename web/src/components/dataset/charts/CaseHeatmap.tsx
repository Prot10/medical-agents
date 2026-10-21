import { cn } from "@/lib/utils"
import { DifficultyStars } from "@/components/ui/DifficultyStars"

interface Props {
  data: Array<{
    condition: string
    straightforward: number
    moderate: number
    diagnostic_puzzle: number
  }>
}

const DIFF_COLORS = {
  straightforward: { bg: "bg-emerald-500", text: "text-emerald-50" },
  moderate: { bg: "bg-amber-500", text: "text-amber-50" },
  diagnostic_puzzle: { bg: "bg-red-500", text: "text-red-50" },
}

export function CaseHeatmap({ data }: Props) {
  const maxVal = Math.max(
    ...data.flatMap((d) => [d.straightforward, d.moderate, d.diagnostic_puzzle]),
  )

  return (
    <div className="space-y-1">
      {/* Column headers */}
      <div className="grid grid-cols-[1fr_60px_60px_60px] gap-1 px-1 pb-1">
        <span />
        <span className="flex justify-center"><DifficultyStars difficulty="straightforward" /></span>
        <span className="flex justify-center"><DifficultyStars difficulty="moderate" /></span>
        <span className="flex justify-center"><DifficultyStars difficulty="diagnostic_puzzle" /></span>
      </div>

      {data.map((row) => (
        <div key={row.condition} className="grid grid-cols-[1fr_60px_60px_60px] gap-1 items-center">
          <span className="text-sm truncate pr-2">{row.condition}</span>
          {(["straightforward", "moderate", "diagnostic_puzzle"] as const).map((diff) => {
            const val = row[diff]
            const opacity = maxVal > 0 ? 0.15 + (val / maxVal) * 0.85 : 0
            const colors = DIFF_COLORS[diff]
            return (
              <div
                key={diff}
                className={cn(
                  "h-8 rounded-md flex items-center justify-center text-sm font-bold transition-all",
                  val > 0 ? colors.bg : "bg-muted",
                  val > 0 ? colors.text : "text-muted-foreground/30",
                )}
                style={{ opacity: val > 0 ? opacity : 0.3 }}
              >
                {val > 0 ? val : "-"}
              </div>
            )
          })}
        </div>
      ))}
    </div>
  )
}
