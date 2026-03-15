import { FileText, Plus, Clock, AlertTriangle, ChevronDown, Search } from "lucide-react"
import { useState } from "react"
import { useAppStore } from "@/stores/appStore"
import { useHospitals, useHospitalRules } from "@/hooks/useCases"
import { cn } from "@/lib/utils"

export function HospitalRulesBrowser() {
  const { rulesHospitalId, setRulesHospitalId, selectedPathwayIndex, selectPathway, setIsCreatingPathway } = useAppStore()
  const { data: hospitals } = useHospitals()
  const { data: rulesData, isLoading } = useHospitalRules(rulesHospitalId)
  const [search, setSearch] = useState("")

  const pathways = rulesData?.pathways ?? []
  const filtered = pathways.filter(
    (p) =>
      !search ||
      p.name.toLowerCase().includes(search.toLowerCase()) ||
      p.triggers.some((t) => t.toLowerCase().includes(search.toLowerCase())),
  )

  if (isLoading) {
    return <div className="p-4 text-base text-muted-foreground">Loading rules...</div>
  }

  return (
    <div className="flex flex-col h-full">
      {/* Top bar */}
      <div className="p-3 border-b border-sidebar-border space-y-2">
        <div className="flex items-center gap-2">
          <div className="relative flex-1">
            <select
              value={rulesHospitalId}
              onChange={(e) => setRulesHospitalId(e.target.value)}
              className="w-full text-sm bg-sidebar-accent border border-sidebar-border rounded-lg px-2.5 py-1.5 text-sidebar-foreground focus:outline-none focus:ring-1 focus:ring-ring appearance-none pr-7"
            >
              {hospitals?.map((h) => (
                <option key={h.id} value={h.id}>{h.name}</option>
              ))}
            </select>
            <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 h-3 w-3 text-muted-foreground pointer-events-none" />
          </div>
          <button
            onClick={() => setIsCreatingPathway(true)}
            className="flex items-center gap-1 px-2.5 py-1.5 text-xs font-medium text-primary bg-primary/10 border border-primary/20 rounded-lg hover:bg-primary/15 transition-colors shrink-0"
          >
            <Plus className="h-3.5 w-3.5" />
            New
          </button>
        </div>
        <div className="relative">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search pathways..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-8 pr-3 py-2 text-base bg-sidebar-accent border border-sidebar-border rounded-lg focus:outline-none focus:ring-1 focus:ring-ring placeholder:text-muted-foreground/50"
          />
        </div>
      </div>

      {/* Pathway list */}
      <div className="flex-1 overflow-y-auto">
        {filtered.map((pathway, _filteredIdx) => {
          const realIndex = pathways.indexOf(pathway)
          const isSelected = selectedPathwayIndex === realIndex
          return (
            <button
              key={realIndex}
              onClick={() => selectPathway(isSelected ? null : realIndex)}
              className={cn(
                "w-full text-left px-3 py-2.5 border-b border-sidebar-border/50 transition-all hover:bg-sidebar-accent",
                isSelected && "bg-primary/10 border-l-[3px] border-l-primary",
              )}
            >
              <div className="flex items-center gap-2">
                <FileText className="h-3.5 w-3.5 text-muted-foreground shrink-0" />
                <span className="text-sm font-semibold text-sidebar-foreground truncate">
                  {pathway.name}
                </span>
              </div>
              <p className="text-xs text-muted-foreground mt-0.5 line-clamp-1 ml-5.5">
                {pathway.description}
              </p>
              <div className="flex flex-wrap gap-1 mt-1.5 ml-5.5">
                {pathway.triggers.slice(0, 3).map((t, i) => (
                  <span
                    key={i}
                    className="inline-flex items-center px-1.5 py-0.5 text-[10px] font-medium rounded bg-sky-500/10 text-sky-600 dark:text-sky-400 border border-sky-500/20"
                  >
                    {t}
                  </span>
                ))}
                {pathway.triggers.length > 3 && (
                  <span className="text-[10px] text-muted-foreground">
                    +{pathway.triggers.length - 3}
                  </span>
                )}
              </div>
              <div className="flex items-center gap-3 mt-1 ml-5.5 text-[10px] text-muted-foreground">
                <span className="flex items-center gap-0.5">
                  <Clock className="h-3 w-3" />
                  {pathway.steps.length} step{pathway.steps.length !== 1 ? "s" : ""}
                </span>
                {pathway.contraindicated.length > 0 && (
                  <span className="flex items-center gap-0.5 text-red-500/70">
                    <AlertTriangle className="h-3 w-3" />
                    {pathway.contraindicated.length}
                  </span>
                )}
              </div>
            </button>
          )
        })}
        {filtered.length === 0 && (
          <div className="p-4 text-sm text-muted-foreground text-center">
            {search ? "No matching pathways." : "No pathways defined."}
          </div>
        )}
      </div>
    </div>
  )
}
