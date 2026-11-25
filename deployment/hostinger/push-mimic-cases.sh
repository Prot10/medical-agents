#!/bin/bash
set -euo pipefail

# ─────────────────────────────────────────────────────────
# Draw the MIMIC case set of agent mode (20 of the final 100 processed
# cases), copy ONLY the drawn cases from the EOS workspace to the review
# VPS, and enable the MIMIC section there.
#
# Run it from rockhopper or lxplus, where EOS is mounted: the files go
# straight from EOS to the VPS over SSH and never touch the Mac's disk.
# Only processed benchmark cases are copied (one JSON per case), never raw
# MIMIC data, and the cases that are not drawn never leave EOS. The script
# prints counts per condition only: never a case id, never case text.
#
# The draw (agent-platform/scripts/review/draw_mimic_set.py, plain python3):
# stratified by condition, one case per condition present, the remaining
# slots in proportion to what each condition has left by largest remainder,
# then a seeded random draw within each condition and a seeded random order.
# The ordered ids are written next to the source folder on EOS
# (agent-mode-mimic-set.txt) and on the VPS (case-list.txt, which the app
# serves in that order). A later run that would draw a different set is
# refused: a set is drawn once.
#
# On the VPS the cases and the records live outside the repo tree, so
# deploy.sh never syncs, overwrites or deletes them and they never enter git:
#   /home/neuroreview/mimic-agent-mode/cases/           the drawn case files (read by the app)
#   /home/neuroreview/mimic-agent-mode/case-list.txt    the drawn ids, in serving order
#   /home/neuroreview/mimic-agent-mode/records/         physicians' MIMIC records (written by the app)
#   /home/neuroreview/mimic-agent-mode/agent-mode.env   read by the systemd unit; its presence enables the section
#
# Usage:
#   deployment/hostinger/push-mimic-cases.sh --dry-run <folder holding the 100 case JSON files, or one holding cases/>
#   deployment/hostinger/push-mimic-cases.sh <folder>
#   Environment: EXPECTED=100 (files in the folder), DRAW=20, SEED=20261125, VPS_HOST=hostinger, FORCE=1
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
DRAW="${DRAW:-20}"
SEED="${SEED:-20261125}"
DRAW_SCRIPT="$(cd "$(dirname "$0")/../.." && pwd)/agent-platform/scripts/review/draw_mimic_set.py"

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
  echo "Refusing: the folder must hold exactly the final $EXPECTED cases (override with EXPECTED=N)." >&2
  exit 1
fi
# The drawn ids are kept next to the source folder on EOS, never on this machine's disk.
SOURCE="$(cd "$SOURCE" && pwd)"
LIST="$(dirname "$SOURCE")/agent-mode-mimic-set.txt"

if [ "$DRY_RUN" -eq 1 ]; then
  python3 "$DRAW_SCRIPT" "$SOURCE" --n "$DRAW" --seed "$SEED"
  echo "Dry run: nothing written, nothing copied. Target: $VPS_HOST:$REMOTE_ROOT/cases/"
  exit 0
fi

# A set that physicians have started is frozen: never change it under them.
started=$(ssh "$VPS_HOST" "find $REMOTE_ROOT/records -type f -name '*.json' 2>/dev/null | wc -l" | tr -d ' ')
if [ "$started" -gt 0 ] && [ "${FORCE:-0}" != "1" ]; then
  echo "Refusing to copy: $started MIMIC record(s) already exist on the VPS, so the case set is in use." >&2
  echo "Changing it would change what physicians worked on. Set FORCE=1 only if you are sure." >&2
  exit 1
fi

python3 "$DRAW_SCRIPT" "$SOURCE" --n "$DRAW" --seed "$SEED" --write "$LIST.new"
if [ -f "$LIST" ] && ! cmp -s "$LIST" "$LIST.new" && [ "${FORCE:-0}" != "1" ]; then
  rm -f "$LIST.new"
  echo "Refusing: a different set was already drawn from this folder (the list next to it differs)." >&2
  echo "The cases, DRAW or SEED changed since. Set FORCE=1 to replace the set." >&2
  exit 1
fi
mv "$LIST.new" "$LIST"
chmod 600 "$LIST"
drawn=$(wc -l < "$LIST" | tr -d ' ')

ssh "$VPS_HOST" "mkdir -p $REMOTE_ROOT/cases $REMOTE_ROOT/records && find $REMOTE_ROOT/cases -maxdepth 1 -type f -name '*.json' -delete"
# Only the drawn files are sent; the list of file names is piped, not stored.
sed 's/$/.json/' "$LIST" | rsync -az --files-from=- "$SOURCE/" "$VPS_HOST:$REMOTE_ROOT/cases/"
rsync -az "$LIST" "$VPS_HOST:$REMOTE_ROOT/case-list.txt"

ssh "$VPS_HOST" "set -e
  cat > $REMOTE_ROOT/agent-mode.env <<'ENV'
REVIEW_AGENT_MIMIC_CASES_DIR=$REMOTE_ROOT/cases
REVIEW_AGENT_MIMIC_LOG_DIR=$REMOTE_ROOT/records
REVIEW_AGENT_MIMIC_CASE_LIST=$REMOTE_ROOT/case-list.txt
ENV
  chown -R $VPS_USER:$VPS_USER $REMOTE_ROOT
  chmod 700 $REMOTE_ROOT $REMOTE_ROOT/cases $REMOTE_ROOT/records
  find $REMOTE_ROOT/cases -type f -exec chmod 600 {} +
  chmod 600 $REMOTE_ROOT/agent-mode.env $REMOTE_ROOT/case-list.txt
"
remote=$(ssh "$VPS_HOST" "find $REMOTE_ROOT/cases -maxdepth 1 -type f -name '*.json' | wc -l" | tr -d ' ')
echo "Cases drawn: $drawn. Case files on the VPS: $remote"
if [ "$remote" -ne "$drawn" ]; then
  echo "Copy check failed: $drawn drawn, $remote on the VPS." >&2
  exit 1
fi

# The app reads the cases at start-up.
ssh "$VPS_HOST" "systemctl restart $SERVICE && sleep 12 && systemctl is-active $SERVICE >/dev/null"
echo "MIMIC section enabled with $drawn cases. If the service did not come back: ssh $VPS_HOST 'journalctl -u $SERVICE -n 30 --no-pager'"
