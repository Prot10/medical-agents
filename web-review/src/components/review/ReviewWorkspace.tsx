import { useEffect } from "react"

import type { ReviewerProfile } from "@/api/types"
import { useToolReview } from "@/hooks/useToolReview"
import { useReviewStore } from "@/stores/reviewStore"
import { AppShell } from "@/components/layout/AppShell"
import { AdminTab } from "@/components/admin/AdminTab"
import { CasesTab } from "@/components/cases/CasesTab"
import { MethodologyTab } from "@/components/methodology/MethodologyTab"
import { OverviewTab } from "@/components/overview/OverviewTab"
import { ToolReviewTab } from "@/components/tools/ToolReviewTab"

export function ReviewWorkspace({ profile }: { profile: ReviewerProfile }) {
  const activeTab = useReviewStore((s) => s.activeTab)
  const datasetVersion = useReviewStore((s) => s.datasetVersion)
  const setActiveTab = useReviewStore((s) => s.setActiveTab)
  const toolReview = useToolReview(datasetVersion)

  // First-run: open the tool review once per browser session if the reviewer
  // has not yet completed it. Skippable — they can navigate away freely, and
  // the persistent tab dot reminds them until they mark it done (server-side,
  // so it survives across devices/browsers).
  useEffect(() => {
    if (!toolReview.data) return
    if (toolReview.data.completed_at != null) return
    const seenKey = `neurobench.tool_review_seen.${profile.code}`
    if (typeof sessionStorage !== "undefined") {
      if (sessionStorage.getItem(seenKey)) return
      sessionStorage.setItem(seenKey, "1")
    }
    setActiveTab("tools")
  }, [toolReview.data, profile.code, setActiveTab])

  return (
    <AppShell profile={profile}>
      {activeTab === "overview" && <OverviewTab profile={profile} />}
      {activeTab === "cases" && <CasesTab />}
      {activeTab === "tools" && <ToolReviewTab />}
      {activeTab === "methodology" && <MethodologyTab />}
      {activeTab === "admin" && profile.role === "admin" && <AdminTab />}
    </AppShell>
  )
}
