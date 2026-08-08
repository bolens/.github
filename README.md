# Shared GitHub configuration

This repository contains default community health files and reusable GitHub
Actions workflows for repositories owned by `bolens`.

Reusable workflows are intentionally small and composable. Individual
repositories retain their project-specific build, test, and release logic.

## Reusable workflows

- `reusable-actionlint.yml`: validates GitHub Actions workflow syntax.
- `reusable-fish.yml`: syntax-checks tracked Fish shell files.

Call reusable workflows by an immutable release tag once the repository begins
publishing baseline releases. Pilot repositories temporarily follow `main` so
the interface can settle.
