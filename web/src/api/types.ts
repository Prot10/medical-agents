// Mirrors of the Pydantic contracts in packages/neuroagent-schemas and the
// policy-harness API (agent-platform/src/neuroagent/api).

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
  schema_version: string
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
    bmi?: number | null
  }
  clinical_history: {
    past_medical_history: string[]
    medications: Medication[]
    allergies: string[]
    family_history: string[]
    social_history: Record<string, string>
  }
  neurological_exam: Record<string, unknown>
  physical_exam: Record<string, string>
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
  hr: number
  temp: number
  rr: number
  spo2: number
}

// Clinical policy (ground truth)
export type PolicyReviewStatus = "draft" | "needs_revision" | "approved"
export type ActionImportance = "required" | "recommended" | "optional"
export type AvoidanceSeverity = "waste" | "harm" | "contraindicated"

export interface ToolCallPattern {
  tool_name: string
  required_arguments: Record<string, unknown>
}

export interface ActionCriterion {
  criterion_id: string
  label: string
  importance: ActionImportance
  alternatives: ToolCallPattern[]
  expected_evidence: string
  rationale: string
  citations: string[]
}

export interface AvoidedActionCriterion {
  criterion_id: string
  severity: AvoidanceSeverity
  alternatives: ToolCallPattern[]
  rationale: string
  citations: string[]
}

export interface SequenceConstraint {
  before_criterion_id: string
  after_criterion_id: string
  reason: string
  citations: string[]
  severity: string
}

export interface DifferentialDx {
  diagnosis: string
  likelihood: string
  key_features: string
  icd_code: string | null
}

export interface RedHerring {
  data_point: string
  location: string
  field_path: string
  intended_effect: string
  correct_interpretation: string
}

export interface GroundTruth {
  review_status: PolicyReviewStatus
  diagnosis: { accepted: string[]; icd_codes: string[] }
  differential: DifferentialDx[]
  action_criteria: ActionCriterion[]
  avoided_actions: AvoidedActionCriterion[]
  sequence_constraints: SequenceConstraint[]
  stop_rule: { required_before_assessment: string[]; max_additional_actions: number }
  assessment: { required_recommendations: string[]; prohibited_recommendations: string[] }
  key_clinical_evidence: string[]
  red_herrings: RedHerring[]
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

// Model panel
export interface ModelInfo {
  key: string
  name: string
  hf_model_id: string
  description: string
  status: "ready" | "loading" | "offline"
}

// Checked experiment profile
export interface Profile {
  profile_id: string
  max_turns: number
  max_cost_usd: number | null
  max_invalid_actions: number
  plugins: { id: string; config: Record<string, unknown> }[]
}

// Clinical actions
export interface ToolAction {
  type: "tool"
  tool_name: string
  arguments: Record<string, unknown>
}

export interface SubmitAssessment {
  type: "submit_assessment"
  primary_diagnosis: string
  icd10_code: string | null
  differential: { diagnosis: string; confidence: number | null }[]
  confidence: number
  urgency: "emergent" | "urgent" | "routine"
  recommendations: string[]
}

export type ClinicalAction = ToolAction | SubmitAssessment

// Append-only episode events
interface EventBase {
  event_id: string
  timestamp: string
  turn: number
}

export interface RunStarted extends EventBase {
  type: "run.started"
  case_id: string
  profile_id: string
  model_id: string
  plugin_versions: Record<string, string>
}

export interface ModelRequested extends EventBase {
  type: "model.requested"
  prompt_tokens: number
}

export interface ActionProposed extends EventBase {
  type: "action.proposed"
  action: ClinicalAction
  completion_tokens: number
  latency_seconds: number
}

export interface ActionRejected extends EventBase {
  type: "action.rejected"
  reason: string
  retry_allowed: boolean
}

export interface ObservationReceived extends EventBase {
  type: "observation.received"
  tool_name: string
  success: boolean
  output: Record<string, unknown> | null
  error_message: string | null
  cost_usd: number
  from_fallback: boolean
  library: boolean
  rejected: boolean
}

export interface AssessmentSubmitted extends EventBase {
  type: "assessment.submitted"
  assessment: SubmitAssessment
}

export interface PluginEvent extends EventBase {
  type: "plugin.event"
  namespace: string
  payload: Record<string, unknown>
}

export interface RunCompleted extends EventBase {
  type: "run.completed"
  reason: "assessment_submitted"
}

export interface RunFailed extends EventBase {
  type: "run.failed"
  reason: "invalid_action" | "budget_exhausted" | "model_error" | "environment_error"
  message: string
}

export type EpisodeEvent =
  | RunStarted
  | ModelRequested
  | ActionProposed
  | ActionRejected
  | ObservationReceived
  | AssessmentSubmitted
  | PluginEvent
  | RunCompleted
  | RunFailed

export interface ClinicalEpisode {
  schema_version: string
  events: EpisodeEvent[]
}

// Policy reward
export interface RewardBreakdown {
  diagnosis: number
  required_action_coverage: number
  recommended_action_coverage: number
  tool_accuracy: number
  safety: number
  waste_avoidance: number
  sequence: number
  stopping: number
  assessment: number
  cost_efficiency: number
  token_efficiency: number
  invalid_actions: number
  scalar: number
  caps_applied: string[]
}

export interface EngineeringReward {
  reward: RewardBreakdown
  policy_review_status: PolicyReviewStatus
}

// Frames of POST /runs/stream beyond the episode events
export interface StreamResult extends EngineeringReward {
  type: "stream.result"
  episode_id: string | null
}

export interface StreamError {
  type: "stream.error"
  message: string
}

export type RunStreamFrame = EpisodeEvent | StreamResult | StreamError

// Persisted episode summary (GET /episodes)
export interface EpisodeSummary {
  episode_id: string
  case_id: string
  profile_id: string
  model_id: string
  condition: string
  difficulty: string
  status: "run.completed" | "run.failed" | "incomplete"
  tool_call_count: number
  tools_called: string[]
  fallback_call_count: number
  total_tokens: number
  total_cost_usd: number
  model_latency_seconds: number
}
