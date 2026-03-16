import { create } from "zustand"
import type { AgentEvent } from "@/api/types"

export type RunStatus = "idle" | "running" | "complete" | "error"

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
  streamingContent: "",
  streamingThinkContent: "",
  streamingTurnNumber: 0,
  totalTokens: 0,
  elapsedTime: 0,

  startRun: () =>
    set({ status: "running", events: [], errorMessage: null, streamingContent: "", streamingThinkContent: "", streamingTurnNumber: 0, totalTokens: 0, elapsedTime: 0 }),

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

      if (event.token_usage) {
        totalTokens += event.token_usage.total_tokens || 0
      }

      if (event.type === "thinking" || event.type === "assessment") {
        // Complete block arrived — clear streaming buffers
        const base = {
          events: newEvents,
          totalTokens,
          elapsedTime,
          streamingContent: "",
          streamingThinkContent: "",
          streamingTurnNumber: 0,
        }
        if (event.type === "assessment") return base
        return base
      }

      if (event.type === "run_complete") {
        return {
          events: newEvents,
          status: "complete" as const,
          totalTokens: event.total_tokens ?? totalTokens,
          elapsedTime: event.elapsed_time_seconds ?? elapsedTime,
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
        }
      }

      return { events: newEvents, totalTokens, elapsedTime }
    }),

  setError: (msg) => set({ status: "error", errorMessage: msg }),

  reset: () =>
    set({ status: "idle", events: [], errorMessage: null, streamingContent: "", streamingThinkContent: "", streamingTurnNumber: 0, totalTokens: 0, elapsedTime: 0 }),
}))
