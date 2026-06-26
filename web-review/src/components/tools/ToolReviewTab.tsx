import {
  CheckCircle2,
  ChevronDown,
  Info,
  Loader2,
  MessageSquarePlus,
  Pencil,
  Plus,
  RotateCcw,
  Trash2,
  TriangleAlert,
} from "lucide-react"
import { useMemo, useState } from "react"

import type {
  ConditionToolMapping,
  FieldAnnotation,
  ProposedTool,
  ToolMeta,
} from "@/api/types"
import { Button } from "@/components/ui/Button"
import { SeverityPill } from "@/components/ui/SeverityPill"
import {
  useDeleteProposal,
  useSetToolReviewComplete,
  useToolCatalog,
  useToolReview,
} from "@/hooks/useToolReview"
import { CONDITION_META } from "@/lib/conditions"
import { cn } from "@/lib/utils"
import { useReviewStore } from "@/stores/reviewStore"
import { ProposeToolDialog } from "./ProposeToolDialog"
import { ToolDetailDialog } from "./ToolDetailDialog"
import {
  ToolAnnotationPopover,
  type ToolAnnotationTarget,
} from "./ToolAnnotationPopover"

const CATEGORY_LABEL: Record<string, string> = {
  neurodegenerative: "Neurodegenerative & dementia",
  cerebrovascular: "Cerebrovascular",
  epilepsy: "Seizure & epilepsy",
  infectious: "Infectious",
  tumor: "Neuro-oncology",
  autoimmune: "Autoimmune & demyelinating",
  neuromuscular: "Neuromuscular",
  headache: "Headache",
  functional: "Functional",
  metabolic: "Metabolic & systemic",
  other: "Other",
}

function categoryOf(condition: string): string {
  return CONDITION_META[condition]?.category ?? "other"
}

export function ToolReviewTab() {
  const version = useReviewStore((s) => s.datasetVersion)
  const catalog = useToolCatalog(version)
  const review = useToolReview(version)
  const completeMut = useSetToolReviewComplete(version)

  const [annTarget, setAnnTarget] = useState<ToolAnnotationTarget | null>(null)
  const [proposeOpen, setProposeOpen] = useState(false)
  const [editingProposal, setEditingProposal] = useState<ProposedTool | null>(null)
  const [detailTool, setDetailTool] = useState<ToolMeta | null>(null)

  const toolByName = useMemo(() => {
    const map = new Map<string, ToolMeta>()
    catalog.data?.tools.forEach((t) => map.set(t.name, t))
    return map
  }, [catalog.data])

  // field_path -> annotation, for indicators on each row.
  const annByPath = useMemo(() => {
    const map = new Map<string, FieldAnnotation>()
    review.data?.field_annotations.forEach((a) => map.set(a.field_path, a))
    return map
  }, [review.data])

  // Group conditions by pathology category.
  const grouped = useMemo(() => {
    const byCat = new Map<string, ConditionToolMapping[]>()
    catalog.data?.conditions.forEach((c) => {
      const cat = categoryOf(c.condition)
      const list = byCat.get(cat) ?? []
      list.push(c)
      byCat.set(cat, list)
    })
    return [...byCat.entries()].sort((a, b) =>
      (CATEGORY_LABEL[a[0]] ?? a[0]).localeCompare(CATEGORY_LABEL[b[0]] ?? b[0]),
    )
  }, [catalog.data])

  const [collapsed, setCollapsed] = useState<Set<string>>(new Set())
  function toggleCat(cat: string) {
    setCollapsed((prev) => {
      const next = new Set(prev)
      if (next.has(cat)) next.delete(cat)
      else next.add(cat)
      return next
    })
  }

  if (catalog.isLoading || review.isLoading) {
    return (
      <div className="flex items-center justify-center py-24 text-muted-foreground">
        <Loader2 className="w-5 h-5 animate-spin" />
      </div>
    )
  }
  if (catalog.error || !catalog.data) {
    return (
      <div className="text-center py-16 text-rose-500 text-sm">
        Could not load the tool catalog.
      </div>
    )
  }

  const completed = review.data?.completed_at != null
  const proposals = review.data?.proposed_tools ?? []

  function openAnnotation(
    e: React.MouseEvent<HTMLButtonElement>,
    fieldPath: string,
    label: string,
  ) {
    setAnnTarget({ fieldPath, label, anchor: e.currentTarget })
  }

  return (
    <div className="px-4 sm:px-6 py-6 sm:py-8 max-w-7xl mx-auto w-full">
      <div className="grid grid-cols-1 xl:grid-cols-[minmax(0,1fr)_22rem] gap-6">
        <div className="space-y-6 min-w-0">
      {/* Intro + actions */}
      <div className="space-y-3">
        <div>
          <p className="text-xs uppercase tracking-widest text-primary font-semibold">
            Step 1 · Tool review
          </p>
          <h1 className="text-2xl font-semibold tracking-tight">
            Review the diagnostic tool list
          </h1>
        </div>
        <p className="text-sm text-muted-foreground max-w-3xl leading-relaxed">
          Below are the {catalog.data.tools.length} tools available to the agent,
          organized by pathology category and condition. For each condition,
          check whether the right tools are marked required vs. optional, and flag
          anything missing or inappropriate. If a capability is missing entirely,
          propose it as a new tool. This grounds the tool set before we expand it.
        </p>
        <p className="text-xs text-muted-foreground/90 max-w-3xl leading-relaxed border-l-2 border-border pl-3">
          <span className="font-medium text-foreground/80">Costs:</span>{" "}
          reference rates in EUR, derived from the US Medicare Physician Fee
          Schedule (CMS PFS, 2024) converted at 1 USD = 0.92 EUR. Italian SSN
          tariffs are typically lower for diagnostic studies; EU private-sector
          rates are typically higher. Use them for relative comparison, not
          billing accuracy.
        </p>

        <div className="flex flex-wrap items-center gap-2">
          <Button
            size="sm"
            onClick={() => {
              setEditingProposal(null)
              setProposeOpen(true)
            }}
          >
            <Plus className="w-4 h-4" />
            Propose a tool
          </Button>
          {completed ? (
            <Button
              size="sm"
              variant="secondary"
              onClick={() => completeMut.mutate(false)}
              disabled={completeMut.isPending}
            >
              <RotateCcw className="w-4 h-4" />
              Reopen review
            </Button>
          ) : (
            <Button
              size="sm"
              variant="secondary"
              onClick={() => completeMut.mutate(true)}
              disabled={completeMut.isPending}
            >
              <CheckCircle2 className="w-4 h-4" />
              Mark as reviewed
            </Button>
          )}
          {completed && (
            <span className="inline-flex items-center gap-1.5 text-xs text-emerald-600 dark:text-emerald-400">
              <CheckCircle2 className="w-4 h-4" />
              Reviewed
            </span>
          )}
        </div>
      </div>

      {/* Proposed tools (this reviewer's) */}
      {proposals.length > 0 && (
        <section className="rounded-2xl border border-primary/30 bg-primary/5 p-4 space-y-3">
          <h2 className="text-sm font-semibold flex items-center gap-2">
            <MessageSquarePlus className="w-4 h-4 text-primary" />
            Your proposed tools ({proposals.length})
          </h2>
          <div className="space-y-2">
            {proposals.map((p) => (
              <ProposalCard
                key={p.id}
                proposal={p}
                conditions={catalog.data!.conditions}
                version={version}
                onEdit={() => {
                  setEditingProposal(p)
                  setProposeOpen(true)
                }}
              />
            ))}
          </div>
        </section>
      )}

      {/* Coverage gap callout */}
      {catalog.data.unmapped_tools.length > 0 && (
        <section className="rounded-2xl border border-amber-500/40 bg-amber-500/5 p-4">
          <h2 className="text-sm font-semibold flex items-center gap-2 text-amber-700 dark:text-amber-300">
            <TriangleAlert className="w-4 h-4" />
            Tools not mapped to any condition
          </h2>
          <p className="text-xs text-muted-foreground mt-1 mb-3">
            These tools exist but aren't expected for any condition in this
            dataset. Flag whether that's a coverage gap.
          </p>
          <div className="space-y-1.5">
            {catalog.data.unmapped_tools.map((name) => {
              const meta = toolByName.get(name)
              const path = `tool:${name}`
              return (
                <ToolRow
                  key={name}
                  meta={meta}
                  toolName={name}
                  annotation={annByPath.get(path)}
                  onComment={(e) =>
                    openAnnotation(e, path, meta?.label ?? name)
                  }
                  onOpenDetail={meta ? () => setDetailTool(meta) : undefined}
                />
              )
            })}
          </div>
        </section>
      )}

      {/* Universal tools */}
      <section className="rounded-2xl border border-border bg-card p-4">
        <h2 className="text-sm font-semibold">Always-available tools</h2>
        <p className="text-xs text-muted-foreground mt-1 mb-3">
          Available for every condition.
        </p>
        <div className="space-y-1.5">
          {catalog.data.universal_tools.map((name) => {
            const meta = toolByName.get(name)
            const path = `tool:${name}`
            return (
              <ToolRow
                key={name}
                meta={meta}
                toolName={name}
                annotation={annByPath.get(path)}
                onComment={(e) => openAnnotation(e, path, meta?.label ?? name)}
                onOpenDetail={meta ? () => setDetailTool(meta) : undefined}
              />
            )
          })}
        </div>
      </section>

      {/* Categories → conditions → tools */}
      <div className="space-y-3">
        {grouped.map(([cat, conditions]) => {
          const isCollapsed = collapsed.has(cat)
          return (
            <section
              key={cat}
              className="rounded-2xl border border-border bg-card overflow-hidden"
            >
              <button
                type="button"
                onClick={() => toggleCat(cat)}
                className="w-full flex items-center justify-between gap-3 px-4 py-3 hover:bg-secondary/30 transition-colors"
              >
                <span className="font-semibold text-sm">
                  {CATEGORY_LABEL[cat] ?? cat}
                  <span className="ml-2 text-xs font-normal text-muted-foreground">
                    {conditions.length} condition
                    {conditions.length === 1 ? "" : "s"}
                  </span>
                </span>
                <ChevronDown
                  className={cn(
                    "w-4 h-4 text-muted-foreground transition-transform",
                    isCollapsed && "-rotate-90",
                  )}
                />
              </button>

              {!isCollapsed && (
                <div className="divide-y divide-border/60 border-t border-border">
                  {conditions.map((c) => (
                    <ConditionBlock
                      key={c.condition}
                      mapping={c}
                      toolByName={toolByName}
                      annByPath={annByPath}
                      onComment={openAnnotation}
                      onOpenDetail={setDetailTool}
                    />
                  ))}
                </div>
              )}
            </section>
          )
        })}
      </div>

      <ToolAnnotationPopover
        version={version}
        review={review.data}
        target={annTarget}
        onClose={() => setAnnTarget(null)}
      />
      <ProposeToolDialog
        version={version}
        conditions={catalog.data.conditions}
        open={proposeOpen}
        onOpenChange={(o) => {
          setProposeOpen(o)
          if (!o) setEditingProposal(null)
        }}
        editing={editingProposal}
      />
      <ToolDetailDialog
        tool={detailTool}
        version={version}
        review={review.data}
        open={!!detailTool}
        onOpenChange={(o) => {
          if (!o) setDetailTool(null)
        }}
      />
        </div>
        <aside className="xl:sticky xl:top-4 xl:self-start xl:max-h-[calc(100vh-2rem)] xl:overflow-y-auto">
          <ToolReferencePanel
            tools={catalog.data.tools}
            onOpenDetail={setDetailTool}
          />
        </aside>
      </div>
    </div>
  )
}

// --- Tool reference (sticky side panel) ------------------------------

function ToolReferencePanel({
  tools,
  onOpenDetail,
}: {
  tools: ToolMeta[]
  onOpenDetail: (tool: ToolMeta) => void
}) {
  return (
    <div className="rounded-2xl border border-border bg-card/60 backdrop-blur p-4">
      <h2 className="text-xs uppercase tracking-widest text-muted-foreground font-semibold mb-3">
        Tool reference
      </h2>
      <p className="text-[11px] text-muted-foreground mb-4 leading-relaxed">
        Quick glance at what each of the {tools.length} tools does. Click a tool
        to see what the agent sends and gets back — and annotate the I/O.
      </p>
      <div className="space-y-1">
        {tools.map((t) => (
          <button
            key={t.name}
            type="button"
            onClick={() => onOpenDetail(t)}
            className="w-full text-left text-sm rounded-lg px-2 py-1.5 hover:bg-secondary/50 transition-colors"
          >
            <div className="flex items-baseline justify-between gap-2">
              <span className="font-medium text-foreground/95 text-[13px]">
                {t.label}
              </span>
              {t.cost_summary && (
                <span className="text-[10px] text-muted-foreground tabular-nums whitespace-nowrap">
                  {t.cost_summary}
                </span>
              )}
            </div>
            {t.description && (
              <p className="text-[11px] text-muted-foreground leading-snug mt-0.5">
                {t.description}
              </p>
            )}
            <p className="text-[10px] text-muted-foreground/70 mt-1 inline-flex items-center gap-1">
              <Info className="w-3 h-3" />
              {t.parameters.length} params · {t.output_fields.length} return fields
            </p>
          </button>
        ))}
      </div>
    </div>
  )
}

// --- Condition block --------------------------------------------------

function ConditionBlock({
  mapping,
  toolByName,
  annByPath,
  onComment,
  onOpenDetail,
}: {
  mapping: ConditionToolMapping
  toolByName: Map<string, ToolMeta>
  annByPath: Map<string, FieldAnnotation>
  onComment: (
    e: React.MouseEvent<HTMLButtonElement>,
    fieldPath: string,
    label: string,
  ) => void
  onOpenDetail: (tool: ToolMeta) => void
}) {
  const condPath = `condition:${mapping.condition}`
  const condAnn = annByPath.get(condPath)

  return (
    <div className="px-4 py-3">
      <div className="flex items-center justify-between gap-2">
        <h3 className="text-sm font-medium">{mapping.label}</h3>
        <CommentButton
          annotation={condAnn}
          onClick={(e) =>
            onComment(e, condPath, `${mapping.label} — overall coverage`)
          }
        />
      </div>

      <div className="mt-2 space-y-1.5">
        {mapping.required_tools.map((name) => {
          const path = `condition_tool:${mapping.condition}:${name}`
          const meta = toolByName.get(name)
          return (
            <ToolRow
              key={name}
              meta={meta}
              toolName={name}
              tier="required"
              annotation={annByPath.get(path)}
              onComment={(e) =>
                onComment(e, path, `${meta?.label ?? name} · ${mapping.label}`)
              }
              onOpenDetail={meta ? () => onOpenDetail(meta) : undefined}
            />
          )
        })}
        {mapping.optional_tools.map((name) => {
          const path = `condition_tool:${mapping.condition}:${name}`
          const meta = toolByName.get(name)
          return (
            <ToolRow
              key={name}
              meta={meta}
              toolName={name}
              tier="optional"
              annotation={annByPath.get(path)}
              onComment={(e) =>
                onComment(e, path, `${meta?.label ?? name} · ${mapping.label}`)
              }
              onOpenDetail={meta ? () => onOpenDetail(meta) : undefined}
            />
          )
        })}
        {mapping.required_tools.length === 0 &&
          mapping.optional_tools.length === 0 && (
            <p className="text-xs text-muted-foreground italic">
              No tools mapped to this condition.
            </p>
          )}
      </div>
    </div>
  )
}

// --- Tool row ---------------------------------------------------------

function ToolRow({
  meta,
  toolName,
  tier,
  annotation,
  onComment,
  onOpenDetail,
}: {
  meta: ToolMeta | undefined
  toolName: string
  tier?: "required" | "optional"
  annotation: FieldAnnotation | undefined
  onComment: (e: React.MouseEvent<HTMLButtonElement>) => void
  onOpenDetail?: () => void
}) {
  return (
    <div
      className={cn(
        "flex items-center gap-3 rounded-lg px-2.5 py-1.5 hover:bg-secondary/30 transition-colors group",
        annotation && "border-l-2 -ml-px pl-2",
        annotation?.severity === "error" && "border-l-rose-500",
        annotation?.severity === "issue" && "border-l-amber-500",
        annotation?.severity === "note" && "border-l-sky-500",
      )}
    >
      <div className="min-w-0 flex-1">
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-sm font-medium">{meta?.label ?? toolName}</span>
          {tier && (
            <span
              className={cn(
                "text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded border",
                tier === "required"
                  ? "border-primary/40 text-primary bg-primary/10"
                  : "border-border text-muted-foreground bg-secondary/40",
              )}
            >
              {tier}
            </span>
          )}
          {meta?.cost_summary && (
            <span className="text-[11px] text-muted-foreground tabular-nums">
              {meta.cost_summary}
            </span>
          )}
        </div>
        {meta?.description && (
          <p className="text-xs text-muted-foreground leading-snug mt-0.5 line-clamp-2">
            {meta.description}
          </p>
        )}
      </div>
      {onOpenDetail && (
        <button
          type="button"
          onClick={onOpenDetail}
          className="flex-shrink-0 inline-flex items-center gap-1 text-[11px] rounded-md px-2 py-1 text-muted-foreground opacity-0 group-hover:opacity-100 focus:opacity-100 hover:bg-secondary/70 transition-colors"
        >
          <Info className="w-3.5 h-3.5" />
          I/O
        </button>
      )}
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
        "flex-shrink-0 inline-flex items-center gap-1.5 text-xs rounded-md px-2 py-1 transition-colors",
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

// --- Proposal card ----------------------------------------------------

function ProposalCard({
  proposal,
  conditions,
  version,
  onEdit,
}: {
  proposal: ProposedTool
  conditions: ConditionToolMapping[]
  version: string
  onEdit: () => void
}) {
  const deleteMut = useDeleteProposal(version)
  const labelOf = (key: string) =>
    conditions.find((c) => c.condition === key)?.label ?? key

  return (
    <div className="rounded-xl border border-border bg-card p-3">
      <div className="flex items-start justify-between gap-2">
        <div className="min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="text-sm font-semibold">{proposal.name}</span>
            {proposal.modality && (
              <span className="text-[10px] uppercase tracking-wider px-1.5 py-0.5 rounded border border-border text-muted-foreground">
                {proposal.modality}
              </span>
            )}
          </div>
          <p className="text-xs text-foreground/80 mt-1 leading-relaxed">
            {proposal.description}
          </p>
          {proposal.rationale && (
            <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
              <span className="font-medium">Why: </span>
              {proposal.rationale}
            </p>
          )}
          {proposal.target_conditions.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2">
              {proposal.target_conditions.map((k) => (
                <span
                  key={k}
                  className="text-[10px] px-1.5 py-0.5 rounded-full bg-secondary/60 text-muted-foreground"
                >
                  {labelOf(k)}
                </span>
              ))}
            </div>
          )}
        </div>
        <div className="flex items-center gap-1 flex-shrink-0">
          <button
            type="button"
            onClick={onEdit}
            className="p-1.5 rounded-md text-muted-foreground hover:bg-secondary/70 hover:text-foreground"
            aria-label="Edit proposal"
          >
            <Pencil className="w-3.5 h-3.5" />
          </button>
          <button
            type="button"
            onClick={() => deleteMut.mutate(proposal.id)}
            disabled={deleteMut.isPending}
            className="p-1.5 rounded-md text-rose-500 hover:bg-rose-500/10 disabled:opacity-50"
            aria-label="Delete proposal"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  )
}
