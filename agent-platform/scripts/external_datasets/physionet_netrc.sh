#!/usr/bin/env bash
# Store the PhysioNet password once for batch downloads (physionet_download.sub), on lxplus.
# Usage: ./physionet_netrc.sh <physionet-username> [dir]
# The password is typed without echo, never on a command line or in the shell history, and lands
# in <dir>/.netrc (mode 600, folder mode 700, private EOS home by default). Delete the folder when
# the downloads are done: rm -r /eos/user/a/aprotani/.physionet-auth
set -euo pipefail
user="${1:?usage: $0 <physionet-username> [dir]}"
dir="${2:-/eos/user/a/aprotani/.physionet-auth}"
umask 077
mkdir -p "$dir"
chmod 700 "$dir"
read -rsp "PhysioNet password for $user: " pw
echo
printf 'machine physionet.org login %s password %s\n' "$user" "$pw" > "$dir/.netrc"
unset pw
chmod 600 "$dir/.netrc"
# Check it against PhysioNet without downloading anything: 200 means the password works.
code=$(HOME="$dir" wget -S --spider -q "https://physionet.org/files/mimiciv/3.1/" 2>&1 \
  | awk '/HTTP\//{c=$2} END{print c}')
echo "PhysioNet answered $code ($([[ $code == 200 ]] && echo 'password OK' || echo 'check the password'))"
