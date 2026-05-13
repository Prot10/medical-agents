import { useEffect } from "react"

import { useReviewStore } from "@/stores/reviewStore"

export function DarkModeSync() {
  const darkMode = useReviewStore((s) => s.darkMode)
  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode)
  }, [darkMode])
  return null
}
