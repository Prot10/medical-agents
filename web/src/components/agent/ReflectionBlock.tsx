import { RotateCcw } from "lucide-react"

export function ReflectionBlock() {
  return (
    <div className="flex items-center gap-2.5 py-1.5 px-1">
      <div className="flex-1 h-px bg-gradient-to-r from-transparent to-reflection/20" />
      <div className="flex items-center gap-1.5 text-[10px] text-reflection/60">
        <RotateCcw className="h-2.5 w-2.5" />
        <span className="tracking-wider uppercase font-medium">Reflect</span>
      </div>
      <div className="flex-1 h-px bg-gradient-to-l from-transparent to-reflection/20" />
    </div>
  )
}
