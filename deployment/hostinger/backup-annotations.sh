#!/bin/bash
set -euo pipefail

# ─────────────────────────────────────────────────────────
# Daily snapshot of the NeuroBench review data.
#
# The "database" is two JSON trees under data/review/:
#   annotations/{version}/{reviewer_code}/{case_id}.json   case reviews
#   tool_reviews/{version}/{reviewer_code}.json            tool-output reviews
#
# This script tars both into:
#   data/review/backups/review-data-YYYY-MM-DD.tar.gz
# and prunes snapshots older than $KEEP_DAYS days. Snapshots made before
# 21 Oct 2026 are named annotations-YYYY-MM-DD.tar.gz and hold annotations
# only; they follow the same rotation.
#
# A copy leaves the VPS every day: the Mac pulls this folder with
# pull-review-backups.sh (see README, "Off-VPS copy").
#
# Invocation: by systemd timer `neurobench-review-backup.timer` daily.
# Manual:     ssh hostinger 'systemctl start neurobench-review-backup.service'
#
# Idempotent: re-running on the same day overwrites that day's snapshot.
# Atomic:     tars to a .tmp file, checks it, renames into place — incomplete
#             snapshots never appear under the canonical name.
# ─────────────────────────────────────────────────────────

DATA_ROOT="/home/neuroreview/medical-agents/data/review"
TREES=(annotations tool_reviews)
BACKUP_DIR="$DATA_ROOT/backups"
KEEP_DAYS="${KEEP_DAYS:-365}"

mkdir -p "$BACKUP_DIR"

PRESENT=()
for tree in "${TREES[@]}"; do
    if [ -d "$DATA_ROOT/$tree" ]; then
        PRESENT+=("$tree")
    else
        echo "warning: no $tree directory at $DATA_ROOT/$tree" >&2
    fi
done
if [ ${#PRESENT[@]} -eq 0 ]; then
    echo "No review data under $DATA_ROOT — nothing to back up." >&2
    exit 0
fi

TS=$(date -u +%Y-%m-%d)
TARBALL="$BACKUP_DIR/review-data-$TS.tar.gz"
TMP="$TARBALL.tmp"

# Tar from the parent dir so the archive holds `annotations/...` and
# `tool_reviews/...` paths (not absolute paths) — restores cleanly with
# `tar -xzf` into any prefix.
tar -czf "$TMP" -C "$DATA_ROOT" "${PRESENT[@]}"

# Refuse to publish an archive that does not hold every file on disk.
on_disk=$(cd "$DATA_ROOT" && find "${PRESENT[@]}" -type f | wc -l)
in_archive=$(tar -tzf "$TMP" | grep -vc '/$')
if [ "$on_disk" -ne "$in_archive" ]; then
    echo "snapshot check failed: $on_disk files on disk, $in_archive in archive" >&2
    rm -f "$TMP"
    exit 1
fi
mv "$TMP" "$TARBALL"

# Rotate: drop tarballs older than KEEP_DAYS by mtime.
find "$BACKUP_DIR" -maxdepth 1 -type f \
    \( -name 'review-data-*.tar.gz' -o -name 'annotations-*.tar.gz' \) \
    -mtime "+${KEEP_DAYS}" -print -delete | sed 's/^/pruned: /' >&2 || true

echo "$(date -u +%FT%TZ) snapshot=$TARBALL files=$in_archive size=$(stat -c%s "$TARBALL") bytes"
