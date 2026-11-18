import { useMemo } from "react"

import type { ReviewStatus } from "@/api/types"
import { useMyReviews } from "@/hooks/useReview"

/** A case counts as reviewed once the reviewer has submitted a decision on it. */
export function isDecided(status: ReviewStatus): boolean {
  return status === "approved" || status === "needs_changes"
}

export interface SetProgress {
  total: number
  /** Cases with a submitted decision. */
  done: number
  /** Cases opened or annotated but not decided yet. */
  started: number
  statusOf: (caseId: string) => ReviewStatus
  /** The first case without a decision (in set order), or null when all are decided. */
  nextCaseId: string | null
  /** 1-based position of `nextCaseId`, or the last position when all are decided. */
  nextNumber: number
  isLoading: boolean
}

/** The reviewer's progress through a review set, in the set's own case order. */
export function useSetProgress(setId: string, caseIds: string[]): SetProgress {
  const reviews = useMyReviews(setId)
  return useMemo(() => {
    const byCase = new Map<string, ReviewStatus>()
    for (const r of reviews.data ?? []) byCase.set(r.case_id, r.status)
    const statusOf = (caseId: string): ReviewStatus => byCase.get(caseId) ?? "pending"
    let done = 0
    let started = 0
    for (const id of caseIds) {
      const s = statusOf(id)
      if (isDecided(s)) done += 1
      else if (s === "in_progress") started += 1
    }
    const nextIndex = caseIds.findIndex((id) => !isDecided(statusOf(id)))
    return {
      total: caseIds.length,
      done,
      started,
      statusOf,
      nextCaseId: nextIndex === -1 ? null : caseIds[nextIndex],
      nextNumber: nextIndex === -1 ? caseIds.length : nextIndex + 1,
      isLoading: reviews.isLoading,
    }
  }, [reviews.data, reviews.isLoading, caseIds])
}
