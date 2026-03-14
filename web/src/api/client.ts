import type { CaseIndexEntry, CaseDetail, Hospital, ModelInfo, TraceSummary, AgentEvent } from "./types"

const BASE = "/api/v1"

async function fetchJSON<T>(url: string): Promise<T> {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`${res.status}: ${res.statusText}`)
  return res.json()
}

export const api = {
  getCases: () => fetchJSON<CaseIndexEntry[]>(`${BASE}/cases`),
  getCase: (id: string) => fetchJSON<CaseDetail>(`${BASE}/cases/${id}`),
  getHospitals: () => fetchJSON<Hospital[]>(`${BASE}/hospitals`),
  getHospitalRules: (id: string) => fetchJSON<Record<string, unknown>>(`${BASE}/hospitals/${id}/rules`),
  getModels: () => fetchJSON<ModelInfo[]>(`${BASE}/models`),
  getTraces: () => fetchJSON<TraceSummary[]>(`${BASE}/traces`),
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
): Promise<void> {
  const response = await fetch(`${BASE}/agent/run`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ case_id: caseId, hospital, model }),
    signal,
  })

  if (!response.ok) {
    onError(new Error(`${response.status}: ${response.statusText}`))
    return
  }

  await consumeSSEStream(response, onEvent)
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
  })

  if (!response.ok) {
    onError(new Error(`${response.status}: ${response.statusText}`))
    return
  }

  await consumeSSEStream(response, onEvent)
}
