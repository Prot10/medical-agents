import * as React from "react"

import { cn } from "@/lib/utils"

export const Card = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & {
    accent?: "primary" | "success" | "warning" | "destructive"
    hover?: boolean
  }
>(({ className, accent, hover = false, ...props }, ref) => {
  const accentBorder = accent
    ? {
        primary: "border-l-4 border-l-primary",
        success: "border-l-4 border-l-emerald-500",
        warning: "border-l-4 border-l-amber-500",
        destructive: "border-l-4 border-l-rose-500",
      }[accent]
    : ""
  return (
    <div
      ref={ref}
      className={cn(
        "bg-card text-card-foreground rounded-xl border border-border",
        accentBorder,
        hover && "transition-shadow hover:shadow-md",
        className,
      )}
      {...props}
    />
  )
})
Card.displayName = "Card"

export const CardHeader = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div
    className={cn("px-5 py-4 border-b border-border", className)}
    {...props}
  />
)

export const CardTitle = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLHeadingElement>) => (
  <h3
    className={cn("text-base font-semibold tracking-tight", className)}
    {...props}
  />
)

export const CardBody = ({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={cn("px-5 py-4", className)} {...props} />
)
