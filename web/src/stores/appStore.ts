import { create } from "zustand"

interface AppState {
  selectedCaseId: string | null
  selectedHospital: string
  selectedModel: string
  darkMode: boolean
  showGroundTruth: boolean

  selectCase: (id: string) => void
  setHospital: (id: string) => void
  setModel: (key: string) => void
  toggleDarkMode: () => void
  toggleGroundTruth: () => void
}

export const useAppStore = create<AppState>((set) => ({
  selectedCaseId: null,
  selectedHospital: "us_mayo",
  selectedModel: "qwen3.5-9b",
  darkMode: true,
  showGroundTruth: false,

  selectCase: (id) => set({ selectedCaseId: id }),
  setHospital: (id) => set({ selectedHospital: id }),
  setModel: (key) => set({ selectedModel: key }),
  toggleDarkMode: () =>
    set((s) => {
      const next = !s.darkMode
      document.documentElement.classList.toggle("dark", next)
      return { darkMode: next }
    }),
  toggleGroundTruth: () => set((s) => ({ showGroundTruth: !s.showGroundTruth })),
}))
