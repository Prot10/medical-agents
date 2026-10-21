import { cn } from "@/lib/utils"

export function Card({
  children,
  className,
  accent,
  hover,
}: {
  children: React.ReactNode
  className?: string
  accent?: "primary" | "success" | "warning" | "destructive"
  hover?: boolean
}) {
  const accentColors = {
    primary: "border-l-primary",
    success: "border-l-emerald-500",
    warning: "border-l-amber-500",
    destructive: "border-l-red-500",
  }

  return (
    <div
      className={cn(
        "rounded-xl border border-border bg-card p-4",
        accent && `border-l-[3px] ${accentColors[accent]}`,
        hover && "transition-all duration-150 hover:shadow-md hover:shadow-primary/5 hover:border-primary/30",
        className,
      )}
    >
      {children}
    </div>
  )
}

export function CardHeader({ children, className }: { children: React.ReactNode; className?: string }) {
  return <div className={cn("mb-3", className)}>{children}</div>
}

export function CardTitle({ children, className }: { children: React.ReactNode; className?: string }) {
  return <h3 className={cn("text-base font-semibold tracking-tight", className)}>{children}</h3>
}
