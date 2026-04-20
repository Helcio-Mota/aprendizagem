#!/usr/bin/env bash
set -euo pipefail
# Converts HTML files in current dir to PDF using available tool.
# Usage: ./convert_htmls_to_pdf.sh [pattern]
PAT=${1:-"assistant_response_*.html"}
TOOL=""
if command -v wkhtmltopdf >/dev/null 2>&1; then
  TOOL=wkhtmltopdf
elif command -v google-chrome >/dev/null 2>&1; then
  TOOL=chrome
elif command -v chromium >/dev/null 2>&1; then
  TOOL=chrome
else
  echo "No conversion tool found (wkhtmltopdf or chrome)." >&2
  exit 1
fi
for f in $PAT; do
  [ -f "$f" ] || continue
  base="${f%.html}"
  out="${base}.pdf"
  if [ "$TOOL" = "wkhtmltopdf" ]; then
    wkhtmltopdf --enable-local-file-access "$f" "$out"
  else
    # use headless chrome
    google-chrome --headless --disable-gpu --print-to-pdf="$out" "file://$PWD/$f"
  fi
  echo "Converted $f -> $out"
done
