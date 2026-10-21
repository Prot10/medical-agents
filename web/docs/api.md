# API used by the dashboard

The endpoint contract lives in [agent-platform/docs/web-api.md](../../agent-platform/docs/web-api.md); this page maps it to `src/api/client.ts`. All paths are under `/api/v1`, which Vite proxies to port 8888 in dev.

| Client call | Endpoint | Used by |
|---|---|---|
| `api.getCases()` | `GET /cases` | `CaseBrowser`, dataset views |
| `api.getCase(id)` | `GET /cases/{case_id}` | `PatientViewer`, `GroundTruthPanel` |
| `api.getProfiles()` | `GET /profiles` | `Sidebar` picker, `ProfilesPanel` |
| `api.getModels()` | `GET /models` | model status of the selected profile |
| `api.loadModel(key)` | `POST /models/{key}/load` (SSE) | `Sidebar` Load button, `ModelLoadingToast` |
| `api.unloadModel()` | `POST /models/unload` | `Sidebar` Stop button |
| `streamRun(caseId, profileId, onFrame, signal)` | `POST /runs/stream` (SSE) | `useAgentRun`, the live timeline |
| `api.getEpisodes()` | `GET /episodes` | `EpisodeBrowser` |
| `api.getEpisode(id)` | `GET /episodes/{id}` | replay |
| `api.getEpisodeReward(id)` | `GET /episodes/{id}/reward` | `ScorePanel` after a replay |
| `api.deleteEpisode(id)` | `DELETE /episodes/{id}` | `EpisodeBrowser` |
| `api.getHospitals()` / `getHospitalRules(id)` | `GET /hospitals`, `GET /hospitals/{id}/rules` | Rules section |
| `createPathway` / `updatePathway` / `deletePathway` | `POST/PUT/DELETE /hospitals/{id}/rules[/{index}]` | `PathwayEditorPanel` |

## Run stream

`POST /runs/stream` takes `{"case_id", "profile_id", "persist": true}`. Each `data:` frame is one `EpisodeEvent` (see `src/api/types.ts`), in the order the episode store records it:

| Event | Timeline item |
|---|---|
| `run.started` | header card: profile, model, loop |
| `model.requested` | token and latency totals |
| `action.proposed` | tool call card (or the assessment, if it is `submit_assessment`) |
| `action.rejected` | "invalid output, retried with a correction" card |
| `observation.received` | the result inside the matching tool card, with its cost |
| `plugin.event` (`react.rationale`) | rationale block (ReAct profiles only) |
| `assessment.submitted` | `AssessmentPanel` |
| `run.completed` / `run.failed` | final status |

The stream ends with `stream.result` (`episode_id`, `reward`, `policy_review_status`) or `stream.error` (`message`). Aborting the fetch closes the connection, and the server cancels the run at its next event.

The reward is computed with `require_approved=False`. While a case policy is `draft`, `ScorePanel` labels it as an engineering score that is not reportable.
