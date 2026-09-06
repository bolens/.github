# Requirement coverage

| Requirement | Source and acceptance evidence |
| --- | --- |
| FR-001 | `scripts/bootstrap-spec-kit`, `tests/test_bootstrap.py`; rejected dirty worktree and input fixtures. |
| FR-002 | `scripts/validate-spec-kit.py`; validator execution and bootstrap/integration fixtures. This is installation evidence, not feature completion. |
| FR-003 | `scripts/lint-source.py`, `tests/test_source_lint.py`, and pinned reusable-source-lint workflow. |
| FR-004 | `.github/workflows/reusable-*.yml`, bootstrap template tests, actionlint and zizmor. |
| FR-005 | `specs/001-maintainer-assignment`, `tests/test_auto_assign.py`; source-lint feature remains authoritative under its own existing spec. |

## Verification receipt

Native pre-push checks passed: JSON/Bash integration checks, installed integration status, Python unit suite, actionlint, and offline zizmor. Separate self-review inspected bootstrap preconditions, manifest validation, lint source selection, and workflow permissions. Existing feature tasks remain complete; this baseline does not invent an implementation-compliance validator.
