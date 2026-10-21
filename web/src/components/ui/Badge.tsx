import { cn } from "@/lib/utils"

const variants = {
  default: "bg-secondary text-secondary-foreground",
  outline: "border border-border text-muted-foreground",
  success: "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400",
  warning: "bg-amber-500/10 text-amber-600 dark:text-amber-400",
  destructive: "bg-red-500/10 text-red-500",
  info: "bg-sky-500/10 text-sky-600 dark:text-sky-400",
} as const

export function Badge({
  children,
  variant = "default",
  className,
}: {
  children: React.ReactNode
  variant?: keyof typeof variants
  className?: string
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center text-sm px-2 py-0.5 rounded-full font-medium",
        variants[variant],
        className,
      )}
    >
      {children}
    </span>
  )
}
