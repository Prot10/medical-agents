# Review app: agent mode

A section of the dataset review app (`review_api` on 8889, `web-review`) in which a physician
works a case exactly as the agent does, so the two work-ups can be compared. The physician gets
the initial presentation, orders one tool at a time from the agent's catalogue with a short
reason, reads each result as the agent would, and submits the agent's structured assessment.

## Same information, same constraints

Nothing is re-implemented. Each step replays `ClinicalPolicyLoop` with `NativeToolModelAdapter`
and a client (`services/agent_mode/engine.py::PhysicianClient`) that answers each chat request
with the next action the physician already sent, and stops the loop at the first request nothing
answers. That request is what the physician is shown.

| What the physician sees | Where it comes from |
|---|---|
| Instructions | `POLICY_SYSTEM_PROMPT`, the system message of the request |
| Presentation | `format_patient_info(case)`, the user message of the request |
| Catalogue and order form | `NeuroBenchEnvironment.tool_definitions()` + `SUBMIT_TOOL`, the request's tool list; the form is generated from each tool's JSON schema |
| Result of an order | `observation_payload(event)`, the content of the `tool` message; served by `BaseTool.execute` and the MockServer |
| Rejected order (schema) | the same error observation the agent gets; the turn is spent |
| Rejected action (no such tool, a tool on the final turn, an invalid assessment) | `ActionDecodeError` of the adapter, with the loop's one-off correction text; counted against the profile's `max_invalid_actions`, and the episode fails when it is spent |
| Final-turn message | the adapter's `_final_turn` instruction, on the last turn only |

Limits come from the checked policy profile named in `agent_mode_sets.yaml` (`policy-qwen3.5-9b`:
12 turns, USD 15,000, 2 invalid actions). The agent is never told its turn budget, so the page
does not show it either (`show_step_budget: false`). The agent sees no cost except the prices
written in the tool descriptions, and so does the physician. The **Raw view** button shows the
request verbatim (messages and tool list).

A case is addressed by its number in the set, never by its id (which names the condition), and
nothing a physician's code can fetch contains a case id, a condition, a policy or a reward. After
the assessment the case is locked and no feedback is given.

`tests/test_review_agent_mode.py` holds the contract; the central test sends the same actions
through the app and through the policy loop with a scripted model and compares every request
and the two episodes.

## Codes and sections

`agent-platform/config/review/reviewer_codes.yaml` (gitignored, hot-reloads). A code with
`sections` is an agent-mode code: it opens those sections and is refused (403) on every other
route of the review app. A code without `sections` behaves as before and is refused on the
agent-mode routes.

```yaml
reviewers:
  - code: NB-XXXX-XXXX-XXXX
    name: Dr Example
    role: reviewer                         # an agent-mode code cannot be an admin
    id: phys-01                            # public id used in records and as model id `physician:phys-01`
    sections: [agent_synthetic]            # or [agent_synthetic, agent_mimic]
    linked_review_codes: [NB-YYYY-YYYY-YYYY]   # the same person's dataset-review code(s)
```

- `id` is optional (default: `r-` + a hash of the code). Set it: records are filed under it, and
  it stays stable if the code is rotated.
- `linked_review_codes`: synthetic cases that person opened in the dataset review (any version
  or review set, read from `data/review/annotations/`) are left out of their list.
- Sections: **Synthetic cases** (`agent_synthetic`) and **MIMIC cases** (`agent_mimic`, give it
  only to physicians credentialed on PhysioNet).

## Case sets

`agent-platform/config/review/agent_mode_sets.yaml` declares both sections, with the drawing rule
and seed. Cases are served in the listed order, one at a time.

- **Synthetic**: `agent-synthetic-2026-11`, 8 cases: 2 per condition from the test split (which
  holds out 4 conditions), seed 20261125, frozen in `data/review/sets/agent-synthetic-2026-11/`.
  A new draw is a new set id: `agent-platform/scripts/review/draw_agent_mode_set.py`.
- **MIMIC**: every case in the configured folder, ids sorted then shuffled with the seed in the
  file (or the order of `REVIEW_AGENT_MIMIC_CASE_LIST`, a text file of case ids).

## Enabling the MIMIC section

It exists only on a server whose environment sets both variables; otherwise no route serves it
and the UI does not show it. The PhysioNet DUA keeps MIMIC off the public review server.

```bash
export REVIEW_AGENT_MIMIC_CASES_DIR=/path/to/final-100   # case JSON files, or a folder holding cases/
export REVIEW_AGENT_MIMIC_LOG_DIR=/path/outside/the/repo/agent-mode-logs
uv run uvicorn neuroagent.review_api.app:app --host 127.0.0.1 --port 8889
```

Both paths must be outside the repository (start-up refuses otherwise). Nothing from the cases is
copied anywhere; the records are written under the log directory only; a malformed case file is
reported by name and field, never by content.

## Storage

```
<records>/<section>/<set id>/<reviewer id>/<case id>.json           the record, replaced atomically
<records>/<section>/<set id>/<reviewer id>/<case id>.events.jsonl   append-only log
```

`<records>` is `data/review/agent-mode/` (gitignored; `REVIEW_AGENT_MODE_DIR` overrides it) for
the synthetic section and `REVIEW_AGENT_MIMIC_LOG_DIR` for MIMIC. The record
(`schemas/agent_mode.py::AgentRecord`) holds:

- `episode`: a `ClinicalEpisode` with the benchmark's event types (`run.started`,
  `model.requested`, `action.proposed`, `action.rejected`, `observation.received`,
  `assessment.submitted`, `run.completed` / `run.failed`), profile `policy-physician`, model
  `physician:<reviewer id>`. `latency_seconds` of an action is the physician's time on that step.
- `steps`: per action sent, the rationale, the outcome, server timestamps (`shown_at`,
  `sent_at`), and light client telemetry (seconds the page was visible, tool cards opened,
  catalogue filter terms, raw view opened, resumed after a reload). Time on the presentation is
  the first step's time.
- `diagnostic_reasoning`: the physician-only reasoning for the diagnosis.
- `provenance`: case file sha256 and case/policy content hashes, set id and hash, hashes of the
  system prompt, presentation and catalogue, profile limits, app version and git commit, hashes
  of `costs.yaml` and the fallback library.

The log keeps every request as received and every time the case was opened.

## Admin and export

The Admin tab has an **Agent mode** view (admin role): per-code progress and, per finished
episode, the policy reward and its components from `ClinicalPolicyReward`, through the same
`episode_row` the benchmark uses. A draft policy is scored with `require_approved=False` and
labelled as not reportable.

```bash
uv run python agent-platform/scripts/review/export_physician_episodes.py \
  --section synthetic --output outputs/physicians/synthetic --allow-draft-policies
```

writes one benchmark run folder per physician (`episodes/<case>.json`, `rewards.jsonl`,
`summary.json`, `manifest.json`) plus `physician.jsonl` with the physician-only data. For MIMIC,
run it on the host that holds the records, with the two variables set and an `--output` outside
the repository.
