# Policy harness API

Run the service with:

```bash
uv run uvicorn neuroagent.api.app:app --host 127.0.0.1 --port 8888
```

The API serves JSON and one Server-Sent Events stream. When `web/dist` exists (after `npm run build` in `web/`), the dashboard is served at `/`.

| Endpoint | Purpose |
|---|---|
| `GET /api/v1/profiles` | list the nine checked experiment profiles |
| `POST /api/v1/runs` | execute one case with a checked profile |
| `POST /api/v1/runs/stream` | the same run, streaming each episode event as SSE |
| `GET /api/v1/models` | list the fixed three-model panel and readiness |
| `POST /api/v1/models/{key}/load` | start one registered vLLM model |
| `POST /api/v1/models/unload` | stop the vLLM process started by this API |
| `GET /api/v1/cases` | browse cases |
| `GET /api/v1/hospitals` | inspect hospital rules |
| `GET /api/v1/episodes` | list persisted typed episodes |
| `GET /api/v1/episodes/{id}` | load one episode |
| `GET /api/v1/episodes/{id}/reward` | engineering reward of a saved episode against its case policy |

Example run body:

```json
{
  "case_id": "FEPI-TEMP-M01",
  "profile_id": "policy-qwen3.5-9b",
  "persist": true
}
```

`POST /api/v1/runs/stream` takes the same body. Each `data:` frame is one episode event
(`run.started`, `model.requested`, `action.proposed`, `action.rejected`, `observation.received`,
`plugin.event`, `assessment.submitted`, `run.completed` or `run.failed`) in the order the episode
store records it, then a final `{"type": "stream.result", "episode_id", "reward",
"policy_review_status"}`. A failure before the loop starts ends the stream with
`{"type": "stream.error", "message"}`. Closing the connection cancels the run at its next event.
The reward in `stream.result` and in `/episodes/{id}/reward` is computed with
`require_approved=False`: on a draft policy it is an engineering check, not a reportable score.

Unknown profiles and model keys are rejected. The service does not accept arbitrary remote models or credentials.
