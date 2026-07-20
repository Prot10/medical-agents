# Shared base-model staging, sourced by the training and eval scripts.
type ui_step >/dev/null 2>&1 || { ui_step(){ echo "▶ $*"; }; ui_ok(){ echo "✓ $*"; }; ui_warn(){ echo "⚠ $*" >&2; }; ui_err(){ echo "✗ $*" >&2; }; }
#
# Reading a full model off the EOS FUSE mount is ~1-2h of scattered small reads, so we copy it
# into /dev/shm (RAM) once and load from there. The copy must be idempotent and VALIDATED: a
# bare `[ -d ]` check treats a half-finished copy as done (this bit us — a partial 9B dir made
# training load offline and fail). rsync completes a partial copy; the sentinel check refuses
# to proceed until the snapshot actually resolves.

EOS_HF="${EOS_HF:-/eos/project-d/diagbox/dvc/NeuroAgent/models/base/huggingface}"
SHM_HF="${SHM_HF:-/dev/shm/hf}"

# True only if the HF cache dir holds a snapshot whose config.json and every *.safetensors
# shard actually resolve (the symlinks' blob targets exist). `-f`/`-e` follow symlinks, so a
# dangling link from a partial copy fails the test.
_base_is_complete() {
  local dir="$1" snap f
  snap="$(ls -d "$dir"/snapshots/*/ 2>/dev/null | head -1)"
  [ -n "$snap" ] || return 1
  [ -f "$snap/config.json" ] || return 1
  local found=0
  for f in "$snap"/*.safetensors; do
    [ -e "$f" ] || return 1   # dangling shard (partial copy) or no shards at all
    found=1
  done
  [ "$found" = 1 ] || return 1
  return 0
}

# stage_base <hf_repo_id>   e.g. stage_base Qwen/Qwen3.5-9B
# Ensures the base model is fully present in /dev/shm and exports HF_HOME to point at it.
stage_base() {
  local repo="$1"
  local model_dir="models--${repo//\//--}"
  local src="$EOS_HF/hub/$model_dir"
  local dst="$SHM_HF/hub/$model_dir"
  local name; name="$(basename "$repo")"

  [ -d "$src" ] || { ui_err "base model not on EOS: $src"; return 1; }

  if _base_is_complete "$dst"; then
    ui_ok "$name base already staged in RAM"
    export HF_HOME="$SHM_HF"; export HF_HUB_OFFLINE=1
    return 0
  fi

  ui_step "Staging $name base weights: EOS → $SHM_HF (RAM)"
  mkdir -p "$SHM_HF/hub"
  # -a preserves the blob/symlink layout; rsync resumes/completes a partial dir.
  if command -v rsync >/dev/null; then
    rsync -a --info=progress2 "$src/" "$dst/" || { ui_err "staging rsync failed"; return 1; }
  else
    cp -a "$src/." "$dst/" || { ui_err "staging cp failed"; return 1; }
  fi

  _base_is_complete "$dst" || { ui_err "staged copy incomplete after sync: $dst"; return 1; }
  ui_ok "$name base staged"
  export HF_HOME="$SHM_HF"; export HF_HUB_OFFLINE=1
}
