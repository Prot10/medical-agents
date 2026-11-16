"""Per-case log of the November 2026 round: data/review/round-2026-11/logs/{CASE_ID}.md.

Fixed headings (resume markers): '## Class changes', '## Reviewer notes', '## Own findings',
'## Changes', '## Verification'. `append(case_id, heading, text)` adds text under a heading,
creating the log and the heading if needed.
"""
from __future__ import annotations
from pathlib import Path
import sys
LOGS = Path(__file__).resolve().parents[1] / "logs"
HEADINGS = ["## Class changes", "## Reviewer notes", "## Own findings", "## Changes", "## Verification"]

def append(case_id: str, heading: str, text: str) -> None:
    assert heading in HEADINGS, heading
    LOGS.mkdir(parents=True, exist_ok=True)
    p = LOGS / f"{case_id}.md"
    body = p.read_text() if p.exists() else f"# {case_id}\n"
    if heading not in body:
        body = body.rstrip("\n") + f"\n\n{heading}\n"
    # insert at the end of the heading's section
    start = body.index(heading) + len(heading)
    nxt = min([body.index(h, start) for h in HEADINGS if h in body[start:]] or [len(body)])
    section = body[start:nxt].rstrip("\n")
    body = body[:start] + section + "\n" + text.rstrip("\n") + "\n" + ("\n" + body[nxt:] if nxt < len(body) else "")
    p.write_text(body)

if __name__ == "__main__":
    append(sys.argv[1], sys.argv[2], sys.stdin.read())
