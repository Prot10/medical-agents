# Hostinger VPS — NeuroBench Review Deployment

Deployment target for the NeuroBench dataset review platform on the shared Hostinger VPS that also hosts Kosmico.

| | |
|---|---|
| Live URL | https://review.andreaprotani.com |
| VPS | `187.77.84.186` (`srv1386500.hstgr.cloud`, AlmaLinux 10.1) |
| SSH alias | `hostinger` → `root@187.77.84.186` |
| App user | `neuroreview` (uid 1001, no sudo, no shared groups) |
| App path | `/home/neuroreview/medical-agents/` |
| FastAPI port | `127.0.0.1:8889` (localhost only — nginx is the public entry) |
| Process supervisor | systemd unit `neurobench-review.service` |
| Reverse proxy | nginx, vhost `/etc/nginx/conf.d/review.andreaprotani.com.conf` |
| TLS | Let's Encrypt via `certbot --nginx`, auto-renewed (`certbot-renew.timer`) |
| "Database" | Per-reviewer JSON files at `data/review/annotations/{version}/{reviewer_code}/{case_id}.json` — file-based, no DB server. |

## Isolation from Kosmico

The same nginx serves Kosmico (`web.kosmico.ai`, `api.kosmico.ai`) and the review platform. The two apps cannot collide because:

- **Different OS user.** Kosmico runs under root via PM2; NeuroBench runs as `neuroreview` via systemd. Neither user can write into the other's tree.
- **Different ports.** Kosmico uses `3000` (web) and `3001` (api); NeuroBench uses `8889`. Bound to localhost — never exposed publicly.
- **Different nginx vhost file.** `/etc/nginx/conf.d/review.andreaprotani.com.conf` is independent from `kosmico.conf` and `api.kosmico.ai.conf`. Always `nginx -t` before any reload.
- **No shared database.** Kosmico talks to OpenRouter; NeuroBench uses file-based annotation storage in `/home/neuroreview/medical-agents/data/review/annotations/`. No DB server is even installed.
- **No PM2 entry for NeuroBench.** Process management is systemd, kept out of `pm2 list` to avoid accidental Kosmico interactions.

## Routine deploy

```bash
./deployment/hostinger/deploy.sh
```

Pipeline: build `web-review/dist` locally → rsync code + data + dist → `uv sync` on VPS → `systemctl restart neurobench-review` → smoke-test the public URL.

### What ships (review-API only)

The deploy script ships **only** the parts of the repo `review_api` imports at runtime — never the agent platform, training, evaluation, or LLM-client code:

- `agent-platform/src/neuroagent/__init__.py` + `agent-platform/src/neuroagent/review_api/` — the review backend
- `agent-platform/pyproject.toml` — workspace member manifest
- `agent-platform/config/review/` — reviewer-config dir (without `reviewer_codes.yaml` unless `--force-codes`)
- `agent-platform/config/tool_costs.yaml` — read by `services/tool_catalog.py`
- `packages/neuroagent-schemas/` — `NeuroBenchCase` Pydantic model
- `dataset-generation/{pyproject.toml,src/}` + `dataset-generation/config/conditions.yaml` — workspace member shell (required by `uv sync`) plus the tool-catalog config
- `pyproject.toml`, `uv.lock` — root workspace + lockfile
- `data/neurobench_v5/` — 600 benchmark cases
- `web-review/dist/` — built static frontend

VPS footprint after a deploy: ~26 MB total (mostly the v5 dataset). The script **never deletes** `data/review/annotations/` or `data/review/backups/` — reviewer data and snapshots are server-owned.

### Flags

| Flag | Effect |
|---|---|
| `--skip-build` | Reuse the existing `web-review/dist/` (skip Vite rebuild) |
| `--code-only` | Skip `data/neurobench_v5/` and `web-review/dist/` — fastest path for backend-only changes |
| `--force-codes` | Also push `agent-platform/config/review/reviewer_codes.yaml` (normally untouched by deploys; that file is gitignored) |

## One-time provisioning (already done; documented for reproduction)

```bash
# 1. Hostinger hPanel → DNS: A record `review` → 187.77.84.186 (TTL default).

# 2. Create dedicated user with no privileges + traversable home for nginx.
ssh hostinger 'useradd -m -s /bin/bash neuroreview && chmod 755 /home/neuroreview'

# 3. Install uv as the user.
ssh hostinger 'sudo -u neuroreview bash -lc "curl -LsSf https://astral.sh/uv/install.sh | sh"'

# 4. Create app + data + bin dirs owned by the user.
ssh hostinger 'sudo -u neuroreview mkdir -p \
    /home/neuroreview/medical-agents/{agent-platform/src/neuroagent,packages,dataset-generation/config,data/neurobench_v5,data/review/annotations,data/review/backups,web-review/dist} \
    /home/neuroreview/bin'

# 5. First-time sync (push code, data, dist, AND reviewer codes).
./deployment/hostinger/deploy.sh --force-codes

# 6. Lock down the synced reviewer_codes.yaml (the deploy script does this
#    automatically on --force-codes, but worth confirming after first run).
ssh hostinger 'chmod 600 /home/neuroreview/medical-agents/agent-platform/config/review/reviewer_codes.yaml'

# 7. Drop in the nginx vhost (HTTP only first — certbot rewrites it).
scp deployment/hostinger/nginx-review.andreaprotani.com.conf \
    hostinger:/etc/nginx/conf.d/review.andreaprotani.com.conf
ssh hostinger 'nginx -t && systemctl reload nginx'

# 8. Issue the TLS cert. -d names only the new domain — kosmico vhosts
#    stay untouched (verified by their inode mtimes after this runs).
ssh hostinger 'certbot --nginx -d review.andreaprotani.com \
    --non-interactive --agree-tos -m protanipaolo@gmail.com --redirect'

# 9. Install + start the FastAPI systemd unit.
scp deployment/hostinger/neurobench-review.service \
    hostinger:/etc/systemd/system/neurobench-review.service
ssh hostinger 'systemctl daemon-reload && \
               systemctl enable --now neurobench-review.service && \
               systemctl status neurobench-review.service --no-pager'

```

## Operations cookbook

```bash
# Tail backend logs
ssh hostinger 'journalctl -u neurobench-review -f'

# Restart backend
ssh hostinger 'systemctl restart neurobench-review'

# Verify backend health locally on VPS
ssh hostinger 'curl -s http://127.0.0.1:8889/api/v1/datasets | head -c 200'

# Inspect reviewer annotations on disk
ssh hostinger 'ls /home/neuroreview/medical-agents/data/review/annotations/'

# Rotate reviewer codes
#   1. edit agent-platform/config/review/reviewer_codes.yaml locally
#   2. ./deployment/hostinger/deploy.sh --force-codes
#   (codes hot-reload — no service restart needed)

# Reload nginx (after editing a vhost file)
ssh hostinger 'nginx -t && systemctl reload nginx'

# Check kosmico is still happy
ssh hostinger 'pm2 status'
```

## Backup

`data/review/annotations/` is the only state worth preserving — schema files come from the deploy and the case fleet is in git. Pull a snapshot to your laptop with:

```bash
rsync -az hostinger:/home/neuroreview/medical-agents/data/review/annotations/ \
    ./data/review/annotations.vps-backup/
```

A scheduled daily backup is tracked separately — see the follow-up commit that adds `backup-annotations.sh` + the timer.
