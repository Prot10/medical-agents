import { useEffect, useRef, useState, useCallback } from "react"
import { useModelLoadingStore } from "@/stores/modelLoadingStore"
import { X, Loader2, CheckCircle2, AlertCircle, Cpu } from "lucide-react"

export function ModelLoadingToast() {
  const {
    modelName, phase, message, elapsed,
    expectedSeconds, sizeGb, reset,
  } = useModelLoadingStore()
  const dismissTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  // Smooth interpolation state
  const [smoothProgress, setSmoothProgress] = useState(0)
  const [smoothElapsed, setSmoothElapsed] = useState(0)
  const rafRef = useRef<number>(0)
  const startTimeRef = useRef<number>(0)
  const lastServerElapsed = useRef(0)

  // Track when loading starts for local clock
  useEffect(() => {
    if (phase === "starting" || (phase === "loading" && startTimeRef.current === 0)) {
      startTimeRef.current = performance.now()
      lastServerElapsed.current = 0
      setSmoothProgress(0)
      setSmoothElapsed(0)
    }
    if (phase === "idle") {
      startTimeRef.current = 0
      lastServerElapsed.current = 0
    }
  }, [phase])

  // Sync server elapsed when SSE event arrives
  useEffect(() => {
    if (elapsed > 0) {
      lastServerElapsed.current = elapsed
      // Resync the local clock to server time
      startTimeRef.current = performance.now() - elapsed * 1000
    }
  }, [elapsed])

  // Smooth animation loop
  const animate = useCallback(() => {
    if (!startTimeRef.current || phase === "idle" || phase === "ready" || phase === "error") return

    const localElapsed = (performance.now() - startTimeRef.current) / 1000
    const clampedElapsed = Math.max(0, localElapsed)
    const expected = expectedSeconds || 60
    // Smooth progress: asymptotic curve that approaches 95% but never reaches it
    const t = clampedElapsed / expected
    const smoothP = Math.min(95, t * 90 / (1 + t * 0.1))

    setSmoothElapsed(Math.round(clampedElapsed))
    setSmoothProgress(Math.round(smoothP))

    rafRef.current = requestAnimationFrame(animate)
  }, [phase, expectedSeconds])

  useEffect(() => {
    const isActive = phase !== "idle" && phase !== "ready" && phase !== "error"
    if (isActive) {
      rafRef.current = requestAnimationFrame(animate)
    }
    return () => { if (rafRef.current) cancelAnimationFrame(rafRef.current) }
  }, [phase, animate])

  // Snap to 100% on ready
  useEffect(() => {
    if (phase === "ready") {
      setSmoothProgress(100)
      setSmoothElapsed(elapsed)
    }
  }, [phase, elapsed])

  // Auto-dismiss
  useEffect(() => {
    if (dismissTimer.current) clearTimeout(dismissTimer.current)
    if (phase === "ready") {
      dismissTimer.current = setTimeout(reset, 3000)
    }
    return () => { if (dismissTimer.current) clearTimeout(dismissTimer.current) }
  }, [phase, reset])

  if (phase === "idle") return null

  const isError = phase === "error"
  const isReady = phase === "ready"
  const displayProgress = isReady ? 100 : isError ? 0 : smoothProgress
  const displayElapsed = isReady ? elapsed : smoothElapsed
  const remaining = Math.max(0, (expectedSeconds || 60) - displayElapsed)

  const phaseLabel: Record<string, string> = {
    unloading: "Unloading",
    starting: "Starting",
    loading: "Loading weights",
    weights: "Loading weights",
    cuda_graphs: "CUDA graphs",
    ready: "Ready",
    error: "Error",
  }

  return (
    <>
      <style>{`
        @keyframes neuroagent-toast-enter {
          from { opacity: 0; transform: translateY(1rem) scale(0.95); }
          to { opacity: 1; transform: translateY(0) scale(1); }
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
          {/* Header */}
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
                <span style={{ fontSize: "0.625rem", color: "#71717a", background: "#27272a", padding: "1px 6px", borderRadius: "9999px" }}>
                  {phaseLabel[phase] ?? phase}
                </span>
              )}
            </div>
            <button
              onClick={reset}
              style={{ padding: "2px", border: "none", background: "transparent", color: "#71717a", cursor: "pointer", display: "flex", borderRadius: "4px" }}
            >
              <X size={14} />
            </button>
          </div>

          {/* Message */}
          <p style={{ padding: "0.25rem 0.75rem 0", margin: 0, fontSize: "0.6875rem", color: "#a1a1aa" }}>
            {message}
          </p>

          {/* Progress bar */}
          <div style={{ padding: "0.5rem 0.75rem 0" }}>
            <div style={{ height: 6, width: "100%", borderRadius: 9999, overflow: "hidden", background: "#27272a" }}>
              <div
                style={{
                  height: "100%",
                  width: `${displayProgress}%`,
                  borderRadius: 9999,
                  background: isError ? "#f87171" : isReady ? "#4ade80" : "linear-gradient(90deg, #3b82f6, #60a5fa)",
                  transition: isReady ? "width 0.3s ease-out" : "none",
                }}
              />
            </div>
          </div>

          {/* Stats */}
          <div style={{ display: "flex", justifyContent: "space-between", padding: "0.375rem 0.75rem 0.625rem", fontSize: "0.625rem", color: "#71717a" }}>
            {sizeGb > 0 && (
              <span style={{ display: "flex", alignItems: "center", gap: "3px" }}>
                <Cpu size={10} />
                {sizeGb.toFixed(1)} GB
              </span>
            )}
            {!isReady && !isError && displayElapsed > 0 && (
              <span>{displayElapsed}s{remaining > 0 ? ` / ~${expectedSeconds}s` : ""}</span>
            )}
            {isReady && elapsed > 0 && (
              <span>Loaded in {elapsed}s</span>
            )}
            {!isReady && !isError && displayProgress > 0 && (
              <span>{displayProgress}%</span>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
