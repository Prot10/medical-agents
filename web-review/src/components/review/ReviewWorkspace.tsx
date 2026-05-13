import type { ReviewerProfile } from "@/api/types"
import { useReviewStore } from "@/stores/reviewStore"
import { AppShell } from "@/components/layout/AppShell"
import { AdminTab } from "@/components/admin/AdminTab"
import { CasesTab } from "@/components/cases/CasesTab"
import { MethodologyTab } from "@/components/methodology/MethodologyTab"
import { OverviewTab } from "@/components/overview/OverviewTab"

export function ReviewWorkspace({ profile }: { profile: ReviewerProfile }) {
  const activeTab = useReviewStore((s) => s.activeTab)
  return (
    <AppShell profile={profile}>
      {activeTab === "overview" && <OverviewTab profile={profile} />}
      {activeTab === "cases" && <CasesTab />}
      {activeTab === "methodology" && <MethodologyTab />}
      {activeTab === "admin" && profile.role === "admin" && <AdminTab />}
    </AppShell>
  )
}
