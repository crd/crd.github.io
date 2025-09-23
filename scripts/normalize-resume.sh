#!/usr/bin/env bash
set -euo pipefail
# Adjust targets here if you want more files normalized
TARGETS=(
  "_pages/resume.md"
)

echo "Normalizing markdown:"
for f in "${TARGETS[@]}"; do
  if [[ -f "$f" ]]; then
    echo " - $f"
    python3 tools/normalize_markdown.py --ensure-frontmatter "$f"
  else
    echo " ! Skipping missing file: $f"
  fi
done
