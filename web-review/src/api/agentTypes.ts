// Agent mode: a physician works a case as the agent does (review_api/routes/agent_mode.py).

export type JsonValue = string | number | boolean | null | JsonValue[] | { [key: string]: JsonValue }

/** One property of a tool's JSON schema, as the agent's catalogue declares it. */
export interface ParamSchema {
  type?: string
  description?: string
  enum?: string[]
  default?: JsonValue
  items?: ParamSchema
}

/** One entry of the tool list sent to the model (OpenAI function format). */
export interface ToolDefinition {
  type: "function"
  function: {
    name: string
    description: string
    parameters: {
      type: "object"
      properties: Record<string, ParamSchema>
      required?: string[]
    }
  }
}

export interface AgentSectionSummary {
  section: string
  title: string
  description: string
  total: number
  done: number
  /** The case to work now: the open one, else the first not started. Null when all are done. */
  current: number | null
}

export type WorkCaseStatus = "todo" | "in_progress" | "done"

export interface AgentWorklist extends AgentSectionSummary {
  cases: Array<{ number: number; status: WorkCaseStatus; orders: number; finished_at: string | null }>
}

/** What the agent receives back for an order: the content of its `tool` message. */
export interface Observation {
  tool_name: string
  success: boolean
  output: Record<string, JsonValue> | null
  error_message: string | null
}

export interface TimelineEntry {
  turn: number
  tool_name: string
  arguments: Record<string, JsonValue>
  rationale: string
  sent_at: string
  observation?: Observation
  /** The `tool` message content, verbatim. */
  observation_text?: string
}

export interface RawMessage {
  role: string
  content: string | null
  tool_calls?: Array<{ id: string; type: string; function: { name: string; arguments: string } }>
  tool_call_id?: string
}

export interface CaseState {
  section: string
  number: number
  status: "in_progress" | "completed" | "failed"
  /** Actions sent so far; echoed back with the next one so a stale page is refused. */
  expected_step: number
  next: number | null
  failure?: { reason: string; message: string } | null
  // Present while the case is in progress.
  turn?: number
  orders?: number
  max_turns?: number | null
  require_assessment?: boolean
  notice?: string | null
  invalid_actions?: number
  instructions?: string
  presentation?: string
  tools?: ToolDefinition[]
  submit_name?: string
  timeline?: TimelineEntry[]
  raw?: { messages: RawMessage[]; tools: ToolDefinition[] }
}

export interface StepTelemetry {
  active_seconds: number
  tools_opened: string[]
  searches: string[]
  raw_view_opened: boolean
  resumed: boolean
}

export interface ActionBody {
  expected_step: number
  name: string
  arguments: Record<string, JsonValue>
  rationale: string
  telemetry: StepTelemetry
}

// ── Admin ─────────────────────────────────────────────────────────────────────────────────

export interface RewardRow {
  case_id: string
  condition: string
  status: string
  failure_reason: string | null
  invalid_actions: number
  tool_calls: number
  tools_called: string[]
  primary_diagnosis: string | null
  total_cost_usd: number
  reward: Record<string, number | string[]> & { scalar: number; caps_applied: string[] }
  policy_review: string
  reportable: boolean
  scorer_id: string
}

export interface AdminEpisode {
  section: string
  reviewer_id: string
  reviewer_name: string
  case_number: number
  case_id: string
  condition: string
  status: "in_progress" | "completed" | "failed"
  orders: number
  invalid_attempts: number
  started_at: string
  finished_at: string | null
  elapsed_seconds: number
  active_seconds: number | null
  row: RewardRow | null
}

export interface AdminEpisodeDetail extends AdminEpisode {
  timeline: TimelineEntry[]
  steps: Array<{
    index: number
    turn: number
    name: string
    outcome: string
    rationale: string
    server_seconds: number
    client: StepTelemetry & { active_seconds: number | null }
  }>
  assessment: {
    primary_diagnosis: string
    icd10_code: string | null
    differential: Array<{ diagnosis: string; confidence: number | null }>
    confidence: number
    urgency: string
    recommendations: string[]
  } | null
  diagnostic_reasoning: string | null
  failure: { reason: string; message: string } | null
  provenance: Record<string, JsonValue>
}

export interface AdminAgentSection {
  key: string
  title: string
  set_id: string
  cases: number
  record_derived: boolean
  reviewers: Array<{
    reviewer_id: string
    name: string
    active: boolean
    assigned: number
    done: number
    failed: number
    in_progress: number
  }>
  episodes: AdminEpisode[]
}

export interface AdminAgentOverview {
  scorer_id: string
  limits: { from: string; max_turns: number }
  sections: AdminAgentSection[]
}
