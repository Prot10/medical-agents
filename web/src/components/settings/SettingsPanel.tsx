import { useState, useEffect, useRef, useCallback } from "react"
import { Github, Check, Loader2, X, ExternalLink, Copy, LogOut } from "lucide-react"
import { useQueryClient } from "@tanstack/react-query"
import { api } from "@/api/client"
import { useCopilotStatus } from "@/hooks/useCases"

type FlowState =
  | { step: "idle" }
  | { step: "loading" }
  | { step: "pairing"; userCode: string; verificationUri: string; deviceCode: string; expiresAt: number; interval: number }
  | { step: "polling"; userCode: string; deviceCode: string }
  | { step: "complete" }
  | { step: "error"; message: string }

export function SettingsPanel() {
  const [flow, setFlow] = useState<FlowState>({ step: "idle" })
  const [copied, setCopied] = useState(false)
  const pollRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const queryClient = useQueryClient()
  const { data: copilotStatus } = useCopilotStatus()

  const isConnected = copilotStatus?.authenticated && copilotStatus?.copilot_access

  // Cleanup polling on unmount
  useEffect(() => {
    return () => {
      if (pollRef.current) clearTimeout(pollRef.current)
    }
  }, [])

  const startDeviceFlow = useCallback(async () => {
    setFlow({ step: "loading" })
    try {
      const data = await api.copilotStartDeviceFlow()
      if ("error" in data && data.error) {
        setFlow({ step: "error", message: data.error as string })
        return
      }
      setFlow({
        step: "pairing",
        userCode: data.user_code,
        verificationUri: data.verification_uri,
        deviceCode: data.device_code,
        expiresAt: Date.now() + data.expires_in * 1000,
        interval: data.interval,
      })
    } catch (err) {
      setFlow({ step: "error", message: (err as Error).message })
    }
  }, [])

  const startPolling = useCallback((deviceCode: string, interval: number) => {
    setFlow((prev) => {
      if (prev.step === "pairing") {
        return { step: "polling", userCode: prev.userCode, deviceCode }
      }
      return prev
    })

    const poll = async () => {
      try {
        const result = await api.copilotPollToken(deviceCode)
        if (result.status === "complete") {
          setFlow({ step: "complete" })
          // Refresh model list and copilot status
          queryClient.invalidateQueries({ queryKey: ["models"] })
          queryClient.invalidateQueries({ queryKey: ["copilot-status"] })
          return
        }
        if (result.status === "expired") {
          setFlow({ step: "error", message: "Code expired. Please try again." })
          return
        }
        if (result.status === "denied") {
          setFlow({ step: "error", message: "Access denied on GitHub." })
          return
        }
        if (result.status === "error") {
          setFlow({ step: "error", message: result.error || "Unknown error" })
          return
        }
        // Still pending — poll again
        const nextInterval = result.interval || interval
        pollRef.current = setTimeout(poll, nextInterval * 1000)
      } catch {
        pollRef.current = setTimeout(poll, interval * 1000)
      }
    }

    pollRef.current = setTimeout(poll, interval * 1000)
  }, [queryClient])

  const handleCopyCode = (code: string) => {
    navigator.clipboard.writeText(code)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleLogout = async () => {
    if (pollRef.current) clearTimeout(pollRef.current)
    await api.copilotLogout()
    setFlow({ step: "idle" })
    queryClient.invalidateQueries({ queryKey: ["models"] })
    queryClient.invalidateQueries({ queryKey: ["copilot-status"] })
  }

  const handleCancel = () => {
    if (pollRef.current) clearTimeout(pollRef.current)
    setFlow({ step: "idle" })
  }

  return (
    <div className="p-3 space-y-4">
      <div className="text-sm uppercase tracking-wider font-semibold text-muted-foreground">
        Settings
      </div>

      {/* GitHub Copilot section */}
      <div className="space-y-3">
        <div className="flex items-center gap-2">
          <div className="h-7 w-7 rounded-lg bg-[#24292e] dark:bg-white/10 flex items-center justify-center">
            <Github className="h-4 w-4 text-white" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-base font-semibold">GitHub Copilot</div>
            <div className="text-xs text-muted-foreground">Claude, GPT, Gemini & more</div>
          </div>
          {isConnected && (
            <span className="flex items-center gap-1 text-xs text-emerald-500 font-medium">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500" />
              Connected
            </span>
          )}
        </div>

        {/* Connected state */}
        {isConnected && flow.step !== "pairing" && flow.step !== "polling" && (
          <div className="space-y-2">
            <div className="flex items-center gap-2 p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-sm text-emerald-600 dark:text-emerald-400">
              <Check className="h-3.5 w-3.5 shrink-0" />
              <span>Copilot models available in the Model picker</span>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center gap-1.5 text-sm text-muted-foreground hover:text-red-500 transition-colors"
            >
              <LogOut className="h-3 w-3" />
              Disconnect
            </button>
          </div>
        )}

        {/* Idle / Start flow */}
        {!isConnected && flow.step === "idle" && (
          <button
            onClick={startDeviceFlow}
            className="w-full flex items-center justify-center gap-2 text-base font-medium py-2 rounded-lg bg-[#24292e] text-white hover:bg-[#333] transition-colors"
          >
            <Github className="h-4 w-4" />
            Sign in with GitHub
          </button>
        )}

        {/* Loading */}
        {flow.step === "loading" && (
          <div className="flex items-center justify-center gap-2 py-4 text-base text-muted-foreground">
            <Loader2 className="h-4 w-4 animate-spin" />
            Starting authentication...
          </div>
        )}

        {/* Pairing screen — show the code */}
        {flow.step === "pairing" && (
          <div className="space-y-3">
            <div className="text-base text-muted-foreground text-center">
              Enter this code on GitHub:
            </div>

            {/* Big code display */}
            <button
              onClick={() => handleCopyCode(flow.userCode)}
              className="w-full flex items-center justify-center gap-3 py-3 rounded-xl border-2 border-dashed border-primary/30 bg-primary/5 hover:bg-primary/10 transition-colors group"
            >
              <span className="text-2xl font-mono font-bold tracking-[0.3em] text-primary">
                {flow.userCode}
              </span>
              {copied ? (
                <Check className="h-4 w-4 text-emerald-500" />
              ) : (
                <Copy className="h-4 w-4 text-muted-foreground group-hover:text-primary transition-colors" />
              )}
            </button>

            <a
              href={flow.verificationUri}
              target="_blank"
              rel="noopener noreferrer"
              onClick={() => startPolling(flow.deviceCode, flow.interval)}
              className="w-full flex items-center justify-center gap-2 text-base font-medium py-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 transition-colors"
            >
              <ExternalLink className="h-3.5 w-3.5" />
              Open GitHub
            </a>

            <button
              onClick={handleCancel}
              className="w-full text-sm text-muted-foreground hover:text-foreground transition-colors py-1"
            >
              Cancel
            </button>
          </div>
        )}

        {/* Polling — waiting for user to authorize */}
        {flow.step === "polling" && (
          <div className="space-y-3">
            <div className="flex flex-col items-center gap-2 py-3">
              <Loader2 className="h-5 w-5 animate-spin text-primary" />
              <div className="text-base text-muted-foreground text-center">
                Waiting for authorization...
              </div>
              <div className="text-sm text-muted-foreground/60 text-center">
                Enter code <span className="font-mono font-bold text-primary">{flow.userCode}</span> on GitHub
              </div>
            </div>
            <button
              onClick={handleCancel}
              className="w-full text-sm text-muted-foreground hover:text-foreground transition-colors py-1"
            >
              Cancel
            </button>
          </div>
        )}

        {/* Complete */}
        {flow.step === "complete" && !isConnected && (
          <div className="flex items-center gap-2 p-2.5 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-sm text-emerald-600 dark:text-emerald-400">
            <Check className="h-3.5 w-3.5 shrink-0" />
            <span>Connected! Copilot models now available.</span>
          </div>
        )}

        {/* Error */}
        {flow.step === "error" && (
          <div className="space-y-2">
            <div className="flex items-center gap-2 p-2.5 rounded-lg bg-red-500/10 border border-red-500/20 text-sm text-red-500">
              <X className="h-3.5 w-3.5 shrink-0" />
              <span>{flow.message}</span>
            </div>
            <button
              onClick={startDeviceFlow}
              className="text-sm text-primary hover:underline"
            >
              Try again
            </button>
          </div>
        )}

        {/* Info */}
        <p className="text-xs text-muted-foreground/50 leading-relaxed">
          Requires an active GitHub Copilot subscription. Uses the device flow for secure authentication.
        </p>
      </div>
    </div>
  )
}
