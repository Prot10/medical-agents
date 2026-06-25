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
| Backups | systemd timer `neurobench-review-backup.timer`, daily 03:15 UTC |
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

# 10. Install the daily backup tooling (timer + service + script).
scp deployment/hostinger/backup-annotations.sh \
    hostinger:/home/neuroreview/bin/backup-annotations.sh
scp deployment/hostinger/neurobench-review-backup.service \
    hostinger:/etc/systemd/system/neurobench-review-backup.service
scp deployment/hostinger/neurobench-review-backup.timer \
    hostinger:/etc/systemd/system/neurobench-review-backup.timer
ssh hostinger 'chown neuroreview:neuroreview /home/neuroreview/bin/backup-annotations.sh && \
               chmod 755 /home/neuroreview/bin/backup-annotations.sh && \
               systemctl daemon-reload && \
               systemctl enable --now neurobench-review-backup.timer'
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

## Backups

`data/review/annotations/` is the only state worth preserving — the schema files come from the deploy and the case fleet is in git. Backups are handled by a systemd timer.

### Schedule

`neurobench-review-backup.timer` fires daily at **03:15 UTC** with `Persistent=true` (a missed run — e.g. host was off — fires at next boot, not silently skipped).

### What it does

`/home/neuroreview/bin/backup-annotations.sh` tars `data/review/annotations/` into `data/review/backups/annotations-YYYY-MM-DD.tar.gz`. Tarballs older than **365 days** are pruned automatically (override with `KEEP_DAYS=N` in the systemd unit's `Environment=` if needed). At ~3 MB per worst-case tarball that's ~1 GB of disk over a full year — negligible against 45 GB free.

The script is atomic (`.tar.gz.tmp` → `mv` rename) and idempotent — running it twice on the same day overwrites that day's snapshot rather than failing.

### Operations

```bash
# When does the next backup run?
ssh hostinger 'systemctl list-timers neurobench-review-backup.timer --no-pager'

# Trigger a backup right now (e.g. before a risky change).
ssh hostinger 'systemctl start neurobench-review-backup.service'

# Inspect the most recent backup.
ssh hostinger 'ls -lh /home/neuroreview/medical-agents/data/review/backups/ | tail -5'

# Read backup logs.
ssh hostinger 'journalctl -u neurobench-review-backup.service -n 50 --no-pager'
```

### Restore

To restore a specific day's snapshot (this wipes whatever's currently on the VPS — make sure that's what you want):

```bash
ssh hostinger 'sudo -u neuroreview bash -lc "
    cd /home/neuroreview/medical-agents/data/review &&
    mv annotations annotations.before-restore-$(date -u +%Y%m%dT%H%M%SZ) &&
    tar -xzf backups/annotations-YYYY-MM-DD.tar.gz
"'
ssh hostinger 'systemctl restart neurobench-review'
```

The pre-restore copy of `annotations/` is kept under `annotations.before-restore-<timestamp>/` so you can roll back the rollback.

### Off-VPS copy (optional, manual)

Local snapshots protect against application bugs and accidental deletes but not VPS-level loss. Pull a copy to your laptop when paranoia spikes:

```bash
rsync -az hostinger:/home/neuroreview/medical-agents/data/review/backups/ \
    ./data/review/vps-backups/
```
