import {
  useMutation,
  useQuery,
  useQueryClient,
  type UseMutationOptions,
} from "@tanstack/react-query"

import {
  deleteJSON,
  fetchJSON,
  patchJSON,
  postJSON,
  putJSON,
} from "@/api/client"
import type {
  AdminAgreement,
  AdminReviewerProgress,
  CaseDiff,
  CaseIndexEntry,
  CaseReview,
  CaseReviewSummary,
  DatasetSummary,
  FieldHotspot,
  Methodology,
  MyProgress,
  NeuroBenchCase,
  ReviewStatus,
  ReviewerProfile,
  Severity,
} from "@/api/types"
import { useReviewStore } from "@/stores/reviewStore"

// ---------- Query keys --------------------------------------------------

const QK = {
  me: () => ["me"] as const,
  datasets: () => ["datasets"] as const,
  cases: (version: string) => ["datasets", version, "cases"] as const,
  caseDetail: (version: string, caseId: string) =>
    ["datasets", version, "cases", caseId] as const,
  myReviews: (version: string, code: string) =>
    ["datasets", version, "reviews", code] as const,
  review: (version: string, caseId: string, code: string) =>
    ["datasets", version, "reviews", caseId, code] as const,
  progress: (version: string, code: string) =>
    ["datasets", version, "progress", code] as const,
  methodology: (version: string) => ["datasets", version, "methodology"] as const,
  adminAgreement: (version: string) => ["admin", version, "agreement"] as const,
  adminProgress: (version: string) => ["admin", version, "progress"] as const,
  adminHotspots: (version: string) => ["admin", version, "hotspots"] as const,
  adminDiff: (version: string, caseId: string) =>
    ["admin", version, "diff", caseId] as const,
}

// ---------- Identity ----------------------------------------------------

export function useReviewerProfile() {
  const profile = useReviewStore((s) => s.profile)
  return useQuery({
    queryKey: QK.me(),
    enabled: !!profile,
    queryFn: () => fetchJSON<ReviewerProfile>("/reviewers/me"),
    staleTime: 5 * 60 * 1000,
  })
}

export async function validateAndLoadProfile(code: string): Promise<ReviewerProfile> {
  return fetchJSON<ReviewerProfile>("/reviewers/me", {
    headers: { "X-Reviewer-Code": code },
    skipAuth: true,
  })
}

// ---------- Datasets + cases (read-only) -------------------------------

export function useDatasets() {
  return useQuery({
    queryKey: QK.datasets(),
    queryFn: () => fetchJSON<DatasetSummary[]>("/datasets"),
    staleTime: 60 * 1000,
  })
}

export function useCases(version: string) {
  return useQuery({
    queryKey: QK.cases(version),
    queryFn: () => fetchJSON<CaseIndexEntry[]>(`/datasets/${version}/cases`),
    staleTime: 60 * 1000,
  })
}

export function useCaseDetail(version: string, caseId: string | null) {
  return useQuery({
    queryKey: QK.caseDetail(version, caseId ?? ""),
    enabled: !!caseId,
    queryFn: () =>
      fetchJSON<NeuroBenchCase>(`/datasets/${version}/cases/${caseId}`),
    staleTime: Infinity,
  })
}

// ---------- Reviews -----------------------------------------------------

export function useMyReviews(version: string) {
  const code = useReviewStore((s) => s.profile?.code ?? "")
  return useQuery({
    queryKey: QK.myReviews(version, code),
    enabled: !!code,
    queryFn: () =>
      fetchJSON<CaseReviewSummary[]>(`/datasets/${version}/reviews`),
    staleTime: 10 * 1000,
  })
}

export function useReview(version: string, caseId: string | null) {
  const code = useReviewStore((s) => s.profile?.code ?? "")
  return useQuery({
    queryKey: QK.review(version, caseId ?? "", code),
    enabled: !!caseId && !!code,
    queryFn: () =>
      fetchJSON<CaseReview>(`/datasets/${version}/reviews/${caseId}`),
    staleTime: 10 * 1000,
  })
}

function applyMutationResult(
  queryClient: ReturnType<typeof useQueryClient>,
  version: string,
  caseId: string,
  code: string,
  data: CaseReview,
) {
  // The server returns the full updated CaseReview — write it straight into
  // the cache instead of refetching. List/progress queries still invalidate
  // so aggregate counts stay correct.
  queryClient.setQueryData(QK.review(version, caseId, code), data)
  queryClient.invalidateQueries({ queryKey: QK.myReviews(version, code) })
  queryClient.invalidateQueries({ queryKey: QK.progress(version, code) })
}

export function useSetStatus(version: string) {
  const queryClient = useQueryClient()
  const code = useReviewStore((s) => s.profile?.code ?? "")
  return useMutation({
    mutationFn: ({
      caseId,
      status,
    }: {
      caseId: string
      status: ReviewStatus
    }) =>
      patchJSON<CaseReview>(
        `/datasets/${version}/reviews/${caseId}/status`,
        { status },
      ),
    onSuccess: (data, vars) => applyMutationResult(queryClient, version, vars.caseId, code, data),
  })
}

export function useCreateAnnotation(version: string) {
  const queryClient = useQueryClient()
  const code = useReviewStore((s) => s.profile?.code ?? "")
  return useMutation({
    mutationFn: ({
      caseId,
      ...body
    }: {
      caseId: string
      id: string
      field_path: string
      field_snippet?: string | null
      comment: string
      severity: Severity
    }) =>
      postJSON<CaseReview>(
        `/datasets/${version}/reviews/${caseId}/annotations`,
        body,
      ),
    onSuccess: (data, vars) => applyMutationResult(queryClient, version, vars.caseId, code, data),
  })
}

export function useUpdateAnnotation(version: string) {
  const queryClient = useQueryClient()
  const code = useReviewStore((s) => s.profile?.code ?? "")
  return useMutation({
    mutationFn: ({
      caseId,
      annotationId,
      ...body
    }: {
      caseId: string
      annotationId: string
      comment?: string
      severity?: Severity
      resolved?: boolean
    }) =>
      putJSON<CaseReview>(
        `/datasets/${version}/reviews/${caseId}/annotations/${annotationId}`,
        body,
      ),
    onSuccess: (data, vars) => applyMutationResult(queryClient, version, vars.caseId, code, data),
  })
}

export function useDeleteAnnotation(version: string) {
  const queryClient = useQueryClient()
  const code = useReviewStore((s) => s.profile?.code ?? "")
  return useMutation({
    mutationFn: ({
      caseId,
      annotationId,
    }: {
      caseId: string
      annotationId: string
    }) =>
      deleteJSON<CaseReview>(
        `/datasets/${version}/reviews/${caseId}/annotations/${annotationId}`,
      ),
    onSuccess: (data, vars) => applyMutationResult(queryClient, version, vars.caseId, code, data),
  })
}

export function useCreateComment(version: string) {
  const queryClient = useQueryClient()
  const code = useReviewStore((s) => s.profile?.code ?? "")
  return useMutation({
    mutationFn: ({
      caseId,
      ...body
    }: {
      caseId: string
      id: string
      comment: string
      severity: Severity
    }) =>
      postJSON<CaseReview>(
        `/datasets/${version}/reviews/${caseId}/comments`,
        body,
      ),
    onSuccess: (data, vars) => applyMutationResult(queryClient, version, vars.caseId, code, data),
  })
}

export function useUpdateComment(version: string) {
  const queryClient = useQueryClient()
  const code = useReviewStore((s) => s.profile?.code ?? "")
  return useMutation({
    mutationFn: ({
      caseId,
      commentId,
      ...body
    }: {
      caseId: string
      commentId: string
      comment?: string
      severity?: Severity
    }) =>
      putJSON<CaseReview>(
        `/datasets/${version}/reviews/${caseId}/comments/${commentId}`,
        body,
      ),
    onSuccess: (data, vars) => applyMutationResult(queryClient, version, vars.caseId, code, data),
  })
}

export function useDeleteComment(version: string) {
  const queryClient = useQueryClient()
  const code = useReviewStore((s) => s.profile?.code ?? "")
  return useMutation({
    mutationFn: ({
      caseId,
      commentId,
    }: {
      caseId: string
      commentId: string
    }) =>
      deleteJSON<CaseReview>(
        `/datasets/${version}/reviews/${caseId}/comments/${commentId}`,
      ),
    onSuccess: (data, vars) => applyMutationResult(queryClient, version, vars.caseId, code, data),
  })
}

export function useHeartbeat(
  options?: UseMutationOptions<unknown, Error, { version: string; caseId: string; seconds: number }>,
) {
  return useMutation({
    mutationFn: ({ version, caseId, seconds }) =>
      postJSON(`/datasets/${version}/reviews/${caseId}/heartbeat`, { seconds }),
    ...options,
  })
}

// ---------- Progress + methodology -------------------------------------

export function useMyProgress(version: string) {
  const code = useReviewStore((s) => s.profile?.code ?? "")
  return useQuery({
    queryKey: QK.progress(version, code),
    enabled: !!code,
    queryFn: () => fetchJSON<MyProgress>(`/datasets/${version}/progress`),
    staleTime: 10 * 1000,
  })
}

export function useMethodology(version: string) {
  return useQuery({
    queryKey: QK.methodology(version),
    queryFn: () => fetchJSON<Methodology>(`/datasets/${version}/methodology`),
    staleTime: 5 * 60 * 1000,
  })
}

// ---------- Admin ------------------------------------------------------

export function useAdminAgreement(version: string) {
  const role = useReviewStore((s) => s.profile?.role)
  return useQuery({
    queryKey: QK.adminAgreement(version),
    enabled: role === "admin",
    queryFn: () =>
      fetchJSON<AdminAgreement>(`/admin/datasets/${version}/agreement`),
    staleTime: 30 * 1000,
  })
}

export function useAdminProgress(version: string) {
  const role = useReviewStore((s) => s.profile?.role)
  return useQuery({
    queryKey: QK.adminProgress(version),
    enabled: role === "admin",
    queryFn: () =>
      fetchJSON<AdminReviewerProgress[]>(`/admin/datasets/${version}/progress`),
    staleTime: 30 * 1000,
  })
}

export function useAdminHotspots(version: string) {
  const role = useReviewStore((s) => s.profile?.role)
  return useQuery({
    queryKey: QK.adminHotspots(version),
    enabled: role === "admin",
    queryFn: () =>
      fetchJSON<FieldHotspot[]>(`/admin/datasets/${version}/field-hotspots`),
    staleTime: 30 * 1000,
  })
}

export function useAdminCaseDiff(version: string, caseId: string | null) {
  const role = useReviewStore((s) => s.profile?.role)
  return useQuery({
    queryKey: QK.adminDiff(version, caseId ?? ""),
    enabled: role === "admin" && !!caseId,
    queryFn: () =>
      fetchJSON<CaseDiff>(`/admin/datasets/${version}/cases/${caseId}/diff`),
    staleTime: 30 * 1000,
  })
}
