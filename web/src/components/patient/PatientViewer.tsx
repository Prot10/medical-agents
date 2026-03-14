import { useState } from "react"
import { User, Activity, Heart, Thermometer, Wind, Droplets, ChevronDown, ChevronRight, Eye } from "lucide-react"
import { useCaseDetail } from "@/hooks/useCases"
import { useAppStore } from "@/stores/appStore"
import { cn } from "@/lib/utils"
import { GroundTruthPanel } from "@/components/ground-truth/GroundTruthPanel"
import type { Vitals } from "@/api/types"

function VitalCard({ label, value, unit, icon: Icon, abnormal }: {
  label: string; value: number | string; unit: string; icon: React.ElementType; abnormal?: boolean
}) {
  return (
    <div className={cn(
      "flex items-center gap-2 rounded-lg border px-3 py-2",
      abnormal ? "border-red-500/50 bg-red-500/5" : "border-border bg-secondary/50",
    )}>
      <Icon className={cn("h-4 w-4", abnormal ? "text-red-500" : "text-muted-foreground")} />
      <div>
        <div className={cn("text-sm font-semibold", abnormal && "text-red-500")}>
          {value} <span className="text-xs font-normal text-muted-foreground">{unit}</span>
        </div>
        <div className="text-[10px] text-muted-foreground">{label}</div>
      </div>
    </div>
  )
}

function isVitalAbnormal(key: string, value: number): boolean {
  const ranges: Record<string, [number, number]> = {
    bp_systolic: [90, 140],
    bp_diastolic: [60, 90],
    heart_rate: [60, 100],
    temperature: [36.1, 37.5],
    respiratory_rate: [12, 20],
    spo2: [95, 100],
  }
  const range = ranges[key]
  return range ? value < range[0] || value > range[1] : false
}

function VitalsRow({ vitals }: { vitals: Vitals }) {
  return (
    <div className="grid grid-cols-3 gap-2">
      <VitalCard label="BP" value={`${vitals.bp_systolic}/${vitals.bp_diastolic}`} unit="mmHg" icon={Activity}
        abnormal={isVitalAbnormal("bp_systolic", vitals.bp_systolic) || isVitalAbnormal("bp_diastolic", vitals.bp_diastolic)} />
      <VitalCard label="HR" value={vitals.heart_rate} unit="bpm" icon={Heart}
        abnormal={isVitalAbnormal("heart_rate", vitals.heart_rate)} />
      <VitalCard label="Temp" value={vitals.temperature} unit="°C" icon={Thermometer}
        abnormal={isVitalAbnormal("temperature", vitals.temperature)} />
      <VitalCard label="RR" value={vitals.respiratory_rate} unit="/min" icon={Wind}
        abnormal={isVitalAbnormal("respiratory_rate", vitals.respiratory_rate)} />
      <VitalCard label="SpO2" value={vitals.spo2} unit="%" icon={Droplets}
        abnormal={isVitalAbnormal("spo2", vitals.spo2)} />
    </div>
  )
}

function NeuroExamSection({ exam }: { exam: Record<string, unknown> }) {
  const [expanded, setExpanded] = useState<Record<string, boolean>>({})

  return (
    <div className="space-y-1">
      {Object.entries(exam).map(([key, value]) => {
        if (value == null) return null
        const isOpen = expanded[key]
        const display = typeof value === "string" ? value : JSON.stringify(value, null, 2)
        const isSimple = typeof value === "string" && display.length < 120

        return (
          <div key={key} className="border border-border rounded-md">
            <button
              onClick={() => setExpanded((s) => ({ ...s, [key]: !s[key] }))}
              className="w-full flex items-center gap-2 px-2 py-1 text-xs hover:bg-accent transition-colors"
            >
              {isOpen ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
              <span className="font-medium capitalize">{key.replace(/_/g, " ")}</span>
              {isSimple && !isOpen && (
                <span className="text-muted-foreground truncate ml-auto">{display}</span>
              )}
            </button>
            {isOpen && (
              <div className="px-3 pb-2 text-xs text-muted-foreground whitespace-pre-wrap">
                {display}
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}

export function PatientViewer() {
  const { selectedCaseId, showGroundTruth, toggleGroundTruth } = useAppStore()
  const { data: caseDetail, isLoading } = useCaseDetail(selectedCaseId)
  const [activeTab, setActiveTab] = useState<"history" | "neuro">("history")

  if (!selectedCaseId) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        <div className="text-center">
          <User className="h-12 w-12 mx-auto mb-3 opacity-30" />
          <p className="text-sm">Select a case from the left panel</p>
        </div>
      </div>
    )
  }

  if (isLoading || !caseDetail) {
    return <div className="p-4 text-sm text-muted-foreground">Loading case...</div>
  }

  const { patient, ground_truth } = caseDetail
  const { demographics, vitals, clinical_history } = patient

  return (
    <div className="h-full overflow-y-auto">
      <div className="p-4 space-y-4 max-w-3xl mx-auto">
        {/* Demographics bar */}
        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-sm font-semibold">{demographics.age}yo {demographics.sex}</span>
          {demographics.handedness && (
            <Badge>{demographics.handedness}-handed</Badge>
          )}
          {demographics.ethnicity && <Badge>{demographics.ethnicity}</Badge>}
          {demographics.bmi && <Badge>BMI {demographics.bmi}</Badge>}
          <Badge variant="outline">{caseDetail.encounter_type}</Badge>
          <Badge variant="outline">{caseDetail.difficulty}</Badge>
        </div>

        {/* Vitals */}
        <VitalsRow vitals={vitals} />

        {/* Chief Complaint */}
        <div>
          <SectionLabel>Chief Complaint</SectionLabel>
          <p className="text-sm font-medium">{patient.chief_complaint}</p>
        </div>

        {/* HPI */}
        <div>
          <SectionLabel>History of Present Illness</SectionLabel>
          <p className="text-sm text-muted-foreground leading-relaxed">
            {patient.history_present_illness}
          </p>
        </div>

        {/* Tabs: History / Neuro Exam */}
        <div>
          <div className="flex border-b border-border">
            <TabButton active={activeTab === "history"} onClick={() => setActiveTab("history")}>
              History
            </TabButton>
            <TabButton active={activeTab === "neuro"} onClick={() => setActiveTab("neuro")}>
              Neurological Exam
            </TabButton>
          </div>

          <div className="pt-3">
            {activeTab === "history" && (
              <div className="space-y-3">
                {clinical_history.past_medical_history.length > 0 && (
                  <div>
                    <SectionLabel>Past Medical History</SectionLabel>
                    <ul className="text-xs text-muted-foreground list-disc ml-4 space-y-0.5">
                      {clinical_history.past_medical_history.map((h, i) => (
                        <li key={i}>{h}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {clinical_history.medications.length > 0 && (
                  <div>
                    <SectionLabel>Medications</SectionLabel>
                    <div className="border border-border rounded-md overflow-hidden">
                      <table className="w-full text-xs">
                        <thead className="bg-secondary">
                          <tr>
                            <th className="text-left px-2 py-1 font-medium">Drug</th>
                            <th className="text-left px-2 py-1 font-medium">Dose</th>
                            <th className="text-left px-2 py-1 font-medium">Frequency</th>
                          </tr>
                        </thead>
                        <tbody>
                          {clinical_history.medications.map((m, i) => (
                            <tr key={i} className="border-t border-border/50">
                              <td className="px-2 py-1">{m.drug}</td>
                              <td className="px-2 py-1 text-muted-foreground">{m.dose}</td>
                              <td className="px-2 py-1 text-muted-foreground">{m.frequency}</td>
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
                    <div className="flex gap-1 flex-wrap">
                      {clinical_history.allergies.map((a, i) => (
                        <Badge key={i} variant="destructive">{a}</Badge>
                      ))}
                    </div>
                  </div>
                )}

                {clinical_history.family_history.length > 0 && (
                  <div>
                    <SectionLabel>Family History</SectionLabel>
                    <ul className="text-xs text-muted-foreground list-disc ml-4 space-y-0.5">
                      {clinical_history.family_history.map((h, i) => (
                        <li key={i}>{h}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {Object.keys(clinical_history.social_history).length > 0 && (
                  <div>
                    <SectionLabel>Social History</SectionLabel>
                    <div className="text-xs text-muted-foreground space-y-0.5">
                      {Object.entries(clinical_history.social_history).map(([k, v]) => (
                        <div key={k}>
                          <span className="font-medium capitalize">{k.replace(/_/g, " ")}:</span>{" "}
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
          </div>
        </div>

        {/* Ground Truth Toggle */}
        <div>
          <button
            onClick={toggleGroundTruth}
            className="flex items-center gap-2 text-xs text-muted-foreground hover:text-foreground transition-colors"
          >
            <Eye className="h-3.5 w-3.5" />
            {showGroundTruth ? "Hide" : "Show"} Ground Truth
          </button>
          {showGroundTruth && <GroundTruthPanel groundTruth={ground_truth} />}
        </div>
      </div>
    </div>
  )
}

// Small helper components

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <div className="text-[10px] uppercase tracking-wider font-semibold text-muted-foreground mb-1">
      {children}
    </div>
  )
}

function Badge({ children, variant = "default" }: {
  children: React.ReactNode
  variant?: "default" | "outline" | "destructive"
}) {
  return (
    <span
      className={cn(
        "text-[10px] px-1.5 py-0.5 rounded-full",
        variant === "default" && "bg-secondary text-secondary-foreground",
        variant === "outline" && "border border-border text-muted-foreground",
        variant === "destructive" && "bg-red-500/10 text-red-500",
      )}
    >
      {children}
    </span>
  )
}

function TabButton({ active, onClick, children }: {
  active: boolean; onClick: () => void; children: React.ReactNode
}) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "px-3 py-1.5 text-xs font-medium transition-colors border-b-2",
        active
          ? "border-primary text-foreground"
          : "border-transparent text-muted-foreground hover:text-foreground",
      )}
    >
      {children}
    </button>
  )
}
