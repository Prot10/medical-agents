import { QueryClient, QueryClientProvider } from "@tanstack/react-query"

import { CodeEntryGate } from "@/components/gate/CodeEntryGate"
import { DarkModeSync } from "@/components/layout/DarkModeSync"
import { ReviewWorkspace } from "@/components/review/ReviewWorkspace"
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
      {profile ? <ReviewWorkspace profile={profile} /> : <CodeEntryGate />}
    </QueryClientProvider>
  )
}
