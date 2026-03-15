import { Star } from "lucide-react"
import { cn } from "@/lib/utils"

const DIFFICULTY_CONFIG = {
  straightforward: { filled: 1, color: "text-emerald-500", fill: "fill-emerald-500", border: "text-emerald-500/40" },
  moderate: { filled: 2, color: "text-amber-500", fill: "fill-amber-500", border: "text-amber-500/40" },
  diagnostic_puzzle: { filled: 3, color: "text-red-500", fill: "fill-red-500", border: "text-red-500" },
} as const

export function DifficultyStars({ difficulty, size = "sm" }: { difficulty: string; size?: "sm" | "md" }) {
  const config = DIFFICULTY_CONFIG[difficulty as keyof typeof DIFFICULTY_CONFIG]
  if (!config) return <span className="text-sm text-muted-foreground">{difficulty}</span>

  const iconSize = size === "sm" ? "h-3 w-3" : "h-3.5 w-3.5"

  return (
    <div className="inline-flex items-center gap-0.5" title={difficulty.replace(/_/g, " ")}>
      {[0, 1, 2].map((i) => (
        <Star
          key={i}
          className={cn(
            iconSize,
            i < config.filled
              ? cn(config.color, config.fill)
              : config.border,
          )}
        />
      ))}
    </div>
  )
}
