import { useState } from "react"
import {
  User, Activity, Heart, Thermometer, Wind, Droplets,
  ChevronDown, ChevronRight, FileText, Stethoscope, ClipboardList, Target, ScanLine,
  Brain, FlaskConical, Zap,
} from "lucide-react"
import { useCaseDetail } from "@/hooks/useCases"
import { useAppStore } from "@/stores/appStore"
import { cn } from "@/lib/utils"
import { GroundTruthPanel } from "@/components/ground-truth/GroundTruthPanel"
import { LabResultsTable } from "@/components/results/LabResultsTable"
import { MRIFindings } from "@/components/results/MRIFindings"
import { ECGReport } from "@/components/results/ECGReport"
import { EEGReport } from "@/components/results/EEGReport"
import { CSFResults } from "@/components/results/CSFResults"
import { Badge } from "@/components/ui/Badge"
import { Card } from "@/components/ui/Card"
import { SectionLabel } from "@/components/ui/SectionLabel"
import { DifficultyStars } from "@/components/ui/DifficultyStars"
import type { Vitals } from "@/api/types"

function VitalCard({ label, value, unit, icon: Icon, abnormal }: {
  label: string; value: number | string; unit: string; icon: React.ElementType; abnormal?: boolean
}) {
  return (
    <div className={cn(
      "flex items-center gap-3 rounded-xl border px-4 py-3 transition-all",
      abnormal ? "border-red-500/50 bg-red-500/5" : "border-border bg-card hover:shadow-sm",
    )}>
      <div className={cn(
        "h-9 w-9 rounded-xl flex items-center justify-center shrink-0",
        abnormal ? "bg-red-500/10" : "bg-primary/10",
      )}>
        <Icon className={cn("h-4.5 w-4.5", abnormal ? "text-red-500" : "text-primary")} />
      </div>
      <div>
        <div className={cn("text-lg font-bold tabular-nums", abnormal && "text-red-500")}>
          {value} <span className="text-sm font-normal text-muted-foreground">{unit}</span>
        </div>
        <div className="text-sm text-muted-foreground">{label}</div>
      </div>
    </div>
  )
}

function isVitalAbnormal(key: string, value: number): boolean {
  const ranges: Record<string, [number, number]> = {
    bp_systolic: [90, 140], bp_diastolic: [60, 90],
    heart_rate: [60, 100], temperature: [36.1, 37.5],
    respiratory_rate: [12, 20], spo2: [95, 100],
  }
  const range = ranges[key]
  return range ? value < range[0] || value > range[1] : false
}

function VitalsGrid({ vitals }: { vitals: Vitals }) {
  const vitalEntries: Array<{ label: string; value: number | string; unit: string; icon: React.ElementType; abnormal: boolean }> = []

  if (vitals.bp_systolic && vitals.bp_diastolic) {
    vitalEntries.push({
      label: "Blood Pressure", value: `${vitals.bp_systolic}/${vitals.bp_diastolic}`, unit: "mmHg", icon: Activity,
      abnormal: isVitalAbnormal("bp_systolic", vitals.bp_systolic) || isVitalAbnormal("bp_diastolic", vitals.bp_diastolic),
    })
  }
  if (vitals.heart_rate) {
    vitalEntries.push({ label: "Heart Rate", value: vitals.heart_rate, unit: "bpm", icon: Heart, abnormal: isVitalAbnormal("heart_rate", vitals.heart_rate) })
  }
  if (vitals.temperature) {
    vitalEntries.push({ label: "Temperature", value: vitals.temperature, unit: "°C", icon: Thermometer, abnormal: isVitalAbnormal("temperature", vitals.temperature) })
  }
  if (vitals.respiratory_rate) {
    vitalEntries.push({ label: "Respiratory Rate", value: vitals.respiratory_rate, unit: "/min", icon: Wind, abnormal: isVitalAbnormal("respiratory_rate", vitals.respiratory_rate) })
  }
  if (vitals.spo2) {
    vitalEntries.push({ label: "SpO2", value: vitals.spo2, unit: "%", icon: Droplets, abnormal: isVitalAbnormal("spo2", vitals.spo2) })
  }

  if (vitalEntries.length === 0) return null

  return (
    <div className={cn("grid gap-3", vitalEntries.length <= 3 ? "grid-cols-3" : "grid-cols-3")}>
      {vitalEntries.map((v) => (
        <VitalCard key={v.label} {...v} />
      ))}
    </div>
  )
}

function NeuroExamSection({ exam }: { exam: Record<string, unknown> }) {
  const [expanded, setExpanded] = useState<Record<string, boolean>>({})

  return (
    <div className="space-y-1.5">
      {Object.entries(exam).map(([key, value]) => {
        if (value == null) return null
        const isOpen = expanded[key]
        const display = typeof value === "string" ? value : JSON.stringify(value, null, 2)
        const isSimple = typeof value === "string" && display.length < 120

        return (
          <div key={key} className="border border-border rounded-xl overflow-hidden">
            <button
              onClick={() => setExpanded((s) => ({ ...s, [key]: !s[key] }))}
              className="w-full flex items-center gap-2 px-3 py-2 text-base hover:bg-accent/50 transition-colors"
            >
              {isOpen ? <ChevronDown className="h-3.5 w-3.5 text-muted-foreground" /> : <ChevronRight className="h-3.5 w-3.5 text-muted-foreground" />}
              <span className="font-medium capitalize">{key.replace(/_/g, " ")}</span>
              {isSimple && !isOpen && (
                <span className="text-base text-muted-foreground truncate ml-auto">{display}</span>
              )}
            </button>
            {isOpen && (
              <div className="px-4 pb-3 text-base text-muted-foreground whitespace-pre-wrap">
                {display}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}

const DIAGNOSTIC_TOOLS: Array<{
  key: string
  toolName: string
  label: string
  icon: React.ElementType
  color: string
}> = [
  { key: "mri", toolName: "analyze_brain_mri", label: "Brain MRI", icon: Brain, color: "text-violet-500" },
  { key: "eeg", toolName: "analyze_eeg", label: "EEG", icon: Zap, color: "text-blue-500" },
  { key: "ecg", toolName: "analyze_ecg", label: "ECG", icon: Heart, color: "text-rose-500" },
  { key: "labs", toolName: "interpret_labs", label: "Lab Results", icon: FlaskConical, color: "text-emerald-500" },
  { key: "csf", toolName: "analyze_csf", label: "CSF Analysis", icon: Droplets, color: "text-cyan-500" },
]

function DiagnosticsSection({ initialOutputs, followupOutputs }: {
  initialOutputs: Record<string, unknown>
  followupOutputs: unknown[]
}) {
  const [expandedSections, setExpandedSections] = useState<Record<string, boolean>>(() => {
    // Auto-expand sections that have data
    const initial: Record<string, boolean> = {}
    for (const tool of DIAGNOSTIC_TOOLS) {
      if (initialOutputs[tool.key]) initial[tool.key] = true
    }
    return initial
  })

  const toggle = (key: string) =>
    setExpandedSections((s) => ({ ...s, [key]: !s[key] }))

  // Collect followup outputs by tool
  const followupsByTool: Record<string, unknown[]> = {}
  if (Array.isArray(followupOutputs)) {
    for (const fo of followupOutputs) {
      const item = fo as Record<string, unknown>
      const toolName = (item.tool_name as string) ?? ""
      const key = DIAGNOSTIC_TOOLS.find((t) => t.toolName === toolName)?.key
      if (key && item.output) {
        if (!followupsByTool[key]) followupsByTool[key] = []
        followupsByTool[key].push(item.output)
      }
    }
  }

  const hasAnyData = DIAGNOSTIC_TOOLS.some((t) => initialOutputs[t.key] || followupsByTool[t.key])

  if (!hasAnyData) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-muted-foreground/30">
        <ScanLine className="h-10 w-10 mb-3" />
        <p className="text-base font-medium">No diagnostic data available</p>
      </div>
    )
  }

  const renderToolResult = (toolName: string, data: unknown) => {
    const d = data as Record<string, unknown>
    switch (toolName) {
      case "analyze_brain_mri": return <MRIFindings data={d} />
      case "analyze_eeg": return <EEGReport data={d} />
      case "analyze_ecg": return <ECGReport data={d} />
      case "interpret_labs": return <LabResultsTable data={d} />
      case "analyze_csf": return <CSFResults data={d} />
      default: return <pre className="text-sm font-mono text-muted-foreground whitespace-pre-wrap">{JSON.stringify(d, null, 2)}</pre>
    }
  }

  return (
    <div className="space-y-3">
      {DIAGNOSTIC_TOOLS.map((tool) => {
        const initialData = initialOutputs[tool.key] as Record<string, unknown> | null | undefined
        const followups = followupsByTool[tool.key]
        if (!initialData && !followups) return null

        const isOpen = expandedSections[tool.key]
        const Icon = tool.icon

        return (
          <div key={tool.key} className="rounded-xl border border-border overflow-hidden">
            <button
              onClick={() => toggle(tool.key)}
              className="w-full flex items-center gap-3 px-4 py-3 hover:bg-accent/30 transition-colors"
            >
              <div className={cn("h-8 w-8 rounded-lg flex items-center justify-center shrink-0", `${tool.color.replace("text-", "bg-")}/15`)}>
                <Icon className={cn("h-4 w-4", tool.color)} />
              </div>
              <span className="text-base font-semibold">{tool.label}</span>
              {followups && (
                <Badge variant="info" className="ml-1">+{followups.length} follow-up</Badge>
              )}
              <span className="ml-auto text-muted-foreground">
                {isOpen ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
              </span>
            </button>

            {isOpen && (
              <div className="px-4 pb-4 space-y-4 border-t border-border/40 pt-3">
                {/* Initial output */}
                {initialData && (
                  <div>
                    {followups && (
                      <div className="text-sm font-semibold text-muted-foreground mb-2 uppercase tracking-wider">Initial</div>
                    )}
                    {renderToolResult(tool.toolName, initialData)}
                  </div>
                )}

                {/* Follow-up outputs */}
                {followups?.map((fo, i) => (
                  <div key={i}>
                    <div className="text-sm font-semibold text-muted-foreground mb-2 uppercase tracking-wider">
                      Follow-up {followups.length > 1 ? `#${i + 1}` : ""}
                    </div>
                    {renderToolResult(tool.toolName, fo)}
                  </div>
                ))}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}

const TABS = [
  { id: "overview" as const, label: "Overview", icon: FileText },
  { id: "history" as const, label: "History", icon: ClipboardList },
  { id: "neuro" as const, label: "Neuro Exam", icon: Stethoscope },
  { id: "diagnostics" as const, label: "Diagnostics", icon: ScanLine },
  { id: "ground_truth" as const, label: "Ground Truth", icon: Target },
]

type TabId = "overview" | "history" | "neuro" | "diagnostics" | "ground_truth"

export function PatientViewer() {
  const { selectedCaseId } = useAppStore()
  const { data: caseDetail, isLoading } = useCaseDetail(selectedCaseId)
  const [activeTab, setActiveTab] = useState<TabId>("overview")

  if (!selectedCaseId) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        <div className="text-center">
          <div className="h-16 w-16 mx-auto mb-4 rounded-2xl bg-primary/10 flex items-center justify-center">
            <User className="h-8 w-8 text-primary/40" />
          </div>
          <p className="text-base font-medium">Select a case</p>
          <p className="text-base text-muted-foreground/60 mt-1">Choose a case from the sidebar to view patient data</p>
        </div>
      </div>
    )
  }

  if (isLoading || !caseDetail) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        <div className="text-base">Loading case...</div>
      </div>
    )
  }

  const { patient, ground_truth } = caseDetail
  const { demographics, vitals, clinical_history } = patient

  return (
    <div className="h-full overflow-y-auto">
      <div className="p-6 space-y-5 max-w-4xl mx-auto">
        {/* Patient header */}
        <div className="flex items-start gap-4">
          <div className="h-12 w-12 rounded-xl bg-primary/10 flex items-center justify-center shrink-0">
            <User className="h-6 w-6 text-primary" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-baseline gap-2">
              <h2 className="text-xl font-bold">{demographics.age}yo {demographics.sex}</h2>
              <span className="text-base text-muted-foreground font-mono">{caseDetail.case_id}</span>
            </div>
            <div className="flex gap-2 mt-2 flex-wrap">
              {demographics.handedness && (
                <span className="inline-flex items-center gap-1.5 text-base px-3 py-1 rounded-lg bg-secondary border border-border font-medium">
                  {demographics.handedness}-handed
                </span>
              )}
              {demographics.ethnicity && (
                <span className="inline-flex items-center gap-1.5 text-base px-3 py-1 rounded-lg bg-secondary border border-border font-medium">
                  {demographics.ethnicity}
                </span>
              )}
              {demographics.bmi && (
                <span className="inline-flex items-center gap-1.5 text-base px-3 py-1 rounded-lg bg-secondary border border-border font-medium">
                  BMI {demographics.bmi}
                </span>
              )}
              <span className="inline-flex items-center gap-1.5 text-base px-3 py-1 rounded-lg bg-primary/10 text-primary border border-primary/20 font-medium">
                {caseDetail.encounter_type}
              </span>
              <span className="inline-flex items-center gap-1.5 text-base px-3 py-1 rounded-lg border border-border text-muted-foreground font-medium">
                <DifficultyStars difficulty={caseDetail.difficulty} size="md" />
              </span>
            </div>
          </div>
        </div>

        {/* Vitals */}
        <VitalsGrid vitals={vitals} />

        {/* Tabs */}
        <div>
          <div className="flex border-b border-border">
            {TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={cn(
                  "flex items-center gap-2 px-4 py-2.5 text-base font-medium transition-colors border-b-2 -mb-px",
                  activeTab === tab.id
                    ? "border-primary text-foreground"
                    : "border-transparent text-muted-foreground hover:text-foreground",
                )}
              >
                <tab.icon className="h-4 w-4" />
                {tab.label}
              </button>
            ))}
          </div>

          <div className="pt-5">
            {activeTab === "overview" && (
              <div className="space-y-4">
                {/* Chief Complaint */}
                <Card accent="primary">
                  <SectionLabel icon={Stethoscope}>Chief Complaint</SectionLabel>
                  <p className="text-base font-semibold">{patient.chief_complaint}</p>
                </Card>

                {/* HPI */}
                <div>
                  <SectionLabel>History of Present Illness</SectionLabel>
                  <p className="text-base text-muted-foreground leading-relaxed">
                    {patient.history_present_illness}
                  </p>
                </div>
              </div>
            )}

            {activeTab === "history" && (
              <div className="space-y-5">
                {clinical_history.past_medical_history.length > 0 && (
                  <div>
                    <SectionLabel>Past Medical History</SectionLabel>
                    <ul className="text-base text-muted-foreground list-disc ml-5 space-y-1">
                      {clinical_history.past_medical_history.map((h, i) => (
                        <li key={i}>{h}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {clinical_history.medications.length > 0 && (
                  <div>
                    <SectionLabel>Medications</SectionLabel>
                    <div className="border border-border rounded-xl overflow-hidden">
                      <table className="w-full text-base">
                        <thead className="bg-secondary/80">
                          <tr>
                            <th className="text-left px-3 py-2 font-medium text-muted-foreground">Drug</th>
                            <th className="text-left px-3 py-2 font-medium text-muted-foreground">Dose</th>
                            <th className="text-left px-3 py-2 font-medium text-muted-foreground">Frequency</th>
                          </tr>
                        </thead>
                        <tbody>
                          {clinical_history.medications.map((m, i) => (
                            <tr key={i} className={cn("border-t border-border/50", i % 2 === 1 && "bg-secondary/30")}>
                              <td className="px-3 py-2 font-medium">{m.drug}</td>
                              <td className="px-3 py-2 text-muted-foreground">{m.dose}</td>
                              <td className="px-3 py-2 text-muted-foreground">{m.frequency}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}

                {clinical_history.allergies.length > 0 && (
                  <div>
                    <SectionLabel>Allergies</SectionLabel>
                    <div className="flex gap-2 flex-wrap">
                      {clinical_history.allergies.map((a, i) => (
                        <Badge key={i} variant="destructive">{a}</Badge>
                      ))}
                    </div>
                  </div>
                )}

                {clinical_history.family_history.length > 0 && (
                  <div>
                    <SectionLabel>Family History</SectionLabel>
                    <ul className="text-base text-muted-foreground list-disc ml-5 space-y-1">
                      {clinical_history.family_history.map((h, i) => (
                        <li key={i}>{h}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {Object.keys(clinical_history.social_history).length > 0 && (
                  <div>
                    <SectionLabel>Social History</SectionLabel>
                    <div className="text-base text-muted-foreground space-y-1">
                      {Object.entries(clinical_history.social_history).map(([k, v]) => (
                        <div key={k}>
                          <span className="font-medium capitalize text-foreground/80">{k.replace(/_/g, " ")}:</span>{" "}
                          {v}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === "neuro" && (
              <NeuroExamSection exam={patient.neurological_exam} />
            )}

            {activeTab === "diagnostics" && (
              <DiagnosticsSection
                initialOutputs={caseDetail.initial_tool_outputs}
                followupOutputs={caseDetail.followup_outputs}
              />
            )}

            {activeTab === "ground_truth" && (
              <GroundTruthPanel groundTruth={ground_truth} />
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
