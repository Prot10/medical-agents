// Presentational helpers for agent mode. They only restyle agent-facing text; the content is
// never changed (the raw view shows the same text verbatim).

/** "interpret_labs" → "Interpret labs". */
export function humanize(name: string): string {
  const text = name.replace(/_/g, " ").trim()
  return text.charAt(0).toUpperCase() + text.slice(1)
}

export interface PresentationBlock {
  label: string
  /** Text after the label on the same line, plus any continuation lines. */
  text: string
  /** Indented "Label: value" lines under the block (the examination). */
  items: Array<{ label: string; text: string }>
}

const LABEL = /^([A-Z][A-Za-z0-9 /-]{1,48}):\s?(.*)$/

/** Split the presentation the agent receives into its labelled lines, in order. */
export function parsePresentation(text: string): PresentationBlock[] {
  const blocks: PresentationBlock[] = []
  for (const line of text.split("\n")) {
    const current = blocks[blocks.length - 1]
    if (line.startsWith("  ") && current) {
      const match = LABEL.exec(line.trim())
      if (match) current.items.push({ label: match[1], text: match[2] })
      else current.items.push({ label: "", text: line.trim() })
      continue
    }
    const match = LABEL.exec(line)
    if (match) blocks.push({ label: match[1], text: match[2], items: [] })
    else if (current) current.text += (current.text ? "\n" : "") + line
    else blocks.push({ label: "", text: line, items: [] })
  }
  return blocks
}

export function formatClock(iso: string): string {
  return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
}
