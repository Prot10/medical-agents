import { useCallback } from "react"
import { streamAgentRun } from "@/api/client"
import { useAgentStore } from "@/stores/agentStore"

export function useAgentRun() {
  const { startRun, setAbortController, appendEvent, setError, status } = useAgentStore()

  const run = useCallback(
    async (
      caseId: string,
      hospital: string,
      model: string,
      options?: { base_url?: string; api_key?: string },
    ) => {
      // Abort any previous in-flight run (its AbortError is swallowed below)
      useAgentStore.getState().abortController?.abort()
      const controller = new AbortController()

      startRun()
      setAbortController(controller)

      try {
        await streamAgentRun(
          caseId,
          hospital,
          model,
          appendEvent,
          (err) => setError(err.message),
          controller.signal,
          options,
        )
      } catch (err) {
        if ((err as Error).name !== "AbortError") {
          setError((err as Error).message)
        }
      } finally {
        // Clear only if this run's controller is still the active one
        if (useAgentStore.getState().abortController === controller) {
          setAbortController(null)
        }
      }
    },
    [startRun, setAbortController, appendEvent, setError],
  )

  const stop = useCallback(() => {
    // Aborts the in-flight stream and moves the run to a terminal "cancelled" state
    useAgentStore.getState().cancel()
  }, [])

  return { run, stop, status }
}
