import * as React from "react"

import { cn } from "@/lib/utils"

const variants = {
  default: "bg-secondary text-secondary-foreground",
  outline: "border border-border text-muted-foreground",
  success:
    "bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/30",
  warning:
    "bg-amber-500/10 text-amber-600 dark:text-amber-400 border border-amber-500/30",
  destructive:
    "bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/30",
  info:
    "bg-sky-500/10 text-sky-600 dark:text-sky-400 border border-sky-500/30",
  primary:
    "bg-primary/10 text-primary border border-primary/30",
} as const

export type BadgeVariant = keyof typeof variants

export function Badge({
  children,
  variant = "default",
  className,
  ...rest
}: {
  children: React.ReactNode
  variant?: BadgeVariant
  className?: string
} & React.HTMLAttributes<HTMLSpanElement>) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium",
        variants[variant],
        className,
      )}
      {...rest}
    >
      {children}
    </span>
  )
}
