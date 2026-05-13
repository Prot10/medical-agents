import {
  MessageCircle,
  MessageCircleWarning,
  MessageSquarePlus,
  OctagonAlert,
} from "lucide-react"
import { useRef } from "react"

import type { Severity } from "@/api/types"
import { cn } from "@/lib/utils"
import { useAnnotationContext } from "./AnnotationContext"

const SEVERITY_ICON = {
  note: MessageCircle,
  issue: MessageCircleWarning,
  error: OctagonAlert,
}

const SEVERITY_TONE = {
  note: "text-sky-500",
  issue: "text-amber-500",
  error: "text-rose-500",
}

const SEVERITY_BORDER = {
  note: "border-l-sky-500",
  issue: "border-l-amber-500",
  error: "border-l-rose-500",
}

function topSeverity(severities: Severity[]): Severity {
  if (severities.includes("error")) return "error"
  if (severities.includes("issue")) return "issue"
  return "note"
}

export function AnnotatableField({
  path,
  snippet,
  children,
  className,
  attachRight,
}: {
  path: string
  snippet?: string
  children: React.ReactNode
  className?: string
  /** If true, the marker icon sits inside the field instead of the right margin. */
  attachRight?: boolean
}) {
  const ctx = useAnnotationContext()
  const wrapperRef = useRef<HTMLDivElement>(null)
  const annotations = ctx.annotationsByPath.get(path) ?? []
  const hasAnnotations = annotations.length > 0
  const top = hasAnnotations
    ? topSeverity(annotations.map((a) => a.severity))
    : null
  const Icon = top ? SEVERITY_ICON[top] : MessageCircle

  const isActive =
    ctx.openPopover?.fieldPath === path &&
    ctx.openPopover.anchor === wrapperRef.current

  function handleOpen(event: React.MouseEvent) {
    event.stopPropagation()
    if (!wrapperRef.current) return
    ctx.setOpenPopover({
      fieldPath: path,
      fieldSnippet: snippet,
      anchor: wrapperRef.current,
    })
  }

  const AddIcon = MessageSquarePlus

  return (
    <div
      ref={wrapperRef}
      data-annotatable-path={path}
      className={cn(
        "group/annotatable relative transition-colors rounded-md",
        hasAnnotations
          ? cn(
              "border-l-[3px] pl-3 -ml-3",
              top ? SEVERITY_BORDER[top] : "border-l-primary/40",
            )
          : cn(
              // Strong hover affordance: tinted background + thick primary stripe
              "hover:bg-primary/[0.04]",
              "hover:before:absolute hover:before:left-[-3px] hover:before:top-0 hover:before:bottom-0",
              "hover:before:w-[3px] hover:before:bg-primary hover:before:rounded-l",
            ),
        isActive && "ring-1 ring-primary/40 ring-offset-2 ring-offset-background",
        className,
      )}
    >
      {children}
      <button
        type="button"
        onClick={handleOpen}
        aria-label={hasAnnotations ? `Edit annotations on ${path}` : `Comment on ${path}`}
        title={hasAnnotations ? "Annotations" : "Comment on this field"}
        className={cn(
          "absolute -translate-y-1/2 top-3 z-10 inline-flex items-center justify-center gap-1 rounded-full",
          "transition-all duration-200 ease-out",
          hasAnnotations
            ? cn(
                "h-7 px-2 opacity-100",
                "bg-card border border-border shadow-sm hover:bg-secondary/80",
              )
            : cn(
                "h-8 px-2.5",
                "opacity-0 scale-90 translate-x-1",
                "group-hover/annotatable:opacity-100 group-hover/annotatable:scale-100 group-hover/annotatable:translate-x-0",
                "focus-visible:opacity-100 focus-visible:scale-100 focus-visible:translate-x-0",
                "bg-primary text-primary-foreground border border-primary",
                "shadow-md shadow-primary/30 hover:brightness-110",
                "ring-2 ring-primary/15",
              ),
          attachRight ? "right-1.5" : "-right-3.5",
        )}
      >
        {hasAnnotations ? (
          <>
            <Icon
              className={cn(
                "w-3.5 h-3.5",
                top ? SEVERITY_TONE[top] : "text-muted-foreground",
              )}
            />
            <span
              className={cn(
                "text-[10px] tabular-nums font-semibold",
                top ? SEVERITY_TONE[top] : "text-muted-foreground",
              )}
            >
              {annotations.length}
            </span>
          </>
        ) : (
          <>
            <AddIcon className="w-3.5 h-3.5" strokeWidth={2.5} />
            {!attachRight && (
              <span className="text-[11px] font-semibold tracking-wide">
                Comment
              </span>
            )}
          </>
        )}
      </button>
    </div>
  )
}
