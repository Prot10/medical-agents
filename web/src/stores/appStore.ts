import { create } from "zustand"

export type ActiveSection = "cases" | "dataset" | "episodes" | "rules" | "architecture" | "profiles"

interface DatasetFilters {
  conditions: string[]
  difficulties: string[]
  sex: string | null
}

interface AppState {
  selectedCaseId: string | null
  selectedProfileId: string
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

  // Reward panel under the timeline
  scoreOpen: boolean

  // Actions
  selectCase: (id: string) => void
  setProfile: (id: string) => void
  toggleDarkMode: () => void
  toggleGroundTruth: () => void
  setScoreOpen: (open: boolean) => void
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
  selectedProfileId: "policy-qwen3.5-9b",
  darkMode: false,
  showGroundTruth: false,
  rulesHospitalId: "us_mayo",
  selectedPathwayIndex: null,
  isCreatingPathway: false,
  scoreOpen: false,
  sidebarCollapsed: false,
  sidebarWidth: 272,
  activeSection: "cases",
  datasetFilters: { conditions: [], difficulties: [], sex: null },

  selectCase: (id) => set({ selectedCaseId: id }),
  setProfile: (id) => set({ selectedProfileId: id }),
  toggleDarkMode: () =>
    set((s) => {
      const next = !s.darkMode
      document.documentElement.classList.toggle("dark", next)
      return { darkMode: next }
    }),
  toggleGroundTruth: () => set((s) => ({ showGroundTruth: !s.showGroundTruth })),
  setScoreOpen: (open) => set({ scoreOpen: open }),
  toggleSidebar: () => set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),
  setSidebarWidth: (width) => set({ sidebarWidth: width }),
  setActiveSection: (section) => set({ activeSection: section }),
  setDatasetFilters: (filters) =>
    set((s) => ({ datasetFilters: { ...s.datasetFilters, ...filters } })),
  setRulesHospitalId: (id) => set({ rulesHospitalId: id, selectedPathwayIndex: null, isCreatingPathway: false }),
  selectPathway: (index) => set({ selectedPathwayIndex: index, isCreatingPathway: false }),
  setIsCreatingPathway: (creating) => set({ isCreatingPathway: creating, selectedPathwayIndex: null }),
}))
