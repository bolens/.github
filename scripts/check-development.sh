#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
npm ci --ignore-scripts --no-audit --no-fund --prefix tools/source-lint
bash .githooks/pre-push
python3 scripts/validate-spec-kit.py .
python3 scripts/lint-source.py .
python3 tests/source_lint_smoke.py
