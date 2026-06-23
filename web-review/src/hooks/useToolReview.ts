import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

import { deleteJSON, fetchJSON, patchJSON, postJSON, putJSON } from "@/api/client"
import type {
  AdminToolReviewSummary,
  ProposedTool,
  Severity,
  ToolCatalog,
  ToolReview,
} from "@/api/types"
import { useReviewStore } from "@/stores/reviewStore"

// ---------- Query keys --------------------------------------------------

const QK = {
  catalog: (version: string) => ["datasets", version, "tool-catalog"] as const,
  review: (version: string, code: string) =>
    ["datasets", version, "tool-review", code] as const,
  adminSummary: (version: string) => ["admin", version, "tool-review"] as const,
}

// ---------- Catalog (read-only) ----------------------------------------

export function useToolCatalog(version: string) {
  const code = useReviewStore((s) => s.profile?.code ?? "")
  return useQuery({
    queryKey: QK.catalog(version),
    enabled: !!code,
    queryFn: () => fetchJSON<ToolCatalog>(`/datasets/${version}/tool-catalog`),
    staleTime: 5 * 60 * 1000,
  })
}

// ---------- Per-reviewer tool review -----------------------------------

export function useToolReview(version: string) {
  const code = useReviewStore((s) => s.profile?.code ?? "")
  return useQuery({
    queryKey: QK.review(version, code),
    enabled: !!code,
    queryFn: () => fetchJSON<ToolReview>(`/datasets/${version}/tool-review`),
    staleTime: 10 * 1000,
  })
}

function useInvalidate(version: string) {
  const queryClient = useQueryClient()
  const code = useReviewStore((s) => s.profile?.code ?? "")
  return () =>
    queryClient.invalidateQueries({ queryKey: QK.review(version, code) })
}

export function useSetToolReviewComplete(version: string) {
  const invalidate = useInvalidate(version)
  return useMutation({
    mutationFn: (completed: boolean) =>
      patchJSON<ToolReview>(`/datasets/${version}/tool-review/complete`, {
        completed,
      }),
    onSuccess: invalidate,
  })
}

// ---------- Coverage annotations (reuse FieldAnnotation shape) ----------

export function useCreateToolAnnotation(version: string) {
  const invalidate = useInvalidate(version)
  return useMutation({
    mutationFn: (body: {
      id: string
      field_path: string
      field_snippet?: string | null
      comment: string
      severity: Severity
    }) =>
      postJSON<ToolReview>(`/datasets/${version}/tool-review/annotations`, body),
    onSuccess: invalidate,
  })
}

export function useUpdateToolAnnotation(version: string) {
  const invalidate = useInvalidate(version)
  return useMutation({
    mutationFn: ({
      annotationId,
      ...body
    }: {
      annotationId: string
      comment?: string
      severity?: Severity
      resolved?: boolean
    }) =>
      putJSON<ToolReview>(
        `/datasets/${version}/tool-review/annotations/${annotationId}`,
        body,
      ),
    onSuccess: invalidate,
  })
}

export function useDeleteToolAnnotation(version: string) {
  const invalidate = useInvalidate(version)
  return useMutation({
    mutationFn: (annotationId: string) =>
      deleteJSON<ToolReview>(
        `/datasets/${version}/tool-review/annotations/${annotationId}`,
      ),
    onSuccess: invalidate,
  })
}

// ---------- Proposed tools ---------------------------------------------

export function useCreateProposal(version: string) {
  const invalidate = useInvalidate(version)
  return useMutation({
    mutationFn: (body: {
      id: string
      name: string
      description: string
      rationale?: string
      target_conditions?: string[]
      modality?: string | null
    }) => postJSON<ToolReview>(`/datasets/${version}/tool-review/proposals`, body),
    onSuccess: invalidate,
  })
}

export function useUpdateProposal(version: string) {
  const invalidate = useInvalidate(version)
  return useMutation({
    mutationFn: ({
      proposalId,
      ...body
    }: {
      proposalId: string
    } & Partial<Pick<ProposedTool, "name" | "description" | "rationale" | "target_conditions" | "modality">>) =>
      putJSON<ToolReview>(
        `/datasets/${version}/tool-review/proposals/${proposalId}`,
        body,
      ),
    onSuccess: invalidate,
  })
}

export function useDeleteProposal(version: string) {
  const invalidate = useInvalidate(version)
  return useMutation({
    mutationFn: (proposalId: string) =>
      deleteJSON<ToolReview>(
        `/datasets/${version}/tool-review/proposals/${proposalId}`,
      ),
    onSuccess: invalidate,
  })
}

// ---------- Admin -------------------------------------------------------

export function useAdminToolReview(version: string) {
  const role = useReviewStore((s) => s.profile?.role)
  return useQuery({
    queryKey: QK.adminSummary(version),
    enabled: role === "admin",
    queryFn: () =>
      fetchJSON<AdminToolReviewSummary>(`/admin/datasets/${version}/tool-review`),
    staleTime: 30 * 1000,
  })
}
