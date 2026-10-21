import { Check, Cpu } from "lucide-react"
import { useModels, useProfiles } from "@/hooks/useCases"
import { useAppStore } from "@/stores/appStore"
import { QueryError } from "@/components/ui/QueryError"
import { LOOP_LABELS, profileLoop, profileModelKey } from "@/lib/policy"
import { cn } from "@/lib/utils"

const STATUS_DOT: Record<string, string> = {
  ready: "bg-emerald-500",
  loading: "bg-amber-500",
  offline: "bg-zinc-500",
}

/** The checked experiment profiles: the only way a run chooses its model and loop. */
export function ProfilesPanel() {
  const { data: profiles, isLoading, isError, error, refetch } = useProfiles()
  const { data: models } = useModels()
  const { selectedProfileId, setProfile } = useAppStore()

  if (isLoading) return <div className="p-4 text-base text-muted-foreground">Loading profiles...</div>
  if (isError) return <QueryError message="Could not load profiles." error={error} onRetry={() => refetch()} />

  return (
    <div className="p-3 space-y-2">
      <div className="text-sm uppercase tracking-wider font-semibold text-muted-foreground px-1">
        Experiment profiles
      </div>
      <p className="text-xs text-muted-foreground/70 px-1 leading-relaxed">
        A run uses one checked profile: a registered model, a loop and fixed budgets. Arbitrary models and
        endpoints are not accepted.
      </p>
      {profiles?.map((profile) => {
        const modelKey = profileModelKey(profile)
        const model = models?.find((m) => m.key === modelKey)
        const loop = profileLoop(profile)
        const selected = profile.profile_id === selectedProfileId
        return (
          <button
            key={profile.profile_id}
            onClick={() => setProfile(profile.profile_id)}
            className={cn(
              "w-full text-left rounded-lg border px-3 py-2 transition-all",
              selected ? "border-primary/40 bg-primary/5" : "border-sidebar-border hover:bg-sidebar-accent",
            )}
          >
            <div className="flex items-center gap-2">
              <span className="font-mono text-sm font-medium truncate flex-1">{profile.profile_id}</span>
              {selected && <Check className="h-3.5 w-3.5 text-primary shrink-0" />}
            </div>
            <div className="flex items-center gap-1.5 mt-1 text-xs text-muted-foreground">
              <span className={cn("h-1.5 w-1.5 rounded-full shrink-0", STATUS_DOT[model?.status ?? "offline"])} />
              <Cpu className="h-3 w-3 shrink-0" />
              <span className="truncate">{model?.name ?? modelKey}</span>
            </div>
            <div className="flex flex-wrap gap-1.5 mt-1.5 text-xs">
              <span className="px-1.5 py-0.5 rounded bg-muted text-muted-foreground">{LOOP_LABELS[loop ?? ""] ?? loop}</span>
              <span className="px-1.5 py-0.5 rounded bg-muted text-muted-foreground">{profile.max_turns} turns</span>
              {profile.max_cost_usd != null && (
                <span className="px-1.5 py-0.5 rounded bg-muted text-muted-foreground">
                  ≤ ${profile.max_cost_usd.toLocaleString()}
                </span>
              )}
              <span className="px-1.5 py-0.5 rounded bg-muted text-muted-foreground">
                {profile.max_invalid_actions} retries
              </span>
            </div>
          </button>
        )
      })}
    </div>
  )
}
