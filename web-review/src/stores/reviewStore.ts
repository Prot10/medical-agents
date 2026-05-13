import { create } from "zustand"

import type { ReviewStatus, ReviewerProfile, Severity } from "@/api/types"

const PROFILE_STORAGE_KEY = "neurobench.reviewer"
const ONBOARDED_STORAGE_KEY = "neurobench.review_onboarded"
const DARK_MODE_STORAGE_KEY = "neurobench.review_dark_mode"

export type ReviewTab = "overview" | "cases" | "methodology" | "admin"

export interface AnnotationDraft {
  fieldPath: string
  fieldSnippet?: string
  // Anchor coordinates in viewport coords (for popover positioning).
  x: number
  y: number
}

export interface ReviewStore {
  profile: ReviewerProfile | null
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

  setProfile: (profile: ReviewerProfile | null) => void
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
  darkMode: loadDarkMode(),
  activeTab: "overview",
  datasetVersion: "v5",
  selectedCaseId: null,
  filterStatus: "all",
  filterConditions: [],
  filterSeverity: "all",
  searchText: "",
  annotationDraft: null,
  onboarded: loadOnboarded(),

  setProfile: (profile) => {
    if (typeof localStorage !== "undefined") {
      if (profile) {
        localStorage.setItem(PROFILE_STORAGE_KEY, JSON.stringify(profile))
      } else {
        localStorage.removeItem(PROFILE_STORAGE_KEY)
      }
    }
    set({ profile })
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
    set({
      profile: null,
      activeTab: "overview",
      selectedCaseId: null,
      annotationDraft: null,
    })
  },
}))
