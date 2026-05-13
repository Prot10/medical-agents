import type { ReviewerProfile } from "@/api/types"
import { useReviewStore } from "@/stores/reviewStore"
import { Header } from "./Header"

export function AppShell({
  profile,
  children,
}: {
  profile: ReviewerProfile
  children: React.ReactNode
}) {
  const activeTab = useReviewStore((s) => s.activeTab)
  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground">
      <Header profile={profile} />
      <main className="flex-1 min-h-0" key={activeTab}>
        {children}
      </main>
    </div>
  )
}
