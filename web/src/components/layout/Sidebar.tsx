import { useEffect, useRef, useCallback, useState } from "react"
import { Stethoscope, BarChart3, History, PanelLeftClose, PanelLeft, Moon, Sun, ChevronDown, ChevronUp, Hospital, SlidersHorizontal, Shield, Play, Square, Network } from "lucide-react"
import { useQueryClient } from "@tanstack/react-query"
import { useAppStore } from "@/stores/appStore"
import { useModels, useProfiles } from "@/hooks/useCases"
import { api, consumeSSEStream } from "@/api/client"
import { useModelLoadingStore } from "@/stores/modelLoadingStore"
import type { LoadEvent } from "@/stores/modelLoadingStore"
import { cn } from "@/lib/utils"
import { LOOP_LABELS, profileLoop, profileModelKey } from "@/lib/policy"
import { CaseBrowser } from "@/components/cases/CaseBrowser"
import { DatasetOverview } from "@/components/dataset/DatasetOverview"
import { EpisodeBrowser } from "@/components/episodes/EpisodeBrowser"
import { ProfilesPanel } from "@/components/profiles/ProfilesPanel"
import { HospitalRulesBrowser } from "@/components/hospital/HospitalRulesBrowser"

const NAV_ITEMS = [
  { id: "cases" as const, label: "Cases", icon: Stethoscope },
  { id: "dataset" as const, label: "Dataset", icon: BarChart3 },
  { id: "episodes" as const, label: "Episodes", icon: History },
  { id: "rules" as const, label: "Rules", icon: Shield },
  { id: "architecture" as const, label: "Architecture", icon: Network },
  { id: "profiles" as const, label: "Profiles", icon: SlidersHorizontal },
]

export function Sidebar() {
  const {
    sidebarCollapsed, toggleSidebar, activeSection, setActiveSection,
    darkMode, toggleDarkMode,
    selectedProfileId, setProfile,
  } = useAppStore()
  const { data: models } = useModels()
  const { data: profiles } = useProfiles()
  const { isLoading, modelKey: loadingKey, startLoading, handleEvent, reset: resetLoading } = useModelLoadingStore()
  const queryClient = useQueryClient()
  const abortRef = useRef<AbortController | null>(null)

  const currentProfile = profiles?.find((p) => p.profile_id === selectedProfileId)
  const modelKey = profileModelKey(currentProfile)
  const currentModel = models?.find((m) => m.key === modelKey)

  // Auto-select a profile whose model is already served, only on initial load
  const hasAutoSelected = useRef(false)
  useEffect(() => {
    if (!models || !profiles || hasAutoSelected.current) return
    hasAutoSelected.current = true
    if (currentModel?.status === "ready") return
    const ready = profiles.find((p) => models.find((m) => m.key === profileModelKey(p))?.status === "ready")
    if (ready) setProfile(ready.profile_id)
  }, [models, profiles, currentModel, setProfile])

  const triggerLoad = useCallback(async (key: string) => {
    const model = models?.find((m) => m.key === key)
    if (!model || model.status === "ready") return

    if (abortRef.current) abortRef.current.abort()
    const controller = new AbortController()
    abortRef.current = controller

    startLoading(key, model.name)

    try {
      const response = await api.loadModel(key, controller.signal)
      if (!response.ok) {
        handleEvent({ phase: "error", message: `Server error: ${response.status}` })
        return
      }

      await consumeSSEStream<LoadEvent>(response, (event) => {
        handleEvent(event)
        if (event.phase === "ready" || event.phase === "error") {
          queryClient.invalidateQueries({ queryKey: ["models"] })
          abortRef.current = null
        }
      })
    } catch (err) {
      if (err instanceof DOMException && err.name === "AbortError") return
      handleEvent({ phase: "error", message: err instanceof Error ? err.message : "Connection failed" })
    }
  }, [models, startLoading, handleEvent, queryClient])

  // Abort any in-flight model-load stream when the sidebar unmounts
  useEffect(() => {
    return () => {
      abortRef.current?.abort()
      abortRef.current = null
    }
  }, [])

  const handleStopLoad = useCallback(() => {
    if (abortRef.current) { abortRef.current.abort(); abortRef.current = null }
    resetLoading()
    api.unloadModel().catch(() => {})
    queryClient.invalidateQueries({ queryKey: ["models"] })
  }, [resetLoading, queryClient])

  const [footerExpanded, setFooterExpanded] = useState(false)

  const statusColor = {
    ready: "bg-emerald-500",
    loading: "bg-amber-500",
    offline: "bg-zinc-500",
  }[currentModel?.status ?? "offline"]
  const canLoad = currentModel && currentModel.status !== "ready" && !isLoading
  const isLoadingThis = isLoading && loadingKey === modelKey

  return (
    <aside
      className="flex flex-col h-full w-full bg-sidebar relative overflow-hidden"
    >
      {/* Header */}
      <div className="flex items-center gap-2.5 px-3 py-3 border-b border-sidebar-border">
        {!sidebarCollapsed && (
          <div className="flex items-center gap-2.5 flex-1 min-w-0">
            <div className="relative h-7 w-7 shrink-0 rounded-lg bg-gradient-to-br from-sky-500 to-emerald-500 flex items-center justify-center">
              <Hospital className="h-4 w-4 text-white" />
            </div>
            <div className="min-w-0">
              <h1 className="text-base font-bold tracking-tight leading-none text-sidebar-foreground">NeuroAgent</h1>
              <span className="text-xs text-muted-foreground tracking-wider uppercase">Dashboard</span>
            </div>
          </div>
        )}
        <button
          onClick={toggleSidebar}
          className="p-1.5 rounded-lg hover:bg-sidebar-accent transition-colors text-muted-foreground hover:text-sidebar-foreground shrink-0"
          title={sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
        >
          {sidebarCollapsed ? <PanelLeft className="h-4 w-4" /> : <PanelLeftClose className="h-4 w-4" />}
        </button>
      </div>

      {/* Navigation */}
      <nav className="px-2 py-2 space-y-0.5">
        {NAV_ITEMS.map((item) => {
          const isActive = activeSection === item.id
          return (
            <button
              key={item.id}
              onClick={() => setActiveSection(item.id)}
              title={sidebarCollapsed ? item.label : undefined}
              className={cn(
                "w-full flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-base font-medium transition-all duration-150",
                isActive
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-sidebar-accent hover:text-sidebar-foreground",
              )}
            >
              <item.icon className={cn("h-4.5 w-4.5 shrink-0", isActive && "text-primary")} />
              {!sidebarCollapsed && <span>{item.label}</span>}
            </button>
          )
        })}
      </nav>

      {/* Section content */}
      <div className="flex-1 overflow-hidden border-t border-sidebar-border mt-1">
        {!sidebarCollapsed && (
          <div className="h-full overflow-y-auto">
            {activeSection === "cases" && <CaseBrowser />}
            {activeSection === "dataset" && <DatasetOverview />}
            {activeSection === "episodes" && <EpisodeBrowser />}
            {activeSection === "rules" && <HospitalRulesBrowser />}
            {activeSection === "profiles" && <ProfilesPanel />}
          </div>
        )}
      </div>

      {/* Footer: Collapsible profile picker + Dark mode */}
      <div className={cn("border-t border-sidebar-border", sidebarCollapsed ? "px-2 py-2" : "")}>
        {!sidebarCollapsed ? (
          <>
            {/* Compact summary bar — always visible */}
            <button
              onClick={() => setFooterExpanded((v) => !v)}
              className="w-full flex items-center gap-2 px-3 py-2 hover:bg-sidebar-accent transition-colors text-sm"
            >
              <span className={cn("h-2 w-2 rounded-full shrink-0", statusColor, isLoadingThis && "animate-pulse")} />
              <span className="truncate text-sidebar-foreground font-medium font-mono">
                {selectedProfileId}
              </span>
              <span className="ml-auto shrink-0 text-muted-foreground">
                {footerExpanded ? <ChevronDown className="h-3.5 w-3.5" /> : <ChevronUp className="h-3.5 w-3.5" />}
              </span>
            </button>

            {/* Expanded picker */}
            {footerExpanded && (
              <div className="px-3 pb-3 space-y-2">
                <div className="space-y-1">
                  <label className="text-xs uppercase tracking-wider font-semibold text-muted-foreground">Profile</label>
                  <div className="relative">
                    <select
                      value={selectedProfileId}
                      onChange={(e) => setProfile(e.target.value)}
                      className="w-full text-sm bg-sidebar-accent border border-sidebar-border rounded-lg pl-2.5 pr-7 py-1.5 text-sidebar-foreground focus:outline-none focus:ring-1 focus:ring-ring appearance-none font-mono"
                    >
                      {profiles?.map((p) => (
                        <option key={p.profile_id} value={p.profile_id}>{p.profile_id}</option>
                      ))}
                    </select>
                    <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 h-3 w-3 text-muted-foreground pointer-events-none" />
                  </div>
                </div>

                {/* The profile's model and its serving state */}
                <div className="space-y-1">
                  <label className="text-xs uppercase tracking-wider font-semibold text-muted-foreground">Model</label>
                  <div className="flex items-center gap-1.5">
                    <div className="flex-1 min-w-0 flex items-center gap-2 text-sm bg-sidebar-accent border border-sidebar-border rounded-lg px-2.5 py-1.5">
                      <span className={cn("h-2 w-2 rounded-full shrink-0", statusColor, isLoadingThis && "animate-pulse")} />
                      <span className="truncate text-sidebar-foreground">{currentModel?.name ?? modelKey ?? "—"}</span>
                      <span className="ml-auto text-xs text-muted-foreground shrink-0">{currentModel?.status ?? "offline"}</span>
                    </div>
                    {isLoadingThis ? (
                      <button
                        onClick={handleStopLoad}
                        className="px-2 py-1.5 text-xs font-medium text-red-400 bg-red-500/10 border border-red-500/20 rounded-lg hover:bg-red-500/15 transition-colors shrink-0"
                        title="Stop loading"
                      >
                        <Square className="h-3.5 w-3.5 fill-current" />
                      </button>
                    ) : canLoad && modelKey ? (
                      <button
                        onClick={() => triggerLoad(modelKey)}
                        className="px-2.5 py-1.5 text-xs font-medium text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 rounded-lg hover:bg-emerald-500/15 transition-colors shrink-0 flex items-center gap-1"
                        title="Load this model"
                      >
                        <Play className="h-3 w-3 fill-current" />
                        Load
                      </button>
                    ) : null}
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {LOOP_LABELS[profileLoop(currentProfile) ?? ""] ?? profileLoop(currentProfile)} loop
                    {currentProfile && ` · ${currentProfile.max_turns} turns`}
                  </div>
                </div>
              </div>
            )}

            {/* Dark mode toggle */}
            <div className="px-3 pb-2">
              <button
                onClick={toggleDarkMode}
                className="w-full flex items-center gap-2 px-2.5 py-1.5 rounded-lg hover:bg-sidebar-accent transition-colors text-muted-foreground hover:text-sidebar-foreground"
                title={darkMode ? "Switch to light mode" : "Switch to dark mode"}
              >
                {darkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
                <span className="text-sm">{darkMode ? "Light mode" : "Dark mode"}</span>
              </button>
            </div>
          </>
        ) : (
          <button
            onClick={toggleDarkMode}
            className="p-2 mx-auto flex rounded-lg hover:bg-sidebar-accent transition-colors text-muted-foreground hover:text-sidebar-foreground"
            title={darkMode ? "Switch to light mode" : "Switch to dark mode"}
          >
            {darkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          </button>
        )}
      </div>
    </aside>
  )
}
