// Display labels + colors for the 20 neurological conditions in NeuroBench.
// Keep keys in sync with `NeurologicalCondition` enum in
// packages/neuroagent-schemas/src/neuroagent_schemas/enums.py

export interface ConditionMeta {
  label: string
  short: string
  color: string
  category: "neurodegenerative" | "cerebrovascular" | "epilepsy" | "infectious" | "tumor" | "autoimmune" | "neuromuscular" | "headache" | "functional" | "metabolic" | "other"
}

export const CONDITION_META: Record<string, ConditionMeta> = {
  alzheimers_early: { label: "Early Alzheimer's", short: "ALZ", color: "#a78bfa", category: "neurodegenerative" },
  alzheimers_moderate: { label: "Moderate Alzheimer's", short: "ALZ-M", color: "#9333ea", category: "neurodegenerative" },
  focal_epilepsy_temporal: { label: "Temporal Lobe Epilepsy", short: "TLE", color: "#06b6d4", category: "epilepsy" },
  focal_epilepsy_frontal: { label: "Frontal Lobe Epilepsy", short: "FLE", color: "#0891b2", category: "epilepsy" },
  generalized_epilepsy: { label: "Generalized Epilepsy", short: "GE", color: "#0e7490", category: "epilepsy" },
  status_epilepticus: { label: "Status Epilepticus", short: "SE", color: "#155e75", category: "epilepsy" },
  ischemic_stroke: { label: "Ischemic Stroke", short: "STK", color: "#f43f5e", category: "cerebrovascular" },
  hemorrhagic_stroke: { label: "Hemorrhagic Stroke", short: "HEM", color: "#e11d48", category: "cerebrovascular" },
  subarachnoid_hemorrhage: { label: "Subarachnoid Hemorrhage", short: "SAH", color: "#be123c", category: "cerebrovascular" },
  tia: { label: "Transient Ischemic Attack", short: "TIA", color: "#fb7185", category: "cerebrovascular" },
  cadasil: { label: "CADASIL", short: "CDS", color: "#fda4af", category: "cerebrovascular" },
  multiple_sclerosis: { label: "Multiple Sclerosis", short: "MS", color: "#10b981", category: "autoimmune" },
  autoimmune_encephalitis_nmdar: { label: "NMDA-R Encephalitis", short: "NMDAR", color: "#059669", category: "autoimmune" },
  autoimmune_encephalitis_lgi1: { label: "LGI1 Encephalitis", short: "LGI1", color: "#047857", category: "autoimmune" },
  neurosarcoidosis: { label: "Neurosarcoidosis", short: "SARC", color: "#34d399", category: "autoimmune" },
  parkinsons: { label: "Parkinson's Disease", short: "PD", color: "#f59e0b", category: "neurodegenerative" },
  atypical_parkinsonism_msa: { label: "MSA", short: "MSA", color: "#d97706", category: "neurodegenerative" },
  atypical_parkinsonism_psp: { label: "PSP", short: "PSP", color: "#b45309", category: "neurodegenerative" },
  ftd: { label: "Frontotemporal Dementia", short: "FTD", color: "#92400e", category: "neurodegenerative" },
  nph: { label: "Normal Pressure Hydrocephalus", short: "NPH", color: "#fbbf24", category: "neurodegenerative" },
  cjd: { label: "Creutzfeldt-Jakob", short: "CJD", color: "#fde68a", category: "neurodegenerative" },
  als: { label: "ALS", short: "ALS", color: "#7c3aed", category: "neuromuscular" },
  myasthenia_gravis: { label: "Myasthenia Gravis", short: "MG", color: "#6d28d9", category: "neuromuscular" },
  guillain_barre: { label: "Guillain-Barré", short: "GBS", color: "#5b21b6", category: "neuromuscular" },
  peripheral_neuropathy: { label: "Peripheral Neuropathy", short: "PN", color: "#a855f7", category: "neuromuscular" },
  bacterial_meningitis: { label: "Bacterial Meningitis", short: "BACT", color: "#dc2626", category: "infectious" },
  viral_encephalitis: { label: "Viral Encephalitis", short: "VENC", color: "#b91c1c", category: "infectious" },
  brain_tumor_glioma: { label: "Glioma", short: "GLI", color: "#1e40af", category: "tumor" },
  brain_tumor_meningioma: { label: "Meningioma", short: "MEN", color: "#1d4ed8", category: "tumor" },
  brain_tumor_metastasis: { label: "Brain Metastasis", short: "MET", color: "#2563eb", category: "tumor" },
  migraine_with_aura: { label: "Migraine w/ Aura", short: "MIG-A", color: "#ec4899", category: "headache" },
  migraine_without_aura: { label: "Migraine", short: "MIG", color: "#db2777", category: "headache" },
  hepatic_encephalopathy: { label: "Hepatic Encephalopathy", short: "HEP", color: "#eab308", category: "metabolic" },
  syncope_cardiac: { label: "Cardiac Syncope", short: "SYNC", color: "#f97316", category: "other" },
  syncope_vasovagal: { label: "Vasovagal Syncope", short: "VVS", color: "#fb923c", category: "other" },
  functional_neurological_disorder: { label: "FND", short: "FND", color: "#64748b", category: "functional" },
}

export function conditionLabel(condition: string): string {
  return CONDITION_META[condition]?.label ?? condition
}

export function conditionShort(condition: string): string {
  return CONDITION_META[condition]?.short ?? condition.slice(0, 4).toUpperCase()
}

export function conditionColor(condition: string): string {
  return CONDITION_META[condition]?.color ?? "#64748b"
}
