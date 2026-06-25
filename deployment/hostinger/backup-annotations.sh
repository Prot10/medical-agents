#!/bin/bash
set -euo pipefail

# ─────────────────────────────────────────────────────────
# Daily snapshot of the NeuroBench review annotations.
#
# The "database" is the per-reviewer JSON tree at:
#   data/review/annotations/{version}/{reviewer_code}/{case_id}.json
#
# This script tars that tree into:
#   data/review/backups/annotations-YYYY-MM-DD.tar.gz
# and prunes snapshots older than $KEEP_DAYS days.
#
# Invocation: by systemd timer `neurobench-review-backup.timer` daily.
# Manual:     ssh hostinger 'sudo -u neuroreview /home/neuroreview/bin/backup-annotations.sh'
#
# Idempotent: re-running on the same day overwrites that day's snapshot.
# Atomic:     tars to a .tmp file, renames into place — incomplete snapshots
#             never appear under the canonical name.
# ─────────────────────────────────────────────────────────

DATA_ROOT="/home/neuroreview/medical-agents/data/review"
ANN_DIR="$DATA_ROOT/annotations"
BACKUP_DIR="$DATA_ROOT/backups"
KEEP_DAYS="${KEEP_DAYS:-365}"

mkdir -p "$BACKUP_DIR"

if [ ! -d "$ANN_DIR" ]; then
    echo "No annotations directory at $ANN_DIR — nothing to back up." >&2
    exit 0
fi

TS=$(date -u +%Y-%m-%d)
TARBALL="$BACKUP_DIR/annotations-$TS.tar.gz"
TMP="$TARBALL.tmp"

# Tar from the parent dir so the archive holds `annotations/...` paths
# (not absolute paths) — restores cleanly with `tar -xzf` into any prefix.
tar -czf "$TMP" -C "$DATA_ROOT" annotations
mv "$TMP" "$TARBALL"

# Rotate: drop tarballs older than KEEP_DAYS by mtime.
find "$BACKUP_DIR" -maxdepth 1 -type f -name 'annotations-*.tar.gz' \
    -mtime "+${KEEP_DAYS}" -print -delete | sed 's/^/pruned: /' >&2 || true

echo "$(date -u +%FT%TZ) snapshot=$TARBALL size=$(stat -c%s "$TARBALL") bytes"
