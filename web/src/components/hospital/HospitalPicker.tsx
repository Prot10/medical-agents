import { Building2 } from "lucide-react"
import { useHospitals } from "@/hooks/useCases"
import { useAppStore } from "@/stores/appStore"

export function HospitalPicker() {
  const { data: hospitals } = useHospitals()
  const { selectedHospital, setHospital } = useAppStore()

  return (
    <div className="flex items-center gap-1.5">
      <Building2 className="h-3.5 w-3.5 text-muted-foreground" />
      <select
        value={selectedHospital}
        onChange={(e) => setHospital(e.target.value)}
        className="text-xs bg-secondary border border-border rounded-md px-2 py-1 text-foreground focus:outline-none focus:ring-1 focus:ring-ring"
      >
        {hospitals?.map((h) => (
          <option key={h.id} value={h.id}>
            {h.name}
          </option>
        ))}
      </select>
    </div>
  )
}
