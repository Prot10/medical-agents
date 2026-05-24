import { motion } from "framer-motion"
import {
  Activity,
  ArrowRight,
  BookOpen,
  Library,
  Loader2,
  ShieldCheck,
  Sparkles,
} from "lucide-react"

import { useMethodology } from "@/hooks/useReview"
import { conditionLabel, conditionShort } from "@/lib/conditions"
import { useReviewStore } from "@/stores/reviewStore"

const STAGE_ICONS: Record<string, React.ComponentType<{ className?: string }>> =
  {
    Library,
    Sparkles,
    Activity,
    ShieldCheck,
    BookOpen,
  }

export function MethodologyTab() {
  const version = useReviewStore((s) => s.datasetVersion)
  const { data, isLoading, error } = useMethodology(version)

  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-32 text-muted-foreground">
        <Loader2 className="w-5 h-5 animate-spin" />
      </div>
    )
  }
  if (error || !data) {
    return (
      <div className="text-center py-20 text-rose-500">
        Could not load methodology.
      </div>
    )
  }

  const { prose, stats, by_condition } = data
  // Rough estimate of annotatable leaves per case: 1 CC + 1 HPI + 8 exam +
  // 6 vitals + ~6 tool outputs + ~6 followups + ~25 ground-truth items ≈ 50.
  const totalAnnotationFields = stats.total_cases * 50

  return (
    <div className="px-4 sm:px-6 py-6 sm:py-10 max-w-6xl mx-auto w-full space-y-8 sm:space-y-12">
      <motion.section
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="text-center space-y-3"
      >
        <p className="text-xs uppercase tracking-widest text-primary font-semibold">
          {prose.title}
        </p>
        <h1 className="prose-serif text-5xl font-semibold tracking-tight leading-tight">
          {prose.tagline}
        </h1>
        <p className="text-base text-muted-foreground max-w-2xl mx-auto leading-relaxed">
          {prose.overview}
        </p>
      </motion.section>

      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="grid grid-cols-2 md:grid-cols-4 gap-3"
      >
        <BigNumber
          label="Cases"
          value={stats.total_cases.toLocaleString()}
        />
        <BigNumber label="Conditions" value={stats.conditions.toString()} />
        <BigNumber
          label="Avg pathway depth"
          value={stats.avg_pathway_depth.toFixed(1)}
          suffix=" steps"
        />
        <BigNumber
          label="Annotatable fields"
          value={(totalAnnotationFields / 1000).toFixed(1) + "k"}
          suffix=" approx"
        />
      </motion.section>

      <motion.section
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true, margin: "0px 0px -100px 0px" }}
        variants={{ hidden: {}, visible: { transition: { staggerChildren: 0.1 } } }}
      >
        <h2 className="text-xs uppercase tracking-wider text-muted-foreground font-semibold mb-4">
          Generation pipeline
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3 items-stretch">
          {prose.pipeline.map((stage, i) => {
            const Icon = STAGE_ICONS[stage.icon] ?? Library
            return (
              <motion.div
                key={stage.label}
                variants={{
                  hidden: { opacity: 0, y: 12 },
                  visible: { opacity: 1, y: 0, transition: { duration: 0.35 } },
                }}
                className="relative bg-card border border-border rounded-2xl p-5 flex flex-col gap-2 min-h-[180px]"
              >
                <div className="flex items-center justify-between">
                  <div className="w-10 h-10 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                    <Icon className="w-5 h-5" />
                  </div>
                  <span className="text-[10px] uppercase tracking-widest text-muted-foreground">
                    Step {i + 1}
                  </span>
                </div>
                <h3 className="text-base font-semibold tracking-tight">
                  {stage.label}
                </h3>
                <p className="text-xs text-muted-foreground leading-relaxed">
                  {stage.description}
                </p>
                {i < prose.pipeline.length - 1 && (
                  <ArrowRight className="hidden md:block absolute -right-3 top-1/2 -translate-y-1/2 w-5 h-5 text-border" />
                )}
              </motion.div>
            )
          })}
        </div>
      </motion.section>

      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true, margin: "0px 0px -100px 0px" }}
        transition={{ duration: 0.4 }}
      >
        <h2 className="text-xs uppercase tracking-wider text-muted-foreground font-semibold mb-4">
          Conditions covered
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2">
          {by_condition.map((c) => (
            <ConditionMiniCard
              key={c.condition}
              condition={c.condition}
              count={c.count}
              byDifficulty={c.by_difficulty}
            />
          ))}
        </div>
      </motion.section>

      <motion.section
        initial={{ opacity: 0 }}
        whileInView={{ opacity: 1 }}
        viewport={{ once: true, margin: "0px 0px -100px 0px" }}
        transition={{ duration: 0.4 }}
        className="grid grid-cols-1 md:grid-cols-2 gap-4"
      >
        <div className="bg-card border border-border rounded-2xl p-5">
          <h3 className="text-xs uppercase tracking-wider text-muted-foreground font-semibold mb-3">
            Severity distribution
          </h3>
          <DifficultyChart byDifficulty={stats.by_difficulty} total={stats.total_cases} />
        </div>
        <div className="bg-card border border-border rounded-2xl p-5">
          <h3 className="text-xs uppercase tracking-wider text-muted-foreground font-semibold mb-3">
            Encounter type
          </h3>
          <DifficultyChart byDifficulty={stats.by_encounter} total={stats.total_cases} />
        </div>
      </motion.section>

    </div>
  )
}

function BigNumber({
  label,
  value,
  suffix,
}: {
  label: string
  value: string
  suffix?: string
}) {
  return (
    <div className="text-center py-6 px-3 rounded-2xl bg-card border border-border">
      <div className="text-4xl font-semibold tracking-tight tabular-nums">
        {value}
      </div>
      <div className="text-[10px] uppercase tracking-widest text-muted-foreground mt-1">
        {label}
        {suffix && <span className="text-muted-foreground/70">{suffix}</span>}
      </div>
    </div>
  )
}

function ConditionMiniCard({
  condition,
  count,
  byDifficulty,
}: {
  condition: string
  count: number
  byDifficulty: Record<string, number>
}) {
  const total = Math.max(1, Object.values(byDifficulty).reduce((a, b) => a + b, 0))
  const setActiveTab = useReviewStore((s) => s.setActiveTab)
  const setFilterConditions = useReviewStore((s) => s.setFilterConditions)

  return (
    <button
      type="button"
      onClick={() => {
        setFilterConditions([condition])
        setActiveTab("cases")
      }}
      className="text-left bg-card border border-border rounded-xl p-3 hover:border-primary/40 hover:-translate-y-0.5 transition-all"
    >
      <div className="flex items-baseline justify-between">
        <span className="text-[10px] font-mono uppercase tracking-wider text-muted-foreground">
          {conditionShort(condition)}
        </span>
        <span className="text-xl font-semibold tabular-nums">{count}</span>
      </div>
      <div className="text-xs mt-0.5 font-medium leading-tight">
        {conditionLabel(condition)}
      </div>
      <div className="mt-2 flex h-1 rounded-full overflow-hidden bg-muted">
        <Bar
          value={byDifficulty.straightforward ?? 0}
          total={total}
          color="bg-emerald-500"
        />
        <Bar
          value={byDifficulty.moderate ?? 0}
          total={total}
          color="bg-amber-500"
        />
        <Bar
          value={byDifficulty.diagnostic_puzzle ?? 0}
          total={total}
          color="bg-rose-500"
        />
      </div>
    </button>
  )
}

function Bar({
  value,
  total,
  color,
}: {
  value: number
  total: number
  color: string
}) {
  const pct = (value / total) * 100
  if (pct === 0) return null
  return <div className={color} style={{ width: `${pct}%` }} />
}

function DifficultyChart({
  byDifficulty,
  total,
}: {
  byDifficulty: Record<string, number>
  total: number
}) {
  const entries = Object.entries(byDifficulty).sort((a, b) => b[1] - a[1])
  return (
    <div className="space-y-2">
      {entries.map(([key, value]) => {
        const pct = (value / Math.max(1, total)) * 100
        return (
          <div key={key} className="space-y-1">
            <div className="flex items-center justify-between text-xs">
              <span className="capitalize text-foreground/90">
                {key.replace(/_/g, " ")}
              </span>
              <span className="text-muted-foreground tabular-nums">
                {value} · {pct.toFixed(0)}%
              </span>
            </div>
            <div className="h-1.5 bg-muted rounded-full overflow-hidden">
              <div
                className="h-full bg-primary"
                style={{ width: `${pct}%` }}
              />
            </div>
          </div>
        )
      })}
    </div>
  )
}

