import { cn } from "@/lib/utils"

export function IconButton({
  children,
  onClick,
  className,
  title,
  disabled,
  variant = "ghost",
}: {
  children: React.ReactNode
  onClick?: () => void
  className?: string
  title?: string
  disabled?: boolean
  variant?: "ghost" | "primary" | "destructive"
}) {
  const variants = {
    ghost: "text-muted-foreground hover:text-foreground hover:bg-accent",
    primary: "text-primary hover:bg-primary/10",
    destructive: "text-red-500 hover:bg-red-500/10",
  }

  return (
    <button
      onClick={onClick}
      disabled={disabled}
      title={title}
      className={cn(
        "p-2 rounded-lg transition-colors disabled:opacity-50 disabled:pointer-events-none",
        variants[variant],
        className,
      )}
    >
      {children}
    </button>
  )
}
