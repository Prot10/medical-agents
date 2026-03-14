import { ExternalLink } from "lucide-react"

interface LitResult {
  title: string
  source: string
  summary: string
}

export function LiteratureResults({ data }: { data: Record<string, unknown> }) {
  const query = data.query as string | undefined
  const results = (data.results ?? []) as LitResult[]
  const summary = data.summary as string | undefined

  return (
    <div className="space-y-2">
      {query && (
        <div className="text-[10px] text-muted-foreground">
          Query: <span className="font-mono italic">"{query}"</span>
        </div>
      )}

      {results.map((r, i) => (
        <div key={i} className="rounded-md border border-border/50 p-2">
          <div className="flex items-start gap-1.5">
            <ExternalLink className="h-3 w-3 text-amber-500 dark:text-amber-400 mt-0.5 shrink-0" />
            <div>
              <div className="text-[11px] font-medium leading-tight">{r.title}</div>
              <div className="text-[9px] text-muted-foreground mt-0.5">{r.source}</div>
            </div>
          </div>
          <p className="text-[10px] text-muted-foreground mt-1 leading-relaxed">
            {r.summary}
          </p>
        </div>
      ))}

      {summary && (
        <div className="text-[11px] text-muted-foreground leading-relaxed border-l-2 border-amber-500/30 pl-2">
          {summary}
        </div>
      )}
    </div>
  )
}
