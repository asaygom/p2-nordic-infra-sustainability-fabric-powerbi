#!/usr/bin/env bash
# Create GitHub issues using gh CLI. Usage:
#   GH_REPO=asaygom/p2-nordic-infra-sustainability-fabric-powerbi ./scripts/create_issues.sh
set -euo pipefail
: "${GH_REPO:?set GH_REPO=owner/repo}"
common="milestone:v0.9,triage,good-first-issue"
gh issue create -R "$GH_REPO" -t "chore(init): scaffold repo" -b "Add .gitignore, LICENSE, theme.json, metadata.yml" -l "$common"
gh issue create -R "$GH_REPO" -t "docs: README EN/ES + docs placeholders" -b "Add README.md/README.es.md, docs/one-pager.*.md, diagramas Mermaid, demo scripts" -l "$common"
gh issue create -R "$GH_REPO" -t "feat(data): synthetic CSVs" -b "Implement python/generate_synthetic_data.py and write to /data/synthetic" -l "$common"
gh issue create -R "$GH_REPO" -t "feat(dax): base + time-intel" -b "Add base DAX, metric-scoped measures, mark date table" -l "$common"
gh issue create -R "$GH_REPO" -t "feat(report): Executive v0.6" -b "Cards + matrix + line/column; filters by city" -l "$common"
gh issue create -R "$GH_REPO" -t "feat(report): What‑if + tooltip" -b "Parameter/What-if and explanatory tooltip" -l "$common"
gh issue create -R "$GH_REPO" -t "docs: one‑pager PDF + GIF 90s" -b "Export and store under /media" -l "$common"
gh issue create -R "$GH_REPO" -t "chore(release): v0.9 + assets" -b "Attach PBIX/PDF/GIF to release" -l "$common"
gh issue create -R "$GH_REPO" -t "fix(p1): patch docs pack" -b "PDF 1‑pág + GIF + SPI/CPI + refresh notes" -l "$common"