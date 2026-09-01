# NeuroBench documentation

Start with the repository `README.md` and the executable contract in
`agent-platform/docs/clinical-policy-harness.md`.

## Current references

| Page | Purpose |
|---|---|
| `architecture.md` | Repository-level typed policy architecture |
| `agent-platform/docs/clinical-policy-harness.md` | Runtime, profiles, reward, review and experiments |
| `agent-platform/docs/models.md` | Fixed model panel and vLLM serving |
| `agent-platform/docs/web-api.md` | Runs, episodes and model endpoints |
| `agent-platform/docs/tools.md` | Clinical tool contracts |
| `agent-platform/docs/hospital-rules.md` | Hospital policy configuration |
| `agent-platform/docs/patient-data.md` | Patient and case data handling |
| `benchmark/tool-contract.md` | Tool vocabulary and cost invariants |

## Authoritative sources

- Case schema: `packages/neuroagent-schemas/`
- Dataset key and loader: `agent-platform/src/neuroagent/datasets.py`
- Profiles: `agent-platform/config/profiles/`
- Harness: `agent-platform/src/neuroagent/harness/`
- Reward: `agent-platform/src/neuroagent/evaluation/policy_reward.py`
- Costs and closed vocabularies: `agent-platform/config/tools/costs.yaml`
- Case validator: `dataset-generation/src/neurobench_gen/validate_case.py`
- Policy authoring: `dataset-generation/POLICY_AUTHORING_GUIDE.md`

Historical audits and superseded plans live under `docs/archive/` and are provenance only.
