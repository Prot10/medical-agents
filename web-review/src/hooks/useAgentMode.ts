import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

import type {
  ActionBody,
  AdminAgentOverview,
  AdminEpisodeDetail,
  AgentSectionSummary,
  AgentWorklist,
  CaseState,
} from "@/api/agentTypes"
import { fetchJSON, postJSON } from "@/api/client"

const QK = {
  sections: () => ["agent-mode", "sections"] as const,
  worklist: (section: string) => ["agent-mode", "worklist", section] as const,
  state: (section: string, number: number) => ["agent-mode", "case", section, number] as const,
  adminOverview: () => ["agent-mode", "admin", "overview"] as const,
  adminEpisode: (section: string, reviewer: string, number: number) =>
    ["agent-mode", "admin", "episode", section, reviewer, number] as const,
}

export function useAgentSections() {
  return useQuery({
    queryKey: QK.sections(),
    queryFn: () => fetchJSON<AgentSectionSummary[]>("/agent-mode/sections"),
  })
}

export function useAgentWorklist(section: string) {
  return useQuery({
    queryKey: QK.worklist(section),
    queryFn: () => fetchJSON<AgentWorklist>(`/agent-mode/sections/${section}`),
  })
}

/** Opens the case (the server creates it on first call and resumes it afterwards). */
export function useCaseState(section: string, number: number) {
  return useQuery({
    queryKey: QK.state(section, number),
    queryFn: () => postJSON<CaseState>(`/agent-mode/sections/${section}/cases/${number}/start`, {}),
    staleTime: Infinity,
    gcTime: 0,
    retry: false,
  })
}

export function useSendAction(section: string, number: number) {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (body: ActionBody) =>
      postJSON<CaseState>(`/agent-mode/sections/${section}/cases/${number}/actions`, body),
    onSuccess: (state) => {
      queryClient.setQueryData(QK.state(section, number), state)
      void queryClient.invalidateQueries({ queryKey: QK.worklist(section) })
      void queryClient.invalidateQueries({ queryKey: QK.sections() })
    },
    onError: () => {
      // A refused step (stale page, locked case): show what the server has.
      void queryClient.invalidateQueries({ queryKey: QK.state(section, number) })
    },
  })
}

export function useAdminAgentOverview() {
  return useQuery({
    queryKey: QK.adminOverview(),
    queryFn: () => fetchJSON<AdminAgentOverview>("/admin/agent-mode/overview"),
    retry: false,
  })
}

export function useAdminAgentEpisode(section: string, reviewer: string, number: number, enabled: boolean) {
  return useQuery({
    queryKey: QK.adminEpisode(section, reviewer, number),
    queryFn: () =>
      fetchJSON<AdminEpisodeDetail>(
        `/admin/agent-mode/sections/${section}/reviewers/${reviewer}/cases/${number}`,
      ),
    enabled,
  })
}
