// Display labels for the NeuroBench conditions (NeurologicalCondition in neuroagent-schemas).
export const CONDITION_LABELS: Record<string, string> = {
  als: "ALS",
  alzheimers_early: "Alzheimer's (Early)",
  autoimmune_encephalitis_nmdar: "NMDAR Encephalitis",
  bacterial_meningitis: "Bacterial Meningitis",
  brain_tumor_glioma: "Glioma",
  focal_epilepsy_temporal: "Temporal Lobe Epilepsy",
  ftd: "Frontotemporal Dementia",
  functional_neurological_disorder: "FND",
  guillain_barre: "Guillain-Barré",
  hepatic_encephalopathy: "Hepatic Encephalopathy",
  ischemic_stroke: "Ischemic Stroke",
  migraine_with_aura: "Migraine with Aura",
  multiple_sclerosis: "Multiple Sclerosis",
  myasthenia_gravis: "Myasthenia Gravis",
  nph: "Normal Pressure Hydrocephalus",
  parkinsons: "Parkinson's",
  status_epilepticus: "Status Epilepticus",
  subarachnoid_hemorrhage: "Subarachnoid Hemorrhage",
  syncope_cardiac: "Cardiac Syncope",
  vascular_dementia: "Vascular Dementia",
}

export function conditionLabel(condition: string): string {
  return CONDITION_LABELS[condition] ?? condition.replace(/_/g, " ")
}

// One distinct hue per condition, shared by the sidebar bars and the dashboard charts.
export const CONDITION_COLORS: Record<string, string> = {
  als: "#a855f7",
  alzheimers_early: "#8b5cf6",
  autoimmune_encephalitis_nmdar: "#10b981",
  bacterial_meningitis: "#ef4444",
  brain_tumor_glioma: "#f43f5e",
  focal_epilepsy_temporal: "#3b82f6",
  ftd: "#d946ef",
  functional_neurological_disorder: "#6b7280",
  guillain_barre: "#14b8a6",
  hepatic_encephalopathy: "#84cc16",
  ischemic_stroke: "#f97316",
  migraine_with_aura: "#eab308",
  multiple_sclerosis: "#06b6d4",
  myasthenia_gravis: "#0ea5e9",
  nph: "#78716c",
  parkinsons: "#f59e0b",
  status_epilepticus: "#2563eb",
  subarachnoid_hemorrhage: "#dc2626",
  syncope_cardiac: "#6366f1",
  vascular_dementia: "#c026d3",
}
