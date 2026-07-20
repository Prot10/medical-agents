#!/bin/bash
# Shared terminal UI for the training/eval scripts: semantic colours + modern panels, so the
# bash side matches the Rich progress bars the Python side renders. Source it once:
#   source "$SCRIPT_DIR/_ui.sh"
# Colours are emitted only when stdout is a real terminal, so redirecting to a file stays clean.
[ -n "${_UI_SH_LOADED:-}" ] && return 0
_UI_SH_LOADED=1

if [ -t 1 ]; then
  C_RESET=$'\033[0m'; C_BOLD=$'\033[1m'; C_DIM=$'\033[2m'
  C_BLUE=$'\033[38;5;39m'; C_GREEN=$'\033[38;5;42m'; C_CYAN=$'\033[38;5;44m'
  C_YELLOW=$'\033[38;5;220m'; C_RED=$'\033[38;5;203m'; C_MAG=$'\033[38;5;170m'
  C_GREY=$'\033[38;5;245m'
else
  C_RESET=; C_BOLD=; C_DIM=; C_BLUE=; C_GREEN=; C_CYAN=; C_YELLOW=; C_RED=; C_MAG=; C_GREY=
fi

# Status lines — the leading glyph carries the meaning by colour.
ui_ok()   { printf '  %s✓%s %s\n'  "$C_GREEN"  "$C_RESET" "$*"; }
ui_step() { printf '  %s▶%s %s\n'  "$C_CYAN"   "$C_RESET" "$*"; }
ui_warn() { printf '  %s⚠%s %s\n'  "$C_YELLOW" "$C_RESET" "$*"; }
ui_err()  { printf '  %s✗%s %s\n'  "$C_RED"    "$C_RESET" "$*" >&2; }
ui_info() { printf '  %s%s%s\n'    "$C_GREY"   "$*" "$C_RESET"; }

# A bold, coloured section divider between phases.
ui_section() {
  printf '\n%s%s━━━━━  %s  %s━━━━━%s\n\n' "$C_BOLD" "$C_MAG" "$*" "$C_MAG" "$C_RESET"
}

# A left-ruled panel with a bold title and grey key / value rows. Robust (no width maths):
#   ui_panel "GRPO · Qwen3.5-4B" "precision|bf16" "output|/eos/…" …
ui_panel() {
  local title="$1"; shift
  printf '\n%s┃%s %s%s%s\n' "$C_BLUE" "$C_RESET" "$C_BOLD$C_BLUE" "$title" "$C_RESET"
  local kv key val
  for kv in "$@"; do
    key="${kv%%|*}"; val="${kv#*|}"
    printf '%s┃%s   %s%-11s%s %s\n' "$C_BLUE" "$C_RESET" "$C_GREY" "$key" "$C_RESET" "$val"
  done
  printf '%s┃%s\n' "$C_BLUE" "$C_RESET"
}
