import { AlertTriangle, RotateCw } from "lucide-react"
import { cn } from "@/lib/utils"

/**
 * Error state for TanStack Query views: message + optional detail + retry.
 * `centered` fills the container (main panels); default is compact (sidebar lists).
 */
export function QueryError({ message, error, onRetry, centered }: {
  message: string
  error?: unknown
  onRetry: () => void
  centered?: boolean
}) {
  const detail = error instanceof Error ? error.message : null

  return (
    <div className={cn(centered ? "flex items-center justify-center h-full" : "p-4")}>
      <div className={cn("space-y-2", centered && "text-center")}>
        <div className={cn("flex items-center gap-2 text-red-500", centered && "justify-center")}>
          <AlertTriangle className="h-4 w-4 shrink-0" />
          <p className="text-base font-medium">{message}</p>
        </div>
        {detail && (
          <p className="text-sm text-muted-foreground font-mono break-all">{detail}</p>
        )}
        <button
          onClick={onRetry}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium rounded-lg border border-border text-muted-foreground hover:text-foreground hover:bg-accent transition-colors"
        >
          <RotateCw className="h-3.5 w-3.5" />
          Retry
        </button>
      </div>
    </div>
  )
}
