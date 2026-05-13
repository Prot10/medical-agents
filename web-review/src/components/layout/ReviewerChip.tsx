import * as Popover from "@radix-ui/react-popover"
import { LogOut, Shield, UserRound } from "lucide-react"

import { cn } from "@/lib/utils"
import type { ReviewerProfile } from "@/api/types"
import { useReviewStore } from "@/stores/reviewStore"

function initials(name: string): string {
  return name
    .split(" ")
    .filter(Boolean)
    .map((part) => part[0]?.toUpperCase() ?? "")
    .slice(0, 2)
    .join("")
}

function colorFromName(name: string): string {
  let hash = 0
  for (let i = 0; i < name.length; i += 1) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash)
  }
  const hue = Math.abs(hash) % 360
  return `hsl(${hue} 60% 45%)`
}

export function ReviewerChip({ profile }: { profile: ReviewerProfile }) {
  const signOut = useReviewStore((s) => s.signOut)
  const accent = colorFromName(profile.name)

  return (
    <Popover.Root>
      <Popover.Trigger asChild>
        <button
          type="button"
          className="group flex items-center gap-2 pl-1 pr-3 py-1 rounded-full hover:bg-secondary/60 transition-colors"
        >
          <span
            className="w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold text-white shadow-sm"
            style={{ background: accent }}
          >
            {initials(profile.name) || <UserRound className="w-3.5 h-3.5" />}
          </span>
          <span className="text-sm font-medium text-foreground/90 hidden md:inline">
            {profile.name}
          </span>
        </button>
      </Popover.Trigger>
      <Popover.Portal>
        <Popover.Content
          align="end"
          sideOffset={6}
          className="z-50 w-64 bg-popover border border-border rounded-xl shadow-xl p-3"
        >
          <div className="flex items-center gap-3 px-1 py-2">
            <span
              className="w-9 h-9 rounded-full flex items-center justify-center text-sm font-semibold text-white"
              style={{ background: accent }}
            >
              {initials(profile.name)}
            </span>
            <div>
              <div className="font-medium text-sm leading-tight">
                {profile.name}
              </div>
              <div className="font-mono text-[11px] text-muted-foreground tracking-wider">
                {profile.code}
              </div>
            </div>
          </div>
          <div className="my-2 h-px bg-border" />
          <div
            className={cn(
              "flex items-center gap-2 px-2 py-1.5 text-xs rounded-md",
              profile.role === "admin"
                ? "text-emerald-600 dark:text-emerald-400"
                : "text-muted-foreground",
            )}
          >
            <Shield className="w-3.5 h-3.5" />
            {profile.role === "admin" ? "Researcher (admin)" : "Reviewer"}
          </div>
          <button
            type="button"
            onClick={signOut}
            className="mt-1 w-full flex items-center gap-2 px-2 py-2 text-sm rounded-md text-foreground hover:bg-secondary/70 transition-colors"
          >
            <LogOut className="w-4 h-4" />
            Switch reviewer
          </button>
        </Popover.Content>
      </Popover.Portal>
    </Popover.Root>
  )
}
