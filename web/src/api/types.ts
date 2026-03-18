// Case index (lightweight)
export interface CaseIndexEntry {
  case_id: string
  condition: string
  difficulty: string
  encounter_type: string
  age: number
  sex: string
  chief_complaint: string
}

// Full case detail (from /api/v1/cases/:id)
export interface CaseDetail {
  case_id: string
  condition: string
  difficulty: string
  encounter_type: string
  patient: Patient
  initial_tool_outputs: Record<string, unknown>
  followup_outputs: unknown[]
  ground_truth: GroundTruth
  metadata: Record<string, unknown>
}

export interface Patient {
  patient_id: string
  demographics: {
    age: number
    sex: string
    handedness?: string
    ethnicity?: string
    bmi?: number
  }
  clinical_history: {
    past_medical_history: string[]
    medications: Medication[]
    allergies: string[]
    family_history: string[]
    social_history: Record<string, string>
  }
  neurological_exam: Record<string, unknown>
  vitals: Vitals
  chief_complaint: string
  history_present_illness: string
}

export interface Medication {
  drug: string
  dose: string
  frequency: string
  indication?: string
}

export interface Vitals {
  bp_systolic: number
  bp_diastolic: number
  heart_rate: number
  temperature: number
  respiratory_rate: number
  spo2: number
}

export interface GroundTruth {
  primary_diagnosis: string
  icd_code: string
  differential: DifferentialDiagnosis[]
  optimal_actions: OptimalAction[]
  critical_actions: string[]
  contraindicated_actions: string[]
  key_reasoning_points: string[]
}

export interface DifferentialDiagnosis {
  diagnosis: string
  likelihood: string
  key_distinguishing: string
}

export interface OptimalAction {
  step: number
  action: string
  category: string
  rationale?: string
}

// Hospital
export interface Hospital {
  id: string
  name: string
  pathways: PathwaySummary[]
}

export interface PathwaySummary {
  name: string
  description: string
  triggers: string[]
}

// Hospital rules detail
export interface PathwayStep {
  action: string
  timing: string
  mandatory: boolean
  condition: string | null
  details: Record<string, unknown>
}

export interface PathwayDetail {
  name: string
  description: string
  triggers: string[]
  steps: PathwayStep[]
  contraindicated: string[]
}

export interface HospitalRulesDetail {
  id: string
  name: string
  pathways: PathwayDetail[]
}

// Model
export interface ModelInfo {
  key: string
  name: string
  hf_model_id: string
  description: string
  status: "ready" | "loading" | "offline"
  provider?: "local" | "github" | "copilot"
}

// Agent SSE Events
export type AgentEventType =
  | "run_started"
  | "think_delta"
  | "content_delta"
  | "thinking"
  | "tool_call"
  | "tool_result"
  | "reflection"
  | "assessment"
  | "run_complete"
  | "error"

export interface AgentEvent {
  type: AgentEventType
  turn_number?: number
  content?: string
  think_content?: string
  delta?: string
  tool_name?: string
  arguments?: Record<string, unknown>
  success?: boolean
  output?: Record<string, unknown>
  token_usage?: { prompt_tokens: number; completion_tokens: number; total_tokens: number }
  // tool_result cost field
  cost_usd?: number
  // run_complete fields
  total_tool_calls?: number
  tools_called?: string[]
  total_tokens?: number
  elapsed_time_seconds?: number
  final_response?: string
  total_cost_usd?: number
  // run_started fields
  case_id?: string
  hospital?: string
  model?: string
  max_turns?: number
  // error fields
  message?: string
}

// Dataset
export interface DatasetInfo {
  version: string
  name: string
  description: string
  case_count: number
  active: boolean
}

// Trace (for replay)
export interface TraceSummary {
  trace_id: string
  case_id: string
  hospital: string
  model: string
  model_short: string
  condition: string
  difficulty: string
  total_tool_calls: number
  tools_called: string[]
  total_tokens: number
  elapsed_time_seconds: number
  total_cost_usd?: number
}
