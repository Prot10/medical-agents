import { Moon, Sun } from "lucide-react"
import { useAppStore } from "@/stores/appStore"
import { HospitalPicker } from "@/components/hospital/HospitalPicker"
import { ModelPicker } from "@/components/model/ModelPicker"

export function Header() {
  const { darkMode, toggleDarkMode } = useAppStore()

  return (
    <header className="flex items-center gap-4 px-4 py-2 border-b border-border bg-card/80 backdrop-blur-sm">
      <div className="flex items-center gap-2.5">
        {/* Custom logo mark */}
        <div className="relative h-6 w-6">
          <div className="absolute inset-0 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 opacity-90" />
          <svg viewBox="0 0 24 24" className="relative h-6 w-6 text-white p-[5px]" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2a7 7 0 0 1 7 7c0 2.5-1.5 4.5-3 6l-4 5-4-5c-1.5-1.5-3-3.5-3-6a7 7 0 0 1 7-7z" />
            <circle cx="12" cy="9" r="1.5" fill="currentColor" />
          </svg>
        </div>
        <div>
          <h1 className="text-sm font-semibold tracking-tight leading-none">NeuroAgent</h1>
          <span className="text-[9px] text-muted-foreground/60 tracking-wider uppercase">Dashboard</span>
        </div>
      </div>

      <div className="flex-1" />

      <ModelPicker />

      <div className="w-px h-4 bg-border" />

      <HospitalPicker />

      <div className="w-px h-4 bg-border" />

      <button
        onClick={toggleDarkMode}
        className="p-1.5 rounded-md hover:bg-accent transition-colors text-muted-foreground hover:text-foreground"
        title={darkMode ? "Switch to light mode" : "Switch to dark mode"}
      >
        {darkMode ? <Sun className="h-3.5 w-3.5" /> : <Moon className="h-3.5 w-3.5" />}
      </button>
    </header>
  )
}
