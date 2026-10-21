import { useCallback } from "react"
import { useQueryClient } from "@tanstack/react-query"
import { streamRun } from "@/api/client"
import { useAgentStore } from "@/stores/agentStore"

export function useAgentRun() {
  const { startRun, setAbortController, appendFrame, setError, status } = useAgentStore()
  const queryClient = useQueryClient()

  const run = useCallback(
    async (caseId: string, profileId: string) => {
      // Abort any previous in-flight run (its AbortError is swallowed below)
      useAgentStore.getState().abortController?.abort()
      const controller = new AbortController()

      startRun()
      setAbortController(controller)

      try {
        await streamRun(caseId, profileId, appendFrame, controller.signal)
        // A stream that closes without a terminal frame was cut off mid-run
        if (useAgentStore.getState().status === "running") {
          setError("The run stream closed before the episode finished")
        }
        queryClient.invalidateQueries({ queryKey: ["episodes"] })
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
    [startRun, setAbortController, appendFrame, setError, queryClient],
  )

  const stop = useCallback(() => {
    // Aborting the request closes the stream; the server stops the run at its next event
    useAgentStore.getState().cancel()
  }, [])

  return { run, stop, status }
}
