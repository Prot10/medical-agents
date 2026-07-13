import { create } from "zustand"
import type { AgentEvent } from "@/api/types"

export type RunStatus = "idle" | "running" | "complete" | "cancelled" | "error"

interface AgentState {
  status: RunStatus
  events: AgentEvent[]
  errorMessage: string | null

  // Streaming buffers (accumulated from delta events)
  streamingContent: string
  streamingThinkContent: string
  streamingTurnNumber: number

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
  appendEvent: (event: AgentEvent) => void
  setError: (msg: string) => void
  cancel: () => void
  reset: () => void
}

export const useAgentStore = create<AgentState>((set, get) => ({
  status: "idle",
  events: [],
  errorMessage: null,
  streamingContent: "",
  streamingThinkContent: "",
  streamingTurnNumber: 0,
  totalTokens: 0,
  startedAt: null,
  elapsedTime: 0,
  totalCost: 0,
  abortController: null,

  startRun: () =>
    set({ status: "running", events: [], errorMessage: null, streamingContent: "", streamingThinkContent: "", streamingTurnNumber: 0, totalTokens: 0, startedAt: Date.now(), elapsedTime: 0, totalCost: 0 }),

  setAbortController: (controller) => set({ abortController: controller }),

  appendEvent: (event) =>
    set((state) => {
      // Delta events: accumulate into streaming buffers, skip events array
      if (event.type === "content_delta") {
        return {
          streamingContent: state.streamingContent + (event.delta ?? ""),
          streamingTurnNumber: event.turn_number ?? state.streamingTurnNumber,
        }
      }

      if (event.type === "think_delta") {
        return {
          streamingThinkContent: state.streamingThinkContent + (event.delta ?? ""),
          streamingTurnNumber: event.turn_number ?? state.streamingTurnNumber,
        }
      }

      // Block events: push to events array, clear streaming buffers where appropriate
      const newEvents = [...state.events, event]
      let totalTokens = state.totalTokens
      let elapsedTime = state.elapsedTime
      let totalCost = state.totalCost

      if (event.token_usage) {
        totalTokens += event.token_usage.total_tokens || 0
      }
      if (event.type === "tool_result" && event.cost_usd) {
        totalCost += event.cost_usd
      }

      if (event.type === "thinking" || event.type === "assessment") {
        // Complete block arrived — clear streaming buffers
        return {
          events: newEvents,
          totalTokens,
          elapsedTime,
          totalCost,
          streamingContent: "",
          streamingThinkContent: "",
          streamingTurnNumber: 0,
        }
      }

      if (event.type === "run_complete") {
        return {
          events: newEvents,
          status: "complete" as const,
          totalTokens: event.total_tokens ?? totalTokens,
          elapsedTime: event.elapsed_time_seconds ?? elapsedTime,
          totalCost: event.total_cost_usd ?? totalCost,
          streamingContent: "",
          streamingThinkContent: "",
          streamingTurnNumber: 0,
        }
      }

      if (event.type === "error") {
        return {
          events: newEvents,
          status: "error" as const,
          errorMessage: event.message ?? "Unknown error",
          totalTokens,
          elapsedTime,
          totalCost,
        }
      }

      return { events: newEvents, totalTokens, elapsedTime, totalCost }
    }),

  setError: (msg) => set({ status: "error", errorMessage: msg }),

  cancel: () => {
    const { abortController, status, startedAt } = get()
    abortController?.abort()
    set({
      abortController: null,
      // Keep events collected so far; freeze the run in a terminal state
      ...(status === "running"
        ? {
            status: "cancelled" as const,
            elapsedTime: startedAt ? (Date.now() - startedAt) / 1000 : 0,
            streamingContent: "",
            streamingThinkContent: "",
            streamingTurnNumber: 0,
          }
        : {}),
    })
  },

  reset: () => {
    // Abort any in-flight run so a stale stream can't append into the reset store
    get().abortController?.abort()
    set({ status: "idle", events: [], errorMessage: null, streamingContent: "", streamingThinkContent: "", streamingTurnNumber: 0, totalTokens: 0, startedAt: null, elapsedTime: 0, totalCost: 0, abortController: null })
  },
}))
