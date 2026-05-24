import * as Popover from "@radix-ui/react-popover"
import { Check, Filter, Search, Shuffle, X } from "lucide-react"
import { useMemo, useState } from "react"

import type { CaseIndexEntry, CaseReviewSummary, ReviewStatus } from "@/api/types"
import { conditionLabel, conditionShort } from "@/lib/conditions"
import { cn } from "@/lib/utils"
import { useReviewStore } from "@/stores/reviewStore"
import { Button } from "@/components/ui/Button"

interface FilterBarProps {
  cases: CaseIndexEntry[]
  reviews: CaseReviewSummary[]
  pendingCases: CaseIndexEntry[]
  onPickRandomPending: () => void
}

const STATUS_OPTIONS: Array<{ value: ReviewStatus | "all"; label: string }> = [
  { value: "all", label: "Any status" },
  { value: "pending", label: "Pending" },
  { value: "in_progress", label: "In progress" },
  { value: "needs_changes", label: "Needs changes" },
  { value: "approved", label: "Approved" },
]

export function FilterBar({
  cases,
  pendingCases,
  onPickRandomPending,
}: FilterBarProps) {
  const search = useReviewStore((s) => s.searchText)
  const setSearch = useReviewStore((s) => s.setSearchText)
  const filterStatus = useReviewStore((s) => s.filterStatus)
  const setFilterStatus = useReviewStore((s) => s.setFilterStatus)
  const filterConditions = useReviewStore((s) => s.filterConditions)
  const setFilterConditions = useReviewStore((s) => s.setFilterConditions)

  const conditionCounts = useMemo(() => {
    const counts = new Map<string, number>()
    for (const c of cases) counts.set(c.condition, (counts.get(c.condition) ?? 0) + 1)
    return counts
  }, [cases])

  const conditionOptions = useMemo(
    () =>
      Array.from(conditionCounts.entries())
        .map(([condition, count]) => ({ condition, count }))
        .sort((a, b) => b.count - a.count),
    [conditionCounts],
  )

  return (
    <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:flex-wrap">
      {/* Search: full-width on mobile, flex-1 on desktop */}
      <div className="relative w-full sm:flex-1 sm:min-w-[200px] sm:max-w-md">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search case ID or complaint…"
          className="w-full h-9 pl-9 pr-9 bg-secondary border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring placeholder:text-muted-foreground"
        />
        {search && (
          <button
            type="button"
            onClick={() => setSearch("")}
            aria-label="Clear search"
            className="absolute right-2 top-1/2 -translate-y-1/2 w-5 h-5 rounded hover:bg-background text-muted-foreground"
          >
            <X className="w-3.5 h-3.5 m-auto" />
          </button>
        )}
      </div>

      {/* Filter group + action: row on all sizes, wraps if needed */}
      <div className="flex items-center gap-2 flex-wrap sm:flex-nowrap sm:ml-auto">
        <ConditionFilter
          options={conditionOptions}
          selected={filterConditions}
          onChange={setFilterConditions}
        />

        <select
          value={filterStatus}
          onChange={(e) => setFilterStatus(e.target.value as ReviewStatus | "all")}
          aria-label="Filter by status"
          className="h-9 px-2 bg-secondary border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
        >
          {STATUS_OPTIONS.map((o) => (
            <option key={o.value} value={o.value}>
              {o.label}
            </option>
          ))}
        </select>

        <Button
          variant="secondary"
          size="sm"
          onClick={onPickRandomPending}
          disabled={pendingCases.length === 0}
          title="Open a random pending case"
        >
          <Shuffle className="w-4 h-4" />
          <span className="hidden sm:inline">Random pending</span>
          <span className="sm:hidden">Random</span>
        </Button>
      </div>
    </div>
  )
}

function ConditionFilter({
  options,
  selected,
  onChange,
}: {
  options: Array<{ condition: string; count: number }>
  selected: string[]
  onChange: (next: string[]) => void
}) {
  const [search, setSearch] = useState("")
  const filtered = options.filter((o) =>
    conditionLabel(o.condition).toLowerCase().includes(search.toLowerCase()) ||
    o.condition.includes(search.toLowerCase()),
  )
  function toggle(condition: string) {
    onChange(
      selected.includes(condition)
        ? selected.filter((c) => c !== condition)
        : [...selected, condition],
    )
  }
  return (
    <Popover.Root>
      <Popover.Trigger asChild>
        <button
          type="button"
          className={cn(
            "h-9 px-3 inline-flex items-center gap-2 bg-secondary border border-border rounded-md text-sm hover:bg-secondary/70",
            selected.length > 0 && "border-primary/40",
          )}
        >
          <Filter className="w-4 h-4" />
          <span>
            {selected.length === 0
              ? "All conditions"
              : `${selected.length} condition${selected.length === 1 ? "" : "s"}`}
          </span>
        </button>
      </Popover.Trigger>
      <Popover.Portal>
        <Popover.Content
          align="start"
          sideOffset={6}
          collisionPadding={12}
          className="z-30 w-[min(20rem,calc(100vw-1.5rem))] bg-popover border border-border rounded-xl shadow-xl p-3"
        >
          <div className="relative mb-2">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-muted-foreground" />
            <input
              type="text"
              autoFocus
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Filter conditions…"
              className="w-full h-8 pl-8 pr-2 bg-background border border-border rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>
          <div className="max-h-72 overflow-y-auto -mx-2">
            {filtered.length === 0 && (
              <div className="text-xs text-muted-foreground px-3 py-2">
                No matching conditions.
              </div>
            )}
            {filtered.map((o) => {
              const isSelected = selected.includes(o.condition)
              return (
                <button
                  key={o.condition}
                  type="button"
                  onClick={() => toggle(o.condition)}
                  className={cn(
                    "w-full flex items-center justify-between gap-2 px-3 py-1.5 text-sm rounded-md transition-colors",
                    isSelected
                      ? "bg-primary/10 text-primary"
                      : "hover:bg-secondary/60 text-foreground",
                  )}
                >
                  <span className="flex items-center gap-2 min-w-0">
                    {isSelected ? (
                      <Check className="w-3.5 h-3.5 flex-shrink-0" />
                    ) : (
                      <span className="w-3.5 h-3.5 flex-shrink-0" />
                    )}
                    <span className="truncate">{conditionLabel(o.condition)}</span>
                    <span className="text-[10px] text-muted-foreground font-mono">
                      {conditionShort(o.condition)}
                    </span>
                  </span>
                  <span className="text-xs text-muted-foreground tabular-nums">
                    {o.count}
                  </span>
                </button>
              )
            })}
          </div>
          {selected.length > 0 && (
            <div className="border-t border-border mt-2 pt-2 flex justify-between items-center">
              <button
                type="button"
                onClick={() => onChange([])}
                className="text-xs text-muted-foreground hover:text-foreground"
              >
                Clear ({selected.length})
              </button>
              <span className="text-[11px] text-muted-foreground">
                Multi-select
              </span>
            </div>
          )}
        </Popover.Content>
      </Popover.Portal>
    </Popover.Root>
  )
}
