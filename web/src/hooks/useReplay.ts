import { useCallback, useRef } from "react"
import { useQuery } from "@tanstack/react-query"
import { api, replayTrace } from "@/api/client"
import { useAgentStore } from "@/stores/agentStore"

export function useTraces() {
  return useQuery({
    queryKey: ["traces"],
    queryFn: api.getTraces,
    staleTime: 5_000,
  })
}

export function useReplay() {
  const { startRun, appendEvent, setError } = useAgentStore()
  const abortRef = useRef<AbortController | null>(null)

  const replay = useCallback(
    async (traceId: string) => {
      abortRef.current?.abort()
      const controller = new AbortController()
      abortRef.current = controller

      startRun()

      try {
        await replayTrace(
          traceId,
          appendEvent,
          (err) => setError(err.message),
          controller.signal,
        )
      } catch (err) {
        if ((err as Error).name !== "AbortError") {
          setError((err as Error).message)
        }
      }
    },
    [startRun, appendEvent, setError],
  )

  const stop = useCallback(() => {
    abortRef.current?.abort()
    abortRef.current = null
  }, [])

  return { replay, stop }
}
