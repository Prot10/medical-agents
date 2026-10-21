import { useEffect } from "react"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { AppShell } from "@/components/layout/AppShell"
import { ModelLoadingToast } from "@/components/model/ModelLoadingToast"
import { useAppStore } from "@/stores/appStore"

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

function DarkModeSync() {
  const darkMode = useAppStore((s) => s.darkMode)
  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode)
  }, [darkMode])
  return null
}

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <DarkModeSync />
      <AppShell />
      <ModelLoadingToast />
    </QueryClientProvider>
  )
}
