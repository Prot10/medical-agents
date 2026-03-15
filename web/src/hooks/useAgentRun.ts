import { useCallback, useRef } from "react"
import { streamAgentRun } from "@/api/client"
import { useAgentStore } from "@/stores/agentStore"

export function useAgentRun() {
  const { startRun, appendEvent, setError, status } = useAgentStore()
  const abortRef = useRef<AbortController | null>(null)

  const run = useCallback(
    async (caseId: string, hospital: string, model: string) => {
      abortRef.current?.abort()
      const controller = new AbortController()
      abortRef.current = controller

      startRun()

      try {
        await streamAgentRun(
          caseId,
          hospital,
          model,
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

  return { run, stop, status }
}
