import { create } from "zustand"

export interface LoadEvent {
  phase: "unloading" | "starting" | "loading" | "weights" | "cuda_graphs" | "ready" | "error"
  message: string
  model?: string
  model_name?: string
  size_gb?: number
  expected_seconds?: number
  elapsed?: number
  progress?: number
  log?: string | null
  detail?: string
}

interface ModelLoadingState {
  isLoading: boolean
  modelKey: string | null
  modelName: string | null
  phase: LoadEvent["phase"] | "idle"
  message: string
  progress: number
  elapsed: number
  expectedSeconds: number
  sizeGb: number
  logLine: string | null
  // Actions
  startLoading: (key: string, name: string) => void
  handleEvent: (event: LoadEvent) => void
  reset: () => void
}

export const useModelLoadingStore = create<ModelLoadingState>((set) => ({
  isLoading: false,
  modelKey: null,
  modelName: null,
  phase: "idle",
  message: "",
  progress: 0,
  elapsed: 0,
  expectedSeconds: 120,
  sizeGb: 0,
  logLine: null,

  startLoading: (key, name) =>
    set({
      isLoading: true,
      modelKey: key,
      modelName: name,
      phase: "starting",
      message: `Starting ${name}...`,
      progress: 0,
      elapsed: 0,
      logLine: null,
    }),

  handleEvent: (event) =>
    set((s) => ({
      phase: event.phase,
      message: event.message,
      progress: event.progress ?? s.progress,
      elapsed: event.elapsed ?? s.elapsed,
      expectedSeconds: event.expected_seconds ?? s.expectedSeconds,
      sizeGb: event.size_gb ?? s.sizeGb,
      modelName: event.model_name ?? s.modelName,
      logLine: event.log ?? s.logLine,
      isLoading: event.phase !== "ready" && event.phase !== "error",
    })),

  reset: () =>
    set({
      isLoading: false,
      modelKey: null,
      modelName: null,
      phase: "idle",
      message: "",
      progress: 0,
      elapsed: 0,
      expectedSeconds: 120,
      sizeGb: 0,
      logLine: null,
    }),
}))
