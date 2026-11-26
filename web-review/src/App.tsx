import { QueryClient, QueryClientProvider, useQuery } from "@tanstack/react-query"
import { Loader2 } from "lucide-react"
import { useEffect } from "react"

import type { ReviewerProfile } from "@/api/types"
import { AgentApp } from "@/components/agent/AgentApp"
import { CodeEntryGate } from "@/components/gate/CodeEntryGate"
import { ConditionPicker } from "@/components/gate/ConditionPicker"
import { WorkspaceChooser } from "@/components/gate/WorkspaceChooser"
import { DarkModeSync } from "@/components/layout/DarkModeSync"
import { RecheckWorkspace } from "@/components/recheck/RecheckWorkspace"
import { ReviewWorkspace } from "@/components/review/ReviewWorkspace"
import { useReviewSets, validateAndLoadProfile } from "@/hooks/useReview"
import { useReviewStore } from "@/stores/reviewStore"

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

export function App() {
  const profile = useReviewStore((s) => s.profile)
  return (
    <QueryClientProvider client={queryClient}>
      <DarkModeSync />
      {profile ? <SignedIn profile={profile} /> : <CodeEntryGate />}
    </QueryClientProvider>
  )
}

function Spinner() {
  return (
    <div className="min-h-screen flex items-center justify-center text-muted-foreground">
      <Loader2 className="w-5 h-5 animate-spin" />
    </div>
  )
}

// After the code: the choice screen, then the chosen view.
function SignedIn({ profile }: { profile: ReviewerProfile }) {
  const workspace = useReviewStore((s) => s.workspace)
  const refreshProfile = useReviewStore((s) => s.refreshProfile)
  const chooseWorkspace = useReviewStore((s) => s.chooseWorkspace)
  // The stored profile may predate a change of assignment on the server: read it again before
  // opening any view, so a guided code never lands on a view it may not open.
  const fresh = useQuery({
    queryKey: ["reviewers", "me", profile.code],
    queryFn: () => validateAndLoadProfile(profile.code),
    staleTime: Infinity,
  })
  useEffect(() => {
    if (fresh.data) refreshProfile(fresh.data)
  }, [fresh.data, refreshProfile])
  // Until the store catches up (effect above), decide from the fresh profile, never the stale one.
  const current = fresh.data ?? profile
  const assigned = current.review_sets ?? []
  const guided = assigned.length > 0
  const single = assigned.length === 1 ? assigned[0] : null
  const inAssignedSet = workspace?.kind === "set" && assigned.includes(workspace.setId)
  // A guided code with one set goes straight into it; with several, it picks among them only.
  const misplaced = guided && !inAssignedSet && (single !== null || workspace !== null)
  useEffect(() => {
    if (fresh.data && misplaced) chooseWorkspace(single ? { kind: "set", setId: single } : null)
  }, [fresh.data, misplaced, single, chooseWorkspace])

  if (!fresh.data && !fresh.isError) return <Spinner />
  // An agent-mode code opens the agent-mode study and nothing else.
  if (current.sections?.length) return <AgentApp profile={current} />
  if (misplaced) return <Spinner />
  if (!workspace) return <WorkspaceChooser profile={profile} />
  if (workspace.kind === "full" && !guided) {
    if (!workspace.condition) return <ConditionPicker profile={profile} />
    return <ReviewWorkspace profile={profile} />
  }
  if (workspace.kind !== "set") return <WorkspaceChooser profile={profile} />
  return <ReviewSetWorkspace profile={profile} setId={workspace.setId} />
}

function ReviewSetWorkspace({ profile, setId }: { profile: ReviewerProfile; setId: string }) {
  const sets = useReviewSets()
  const chooseWorkspace = useReviewStore((s) => s.chooseWorkspace)
  const reviewSet = sets.data?.find((s) => s.id === setId)
  if (sets.isLoading) return <Spinner />
  if (!reviewSet) {
    // The set was withdrawn on the server: go back to the choice.
    queueMicrotask(() => chooseWorkspace(null))
    return null
  }
  return <RecheckWorkspace profile={profile} reviewSet={reviewSet} />
}
