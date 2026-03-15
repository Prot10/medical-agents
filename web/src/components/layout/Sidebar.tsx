import { useEffect } from "react"
import { Stethoscope, BarChart3, History, PanelLeftClose, PanelLeft, Moon, Sun, ChevronDown, Hospital, Settings } from "lucide-react"
import { useAppStore } from "@/stores/appStore"
import { useModels, useHospitals } from "@/hooks/useCases"
import { cn } from "@/lib/utils"
import { CaseBrowser } from "@/components/cases/CaseBrowser"
import { DatasetOverview } from "@/components/dataset/DatasetOverview"
import { TraceBrowser } from "@/components/traces/TraceBrowser"
import { SettingsPanel } from "@/components/settings/SettingsPanel"

const NAV_ITEMS = [
  { id: "cases" as const, label: "Cases", icon: Stethoscope },
  { id: "dataset" as const, label: "Dataset", icon: BarChart3 },
  { id: "traces" as const, label: "Traces", icon: History },
  { id: "settings" as const, label: "Settings", icon: Settings },
]

export function Sidebar() {
  const {
    sidebarCollapsed, toggleSidebar, activeSection, setActiveSection,
    darkMode, toggleDarkMode,
    selectedModel, setModel, selectedEvaluatorModel, setEvaluatorModel,
    selectedHospital, setHospital,
  } = useAppStore()
  const { data: models } = useModels()
  const { data: hospitals } = useHospitals()

  // Auto-select first ready model if current selection is offline
  useEffect(() => {
    if (!models) return
    const current = models.find((m) => m.key === selectedModel)
    if (!current || current.status !== "ready") {
      const firstReady = models.find((m) => m.status === "ready")
      if (firstReady) setModel(firstReady.key)
    }
  }, [models, selectedModel, setModel])

  const currentModel = models?.find((m) => m.key === selectedModel)
  const statusColor = {
    ready: "bg-emerald-500",
    loading: "bg-amber-500",
    offline: "bg-zinc-500",
  }[currentModel?.status ?? "offline"]

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
            {activeSection === "traces" && <TraceBrowser />}
            {activeSection === "settings" && <SettingsPanel />}
          </div>
        )}
      </div>

      {/* Footer: Model + Hospital pickers + Dark mode */}
      <div className={cn("border-t border-sidebar-border", sidebarCollapsed ? "px-2 py-2" : "px-3 py-3 space-y-2")}>
        {!sidebarCollapsed ? (
          <>
            {/* Agent Model picker */}
            <div className="space-y-1">
              <label className="text-xs uppercase tracking-wider font-semibold text-muted-foreground">Agent Model</label>
              <div className="relative">
                <select
                  value={selectedModel}
                  onChange={(e) => setModel(e.target.value)}
                  className="w-full text-sm bg-sidebar-accent border border-sidebar-border rounded-lg px-2.5 py-1.5 text-sidebar-foreground focus:outline-none focus:ring-1 focus:ring-ring appearance-none pr-7"
                >
                  {models?.filter((m) => m.provider !== "copilot").map((m) => (
                    <option key={m.key} value={m.key}>
                      {m.name} {m.status !== "ready" ? `(${m.status})` : ""}
                    </option>
                  ))}
                  {models?.some((m) => m.provider === "copilot") && (
                    <optgroup label="GitHub Copilot">
                      {models?.filter((m) => m.provider === "copilot").map((m) => (
                        <option key={m.key} value={m.key}>{m.name}</option>
                      ))}
                    </optgroup>
                  )}
                </select>
                <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 h-3 w-3 text-muted-foreground pointer-events-none" />
                <span className={`absolute left-2 top-1/2 -translate-y-1/2 h-2 w-2 rounded-full ${statusColor}`} />
              </div>
            </div>

            {/* Evaluator Model picker */}
            <div className="space-y-1">
              <label className="text-xs uppercase tracking-wider font-semibold text-muted-foreground">Evaluator Model</label>
              <div className="relative">
                <select
                  value={selectedEvaluatorModel}
                  onChange={(e) => setEvaluatorModel(e.target.value)}
                  className="w-full text-sm bg-sidebar-accent border border-sidebar-border rounded-lg px-2.5 py-1.5 text-sidebar-foreground focus:outline-none focus:ring-1 focus:ring-ring appearance-none pr-7"
                >
                  <option value="">Select evaluator...</option>
                  {models?.filter((m) => m.provider !== "copilot").map((m) => (
                    <option key={m.key} value={m.key}>
                      {m.name} {m.status !== "ready" ? `(${m.status})` : ""}
                    </option>
                  ))}
                  {models?.some((m) => m.provider === "copilot") && (
                    <optgroup label="GitHub Copilot">
                      {models?.filter((m) => m.provider === "copilot").map((m) => (
                        <option key={m.key} value={m.key}>{m.name}</option>
                      ))}
                    </optgroup>
                  )}
                </select>
                <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 h-3 w-3 text-muted-foreground pointer-events-none" />
              </div>
            </div>

            {/* Hospital picker */}
            <div className="space-y-1">
              <label className="text-xs uppercase tracking-wider font-semibold text-muted-foreground">Hospital</label>
              <div className="relative">
                <select
                  value={selectedHospital}
                  onChange={(e) => setHospital(e.target.value)}
                  className="w-full text-sm bg-sidebar-accent border border-sidebar-border rounded-lg px-2.5 py-1.5 text-sidebar-foreground focus:outline-none focus:ring-1 focus:ring-ring appearance-none pr-7"
                >
                  {hospitals?.map((h) => (
                    <option key={h.id} value={h.id}>{h.name}</option>
                  ))}
                </select>
                <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 h-3 w-3 text-muted-foreground pointer-events-none" />
              </div>
            </div>
          </>
        ) : null}

        {/* Dark mode toggle */}
        <button
          onClick={toggleDarkMode}
          className={cn(
            "flex items-center gap-2 rounded-lg hover:bg-sidebar-accent transition-colors text-muted-foreground hover:text-sidebar-foreground",
            sidebarCollapsed ? "p-2 mx-auto" : "w-full px-2.5 py-1.5",
          )}
          title={darkMode ? "Switch to light mode" : "Switch to dark mode"}
        >
          {darkMode ? <Sun className="h-4 w-4" /> : <Moon className="h-4 w-4" />}
          {!sidebarCollapsed && <span className="text-sm">{darkMode ? "Light mode" : "Dark mode"}</span>}
        </button>
      </div>
    </aside>
  )
}
