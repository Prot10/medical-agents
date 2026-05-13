import { motion } from "framer-motion"

import { cn } from "@/lib/utils"
import type { ReviewTab } from "@/stores/reviewStore"

interface TabItem {
  id: ReviewTab
  label: string
  count?: number
  hidden?: boolean
}

export function TabBar({
  tabs,
  active,
  onChange,
}: {
  tabs: TabItem[]
  active: ReviewTab
  onChange: (tab: ReviewTab) => void
}) {
  return (
    <div className="relative flex items-center gap-1 px-1">
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
                "relative px-4 py-2.5 text-sm font-medium rounded-md transition-colors",
                isActive
                  ? "text-foreground"
                  : "text-muted-foreground hover:text-foreground",
              )}
            >
              <span className="relative z-10 flex items-center gap-2">
                {tab.label}
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
                  layoutId="tab-underline"
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
