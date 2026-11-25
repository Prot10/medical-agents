import { BrainCircuit, ChevronRight, LogOut, Moon, Sun } from "lucide-react"

import type { ReviewerProfile } from "@/api/types"
import { useAgentStore } from "@/stores/agentStore"
import { useReviewStore } from "@/stores/reviewStore"

/** Top bar of the agent-mode study: where you are, and the way out. */
export function AgentHeader({
  profile,
  crumbs,
  children,
}: {
  profile: ReviewerProfile
  crumbs: Array<{ label: string; onClick?: () => void }>
  children?: React.ReactNode
}) {
  const signOut = useReviewStore((s) => s.signOut)
  const darkMode = useReviewStore((s) => s.darkMode)
  const setDarkMode = useReviewStore((s) => s.setDarkMode)
  const reset = useAgentStore((s) => s.reset)
  return (
    <header className="sticky top-0 z-30 bg-background/90 backdrop-blur border-b border-border">
      <div className="px-4 sm:px-6 h-14 flex items-center justify-between gap-3">
        <nav className="flex items-center gap-1.5 min-w-0 text-sm" aria-label="Breadcrumb">
          <span className="w-8 h-8 rounded-lg bg-primary/10 text-primary flex items-center justify-center flex-shrink-0">
            <BrainCircuit className="w-4 h-4" />
          </span>
          {crumbs.map((crumb, i) => (
            <span key={i} className="flex items-center gap-1.5 min-w-0">
              {i > 0 && <ChevronRight className="w-3.5 h-3.5 text-muted-foreground flex-shrink-0" />}
              {crumb.onClick ? (
                <button type="button" onClick={crumb.onClick} className="text-muted-foreground hover:text-foreground truncate px-1 rounded">
                  {crumb.label}
                </button>
              ) : (
                <span className="font-semibold truncate px-1">{crumb.label}</span>
              )}
            </span>
          ))}
        </nav>
        <div className="flex items-center gap-1 sm:gap-2 flex-shrink-0">
          {children}
          <span className="hidden md:inline text-sm text-muted-foreground px-1">{profile.name}</span>
          <button
            type="button"
            onClick={() => setDarkMode(!darkMode)}
            className="p-2 rounded-md text-muted-foreground hover:bg-secondary/70"
            aria-label={darkMode ? "Light mode" : "Dark mode"}
          >
            {darkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
          </button>
          <button
            type="button"
            onClick={() => {
              reset()
              signOut()
            }}
            className="p-2 rounded-md text-muted-foreground hover:bg-secondary/70"
            aria-label="Sign out"
            title="Sign out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </header>
  )
}
