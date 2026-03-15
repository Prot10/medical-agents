import { useState } from "react"
import {
  User, Activity, Heart, Thermometer, Wind, Droplets,
  ChevronDown, ChevronRight, FileText, Stethoscope, ClipboardList, Target,
} from "lucide-react"
import { useCaseDetail } from "@/hooks/useCases"
import { useAppStore } from "@/stores/appStore"
import { cn } from "@/lib/utils"
import { GroundTruthPanel } from "@/components/ground-truth/GroundTruthPanel"
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

const TABS = [
  { id: "overview" as const, label: "Overview", icon: FileText },
  { id: "history" as const, label: "History", icon: ClipboardList },
  { id: "neuro" as const, label: "Neuro Exam", icon: Stethoscope },
  { id: "ground_truth" as const, label: "Ground Truth", icon: Target },
]

export function PatientViewer() {
  const { selectedCaseId } = useAppStore()
  const { data: caseDetail, isLoading } = useCaseDetail(selectedCaseId)
  const [activeTab, setActiveTab] = useState<"overview" | "history" | "neuro" | "ground_truth">("overview")

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

            {activeTab === "ground_truth" && (
              <GroundTruthPanel groundTruth={ground_truth} />
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
