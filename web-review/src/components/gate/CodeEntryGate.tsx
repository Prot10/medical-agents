import { motion } from "framer-motion"
import { ArrowRight, BrainCircuit, Loader2 } from "lucide-react"
import { useState } from "react"

import { ReviewApiError } from "@/api/client"
import { validateAndLoadProfile } from "@/hooks/useReview"
import { useReviewStore } from "@/stores/reviewStore"
import { Button } from "@/components/ui/Button"

export function CodeEntryGate() {
  const setProfile = useReviewStore((s) => s.setProfile)
  const sessionMessage = useReviewStore((s) => s.sessionMessage)
  const [code, setCode] = useState("")
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [welcomeName, setWelcomeName] = useState<string | null>(null)

  async function handleSubmit(event: React.FormEvent) {
    event.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      const profile = await validateAndLoadProfile(code.trim())
      setWelcomeName(profile.name)
      await new Promise((r) => setTimeout(r, 700))
      setProfile(profile)
    } catch (exc) {
      const message =
        exc instanceof ReviewApiError
          ? exc.status === 401
            ? "That code doesn't match an active reviewer."
            : exc.message
          : "Something went wrong. Try again."
      setError(message)
      setSubmitting(false)
    }
  }

  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden bg-background">
      <BackgroundOrbs />

      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, ease: "easeOut" }}
        className="relative z-10 w-full max-w-md mx-auto px-6"
      >
        <div className="bg-card border border-border rounded-2xl shadow-xl shadow-primary/5 p-8">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
              <BrainCircuit className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xs uppercase tracking-wider text-muted-foreground">
                NeuroBench
              </div>
              <h1 className="text-lg font-semibold tracking-tight">
                Expert Review
              </h1>
            </div>
          </div>

          {welcomeName ? (
            <motion.div
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
              className="py-6"
            >
              <p className="text-2xl font-semibold tracking-tight">
                Welcome, {welcomeName}.
              </p>
              <p className="text-muted-foreground mt-2 text-sm">
                Loading your review workspace…
              </p>
            </motion.div>
          ) : (
            <>
              <p className="text-sm text-muted-foreground mb-6 leading-relaxed">
                Enter the reviewer code you were provided. Your annotations are
                private to you and saved against this code.
              </p>

              {sessionMessage && !error && (
                <div className="mb-4 text-sm rounded-md border border-amber-500/40 bg-amber-500/10 text-amber-700 dark:text-amber-300 px-3 py-2">
                  {sessionMessage}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-3">
                <label className="block">
                  <span className="block text-xs font-medium text-muted-foreground mb-1.5">
                    Reviewer code
                  </span>
                  <input
                    type="text"
                    value={code}
                    onChange={(e) => setCode(e.target.value.toUpperCase())}
                    autoFocus
                    spellCheck={false}
                    autoComplete="off"
                    placeholder="NEURO-XXXX"
                    className="w-full bg-background border border-input rounded-md h-11 px-3.5 text-base font-mono tracking-wider tabular-nums focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring transition"
                  />
                </label>

                {error && (
                  <div className="text-sm text-rose-600 dark:text-rose-400">
                    {error}
                  </div>
                )}

                <Button
                  type="submit"
                  size="lg"
                  className="w-full"
                  disabled={submitting || code.trim().length < 3}
                >
                  {submitting ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <>
                      Continue
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </Button>
              </form>
            </>
          )}
        </div>

        <p className="text-center text-xs text-muted-foreground mt-6">
          Your code identifies your review only. Other reviewers cannot see it.
        </p>
      </motion.div>
    </div>
  )
}

function BackgroundOrbs() {
  return (
    <div aria-hidden className="pointer-events-none absolute inset-0">
      <div className="absolute top-[-10%] left-[-10%] w-[40rem] h-[40rem] rounded-full bg-primary/10 blur-3xl" />
      <div className="absolute bottom-[-15%] right-[-10%] w-[36rem] h-[36rem] rounded-full bg-emerald-500/10 blur-3xl" />
      <svg
        className="absolute inset-0 w-full h-full opacity-[0.04] dark:opacity-[0.06]"
        viewBox="0 0 600 600"
        preserveAspectRatio="xMidYMid slice"
      >
        <defs>
          <radialGradient id="dot" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stopColor="currentColor" stopOpacity="1" />
            <stop offset="100%" stopColor="currentColor" stopOpacity="0" />
          </radialGradient>
        </defs>
        {Array.from({ length: 60 }).map((_, i) => {
          const x = (i * 73) % 600
          const y = (i * 109 + 31) % 600
          return (
            <circle
              key={i}
              cx={x}
              cy={y}
              r={1.2 + (i % 3)}
              fill="currentColor"
            />
          )
        })}
      </svg>
    </div>
  )
}
