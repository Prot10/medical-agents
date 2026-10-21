import { useCallback, useRef } from "react"
import { useAppStore } from "@/stores/appStore"

const MIN_WIDTH = 200
const MAX_WIDTH = 400

export function SidebarResizeHandle() {
  const dragRef = useRef<{ startX: number; startWidth: number } | null>(null)

  const handleMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
    const currentWidth = useAppStore.getState().sidebarWidth
    dragRef.current = { startX: e.clientX, startWidth: currentWidth }

    const handleMouseMove = (e: MouseEvent) => {
      if (!dragRef.current) return
      const newWidth = dragRef.current.startWidth + (e.clientX - dragRef.current.startX)
      const clamped = Math.min(MAX_WIDTH, Math.max(MIN_WIDTH, newWidth))
      useAppStore.getState().setSidebarWidth(clamped)
    }

    const handleMouseUp = () => {
      dragRef.current = null
      document.removeEventListener("mousemove", handleMouseMove)
      document.removeEventListener("mouseup", handleMouseUp)
      document.body.style.cursor = ""
      document.body.style.userSelect = ""
    }

    document.addEventListener("mousemove", handleMouseMove)
    document.addEventListener("mouseup", handleMouseUp)
    document.body.style.cursor = "col-resize"
    document.body.style.userSelect = "none"
  }, [])

  return (
    <div
      onMouseDown={handleMouseDown}
      className="w-1.5 cursor-col-resize group flex items-center justify-center shrink-0 hover:bg-primary/10 transition-colors"
    >
      <div className="w-[1px] h-full bg-sidebar-border group-hover:bg-primary/40 transition-colors" />
    </div>
  )
}
