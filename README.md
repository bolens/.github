# Shared GitHub configuration

This repository contains default community health files and reusable GitHub
Actions workflows for repositories owned by `bolens`.

Reusable workflows are intentionally small and composable. Individual
repositories retain their project-specific build, test, and release logic.

## Reusable workflows

- `reusable-actionlint.yml`: validates workflow syntax and can enforce the centrally pinned, offline, blocking zizmor policy for callers that enable `security-audit`.
- `reusable-fish.yml`: syntax-checks tracked Fish shell files.
- `reusable-pr-labeler.yml`: labels pull requests from repository-owned path
  rules without checking out pull-request code.

Call reusable workflows by an immutable release tag once the repository begins
publishing baseline releases. Pilot repositories temporarily follow `main` so
the interface can settle.

### Git hooks

Run `bash scripts/install-git-hooks` once per clone. The pre-commit hook runs fast staged checks; pre-push runs the broader local CI gate.
