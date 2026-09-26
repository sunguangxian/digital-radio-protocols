#!/usr/bin/env bash
# Sync library (Markdown + PDFs + 进度.json) from /workspace/dmr-protocol to sunguangxian/dmr-protocol
set -euo pipefail
SRC=/workspace/dmr-protocol
DST=/tmp/dmr-sync
gh auth setup-git >/dev/null
if [ ! -d "$DST/.git" ]; then
  rm -rf "$DST"
  git clone https://github.com/sunguangxian/dmr-protocol.git "$DST"
fi
cd "$DST"
git fetch origin
git checkout main
git pull --ff-only origin main || true
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cd "$SRC"
# Sync md, pdf, progress json; skip scripts helper-only noise optional — include scripts
find . -type f \( -name '*.md' -o -name '*.pdf' -o -name '进度.json' -o -path './scripts/*' \) ! -path './.git/*' -print0 |
while IFS= read -r -d '' f; do
  mkdir -p "$DST/$(dirname "$f")"
  cp -a "$f" "$DST/$f"
done
# also copy codex tree fully if any non-md
if [ -d "$SRC/codex" ]; then
  mkdir -p "$DST/codex"
  cp -a "$SRC/codex/." "$DST/codex/" 2>/dev/null || true
fi
cd "$DST"
git config user.email "sunguangxian@users.noreply.github.com"
git config user.name "sunguangxian"
git add -A
if git diff --cached --quiet; then
  echo "NO_CHANGE"
  exit 0
fi
git commit -m "Sync materials from local library (Markdown + PDFs)"
git push origin main
echo "PUSHED"
