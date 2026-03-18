import { create } from "zustand"

export type ActiveSection = "cases" | "dataset" | "traces" | "rules" | "settings"

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

  // Rules
  rulesHospitalId: string
  selectedPathwayIndex: number | null
  isCreatingPathway: boolean

  // Dual-model specialist
  dualModelEnabled: boolean
  specialistModel: string

  // Oracle
  oracleOpen: boolean
  oracleTrigger: number  // increment to trigger evaluation

  // Actions
  selectCase: (id: string) => void
  setHospital: (id: string) => void
  setModel: (key: string) => void
  setEvaluatorModel: (key: string) => void
  setDualModel: (enabled: boolean) => void
  setSpecialistModel: (key: string) => void
  toggleDarkMode: () => void
  toggleGroundTruth: () => void
  setOracleOpen: (open: boolean) => void
  triggerOracle: () => void
  toggleSidebar: () => void
  setSidebarWidth: (width: number) => void
  setActiveSection: (section: ActiveSection) => void
  setDatasetFilters: (filters: Partial<DatasetFilters>) => void
  setRulesHospitalId: (id: string) => void
  selectPathway: (index: number | null) => void
  setIsCreatingPathway: (creating: boolean) => void
}

export const useAppStore = create<AppState>((set) => ({
  selectedCaseId: null,
  selectedHospital: "us_mayo",
  selectedModel: "qwen3.5-9b",
  selectedEvaluatorModel: "",
  dualModelEnabled: false,
  specialistModel: "medgemma-4b",
  darkMode: false,
  showGroundTruth: false,
  rulesHospitalId: "us_mayo",
  selectedPathwayIndex: null,
  isCreatingPathway: false,
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
  setDualModel: (enabled) => set({ dualModelEnabled: enabled }),
  setSpecialistModel: (key) => set({ specialistModel: key }),
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
  setRulesHospitalId: (id) => set({ rulesHospitalId: id, selectedPathwayIndex: null, isCreatingPathway: false }),
  selectPathway: (index) => set({ selectedPathwayIndex: index, isCreatingPathway: false }),
  setIsCreatingPathway: (creating) => set({ isCreatingPathway: creating, selectedPathwayIndex: null }),
}))
