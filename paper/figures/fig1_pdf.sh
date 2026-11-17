#!/usr/bin/env bash
# Figure 1 SVG -> PDF with headless Chrome (17 Nov 2026). rsvg-convert left a Type 3 font in the PDF,
# which the Nature figure guide refuses; Chrome embeds Arial as TrueType with editable text.
set -euo pipefail
cd "$(dirname "$0")"
uv run --no-project --with pillow python fig1_svg.py
H=$(grep -o 'height="[0-9.]*mm"' fig1.svg | head -1 | grep -o '[0-9.]*')
TMP=$(mktemp -d)
{ printf '<!doctype html><html><head><meta charset="utf-8"><style>@page{size:180mm %smm;margin:0}' "$H"
  printf 'html,body{margin:0;padding:0}svg{display:block;width:180mm;height:%smm}</style></head><body>' "$H"
  cat fig1.svg; printf '</body></html>'; } > "$TMP/fig1.html"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu \
  --no-pdf-header-footer --print-to-pdf="$PWD/fig1-new.pdf" "file://$TMP/fig1.html" 2>/dev/null
rm -r "$TMP"
pdffonts fig1-new.pdf | awk 'NR>2 && $0 ~ /Type 3/ {bad=1} END {if (bad) {print "Type 3 font in fig1-new.pdf"; exit 1}}'
pdfinfo fig1-new.pdf | grep -E "Pages|Page size"
