import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { Loader2 } from "lucide-react"

import type { ReviewerProfile } from "@/api/types"
import { CodeEntryGate } from "@/components/gate/CodeEntryGate"
import { ConditionPicker } from "@/components/gate/ConditionPicker"
import { WorkspaceChooser } from "@/components/gate/WorkspaceChooser"
import { DarkModeSync } from "@/components/layout/DarkModeSync"
import { RecheckWorkspace } from "@/components/recheck/RecheckWorkspace"
import { ReviewWorkspace } from "@/components/review/ReviewWorkspace"
import { useReviewSets } from "@/hooks/useReview"
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

// After the code: the choice screen, then the chosen view.
function SignedIn({ profile }: { profile: ReviewerProfile }) {
  const workspace = useReviewStore((s) => s.workspace)
  if (!workspace) return <WorkspaceChooser profile={profile} />
  if (workspace.kind === "full") {
    if (!workspace.condition) return <ConditionPicker profile={profile} />
    return <ReviewWorkspace profile={profile} />
  }
  return <ReviewSetWorkspace profile={profile} setId={workspace.setId} />
}

function ReviewSetWorkspace({ profile, setId }: { profile: ReviewerProfile; setId: string }) {
  const sets = useReviewSets()
  const chooseWorkspace = useReviewStore((s) => s.chooseWorkspace)
  const reviewSet = sets.data?.find((s) => s.id === setId)
  if (sets.isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center text-muted-foreground">
        <Loader2 className="w-5 h-5 animate-spin" />
      </div>
    )
  }
  if (!reviewSet) {
    // The set was withdrawn on the server: go back to the choice.
    queueMicrotask(() => chooseWorkspace(null))
    return null
  }
  return <RecheckWorkspace profile={profile} reviewSet={reviewSet} />
}
