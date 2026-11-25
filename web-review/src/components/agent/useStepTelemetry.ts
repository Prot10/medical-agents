import { useCallback, useEffect, useRef } from "react"

import type { StepTelemetry } from "@/api/agentTypes"

/**
 * Light context of one step, sent with the action: time the page was visible, which tool cards
 * were opened, the catalogue filter terms, whether the raw view was opened. No keystrokes.
 * Everything resets when `step` changes.
 */
export function useStepTelemetry(step: number) {
  const mountedStep = useRef(step)
  const data = useRef({ active: 0, since: 0, tools: [] as string[], searches: [] as string[], raw: false })

  useEffect(() => {
    const d = data.current
    d.active = 0
    d.tools = []
    d.searches = []
    d.raw = false
    d.since = document.visibilityState === "visible" ? performance.now() : 0
    const onVisibility = () => {
      if (document.visibilityState === "visible") d.since = performance.now()
      else if (d.since) {
        d.active += performance.now() - d.since
        d.since = 0
      }
    }
    document.addEventListener("visibilitychange", onVisibility)
    return () => document.removeEventListener("visibilitychange", onVisibility)
  }, [step])

  const noteTool = useCallback((name: string) => {
    const tools = data.current.tools
    if (tools[tools.length - 1] !== name && tools.length < 80) tools.push(name)
  }, [])
  const noteSearch = useCallback((term: string) => {
    const searches = data.current.searches
    const clean = term.trim().slice(0, 80)
    if (clean.length >= 2 && searches[searches.length - 1] !== clean && searches.length < 20) searches.push(clean)
  }, [])
  const noteRawView = useCallback(() => {
    data.current.raw = true
  }, [])
  const collect = useCallback((): StepTelemetry => {
    const d = data.current
    const running = d.since ? performance.now() - d.since : 0
    return {
      active_seconds: Math.round((d.active + running) / 100) / 10,
      tools_opened: [...d.tools],
      searches: [...d.searches],
      raw_view_opened: d.raw,
      // The page was loaded again in the middle of the case and this step was waiting.
      resumed: step > 0 && mountedStep.current === step,
    }
  }, [step])

  return { noteTool, noteSearch, noteRawView, collect }
}
