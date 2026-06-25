#!/bin/bash
set -euo pipefail

# ─────────────────────────────────────────────────────────
# NeuroBench Review — Hostinger VPS Deploy
#
# Mirrors the kosmico-api deploy.sh pattern: build locally → rsync → restart.
# Connects as root via the SSH alias `hostinger` (defined in ~/.ssh/config →
# root@187.77.84.186) and pushes into /home/neuroreview/medical-agents/.
#
# Provisioning (one-time, manual): see ./README.md.
#
# What this script ships (REVIEW-API ONLY — the agent platform, training,
# evaluation, LLM clients, tools, etc. are deliberately NOT synced to keep
# the VPS minimal):
#   - agent-platform/src/neuroagent/__init__.py .......... package marker
#   - agent-platform/src/neuroagent/review_api/ .......... the only runtime code
#   - agent-platform/pyproject.toml ...................... workspace member manifest
#   - agent-platform/config/review/ ...................... reviewer-config dir
#   - agent-platform/config/tool_costs.yaml .............. tool catalog cost summaries
#   - packages/neuroagent-schemas/ ....................... NeuroBenchCase model
#   - dataset-generation/{pyproject.toml,src/} ........... workspace member shell (uv sync requires it)
#   - dataset-generation/config/conditions.yaml .......... tool-catalog per-condition rules
#   - pyproject.toml, uv.lock ............................ root workspace + lockfile
#   - data/neurobench_v5/ ................................ 600 benchmark cases
#   - web-review/dist/ ................................... built static frontend
#
# What this script never touches on the VPS:
#   - data/review/annotations/ . reviewer-produced data, server-owned (never --delete'd)
#   - data/review/backups/ ..... daily snapshots from the backup timer
#   - .venv/, node_modules/ .... installed on the VPS, never synced
#   - reviewer_codes.yaml ...... gated behind --force-codes; never wiped on routine deploy
#   - logs/ .................... server-local
#
# Usage:
#   ./deployment/hostinger/deploy.sh                # full build + sync + restart
#   ./deployment/hostinger/deploy.sh --skip-build   # reuse existing web-review/dist
#   ./deployment/hostinger/deploy.sh --code-only    # skip data + dist (faster code push)
#   ./deployment/hostinger/deploy.sh --force-codes  # also sync reviewer_codes.yaml
# ─────────────────────────────────────────────────────────

VPS_HOST="hostinger"
VPS_USER="neuroreview"
VPS_PATH="/home/${VPS_USER}/medical-agents"
SERVICE="neurobench-review.service"
HEALTH_URL="https://review.andreaprotani.com/api/v1/datasets"

CYAN='\033[0;36m'; YELLOW='\033[1;33m'; GREEN='\033[0;32m'; RED='\033[0;31m'; NC='\033[0m'

cd "$(dirname "$0")/../.."
REPO_ROOT=$(pwd)

SKIP_BUILD=0
CODE_ONLY=0
FORCE_CODES=0
for arg in "$@"; do
  case "$arg" in
    --skip-build)   SKIP_BUILD=1 ;;
    --code-only)    CODE_ONLY=1 ;;
    --force-codes)  FORCE_CODES=1 ;;
    *) echo "Unknown flag: $arg"; exit 2 ;;
  esac
done

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  NeuroBench Review — deploy to ${VPS_HOST}${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# ── Step 1: Build frontend ──────────────────────────────
if [ "$SKIP_BUILD" -eq 1 ] || [ "$CODE_ONLY" -eq 1 ]; then
  echo -e "${YELLOW}[1/5] Skipping frontend build${NC}"
else
  echo -e "${YELLOW}[1/5] Building web-review/dist (Vite)...${NC}"
  ( cd web-review && npm run build )
  echo -e "${GREEN}  Build complete.${NC}"
fi

# ── Step 2: Rsync code ──────────────────────────────────
# Editable installs in the uv workspace mean syncing source is enough — no
# dist/ build needed for Python. --delete keeps the remote tidy but the
# excludes below protect server-owned state (annotations, .venv, logs).
echo -e "${YELLOW}[2/5] Rsyncing source (review_api only)...${NC}"

# Only ship neuroagent.review_api + the package's __init__.py. The rest of
# neuroagent (agent/, api/, evaluation/, llm/, memory/, rules/, tools/,
# training/) is never imported by review_api and stays off the VPS.
rsync -az --delete \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude 'tests/' \
  agent-platform/src/neuroagent/review_api/ \
  "$VPS_HOST:$VPS_PATH/agent-platform/src/neuroagent/review_api/"
rsync -az agent-platform/src/neuroagent/__init__.py \
  "$VPS_HOST:$VPS_PATH/agent-platform/src/neuroagent/__init__.py"

# agent-platform/pyproject.toml is the workspace member manifest — required
# even if we only use review_api, because `uv sync` resolves the workspace.
rsync -az agent-platform/pyproject.toml "$VPS_HOST:$VPS_PATH/agent-platform/pyproject.toml"

# neuroagent-schemas package — review_api imports NeuroBenchCase from it.
rsync -az --delete \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  packages/neuroagent-schemas/ \
  "$VPS_HOST:$VPS_PATH/packages/neuroagent-schemas/"

# Config: ONLY the review/ subdir is needed (reviewer codes + future review
# config). hospital_rules/, system_prompts/, tool_costs.yaml, etc. belong to
# the main agent and stay local.
# reviewer_codes.yaml itself is excluded here — gated behind --force-codes.
rsync -az --delete \
  --exclude 'reviewer_codes.yaml' \
  agent-platform/config/review/ \
  "$VPS_HOST:$VPS_PATH/agent-platform/config/review/"

# dataset-generation is declared as a uv workspace member in the root
# pyproject.toml, so `uv sync` requires its package files to exist on the
# VPS even though review_api never imports neurobench_gen. The whole
# package is small (~16K) and ship-cost is trivial.
rsync -az --delete \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  dataset-generation/pyproject.toml \
  dataset-generation/src \
  "$VPS_HOST:$VPS_PATH/dataset-generation/"

# conditions.yaml + tool_costs.yaml — review_api/services/tool_catalog.py
# reads both to build the per-condition tool-permission map and cost-summary
# labels. Without them, the tool catalog endpoint is degraded.
rsync -az dataset-generation/config/conditions.yaml \
  "$VPS_HOST:$VPS_PATH/dataset-generation/config/conditions.yaml"
rsync -az agent-platform/config/tool_costs.yaml \
  "$VPS_HOST:$VPS_PATH/agent-platform/config/tool_costs.yaml"

if [ "$FORCE_CODES" -eq 1 ]; then
  if [ -f agent-platform/config/review/reviewer_codes.yaml ]; then
    echo -e "${YELLOW}  Pushing reviewer_codes.yaml (--force-codes)${NC}"
    rsync -az agent-platform/config/review/reviewer_codes.yaml \
      "$VPS_HOST:$VPS_PATH/agent-platform/config/review/reviewer_codes.yaml"
    ssh "$VPS_HOST" "chmod 600 $VPS_PATH/agent-platform/config/review/reviewer_codes.yaml && \
                     chown $VPS_USER:$VPS_USER $VPS_PATH/agent-platform/config/review/reviewer_codes.yaml"
  else
    echo -e "${RED}  WARN: --force-codes set but local reviewer_codes.yaml missing${NC}"
  fi
fi

rsync -az pyproject.toml uv.lock "$VPS_HOST:$VPS_PATH/"
echo -e "${GREEN}  Source synced.${NC}"

# ── Step 3: Rsync data + frontend dist ──────────────────
if [ "$CODE_ONLY" -eq 1 ]; then
  echo -e "${YELLOW}[3/5] Skipping data + dist (--code-only)${NC}"
else
  echo -e "${YELLOW}[3/5] Rsyncing data + dist...${NC}"
  rsync -az --delete \
    data/neurobench_v5/ \
    "$VPS_HOST:$VPS_PATH/data/neurobench_v5/"

  rsync -az --delete \
    web-review/dist/ \
    "$VPS_HOST:$VPS_PATH/web-review/dist/"
  echo -e "${GREEN}  Data + dist synced.${NC}"
fi

# ── Step 4: Reset ownership + uv sync + restart ─────────
# pipefail catches `uv sync` failures even though we tail its output. Without
# it, a broken workspace would fall through silently and the service would
# restart on stale deps.
echo -e "${YELLOW}[4/5] Fixing ownership + syncing deps + restarting service...${NC}"
ssh "$VPS_HOST" "set -eo pipefail
  chown -R $VPS_USER:$VPS_USER $VPS_PATH
  sudo -u $VPS_USER bash -lc 'cd $VPS_PATH && ~/.local/bin/uv sync --all-packages 2>&1 | tail -5'
  systemctl restart $SERVICE
  systemctl is-active $SERVICE >/dev/null
"
echo -e "${GREEN}  Service restarted.${NC}"

# ── Step 5: Smoke test ──────────────────────────────────
# uvicorn needs ~2s after systemctl restart returns to finish loading the
# v5 case fleet. Retry a few times. We accept any non-5xx code: a 401 with
# our probe header is evidence the backend processed the request and ran
# its auth check, which is exactly what we want to verify here.
echo -e "${YELLOW}[5/5] Smoke-testing...${NC}"
for attempt in 1 2 3 4 5; do
  code=$(curl -s -o /dev/null -m 10 -w "%{http_code}" "$HEALTH_URL" -H "X-Reviewer-Code: probe")
  if [ -n "$code" ] && [ "$code" -lt 500 ]; then
    echo -e "${GREEN}  ${HEALTH_URL} responding HTTP $code (attempt $attempt).${NC}"
    break
  fi
  if [ "$attempt" -eq 5 ]; then
    echo -e "${RED}  ${HEALTH_URL} returned HTTP $code after 5 tries.${NC}"
    echo -e "${RED}  Check: ssh $VPS_HOST 'journalctl -u $SERVICE -n 50 --no-pager'${NC}"
    exit 1
  fi
  sleep 2
done

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  Deploy complete.${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  Live URL:  ${YELLOW}https://review.andreaprotani.com${NC}"
echo -e "  Logs:      ${YELLOW}ssh $VPS_HOST 'journalctl -u $SERVICE -f'${NC}"
echo -e "  Status:    ${YELLOW}ssh $VPS_HOST 'systemctl status $SERVICE'${NC}"
