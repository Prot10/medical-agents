import { useCallback } from "react"
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
  const { startRun, setAbortController, appendEvent, setError } = useAgentStore()

  const replay = useCallback(
    async (traceId: string) => {
      useAgentStore.getState().abortController?.abort()
      const controller = new AbortController()

      startRun()
      setAbortController(controller)

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
      } finally {
        if (useAgentStore.getState().abortController === controller) {
          setAbortController(null)
        }
      }
    },
    [startRun, setAbortController, appendEvent, setError],
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
    useAgentStore.getState().cancel()
  }, [])

  return { replay, replayInstant, stop }
}
