import { useCallback, useRef } from "react"
import { useQuery } from "@tanstack/react-query"
import { api, replayTrace } from "@/api/client"
import { useAgentStore } from "@/stores/agentStore"
import { useAppStore } from "@/stores/appStore"

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
          (event) => {
            // Set selectedCaseId from the run_started event
            if (event.type === "run_started" && event.case_id) {
              useAppStore.getState().selectCase(event.case_id)
            }
            appendEvent(event)
          },
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

  const replayInstant = useCallback(
    async (traceId: string) => {
      // Fetch the trace JSON directly and load all events at once
      try {
        const traceData = await api.getTrace(traceId)
        const events = traceData.events ?? []
        const caseId = traceData.case_id

        if (caseId) {
          useAppStore.getState().selectCase(caseId)
        }

        startRun()

        // Append all events immediately (no streaming delays)
        for (const event of events) {
          appendEvent(event)
        }
      } catch (err) {
        setError((err as Error).message)
      }
    },
    [startRun, appendEvent, setError],
  )

  const stop = useCallback(() => {
    abortRef.current?.abort()
    abortRef.current = null
  }, [])

  return { replay, replayInstant, stop }
}
