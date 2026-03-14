import { useQuery } from "@tanstack/react-query"
import { api } from "@/api/client"

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
    queryFn: api.getModels,
    staleTime: 10_000,
  })
}
