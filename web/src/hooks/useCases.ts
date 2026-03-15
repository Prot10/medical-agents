import { useQuery } from "@tanstack/react-query"
import { api } from "@/api/client"
import type { ModelInfo } from "@/api/types"

export function useCases() {
  return useQuery({
    queryKey: ["cases"],
    queryFn: api.getCases,
    staleTime: Infinity,
  })
}

export function useCaseDetail(caseId: string | null) {
  return useQuery({
    queryKey: ["case", caseId],
    queryFn: () => api.getCase(caseId!),
    enabled: !!caseId,
    staleTime: Infinity,
  })
}

export function useHospitals() {
  return useQuery({
    queryKey: ["hospitals"],
    queryFn: api.getHospitals,
    staleTime: Infinity,
  })
}

export function useModels() {
  return useQuery({
    queryKey: ["models"],
    queryFn: async (): Promise<ModelInfo[]> => {
      // Fetch local models first, then try copilot (may not be available)
      const local = await api.getModels()
      try {
        const copilot = await api.copilotModels()
        if (copilot.length > 0) return [...local, ...copilot]
      } catch {
        // Copilot not configured or not authenticated — silently skip
      }
      return local
    },
    staleTime: 10_000,
  })
}

export function useHospitalRules(hospitalId: string) {
  return useQuery({
    queryKey: ["hospital-rules", hospitalId],
    queryFn: () => api.getHospitalRules(hospitalId),
    enabled: !!hospitalId,
    staleTime: 30_000,
  })
}

export function useCopilotStatus() {
  return useQuery({
    queryKey: ["copilot-status"],
    queryFn: async () => {
      try {
        return await api.copilotStatus()
      } catch {
        return { authenticated: false, copilot_access: false }
      }
    },
    staleTime: 5_000,
    retry: false,
  })
}
