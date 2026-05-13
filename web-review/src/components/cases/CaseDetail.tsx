import {
  ArrowLeft,
  ChevronDown,
  ChevronRight,
  Loader2,
} from "lucide-react"
import { useCallback, useMemo, useState } from "react"

import type {
  CaseIndexEntry,
  CaseReviewSummary,
  GroundTruth,
  NeuroBenchCase,
  PatientProfile,
  ReviewStatus,
} from "@/api/types"
import {
  useCaseDetail,
  useCases,
  useCreateAnnotation,
  useCreateComment,
  useDeleteAnnotation,
  useDeleteComment,
  useMyReviews,
  useReview,
  useSetStatus,
  useUpdateAnnotation,
} from "@/hooks/useReview"
import {
  conditionColor,
  conditionLabel,
  conditionShort,
} from "@/lib/conditions"
import { cn } from "@/lib/utils"
import { useReviewStore } from "@/stores/reviewStore"
import { AnnotatableField } from "@/components/annotation/AnnotatableField"
import { AnnotationPopover } from "@/components/annotation/AnnotationPopover"
import { AnnotationProvider } from "@/components/annotation/AnnotationContext"
import { AnnotationSidebar } from "@/components/annotation/AnnotationSidebar"
import { DifficultyStars } from "@/components/ui/DifficultyStars"
import { StatusPill } from "@/components/ui/StatusPill"

export function CaseDetail({ caseId }: { caseId: string }) {
  const version = useReviewStore((s) => s.datasetVersion)
  const setSelectedCaseId = useReviewStore((s) => s.setSelectedCaseId)
  const cases = useCases(version)
  const reviews = useMyReviews(version)
  const caseDetail = useCaseDetail(version, caseId)
  const review = useReview(version, caseId)

  const createAnnotation = useCreateAnnotation(version)
  const updateAnnotation = useUpdateAnnotation(version)
  const deleteAnnotation = useDeleteAnnotation(version)
  const createComment = useCreateComment(version)
  const deleteComment = useDeleteComment(version)
  const setStatus = useSetStatus(version)

  const onCreate = useCallback(
    async (vars: Parameters<typeof createAnnotation.mutateAsync>[0]) => {
      await createAnnotation.mutateAsync(vars)
    },
    [createAnnotation],
  )
  const onUpdate = useCallback(
    async (vars: Parameters<typeof updateAnnotation.mutateAsync>[0]) => {
      await updateAnnotation.mutateAsync(vars)
    },
    [updateAnnotation],
  )
  const onDelete = useCallback(
    async (vars: Parameters<typeof deleteAnnotation.mutateAsync>[0]) => {
      await deleteAnnotation.mutateAsync(vars)
    },
    [deleteAnnotation],
  )

  if (caseDetail.isLoading) {
    return (
      <div className="flex items-center justify-center py-32 text-muted-foreground">
        <Loader2 className="w-5 h-5 animate-spin" />
      </div>
    )
  }
  if (caseDetail.error || !caseDetail.data) {
    return (
      <div className="text-center py-20 text-rose-500">
        Could not load case {caseId}.
      </div>
    )
  }

  const status: ReviewStatus = review.data?.status ?? "pending"

  return (
    <AnnotationProvider
      caseId={caseId}
      version={version}
      review={review.data}
      onCreate={onCreate}
      onUpdate={onUpdate}
      onDelete={onDelete}
    >
      <button
        type="button"
        onClick={() => setSelectedCaseId(null)}
        className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground mb-5"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to all cases
      </button>

      <div className="grid grid-cols-1 xl:grid-cols-[1fr_22rem] gap-5">
        <div className="space-y-5 min-w-0">
          <CaseHeader caseData={caseDetail.data} status={status} />
          <PatientSection patient={caseDetail.data.patient} />
          <NeuroExamSection patient={caseDetail.data.patient} />
          <InitialWorkupSection
            toolOutputs={
              caseDetail.data.initial_tool_outputs as Record<string, unknown> | null
            }
          />
          <PathwaySection followups={caseDetail.data.followup_outputs} />
          <GroundTruthSection groundTruth={caseDetail.data.ground_truth} />
          <MetadataSection metadata={caseDetail.data.metadata} />
        </div>

        <div className="xl:sticky xl:top-20 xl:self-start">
          <AnnotationSidebar
            status={status}
            statusPending={setStatus.isPending}
            onSetStatus={async (s) => {
              await setStatus.mutateAsync({ caseId, status: s })
            }}
            cases={(cases.data ?? []) as CaseIndexEntry[]}
            reviews={(reviews.data ?? []) as CaseReviewSummary[]}
            currentCaseId={caseId}
            onNavigate={(next) => setSelectedCaseId(next)}
            onCreateComment={async (vars) => {
              await createComment.mutateAsync({ caseId, ...vars })
            }}
            onDeleteComment={async (id) => {
              await deleteComment.mutateAsync({ caseId, commentId: id })
            }}
          />
        </div>
      </div>

      <AnnotationPopover />
    </AnnotationProvider>
  )
}

function CaseHeader({
  caseData,
  status,
}: {
  caseData: NeuroBenchCase
  status: ReviewStatus
}) {
  return (
    <div className="rounded-2xl bg-card border border-border p-5">
      <div className="flex items-start justify-between gap-3 flex-wrap">
        <div className="space-y-2">
          <div className="flex items-center gap-2 flex-wrap">
            <span
              className="px-2 py-0.5 rounded-md text-[11px] font-bold tracking-wider"
              style={{
                background: `${conditionColor(caseData.condition)}1a`,
                color: conditionColor(caseData.condition),
              }}
            >
              {conditionShort(caseData.condition)}
            </span>
            <span className="font-mono text-xs tracking-wider text-muted-foreground">
              {caseData.case_id}
            </span>
            <DifficultyStars difficulty={caseData.difficulty} />
            <span className="text-xs text-muted-foreground capitalize">
              {caseData.encounter_type}
            </span>
          </div>
          <h2 className="text-2xl font-semibold tracking-tight">
            {conditionLabel(caseData.condition)}
          </h2>
          <div className="text-sm text-muted-foreground">
            {caseData.patient.demographics.age} y · {caseData.patient.demographics.sex}
            {caseData.patient.demographics.handedness
              ? ` · ${caseData.patient.demographics.handedness}`
              : ""}
          </div>
        </div>
        <StatusPill status={status} />
      </div>
      <AnnotatableField path="patient.chief_complaint" snippet={caseData.patient.chief_complaint}>
        <blockquote className="prose-serif text-lg text-foreground/90 leading-relaxed mt-4 max-w-3xl border-l-2 border-primary/30 pl-4">
          “{caseData.patient.chief_complaint}”
        </blockquote>
      </AnnotatableField>
    </div>
  )
}

function Section({
  title,
  children,
  defaultOpen = true,
  rightSlot,
}: {
  title: string
  children: React.ReactNode
  defaultOpen?: boolean
  rightSlot?: React.ReactNode
}) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <section className="rounded-2xl bg-card border border-border">
      <button
        type="button"
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center justify-between gap-3 px-5 py-3.5 hover:bg-secondary/30 rounded-t-2xl transition-colors"
      >
        <span className="flex items-center gap-2">
          {open ? (
            <ChevronDown className="w-4 h-4 text-muted-foreground" />
          ) : (
            <ChevronRight className="w-4 h-4 text-muted-foreground" />
          )}
          <span className="font-semibold tracking-tight text-sm uppercase text-muted-foreground">
            {title}
          </span>
        </span>
        {rightSlot}
      </button>
      {open && (
        <div className="px-5 pb-5 border-t border-border pt-4">{children}</div>
      )}
    </section>
  )
}

function VitalCard({
  label,
  value,
  unit,
  path,
}: {
  label: string
  value: string | number | undefined
  unit?: string
  path: string
}) {
  if (value === undefined || value === null || value === "") return null
  return (
    <AnnotatableField path={path} attachRight>
      <div className="bg-secondary/40 border border-border rounded-lg px-3 py-2">
        <div className="text-[10px] uppercase tracking-wider text-muted-foreground">
          {label}
        </div>
        <div className="text-sm font-mono tabular-nums">
          {value}
          {unit ? <span className="text-muted-foreground"> {unit}</span> : null}
        </div>
      </div>
    </AnnotatableField>
  )
}

function PatientSection({ patient }: { patient: PatientProfile }) {
  const v = patient.vitals
  const h = patient.clinical_history
  return (
    <Section title="Patient">
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 mb-5">
        <VitalCard
          label="BP"
          value={
            v.bp_systolic && v.bp_diastolic
              ? `${v.bp_systolic}/${v.bp_diastolic}`
              : v.bp_systolic ?? v.bp_diastolic
          }
          unit="mmHg"
          path="patient.vitals.bp_systolic"
        />
        <VitalCard label="HR" value={v.hr} unit="bpm" path="patient.vitals.hr" />
        <VitalCard label="Temp" value={v.temp} unit="°C" path="patient.vitals.temp" />
        <VitalCard label="RR" value={v.rr} unit="/min" path="patient.vitals.rr" />
        <VitalCard label="SpO₂" value={v.spo2} unit="%" path="patient.vitals.spo2" />
        <VitalCard
          label="BMI"
          value={patient.demographics.bmi}
          path="patient.demographics.bmi"
        />
      </div>

      <div className="space-y-4">
        <AnnotatableField
          path="patient.history_present_illness"
          snippet={patient.history_present_illness.slice(0, 200)}
        >
          <div>
            <h4 className="text-xs uppercase tracking-wider text-muted-foreground mb-2">
              History of present illness
            </h4>
            <p className="prose-serif text-[15px] leading-relaxed text-foreground/95 whitespace-pre-wrap pr-6">
              {patient.history_present_illness}
            </p>
          </div>
        </AnnotatableField>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <ListBox
            title="Past medical history"
            items={h.past_medical_history}
            basePath="patient.clinical_history.past_medical_history"
          />
          <ListBox
            title="Allergies"
            items={h.allergies}
            basePath="patient.clinical_history.allergies"
            tone="warning"
          />
          <ListBox
            title="Family history"
            items={h.family_history}
            basePath="patient.clinical_history.family_history"
          />
          <MedicationsBox medications={h.medications} />
          <SocialHistoryBox social={h.social_history} />
        </div>
      </div>
    </Section>
  )
}

function ListBox({
  title,
  items,
  basePath,
  tone = "default",
}: {
  title: string
  items?: string[]
  basePath: string
  tone?: "default" | "warning"
}) {
  if (!items || items.length === 0) return null
  return (
    <div>
      <h4 className="text-xs uppercase tracking-wider text-muted-foreground mb-2">
        {title}
      </h4>
      <ul className="space-y-1">
        {items.map((item, i) => (
          <AnnotatableField
            key={i}
            path={`${basePath}[${i}]`}
            snippet={item}
          >
            <li
              className={cn(
                "text-sm pl-3 border-l-2 leading-relaxed pr-6",
                tone === "warning" ? "border-amber-500/40" : "border-border",
              )}
            >
              {item}
            </li>
          </AnnotatableField>
        ))}
      </ul>
    </div>
  )
}

function MedicationsBox({
  medications,
}: {
  medications?: PatientProfile["clinical_history"]["medications"]
}) {
  if (!medications || medications.length === 0) return null
  return (
    <div>
      <h4 className="text-xs uppercase tracking-wider text-muted-foreground mb-2">
        Medications
      </h4>
      <ul className="space-y-1">
        {medications.map((m, i) => (
          <AnnotatableField
            key={i}
            path={`patient.clinical_history.medications[${i}]`}
            snippet={m.drug}
          >
            <li className="text-sm pl-3 border-l-2 border-border pr-6">
              <span className="font-medium">{m.drug}</span>
              {m.dose && <span className="text-muted-foreground"> · {m.dose}</span>}
              {m.frequency && (
                <span className="text-muted-foreground"> · {m.frequency}</span>
              )}
              {m.indication && (
                <span className="text-xs text-muted-foreground italic block ml-0.5">
                  for {m.indication}
                </span>
              )}
            </li>
          </AnnotatableField>
        ))}
      </ul>
    </div>
  )
}

function SocialHistoryBox({
  social,
}: {
  social?: PatientProfile["clinical_history"]["social_history"]
}) {
  if (!social || Object.keys(social).length === 0) return null
  return (
    <div>
      <h4 className="text-xs uppercase tracking-wider text-muted-foreground mb-2">
        Social history
      </h4>
      <ul className="space-y-1">
        {Object.entries(social).map(([key, value]) => (
          <AnnotatableField
            key={key}
            path={`patient.clinical_history.social_history.${key}`}
            snippet={String(value)}
          >
            <li className="text-sm flex gap-2 pr-6">
              <span className="text-muted-foreground capitalize">
                {key.replace(/_/g, " ")}
              </span>
              <span>{String(value)}</span>
            </li>
          </AnnotatableField>
        ))}
      </ul>
    </div>
  )
}

function NeuroExamSection({ patient }: { patient: PatientProfile }) {
  const exam = patient.neurological_exam
  const sections: Array<{
    key: keyof PatientProfile["neurological_exam"]
    label: string
  }> = [
    { key: "mental_status", label: "Mental status" },
    { key: "cranial_nerves", label: "Cranial nerves" },
    { key: "motor", label: "Motor" },
    { key: "sensory", label: "Sensory" },
    { key: "reflexes", label: "Reflexes" },
    { key: "coordination", label: "Coordination" },
    { key: "gait", label: "Gait" },
    { key: "additional", label: "Additional findings" },
  ]
  const present = sections.filter((s) => exam[s.key])
  if (present.length === 0) return null
  return (
    <Section title="Neurological exam">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {present.map((s) => (
          <AnnotatableField
            key={s.key}
            path={`patient.neurological_exam.${s.key}`}
            snippet={(exam[s.key] ?? "").slice(0, 200)}
          >
            <div className="pr-6">
              <h4 className="text-xs uppercase tracking-wider text-muted-foreground mb-1.5">
                {s.label}
              </h4>
              <p className="text-sm leading-relaxed text-foreground/90 whitespace-pre-wrap">
                {exam[s.key]}
              </p>
            </div>
          </AnnotatableField>
        ))}
      </div>
    </Section>
  )
}

function ToolOutputCard({
  toolName,
  output,
  path,
}: {
  toolName: string
  output: unknown
  path: string
}) {
  const [open, setOpen] = useState(false)
  if (output === null || output === undefined) return null
  const label = toolName.replace(/_/g, " ")
  return (
    <AnnotatableField path={path} attachRight>
      <div className="border border-border rounded-lg overflow-hidden">
        <button
          type="button"
          onClick={() => setOpen((o) => !o)}
          className="w-full flex items-center justify-between gap-2 px-4 py-2.5 bg-secondary/30 hover:bg-secondary/60 transition-colors"
        >
          <span className="flex items-center gap-2">
            {open ? (
              <ChevronDown className="w-3.5 h-3.5 text-muted-foreground" />
            ) : (
              <ChevronRight className="w-3.5 h-3.5 text-muted-foreground" />
            )}
            <span className="font-medium text-sm capitalize">{label}</span>
          </span>
        </button>
        {open && (
          <div className="px-4 py-3 bg-background/40 text-xs">
            <RenderValue value={output} />
          </div>
        )}
      </div>
    </AnnotatableField>
  )
}

function RenderValue({
  value,
  depth = 0,
}: {
  value: unknown
  depth?: number
}): React.ReactElement {
  if (value === null || value === undefined) {
    return <span className="text-muted-foreground italic">none</span>
  }
  if (typeof value === "string") {
    return <span className="whitespace-pre-wrap">{value}</span>
  }
  if (typeof value === "number" || typeof value === "boolean") {
    return <span className="font-mono tabular-nums">{String(value)}</span>
  }
  if (Array.isArray(value)) {
    if (value.length === 0)
      return <span className="text-muted-foreground italic">empty</span>
    return (
      <ul
        className={cn(
          "space-y-1.5",
          depth > 0 && "border-l border-border pl-3",
        )}
      >
        {value.map((item, i) => (
          <li key={i}>
            <RenderValue value={item} depth={depth + 1} />
          </li>
        ))}
      </ul>
    )
  }
  if (typeof value === "object") {
    const entries = Object.entries(value as Record<string, unknown>)
    return (
      <div
        className={cn(
          "space-y-1.5",
          depth > 0 && "border-l border-border pl-3 mt-1",
        )}
      >
        {entries.map(([key, val]) => (
          <div key={key}>
            <span className="text-muted-foreground text-[11px] uppercase tracking-wider">
              {key.replace(/_/g, " ")}
            </span>
            <div className="ml-1 mt-0.5 text-foreground/90">
              <RenderValue value={val} depth={depth + 1} />
            </div>
          </div>
        ))}
      </div>
    )
  }
  return <span>{String(value)}</span>
}

function InitialWorkupSection({
  toolOutputs,
}: {
  toolOutputs: Record<string, unknown> | null
}) {
  const present = useMemo(() => {
    if (!toolOutputs) return [] as Array<[string, unknown]>
    return Object.entries(toolOutputs).filter(
      ([, v]) => v !== null && v !== undefined,
    )
  }, [toolOutputs])
  if (present.length === 0) return null
  return (
    <Section title={`Initial workup (${present.length})`} defaultOpen={false}>
      <div className="space-y-2">
        {present.map(([name, output]) => (
          <ToolOutputCard
            key={name}
            toolName={name}
            output={output}
            path={`initial_tool_outputs.${name}`}
          />
        ))}
      </div>
    </Section>
  )
}

function PathwaySection({
  followups,
}: {
  followups: NeuroBenchCase["followup_outputs"]
}) {
  if (!followups || followups.length === 0) return null
  return (
    <Section
      title={`Diagnostic pathway (${followups.length})`}
      defaultOpen={false}
    >
      <ol className="relative border-l-2 border-primary/30 ml-2 space-y-4 pl-5">
        {followups.map((step, i) => (
          <AnnotatableField
            key={i}
            path={`followup_outputs[${i}]`}
            snippet={`${step.tool_name}: ${step.trigger_action}`}
          >
            <li className="relative pr-6">
              <span className="absolute -left-[27px] top-1 w-3 h-3 rounded-full bg-primary border-2 border-background" />
              <div className="text-xs text-muted-foreground uppercase tracking-wider">
                Step {i + 1} · {step.tool_name}
              </div>
              <div className="text-sm font-medium">{step.trigger_action}</div>
              <details className="mt-1 group">
                <summary className="text-xs text-primary cursor-pointer select-none">
                  Show output
                </summary>
                <div className="mt-2 px-3 py-2 bg-secondary/30 border border-border rounded-md text-xs">
                  <RenderValue value={step.output} />
                </div>
              </details>
            </li>
          </AnnotatableField>
        ))}
      </ol>
    </Section>
  )
}

function GroundTruthSection({ groundTruth }: { groundTruth: GroundTruth }) {
  return (
    <Section title="Ground truth">
      <div className="rounded-xl bg-accent/40 border border-accent/30 p-5 space-y-5">
        <AnnotatableField
          path="ground_truth.primary_diagnosis"
          snippet={groundTruth.primary_diagnosis}
        >
          <div className="pr-6">
            <div className="text-xs uppercase tracking-wider text-muted-foreground mb-1">
              Primary diagnosis
            </div>
            <div className="text-2xl font-semibold tracking-tight">
              {groundTruth.primary_diagnosis}
            </div>
            {groundTruth.icd_code && (
              <span className="inline-block mt-1 px-2 py-0.5 rounded-full bg-background border border-border text-[11px] font-mono">
                ICD {groundTruth.icd_code}
              </span>
            )}
          </div>
        </AnnotatableField>

        {groundTruth.differential && groundTruth.differential.length > 0 && (
          <div>
            <h4 className="text-xs uppercase tracking-wider text-muted-foreground mb-2">
              Differential
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {groundTruth.differential.map((d, i) => (
                <AnnotatableField
                  key={i}
                  path={`ground_truth.differential[${i}]`}
                  snippet={d.diagnosis}
                  attachRight
                >
                  <div className="bg-card border border-border rounded-lg p-3 border-l-4 border-l-amber-500/60">
                    <div className="flex items-center justify-between gap-2 mb-1 pr-4">
                      <span className="font-medium text-sm">{d.diagnosis}</span>
                      <span className="text-[11px] uppercase tracking-wider text-muted-foreground">
                        {d.likelihood}
                      </span>
                    </div>
                    {d.key_distinguishing && (
                      <p className="text-xs text-muted-foreground leading-relaxed">
                        {d.key_distinguishing}
                      </p>
                    )}
                  </div>
                </AnnotatableField>
              ))}
            </div>
          </div>
        )}

        {groundTruth.optimal_actions && groundTruth.optimal_actions.length > 0 && (
          <div>
            <h4 className="text-xs uppercase tracking-wider text-muted-foreground mb-2">
              Optimal actions
            </h4>
            <ol className="space-y-1.5">
              {groundTruth.optimal_actions.map((a, i) => (
                <AnnotatableField
                  key={a.step}
                  path={`ground_truth.optimal_actions[${i}]`}
                  snippet={a.action}
                >
                  <li className="flex items-start gap-3 text-sm leading-relaxed pr-6">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-primary/15 text-primary text-xs font-semibold flex items-center justify-center">
                      {a.step}
                    </span>
                    <span>
                      {a.action}
                      {a.tool_name && (
                        <span className="ml-2 px-1.5 py-0.5 rounded bg-secondary text-[10px] font-mono">
                          {a.tool_name}
                        </span>
                      )}
                      {a.category === "contraindicated" && (
                        <span className="ml-2 text-xs text-rose-500">
                          contraindicated
                        </span>
                      )}
                    </span>
                  </li>
                </AnnotatableField>
              ))}
            </ol>
          </div>
        )}

        {groundTruth.critical_actions &&
          groundTruth.critical_actions.length > 0 && (
            <ListGroup
              title="Critical actions (musts)"
              tone="success"
              items={groundTruth.critical_actions}
              basePath="ground_truth.critical_actions"
            />
          )}

        {groundTruth.contraindicated_actions &&
          groundTruth.contraindicated_actions.length > 0 && (
            <ListGroup
              title="Contraindicated"
              tone="danger"
              items={groundTruth.contraindicated_actions}
              basePath="ground_truth.contraindicated_actions"
            />
          )}

        {groundTruth.red_herrings && groundTruth.red_herrings.length > 0 && (
          <div>
            <h4 className="text-xs uppercase tracking-wider text-muted-foreground mb-2">
              Red herrings
            </h4>
            <div className="space-y-2">
              {groundTruth.red_herrings.map((rh, i) => (
                <AnnotatableField
                  key={i}
                  path={`ground_truth.red_herrings[${i}]`}
                  snippet={rh.data_point}
                  attachRight
                >
                  <div className="border-2 border-dashed border-amber-500/40 rounded-lg p-3 bg-amber-500/5 pr-6">
                    <div className="text-sm font-medium">{rh.data_point}</div>
                    <div className="text-[11px] uppercase tracking-wider text-muted-foreground mt-1.5">
                      Intended effect
                    </div>
                    <p className="text-sm text-foreground/90">
                      {rh.intended_effect}
                    </p>
                    <div className="text-[11px] uppercase tracking-wider text-muted-foreground mt-2">
                      Correct interpretation
                    </div>
                    <p className="text-sm text-foreground/90">
                      {rh.correct_interpretation}
                    </p>
                  </div>
                </AnnotatableField>
              ))}
            </div>
          </div>
        )}

        {groundTruth.key_reasoning_points &&
          groundTruth.key_reasoning_points.length > 0 && (
            <div className="rounded-lg bg-primary/5 border border-primary/15 p-4">
              <h4 className="text-xs uppercase tracking-wider text-primary mb-2">
                Teaching pearls
              </h4>
              <ul className="space-y-1.5 prose-serif text-sm leading-relaxed">
                {groundTruth.key_reasoning_points.map((point, i) => (
                  <AnnotatableField
                    key={i}
                    path={`ground_truth.key_reasoning_points[${i}]`}
                    snippet={point}
                  >
                    <li className="pl-4 border-l-2 border-primary/30 pr-6">
                      {point}
                    </li>
                  </AnnotatableField>
                ))}
              </ul>
            </div>
          )}
      </div>
    </Section>
  )
}

function ListGroup({
  title,
  items,
  tone,
  basePath,
}: {
  title: string
  items: string[]
  tone: "success" | "danger"
  basePath: string
}) {
  const toneClasses =
    tone === "success"
      ? "border-emerald-500/40 bg-emerald-500/5 text-emerald-700 dark:text-emerald-300"
      : "border-rose-500/40 bg-rose-500/5 text-rose-700 dark:text-rose-300"
  return (
    <div>
      <h4 className="text-xs uppercase tracking-wider text-muted-foreground mb-2">
        {title}
      </h4>
      <ul className="grid grid-cols-1 md:grid-cols-2 gap-2">
        {items.map((item, i) => (
          <AnnotatableField
            key={i}
            path={`${basePath}[${i}]`}
            snippet={item}
            attachRight
          >
            <li
              className={cn(
                "text-sm p-2.5 border rounded-md leading-relaxed pr-6",
                toneClasses,
              )}
            >
              {item}
            </li>
          </AnnotatableField>
        ))}
      </ul>
    </div>
  )
}

function MetadataSection({ metadata }: { metadata: Record<string, unknown> }) {
  if (!metadata || Object.keys(metadata).length === 0) return null
  return (
    <Section title="Metadata" defaultOpen={false}>
      <div className="text-xs font-mono whitespace-pre-wrap break-words bg-secondary/30 border border-border rounded-md p-3 max-h-80 overflow-y-auto">
        {JSON.stringify(metadata, null, 2)}
      </div>
    </Section>
  )
}
