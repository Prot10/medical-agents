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
| Backups | systemd timer `neurobench-review-backup.timer`, daily 03:15 UTC; pulled to the Mac daily by a launchd agent |
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

### What ships

The deploy script ships **only** the parts of the repo `review_api` imports at runtime. Since agent mode (`agent-platform/docs/review-agent-mode.md`) that includes the benchmark harness it drives; training, the run API and the agent platform stay off the VPS, and no model is called from it:

- `agent-platform/src/neuroagent/{harness,tools,evaluation,llm}/` + `model_registry.py`, `agent-platform/config/profiles/`, `agent-platform/config/tools/fallback_library.yaml` — the harness, MockServer and reward that agent mode uses

- `agent-platform/src/neuroagent/__init__.py` + `agent-platform/src/neuroagent/review_api/` — the review backend
- `agent-platform/pyproject.toml` — workspace member manifest
- `agent-platform/config/review/` — reviewer-config dir (without `reviewer_codes.yaml` unless `--force-codes`)
- `agent-platform/config/tools/costs.yaml` — read by `services/tool_catalog.py`
- `packages/neuroagent-schemas/` — `NeuroBenchCase` Pydantic model
- `dataset-generation/{pyproject.toml,src/}` + `dataset-generation/config/conditions.yaml` — workspace member shell (required by `uv sync`) plus the tool-catalog config
- `pyproject.toml`, `uv.lock` — root workspace + lockfile
- `data/neurobench/` — 600 benchmark cases
- `web-review/dist/` — built static frontend

VPS footprint after a deploy: ~26 MB total (mostly the NeuroBench dataset). The script **never deletes** `data/review/annotations/`, `data/review/agent-mode/` or `data/review/backups/` — reviewer data and snapshots are server-owned.

### Flags

| Flag | Effect |
|---|---|
| `--skip-build` | Reuse the existing `web-review/dist/` (skip Vite rebuild) |
| `--code-only` | Skip `data/neurobench/` and `web-review/dist/` — fastest path for backend-only changes |
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
    /home/neuroreview/medical-agents/{agent-platform/src/neuroagent,packages,dataset-generation/config,data/neurobench,data/review/annotations,data/review/backups,web-review/dist} \
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

`data/review/annotations/` (case reviews), `data/review/tool_reviews/` (tool-output reviews) and `data/review/agent-mode/` (physicians' agent-mode records) are the only state worth preserving — the schema files come from the deploy and the case fleet is in git. A systemd timer snapshots them on the VPS, and the Mac pulls the snapshots every day.

### Schedule

`neurobench-review-backup.timer` fires daily at **03:15 UTC** with `Persistent=true` (a missed run — e.g. host was off — fires at next boot, not silently skipped).

### What it does

`/home/neuroreview/bin/backup-annotations.sh` tars `data/review/annotations/`, `data/review/tool_reviews/` and `data/review/agent-mode/` into `data/review/backups/review-data-YYYY-MM-DD.tar.gz`, and refuses to publish an archive that does not hold every file on disk. Snapshots made before 21 Oct 2026 are named `annotations-YYYY-MM-DD.tar.gz` and hold annotations only. Tarballs older than **365 days** are pruned automatically (override with `KEEP_DAYS=N` in the systemd unit's `Environment=` if needed). At ~3 MB per worst-case tarball that's ~1 GB of disk over a full year — negligible against 45 GB free.

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
    stamp=$(date -u +%Y%m%dT%H%M%SZ) &&
    mv annotations annotations.before-restore-$stamp &&
    mv tool_reviews tool_reviews.before-restore-$stamp &&
    tar -xzf backups/review-data-YYYY-MM-DD.tar.gz
"'
ssh hostinger 'systemctl restart neurobench-review'
```

The pre-restore copies are kept under `annotations.before-restore-<timestamp>/` and `tool_reviews.before-restore-<timestamp>/` so you can roll back the rollback.

### Off-VPS copy (daily, on the Mac)

Local snapshots protect against application bugs and accidental deletes but not VPS-level loss. The Mac pulls `data/review/backups/` every day into `~/Backups/neurobench-review-backups/server-backups/` with `pull-review-backups.sh`, run by the launchd agent `com.andreaprotani.neurobench-review-backups` (09:30 local time and at login; a run missed while the Mac slept fires on wake). It never deletes on the Mac, checks the newest archive, and raises a macOS notification if the pull fails or the newest VPS snapshot is more than two days old. The VPS holds no credentials for the Mac. The folder sits outside `~/Documents` on purpose: macOS privacy protection (TCC) blocks launchd jobs from reading or writing `~/Documents`, `~/Desktop` and `~/Downloads`.

```bash
# Install or update on the Mac (from the repo root).
D=~/Backups/neurobench-review-backups
mkdir -p $D && install -m 700 deployment/hostinger/pull-review-backups.sh $D/
sed "s#__HOME__#$HOME#g" deployment/hostinger/com.andreaprotani.neurobench-review-backups.plist \
    > ~/Library/LaunchAgents/com.andreaprotani.neurobench-review-backups.plist
launchctl bootout gui/$(id -u)/com.andreaprotani.neurobench-review-backups 2>/dev/null || true
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.andreaprotani.neurobench-review-backups.plist

# Pull now, and read the log.
launchctl kickstart gui/$(id -u)/com.andreaprotani.neurobench-review-backups
tail -3 ~/Backups/neurobench-review-backups/pull.log
```

## Agent mode on the VPS

Both sections of agent mode (`agent-platform/docs/review-agent-mode.md`) are served by the same service.

### Synthetic section

Served once deployed. Add the physicians' codes (`sections: [agent_synthetic]`) to `reviewer_codes.yaml` and push it with `--force-codes`. After the first deploy that includes agent mode, reinstall the backup script so that `data/review/agent-mode/` is in the daily snapshot:

```bash
scp deployment/hostinger/backup-annotations.sh hostinger:/home/neuroreview/bin/backup-annotations.sh
```

### MIMIC section

Decided by Andrea on 25 Nov 2026: the MIMIC section runs here too, with 20 of the final 100 processed benchmark cases. Never raw MIMIC data; the 80 cases that are not drawn never leave EOS. Everything lives **outside the repo tree**:

```
/home/neuroreview/mimic-agent-mode/cases/           the 20 drawn case JSON files (read-only for the app)
/home/neuroreview/mimic-agent-mode/case-list.txt    their ids, in the order they are served
/home/neuroreview/mimic-agent-mode/records/         physicians' MIMIC records (the only path the app writes there)
/home/neuroreview/mimic-agent-mode/agent-mode.env   the three REVIEW_AGENT_MIMIC_* variables
```

`deploy.sh` only ever writes under `/home/neuroreview/medical-agents`, so it never syncs, overwrites or deletes these, and they never enter git. The app refuses to start the section from a path inside the repo.

To enable it:

```bash
# 1. Once: install the unit that reads agent-mode.env and may write the records directory.
scp deployment/hostinger/neurobench-review.service hostinger:/etc/systemd/system/neurobench-review.service
ssh hostinger 'systemctl daemon-reload'

# 2. From rockhopper or lxplus (EOS mounted; never from the Mac, so the cases never touch its disk),
#    in a checkout of this repo:
deployment/hostinger/push-mimic-cases.sh --dry-run <EOS folder of the final 100 cases>   # counts per condition only
deployment/hostinger/push-mimic-cases.sh <EOS folder of the final 100 cases>
```

What the script does:

1. Refuses a folder that does not hold exactly 100 case files (`EXPECTED=N` to override), and refuses to run on macOS.
2. Draws the set with `agent-platform/scripts/review/draw_mimic_set.py` (plain `python3`, seed `SEED=20261125`, `DRAW=20`): stratified by condition, one case per condition present, the remaining slots in proportion to what each condition has left by largest remainder, a seeded draw within each condition, a seeded random order. It reads only each case's id and condition, and prints only how many cases each condition gives (expected for the final 100: ISCH 6, MS 4, SAH 2, HEP 2, SE 2, GBS 1, FND 1, FEPI 1, BACT 1). No case id or text is printed.
3. Writes the 20 ids to `agent-mode-mimic-set.txt` next to the source folder on EOS, and refuses a later run that would draw a different set (`FORCE=1` to replace it).
4. Copies only those 20 files straight from EOS to the VPS over SSH, with the list as `case-list.txt`, writes `agent-mode.env`, sets owner and modes (700/600) and restarts the service.

It needs an SSH destination that logs in as root on the VPS: the `hostinger` alias, or `VPS_HOST=root@<address>`. Once a physician has a MIMIC record it refuses to change the case set (`FORCE=1` to override).

To add MIMIC codes, add rows with `sections: [agent_mimic]` (or `[agent_synthetic, agent_mimic]`) and an `id` to `reviewer_codes.yaml`, only for physicians credentialed on PhysioNet, and push with `./deployment/hostinger/deploy.sh --force-codes`. A code without `agent_mimic` gets 404 on the section.

To disable the section: `ssh hostinger 'rm /home/neuroreview/mimic-agent-mode/agent-mode.env && systemctl restart neurobench-review'` (cases and records stay).

MIMIC records are **not** in the daily snapshot: that archive is pulled to the Mac, and the records hold record-derived text. They stay on the VPS only; export them there with `export_physician_episodes.py --section mimic --output <path outside the repo>`.
