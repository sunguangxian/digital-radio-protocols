#!/usr/bin/env bash
# Sync library (Markdown + PDFs + 进度.json + codex + scripts)
# from /workspace/digital-radio-protocols to sunguangxian/digital-radio-protocols
set -euo pipefail
SRC=/workspace/digital-radio-protocols
DST=/tmp/digital-radio-sync
REPO=https://github.com/sunguangxian/digital-radio-protocols.git
gh auth setup-git >/dev/null
# Migrate old sync clone path if present
if [ -d /tmp/dmr-sync ] && [ ! -d "$DST" ]; then
  mv /tmp/dmr-sync "$DST"
fi
if [ ! -d "$DST/.git" ]; then
  rm -rf "$DST"
  git clone "$REPO" "$DST"
fi
cd "$DST"
# Ensure remote points at new repo name
git remote set-url origin "$REPO"
git fetch origin
git checkout main
git pull --ff-only origin main || true
find . -mindepth 1 -maxdepth 1 ! -name '.git' -exec rm -rf {} +
cd "$SRC"
# Sync md, pdf, progress json, scripts, and whole tree structure
find . -type f \( -name '*.md' -o -name '*.pdf' -o -name '进度.json' -o -path './scripts/*' -o -path './codex/*' \) ! -path './.git/*' -print0 |
while IFS= read -r -d '' f; do
  mkdir -p "$DST/$(dirname "$f")"
  cp -a "$f" "$DST/$f"
done
# Ensure empty placeholder dirs exist even if only README was copied
for d in shared dpmr nxdn pdt compare dmr codex scripts; do
  mkdir -p "$DST/$d"
done
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
git commit -m "Restructure as multi-protocol digital-radio-protocols (DMR under dmr/)"
git push origin main
echo "PUSHED"
