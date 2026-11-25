#!/bin/bash
set -euo pipefail

# ─────────────────────────────────────────────────────────
# Copy the processed MIMIC benchmark cases (the final 100) from the EOS
# workspace to the review VPS, and enable the MIMIC section of agent mode.
#
# Run it from rockhopper or lxplus, where EOS is mounted: the files go
# straight from EOS to the VPS over SSH and never touch the Mac's disk.
# Only processed benchmark cases are copied (one JSON per case), never raw
# MIMIC data. The script prints file counts only, never names or content.
#
# On the VPS the cases and the records live outside the repo tree, so
# deploy.sh never syncs, overwrites or deletes them and they never enter git:
#   /home/neuroreview/mimic-agent-mode/cases/           the case files (read by the app)
#   /home/neuroreview/mimic-agent-mode/records/         physicians' MIMIC records (written by the app)
#   /home/neuroreview/mimic-agent-mode/agent-mode.env   read by the systemd unit; its presence enables the section
#
# Usage:
#   deployment/hostinger/push-mimic-cases.sh <folder holding the 100 case JSON files, or one holding cases/>
#   EXPECTED=100 VPS_HOST=hostinger deployment/hostinger/push-mimic-cases.sh --dry-run <folder>
#
# VPS_HOST must be an SSH destination that logs in as root on the VPS (the
# `hostinger` alias of deploy.sh; define it in ~/.ssh/config on the machine
# you run this from, or pass VPS_HOST=root@<address>).
# ─────────────────────────────────────────────────────────

VPS_HOST="${VPS_HOST:-hostinger}"
VPS_USER="neuroreview"
REMOTE_ROOT="/home/${VPS_USER}/mimic-agent-mode"
SERVICE="neurobench-review"
EXPECTED="${EXPECTED:-100}"

DRY_RUN=0
if [ "${1:-}" = "--dry-run" ]; then DRY_RUN=1; shift; fi
SOURCE="${1:-}"
if [ -z "$SOURCE" ] || [ ! -d "$SOURCE" ]; then
  echo "usage: $0 [--dry-run] <folder holding the processed case JSON files>" >&2
  exit 2
fi
[ -d "$SOURCE/cases" ] && SOURCE="$SOURCE/cases"

case "$(uname -s)" in
  Darwin) echo "Refusing to run on macOS: run it from rockhopper or lxplus, so the cases never touch the Mac's disk." >&2; exit 1 ;;
esac

count=$(find "$SOURCE" -maxdepth 1 -type f -name '*.json' | wc -l | tr -d ' ')
echo "Case files in the source folder: $count (expected $EXPECTED)"
if [ "$count" -ne "$EXPECTED" ]; then
  echo "Refusing to copy: the folder must hold exactly the final $EXPECTED cases (override with EXPECTED=N)." >&2
  exit 1
fi
if [ "$DRY_RUN" -eq 1 ]; then
  echo "Dry run: nothing copied. Target: $VPS_HOST:$REMOTE_ROOT/cases/"
  exit 0
fi

# A set that physicians have started is frozen: never change it under them.
started=$(ssh "$VPS_HOST" "find $REMOTE_ROOT/records -type f -name '*.json' 2>/dev/null | wc -l" | tr -d ' ')
if [ "$started" -gt 0 ] && [ "${FORCE:-0}" != "1" ]; then
  echo "Refusing to copy: $started MIMIC record(s) already exist on the VPS, so the case set is in use." >&2
  echo "Changing it would change what physicians worked on. Set FORCE=1 only if you are sure." >&2
  exit 1
fi

ssh "$VPS_HOST" "mkdir -p $REMOTE_ROOT/cases $REMOTE_ROOT/records"
# Only the top-level case JSON files; --delete keeps the VPS folder equal to the final set.
rsync -az --delete --include='*.json' --exclude='*' "$SOURCE/" "$VPS_HOST:$REMOTE_ROOT/cases/"

ssh "$VPS_HOST" "set -e
  cat > $REMOTE_ROOT/agent-mode.env <<'ENV'
REVIEW_AGENT_MIMIC_CASES_DIR=$REMOTE_ROOT/cases
REVIEW_AGENT_MIMIC_LOG_DIR=$REMOTE_ROOT/records
ENV
  chown -R $VPS_USER:$VPS_USER $REMOTE_ROOT
  chmod 700 $REMOTE_ROOT $REMOTE_ROOT/cases $REMOTE_ROOT/records
  find $REMOTE_ROOT/cases -type f -exec chmod 600 {} +
  chmod 600 $REMOTE_ROOT/agent-mode.env
"
remote=$(ssh "$VPS_HOST" "find $REMOTE_ROOT/cases -maxdepth 1 -type f -name '*.json' | wc -l" | tr -d ' ')
echo "Case files on the VPS: $remote"
if [ "$remote" -ne "$count" ]; then
  echo "Copy check failed: $count files here, $remote on the VPS." >&2
  exit 1
fi

# The app reads the cases at start-up.
ssh "$VPS_HOST" "systemctl restart $SERVICE && sleep 12 && systemctl is-active $SERVICE >/dev/null"
echo "MIMIC section enabled. If the service did not come back: ssh $VPS_HOST 'journalctl -u $SERVICE -n 30 --no-pager'"
