---
name: run-review-app
description: Build, run, and drive the NeuroBench dataset review app (review_api backend + web-review frontend). Use when asked to start the review app, run its backend/frontend dev servers, screenshot the reviewer UI or admin dashboard, seed reviewer annotation/heartbeat data for testing, or verify a review-app change end-to-end in a browser.
---

The review app is two halves in this repo: the FastAPI backend at
`agent-platform/src/neuroagent/review_api/` and the Vite/React frontend at
`web-review/`. Drive it via `.claude/skills/run-review-app/driver.py`, a
Playwright script run through `uvx --from playwright python`. There is no
`chromium-cli` in this environment — this driver replaces it.

All paths below are relative to the repo root (`medical-agents/`).

## Prerequisites

Chromium for Playwright, installed once (downloads ~260MB, cached after):

```bash
uvx --from playwright playwright install chromium --with-deps
```

Everything else (`uv`, `npm`) is already required by the rest of the repo.

## Setup

```bash
uv sync --all-packages
cd web-review && npm install
```

No env vars are required for local runs — the frontend's Vite proxy
defaults `REVIEW_API_PROXY_TARGET` to `http://127.0.0.1:8889`, matching the
backend's default port below.

## Build

No build step needed to run the dev servers (see below). Only needed to
produce the static bundle the Hostinger deploy ships:

```bash
cd web-review && npm run build   # → web-review/dist/
```

## Run (agent path)

1. Start the backend (from repo root):

```bash
uv run uvicorn neuroagent.review_api.app:app --app-dir agent-platform/src --host 127.0.0.1 --port 8889 &
until curl -sf -o /dev/null http://127.0.0.1:8889/api/v1/datasets -H "X-Reviewer-Code: NB-KSC3-TWUA-QDTM"; do sleep 1; done
```

2. Start the frontend (from `web-review/`):

```bash
cd web-review && npm run dev &
until curl -sf -o /dev/null http://localhost:5174; do sleep 1; done
```

3. Drive it and screenshot:

```bash
uvx --from playwright python .claude/skills/run-review-app/driver.py \
  --code <reviewer-code-from-reviewer_codes.yaml> \
  --click "Admin" --click "Reviewer progress" \
  --out /tmp/review-app.png
```

`driver.py` logs in with the given code (typed into the login input,
Enter submitted), clicks each `--click` label in order (use this to reach
a specific tab/sub-tab), screenshots the result, and prints any browser
console errors it saw. Exit code is 1 if there were console errors, 0
otherwise. Omit `--click` to land on the default post-login tab
(Overview).

Reviewer codes live in `agent-platform/config/review/reviewer_codes.yaml`
(gitignored — read it locally, don't guess). Admin-role codes can reach
`Admin` tab views; plain `reviewer`-role codes cannot.

### Seeding test data

To see non-empty state (progress bars, time-spent, annotations) without a
real reviewer session, hit the backend API directly before taking a
screenshot:

```bash
R="<a reviewer-role code>"
curl -s -X PATCH http://localhost:8889/api/v1/datasets/v5/reviews/ALS-M01/status \
  -H "X-Reviewer-Code: $R" -H "Content-Type: application/json" -d '{"status":"in_progress"}'
curl -s -X POST http://localhost:8889/api/v1/datasets/v5/reviews/ALS-M01/heartbeat \
  -H "X-Reviewer-Code: $R" -H "Content-Type: application/json" -d '{"seconds":120}'
```

**Always clean up seeded data afterward** — `data/review/annotations/` is
gitignored and reviewer-owned; it must come back to exactly its prior
state (empty, in local dev) so real review state is never polluted:

```bash
find data/review/annotations -type f -delete
find data/review/annotations -mindepth 1 -type d -empty -delete
mkdir -p data/review/annotations   # restore the (empty) directory itself
```

### Stopping

```bash
pkill -f "vite --port 5174"
pkill -f "uvicorn neuroagent.review_api.app:app"
```

## Run (human path)

```bash
uv run uvicorn neuroagent.review_api.app:app --app-dir agent-platform/src --host 0.0.0.0 --port 8889
cd web-review && npm run dev   # separate terminal — http://localhost:5174
```

Open `http://localhost:5174`, enter a reviewer code from
`reviewer_codes.yaml` on the login screen. Ctrl-C both processes to stop.

## Test

```bash
uv run pytest agent-platform/tests/test_tool_review.py agent-platform/tests/test_agreement_kappa.py -q
```

18 tests pass. Note: this covers the tool-review sub-feature and
inter-rater kappa math — there is currently no dedicated test file for
`review_api/services/aggregations.py`'s reviewer-progress summary or the
annotation store's `list_for_reviewer`; changes there are best verified
with this driver, not `pytest -k`.

---

## Gotchas

- **`npm run dev` binds to IPv6 `localhost` (`::1`), not `127.0.0.1`.**
  `curl http://127.0.0.1:5174` gets connection refused even though the
  server is up and `curl http://localhost:5174` succeeds. Always poll
  `localhost`, not `127.0.0.1`, for the frontend readiness check. (The
  backend binds fine on `127.0.0.1` — this is Vite-specific.)
- **The admin "Reviewer progress" view only lists `role: reviewer`
  codes** (`all_reviewers_progress` in `aggregations.py` filters out
  admins) — logging in as an admin code and expecting to see yourself on
  that screen will show nothing for your own row; that's correct
  behavior, not a bug.
- **`data/review/annotations/` is gitignored and has no fixture data
  checked in.** A fresh clone's admin dashboard shows all-zero progress
  cards until you seed data (see above) — that's expected, not broken.

## Troubleshooting

- **Login input never appears / `page.wait_for_selector("input")`
  times out**: the frontend dev server isn't actually up yet (Vite
  reports "ready" before the SPA is reachable at `localhost`, not
  `127.0.0.1` — see Gotchas). Poll `curl http://localhost:5174` before
  running the driver.
- **Backend curl gets a 401**: expected without the `X-Reviewer-Code`
  header, or with a code not present/active in `reviewer_codes.yaml`.
