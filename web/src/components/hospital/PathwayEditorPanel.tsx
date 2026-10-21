import { useState, useEffect, useCallback } from "react"
import {
  FileText, Plus, Trash2, Save, X, Clock, Shield, AlertTriangle, ChevronDown,
} from "lucide-react"
import { useQueryClient } from "@tanstack/react-query"
import { useAppStore } from "@/stores/appStore"
import { useHospitalRules } from "@/hooks/useCases"
import { api } from "@/api/client"
import { cn } from "@/lib/utils"
import type { PathwayDetail, PathwayStep } from "@/api/types"

const TOOL_ACTIONS = [
  "analyze_eeg", "analyze_brain_mri", "analyze_ecg",
  "interpret_labs", "analyze_csf", "search_medical_literature", "check_drug_interactions",
  "order_ct_scan", "order_echocardiogram", "order_cardiac_monitoring",
  "order_advanced_imaging", "order_specialized_test",
]

const TIMINGS = ["immediate", "within_24h", "initial", "before_treatment", "before_discharge", "if_treatment_started"]

function emptyStep(): PathwayStep {
  return { action: TOOL_ACTIONS[0], timing: "immediate", mandatory: true, condition: null, details: {} }
}

function emptyPathway(): PathwayDetail {
  return { name: "", description: "", triggers: [], steps: [emptyStep()], contraindicated: [] }
}

export function PathwayEditorPanel() {
  const {
    rulesHospitalId, selectedPathwayIndex, isCreatingPathway,
    selectPathway, setIsCreatingPathway,
  } = useAppStore()
  const { data: rulesData } = useHospitalRules(rulesHospitalId)
  const queryClient = useQueryClient()

  const pathway = selectedPathwayIndex !== null ? rulesData?.pathways[selectedPathwayIndex] ?? null : null
  const isEditing = pathway !== null || isCreatingPathway

  const [editData, setEditData] = useState<PathwayDetail>(emptyPathway())
  const [triggerInput, setTriggerInput] = useState("")
  const [saving, setSaving] = useState(false)
  const [deleteConfirm, setDeleteConfirm] = useState(false)
  const [dirty, setDirty] = useState(false)

  // Load pathway data when selection changes
  useEffect(() => {
    if (isCreatingPathway) {
      setEditData(emptyPathway())
      setDirty(false)
      setDeleteConfirm(false)
    } else if (pathway) {
      setEditData(structuredClone(pathway))
      setDirty(false)
      setDeleteConfirm(false)
    }
  }, [pathway, isCreatingPathway])

  const invalidate = useCallback(() => {
    queryClient.invalidateQueries({ queryKey: ["hospital-rules", rulesHospitalId] })
    queryClient.invalidateQueries({ queryKey: ["hospitals"] })
  }, [queryClient, rulesHospitalId])

  const handleSave = async () => {
    setSaving(true)
    try {
      if (isCreatingPathway) {
        await api.createPathway(rulesHospitalId, editData)
        setIsCreatingPathway(false)
      } else if (selectedPathwayIndex !== null) {
        await api.updatePathway(rulesHospitalId, selectedPathwayIndex, editData)
      }
      invalidate()
      setDirty(false)
    } catch (err) {
      console.error("Failed to save:", err)
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    if (selectedPathwayIndex === null) return
    if (!deleteConfirm) { setDeleteConfirm(true); return }
    setSaving(true)
    try {
      await api.deletePathway(rulesHospitalId, selectedPathwayIndex)
      invalidate()
      selectPathway(null)
    } catch (err) {
      console.error("Failed to delete:", err)
    } finally {
      setSaving(false)
      setDeleteConfirm(false)
    }
  }

  const update = <K extends keyof PathwayDetail>(key: K, value: PathwayDetail[K]) => {
    setEditData((d) => ({ ...d, [key]: value }))
    setDirty(true)
  }

  const updateStep = (idx: number, field: keyof PathwayStep, value: unknown) => {
    setEditData((d) => {
      const steps = [...d.steps]
      steps[idx] = { ...steps[idx], [field]: value }
      return { ...d, steps }
    })
    setDirty(true)
  }

  const removeStep = (idx: number) => {
    setEditData((d) => ({ ...d, steps: d.steps.filter((_, i) => i !== idx) }))
    setDirty(true)
  }

  const addTrigger = () => {
    if (!triggerInput.trim()) return
    const newT = triggerInput.split(",").map((t) => t.trim()).filter((t) => t && !editData.triggers.includes(t))
    update("triggers", [...editData.triggers, ...newT])
    setTriggerInput("")
  }

  if (!isEditing) {
    return (
      <div className="h-full flex items-center justify-center text-muted-foreground">
        <div className="text-center space-y-2">
          <Shield className="h-12 w-12 mx-auto opacity-20" />
          <p className="text-lg font-medium">Hospital Rules</p>
          <p className="text-sm">Select a pathway from the sidebar to view or edit it.</p>
        </div>
      </div>
    )
  }

  const inputClass =
    "w-full text-sm bg-muted/50 border border-border rounded-lg px-3 py-2 text-foreground focus:outline-none focus:ring-1 focus:ring-ring placeholder:text-muted-foreground/50"

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-6 py-3 border-b border-border bg-card/50">
        <div className="flex items-center gap-3">
          <FileText className="h-5 w-5 text-primary" />
          <div>
            <h2 className="text-base font-semibold">
              {isCreatingPathway ? "New Pathway" : editData.name || "Untitled"}
            </h2>
            <p className="text-xs text-muted-foreground">{rulesData?.name}</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          {!isCreatingPathway && (
            <button
              onClick={handleDelete}
              className={cn(
                "flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium rounded-lg transition-colors",
                deleteConfirm
                  ? "bg-red-500 text-white hover:bg-red-600"
                  : "text-red-500/70 hover:text-red-500 hover:bg-red-500/10",
              )}
            >
              <Trash2 className="h-3.5 w-3.5" />
              {deleteConfirm ? "Confirm Delete" : "Delete"}
            </button>
          )}
          <button
            onClick={() => { selectPathway(null); setIsCreatingPathway(false) }}
            className="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-muted-foreground hover:text-foreground rounded-lg hover:bg-accent transition-colors"
          >
            <X className="h-3.5 w-3.5" />
            Close
          </button>
          <button
            onClick={handleSave}
            disabled={saving || !editData.name.trim()}
            className={cn(
              "flex items-center gap-1.5 px-4 py-1.5 text-sm font-medium rounded-lg transition-colors",
              saving || !editData.name.trim()
                ? "bg-muted text-muted-foreground cursor-not-allowed"
                : "bg-primary text-primary-foreground hover:bg-primary/90",
            )}
          >
            <Save className="h-3.5 w-3.5" />
            {saving ? "Saving..." : dirty ? "Save *" : "Save"}
          </button>
        </div>
      </div>

      {/* Scrollable content */}
      <div className="flex-1 overflow-y-auto px-6 py-5 space-y-6">
        {/* Name & Description */}
        <div className="grid grid-cols-1 gap-4">
          <div className="space-y-1.5">
            <label className="text-xs uppercase tracking-wider font-semibold text-muted-foreground">
              Pathway Name
            </label>
            <input
              type="text"
              value={editData.name}
              onChange={(e) => update("name", e.target.value)}
              placeholder="e.g. Acute Stroke Code (AHA/ASA Guidelines)"
              className={inputClass}
            />
          </div>
          <div className="space-y-1.5">
            <label className="text-xs uppercase tracking-wider font-semibold text-muted-foreground">
              Description
            </label>
            <textarea
              value={editData.description}
              onChange={(e) => update("description", e.target.value)}
              placeholder="Brief description of the protocol, guidelines, timing windows..."
              rows={3}
              className={cn(inputClass, "resize-none")}
            />
          </div>
        </div>

        {/* Triggers */}
        <div className="space-y-2">
          <label className="text-xs uppercase tracking-wider font-semibold text-muted-foreground">
            Triggers
          </label>
          <div className="flex flex-wrap gap-1.5">
            {editData.triggers.map((t, i) => (
              <span
                key={i}
                className="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-lg bg-sky-500/10 text-sky-600 dark:text-sky-400 border border-sky-500/20"
              >
                {t}
                <button onClick={() => update("triggers", editData.triggers.filter((_, j) => j !== i))} className="hover:text-red-500">
                  <X className="h-3 w-3" />
                </button>
              </span>
            ))}
          </div>
          <div className="flex gap-2">
            <input
              type="text"
              value={triggerInput}
              onChange={(e) => setTriggerInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); addTrigger() } }}
              placeholder="Add triggers (comma-separated, press Enter)"
              className={cn(inputClass, "flex-1")}
            />
            <button onClick={addTrigger} className="px-3 py-2 text-sm font-medium text-primary bg-primary/10 border border-primary/20 rounded-lg hover:bg-primary/15 transition-colors shrink-0">
              Add
            </button>
          </div>
        </div>

        {/* Steps */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-xs uppercase tracking-wider font-semibold text-muted-foreground flex items-center gap-1.5">
              <Clock className="h-3.5 w-3.5" />
              Steps ({editData.steps.length})
            </label>
            <button
              onClick={() => { update("steps", [...editData.steps, emptyStep()]) }}
              className="flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-primary hover:bg-primary/10 rounded-lg transition-colors"
            >
              <Plus className="h-3 w-3" />
              Add Step
            </button>
          </div>
          <div className="space-y-3">
            {editData.steps.map((step, idx) => (
              <div key={idx} className="p-4 rounded-xl border border-border bg-card space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-muted-foreground uppercase tracking-wider">
                    Step {idx + 1}
                  </span>
                  <button
                    onClick={() => removeStep(idx)}
                    className="p-1 text-muted-foreground hover:text-red-500 transition-colors"
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                  </button>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-1">
                    <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-medium">Action</label>
                    <div className="relative">
                      <select
                        value={step.action}
                        onChange={(e) => updateStep(idx, "action", e.target.value)}
                        className={cn(inputClass, "appearance-none pr-8")}
                      >
                        {TOOL_ACTIONS.map((a) => (
                          <option key={a} value={a}>{a}</option>
                        ))}
                      </select>
                      <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 h-3 w-3 text-muted-foreground pointer-events-none" />
                    </div>
                  </div>
                  <div className="space-y-1">
                    <label className="text-[10px] uppercase tracking-wider text-muted-foreground font-medium">Timing</label>
                    <div className="relative">
                      <select
                        value={step.timing}
                        onChange={(e) => updateStep(idx, "timing", e.target.value)}
                        className={cn(inputClass, "appearance-none pr-8")}
                      >
                        {TIMINGS.map((t) => (
                          <option key={t} value={t}>{t}</option>
                        ))}
                      </select>
                      <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 h-3 w-3 text-muted-foreground pointer-events-none" />
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <label className="flex items-center gap-2 text-sm text-foreground cursor-pointer">
                    <input
                      type="checkbox"
                      checked={step.mandatory}
                      onChange={(e) => updateStep(idx, "mandatory", e.target.checked)}
                      className="rounded border-border"
                    />
                    <Shield className="h-3.5 w-3.5 text-muted-foreground" />
                    Mandatory
                  </label>
                </div>
                <input
                  type="text"
                  value={step.condition ?? ""}
                  onChange={(e) => updateStep(idx, "condition", e.target.value || null)}
                  placeholder="Condition (optional, e.g. 'if_thrombolysis_considered')"
                  className={inputClass}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Contraindicated */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-xs uppercase tracking-wider font-semibold text-muted-foreground flex items-center gap-1.5">
              <AlertTriangle className="h-3.5 w-3.5 text-red-500/70" />
              Contraindicated ({editData.contraindicated.length})
            </label>
            <button
              onClick={() => update("contraindicated", [...editData.contraindicated, ""])}
              className="flex items-center gap-1 px-2.5 py-1 text-xs font-medium text-red-500/70 hover:bg-red-500/10 rounded-lg transition-colors"
            >
              <Plus className="h-3 w-3" />
              Add
            </button>
          </div>
          <div className="space-y-2">
            {editData.contraindicated.map((item, idx) => (
              <div key={idx} className="flex gap-2">
                <div className="flex items-center px-2 text-red-500/50">
                  <AlertTriangle className="h-3.5 w-3.5" />
                </div>
                <input
                  type="text"
                  value={item}
                  onChange={(e) => {
                    const items = [...editData.contraindicated]
                    items[idx] = e.target.value
                    update("contraindicated", items)
                  }}
                  placeholder="Describe contraindicated action..."
                  className={cn(inputClass, "flex-1")}
                />
                <button
                  onClick={() => update("contraindicated", editData.contraindicated.filter((_, i) => i !== idx))}
                  className="p-2 text-muted-foreground hover:text-red-500 transition-colors"
                >
                  <X className="h-3.5 w-3.5" />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
