import { motion } from "framer-motion"

import { cn } from "@/lib/utils"
import type { ReviewTab } from "@/stores/reviewStore"

interface TabItem {
  id: ReviewTab
  label: string
  count?: number
  hidden?: boolean
  /** Show a small attention dot (e.g. an unfinished onboarding step). */
  dot?: boolean
}

export function TabBar({
  tabs,
  active,
  onChange,
  layoutId = "tab-underline",
}: {
  tabs: TabItem[]
  active: ReviewTab
  onChange: (tab: ReviewTab) => void
  /**
   * Unique framer-motion layoutId for the animated underline.
   * Pass distinct values when rendering more than one TabBar (e.g. mobile + desktop) so animations don't fight.
   */
  layoutId?: string
}) {
  return (
    <div className="relative flex items-center gap-0.5 sm:gap-1 px-1">
      {tabs
        .filter((t) => !t.hidden)
        .map((tab) => {
          const isActive = tab.id === active
          return (
            <button
              key={tab.id}
              type="button"
              onClick={() => onChange(tab.id)}
              className={cn(
                "relative px-3 sm:px-4 py-2 sm:py-2.5 text-sm font-medium rounded-md transition-colors whitespace-nowrap",
                isActive
                  ? "text-foreground"
                  : "text-muted-foreground hover:text-foreground",
              )}
            >
              <span className="relative z-10 flex items-center gap-1.5 sm:gap-2">
                {tab.label}
                {tab.dot && (
                  <span
                    aria-label="Action needed"
                    className="w-1.5 h-1.5 rounded-full bg-primary"
                  />
                )}
                {typeof tab.count === "number" && (
                  <span
                    className={cn(
                      "px-1.5 py-0.5 rounded text-[10px] font-semibold tabular-nums",
                      isActive
                        ? "bg-primary/15 text-primary"
                        : "bg-muted text-muted-foreground",
                    )}
                  >
                    {tab.count.toLocaleString()}
                  </span>
                )}
              </span>
              {isActive && (
                <motion.div
                  layoutId={layoutId}
                  className="absolute left-3 right-3 -bottom-px h-0.5 rounded-full bg-primary"
                  transition={{ type: "spring", stiffness: 380, damping: 32 }}
                />
              )}
            </button>
          )
        })}
    </div>
  )
}
