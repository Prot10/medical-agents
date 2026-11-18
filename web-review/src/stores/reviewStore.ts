import { create } from "zustand"

import type { ReviewStatus, ReviewerProfile, Severity } from "@/api/types"

const PROFILE_STORAGE_KEY = "neurobench.reviewer"
const ONBOARDED_STORAGE_KEY = "neurobench.review_onboarded"
const DARK_MODE_STORAGE_KEY = "neurobench.review_dark_mode"
const WORKSPACE_STORAGE_KEY = "neurobench.review_workspace"
const DEFAULT_DATASET_VERSION = "neurobench"

export type ReviewTab = "overview" | "cases" | "tools" | "methodology" | "admin"

/**
 * Which view the reviewer chose after entering the code: the full review of the dataset, or a
 * review set (a fixed list of cases re-reviewed in a space of its own, addressed by its id).
 * `null` shows the choice screen.
 */
export type Workspace = { kind: "full" } | { kind: "set"; setId: string }

export interface AnnotationDraft {
  fieldPath: string
  fieldSnippet?: string
  // Anchor coordinates in viewport coords (for popover positioning).
  x: number
  y: number
}

export interface ReviewStore {
  profile: ReviewerProfile | null
  workspace: Workspace | null
  darkMode: boolean
  activeTab: ReviewTab
  datasetVersion: string
  selectedCaseId: string | null
  filterStatus: ReviewStatus | "all"
  filterConditions: string[]
  filterSeverity: Severity | "all"
  searchText: string
  annotationDraft: AnnotationDraft | null
  onboarded: boolean
  /** Set when an authenticated request 401s, so the gate can explain why. */
  sessionMessage: string | null

  handleAuthExpired: () => void
  setProfile: (profile: ReviewerProfile | null) => void
  chooseWorkspace: (workspace: Workspace | null) => void
  setDarkMode: (dark: boolean) => void
  setActiveTab: (tab: ReviewTab) => void
  setDatasetVersion: (version: string) => void
  setSelectedCaseId: (caseId: string | null) => void
  setFilterStatus: (status: ReviewStatus | "all") => void
  setFilterConditions: (conditions: string[]) => void
  setFilterSeverity: (severity: Severity | "all") => void
  setSearchText: (text: string) => void
  setAnnotationDraft: (draft: AnnotationDraft | null) => void
  markOnboarded: () => void
  signOut: () => void
}

function loadProfile(): ReviewerProfile | null {
  if (typeof localStorage === "undefined") return null
  try {
    const raw = localStorage.getItem(PROFILE_STORAGE_KEY)
    if (!raw) return null
    return JSON.parse(raw) as ReviewerProfile
  } catch {
    return null
  }
}

// Kept for the browser tab only: a reload returns to the chosen view, a new visit asks again.
function loadWorkspace(): Workspace | null {
  if (typeof sessionStorage === "undefined") return null
  try {
    const raw = sessionStorage.getItem(WORKSPACE_STORAGE_KEY)
    return raw ? (JSON.parse(raw) as Workspace) : null
  } catch {
    return null
  }
}

function storeWorkspace(workspace: Workspace | null) {
  if (typeof sessionStorage === "undefined") return
  try {
    if (workspace) sessionStorage.setItem(WORKSPACE_STORAGE_KEY, JSON.stringify(workspace))
    else sessionStorage.removeItem(WORKSPACE_STORAGE_KEY)
  } catch {
    // storage blocked: the choice simply is not remembered
  }
}

function versionOf(workspace: Workspace | null): string {
  return workspace?.kind === "set" ? workspace.setId : DEFAULT_DATASET_VERSION
}

const initialWorkspace = loadProfile() ? loadWorkspace() : null

function loadDarkMode(): boolean {
  if (typeof localStorage === "undefined") return false
  const stored = localStorage.getItem(DARK_MODE_STORAGE_KEY)
  if (stored != null) return stored === "true"
  return false
}

function loadOnboarded(): boolean {
  if (typeof localStorage === "undefined") return false
  return localStorage.getItem(ONBOARDED_STORAGE_KEY) === "true"
}

export const useReviewStore = create<ReviewStore>((set) => ({
  profile: loadProfile(),
  workspace: initialWorkspace,
  darkMode: loadDarkMode(),
  activeTab: "overview",
  datasetVersion: versionOf(initialWorkspace),
  selectedCaseId: null,
  filterStatus: "all",
  filterConditions: [],
  filterSeverity: "all",
  searchText: "",
  annotationDraft: null,
  onboarded: loadOnboarded(),
  sessionMessage: null,

  handleAuthExpired: () => {
    if (typeof localStorage !== "undefined") {
      localStorage.removeItem(PROFILE_STORAGE_KEY)
    }
    storeWorkspace(null)
    set({
      profile: null,
      workspace: null,
      datasetVersion: DEFAULT_DATASET_VERSION,
      activeTab: "overview",
      selectedCaseId: null,
      annotationDraft: null,
      sessionMessage:
        "Your session ended — your reviewer code may have been disabled or rotated. Please re-enter it.",
    })
  },
  setProfile: (profile) => {
    if (typeof localStorage !== "undefined") {
      if (profile) {
        localStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(profile))
      } else {
        localStorage.removeItem(PROFILE_STORAGE_KEY)
      }
    }
    // A new code always lands on the choice screen.
    storeWorkspace(null)
    set({ profile, workspace: null, sessionMessage: null })
  },
  chooseWorkspace: (workspace) => {
    storeWorkspace(workspace)
    set({
      workspace,
      datasetVersion: versionOf(workspace),
      activeTab: "overview",
      selectedCaseId: null,
      annotationDraft: null,
      filterStatus: "all",
      filterConditions: [],
    })
  },
  setDarkMode: (dark) => {
    if (typeof localStorage !== "undefined") {
      localStorage.setItem(DARK_MODE_STORAGE_KEY, dark ? "true" : "false")
    }
    set({ darkMode: dark })
  },
  setActiveTab: (activeTab) => set({ activeTab }),
  setDatasetVersion: (datasetVersion) =>
    set({
      datasetVersion,
      selectedCaseId: null,
      filterStatus: "all",
      filterConditions: [],
    }),
  setSelectedCaseId: (selectedCaseId) => set({ selectedCaseId }),
  setFilterStatus: (filterStatus) => set({ filterStatus }),
  setFilterConditions: (filterConditions) => set({ filterConditions }),
  setFilterSeverity: (filterSeverity) => set({ filterSeverity }),
  setSearchText: (searchText) => set({ searchText }),
  setAnnotationDraft: (annotationDraft) => set({ annotationDraft }),
  markOnboarded: () => {
    if (typeof localStorage !== "undefined") {
      localStorage.setItem(ONBOARDED_STORAGE_KEY, "true")
    }
    set({ onboarded: true })
  },
  signOut: () => {
    if (typeof localStorage !== "undefined") {
      localStorage.removeItem(PROFILE_STORAGE_KEY)
    }
    storeWorkspace(null)
    set({
      profile: null,
      workspace: null,
      datasetVersion: DEFAULT_DATASET_VERSION,
      activeTab: "overview",
      selectedCaseId: null,
      annotationDraft: null,
    })
  },
}))
