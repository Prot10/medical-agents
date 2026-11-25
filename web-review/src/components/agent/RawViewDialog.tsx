import * as Dialog from "@radix-ui/react-dialog"
import { X } from "lucide-react"
import { useState } from "react"

import type { CaseState } from "@/api/agentTypes"
import { cn } from "@/lib/utils"

/** The request the model server would receive at this step, verbatim: every message and the
 * tool list. What the page shows is this same content, laid out for reading. */
export function RawViewDialog({
  raw,
  open,
  onOpenChange,
}: {
  raw: NonNullable<CaseState["raw"]>
  open: boolean
  onOpenChange: (open: boolean) => void
}) {
  const [tab, setTab] = useState<"messages" | "tools">("messages")
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-40 bg-slate-950/50" />
        <Dialog.Content className="fixed z-50 inset-3 sm:inset-8 lg:inset-x-[12%] bg-card border border-border rounded-2xl shadow-2xl flex flex-col overflow-hidden focus:outline-none">
          <div className="flex items-start justify-between gap-4 px-5 pt-4 pb-3 border-b border-border">
            <div>
              <Dialog.Title className="text-base font-semibold">Raw view</Dialog.Title>
              <Dialog.Description className="text-sm text-muted-foreground mt-0.5">
                Exactly what the agent receives at this step: the messages and the tool list, unformatted.
              </Dialog.Description>
            </div>
            <Dialog.Close className="p-1.5 rounded-md text-muted-foreground hover:bg-secondary/70" aria-label="Close">
              <X className="w-4 h-4" />
            </Dialog.Close>
          </div>
          <div className="flex gap-1 px-5 pt-3">
            {(["messages", "tools"] as const).map((id) => (
              <button
                key={id}
                type="button"
                onClick={() => setTab(id)}
                className={cn(
                  "px-3 py-1.5 rounded-md text-sm font-medium",
                  tab === id ? "bg-primary/10 text-primary" : "text-muted-foreground hover:bg-secondary/60",
                )}
              >
                {id === "messages" ? `Messages (${raw.messages.length})` : `Tool list (${raw.tools.length})`}
              </button>
            ))}
          </div>
          <div className="flex-1 overflow-auto px-5 py-4 space-y-3" data-testid="raw-view">
            {tab === "messages" ? (
              raw.messages.map((message, i) => (
                <div key={i} className="rounded-lg border border-border overflow-hidden">
                  <div className="px-3 py-1.5 text-xs font-medium bg-secondary/60 text-muted-foreground font-mono">
                    {message.role}
                    {message.tool_call_id ? ` (${message.tool_call_id})` : ""}
                  </div>
                  {message.content != null && (
                    <pre className="px-3 py-2.5 text-xs leading-relaxed font-mono whitespace-pre-wrap break-words">{message.content}</pre>
                  )}
                  {message.tool_calls && (
                    <pre className="px-3 py-2.5 text-xs leading-relaxed font-mono whitespace-pre-wrap break-words border-t border-border/60">
                      {JSON.stringify(message.tool_calls, null, 2)}
                    </pre>
                  )}
                </div>
              ))
            ) : (
              <pre className="text-xs leading-relaxed font-mono whitespace-pre-wrap break-words">
                {JSON.stringify(raw.tools, null, 2)}
              </pre>
            )}
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  )
}
