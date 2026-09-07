# Shared GitHub configuration

[Documentation](docs/README.md)

This repository contains default community health files and reusable GitHub
Actions workflows for repositories owned by `bolens`.

Reusable workflows are intentionally small and composable. Individual
repositories retain their project-specific build, test, and release logic.

## Reusable workflows

- `reusable-actionlint.yml`: validates workflow syntax and can enforce the centrally pinned, offline, blocking zizmor policy for callers that enable `security-audit`.
- `reusable-fish.yml`: syntax-checks tracked Fish shell files.
- `reusable-pr-labeler.yml`: labels pull requests from repository-owned path
  rules without checking out pull-request code.
- `reusable-auto-assign.yml`: assigns the maintainer to open issues and pull requests.
- `reusable-source-lint.yml`: checks configured tracked source with fleet lint rules.
- `reusable-spec-kit.yml`: validates repository-managed Spec Kit files.
- `reusable-spec-kit-update.yml`: opens pinned upstream update pull requests.

Call reusable workflows by a full immutable commit SHA. Where a workflow accepts
`tooling-ref`, pass that same SHA. Roll updated pins out through reviewed consumer
PRs after verifying the shared change.

## Development tooling

See [development environments](docs/development-environments.md) for the locked toolchain and local container adapters.

## License scope and attribution

See [third-party notices](THIRD_PARTY_NOTICES.md) for the project license scope,
retained upstream notices, and dependency or asset exceptions.
