import { Lightbulb } from "lucide-react"

export function ReflectionBlock() {
  return (
    <div className="flex justify-center py-0.5">
      <div className="reflection-badge bg-reflection/15 px-6 py-1.5 flex items-center gap-1.5">
        <Lightbulb className="h-3.5 w-3.5 text-reflection" />
        <span className="text-sm font-medium text-reflection">Analyzing Results</span>
      </div>
    </div>
  )
}
