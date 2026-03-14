import { Header } from "./Header"
import { CaseBrowser } from "@/components/cases/CaseBrowser"
import { PatientViewer } from "@/components/patient/PatientViewer"
import { AgentTimeline } from "@/components/agent/AgentTimeline"

export function AppShell() {
  return (
    <>
      <Header />
      <div className="flex flex-1 overflow-hidden">
        {/* Left panel: Case browser */}
        <div className="w-64 flex-shrink-0 border-r border-border overflow-y-auto bg-card">
          <CaseBrowser />
        </div>

        {/* Center panel: Patient viewer */}
        <div className="flex-1 overflow-y-auto">
          <PatientViewer />
        </div>

        {/* Right panel: Agent timeline */}
        <div className="w-[480px] flex-shrink-0 border-l border-border flex flex-col bg-card">
          <AgentTimeline />
        </div>
      </div>
    </>
  )
}
