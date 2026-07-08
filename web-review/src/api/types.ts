// TypeScript mirrors of the Pydantic models in the review API. Keep in sync
// with agent-platform/src/neuroagent/review_api/schemas/.

export type Severity = "note" | "issue" | "error"

export type ReviewStatus =
  | "pending"
  | "in_progress"
  | "needs_changes"
  | "approved"

export type ReviewerRole = "reviewer" | "admin"

export interface ReviewerProfile {
  code: string
  name: string
  role: ReviewerRole
}

export interface DatasetSummary {
  version: string
  name: string
  description: string
  case_count: number
  is_default: boolean
}

export interface CaseIndexEntry {
  case_id: string
  condition: string
  difficulty: "straightforward" | "moderate" | "diagnostic_puzzle"
  encounter_type: "emergency" | "inpatient" | "outpatient"
  age: number
  sex: string
  chief_complaint: string
}

export interface FieldAnnotation {
  id: string
  field_path: string
  field_snippet: string | null
  comment: string
  severity: Severity
  created_at: string
  updated_at: string
  resolved: boolean
}

export interface CaseComment {
  id: string
  comment: string
  severity: Severity
  created_at: string
  updated_at: string
}

export interface CaseReview {
  case_id: string
  dataset_version: string
  reviewer_code: string
  status: ReviewStatus
  field_annotations: FieldAnnotation[]
  case_comments: CaseComment[]
  first_opened_at: string | null
  last_updated_at: string
  last_active_at: string | null
  time_spent_seconds: number
}

export interface CaseReviewSummary {
  case_id: string
  status: ReviewStatus
  annotation_count: number
  comment_count: number
  severity_counts: Record<Severity, number>
  last_updated_at: string | null
  time_spent_seconds: number
}

export interface MyProgress {
  reviewer_code: string
  dataset_version: string
  total_cases: number
  touched_cases: number
  total_time_spent_seconds: number
  avg_time_spent_seconds: number
  by_status: Record<ReviewStatus, number>
  by_condition: Record<string, Record<ReviewStatus, number>>
}

export interface MethodologyStats {
  total_cases: number
  conditions: number
  by_difficulty: Record<string, number>
  by_encounter: Record<string, number>
  avg_pathway_depth: number
}

export interface MethodologyPipelineStage {
  label: string
  icon: string
  description: string
}

export interface MethodologyProse {
  title: string
  tagline: string
  overview: string
  pipeline: MethodologyPipelineStage[]
  citation_bibtex: string
}

export interface Methodology {
  version: string
  prose: MethodologyProse
  stats: MethodologyStats
  by_condition: Array<{
    condition: string
    count: number
    by_difficulty: Record<string, number>
  }>
}

// Admin views ------------------------------------------------------------

export interface AdminAgreementRow {
  case_id: string
  condition: string
  difficulty: string
  statuses: Record<string, ReviewStatus>
  consensus: "unanimous" | "agree" | "in_review" | "disagree"
}

export interface AgreementKappa {
  overall: number | null
  interpretation: string | null
  method: string
  pairs: Array<{ a: string; b: string; kappa: number; n: number }>
  note: string | null
}

export interface AdminAgreement {
  reviewer_codes: string[]
  rows: AdminAgreementRow[]
  consensus_summary: Record<string, number>
  kappa: AgreementKappa
}

export interface AdminReviewerProgress extends MyProgress {
  code: string
  name: string
  role: ReviewerRole
}

export interface FieldHotspot {
  field_path: string
  total: number
  by_severity: Record<Severity, number>
  reviewer_codes: string[]
  case_ids: string[]
  latest_comment: string | null
  latest_at: string | null
}

export interface CaseDiffReviewer {
  code: string
  name: string
  status: ReviewStatus
  annotation_count: number
  comment_count: number
  case_comments: CaseComment[]
}

export interface CaseDiffFieldRow {
  field_path: string
  by_reviewer: Record<string, FieldAnnotation>
}

export interface CaseDiff {
  case_id: string
  dataset_version: string
  reviewers: CaseDiffReviewer[]
  field_rows: CaseDiffFieldRow[]
  consensus: "unanimous" | "partial" | "disagree"
}

// --- Tool review ---------------------------------------------------------

export interface ToolMeta {
  name: string
  label: string
  description: string
  modality: string | null
  cost_summary: string | null
  parameters: ToolParameter[]
  output_fields: ToolOutputField[]
}

export interface ToolParameter {
  name: string
  type: string
  description: string
  required: boolean
  enum: string[] | null
  default: string | number | boolean | null
  items_type: string | null
}

export interface ToolOutputField {
  name: string
  type: string
  description: string
  required: boolean
}

export interface ConditionToolMapping {
  condition: string
  label: string
  required_tools: string[]
  optional_tools: string[]
}

export interface ToolCatalog {
  version: string
  tools: ToolMeta[]
  universal_tools: string[]
  conditions: ConditionToolMapping[]
  unmapped_tools: string[]
}

export interface ProposedTool {
  id: string
  name: string
  description: string
  rationale: string
  target_conditions: string[]
  modality: string | null
  created_at: string
  updated_at: string
}

export interface ToolReview {
  reviewer_code: string
  dataset_version: string
  field_annotations: FieldAnnotation[]
  proposed_tools: ProposedTool[]
  completed_at: string | null
  first_opened_at: string | null
  last_updated_at: string
}

export interface AdminToolReviewProposal extends ProposedTool {
  reviewer_code: string
  reviewer_name: string
}

export interface AdminToolReviewCoverage {
  field_path: string
  total: number
  severity_counts: Record<string, number>
  reviewers: string[]
  comments: Array<{
    reviewer_code: string
    reviewer_name: string
    severity: Severity
    comment: string
  }>
}

export interface AdminToolReviewStatus {
  reviewer_code: string
  reviewer_name: string
  completed: boolean
  started: boolean
  proposal_count: number
  annotation_count: number
}

export interface AdminToolReviewSummary {
  proposals: AdminToolReviewProposal[]
  coverage: AdminToolReviewCoverage[]
  reviewer_status: AdminToolReviewStatus[]
}

// --- Full NeuroBenchCase (used by the case detail view) ------------------
// Loose typing — keeping the surface area small. The detail view treats most
// fields as JSON values and lets typed sub-components claim what they need.

export interface NeuroBenchCase {
  case_id: string
  condition: string
  difficulty: string
  encounter_type: string
  patient: PatientProfile
  initial_tool_outputs: Record<string, unknown> | null
  followup_outputs: Array<{
    trigger_action: string
    tool_name: string
    output: unknown
  }>
  ground_truth: GroundTruth
  metadata: Record<string, unknown>
}

export interface PatientProfile {
  patient_id?: string
  demographics: {
    age: number
    sex: string
    handedness?: string
    ethnicity?: string
    bmi?: number
  }
  clinical_history: {
    past_medical_history?: string[]
    medications?: Array<{
      drug: string
      dose?: string
      frequency?: string
      indication?: string
    }>
    allergies?: string[]
    family_history?: string[]
    social_history?: Record<string, string>
  }
  neurological_exam: {
    mental_status?: string
    cranial_nerves?: string
    motor?: string
    sensory?: string
    reflexes?: string
    coordination?: string
    gait?: string
    additional?: string
  }
  physical_exam?: Record<string, string>
  vitals: {
    bp_systolic?: number
    bp_diastolic?: number
    hr?: number
    temp?: number
    rr?: number
    spo2?: number
  }
  chief_complaint: string
  history_present_illness: string
}

export interface ToolClassification {
  tool_name: string
  tool_parameters?: Record<string, unknown>
  rationale: string
  citation?: string
}

export interface SequenceConstraint {
  before: string
  after: string
  reason: string
  citation?: string
  severity: "soft" | "hard"
}

export interface GroundTruth {
  primary_diagnosis: string
  icd_code?: string
  differential?: Array<{
    diagnosis: string
    likelihood: string
    key_distinguishing?: string
  }>
  optimal_actions?: Array<{
    step: number
    action: string
    tool_name?: string
    expected_finding?: string
    category?: string
    tool_parameters?: Record<string, unknown>
  }>
  useless_tools?: ToolClassification[]
  harmful_tools?: ToolClassification[]
  sequence_constraints?: SequenceConstraint[]
  critical_actions?: string[]
  contraindicated_actions?: string[]
  key_reasoning_points?: string[]
  red_herrings?: Array<{
    data_point: string
    location: string
    intended_effect: string
    correct_interpretation: string
  }>
}
