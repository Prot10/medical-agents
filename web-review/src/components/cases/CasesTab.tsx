import { Loader2 } from "lucide-react"
import { useMemo } from "react"

import type { CaseReviewSummary } from "@/api/types"
import { useCases, useMyReviews } from "@/hooks/useReview"
import { useReviewStore } from "@/stores/reviewStore"
import { CaseDetail } from "./CaseDetail"
import { CaseList } from "./CaseList"
import { FilterBar } from "./FilterBar"

export function CasesTab() {
  const version = useReviewStore((s) => s.datasetVersion)
  const selectedCaseId = useReviewStore((s) => s.selectedCaseId)
  const setSelectedCaseId = useReviewStore((s) => s.setSelectedCaseId)
  const cases = useCases(version)
  const reviews = useMyReviews(version)

  const reviewByCase = useMemo(() => {
    const map = new Map<string, CaseReviewSummary>()
    for (const r of reviews.data ?? []) map.set(r.case_id, r)
    return map
  }, [reviews.data])

  const pendingCases = useMemo(() => {
    if (!cases.data) return []
    return cases.data.filter((c) => {
      const review = reviewByCase.get(c.case_id)
      const status = review?.status ?? "pending"
      return status === "pending"
    })
  }, [cases.data, reviewByCase])

  const handleRandomPending = () => {
    if (pendingCases.length === 0) return
    const idx = Math.floor(Math.random() * pendingCases.length)
    setSelectedCaseId(pendingCases[idx].case_id)
  }

  if (cases.isLoading) {
    return (
      <div className="flex items-center justify-center py-32 text-muted-foreground">
        <Loader2 className="w-5 h-5 animate-spin" />
      </div>
    )
  }

  if (cases.error || !cases.data) {
    return (
      <div className="text-center py-20 text-rose-500">
        Could not load cases.
      </div>
    )
  }

  return (
    <div className="px-6 py-6 max-w-7xl mx-auto w-full">
      {selectedCaseId ? (
        <CaseDetail caseId={selectedCaseId} />
      ) : (
        <div className="space-y-4">
          <FilterBar
            cases={cases.data}
            reviews={reviews.data ?? []}
            pendingCases={pendingCases}
            onPickRandomPending={handleRandomPending}
          />
          <CaseList
            cases={cases.data}
            reviews={reviews.data ?? []}
            selectedCaseId={selectedCaseId}
            onSelectCase={setSelectedCaseId}
          />
        </div>
      )}
    </div>
  )
}
