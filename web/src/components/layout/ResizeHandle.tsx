import { Separator } from "react-resizable-panels"
import { GripVertical } from "lucide-react"

export function ResizeHandle() {
  return (
    <Separator className="relative flex items-center justify-center w-2 group">
      <div className="absolute inset-y-0 w-[2px] bg-border group-hover:bg-primary/50 group-data-[resize-handle-active]:bg-primary transition-colors rounded-full" />
      <div className="relative z-10 flex items-center justify-center h-8 w-4 rounded-sm opacity-0 group-hover:opacity-100 group-data-[resize-handle-active]:opacity-100 transition-opacity">
        <GripVertical className="h-4 w-4 text-muted-foreground" />
      </div>
    </Separator>
  )
}
