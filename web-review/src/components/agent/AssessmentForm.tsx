import { Loader2, Plus, X } from "lucide-react"
import { useState } from "react"

import type { JsonValue } from "@/api/agentTypes"
import { Button } from "@/components/ui/Button"
import { cn } from "@/lib/utils"
import { FreeList } from "./SchemaForm"

const inputClass =
  "w-full bg-background border border-input rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring transition"

const URGENCY: Array<{ value: "emergent" | "urgent" | "routine"; label: string }> = [
  { value: "emergent", label: "Emergent" },
  { value: "urgent", label: "Urgent" },
  { value: "routine", label: "Routine" },
]

interface Hypothesis {
  diagnosis: string
  confidence: number | null
}

/**
 * The final assessment, field for field the `submit_assessment` call the agent makes: primary
 * diagnosis (free text, no suggestions), optional ICD-10 code, differential with confidences,
 * overall confidence, urgency, recommendations. The reasoning is asked of physicians only and
 * is stored apart from the assessment.
 */
export function AssessmentForm({
  sending,
  onSubmit,
}: {
  sending: boolean
  onSubmit: (assessment: Record<string, JsonValue>, reasoning: string) => void
}) {
  const [diagnosis, setDiagnosis] = useState("")
  const [icd, setIcd] = useState("")
  const [differential, setDifferential] = useState<Hypothesis[]>([])
  const [confidence, setConfidence] = useState<number | null>(null)
  const [urgency, setUrgency] = useState<string | null>(null)
  const [recommendations, setRecommendations] = useState<string[]>([])
  const [reasoning, setReasoning] = useState("")
  const [confirming, setConfirming] = useState(false)

  const missing = [
    !diagnosis.trim() && "primary diagnosis",
    confidence === null && "confidence",
    !urgency && "urgency",
    !reasoning.trim() && "your reasoning",
  ].filter(Boolean) as string[]
  const ready = missing.length === 0

  const submit = () => {
    const assessment: Record<string, JsonValue> = {
      primary_diagnosis: diagnosis.trim(),
      differential: differential
        .filter((row) => row.diagnosis.trim())
        .map((row) => ({ diagnosis: row.diagnosis.trim(), confidence: row.confidence === null ? null : row.confidence / 100 })),
      confidence: (confidence ?? 0) / 100,
      urgency: urgency ?? "",
      recommendations,
    }
    if (icd.trim()) assessment.icd10_code = icd.trim()
    onSubmit(assessment, reasoning.trim())
  }

  const setRow = (index: number, patch: Partial<Hypothesis>) =>
    setDifferential(differential.map((row, i) => (i === index ? { ...row, ...patch } : row)))

  return (
    <form
      className="space-y-5"
      onSubmit={(e) => {
        e.preventDefault()
        if (ready) setConfirming(true)
      }}
    >
      <div>
        <Label htmlFor="dx" required>Primary diagnosis</Label>
        <input
          id="dx"
          type="text"
          value={diagnosis}
          onChange={(e) => setDiagnosis(e.target.value)}
          autoComplete="off"
          spellCheck={false}
          placeholder="In your own words"
          className={inputClass}
        />
      </div>

      <div>
        <Label htmlFor="icd">ICD-10 code</Label>
        <input
          id="icd"
          type="text"
          value={icd}
          onChange={(e) => setIcd(e.target.value)}
          autoComplete="off"
          spellCheck={false}
          placeholder="e.g. G40.209"
          className={cn(inputClass, "max-w-[11rem] font-mono")}
        />
      </div>

      <div>
        <Label>Differential diagnosis</Label>
        <p className="-mt-0.5 mb-2 text-[13px] text-muted-foreground">Alternatives you still consider, each with how likely you think it is.</p>
        <div className="space-y-2">
          {differential.map((row, i) => (
            <div key={i} className="rounded-md border border-border/80 bg-background p-2.5">
              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={row.diagnosis}
                  onChange={(e) => setRow(i, { diagnosis: e.target.value })}
                  autoComplete="off"
                  aria-label={`Alternative diagnosis ${i + 1}`}
                  placeholder="Alternative diagnosis"
                  className={inputClass}
                />
                <button
                  type="button"
                  onClick={() => setDifferential(differential.filter((_, j) => j !== i))}
                  className="p-1.5 text-muted-foreground hover:text-foreground"
                  aria-label="Remove this alternative"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
              <Percent
                className="mt-2"
                label="Likelihood"
                value={row.confidence}
                onChange={(value) => setRow(i, { confidence: value })}
              />
            </div>
          ))}
        </div>
        {differential.length < 6 && (
          <button
            type="button"
            onClick={() => setDifferential([...differential, { diagnosis: "", confidence: null }])}
            className="mt-2 inline-flex items-center gap-1.5 text-sm text-primary hover:underline"
          >
            <Plus className="w-4 h-4" />
            Add an alternative
          </button>
        )}
      </div>

      <div>
        <Label required>Confidence in the primary diagnosis</Label>
        <Percent label="Confidence" value={confidence} onChange={setConfidence} testId="confidence" />
      </div>

      <div>
        <Label required>Urgency</Label>
        <div className="grid grid-cols-3 gap-2" role="radiogroup" aria-label="Urgency">
          {URGENCY.map(({ value, label }) => (
            <button
              key={value}
              type="button"
              role="radio"
              aria-checked={urgency === value}
              onClick={() => setUrgency(value)}
              className={cn(
                "h-11 rounded-md border text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
                urgency === value
                  ? "bg-primary text-primary-foreground border-primary"
                  : "bg-background border-input hover:border-primary/60",
              )}
            >
              {label}
            </button>
          ))}
        </div>
      </div>

      <div>
        <Label htmlFor="recs">Recommendations</Label>
        <FreeList id="recs" items={recommendations} onChange={setRecommendations} placeholder="One per line: type and press Enter" />
      </div>

      <div className="pt-5 border-t border-border">
        <Label htmlFor="reasoning" required>Reasoning for the diagnosis</Label>
        <p className="-mt-0.5 mb-2 text-[13px] text-muted-foreground">
          What made you settle on it. Kept for the study, apart from the assessment above.
        </p>
        <textarea
          id="reasoning"
          rows={3}
          value={reasoning}
          onChange={(e) => setReasoning(e.target.value)}
          className={cn(inputClass, "resize-y leading-relaxed")}
        />
      </div>

      {confirming ? (
        <div className="rounded-lg border border-primary/40 bg-primary/5 p-3.5" role="alertdialog" aria-label="Confirm the assessment">
          <p className="text-sm font-medium">Submit this assessment and finish the case?</p>
          <p className="mt-0.5 text-[13px] text-muted-foreground">The case is then locked: nothing can be changed or added.</p>
          <div className="mt-3 flex gap-2 justify-end">
            <Button type="button" variant="outline" size="sm" onClick={() => setConfirming(false)} disabled={sending}>
              Keep editing
            </Button>
            <Button type="button" size="sm" onClick={submit} disabled={sending}>
              {sending ? <Loader2 className="w-4 h-4 animate-spin" /> : "Submit and finish"}
            </Button>
          </div>
        </div>
      ) : (
        <div className="flex items-center justify-between gap-3">
          <p className="text-[13px] text-amber-700 dark:text-amber-300" role="status">
            {ready ? "" : `Still needed: ${missing.join(", ")}`}
          </p>
          <Button type="submit" disabled={!ready} className="flex-shrink-0">
            Submit assessment
          </Button>
        </div>
      )}
    </form>
  )
}

function Label({ children, htmlFor, required }: { children: React.ReactNode; htmlFor?: string; required?: boolean }) {
  return (
    <label htmlFor={htmlFor} className="flex items-baseline justify-between gap-2 text-sm font-medium mb-1.5">
      <span>
        {children}
        {required && <span className="text-rose-600 dark:text-rose-400 ml-0.5" aria-hidden>*</span>}
      </span>
      <span className="text-xs font-normal text-muted-foreground">{required ? "required" : "optional"}</span>
    </label>
  )
}

/** A 0–100% slider that starts unset, so a value is always a deliberate choice. */
function Percent({
  label,
  value,
  onChange,
  className,
  testId,
}: {
  label: string
  value: number | null
  onChange: (value: number | null) => void
  className?: string
  testId?: string
}) {
  return (
    <div className={cn("flex items-center gap-3", className)}>
      <input
        type="range"
        min={0}
        max={100}
        step={5}
        value={value ?? 50}
        onChange={(e) => onChange(Number(e.target.value))}
        onPointerDown={() => value === null && onChange(50)}
        aria-label={label}
        data-testid={testId}
        className={cn("flex-1 accent-[var(--color-primary)] h-6", value === null && "opacity-40")}
      />
      <span className="w-20 text-right text-sm tabular-nums">
        {value === null ? <span className="text-muted-foreground">not set</span> : `${value}%`}
      </span>
    </div>
  )
}
