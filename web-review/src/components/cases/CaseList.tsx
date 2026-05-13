import { Inbox } from "lucide-react"
import { useMemo } from "react"

import type {
  CaseIndexEntry,
  CaseReviewSummary,
  ReviewStatus,
} from "@/api/types"
import { useReviewStore } from "@/stores/reviewStore"
import { CaseListRow } from "./CaseListRow"

export function CaseList({
  cases,
  reviews,
  selectedCaseId,
  onSelectCase,
}: {
  cases: CaseIndexEntry[]
  reviews: CaseReviewSummary[]
  selectedCaseId: string | null
  onSelectCase: (caseId: string) => void
}) {
  const searchText = useReviewStore((s) => s.searchText)
  const filterStatus = useReviewStore((s) => s.filterStatus)
  const filterConditions = useReviewStore((s) => s.filterConditions)

  const reviewByCase = useMemo(() => {
    const map = new Map<string, CaseReviewSummary>()
    for (const r of reviews) map.set(r.case_id, r)
    return map
  }, [reviews])

  const filtered = useMemo(() => {
    const lowerSearch = searchText.trim().toLowerCase()
    return cases.filter((c) => {
      if (filterConditions.length > 0 && !filterConditions.includes(c.condition)) {
        return false
      }
      const review = reviewByCase.get(c.case_id)
      const status: ReviewStatus = review?.status ?? "pending"
      if (filterStatus !== "all" && status !== filterStatus) return false
      if (
        lowerSearch &&
        !c.case_id.toLowerCase().includes(lowerSearch) &&
        !c.chief_complaint.toLowerCase().includes(lowerSearch)
      ) {
        return false
      }
      return true
    })
  }, [cases, filterConditions, filterStatus, reviewByCase, searchText])

  if (filtered.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 text-center text-muted-foreground">
        <Inbox className="w-8 h-8 mb-3 opacity-40" />
        <p className="text-sm">No cases match these filters.</p>
        <p className="text-xs mt-1">Try clearing some filters or the search.</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-1.5">
      <div className="text-xs text-muted-foreground mb-1 tabular-nums">
        Showing {filtered.length.toLocaleString()} of {cases.length.toLocaleString()} cases
      </div>
      {filtered.map((entry) => (
        <CaseListRow
          key={entry.case_id}
          entry={entry}
          review={reviewByCase.get(entry.case_id)}
          selected={entry.case_id === selectedCaseId}
          onSelect={() => onSelectCase(entry.case_id)}
        />
      ))}
    </div>
  )
}
