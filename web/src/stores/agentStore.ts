import { create } from "zustand"
import type { EngineeringReward, EpisodeEvent, RunStreamFrame } from "@/api/types"

export type RunStatus = "idle" | "running" | "complete" | "failed" | "cancelled" | "error"

interface AgentState {
  status: RunStatus
  events: EpisodeEvent[]
  errorMessage: string | null

  /** Persisted id of the episode on screen, once the server has saved it. */
  episodeId: string | null
  /** Engineering reward of the episode on screen. */
  reward: EngineeringReward | null

  // Accumulated metrics
  totalTokens: number
  /** Wall-clock start of the current run (ms epoch); used to derive live elapsed time. */
  startedAt: number | null
  elapsedTime: number
  totalCost: number

  // In-flight stream controller — lives in the store so any component
  // (Header stop button, CaseBrowser case switch, ...) can abort the run.
  abortController: AbortController | null

  // Actions
  startRun: () => void
  setAbortController: (controller: AbortController | null) => void
  appendFrame: (frame: RunStreamFrame) => void
  loadEpisode: (events: EpisodeEvent[], episodeId: string) => void
  setReward: (reward: EngineeringReward | null) => void
  setError: (msg: string) => void
  cancel: () => void
  reset: () => void
}

const EMPTY = {
  events: [] as EpisodeEvent[],
  errorMessage: null,
  episodeId: null,
  reward: null,
  totalTokens: 0,
  elapsedTime: 0,
  totalCost: 0,
}

function eventMetrics(event: EpisodeEvent): { tokens: number; cost: number } {
  if (event.type === "model.requested") return { tokens: event.prompt_tokens, cost: 0 }
  if (event.type === "action.proposed") return { tokens: event.completion_tokens, cost: 0 }
  if (event.type === "observation.received") return { tokens: 0, cost: event.cost_usd }
  return { tokens: 0, cost: 0 }
}

function terminalStatus(events: EpisodeEvent[]): RunStatus {
  return events[events.length - 1]?.type === "run.failed" ? "failed" : "complete"
}

function episodeSeconds(events: EpisodeEvent[]): number {
  if (events.length < 2) return 0
  return (Date.parse(events[events.length - 1].timestamp) - Date.parse(events[0].timestamp)) / 1000
}

function elapsed(startedAt: number | null): number {
  return startedAt ? (Date.now() - startedAt) / 1000 : 0
}

export const useAgentStore = create<AgentState>((set, get) => ({
  status: "idle",
  ...EMPTY,
  startedAt: null,
  abortController: null,

  startRun: () => set({ status: "running", ...EMPTY, startedAt: Date.now() }),

  setAbortController: (controller) => set({ abortController: controller }),

  appendFrame: (frame) =>
    set((state) => {
      if (frame.type === "stream.error") {
        return { status: "error" as const, errorMessage: frame.message, elapsedTime: elapsed(state.startedAt) }
      }
      if (frame.type === "stream.result") {
        return {
          status: terminalStatus(state.events),
          episodeId: frame.episode_id,
          reward: { reward: frame.reward, policy_review_status: frame.policy_review_status },
          elapsedTime: elapsed(state.startedAt),
        }
      }
      const { tokens, cost } = eventMetrics(frame)
      return {
        events: [...state.events, frame],
        totalTokens: state.totalTokens + tokens,
        totalCost: state.totalCost + cost,
      }
    }),

  loadEpisode: (events, episodeId) =>
    set({
      ...EMPTY,
      status: terminalStatus(events),
      events,
      episodeId,
      startedAt: null,
      totalTokens: events.reduce((sum, e) => sum + eventMetrics(e).tokens, 0),
      totalCost: events.reduce((sum, e) => sum + eventMetrics(e).cost, 0),
      elapsedTime: episodeSeconds(events),
    }),

  setReward: (reward) => set({ reward }),

  setError: (msg) => set((state) => ({ status: "error", errorMessage: msg, elapsedTime: elapsed(state.startedAt) })),

  cancel: () => {
    const { abortController, status, startedAt } = get()
    abortController?.abort()
    set({
      abortController: null,
      // Keep events collected so far; freeze the run in a terminal state
      ...(status === "running" ? { status: "cancelled" as const, elapsedTime: elapsed(startedAt) } : {}),
    })
  },

  reset: () => {
    // Abort any in-flight run so a stale stream can't append into the reset store
    get().abortController?.abort()
    set({ status: "idle", ...EMPTY, startedAt: null, abortController: null })
  },
}))
