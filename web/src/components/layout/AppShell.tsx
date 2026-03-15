import { Group, Panel, Separator } from "react-resizable-panels"
import { Header } from "./Header"
import { Sidebar } from "./Sidebar"
import { SidebarResizeHandle } from "./SidebarResizeHandle"
import { PatientViewer } from "@/components/patient/PatientViewer"
import { AgentTimeline } from "@/components/agent/AgentTimeline"
import { OraclePanel } from "@/components/agent/OraclePanel"
import { DatasetDashboard } from "@/components/dataset/DatasetDashboard"
import { useAppStore } from "@/stores/appStore"
import { GripVertical, MoreHorizontal } from "lucide-react"

function VerticalResizeHandle() {
  return (
    <Separator className="relative flex items-center justify-center h-2 group">
      <div className="absolute inset-x-0 h-[2px] bg-border group-hover:bg-primary/50 group-data-[resize-handle-active]:bg-primary transition-colors rounded-full" />
      <div className="relative z-10 flex items-center justify-center w-8 h-4 rounded-sm opacity-0 group-hover:opacity-100 group-data-[resize-handle-active]:opacity-100 transition-opacity">
        <MoreHorizontal className="h-4 w-4 text-muted-foreground" />
      </div>
    </Separator>
  )
}

function HorizontalResizeHandle() {
  return (
    <Separator className="relative flex items-center justify-center w-2 group">
      <div className="absolute inset-y-0 w-[2px] bg-border group-hover:bg-primary/50 group-data-[resize-handle-active]:bg-primary transition-colors rounded-full" />
      <div className="relative z-10 flex items-center justify-center h-8 w-4 rounded-sm opacity-0 group-hover:opacity-100 group-data-[resize-handle-active]:opacity-100 transition-opacity">
        <GripVertical className="h-4 w-4 text-muted-foreground" />
      </div>
    </Separator>
  )
}

export function AppShell() {
  const activeSection = useAppStore((s) => s.activeSection)
  const sidebarCollapsed = useAppStore((s) => s.sidebarCollapsed)
  const sidebarWidth = useAppStore((s) => s.sidebarWidth)
  const oracleOpen = useAppStore((s) => s.oracleOpen)

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div
        className="shrink-0 flex border-r border-sidebar-border"
        style={{ width: sidebarCollapsed ? 64 : sidebarWidth }}
      >
        <Sidebar />
        {!sidebarCollapsed && <SidebarResizeHandle />}
      </div>

      {/* Main content */}
      <main className="flex-1 flex flex-col overflow-hidden min-w-0">
        <Header />
        <Group orientation="horizontal" className="flex-1">
          {/* Content panel */}
          <Panel defaultSize={55} minSize={30}>
            <div className="h-full overflow-hidden">
              {activeSection === "dataset" ? <DatasetDashboard /> : <PatientViewer />}
            </div>
          </Panel>
          <HorizontalResizeHandle />
          {/* Agent panel — optionally split with oracle */}
          <Panel defaultSize={45} minSize={25}>
            {oracleOpen ? (
              <Group orientation="vertical" className="h-full">
                <Panel defaultSize={50} minSize={20}>
                  <div className="h-full overflow-hidden">
                    <AgentTimeline />
                  </div>
                </Panel>
                <VerticalResizeHandle />
                <Panel defaultSize={50} minSize={20}>
                  <div className="h-full overflow-hidden">
                    <OraclePanel />
                  </div>
                </Panel>
              </Group>
            ) : (
              <div className="h-full overflow-hidden">
                <AgentTimeline />
              </div>
            )}
          </Panel>
        </Group>
      </main>
    </div>
  )
}
