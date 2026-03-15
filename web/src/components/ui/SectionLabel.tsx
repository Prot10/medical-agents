import { cn } from "@/lib/utils"

export function SectionLabel({
  children,
  icon: Icon,
  className,
}: {
  children: React.ReactNode
  icon?: React.ElementType
  className?: string
}) {
  return (
    <div className={cn("flex items-center gap-1.5 text-sm uppercase tracking-wider font-semibold text-muted-foreground mb-2", className)}>
      {Icon && <Icon className="h-3.5 w-3.5" />}
      {children}
    </div>
  )
}
