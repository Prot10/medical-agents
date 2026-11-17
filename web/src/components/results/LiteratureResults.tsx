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
        <div className="text-sm text-muted-foreground">
          Query: <span className="font-mono italic">"{query}"</span>
        </div>
      )}

      {results.map((r, i) => (
        <div key={i} className="rounded-lg border border-border/50 p-3">
          <div className="flex items-start gap-2">
            <ExternalLink className="h-3.5 w-3.5 text-amber-500 dark:text-amber-400 mt-0.5 shrink-0" />
            <div>
              <div className="text-base font-medium leading-snug">{r.title}</div>
              <div className="text-sm text-muted-foreground mt-0.5">{r.source}</div>
            </div>
          </div>
          <p className="text-base text-muted-foreground mt-2 leading-relaxed">
            {r.summary}
          </p>
        </div>
      ))}

      {summary && (
        <div className="text-base text-muted-foreground leading-relaxed border-l-2 border-amber-500/30 pl-3">
          {summary}
        </div>
      )}
    </div>
  )
}
