# Policy harness API

Run the service with:

```bash
uv run uvicorn neuroagent.api.app:app --host 127.0.0.1 --port 8888
```

The API serves JSON only.

| Endpoint | Purpose |
|---|---|
| `GET /api/v1/profiles` | list the eight checked experiment profiles |
| `POST /api/v1/runs` | execute one case with a checked profile |
| `GET /api/v1/models` | list the fixed three-model panel and readiness |
| `POST /api/v1/models/{key}/load` | start one registered vLLM model |
| `POST /api/v1/models/unload` | stop the vLLM process started by this API |
| `GET /api/v1/cases` | browse cases |
| `GET /api/v1/hospitals` | inspect hospital rules |
| `GET /api/v1/episodes` | inspect persisted typed episodes |

Example run body:

```json
{
  "case_id": "FEPI-TEMP-M01",
  "profile_id": "policy-qwen3.5-9b",
  "persist": true
}
```

Unknown profiles and model keys are rejected. The service does not accept arbitrary remote models or credentials.
