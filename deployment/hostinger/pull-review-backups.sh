#!/bin/bash
set -euo pipefail

# ─────────────────────────────────────────────────────────
# Daily off-VPS copy of the NeuroBench review backups, run on the Mac.
#
# Pulls data/review/backups/ from the VPS into
#   ~/Backups/neurobench-review-backups/server-backups/
# Nothing is ever deleted here: snapshots the VPS prunes after 365 days
# stay on the Mac. The VPS holds no credentials for the Mac; the copy is
# a pull over the existing `hostinger` SSH entry.
#
# Invocation: launchd agent com.andreaprotani.neurobench-review-backups,
#             daily and at login (a run missed while the Mac slept fires
#             on wake).
# Manual:     launchctl kickstart gui/$(id -u)/com.andreaprotani.neurobench-review-backups
# Log:        ~/Backups/neurobench-review-backups/pull.log
#
# A failed pull, a damaged archive or a newest snapshot older than
# $MAX_AGE_DAYS days raises a macOS notification and exits non-zero.
# ─────────────────────────────────────────────────────────

SRC="hostinger:/home/neuroreview/medical-agents/data/review/backups/"
DEST="${DEST:-$HOME/Backups/neurobench-review-backups/server-backups}"
MAX_AGE_DAYS="${MAX_AGE_DAYS:-2}"

fail() {
    echo "$(date -u +%FT%TZ) FAILED: $1" >&2
    osascript -e "display notification \"$1\" with title \"NeuroBench review backup\"" >/dev/null 2>&1 || true
    exit 1
}
trap 'fail "pull stopped at line $LINENO"' ERR

mkdir -p "$DEST"
chmod 700 "$DEST"

# macOS ships openrsync, which has no --chmod: tighten permissions after.
rsync -a \
    -e "ssh -o BatchMode=yes -o ConnectTimeout=30" \
    --include 'review-data-*.tar.gz' --include 'annotations-*.tar.gz' --exclude '*' \
    "$SRC" "$DEST/" || fail "rsync from the VPS failed"
chmod 600 "$DEST"/*.tar.gz

latest=$(find "$DEST" -maxdepth 1 -name 'review-data-*.tar.gz' | sort | tail -1)
[ -n "$latest" ] || fail "no review-data snapshot in $DEST"
tar -tzf "$latest" >/dev/null || fail "damaged archive $(basename "$latest")"

day=$(basename "$latest" .tar.gz)
day=${day#review-data-}
age_days=$(( ( $(date -u +%s) - $(date -j -u -f %Y-%m-%d "$day" +%s) ) / 86400 ))
[ "$age_days" -le "$MAX_AGE_DAYS" ] || fail "newest VPS snapshot is $age_days days old ($day)"

files=$(tar -tzf "$latest" | grep -vc '/$')
echo "$(date -u +%FT%TZ) ok latest=$(basename "$latest") files=$files snapshots=$(find "$DEST" -maxdepth 1 -name '*.tar.gz' | wc -l | tr -d ' ')"
