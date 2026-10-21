import type {
  CaseIndexEntry, CaseDetail, Hospital, HospitalRulesDetail, PathwayDetail, ModelInfo, Profile,
  EpisodeSummary, ClinicalEpisode, EngineeringReward, RunStreamFrame,
} from "./types"

const BASE = "/api/v1"

async function fetchJSON<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, init)
  if (!res.ok) throw new Error(`${res.status}: ${await errorDetail(res)}`)
  return res.json()
}

/** FastAPI puts the reason in `detail` (a string, or an object with a message). */
async function errorDetail(res: Response): Promise<string> {
  try {
    const body = await res.json()
    const detail = body?.detail
    if (typeof detail === "string") return detail
    if (detail?.message) return detail.message
  } catch {
    // not JSON
  }
  return res.statusText
}

export const api = {
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
  loadModel: (modelKey: string, signal?: AbortSignal) =>
    fetch(`${BASE}/models/${modelKey}/load`, { method: "POST", signal }),
  unloadModel: () =>
    fetchJSON<{ status: string; message: string }>(`${BASE}/models/unload`, { method: "POST" }),
  getProfiles: () => fetchJSON<Profile[]>(`${BASE}/profiles`),
  getEpisodes: () => fetchJSON<EpisodeSummary[]>(`${BASE}/episodes`),
  getEpisode: (id: string) => fetchJSON<ClinicalEpisode>(`${BASE}/episodes/${id}`),
  getEpisodeReward: (id: string) => fetchJSON<EngineeringReward>(`${BASE}/episodes/${id}/reward`),
  deleteEpisode: (id: string) =>
    fetch(`${BASE}/episodes/${id}`, { method: "DELETE" }).then(async (res) => {
      if (!res.ok) throw new Error(`${res.status}: ${await errorDetail(res)}`)
    }),
}

/** Parse SSE events from a ReadableStream, calling onEvent for each. */
export async function consumeSSEStream<T>(
  response: Response,
  onEvent: (event: T) => void,
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

function parseSSELine<T>(raw: string, onEvent: (event: T) => void): void {
  const line = raw.trim()
  if (line.startsWith("data: ")) {
    try {
      onEvent(JSON.parse(line.slice(6)) as T)
    } catch {
      // skip malformed events
    }
  }
}

/** Run one case through a checked profile, receiving each episode event as it is appended. */
export async function streamRun(
  caseId: string,
  profileId: string,
  onFrame: (frame: RunStreamFrame) => void,
  signal?: AbortSignal,
): Promise<void> {
  const response = await fetch(`${BASE}/runs/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ case_id: caseId, profile_id: profileId }),
    signal,
    cache: "no-store",
  })

  if (!response.ok) {
    throw new Error(`${response.status}: ${await errorDetail(response)}`)
  }

  await consumeSSEStream<RunStreamFrame>(response, onFrame)
}
