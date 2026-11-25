import { ArrowLeft, ChevronRight, Loader2, Search } from "lucide-react"
import { useEffect, useMemo, useState } from "react"

import type { JsonValue, ToolDefinition } from "@/api/agentTypes"
import { Button } from "@/components/ui/Button"
import { humanize } from "@/lib/agentText"
import { cn } from "@/lib/utils"
import { filledArguments, missingRequired, SchemaForm, type FormValues } from "./SchemaForm"

interface OrderPadProps {
  tools: ToolDefinition[]
  sending: boolean
  onSend: (name: string, args: Record<string, JsonValue>, rationale: string) => void
  onToolOpened: (name: string) => void
  onSearch: (term: string) => void
}

/** Where an entry of the catalogue mentions the search term, so a value deep in a long
 * vocabulary (an assay, a modality) is found from the list. */
function matchHint(tool: ToolDefinition, term: string): string | null | undefined {
  const fn = tool.function
  if (`${fn.name} ${humanize(fn.name)} ${fn.description}`.toLowerCase().includes(term)) return null
  const loose = term.replace(/[\s-]+/g, "_")
  for (const [key, schema] of Object.entries(fn.parameters.properties)) {
    const values = schema.enum ?? schema.items?.enum ?? []
    const hits = values.filter((v) => v.toLowerCase().replace(/[\s-]+/g, "_").includes(loose))
    if (hits.length) return `${humanize(key)}: ${hits.slice(0, 4).join(", ")}${hits.length > 4 ? "…" : ""}`
    if ((schema.description ?? "").toLowerCase().includes(term)) return `Mentioned under ${humanize(key).toLowerCase()}`
  }
  return undefined
}

/** The catalogue the agent is given, in the agent's order, and the order form of one tool. */
export function OrderPad({ tools, sending, onSend, onToolOpened, onSearch }: OrderPadProps) {
  const [search, setSearch] = useState("")
  const [selected, setSelected] = useState<string | null>(null)
  const tool = tools.find((t) => t.function.name === selected) ?? null

  // The filter term is noted once typing has stopped, not per keystroke.
  useEffect(() => {
    if (!search.trim()) return
    const timer = setTimeout(() => onSearch(search), 900)
    return () => clearTimeout(timer)
  }, [search, onSearch])

  const shown = useMemo(() => {
    const term = search.trim().toLowerCase()
    return tools
      .map((t) => ({ tool: t, hint: term ? matchHint(t, term) : null }))
      .filter((item) => item.hint !== undefined)
  }, [tools, search])

  if (tool) {
    return (
      <OrderForm
        key={tool.function.name}
        tool={tool}
        sending={sending}
        onBack={() => setSelected(null)}
        onSend={(args, rationale) => onSend(tool.function.name, args, rationale)}
      />
    )
  }

  return (
    <div>
      <div className="relative">
        <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
        <input
          type="search"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search tests, e.g. EEG, ammonia, biopsy"
          aria-label="Search the test catalogue"
          className="w-full bg-background border border-input rounded-md h-10 pl-9 pr-3 text-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring"
        />
      </div>
      <ul className="mt-3 divide-y divide-border/70 border-y border-border/70" data-testid="tool-list">
        {shown.map(({ tool: t, hint }) => (
          <li key={t.function.name}>
            <button
              type="button"
              onClick={() => {
                onToolOpened(t.function.name)
                setSelected(t.function.name)
              }}
              className="group w-full text-left py-3 px-1.5 flex items-start gap-2 hover:bg-secondary/50 rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            >
              <span className="min-w-0 flex-1">
                <span className="block font-medium text-[15px] group-hover:text-primary">
                  {humanize(t.function.name)}
                  <span className="ml-2 font-mono text-[11px] font-normal text-muted-foreground">{t.function.name}</span>
                </span>
                <span className="block mt-0.5 text-[13px] leading-relaxed text-muted-foreground">{t.function.description}</span>
                {hint && <span className="block mt-1 text-[13px] text-primary">{hint}</span>}
              </span>
              <ChevronRight className="w-4 h-4 mt-1 text-muted-foreground group-hover:text-primary flex-shrink-0" />
            </button>
          </li>
        ))}
        {shown.length === 0 && (
          <li className="py-6 text-sm text-muted-foreground text-center">
            Nothing in the catalogue matches “{search}”. Only the listed tests can be ordered.
          </li>
        )}
      </ul>
    </div>
  )
}

function OrderForm({
  tool,
  sending,
  onBack,
  onSend,
}: {
  tool: ToolDefinition
  sending: boolean
  onBack: () => void
  onSend: (args: Record<string, JsonValue>, rationale: string) => void
}) {
  const [values, setValues] = useState<FormValues>({})
  const [rationale, setRationale] = useState("")
  const missing = missingRequired(tool, values)
  const ready = missing.length === 0 && rationale.trim().length > 0
  const context = typeof values.clinical_context === "string" ? values.clinical_context.trim() : ""

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault()
        if (ready && !sending) onSend(filledArguments(values), rationale.trim())
      }}
    >
      <button
        type="button"
        onClick={onBack}
        className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground -ml-1 px-1 py-0.5 rounded"
      >
        <ArrowLeft className="w-4 h-4" />
        All tests
      </button>
      <h3 className="mt-2 text-lg font-semibold tracking-tight">
        {humanize(tool.function.name)}
        <span className="ml-2 font-mono text-xs font-normal text-muted-foreground">{tool.function.name}</span>
      </h3>
      <p className="mt-1 text-sm leading-relaxed text-muted-foreground">{tool.function.description}</p>

      <div className="mt-5">
        <SchemaForm tool={tool} values={values} onChange={setValues} />
      </div>

      <div className="mt-6 pt-5 border-t border-border">
        <div className="flex items-baseline justify-between gap-2">
          <label htmlFor="rationale" className="text-sm font-medium">
            Why this test now?<span className="text-rose-600 dark:text-rose-400 ml-0.5" aria-hidden>*</span>
          </label>
          {context && !rationale && (
            <button type="button" onClick={() => setRationale(context)} className="text-xs text-primary hover:underline">
              Same as clinical context
            </button>
          )}
        </div>
        <p className="mt-1 mb-2 text-[13px] text-muted-foreground">
          A line is enough. It is kept for the study and is not part of the order.
        </p>
        <textarea
          id="rationale"
          rows={2}
          value={rationale}
          onChange={(e) => setRationale(e.target.value)}
          className="w-full bg-background border border-input rounded-md px-3 py-2 text-sm leading-relaxed resize-y focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring"
        />
      </div>

      <div className="mt-4 flex items-center justify-between gap-3">
        <p className={cn("text-[13px]", ready ? "text-muted-foreground" : "text-amber-700 dark:text-amber-300")} role="status">
          {missing.length > 0
            ? `Still needed: ${missing.map((m) => humanize(m).toLowerCase()).join(", ")}`
            : !rationale.trim()
              ? "Still needed: your reason"
              : "Once placed, an order cannot be undone."}
        </p>
        <Button type="submit" disabled={!ready || sending} className="flex-shrink-0">
          {sending ? <Loader2 className="w-4 h-4 animate-spin" /> : "Place order"}
        </Button>
      </div>
    </form>
  )
}
