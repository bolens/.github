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

## Detailed audit, 2026-09-06

[Legacy contracts](legacy-contracts.md) enumerate the inspected capabilities.

| Contract | Source owner | Acceptance evidence |
| --- | --- | --- |
| LC-001 / FR-001 | bootstrap script and caller template | Disposable clean/dirty, malformed options, mutable refs, cron and spaced-path fixtures in `test_bootstrap.py`. |
| LC-002 / FR-002,008 | installation validator | Valid integration, malformed nested objects/UTF-8, multi-repository continuation and external/symlink path fixtures in `test_spec_kit_validation.py`; candidate validator accepted all 28 included local installations. |
| LC-003 / FR-004,006 | reusable Spec Kit validation | Exact shell input guard fixtures; repository-local reusable CI caller exercises checkout and validation on GitHub. Hosted result belongs to the PR. |
| LC-004 / FR-007 | reusable updater and regeneration helper | Original workflow allowed guide/AGENTS mutation while rejecting constitution mutation. Disposable fixtures now reject changes/removals of each project file, propagate upstream failure, permit upstream template metadata changes and exercise the exact workflow invocation. |
| LC-005 | template, caller, project guide and policy | Source review of event selection, immutable reference pairs, job permissions and validation-only concurrency; actionlint and offline zizmor. |
| LC-006 | reusable actionlint | Source review of pinned archive checksum, blocking policy and disabled credential persistence; native lint/audit. |
| LC-007 | reusable Fish | Source review of NUL-delimited tracked selection and per-file `--no-execute`; existing source-lint specification owns consumer acceptance. No live shell customization. |
| LC-008 | reusable labeler | Source review of pinned metadata-only action, caller token, sync-label policy and permissions; workflow lint. No synthetic public labels were applied. |
| LC-009 / FR-005 | assignment workflow and original feature spec | Existing API fixtures cover author classes, open/current state, pagination, additive assignment, invalid events and rejected writes. |
| LC-010 / FR-003 | selector, Node lint driver and original feature spec | Existing selector tests plus real valid/invalid Python, shell, JavaScript, CSS and Markdown smoke fixtures. |
| LC-011 | CI, hooks, development adapters | Native full development check; five adapter fixtures; separate development specification retains platform limitations. |
| LC-012 | community files and release playbook | Complete source review of issue/PR inputs, reporting guidance, delivery and recovery boundaries. |

`bash scripts/check-development.sh` passed: native hooks/integration checks,
Python tests, workflow lint/security audit, maintained-source lint and all five
real-tool acceptance/rejection pairs. After adding explicit bootstrap and workflow
wiring cases, the full Python suite passed 34 tests without skips. The new update
and validator rejection cases failed before their fixes. Separate self-review
inspected the full source diff, caller compatibility, source-to-contract mapping,
and failure propagation. No product implementation is inferred from installation
validation, and no live update, label or assignment was triggered for test purposes.

Adoption requires consumers to pin both the reusable workflow and tooling helper
to the same merged revision. Existing immutable callers retain their inputs,
outputs and permissions. Exact-head PR, representative caller, main and consumer
pin-delivery results remain recorded in their delivery PRs.
