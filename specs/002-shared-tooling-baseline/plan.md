# Plan: Shared workflow and Spec Kit integration contracts

The [specification](spec.md) preserves existing behavior. Use the project guide
and constitution for implementation constraints. Keep upstream-managed templates,
helpers, and integration manifests unchanged.

## Source ownership

- `scripts/bootstrap-spec-kit`
- `scripts/validate-spec-kit.py`
- `scripts/lint-source.py`
- `templates`
- `.github/workflows`
- `tests`

## Constitution check

Preserve canonical source ownership, compatibility, bounded inputs, and native validation. This baseline changes project-owned documentation without altering managed integration files or applying live operations.

## Validation

```sh
bash .githooks/pre-push
```

Run checks in an isolated checkout. Commands are instructions, not evidence of
a pass. Record results in `coverage.md`, keep incomplete work in `tasks.md`, and
follow `RELEASING.md` for reviewed delivery. No live operation is required solely
to create this retrospective baseline.

## 2026-09-06 corrective extension

The detailed legacy contracts expose missing immutable-input checks and incomplete
project-memory preservation. Add rejection tests before implementing the workflow
guards and isolated regeneration helper. Add malformed-metadata and escaped-path
fixtures for the installation validator. Validate all included local consumers
with the candidate validator; existing version defaults and workflow inputs remain
unchanged. Exercise the reusable validation workflow as a repository-local CI caller.
Updater tests use a fake upstream command and must never open live fixture PRs.
Consumers adopt the merged workflow/helper pair together through immutable pins.
