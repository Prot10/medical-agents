import { cn } from "@/lib/utils"

const LEVEL: Record<string, number> = {
  straightforward: 1,
  moderate: 2,
  diagnostic_puzzle: 3,
}

const LABEL: Record<string, string> = {
  straightforward: "Straightforward",
  moderate: "Moderate",
  diagnostic_puzzle: "Diagnostic puzzle",
}

export function DifficultyStars({
  difficulty,
  className,
}: {
  difficulty: string
  className?: string
}) {
  const level = LEVEL[difficulty] ?? 1
  return (
    <span
      className={cn("inline-flex items-center gap-0.5", className)}
      title={LABEL[difficulty] ?? difficulty}
    >
      {[1, 2, 3].map((i) => (
        <span
          key={i}
          aria-hidden
          className={cn(
            "text-sm leading-none",
            i <= level ? "text-amber-500" : "text-muted-foreground/30",
          )}
        >
          ★
        </span>
      ))}
    </span>
  )
}
