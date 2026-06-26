import * as Dialog from "@radix-ui/react-dialog"
import { AnimatePresence, motion } from "framer-motion"
import { MessageSquarePlus, X } from "lucide-react"
import { useMemo, useState } from "react"

import type {
  FieldAnnotation,
  ToolMeta,
  ToolOutputField,
  ToolParameter,
  ToolReview,
} from "@/api/types"
import { SeverityPill } from "@/components/ui/SeverityPill"
import { cn } from "@/lib/utils"
import {
  ToolAnnotationPopover,
  type ToolAnnotationTarget,
} from "./ToolAnnotationPopover"

/**
 * Tool I/O detail sheet — what the agent passes and what it gets back.
 *
 * Each parameter and return field is independently annotatable so reviewers
 * can flag a specific knob ("`contrast` shouldn't be optional for tumor")
 * or a specific return field ("EEG report should include sleep staging")
 * without conflating it with a tool-level comment.
 *
 * field_path scheme:
 *   tool:<name>:param:<param_key>
 *   tool:<name>:return:<field_name>
 */
export function ToolDetailDialog({
  tool,
  version,
  review,
  open,
  onOpenChange,
}: {
  tool: ToolMeta | null
  version: string
  review: ToolReview | undefined
  open: boolean
  onOpenChange: (open: boolean) => void
}) {
  const [annTarget, setAnnTarget] = useState<ToolAnnotationTarget | null>(null)

  const annByPath = useMemo(() => {
    const map = new Map<string, FieldAnnotation>()
    review?.field_annotations.forEach((a) => map.set(a.field_path, a))
    return map
  }, [review])

  if (!tool) return null

  function openAnn(
    e: React.MouseEvent<HTMLButtonElement>,
    fieldPath: string,
    label: string,
  ) {
    setAnnTarget({ fieldPath, label, anchor: e.currentTarget })
  }

  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <AnimatePresence>
        {open && (
          <Dialog.Portal forceMount>
            <Dialog.Overlay asChild>
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm"
              />
            </Dialog.Overlay>
            <Dialog.Content asChild>
              <motion.div
                initial={{ opacity: 0, y: 12, scale: 0.98 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 8, scale: 0.98 }}
                transition={{ type: "spring", stiffness: 360, damping: 30 }}
                className="fixed left-1/2 top-1/2 z-50 w-[min(720px,calc(100vw-1.5rem))] max-h-[calc(100vh-2rem)] -translate-x-1/2 -translate-y-1/2 overflow-y-auto rounded-2xl border border-border bg-card p-6 shadow-2xl"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0">
                    <p className="text-[11px] uppercase tracking-widest text-muted-foreground font-semibold">
                      Tool I/O
                    </p>
                    <Dialog.Title className="text-lg font-semibold flex items-baseline gap-2 flex-wrap">
                      {tool.label}
                      {tool.cost_summary && (
                        <span className="text-xs font-normal text-muted-foreground tabular-nums">
                          {tool.cost_summary}
                        </span>
                      )}
                    </Dialog.Title>
                    <Dialog.Description className="text-sm text-muted-foreground mt-1.5 leading-relaxed">
                      {tool.description}
                    </Dialog.Description>
                    <p className="text-[10px] uppercase tracking-wider text-muted-foreground/80 mt-2 font-mono">
                      {tool.name}
                    </p>
                  </div>
                  <Dialog.Close asChild>
                    <button
                      type="button"
                      className="text-muted-foreground hover:text-foreground"
                      aria-label="Close"
                    >
                      <X className="w-5 h-5" />
                    </button>
                  </Dialog.Close>
                </div>

                <Section title="Parameters" subtitle="What the agent sends">
                  {tool.parameters.length === 0 ? (
                    <p className="text-xs text-muted-foreground italic">
                      No parameter metadata published.
                    </p>
                  ) : (
                    <div className="space-y-1.5">
                      {tool.parameters.map((p) => {
                        const path = `tool:${tool.name}:param:${p.name}`
                        return (
                          <ParamRow
                            key={p.name}
                            param={p}
                            annotation={annByPath.get(path)}
                            onComment={(e) =>
                              openAnn(
                                e,
                                path,
                                `${tool.label} · param ${p.name}`,
                              )
                            }
                          />
                        )
                      })}
                    </div>
                  )}
                </Section>

                <Section title="Returns" subtitle="What the agent gets back">
                  {tool.output_fields.length === 0 ? (
                    <p className="text-xs text-muted-foreground italic">
                      No return metadata published.
                    </p>
                  ) : (
                    <div className="space-y-1.5">
                      {tool.output_fields.map((f) => {
                        const path = `tool:${tool.name}:return:${f.name}`
                        return (
                          <ReturnRow
                            key={f.name}
                            field={f}
                            annotation={annByPath.get(path)}
                            onComment={(e) =>
                              openAnn(
                                e,
                                path,
                                `${tool.label} · return ${f.name}`,
                              )
                            }
                          />
                        )
                      })}
                    </div>
                  )}
                </Section>

                <ToolAnnotationPopover
                  version={version}
                  review={review}
                  target={annTarget}
                  onClose={() => setAnnTarget(null)}
                />
              </motion.div>
            </Dialog.Content>
          </Dialog.Portal>
        )}
      </AnimatePresence>
    </Dialog.Root>
  )
}

function Section({
  title,
  subtitle,
  children,
}: {
  title: string
  subtitle?: string
  children: React.ReactNode
}) {
  return (
    <section className="mt-6">
      <div className="mb-2.5">
        <h3 className="text-sm font-semibold">{title}</h3>
        {subtitle && (
          <p className="text-[11px] text-muted-foreground">{subtitle}</p>
        )}
      </div>
      {children}
    </section>
  )
}

function ParamRow({
  param,
  annotation,
  onComment,
}: {
  param: ToolParameter
  annotation: FieldAnnotation | undefined
  onComment: (e: React.MouseEvent<HTMLButtonElement>) => void
}) {
  const typeLabel =
    param.type === "array" && param.items_type
      ? `list[${param.items_type}]`
      : param.type
  return (
    <div
      className={cn(
        "flex items-start gap-3 rounded-lg px-2.5 py-2 hover:bg-secondary/30 transition-colors group",
        annotation && "border-l-2 -ml-px pl-2",
        annotation?.severity === "error" && "border-l-rose-500",
        annotation?.severity === "issue" && "border-l-amber-500",
        annotation?.severity === "note" && "border-l-sky-500",
      )}
    >
      <div className="min-w-0 flex-1">
        <div className="flex items-baseline gap-2 flex-wrap">
          <span className="font-mono text-[13px] font-medium">{param.name}</span>
          <span className="text-[10px] uppercase tracking-wider text-muted-foreground">
            {typeLabel}
          </span>
          {param.required ? (
            <span className="text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded border border-primary/40 text-primary bg-primary/10">
              required
            </span>
          ) : (
            <span className="text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded border border-border text-muted-foreground bg-secondary/40">
              optional
            </span>
          )}
          {param.default != null && (
            <span className="text-[10px] text-muted-foreground tabular-nums">
              default: <span className="font-mono">{String(param.default)}</span>
            </span>
          )}
        </div>
        {param.enum && param.enum.length > 0 && (
          <div className="flex flex-wrap gap-1 mt-1.5">
            {param.enum.map((v) => (
              <span
                key={v}
                className="text-[10px] px-1.5 py-0.5 rounded-full bg-secondary/60 text-foreground/80 font-mono"
              >
                {v}
              </span>
            ))}
          </div>
        )}
        {param.description && (
          <p className="text-xs text-muted-foreground leading-snug mt-1">
            {param.description}
          </p>
        )}
      </div>
      <CommentButton annotation={annotation} onClick={onComment} />
    </div>
  )
}

function ReturnRow({
  field,
  annotation,
  onComment,
}: {
  field: ToolOutputField
  annotation: FieldAnnotation | undefined
  onComment: (e: React.MouseEvent<HTMLButtonElement>) => void
}) {
  return (
    <div
      className={cn(
        "flex items-start gap-3 rounded-lg px-2.5 py-2 hover:bg-secondary/30 transition-colors group",
        annotation && "border-l-2 -ml-px pl-2",
        annotation?.severity === "error" && "border-l-rose-500",
        annotation?.severity === "issue" && "border-l-amber-500",
        annotation?.severity === "note" && "border-l-sky-500",
      )}
    >
      <div className="min-w-0 flex-1">
        <div className="flex items-baseline gap-2 flex-wrap">
          <span className="font-mono text-[13px] font-medium">{field.name}</span>
          <span className="text-[10px] uppercase tracking-wider text-muted-foreground">
            {field.type}
          </span>
          {!field.required && (
            <span className="text-[10px] uppercase tracking-wider text-muted-foreground">
              optional
            </span>
          )}
        </div>
        {field.description && (
          <p className="text-xs text-muted-foreground leading-snug mt-1">
            {field.description}
          </p>
        )}
      </div>
      <CommentButton annotation={annotation} onClick={onComment} />
    </div>
  )
}

function CommentButton({
  annotation,
  onClick,
}: {
  annotation: FieldAnnotation | undefined
  onClick: (e: React.MouseEvent<HTMLButtonElement>) => void
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "flex-shrink-0 inline-flex items-center gap-1.5 text-xs rounded-md px-2 py-1 transition-colors mt-0.5",
        annotation
          ? "text-foreground"
          : "text-muted-foreground opacity-0 group-hover:opacity-100 focus:opacity-100 hover:bg-secondary/70",
      )}
    >
      {annotation ? (
        <SeverityPill severity={annotation.severity} />
      ) : (
        <>
          <MessageSquarePlus className="w-3.5 h-3.5" />
          Comment
        </>
      )}
    </button>
  )
}
