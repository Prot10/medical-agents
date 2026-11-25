import { create } from "zustand"

const STORAGE_KEY = "neurobench.agent_mode"

/** Where the physician is in the agent-mode study. Kept for the browser tab only; the case
 * itself lives on the server, so a new visit resumes from the home screen. */
interface AgentLocation {
  section: string | null
  caseNumber: number | null
}

export interface AgentStore extends AgentLocation {
  openSection: (section: string | null) => void
  openCase: (caseNumber: number | null) => void
  reset: () => void
}

function load(): AgentLocation {
  try {
    const raw = sessionStorage.getItem(STORAGE_KEY)
    if (raw) return JSON.parse(raw) as AgentLocation
  } catch {
    // storage blocked: start from the home screen
  }
  return { section: null, caseNumber: null }
}

function save(location: AgentLocation) {
  try {
    sessionStorage.setItem(STORAGE_KEY, JSON.stringify(location))
  } catch {
    // not remembered
  }
}

export const useAgentStore = create<AgentStore>((set) => ({
  ...load(),
  openSection: (section) => {
    save({ section, caseNumber: null })
    set({ section, caseNumber: null })
  },
  openCase: (caseNumber) =>
    set((state) => {
      save({ section: state.section, caseNumber })
      return { caseNumber }
    }),
  reset: () => {
    save({ section: null, caseNumber: null })
    set({ section: null, caseNumber: null })
  },
}))
