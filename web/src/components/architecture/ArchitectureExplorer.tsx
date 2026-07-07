import { useMemo, useState, type ComponentType } from "react"
import {
  Activity,
  BrainCircuit,
  Database,
  FileJson,
  FlaskConical,
  GitBranch,
  Layers3,
  Network,
  PanelTop,
  Route,
  ScrollText,
  Server,
  ShieldCheck,
  Sparkles,
  Stethoscope,
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
    purpose: "Main clinician-facing dashboard for case exploration, model selection, agent execution, trace replay, rules editing, and this architecture explorer.",
    kind: "React app",
    layers: ["Frontend", "Runtime"],
    icon: PanelTop,
    accent: "sky",
    x: 12,
    y: 16,
    files: ["web/src/components/layout/AppShell.tsx", "web/src/api/client.ts", "web/src/components/agent/AgentTimeline.tsx"],
    details: ["Vite + React 19 + TypeScript + Tailwind CSS v4.", "Consumes REST endpoints and SSE streams under /api/v1.", "Uses Zustand for app state and TanStack Query for server state."],
  },
  {
    id: "api",
    title: "FastAPI Runtime",
    path: "agent-platform/src/neuroagent/api/",
    purpose: "Backend API that loads datasets, serves cases and hospital rules, streams agent runs, manages model loading, saves traces, and serves the built dashboard.",
    kind: "Service boundary",
    layers: ["Runtime", "Frontend"],
    icon: Server,
    accent: "cyan",
    x: 34,
    y: 16,
    files: ["api/app.py", "api/routes/agent.py", "api/routes/cases.py"],
    details: ["Port 8888 in the documented setup.", "Streams agent events as Server-Sent Events.", "Preloads NeuroBench dataset indexes into app state."],
  },
  {
    id: "schemas",
    title: "Shared Schemas",
    path: "packages/neuroagent-schemas/",
    purpose: "Pydantic contract for NeuroBench cases, patient profiles, ground truth, evaluation records, and all structured diagnostic tool outputs.",
    kind: "Workspace package",
    layers: ["Data", "Runtime"],
    icon: FileJson,
    accent: "violet",
    x: 57,
    y: 16,
    files: ["case.py", "patient.py", "tool_outputs.py"],
    details: ["Used by API, evaluation runner, mock server, and dataset generation.", "Dispatches follow-up output parsing by tool name to avoid ambiguous union resolution.", "Covers the expanded v4/v5 tool output set."],
  },
  {
    id: "data",
    title: "NeuroBench Data",
    path: "data/",
    purpose: "Versioned neurological benchmark cases, generated tool outputs, review artifacts, traces, and dataset evolution records.",
    kind: "Dataset corpus",
    layers: ["Data", "Evaluation", "Review"],
    icon: Database,
    accent: "emerald",
    x: 80,
    y: 16,
    files: ["data/neurobench_v5/cases/", "data/review/", "data/traces/"],
    details: ["v5 is the current default: 516 cases across 20 conditions.", "Case JSON includes initial outputs, follow-up outputs, fallback tool outputs, and ground truth.", "Traces are saved after streamed runs for replay."],
  },
  {
    id: "orchestrator",
    title: "Agent Orchestrator",
    path: "agent-platform/src/neuroagent/agent/",
    purpose: "The core ReAct loop: builds prompt context, calls the LLM, dispatches tool calls, injects reflection, records traces, tracks cost, and stores memory.",
    kind: "Reasoning core",
    layers: ["Runtime", "Reasoning"],
    icon: BrainCircuit,
    accent: "rose",
    x: 34,
    y: 43,
    files: ["agent/orchestrator.py", "agent/reasoning.py", "agent/reflection.py"],
    details: ["Runs up to 15 turns by default.", "Supports non-streaming and SSE streaming execution.", "Current reasoning state is transcript-based, not graph-based."],
  },
  {
    id: "llm",
    title: "LLM Client",
    path: "agent-platform/src/neuroagent/llm/",
    purpose: "OpenAI-compatible client wrapper for vLLM, Ollama, GitHub Copilot models, and streaming tool-call responses.",
    kind: "Model adapter",
    layers: ["Runtime", "Reasoning"],
    icon: Sparkles,
    accent: "amber",
    x: 12,
    y: 43,
    files: ["llm/client.py", "llm/prompts.py", "config/system_prompts/"],
    details: ["Strips Qwen thinking tags and parses tool calls.", "Loads orchestrator, reflection, report, specialist, and judge prompts.", "Feeds token usage back into traces."],
  },
  {
    id: "tools",
    title: "Diagnostic Tools",
    path: "agent-platform/src/neuroagent/tools/",
    purpose: "OpenAI-style diagnostic tool registry for EEG, MRI, ECG, labs, CSF, CT, echo, monitoring, imaging, specialist tests, literature, drug checks, and specialist consults.",
    kind: "Tool layer",
    layers: ["Runtime", "Tools", "Reasoning"],
    icon: TestTube2,
    accent: "sky",
    x: 57,
    y: 43,
    files: ["tools/tool_registry.py", "tools/base.py", "tools/mock_server.py"],
    details: ["12 base tools in single-model mode.", "Specialist consult becomes the 13th tool in mock or dual-model mode.", "Every tool returns a serialized ToolResult with optional cost."],
  },
  {
    id: "rules",
    title: "Hospital Rules",
    path: "agent-platform/config/hospital_rules/",
    purpose: "Hospital-specific YAML protocols injected into the system prompt and checked after runs for compliance.",
    kind: "Protocol engine",
    layers: ["Runtime", "Reasoning", "Data"],
    icon: ShieldCheck,
    accent: "emerald",
    x: 80,
    y: 43,
    files: ["rules/rules_engine.py", "rules/pathway_checker.py", "config/hospital_rules/*"],
    details: ["Five hospital profiles: Mayo, NHS, Charite, Todai, HC-FMUSP.", "All pathways are injected so matching does not leak the diagnosis.", "Mandatory and contraindicated actions are exposed to metrics and UI."],
  },
  {
    id: "memory",
    title: "Patient Memory",
    path: "agent-platform/src/neuroagent/memory/",
    purpose: "ChromaDB-backed longitudinal memory that retrieves prior encounters and stores compact post-run summaries.",
    kind: "Vector memory",
    layers: ["Runtime", "Reasoning", "Data"],
    icon: ScrollText,
    accent: "violet",
    x: 21,
    y: 70,
    files: ["memory/patient_memory.py", "memory/memory_retriever.py", "memory/memory_summarizer.py"],
    details: ["Injects previous encounters into the system prompt when enabled.", "Stores tools used and final assessment per patient.", "Defaults to ./data/patient_memory."],
  },
  {
    id: "evaluation",
    title: "Evaluation Stack",
    path: "agent-platform/src/neuroagent/evaluation/",
    purpose: "Runs agents on NeuroBench, computes metrics, injects noise for ablations, analyzes results, and delegates reasoning-quality assessment to an LLM judge.",
    kind: "Benchmark runner",
    layers: ["Evaluation", "Runtime"],
    icon: Activity,
    accent: "amber",
    x: 43,
    y: 70,
    files: ["evaluation/runner.py", "evaluation/metrics.py", "evaluation/llm_judge.py"],
    details: ["Uses MockServer per case for deterministic tool outputs.", "Formats patient information exactly as the API does.", "Feeds traces and tools-called lists into metrics and judge workflows."],
  },
  {
    id: "generation",
    title: "Dataset Generation",
    path: "dataset-generation/",
    purpose: "Pipeline and documentation for building, validating, balancing, and reviewing NeuroBench cases and gold trajectories.",
    kind: "Data factory",
    layers: ["Data", "Research"],
    icon: FlaskConical,
    accent: "rose",
    x: 65,
    y: 70,
    files: ["src/neurobench_gen/", "criteria_packs/", "GOLD_TRAJECTORY_AUTHORING_GUIDE.md"],
    details: ["Contains condition-specific criteria packs.", "Defines tool report style and tool parameter vocabulary.", "Supports v5 balancing and validation workflows."],
  },
  {
    id: "review",
    title: "Review Platform",
    path: "web-review/ + review_api/",
    purpose: "Separate doctor-led dataset review app with reviewer-code isolation, annotation persistence, admin aggregation, and tool-output review workflows.",
    kind: "Review workflow",
    layers: ["Review", "Frontend", "Runtime"],
    icon: Stethoscope,
    accent: "cyan",
    x: 88,
    y: 70,
    files: ["agent-platform/src/neuroagent/review_api/", "web-review/src/", "data/review/"],
    details: ["Backend runs on port 8889 and frontend on 5174 in dev.", "Uses X-Reviewer-Code for reviewer isolation.", "Stores annotations in data/review/annotations by version and reviewer."],
  },
  {
    id: "research",
    title: "Reasoning Research",
    path: "research/reasoning-frameworks/",
    purpose: "State-of-the-art survey and roadmap for moving beyond linear ReAct toward graph, search, and multi-agent blackboard reasoning.",
    kind: "Research direction",
    layers: ["Research", "Reasoning"],
    icon: GitBranch,
    accent: "slate",
    x: 12,
    y: 88,
    files: ["reasoning-frameworks-research.md", "references.bib"],
    details: ["Proposes Diagnostic Hypothesis Graph first.", "Adds deliberate search over diagnostic trajectories as an offline/advanced engine.", "Frames multi-agent clinical panel as a shared graph blackboard."],
  },
  {
    id: "deployment",
    title: "Deployment",
    path: "deployment/",
    purpose: "Hostinger and Raspberry Pi deployment notes, services, Nginx config, review app backup scripts, and operating runbooks.",
    kind: "Operations",
    layers: ["Deployment", "Runtime"],
    icon: Route,
    accent: "emerald",
    x: 35,
    y: 88,
    files: ["deployment/hostinger/", "deployment/raspberry-pi/README.md"],
    details: ["Includes systemd services and timers for the review platform.", "Documents static frontend plus Python backend deployment shape.", "Keeps GPU-serving concerns separate from review deployment."],
  },
]

const LINKS: ArchitectureLink[] = [
  { from: "web", to: "api", label: "REST + SSE", layers: ["Frontend", "Runtime"] },
  { from: "api", to: "orchestrator", label: "run case", layers: ["Runtime", "Reasoning"] },
  { from: "api", to: "data", label: "load cases", layers: ["Data", "Runtime"] },
  { from: "api", to: "schemas", label: "validate", layers: ["Data", "Runtime"] },
  { from: "orchestrator", to: "llm", label: "chat/tool calls", layers: ["Runtime", "Reasoning"] },
  { from: "orchestrator", to: "tools", label: "dispatch", layers: ["Runtime", "Tools", "Reasoning"] },
  { from: "orchestrator", to: "rules", label: "prompt context", layers: ["Runtime", "Reasoning"] },
  { from: "orchestrator", to: "memory", label: "retrieve/store", layers: ["Runtime", "Reasoning", "Data"] },
  { from: "tools", to: "data", label: "mock outputs", layers: ["Tools", "Data", "Evaluation"] },
  { from: "evaluation", to: "orchestrator", label: "batch runs", layers: ["Evaluation", "Runtime"] },
  { from: "evaluation", to: "schemas", label: "case contracts", layers: ["Evaluation", "Data"] },
  { from: "generation", to: "data", label: "case JSON", layers: ["Data", "Research"] },
  { from: "generation", to: "schemas", label: "validate", layers: ["Data"] },
  { from: "review", to: "data", label: "annotations", layers: ["Review", "Data"] },
  { from: "research", to: "orchestrator", label: "next framework", layers: ["Research", "Reasoning"] },
  { from: "deployment", to: "api", label: "serve", layers: ["Deployment", "Runtime"] },
  { from: "deployment", to: "review", label: "deploy review", layers: ["Deployment", "Review"] },
]

const REPO_ROWS = [
  ["agent-platform", "Main Python package: orchestrator, tools, API, rules, memory, evaluation, training.", "Core runtime"],
  ["packages/neuroagent-schemas", "Shared Pydantic schema package for cases, patient profiles, tool outputs, and evaluation.", "Contracts"],
  ["dataset-generation", "Case generation, validation, criteria packs, and gold trajectory authoring docs.", "Data factory"],
  ["data", "Versioned NeuroBench datasets, review artifacts, traces, and generated benchmark outputs.", "Corpus"],
  ["web", "Main React dashboard for interactive agent execution, dataset exploration, trace replay, rules editing.", "Frontend"],
  ["web-review", "Separate clinical review UI for blind reviewer annotation and admin aggregation.", "Review frontend"],
  ["research", "Reasoning-framework survey and bibliography driving the post-ReAct roadmap.", "Research"],
  ["deployment", "Hostinger, Raspberry Pi, service, Nginx, and backup operational files.", "Ops"],
  ["papers / presentations", "Explainers, paper assets, and presentation material for publication workflows.", "Publication"],
]

const FLOW_STEPS = [
  { title: "1. Case Context", body: "FastAPI loads NeuroBench JSON, validates it through shared schemas, and formats only the clinician-visible patient presentation." },
  { title: "2. Prompt Assembly", body: "The orchestrator combines the base system prompt, selected hospital protocols, optional patient memory, and the case presentation." },
  { title: "3. ReAct Turns", body: "The LLM emits visible reasoning plus tool calls. The registry executes valid tools and returns structured observations." },
  { title: "4. Reflection", body: "After tool results, a reflection prompt asks the model to update its differential before the next action." },
  { title: "5. Trace + Metrics", body: "Assistant turns, tool results, token usage, costs, final assessment, and replay events are saved for review and evaluation." },
]

const REASONING_ROADMAP = [
  ["Current", "Linear ReAct", "Transcript state, tool calls, observations, reflection prompts, regex-extracted final assessment."],
  ["Next", "Diagnostic Hypothesis Graph", "Typed findings, hypotheses, evidence, probabilities, and cost-aware value-of-information test choice."],
  ["Advanced", "Deliberate Search", "Search over diagnostic trajectories for hard cases and high-quality fine-tuning data generation."],
  ["Panel", "Shared Blackboard", "Specialist agents read/write one graph state: diagnostician, planner, skeptic, protocol officer, cost steward."],
]

export function ArchitectureExplorer() {
  const [selectedLayer, setSelectedLayer] = useState<Layer>("All")
  const [selectedNodeId, setSelectedNodeId] = useState("orchestrator")

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
    <div className="flex-1 overflow-y-auto bg-background">
      <div className="mx-auto max-w-7xl p-6 space-y-6">
        <header className="flex flex-wrap items-start justify-between gap-4">
          <div className="max-w-3xl">
            <div className="flex items-center gap-2 text-sm font-semibold uppercase text-primary">
              <Network className="h-4 w-4" />
              Architecture Explorer
            </div>
            <h2 className="mt-2 text-2xl font-bold">NeuroAgent repository map</h2>
            <p className="mt-2 text-base leading-7 text-muted-foreground">
              Explore how the agent platform, reasoning loop, tool simulation, datasets, evaluation stack,
              and review interfaces fit together.
            </p>
          </div>
          <div className="grid grid-cols-3 gap-2 text-center">
            <Metric value="13" label="max tools" />
            <Metric value="5" label="hospitals" />
            <Metric value="516" label="v5 cases" />
          </div>
        </header>

        <section className="rounded-lg border border-border bg-card">
          <div className="flex flex-wrap items-center gap-2 border-b border-border p-3">
            {LAYERS.map((layer) => (
              <button
                key={layer}
                onClick={() => setSelectedLayer(layer)}
                className={cn(
                  "rounded-md border px-3 py-1.5 text-sm font-medium transition-colors",
                  selectedLayer === layer
                    ? "border-primary bg-primary/10 text-primary"
                    : "border-border text-muted-foreground hover:bg-secondary hover:text-foreground",
                )}
              >
                {layer}
              </button>
            ))}
          </div>

          <div className="grid min-h-[620px] grid-cols-[minmax(0,1fr)_360px]">
            <div className="relative min-h-[620px] overflow-hidden border-r border-border bg-secondary/30">
              <svg className="absolute inset-0 h-full w-full" viewBox="0 0 100 100" preserveAspectRatio="none">
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
                        strokeWidth={isFocused ? 0.45 : 0.22}
                        opacity={isFocused ? 0.75 : 0.25}
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
                      "absolute flex w-44 -translate-x-1/2 -translate-y-1/2 items-center gap-2 rounded-lg border bg-card/95 p-2 text-left shadow-sm backdrop-blur transition-all hover:border-primary/60 hover:shadow-md",
                      isSelected ? cn("ring-2 ring-primary/40", accent.border) : "border-border",
                    )}
                    style={{ left: `${node.x}%`, top: `${node.y}%` }}
                  >
                    <span className={cn("flex h-9 w-9 shrink-0 items-center justify-center rounded-md", accent.bg)}>
                      <Icon className={cn("h-4 w-4", accent.text)} />
                    </span>
                    <span className="min-w-0">
                      <span className="block truncate text-sm font-semibold text-foreground">{node.title}</span>
                      <span className="block truncate text-xs text-muted-foreground">{node.kind}</span>
                    </span>
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
          <div className="rounded-lg border border-border bg-card p-4">
            <div className="mb-4 flex items-center gap-2">
              <Workflow className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold">Runtime Flow</h3>
            </div>
            <div className="grid grid-cols-5 gap-2">
              {FLOW_STEPS.map((step) => (
                <div key={step.title} className="rounded-lg border border-border bg-background p-3">
                  <div className="text-sm font-semibold">{step.title}</div>
                  <p className="mt-2 text-sm leading-6 text-muted-foreground">{step.body}</p>
                </div>
              ))}
            </div>
          </div>

          <div className="rounded-lg border border-border bg-card p-4">
            <div className="mb-4 flex items-center gap-2">
              <Layers3 className="h-5 w-5 text-primary" />
              <h3 className="text-lg font-semibold">Reasoning Framework</h3>
            </div>
            <div className="space-y-2">
              {REASONING_ROADMAP.map(([stage, title, body]) => (
                <div key={stage} className="grid grid-cols-[88px_minmax(0,1fr)] gap-3 rounded-lg border border-border bg-background p-3">
                  <Badge variant={stage === "Current" ? "info" : "success"} className="justify-center rounded-md">
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

        <section className="rounded-lg border border-border bg-card p-4">
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
    <div className="rounded-lg border border-border bg-card px-4 py-3">
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
      <div className="border-b border-border p-4">
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
              <div key={file} className="rounded-md bg-secondary px-2 py-1.5 font-mono text-xs text-foreground">
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
                  <div className="text-sm font-medium">{other.title}</div>
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
