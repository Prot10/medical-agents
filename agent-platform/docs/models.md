# Fixed model panel

The benchmark compares exactly three open models below 10B parameters:

| Key | Model | Adapter |
|---|---|---|
| `qwen3.5-9b` | `Qwen/Qwen3.5-9B` | native structured tools |
| `gemma-4-e4b` | `google/gemma-4-E4B-it` | native structured tools |
| `medgemma-1.5-4b` | `google/medgemma-1.5-4b-it` | strict JSON action |

Qwen and Gemma cover the main policy, direct and ReAct-prompt conditions. MedGemma covers policy and direct conditions only. This keeps the comparison focused while retaining a medical-domain model without native tool calling.

Serve one model:

```bash
agent-platform/scripts/runtime/serve_model.sh qwen3.5-9b
```

The registry, profiles, API and serve script use the same keys. Unknown models are rejected.
