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
#   - agent-platform/src/neuroagent/datasets.py .......... shared dataset registry (review_api imports it)
#   - agent-platform/src/neuroagent/review_api/ .......... the review backend
#   - agent-platform/src/neuroagent/{harness,tools,evaluation,llm}/ + model_registry.py
#                                                          the benchmark harness that agent mode drives
#   - agent-platform/config/profiles/, config/tools/fallback_library.yaml ... its configuration
#   - agent-platform/pyproject.toml ...................... workspace member manifest
#   - agent-platform/config/review/ ...................... reviewer-config dir
#   - agent-platform/config/tools/costs.yaml ............. tool catalog cost summaries
#   - packages/neuroagent-schemas/ ....................... NeuroBenchCase model
#   - dataset-generation/{pyproject.toml,src/} ........... workspace member shell (uv sync requires it)
#   - dataset-generation/config/conditions.yaml .......... tool-catalog per-condition rules
#   - pyproject.toml, uv.lock ............................ root workspace + lockfile
#   - data/neurobench/ .................................. 600 benchmark cases (not with --keep-cases)
#   - data/review/sets/ .................................. frozen case copies of the review sets
#   - web-review/dist/ ................................... built static frontend
#
# What this script never touches on the VPS:
#   - data/review/annotations/ . reviewer-produced data, server-owned (never --delete'd)
#   - data/review/agent-mode/ .. physicians' agent-mode records, server-owned
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
#   ./deployment/hostinger/deploy.sh --keep-cases   # leave the VPS's data/neurobench as it is
#       (the full review keeps serving the version the physicians annotated; review sets
#        with their own cases_dir still get their frozen copies)
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
KEEP_CASES=0
for arg in "$@"; do
  case "$arg" in
    --skip-build)   SKIP_BUILD=1 ;;
    --code-only)    CODE_ONLY=1 ;;
    --force-codes)  FORCE_CODES=1 ;;
    --keep-cases)   KEEP_CASES=1 ;;
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
echo -e "${YELLOW}[2/5] Rsyncing source (review_api and the harness it drives)...${NC}"

# Ship neuroagent.review_api + the package's __init__.py, then (below) the harness modules
# agent mode imports. The rest of neuroagent (agent/, api/, memory/, rules/, training/) is
# never imported by review_api and stays off the VPS.
rsync -az --delete \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude 'tests/' \
  agent-platform/src/neuroagent/review_api/ \
  "$VPS_HOST:$VPS_PATH/agent-platform/src/neuroagent/review_api/"
rsync -az agent-platform/src/neuroagent/__init__.py \
  "$VPS_HOST:$VPS_PATH/agent-platform/src/neuroagent/__init__.py"

# Shared dataset registry — review_api's config/routes/services all import
# from neuroagent.datasets (strict dataset registry and loader).
# It lives outside review_api/ so it must be shipped explicitly.
rsync -az agent-platform/src/neuroagent/datasets.py \
  "$VPS_HOST:$VPS_PATH/agent-platform/src/neuroagent/datasets.py"

# Agent mode (review_api/services/agent_mode) drives the benchmark harness itself, so a physician
# gets exactly the agent's presentation, catalogue and observations: the harness, the tools with
# the MockServer, the reward (admin view) and the modules they import go with it. No model is
# ever called from the VPS; llm/ is shipped only because the harness imports its types.
for module in harness tools evaluation llm; do
  rsync -az --delete \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    "agent-platform/src/neuroagent/$module/" \
    "$VPS_HOST:$VPS_PATH/agent-platform/src/neuroagent/$module/"
done
rsync -az agent-platform/src/neuroagent/model_registry.py \
  "$VPS_HOST:$VPS_PATH/agent-platform/src/neuroagent/model_registry.py"
# Its configuration: the checked profiles (turn limits) and the whole tool configuration (the
# cost registry and the fallback library that answers off-pathway orders).
ssh "$VPS_HOST" "mkdir -p $VPS_PATH/agent-platform/config/profiles $VPS_PATH/agent-platform/config/tools"
rsync -az --delete agent-platform/config/profiles/ "$VPS_HOST:$VPS_PATH/agent-platform/config/profiles/"
rsync -az agent-platform/config/tools/fallback_library.yaml \
  "$VPS_HOST:$VPS_PATH/agent-platform/config/tools/fallback_library.yaml"
# The commit this copy runs from, recorded in every agent-mode record (the VPS has no git tree).
git rev-parse HEAD > agent-platform/config/review/deployed_commit.txt

# agent-platform/pyproject.toml is the workspace member manifest — required
# even if we only use review_api, because `uv sync` resolves the workspace.
rsync -az agent-platform/pyproject.toml "$VPS_HOST:$VPS_PATH/agent-platform/pyproject.toml"

# neuroagent-schemas package — review_api imports NeuroBenchCase from it.
rsync -az --delete \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  packages/neuroagent-schemas/ \
  "$VPS_HOST:$VPS_PATH/packages/neuroagent-schemas/"

# Config: of config/, only review/ is synced here. hospital_rules/ and
# system_prompts/ belong to the main agent and stay local. config/tools/costs.yaml
# IS shipped, further down with conditions.yaml — the tool catalog reads both, and
# the enum vocabularies the review app serves are derived from costs.yaml, so a
# stale copy silently misrepresents the action space to reviewers.
# condition_tool_guidance.yaml goes with it: it carries the clinical reviewers' own revised
# descriptions per condition, and without it the app renders their comments with no answer.
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

# conditions.yaml + tools/costs.yaml — review_api/services/tool_catalog.py
# reads both to build the per-condition tool-permission map and cost-summary
# labels. Without them, the tool catalog endpoint is degraded.
rsync -az dataset-generation/config/conditions.yaml \
  "$VPS_HOST:$VPS_PATH/dataset-generation/config/conditions.yaml"
ssh "$VPS_HOST" "mkdir -p $VPS_PATH/agent-platform/config/tools"
rsync -az agent-platform/config/tools/costs.yaml \
  "$VPS_HOST:$VPS_PATH/agent-platform/config/tools/costs.yaml"

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
  if [ "$KEEP_CASES" -eq 1 ]; then
    echo -e "${YELLOW}  Keeping the VPS's data/neurobench (--keep-cases)${NC}"
  else
    rsync -az --delete \
      data/neurobench/ \
      "$VPS_HOST:$VPS_PATH/data/neurobench/"
  fi

  # Review sets' own frozen case copies (config/review/review_sets.yaml `cases_dir`).
  if [ -d data/review/sets ]; then
    rsync -az --delete \
      data/review/sets/ \
      "$VPS_HOST:$VPS_PATH/data/review/sets/"
  fi

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
# uvicorn needs ~10s after systemctl restart returns to finish loading the
# case fleet. Retry a few times. We accept any non-5xx code: a 401 with
# our probe header is evidence the backend processed the request and ran
# its auth check, which is exactly what we want to verify here.
echo -e "${YELLOW}[5/5] Smoke-testing...${NC}"
for attempt in $(seq 1 15); do
  code=$(curl -s -o /dev/null -m 10 -w "%{http_code}" "$HEALTH_URL" -H "X-Reviewer-Code: probe")
  if [ -n "$code" ] && [ "$code" -lt 500 ]; then
    echo -e "${GREEN}  ${HEALTH_URL} responding HTTP $code (attempt $attempt).${NC}"
    break
  fi
  if [ "$attempt" -eq 15 ]; then
    echo -e "${RED}  ${HEALTH_URL} returned HTTP $code after 15 tries.${NC}"
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
