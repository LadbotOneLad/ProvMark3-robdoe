#!/usr/bin/env bash
set -euo pipefail

USER="LadbotOneLad"
K_COUPLING=1.0   # your Kuramoto knob
TAG_PREFIX="phase"

# 1. Get all repos (source + forks)
repos=$(gh repo list "$USER" --limit 200 --json name --jq '.[].name')

for repo in $repos; do
  echo "=== ORCHESTRATING $USER/$repo ==="

  # 2. Clone or update
  if [ -d "$repo" ]; then
    cd "$repo"
    git fetch --all
  else
    gh repo clone "$USER/$repo"
    cd "$repo"
  fi

  # 3. Try to detect upstream (for forks)
  if git remote get-url upstream >/dev/null 2>&1; then
    git checkout main || git checkout master || true
    git fetch upstream

    # Kuramoto-style “sync” decision placeholder
    # (here we just always rebase; you can plug your math in)
    git rebase upstream/$(git branch --show-current || echo main)
  fi

  # 4. Commit any staged/working changes (if any)
  if ! git diff --quiet || ! git diff --cached --quiet; then
    git add .
    git commit -m "crewAI: phase update"
  fi

  # 5. Tag a phase transition
  COMMIT=$(git rev-parse HEAD)
  TAG="${TAG_PREFIX}-$(date +%s)"
  git tag -a "$TAG" -m "phase transition on $COMMIT"

  # 6. Push branch + tags
  CURRENT_BRANCH=$(git branch --show-current || echo main)
  git push origin "$CURRENT_BRANCH" --tags

  cd ..
done
