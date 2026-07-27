#!/usr/bin/env bash
set -euo pipefail

project_dir="$(cd "$(dirname "$0")" && pwd)"
chrome_bin="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
output_dir="$project_dir/output"
encoded_dir="${project_dir// /%20}"
source_url="file://$encoded_dir/index.html"

if [[ ! -x "$chrome_bin" ]]; then
  echo "Google Chrome was not found at: $chrome_bin" >&2
  exit 1
fi

if ! command -v pdftocairo >/dev/null 2>&1; then
  echo "pdftocairo is required to generate PNG previews." >&2
  exit 1
fi

mkdir -p "$output_dir"

chrome_flags=(
  --headless
  --disable-gpu
  --disable-background-networking
  --disable-component-update
  --disable-default-apps
  --disable-extensions
  --no-first-run
  --allow-file-access-from-files
  --no-pdf-header-footer
  --run-all-compositor-stages-before-draw
  --virtual-time-budget=6000
)

"$chrome_bin" "${chrome_flags[@]}" \
  --print-to-pdf="$output_dir/Blue-Ocean-Five-Identity-Directions.pdf" \
  "$source_url"

directions=(long-horizon field-notes proof-standard open-futures delhi-modern)
for direction in "${directions[@]}"; do
  "$chrome_bin" "${chrome_flags[@]}" \
    --print-to-pdf="$output_dir/$direction.pdf" \
    "$source_url?direction=$direction"
  pdftocairo -png -singlefile -r 144 \
    "$output_dir/$direction.pdf" \
    "$output_dir/$direction-preview"
done

echo "Rendered five identities to: $output_dir"
