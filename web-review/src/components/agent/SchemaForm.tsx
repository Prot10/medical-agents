import { Check, Search, X } from "lucide-react"
import { useMemo, useState } from "react"

import type { JsonValue, ParamSchema, ToolDefinition } from "@/api/agentTypes"
import { humanize } from "@/lib/agentText"
import { cn } from "@/lib/utils"

export type FormValues = Record<string, JsonValue | undefined>

const inputClass =
  "w-full bg-background border border-input rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-ring transition"

/** The arguments to send: only what was filled in, as an agent omits what it does not set. */
export function filledArguments(values: FormValues): Record<string, JsonValue> {
  const out: Record<string, JsonValue> = {}
  for (const [key, value] of Object.entries(values)) {
    if (value === undefined || value === "" || (Array.isArray(value) && value.length === 0)) continue
    out[key] = typeof value === "string" ? value.trim() : value
  }
  return out
}

export function missingRequired(tool: ToolDefinition, values: FormValues): string[] {
  const filled = filledArguments(values)
  return (tool.function.parameters.required ?? []).filter((key) => !(key in filled) || filled[key] === "")
}

/** One field per parameter of the tool's JSON schema, in the schema's order, with the schema's
 * own descriptions: enums as choices, booleans as yes/no, lists as chips. */
export function SchemaForm({
  tool,
  values,
  onChange,
}: {
  tool: ToolDefinition
  values: FormValues
  onChange: (values: FormValues) => void
}) {
  const { properties, required = [] } = tool.function.parameters
  return (
    <div className="space-y-5">
      {Object.entries(properties).map(([key, schema]) => (
        <Field
          key={key}
          name={key}
          schema={schema}
          required={required.includes(key)}
          value={values[key]}
          onChange={(value) => onChange({ ...values, [key]: value })}
        />
      ))}
    </div>
  )
}

function Field({
  name,
  schema,
  required,
  value,
  onChange,
}: {
  name: string
  schema: ParamSchema
  required: boolean
  value: JsonValue | undefined
  onChange: (value: JsonValue | undefined) => void
}) {
  const id = `param-${name}`
  return (
    <div data-param={name}>
      <div className="flex items-baseline justify-between gap-2">
        <label htmlFor={id} className="text-sm font-medium">
          {humanize(name)}
          {required && <span className="text-rose-600 dark:text-rose-400 ml-0.5" aria-hidden>*</span>}
        </label>
        <span className="text-xs text-muted-foreground">
          {required ? "required" : "optional"}
          {schema.default !== undefined && schema.default !== null && (
            <> · default {typeof schema.default === "boolean" ? (schema.default ? "yes" : "no") : String(schema.default)}</>
          )}
        </span>
      </div>
      {schema.description && (
        <p className="mt-1 mb-2 text-[13px] leading-relaxed text-muted-foreground">{schema.description}</p>
      )}
      <Control id={id} schema={schema} value={value} onChange={onChange} long={name === "clinical_context"} />
    </div>
  )
}

function Control({
  id,
  schema,
  value,
  onChange,
  long,
}: {
  id: string
  schema: ParamSchema
  value: JsonValue | undefined
  onChange: (value: JsonValue | undefined) => void
  long: boolean
}) {
  if (schema.type === "boolean") {
    return (
      <Choices
        options={["yes", "no"]}
        selected={value === undefined ? [] : [value ? "yes" : "no"]}
        onToggle={(option) => {
          const next = option === "yes"
          onChange(value === next ? undefined : next)
        }}
      />
    )
  }
  if (schema.type === "integer" || schema.type === "number") {
    return (
      <input
        id={id}
        type="number"
        inputMode="numeric"
        step={schema.type === "integer" ? 1 : "any"}
        value={typeof value === "number" ? value : ""}
        onChange={(e) => {
          const parsed = schema.type === "integer" ? parseInt(e.target.value, 10) : parseFloat(e.target.value)
          onChange(Number.isFinite(parsed) ? parsed : undefined)
        }}
        className={cn(inputClass, "max-w-[9rem]")}
      />
    )
  }
  if (schema.type === "array") {
    const selected = Array.isArray(value) ? (value as string[]) : []
    if (schema.items?.enum) {
      return <MultiEnum id={id} options={schema.items.enum} selected={selected} onChange={(next) => onChange(next)} />
    }
    return <FreeList id={id} items={selected} onChange={(next) => onChange(next)} />
  }
  if (schema.enum) {
    if (schema.enum.length <= 8) {
      return (
        <Choices
          options={schema.enum}
          selected={typeof value === "string" ? [value] : []}
          onToggle={(option) => onChange(value === option ? undefined : option)}
        />
      )
    }
    return (
      <select
        id={id}
        value={typeof value === "string" ? value : ""}
        onChange={(e) => onChange(e.target.value || undefined)}
        className={cn(inputClass, "h-10")}
      >
        <option value="">Choose…</option>
        {schema.enum.map((option) => (
          <option key={option} value={option}>
            {option}
          </option>
        ))}
      </select>
    )
  }
  if (long) {
    return (
      <textarea
        id={id}
        rows={2}
        value={typeof value === "string" ? value : ""}
        onChange={(e) => onChange(e.target.value)}
        className={cn(inputClass, "resize-y leading-relaxed")}
      />
    )
  }
  return (
    <input
      id={id}
      type="text"
      value={typeof value === "string" ? value : ""}
      onChange={(e) => onChange(e.target.value)}
      className={inputClass}
    />
  )
}

function Choices({
  options,
  selected,
  onToggle,
}: {
  options: string[]
  selected: string[]
  onToggle: (option: string) => void
}) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {options.map((option) => {
        const on = selected.includes(option)
        return (
          <button
            key={option}
            type="button"
            aria-pressed={on}
            onClick={() => onToggle(option)}
            className={cn(
              "px-3 py-1.5 rounded-md border text-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring",
              on
                ? "bg-primary text-primary-foreground border-primary"
                : "bg-background border-input text-foreground hover:border-primary/60",
            )}
          >
            {option}
          </button>
        )
      })}
    </div>
  )
}

/** Many values from a long vocabulary: a filter, a checklist, and the chosen values on top. */
function MultiEnum({
  id,
  options,
  selected,
  onChange,
}: {
  id: string
  options: string[]
  selected: string[]
  onChange: (next: string[]) => void
}) {
  const [filter, setFilter] = useState("")
  const shown = useMemo(() => {
    const term = filter.trim().toLowerCase().replace(/[\s-]+/g, "_")
    return term ? options.filter((o) => o.toLowerCase().replace(/[\s-]+/g, "_").includes(term)) : options
  }, [filter, options])
  const toggle = (option: string) =>
    onChange(selected.includes(option) ? selected.filter((o) => o !== option) : [...selected, option])

  return (
    <div className="rounded-md border border-input bg-background">
      {selected.length > 0 && (
        <div className="flex flex-wrap gap-1.5 p-2 border-b border-border/70">
          {selected.map((option) => (
            <button
              key={option}
              type="button"
              onClick={() => toggle(option)}
              className="inline-flex items-center gap-1 pl-2.5 pr-1.5 py-1 rounded-md bg-primary/10 text-primary text-[13px] font-medium hover:bg-primary/15"
              aria-label={`Remove ${option}`}
            >
              {option}
              <X className="w-3.5 h-3.5" />
            </button>
          ))}
        </div>
      )}
      {options.length > 10 && (
        <div className="relative border-b border-border/70">
          <Search className="w-4 h-4 absolute left-2.5 top-1/2 -translate-y-1/2 text-muted-foreground" />
          <input
            id={id}
            type="search"
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            placeholder={`Filter ${options.length} values`}
            className="w-full bg-transparent pl-8 pr-3 py-2 text-sm focus:outline-none"
          />
        </div>
      )}
      <ul className="max-h-52 overflow-y-auto p-1 grid grid-cols-1 sm:grid-cols-2 gap-x-1">
        {shown.map((option) => {
          const on = selected.includes(option)
          return (
            <li key={option}>
              <button
                type="button"
                role="checkbox"
                aria-checked={on}
                onClick={() => toggle(option)}
                className="w-full flex items-center gap-2 px-2 py-1.5 rounded text-left text-[13px] hover:bg-secondary/70"
              >
                <span
                  className={cn(
                    "w-4 h-4 rounded border flex items-center justify-center flex-shrink-0",
                    on ? "bg-primary border-primary text-primary-foreground" : "border-input",
                  )}
                >
                  {on && <Check className="w-3 h-3" />}
                </span>
                <span className="break-all">{option}</span>
              </button>
            </li>
          )
        })}
        {shown.length === 0 && <li className="px-2 py-2 text-[13px] text-muted-foreground">No value matches.</li>}
      </ul>
    </div>
  )
}

/** A list of free-text entries: type one, press Enter. */
export function FreeList({
  id,
  items,
  onChange,
  placeholder = "Type and press Enter",
}: {
  id?: string
  items: string[]
  onChange: (next: string[]) => void
  placeholder?: string
}) {
  const [draft, setDraft] = useState("")
  const add = () => {
    const clean = draft.trim()
    if (clean && !items.includes(clean)) onChange([...items, clean])
    setDraft("")
  }
  return (
    <div>
      {items.length > 0 && (
        <ul className="mb-2 space-y-1">
          {items.map((item) => (
            <li key={item} className="flex items-start justify-between gap-2 rounded-md bg-secondary/60 px-2.5 py-1.5 text-sm">
              <span className="break-words min-w-0">{item}</span>
              <button
                type="button"
                onClick={() => onChange(items.filter((i) => i !== item))}
                className="text-muted-foreground hover:text-foreground mt-0.5"
                aria-label={`Remove ${item}`}
              >
                <X className="w-3.5 h-3.5" />
              </button>
            </li>
          ))}
        </ul>
      )}
      <input
        id={id}
        type="text"
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            e.preventDefault()
            add()
          }
        }}
        onBlur={add}
        placeholder={placeholder}
        className={inputClass}
      />
    </div>
  )
}
