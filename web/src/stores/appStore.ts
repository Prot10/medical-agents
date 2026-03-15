import { create } from "zustand"

export type ActiveSection = "cases" | "dataset" | "traces" | "settings"

interface DatasetFilters {
  conditions: string[]
  difficulties: string[]
  sex: string | null
}

interface AppState {
  selectedCaseId: string | null
  selectedHospital: string
  selectedModel: string
  selectedEvaluatorModel: string
  darkMode: boolean
  showGroundTruth: boolean

  // Sidebar
  sidebarCollapsed: boolean
  sidebarWidth: number
  activeSection: ActiveSection
  datasetFilters: DatasetFilters

  // Oracle
  oracleOpen: boolean
  oracleTrigger: number  // increment to trigger evaluation

  // Actions
  selectCase: (id: string) => void
  setHospital: (id: string) => void
  setModel: (key: string) => void
  setEvaluatorModel: (key: string) => void
  toggleDarkMode: () => void
  toggleGroundTruth: () => void
  setOracleOpen: (open: boolean) => void
  triggerOracle: () => void
  toggleSidebar: () => void
  setSidebarWidth: (width: number) => void
  setActiveSection: (section: ActiveSection) => void
  setDatasetFilters: (filters: Partial<DatasetFilters>) => void
}

export const useAppStore = create<AppState>((set) => ({
  selectedCaseId: null,
  selectedHospital: "us_mayo",
  selectedModel: "qwen3.5-9b",
  selectedEvaluatorModel: "",
  darkMode: false,
  showGroundTruth: false,
  oracleOpen: false,
  oracleTrigger: 0,
  sidebarCollapsed: false,
  sidebarWidth: 272,
  activeSection: "cases",
  datasetFilters: { conditions: [], difficulties: [], sex: null },

  selectCase: (id) => set({ selectedCaseId: id }),
  setHospital: (id) => set({ selectedHospital: id }),
  setModel: (key) => set({ selectedModel: key }),
  setEvaluatorModel: (key) => set({ selectedEvaluatorModel: key }),
  toggleDarkMode: () =>
    set((s) => {
      const next = !s.darkMode
      document.documentElement.classList.toggle("dark", next)
      return { darkMode: next }
    }),
  toggleGroundTruth: () => set((s) => ({ showGroundTruth: !s.showGroundTruth })),
  setOracleOpen: (open) => set({ oracleOpen: open }),
  triggerOracle: () => set((s) => ({ oracleOpen: true, oracleTrigger: s.oracleTrigger + 1 })),
  toggleSidebar: () => set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),
  setSidebarWidth: (width) => set({ sidebarWidth: width }),
  setActiveSection: (section) => set({ activeSection: section }),
  setDatasetFilters: (filters) =>
    set((s) => ({ datasetFilters: { ...s.datasetFilters, ...filters } })),
}))
