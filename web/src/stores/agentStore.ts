import { create } from "zustand"
import type { AgentEvent } from "@/api/types"

export type RunStatus = "idle" | "running" | "complete" | "error"

interface AgentState {
  status: RunStatus
  events: AgentEvent[]
  errorMessage: string | null

  // Accumulated metrics
  totalTokens: number
  elapsedTime: number

  // Actions
  startRun: () => void
  appendEvent: (event: AgentEvent) => void
  setError: (msg: string) => void
  reset: () => void
}

export const useAgentStore = create<AgentState>((set) => ({
  status: "idle",
  events: [],
  errorMessage: null,
  totalTokens: 0,
  elapsedTime: 0,

  startRun: () =>
    set({ status: "running", events: [], errorMessage: null, totalTokens: 0, elapsedTime: 0 }),

  appendEvent: (event) =>
    set((state) => {
      const newEvents = [...state.events, event]
      let totalTokens = state.totalTokens
      let elapsedTime = state.elapsedTime

      if (event.token_usage) {
        totalTokens += event.token_usage.total_tokens || 0
      }

      if (event.type === "run_complete") {
        return {
          events: newEvents,
          status: "complete",
          totalTokens: event.total_tokens ?? totalTokens,
          elapsedTime: event.elapsed_time_seconds ?? elapsedTime,
        }
      }

      if (event.type === "error") {
        return {
          events: newEvents,
          status: "error",
          errorMessage: event.message ?? "Unknown error",
          totalTokens,
          elapsedTime,
        }
      }

      return { events: newEvents, totalTokens, elapsedTime }
    }),

  setError: (msg) => set({ status: "error", errorMessage: msg }),

  reset: () =>
    set({ status: "idle", events: [], errorMessage: null, totalTokens: 0, elapsedTime: 0 }),
}))
