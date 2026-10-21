import { useCallback } from "react"
import { useQuery } from "@tanstack/react-query"
import { api } from "@/api/client"
import { useAgentStore } from "@/stores/agentStore"
import { useAppStore } from "@/stores/appStore"
import type { ClinicalEpisode, EpisodeEvent } from "@/api/types"

/** Delay between replayed events, so a saved episode unfolds like a live run. */
const REPLAY_STEP_MS = 450

export function useEpisodes() {
  return useQuery({
    queryKey: ["episodes"],
    queryFn: api.getEpisodes,
    staleTime: 5_000,
  })
}

function caseIdOf(episode: ClinicalEpisode): string | undefined {
  const started = episode.events.find((e) => e.type === "run.started")
  return started?.type === "run.started" ? started.case_id : undefined
}

export function useReplay() {
  const { startRun, setAbortController, appendFrame, loadEpisode, setReward, setError } = useAgentStore()

  const fetchEpisode = useCallback(async (episodeId: string) => {
    const [episode, reward] = await Promise.all([
      api.getEpisode(episodeId),
      api.getEpisodeReward(episodeId).catch(() => null),
    ])
    const caseId = caseIdOf(episode)
    if (caseId) useAppStore.getState().selectCase(caseId)
    return { events: episode.events, reward }
  }, [])

  const replay = useCallback(
    async (episodeId: string) => {
      useAgentStore.getState().abortController?.abort()
      const controller = new AbortController()
      try {
        const { events, reward } = await fetchEpisode(episodeId)
        startRun()
        setAbortController(controller)
        for (const event of events as EpisodeEvent[]) {
          await new Promise((resolve) => setTimeout(resolve, REPLAY_STEP_MS))
          if (controller.signal.aborted) return
          appendFrame(event)
        }
        loadEpisode(events, episodeId)
        setReward(reward)
      } catch (err) {
        setError((err as Error).message)
      } finally {
        if (useAgentStore.getState().abortController === controller) {
          setAbortController(null)
        }
      }
    },
    [fetchEpisode, startRun, setAbortController, appendFrame, loadEpisode, setReward, setError],
  )

  const replayInstant = useCallback(
    async (episodeId: string) => {
      useAgentStore.getState().abortController?.abort()
      try {
        const { events, reward } = await fetchEpisode(episodeId)
        loadEpisode(events, episodeId)
        setReward(reward)
      } catch (err) {
        setError((err as Error).message)
      }
    },
    [fetchEpisode, loadEpisode, setReward, setError],
  )

  const stop = useCallback(() => {
    useAgentStore.getState().cancel()
  }, [])

  return { replay, replayInstant, stop }
}
