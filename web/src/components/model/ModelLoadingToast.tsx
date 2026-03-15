import { useEffect, useRef } from "react"
import { useModelLoadingStore } from "@/stores/modelLoadingStore"
import { X, Loader2, CheckCircle2, AlertCircle, Cpu } from "lucide-react"

export function ModelLoadingToast() {
  const {
    modelName,
    phase,
    message,
    progress,
    elapsed,
    expectedSeconds,
    sizeGb,
    reset,
  } = useModelLoadingStore()
  const dismissTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  useEffect(() => {
    if (dismissTimer.current) clearTimeout(dismissTimer.current)
    if (phase === "ready") {
      dismissTimer.current = setTimeout(reset, 3000)
    }
    return () => {
      if (dismissTimer.current) clearTimeout(dismissTimer.current)
    }
  }, [phase, reset])

  if (phase === "idle") return null

  const isError = phase === "error"
  const isReady = phase === "ready"
  const clampedProgress = Math.min(100, Math.max(0, progress))

  const phaseLabel: Record<string, string> = {
    unloading: "Unloading",
    starting: "Starting",
    loading: "Loading weights",
    weights: "Loading weights",
    cuda_graphs: "CUDA graphs",
    ready: "Ready",
    error: "Error",
  }

  const remaining = Math.max(0, expectedSeconds - elapsed)

  return (
    <>
      <style>{`
        @keyframes neuroagent-toast-enter {
          from { opacity: 0; transform: translateY(1rem) scale(0.95); }
          to { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes neuroagent-pulse-bar {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }
      `}</style>
      <div
        style={{
          position: "fixed",
          bottom: "1rem",
          right: "1rem",
          zIndex: 99999,
          width: "22rem",
          animation: "neuroagent-toast-enter 0.2s ease-out",
          fontFamily: "system-ui, -apple-system, sans-serif",
        }}
      >
        <div
          style={{
            background: "#18181b",
            color: "#fafafa",
            borderRadius: "0.75rem",
            border: `1px solid ${isError ? "rgba(248,113,113,0.4)" : isReady ? "rgba(74,222,128,0.4)" : "rgba(63,63,70,0.6)"}`,
            boxShadow: "0 25px 50px -12px rgba(0,0,0,0.6)",
            overflow: "hidden",
          }}
        >
          {/* Header row */}
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "0.75rem 0.75rem 0" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "0.5rem" }}>
              {isReady ? (
                <CheckCircle2 size={16} color="#4ade80" />
              ) : isError ? (
                <AlertCircle size={16} color="#f87171" />
              ) : (
                <Loader2 size={16} color="#60a5fa" style={{ animation: "spin 1s linear infinite" }} />
              )}
              <span style={{ fontSize: "0.8125rem", fontWeight: 600 }}>
                {modelName ?? "Model"}
              </span>
              {!isReady && !isError && (
                <span
                  style={{
                    fontSize: "0.625rem",
                    color: "#71717a",
                    background: "#27272a",
                    padding: "1px 6px",
                    borderRadius: "9999px",
                  }}
                >
                  {phaseLabel[phase] ?? phase}
                </span>
              )}
            </div>
            <button
              onClick={reset}
              style={{
                padding: "2px",
                border: "none",
                background: "transparent",
                color: "#71717a",
                cursor: "pointer",
                display: "flex",
                borderRadius: "4px",
              }}
            >
              <X size={14} />
            </button>
          </div>

          {/* Status message */}
          <p style={{ padding: "0.25rem 0.75rem 0", margin: 0, fontSize: "0.6875rem", color: "#a1a1aa" }}>
            {message}
          </p>

          {/* Progress bar */}
          <div style={{ padding: "0.5rem 0.75rem 0" }}>
            <div
              style={{
                height: 6,
                width: "100%",
                borderRadius: 9999,
                overflow: "hidden",
                background: "#27272a",
              }}
            >
              <div
                style={{
                  height: "100%",
                  width: `${clampedProgress}%`,
                  borderRadius: 9999,
                  background: isError
                    ? "#f87171"
                    : isReady
                      ? "#4ade80"
                      : "linear-gradient(90deg, #3b82f6, #60a5fa)",
                  transition: "width 0.5s ease-out",
                  ...((!isReady && !isError)
                    ? { animation: "neuroagent-pulse-bar 2s ease-in-out infinite" }
                    : {}),
                }}
              />
            </div>
          </div>

          {/* Stats row */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              padding: "0.375rem 0.75rem 0.625rem",
              fontSize: "0.625rem",
              color: "#71717a",
            }}
          >
            {sizeGb > 0 && (
              <span style={{ display: "flex", alignItems: "center", gap: "3px" }}>
                <Cpu size={10} />
                {sizeGb.toFixed(1)} GB
              </span>
            )}
            {!isReady && !isError && elapsed > 0 && (
              <span>{elapsed}s{remaining > 0 ? ` / ~${expectedSeconds}s` : ""}</span>
            )}
            {isReady && elapsed > 0 && (
              <span>Loaded in {elapsed}s</span>
            )}
            {!isReady && !isError && clampedProgress > 0 && (
              <span>{clampedProgress}%</span>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
