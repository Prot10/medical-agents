import { Cpu } from "lucide-react"
import { useModels } from "@/hooks/useCases"
import { useAppStore } from "@/stores/appStore"

const statusColors: Record<string, string> = {
  ready: "bg-green-500",
  loading: "bg-yellow-500",
  offline: "bg-zinc-500",
}

export function ModelPicker() {
  const { data: models } = useModels()
  const { selectedModel, setModel } = useAppStore()

  const currentModel = models?.find((m) => m.key === selectedModel)
  const statusColor = statusColors[currentModel?.status ?? "offline"]

  return (
    <div className="flex items-center gap-1.5">
      <Cpu className="h-3.5 w-3.5 text-muted-foreground" />
      <select
        value={selectedModel}
        onChange={(e) => setModel(e.target.value)}
        className="text-xs bg-secondary border border-border rounded-md px-2 py-1 text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
      >
        {models?.map((m) => (
          <option key={m.key} value={m.key}>
            {m.name} {m.status === "ready" ? "" : `(${m.status})`}
          </option>
        ))}
      </select>
      <span className={`h-2 w-2 rounded-full ${statusColor}`} title={currentModel?.status} />
    </div>
  )
}
