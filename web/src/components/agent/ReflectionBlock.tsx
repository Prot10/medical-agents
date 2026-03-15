import { RotateCcw } from "lucide-react"

export function ReflectionBlock() {
  return (
    <div className="flex items-center gap-3 py-2 px-1">
      <div className="flex-1 h-px bg-gradient-to-r from-transparent to-reflection/25" />
      <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-reflection/10 border border-reflection/15">
        <RotateCcw className="h-3 w-3 text-reflection/70" />
        <span className="text-sm tracking-wider uppercase font-semibold text-reflection/70">Reflect</span>
      </div>
      <div className="flex-1 h-px bg-gradient-to-l from-transparent to-reflection/25" />
    </div>
  )
}
