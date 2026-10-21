import { useMemo, useState, type ComponentType } from "react"
import {
  Activity,
  BrainCircuit,
  Database,
  FileJson,
  FlaskConical,
  GitBranch,
  GraduationCap,
  Layers3,
  Network,
  PanelTop,
  Route,
  Server,
  ShieldCheck,
  Sparkles,
  Stethoscope,
  TerminalSquare,
  TestTube2,
  Workflow,
} from "lucide-react"
import { Badge } from "@/components/ui/Badge"
import { cn } from "@/lib/utils"

const LAYERS = [
  "All",
  "Runtime",
  "Reasoning",
  "Tools",
  "Data",
  "Evaluation",
  "Frontend",
  "Review",
  "Research",
  "Fine-tuning",
  "Deployment",
] as const

type Layer = (typeof LAYERS)[number]
type NodeLayer = Exclude<Layer, "All">

interface ArchitectureNode {
  id: string
  title: string
  path: string
  purpose: string
  kind: string
  layers: NodeLayer[]
  icon: ComponentType<{ className?: string }>
  accent: "sky" | "emerald" | "amber" | "rose" | "violet" | "cyan" | "slate"
  x: number
  y: number
  files: string[]
  details: string[]
}

interface ArchitectureLink {
  from: string
  to: string
  label: string
  layers: NodeLayer[]
}

const ACCENT_STYLES = {
  sky: {
    border: "border-sky-400/50",
    bg: "bg-sky-500/10",
    text: "text-sky-600 dark:text-sky-300",
    line: "#0ea5e9",
  },
  emerald: {
    border: "border-emerald-400/50",
    bg: "bg-emerald-500/10",
    text: "text-emerald-600 dark:text-emerald-300",
    line: "#10b981",
  },
  amber: {
    border: "border-amber-400/50",
    bg: "bg-amber-500/10",
    text: "text-amber-600 dark:text-amber-300",
    line: "#f59e0b",
  },
  rose: {
    border: "border-rose-400/50",
    bg: "bg-rose-500/10",
    text: "text-rose-600 dark:text-rose-300",
    line: "#f43f5e",
  },
  violet: {
    border: "border-violet-400/50",
    bg: "bg-violet-500/10",
    text: "text-violet-600 dark:text-violet-300",
    line: "#8b5cf6",
  },
  cyan: {
    border: "border-cyan-400/50",
    bg: "bg-cyan-500/10",
    text: "text-cyan-600 dark:text-cyan-300",
    line: "#06b6d4",
  },
  slate: {
    border: "border-slate-400/50",
    bg: "bg-slate-500/10",
    text: "text-slate-600 dark:text-slate-300",
    line: "#64748b",
  },
}

const NODES: ArchitectureNode[] = [
  {
    id: "web",
    title: "Dashboard UI",
    path: "web/",
    purpose: "Dashboard for case exploration, the case policy, profile selection, live and replayed episodes, the engineering reward, rules and this architecture explorer.",
    kind: "React app",
    layers: ["Frontend", "Runtime"],
    icon: PanelTop,
    accent: "sky",
    x: 12,
    y: 16,
    files: ["web/src/components/layout/AppShell.tsx", "web/src/api/client.ts", "web/src/components/agent/AgentTimeline.tsx"],
    details: ["Vite + React 19 + TypeScript + Tailwind CSS v4.", "Streams a run's episode events from POST /api/v1/runs/stream.", "Uses Zustand for app state and TanStack Query for server state."],
  },
  {
    id: "api",
    title: "FastAPI Runtime",
    path: "agent-platform/src/neuroagent/api/",
    purpose: "Serves cases and hospital rules, loads the fixed model panel, runs one profile on one case, stores episodes and serves the built dashboard.",
    kind: "Service boundary",
    layers: ["Runtime", "Frontend"],
    icon: Server,
    accent: "cyan",
    x: 34,
    y: 16,
    files: ["api/app.py", "api/routes/runs.py", "api/routes/episodes.py"],
    details: ["Port 8888 in the documented setup.", "Runs accept only a checked profile id, never a model name or endpoint.", "Episodes are saved under data/episodes and scored on request."],
  },
  {
    id: "schemas",
    title: "Shared Schemas",
    path: "packages/neuroagent-schemas/",
    purpose: "Strict Pydantic contract for NeuroBench cases, patient profiles, the case policy (ground truth) and every structured tool output.",
    kind: "Workspace package",
    layers: ["Data", "Runtime"],
    icon: FileJson,
    accent: "violet",
    x: 57,
    y: 16,
    files: ["case.py", "patient.py", "tool_outputs.py"],
    details: ["Schema v2: set-valued action criteria, avoided actions, sequence constraints, stop rule.", "Used by the harness, the API, dataset generation and review.", "Policies carry a review status: draft, needs revision or approved."],
  },
  {
    id: "data",
    title: "NeuroBench Data",
    path: "data/",
    purpose: "600 schema-v2 cases across 20 neurological conditions, split manifests and saved episodes.",
    kind: "Dataset corpus",
    layers: ["Data", "Evaluation", "Review"],
    icon: Database,
    accent: "emerald",
    x: 80,
    y: 16,
    files: ["data/neurobench/cases/", "data/neurobench/splits/", "data/episodes/"],
    details: ["Case JSON holds the presentation, stored tool outputs and the clinical policy.", "All policies are drafts until two physicians approve them.", "Episodes are append-only event logs, one JSON file per run."],
  },
  {
    id: "harness",
    title: "Harness Kernel",
    path: "agent-platform/src/neuroagent/harness/",
    purpose: "Boots a profile into a model adapter and an agent loop, runs it against the environment and records every step as a typed episode event.",
    kind: "Runtime core",
    layers: ["Runtime", "Reasoning"],
    icon: BrainCircuit,
    accent: "rose",
    x: 34,
    y: 43,
    files: ["harness/kernel.py", "harness/loops.py", "harness/profile.py", "harness/store.py"],
    details: ["Path: HarnessProfile → ModelAdapter → AgentLoop → NeuroBenchEnvironment → ClinicalEpisode.", "Three loops: policy (primary), direct and ReAct (ablations).", "Every output is a typed tool call or a typed final assessment; hidden reasoning is never stored."],
  },
  {
    id: "llm",
    title: "Model Adapters",
    path: "harness/adapters.py + llm/",
    purpose: "Native tool-calling adapters over an OpenAI-compatible vLLM endpoint for the fixed three-model panel.",
    kind: "Model adapter",
    layers: ["Runtime", "Reasoning"],
    icon: Sparkles,
    accent: "amber",
    x: 12,
    y: 43,
    files: ["harness/adapters.py", "llm/client.py", "config/profiles/*.yaml"],
    details: ["Qwen3.5-9B, Granite 4.1 8B and Gemma 4 E4B, thinking disabled.", "Sampling frozen per model at the model card's recommendation.", "A text-only reply is an invalid action, retried within the profile's budget."],
  },
  {
    id: "tools",
    title: "Clinical Environment",
    path: "harness/environment.py + tools/",
    purpose: "NeuroBenchEnvironment exposes 16 typed diagnostic tools and answers each action from the case's stored outputs, a fallback library or a rejection.",
    kind: "Environment",
    layers: ["Runtime", "Tools", "Reasoning"],
    icon: TestTube2,
    accent: "sky",
    x: 57,
    y: 43,
    files: ["harness/environment.py", "tools/tool_registry.py", "tools/fallback_library.py", "config/tools/costs.yaml"],
    details: ["Imaging, EEG, ECG, labs, CSF, echo, monitoring, specialised tests, literature and drug checks.", "Each observation carries its simulated cost.", "The direct ablation receives every stored initial result up front."],
  },
  {
    id: "rules",
    title: "Hospital Rules",
    path: "agent-platform/config/hospital_rules/",
    purpose: "Hospital-specific YAML pathways, browsable and editable in the dashboard. Harness runs do not read them.",
    kind: "Protocol library",
    layers: ["Data"],
    icon: ShieldCheck,
    accent: "emerald",
    x: 80,
    y: 43,
    files: ["rules/rules_engine.py", "rules/pathway_checker.py", "config/hospital_rules/*"],
    details: ["Five hospital profiles: Mayo, NHS, Charite, Todai, HC-FMUSP.", "Not part of the prompt, the environment or the reward.", "Kept as reference material for future protocol-conditioned experiments."],
  },
  {
    id: "evaluation",
    title: "Policy Reward",
    path: "agent-platform/src/neuroagent/evaluation/",
    purpose: "Deterministic ClinicalPolicyReward over an episode and its case policy, plus the benchmark runner over splits, profiles and seeds.",
    kind: "Benchmark + reward",
    layers: ["Evaluation", "Runtime"],
    icon: Activity,
    accent: "amber",
    x: 43,
    y: 70,
    files: ["evaluation/policy_reward.py", "evaluation/benchmark.py"],
    details: ["Diagnosis, coverage, tool accuracy, safety, waste, sequence, stopping, cost and token efficiency.", "Safety caps: contraindicated 0.10, harmful 0.35, hard sequence violation 0.50.", "Reportable numbers need approved policies; drafts are engineering checks only."],
  },
  {
    id: "training",
    title: "Training",
    path: "agent-platform/src/neuroagent/training/",
    purpose: "LoRA SFT over typed episodes and single-GPU GRPO with verifiable rewards, both running the unchanged benchmark loop.",
    kind: "Model training",
    layers: ["Fine-tuning", "Evaluation", "Research"],
    icon: GraduationCap,
    accent: "violet",
    x: 18,
    y: 88,
    files: ["training/train_sft.py", "training/train_grpo.py", "training/prefix_packing.py", "training/data/episodes.py"],
    details: ["SFT: one sequence per episode, loss on every model action, prefix chaining asserted.", "GRPO: colocated vLLM rollouts scored by the policy reward, token-level DAPO loss, no KL.", "No golden reasoning trajectories."],
  },
  {
    id: "serving",
    title: "Model Serving",
    path: "agent-platform/scripts/runtime/",
    purpose: "vLLM serving for the fixed panel, with LoRA adapters served under an alias that a profile can point at.",
    kind: "Inference serving",
    layers: ["Runtime", "Fine-tuning", "Deployment"],
    icon: TerminalSquare,
    accent: "amber",
    x: 43,
    y: 88,
    files: ["scripts/runtime/serve_model.sh", "scripts/runtime/vllm_serve.py", "docs/models.md"],
    details: ["Only the three panel models are accepted.", "The API stops only a server it started itself.", "Adapters: LORA_ADAPTER / LORA_NAME, recorded as the episode's model_id."],
  },
  {
    id: "generation",
    title: "Dataset Generation",
    path: "dataset-generation/",
    purpose: "Authoring, validation and balancing of NeuroBench cases and their clinical policies.",
    kind: "Data factory",
    layers: ["Data", "Research", "Fine-tuning"],
    icon: FlaskConical,
    accent: "rose",
    x: 65,
    y: 70,
    files: ["src/neurobench_gen/", "criteria_packs/"],
    details: ["Condition-specific criteria packs.", "Tool report style and parameter vocabulary.", "Policies are generated as drafts for physician review."],
  },
  {
    id: "review",
    title: "Review Platform",
    path: "web-review/ + review_api/",
    purpose: "Separate physician review app: two independent reviewers approve each policy on seven dimensions, a third adjudicates disagreements.",
    kind: "Review workflow",
    layers: ["Review", "Frontend", "Runtime"],
    icon: Stethoscope,
    accent: "cyan",
    x: 88,
    y: 70,
    files: ["agent-platform/src/neuroagent/review_api/", "web-review/src/", "data/review/"],
    details: ["Backend runs on port 8889 and frontend on 5174 in dev.", "Uses X-Reviewer-Code for reviewer isolation.", "Approval moves a policy from draft to approved."],
  },
  {
    id: "research",
    title: "Research Notes",
    path: "docs/research/",
    purpose: "Literature reviews and proposals beyond the current loops, such as localization-first and graph-structured reasoning.",
    kind: "Research direction",
    layers: ["Research", "Reasoning"],
    icon: GitBranch,
    accent: "slate",
    x: 65,
    y: 88,
    files: ["literature-review.md", "reasoning-frameworks.md", "proposal-localization-first-reasoning.md"],
    details: ["Proposals, not implemented loops.", "A new approach would enter as another loop plugin with the same environment and reward.", "Bibliography in references.bib."],
  },
  {
    id: "deployment",
    title: "Deployment",
    path: "deployment/",
    purpose: "Hostinger and Raspberry Pi deployment notes, services, Nginx config, review app backup scripts and runbooks.",
    kind: "Operations",
    layers: ["Deployment", "Runtime"],
    icon: Route,
    accent: "emerald",
    x: 88,
    y: 88,
    files: ["deployment/hostinger/", "deployment/raspberry-pi/README.md"],
    details: ["Systemd services and timers for the review platform.", "Static frontend plus Python backend.", "GPU serving stays separate from review deployment."],
  },
]

const LINKS: ArchitectureLink[] = [
  { from: "web", to: "api", label: "REST + SSE", layers: ["Frontend", "Runtime"] },
  { from: "api", to: "harness", label: "run profile", layers: ["Runtime", "Reasoning"] },
  { from: "api", to: "data", label: "cases + episodes", layers: ["Data", "Runtime"] },
  { from: "api", to: "schemas", label: "validate", layers: ["Data", "Runtime"] },
  { from: "api", to: "rules", label: "browse + edit", layers: ["Data", "Runtime"] },
  { from: "harness", to: "llm", label: "typed actions", layers: ["Runtime", "Reasoning"] },
  { from: "harness", to: "tools", label: "execute", layers: ["Runtime", "Tools", "Reasoning"] },
  { from: "tools", to: "data", label: "stored outputs", layers: ["Tools", "Data", "Evaluation"] },
  { from: "evaluation", to: "harness", label: "batch episodes", layers: ["Evaluation", "Runtime"] },
  { from: "evaluation", to: "schemas", label: "case policy", layers: ["Evaluation", "Data"] },
  { from: "training", to: "evaluation", label: "policy reward", layers: ["Fine-tuning", "Evaluation"] },
  { from: "training", to: "harness", label: "rollouts", layers: ["Fine-tuning", "Runtime"] },
  { from: "training", to: "data", label: "splits + episodes", layers: ["Fine-tuning", "Data"] },
  { from: "training", to: "serving", label: "LoRA adapters", layers: ["Fine-tuning", "Runtime"] },
  { from: "serving", to: "llm", label: "OpenAI API", layers: ["Fine-tuning", "Runtime"] },
  { from: "serving", to: "api", label: "model loading", layers: ["Fine-tuning", "Runtime"] },
  { from: "generation", to: "data", label: "case JSON", layers: ["Data", "Research"] },
  { from: "generation", to: "schemas", label: "validate", layers: ["Data"] },
  { from: "review", to: "data", label: "policy approval", layers: ["Review", "Data"] },
  { from: "research", to: "harness", label: "new loops", layers: ["Research", "Reasoning"] },
  { from: "deployment", to: "api", label: "serve", layers: ["Deployment", "Runtime"] },
  { from: "deployment", to: "review", label: "deploy review", layers: ["Deployment", "Review"] },
]

const REPO_ROWS = [
  ["agent-platform/src/neuroagent/harness", "Profiles, adapters, loops, environment, episode store and kernel.", "Core runtime"],
  ["agent-platform/src/neuroagent/evaluation", "ClinicalPolicyReward and the benchmark runner.", "Evaluation"],
  ["agent-platform/src/neuroagent/training", "LoRA SFT over episodes, GRPO with verifiable rewards, prefix packing.", "Fine-tuning"],
  ["agent-platform/src/neuroagent/api", "FastAPI: cases, hospitals, models, runs, episodes, static dashboard.", "Service"],
  ["agent-platform/config/profiles", "The nine checked experiment profiles (3 models × 3 loops).", "Experiments"],
  ["agent-platform/docs/clinical-policy-harness.md", "Runtime contract, reward components, training design and experimental claims.", "Specification"],
  ["packages/neuroagent-schemas", "Shared Pydantic schema package for cases, policies and tool outputs.", "Contracts"],
  ["dataset-generation", "Case and policy authoring, validation and criteria packs.", "Data factory"],
  ["data", "NeuroBench cases, split manifests, review artifacts and saved episodes.", "Corpus"],
  ["web", "Main React dashboard for live runs, episode replay, the case policy and the reward.", "Frontend"],
  ["web-review", "Separate physician review UI for blind policy review and adjudication.", "Review frontend"],
  ["docs/research", "Literature reviews and reasoning proposals.", "Research"],
  ["deployment", "Hostinger, Raspberry Pi, service, Nginx and backup operational files.", "Ops"],
]

const FLOW_STEPS = [
  { title: "1. Profile", body: "A checked profile fixes the model, the loop, the turn budget, the invalid-action budget and the cost budget." },
  { title: "2. Case", body: "The environment loads the case and shows the model only the clinician-visible presentation and the tool catalogue." },
  { title: "3. Typed actions", body: "Each turn the model emits a tool call or a final assessment. Invalid actions are rejected and retried within budget." },
  { title: "4. Observations", body: "The environment answers from stored outputs or the fallback library, with a simulated cost per study." },
  { title: "5. Episode + reward", body: "Every step is an append-only event; the policy reward scores the finished episode against the case policy." },
]

const REASONING_ROADMAP = [
  ["Primary", "Policy loop", "Presentation only; evidence is discovered through typed tool calls until a structured assessment."],
  ["Ablation", "Direct", "Receives every stored initial result and submits an assessment: a diagnostic upper bound."],
  ["Ablation", "ReAct prompt", "Same typed loop, plus a short visible rationale recorded as a react.rationale plugin event."],
  ["Proposal", "Beyond the loops", "Graph-structured or localization-first reasoning would enter as a new loop plugin with the same environment and reward."],
]

const FINETUNING_STEPS = [
  { title: "Episodes", body: "Completed typed episodes from the benchmark loop; bootstrap candidates are labelled candidate_not_gold and rejected by default." },
  { title: "SFT", body: "LoRA SFT with one sequence per episode and loss on every model action, rendered exactly as at inference." },
  { title: "GRPO", body: "Rollouts run the unchanged loop on a colocated vLLM engine; each episode is scored by the deterministic policy reward." },
  { title: "Serve + evaluate", body: "Serve the adapter under an alias, point a profile at it and run the standard benchmark on held-out splits." },
]

const FINETUNING_TECHNIQUES = [
  ["LoRA", "Adapters on the language model's decoder projections only (attention, gated delta net, MLP), r=16 for GRPO."],
  ["SFT", "Whole-episode rendering with prefix chaining asserted per episode and vocabulary projection only at supervised positions."],
  ["GRPO", "Group-relative advantages from verifiable rewards, batch-level normalisation, one optimizer step per group batch."],
  ["DAPO loss", "Token-level loss with clip-higher (0.2 / 0.28), truncated episodes masked, no KL term."],
  ["Prefix packing", "A group's shared ~8.5k-token prompt in one forward with a FlexAttention block mask (Gemma, Granite)."],
  ["vLLM", "Colocated engine with sleep/wake around rollouts and token-level truncated importance sampling."],
]

export function ArchitectureExplorer() {
  const [selectedLayer, setSelectedLayer] = useState<Layer>("All")
  const [selectedNodeId, setSelectedNodeId] = useState("harness")

  const visibleNodes = useMemo(
    () => NODES.filter((node) => selectedLayer === "All" || node.layers.includes(selectedLayer)),
    [selectedLayer],
  )
  const visibleNodeIds = useMemo(() => new Set(visibleNodes.map((node) => node.id)), [visibleNodes])
  const visibleLinks = useMemo(
    () => LINKS.filter((link) => visibleNodeIds.has(link.from) && visibleNodeIds.has(link.to)),
    [visibleNodeIds],
  )
  const selectedNode = visibleNodes.find((node) => node.id === selectedNodeId) ?? visibleNodes[0] ?? NODES[0]
  const connectedLinks = LINKS.filter((link) => link.from === selectedNode.id || link.to === selectedNode.id)

  return (
    <div className="flex-1 overflow-y-auto bg-background noise-bg">
      <div className="mx-auto max-w-7xl p-6 space-y-6">
        <header className="relative overflow-hidden rounded-lg border border-border bg-card p-5 shadow-sm">
          <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(120deg,transparent,rgba(56,189,248,0.08),transparent),linear-gradient(180deg,rgba(16,185,129,0.08),transparent)]" />
          <div className="relative flex flex-wrap items-start justify-between gap-4">
          <div className="max-w-3xl">
            <div className="flex items-center gap-2 text-sm font-semibold uppercase text-primary">
              <Network className="h-4 w-4" />
              Architecture Explorer
            </div>
            <h2 className="mt-2 text-2xl font-bold">NeuroAgent repository map</h2>
            <p className="mt-2 text-base leading-7 text-muted-foreground">
              Explore how profiles, the harness loops, the clinical environment, the policy reward, training
              and the review interfaces fit together.
            </p>
          </div>
          <div className="grid grid-cols-3 gap-2 text-center">
            <Metric value="16" label="tools" />
            <Metric value="9" label="profiles" />
            <Metric value="600" label="cases" />
          </div>
          </div>
        </header>

        <section className="overflow-hidden rounded-lg border border-border bg-card shadow-sm">
          <div className="flex flex-wrap items-center gap-2 border-b border-border bg-secondary/40 p-3">
            {LAYERS.map((layer) => (
              <button
                key={layer}
                onClick={() => setSelectedLayer(layer)}
                className={cn(
                  "rounded-md border px-3 py-1.5 text-sm font-medium transition-all duration-200",
                  selectedLayer === layer
                    ? "border-primary bg-primary/15 text-primary shadow-sm shadow-primary/10"
                    : "border-border bg-background/70 text-muted-foreground hover:-translate-y-0.5 hover:bg-secondary hover:text-foreground",
                )}
              >
                {layer}
              </button>
            ))}
          </div>

          <div className="grid min-h-[620px] grid-cols-[minmax(0,1fr)_360px]">
            <div className="arch-grid relative min-h-[620px] overflow-hidden border-r border-border bg-secondary/30">
              <svg className="absolute inset-0 h-full w-full" viewBox="0 0 100 100" preserveAspectRatio="none">
                <defs>
                  <filter id="archGlow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur stdDeviation="0.9" result="coloredBlur" />
                    <feMerge>
                      <feMergeNode in="coloredBlur" />
                      <feMergeNode in="SourceGraphic" />
                    </feMerge>
                  </filter>
                </defs>
                {visibleLinks.map((link) => {
                  const from = NODES.find((node) => node.id === link.from)
                  const to = NODES.find((node) => node.id === link.to)
                  if (!from || !to) return null
                  const isFocused = link.from === selectedNode.id || link.to === selectedNode.id
                  const color = ACCENT_STYLES[from.accent].line
                  return (
                    <g key={`${link.from}-${link.to}`}>
                      <line
                        x1={from.x}
                        y1={from.y}
                        x2={to.x}
                        y2={to.y}
                        stroke={color}
                        strokeWidth={isFocused ? 0.62 : 0.28}
                        opacity={isFocused ? 0.88 : 0.3}
                        filter={isFocused ? "url(#archGlow)" : undefined}
                      />
                      <line
                        className="arch-flow-line"
                        x1={from.x}
                        y1={from.y}
                        x2={to.x}
                        y2={to.y}
                        stroke={color}
                        strokeWidth={isFocused ? 0.36 : 0.18}
                        opacity={isFocused ? 0.9 : 0.28}
                      />
                    </g>
                  )
                })}
              </svg>

              {visibleNodes.map((node) => {
                const Icon = node.icon
                const accent = ACCENT_STYLES[node.accent]
                const isSelected = selectedNode.id === node.id
                return (
                  <button
                    key={node.id}
                    onClick={() => setSelectedNodeId(node.id)}
                    className={cn(
                      "arch-node group absolute flex w-44 -translate-x-1/2 -translate-y-1/2 items-center gap-2 overflow-hidden rounded-lg border bg-card/90 p-2 text-left shadow-sm backdrop-blur transition-all duration-300 hover:-translate-y-[54%] hover:border-primary/60 hover:shadow-lg hover:shadow-primary/10",
                      isSelected ? cn("ring-2 ring-primary/40 shadow-lg shadow-primary/15", accent.border) : "border-border",
                    )}
                    style={{ left: `${node.x}%`, top: `${node.y}%` }}
                  >
                    <span className={cn("relative flex h-9 w-9 shrink-0 items-center justify-center rounded-md transition-transform duration-300 group-hover:scale-105", accent.bg)}>
                      <Icon className={cn("h-4 w-4", accent.text)} />
                    </span>
                    <span className="min-w-0">
                      <span className="block truncate text-sm font-semibold text-foreground">{node.title}</span>
                      <span className="block truncate text-xs text-muted-foreground">{node.kind}</span>
                    </span>
                    {isSelected && <span className="absolute inset-x-2 bottom-0 h-[2px] rounded-full bg-primary" />}
                  </button>
                )
              })}
            </div>

            <aside className="flex min-h-[620px] flex-col">
              <NodeInspector node={selectedNode} connectedLinks={connectedLinks} />
            </aside>
          </div>
        </section>

        <section className="grid grid-cols-[minmax(0,1.1fr)_minmax(360px,0.9fr)] gap-4">
          <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
            <div className="mb-4 flex items-center gap-2">
              <Workflow className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold">Runtime Flow</h3>
            </div>
            <div className="grid grid-cols-5 gap-2">
              {FLOW_STEPS.map((step) => (
                <div key={step.title} className="rounded-lg border border-border bg-background p-3 transition-all duration-200 hover:-translate-y-1 hover:border-primary/40 hover:shadow-md hover:shadow-primary/5">
                  <div className="text-sm font-semibold">{step.title}</div>
                  <p className="mt-2 text-sm leading-6 text-muted-foreground">{step.body}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-lg border border-border bg-card p-4 shadow-sm">
            <div className="mb-4 flex items-center gap-2">
              <Layers3 className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold">Agent approaches</h3>
            </div>
            <div className="space-y-2">
              {REASONING_ROADMAP.map(([stage, title, body]) => (
                <div key={stage} className="grid grid-cols-[88px_minmax(0,1fr)] gap-3 rounded-lg border border-border bg-background p-3 transition-all duration-200 hover:border-primary/40">
                  <Badge variant={stage === "Primary" ? "info" : stage === "Ablation" ? "outline" : "default"} className="justify-center rounded-md">
                    {stage}
                  </Badge>
                  <div>
                    <div className="text-sm font-semibold">{title}</div>
                    <p className="mt-1 text-sm leading-6 text-muted-foreground">{body}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="rounded-lg border border-border bg-card p-4 shadow-sm">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <GraduationCap className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold">Fine-tuning and Model Serving</h3>
            </div>
            <div className="flex gap-2">
              <Badge variant="info" className="rounded-md">QLoRA</Badge>
              <Badge variant="success" className="rounded-md">SFT complete</Badge>
              <Badge variant="warning" className="rounded-md">RL memory bottleneck</Badge>
            </div>
          </div>

          <div className="grid grid-cols-[minmax(0,0.95fr)_minmax(0,1.05fr)] gap-4">
            <div className="grid grid-cols-2 gap-2">
              {FINETUNING_STEPS.map((step) => (
                <div key={step.title} className="rounded-lg border border-border bg-background p-3 transition-all duration-200 hover:-translate-y-1 hover:border-primary/40 hover:shadow-md hover:shadow-primary/5">
                  <div className="text-sm font-semibold">{step.title}</div>
                  <p className="mt-2 text-sm leading-6 text-muted-foreground">{step.body}</p>
                </div>
              ))}
            </div>

            <div className="overflow-hidden rounded-lg border border-border">
              <table className="w-full border-collapse text-left text-sm">
                <thead className="bg-secondary text-muted-foreground">
                  <tr>
                    <th className="w-28 px-3 py-2 font-semibold">Technique</th>
                    <th className="px-3 py-2 font-semibold">How this repo uses it</th>
                  </tr>
                </thead>
                <tbody>
                  {FINETUNING_TECHNIQUES.map(([technique, body]) => (
                    <tr key={technique} className="border-t border-border">
                      <td className="px-3 py-2 font-semibold text-primary">{technique}</td>
                      <td className="px-3 py-2 text-muted-foreground">{body}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <section className="rounded-lg border border-border bg-card p-4 shadow-sm">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <Route className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold">Repository Breakdown</h3>
            </div>
            <Badge variant="warning" className="rounded-md">
              architecture docs note: old 7-tool references are stale
            </Badge>
          </div>
          <div className="overflow-hidden rounded-lg border border-border">
            <table className="w-full border-collapse text-left text-sm">
              <thead className="bg-secondary text-muted-foreground">
                <tr>
                  <th className="w-56 px-3 py-2 font-semibold">Path</th>
                  <th className="px-3 py-2 font-semibold">Purpose</th>
                  <th className="w-36 px-3 py-2 font-semibold">Role</th>
                </tr>
              </thead>
              <tbody>
                {REPO_ROWS.map(([path, purpose, role]) => (
                  <tr key={path} className="border-t border-border">
                    <td className="px-3 py-2 font-mono text-xs text-primary">{path}</td>
                    <td className="px-3 py-2 text-muted-foreground">{purpose}</td>
                    <td className="px-3 py-2">
                      <Badge variant="outline" className="rounded-md">{role}</Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  )
}

function Metric({ value, label }: { value: string; label: string }) {
  return (
    <div className="rounded-lg border border-border bg-background/80 px-4 py-3 shadow-sm backdrop-blur">
      <div className="text-xl font-bold">{value}</div>
      <div className="text-xs font-medium uppercase text-muted-foreground">{label}</div>
    </div>
  )
}

function NodeInspector({ node, connectedLinks }: { node: ArchitectureNode; connectedLinks: ArchitectureLink[] }) {
  const Icon = node.icon
  const accent = ACCENT_STYLES[node.accent]

  return (
    <div className="flex h-full flex-col">
      <div className="relative overflow-hidden border-b border-border p-4">
        <div className={cn("absolute inset-x-0 top-0 h-1", accent.bg)} />
        <div className="flex items-start gap-3">
          <span className={cn("flex h-11 w-11 shrink-0 items-center justify-center rounded-lg", accent.bg)}>
            <Icon className={cn("h-5 w-5", accent.text)} />
          </span>
          <div className="min-w-0">
            <h3 className="text-lg font-semibold">{node.title}</h3>
            <p className="mt-1 font-mono text-xs text-primary">{node.path}</p>
          </div>
        </div>
        <p className="mt-4 text-sm leading-6 text-muted-foreground">{node.purpose}</p>
        <div className="mt-4 flex flex-wrap gap-2">
          {node.layers.map((layer) => (
            <Badge key={layer} variant="outline" className="rounded-md">
              {layer}
            </Badge>
          ))}
        </div>
      </div>

      <div className="min-h-0 flex-1 overflow-y-auto p-4 space-y-5">
        <InspectorSection title="Important files">
          <div className="space-y-2">
            {node.files.map((file) => (
              <div key={file} className="rounded-md border border-border bg-secondary/70 px-2 py-1.5 font-mono text-xs text-foreground">
                {file}
              </div>
            ))}
          </div>
        </InspectorSection>

        <InspectorSection title="Responsibilities">
          <ul className="space-y-2 text-sm leading-6 text-muted-foreground">
            {node.details.map((detail) => (
              <li key={detail} className="flex gap-2">
                <span className={cn("mt-2 h-1.5 w-1.5 shrink-0 rounded-full", accent.bg)} />
                <span>{detail}</span>
              </li>
            ))}
          </ul>
        </InspectorSection>

        <InspectorSection title="Connected systems">
          <div className="space-y-2">
            {connectedLinks.map((link) => {
              const otherId = link.from === node.id ? link.to : link.from
              const other = NODES.find((candidate) => candidate.id === otherId)
              if (!other) return null
              return (
                <div key={`${link.from}-${link.to}`} className="rounded-md border border-border p-2">
                  <div className="flex items-center justify-between gap-2">
                    <div className="text-sm font-medium">{other.title}</div>
                    <span className="h-1.5 w-8 rounded-full bg-primary/40" />
                  </div>
                  <div className="mt-1 text-xs text-muted-foreground">{link.label}</div>
                </div>
              )
            })}
          </div>
        </InspectorSection>
      </div>
    </div>
  )
}

function InspectorSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section>
      <h4 className="mb-2 text-xs font-semibold uppercase text-muted-foreground">{title}</h4>
      {children}
    </section>
  )
}
