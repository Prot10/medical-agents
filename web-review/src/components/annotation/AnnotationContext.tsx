import { createContext, useCallback, useContext, useMemo, useState } from "react"

import type {
  CaseReview,
  FieldAnnotation,
  Severity,
} from "@/api/types"

interface OpenPopoverState {
  fieldPath: string
  fieldSnippet?: string
  anchor: HTMLElement
  /** If set, popover opens in edit mode for this annotation. */
  annotationId?: string
}

interface AnnotationContextValue {
  caseId: string
  version: string
  review: CaseReview | undefined
  annotationsByPath: Map<string, FieldAnnotation[]>
  totalAnnotations: number
  openPopover: OpenPopoverState | null
  setOpenPopover: (s: OpenPopoverState | null) => void

  createAnnotation: (input: {
    fieldPath: string
    fieldSnippet?: string
    comment: string
    severity: Severity
  }) => Promise<void>
  updateAnnotation: (
    annotationId: string,
    updates: { comment?: string; severity?: Severity; resolved?: boolean },
  ) => Promise<void>
  deleteAnnotation: (annotationId: string) => Promise<void>
}

const Ctx = createContext<AnnotationContextValue | null>(null)

export function useAnnotationContext(): AnnotationContextValue {
  const value = useContext(Ctx)
  if (!value) {
    throw new Error("useAnnotationContext must be used inside AnnotationProvider")
  }
  return value
}

function generateId(): string {
  // Tiny UUID-ish — server treats it as opaque
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID()
  }
  return `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`
}

export function AnnotationProvider({
  caseId,
  version,
  review,
  onCreate,
  onUpdate,
  onDelete,
  children,
}: {
  caseId: string
  version: string
  review: CaseReview | undefined
  onCreate: (vars: {
    caseId: string
    id: string
    field_path: string
    field_snippet?: string | null
    comment: string
    severity: Severity
  }) => Promise<void>
  onUpdate: (vars: {
    caseId: string
    annotationId: string
    comment?: string
    severity?: Severity
    resolved?: boolean
  }) => Promise<void>
  onDelete: (vars: {
    caseId: string
    annotationId: string
  }) => Promise<void>
  children: React.ReactNode
}) {
  const [openPopover, setOpenPopover] = useState<OpenPopoverState | null>(null)

  const { annotationsByPath, totalAnnotations } = useMemo(() => {
    const map = new Map<string, FieldAnnotation[]>()
    let total = 0
    for (const annotation of review?.field_annotations ?? []) {
      const list = map.get(annotation.field_path) ?? []
      list.push(annotation)
      map.set(annotation.field_path, list)
      total += 1
    }
    return { annotationsByPath: map, totalAnnotations: total }
  }, [review])

  const createAnnotation = useCallback(
    async ({
      fieldPath,
      fieldSnippet,
      comment,
      severity,
    }: {
      fieldPath: string
      fieldSnippet?: string
      comment: string
      severity: Severity
    }) => {
      await onCreate({
        caseId,
        id: generateId(),
        field_path: fieldPath,
        field_snippet: fieldSnippet ?? null,
        comment,
        severity,
      })
    },
    [caseId, onCreate],
  )

  const updateAnnotation = useCallback(
    async (
      annotationId: string,
      updates: { comment?: string; severity?: Severity; resolved?: boolean },
    ) => {
      await onUpdate({ caseId, annotationId, ...updates })
    },
    [caseId, onUpdate],
  )

  const deleteAnnotation = useCallback(
    async (annotationId: string) => {
      await onDelete({ caseId, annotationId })
    },
    [caseId, onDelete],
  )

  const value: AnnotationContextValue = {
    caseId,
    version,
    review,
    annotationsByPath,
    totalAnnotations,
    openPopover,
    setOpenPopover,
    createAnnotation,
    updateAnnotation,
    deleteAnnotation,
  }

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>
}
