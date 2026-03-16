import type { CaseIndexEntry, CaseDetail, Hospital, HospitalRulesDetail, PathwayDetail, ModelInfo, TraceSummary, AgentEvent, DatasetInfo } from "./types"

const BASE = "/api/v1"

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init)
  if (!res.ok) throw new Error(`${res.status}: ${res.statusText}`)
  return res.json()
}

export const api = {
  getDatasets: () => fetchJSON<DatasetInfo[]>(`${BASE}/datasets`),
  activateDataset: (version: string) =>
    fetchJSON<{ status: string; version: string; case_count: number }>(
      `${BASE}/datasets/${version}/activate`,
      { method: "POST" },
    ),
  getCases: () => fetchJSON<CaseIndexEntry[]>(`${BASE}/cases`),
  getCase: (id: string) => fetchJSON<CaseDetail>(`${BASE}/cases/${id}`),
  getHospitals: () => fetchJSON<Hospital[]>(`${BASE}/hospitals`),
  getHospitalRules: (id: string) => fetchJSON<HospitalRulesDetail>(`${BASE}/hospitals/${id}/rules`),
  updatePathway: (hospitalId: string, index: number, data: PathwayDetail) =>
    fetchJSON<PathwayDetail>(`${BASE}/hospitals/${hospitalId}/rules/${index}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }),
  createPathway: (hospitalId: string, data: PathwayDetail) =>
    fetchJSON<PathwayDetail>(`${BASE}/hospitals/${hospitalId}/rules`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }),
  deletePathway: (hospitalId: string, index: number) =>
    fetchJSON<{ status: string }>(`${BASE}/hospitals/${hospitalId}/rules/${index}`, {
      method: "DELETE",
    }),
  getModels: () => fetchJSON<ModelInfo[]>(`${BASE}/models`),
  // Copilot device flow
  copilotStartDeviceFlow: () => fetchJSON<{ device_code: string; user_code: string; verification_uri: string; expires_in: number; interval: number }>(`${BASE}/copilot/device-code`, { method: "POST" }),
  copilotPollToken: (deviceCode: string) => fetchJSON<{ status: string; error?: string; interval?: number }>(`${BASE}/copilot/poll-token`, { method: "POST", body: JSON.stringify({ device_code: deviceCode }), headers: { "Content-Type": "application/json" } }),
  copilotStatus: () => fetchJSON<{ authenticated: boolean; copilot_access: boolean }>(`${BASE}/copilot/status`),
  copilotModels: () => fetchJSON<ModelInfo[]>(`${BASE}/copilot/models`),
  copilotLogout: () => fetchJSON<{ status: string }>(`${BASE}/copilot/logout`, { method: "POST" }),
  getTraces: () => fetchJSON<TraceSummary[]>(`${BASE}/traces`),
  deleteTrace: (id: string) =>
    fetch(`${BASE}/traces/${id}`, { method: "DELETE" }).then((res) => {
      if (!res.ok) throw new Error(`${res.status}: ${res.statusText}`)
    }),
  getTrace: (id: string) => fetchJSON<{ case_id: string; events: AgentEvent[]; [key: string]: unknown }>(`${BASE}/traces/${id}`),
  loadModel: (modelKey: string) =>
    fetch(`${BASE}/models/${modelKey}/load`, { method: "POST" }),
  unloadModel: () =>
    fetchJSON<{ status: string; message: string }>(`${BASE}/models/unload`, { method: "POST" }),
}

/** Parse SSE events from a ReadableStream, calling onEvent for each. */
async function consumeSSEStream(
  response: Response,
  onEvent: (event: AgentEvent) => void,
): Promise<void> {
  const reader = response.body!.getReader()
  const decoder = new TextDecoder()
  let buffer = ""

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })

    const parts = buffer.split("\n\n")
    buffer = parts.pop()!

    for (const part of parts) {
      parseSSELine(part, onEvent)
    }
  }

  // Flush any remaining data in the buffer after stream ends
  if (buffer.trim()) {
    parseSSELine(buffer, onEvent)
  }
}

function parseSSELine(raw: string, onEvent: (event: AgentEvent) => void): void {
  const line = raw.trim()
  if (line.startsWith("data: ")) {
    try {
      onEvent(JSON.parse(line.slice(6)) as AgentEvent)
    } catch {
      // skip malformed events
    }
  }
}

export async function streamAgentRun(
  caseId: string,
  hospital: string,
  model: string,
  onEvent: (event: AgentEvent) => void,
  onError: (error: Error) => void,
  signal?: AbortSignal,
  options?: { base_url?: string; api_key?: string },
): Promise<void> {
  const response = await fetch(`${BASE}/agent/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      case_id: caseId,
      hospital,
      model,
      ...(options?.base_url && { base_url: options.base_url }),
      ...(options?.api_key && { api_key: options.api_key }),
    }),
    signal,
    cache: "no-store",
  })

  if (!response.ok) {
    onError(new Error(`${response.status}: ${response.statusText}`))
    return
  }

  await consumeSSEStream(response, onEvent)
}

export async function streamEvaluation(
  caseId: string,
  model: string,
  events: AgentEvent[],
  finalResponse: string,
  toolsCalled: string[],
  onEvent: (event: Record<string, unknown>) => void,
  onError: (error: Error) => void,
  signal?: AbortSignal,
): Promise<void> {
  const response = await fetch(`${BASE}/agent/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      case_id: caseId,
      model,
      events,
      final_response: finalResponse,
      tools_called: toolsCalled,
    }),
    signal,
    cache: "no-store",
  })

  if (!response.ok) {
    onError(new Error(`${response.status}: ${response.statusText}`))
    return
  }

  await consumeSSEStream(response, onEvent as unknown as (event: AgentEvent) => void)
}

export async function replayTrace(
  traceId: string,
  onEvent: (event: AgentEvent) => void,
  onError: (error: Error) => void,
  signal?: AbortSignal,
): Promise<void> {
  const response = await fetch(`${BASE}/agent/replay`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ trace_id: traceId }),
    signal,
    cache: "no-store",
  })

  if (!response.ok) {
    onError(new Error(`${response.status}: ${response.statusText}`))
    return
  }

  await consumeSSEStream(response, onEvent)
}
