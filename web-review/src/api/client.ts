import { useReviewStore } from "@/stores/reviewStore"

const BASE = import.meta.env.VITE_REVIEW_API_BASE ?? "/api/v1"

export class ReviewApiError extends Error {
  status: number
  body: unknown

  constructor(message: string, status: number, body: unknown) {
    super(message)
    this.name = "ReviewApiError"
    this.status = status
    this.body = body
  }
}

export async function fetchJSON<T>(
  path: string,
  init: RequestInit & { skipAuth?: boolean } = {},
): Promise<T> {
  const { skipAuth, headers: extraHeaders, ...rest } = init

  const headers = new Headers(extraHeaders)
  headers.set("Accept", "application/json")
  if (rest.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json")
  }
  if (!skipAuth) {
    const code = useReviewStore.getState().profile?.code
    if (code) headers.set("X-Reviewer-Code", code)
  }

  const url = path.startsWith("http") ? path : `${BASE}${path}`
  const response = await fetch(url, { ...rest, headers })
  if (!response.ok) {
    let body: unknown = null
    try {
      body = await response.json()
    } catch {
      // ignore
    }
    const detail =
      (body as { detail?: string } | null)?.detail ?? `Request failed (${response.status})`
    throw new ReviewApiError(detail, response.status, body)
  }
  if (response.status === 204) return undefined as T
  return (await response.json()) as T
}

export async function postJSON<T>(path: string, body: unknown): Promise<T> {
  return fetchJSON<T>(path, { method: "POST", body: JSON.stringify(body) })
}

export async function putJSON<T>(path: string, body: unknown): Promise<T> {
  return fetchJSON<T>(path, { method: "PUT", body: JSON.stringify(body) })
}

export async function patchJSON<T>(path: string, body: unknown): Promise<T> {
  return fetchJSON<T>(path, { method: "PATCH", body: JSON.stringify(body) })
}

export async function deleteJSON<T>(path: string): Promise<T> {
  return fetchJSON<T>(path, { method: "DELETE" })
}
