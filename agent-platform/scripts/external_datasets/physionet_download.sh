#!/usr/bin/env bash
# Download the credentialed PhysioNet projects NeuroAgent uses onto private CERN storage.
# Usage (on lxplus):
#   ./physionet_download.sh <physionet-username> [dest] [path ...]
# path defaults to the four projects below; a sub-folder such as mimiciv/3.1/hosp downloads only
# that part and checks only its lines of the project's SHA256SUMS.txt (one job per folder runs
# in parallel: PhysioNet throttles each connection to ~250 KB/s).
# tmux does NOT keep it alive on lxplus: logind kills the session's processes (tmux included)
# when the SSH login that started it closes (KillUserProcesses=yes, tested 5 Nov 2026). A rerun
# resumes where it stopped; for a run that must outlive the laptop, submit physionet_download.sub
# to HTCondor. In a batch job there is no terminal: set PHYSIONET_NETRC_DIR to a private folder
# holding a .netrc (`machine physionet.org login <user> password <pw>`, mode 600) and wget
# reads the password from it.
#
# dest defaults to /eos/user/a/aprotani/physionet, a mode-700 folder of the EOS home: the DUA
# restricts access to credentialed users, so never the shared /eos/project-d/diagbox, never the
# Mac, never a pod's /scratch as the only copy. wget asks the PhysioNet password once, on the
# terminal; it is never passed on the command line (visible to other lxplus users in `ps`).
#
# Needs the DUA signed on every project page first (Settings → Training must show the CITI
# course as accepted). Re-running resumes and skips files already complete (-N -c), then checks
# every project against its SHA256SUMS.txt. Prints file names and counts only, never contents.
#
# Projects (all PhysioNet Credentialed Health Data Use Agreement 1.5.0, CITI training):
#   mimiciv/3.1            hosp + icu modules
#   mimic-iv-note/2.2      discharge and radiology notes
#   mimic-iv-ed/2.2        ED stays, triage, vitals
#   mimic-iv-ext-cdm/1.1   curated abdominal cases (Hager et al., Nat Med 2024)

set -euo pipefail

user="${1:?usage: $0 <physionet-username> [dest] [path ...]}"
dest="${2:-/eos/user/a/aprotani/physionet}"
projects=("${@:3}")
[[ ${#projects[@]} -gt 0 ]] || projects=(mimic-iv-ext-cdm/1.1 mimic-iv-ed/2.2 mimic-iv-note/2.2 mimiciv/3.1)

auth=(--user "$user" --ask-password)
if [[ -n "${PHYSIONET_NETRC_DIR:-}" ]]; then
  [[ -f "$PHYSIONET_NETRC_DIR/.netrc" ]] || { echo "no .netrc in PHYSIONET_NETRC_DIR" >&2; exit 2; }
  export HOME="$PHYSIONET_NETRC_DIR"   # wget reads $HOME/.netrc
  auth=(--progress=dot:giga)           # batch log: one progress line per 32 MB, not per 50 KB
fi

umask 077
mkdir -p "$dest"
chmod 700 "$dest"
cd "$dest"

urls=()
for p in "${projects[@]}"; do urls+=("https://physionet.org/files/$p/"); done

# One invocation for all projects, so the password is asked once. --cut-dirs=1 drops "files/".
wget -r -N -c -np -nH --cut-dirs=1 -R "index.html*" "${auth[@]}" \
  --wait=1 --random-wait "${urls[@]}"

for p in "${projects[@]}"; do
  echo "== $p"
  root="$(cut -d/ -f1-2 <<<"$p")"   # project/version, where SHA256SUMS.txt lives
  sub="${p#"$root"}"; sub="${sub#/}"
  if [[ ! -f "$root/SHA256SUMS.txt" ]]; then
    echo "no SHA256SUMS.txt"
  elif [[ -z "$sub" ]]; then
    (cd "$root" && sha256sum --quiet -c SHA256SUMS.txt && echo "checksums OK")
  else
    (cd "$root" && awk -v s="$sub/" 'index($2, s) == 1' SHA256SUMS.txt | sha256sum --quiet -c - \
      && echo "checksums OK for $sub")
  fi
  echo "$(find "$p" -type f | wc -l) files, $(du -sh "$p" | cut -f1)"
done
